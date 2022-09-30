
# Font Awesome for Shiny

An interface to Font Awesome for use in Shiny for Python.

## Installation

```python
pip install faicons
```

## Usage

Use `icon_svg()` to get an `<svg>` representation of any Font Awesome 5 icon.

```python
from faicons import icon_svg
icon_svg("play")
```

And use it with PyShiny

```python
from shiny import *
input_button("btn", "Press me", icon_svg("play")).show()
```
