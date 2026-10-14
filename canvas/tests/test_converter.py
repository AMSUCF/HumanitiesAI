import textwrap
from datetime import date

import pytest
from converter import (
    UNIT_COLORS, UNIT_LABELS, apply_canvas_style, configure_units, due_at_utc,
    kramdown_id, load_week, lock_at_utc, render_html, split_discussion, unlock_at_utc,
)

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


def test_unlock_at_utc_monday_midnight():
    # Monday Aug 24 2026 00:00 ET (EDT, UTC-4) -> 04:00Z
    assert due_at_utc.__module__ == "converter"
    assert unlock_at_utc(date(2026, 8, 24)) == "2026-08-24T04:00:00Z"


def test_lock_at_utc_one_week_grace():
    # due Sun Aug 30 -> locks Sun Sep 6 23:59 EDT -> Sep 7 03:59Z
    assert lock_at_utc(date(2026, 8, 30)) == "2026-09-07T03:59:00Z"
    # DST edge: due Sun Nov 1 (fallback day) -> locks Nov 8 23:59 EST -> Nov 9 04:59Z
    assert lock_at_utc(date(2026, 11, 1)) == "2026-11-09T04:59:00Z"


def test_configure_units_merges_course_units():
    configure_units({"words": {"label": "Words", "color": "#0f766e"}})
    assert UNIT_COLORS["words"] == "#0f766e" and UNIT_LABELS["words"] == "Words"
    assert "ghosts" in UNIT_COLORS  # grad units untouched

def test_lock_at_utc_hour_window():
    # Sunday Jan 24 2027 23:59 ET + 24h = Mon Jan 25 23:59 ET = Jan 26 04:59Z
    assert lock_at_utc(date(2027, 1, 24), grace_hours=24) == "2027-01-26T04:59:00Z"

def test_apply_canvas_style_drops_site_unit_badge():
    configure_units({"words": {"label": "Words", "color": "#0f766e"}})
    html = apply_canvas_style('<p><span class="unit-badge unit-badge--words">Words</span></p><p>Hi</p>', "words")
    assert "unit-badge" not in html and html.count("Words") == 1


def test_kramdown_id_matches_jekyll_toc():
    assert kramdown_id("Module One: What Is Digital Humanities? (Weeks 1-2, January 11 - 24)")         == "module-one-what-is-digital-humanities-weeks-1-2-january-11---24"
    assert kramdown_id("AI Use Policy") == "ai-use-policy"

def test_render_adds_heading_ids():
    assert '<h2 id="ai-use-policy">AI Use Policy</h2>' in render_html("## AI Use Policy", "https://x.y")

def test_link_map_rewrites_and_keeps_fragment():
    m = {"index.html": "/courses/9/pages/syllabus", "slides/moduleone.html": "/courses/9/files/77"}
    out = render_html("[p](index.md#ai-use-policy) [s](slides/moduleone.html)", "https://x.y", link_map=m)
    assert 'href="/courses/9/pages/syllabus#ai-use-policy"' in out
    assert 'href="/courses/9/files/77"' in out

def test_link_map_reports_unresolved():
    bad = []
    out = render_html("![a](images/new.png)", "https://x.y", link_map={}, unresolved=bad)
    assert bad == ["images/new.png"] and 'src="https://x.y/images/new.png"' in out

def test_no_link_map_is_unchanged_grad_behavior():
    assert 'href="https://x.y/weektwo.html"' in render_html("[w](weektwo.md)", "https://x.y")


def test_badge_strip_leaves_no_empty_paragraph():
    configure_units({"words": {"label": "Words", "color": "#0f766e"}})
    alone = apply_canvas_style(
        '<p><span class="unit-badge unit-badge--words">Words</span></p>\n<p>Hi</p>', "words")
    assert "<p></p>" not in alone and alone.endswith("<p>Hi</p>")
    # a badge sharing its paragraph with text keeps the paragraph
    shared = apply_canvas_style(
        '<p><span class="unit-badge unit-badge--words">Words</span> Hi</p>', "words")
    assert shared.endswith("<p>Hi</p>")
