import textwrap
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
    assert '<h2 id="readings">Readings</h2>' in html and '<h2>Lecture</h2>' in html
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


def test_extract_readings_stops_at_do_subheading():
    # undergrad syllabus: one heading per module, Think / Do as subheadings;
    # only the Think readings belong on the lecture page
    from converter import extract_readings
    syl = textwrap.dedent("""        ### Module One: What Is DH? (Weeks 1-2, January 11 - 24)

        #### Think: Week 1 (January 11 - 17)

        -   Kirschenbaum reading

        #### Do: Week 2 (January 18 - 24)

        -   **Watch:** a video
        -   [**Exercise: Chatbots**](moduleone.md)

        ### Module Two: Text (Weeks 3-4, January 25 - February 7)

        -   Chiang reading
        """)
    out = extract_readings(syl, "Module One")
    assert "Kirschenbaum reading" in out
    assert "Watch" not in out and "Do: Week 2" not in out
    assert "Chiang" not in out


def test_video_embed_regex_matches_canvas_media_iframe():
    live = ('<div>band</div><p><iframe style="width: 480px;" '
            'title="HumanitiesAI_One.mp4" data-media-type="video" '
            'src="https://webcourses.ucf.edu/media_attachments_iframe/1?x=1" '
            'allowfullscreen="allowfullscreen"></iframe></p><p>rest</p>')
    m = deploy.VIDEO_EMBED_RE.search(live)
    assert m and m.group(0).startswith("<p><iframe")
    assert m.group(0).endswith("</iframe></p>")
    assert "rest" not in m.group(0)



def test_plan_week_uses_late_hours(tmp_path):
    wk = tmp_path / "moduleone.md"
    wk.write_text("---\ncanvas:\n  module: \"Module One: X\"\n  week_start: 2027-01-11\n"
                  "  due: 2027-01-24\n  points: 10\n  discussion: true\n  unit: ghosts\n"
                  "  hard_close: true\n---\nBody\n\n### Discussion\n\nQ?\n", encoding="utf-8")
    plan = deploy.plan_week(wk, site_base="https://x.y", late_hours=24)
    assert plan["lock_at"] == "2027-01-26T04:59:00Z"   # hours win over hard_close

def test_main_loads_env_from_cwd_only(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(deploy, "load_dotenv", lambda *a, **k: calls.append(a))
    monkeypatch.chdir(tmp_path)
    # minimal course; no env -> KeyError after load_dotenv is called
    (tmp_path / "course.yml").write_text(
        "site_base: https://x.y\nassignment_groups: {exercises: E, other: O}\n"
        "syllabus_file: index.md\nweeks: [weekone]\n", encoding="utf-8")
    (tmp_path / "weekone.md").write_text(
        "---\ncanvas:\n  module: M1\n  week_start: 2030-01-07\n  due: 2030-01-13\n"
        "  points: 6\n  discussion: false\n  unit: ghosts\n---\nBody\n", encoding="utf-8")
    for k in ("CANVAS_API_URL", "CANVAS_API_TOKEN", "CANVAS_COURSE_ID"):
        monkeypatch.delenv(k, raising=False)
    import pytest
    with pytest.raises(SystemExit):
        deploy.main(["--all"])
    assert calls and Path(calls[0][0]) == tmp_path / ".env"


# --- self-contained mode, course guard, edit guard --------------------------

import pytest
import assets


def _sc_course(tmp_path):
    root = tmp_path / "course"; canvas = root / "canvas"; canvas.mkdir(parents=True)
    (root / "slides").mkdir()
    (root / "slides" / "decks.yml").write_text("moduleone: []\n", encoding="utf-8")
    (root / "slides" / "moduleone.pptx").write_bytes(b"PK")
    (root / "index.md").write_text("---\n---\n## AI Use Policy\n\n[m](moduleone.md)\n", encoding="utf-8")
    (root / "moduleone.md").write_text(
        "---\ncanvas:\n  module: \"Module One: X\"\n  week_start: 2030-01-07\n"
        "  due: 2030-01-20\n  points: 10\n  discussion: true\n  unit: words\n---\n"
        "See [slides](slides/moduleone.html) and [policy](index.md#ai-use-policy).\n\n"
        "### Discussion\n\nQ?\n", encoding="utf-8")
    (canvas / "course.yml").write_text(
        "site_base: https://x.y\nassignment_groups: {exercises: E, other: O}\n"
        "syllabus_file: index.md\nweeks: [moduleone]\nself_contained: true\n"
        "late_window_hours: 24\nunits: {words: {label: Words, color: '#0f766e'}}\n",
        encoding="utf-8")
    _fresh(root / "slides" / "moduleone.pptx")
    return canvas


def _fresh(deck):
    # the deck is built after decks.yml and the module .md, even when a test
    # edits the .md afterwards
    import os, time
    later = time.time() + 1000
    os.utime(deck, (later, later))


def test_self_contained_dry_run_has_no_site_links(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(_sc_course(tmp_path))
    deploy.main(["--all", "--dry-run"])
    page = (tmp_path / "course/canvas/preview/moduleone.html").read_text(encoding="utf-8")
    lecture = (tmp_path / "course/canvas/preview/moduleone-lecture.html").read_text(encoding="utf-8")
    assert "x.y" not in page and "x.y" not in lecture
    assert "/pages/syllabus#ai-use-policy" in page
    assert "instructure_file_link" in lecture and "<iframe" not in lecture
    assert "[unresolved]" not in capsys.readouterr().out


def test_self_contained_unresolved_link_reported(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    md = canvas.parent / "moduleone.md"
    md.write_text(md.read_text(encoding="utf-8").replace("Q?", "[x](notes/thing.pdf)"), encoding="utf-8")
    monkeypatch.chdir(canvas)
    deploy.main(["--all", "--dry-run"])
    assert "[unresolved] moduleone: notes/thing.pdf" in capsys.readouterr().out


def _set_env(monkeypatch):
    for k, v in {"CANVAS_API_URL": "https://c.t", "CANVAS_API_TOKEN": "t",
                 "CANVAS_COURSE_ID": "1"}.items():
        monkeypatch.setenv(k, v)


def test_course_guard_aborts_on_wrong_course(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    (canvas / "course.yml").write_text((canvas / "course.yml").read_text() +
                                       "expect_course_code: '3861'\n")
    monkeypatch.chdir(canvas)
    _set_env(monkeypatch)

    class Wrong:
        def __init__(self, *a): pass
        def course_info(self): return {"name": "Humanities AI", "course_code": "ENG6806"}
        def __getattr__(self, n): raise AssertionError(f"wrote to wrong course via {n}")
    monkeypatch.setattr("canvas_client.CanvasClient", Wrong)
    with pytest.raises(SystemExit, match="3861"):
        deploy.main(["--all"])


def _slug(title):
    return title.lower().replace(" ", "-").replace(":", "")


class FakeCanvas:
    """Records every call; updated_at answers from `live`, else a stable stamp
    (an exception in `live` is raised). `removed` items were taken out of
    their module in Canvas; `modules`/`pages` already exist in the course."""
    def __init__(self, live=None, code="ENG3861-0001", removed=(), modules=(), pages=()):
        self.calls, self.bodies, self.live, self.code = [], {}, dict(live or {}), code
        self.removed, self.modules, self.pages = set(removed), list(modules), set(pages)
        self.repositions, self.module_kw = [], []
    def course_info(self): return {"name": "Humanities and AI", "course_code": self.code}
    def upsert_assignment_group(self, name): self.calls.append(("group", name)); return 7
    def upsert_assignment(self, name, *a, known_id=None, **k):
        self.calls.append(("assignment", name, known_id)); return known_id or 8
    def upsert_module(self, name, **k):
        self.calls.append(("module", name)); self.module_kw.append(k); return 11
    def publish_page(self, url): self.calls.append(("publish", "page", url))
    def publish_discussion(self, i): self.calls.append(("publish", "discussion", i))
    def publish_assignment(self, i): self.calls.append(("publish", "assignment", i))
    def publish_module(self, i): self.calls.append(("publish", "module", i))
    def module_names(self): self.calls.append(("list-modules",)); return list(self.modules)
    def find_page(self, title):
        self.calls.append(("find-page", title))
        return _slug(title) if title in self.pages else None
    def upsert_page(self, title, body, published=False, known_url=None):
        self.calls.append(("page", title, published, known_url)); self.bodies[title] = body
        return known_url or _slug(title)
    def upsert_discussion(self, title, message, *a, known_id=None, **k):
        self.calls.append(("discussion", title, known_id)); self.bodies[title] = message
        return known_id or 21
    def add_to_module(self, module_id, kind, ref, position=None, reposition=True,
                      add_missing=True):
        if (kind, ref) in self.removed and not add_missing:
            self.calls.append(("not-added", kind, ref)); return False
        self.calls.append(("item", kind, ref, position)); self.repositions.append(reposition)
        return True
    def get_page_body(self, url): return None
    def upload_file(self, path, folder, ctype):
        self.calls.append(("upload", path.name)); return {"id": 5, "updated_at": "F1"}
    def find_or_create_page(self, title):
        self.calls.append(("reserve", title)); return _slug(title)
    def updated_at(self, kind, ref):
        v = self.live.get((kind, ref), f"{kind}/{ref}@T1")
        if isinstance(v, Exception):
            raise v
        return v
    def of(self, kind): return [c for c in self.calls if c[0] == kind]


def _live(monkeypatch, canvas, fake, state=None):
    monkeypatch.chdir(canvas)
    _set_env(monkeypatch)
    if state is not None:
        (canvas / ".state.json").write_text(json.dumps(state), encoding="utf-8")
    monkeypatch.setattr("canvas_client.CanvasClient", lambda *a: fake)


def _state(canvas):
    return json.loads((canvas / ".state.json").read_text(encoding="utf-8"))


def test_course_guard_passes_and_names_course(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    (canvas / "course.yml").write_text((canvas / "course.yml").read_text() +
                                       "expect_course_code: '3861'\n")
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--week", "moduleone"]) == 0
    assert "deploying to: Humanities and AI (ENG3861-0001)" in capsys.readouterr().out


def test_self_contained_live_wires_deck_file_item(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--week", "moduleone"]) == 0
    assert fake.of("upload") == [("upload", "moduleone.pptx")]
    assert fake.of("item") == [("item", "Page", "module-one-readings-+-lecture", 1),
                               ("item", "File", 5, 2),
                               ("item", "Page", "module-one-x", 3),
                               ("item", "Discussion", 21, 4)]
    lecture = fake.bodies["Module One Readings + Lecture"]
    assert "/courses/1/files/5" in lecture and "https://c.t/api/v1/courses/1/files/5" in lecture
    assert "<iframe" not in lecture
    page = fake.bodies["Module One: X"]
    assert "/courses/1/pages/syllabus#ai-use-policy" in page and "x.y" not in page
    st = _state(canvas)["moduleone"]
    assert st["lecture_updated"] == "pages/module-one-readings-+-lecture@T1"
    assert st["page_updated"] == "pages/module-one-x@T1"
    assert st["discussion_updated"] == "discussion_topics/21@T1"


def test_live_unresolved_link_aborts_before_any_page_write(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    md = canvas.parent / "moduleone.md"
    md.write_text(md.read_text(encoding="utf-8").replace(
        "Q?", "[x](notes/thing.pdf) and [y](notes/thing.pdf)"), encoding="utf-8")
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake)
    with pytest.raises(SystemExit, match="moduleone: notes/thing.pdf") as e:
        deploy.main(["--week", "moduleone"])
    assert str(e.value).count("notes/thing.pdf") == 1          # deduplicated
    assert not fake.of("page") and not fake.of("module") and not fake.of("discussion")
    assert _state(canvas)["files"]["slides/moduleone.pptx"]["id"] == 5   # sync recorded


def test_edit_guard_skips_page_edited_in_canvas(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(live={("pages", "module-one-x"): "T2-gta-edit"})
    _live(monkeypatch, canvas, fake, state={"moduleone": {
        "module_id": 11, "page_url": "module-one-x", "page_updated": "T1"}})
    assert deploy.main(["--week", "moduleone"]) == 0
    assert not [c for c in fake.of("page") if c[1] == "Module One: X"]
    assert ("[edited in Canvas] Module One: X was edited in Canvas; not redeployed "
            "(pass --overwrite-canvas-edits to override)") in capsys.readouterr().out
    assert not fake.of("publish")              # no --publish: nothing published
    # the skipped page keeps its place in the module
    assert ("item", "Page", "module-one-x", 3) in fake.calls
    assert _state(canvas)["moduleone"]["page_updated"] == "T1"


def test_edit_guard_skips_discussion_deleted_in_canvas(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(live={("discussion_topics", 21): None})
    _live(monkeypatch, canvas, fake, state={"moduleone": {
        "module_id": 11, "discussion_id": 21, "discussion_updated": "sha:abc"}})
    assert deploy.main(["--week", "moduleone"]) == 0
    assert not fake.of("discussion")
    assert not [c for c in fake.of("item") if c[1] == "Discussion"]   # not re-added
    assert ("[missing in Canvas] Exercise Discussion: Module One: X was deleted in Canvas; "
            "not recreated (pass --overwrite-canvas-edits to recreate it)"
            ) in capsys.readouterr().out


def test_edit_guard_overwrite_overrides_and_restamps(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(live={("pages", "module-one-x"): "T2-gta-edit"})
    _live(monkeypatch, canvas, fake, state={"moduleone": {
        "module_id": 11, "page_url": "module-one-x", "page_updated": "T1"}})
    assert deploy.main(["--week", "moduleone", "--overwrite-canvas-edits"]) == 0
    assert ("page", "Module One: X", False, "module-one-x") in fake.calls
    assert "[edited in Canvas]" not in capsys.readouterr().out
    assert _state(canvas)["moduleone"]["page_updated"] == "T2-gta-edit"


def test_overwrite_recreates_discussion_deleted_in_canvas(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    # the recreated topic gets a new id (21); the deleted one was 31
    fake = FakeCanvas(live={("discussion_topics", 31): None})
    _live(monkeypatch, canvas, fake, state={"moduleone": {
        "module_id": 11, "discussion_id": 31, "discussion_updated": "sha:abc"}})
    assert deploy.main(["--week", "moduleone", "--overwrite-canvas-edits"]) == 0
    assert ("discussion", "Exercise Discussion: Module One: X", None) in fake.calls


def _with_av(canvas, extra=""):
    (canvas / "course.yml").write_text(
        (canvas / "course.yml").read_text() +
        "activity_verification: {name: AV, points: 5, open: 2030-01-07, due: 2030-01-11}\n"
        + extra, encoding="utf-8")


def test_syllabus_rendered_with_link_map_and_guarded(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    _with_av(canvas)
    fake = FakeCanvas(live={("pages", "syllabus"): "T9"})
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--all"]) == 0
    syl = fake.bodies["Syllabus"]
    assert 'href="/courses/1/pages/module-one-x"' in syl and "x.y" not in syl
    assert _state(canvas)["syllabus_updated"] == "T9"
    # second run: the GTA edited the syllabus in Canvas
    fake2 = FakeCanvas(live={("pages", "syllabus"): "T10-gta"})
    monkeypatch.setattr("canvas_client.CanvasClient", lambda *a: fake2)
    capsys.readouterr()
    assert deploy.main(["--all"]) == 0
    assert not [c for c in fake2.of("page") if c[1] == "Syllabus"]
    assert "[edited in Canvas] Syllabus" in capsys.readouterr().out


def test_self_contained_dry_run_previews_syllabus(tmp_path, monkeypatch):
    monkeypatch.chdir(_sc_course(tmp_path))
    deploy.main(["--all", "--dry-run"])
    syl = (tmp_path / "course/canvas/preview/syllabus.html").read_text(encoding="utf-8")
    assert '<h2 id="ai-use-policy">' in syl
    assert 'href="/courses/COURSE/pages/moduleone"' in syl


def test_instructor_guide_missing_file_is_an_error(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    _with_av(canvas, "instructor_guide: instructor-guide.md\n")
    monkeypatch.chdir(canvas)
    with pytest.raises(SystemExit, match="instructor-guide.md"):
        deploy.main(["--all", "--dry-run"])


def _with_guide(canvas):
    _with_av(canvas, "instructor_guide: instructor-guide.md\n")
    (canvas / "instructor-guide.md").write_text(
        "---\ntitle: Instructor Guide\n---\n## For the GTA\n\n"
        "See [the syllabus](../index.md#ai-use-policy) and [m1](../moduleone.md).\n",
        encoding="utf-8")


def test_instructor_guide_dry_run_preview(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    _with_guide(canvas)
    monkeypatch.chdir(canvas)
    deploy.main(["--all", "--dry-run"])
    guide = (canvas / "preview" / "instructor-guide.html").read_text(encoding="utf-8")
    assert '<h2 id="for-the-gta">' in guide
    # links written relative to the guide's own folder don't resolve: reported
    assert "[unresolved] instructor-guide.md: ../index.html" in capsys.readouterr().out


def test_instructor_guide_deployed_unpublished_outside_modules(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    _with_guide(canvas)
    g = canvas / "instructor-guide.md"
    g.write_text(g.read_text(encoding="utf-8").replace("../", ""), encoding="utf-8")
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--all", "--publish"]) == 0
    title = "Instructor Guide (not visible to students)"
    assert ("page", title, False, None) in fake.calls
    assert "/courses/1/pages/syllabus#ai-use-policy" in fake.bodies[title]
    assert not [c for c in fake.of("item") if c[2] == _slug(title)]
    st = _state(canvas)
    assert st["guide_url"] == _slug(title)
    assert st["guide_updated"] == f"pages/{_slug(title)}@T1"
    # guarded like every other page
    fake2 = FakeCanvas(live={("pages", _slug(title)): "T2-gta"})
    monkeypatch.setattr("canvas_client.CanvasClient", lambda *a: fake2)
    capsys.readouterr()
    assert deploy.main(["--all"]) == 0
    assert not [c for c in fake2.of("page") if c[1] == title]
    assert f"[edited in Canvas] {title}" in capsys.readouterr().out


def _grad_course(tmp_path):
    (tmp_path / "course.yml").write_text(
        "site_base: https://x.y\nassignment_groups: {exercises: E, other: O}\n"
        "syllabus_file: index.md\nweeks: [weekone]\n"
        "activity_verification: {name: AV, points: 6, open: 2030-01-07, due: 2030-01-11}\n",
        encoding="utf-8")
    (tmp_path / "index.md").write_text("---\n---\n## Policy\n\n[w](weekone.md)\n",
                                       encoding="utf-8")
    (tmp_path / "weekone.md").write_text(
        "---\ncanvas:\n  module: \"Week One: G\"\n  week_start: 2030-01-07\n"
        "  due: 2030-01-13\n  points: 6\n  discussion: true\n  unit: ghosts\n---\n"
        "Body [s](slides/weekone.html)\n\n### Discussion\n\nQ?\n", encoding="utf-8")
    return tmp_path


class NoGuardCanvas(FakeCanvas):
    """A grad-course client: the edit guard must never ask for updated_at."""
    def updated_at(self, kind, ref):
        raise AssertionError(f"updated_at({kind!r}, {ref!r}) called outside self-contained")
    def module_names(self):
        raise AssertionError("lost-state check outside self-contained")
    def find_page(self, title):
        raise AssertionError("lost-state check outside self-contained")


def test_grad_live_run_unchanged(tmp_path, monkeypatch, capsys):
    canvas = _grad_course(tmp_path)
    fake = NoGuardCanvas(code="ENG6806")
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--all"]) == 0
    assert "deploying to: Humanities and AI (ENG6806)" in capsys.readouterr().out
    assert not fake.of("upload") and not fake.of("reserve")
    assert [c[1] for c in fake.of("item")] == ["Page", "Page", "Discussion"]
    lecture = fake.bodies["Week One Readings + Lecture"]
    assert 'iframe src="https://x.y/slides/weekone.html"' in lecture
    assert 'href="https://x.y/slides/weekone.html"' in fake.bodies["Week One: G"]
    assert 'href="https://x.y/weekone.html"' in fake.bodies["Syllabus"]
    st = _state(canvas)
    assert not [k for k in st["weekone"] if k.endswith("_updated")]
    assert "syllabus_updated" not in st and "av_updated" not in st
    assert "module_items" not in st["weekone"]
    # grad modules are always upserted (name, unlock_at) and items repositioned
    assert fake.of("module") == [("module", "Week One: G")]
    assert fake.module_kw[0]["unlock_at"] and set(fake.repositions) == {True}


def test_grad_live_run_ignores_stale_markers(tmp_path, monkeypatch, capsys):
    # grad lecture pages are edited in Canvas on purpose (hand-added videos):
    # markers left in state must not make the deployer skip anything
    canvas = _grad_course(tmp_path)
    fake = NoGuardCanvas(code="ENG6806")
    _live(monkeypatch, canvas, fake, state={
        "syllabus_url": "syllabus", "syllabus_updated": "OLD",
        "weekone": {"module_id": 11, "lecture_url": "week-one-readings-+-lecture",
                    "lecture_updated": "OLD", "page_url": "week-one-g",
                    "page_updated": "OLD", "discussion_id": 21,
                    "discussion_updated": "OLD"}})
    assert deploy.main(["--all"]) == 0
    assert "in Canvas]" not in capsys.readouterr().out
    assert [c[1] for c in fake.of("page")] == ["Week One Readings + Lecture", "Week One: G",
                                               "Syllabus"]
    assert fake.of("discussion") == [("discussion", "Exercise Discussion: Week One: G", 21)]
    assert [c[1] for c in fake.of("item")] == ["Page", "Page", "Discussion"]


@pytest.mark.parametrize("stored_sha", [
    "an-older-build",                                    # rebuilt locally since
    __import__("hashlib").sha256(b"PK").hexdigest(),     # unchanged locally
])
def test_deck_missing_in_canvas_gets_no_file_item(tmp_path, monkeypatch, capsys, stored_sha):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(live={("files", 5): None})
    _live(monkeypatch, canvas, fake, state={"files": {"slides/moduleone.pptx": {
        "id": 5, "sha256": stored_sha, "updated_at": "F1"}}})
    assert deploy.main(["--week", "moduleone"]) == 0
    assert "[missing in Canvas] slides/moduleone.pptx" in capsys.readouterr().out
    assert not fake.of("upload")
    assert fake.of("item") == [("item", "Page", "module-one-readings-+-lecture", 1),
                               ("item", "Page", "module-one-x", 2),
                               ("item", "Discussion", 21, 3)]


def _stamped_state():
    return {"moduleone": {
        "module_id": 11,
        "lecture_url": "module-one-readings-+-lecture",
        "lecture_updated": "pages/module-one-readings-+-lecture@T1",
        "page_url": "module-one-x", "page_updated": "pages/module-one-x@T1",
        "discussion_id": 21, "discussion_updated": "discussion_topics/21@T1"}}


class PublishBumps(FakeCanvas):
    """Publishing a module publishes its items, bumping their updated_at."""
    bumped = False
    def upsert_module(self, name, **k):
        self.bumped = self.bumped or bool(k.get("published"))
        return super().upsert_module(name, **k)
    def publish_module(self, i):
        self.bumped = True
        return super().publish_module(i)
    def updated_at(self, kind, ref):
        v = super().updated_at(kind, ref)
        return f"{v}+published" if self.bumped and kind != "files" else v


def test_module_publish_does_not_trip_the_edit_guard(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    fake = PublishBumps()
    _live(monkeypatch, canvas, fake, state=_stamped_state())
    assert deploy.main(["--week", "moduleone", "--publish"]) == 0
    assert "in Canvas]" not in capsys.readouterr().out
    assert [c[1] for c in fake.of("page")] == ["Module One Readings + Lecture", "Module One: X"]
    assert fake.of("discussion") == [("discussion", "Exercise Discussion: Module One: X", 21)]
    st = _state(canvas)["moduleone"]
    assert st["page_updated"] == "pages/module-one-x@T1+published"   # re-stamped after


def test_lecture_edited_in_canvas_is_skipped_and_keeps_its_slot(tmp_path, monkeypatch, capsys):
    # the GTA added a lecture video in Canvas
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(live={("pages", "module-one-readings-+-lecture"): "T2-gta-video"})
    _live(monkeypatch, canvas, fake, state=_stamped_state())
    assert deploy.main(["--week", "moduleone"]) == 0
    assert "[edited in Canvas] Module One Readings + Lecture" in capsys.readouterr().out
    assert [c[1] for c in fake.of("page")] == ["Module One: X"]
    assert fake.of("item") == [("item", "Page", "module-one-readings-+-lecture", 1),
                               ("item", "File", 5, 2),
                               ("item", "Page", "module-one-x", 3),
                               ("item", "Discussion", 21, 4)]


def test_page_missing_in_canvas_gives_up_its_position(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(live={("pages", "module-one-readings-+-lecture"): None})
    _live(monkeypatch, canvas, fake, state=_stamped_state())
    assert deploy.main(["--week", "moduleone"]) == 0
    assert "[missing in Canvas] Module One Readings + Lecture" in capsys.readouterr().out
    assert fake.of("item") == [("item", "File", 5, 1),
                               ("item", "Page", "module-one-x", 2),
                               ("item", "Discussion", 21, 3)]


@pytest.mark.parametrize("status, hint", [(401, "fresh CANVAS_API_TOKEN"), (403, "HTTP 403"),
                                          (404, "check CANVAS_COURSE_ID in .env")])
def test_course_info_http_error_is_a_clean_exit(tmp_path, monkeypatch, status, hint):
    import requests

    class Rejected(FakeCanvas):
        def course_info(self):
            r = requests.Response(); r.status_code = status
            raise requests.HTTPError(f"{status} Client Error", response=r)
    canvas = _sc_course(tmp_path)
    _live(monkeypatch, canvas, Rejected())
    with pytest.raises(SystemExit, match=hint):
        deploy.main(["--week", "moduleone"])


def test_grad_dry_run_writes_no_syllabus_preview(tmp_path, monkeypatch):
    monkeypatch.chdir(_grad_course(tmp_path))
    deploy.main(["--all", "--dry-run"])
    assert (tmp_path / "preview" / "weekone-lecture.html").exists()
    assert not (tmp_path / "preview" / "syllabus.html").exists()


# --- final fix wave: --overwrite-canvas-edits (R15) --------------------------

def test_force_no_longer_overrides_the_edit_guard(tmp_path, monkeypatch, capsys):
    # --force is the freeze override only; the GTA's edit survives it
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(live={("pages", "module-one-x"): "T2-gta-edit"})
    _live(monkeypatch, canvas, fake, state={"moduleone": {
        "module_id": 11, "page_url": "module-one-x", "page_updated": "T1"}})
    assert deploy.main(["--week", "moduleone", "--force"]) == 0
    assert not [c for c in fake.of("page") if c[1] == "Module One: X"]
    out = capsys.readouterr().out
    assert "[edited in Canvas] Module One: X" in out and "overwritten" not in out


def test_force_does_not_reupload_a_replaced_deck(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    state = {"files": {"slides/moduleone.pptx": {
        "id": 5, "sha256": "an-older-build", "updated_at": "F1"}}}
    fake = FakeCanvas(live={("files", 5): "F2-gta-replaced"})
    _live(monkeypatch, canvas, fake, state=state)
    assert deploy.main(["--week", "moduleone", "--force"]) == 0
    assert not fake.of("upload")
    assert "[edited in Canvas] slides/moduleone.pptx was replaced" in capsys.readouterr().out
    fake = FakeCanvas(live={("files", 5): "F2-gta-replaced"})
    _live(monkeypatch, canvas, fake, state=state)
    assert deploy.main(["--week", "moduleone", "--overwrite-canvas-edits"]) == 0
    assert fake.of("upload") == [("upload", "moduleone.pptx")]


def test_overwrite_flag_warns_at_start_of_run(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--week", "moduleone", "--overwrite-canvas-edits"]) == 0
    first = capsys.readouterr().out.splitlines()[0]
    assert "--overwrite-canvas-edits" in first and "overwritten" in first


# --- I3: --publish publishes items kept as edited -----------------------------

def test_publish_publishes_items_kept_as_edited(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    lec = "module-one-readings-+-lecture"
    fake = FakeCanvas(live={("pages", lec): "T2-gta", ("pages", "module-one-x"): "T2-gta",
                            ("discussion_topics", 21): "T2-gta"})
    _live(monkeypatch, canvas, fake, state=_stamped_state())
    assert deploy.main(["--week", "moduleone", "--publish"]) == 0
    assert not fake.of("page") and not fake.of("discussion")       # content kept
    assert fake.of("publish") == [("publish", "module", 11), ("publish", "page", lec),
                                  ("publish", "page", "module-one-x"),
                                  ("publish", "discussion", 21)]
    out = capsys.readouterr().out
    for title in ("Module One Readings + Lecture", "Module One: X",
                  "Exercise Discussion: Module One: X"):
        assert f"[edited in Canvas] {title}: kept your Canvas version, published it" in out
    st = _state(canvas)["moduleone"]
    assert st["page_updated"] == "pages/module-one-x@T1"            # not re-stamped


def test_publish_publishes_edited_syllabus_never_the_guide(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    _with_guide(canvas)
    g = canvas / "instructor-guide.md"
    g.write_text(g.read_text(encoding="utf-8").replace("../", ""), encoding="utf-8")
    guide = _slug(deploy.GUIDE_TITLE)
    state = {**_stamped_state(), "syllabus_url": "syllabus", "syllabus_updated": "T1",
             "guide_url": guide, "guide_updated": "T1"}
    fake = FakeCanvas(live={("pages", "syllabus"): "T2-gta", ("pages", guide): "T2-gta"})
    _live(monkeypatch, canvas, fake, state=state)
    assert deploy.main(["--all", "--publish"]) == 0
    assert ("publish", "page", "syllabus") in fake.calls
    assert ("publish", "page", guide) not in fake.calls
    assert not [c for c in fake.of("page") if c[1] in ("Syllabus", deploy.GUIDE_TITLE)]
    assert "[edited in Canvas] Syllabus: kept your Canvas version, published it" in \
        capsys.readouterr().out


# --- I5: a lost .state.json -----------------------------------------------------

@pytest.mark.parametrize("existing", [
    {"modules": ["Module One: X"]}, {"pages": ["Syllabus"]},
    {"pages": ["Instructor Guide (not visible to students)"]}])
@pytest.mark.parametrize("state_text", [None, "", "{}"])
def test_lost_state_aborts_when_course_has_content(tmp_path, monkeypatch, existing,
                                                    state_text):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(**existing)
    _live(monkeypatch, canvas, fake)
    if state_text is not None:
        (canvas / ".state.json").write_text(state_text, encoding="utf-8")
    with pytest.raises(SystemExit, match=r"state.*missing.*--overwrite-canvas-edits"):
        deploy.main(["--week", "moduleone"])
    assert not [c for c in fake.calls if c[0] not in ("list-modules", "find-page")]


def test_lost_state_with_overwrite_proceeds(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(modules=["Module One: X"], pages=["Syllabus"])
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--week", "moduleone", "--overwrite-canvas-edits"]) == 0
    assert fake.of("upload") and fake.of("page")


def test_fresh_course_with_no_state_proceeds(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas(modules=["Some Other Module"])
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--week", "moduleone"]) == 0
    assert fake.of("list-modules") and fake.of("upload")


@pytest.mark.parametrize("failure", ["http", "none"])
def test_failed_stamp_read_after_upsert_fails_loudly(tmp_path, monkeypatch, failure):
    import requests
    canvas = _sc_course(tmp_path)
    err = requests.HTTPError("500 Server Error") if failure == "http" else None
    fake = FakeCanvas(live={("pages", "module-one-x"): err})
    _live(monkeypatch, canvas, fake)
    with pytest.raises(SystemExit, match="Module One: X"):
        deploy.main(["--week", "moduleone"])
    assert ("page", "Module One: X", False, "module-one-x") in fake.calls
    # never a url with no stamp: the next run treats the page as edited
    st = _state(canvas)["moduleone"]
    assert st["page_url"] == "module-one-x" and st["page_updated"] == deploy.UNREAD_STAMP


# --- I6: module structure and Activity Verification (R16) ---------------------

def test_known_module_is_not_renamed_or_redated(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake, state=_stamped_state())
    assert deploy.main(["--week", "moduleone"]) == 0
    assert not fake.of("module") and not fake.of("publish")
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake, state=_stamped_state())
    assert deploy.main(["--week", "moduleone", "--publish"]) == 0
    assert not fake.of("module") and fake.of("publish") == [("publish", "module", 11)]


def test_new_module_is_created_and_overwrite_updates_known(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--week", "moduleone"]) == 0
    assert fake.of("module") == [("module", "Module One: X")]
    assert fake.module_kw[0]["unlock_at"] == "2030-01-07T05:00:00Z"
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake, state=_stamped_state())
    assert deploy.main(["--week", "moduleone", "--overwrite-canvas-edits"]) == 0
    assert fake.of("module") == [("module", "Module One: X")]
    assert fake.module_kw[0]["known_id"] == 11


def test_self_contained_items_are_never_moved(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake, state=_stamped_state())
    assert deploy.main(["--week", "moduleone"]) == 0
    assert fake.repositions and set(fake.repositions) == {False}
    assert _state(canvas)["moduleone"]["module_items"] == [
        "Page:module-one-readings-+-lecture", "File:5", "Page:module-one-x", "Discussion:21"]


def test_item_removed_from_module_in_canvas_is_not_readded(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    state = _stamped_state()
    state["moduleone"]["module_items"] = [
        "Page:module-one-readings-+-lecture", "File:5", "Page:module-one-x", "Discussion:21"]
    fake = FakeCanvas(removed={("Page", "module-one-x")})
    _live(monkeypatch, canvas, fake, state=state)
    assert deploy.main(["--week", "moduleone"]) == 0
    assert ("not-added", "Page", "module-one-x") in fake.calls
    assert fake.of("item")[-1] == ("item", "Discussion", 21, 3)      # gave up its slot
    assert ("[removed in Canvas] Module One: X was removed from its module in Canvas; "
            "not re-added (pass --overwrite-canvas-edits to re-add it)"
            ) in capsys.readouterr().out
    assert "Page:module-one-x" in _state(canvas)["moduleone"]["module_items"]
    fake = FakeCanvas(removed={("Page", "module-one-x")})
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--week", "moduleone", "--overwrite-canvas-edits"]) == 0
    assert ("item", "Page", "module-one-x", 3) in fake.calls


def _av_state(**av):
    return {**_stamped_state(), "syllabus_url": "syllabus",
            "syllabus_updated": "pages/syllabus@T1", **av}


def test_activity_verification_is_stamped_and_guarded(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    _with_av(canvas)
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake)
    assert deploy.main(["--all"]) == 0
    st = _state(canvas)
    assert st["activity_verification_id"] == 8 and st["av_updated"] == "assignments/8@T1"
    # edited in Canvas: kept; with --publish, published as is
    fake = FakeCanvas(live={("assignments", 8): "A2-gta"})
    _live(monkeypatch, canvas, fake)
    capsys.readouterr()
    assert deploy.main(["--all", "--publish"]) == 0
    assert not fake.of("assignment")
    assert ("publish", "assignment", 8) in fake.calls
    assert "[edited in Canvas] AV: kept your Canvas version, published it" in \
        capsys.readouterr().out
    assert _state(canvas)["av_updated"] == "assignments/8@T1"


def test_activity_verification_deleted_in_canvas(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    _with_av(canvas)
    state = _av_state(activity_verification_id=9, av_updated="assignments/9@T1")
    fake = FakeCanvas(live={("assignments", 9): None})
    _live(monkeypatch, canvas, fake, state=state)
    assert deploy.main(["--all", "--publish"]) == 0
    assert not fake.of("assignment") and not [c for c in fake.of("publish")
                                              if c[1] == "assignment"]
    assert "[missing in Canvas] AV was deleted in Canvas" in capsys.readouterr().out
    fake = FakeCanvas(live={("assignments", 9): None})
    _live(monkeypatch, canvas, fake, state=state)
    assert deploy.main(["--all", "--overwrite-canvas-edits"]) == 0
    assert fake.of("assignment") == [("assignment", "AV", None)]      # recreated


# --- M3: credentials -----------------------------------------------------------

def test_missing_env_is_a_clean_exit_naming_the_env_path(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    monkeypatch.chdir(canvas)
    for k in ("CANVAS_API_URL", "CANVAS_API_TOKEN", "CANVAS_COURSE_ID"):
        monkeypatch.delenv(k, raising=False)
    with pytest.raises(SystemExit) as e:
        deploy.main(["--week", "moduleone"])
    msg = str(e.value)
    assert str(canvas / ".env") in msg and "CANVAS_API_URL" in msg


# --- M5b: syllabus fragment links ------------------------------------------------

def _broken_anchors(canvas):
    syl = canvas.parent / "index.md"
    syl.write_text("---\n---\n[toc](#ai-use-policy) [old](#module-one-old-dates)\n\n"
                   "## AI Use Policy\n\n[m](moduleone.md)\n", encoding="utf-8")
    md = canvas.parent / "moduleone.md"
    md.write_text(md.read_text(encoding="utf-8").replace(
        "Q?", "Q? [see](index.md#gone)"), encoding="utf-8")


def test_dry_run_reports_broken_syllabus_anchors(tmp_path, monkeypatch, capsys):
    canvas = _sc_course(tmp_path)
    _broken_anchors(canvas)
    monkeypatch.chdir(canvas)
    assert deploy.main(["--all", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "[broken anchor] index.md: #module-one-old-dates" in out
    assert "[broken anchor] moduleone: #gone" in out
    assert "#ai-use-policy" not in out
    # a --week run still checks the module's links against the syllabus
    assert deploy.main(["--week", "moduleone", "--dry-run"]) == 0
    assert "[broken anchor] moduleone: #gone" in capsys.readouterr().out


def test_live_run_with_broken_anchor_aborts_before_any_write(tmp_path, monkeypatch):
    canvas = _sc_course(tmp_path)
    _broken_anchors(canvas)
    fake = FakeCanvas()
    _live(monkeypatch, canvas, fake)
    with pytest.raises(SystemExit, match="moduleone: #gone"):
        deploy.main(["--week", "moduleone"])
    assert not fake.of("page") and not fake.of("module") and not fake.of("discussion")
