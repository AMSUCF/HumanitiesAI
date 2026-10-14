import os, time
import pytest
import assets

CFG = {"weeks": ["moduleone"], "extra": ["finalreflection"], "syllabus_file": "index.md"}

def _course(tmp_path):
    (tmp_path / "slides").mkdir()
    (tmp_path / "slides" / "decks.yml").write_text("moduleone: []\n", encoding="utf-8")
    (tmp_path / "slides" / "moduleone.pptx").write_bytes(b"PK")
    (tmp_path / "images").mkdir()
    (tmp_path / "images" / "a.png").write_bytes(b"\x89PNG")
    (tmp_path / "index.md").write_text("---\n---\n[s](slides/moduleone.html)\n", encoding="utf-8")
    (tmp_path / "moduleone.md").write_text(
        '---\ncanvas:\n  module: "Module One: X"\n---\n![x](images/a.png)\n', encoding="utf-8")
    (tmp_path / "finalreflection.md").write_text(
        '---\ncanvas:\n  module: "Finals: Y"\n---\nhi\n', encoding="utf-8")
    later = time.time() + 1000      # the deck is built after its sources
    os.utime(tmp_path / "slides" / "moduleone.pptx", (later, later))
    return tmp_path

def test_find_assets(tmp_path):
    found = assets.find_assets(CFG, _course(tmp_path))
    assert set(found) == {"slides/moduleone.pptx", "images/a.png"}

def test_missing_pptx_is_an_error(tmp_path):
    root = _course(tmp_path); (root / "slides" / "moduleone.pptx").unlink()
    with pytest.raises(SystemExit, match="build_pptx.py"):
        assets.find_assets(CFG, root)

def test_stale_deck_is_an_error(tmp_path):
    root = _course(tmp_path)
    old = time.time() - 100
    os.utime(root / "slides" / "moduleone.pptx", (old, old))
    with pytest.raises(SystemExit, match="moduleone.pptx"):
        assets.check_decks_fresh(root)

def test_deck_older_than_its_module_md_is_an_error(tmp_path):
    # the title slide carries the module name and dates from moduleone.md
    root = _course(tmp_path)
    deck = root / "slides" / "moduleone.pptx"
    old = time.time() - 100
    os.utime(root / "slides" / "decks.yml", (old - 50, old - 50))
    os.utime(deck, (old, old))
    with pytest.raises(SystemExit, match=r"moduleone\.md is newer than moduleone\.pptx.*build_pptx\.py"):
        assets.check_decks_fresh(root)
    os.utime(root / "moduleone.md", (old - 10, old - 10))
    assets.check_decks_fresh(root)            # both sources older: fresh


def test_link_map(tmp_path):
    m = assets.build_link_map(CFG, "/courses/9",
                              {"slides/moduleone.pptx": 5, "images/a.png": 6},
                              {"moduleone": "module-one", "moduleone:lecture": "m1-lecture",
                               "finalreflection": "final", "index": "syllabus"})
    assert m["slides/moduleone.html"] == "/courses/9/files/5"
    assert m["moduleone.html"] == "/courses/9/pages/module-one"
    assert m["index.html"] == "/courses/9/pages/syllabus"
    assert m["images/a.png"] == "/courses/9/files/6/preview"

class FakeClient:
    def __init__(self, live_updated="T1"):
        self.uploads, self.live = [], live_updated
    def upload_file(self, path, folder, ctype):
        self.uploads.append(path.name); return {"id": 5, "updated_at": "T1"}
    def updated_at(self, kind, ref): return self.live
    def find_or_create_page(self, title): return title.lower().replace(" ", "-")

def test_sync_skips_unchanged_and_edited(tmp_path, capsys):
    root = _course(tmp_path); cfg = {**CFG, "self_contained": True}
    state = {}
    c = FakeClient(); assets.sync_assets(c, cfg, root, state)
    assert sorted(c.uploads) == ["a.png", "moduleone.pptx"]
    c = FakeClient(); assets.sync_assets(c, cfg, root, state)
    assert c.uploads == []                                   # same sha: no re-upload
    (root / "slides" / "moduleone.pptx").write_bytes(b"PK2")
    c = FakeClient(live_updated="T2-gta-replaced-it")
    assets.sync_assets(c, cfg, root, state)
    assert c.uploads == []
    assert ("[edited in Canvas] slides/moduleone.pptx was replaced in Canvas Files; not "
            "re-uploaded (pass --overwrite-canvas-edits to upload the repo copy over it)"
            ) in capsys.readouterr().out


class StampClient(FakeClient):
    """Upload response omits updated_at; the follow-up fetch supplies it."""
    def upload_file(self, path, folder, ctype):
        self.uploads.append(path.name); return {"id": 5}


def _synced(tmp_path):
    root = _course(tmp_path); cfg = {**CFG, "self_contained": True}
    state = {}
    assets.sync_assets(FakeClient(), cfg, root, state)
    (root / "slides" / "moduleone.pptx").write_bytes(b"PK2")
    return root, cfg, state


def test_missing_in_canvas_is_skipped(tmp_path, capsys):
    root, cfg, state = _synced(tmp_path)
    capsys.readouterr()
    c = FakeClient(live_updated=None)
    files, _, missing = assets.sync_assets(c, cfg, root, state)
    assert c.uploads == [] and "[missing in Canvas]" in capsys.readouterr().out
    # every known file is checked live, so the unchanged image is missing too
    assert missing == {"slides/moduleone.pptx", "images/a.png"}
    assert files["slides/moduleone.pptx"] == 5      # old id kept, flagged as missing


def test_unchanged_file_deleted_in_canvas_is_missing(tmp_path, capsys):
    # no local rebuild, but the GTA deleted the deck in Canvas Files
    root = _course(tmp_path); cfg = {**CFG, "self_contained": True}
    state = {}
    assets.sync_assets(FakeClient(), cfg, root, state)
    capsys.readouterr()
    c = FakeClient(live_updated=None)
    _, _, missing = assets.sync_assets(c, cfg, root, state)
    assert missing == {"slides/moduleone.pptx", "images/a.png"} and c.uploads == []
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 2 and all(l.startswith("[missing in Canvas]") for l in out)
    assert out[0] == ("[missing in Canvas] slides/moduleone.pptx was deleted or replaced in "
                      "Canvas Files; kept as is (pass --overwrite-canvas-edits to upload the "
                      "repo copy over it)")
    c = FakeClient(live_updated=None)
    _, _, missing = assets.sync_assets(c, cfg, root, state, overwrite=True)
    assert sorted(c.uploads) == ["a.png", "moduleone.pptx"] and missing == set()


def test_unchanged_file_replaced_in_canvas_is_left_alone(tmp_path, capsys):
    # same local sha, different live stamp: that is the GTA's version, kept
    root = _course(tmp_path); cfg = {**CFG, "self_contained": True}
    state = {}
    assets.sync_assets(FakeClient(), cfg, root, state)
    capsys.readouterr()
    c = FakeClient(live_updated="T5-gta")
    _, _, missing = assets.sync_assets(c, cfg, root, state)
    assert c.uploads == [] and missing == set()
    assert capsys.readouterr().out.splitlines() == [
        "[edited in Canvas] slides/moduleone.pptx was replaced in Canvas Files; kept",
        "[edited in Canvas] images/a.png was replaced in Canvas Files; kept"]


def test_sync_reports_nothing_missing_when_edited_or_uploaded(tmp_path):
    root, cfg, state = _synced(tmp_path)
    assert assets.sync_assets(FakeClient(live_updated="T2-gta"), cfg, root, state)[2] == set()
    assert assets.sync_assets(FakeClient(), cfg, root, state)[2] == set()   # uploads


def test_overwrite_reuploads_missing_and_edited(tmp_path):
    for live in (None, "T2-edited"):
        root, cfg, state = _synced(_mk(tmp_path, str(live)))
        c = FakeClient(live_updated=live)
        assets.sync_assets(c, cfg, root, state, overwrite=True)
        # a deleted file comes back even if unchanged here; an edited one only if changed
        want = ["a.png", "moduleone.pptx"] if live is None else ["moduleone.pptx"]
        assert sorted(c.uploads) == want


def test_upload_without_updated_at_fetches_it(tmp_path):
    root = _course(tmp_path); cfg = {**CFG, "self_contained": True}
    state = {}
    c = StampClient(live_updated="T7")
    assets.sync_assets(c, cfg, root, state)
    assert state["files"]["slides/moduleone.pptx"]["updated_at"] == "T7"


def _mk(base, name):
    d = base / name; d.mkdir(); return d
