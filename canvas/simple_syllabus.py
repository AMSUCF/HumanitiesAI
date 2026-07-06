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
