from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, time
from pathlib import Path

import frontmatter
import yaml
from dotenv import load_dotenv

from converter import (TZ, UNIT_COLORS, apply_canvas_style, due_at_utc,
                       extract_readings, load_week, lock_at_utc, render_html,
                       split_discussion, unlock_at_utc)

STATE_FILE = Path(".state.json")

# an uploaded Canvas video embed, hand-placed on a live lecture page —
# deploys keep it in place of the placeholder paragraph
VIDEO_EMBED_RE = re.compile(
    r'<p><iframe[^>]*data-media-type="video".*?</iframe></p>', re.DOTALL)


def now_et() -> datetime:
    return datetime.now(TZ)


def is_live(start_date: date, now: datetime | None = None) -> bool:
    """A module is live from midnight ET on its start date.

    Live content is frozen: students are already working in it, so deploys
    leave it alone unless --force is passed.
    """
    now = now or now_et()
    return datetime.combine(start_date, time(0, 0), tzinfo=TZ) <= now


def av_is_live(av: dict, now: datetime | None = None) -> bool:
    """Activity Verification freezes once its open date has passed."""
    return bool(av.get("open")) and is_live(av["open"], now)


def plan_week(path: Path, site_base: str, syllabus_md: str = "") -> dict:
    doc = load_week(path)
    c = doc.canvas
    if c["unit"] not in UNIT_COLORS:
        raise ValueError(f"{path}: unknown unit '{c['unit']}'")
    page_md, disc_md = split_discussion(doc.body)
    week_label = c["module"].split(":")[0].strip()
    slides_url = f"{site_base}/slides/{path.stem}.html"
    readings_md = extract_readings(syllabus_md, week_label) if syllabus_md else ""
    readings_html = (render_html(f"## Readings\n\n{readings_md}", site_base)
                     if readings_md else "")
    placeholder = (f"<p><em>The {week_label} video lecture will be posted "
                   f"here at the start of the week.</em></p>")
    lecture_html = apply_canvas_style(
        readings_html
        + "<h2>Lecture</h2>"
        + placeholder
        + f'<p><strong>Slides:</strong> <a href="{slides_url}">open the '
        f"{week_label} slides in a new tab</a></p>"
        f'<div style="position: relative; width: 100%; padding-bottom: 56.25%; '
        f'height: 0; overflow: hidden;">'
        f'<iframe src="{slides_url}" title="{week_label} slides" '
        f'style="position: absolute; top: 0; left: 0; width: 100%; '
        f'height: 100%; border: 1px solid #c6d4cf; border-radius: 6px;" '
        f'allowfullscreen></iframe></div>', c["unit"])
    return {
        "stem": path.stem,
        "module": c["module"],
        "week_start": c["week_start"],
        "points": int(c["points"]),
        "extra_credit": bool(c.get("extra_credit", False)),
        "due_at": due_at_utc(c["due"]),
        "unlock_at": unlock_at_utc(c["week_start"]),
        "lock_at": due_at_utc(c["due"]) if c.get("hard_close") else lock_at_utc(c["due"]),
        "lecture_title": f"{week_label} Readings + Lecture",
        "lecture_html": lecture_html,
        "lecture_placeholder": placeholder,
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
    ap.add_argument("--force", action="store_true",
                    help="also update modules that have already opened")
    args = ap.parse_args(argv)

    cfg = yaml.safe_load(Path("course.yml").read_text(encoding="utf-8"))
    root = _course_root(cfg)

    if args.simple_syllabus:
        from simple_syllabus import build_package
        out = build_package(root / cfg["syllabus_file"], Path("preview"), cfg["site_base"])
        print(f"simple syllabus package: {out}")
        return 0

    stems = cfg["weeks"] + cfg.get("extra", []) if args.all else [args.week]
    if not stems or stems == [None]:
        ap.error("pass --all or --week NAME")

    syl_path = root / cfg["syllabus_file"]
    syllabus_md = frontmatter.load(str(syl_path)).content if syl_path.exists() else ""
    plans = [plan_week(root / f"{s}.md", cfg["site_base"], syllabus_md)
             for s in stems]

    # freeze check first: anything students can already see is left alone
    now = now_et()
    if not args.force:
        for p in plans:
            if is_live(p["week_start"], now):
                print(f"[frozen] {p['module']} opened {p['week_start']} and is live; "
                      f"not redeployed (pass --force to override)")
        plans = [p for p in plans if not is_live(p["week_start"], now)]
        if not plans and not args.all:
            return 1

    if args.dry_run:
        prev = Path("preview")
        prev.mkdir(exist_ok=True)
        lecture_stems = set(cfg["weeks"])
        for p in plans:
            (prev / f"{p['stem']}.html").write_text(p["page_html"], encoding="utf-8")
            if p["has_discussion"]:
                (prev / f"{p['stem']}-discussion.html").write_text(
                    p["discussion_html"], encoding="utf-8")
            lecture = ""
            if p["stem"] in lecture_stems:
                (prev / f"{p['stem']}-lecture.html").write_text(
                    p["lecture_html"], encoding="utf-8")
                lecture = " + readings/lecture"
            print(f"[dry-run] module '{p['module']}' | opens {p['unlock_at']} | "
                  f"page{lecture} | discussion {p['points']}pts "
                  f"due {p['due_at']} locks {p['lock_at']}"
                  + (" [extra credit]" if p["extra_credit"] else ""))
        return 0

    load_dotenv()
    import requests
    from canvas_client import CanvasClient
    client = CanvasClient(os.environ["CANVAS_API_URL"],
                          os.environ["CANVAS_API_TOKEN"],
                          os.environ["CANVAS_COURSE_ID"])
    state = _load_state()
    group_id = client.upsert_assignment_group(cfg["assignment_groups"]["exercises"])
    lecture_stems = set(cfg["weeks"])
    try:
        for p in plans:
            try:
                st = state.setdefault(p["stem"], {})
                module_id = client.upsert_module(p["module"], unlock_at=p["unlock_at"],
                                                 published=args.publish or None)
                pos = 1
                if p["stem"] in lecture_stems:
                    lecture_html = p["lecture_html"]
                    live = (client.get_page_body(st["lecture_url"])
                            if st.get("lecture_url") else None)
                    video = VIDEO_EMBED_RE.search(live) if live else None
                    if video:
                        lecture_html = lecture_html.replace(
                            p["lecture_placeholder"], video.group(0))
                    lecture_url = client.upsert_page(
                        p["lecture_title"], lecture_html, args.publish,
                        known_url=st.get("lecture_url"))
                    client.add_to_module(module_id, "Page", lecture_url, position=pos)
                    st["lecture_url"] = lecture_url
                    pos += 1
                page_url = client.upsert_page(p["module"], p["page_html"], args.publish,
                                              known_url=st.get("page_url"))
                client.add_to_module(module_id, "Page", page_url, position=pos)
                st.update(module_id=module_id, page_url=page_url)
                pos += 1
                if p["has_discussion"]:
                    title = f"Exercise Discussion: {p['module']}"
                    disc_id = client.upsert_discussion(
                        title, p["discussion_html"],
                        0 if p["extra_credit"] else p["points"],
                        p["due_at"], group_id, args.publish,
                        known_id=st.get("discussion_id"),
                        unlock_at=p["unlock_at"], lock_at=p["lock_at"])
                    client.add_to_module(module_id, "Discussion", disc_id, position=pos)
                    st["discussion_id"] = disc_id
                print(f"deployed: {p['module']}")
            except requests.HTTPError as e:
                raise SystemExit(f"deploy failed at '{p['module']}': {e}")

        if args.all:
            syllabus_post = frontmatter.load(str(root / cfg["syllabus_file"]))
            syllabus_html = render_html(syllabus_post.content, cfg["site_base"])
            client.upsert_page("Syllabus", syllabus_html, args.publish)

            other_group_id = client.upsert_assignment_group(cfg["assignment_groups"]["other"])
            av = cfg["activity_verification"]
            if av_is_live(av, now) and not args.force:
                print(f"[frozen] {av['name']} opened {av['open']} and is live; not updated")
                print("deployed: Syllabus page")
            else:
                av_id = client.upsert_assignment(
                    av["name"], av["points"], due_at_utc(av["due"]), other_group_id,
                    ["online_url", "online_text_entry"], args.publish,
                    known_id=state.get("activity_verification_id"),
                    unlock_at=unlock_at_utc(av["open"]) if av.get("open") else None,
                    lock_at=lock_at_utc(av["due"]))
                state["activity_verification_id"] = av_id
                print("deployed: Syllabus page, Activity Verification")
    finally:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    sys.exit(main())
