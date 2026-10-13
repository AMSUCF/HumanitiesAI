# -*- coding: utf-8 -*-
"""Build the ENG 3861 reveal.js decks from decks.yml.

Each module's slides are listed in decks.yml; this script writes
<stem>.html beside it. Images are referenced in place (usually from the
grad decks' slides/media/), not copied. Edit decks.yml, then rerun:

    ../../.venv/Scripts/python build_decks.py      (from undergrad/slides/)
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import frontmatter
import yaml

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent
REPO = COURSE.parent

UNIT_LABELS = {"words": "Words", "images": "Images", "code": "Code", "coda": "Futures"}

_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITAL = re.compile(r"\*(.+?)\*")


def inline(text: str) -> str:
    """Escape, then allow [text](url), **bold**, and *italic*."""
    out = html.escape(str(text).strip(), quote=False)
    out = _LINK.sub(lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', out)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    return _ITAL.sub(r"<em>\1</em>", out)


def window(body: str, label: str, extra: str = "") -> str:
    return (f'<div class="win {extra}"><div class="win-bar"><span class="dots" '
            f'aria-hidden="true"><i></i><i></i><i></i></span>{html.escape(label)}'
            f'</div><div class="win-body">{body}</div></div>')


def image_url(src: str) -> str:
    """Images stay where they live in the repo (mostly the grad decks'
    slides/media/); decks reference them relative to undergrad/slides/."""
    if not (REPO / src).exists():
        raise FileNotFoundError(f"image not found: {src}")
    return "../../" + src


def notes(s: dict) -> str:
    return f'<aside class="notes">{html.escape(s["notes"])}</aside>' if s.get("notes") else ""


def render(s: dict) -> str:
    if "section" in s:
        sub = f'<p class="sub">{inline(s["sub"])}</p>' if s.get("sub") else ""
        return (f'<section class="section-slide"><div class="big">{inline(s["section"])}'
                f'</div>{sub}{notes(s)}</section>')
    if "quote" in s:
        who = s.get("cite", "")
        if s.get("url"):
            who = f'[{who}]({s["url"]})'
        long = " long" if len(s["quote"]) > 230 else ""
        body = (f'<blockquote class="{long.strip()}">{inline(s["quote"])}</blockquote>'
                f'<p class="cite">{inline(who)}</p>')
        return (f'<section class="quote-slide">{window(body, s.get("label", "quote.txt"))}'
                f'{notes(s)}</section>')
    if "image" in s:
        src = image_url(s["image"])
        cap = s.get("caption", "")
        credit = (f' <span class="credit"><a href="{html.escape(s["credit_url"])}">source</a></span>'
                  if s.get("credit_url") else "")
        cap_html = (f'<p class="caption">{inline(cap)}{credit}</p>'
                    if cap or credit else "")
        cls = "image-slide" + ("" if cap_html else " no-caption")
        img = f'<img data-src="{src}" alt="{html.escape(s.get("alt", ""))}">'
        return (f'<section class="{cls}">{window(img, s.get("label", "image.png"))}'
                f'{cap_html}{notes(s)}</section>')
    if "prompt" in s:
        label = f'<p class="label">{inline(s["title"])}</p>' if s.get("title") else ""
        body = f'{label}<span class="ps">&gt;</span> {inline(s["prompt"])}'
        return (f'<section class="prompt-slide">{window(body, "prompt.exe", "term")}'
                f'{notes(s)}</section>')
    if "question" in s:
        hint = f'<p class="hint">{inline(s["hint"])}</p>' if s.get("hint") else ""
        body = f'<p class="q">{inline(s["question"])}</p>{hint}'
        return (f'<section class="question-slide">{window(body, s.get("label", "discuss.txt"))}'
                f'{notes(s)}</section>')
    if "readings" in s:
        items = "".join(
            f'<li>{inline(r["cite"])}<span class="what">{inline(r.get("what", ""))}</span></li>'
            for r in s["readings"])
        return (f'<section class="points-slide readings-slide"><h2 class="slide-title">'
                f'{inline(s.get("title", "Readings"))}</h2><ul>{items}</ul>{notes(s)}</section>')
    if "points" in s:
        items = "".join(f"<li>{inline(p)}</li>" for p in s["points"])
        return (f'<section class="points-slide"><h2 class="slide-title">{inline(s["title"])}'
                f'</h2><ul>{items}</ul>{notes(s)}</section>')
    raise ValueError(f"unknown slide type: {s}")


def title_slide(meta: dict) -> str:
    c = meta["canvas"]
    label, rest = c["module"].split(":", 1)
    start, due = c["week_start"], c["due"]
    dates = f"{start:%b} {start.day} – {due:%b} {due.day}, {due.year}".upper()
    body = (f'<span class="sticker">{UNIT_LABELS[c["unit"]]}</span>'
            f'<p class="kicker">{html.escape(label)}</p>'
            f'<h1>{html.escape(rest.strip())}</h1>'
            f'<p class="prompt">&gt; ENG 3861 // {dates}<span class="cursor" '
            f'aria-hidden="true">_</span></p>')
    return f'<section class="title-slide">{window(body, "ENG3861.EXE")}</section>'


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Slides</title>
<link rel="stylesheet" href="../../assets/reveal/dist/reset.css">
<link rel="stylesheet" href="../../assets/reveal/dist/reveal.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Bungee&family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
<link rel="stylesheet" href="undergrad-slides.css">
</head>
<body class="unit-{unit}">
<div class="reveal"><div class="slides">
{slides}
</div></div>
<script src="../../assets/reveal/dist/reveal.js"></script>
<script src="../../assets/reveal/plugin/notes/notes.js"></script>
<script>
Reveal.initialize({{ hash: true, slideNumber: 'c/t',
  width: 1280, height: 720, margin: 0.06, center: true,
  plugins: [ RevealNotes ] }}).then(() => {{
  let lastStep = 0;
  document.addEventListener('wheel', e => {{
    if (Date.now() - lastStep < 700) return;
    lastStep = Date.now();
    if (e.deltaY > 0) Reveal.next(); else if (e.deltaY < 0) Reveal.prev();
  }}, {{ passive: true }});
}});
</script>
</body>
</html>
"""


def main() -> int:
    decks = yaml.safe_load((HERE / "decks.yml").read_text(encoding="utf-8"))
    for stem, slides in decks.items():
        meta = frontmatter.load(str(COURSE / f"{stem}.md")).metadata
        sections = [title_slide(meta)] + [render(s) for s in slides]
        (HERE / f"{stem}.html").write_text(
            PAGE.format(title=html.escape(meta["canvas"]["module"]),
                        unit=meta["canvas"]["unit"], slides="\n".join(sections)),
            encoding="utf-8", newline="\n")
        print(f"{stem}: {len(sections)} slides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
