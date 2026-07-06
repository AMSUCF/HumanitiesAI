from pathlib import Path
from simple_syllabus import build_package

def test_build_package_sections(tmp_path):
    idx = tmp_path / "index.md"
    idx.write_text("---\ntitle: X\n---\nintro\n\n## Course Description\n\nBody A "
                   "[wk](weekone.md)\n\n"
                   "## Evaluation and Grading\n\n| a | b |\n|---|---|\n| 1 | 2 |\n",
                   encoding="utf-8")
    out = build_package(idx, tmp_path / "preview", "https://x.y")
    html = out.read_text(encoding="utf-8")
    assert "<h2>Course Description</h2>" in html
    assert "Body A" in html and "<table>" in html
    assert 'data-component="Evaluation and Grading"' in html
    assert 'href="https://x.y/weekone.html"' in html


def test_build_package_includes_preamble_as_instructor_section(tmp_path):
    idx = tmp_path / "index.md"
    idx.write_text("---\ntitle: X\n---\n- **Office Hours:** Wednesdays\n\n"
                   "## Course Description\n\nBody A\n", encoding="utf-8")
    out = build_package(idx, tmp_path / "preview", "https://x.y")
    html = out.read_text(encoding="utf-8")
    assert 'data-component="Instructor Information"' in html
    assert "Wednesdays" in html
    assert html.index("Instructor Information") < html.index("Course Description")
