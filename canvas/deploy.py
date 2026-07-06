from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import frontmatter
import yaml
from dotenv import load_dotenv

from converter import (UNIT_COLORS, apply_canvas_style, due_at_utc, load_week,
                       render_html, split_discussion)

STATE_FILE = Path(".state.json")


def plan_week(path: Path, site_base: str) -> dict:
    doc = load_week(path)
    c = doc.canvas
    if c["unit"] not in UNIT_COLORS:
        raise ValueError(f"{path}: unknown unit '{c['unit']}'")
    page_md, disc_md = split_discussion(doc.body)
    return {
        "stem": path.stem,
        "module": c["module"],
        "points": int(c["points"]),
        "extra_credit": bool(c.get("extra_credit", False)),
        "due_at": due_at_utc(c["due"]),
        "has_discussion": bool(c["discussion"]) and bool(disc_md),
        "page_html": apply_canvas_style(render_html(page_md, site_base), c["unit"]),
        "discussion_html": apply_canvas_style(render_html(disc_md, site_base), c["unit"])
        if disc_md else "",
    }


def _load_state() -> dict:
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}


def _course_root(cfg: dict) -> Path:
    # week files live one directory above canvas/ when run in-place,
    # or in cwd when tests fabricate a flat layout
    for base in (Path("."), Path("..")):
        if (base / (cfg["weeks"][0] + ".md")).exists():
            return base
    raise FileNotFoundError("week files not found relative to cwd")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--week")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--simple-syllabus", action="store_true")
    args = ap.parse_args(argv)

    cfg = yaml.safe_load(Path("course.yml").read_text(encoding="utf-8"))
    root = _course_root(cfg)

    if args.simple_syllabus:
        from simple_syllabus import build_package
        out = build_package(root / cfg["syllabus_file"], Path("preview"))
        print(f"simple syllabus package: {out}")
        return 0

    stems = cfg["weeks"] + cfg.get("extra", []) if args.all else [args.week]
    if not stems or stems == [None]:
        ap.error("pass --all or --week NAME")

    plans = [plan_week(root / f"{s}.md", cfg["site_base"]) for s in stems]

    if args.dry_run:
        prev = Path("preview")
        prev.mkdir(exist_ok=True)
        for p in plans:
            (prev / f"{p['stem']}.html").write_text(p["page_html"], encoding="utf-8")
            if p["has_discussion"]:
                (prev / f"{p['stem']}-discussion.html").write_text(
                    p["discussion_html"], encoding="utf-8")
            print(f"[dry-run] module '{p['module']}' | page | "
                  f"discussion {p['points']}pts due {p['due_at']}"
                  + (" [extra credit]" if p["extra_credit"] else ""))
        return 0

    load_dotenv()
    from canvas_client import CanvasClient
    client = CanvasClient(os.environ["CANVAS_API_URL"],
                          os.environ["CANVAS_API_TOKEN"],
                          os.environ["CANVAS_COURSE_ID"])
    state = _load_state()
    group_id = client.upsert_assignment_group(cfg["assignment_groups"]["exercises"])
    for p in plans:
        st = state.setdefault(p["stem"], {})
        module_id = client.upsert_module(p["module"])
        page_url = client.upsert_page(p["module"], p["page_html"], args.publish)
        client.add_to_module(module_id, "Page", page_url)
        st.update(module_id=module_id, page_url=page_url)
        if p["has_discussion"]:
            title = f"Exercise Discussion: {p['module']}"
            disc_id = client.upsert_discussion(
                title, p["discussion_html"],
                0 if p["extra_credit"] else p["points"],
                p["due_at"], group_id, args.publish,
                known_id=st.get("discussion_id"))
            client.add_to_module(module_id, "Discussion", disc_id)
            st["discussion_id"] = disc_id
        print(f"deployed: {p['module']}")

    if args.all:
        syllabus_post = frontmatter.load(str(root / cfg["syllabus_file"]))
        syllabus_html = render_html(syllabus_post.content, cfg["site_base"])
        client.upsert_page("Syllabus", syllabus_html, args.publish)

        other_group_id = client.upsert_assignment_group(cfg["assignment_groups"]["other"])
        av = cfg["activity_verification"]
        av_id = client.upsert_assignment(
            av["name"], av["points"], due_at_utc(av["due"]), other_group_id,
            ["online_url", "online_text_entry"], args.publish,
            known_id=state.get("activity_verification_id"))
        state["activity_verification_id"] = av_id
        print("deployed: Syllabus page, Activity Verification")

    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
