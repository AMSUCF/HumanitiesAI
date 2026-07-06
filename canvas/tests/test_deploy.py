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
    deploy.main(["--all", "--dry-run"])
    assert (tmp_path / "preview" / "weekone.html").exists()
    out = capsys.readouterr().out
    assert "[dry-run]" in out and "M1" in out

def test_plan_week_rejects_unknown_unit(tmp_path):
    wk = tmp_path / "weekbad.md"
    wk.write_text(
        "---\ntitle: T\ncanvas:\n  module: M\n  week_start: 2026-08-24\n"
        "  due: 2026-08-30\n  points: 6\n  discussion: true\n"
        "  extra_credit: false\n  unit: shell\n---\nBody\n", encoding="utf-8")
    import pytest as _pytest
    with _pytest.raises(ValueError, match="unknown unit"):
        deploy.plan_week(wk, site_base="https://x.y")
