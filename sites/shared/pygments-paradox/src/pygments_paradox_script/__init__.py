"""Pygments lexers for Paradox (Clausewitz) script and localisation files.

Hearts of Iron IV, like other Paradox games, uses one block syntax for scripted
effects, triggers, scripted GUIs and ``.gui`` interface files: ``key = value``
pairs, ``{ ... }`` blocks, ``#`` comments, ``yes``/``no`` booleans and dotted
dates. Localisation files are YAML-like (``l_english:`` then ``KEY: "text"``)
with the game's own markup inside the strings: ``§R...§!`` colour codes,
``$KEY$`` nesting and ``[Scope.GetName]`` script calls.

Pygments ships no lexer for either format. This package adds two, registered
through the ``pygments.lexers`` entry-point group:

* ``paradox`` (aliases ``clausewitz``, ``hoi4``, ``pdx``): script and ``.gui``.
* ``paradox-loc`` (alias ``hoi4-loc``): localisation ``.yml``.

The lexers only colour text; they do not validate it. Identifiers that start
with ``capie_`` are marked as functions because the prefix is reserved for the
CAPIE script SDK, which the documentation wants to make visible.
"""

from __future__ import annotations

from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Whitespace,
)

__all__ = ["ParadoxLocalisationLexer", "ParadoxScriptLexer"]

CONTROL_KEYWORDS = (
    "if",
    "else_if",
    "else",
    "limit",
    "NOT",
    "AND",
    "OR",
    "count_triggers",
    "hidden_effect",
    "hidden_trigger",
    "custom_effect_tooltip",
    "custom_trigger_tooltip",
    "meta_effect",
    "meta_trigger",
    "while_loop_effect",
    "for_loop_effect",
    "for_each_loop",
    "for_each_scope_loop",
    "random_list",
    "break",
)
"""Flow-control and logic keywords, coloured as language keywords."""

SCOPE_KEYWORDS = (
    "ROOT",
    "FROM",
    "PREV",
    "THIS",
    "OWNER",
    "CONTROLLER",
    "CAPITAL",
    "OVERLORD",
    "FACTION_LEADER",
)
"""Built-in scope names, coloured as pseudo built-ins."""

BLOCK_TYPES = (
    "scripted_gui",
    "containerWindowType",
    "windowType",
    "buttonType",
    "iconType",
    "instantTextBoxType",
    "textBoxType",
    "editBoxType",
    "guiTypes",
    "spriteTypes",
    "spriteType",
)
"""Top-level block and GUI element types, coloured as declarations."""

IDENTIFIER = r"[A-Za-z_@][\w.@-]*"
"""Regular expression for a bare script identifier, including dotted event ids."""

CAPIE_IDENTIFIER = r"capie_\w*"
"""Regular expression for names under the reserved ``capie_`` prefix."""


class ParadoxScriptLexer(RegexLexer):
    """Lexer for Paradox (Clausewitz) script and interface files.

    It covers the subset of the syntax that appears in HOI4 mods: comments,
    ``key = value`` pairs with the comparison operators the game accepts,
    nested blocks, quoted strings with localisation markup, numbers, dotted
    dates, ``yes``/``no``, scope prefixes such as ``temp_var:capie_cap`` and
    ``@constants``.
    """

    name = "Paradox script"
    aliases = (
        "paradox",
        "clausewitz",
        "hoi4",
        "pdx",
    )
    filenames = (
        "*.gui",
        "*.gfx",
    )
    mimetypes = ("text/x-paradox-script",)
    url = "https://hearts-of-iron-4.fandom.com/wiki/Modding"

    tokens = {  # noqa: RUF012 - Pygments reads this dict once, in its metaclass.
        "root": [
            (r"\s+", Whitespace),
            (r"#.*?$", Comment.Single),
            (r'"', String.Double, "string"),
            (r"[{}]", Punctuation),
            (r"[<>!?]?=|[<>]", Operator),
            (r"-?\d+\.\d+\.\d+(?:\.\d+)?\b", Number.Other),
            (r"-?\d+\.\d+", Number.Float),
            (r"-?\d+\b", Number.Integer),
            (words(("yes", "no"), suffix=r"\b"), Keyword.Constant),
            (words(CONTROL_KEYWORDS, prefix=r"\b", suffix=r"\b"), Keyword),
            (words(SCOPE_KEYWORDS, prefix=r"\b", suffix=r"\b"), Name.Builtin.Pseudo),
            (words(BLOCK_TYPES, prefix=r"\b", suffix=r"\b"), Keyword.Declaration),
            (
                r"(\w+)(:)(" + CAPIE_IDENTIFIER + r")",
                bygroups(Name.Namespace, Punctuation, Name.Function),
            ),
            (
                r"(\w+)(:)(" + IDENTIFIER + r")",
                bygroups(Name.Namespace, Punctuation, Name.Variable),
            ),
            (CAPIE_IDENTIFIER, Name.Function),
            (r"@\w+", Name.Constant),
            (r"\b[A-Z]{3}\b", Name.Constant),
            (r"(" + IDENTIFIER + r")(\s*)(?=[<>!?]?=|[<>])", bygroups(Name.Attribute, Whitespace)),
            (IDENTIFIER, Name),
            (r".", Text),
        ],
        "string": [
            (r'"', String.Double, "#pop"),
            include("markup"),
            (r'[^"\\§$\[£]+', String.Double),
            (r".", String.Double),
        ],
        "markup": [
            (r"\\.", String.Escape),
            (r"§[A-Za-z!]", String.Escape),
            (r"\$[^$\s\"]+\$", String.Interpol),
            (r"\[[^\]\"]+\]", String.Interpol),
            (r"£[\w|]+", String.Symbol),
        ],
    }
    """Lexer states: ``root`` for script, ``string`` and ``markup`` for quoted text."""


class ParadoxLocalisationLexer(RegexLexer):
    """Lexer for Paradox localisation files (``l_<language>:`` YAML-like format).

    It colours the language header, keys with their optional version number,
    comments, and the in-string markup the game evaluates: ``§`` colour codes,
    ``$KEY$`` nesting, ``[Scope.Function]`` calls and ``£icon`` text icons.
    """

    name = "Paradox localisation"
    aliases = (
        "paradox-loc",
        "hoi4-loc",
    )
    filenames = ()
    mimetypes = ("text/x-paradox-localisation",)
    url = "https://hearts-of-iron-4.fandom.com/wiki/Localisation"

    tokens = {  # noqa: RUF012 - Pygments reads this dict once, in its metaclass.
        "root": [
            (r"\s+", Whitespace),
            (r"#.*?$", Comment.Single),
            (r"(l_\w+)(:)", bygroups(Keyword.Namespace, Punctuation)),
            (
                r"((?i:capie_)\w*)(:)(\d*)",
                bygroups(Name.Function, Punctuation, Number.Integer),
            ),
            (r"([\w.-]+)(:)(\d*)", bygroups(Name.Attribute, Punctuation, Number.Integer)),
            (r'"', String.Double, "string"),
            (r".", Text),
        ],
        "string": [
            (r'"(?=\s*(?:#.*)?$)', String.Double, "#pop"),
            include("markup"),
            (r'[^"\\§$\[£\n]+', String.Double),
            (r"\n", String.Double, "#pop"),
            (r".", String.Double),
        ],
        "markup": ParadoxScriptLexer.tokens["markup"],
    }
    """Lexer states: ``root`` for keys, ``string`` and ``markup`` for values."""
