# Fall 2026 Humanities AI Course Build — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Fall 2026 ENG 6806 course (Ghost in the Shell agentic theme, UCF Fall 2026 calendar) at repo root with the 2025 course archived, plus a Python CLI that deploys the markdown course to Canvas.

**Architecture:** Markdown files with `canvas:` front matter are the single source of truth; Jekyll renders them as the public site (light-first GitS theme) and `canvas/deploy.py` converts the same files into Canvas modules, pages, and graded discussions (idempotent upserts, dry-run first). Spec: `docs/superpowers/specs/2026-07-05-fall2026-course-design.md`.

**Tech Stack:** Jekyll (GitHub Pages), Python 3.11+, python-frontmatter, markdown-it-py, PyYAML, requests, python-dotenv, pytest, responses.

## Global Constraints

- **Light mode is the site default**, dark mode via toggle persisted in localStorage; `prefers-color-scheme` is the initial hint only.
- **Timezone:** America/New_York. All weekly work due **Sundays 11:59 PM ET**; Canvas `due_at` sent as UTC ISO-8601 (mind the Nov 1, 2026 DST fallback).
- **Grading totals exactly 100:** Activity Verification 6 (Fri Aug 28) + 12 exercises × 6 + merged Week 10 exercise 12 + Final Reflection 10 (Thu Dec 10). Week 14 is extra credit (Canvas `points_possible: 0`, graded above zero; tiers 6/6/10).
- **Canvas objects are created unpublished** unless `--publish` is passed.
- **Never commit `.env`**; credentials only via environment.
- **2025 content is archived unmodified** under `2025/` (renders under the new theme; that's acceptable per spec). Images still needed by 2026 pages are **copied** to root `images/`, never referenced into `2025/`.
- **`canvas:` front matter schema** (exact keys, every week file):

```yaml
canvas:
  module: "<module title>"     # string
  week_start: 2026-08-24       # date, the module Monday
  due: 2026-08-30              # date, the Sunday deadline
  points: 6                    # int; 12 for week 10; 0 for week 14
  discussion: true             # bool
  extra_credit: false          # bool; true only week 14
  unit: ghosts                 # ghosts | shells | puppetmasters | coda
```

- **Unit slugs, labels, accent colors** (used by SCSS and converter identically):

| slug | label | color |
|------|-------|-------|
| ghosts | Ghosts | `#0f766e` |
| shells | Shells | `#b45309` |
| puppetmasters | Puppet Masters | `#365314` |
| coda | The Net Is Vast and Infinite | `#475569` |

- **Canonical week table** (titles, files, dates, points — referenced by all content and deployer tasks):

| Wk | File | Module title | week_start | due | pts | unit |
|----|------|--------------|-----------|-----|-----|------|
| 1 | weekone.md | Week One: Ghosts — Histories | 2026-08-24 | 2026-08-30 | 6 | ghosts |
| 2 | weektwo.md | Week Two: Ghosts — Generation | 2026-08-31 | 2026-09-06 | 6 | ghosts |
| 3 | weekthree.md | Week Three: Ghosts — Sources | 2026-09-07 | 2026-09-13 | 6 | ghosts |
| 4 | weekfour.md | Week Four: Ghosts — Reading | 2026-09-14 | 2026-09-20 | 6 | ghosts |
| 5 | weekfive.md | Week Five: Shells — Aesthetics | 2026-09-21 | 2026-09-27 | 6 | shells |
| 6 | weeksix.md | Week Six: Shells — Art and Creativity | 2026-09-28 | 2026-10-04 | 6 | shells |
| 7 | weekseven.md | Week Seven: Shells — Video and Realism | 2026-10-05 | 2026-10-11 | 6 | shells |
| 8 | weekeight.md | Week Eight: Shells — Perceptions | 2026-10-12 | 2026-10-18 | 6 | shells |
| 9 | weeknine.md | Week Nine: Puppet Masters — Distant Coding | 2026-10-19 | 2026-10-25 | 6 | puppetmasters |
| 10 | weekten.md | Week Ten: Puppet Masters — Building and Deploying | 2026-10-26 | 2026-11-01 | 12 | puppetmasters |
| 11 | weekeleven.md | Week Eleven: Puppet Masters — Agentic Code | 2026-11-02 | 2026-11-08 | 6 | puppetmasters |
| 12 | weektwelve.md | Week Twelve: Puppet Masters — Local Ghosts | 2026-11-09 | 2026-11-15 | 6 | puppetmasters |
| 13 | weekthirteen.md | Week Thirteen: Puppet Masters — Distant Reading with and for AI | 2026-11-16 | 2026-11-22 | 6 | puppetmasters |
| 14 | weekfourteen.md | Week Fourteen: The Net Is Vast and Infinite — Custom Bots (Extra Credit) | 2026-11-30 | 2026-12-06 | 0 | coda |

- **Commit style:** short conventional messages (`feat:`, `chore:`, `content:`, `test:`); commit at the end of every task, plus mid-task where steps say so.
- **Verification limits:** local Jekyll may be unavailable on this Windows machine. Site verification = front-matter YAML parses + relative links/images resolve + (if `bundle exec jekyll build` exists) a clean build; otherwise push and check the Pages build action.

---

## Phase A — Repo reorganization and theme

### Task 1: Archive the 2025 course into `2025/`

**Files:**
- Create: `2025/` (via `git mv`), root `index.md` placeholder, root `images/` (empty, `.gitkeep`)
- Modify: nothing else

**Interfaces:**
- Produces: `2025/` containing every 2025 course file with intact relative links; a root that later tasks build into.

- [ ] **Step 1: Move course content**

Move ALL root-level course files into `2025/` with `git mv`: every `week*.md` (including `*old.md`), `index.md`, `finalreflection.md`, all root images (`*.png`, `*.jpg`), all media (`*.mp4`), `dream.html`, `markov.html`, `test-theme.html`, `sample_cleaning.py`, `THEME_README.md`, and the exercise-artifact directories `character/`, `model/`, `ranker/`, `WeekOne/`. Do NOT move: `_config.yml`, `_layouts/`, `assets/`, `app.js` (check first — if `app.js` is only referenced by moved HTML files, move it too), `docs/`, `desktop.ini`.

```powershell
git mv weekone.md 2025/weekone.md   # ... etc for each file
```

- [ ] **Step 2: Verify no root references break**

Run: `Grep pattern "2025/" glob "_layouts/*.html"` and check `_config.yml` for `include`/`exclude`/nav entries pointing at moved files. Grep the moved files for absolute-path references (`](/`) that would now 404; fix only by editing `_config.yml`/layouts, never the archived files.

- [ ] **Step 3: Create placeholder root index**

```markdown
---
layout: default
title: Humanities in the Age of AI
---

Fall 2026 course under construction. The Fall 2025 version is archived at [2025/](2025/index.md).
```

- [ ] **Step 4: Create root `images/.gitkeep`**

- [ ] **Step 5: Commit**

```powershell
git add -A; git commit -m "chore: archive 2025 course under 2025/"
```

### Task 2: Light-first theme with dark toggle

**Files:**
- Modify: `assets/css/style.scss`, `_layouts/default.html`, `_layouts/page.html`
- Create: `assets/js/theme-toggle.js`

**Interfaces:**
- Produces: CSS custom properties on `:root[data-theme="light"]` and `:root[data-theme="dark"]`; global `toggleTheme()`; `.unit-badge--<slug>` classes for Task 3.

- [ ] **Step 1: Write the toggle script** (`assets/js/theme-toggle.js`, exactly):

```javascript
(function () {
  var stored = localStorage.getItem("theme");
  var preferred = stored ||
    (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.documentElement.setAttribute("data-theme", preferred);
  window.toggleTheme = function () {
    var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  };
})();
```

Load it in the `<head>` of both layouts (before body renders, to avoid flash), and add a toggle button to both headers:

```html
<script src="{{ '/assets/js/theme-toggle.js' | relative_url }}"></script>
<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle dark mode">◐</button>
```

- [ ] **Step 2: Replace the palette in `style.scss` with design tokens**

Exact tokens (decorative CSS around them is implementer's judgment, acceptance criteria in Step 4):

```scss
:root[data-theme="light"] {
  --bg: #f6f8f7; --bg-alt: #e8efec; --text: #1a2b27; --text-muted: #4a5f59;
  --accent: #0f766e; --accent-2: #b45309; --link: #0e7490; --border: #c6d4cf;
}
:root[data-theme="dark"] {
  --bg: #0c1210; --bg-alt: #14201c; --text: #d7e5e0; --text-muted: #8aa39b;
  --accent: #2dd4bf; --accent-2: #f59e0b; --link: #67e8f9; --border: #23332e;
}
```

Replace every hardcoded color in the existing SCSS with these variables. Headers switch from Orbitron to **Chakra Petch** (Google Fonts); body stays Roboto Mono. All animations wrapped in `@media (prefers-reduced-motion: no-preference)`.

- [ ] **Step 3: Add unit badge classes**

```scss
.unit-badge { display: inline-block; padding: 2px 10px; border-radius: 9999px;
  color: #fff; font-family: "Chakra Petch", sans-serif; font-size: 0.75rem;
  letter-spacing: 1px; text-transform: uppercase; }
.unit-badge--ghosts { background: #0f766e; }
.unit-badge--shells { background: #b45309; }
.unit-badge--puppetmasters { background: #365314; }
.unit-badge--coda { background: #475569; }
```

- [ ] **Step 4: Verify**

Both layouts reference the script and button; SCSS has no remaining hardcoded page colors outside the token blocks; `python -c "import yaml,glob; [yaml.safe_load(open(f).read().split('---')[1]) for f in glob.glob('*.md')]"` parses. If Ruby/Jekyll available: `bundle exec jekyll build` succeeds. Acceptance: light renders by default in a fresh profile; toggle flips and persists across reload; contrast of `--text` on `--bg` ≥ 7:1 both modes (check with a contrast calculator).

- [ ] **Step 5: Commit** — `git add -A; git commit -m "feat: light-first Ghost in the Shell theme with dark toggle"`

### Task 3: Header art, tagline, THEME_README

**Files:**
- Modify: `_layouts/default.html`, `_layouts/page.html`, `assets/js/circuit-animations.js` (replace), `assets/css/style.scss`
- Create: `THEME_README.md` (root; the 2025 one lives in `2025/`)

**Interfaces:**
- Consumes: tokens and badge classes from Task 2.
- Produces: final site chrome used by all content pages.

- [ ] **Step 1: Replace circuit-board header art** with a falling-data / thermoptic-shimmer SVG+JS motif: a sparse column-drift of glyphs in `--accent` at low opacity over `--bg-alt`, with a faint ghost-silhouette reveal on scroll. Must read correctly on light AND dark tokens, and render static (first frame) under `prefers-reduced-motion`. Delete or repurpose `circuit-animations.js` accordingly.
- [ ] **Step 2: Footer tagline** in both layouts: `<footer>… <em>the net is vast and infinite</em></footer>`.
- [ ] **Step 3: Write new `THEME_README.md`** documenting: token table (copy from Task 2), toggle behavior, unit badge usage (`<span class="unit-badge unit-badge--ghosts">Ghosts</span>`), header art behavior, reduced-motion handling, file map.
- [ ] **Step 4: Verify** — same checks as Task 2 Step 4; view `index.md` placeholder page if Jekyll available.
- [ ] **Step 5: Commit** — `git commit -m "feat: header art, tagline, theme docs"`

---

## Phase B — Content foundations

### Task 4: Reading & currency research (build log) — ends in USER CHECKPOINT

**Files:**
- Create: `docs/2026-buildlog.md`

**Interfaces:**
- Produces: `docs/2026-buildlog.md` with four sections other tasks consume verbatim: `## Readings`, `## Model and tool currency`, `## Corpus`, `## Claude Code Web setup`.

- [ ] **Step 1: Verify/select all ⚠ readings** (WebSearch/WebFetch; record chosen URL + 1-line rationale per item under `## Readings`, keyed by week):
  - W1: GitS (1995) 30th-anniversary critical essay — surface 2–3 candidates, pick 1, list alternates.
  - W3: Karen Hao — *Empire of AI* excerpt or 2025–26 reporting piece.
  - W4: newer Underwood on LLMs and literary study.
  - W6: check for a stronger 2026 archival-AI-art piece than the Anadol interview; keep Anadol if none.
  - W7: 2 current generative-video pieces (state of Sora/Veo in 2026 + labor response).
  - W8: refresh AI-images-in-communities news links (2 items).
  - W9–12: confirm live URLs for Willison: "Here's how I use LLMs to help me write code", "Vibe engineering", "Designing agentic loops", "The lethal trifecta for AI agents"; W12 also 1 current local-model piece.
  - W13: 2–3 candidates of updated DH scholarship on AI-assisted computational literary study (recent Underwood; Klein/D'Ignazio; DHQ/CA LLM special issues), pick 2.
  - *AI for Good* (Tyrangiel): fetch TOC; map chapters to weeks 9–14 (double up chapters if count exceeds six; record mapping).
  - Re-verify GitS (1995) streaming availability + Science SARU series status on Prime.
- [ ] **Step 2: Model/tool currency table** under `## Model and tool currency`: for each stale reference in the 2025 pages (Claude Sonnet 4/4.5, Opus 4, "Research mode" naming, DeepSeek-R1, Veo 3, GPT Image 1, Copilot image tools, expired Gemini student offer), record the July-2026-current replacement wording. One row per mapping: `old → new`.
- [ ] **Step 3: Corpus verification** under `## Corpus`: Project Gutenberg IDs + license check for the "Ghosts Before the Shell" texts (*Frankenstein*, *R.U.R.*, *Metropolis* (von Harbou), "Moxon's Master", "The Sandman"). **Known trap:** *Tomorrow's Eve* English translation (Adams, 1982) is under copyright — confirm, and if so drop it or substitute another PD proto-cyborg text; record decision.
- [ ] **Step 4: Claude Code Web setup facts** under `## Claude Code Web setup`: verify the current first-run flow, the "personal access token" option's exact UI wording, and required fine-grained PAT permissions (expect: Contents read/write + Metadata; note whether Pages/Administration permissions are needed for enabling GitHub Pages). Record the GitHub click-path: Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token.
- [ ] **Step 5: Commit** — `git add docs/2026-buildlog.md; git commit -m "content: verified readings, currency, and corpus decisions for 2026"`
- [ ] **Step 6: USER CHECKPOINT** — present the build log to the user as the promised change log; get sign-off (or edits) before Phase C content tasks run.

### Task 5: 2026 syllabus (`index.md`)

**Files:**
- Modify: `index.md` (replace placeholder)

**Interfaces:**
- Consumes: `docs/2026-buildlog.md ## Readings` (chosen articles), streaming availability.
- Produces: the syllabus whose `## `-sections Task 15 (Simple Syllabus) splits; the weekly schedule that links every week file.

- [ ] **Step 1: Write the full syllabus**, structured exactly like `2025/index.md` (same `## ` section names — Course Description, Course Objectives, Materials and Texts, Required Subscriptions, Evaluation and Grading, Asynchronous Online Course Structure, Weekly Schedule) with these changes:
  - Course description rewritten around the GitS frame and units **Ghosts / Shells / Puppet Masters** + coda "The Net Is Vast and Infinite" (spec §3 language).
  - Materials: books = Mitchell, Noble, *The AI Con*, **Tyrangiel *AI for Good*** (drop *Code to Joy*); add **Required Viewing:** GitS (1995) with availability ("as of August 2026: free with ads on Tubi, Plex, Hoopla (free with a public library card); streaming on Prime Video, Hulu, Netflix; rental on Apple TV/Amazon — check current availability") and **Recommended ongoing viewing:** Science SARU's *The Ghost in the Shell* (2026) on Prime Video, new episodes during the semester.
  - Grading table per Global Constraints (6 / 72 / 12 / 10; Activity Verification due Friday, August 28; Final Reflection due Thursday, December 10; Week 14 extra credit).
  - Weekly Schedule: 14 entries from the canonical week table, each listing that week's readings — books per spec §4 pacing (AI Con ch.1–7 → W1–7; Mitchell Parts I–V → W1–5; Noble → W4–8; AI for Good per build-log mapping → W9–14) plus the chosen articles from the build log; link each exercise to its week file. Include the Labor Day note (W3), "due Sunday, November 22, before break" note (W13), and the Thanksgiving-break row (no module, Nov 23–27).
- [ ] **Step 2: Verify** — every week link resolves to a file that will exist (Phase C creates them — dead links acceptable until then, but names must match the canonical table); dates cross-checked against the canonical table; grading sums to 100.
- [ ] **Step 3: Commit** — `git commit -m "content: Fall 2026 syllabus"`

### Task 6: Final reflection page

**Files:**
- Create: `finalreflection.md`

- [ ] **Step 1: Write it** from `2025/finalreflection.md` with: dates updated (due Thursday, December 10, 2026), word count 750–1000 (matches syllabus), coda framing — the three reflective prompts kept but re-inflected through the ghost/shell/agent arc, closing on "the net is vast and infinite." Front matter:

```yaml
---
layout: page
title: Final Reflection
canvas:
  module: "Finals Week: Final Reflection"
  week_start: 2026-12-04
  due: 2026-12-10
  points: 10
  discussion: true
  extra_credit: false
  unit: coda
---
```

- [ ] **Step 2: Commit** — `git commit -m "content: 2026 final reflection"`

---

## Phase C — Week files (Tasks 7–20, one per week)

**Shared recipe for every week task** (deviations listed per task):

1. Start from the named 2025 source file(s) in `2025/`.
2. Front matter: `layout: page`, `title:` = module title, `hide_warning: true`, plus the exact `canvas:` block from the canonical table (`discussion: true`, `extra_credit: false` except W14).
3. Add the week's **GitS epigraph** as a styled blockquote directly under the H1, with the unit badge span above it.
4. Apply the **currency mappings** from `docs/2026-buildlog.md ## Model and tool currency` to every model/tool mention.
5. Copy any image the page still uses from `2025/` to root `images/` and update references to `images/<name>`; drop references to removed content.
6. Keep the `### Discussion` heading EXACTLY (converter contract); update discussion questions to add the week's GitS/theme connection.
7. Verify: front matter parses (`python -c "import frontmatter; frontmatter.load('weekN.md')"` once Task 21 installs deps — before that, visual YAML check); all links/images resolve.
8. Commit: `git commit -m "content: week <N> 2026"`.

### Task 7: Week 1 — Ghosts — Histories (from `2025/weekone.md`)
- Epigraph: Puppet Master, "There is no program called 'me'" — against ELIZA.
- Add a **Required Viewing** section for GitS (1995) before the exercise: availability list (from syllabus), what to watch for (ghosts, shells, the Puppet Master's emergence), note on the 2026 Science SARU series as optional running companion.
- Exercise (three conversations: masswerk ELIZA / Claude / "Future ELIZA") kept; Claude model references updated per build log.
- Discussion adds: introduce yourself + first GitS reaction question (ELIZA vs. the ghost).

### Task 8: Week 2 — Ghosts — Generation (from `2025/weektwo.md`)
- Epigraph: ghost-writing/whispering theme (generated language as a voice with no one behind it).
- Poem-iteration + published-artifact exercise kept; artifact instructions checked against current Claude UI naming.

### Task 9: Week 3 — Ghosts — Sources (from `2025/weekthree.md`)
- Epigraph: the sea of information (Puppet Master's origin) vs. "deep research."
- Update Research-mode naming/screenshots references per build log; replace April 2025 Anthropic quote with current equivalent. Hao reading integrated into the framing paragraph. Labor Day note at top (async week proceeds normally).

### Task 10: Week 4 — Ghosts — Reading (from `2025/weekfour.md`)
- Epigraph: machine reading as a ghost skimming an archive.
- Distant-reading exercise kept (Project Gutenberg text, preprocessing → visualizations); model refs updated; newer Underwood piece woven into discussion.

### Task 11: Week 5 — Shells — Aesthetics (from `2025/weekfive.md`)
- Epigraph: the shelling sequence — a body assembled as imagery. Haraway framing paragraph opens the Shells unit.
- Image-generation exercise kept; tool list updated per build log (current Firefly/Canva/Gemini/Copilot state; drop expired offers).

### Task 12: Week 6 — Shells — Art and Creativity (from `2025/weeksix.md`)
- Epigraph: dolls/gynoids and the crafted surface.
- Archival-images exercise kept (upload set → descriptions, alt-text, visualization artifact); Anadol piece kept or swapped per build log.

### Task 13: Week 7 — Shells — Video and Realism (from `2025/weekseven.md`)
- Epigraph: thermoptic camouflage — synthetic moving images hiding in plain sight.
- Replace 2025 news links with build-log selections; video tools updated (current Veo/Sora tiers, free options); Netflix/El Eternauta and expired Gemini offer removed. Add pointer to the currently-airing Science SARU series as material for the discussion.

### Task 14: Week 8 — Shells — Perceptions (from `2025/weekeight.md`)
- Epigraph: "your effort to remain what you are is what limits you" — communities policing the real.
- AI-images-in-communities investigation kept; news links + Claude model refs updated.

### Task 15: Week 9 — Puppet Masters — Distant Coding (from `2025/weeknine.md`)
- Epigraph: introduce the Puppet Master as agent — code that acts.
- **Dataset switch:** the 100-work JSON dataset is now **cyborg/AI media** (anime, film, fiction, games) instead of generic retro sci-fi; rating/recommendation artifact styling brief switches from "retro sci-fi" to GitS-adjacent cyberpunk. Willison "Here's how I use LLMs…" framing in discussion.

### Task 16: Week 10 — Puppet Masters — Building and Deploying (MERGED, from `2025/weekten.md` + `2025/weekeleven.md`) — 12 points
- Epigraph: fusion — two systems becoming one agent.
- Structure: `## Exercise: Building and Deploying an AI Recommender` with Part One (AI-app rebuild of the Week 9 recommender parsing free-text input, from old weekten) and Part Two (deploy to GitHub Pages via Claude Code for web, from old weekeleven), then single `### Discussion` covering both.
- **Include the full first-run Claude Code Web walkthrough** from `docs/2026-buildlog.md ## Claude Code Web setup`: GitHub Education account → create repo → launch Claude Code Web → **select the "personal access token" option** → generate a fine-grained PAT (click-path, repo selection, permissions, expiration guidance) → paste token → enable Pages. Number the steps; this is the walkthrough later weeks reference.
- Note in page body that this is a double week worth 12 points.

### Task 17: Week 11 — Puppet Masters — Agentic Code (from `2025/weektwelve.md`)
- Epigraph: Stand Alone Complex — coordinated behavior with no originator — for agents that plan/execute/iterate.
- Build-any-site exercise kept (plan mode, `/init`, deploy); references the Week 10 PAT walkthrough instead of re-explaining setup. Willison "Designing agentic loops" + Martin in discussion framing.

### Task 18: Week 12 — Puppet Masters — Local Ghosts (from `2025/weekthirteen.md`)
- Epigraph: a ghost that lives off-network.
- Option 1 Ollama: current local model per build log (replaces DeepSeek-R1 if superseded). Option 2 Claude Code non-code task kept. Lethal-trifecta reading anchors the privacy/security discussion.

### Task 19: Week 13 — Puppet Masters — Distant Reading with and for AI (from `2025/weekfourteen.md`)
- Epigraph: reading at machine scale — the ghost in the archive, revisited.
- Pipeline exercise kept (5–10 Gutenberg texts, sentiment/topics/style + visualization, Web or Desktop options); DH readings from build log in discussion. Deadline note: due Sunday, November 22, before break.

### Task 20: Week 14 — The Net Is Vast and Infinite — Custom Bots, Extra Credit (from `2025/weekfifteen.md`)
- Epigraph: the Puppet Master's merge — "the net is vast and infinite."
- Three tiers kept (Skills up to 6 / subagents up to 6 / fine-tuning up to 10). **Fine-tuning corpus replaced** with "Ghosts Before the Shell" per `docs/2026-buildlog.md ## Corpus` (Gutenberg IDs verified there; dataset-building Colab instructions updated to those source texts). ELIZA + Puppet Master callback framing. `extra_credit: true`, `points: 0` in front matter; page states extra-credit values explicitly.

---

## Phase D — Canvas deployer

### Task 21: Scaffold `canvas/`

**Files:**
- Create: `canvas/requirements.txt`, `canvas/.env.example`, `canvas/course.yml`, `canvas/README.md` (stub: setup + venv + commands), `canvas/tests/__init__.py`
- Modify: `.gitignore` (add `canvas/.env`, `canvas/preview/`, `canvas/.state.json`, `__pycache__/`, `.venv/`)

**Interfaces:**
- Produces: `course.yml` schema all later tasks consume:

```yaml
site_base: "<GitHub Pages URL>"        # derive from `git remote -v` + repo name; verify against _config.yml
timezone: America/New_York
assignment_groups:
  exercises: Exercises
  other: Course Requirements
syllabus_file: ../index.md
weeks: [weekone, weektwo, weekthree, weekfour, weekfive, weeksix, weekseven,
        weekeight, weeknine, weekten, weekeleven, weektwelve, weekthirteen, weekfourteen]
extra: [finalreflection]
activity_verification: {name: "Activity Verification", points: 6, due: 2026-08-28}
```

- [ ] **Step 1: Write the files.** `requirements.txt`:

```
python-frontmatter>=1.1
markdown-it-py>=3.0
PyYAML>=6.0
requests>=2.32
python-dotenv>=1.0
pytest>=8.0
responses>=0.25
```

`.env.example`:

```
CANVAS_API_URL=https://webcourses.ucf.edu
CANVAS_API_TOKEN=paste-token-here
CANVAS_COURSE_ID=000000
```

- [ ] **Step 2: Create venv, install, sanity-check** — `python -m venv .venv; .venv\Scripts\pip install -r canvas/requirements.txt; .venv\Scripts\python -c "import frontmatter, markdown_it, yaml, requests, responses"`
- [ ] **Step 3: Commit** — `git commit -m "chore: scaffold canvas deployer"`

### Task 22: Converter — load, render, rewrite links

**Files:**
- Create: `canvas/converter.py`, `canvas/tests/test_converter.py`

**Interfaces:**
- Produces: `load_week(path) -> WeekDoc` (`.meta: dict`, `.canvas: dict`, `.body: str`, `.path: Path`); `render_html(md_text: str, site_base: str) -> str`; module constants `UNIT_COLORS: dict[str,str]`, `UNIT_LABELS: dict[str,str]` (values from Global Constraints).

- [ ] **Step 1: Write failing tests**

```python
import textwrap
import pytest
from converter import load_week, render_html

def test_load_week_parses_canvas_block(tmp_path):
    f = tmp_path / "weekone.md"
    f.write_text(textwrap.dedent("""\
        ---
        layout: page
        title: "Week One: Ghosts — Histories"
        canvas:
          module: "Week One: Ghosts — Histories"
          week_start: 2026-08-24
          due: 2026-08-30
          points: 6
          discussion: true
          extra_credit: false
          unit: ghosts
        ---
        # Week One
        """), encoding="utf-8")
    doc = load_week(f)
    assert doc.canvas["points"] == 6
    assert doc.canvas["unit"] == "ghosts"
    assert doc.body.startswith("# Week One")

def test_load_week_rejects_missing_keys(tmp_path):
    f = tmp_path / "bad.md"
    f.write_text("---\ncanvas:\n  module: X\n---\nbody", encoding="utf-8")
    with pytest.raises(ValueError, match="due"):
        load_week(f)

def test_render_rewrites_relative_links_and_md_suffix():
    html = render_html("[wk2](weektwo.md) ![e](images/eliza.png)",
                       "https://example.github.io/HumanitiesAI")
    assert 'href="https://example.github.io/HumanitiesAI/weektwo.html"' in html
    assert 'src="https://example.github.io/HumanitiesAI/images/eliza.png"' in html

def test_render_leaves_absolute_and_anchor_links():
    html = render_html("[a](https://claude.ai) [b](#discussion)", "https://x.y")
    assert 'href="https://claude.ai"' in html
    assert 'href="#discussion"' in html
```

- [ ] **Step 2: Create `canvas/pytest.ini` then run to verify failure**

```ini
[pytest]
pythonpath = .
testpaths = tests
```

Run from `canvas/`: `..\.venv\Scripts\python -m pytest -v`. Expected: ImportError/FAIL. (All later pytest steps run from `canvas/` the same way; Task 27 documents this in the README.)
- [ ] **Step 3: Implement**

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import frontmatter
from markdown_it import MarkdownIt

UNIT_COLORS = {"ghosts": "#0f766e", "shells": "#b45309",
               "puppetmasters": "#365314", "coda": "#475569"}
UNIT_LABELS = {"ghosts": "Ghosts", "shells": "Shells",
               "puppetmasters": "Puppet Masters",
               "coda": "The Net Is Vast and Infinite"}

REQUIRED_KEYS = ("module", "week_start", "due", "points", "discussion", "unit")

_md = MarkdownIt("commonmark", {"html": True}).enable("table")


@dataclass
class WeekDoc:
    path: Path
    meta: dict
    canvas: dict
    body: str


def load_week(path) -> WeekDoc:
    post = frontmatter.load(str(path))
    canvas = post.metadata.get("canvas")
    if not isinstance(canvas, dict):
        raise ValueError(f"{path}: missing 'canvas' front matter block")
    missing = [k for k in REQUIRED_KEYS if k not in canvas]
    if missing:
        raise ValueError(f"{path}: canvas block missing {', '.join(missing)}")
    return WeekDoc(Path(path), post.metadata, canvas, post.content)


def _rewrite(html: str, site_base: str) -> str:
    base = site_base.rstrip("/")

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#|data:|//)", url):
            return m.group(0)
        url = re.sub(r"\.md(?=(#|$))", ".html", url)
        return f'{attr}="{base}/{url.lstrip("./")}"'

    return re.sub(r'(href|src)="([^"]+)"', fix, html)


def render_html(md_text: str, site_base: str) -> str:
    return _rewrite(_md.render(md_text), site_base)
```

- [ ] **Step 4: Run tests** — Expected: 4 PASS.
- [ ] **Step 5: Commit** — `git commit -m "feat: canvas converter core (load, render, link rewrite)"`

### Task 23: Converter — discussion split, due dates, canvas styling

**Files:**
- Modify: `canvas/converter.py`
- Test: `canvas/tests/test_converter.py` (append)

**Interfaces:**
- Produces: `split_discussion(md_text) -> tuple[str, str]`; `due_at_utc(due_date: datetime.date) -> str`; `apply_canvas_style(html: str, unit: str) -> str`.

- [ ] **Step 1: Write failing tests**

```python
from datetime import date
from converter import split_discussion, due_at_utc, apply_canvas_style

def test_split_discussion():
    page, disc = split_discussion("intro\n\n### Discussion\n\nQ1?\nQ2?")
    assert page == "intro"
    assert disc == "Q1?\nQ2?"

def test_split_without_discussion_returns_empty():
    page, disc = split_discussion("intro only")
    assert (page, disc) == ("intro only", "")

def test_due_at_utc_handles_dst_fallback():
    # EDT (UTC-4): Oct 25 23:59 ET -> Oct 26 03:59Z
    assert due_at_utc(date(2026, 10, 25)) == "2026-10-26T03:59:00Z"
    # EST (UTC-5): Nov 1 2026 is the fallback day; 23:59 ET -> 04:59Z
    assert due_at_utc(date(2026, 11, 1)) == "2026-11-02T04:59:00Z"

def test_apply_canvas_style_bands_and_badges():
    out = apply_canvas_style("<p>x</p>", "shells")
    assert "border-top: 6px solid #b45309" in out
    assert ">Shells</span>" in out
    assert out.endswith("<p>x</p>")
```

- [ ] **Step 2: Run to verify failure** — Expected: ImportError on new names.
- [ ] **Step 3: Implement** (append to converter.py)

```python
from datetime import datetime, time
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/New_York")
_DISCUSSION_RE = re.compile(r"^### Discussion[ \t]*$", re.MULTILINE)


def split_discussion(md_text: str) -> tuple[str, str]:
    m = _DISCUSSION_RE.search(md_text)
    if not m:
        return md_text.strip(), ""
    return md_text[: m.start()].strip(), md_text[m.end():].strip()


def due_at_utc(due_date) -> str:
    dt = datetime.combine(due_date, time(23, 59), tzinfo=TZ)
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")


def apply_canvas_style(html: str, unit: str) -> str:
    color, label = UNIT_COLORS[unit], UNIT_LABELS[unit]
    band = (
        f'<div style="border-top: 6px solid {color}; padding: 12px 0 4px 0; '
        f'margin-bottom: 16px;"><span style="display: inline-block; '
        f'padding: 2px 10px; border-radius: 9999px; background: {color}; '
        f'color: #ffffff; font-size: 12px; letter-spacing: 1px; '
        f'text-transform: uppercase;">{label}</span></div>'
    )
    return band + html
```

- [ ] **Step 4: Run tests** — Expected: all PASS.
- [ ] **Step 5: Commit** — `git commit -m "feat: discussion split, due dates, canvas inline styling"`

### Task 24: Canvas API client

**Files:**
- Create: `canvas/canvas_client.py`, `canvas/tests/test_canvas_client.py`

**Interfaces:**
- Produces: `CanvasClient(base_url, token, course_id)` with methods:
  - `upsert_module(name: str) -> int`
  - `upsert_page(title: str, body: str, published: bool = False) -> str`  (returns page url slug)
  - `upsert_assignment_group(name: str) -> int`
  - `upsert_discussion(title: str, message: str, points: int, due_at: str | None, assignment_group_id: int, published: bool = False, known_id: int | None = None) -> int`
  - `add_to_module(module_id: int, item_type: str, ref: int | str) -> None`  (item_type "Page" uses page_url; "Discussion" uses content_id; skips if an identical item exists)

- [ ] **Step 1: Write failing tests** (using `responses`)

```python
import responses
from canvas_client import CanvasClient

BASE = "https://webcourses.ucf.edu/api/v1/courses/123"

def client():
    return CanvasClient("https://webcourses.ucf.edu", "tok", "123")

@responses.activate
def test_upsert_module_finds_existing():
    responses.get(f"{BASE}/modules", json=[{"id": 7, "name": "Week One"}])
    assert client().upsert_module("Week One") == 7

@responses.activate
def test_upsert_module_creates_when_missing():
    responses.get(f"{BASE}/modules", json=[])
    responses.post(f"{BASE}/modules", json={"id": 9, "name": "Week Two"})
    assert client().upsert_module("Week Two") == 9

@responses.activate
def test_upsert_discussion_updates_known_id():
    responses.put(f"{BASE}/discussion_topics/42", json={"id": 42})
    got = client().upsert_discussion("T", "<p>m</p>", 6,
                                     "2026-08-31T03:59:00Z", 5, known_id=42)
    assert got == 42

@responses.activate
def test_upsert_discussion_creates_graded():
    responses.get(f"{BASE}/discussion_topics", json=[])
    rsp = responses.post(f"{BASE}/discussion_topics", json={"id": 43})
    assert client().upsert_discussion("T", "<p>m</p>", 6,
                                      "2026-08-31T03:59:00Z", 5) == 43
    import json as j
    sent = j.loads(rsp.calls[0].request.body)
    assert sent["assignment"]["points_possible"] == 6
    assert sent["assignment"]["assignment_group_id"] == 5
    assert sent["published"] is False
```

- [ ] **Step 2: Run to verify failure.**
- [ ] **Step 3: Implement**

```python
from __future__ import annotations

import requests


class CanvasClient:
    def __init__(self, base_url: str, token: str, course_id: str, session=None):
        self.course = f"{base_url.rstrip('/')}/api/v1/courses/{course_id}"
        self.s = session or requests.Session()
        self.s.headers["Authorization"] = f"Bearer {token}"

    def _get_all(self, url: str, **params) -> list:
        out, params = [], {"per_page": 100, **params}
        while url:
            r = self.s.get(url, params=params)
            r.raise_for_status()
            out.extend(r.json())
            url = r.links.get("next", {}).get("url")
            params = {}
        return out

    def _post(self, url: str, payload: dict) -> dict:
        r = self.s.post(url, json=payload)
        r.raise_for_status()
        return r.json()

    def _put(self, url: str, payload: dict) -> dict:
        r = self.s.put(url, json=payload)
        r.raise_for_status()
        return r.json()

    def upsert_module(self, name: str) -> int:
        for m in self._get_all(f"{self.course}/modules"):
            if m["name"] == name:
                return m["id"]
        return self._post(f"{self.course}/modules", {"module": {"name": name}})["id"]

    def upsert_page(self, title: str, body: str, published: bool = False) -> str:
        payload = {"wiki_page": {"title": title, "body": body, "published": published}}
        for p in self._get_all(f"{self.course}/pages", search_term=title):
            if p["title"] == title:
                return self._put(f"{self.course}/pages/{p['url']}", payload)["url"]
        return self._post(f"{self.course}/pages", payload)["url"]

    def upsert_assignment_group(self, name: str) -> int:
        for g in self._get_all(f"{self.course}/assignment_groups"):
            if g["name"] == name:
                return g["id"]
        return self._post(f"{self.course}/assignment_groups", {"name": name})["id"]

    def upsert_discussion(self, title: str, message: str, points: int,
                          due_at: str | None, assignment_group_id: int,
                          published: bool = False,
                          known_id: int | None = None) -> int:
        payload = {
            "title": title, "message": message, "published": published,
            "assignment": {"points_possible": points, "due_at": due_at,
                           "assignment_group_id": assignment_group_id},
        }
        if known_id is None:
            for d in self._get_all(f"{self.course}/discussion_topics"):
                if d["title"] == title:
                    known_id = d["id"]
                    break
        if known_id is not None:
            return self._put(f"{self.course}/discussion_topics/{known_id}", payload)["id"]
        return self._post(f"{self.course}/discussion_topics", payload)["id"]

    def add_to_module(self, module_id: int, item_type: str, ref) -> None:
        items = self._get_all(f"{self.course}/modules/{module_id}/items")
        if item_type == "Page":
            if any(i.get("page_url") == ref for i in items):
                return
            item = {"type": "Page", "page_url": ref}
        else:
            if any(i.get("content_id") == ref and i["type"] == item_type for i in items):
                return
            item = {"type": item_type, "content_id": ref}
        self._post(f"{self.course}/modules/{module_id}/items", {"module_item": item})
```

- [ ] **Step 4: Run tests** — Expected: all PASS. (Note: `responses` matches GET query params loosely by default; if the `search_term` GET in `upsert_page` tests fails on matching, register with `match_querystring=False` semantics via `responses.get(url, json=...)` which ignores params.)
- [ ] **Step 5: Commit** — `git commit -m "feat: canvas API client with idempotent upserts"`

### Task 25: `deploy.py` CLI with dry-run and state file

**Files:**
- Create: `canvas/deploy.py`, `canvas/tests/test_deploy.py`

**Interfaces:**
- Consumes: everything from Tasks 22–24; `course.yml` from Task 21.
- Produces: CLI `python deploy.py [--all | --week NAME] [--dry-run] [--publish] [--simple-syllabus]`; state file `canvas/.state.json` (`{ "<file stem>": {"module_id": int, "page_url": str, "discussion_id": int} }`); dry-run previews in `canvas/preview/<week>.html` and `<week>-discussion.html`.

- [ ] **Step 1: Write failing tests**

```python
import json
from pathlib import Path
import deploy

def test_plan_week_builds_operations(tmp_path, monkeypatch):
    wk = tmp_path / "weekone.md"
    wk.write_text(
        "---\nlayout: page\ntitle: T\ncanvas:\n"
        "  module: \"Week One: Ghosts — Histories\"\n"
        "  week_start: 2026-08-24\n  due: 2026-08-30\n  points: 6\n"
        "  discussion: true\n  extra_credit: false\n  unit: ghosts\n---\n"
        "Body\n\n### Discussion\n\nQ?\n", encoding="utf-8")
    plan = deploy.plan_week(wk, site_base="https://x.y")
    assert plan["module"] == "Week One: Ghosts — Histories"
    assert plan["points"] == 6
    assert plan["due_at"] == "2026-08-31T03:59:00Z"
    assert "border-top" in plan["page_html"]
    assert "Q?" in plan["discussion_html"]

def test_dry_run_writes_previews_and_no_network(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "course.yml").write_text(
        "site_base: https://x.y\ntimezone: America/New_York\n"
        "assignment_groups: {exercises: Exercises, other: Course Requirements}\n"
        "syllabus_file: index.md\nweeks: [weekone]\nextra: []\n", encoding="utf-8")
    (tmp_path / "weekone.md").write_text(
        "---\ntitle: T\ncanvas:\n  module: M1\n  week_start: 2026-08-24\n"
        "  due: 2026-08-30\n  points: 6\n  discussion: true\n"
        "  extra_credit: false\n  unit: ghosts\n---\nBody\n\n### Discussion\n\nQ?\n",
        encoding="utf-8")
    deploy.main(["--all", "--dry-run"])
    assert (tmp_path / "preview" / "weekone.html").exists()
    out = capsys.readouterr().out
    assert "[dry-run]" in out and "M1" in out
```

- [ ] **Step 2: Run to verify failure.**
- [ ] **Step 3: Implement**

```python
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from converter import (apply_canvas_style, due_at_utc, load_week,
                       render_html, split_discussion)

STATE_FILE = Path(".state.json")


def plan_week(path: Path, site_base: str) -> dict:
    doc = load_week(path)
    c = doc.canvas
    page_md, disc_md = split_discussion(doc.body)
    return {
        "stem": path.stem,
        "module": c["module"],
        "points": int(c["points"]),
        "extra_credit": bool(c.get("extra_credit", False)),
        "due_at": due_at_utc(c["due"]),
        "has_discussion": bool(c["discussion"]) and bool(disc_md),
        "page_html": apply_canvas_style(render_html(page_md, site_base), c["unit"]),
        "discussion_html": apply_canvas_style(render_html(disc_md, site_base), c["unit"])
        if disc_md else "",
    }


def _load_state() -> dict:
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}


def _course_root(cfg: dict) -> Path:
    # week files live one directory above canvas/ when run in-place,
    # or in cwd when tests fabricate a flat layout
    for base in (Path("."), Path("..")):
        if (base / (cfg["weeks"][0] + ".md")).exists():
            return base
    raise FileNotFoundError("week files not found relative to cwd")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--week")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--simple-syllabus", action="store_true")
    args = ap.parse_args(argv)

    cfg = yaml.safe_load(Path("course.yml").read_text(encoding="utf-8"))
    root = _course_root(cfg)
    stems = cfg["weeks"] + cfg.get("extra", []) if args.all else [args.week]
    if not stems or stems == [None]:
        ap.error("pass --all or --week NAME")

    if args.simple_syllabus:
        from simple_syllabus import build_package
        out = build_package(root / cfg["syllabus_file"], Path("preview"))
        print(f"simple syllabus package: {out}")
        return 0

    plans = [plan_week(root / f"{s}.md", cfg["site_base"]) for s in stems]

    if args.dry_run:
        prev = Path("preview")
        prev.mkdir(exist_ok=True)
        for p in plans:
            (prev / f"{p['stem']}.html").write_text(p["page_html"], encoding="utf-8")
            if p["has_discussion"]:
                (prev / f"{p['stem']}-discussion.html").write_text(
                    p["discussion_html"], encoding="utf-8")
            print(f"[dry-run] module '{p['module']}' | page | "
                  f"discussion {p['points']}pts due {p['due_at']}"
                  + (" [extra credit]" if p["extra_credit"] else ""))
        return 0

    load_dotenv()
    from canvas_client import CanvasClient
    client = CanvasClient(os.environ["CANVAS_API_URL"],
                          os.environ["CANVAS_API_TOKEN"],
                          os.environ["CANVAS_COURSE_ID"])
    state = _load_state()
    group_id = client.upsert_assignment_group(cfg["assignment_groups"]["exercises"])
    for p in plans:
        st = state.setdefault(p["stem"], {})
        module_id = client.upsert_module(p["module"])
        page_url = client.upsert_page(p["module"], p["page_html"], args.publish)
        client.add_to_module(module_id, "Page", page_url)
        st.update(module_id=module_id, page_url=page_url)
        if p["has_discussion"]:
            title = f"Exercise Discussion: {p['module']}"
            disc_id = client.upsert_discussion(
                title, p["discussion_html"],
                0 if p["extra_credit"] else p["points"],
                p["due_at"], group_id, args.publish,
                known_id=st.get("discussion_id"))
            client.add_to_module(module_id, "Discussion", disc_id)
            st["discussion_id"] = disc_id
        print(f"deployed: {p['module']}")
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests** — Expected: PASS (the `--simple-syllabus` import lands in Task 26; tests here don't touch it).
- [ ] **Step 5: Full dry-run over the real course** — from `canvas/`: `..\.venv\Scripts\python deploy.py --all --dry-run`. Expected: 15 `[dry-run]` lines (14 weeks + finalreflection), previews written; open two previews and eyeball the band/badge and rewritten links.
- [ ] **Step 6: Commit** — `git commit -m "feat: deploy CLI with dry-run, state file"`

### Task 26: Simple Syllabus package generator + course-level items

**Files:**
- Create: `canvas/simple_syllabus.py`, `canvas/tests/test_simple_syllabus.py`
- Modify: `canvas/deploy.py` (course-level deploy: syllabus page, activity verification)

**Interfaces:**
- Produces: `build_package(index_md: Path, out_dir: Path) -> Path` — writes `preview/simple_syllabus.html`, one labeled `<section>` per `## ` heading of index.md, paste-ready. Deploy gains: syllabus page upsert (Canvas page titled "Syllabus" from index.md) and Activity Verification assignment (6 pts, due per course.yml, `submission_types: ["online_url","online_text_entry"]` shell created as a plain assignment via `POST /assignments` — add `upsert_assignment` to CanvasClient mirroring `upsert_discussion`).

- [ ] **Step 1: Write failing tests**

```python
from pathlib import Path
from simple_syllabus import build_package

def test_build_package_sections(tmp_path):
    idx = tmp_path / "index.md"
    idx.write_text("---\ntitle: X\n---\nintro\n\n## Course Description\n\nBody A\n\n"
                   "## Evaluation and Grading\n\n| a | b |\n|---|---|\n| 1 | 2 |\n",
                   encoding="utf-8")
    out = build_package(idx, tmp_path / "preview")
    html = out.read_text(encoding="utf-8")
    assert "<h2>Course Description</h2>" in html
    assert "Body A" in html and "<table>" in html
    assert 'data-component="Evaluation and Grading"' in html
```

- [ ] **Step 2: Run to verify failure.**
- [ ] **Step 3: Implement**

```python
from __future__ import annotations

import re
from pathlib import Path

import frontmatter
from markdown_it import MarkdownIt

_md = MarkdownIt("commonmark", {"html": True}).enable("table")

def build_package(index_md: Path, out_dir: Path) -> Path:
    post = frontmatter.load(str(index_md))
    parts = re.split(r"^## +(.+)$", post.content, flags=re.MULTILINE)
    # parts = [preamble, title1, body1, title2, body2, ...]
    sections = []
    for i in range(1, len(parts), 2):
        title, body = parts[i].strip(), parts[i + 1]
        sections.append(
            f'<section data-component="{title}">\n<h2>{title}</h2>\n'
            f"{_md.render(body)}\n</section>\n<hr>")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "simple_syllabus.html"
    out.write_text(
        "<!-- Paste each <section> into the matching Simple Syllabus component -->\n"
        + "\n".join(sections), encoding="utf-8")
    return out
```

- [ ] **Step 4: Add `upsert_assignment` to CanvasClient** (same find-by-title-then-PUT-else-POST shape as `upsert_discussion`, endpoint `/assignments`, payload `{"assignment": {"name":…, "points_possible":…, "due_at":…, "assignment_group_id":…, "submission_types": […], "published":…}}`) with one responses-based test each for create and update; wire syllabus page + activity verification into `deploy.py` `--all` runs using `cfg["activity_verification"]` and `cfg["assignment_groups"]["other"]`.
- [ ] **Step 5: Run all canvas tests** — `pytest canvas/tests -v`, Expected: all PASS.
- [ ] **Step 6: Regenerate dry-run + simple syllabus package**; eyeball `preview/simple_syllabus.html`.
- [ ] **Step 7: Commit** — `git commit -m "feat: simple syllabus package, course-level deploy items"`

### Task 27: Deployer docs + final verification sweep

**Files:**
- Modify: `canvas/README.md`
- Create: none

- [ ] **Step 1: Write the README**: setup (venv, requirements, `.env` from `.env.example`, where to get a Canvas token: Webcourses → Account → Settings → New Access Token), command reference (`--all/--week/--dry-run/--publish/--simple-syllabus`), the deploy order (dry-run → deploy unpublished → review in Canvas → `--publish`), Simple Syllabus procedure (browser session primary / paste fallback), state-file explanation, troubleshooting (401 = token, 404 = course id, partial failure = rerun safely).
- [ ] **Step 2: Full verification sweep**: `pytest canvas/tests -v` all green; `deploy.py --all --dry-run` produces 15 previews with no warnings; every week file front matter loads via `load_week`; every `[…](…)` link in the 14 week files + index resolves (script the check with a short Python loop over regex matches, checking local paths exist); Jekyll build green if available, else push and confirm the Pages action passes.
- [ ] **Step 3: Commit** — `git commit -m "docs: canvas deployer guide + verification sweep"`

---

## Deferred tasks (blocked on user-provided credentials / SSO)

**D1 — Live Canvas deploy:** user supplies `.env` values → `deploy.py --all` (unpublished) → user reviews modules in Webcourses → fix/re-run as needed → `deploy.py --all --publish`.

**D2 — Simple Syllabus session:** user logs into Webcourses in Chrome and opens the course's Simple Syllabus editor → Claude drives the browser (Claude-in-Chrome) filling instructor-editable components from `preview/simple_syllabus.html` → user reviews before submit. Fallback: section-by-section manual paste from the same file. Confirm instructor-editable components at session start.
