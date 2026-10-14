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
