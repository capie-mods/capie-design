# Documentation sites

Two static sites built with [Zensical](https://zensical.org/), the site generator from the team
behind Material for MkDocs:

| Folder | Site | Audience |
|---|---|---|
| `capie/` | CAPIE (Cyprian's API Extender) | Players who want to know if CAPIE is safe, and modders |
| `rename-anything/` | Rename Anything | Players of the mod |
| `shared/` | Theme, marks, diagrams and the Paradox script lexer used by both | Maintainers |

Nothing here is deployed yet. The sites are not published on GitHub Pages.

Websites: [Rename Anything](https://capie-mods.github.io/rename-anything/) and [CAPIE](https://capie-mods.github.io/capie/).

## Build and preview

Zensical and the local lexer are in the `docs` dependency group of the root `pyproject.toml`
(installed by `uv sync`, like the other default groups).

```powershell
uv sync
uv run python sites/shared/sync_shared.py              # copy the shared theme into both sites
uv run python sites/shared/zensical_overrides.py       # Zensical assets without layout transitions
uv run zensical build -f sites/capie/zensical.toml --clean --strict
uv run zensical build -f sites/rename-anything/zensical.toml --clean --strict
uv run zensical serve -f sites/capie/zensical.toml     # live preview on http://localhost:8000
```

`--strict` turns every warning (for example a broken link or anchor) into a failed build. Output
goes to `sites/<site>/site/`, the build cache to `sites/<site>/.cache/`; both are gitignored.

## Shared theme

`shared/theme/` is the one source for both sites:

- `stylesheets/tokens.css`: generated from `docs/design/tokens.json` as `--capie-*` custom
  properties. Do not edit it; edit the tokens and run `sync_shared.py`.
- `stylesheets/theme.css`: maps the tokens onto Zensical's variables for the dark scheme (game
  panels) and the light scheme. The light scheme uses a field grey mixed from steel-bevel and
  ink; those shades are derived, and the file marks them as such. It also defines the status marks (`<span class="st st-today">Works today</span>`,
  `st-progress`, `st-planned`, `st-not`), the `proposed` admonition and the
  `<span class="proposed-tag">Proposed, subject to change</span>` tag.
- `marks/`: the CAPIE connector and the Rename Anything pencil as SVG (logo and favicon), plus
  the warning glyph.
- `diagrams/`: SVG diagrams in the design system's style. `architecture.svg` and
  `launch-chain.svg` are the same files as the README diagrams in `docs/assets/readme/`; change
  both together. Animations are CSS only, run only under
  `prefers-reduced-motion: no-preference`, and move only along flows that work today; structure
  diagrams and planned flows stay still, as `docs/design/DESIGN-SYSTEM.md` requires.

`sync_shared.py` copies `shared/theme/` into `<site>/docs/assets/shared/` of each site, so each
site folder builds on its own and can move to its own repository unchanged. Run it after every
change to the theme or the tokens; `--check` only reports drift (exit code 1) and suits CI.

Diagrams that belong to one site live in that site (`rename-anything/docs/assets/diagrams/`).

## Zensical override

Zensical's bundled stylesheets and script animate layout properties (`max-height`, `width`,
`height`) for the navigation, the language and version menus, the drawer overlay, the content
tab indicator and two script components. The design system does not allow that, and the
impeccable detector reports it even when `theme.css` overrides it in the cascade, because the
original rules still ship. `shared/zensical_overrides.py` fixes it with as little change as
possible: it copies only the
three affected vendor files from the installed Zensical, removes the layout entries from their
`transition` declarations (nothing else), and writes them to `<site>/overrides/`, which both
`zensical.toml` files use as `custom_dir`. The folder is generated and gitignored; run the script
before every build (the Pages templates do).

When Zensical is upgraded, the asset names change (they carry a content hash) and the script
stops with "missing in Zensical ...". Then:

1. Find the new files under `.venv/Lib/site-packages/zensical/templates/assets/` that contain
   `transition` with `max-height`, `width` or `height`, and put their paths in `VENDOR_FILES`.
2. Run the script and read its diff against the vendor files: only `transition` values may change.
3. Check that the replacements in `theme/stylesheets/theme.css` ("Motion" and "Page chrome") still
   match the new components, build with `--strict`, and run the detector again.

## Syntax highlighting

Zensical highlights code with Pygments through `pymdownx.highlight`. PowerShell, C++, JSON and
YAML have stock lexers. HOI4 script (Paradox's Clausewitz format) has none, and the nearest stock
lexers either colour nothing (`text`) or break on its blocks (`yaml`). So
`shared/pygments-paradox/` is a small local package with two lexers, registered through the
`pygments.lexers` entry point:

| Fence | For |
|---|---|
| `paradox` (also `clausewitz`, `hoi4`, `pdx`) | Script and `.gui` files |
| `paradox-loc` (also `hoi4-loc`) | Localisation `.yml` with `§` colours, `$KEY$` and `[Scope.GetName]` |

Names with the reserved `capie_` prefix are coloured like functions, so readers can see which
names belong to CAPIE. The package is installed as an editable path dependency of the `docs`
group; nothing is published. Check it with:

```powershell
uv run python -c "from pygments.lexers import get_lexer_by_name; print(get_lexer_by_name('paradox'))"
```

Its Python code is linted like the rest of the repository (`uv run ruff check`,
`uv run ruff format --check`, `uv run ty check`,
`uv run python tools/check_constant_docstrings.py`).

## Deploying later

Each site has a GitHub Actions template, `deploy-pages.yml.example`. It is not active. To publish:

1. Copy it to `.github/workflows/` of the repository that hosts the site.
2. Set `site_url` in that site's `zensical.toml` (today a placeholder on `example.invalid`).
3. In the repository settings choose Pages, Source: GitHub Actions.

When the repositories are split, move `capie/` together with a copy of `shared/` (theme and lexer)
into the CAPIE repository, drop the `sites/capie/` prefixes from the template, and give that
repository a `pyproject.toml` with the `docs` group. The same applies to `rename-anything/`.

## Writing rules

- Never present a planned feature as working. Use the four status marks and the words "Works
  today", "In progress", "Planned", "Not supported".
- Label every code sample that is not implemented with the proposed tag and a `# PROPOSED`
  comment.
- The DLLs and the injector are `capie_*`. The launcher (`RenameAnythingLauncher.exe`) and the
  install folder still carry the old name; say so where those names appear.
- English, plain sentences, straight quotes, no dashes as punctuation, sentence-case headings
  (the voice rules in `docs/design/DESIGN-SYSTEM.md`).
- Player pages of Rename Anything exist in English and Polish (`rename-anything/docs/pl/`). Change
  both in the same edit; the Polish pages use the in-game Polish labels from
  `mod/localisation/polish/` and Polish quotation marks.
- Use the status legend (`<ul class="st-legend">`) once on a page that relies on the marks.
