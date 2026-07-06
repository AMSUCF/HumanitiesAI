# Humanities in the Age of AI — Ghost in the Shell Theme

This Jekyll site's theme takes its visual and structural cues from *Ghost in
the Shell* (1995): a light-first interface with a dark "net-dive" mode, a
falling-data header motif standing in for the old circuit-board look, and
unit badges that map the course's four units onto the film's vocabulary.
This document is the current (Fall 2026) theme reference. The Fall 2025
theme writeup is archived separately at `2025/THEME_README.md` and describes
the older, dark-only circuit-board version — it is not updated for this
theme and should be left as a historical record.

## Token table

All color is expressed as CSS custom properties on `:root[data-theme="light"]`
and `:root[data-theme="dark"]`, defined in `assets/css/style.scss`. Every
themed rule in the stylesheet reads from these tokens (via `var(--token)` or
`color-mix(in srgb, var(--token) X%, ...)`) rather than hardcoding colors, so
the entire site repaints correctly when the theme flips.

| Token           | Light      | Dark       | Used for |
|-----------------|------------|------------|----------|
| `--bg`          | `#f6f8f7`  | `#0c1210`  | Page background |
| `--bg-alt`      | `#e8efec`  | `#14201c`  | Panels, header art backdrop, code/table backgrounds |
| `--text`        | `#1a2b27`  | `#d7e5e0`  | Body text; also the ghost-silhouette fill (see below) |
| `--text-muted`  | `#4a5f59`  | `#8aa39b`  | Secondary text, captions, footer tagline |
| `--accent`      | `#0f766e`  | `#2dd4bf`  | Headings, primary highlight, data-stream glyphs |
| `--accent-2`    | `#b45309`  | `#f59e0b`  | Secondary highlight, warning banner |
| `--link`        | `#0e7490`  | `#67e8f9`  | Links, gradients |
| `--border`      | `#c6d4cf`  | `#23332e`  | Borders, table rules |

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

## Header art: falling-data / thermoptic shimmer

The old animated circuit-board header (SVG traces, pulsing nodes, floating
particles) has been replaced by a subtler motif:

- **Data stream** (`.data-stream` / `.data-stream-svg` / `.data-glyph-col`):
  a sparse grid of vertical glyph columns (`0 1 ø λ Ω § ∆ ¶`), placed by
  `assets/js/circuit-animations.js` and rendered in `var(--accent)` at low
  opacity (0.22) over a translucent `var(--bg-alt)` tint (applied as a
  `color-mix` background on the `.data-stream` wrapper — deliberately *not*
  as wrapper `opacity`, which would multiply into the children and crush
  their visibility). Roughly a third of grid
  positions are skipped at random so the effect stays sparse rather than
  filling the header. It appears on both the full header
  (`#header-container`, `_layouts/default.html`) and the compact per-page
  header (`#compact-header`, `_layouts/page.html`), at different column/row
  densities.
- **Ghost-silhouette reveal** (`.ghost-silhouette` and its `-head` /
  `-shoulders` children, full header only): a plain CSS bust shape, colored
  with `var(--text)` at very low opacity (0.07 resting). Because `--text` is
  dark in light mode and light in dark mode, the silhouette always reads as a
  faint, correctly-contrasted presence against the header background in
  *either* theme, with no separate dark-mode override needed.
  `initializeGhostReveal()` adds an `.is-revealed` class (raising the opacity
  to 0.22) once the reader scrolls past the header.
- Both effects use CSS custom properties exclusively — no hardcoded colors —
  so they repaint correctly the instant the theme is toggled.

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
| `2025/THEME_README.md` | Archived documentation for the Fall 2025 circuit-board theme — left untouched. |

## Footer tagline

Both layouts' `<footer>` include the line *"the net is vast and infinite"*
— a nod to the film's closing line — set in `<em>` beneath the standard
copyright line.
