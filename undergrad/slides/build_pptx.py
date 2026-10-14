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
