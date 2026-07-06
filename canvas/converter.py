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
