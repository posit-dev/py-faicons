import json
import re
from os.path import join, dirname
from htmltools import tags, Tag, css

# TODO: make _html_escape public?
from htmltools._util import _html_escape
from typing import Dict, Literal, Optional, Union

__all__ = ("icon_svg", "metadata")

with open(join(dirname(__file__), "icons.json")) as f:
    _ICONS = json.load(f)


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
            f"Style {style} not found for {name} icon. Posible styles are: {styles}"
        )

    svg = icon["svg"][style]

    h = _parse_length_unit(height)
    w = _parse_length_unit(width)
    if height is None and width is None:
        height = "1em"
        width = str(round(svg["width"] / 512, 2)) + "em"
    elif width is None:
        width = str(round((svg["width"] / 512) * h.value, 2)) + h.unit
    elif height is None:
        height = str(round(w.value / (svg["width"] / 512), 2)) + w.unit

    svg_attrs = dict(viewBox=f"0 0 {svg['width']} 512")

    if height is not None and width is not None:
        svg_attrs["preserveAspectRatio"] = "none"

    if a11y == "deco":
        svg_attrs["aria-hidden"] = "true"
        svg_attrs["role"] = "img"
    elif a11y == "sem":
        title = icon["label"] if title is None else title
        svg_attrs["aria-label"] = _html_escape(title, attr=True)
        svg_attrs["role"] = "img"

    # N.B. this returns a tag object, not a string, because I don't think it's
    # possible for jsxTag() to handle HTML() attributes, which means nav() can't
    # support it out-of-the-box (if we really need this to be a string, we can
    # probably make nav()'s JSX component smarter)
    return tags.svg(
        None if title is None else tags.title(_html_escape(title)),
        Tag("path", d=svg["path"]),
        **svg_attrs,
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
            font_size="inherit",
            overflow="visible",
        ),
    )


def _parse_length_unit(x: str) -> Dict[str, Union[str, float]]:
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

    return dict(value=value, unit=unit)


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