from __future__ import annotations

import re
from pathlib import Path

import frontmatter

from converter import render_html


def build_package(index_md: Path, out_dir: Path, site_base: str) -> Path:
    post = frontmatter.load(str(index_md))
    parts = re.split(r"^## +(.+)$", post.content, flags=re.MULTILINE)
    # parts = [preamble, title1, body1, title2, body2, ...]
    sections = []
    preamble = parts[0].strip()
    if preamble:
        # Instructor block (name, office hours, course number, email) lives
        # above the first ## heading and would otherwise be dropped.
        sections.append(
            '<section data-component="Instructor Information">\n'
            "<h2>Instructor Information</h2>\n"
            f"{render_html(preamble, site_base)}\n</section>\n<hr>")
    for i in range(1, len(parts), 2):
        title, body = parts[i].strip(), parts[i + 1]
        sections.append(
            f'<section data-component="{title}">\n<h2>{title}</h2>\n'
            f"{render_html(body, site_base)}\n</section>\n<hr>")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "simple_syllabus.html"
    out.write_text(
        "<!-- Paste each <section> into the matching Simple Syllabus component -->\n"
        + "\n".join(sections), encoding="utf-8")
    return out
