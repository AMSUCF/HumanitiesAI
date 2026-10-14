"""Self-contained course assets: decks and page images go into Canvas
Files, and every repo-relative link is rewritten to its Canvas target,
so the course runs with no dependency on the website or this repo."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

PPTX_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
               ".gif": "image/gif", ".webp": "image/webp"}
FOLDERS = {"slides": "Lecture Slides", "images": "Page Images"}
_IMG_REF = re.compile(r'(?:\]\(|src=")(images/[^)"\s#]+)')


def _sources(cfg, root: Path) -> list[Path]:
    stems = cfg["weeks"] + cfg.get("extra", [])
    return [root / cfg["syllabus_file"]] + [root / f"{s}.md" for s in stems]


def find_assets(cfg, root: Path) -> dict[str, Path]:
    found = {}
    for stem in cfg["weeks"]:
        p = root / "slides" / f"{stem}.pptx"
        if not p.exists():
            raise SystemExit(f"missing {p}: run build_pptx.py in {root / 'slides'}")
        found[f"slides/{stem}.pptx"] = p
    for src in _sources(cfg, root):
        for rel in _IMG_REF.findall(src.read_text(encoding="utf-8")):
            if not (root / rel).exists():
                raise SystemExit(f"{src.name}: image {rel} not found")
            found[rel] = root / rel
    return found


def check_decks_fresh(root: Path) -> None:
    yml = root / "slides" / "decks.yml"
    stale = [p.name for p in sorted((root / "slides").glob("*.pptx"))
             if p.stat().st_mtime < yml.stat().st_mtime]
    if stale:
        raise SystemExit(f"decks.yml is newer than {', '.join(stale)}: "
                         f"run build_pptx.py before deploying")


def build_link_map(cfg, course_path, files, pages) -> dict[str, str]:
    m = {"index.html": f"{course_path}/pages/{pages['index']}"}
    for stem in cfg["weeks"]:
        fid = files[f"slides/{stem}.pptx"]
        m[f"slides/{stem}.html"] = m[f"slides/{stem}.pptx"] = f"{course_path}/files/{fid}"
    for stem in cfg["weeks"] + cfg.get("extra", []):
        m[f"{stem}.html"] = f"{course_path}/pages/{pages[stem]}"
    for rel, fid in files.items():
        if rel.startswith("images/"):
            m[rel] = f"{course_path}/files/{fid}/preview"
    return m


def placeholder_ids(cfg, found) -> tuple[dict, dict]:
    files = {rel: f"FILE-{Path(rel).name}" for rel in found}
    pages = {"index": "syllabus"}
    for stem in cfg["weeks"] + cfg.get("extra", []):
        pages[stem] = stem
        pages[f"{stem}:lecture"] = f"{stem}-lecture"
    return files, pages


def slides_html(course_path, api_base, file_id, week_label) -> str:
    href = f"{course_path}/files/{file_id}"
    return (f'<p><a class="instructure_file_link instructure_scribd_file auto_open" '
            f'title="{week_label} slides" href="{href}?wrap=1" '
            f'data-api-endpoint="{api_base}{href}" data-api-returntype="File">'
            f'{week_label} slides (PowerPoint)</a></p>'
            f'<p><a href="{href}/download?download_frd=1">Download the {week_label} '
            f'slides</a> to view them full screen, with speaker notes.</p>')


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sync_assets(client, cfg, root, state, force=False):
    found = find_assets(cfg, root)
    check_decks_fresh(root)
    known = state.setdefault("files", {})
    for rel, path in found.items():
        rec, sha = known.get(rel), _sha(path)
        if rec and rec["sha256"] == sha:
            continue
        if rec and not force:
            live = client.updated_at("files", rec["id"])
            if live is None:
                print(f"[missing in Canvas] {rel} was deleted or replaced in Canvas Files; "
                      f"not re-uploaded (pass --force to upload it again)")
                continue
            if live != rec["updated_at"]:
                print(f"[edited in Canvas] {rel} was replaced in Canvas Files; "
                      f"not re-uploaded (pass --force to override)")
                continue
        ctype = PPTX_TYPE if path.suffix == ".pptx" else IMAGE_TYPES[path.suffix.lower()]
        out = client.upload_file(path, FOLDERS[rel.split("/")[0]], ctype)
        stamp = out.get("updated_at") or client.updated_at("files", out["id"])
        known[rel] = {"id": out["id"], "sha256": sha, "updated_at": stamp}
        print(f"uploaded: {rel}")
    pages = {"index": state.get("syllabus_url") or client.find_or_create_page("Syllabus")}
    state["syllabus_url"] = pages["index"]
    for stem in cfg["weeks"] + cfg.get("extra", []):
        st = state.setdefault(stem, {})
        pages[stem] = st.get("page_url") or client.find_or_create_page(_title(root, stem))
        st["page_url"] = pages[stem]
        if stem in cfg["weeks"]:
            pages[f"{stem}:lecture"] = st.get("lecture_url") or client.find_or_create_page(
                f"{_label(root, stem)} Readings + Lecture")
            st["lecture_url"] = pages[f"{stem}:lecture"]
    return {rel: r["id"] for rel, r in known.items()}, pages


def _title(root, stem):
    import frontmatter
    return frontmatter.load(str(root / f"{stem}.md")).metadata["canvas"]["module"]


def _label(root, stem):
    return _title(root, stem).split(":")[0].strip()
