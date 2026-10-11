# pygments-paradox-script

Two small Pygments lexers for the documentation sites in `sites/`:

| Fence name | Aliases | For |
|---|---|---|
| `paradox` | `clausewitz`, `hoi4`, `pdx` | HOI4 script: scripted effects, triggers, scripted GUIs, `.gui` files |
| `paradox-loc` | `hoi4-loc` | HOI4 localisation `.yml` files with `§` colour codes, `$KEY$` and `[Scope.GetName]` |

Pygments has no lexer for Paradox's Clausewitz script. The closest stock lexers
(`text`, `yaml`, `ruby`) either colour nothing or colour the wrong things:
`yaml` breaks on `{ }` blocks and `#` inside strings. So this package registers
its own lexers through the `pygments.lexers` entry point, and every tool that
asks Pygments for a lexer by name (Zensical through `pymdownx.highlight`,
MkDocs, Sphinx) finds them once the package is installed.

It is not published. The repository's `pyproject.toml` installs it as an
editable path dependency of the `docs` dependency group. Names with the reserved
`capie_` prefix are coloured as functions on purpose, so readers can see which
names belong to CAPIE.

Check it by hand:

```powershell
uv run python -c "from pygments.lexers import get_lexer_by_name; print(get_lexer_by_name('paradox'))"
```
