from __future__ import annotations

import html as _html
import re
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

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


def _rewrite(html: str, site_base: str, link_map: dict[str, str] | None = None,
             unresolved: list[str] | None = None) -> str:
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


def render_html(md_text: str, site_base: str, link_map: dict[str, str] | None = None,
                unresolved: list[str] | None = None) -> str:
    return _rewrite(_add_heading_ids(_md.render(md_text)), site_base, link_map, unresolved)


TZ = ZoneInfo("America/New_York")
_DISCUSSION_RE = re.compile(r"^### Discussion[ \t]*$", re.MULTILINE)
_SKIP_BULLET_RE = re.compile(r"^-\s+\[?\*\*(Slides|(Extra Credit )?Exercise)")


def extract_readings(syllabus_md: str, week_label: str) -> str:
    """Pull a week's readings from the syllabus Weekly Schedule.

    Returns the section's markdown (bullets and prose) minus the Slides
    and Exercise bullets (those live elsewhere on the Canvas module),
    or "" if the week heading isn't found.
    """
    m = re.search(
        rf"^###\s+{re.escape(week_label)}[:\s][^\n]*\n(.*?)(?=^###\s|\Z)",
        syllabus_md, re.MULTILINE | re.DOTALL)
    if not m:
        return ""
    # a "#### Do" subheading (undergrad syllabus) starts the exercise half
    # of the module, which belongs on the exercise page, not the lecture page
    section = re.split(r"^####\s+Do\b", m.group(1), maxsplit=1, flags=re.MULTILINE)[0]
    kept, skipping = [], False
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            skipping = bool(_SKIP_BULLET_RE.match(stripped))
            if not skipping:
                kept.append(line)
        elif not stripped:
            skipping = False  # blank line ends any bullet continuation
            kept.append(line)
        elif not skipping:
            kept.append(line)
    return "\n".join(kept).strip()


def split_discussion(md_text: str) -> tuple[str, str]:
    m = _DISCUSSION_RE.search(md_text)
    if not m:
        return md_text.strip(), ""
    return md_text[: m.start()].strip(), md_text[m.end():].strip()


def due_at_utc(due_date) -> str:
    dt = datetime.combine(due_date, time(23, 59), tzinfo=TZ)
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")


def unlock_at_utc(start_date) -> str:
    """Module/assignment opens at midnight ET on its start date."""
    dt = datetime.combine(start_date, time(0, 0), tzinfo=TZ)
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")


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


_BADGE = r'<span class="unit-badge[^"]*">[^<]*</span>'
# a paragraph holding only the badge goes with it; else just the badge
_BADGE_RE = re.compile(rf'<p>\s*{_BADGE}\s*</p>\s*|{_BADGE}\s*')


def apply_canvas_style(html: str, unit: str) -> str:
    html = _BADGE_RE.sub("", html)
    color, label = UNIT_COLORS[unit], UNIT_LABELS[unit]
    band = (
        f'<div style="border-top: 6px solid {color}; padding: 12px 0 4px 0; '
        f'margin-bottom: 16px;"><span style="display: inline-block; '
        f'padding: 2px 10px; border-radius: 9999px; background: {color}; '
        f'color: #ffffff; font-size: 12px; letter-spacing: 1px; '
        f'text-transform: uppercase;">{label}</span></div>'
    )
    return band + html
