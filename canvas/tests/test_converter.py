import textwrap
import pytest
from converter import load_week, render_html

def test_load_week_parses_canvas_block(tmp_path):
    f = tmp_path / "weekone.md"
    f.write_text(textwrap.dedent("""\
        ---
        layout: page
        title: "Week One: Ghosts — Histories"
        canvas:
          module: "Week One: Ghosts — Histories"
          week_start: 2026-08-24
          due: 2026-08-30
          points: 6
          discussion: true
          extra_credit: false
          unit: ghosts
        ---
        # Week One
        """), encoding="utf-8")
    doc = load_week(f)
    assert doc.canvas["points"] == 6
    assert doc.canvas["unit"] == "ghosts"
    assert doc.body.startswith("# Week One")

def test_load_week_rejects_missing_keys(tmp_path):
    f = tmp_path / "bad.md"
    f.write_text("---\ncanvas:\n  module: X\n---\nbody", encoding="utf-8")
    with pytest.raises(ValueError, match="due"):
        load_week(f)

def test_render_rewrites_relative_links_and_md_suffix():
    html = render_html("[wk2](weektwo.md) ![e](images/eliza.png)",
                       "https://example.github.io/HumanitiesAI")
    assert 'href="https://example.github.io/HumanitiesAI/weektwo.html"' in html
    assert 'src="https://example.github.io/HumanitiesAI/images/eliza.png"' in html

def test_render_leaves_absolute_and_anchor_links():
    html = render_html("[a](https://claude.ai) [b](#discussion)", "https://x.y")
    assert 'href="https://claude.ai"' in html
    assert 'href="#discussion"' in html

def test_render_strips_dot_slash_prefix_only():
    html = render_html("![x](./images/x.png)", "https://x.y")
    assert 'src="https://x.y/images/x.png"' in html

def test_render_preserves_parent_traversal():
    html = render_html("[up](../other/page.md)", "https://x.y")
    assert 'href="https://x.y/../other/page.html"' in html

from datetime import date
from converter import split_discussion, due_at_utc, apply_canvas_style

def test_split_discussion():
    page, disc = split_discussion("intro\n\n### Discussion\n\nQ1?\nQ2?")
    assert page == "intro"
    assert disc == "Q1?\nQ2?"

def test_split_without_discussion_returns_empty():
    page, disc = split_discussion("intro only")
    assert (page, disc) == ("intro only", "")

def test_due_at_utc_handles_dst_fallback():
    # EDT (UTC-4): Oct 25 23:59 ET -> Oct 26 03:59Z
    assert due_at_utc(date(2026, 10, 25)) == "2026-10-26T03:59:00Z"
    # EST (UTC-5): Nov 1 2026 is the fallback day; 23:59 ET -> 04:59Z
    assert due_at_utc(date(2026, 11, 1)) == "2026-11-02T04:59:00Z"

def test_apply_canvas_style_bands_and_badges():
    out = apply_canvas_style("<p>x</p>", "shells")
    assert "border-top: 6px solid #b45309" in out
    assert ">Shells</span>" in out
    assert out.endswith("<p>x</p>")
