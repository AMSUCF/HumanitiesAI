import re
from datetime import datetime
from pathlib import Path
import frontmatter, yaml
import pytest
import build_pptx as bp

HERE = Path(__file__).resolve().parent
DECKS = yaml.safe_load((HERE / "decks.yml").read_text(encoding="utf-8"))
_BUILT = {}

def _meta(stem):
    return frontmatter.load(str(HERE.parent / f"{stem}.md")).metadata

def _deck(stem):
    if stem not in _BUILT:
        _BUILT[stem] = bp.build_deck(stem, DECKS[stem], _meta(stem))
    return _BUILT[stem]

def _all_shapes(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:   # 6 = GROUP
            yield from _all_shapes(sh.shapes)

def _texts(slide):
    return "\n".join(s.text_frame.text for s in _all_shapes(slide.shapes)
                     if s.has_text_frame and not s.is_placeholder)

def _first(kind):
    return next((st, i) for st in DECKS for i, s in enumerate(DECKS[st], 1) if kind in s)

def test_plain_strips_markup():
    assert bp.plain("see [the *essay*](https://a.b) and **this**") == "see the essay and this"

@pytest.mark.parametrize("stem", list(DECKS))
def test_slide_count_title_plus_yaml(stem):
    assert len(_deck(stem).slides) == len(DECKS[stem]) + 1

@pytest.mark.parametrize("stem", list(DECKS))
def test_quotes_survive_verbatim(stem):
    prs = _deck(stem)
    for i, s in enumerate(DECKS[stem], start=1):
        if "quote" in s:
            assert bp.plain(s["quote"]) in _texts(prs.slides[i]).replace("\v", "\n"), (stem, i)

def test_quote_markup_never_leaks_into_plain_text():
    for stem, slides in DECKS.items():
        for s in slides:
            if "quote" in s:
                q = s["quote"]
                expected = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", q).replace("**", "").replace("*", "")
                p = bp.plain(q)
                assert p == expected, (stem, q[:40])
                assert "*" not in p and "](" not in p and "**" not in p

@pytest.mark.parametrize("stem", list(DECKS))
def test_notes_and_alt_text(stem):
    prs = _deck(stem)
    for i, s in enumerate(DECKS[stem], start=1):
        slide = prs.slides[i]
        if s.get("notes"):
            assert slide.notes_slide.notes_text_frame.text == s["notes"].strip()
        if "image" in s:
            pics = [sh for sh in slide.shapes if sh.shape_type == 13]   # 13 = PICTURE
            assert pics and pics[0]._element.nvPicPr.cNvPr.get("descr") == s.get("alt", "")

def test_links_are_real_hyperlinks():
    prs = _deck("moduleone")
    addrs = {r.hyperlink.address for sh in prs.slides[1].shapes if sh.has_text_frame
             for p in sh.text_frame.paragraphs for r in p.runs if r.hyperlink.address}
    assert "https://99percentinvisible.org/episode/the-eliza-effect/" in addrs

@pytest.mark.parametrize("kind", ["points", "readings"])
def test_points_and_readings_use_real_bullets(kind):
    stem, idx = _first(kind)
    slide = _deck(stem).slides[idx]
    n_items = len(DECKS[stem][idx - 1][kind])
    bodies = [sh for sh in slide.shapes if sh.has_text_frame and not sh.is_placeholder
              and len(sh.text_frame.paragraphs) == n_items]
    assert bodies, (stem, idx)
    for p in bodies[0].text_frame.paragraphs:
        assert p._p.find(".//" + bp.qn("a:buChar")) is not None, p.text

def test_run_spacing_survives():
    stem, idx = _first("readings")
    item = DECKS[stem][idx - 1]["readings"][0]
    assert f"{bp.plain(item['cite'])} — {item['what']}" in _texts(_deck(stem).slides[idx])
    stem, idx = _first("prompt")
    assert "> " + bp.plain(DECKS[stem][idx - 1]["prompt"]) in _texts(_deck(stem).slides[idx])

@pytest.mark.parametrize("stem", list(DECKS))
def test_every_slide_has_a_hidden_title(stem):
    prs = _deck(stem)
    for n, slide in enumerate(prs.slides):
        phs = list(slide.placeholders)
        assert len(phs) == 1, (stem, n, [p.name for p in phs])
        title = slide.shapes.title
        assert title is not None and title.text_frame.text.strip(), (stem, n)
        assert title.left + title.width <= 0, (stem, n)   # parked off the slide
    assert prs.slides[0].shapes.title.text_frame.text == _meta(stem)["canvas"]["module"]

def test_hidden_title_text_by_slide_type():
    titles = {}
    for stem, slides in DECKS.items():
        prs = _deck(stem)
        for i, s in enumerate(slides, start=1):
            titles[(stem, i)] = (s, prs.slides[i].shapes.title.text_frame.text)
    for s, t in titles.values():
        if "section" in s:
            assert t == bp.plain(s["section"])
        elif "quote" in s:
            assert t == "Quote: " + bp.plain(s.get("cite", ""))
        elif "image" in s:
            if s.get("caption"):
                assert t == bp.plain(s["caption"])
            else:
                assert 0 < len(t) <= 81 and bp.plain(s["alt"]).startswith(t.rstrip("…"))
        elif "question" in s:
            assert t == "Discussion question"
        elif "prompt" in s:
            assert t == ("Prompt: " + bp.plain(s["title"]) if s.get("title") else "Prompt")
        elif "points" in s:
            assert t == bp.plain(s["title"])
        elif "readings" in s:
            assert t == bp.plain(s.get("title", "Readings"))

def test_core_properties_are_deterministic():
    cp = _deck("moduleone").core_properties
    assert cp.author == "ENG 3861"
    assert cp.created == cp.modified == datetime(2027, 1, 1)
    assert cp.revision == 1
    assert not cp.last_modified_by
    assert cp.title == _meta("moduleone")["canvas"]["module"]

LOW_CONTRAST_FILLS = {"00B894", "FF7A1A"}   # mint, orange

def _fill_hex(fill):
    try:
        return str(fill.fore_color.rgb) if fill.type == 1 else None   # 1 = SOLID
    except (AttributeError, TypeError):
        return None

@pytest.mark.parametrize("stem", list(DECKS))
def test_no_white_on_mint_or_orange_and_no_mint_or_orange_text(stem):
    for n, slide in enumerate(_deck(stem).slides):
        slide_bg = _fill_hex(slide.background.fill)
        for sh in _all_shapes(slide.shapes):
            if not sh.has_text_frame or sh.is_placeholder:
                continue
            behind = _fill_hex(sh.fill) or slide_bg
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if not r.text.strip():
                        continue
                    col = str(r.font.color.rgb)
                    assert col not in LOW_CONTRAST_FILLS, (stem, n, r.text)
                    if behind in LOW_CONTRAST_FILLS:
                        assert col != "FFFFFF", (stem, n, r.text)

@pytest.mark.parametrize("stem", list(DECKS))
def test_text_fits_its_box_as_rendered(stem):
    for n, slide in enumerate(_deck(stem).slides):
        for sh in _all_shapes(slide.shapes):
            if sh.has_text_frame and not sh.is_placeholder and sh.text_frame.text.strip():
                assert bp.fits(sh), (stem, n, sh.text_frame.text[:50])

def test_frames_are_groups_and_quotes_are_top_level():
    stem, idx = _first("quote")
    slide = _deck(stem).slides[idx]
    assert any(sh.shape_type == 6 for sh in slide.shapes)
    quote = bp.plain(DECKS[stem][idx - 1]["quote"])
    top = [sh for sh in slide.shapes if sh.has_text_frame and quote in sh.text_frame.text]
    assert top and top[0].shape_type != 6
