---
name: CAPIE and Rename Anything
description: One design system for CAPIE (Cyprian's API Extender) and the mods built on it, starting with Rename Anything.
colors:
  window-ink: "#0f0e0d"
  field-ink: "#161412"
  panel-umber: "#272421"
  panel-rim: "#3c3936"
  steel-shadow: "#3c3b38"
  steel-bevel: "#76776b"
  olive-button: "#2e3627"
  olive-lit: "#424e38"
  pencil-green: "#406030"
  pencil-green-lit: "#507040"
  brass: "#d0a070"
  brass-dim: "#908060"
  parchment: "#ece6d3"
  khaki: "#c3b091"
  ash: "#a39a86"
  header-amber: "#ffbd00"
  go-green: "#7db35a"
  alarm-red: "#ff3232"
  caution-orange: "#ff7019"
  warning-rust: "#c64811"
typography:
  label-caps:
    fontFamily: "Ubuntu, 'Segoe UI', 'DejaVu Sans', Verdana, sans-serif"
    fontSize: "11.5px"
    fontWeight: 700
    letterSpacing: "0.14em"
  node-title:
    fontFamily: "Ubuntu, 'Segoe UI', 'DejaVu Sans', Verdana, sans-serif"
    fontSize: "15px"
    fontWeight: 700
    lineHeight: "18px"
  node-body:
    fontFamily: "Ubuntu, 'Segoe UI', 'DejaVu Sans', Verdana, sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: "18px"
  tag:
    fontFamily: "Ubuntu, 'Segoe UI', 'DejaVu Sans', Verdana, sans-serif"
    fontSize: "10px"
    fontWeight: 700
    letterSpacing: "0.08em"
  tooltip:
    fontFamily: "'EB Garamond', Garamond, Georgia, 'Times New Roman', serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: "17px"
rounded:
  node: "2px"
  panel: "6px"
spacing:
  space-1: "4px"
  space-2: "8px"
  space-3: "14px"
  space-4: "24px"
  space-5: "32px"
components:
  diagram-canvas:
    backgroundColor: "{colors.panel-umber}"
    rounded: "{rounded.panel}"
    width: "880px"
  diagram-node:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.parchment}"
    rounded: "{rounded.node}"
    padding: "14px"
  node-column:
    textColor: "{colors.parchment}"
    dividerColor: "{colors.panel-rim}"
  node-column-planned:
    textColor: "{colors.khaki}"
    dividerColor: "{colors.panel-rim}"
  badge-key:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.parchment}"
    rounded: "{rounded.node}"
    height: "22px"
  badge-value-today:
    backgroundColor: "{colors.olive-button}"
    textColor: "{colors.go-green}"
    height: "22px"
  game-pencil:
    size: "20px"
  game-field:
    backgroundColor: "{colors.field-ink}"
    textColor: "{colors.parchment}"
    width: "356px"
    height: "20px"
---

# Design System: CAPIE and Rename Anything

One system, one token file ([tokens.json](tokens.json)), one set of rules for type, motion,
iconography and voice. It serves two products that differ only in name and in one mark:

- **CAPIE (Cyprian's API Extender)**: a native library that extends what Hearts of Iron IV mods
  can do. It appears in the section for modders, on release pages, in the launcher and bootstrap
  CLI, and in two small in-game indicators.
- **Rename Anything**: the first mod built on CAPIE. It appears in the game's own panels as
  pencils and text fields.

This folder is self-contained. It references the game's files by their path inside a HOI4
installation, never by a path inside any of our repositories, so it can move to a shared design
repository unchanged. If this file and `tokens.json` disagree, the token file wins and this file
gets fixed.

Every colour was either copied from the game's text colour table (`interface/core.gfx`,
`textcolors`) or sampled read-only from vanilla textures of HOI4 1.19.3.0. No game asset is copied;
in game we reference vanilla sprites by name, and web surfaces draw their own shapes in the same
colours.

## Overview

**Creative North Star: "The Staff Annotation"**

A staff officer does not redesign the map. He writes a new name on it, in the margin, in the same
ink. Our UI adds a pencil and a text field to panels the player already knows, then gets out of
the way. Anything we add must look like it shipped with the game; the player should notice the new
name, not the tool that wrote it.

CAPIE is the same ink one level down: infrastructure that mods write with. It speaks only when it
has to (loaded, missing, wrong version) and otherwise stays out of sight.

On the web the rule holds too. Pages read as an extension of the game's panels: warm umber
backgrounds, olive buttons, steel bevels, khaki secondary text, a little amber for headings, brass
for the native layer. No neon, no gradients, no glow. Status is said in words and shown with a
simple, consistent mark.

The North Star was derived from the product design context (native, legible, discreet; edit in
place the way divisions, armies and fleets are renamed). It is a working name for that context,
not yet confirmed as the project's metaphor.

**Key Characteristics:**
- Edits happen in the panel that shows the object, next to its name.
- Vanilla sprites and fonts in game; web surfaces reuse the colours, not the files.
- Honest status everywhere: works today, in progress, planned, not supported.
- Quiet by default; motion only explains a sequence.

### Two names, one system

Both products use the same palette, type, spacing, marks, motion and voice. The only differences:

| | CAPIE | Rename Anything |
|---|---|---|
| Name on first mention | CAPIE (Cyprian's API Extender) | Rename Anything |
| Mark (app and release icon only) | Three-slot connector | Pencil |
| Leads on | Release pages, launcher, CLI, section for modders, in-game CAPIE indicators | Workshop page, top of the README, in-game panels |

**The Endorsement Rule.** On a Rename Anything surface, CAPIE appears once, as the line "Built on
CAPIE" in `tag` style, after the mod's name and smaller than it. On a CAPIE surface, Rename
Anything appears in body text as "the first mod built on CAPIE", never as a second logo.

**The Silent Infrastructure Rule.** The pencil and the editors carry no product name. In game,
CAPIE is named only by its indicators and by recovery text when it is missing.

**The Spelling Rule.** Write "CAPIE" in capitals with no dots. Spell out "Cyprian's API Extender"
once per page on CAPIE surfaces, in parentheses after the short name. Never write "Rename Anything
API". Binaries built before the naming decision keep their legacy file names until a separate
renaming step; copy may say "current builds use legacy file names".

## Colors

Warm, low-chroma dark neutrals, one olive family for actions, brass for the native layer, and the
game's signal colours for state. Colour roles describe what a thing is, never which product it
belongs to.

### Primary
- **Olive Button** (`olive-button`): the fill of buttons and of the value part of a "supported"
  badge. Sampled from vanilla `button_123x34.dds`. Hover uses **Olive Lit** (`olive-lit`).
- **Pencil Green** (`pencil-green`, `pencil-green-lit`): the edit affordance. Taken from the
  notepad in vanilla `edit_notes_button.dds`, the sprite the in-game pencils use.

### Secondary
- **Brass** (`brass`): the native layer. Outlines the library in diagrams, colours "planned" tags
  and the CAPIE value in the endorsement badge. Never a decorative rim. Sampled from the vanilla close button. **Brass Dim** (`brass-dim`) is for dashed
  strokes of planned items only; it fails contrast as small text.

### Tertiary
- **Header Amber** (`header-amber`, game `§H`/`§Y`): group labels that name a real layer or
  column, the in-progress status, and at most one highlighted value per view. Never body text,
  never a slogan.

### Neutral
- **Window Ink** (`window-ink`): outer frames, the deepest layer.
- **Field Ink** (`field-ink`): recessed areas such as text fields and diagram nodes.
- **Panel Umber** (`panel-umber`): panels, editors and the diagram canvas (vanilla `generic_bg2`).
- **Panel Rim** (`panel-rim`): hairline borders and dividers.
- **Steel Shadow / Steel Bevel** (`steel-shadow`, `steel-bevel`): icon frames, neutral strokes,
  connectors.
- **Parchment** (`parchment`): primary web text. In game, the default white.
- **Khaki** (`khaki`, game `§L`): secondary text, hints, the neutral status line.
- **Ash** (`ash`, web stand-in for `§g`): captions and disabled labels.

### Signal
- **Go Green** (`go-green`, game `§G`): success and "works today". The game value `#009f03`
  reaches only 4.4:1 on umber, so web text uses the lighter token.
- **Alarm Red** (`alarm-red`, game `§R`): errors and blocking conditions, including the cooldown
  line of a disabled pencil, as vanilla tooltips show unmet conditions. On the web only on
  `field-ink` (5.0:1).
- **Caution Orange** (`caution-orange`, game `§O`) and **Warning Rust** (`warning-rust`): CAPIE is
  missing, the game version is unknown, a fallback path was taken.

**The One Accent Rule.** A view gets olive for actions plus at most one of amber, brass or a
signal colour as its accent.

**The Signal Means State Rule.** Red, orange and green only describe state. Never decoration,
never a product colour, never a heading.

## Typography

**Game:** `hoi_18` (Ubuntu Light, 18 px) for typed text, `hoi_18mbs` (Ubuntu Bold, 18 px) for
names and titles, `hoi_16mbs` (Ubuntu Bold, 16 px) for buttons and tabs, `Arial12` for one-line
status text. All four have complete Polish glyphs. Tooltips keep the game's `ToolTip_Font`
(Garamond 16); we never override it.

**Web:** Ubuntu, falling back to `'Segoe UI', 'DejaVu Sans', Verdana, sans-serif`. Ubuntu is the
face the game's `hoi_*` bitmap fonts were made from and is free under the Ubuntu Font Licence, so
release pages may load it. SVGs shown on GitHub cannot load fonts and use the fallback stack.
Tooltip-like asides use `'EB Garamond', Garamond, Georgia, serif`. Mono only for code, hashes and
CLI output.

On web pages no text is smaller than 11.5px: label caps keep their 11.5px, status tags and small
chrome use 12px (the 10px `tag` size is for diagrams only), tables and code 14px, and body text
keeps a measure of about 75 characters. The documentation sites also have a light page scheme for
readers who ask for one; it is a field grey mixed from `steel-bevel` with white, never cream, and
the footer and header stay `window-ink` in both schemes.

**Character:** a sturdy humanist sans for everything you read, and a book serif only where the
game itself would show a tooltip.

### Hierarchy
- **Label caps** (700, 11.5 px, 0.14em tracking, uppercase, `header-amber`): the name of a real
  group in a diagram ("HEARTS OF IRON IV 1.19.3.0", "WHAT HAPPENS"). Evokes the game's Orator
  headers without using that licensed face. It is never a slogan ("EDIT WHERE YOU SEE IT") and
  never an eyebrow that repeats the title under it.
- **Node title** (700, 15 px, 18 px line): the name of a box in a diagram.
- **Node body** (400, 12 px, 18 px line): one or two short lines under a title.
- **Tag** (700, 10 px, 0.08em, uppercase): status tags inside boxes and badges.
- **Tooltip** (400, 13 px serif): text drawn as an in-game tooltip in a diagram.

**The Polish Glyph Rule.** Any game text that can show a player-entered name uses `hoi_18`,
`hoi_18mbs`, `hoi_16mbs` or `Arial12`. Other fonts (for example `Main_14`) may only carry hidden
values.

**The No Bundled Font Rule.** Never ship, trace or imitate glyph by glyph the game's Orator,
Garamond or any other bundled font file. Use the free stacks above.

## Layout

In game, geometry is local to the vanilla panel being extended, in exact 1.19.3 coordinates.
Pencils sit beside the name they edit with a gap of at least 4 px, never over the name text, the
portrait face or another vanilla control. An opened editor may cover neighbouring controls only
while it is open, as a single overlay anchored to the edited object.

Editor grid: overlay width 420 px; field frame 364 x 26 px; edit box 356 x 20 px inset 4 px / 3 px
(32 times the widest `hoi_18` glyph is 352 px); Apply at x 370, Cancel at x 396; a 408 x 14 px
status line directly under the last field. Rows of a two-field editor repeat every 30 px; a row
with its own label adds 12 px.

On the web, diagrams are 880 px wide and drawn on their own panel so they read the same in light
and dark page themes. Spacing steps are 4, 8, 14, 24 and 32 px: tight inside a node, 24 px between
nodes, 32 px between layers.

## Elevation & Depth

Flat. Depth comes from tone, as in the game: frames darker than panels, fields darker than frames
(recessed), buttons lighter than panels (raised). No drop shadows on the web and no glow. The
only emphasis stroke is brass, around the native layer.

**The Recessed Field Rule.** A place where the player types is always darker than its
surroundings (`field-ink` on `panel-umber`), never lighter.

## Shapes

Near-square. Nodes and badges use a 2 px radius, the outer diagram panel 6 px. Planned items
keep the same shape with a dashed `brass-dim` stroke (`5 4`). In game, shapes come from vanilla
sprites (`GFX_generic_bg2`, `GFX_tiles_dark_area_cut_8`, `GFX_button_94x31`).

## Components

### In-game: pencil launcher
- **Sprite:** vanilla `GFX_edit_designer_notes_button`, 30 px frame at `scale = 0.67` (20 x 20 px).
- **Placement:** beside the name it edits, at least 4 px away, inside the same panel.
- **Enabled:** frame 1; hover and pressed frames come with the sprite.
- **Disabled by cooldown:** the grey disabled frame. The tooltip keeps its first line ("Rename
  leader") and adds one `§R` line: "Next rename possible in 3 days (last change: 4 January 1936)."
- **CAPIE missing:** hidden. In-place editing needs CAPIE; the scripted editor for states, cities
  and characters stays available.
- **Not your object:** hidden. Players rename only their own country's objects. Subjects are
  renamed by their overlord through a diplomatic action, and the lobby rule can let the host
  rename every country.

### In-game: inline editor
- **Container:** `GFX_generic_bg2`, 420 px wide, anchored to the edited name.
- **Field:** frame `GFX_tiles_dark_area_cut_8` 364 x 26 px; `editBoxType` 356 x 20 px, `hoi_18`,
  `ignore_enter = yes`, prefilled with the current name.
- **Apply:** `GFX_preset_button_save` at 20 x 20 px with `shortcut = "RETURN"`. Enter and a click
  run the same game command.
- **Cancel:** `GFX_closebutton_16` (16 px). No `ESCAPE` shortcut while the vanilla panel owns Esc.
- **Labels:** every field of a multi-field editor has a visible label ("Name", "Adjective", "Short
  name", "Full name"). A tooltip alone is not enough.
- **States:** editing (khaki hint "Enter: apply"); error (one `§R` line naming the field and the
  problem, draft kept); stale target (`§R` "This editor is out of date. Cancel and open it
  again."); cooldown (Apply disabled with the cooldown line).
- **Limits:** 32 characters per field; the visible width must fit 32 of the widest glyph.

### In-game: status line
- `Arial12`, one line, 408 x 14 px, under the last field.
- Neutral text in `§L`, errors in `§R`. No success message: the new name in the panel is the
  confirmation.

### In-game: party tabs
- Vanilla `GFX_button_94x31`, `hoi_16mbs`, one tab per ideology group, the open group pressed.
  The tab tooltip shows the party's current name.

### In-game: "CAPIE missing" indicator in a campaign (planned)
- **Where:** in place of the hidden pencil that needs CAPIE (for Rename Anything: the country
  pencil on the Politics title line).
- **Look:** a 16 px warning glyph in `§O`, no text on the panel itself.
- **Tooltip:** "Rename Anything needs CAPIE, which is not loaded. Custom country names show as
  the original. Start the game with the CAPIE launcher."
- Never a pop-up, never a blocking dialog.

### In-game: main-menu indicator (planned)
- **Where:** bottom-left corner of the main menu, one line, `Arial12`. Every mod built on CAPIE
  ships the same snippet; one line is drawn even if several mods include it.
- **Loaded:** `§L`CAPIE 1.0 loaded`§!` (version reported by the library). Tooltip lists the mods
  using it.
- **Required but missing:** `§O`CAPIE missing: Rename Anything needs it`§!`; with several mods
  "CAPIE missing: 2 mods need it". Tooltip says how to start with the launcher.
- **Wrong version:** `§O`CAPIE 1.0 loaded, Rename Anything needs 1.1`§!`.
- Nothing is shown when no enabled mod uses CAPIE.

### Web: diagram panel, nodes and columns
- **Panel:** `panel-umber` fill, 1 px `panel-rim` inner frame, 6 px radius, 880 px wide.
- **Node:** `field-ink` fill, 1.25 px `steel-bevel` stroke, 2 px radius, `node-title` +
  `node-body`. The native layer: 1.75 px `brass` stroke. A planned node keeps the shape with a
  dashed `brass-dim` stroke.
- **Columns inside a node:** the parts of one node are text columns separated by 1 px
  `panel-rim` hairlines, never boxes inside the box. Text in `parchment` for parts that work
  today, `khaki` for planned parts; the status is the `tag` under it (`go-green` TODAY, `brass`
  PLANNED).
- **Legend:** shows the line style that carries the status (solid for works today, dashed for
  planned), not a coloured fill used nowhere else.
- **Fallback path:** dashed `warning-rust` stroke, text in `caution-orange`.
- **Numbered steps:** only where the order is the information (the edit-in-place story). A step
  is a number in `ash`, a `node-title` and one `node-body` line, separated by hairlines; not a
  stack of identical boxes.

### Web: badges
- 22 px tall, 2 px radius, two parts: a `field-ink` key and a value part, `olive-button` for
  supported, `panel-umber` otherwise. No marks inside badges.
- Every badge has the same 1 px `panel-rim` rim; a planned value uses a dashed `brass-dim` rim.
  The state is carried by the value text colour alone (`go-green`, `header-amber`,
  `caution-orange`, `brass`), never by a different coloured frame per badge.
- Text in `tag` style: parchment on the key, the state colour on the value.

### Web: status marks
- **Works today:** filled `pencil-green-lit` square, 10 px.
- **In progress:** `header-amber` square outline, 10 px.
- **Planned:** dashed `brass-dim` square outline, 10 px.
- **Not supported:** `warning-rust` square outline with a diagonal.

### Iconography
One drawing style for every icon: 20 px grid, 1.5 px strokes, flat fills from the palette, square
corners rounded at most 1 px, no gloss.
- **Where marks go:** the launcher's window and file icon, release pages and the site favicon.
  Not before a heading, not inside a badge, not beside a box title in a diagram: the name
  already says it.
- **Pencil (Rename Anything mark):** in game, the vanilla sprite. On the web, our drawing: a
  steel-framed square with a `pencil-green` pad and a diagonal `khaki` pencil. In a diagram it
  appears only where it shows the real in-game control (the edit-in-place story).
- **Connector (CAPIE mark):** three short horizontal `brass` bars stacked on the left of a small
  `field-ink` plate, like a plug. In the CLI banner it is text only:
  `CAPIE (Cyprian's API Extender)`.
- **Warning:** a triangle in `warning-rust` with a `parchment` bar and dot. In game, a vanilla
  warning sprite.
- **Status marks:** as above.
- No emoji and no Unicode symbols as icons.

### Diagram motion
- Motion only where the order of events is the content: the edit-in-place story and the branch
  of the launch chain. A structure (the architecture layers) stays still.
- No ambient pulses, no colour flashes or glowing strokes, and no motion on items marked planned
  that would suggest they already run.
- The resting frame is complete and true. Animations are written only inside
  `@media (prefers-reduced-motion: no-preference)`, so with reduced motion the final state shows.
- CSS keyframes only. No SMIL (it ignores the reduced-motion query) and no script.
- Easing `cubic-bezier(.16,1,.3,1)` for arrivals, linear for visibility switches, `steps()` for
  typing. No bounce, no elastic.
- Loops: 10 s for a story, 12 s for a two-branch flow. At least 20 % of every loop is still.
  Moving tokens at most 3.5 px in radius. Nothing flashes.

## Do's and Don'ts

### Do:
- **Do** put the pencil beside the name it changes, 20 px, with a 4 px gap.
- **Do** reuse vanilla sprites by name in game and the sampled colours on the web.
- **Do** keep the typed text recessed (`field-ink`) and the action olive.
- **Do** label every field of a multi-field editor on the panel itself.
- **Do** show status with the four marks and the words "Works today", "In progress", "Planned",
  "Not supported".
- **Do** draw diagrams on their own `panel-umber` canvas so light and dark page themes read the
  same.
- **Do** use brass for the native layer in any diagram, whichever product the diagram is about.

### Don't:
The same list is machine-readable in `tokens.json` under `avoid`. It applies to every surface:
README, diagrams, sites, launcher, CLI and the game.

Product rules:
- **Don't** add a global floating button over portraits, decisions or other vanilla controls.
- **Don't** use `§R` for anything that is not an error or a blocking condition.
- **Don't** give CAPIE and Rename Anything different palettes, fonts or motion.
- **Don't** put the CAPIE mark inside the Rename Anything panels.
- **Don't** show player-entered text in a font without Polish glyphs.
- **Don't** claim a feature in a diagram that the status table does not mark "Works today".
- **Don't** write "Rename Anything API": the library is CAPIE.

Visual anti-patterns (generic, templated looks that do not belong to the game):
- **Don't** use side-tab accents: a coloured `border-left` or `border-right` thicker than 1 px on
  cards, callouts, alerts or list items.
- **Don't** use gradient text, gradient fills, glassmorphism or blur as decoration.
- **Don't** use neon, glow, zero-offset coloured halos or colour-flash animations, and no cyan,
  purple or blue-violet palettes.
- **Don't** put cards, chips or boxes inside a card or node. Use columns and hairline dividers.
- **Don't** build a page or diagram from a grid of identical icon + heading + text cards.
- **Don't** use the hero-metric template (big number, small label, supporting stats, accent).
- **Don't** use generic rounded rectangles with drop shadows. Radius stays at 2 px for nodes and
  6 px for the outer panel; there are no drop shadows.
- **Don't** use bounce or elastic easing.
- **Don't** use pure black `#000` or pure white `#fff` on the web; use `window-ink` and
  `parchment`.
- **Don't** add decorative sparklines, progress rings or charts without real data.
- **Don't** put an icon or mark above or before every heading, box title or badge.
- **Don't** use monospace as a costume for "technical". Mono is for code, hashes and CLI output.
- **Don't** centre everything. Text is left-aligned; centring is for a single short label in a
  fixed box at most.
- **Don't** use one uniform spacing value everywhere. Space follows relationship: 4 or 8 px
  inside a group, 24 px between nodes, 32 px between layers.
- **Don't** put an eyebrow or slogan in label caps above a heading.
- **Don't** animate for atmosphere. Infinite motion must show a sequence the still frame cannot.
- **Don't** use emoji or Unicode glyphs as icons.
- **Don't** give each badge or box its own accent colour; one rim colour, state in the text.

In game:
- **Don't** draw custom sprites, frames or ornaments where a vanilla sprite exists. Custom
  textures that remain (the old on-screen keyboard) use the token colours and the vanilla steel
  bevel.
- **Don't** colour text with `§` for emphasis. `§Y`/`§H` at most once per view (the edited
  target), `§L` for labels and hints, `§R`/`§O`/`§G` only for state.
- **Don't** use exclamation marks, "Successfully", success toasts or pop-ups.
- **Don't** put the product name in an editor title or next to a pencil.
- **Don't** put several identical icons in a row that differ only by tooltip.

## Voice and Tone

The voice is a clear staff note: short, specific, calm. It names the object, says what happened
and, when something failed, says what to do next and whether anything changed. Both products use
this one voice.

- Name the thing. "Rename leader", not "Edit". "Country name", not "Field 1".
- Problem, then recovery. Say "Nothing was changed" when that is true.
- No exclamation marks, no "Oops", no "Successfully". The new name on screen is the success.
- Digits for numbers ("5 days", "32 characters").
- Players never see internal words: DLL, bridge, epoch, payload, hook, RN1. Call the library
  "CAPIE" and the program that starts the game with it "the CAPIE launcher". README, release notes
  and CLI may say DLL where the audience is technical.
- English uses straight quotes and no dashes as punctuation. Polish uses „…" quotation marks, as
  in the game's Polish localisation.
- Polish: plain verbs ("Zmień nazwę przywódcy", "Nic nie zmieniono"). Avoid officialese such as
  "okres karencji".

### Reference strings

| Situation | English | Polish |
|---|---|---|
| Pencil tooltip | Rename leader | Zmień nazwę przywódcy |
| Cooldown line | Next rename possible in 3 days (last change: 4 January 1936). | Kolejna zmiana nazwy możliwa za 3 dni (ostatnia zmiana: 4 stycznia 1936). |
| Hint | Enter: apply | Enter: zatwierdź |
| Too long | Name is too long: 32 characters at most. | Nazwa jest za długa: najwyżej 32 znaki. |
| Empty | Name is empty. Type a name or press Cancel. | Nazwa jest pusta. Wpisz nazwę albo anuluj. |
| Illegal character | Name contains a character the game cannot show. | Nazwa zawiera znak, którego gra nie wyświetli. |
| Stale editor | This editor is out of date. Cancel and open it again. | Ten edytor jest nieaktualny. Anuluj i otwórz go ponownie. |
| CAPIE missing (in game) | Rename Anything needs CAPIE, which is not loaded. Start the game with the CAPIE launcher. Nothing was changed. | Rename Anything wymaga CAPIE, które nie jest załadowane. Uruchom grę przez launcher CAPIE. Nic nie zmieniono. |
| Main menu, loaded | CAPIE 1.0 loaded | CAPIE 1.0 załadowane |
| Main menu, missing | CAPIE missing: Rename Anything needs it | Brak CAPIE: wymaga go Rename Anything |
| Endorsement line | Built on CAPIE | Zbudowane na CAPIE |

### CLI output pattern (bootstrap and launcher)

One line per step: a fixed status word, the object, the result. Questions end with the default in
brackets. Intended shape (proposed, not implemented):

```text
CAPIE (Cyprian's API Extender) setup

  OK    Hearts of Iron IV 1.19.3.0 found (hash matches)
  OK    CAPIE launcher installed
  ASK   Add the launcher to Steam launch options? Multiplayer is not supported
        while it is set. [y/N]
  SKIP  Steam launch options left unchanged
  NOTE  Start the game with the desktop shortcut "Hearts of Iron IV (CAPIE)".
  NOTE  Mods built on CAPIE in this setup: Rename Anything
```

Status words: `OK`, `ASK`, `SKIP`, `NOTE`, `FAIL`. A `FAIL` line is followed by one line that says
what to do. The output must make sense without colour; when colour is available, `OK` is
go-green, `FAIL` alarm-red, `NOTE` and `SKIP` khaki, `ASK` header-amber.
