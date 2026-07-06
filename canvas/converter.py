from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, time
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


def _rewrite(html: str, site_base: str) -> str:
    base = site_base.rstrip("/")

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|#|data:|//)", url):
            return m.group(0)
        url = re.sub(r"\.md(?=(#|$))", ".html", url)
        url = re.sub(r"^(\./)+", "", url)
        return f'{attr}="{base}/{url}"'

    return re.sub(r'(href|src)="([^"]+)"', fix, html)


def render_html(md_text: str, site_base: str) -> str:
    return _rewrite(_md.render(md_text), site_base)


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
