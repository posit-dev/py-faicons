import json
import re
from os.path import dirname, join
from typing import Any, Dict, List, Literal, Optional, TypedDict, cast

from htmltools import Tag, css, html_escape, tags

__all__ = ("icon_svg", "metadata")


class IconDataSvg(TypedDict):
    last_modified: float
    raw: str
    viewBox: List[str]
    width: int
    height: int
    path: str


class IconData(TypedDict):
    # In practice, the keys appear to be "names" and "unicodes" but "names" is not
    # always present. For now, we'll just leave this as Dict[str, Any].
    aliases: Dict[str, Any]
    changes: List[str]
    ligatures: List[str]
    search: Dict[str, List[str]]
    styles: List[str]
    unicode: str
    label: str
    voted: bool
    # It looks like in practice, the only keys for `svg` are "solid" and "brands", and
    # it must contain exactly one of them, but it's not clear to me how to declare that
    # type, so we'll just use a Dict.
    svg: Dict[str, IconDataSvg]
    free: List[str]


with open(join(dirname(__file__), "icons.json")) as f:
    _ICONS = cast(Dict[str, IconData], json.load(f))


def metadata():
    """
    Get the metadata for all icons.

    Returns:
      A dictionary of icon metadata.

    Examples:

    """
    return _ICONS


def icon_svg(
    name: str,
    style: Optional[str] = None,
    fill: Optional[str] = "currentColor",
    fill_opacity: Optional[str] = None,
    stroke: Optional[str] = None,
    stroke_width: Optional[str] = None,
    stroke_opacity: Optional[str] = None,
    height: Optional[str] = None,
    width: Optional[str] = None,
    margin_left: Optional[str] = "auto",
    margin_right: Optional[str] = "0.2em",
    position: Optional[str] = "relative",
    title: Optional[str] = None,
    a11y: Literal["deco", "sem", "none"] = "deco",
) -> Tag:
    """
    Generate Font Awesome icons as SVGs

    Parameters:
      name: The icon's name (e.g., "play", "pause", etc).

      style: The FontAwesome style for the icon (e.g., "regular", "solid", etc).

      fill: The icon's fill color.

      fill_opacity: The icon's fill opacity (0.0 - 1.0).

      stroke: The icon's stroke color.

      stroke_width: The icon's stroke width.

      stroke_opacity: The icon's stroke opacity (0.0 - 1.0).

      height: The icon's height.

      width: The icon's width.

      margin_left: The icon's left margin.

      margin_right: The icon's right margin.

      position: The icon's position (e.g., "absolute", "relative", etc).

      title: A description of the icon to display on mouse hover.
      When `a11y == "sem"`, this description is also used as an aria-label
      (otherwise, the icon's inherent label is used for the aria-label).

      a11y: Either "deco" (decorative) or "sem" (semantic). Using "none" will
      result in no accessibility features for the icon.

    Returns:
      An HTML string containing the SVG of the icon.

    Raises:
      ValueError: If the icon name is not valid.
    """

    icon = _ICONS.get(name)
    if icon is None:
        raise ValueError(f"Icon {name} not found.")

    styles = icon["styles"]
    style = styles[0] if style is None else style
    if style not in styles:
        raise ValueError(
            f"Style {style} not found for {name} icon. Possible styles are: {styles}"
        )

    svg = icon["svg"][style]
    svg_width = float(svg["width"])

    h = _parse_length_unit(height)
    w = _parse_length_unit(width)
    if h is None and w is None:
        height = "1em"
        width = str(round(svg_width / 512, 2)) + "em"
    elif h is not None and w is None:
        width = str(round(svg_width / 512 * h["value"], 2)) + h["unit"]
    elif h is None and w is not None:
        height = str(round(w["value"] / (svg_width / 512), 2)) + w["unit"]

    svg_attrs = dict(viewBox=f"0 0 {svg['width']} 512")

    if height is not None and width is not None:
        svg_attrs["preserveAspectRatio"] = "none"

    if a11y == "deco":
        svg_attrs["aria-hidden"] = "true"
        svg_attrs["role"] = "img"
    elif a11y == "sem":
        title = icon["label"] if title is None else title
        svg_attrs["aria-label"] = html_escape(title, attr=True)
        svg_attrs["role"] = "img"

    # N.B. this returns a tag object, not a string, because I don't think it's possible
    # for jsxTag() to handle HTML() attributes, which means nav() can't support it
    # out-of-the-box (if we really need this to be a string, we can probably make
    # nav()'s JSX component smarter)
    return tags.svg(
        None if title is None else tags.title(html_escape(title)),
        Tag("path", d=svg["path"]),
        **svg_attrs,
        class_="fa",
        style=css(
            fill=fill,
            fill_opacity=fill_opacity,
            stroke=stroke,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
            height=height,
            width=width,
            margin_left=margin_left,
            margin_right=margin_right,
            position=position,
            vertical_align="-0.125em",
            overflow="visible",
        ),
    )


class ParsedUnit(TypedDict):
    value: float
    unit: str


def _parse_length_unit(x: Optional[str]) -> Optional[ParsedUnit]:
    if x is None:
        return None

    if not re.search("^^[0-9]*\\.?[0-9]+[a-z]+$", x):
        raise ValueError(
            "Values provided to `height` and `width` must have a numerical value followed by a CSS length unit."
        )

    unit = re.sub("[0-9\\.]+?", "", x)

    if unit not in _css_length_units:
        raise ValueError(f"{unit} is not a valid CSS length unit.")

    value = float(re.sub("[a-z]+$", "", x))

    return ParsedUnit(value=value, unit=unit)


_css_length_units = [
    "cm",
    "mm",
    "in",
    "px",
    "pt",
    "pc",
    "em",
    "ex",
    "ch",
    "rem",
    "vw",
    "vh",
    "vmin",
    "vmax",
    "%",
]
