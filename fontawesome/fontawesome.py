import json
import re
from os.path import join, dirname
from htmltools import HTML
from htmltools.util import _html_escape
from typing import Dict, Literal, Optional, Union

__all__ = ("fa")

with open(join(dirname(__file__), 'icons.json')) as f:
    _ICONS = json.load(f)

def fa(name: str, 
       style: Optional[str] = None,
       fill: Optional[str] = None,
       fill_opacity: Optional[str] = None,
       stroke: Optional[str] = None,
       stroke_width: Optional[str] = None,
       stroke_opacity: Optional[str] = None,
       height: Optional[str] = None,
       width: Optional[str] = None,
       margin_left: Optional[str] = None,
       margin_right: Optional[str] = None,
       position: Optional[str] = None,
       title: Optional[str] = None,
       a11y: Literal["deco", "sem", "none"] = "deco") -> HTML:

    icon = _ICONS.get(name)
    if icon is None:
      raise ValueError(f"Icon {name} not found.")

    styles = icon["styles"]
    style = styles[0] if style is None else style
    if style not in styles:
      raise ValueError(f"Style {style} not found for {name} icon. Posible styles are: {styles}")

    svg = icon["svg"][style]
    
    # Validate height/width and populate sensible defaults
    h = _parse_length_unit(height)
    w = _parse_length_unit(width)
    if height is None and width is None:
      height = "1em"
      width = str(round(svg["width"] / 512, 2)) + "em"
    elif width is None:
      width = str(round((svg["width"] / 512) * h.value, 2)) + h.unit
    elif height is None:
      height = str(round(w.value / (svg["width"] / 512), 2)) + w.unit

    par_attr = 'preserveAspectRatio="none" ' if height is not None and width is not None else ''

    a11y_attr = ""
    if a11y == "deco":
      a11y_attr = 'aria-hidden="true" role="img" '
    elif a11y == "sem":
      title = icon["label"] if title is None else title
      a11y_attr = f'aria-label="{_html_escape(title, attr = True)}" role="img" '

    styles = [
      'height:' + height,
      'width:' + width,
      'vertical-align:-0.125em',
      'margin-left:' + "auto" if margin_left is None else margin_left,
      'margin-right:' + "auto" if margin_right is None else margin_right,
      'font-size:inherit',
      'fill:' + "currentColor" if fill is None else fill,
      'overflow:visible',
      'position:' + "relative" if position is None else position
    ]

    if fill_opacity is not None:
      styles.append('fill-opacity:' + fill_opacity)
    if stroke is not None:
      styles.append('stroke:' + stroke)
    if stroke_width is not None:
      styles.append('stroke-width:' + stroke_width)
    if stroke_opacity is not None:
      styles.append('stroke-opacity:' + stroke_opacity)

    style = ";".join(styles)

    return HTML(
    f"""<svg {par_attr}{a11y_attr}viewBox="0 0 {width} {height}" style="{style}">
      {'<title>{_html_escape(title)}</title>' if title is not None else ''}
      <path d="{svg['path']}"/>
    </svg>
    """
    )

def _parse_length_unit(x: str) -> Dict[str, Union[str, float]]:
  if x is None:
    return None

  if not re.search("^^[0-9]*\\.?[0-9]+[a-z]+$", x):
    raise ValueError("Values provided to `height` and `width` must have a numerical value followed by a CSS length unit.")

  unit = re.sub("[0-9\\.]+?", "", x)

  if unit not in _css_length_units:
    raise ValueError(f"{unit} is not a valid CSS length unit.")

  value = float(re.sub("[a-z]+$", "", x))
  
  return dict(value=value, unit=unit)


_css_length_units = [
    "cm", "mm", "in", "px", "pt", "pc", "em", "ex",
    "ch", "rem", "vw", "vh", "vmin", "vmax", "%"
]
