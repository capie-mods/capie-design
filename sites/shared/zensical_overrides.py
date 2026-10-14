#!/usr/bin/env python3
"""Write each site's Zensical theme override: vendor assets without layout transitions.

Zensical's bundled stylesheets and script animate layout properties (``max-height``, ``width``
and ``height``): the navigation, the language and version menus, the drawer overlay, the content
tab indicator and two script components. The design system forbids animating layout
(``docs/design/DESIGN-SYSTEM.md``, motion rules), and ``sites/shared/theme/stylesheets/theme.css``
already gives every one of those components a replacement based on opacity, transform and
visibility. Overriding them in the cascade is not enough, because the original rules still ship.

This script is the smallest override that removes them. It reads the three vendor files from
the installed Zensical package, drops only the layout entries from each ``transition``
declaration, and writes the result under ``sites/<site>/overrides/`` with the same relative path
and file name. Both sites set ``custom_dir = "overrides"`` in ``zensical.toml``, so Zensical
serves these files in place of its own. Nothing else of the theme is copied or changed.

The output is a build product, like ``site/``, and is ignored by Git. Run the script before every
build. It refuses to write when a vendor file is missing or when it finds no layout transition in
a file that had some: both mean the Zensical version changed (the asset names carry a content
hash). Then compare the new vendor files, update ``VENDOR_FILES`` and check the replacements in
``theme.css`` (see ``sites/README.md``, "Zensical override").

Usage::

    uv run python sites/shared/zensical_overrides.py
"""

from __future__ import annotations

import re
import sys
from importlib import metadata, resources
from pathlib import Path

SHARED = Path(__file__).resolve().parent
"""The ``sites/shared`` folder."""

SITES = ("capie", "rename-anything")
"""Site folders under ``sites/`` that use the override."""

OVERRIDE_DIR = "overrides"
"""Folder inside each site that ``custom_dir`` in ``zensical.toml`` points at."""

VENDOR_FILES = (
    "assets/stylesheets/modern/main.e15858d4.min.css",
    "assets/stylesheets/classic/main.3d7537f3.min.css",
    "assets/javascripts/bundle.8b1c90bd.min.js",
)
"""Zensical 0.0.69 assets that contain layout transitions, relative to its templates folder."""

LAYOUT_PROPERTIES = frozenset({"max-height", "width", "height"})
"""Transition properties that animate layout; their entries are removed."""

TRANSITION = re.compile(r"transition:([^;}\"'`]*)")
"""A ``transition`` declaration value, inside CSS or inside a CSS string in the script."""


def split_top_level(value: str) -> list[str]:
    """Split a ``transition`` value at the commas that separate its entries.

    Args:
        value: The declaration value; commas inside parentheses (``cubic-bezier(...)``) stay.

    Returns:
        The entries, in order, with their original spacing.
    """
    entries: list[str] = []
    depth = 0
    start = 0
    for index, char in enumerate(value):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            entries.append(value[start:index])
            start = index + 1
    entries.append(value[start:])
    return entries


def strip_layout(value: str) -> str:
    """Remove the layout entries from one ``transition`` value.

    Args:
        value: The text after ``transition:``, for example ``max-height .25s,opacity .25s``.

    Returns:
        The value without entries whose property is in ``LAYOUT_PROPERTIES``; ``none`` when no
        entry is left. A value with no layout entry (including script code that only looks like
        a declaration) comes back unchanged, byte for byte.
    """
    entries = split_top_level(value)

    def is_layout(entry: str) -> bool:
        """Tell whether one entry animates a layout property.

        Args:
            entry: One comma-separated part of the value.

        Returns:
            True when its first word is a layout property.
        """
        words = entry.split()
        return bool(words) and words[0] in LAYOUT_PROPERTIES

    if not any(is_layout(entry) for entry in entries):
        return value
    kept = [entry for entry in entries if not is_layout(entry)]
    return ",".join(kept) if kept else "none"


def patch(text: str) -> tuple[str, int]:
    """Remove layout entries from every ``transition`` declaration of one file.

    Args:
        text: Content of a vendor stylesheet or script.

    Returns:
        The patched text and the number of declarations that changed.
    """
    changed = 0

    def replace(match: re.Match[str]) -> str:
        """Rewrite one declaration and count it when it changes.

        Args:
            match: A ``TRANSITION`` match.

        Returns:
            The rewritten declaration.
        """
        nonlocal changed
        value = match.group(1)
        new = strip_layout(value)
        if new != value:
            changed += 1
        return f"transition:{new}"

    return TRANSITION.sub(replace, text), changed


def main() -> int:
    """Write the patched vendor files into every site's override folder.

    Returns:
        0 on success, 1 when the installed Zensical does not match ``VENDOR_FILES``.
    """
    templates = resources.files("zensical") / "templates"
    version = metadata.version("zensical")
    for relative in VENDOR_FILES:
        source = templates.joinpath(*relative.split("/"))
        if not source.is_file():
            print(f"missing in Zensical {version}: {relative}; update VENDOR_FILES")
            return 1
        patched, changed = patch(source.read_bytes().decode("utf-8"))
        if not changed:
            print(f"no layout transition in {relative} (Zensical {version}); review the override")
            return 1
        for site in SITES:
            target = SHARED.parent / site / OVERRIDE_DIR / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(patched.encode("utf-8"))
        print(f"{relative}: {changed} transition(s) without layout properties")
    return 0


if __name__ == "__main__":
    sys.exit(main())
