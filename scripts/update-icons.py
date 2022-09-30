#! /usr/bin/env python3

import os
from urllib.request import urlretrieve

version = "6.2.0"
urlretrieve(
    f"https://raw.githubusercontent.com/FortAwesome/Font-Awesome/{version}/metadata/icons.json",
    os.path.join(os.path.dirname(__file__), "../faicons/icons.json"),
)
