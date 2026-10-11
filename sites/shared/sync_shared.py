#!/usr/bin/env python3
"""Generate the shared token stylesheet and copy the shared theme into each site.

The two documentation sites (``sites/capie`` and ``sites/rename-anything``)
must each build on their own, so that either folder can later move to its own
repository unchanged. They therefore carry a copy of the shared theme inside
their ``docs/assets/shared/`` folder instead of referencing ``sites/shared``.

This script keeps those copies honest:

1. It reads the design tokens (``docs/design/tokens.json``) and writes
   ``sites/shared/theme/stylesheets/tokens.css``, one CSS custom property per
   colour, font, spacing and motion token.
2. It copies every file under ``sites/shared/theme/`` into each site's
   ``docs/assets/shared/`` folder and removes files there that no longer exist
   in the source.

With ``--check`` nothing is written. The script exits with 1 and lists every
file that is missing, stale or extra, which makes it usable as a CI step.
When the tokens file is absent (for example after the repositories are split)
the existing ``tokens.css`` is kept and only the copy step runs.

Usage::

    uv run python sites/shared/sync_shared.py [--check]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parent
"""The ``sites/shared`` folder that holds the canonical theme."""

THEME = SHARED / "theme"
"""Source folder whose contents are copied into every site."""

TOKENS_JSON = SHARED.parent.parent / "docs" / "design" / "tokens.json"
"""Design tokens, the single source of colours, fonts, spacing and motion."""

TOKENS_CSS = THEME / "stylesheets" / "tokens.css"
"""Generated stylesheet with the tokens as CSS custom properties."""

SITES = ("capie", "rename-anything")
"""Site folders under ``sites/`` that receive a copy of the theme."""

TARGET = Path("docs") / "assets" / "shared"
"""Destination of the copy, relative to each site folder."""

PREFIX = "--capie-"
"""Prefix of every generated custom property; one namespace for both products."""


def css_value(token: dict[str, object]) -> str:
    """Turn one W3C design token into a CSS value.

    Args:
        token: A token object with ``$type`` and ``$value``.

    Returns:
        The value as CSS text: cubic-bezier lists become ``cubic-bezier()``,
        millisecond durations stay as they are, everything else is used as-is.
    """
    value = token["$value"]
    if token.get("$type") == "cubicBezier" and isinstance(value, list):
        return "cubic-bezier(" + ", ".join(str(part) for part in value) + ")"
    return str(value)


def subtree(tokens: dict[str, object], *path: str) -> dict[str, object]:
    """Follow ``path`` through nested token groups.

    Args:
        tokens: The parsed ``tokens.json`` document.
        *path: Group names, outermost first.

    Returns:
        The group found at ``path``, or an empty dict when any step is missing
        or is not a group.
    """
    node: object = tokens
    for key in path:
        node = node.get(key, {}) if isinstance(node, dict) else {}
    if not isinstance(node, dict):
        return {}
    return {str(key): value for key, value in node.items()}


def declarations(group: dict[str, object], prefix: str, types: set[str] | None) -> list[str]:
    """Turn the tokens of one group into CSS declarations.

    Args:
        group: Token group mapping names to token objects.
        prefix: Text placed between ``PREFIX`` and the token name.
        types: Accepted ``$type`` values, or None to accept every token.

    Returns:
        One ``--capie-<prefix><name>: <value>;`` line per accepted token.
    """
    return [
        f"{PREFIX}{prefix}{name}: {css_value(token)};"
        for name, token in group.items()
        if isinstance(token, dict)
        and "$value" in token
        and (types is None or token.get("$type") in types)
    ]


def token_lines(tokens: dict[str, object]) -> list[str]:
    """Collect ``name: value;`` declarations from the token tree.

    Colours use their own names (``--capie-brass``), web fonts become
    ``--capie-font-sans`` and friends, web sizes ``--capie-space-3`` and so on,
    motion tokens ``--capie-motion-ease-settle``.

    Args:
        tokens: The parsed ``tokens.json`` document.

    Returns:
        Declarations in a stable order, without indentation.
    """
    lines: list[str] = []
    for group in subtree(tokens, "color").values():
        if isinstance(group, dict):
            lines.extend(declarations(group, "", None))
    lines.extend(declarations(subtree(tokens, "font", "web"), "font-", None))
    lines.extend(declarations(subtree(tokens, "size", "web"), "", {"dimension"}))
    lines.extend(declarations(subtree(tokens, "motion"), "motion-", {"cubicBezier", "duration"}))
    return lines


def render_tokens_css(tokens: dict[str, object]) -> str:
    """Render the complete ``tokens.css`` file.

    Args:
        tokens: The parsed ``tokens.json`` document.

    Returns:
        The stylesheet text, ending with a newline.
    """
    meta = tokens.get("meta", {})
    version = meta.get("version", "unknown") if isinstance(meta, dict) else "unknown"
    body = "\n".join(f"  {line}" for line in token_lines(tokens))
    return (
        "/* GENERATED by sites/shared/sync_shared.py from docs/design/tokens.json"
        f" v{version}. Do not edit; edit the tokens and run the script. */\n"
        f":root {{\n{body}\n}}\n"
    )


def planned_files() -> dict[Path, bytes]:
    """Map every destination file of every site to the bytes it must contain.

    Returns:
        Absolute destination paths and their expected content.
    """
    plan: dict[Path, bytes] = {}
    sources = sorted(path for path in THEME.rglob("*") if path.is_file())
    for site in SITES:
        root = SHARED.parent / site / TARGET
        for source in sources:
            plan[root / source.relative_to(THEME)] = source.read_bytes()
    return plan


def extra_files(plan: dict[Path, bytes]) -> list[Path]:
    """List files inside the site copies that the source no longer has.

    Args:
        plan: Result of :func:`planned_files`.

    Returns:
        Paths that exist in a site's ``docs/assets/shared`` but not in the plan.
    """
    extras: list[Path] = []
    for site in SITES:
        root = SHARED.parent / site / TARGET
        if root.is_dir():
            extras.extend(path for path in root.rglob("*") if path.is_file() and path not in plan)
    return sorted(extras)


def write_if_stale(path: Path, content: bytes, *, check: bool) -> list[str]:
    """Compare one file with its expected bytes and rewrite it unless checking.

    Args:
        path: File to compare and, outside ``--check`` mode, to write.
        content: The bytes the file must contain.
        check: When True, nothing is written.

    Returns:
        A one-item list naming the stale file, or an empty list when it matches.
    """
    if path.is_file() and path.read_bytes() == content:
        return []
    if not check:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return [f"stale: {path.relative_to(SHARED.parent)}"]


def sync_tokens(*, check: bool) -> list[str]:
    """Regenerate ``tokens.css`` from ``tokens.json`` when the tokens file exists.

    Args:
        check: When True, only compare.

    Returns:
        Problems found, as printable lines.
    """
    if not TOKENS_JSON.is_file():
        return []
    tokens = json.loads(TOKENS_JSON.read_text(encoding="utf-8"))
    return write_if_stale(TOKENS_CSS, render_tokens_css(tokens).encode("utf-8"), check=check)


def sync_copies(*, check: bool) -> list[str]:
    """Bring every site's copy of the theme in line with ``sites/shared/theme``.

    Args:
        check: When True, only compare.

    Returns:
        Problems found, as printable lines.
    """
    problems: list[str] = []
    plan = planned_files()
    for destination, content in plan.items():
        problems.extend(write_if_stale(destination, content, check=check))
    for extra in extra_files(plan):
        problems.append(f"extra: {extra.relative_to(SHARED.parent)}")
        if not check:
            extra.unlink()
    return problems


def main() -> int:
    """Run the generator and the copy, or only compare in ``--check`` mode.

    Returns:
        0 when everything is (or now is) in sync, 1 when ``--check`` found drift.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("--check", action="store_true", help="compare only, write nothing")
    args = parser.parse_args()

    problems = sync_tokens(check=args.check)
    problems.extend(sync_copies(check=args.check))
    for problem in problems:
        print(problem)
    if args.check:
        print(f"{len(problems)} file(s) out of sync" if problems else "shared theme in sync")
        return 1 if problems else 0
    print(f"updated {len(problems)} file(s)" if problems else "shared theme already in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
