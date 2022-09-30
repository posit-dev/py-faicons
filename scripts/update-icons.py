#! /usr/bin/env python3

from pathlib import Path
from urllib.request import urlretrieve
import json

version = "6.2.0"
tempfile = Path(__file__).parent.parent / "faicons/icons.json.tmp"
destfile = Path(__file__).parent.parent / "faicons/icons.json"

if tempfile.exists():
    tempfile.unlink()

urlretrieve(
    f"https://raw.githubusercontent.com/FortAwesome/Font-Awesome/{version}/metadata/icons.json",
    tempfile,
)

# Read in the JSON, then write it out, so that the result is minified.
with open(tempfile) as f:
    icon_data = json.load(f)

tempfile.unlink()


if destfile.exists():
    destfile.unlink()

with open(destfile, "w") as f:
    json.dump(icon_data, f)
