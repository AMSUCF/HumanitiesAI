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
