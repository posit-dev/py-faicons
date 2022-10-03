#!/usr/bin/env python

"""Tests for `faicons` package."""

import pytest
import faicons


def test_icon_svg():
    # Try with canonical name
    icon_magnifying_glass = faicons.icon_svg("magnifying-glass")
    assert str(icon_magnifying_glass).startswith("<svg ")

    # Try with alias
    icon_search = faicons.icon_svg("search")

    assert str(icon_magnifying_glass) == str(icon_search)

    with pytest.raises(ValueError, match="^Icon ninja-shark not found\\.$"):
        faicons.icon_svg("ninja-shark")

    with pytest.raises(ValueError, match="^Style brand not found"):
        faicons.icon_svg("magnifying-glass", style="brand")
