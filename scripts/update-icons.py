import os
from urllib.request import urlretrieve
version = "5.15.4"
urlretrieve(
    f"https://raw.githubusercontent.com/FortAwesome/Font-Awesome/{version}/metadata/icons.json", 
    os.path.join(os.path.dirname(__file__), "../fontawesome/icons.json")
)