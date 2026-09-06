import json
from pathlib import Path
import deploy

def test_plan_week_builds_operations(tmp_path, monkeypatch):
    wk = tmp_path / "weekone.md"
    wk.write_text(
        "---\nlayout: page\ntitle: T\ncanvas:\n"
        "  module: \"Week One: Ghosts — Histories\"\n"
        "  week_start: 2026-08-24\n  due: 2026-08-30\n  points: 6\n"
        "  discussion: true\n  extra_credit: false\n  unit: ghosts\n---\n"
        "Body\n\n### Discussion\n\nQ?\n", encoding="utf-8")
    plan = deploy.plan_week(wk, site_base="https://x.y")
    assert plan["module"] == "Week One: Ghosts — Histories"
    assert plan["points"] == 6
    assert plan["due_at"] == "2026-08-31T03:59:00Z"
    assert "border-top" in plan["page_html"]
    assert "Q?" in plan["discussion_html"]

def test_dry_run_writes_previews_and_no_network(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "course.yml").write_text(
        "site_base: https://x.y\ntimezone: America/New_York\n"
        "assignment_groups: {exercises: Exercises, other: Course Requirements}\n"
        "syllabus_file: index.md\nweeks: [weekone]\nextra: []\n", encoding="utf-8")
    (tmp_path / "weekone.md").write_text(
        "---\ntitle: T\ncanvas:\n  module: M1\n  week_start: 2026-08-24\n"
        "  due: 2026-08-30\n  points: 6\n  discussion: true\n"
        "  extra_credit: false\n  unit: ghosts\n---\nBody\n\n### Discussion\n\nQ?\n",
        encoding="utf-8")
    monkeypatch.setattr(deploy, "now_et", lambda: deploy.datetime(2026, 8, 20, tzinfo=deploy.TZ))
    deploy.main(["--all", "--dry-run"])
    assert (tmp_path / "preview" / "weekone.html").exists()
    out = capsys.readouterr().out
    assert "[dry-run]" in out and "M1" in out

def test_simple_syllabus_cli_writes_preview(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "course.yml").write_text(
        "site_base: https://x.y\ntimezone: America/New_York\n"
        "assignment_groups: {exercises: Exercises, other: Course Requirements}\n"
        "syllabus_file: index.md\nweeks: [weekone]\nextra: []\n", encoding="utf-8")
    (tmp_path / "index.md").write_text(
        "---\ntitle: X\n---\nintro\n\n## Course Description\n\nBody A [wk](weekone.md)\n",
        encoding="utf-8")
    (tmp_path / "weekone.md").write_text("---\ntitle: T\n---\nBody\n", encoding="utf-8")
    assert deploy.main(["--simple-syllabus"]) == 0
    out = (tmp_path / "preview" / "simple_syllabus.html")
    assert out.exists()
    assert 'href="https://x.y/weekone.html"' in out.read_text(encoding="utf-8")

def test_plan_week_rejects_unknown_unit(tmp_path):
    wk = tmp_path / "weekbad.md"
    wk.write_text(
        "---\ntitle: T\ncanvas:\n  module: M\n  week_start: 2026-08-24\n"
        "  due: 2026-08-30\n  points: 6\n  discussion: true\n"
        "  extra_credit: false\n  unit: shell\n---\nBody\n", encoding="utf-8")
    import pytest as _pytest
    with _pytest.raises(ValueError, match="unknown unit"):
        deploy.plan_week(wk, site_base="https://x.y")


def test_plan_week_includes_availability_and_lecture(tmp_path):
    wk = tmp_path / "weekone.md"
    wk.write_text(
        "---\ntitle: T\ncanvas:\n  module: \"Week One: Ghosts — Histories\"\n"
        "  week_start: 2026-08-24\n  due: 2026-08-30\n  points: 6\n"
        "  discussion: true\n  extra_credit: false\n  unit: ghosts\n---\n"
        "Body\n\n### Discussion\n\nQ?\n", encoding="utf-8")
    plan = deploy.plan_week(wk, site_base="https://x.y")
    assert plan["unlock_at"] == "2026-08-24T04:00:00Z"
    assert plan["lock_at"] == "2026-09-07T03:59:00Z"
    assert plan["lecture_title"] == "Week One Readings + Lecture"
    assert "video lecture" in plan["lecture_html"].lower()


def test_plan_week_hard_close_locks_at_due(tmp_path):
    wk = tmp_path / "finalreflection.md"
    wk.write_text(
        "---\ntitle: T\ncanvas:\n  module: \"Finals Week: Final Reflection\"\n"
        "  week_start: 2026-12-04\n  due: 2026-12-10\n  points: 10\n"
        "  discussion: true\n  extra_credit: false\n  unit: coda\n"
        "  hard_close: true\n---\nBody\n\n### Discussion\n\nQ?\n", encoding="utf-8")
    plan = deploy.plan_week(wk, site_base="https://x.y")
    assert plan["lock_at"] == plan["due_at"] == "2026-12-11T04:59:00Z"


def test_plan_week_lecture_embeds_slides(tmp_path):
    wk = tmp_path / "weekone.md"
    wk.write_text(
        "---\ntitle: T\ncanvas:\n  module: \"Week One: Ghosts — Histories\"\n"
        "  week_start: 2026-08-24\n  due: 2026-08-30\n  points: 6\n"
        "  discussion: true\n  extra_credit: false\n  unit: ghosts\n---\n"
        "Body\n\n### Discussion\n\nQ?\n", encoding="utf-8")
    plan = deploy.plan_week(wk, site_base="https://x.y")
    assert 'iframe src="https://x.y/slides/weekone.html"' in plan["lecture_html"]
    assert "video lecture will be posted" in plan["lecture_html"]


SYLLABUS = (
    "## Weekly Schedule\n\n"
    "### Week One: Ghosts - Histories (Monday, August 24 - Sunday, August 30)\n\n"
    "-   [**Slides: Week One**](slides/weekone.html)\n"
    "-   *Artificial Intelligence* - Part I: Background\n"
    "-   Berry, D. M. (2023). The Limits of Computation. [link](https://doi.org/x)\n"
    "-   **Due: Activity Verification (Friday, August 28)**\n"
    "-   [**Exercise: ELIZA and Ghosts**](weekone.md)\n\n"
    "### Week Two: Ghosts - Generation (Monday, August 31 - Sunday, September 6)\n\n"
    "-   [**Slides: Week Two**](slides/weektwo.html)\n"
    "-   *The AI Con* - Chapter 2\n"
    "-   [**Exercise: Generation and Interfaces**](weektwo.md)\n"
)


def _week_md(module="Week One: Ghosts — Histories"):
    return ("---\ntitle: T\ncanvas:\n"
            f"  module: \"{module}\"\n"
            "  week_start: 2026-08-24\n  due: 2026-08-30\n  points: 6\n"
            "  discussion: true\n  extra_credit: false\n  unit: ghosts\n---\n"
            "Body\n\n### Discussion\n\nQ?\n")


def test_plan_week_lecture_lists_readings_before_video(tmp_path):
    wk = tmp_path / "weekone.md"
    wk.write_text(_week_md(), encoding="utf-8")
    plan = deploy.plan_week(wk, site_base="https://x.y", syllabus_md=SYLLABUS)
    html = plan["lecture_html"]
    assert plan["lecture_title"] == "Week One Readings + Lecture"
    assert "<h2>Readings</h2>" in html and "<h2>Lecture</h2>" in html
    assert html.index("Readings") < html.index("Lecture")
    assert "Part I: Background" in html
    assert html.index("Part I: Background") < html.index("video lecture will be posted")
    # slides and exercise bullets are dropped from the readings list
    assert "Slides: Week One" not in html
    assert "Exercise: ELIZA" not in html
    # only week one's readings, not week two's
    assert "Chapter 2" not in html


def test_extract_readings_missing_week_returns_empty():
    from converter import extract_readings
    assert extract_readings(SYLLABUS, "Week Nine") == ""


def test_video_embed_regex_matches_canvas_media_iframe():
    live = ('<div>band</div><p><iframe style="width: 480px;" '
            'title="HumanitiesAI_One.mp4" data-media-type="video" '
            'src="https://webcourses.ucf.edu/media_attachments_iframe/1?x=1" '
            'allowfullscreen="allowfullscreen"></iframe></p><p>rest</p>')
    m = deploy.VIDEO_EMBED_RE.search(live)
    assert m and m.group(0).startswith("<p><iframe")
    assert m.group(0).endswith("</iframe></p>")
    assert "rest" not in m.group(0)

