import os, time
from pathlib import Path
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
    assert c.uploads == [] and "[edited in Canvas]" in capsys.readouterr().out
