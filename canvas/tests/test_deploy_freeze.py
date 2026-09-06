"""Live modules are frozen: once a module's open date has passed, deploy.py
leaves it (and the Activity Verification assignment) alone unless --force."""
import deploy


def _two_week_course(tmp_path):
    (tmp_path / "course.yml").write_text(
        "site_base: https://x.y\ntimezone: America/New_York\n"
        "assignment_groups: {exercises: Exercises, other: Course Requirements}\n"
        "syllabus_file: index.md\nweeks: [weekone, weektwo]\nextra: []\n"
        "activity_verification: {name: AV, points: 6, open: 2026-08-24, due: 2026-08-28}\n",
        encoding="utf-8")
    for stem, start, due in (("weekone", "2026-08-24", "2026-08-30"),
                             ("weektwo", "2026-08-31", "2026-09-06")):
        (tmp_path / f"{stem}.md").write_text(
            f"---\ntitle: T\ncanvas:\n  module: {stem.upper()}\n  week_start: {start}\n"
            f"  due: {due}\n  points: 6\n  discussion: true\n"
            "  extra_credit: false\n  unit: ghosts\n---\nBody\n\n### Discussion\n\nQ?\n",
            encoding="utf-8")


def _at(y, m, d, hh=12, mm=0):
    return deploy.datetime(y, m, d, hh, mm, tzinfo=deploy.TZ)


def test_is_live_once_module_opens():
    opens = deploy.date(2026, 8, 24)
    assert deploy.is_live(opens, _at(2026, 8, 24, 0, 0))        # midnight ET on open date
    assert deploy.is_live(opens, _at(2026, 8, 27))
    assert not deploy.is_live(opens, _at(2026, 8, 23, 23, 59))  # the night before


def test_dry_run_skips_live_weeks(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    _two_week_course(tmp_path)
    monkeypatch.setattr(deploy, "now_et", lambda: _at(2026, 8, 27))
    assert deploy.main(["--all", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "[frozen] WEEKONE" in out
    assert "[dry-run] module 'WEEKTWO'" in out
    assert not (tmp_path / "preview" / "weekone.html").exists()
    assert (tmp_path / "preview" / "weektwo.html").exists()


def test_week_flag_on_live_week_refuses_without_force(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    _two_week_course(tmp_path)
    monkeypatch.setattr(deploy, "now_et", lambda: _at(2026, 8, 27))
    assert deploy.main(["--week", "weekone", "--dry-run"]) != 0
    assert "--force" in capsys.readouterr().out
    assert not (tmp_path / "preview" / "weekone.html").exists()
    assert deploy.main(["--week", "weekone", "--dry-run", "--force"]) == 0
    assert (tmp_path / "preview" / "weekone.html").exists()


def test_activity_verification_frozen_once_open():
    av = {"open": deploy.date(2026, 8, 24)}
    assert deploy.av_is_live(av, _at(2026, 8, 27))
    assert not deploy.av_is_live(av, _at(2026, 8, 20))
    assert not deploy.av_is_live({}, _at(2026, 8, 27))  # no open date: never frozen
