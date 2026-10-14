# ENG 3861 Canvas Handoff Build — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy the undergrad course (`undergrad/`) to a new Canvas shell so that it is **self-contained**. The GTA teaching it must be able to run and edit everything from Canvas and PowerPoint, with no access to this repo or the website. That means lecture slides ship as editable `.pptx` files in Canvas Files, not iframes of the reveal.js decks.

**Architecture:** A new `build_pptx.py` reads the same `undergrad/slides/decks.yml` as `build_decks.py` and writes one native, editable `.pptx` per module: real text boxes, real bullets, embedded images with alt text, and speaker notes. The shared deployer in `canvas/` gets a `self_contained: true` mode, switched on per course in `course.yml`. That mode uploads the decks and page images to Canvas Files, reserves every page so its Canvas URL is known, and then rewrites every repo-relative link (`moduleone.md`, `slides/moduleone.html`, `images/x.png`, `index.md#ai-use-policy`) to the matching Canvas URL. It fails the deploy if any link would still point at the website. A Canvas-edit guard skips any page, discussion, or file whose Canvas `updated_at` changed since the last deploy, so a redeploy can never overwrite the GTA's edits.

**Tech Stack:** Python 3.13 (repo `.venv`), python-pptx 1.0.2 and Pillow (already installed), PyYAML, python-frontmatter, markdown-it-py, requests, pytest and responses. PowerPoint desktop (installed) is used only for the visual review export.

**Spec:** This plan, plus `undergrad/README.md` § "Before the first Canvas deploy" (the four deployer changes listed there are Tasks 1–2 here).

## Global Constraints

- **The grad course must not change.** `canvas/course.yml` has none of the new keys, and every new behavior is off when its key is missing. All existing tests in `canvas/tests/` must pass unchanged, except where a task says it updates one.
- **Self-contained means zero website dependencies** in the undergrad Canvas content. That means no `anastasiasalter.net` iframe, `src`, or `href` that comes from a repo-relative path. Absolute links to outside sources (readings, YouTube) are fine.
- **Verified quotes are sacred.** Every quote in `decks.yml` was checked word for word. The PPTX text must equal the YAML text after inline markup is stripped, and a test enforces this.
- **Fonts must exist on stock Windows and Mac Office**, because python-pptx cannot embed fonts. Use Arial Black for titles and stickers, Verdana for body text, and Courier New for terminal and prompt text. Colors come from `undergrad/slides/undergrad-slides.css`: paper `#FFF7E3`, ink `#1B1035`, ink-soft `#4A3F66`, pink `#FF3D7F`, blue `#2E5BFF`, yellow `#FFD23F`, mint `#00B894`, orange `#FF7A1A`. The unit colors are words=blue, images=pink, code=mint, coda=orange.
- **Slide size is 16:9, 13.333 × 7.5 in.**
- **Canvas objects are created unpublished** unless `--publish` is passed. The Instructor Guide page is **never** published, even with `--publish`.
- **Never commit `.env`.** The undergrad credentials live in `undergrad/canvas/.env`, which is already gitignored.
- **The deployer runs from `undergrad/canvas/`** as `..\..\.venv\Scripts\python ..\..\canvas\deploy.py ...`.
- **Late window:** the undergrad discussions lock `late_window_hours: 24` after the Sunday 11:59 PM ET due date, and that includes the final.

## Review Focus

1. **A redeploy after the GTA has edited something in Canvas** must skip that item and print `[edited in Canvas]`. It must never overwrite it, and that goes for a page, a discussion, and a re-uploaded PPTX. The tests are in Task 6.
2. **A PPTX that is older than `decks.yml`**, meaning someone edited the YAML and forgot to rebuild, must stop the deploy with a message saying to run `build_pptx.py`. The test is in Task 5.
3. **A repo-relative link with no Canvas target**, such as a new image added to a module page, must fail the self-contained deploy and name the file and the link. It must not fall back silently to the website. The test is in Task 2.
4. **The `.env` from the wrong course:** running from `undergrad/canvas/` must never load `canvas/.env`, the grad course. If the target course's `course_code` doesn't contain `expect_course_code`, the deploy aborts before writing anything. The tests are in Tasks 1 and 4.
5. **Syllabus TOC anchors and `index.md#ai-use-policy`** must still resolve inside Canvas. Headings need kramdown-compatible ids. The test is in Task 2.

---

## File Structure

| File | Responsibility |
| --- | --- |
| `canvas/converter.py` (modify) | Units from config, the hour-based late window, kramdown heading ids, link-map rewriting with unresolved-link reporting, and removing the `unit-badge` span |
| `canvas/canvas_client.py` (modify) | `upload_file`, `find_or_create_page`, `updated_at`, `course_info` |
| `canvas/assets.py` (create) | The self-contained asset sync: find the PPTX and image assets, check that decks are fresh, upload with the edit guard, reserve pages, and build the link map |
| `canvas/deploy.py` (modify) | Wires config, the cwd `.env`, the course-code guard, the self-contained lecture page (PPTX preview and download plus a module File item), the edit guard, and the Instructor Guide |
| `canvas/tests/test_assets.py` (create) | Tests for `assets.py` |
| `undergrad/slides/build_pptx.py` (create) | `decks.yml` → `<stem>.pptx` |
| `undergrad/slides/test_build_pptx.py` (create) | PPTX structure and quote-fidelity tests |
| `undergrad/slides/export_pngs.ps1` (create) | Exports every slide to PNG through PowerPoint for visual review |
| `undergrad/canvas/course.yml` (modify) | `self_contained`, `expect_course_code`, `instructor_guide` |
| `undergrad/canvas/instructor-guide.md` (create) | The GTA-facing how-to that becomes the unpublished Canvas page |
| `undergrad/README.md`, `canvas/README.md` (modify) | Document the new mode and the handoff rule |

`*.pptx` under `undergrad/slides/` is **committed**. The decks are the deliverable, and the GTA may get them by download as well as through Canvas.

---

### Task 1: Config-driven deployer basics (units, 24-hour window, cwd `.env`)

**Files:**
- Modify: `canvas/converter.py` (UNIT tables, `lock_at_utc`, `apply_canvas_style`)
- Modify: `canvas/deploy.py` (`main`: config load, `load_dotenv`, `plan_week` lock logic)
- Test: `canvas/tests/test_converter.py`, `canvas/tests/test_deploy.py`

**Interfaces:**
- Produces: `converter.configure_units(units: dict | None) -> None`, `converter.lock_at_utc(due_date, grace_days: int = 7, grace_hours: int | None = None) -> str`, and `deploy.plan_week(path, site_base, syllabus_md="", *, late_hours: int | None = None, link_map=None, slides=None, unresolved=None) -> dict`. The last three keyword arguments are wired in Tasks 2 and 5. Accept them now and ignore them.

- [ ] **Step 1: Write the failing tests** (append to `canvas/tests/test_converter.py`)

```python
from converter import configure_units, UNIT_COLORS, UNIT_LABELS, lock_at_utc, apply_canvas_style
from datetime import date

def test_configure_units_merges_course_units():
    configure_units({"words": {"label": "Words", "color": "#0f766e"}})
    assert UNIT_COLORS["words"] == "#0f766e" and UNIT_LABELS["words"] == "Words"
    assert "ghosts" in UNIT_COLORS  # grad units untouched

def test_lock_at_utc_hour_window():
    # Sunday Jan 24 2027 23:59 ET + 24h = Mon Jan 25 23:59 ET = Jan 26 04:59Z
    assert lock_at_utc(date(2027, 1, 24), grace_hours=24) == "2027-01-26T04:59:00Z"

def test_apply_canvas_style_drops_site_unit_badge():
    configure_units({"words": {"label": "Words", "color": "#0f766e"}})
    html = apply_canvas_style('<p><span class="unit-badge unit-badge--words">Words</span></p><p>Hi</p>', "words")
    assert "unit-badge" not in html and html.count("Words") == 1
```

Append to `canvas/tests/test_deploy.py`:

```python
def test_plan_week_uses_late_hours(tmp_path):
    wk = tmp_path / "moduleone.md"
    wk.write_text("---\ncanvas:\n  module: \"Module One: X\"\n  week_start: 2027-01-11\n"
                  "  due: 2027-01-24\n  points: 10\n  discussion: true\n  unit: ghosts\n"
                  "  hard_close: true\n---\nBody\n\n### Discussion\n\nQ?\n", encoding="utf-8")
    plan = deploy.plan_week(wk, site_base="https://x.y", late_hours=24)
    assert plan["lock_at"] == "2027-01-26T04:59:00Z"   # hours win over hard_close

def test_main_loads_env_from_cwd_only(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(deploy, "load_dotenv", lambda *a, **k: calls.append(a))
    monkeypatch.chdir(tmp_path)
    # minimal course; no env -> KeyError after load_dotenv is called
    (tmp_path / "course.yml").write_text(
        "site_base: https://x.y\nassignment_groups: {exercises: E, other: O}\n"
        "syllabus_file: index.md\nweeks: [weekone]\n", encoding="utf-8")
    (tmp_path / "weekone.md").write_text(
        "---\ncanvas:\n  module: M1\n  week_start: 2030-01-07\n  due: 2030-01-13\n"
        "  points: 6\n  discussion: false\n  unit: ghosts\n---\nBody\n", encoding="utf-8")
    for k in ("CANVAS_API_URL", "CANVAS_API_TOKEN", "CANVAS_COURSE_ID"):
        monkeypatch.delenv(k, raising=False)
    try:
        deploy.main(["--all"])
    except KeyError:
        pass
    assert calls and Path(calls[0][0]) == tmp_path / ".env"
```

- [ ] **Step 2: Run them to verify they fail**

Run (from `canvas/`): `..\.venv\Scripts\python -m pytest tests -k "configure_units or hour_window or unit_badge or late_hours or env_from_cwd" -v`
Expected: FAIL (ImportError for `configure_units`, TypeError for `grace_hours`/`late_hours`)

- [ ] **Step 3: Implement**

In `canvas/converter.py`:

```python
def configure_units(units: dict | None) -> None:
    """Merge a course.yml `units:` block into the unit tables (in place,
    so modules that imported UNIT_COLORS by name see the change)."""
    for key, u in (units or {}).items():
        UNIT_COLORS[key] = u["color"]
        UNIT_LABELS[key] = u["label"]


def lock_at_utc(due_date, grace_days: int = 7, grace_hours: int | None = None) -> str:
    """Hard close after the due date: grace_hours if given, else grace_days."""
    due = datetime.combine(due_date, time(23, 59), tzinfo=TZ)
    dt = due + (timedelta(hours=grace_hours) if grace_hours is not None
                else timedelta(days=grace_days))
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")

_BADGE_RE = re.compile(r'<span class="unit-badge[^"]*">[^<]*</span>\s*')
```

Then, as the first line of `apply_canvas_style`, add `html = _BADGE_RE.sub("", html)` (the Canvas band already shows the unit label).

In `canvas/deploy.py`:
- Change the `plan_week` signature to `def plan_week(path, site_base, syllabus_md="", *, late_hours=None, link_map=None, slides=None, unresolved=None):`
- Replace the `"lock_at"` line with:

```python
        "lock_at": (lock_at_utc(c["due"], grace_hours=late_hours) if late_hours is not None
                    else due_at_utc(c["due"]) if c.get("hard_close")
                    else lock_at_utc(c["due"])),
```

- In `main`, right after `cfg = yaml.safe_load(...)`, add `configure_units(cfg.get("units"))` and `late_hours = cfg.get("late_window_hours")`. Pass `late_hours=late_hours` into every `plan_week` call. Import `configure_units`.
- Replace `load_dotenv()` with `load_dotenv(Path.cwd() / ".env")`. The grad course runs from `canvas/`, so it still finds `canvas/.env`.
- Apply the AV `lock_at` the same way: `lock_at_utc(av["due"], grace_hours=late_hours) if late_hours is not None else lock_at_utc(av["due"])`.

- [ ] **Step 4: Run the full suite**

Run (from `canvas/`): `..\.venv\Scripts\python -m pytest -q`
Expected: all pass (the old tests included)

- [ ] **Step 5: Remove the units patch note and commit**

Remove from `undergrad/canvas/course.yml` the comment lines that say the converter and deployer "need" these changes. Keep the keys.

```bash
git add canvas/converter.py canvas/deploy.py canvas/tests undergrad/canvas/course.yml
git commit -m "canvas: units, late window, and .env come from the course folder"
```

---

### Task 2: Heading ids and link-map rewriting

**Files:**
- Modify: `canvas/converter.py` (`_rewrite`, `render_html`)
- Test: `canvas/tests/test_converter.py`

**Interfaces:**
- Produces: `converter.kramdown_id(text: str) -> str` and `converter.render_html(md_text, site_base, link_map: dict[str, str] | None = None, unresolved: list[str] | None = None) -> str`. Link-map keys are repo-relative paths **after** `.md` → `.html` (e.g. `"moduleone.html"`, `"index.html"`, `"slides/moduleone.html"`, `"images/voyant-frankenstein.png"`). Values are Canvas paths such as `"/courses/123/pages/module-one-what-is-digital-humanities"`. Fragments (`#ai-use-policy`) are kept. When `link_map` is given and a relative path is missing from it, the path is appended to `unresolved` and still rewritten to `site_base`, so dry-run previews keep working.

- [ ] **Step 1: Write the failing tests**

```python
from converter import kramdown_id, render_html

def test_kramdown_id_matches_jekyll_toc():
    assert kramdown_id("Module One: What Is Digital Humanities? (Weeks 1-2, January 11 - 24)") \
        == "module-one-what-is-digital-humanities-weeks-1-2-january-11---24"
    assert kramdown_id("AI Use Policy") == "ai-use-policy"

def test_render_adds_heading_ids():
    assert '<h2 id="ai-use-policy">AI Use Policy</h2>' in render_html("## AI Use Policy", "https://x.y")

def test_link_map_rewrites_and_keeps_fragment():
    m = {"index.html": "/courses/9/pages/syllabus", "slides/moduleone.html": "/courses/9/files/77"}
    out = render_html("[p](index.md#ai-use-policy) [s](slides/moduleone.html)", "https://x.y", link_map=m)
    assert 'href="/courses/9/pages/syllabus#ai-use-policy"' in out
    assert 'href="/courses/9/files/77"' in out

def test_link_map_reports_unresolved():
    bad = []
    out = render_html("![a](images/new.png)", "https://x.y", link_map={}, unresolved=bad)
    assert bad == ["images/new.png"] and 'src="https://x.y/images/new.png"' in out

def test_no_link_map_is_unchanged_grad_behavior():
    assert 'href="https://x.y/weektwo.html"' in render_html("[w](weektwo.md)", "https://x.y")
```

- [ ] **Step 2: Run them to verify they fail**

Run: `..\.venv\Scripts\python -m pytest tests/test_converter.py -v`
Expected: the 5 new tests FAIL

- [ ] **Step 3: Implement**

```python
import html as _html

def kramdown_id(text: str) -> str:
    """Jekyll/kramdown auto_ids, so syllabus TOC links work in Canvas."""
    t = re.sub(r"^[^a-zA-Z]+", "", text)
    t = re.sub(r"[^a-zA-Z0-9 -]", "", t)
    return t.replace(" ", "-").lower()

_HEADING_RE = re.compile(r"<h([1-6])>(.*?)</h\1>", re.DOTALL)

def _add_heading_ids(html: str) -> str:
    def add(m):
        plain = _html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))
        return f'<h{m.group(1)} id="{kramdown_id(plain)}">{m.group(2)}</h{m.group(1)}>'
    return _HEADING_RE.sub(add, html)


def _rewrite(html, site_base, link_map=None, unresolved=None):
    base = site_base.rstrip("/")

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#|data:|//|/courses/)", url):
            return m.group(0)
        url = re.sub(r"\.md(?=(#|$))", ".html", url)
        url = re.sub(r"^(\./)+", "", url)
        if link_map is not None:
            path, _, frag = url.partition("#")
            if path in link_map:
                return f'{attr}="{link_map[path]}{"#" + frag if frag else ""}"'
            if unresolved is not None:
                unresolved.append(path)
        return f'{attr}="{base}/{url}"'

    return re.sub(r'(href|src|poster)="([^"]+)"', fix, html)


def render_html(md_text, site_base, link_map=None, unresolved=None):
    return _rewrite(_add_heading_ids(_md.render(md_text)), site_base, link_map, unresolved)
```

- [ ] **Step 4: Run the full suite**

Run: `..\.venv\Scripts\python -m pytest -q`
Expected: all pass. If an old test asserts exact `<h2>` markup, update it to expect the `id`, and say so in the commit message.

- [ ] **Step 5: Commit**

```bash
git add canvas/converter.py canvas/tests/test_converter.py
git commit -m "canvas: kramdown heading ids and Canvas link map for self-contained courses"
```

---

### Task 3: Editable PPTX decks from decks.yml

**Files:**
- Create: `undergrad/slides/build_pptx.py`
- Create: `undergrad/slides/test_build_pptx.py`
- Output: `undergrad/slides/moduleone.pptx` … `moduleseven.pptx` (committed)

**Interfaces:**
- Consumes: `decks.yml` (the slide types section, quote, image, points, readings, prompt, question, and `notes`), plus the module front matter (`canvas.module`, `week_start`, `due`, `unit`). These are the same inputs `build_decks.py` reads.
- Produces: `build_pptx.build_deck(stem: str, slides: list[dict], meta: dict) -> pptx.Presentation`, `build_pptx.plain(text: str) -> str` (inline markup stripped), and `build_pptx.main() -> int` (writes `<stem>.pptx`).

Design, to keep everything editable in PowerPoint:
- Every slide uses the default template's **Blank** layout, `prs.slide_layouts[6]`. The retro window frame is a **grouped** set of shapes: the ink-bordered panel, the colored title bar, three dot squares, and the label. The frame moves as one piece, and the content text box sits on top of it, outside the group, so clicking the text edits it directly.
- The window bar color cycles yellow, `#8FE9D3`, `#FFB3CF`, `#B9C8FF` by slide position, matching the CSS `nth-child(4n+…)` rules. The title slide uses a pink bar with white text.
- A section slide is a full-bleed unit-color background with big Arial Black text. The text is white for words and images and ink for code and coda, as in the CSS.
- On an image slide, the picture is fitted inside the frame without changing its aspect ratio and is downscaled to a 1920 px long side. The `alt` text goes on the picture (`descr`), so PowerPoint's and Canvas's accessibility checkers see it. The caption sits under the frame, and `credit_url` becomes a "source" hyperlink.
- Quote, cite, readings, and points text keeps `[text](url)` as real hyperlinks and `**bold**`/`*italic*` as run formatting.
- Points and readings use real paragraph bullets (`a:buChar`), not typed "•" characters.
- Text frames use `TEXT_TO_FIT_SHAPE` autofit, and long quotes (>230 chars) start at a smaller size. That is the same threshold as the web deck.
- `notes:` goes into each slide's speaker notes.

- [ ] **Step 1: Write the failing tests** (`undergrad/slides/test_build_pptx.py`)

```python
from pathlib import Path
import frontmatter, yaml
import pytest
import build_pptx as bp

HERE = Path(__file__).resolve().parent
DECKS = yaml.safe_load((HERE / "decks.yml").read_text(encoding="utf-8"))

def _meta(stem):
    return frontmatter.load(str(HERE.parent / f"{stem}.md")).metadata

def _texts(slide):
    out = []
    for sh in slide.shapes:
        shapes = sh.shapes if sh.shape_type == 6 else [sh]   # 6 = GROUP
        out += [s.text_frame.text for s in shapes if s.has_text_frame]
    return "\n".join(out)

def test_plain_strips_markup():
    assert bp.plain("see [the *essay*](https://a.b) and **this**") == "see the essay and this"

@pytest.mark.parametrize("stem", list(DECKS))
def test_slide_count_title_plus_yaml(stem):
    prs = bp.build_deck(stem, DECKS[stem], _meta(stem))
    assert len(prs.slides) == len(DECKS[stem]) + 1

@pytest.mark.parametrize("stem", list(DECKS))
def test_quotes_survive_verbatim(stem):
    prs = bp.build_deck(stem, DECKS[stem], _meta(stem))
    for i, s in enumerate(DECKS[stem], start=1):
        if "quote" in s:
            assert bp.plain(s["quote"]) in _texts(prs.slides[i]).replace("\v", "\n"), (stem, i)

@pytest.mark.parametrize("stem", list(DECKS))
def test_notes_and_alt_text(stem):
    prs = bp.build_deck(stem, DECKS[stem], _meta(stem))
    for i, s in enumerate(DECKS[stem], start=1):
        slide = prs.slides[i]
        if s.get("notes"):
            assert slide.notes_slide.notes_text_frame.text == s["notes"].strip()
        if "image" in s:
            pics = [sh for sh in slide.shapes if sh.shape_type == 13]   # 13 = PICTURE
            assert pics and pics[0]._element.nvPicPr.cNvPr.get("descr") == s.get("alt", "")

def test_links_are_real_hyperlinks():
    prs = bp.build_deck("moduleone", DECKS["moduleone"], _meta("moduleone"))
    addrs = {r.hyperlink.address for sh in prs.slides[1].shapes if sh.has_text_frame
             for p in sh.text_frame.paragraphs for r in p.runs if r.hyperlink.address}
    assert "https://99percentinvisible.org/episode/the-eliza-effect/" in addrs

def test_points_use_real_bullets():
    stem, idx = next((st, i) for st in DECKS for i, s in enumerate(DECKS[st], 1) if "points" in s)
    slide = bp.build_deck(stem, DECKS[stem], _meta(stem)).slides[idx]
    xml = "".join(sh._element.xml for sh in slide.shapes if sh.has_text_frame)
    assert "buChar" in xml and "•" not in xml.replace('char="•"', "")
```

- [ ] **Step 2: Run them to verify they fail**

Run (from `undergrad/slides/`): `..\..\.venv\Scripts\python -m pytest test_build_pptx.py -q`
Expected: FAIL with `ModuleNotFoundError: build_pptx`

- [ ] **Step 3: Implement `build_pptx.py`**

```python
# -*- coding: utf-8 -*-
"""Build editable PowerPoint versions of the ENG 3861 decks from decks.yml.

Same source as build_decks.py (the reveal.js web decks). These .pptx files
are what goes to Canvas: the course is handed off to an instructor who
edits slides in PowerPoint, not in this repo. Rebuild after editing decks.yml:

    ../../.venv/Scripts/python build_pptx.py      (from undergrad/slides/)
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

import frontmatter
import yaml
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent
REPO = COURSE.parent

TITLE_FONT, BODY_FONT, MONO_FONT = "Arial Black", "Verdana", "Courier New"
C = {k: RGBColor.from_string(v) for k, v in {
    "paper": "FFF7E3", "panel": "FFFFFF", "ink": "1B1035", "soft": "4A3F66",
    "pink": "FF3D7F", "blue": "2E5BFF", "yellow": "FFD23F", "mint": "00B894",
    "orange": "FF7A1A", "termbg": "1B1035", "termfg": "7DFFB3",
    "bar1": "FFD23F", "bar2": "8FE9D3", "bar3": "FFB3CF", "bar0": "B9C8FF"}.items()}
UNIT = {"words": "blue", "images": "pink", "code": "mint", "coda": "orange"}
UNIT_LABELS = {"words": "Words", "images": "Images", "code": "Code", "coda": "Futures"}
DARK_TEXT_UNITS = {"code", "coda"}
W, H = Inches(13.333), Inches(7.5)
MAX_PX = 1920

_TOKEN = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)|\*\*(.+?)\*\*|\*(.+?)\*")


def runs(text: str) -> list[tuple[str, bool, bool, str | None]]:
    """Split inline markup into (text, bold, italic, url) runs."""
    text, out, pos = str(text).strip(), [], 0
    for m in _TOKEN.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False, False, None))
        if m.group(1) is not None:
            for t, b, i, _ in runs(m.group(1)):   # *italic* inside link text
                out.append((t, b, i, m.group(2)))
        elif m.group(3) is not None:
            out.append((m.group(3), True, False, None))
        else:
            out.append((m.group(4), False, True, None))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False, False, None))
    return out


def plain(text: str) -> str:
    return "".join(r[0] for r in runs(text))


def write(p, text, size, font=BODY_FONT, color="ink", bold=False):
    for t, b, i, url in runs(text):
        r = p.add_run()
        r.text = t
        f = r.font
        f.name, f.size, f.bold, f.italic = font, Pt(size), bold or b, i
        f.color.rgb = C[color]
        if url:
            r.hyperlink.address = url


def textbox(slide, x, y, w, h, *, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    tf.vertical_anchor = anchor
    return tf


def bullet(p, char="■"):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Emu(Inches(0.45))))
    pPr.set("indent", str(-Emu(Inches(0.35))))
    etree.SubElement(pPr, qn("a:buChar")).set("char", char)


def rect(shapes, x, y, w, h, fill, line="ink", line_pt=3.0):
    s = shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = C[fill]
    if line:
        s.line.color.rgb = C[line]
        s.line.width = Pt(line_pt)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def window(slide, x, y, w, h, label, bar, body="panel", label_color="ink"):
    """Grouped retro window frame; returns the body box (x, y, w, h)."""
    g = slide.shapes.add_group_shape()
    bar_h = Inches(0.55)
    rect(g.shapes, x + Inches(0.12), y + Inches(0.12), w, h, "ink", line=None)  # hard shadow
    rect(g.shapes, x, y, w, h, body)
    rect(g.shapes, x, y, w, bar_h, bar)
    for n, col in enumerate(("pink", "blue", "mint")):
        rect(g.shapes, x + Inches(0.25 + n * 0.33), y + Inches(0.16),
             Inches(0.22), Inches(0.22), col, line_pt=2.0)
    lt = g.shapes.add_textbox(x + Inches(1.35), y, w - Inches(1.5), bar_h).text_frame
    lt.vertical_anchor = MSO_ANCHOR.MIDDLE
    write(lt.paragraphs[0], label, 16, MONO_FONT, label_color, bold=True)
    pad = Inches(0.4)
    return x + pad, y + bar_h + Inches(0.25), w - 2 * pad, h - bar_h - Inches(0.5)


def bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = C[color]


def add_notes(slide, s):
    if s.get("notes"):
        slide.notes_slide.notes_text_frame.text = s["notes"].strip()


def fitted_picture(slide, src: Path, x, y, w, h, alt: str):
    im = Image.open(src)
    if max(im.size) > MAX_PX:
        im.thumbnail((MAX_PX, MAX_PX))
    buf = io.BytesIO()
    fmt = "PNG" if src.suffix.lower() == ".png" else "JPEG"
    (im if fmt == "PNG" else im.convert("RGB")).save(buf, fmt, quality=88)
    buf.seek(0)
    ratio = min(w / im.size[0], h / im.size[1])
    pw, ph = int(im.size[0] * ratio), int(im.size[1] * ratio)
    pic = slide.shapes.add_picture(buf, x + (w - pw) // 2, y + (h - ph) // 2, pw, ph)
    pic._element.nvPicPr.cNvPr.set("descr", alt)
    return pic


def bar_for(index: int) -> str:
    return f"bar{index % 4}"


def render(prs, s: dict, index: int, unit: str):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, "paper")
    bar = bar_for(index + 1)
    if "section" in s:
        bg(slide, UNIT[unit])
        fg = "ink" if unit in DARK_TEXT_UNITS else "panel"
        tf = textbox(slide, Inches(0.8), Inches(1.6), W - Inches(1.6), Inches(3.2),
                     anchor=MSO_ANCHOR.MIDDLE)
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        write(tf.paragraphs[0], s["section"], 54, TITLE_FONT, fg)
        if s.get("sub"):
            p = tf.add_paragraph()
            p.alignment = PP_ALIGN.CENTER
            write(p, s["sub"], 28, MONO_FONT, fg)
    elif "quote" in s:
        bx, by, bw, bh = window(slide, Inches(0.9), Inches(0.7), W - Inches(1.8),
                                H - Inches(1.4), s.get("label", "quote.txt"), bar)
        tf = textbox(slide, bx, by, bw, bh - Inches(0.8), anchor=MSO_ANCHOR.MIDDLE)
        write(tf.paragraphs[0], f"“{s['quote'].strip()}”",
              22 if len(s["quote"]) > 230 else 28)
        cite = f"[{s.get('cite', '')}]({s['url']})" if s.get("url") else s.get("cite", "")
        ctf = textbox(slide, bx, by + bh - Inches(0.7), bw, Inches(0.6))
        ctf.paragraphs[0].alignment = PP_ALIGN.RIGHT
        write(ctf.paragraphs[0], f"— {cite}", 16, MONO_FONT, "soft")
    elif "image" in s:
        src = REPO / s["image"]
        if not src.exists():
            raise FileNotFoundError(f"image not found: {s['image']}")
        cap_h = Inches(0.8) if (s.get("caption") or s.get("credit_url")) else 0
        bx, by, bw, bh = window(slide, Inches(0.9), Inches(0.4), W - Inches(1.8),
                                H - Inches(0.8) - cap_h, s.get("label", "image.png"), bar,
                                body="ink")
        fitted_picture(slide, src, bx, by, bw, bh, s.get("alt", ""))
        if cap_h:
            tf = textbox(slide, Inches(0.9), H - cap_h - Inches(0.15), W - Inches(1.8), cap_h)
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            cap = s.get("caption", "")
            if s.get("credit_url"):
                cap = f"{cap} [source]({s['credit_url']})".strip()
            write(tf.paragraphs[0], cap, 18)
    elif "prompt" in s:
        bx, by, bw, bh = window(slide, Inches(1.2), Inches(1.2), W - Inches(2.4),
                                H - Inches(2.4), "prompt.exe", bar, body="termbg")
        tf = textbox(slide, bx, by, bw, bh, anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        if s.get("title"):
            write(p, s["title"], 20, MONO_FONT, "bar3")
            p = tf.add_paragraph()
        write(p, "> ", 28, MONO_FONT, "yellow", bold=True)
        write(p, s["prompt"], 28, MONO_FONT, "termfg")
    elif "question" in s:
        bx, by, bw, bh = window(slide, Inches(1.2), Inches(1.0), W - Inches(2.4),
                                H - Inches(2.0), s.get("label", "discuss.txt"), bar)
        tf = textbox(slide, bx, by, bw, bh, anchor=MSO_ANCHOR.MIDDLE)
        write(tf.paragraphs[0], s["question"], 32, TITLE_FONT)
        if s.get("hint"):
            write(tf.add_paragraph(), s["hint"], 20, BODY_FONT, "soft")
    elif "points" in s or "readings" in s:
        title = s.get("title", "Readings") if "readings" in s else s["title"]
        ttf = textbox(slide, Inches(0.8), Inches(0.5), W - Inches(1.6), Inches(1.0))
        write(ttf.paragraphs[0], title, 36, TITLE_FONT, UNIT[unit] if unit not in
              DARK_TEXT_UNITS else "ink")
        tf = textbox(slide, Inches(0.8), Inches(1.7), W - Inches(1.6), H - Inches(2.3))
        items = s.get("points") or s["readings"]
        for n, item in enumerate(items):
            p = tf.paragraphs[0] if n == 0 else tf.add_paragraph()
            bullet(p)
            p.space_after = Pt(12)
            if isinstance(item, dict):
                write(p, item["cite"], 22)
                if item.get("what"):
                    write(p, f" — {item['what']}", 18, BODY_FONT, "soft")
            else:
                write(p, item, 24)
    else:
        raise ValueError(f"unknown slide type: {s}")
    add_notes(slide, s)


def title_slide(prs, meta: dict):
    c = meta["canvas"]
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg(slide, "paper")
    label, rest = c["module"].split(":", 1)
    start, due = c["week_start"], c["due"]
    dates = f"{start:%b} {start.day} – {due:%b} {due.day}, {due.year}".upper()
    bx, by, bw, bh = window(slide, Inches(1.0), Inches(1.0), W - Inches(2.0),
                            H - Inches(2.0), "ENG3861.EXE", "pink", label_color="panel")
    tf = textbox(slide, bx, by, bw, bh, anchor=MSO_ANCHOR.MIDDLE)
    write(tf.paragraphs[0], UNIT_LABELS[c["unit"]].upper(), 18, TITLE_FONT, UNIT[c["unit"]])
    write(tf.add_paragraph(), label.strip(), 24, MONO_FONT, "soft")
    write(tf.add_paragraph(), rest.strip(), 48, TITLE_FONT)
    write(tf.add_paragraph(), f"> ENG 3861 // {dates}_", 20, MONO_FONT, "soft")


def build_deck(stem: str, slides: list[dict], meta: dict) -> Presentation:
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    title_slide(prs, meta)
    for i, s in enumerate(slides, start=1):
        render(prs, s, i, meta["canvas"]["unit"])
    prs.core_properties.title = meta["canvas"]["module"]
    return prs


def main() -> int:
    decks = yaml.safe_load((HERE / "decks.yml").read_text(encoding="utf-8"))
    for stem, slides in decks.items():
        meta = frontmatter.load(str(COURSE / f"{stem}.md")).metadata
        out = HERE / f"{stem}.pptx"
        build_deck(stem, slides, meta).save(out)
        print(f"{stem}.pptx: {len(slides) + 1} slides, {out.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the tests and build**

Run (from `undergrad/slides/`): `..\..\.venv\Scripts\python -m pytest test_build_pptx.py -q`, then `..\..\.venv\Scripts\python build_pptx.py`
Expected: all pass, and seven `.pptx` files are written. Each should be under about 15 MB. If one is larger, lower `MAX_PX` to 1600.

- [ ] **Step 5: Commit**

```bash
git add undergrad/slides/build_pptx.py undergrad/slides/test_build_pptx.py undergrad/slides/*.pptx
git commit -m "content: undergrad decks also build as editable PowerPoint files"
```

---

### Task 4: Visual review of the PPTX decks

**Files:**
- Create: `undergrad/slides/export_pngs.ps1`
- Possibly modify: `undergrad/slides/build_pptx.py` (layout fixes only)

- [ ] **Step 1: Write the export script**

```powershell
# Export every slide of each deck to PNG via PowerPoint, for visual review.
# Usage (from undergrad/slides/):  powershell -File export_pngs.ps1 [-OutDir <dir>]
param([string]$OutDir = "$env:TEMP\eng3861-pptx-review")
$pp = New-Object -ComObject PowerPoint.Application
try {
  Get-ChildItem -Path $PSScriptRoot -Filter *.pptx | ForEach-Object {
    $deck = $pp.Presentations.Open($_.FullName, $true, $false, $false)
    $dest = Join-Path $OutDir $_.BaseName
    $deck.SaveAs($dest, 18)   # ppSaveAsPNG: one PNG per slide in $dest
    $deck.Close()
    Write-Output "$($_.Name) -> $dest"
  }
} finally { $pp.Quit() }
```

- [ ] **Step 2: Export into the scratchpad and look at every slide**

Run: `powershell -File undergrad/slides/export_pngs.ps1 -OutDir <scratchpad>/pptx-review`
Then read each PNG with the Read tool. Check for these problems:
- text overflowing a window frame (PowerPoint applies the shrink-to-fit autofit when it renders)
- unreadable contrast (white on mint or orange should never appear)
- pictures that are distorted or overlap their captions
- frames that don't line up with their shadows
- any title slide where the module name wraps badly

- [ ] **Step 3: Fix the layout constants in `build_pptx.py`, rebuild, and re-export until it's clean**

Fixes should go into sizes, insets, and the long-quote threshold. Never edit quote text.

- [ ] **Step 4: Open one deck in PowerPoint by hand**

Confirm that clicking a quote edits it directly, that the frame group moves as one piece, that the speaker notes are there, and that Review → Check Accessibility reports no missing alt text.

- [ ] **Step 5: Commit**

```bash
git add undergrad/slides/export_pngs.ps1 undergrad/slides/build_pptx.py undergrad/slides/*.pptx
git commit -m "content: undergrad PPTX layout pass after visual review"
```

---

### Task 5: Canvas client additions and the self-contained asset sync

**Files:**
- Modify: `canvas/canvas_client.py`
- Create: `canvas/assets.py`
- Test: `canvas/tests/test_canvas_client.py`, `canvas/tests/test_assets.py`

**Interfaces:**
- Produces in `CanvasClient`:
  - `course_info() -> dict` (GET the course: `name`, `course_code`)
  - `upload_file(path: Path, folder: str, content_type: str) -> dict` (Canvas file JSON: `id`, `updated_at`, …)
  - `find_or_create_page(title: str) -> str` (page url slug, and it **never** modifies an existing page)
  - `updated_at(kind: str, ref) -> str | None` (`kind` ∈ `"pages"`, `"discussion_topics"`, `"files"`. Files use the course-independent `/api/v1/files/{id}`. Returns None on 404.)
- Produces in `assets.py`:
  - `PPTX_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation"`
  - `find_assets(cfg, root: Path) -> dict[str, Path]` (repo-relative key → file. The keys are `slides/<stem>.pptx` for every week and every `images/...` path referenced in the syllabus, week, or extra files.)
  - `check_decks_fresh(root: Path) -> None` (raises `SystemExit` naming the stale decks)
  - `build_link_map(cfg, course_path: str, files: dict[str, int], pages: dict[str, str]) -> dict[str, str]`
  - `placeholder_ids(cfg, assets) -> tuple[dict, dict]` (fake file ids and page slugs for dry runs)
  - `sync_assets(client, cfg, root, state, force=False) -> tuple[dict[str, int], dict[str, str]]` (uploads changed assets with the edit guard, reserves pages, and returns `(files, pages)`). `pages` is keyed by `stem` for exercise pages, `stem + ":lecture"` for lecture pages, and `"index"` for the syllabus.
  - `slides_html(course_path, api_base, file_id, week_label) -> str`

- [ ] **Step 1: Write the failing client tests** (append to `canvas/tests/test_canvas_client.py`, following the `responses` setup already in that file)

```python
import responses
from pathlib import Path
from canvas_client import CanvasClient

API = "https://canvas.test"
COURSE = f"{API}/api/v1/courses/42"

@responses.activate
def test_upload_file_three_step(tmp_path):
    f = tmp_path / "moduleone.pptx"; f.write_bytes(b"PK..")
    responses.post(f"{COURSE}/files", json={"upload_url": "https://up.test/x",
                                            "upload_params": {"key": "k"}})
    responses.post("https://up.test/x", status=302,
                   headers={"Location": f"{API}/api/v1/files/7/create_success"})
    responses.get(f"{API}/api/v1/files/7/create_success", json={"id": 7, "updated_at": "T1"})
    out = CanvasClient(API, "tok", "42").upload_file(f, "Lecture Slides", "application/x")
    assert out["id"] == 7
    pre = responses.calls[0].request
    assert b'"on_duplicate": "overwrite"' in pre.body and b'"parent_folder_path": "Lecture Slides"' in pre.body
    assert "Authorization" not in responses.calls[1].request.headers   # never send the token to the upload host

@responses.activate
def test_find_or_create_page_never_overwrites():
    responses.get(f"{COURSE}/pages", json=[{"title": "Syllabus", "url": "syllabus"}])
    assert CanvasClient(API, "tok", "42").find_or_create_page("Syllabus") == "syllabus"
    assert all(c.request.method == "GET" for c in responses.calls)

@responses.activate
def test_updated_at_none_on_404():
    responses.get(f"{COURSE}/pages/gone", status=404)
    assert CanvasClient(API, "tok", "42").updated_at("pages", "gone") is None
```

- [ ] **Step 2: Write the failing asset tests** (`canvas/tests/test_assets.py`)

```python
import os, time
from pathlib import Path
import pytest
import assets

CFG = {"weeks": ["moduleone"], "extra": ["finalreflection"], "syllabus_file": "index.md"}

def _course(tmp_path):
    (tmp_path / "slides").mkdir()
    (tmp_path / "slides" / "decks.yml").write_text("moduleone: []\n", encoding="utf-8")
    (tmp_path / "slides" / "moduleone.pptx").write_bytes(b"PK")
    (tmp_path / "images").mkdir()
    (tmp_path / "images" / "a.png").write_bytes(b"\x89PNG")
    (tmp_path / "index.md").write_text("---\n---\n[s](slides/moduleone.html)\n", encoding="utf-8")
    (tmp_path / "moduleone.md").write_text("---\n---\n![x](images/a.png)\n", encoding="utf-8")
    (tmp_path / "finalreflection.md").write_text("---\n---\nhi\n", encoding="utf-8")
    return tmp_path

def test_find_assets(tmp_path):
    found = assets.find_assets(CFG, _course(tmp_path))
    assert set(found) == {"slides/moduleone.pptx", "images/a.png"}

def test_missing_pptx_is_an_error(tmp_path):
    root = _course(tmp_path); (root / "slides" / "moduleone.pptx").unlink()
    with pytest.raises(SystemExit, match="build_pptx.py"):
        assets.find_assets(CFG, root)

def test_stale_deck_is_an_error(tmp_path):
    root = _course(tmp_path)
    old = time.time() - 100
    os.utime(root / "slides" / "moduleone.pptx", (old, old))
    with pytest.raises(SystemExit, match="moduleone.pptx"):
        assets.check_decks_fresh(root)

def test_link_map(tmp_path):
    m = assets.build_link_map(CFG, "/courses/9",
                              {"slides/moduleone.pptx": 5, "images/a.png": 6},
                              {"moduleone": "module-one", "moduleone:lecture": "m1-lecture",
                               "finalreflection": "final", "index": "syllabus"})
    assert m["slides/moduleone.html"] == "/courses/9/files/5"
    assert m["moduleone.html"] == "/courses/9/pages/module-one"
    assert m["index.html"] == "/courses/9/pages/syllabus"
    assert m["images/a.png"] == "/courses/9/files/6/preview"

class FakeClient:
    def __init__(self, live_updated="T1"):
        self.uploads, self.live = [], live_updated
    def upload_file(self, path, folder, ctype):
        self.uploads.append(path.name); return {"id": 5, "updated_at": "T1"}
    def updated_at(self, kind, ref): return self.live
    def find_or_create_page(self, title): return title.lower().replace(" ", "-")

def test_sync_skips_unchanged_and_edited(tmp_path, capsys):
    root = _course(tmp_path); cfg = {**CFG, "self_contained": True}
    state = {}
    c = FakeClient(); assets.sync_assets(c, cfg, root, state)
    assert sorted(c.uploads) == ["a.png", "moduleone.pptx"]
    c = FakeClient(); assets.sync_assets(c, cfg, root, state)
    assert c.uploads == []                                   # same sha: no re-upload
    (root / "slides" / "moduleone.pptx").write_bytes(b"PK2")
    c = FakeClient(live_updated="T2-gta-replaced-it")
    assets.sync_assets(c, cfg, root, state)
    assert c.uploads == [] and "[edited in Canvas]" in capsys.readouterr().out
```

- [ ] **Step 3: Run them to verify they fail**

Run (from `canvas/`): `..\.venv\Scripts\python -m pytest tests/test_canvas_client.py tests/test_assets.py -q`
Expected: FAIL (missing methods, missing module)

- [ ] **Step 4: Implement the client methods** (in `CanvasClient`)

```python
    def course_info(self) -> dict:
        r = self.s.get(self.course)
        r.raise_for_status()
        return r.json()

    def upload_file(self, path, folder: str, content_type: str) -> dict:
        """Canvas three-step upload; replaces a same-named file in `folder`."""
        data = path.read_bytes()
        pre = self._post(f"{self.course}/files", {
            "name": path.name, "size": len(data), "content_type": content_type,
            "parent_folder_path": folder, "on_duplicate": "overwrite"})
        # step 2 goes to the storage host, which must not get our token
        r = requests.post(pre["upload_url"], data=pre["upload_params"],
                          files={"file": (path.name, data, content_type)},
                          allow_redirects=False)
        if r.is_redirect:
            r = self.s.get(r.headers["Location"])
        r.raise_for_status()
        out = r.json()
        if "id" not in out and out.get("location"):
            out = self.s.get(out["location"]).json()
        return out

    def find_or_create_page(self, title: str) -> str:
        for p in self._get_all(f"{self.course}/pages", search_term=title):
            if p["title"] == title:
                return p["url"]
        return self._post(f"{self.course}/pages",
                          {"wiki_page": {"title": title, "body": "<p></p>",
                                         "published": False}})["url"]

    def updated_at(self, kind: str, ref) -> str | None:
        root = self.course.split("/courses/")[0]
        url = (f"{root}/files/{ref}" if kind == "files"
               else f"{self.course}/{kind}/{ref}")
        r = self.s.get(url)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json().get("updated_at")
```

- [ ] **Step 5: Implement `canvas/assets.py`**

```python
"""Self-contained course assets: decks and page images go into Canvas
Files, and every repo-relative link is rewritten to its Canvas target,
so the course runs with no dependency on the website or this repo."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

PPTX_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
               ".gif": "image/gif", ".webp": "image/webp"}
FOLDERS = {"slides": "Lecture Slides", "images": "Page Images"}
_IMG_REF = re.compile(r'(?:\]\(|src=")(images/[^)"\s#]+)')


def _sources(cfg, root: Path) -> list[Path]:
    stems = cfg["weeks"] + cfg.get("extra", [])
    return [root / cfg["syllabus_file"]] + [root / f"{s}.md" for s in stems]


def find_assets(cfg, root: Path) -> dict[str, Path]:
    found = {}
    for stem in cfg["weeks"]:
        p = root / "slides" / f"{stem}.pptx"
        if not p.exists():
            raise SystemExit(f"missing {p}: run build_pptx.py in {root / 'slides'}")
        found[f"slides/{stem}.pptx"] = p
    for src in _sources(cfg, root):
        for rel in _IMG_REF.findall(src.read_text(encoding="utf-8")):
            if not (root / rel).exists():
                raise SystemExit(f"{src.name}: image {rel} not found")
            found[rel] = root / rel
    return found


def check_decks_fresh(root: Path) -> None:
    yml = root / "slides" / "decks.yml"
    stale = [p.name for p in sorted((root / "slides").glob("*.pptx"))
             if p.stat().st_mtime < yml.stat().st_mtime]
    if stale:
        raise SystemExit(f"decks.yml is newer than {', '.join(stale)}: "
                         f"run build_pptx.py before deploying")


def build_link_map(cfg, course_path, files, pages) -> dict[str, str]:
    m = {"index.html": f"{course_path}/pages/{pages['index']}"}
    for stem in cfg["weeks"]:
        fid = files[f"slides/{stem}.pptx"]
        m[f"slides/{stem}.html"] = m[f"slides/{stem}.pptx"] = f"{course_path}/files/{fid}"
    for stem in cfg["weeks"] + cfg.get("extra", []):
        m[f"{stem}.html"] = f"{course_path}/pages/{pages[stem]}"
    for rel, fid in files.items():
        if rel.startswith("images/"):
            m[rel] = f"{course_path}/files/{fid}/preview"
    return m


def placeholder_ids(cfg, found) -> tuple[dict, dict]:
    files = {rel: f"FILE-{Path(rel).name}" for rel in found}
    pages = {"index": "syllabus"}
    for stem in cfg["weeks"] + cfg.get("extra", []):
        pages[stem] = stem
        pages[f"{stem}:lecture"] = f"{stem}-lecture"
    return files, pages


def slides_html(course_path, api_base, file_id, week_label) -> str:
    href = f"{course_path}/files/{file_id}"
    return (f'<p><a class="instructure_file_link instructure_scribd_file auto_open" '
            f'title="{week_label} slides" href="{href}?wrap=1" '
            f'data-api-endpoint="{api_base}{href}" data-api-returntype="File">'
            f'{week_label} slides (PowerPoint)</a></p>'
            f'<p><a href="{href}/download?download_frd=1">Download the {week_label} '
            f'slides</a> to view them full screen, with speaker notes.</p>')


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sync_assets(client, cfg, root, state, force=False):
    found = find_assets(cfg, root)
    check_decks_fresh(root)
    known = state.setdefault("files", {})
    for rel, path in found.items():
        rec, sha = known.get(rel), _sha(path)
        if rec and rec["sha256"] == sha:
            continue
        if rec and not force and client.updated_at("files", rec["id"]) != rec["updated_at"]:
            print(f"[edited in Canvas] {rel} was replaced in Canvas Files; "
                  f"not re-uploaded (pass --force to override)")
            continue
        ctype = PPTX_TYPE if path.suffix == ".pptx" else IMAGE_TYPES[path.suffix.lower()]
        out = client.upload_file(path, FOLDERS[rel.split("/")[0]], ctype)
        known[rel] = {"id": out["id"], "sha256": sha, "updated_at": out.get("updated_at")}
        print(f"uploaded: {rel}")
    pages = {"index": state.get("syllabus_url") or client.find_or_create_page("Syllabus")}
    state["syllabus_url"] = pages["index"]
    for stem in cfg["weeks"] + cfg.get("extra", []):
        st = state.setdefault(stem, {})
        pages[stem] = st.get("page_url") or client.find_or_create_page(st.get("module")
                                                                        or _title(root, stem))
        st["page_url"] = pages[stem]
        if stem in cfg["weeks"]:
            pages[f"{stem}:lecture"] = st.get("lecture_url") or client.find_or_create_page(
                f"{_label(root, stem)} Readings + Lecture")
            st["lecture_url"] = pages[f"{stem}:lecture"]
    return {rel: r["id"] for rel, r in known.items()}, pages


def _title(root, stem):
    import frontmatter
    return frontmatter.load(str(root / f"{stem}.md")).metadata["canvas"]["module"]


def _label(root, stem):
    return _title(root, stem).split(":")[0].strip()
```

Note that the page titles reserved here must equal the titles `deploy.py` upserts: the module title for the exercise page and `"{label} Readings + Lecture"` for the lecture page. Otherwise the reserve step creates duplicates.

- [ ] **Step 6: Run the tests**

Run: `..\.venv\Scripts\python -m pytest -q`
Expected: all pass

- [ ] **Step 7: Commit**

```bash
git add canvas/canvas_client.py canvas/assets.py canvas/tests
git commit -m "canvas: file uploads, page reservation, and asset sync for self-contained courses"
```

---

### Task 6: Wire self-contained mode, the course guard, and the edit guard into deploy.py

**Files:**
- Modify: `canvas/deploy.py`
- Modify: `undergrad/canvas/course.yml`
- Test: `canvas/tests/test_deploy.py`

**Interfaces:**
- Consumes: everything from Tasks 1, 2, and 5.
- `course.yml` keys (all optional, and the grad course has none of them): `self_contained: true`, `expect_course_code: "3861"`, `instructor_guide: instructor-guide.md`.

Behavior when `self_contained: true`:
1. The plans are built with a `link_map`, which comes from `placeholder_ids` on a dry run and from `sync_assets` on a live run.
2. The lecture page replaces the iframe block with `assets.slides_html(...)`.
3. The module gets a `File` item for the deck at position 2. The exercise page moves to 3 and the discussion to 4.
4. Any `unresolved` link aborts a live deploy (`SystemExit` listing `file: path`). A dry run prints it as `[unresolved]` and keeps going.
5. The syllabus page is rendered with the same link map.

Behavior whenever `state` has a stored `updated_at` for a page or discussion, in every mode: if the live `updated_at` differs and `--force` is not set, the item is skipped with `[edited in Canvas] <title>`. After every upsert, the new live `updated_at` is stored. These are the keys `lecture_updated`, `page_updated`, `discussion_updated`, and `syllabus_updated`. The Instructor Guide is guarded the same way.

Course guard: when `expect_course_code` is set, `client.course_info()["course_code"]` must contain it, or the deploy exits before writing anything. It always prints `deploying to: <name> (<course_code>)`.

- [ ] **Step 1: Write the failing tests**

```python
import deploy, assets

def _sc_course(tmp_path):
    root = tmp_path / "course"; canvas = root / "canvas"; canvas.mkdir(parents=True)
    (root / "slides").mkdir()
    (root / "slides" / "decks.yml").write_text("moduleone: []\n", encoding="utf-8")
    (root / "slides" / "moduleone.pptx").write_bytes(b"PK")
    (root / "index.md").write_text("---\n---\n## AI Use Policy\n\n[m](moduleone.md)\n", encoding="utf-8")
    (root / "moduleone.md").write_text(
        "---\ncanvas:\n  module: \"Module One: X\"\n  week_start: 2030-01-07\n"
        "  due: 2030-01-20\n  points: 10\n  discussion: true\n  unit: words\n---\n"
        "See [slides](slides/moduleone.html) and [policy](index.md#ai-use-policy).\n\n"
        "### Discussion\n\nQ?\n", encoding="utf-8")
    (canvas / "course.yml").write_text(
        "site_base: https://x.y\nassignment_groups: {exercises: E, other: O}\n"
        "syllabus_file: index.md\nweeks: [moduleone]\nself_contained: true\n"
        "late_window_hours: 24\nunits: {words: {label: Words, color: '#0f766e'}}\n",
        encoding="utf-8")
    return canvas

def test_self_contained_dry_run_has_no_site_links(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(_sc_course(tmp_path))
    deploy.main(["--all", "--dry-run"])
    page = (tmp_path / "course/canvas/preview/moduleone.html").read_text(encoding="utf-8")
    lecture = (tmp_path / "course/canvas/preview/moduleone-lecture.html").read_text(encoding="utf-8")
    assert "x.y" not in page and "x.y" not in lecture
    assert "/pages/syllabus#ai-use-policy" in page
    assert "instructure_file_link" in lecture and "<iframe" not in lecture
    assert "[unresolved]" not in capsys.readouterr().out

def test_self_contained_unresolved_link_reported(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    md = canvas.parent / "moduleone.md"
    md.write_text(md.read_text(encoding="utf-8").replace("Q?", "[x](notes/thing.pdf)"), encoding="utf-8")
    monkeypatch.chdir(canvas)
    deploy.main(["--all", "--dry-run"])
    assert "[unresolved] moduleone: notes/thing.pdf" in capsys.readouterr().out

def test_course_guard_aborts_on_wrong_course(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    (canvas / "course.yml").write_text((canvas / "course.yml").read_text() +
                                       "expect_course_code: '3861'\n")
    monkeypatch.chdir(canvas)
    for k, v in {"CANVAS_API_URL": "https://c.t", "CANVAS_API_TOKEN": "t",
                 "CANVAS_COURSE_ID": "1"}.items():
        monkeypatch.setenv(k, v)

    class Wrong:
        def __init__(self, *a): pass
        def course_info(self): return {"name": "Humanities AI", "course_code": "ENG6806"}
        def __getattr__(self, n): raise AssertionError(f"wrote to wrong course via {n}")
    monkeypatch.setattr("canvas_client.CanvasClient", Wrong)
    with pytest.raises(SystemExit, match="3861"):
        deploy.main(["--all"])
```

Add one edit-guard test. It uses a fake client whose `updated_at("pages", ...)` returns a value different from the `page_updated` value seeded in `.state.json`. Assert that `upsert_page` is never called for that page and that the output contains `[edited in Canvas] Module One: X`. Model the fake on `FakeClient` in `test_assets.py`, and add `upsert_module`, `upsert_page`, `upsert_discussion`, `upsert_assignment_group`, `add_to_module`, `get_page_body`, `course_info`, `upload_file`, and `find_or_create_page` methods that record their calls.

- [ ] **Step 2: Run them to verify they fail**

Run: `..\.venv\Scripts\python -m pytest tests/test_deploy.py -q`

- [ ] **Step 3: Implement in `deploy.py`**

1. Refactor the planning into `make_plans(stems, root, cfg, syllabus_md, link_map, slide_ids, course_path, api_base)`. It returns `(plans, unresolved)`, where `unresolved` is a list of `(stem, path)`. `plan_week` passes `link_map` and `unresolved` into every `render_html` call. When `slides` (a dict holding `course_path`, `api_base`, and `file_id`) is given, the lecture HTML is built as `readings_html + "<h2>Lecture</h2>" + placeholder + assets.slides_html(...)` instead of the iframe block.
2. In `main`: if `cfg.get("self_contained")` and this is a dry run, run `find_assets` and `check_decks_fresh`, take ids from `placeholder_ids`, use `course_path="/courses/COURSE"`, then print every unresolved link as `[unresolved] {stem}: {path}`.
3. On a live run, the order is: `load_dotenv(cwd)` → client → `info = client.course_info()` → print `deploying to:` → the `expect_course_code` check (`raise SystemExit(f"course_code {info['course_code']!r} does not contain {want!r}; wrong CANVAS_COURSE_ID?")`) → `files, pages = assets.sync_assets(client, cfg, root, state, force=args.force)` when self-contained → `make_plans` with the live link map (`course_path=f"/courses/{os.environ['CANVAS_COURSE_ID']}"`, `api_base=os.environ['CANVAS_API_URL'].rstrip('/') + '/api/v1'`) → `raise SystemExit` if any link is unresolved → the freeze filter → the existing upsert loop.
4. Add an edit-guard helper and call it before each `upsert_page` or `upsert_discussion`:

```python
def edited_in_canvas(client, kind, ref, stored, force) -> bool:
    if force or not ref or not stored:
        return False
    return client.updated_at(kind, ref) != stored
```

After each successful upsert, store `client.updated_at(kind, ref)` in state under the matching `*_updated` key.
5. When self-contained, call `client.add_to_module(module_id, "File", file_id, position=2)` after the lecture page and shift the later positions.
6. Instructor Guide: if `cfg.get("instructor_guide")`, render `Path(cfg["instructor_guide"])` with the link map, then call `client.upsert_page("Instructor Guide (not visible to students)", html, False, known_url=state.get("guide_url"))`. Always pass `published=False` and keep it out of every module. Use the same edit guard.

- [ ] **Step 4: Update `undergrad/canvas/course.yml`**

```yaml
# Built to be handed off: everything lives in Canvas (decks as .pptx in
# Files, images uploaded, links rewritten), nothing points back at the site.
self_contained: true
expect_course_code: "3861"
instructor_guide: instructor-guide.md
```

- [ ] **Step 5: Run the full suite, then dry-run both courses**

Run (from `canvas/`): `..\.venv\Scripts\python -m pytest -q`, then `..\.venv\Scripts\python deploy.py --all --dry-run`. The grad output should match what it printed before this work, apart from the frozen-week lines.
Run (from `undergrad/canvas/`): `..\..\.venv\Scripts\python ..\..\canvas\deploy.py --all --dry-run`
Expected: 8 modules planned, no `[unresolved]`, and `grep -l anastasiasalter undergrad/canvas/preview/*.html` prints nothing.

- [ ] **Step 6: Commit**

```bash
git add canvas/deploy.py canvas/tests undergrad/canvas/course.yml
git commit -m "canvas: self-contained deploy mode with course guard and Canvas-edit guard"
```

---

### Task 7: Instructor Guide and docs

**Files:**
- Create: `undergrad/canvas/instructor-guide.md`
- Modify: `undergrad/README.md` (replace "Before the first Canvas deploy" with a "Canvas handoff" section), `canvas/README.md` (document the new `course.yml` keys)

- [ ] **Step 1: Write `undergrad/canvas/instructor-guide.md`**

```markdown
---
title: Instructor Guide
---

## Instructor Guide (not visible to students)

This course was built outside Canvas and then handed off. **Canvas is now
the master copy:** edit anything here directly. Nothing outside Canvas
will overwrite your changes.

### How each module is set up

Each module is two weeks long:

1. **Readings + Lecture** (Think week): the readings list, the lecture video, and the slides.
2. **Slides** (PowerPoint): the same deck as a file in the module.
3. **Exercise page** (Do week): the week's YouTube talk, then the exercise.
4. **Exercise Discussion**, graded, worth 10 points. It is due Sunday at 11:59 PM, closes Monday at 11:59 PM, and has a points table at the top.

### Adding your lecture video

On each Readings + Lecture page, click **Edit**. Replace the line that says
the video lecture "will be posted here" with your recording, using
*Insert → Media → Upload/Record Media*, and save.

### Editing the slides

The decks are in **Files → Lecture Slides** (`moduleone.pptx` …
`moduleseven.pptx`). To change one:

1. Download it, then open it in PowerPoint. PowerPoint for the web through your UCF Microsoft 365 account works too.
2. Edit it. The fonts are Arial Black, Verdana, and Courier New, which every copy of PowerPoint has. Each "window" frame is a group, so you can move it as one piece. Click the text to edit it. Speaker notes are under each slide.
3. In **Files → Lecture Slides**, upload it with **exactly the same file name** and choose **Replace**. The module item and the preview on the lecture page then show the new version.

To add a slide in the same style, duplicate an existing slide (right-click → Duplicate Slide) and change its text.

### Dates

Every date in the syllabus, the module pages, and the discussions was set
for the term the course was built for. If you teach a different term, use
Canvas's *Course Copy* with *Adjust events and due dates*, then update the
dates written into the Syllabus page and the module pages.

### Grading

Every discussion begins with its points table. Students get one point per
required screenshot or piece of evidence, plus the reflection (250 words
minimum), one citation from the readings, and two peer replies (one point
each). The AI policy (see the Syllabus) allows AI for the exercise tasks
but **not** for reflections or replies.
```

- [ ] **Step 2: Rewrite the README sections**

In `undergrad/README.md`, replace § "Before the first Canvas deploy" with a "Canvas handoff" section. It should say:
- the course deploys self-contained;
- decks are built with `build_pptx.py`, and `build_decks.py` still builds the web versions;
- the run order is dry run → unpublished → review → `--publish`;
- **after the handoff, Canvas is the master copy.** Redeploys skip anything edited there, but the intent is that the repo stops being edited for this course once the GTA has it.

Add the `self_contained`, `expect_course_code`, `instructor_guide`, `late_window_hours`, and `units` keys to the `course.yml` table in `canvas/README.md`.

- [ ] **Step 3: Rerun the undergrad dry run** so `preview/` includes the guide, then read `preview/` for the guide and one module and check how they read.

- [ ] **Step 4: Commit**

```bash
git add undergrad/canvas/instructor-guide.md undergrad/README.md canvas/README.md
git commit -m "docs: undergrad instructor guide and Canvas handoff notes"
```

---

### Task 8: First deploy to the new course (runs once the course ID arrives)

This task contains no code. The user supplies the course ID and confirms the term first.

- [ ] **Step 1: Confirm with the user** that the term is Spring 2027 (all dates in the module front matter and `index.md` assume it), and fill in the instructor name, email, and office hours if they are known. Otherwise leave TBD for the GTA to edit in Canvas.
- [ ] **Step 2: Write `undergrad/canvas/.env`** with `CANVAS_API_URL=https://webcourses.ucf.edu`, the new `CANVAS_COURSE_ID`, and a fresh token. Copy the URL and token from `canvas/.env` only if the token is still valid.
- [ ] **Step 3: Run the dry run** (from `undergrad/canvas/`): `..\..\.venv\Scripts\python ..\..\canvas\deploy.py --all --dry-run`
- [ ] **Step 4: Run the unpublished live deploy**: `..\..\.venv\Scripts\python ..\..\canvas\deploy.py --all`. The first output line must read `deploying to: ... (…3861…)`.
- [ ] **Step 5: Review in Canvas with the user.** Check these items:
  - the inline PPTX preview renders on each lecture page;
  - the module File item opens;
  - the syllabus TOC anchors jump;
  - `index.md#ai-use-policy` links land on the policy;
  - the module-three images display;
  - the YouTube embeds play;
  - the discussion due and lock times are Sunday and Monday 11:59 PM ET;
  - the Instructor Guide is unpublished.

  **Live checks** (each one confirms an assumption the deployer makes):
  - **No-change redeploy:** run `deploy.py --all` again right after the first deploy, with nothing changed anywhere. It must print no `[edited in Canvas]` lines.
  - **Replace keeps the file id?** After the replace test below, note whether the deck's Canvas file id changed.
  - **Module publish cascades?** Publish one module by hand and note whether its items get published too, and whether their `updated_at` moves.
  - **Discussion GET includes `assignment`?** GET one discussion topic and confirm the plain response has an `assignment` object (the change marker reads its dates and points).
  - **Heading ids survive?** Open the Syllabus HTML editor and confirm the `<h2 id="...">` / `<h3 id="...">` attributes are still there, so the TOC anchors jump.

  **Test the replace flow once:** upload a renamed copy of one deck over the original with *Replace*, confirm the lecture-page preview follows it, then run `deploy.py --all` again. It must print `[edited in Canvas] slides/<deck>.pptx was replaced ...` or `[missing in Canvas] slides/<deck>.pptx was deleted or replaced ...`, and the GTA's deck must be kept (no `uploaded:` line for it).
- [ ] **Step 6: Run `deploy.py --all --publish`** once the user approves (memory rule: always pass `--publish` when going live).
- [ ] **Step 7: Update the memory files** (`undergrad-eng3861-course.md`) with the course ID, the handoff state, and the rule that Canvas is the master copy after handoff. Then commit `.state.json` if the grad course's state is committed, matching the grad convention.
