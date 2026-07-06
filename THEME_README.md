# Humanities in the Age of AI — Ghost in the Shell Theme

This Jekyll site's theme takes its visual and structural cues from *Ghost in
the Shell* (1995): a light-first interface with a dark "net-dive" mode, a
cinematic dark title band (styled after the film's title card) on every
page's header, a falling-data header motif standing in for the old
circuit-board look, and unit badges that map the course's four units onto
the film's vocabulary. This document is the current (Fall 2026) theme
reference. The Fall 2025 theme writeup for the prior circuit-board design is
kept locally in the untracked `2025/` folder and describes the older,
dark-only circuit-board version — it is not updated for this theme and
should be left as a historical record.

## Token table

Page-body color is expressed as CSS custom properties on
`:root[data-theme="light"]` and `:root[data-theme="dark"]`, defined in
`assets/css/style.scss`. Every themed rule in the stylesheet reads from these
tokens (via `var(--token)` or `color-mix(in srgb, var(--token) X%, ...)`)
rather than hardcoding colors, so the entire site repaints correctly when the
theme flips.

| Token           | Light      | Dark       | Used for |
|-----------------|------------|------------|----------|
| `--bg`          | `#f6f8f7`  | `#0c1210`  | Page background |
| `--bg-alt`      | `#e8efec`  | `#14201c`  | Panels, header art backdrop, code/table backgrounds |
| `--text`        | `#1a2b27`  | `#d7e5e0`  | Body text |
| `--text-muted`  | `#4a5f59`  | `#8aa39b`  | Secondary text, captions, footer tagline |
| `--accent`      | `#0f766e`  | `#2dd4bf`  | Headings, primary highlight, list markers, header-band bottom edge |
| `--accent-2`    | `#b45309`  | `#f59e0b`  | Secondary highlight, warning banner |
| `--link`        | `#0e7490`  | `#67e8f9`  | Links, gradients |
| `--border`      | `#c6d4cf`  | `#23332e`  | Borders, table rules |

### Header-band tokens (theme-independent)

The header/title band is a fixed dark cinematic strip in **both** themes —
it does not repaint on toggle. Its colors are plain `:root` variables (not
scoped under `[data-theme]`) so they stay constant regardless of the page
theme:

| Token           | Value      | Used for |
|-----------------|------------|----------|
| `--band-bg`     | `#0c1210`  | Header/title band background |
| `--band-bg-alt` | `#14201c`  | Header band gradient stop, data-stream tint |
| `--band-text`   | `#d7e5e0`  | Band title text, ghost-silhouette fill, page-title text |
| `--band-accent` | `#2dd4bf`  | Band emphasis text (e.g. "AI"), data-stream glyphs, nav-home link |
| `--band-muted`  | `#8aa39b`  | Dossier line, site description under the hero |

Contrast of `--band-text` (`#d7e5e0`) on `--band-bg` (`#0c1210`) is
**~14.6:1**, well past WCAG AAA (7:1) for normal text.

The one deliberate exception: the header band's bottom-edge rule
(`border-bottom` on `#header-container` / `#compact-header`) uses the
theme-reactive `var(--accent)`, not a band token — a quiet 3px cue of which
theme is active, sitting right at the seam where the fixed-dark band meets
the theme-controlled page body.

Translucent surfaces (button backgrounds, panel overlays, hover highlights,
focus rings) are built with `color-mix(in srgb, var(--token) X%, transparent)`
instead of hardcoded `rgba(...)`, so they stay correct in both themes without
duplicating color logic.

## Toggle behavior

- `assets/js/theme-toggle.js` runs in `<head>` (before body paint) and sets
  `data-theme` on `<html>` from, in priority order: a stored
  `localStorage["theme"]` value, then `prefers-color-scheme`, defaulting to
  **light** if neither is available.
- It exposes `window.toggleTheme()`, wired to the floating
  `<button class="theme-toggle" onclick="toggleTheme()">` present in both
  `_layouts/default.html` and `_layouts/page.html`. Toggling flips
  `data-theme` and persists the choice to `localStorage["theme"]`.
- Because the script runs before body render, there is no flash of the wrong
  theme on load.

## Unit badges

Four fixed-color pill badges mark the course's four units, independent of
the light/dark toggle (they're brand chips, not theme-reactive surfaces):

```html
<span class="unit-badge unit-badge--ghosts">Ghosts</span>
<span class="unit-badge unit-badge--shells">Shells</span>
<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>
<span class="unit-badge unit-badge--coda">The Net Is Vast and Infinite</span>
```

| Class                          | Color     |
|--------------------------------|-----------|
| `.unit-badge--ghosts`          | `#0f766e` |
| `.unit-badge--shells`          | `#b45309` |
| `.unit-badge--puppetmasters`   | `#365314` |
| `.unit-badge--coda`            | `#475569` |

## Header: cinematic title band

Both headers (`#header-container` in `_layouts/default.html`, `#compact-header`
in `_layouts/page.html`) render as a fixed dark title-card band — the film's
opening credits look — using the `--band-*` tokens described above, so the
band's look never changes when the reader toggles light/dark. Only the page
body underneath repaints with the theme.

- **`default.html` hero**: an uppercase, letterspaced (`0.22em`) site title
  in Rajdhani (`.site-title`), with the "AI" span picked out in
  `var(--band-accent)`. Beneath it, a mono "dossier line"
  (`.dossier-line`, IBM Plex Mono, `var(--band-muted)`, uppercase) renders the
  literal text `[ ENG 6806 // FALL 2026 ]`. If `site.description` is set, it
  renders quietly beneath that in IBM Plex Sans.
- **`page.html` compact band**: the same treatment at a smaller scale — the
  per-page title (`.page-title h1`) in uppercase letterspaced Rajdhani, with
  its own `.dossier-line` underneath. The back-to-home `.nav-home` link uses
  `var(--band-accent)`, brightening to `var(--band-text)` on hover.
- The floating `.theme-toggle` button is styled with `--band-*` tokens too
  (not the theme tokens), since it sits fixed over the dark band on every
  page and must stay legible there regardless of which theme is active.

## Header art: falling-data / thermoptic shimmer

The old animated circuit-board header (SVG traces, pulsing nodes, floating
particles) has been replaced by a subtler motif, now retuned to the
header-band tokens so it reads correctly against the band's fixed dark
background in both themes:

- **Data stream** (`.data-stream` / `.data-stream-svg` / `.data-glyph-col`):
  a sparse grid of vertical glyph columns (`0 1 ø λ Ω § ∆ ¶`), placed by
  `assets/js/circuit-animations.js` and rendered in `var(--band-accent)` at
  low opacity (0.22) over a translucent `var(--band-bg-alt)` tint (applied as
  a `color-mix` background on the `.data-stream` wrapper — deliberately *not*
  as wrapper `opacity`, which would multiply into the children and crush
  their visibility). Roughly a third of grid
  positions are skipped at random so the effect stays sparse rather than
  filling the header. It appears on both the full header
  (`#header-container`, `_layouts/default.html`) and the compact per-page
  header (`#compact-header`, `_layouts/page.html`), at different column/row
  densities.
- **Ghost-silhouette reveal** (`.ghost-silhouette` and its `-head` /
  `-shoulders` children, full header only): a plain CSS bust shape, colored
  with `var(--band-text)` at very low opacity (0.07 resting). Because the
  band is always dark, tying the silhouette to the fixed `--band-text` token
  (rather than the theme-reactive `--text`) keeps it a correctly-contrasted
  faint presence regardless of which theme the reader has selected.
  `initializeGhostReveal()` adds an `.is-revealed` class (raising the opacity
  to 0.22) once the reader scrolls past the header.
- Both effects use CSS custom properties exclusively — no hardcoded colors —
  so they repaint correctly the instant the theme is toggled (in the case of
  the band tokens, that means: they don't repaint at all, by design).

## Fonts

Three Google Fonts, loaded via a single `<link>` in both layouts' `<head>`
(Rajdhani 500/700, IBM Plex Sans 400/400italic/600/700, IBM Plex Mono
400/600). The former Chakra Petch + Roboto Mono pairing has been removed
entirely (no remaining references anywhere in `assets/` or `_layouts/`):

- **Rajdhani** — all headings (`h1`–`h6`), `.site-title`, page/band titles,
  and nav-ish chrome (`.nav-home`, buttons, the tutorial warning banner's
  `<strong>`). `h1`/`h2` and the band titles are uppercase with wide letter
  spacing (0.2em+ on the hero title); `h3`–`h6` stay Rajdhani but keep normal
  case.
- **IBM Plex Sans** — body copy (`body`), at `line-height: 1.65` for
  proportional-face readability, and the optional `.site-description` line.
- **IBM Plex Mono** — code/`pre`, table `th`, `.unit-badge`, the
  `.dossier-line` caption, form inputs, and other label-ish chrome.

## List markers (HUD style)

Content lists in the main article area use custom markers instead of
default bullets/numbers:

- **Top-level `ul li`**: `list-style: none` with a `❯` marker in
  `var(--accent)`, implemented via `li::before` plus the
  `text-indent: -1.5em` / `padding-left: 1.5em` hanging-indent pair (the
  `::before`'s own fixed width keeps wrapped lines aligned under the first,
  rather than sagging back to the left margin) — this matters for the
  syllabus's longer reading-list entries.
- **Nested `ul ul li`**: a quieter `▸` marker in `var(--text-muted)`.
- **`ol`**: keeps native browser numbering (so `start=`, nesting, etc. all
  keep working) but recolors the number itself via `ol li::marker` to
  `var(--accent)` in IBM Plex Mono.
- `li` spacing is `margin-block: 0.35em` for easier scanning of dense
  reading lists and the table of contents.

## Reduced-motion handling

Every `animation:` / `transition:` declaration tied to motion in
`style.scss` lives inside `@media (prefers-reduced-motion: no-preference) { ... }`
blocks. The base (non-animated) rules only ever set static properties. This
applies to the header art too:

- `.data-glyph-col`'s drift (`dataDrift` keyframe) only exists inside the
  no-preference block. With reduced motion requested, columns simply sit at
  the position JS placed them — no separate "static mode" markup or JS
  branch is needed; the CSS keyframe is just absent.
- `.ghost-silhouette`'s opacity transition is likewise gated. Its JS
  initializer (`initializeGhostReveal()`) explicitly checks
  `matchMedia('(prefers-reduced-motion: reduce)')` and skips attaching the
  scroll listener entirely when motion is reduced, leaving the silhouette at
  its CSS resting opacity — that resting state *is* the required static
  first frame.

In short: under reduced motion, the header renders exactly one frame of the
falling-data/ghost-silhouette scene, permanently.

## File map

| File | Role |
|------|------|
| `assets/css/style.scss` | All theme tokens, header art rules, unit badges, and general site styling. |
| `assets/js/theme-toggle.js` | Sets `data-theme` before paint; exposes `window.toggleTheme()`. |
| `assets/js/circuit-animations.js` | Builds the falling-data header art (`initializeDataStream`, `initializeGhostReveal`) plus unrelated general site interactions (scroll fade-ins, page loader, keyboard shortcuts, table row/header hover). Historically the circuit-board animation file; repurposed rather than renamed. |
| `_layouts/default.html` | Full-width header (`#header-container`) with the data-stream + ghost-silhouette header art; used for top-level pages. |
| `_layouts/page.html` | Compact header (`#compact-header`) with the data-stream header art only; used for individual week/lesson pages, including the archived 2025 content. |
| `THEME_README.md` (this file) | Current theme documentation, repo root. |

## Footer tagline

Both layouts' `<footer>` include the line *"the net is vast and infinite"*
— a nod to the film's closing line — set in `<em>` beneath the standard
copyright line.
