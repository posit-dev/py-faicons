
# Font Awesome for PyShiny

An interface to Font Awesome for use in PyShiny

## Usage

Use `icon_svg()` to get an `<svg>` representation of any Font Awesome 5 icon.

```python
from fontawesome import icon_svg
icon_svg("play")
```

And use it with PyShiny 

```python
from shiny import *
input_button("btn", "Press me", icon_svg("play")).show()
```



First clone the [py-htmltools](https://github.com/rstudio/py-htmltools) repository and install the package:

```sh
git clone https://github.com/rstudio/py-htmltools.git
cd py-htmltools
pip install -r requirements.txt
make install
```

Then do the same for [py-fontawesome]

```sh
git clone https://github.com/rstudio/py-fontawesome.git
cd py-fontawesome
make install
```
