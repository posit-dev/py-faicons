
# Font Awesome for Shiny

An interface to [Font-Awesome](https://fontawesome.com/) for use in Shiny for Python.

This package currently uses Font-Awesome 6.2.0.

## Installation

```python
pip install faicons
```

## Usage

Use `icon_svg()` to get an `<svg>` representation of the icon.

```python
from faicons import icon_svg
icon_svg("play")
```

Example usage in Shiny:

```python
from shiny import ui
ui.input_action_button("btn", "Press me", icon=icon_svg("play")).show()
```
