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

import assets
from converter import (TZ, UNIT_COLORS, apply_canvas_style, configure_units, due_at_utc,
                       extract_readings, load_week, lock_at_utc, render_html,
                       split_discussion, unlock_at_utc)

STATE_FILE = Path(".state.json")
GUIDE_TITLE = "Instructor Guide (not visible to students)"

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


def plan_week(path: Path, site_base: str, syllabus_md: str = "", *,
              late_hours=None, link_map=None, slides=None, unresolved=None) -> dict:
    doc = load_week(path)
    c = doc.canvas
    if c["unit"] not in UNIT_COLORS:
        raise ValueError(f"{path}: unknown unit '{c['unit']}'")
    page_md, disc_md = split_discussion(doc.body)
    week_label = c["module"].split(":")[0].strip()
    slides_url = f"{site_base}/slides/{path.stem}.html"
    readings_md = extract_readings(syllabus_md, week_label) if syllabus_md else ""
    readings_html = (render_html(f"## Readings\n\n{readings_md}", site_base,
                                 link_map, unresolved)
                     if readings_md else "")
    placeholder = (f"<p><em>The {week_label} video lecture will be posted "
                   f"here at the start of the week.</em></p>")
    if slides:
        slides_block = assets.slides_html(slides["course_path"], slides["api_base"],
                                          slides["file_id"], week_label)
    else:
        slides_block = (
            f'<p><strong>Slides:</strong> <a href="{slides_url}">open the '
            f"{week_label} slides in a new tab</a></p>"
            f'<div style="position: relative; width: 100%; padding-bottom: 56.25%; '
            f'height: 0; overflow: hidden;">'
            f'<iframe src="{slides_url}" title="{week_label} slides" '
            f'style="position: absolute; top: 0; left: 0; width: 100%; '
            f'height: 100%; border: 1px solid #c6d4cf; border-radius: 6px;" '
            f'allowfullscreen></iframe></div>')
    lecture_html = apply_canvas_style(
        readings_html + "<h2>Lecture</h2>" + placeholder + slides_block, c["unit"])
    return {
        "stem": path.stem,
        "module": c["module"],
        "week_start": c["week_start"],
        "points": int(c["points"]),
        "extra_credit": bool(c.get("extra_credit", False)),
        "due_at": due_at_utc(c["due"]),
        "unlock_at": unlock_at_utc(c["week_start"]),
        "lock_at": (lock_at_utc(c["due"], grace_hours=late_hours) if late_hours is not None
                    else due_at_utc(c["due"]) if c.get("hard_close")
                    else lock_at_utc(c["due"])),
        "lecture_title": f"{week_label} Readings + Lecture",
        "lecture_html": lecture_html,
        "lecture_placeholder": placeholder,
        "has_discussion": bool(c["discussion"]) and bool(disc_md),
        "page_html": apply_canvas_style(
            render_html(page_md, site_base, link_map, unresolved), c["unit"]),
        "discussion_html": apply_canvas_style(
            render_html(disc_md, site_base, link_map, unresolved), c["unit"])
        if disc_md else "",
    }


def make_plans(stems, root, cfg, syllabus_md, link_map=None, slide_ids=None,
               course_path=None, api_base=None):
    """Plan each week. Returns (plans, unresolved), where unresolved lists
    the (stem, path) links the link map has no Canvas target for."""
    plans, unresolved = [], []
    for s in stems:
        missing = []
        slides = ({"course_path": course_path, "api_base": api_base,
                   "file_id": slide_ids[s]} if slide_ids and s in slide_ids else None)
        plans.append(plan_week(root / f"{s}.md", cfg["site_base"], syllabus_md,
                               late_hours=cfg.get("late_window_hours"),
                               link_map=link_map, slides=slides, unresolved=missing))
        unresolved += [(s, path) for path in missing]
    return plans, list(dict.fromkeys(unresolved))


def _render_page(md, cfg, link_map, label, unresolved) -> str:
    """A course-level page (syllabus, instructor guide); its unresolved
    links are added to `unresolved` under `label`."""
    missing = []
    html = render_html(md, cfg["site_base"], link_map, missing)
    unresolved += [(label, path) for path in missing]
    return html


def edited_in_canvas(client, kind, ref, stored, force, title) -> str | None:
    """Edit guard: "edited" or "missing" when `ref` was changed or deleted
    in Canvas since our last upsert recorded `stored`, else None (deploy).

    Once someone edits an item in Canvas, Canvas is its master copy, so it
    is left alone unless --force.
    """
    if force or not ref or not stored:
        return None
    live = client.updated_at(kind, ref)
    if live is None:
        print(f"[missing in Canvas] {title} was deleted in Canvas; "
              f"not recreated (pass --force to recreate it)")
        return "missing"
    if live != stored:
        print(f"[edited in Canvas] {title} was edited in Canvas; "
              f"not redeployed (pass --force to override)")
        return "edited"
    return None


def _load_state() -> dict:
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}


def _save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


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
                    help="also update modules that have already opened, "
                         "and items edited in Canvas")
    args = ap.parse_args(argv)

    cfg = yaml.safe_load(Path("course.yml").read_text(encoding="utf-8"))
    configure_units(cfg.get("units"))
    late_hours = cfg.get("late_window_hours")
    root = _course_root(cfg)

    if args.simple_syllabus:
        from simple_syllabus import build_package
        out = build_package(root / cfg["syllabus_file"], Path("preview"), cfg["site_base"])
        print(f"simple syllabus package: {out}")
        return 0

    stems = cfg["weeks"] + cfg.get("extra", []) if args.all else [args.week]
    if not stems or stems == [None]:
        ap.error("pass --all or --week NAME")

    self_contained = bool(cfg.get("self_contained"))
    guide = Path(cfg["instructor_guide"]) if cfg.get("instructor_guide") else None
    if guide and not guide.exists():
        raise SystemExit(f"instructor_guide: {guide} not found (relative to {Path.cwd()})")

    syl_path = root / cfg["syllabus_file"]
    syllabus_md = frontmatter.load(str(syl_path)).content if syl_path.exists() else ""

    # a self-contained course rewrites every repo link to its Canvas target:
    # placeholder ids on a dry run, the uploaded files and reserved pages live
    link_map = slide_ids = course_path = api_base = None
    missing_files = set()   # files deleted in Canvas that sync_assets left alone
    if not args.dry_run:
        load_dotenv(Path.cwd() / ".env")
        import requests
        from canvas_client import CanvasClient
        client = CanvasClient(os.environ["CANVAS_API_URL"],
                              os.environ["CANVAS_API_TOKEN"],
                              os.environ["CANVAS_COURSE_ID"])
        try:
            info = client.course_info()
        except requests.HTTPError as e:
            code = getattr(e.response, "status_code", None)
            hint = ("; Canvas token rejected (expired?); put a fresh CANVAS_API_TOKEN "
                    "in .env" if code == 401 else "")
            raise SystemExit(f"could not read the Canvas course (HTTP {code}){hint}")
        print(f"deploying to: {info.get('name')} ({info.get('course_code')})")
        want = cfg.get("expect_course_code")
        if want and str(want) not in (info.get("course_code") or ""):
            raise SystemExit(f"course_code {info.get('course_code')!r} does not contain "
                             f"{str(want)!r}; wrong CANVAS_COURSE_ID?")
        state = _load_state()
        if self_contained:
            try:
                files, pages, missing_files = assets.sync_assets(
                    client, cfg, root, state, force=args.force)
            except requests.HTTPError as e:
                raise SystemExit(f"asset sync failed: {e}")
            finally:
                _save_state(state)
            course_path = f"/courses/{os.environ['CANVAS_COURSE_ID']}"
            api_base = os.environ["CANVAS_API_URL"].rstrip("/") + "/api/v1"
    elif self_contained:
        found = assets.find_assets(cfg, root)
        assets.check_decks_fresh(root)
        files, pages = assets.placeholder_ids(cfg, found)
        course_path, api_base = "/courses/COURSE", "https://CANVAS_API_URL/api/v1"
    if self_contained:
        link_map = assets.build_link_map(cfg, course_path, files, pages)
        slide_ids = {s: files[f"slides/{s}.pptx"] for s in cfg["weeks"]}

    plans, unresolved = make_plans(stems, root, cfg, syllabus_md, link_map, slide_ids,
                                   course_path, api_base)
    syllabus_html = guide_html = None
    if args.all:
        syllabus_html = _render_page(syllabus_md, cfg, link_map, cfg["syllabus_file"],
                                     unresolved)
        if guide:
            guide_html = _render_page(frontmatter.load(str(guide)).content, cfg, link_map,
                                      cfg["instructor_guide"], unresolved)
    unresolved = list(dict.fromkeys(unresolved))
    if unresolved and not args.dry_run:
        raise SystemExit("links with no Canvas target; fix them before deploying:\n"
                         + "\n".join(f"  {f}: {path}" for f, path in unresolved))
    for f, path in unresolved:
        print(f"[unresolved] {f}: {path}")

    # freeze check: anything students can already see is left alone
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
                lecture = " + readings/lecture" + (" + slides file" if slide_ids else "")
            print(f"[dry-run] module '{p['module']}' | opens {p['unlock_at']} | "
                  f"page{lecture} | discussion {p['points']}pts "
                  f"due {p['due_at']} locks {p['lock_at']}"
                  + (" [extra credit]" if p["extra_credit"] else ""))
        if self_contained and syllabus_html is not None:
            (prev / "syllabus.html").write_text(syllabus_html, encoding="utf-8")
            print("[dry-run] Syllabus page")
        if guide_html is not None:
            (prev / "instructor-guide.html").write_text(guide_html, encoding="utf-8")
            print(f"[dry-run] {GUIDE_TITLE} (unpublished, in no module)")
        return 0

    # The edit guard is for self-contained (handed-off) courses only. The grad
    # course edits lecture pages in Canvas on purpose (hand-added videos, kept
    # via VIDEO_EMBED_RE), so it makes no updated_at calls and stores no markers.
    def guard(kind, ref, stored, title):
        return (edited_in_canvas(client, kind, ref, stored, args.force, title)
                if self_contained else None)

    def stamp(target, key, kind, ref):
        if self_contained:
            target[key] = client.updated_at(kind, ref)

    group_id = client.upsert_assignment_group(cfg["assignment_groups"]["exercises"])
    lecture_stems = set(cfg["weeks"])
    try:
        for p in plans:
            try:
                st = state.setdefault(p["stem"], {})
                title = f"Exercise Discussion: {p['module']}"
                # guards are read before upsert_module: publishing a module can
                # publish its items in Canvas and bump their updated_at
                lecture_skip = (guard("pages", st.get("lecture_url"),
                                      st.get("lecture_updated"), p["lecture_title"])
                                if p["stem"] in lecture_stems else None)
                page_skip = guard("pages", st.get("page_url"), st.get("page_updated"),
                                  p["module"])
                disc_skip = (guard("discussion_topics", st.get("discussion_id"),
                                   st.get("discussion_updated"), title)
                             if p["has_discussion"] else None)
                module_id = client.upsert_module(p["module"], unlock_at=p["unlock_at"],
                                                 published=args.publish or None,
                                                 known_id=st.get("module_id"))
                st["module_id"] = module_id
                pos = 1
                # an item skipped as edited keeps its module slot; a deleted one
                # is not re-added and gives up its position
                if p["stem"] in lecture_stems:
                    skip = lecture_skip
                    if not skip:
                        lecture_html = p["lecture_html"]
                        live = (client.get_page_body(st["lecture_url"])
                                if st.get("lecture_url") else None)
                        video = VIDEO_EMBED_RE.search(live) if live else None
                        if video:
                            lecture_html = lecture_html.replace(
                                p["lecture_placeholder"], video.group(0))
                        st["lecture_url"] = client.upsert_page(
                            p["lecture_title"], lecture_html, args.publish,
                            known_url=st.get("lecture_url"))
                        stamp(st, "lecture_updated", "pages", st["lecture_url"])
                    if skip != "missing":
                        client.add_to_module(module_id, "Page", st["lecture_url"],
                                             position=pos)
                        pos += 1
                    if slide_ids and f"slides/{p['stem']}.pptx" not in missing_files:
                        client.add_to_module(module_id, "File", slide_ids[p["stem"]],
                                             position=pos)
                        pos += 1
                skip = page_skip
                if not skip:
                    st["page_url"] = client.upsert_page(p["module"], p["page_html"],
                                                        args.publish,
                                                        known_url=st.get("page_url"))
                    stamp(st, "page_updated", "pages", st["page_url"])
                if skip != "missing":
                    client.add_to_module(module_id, "Page", st["page_url"], position=pos)
                    pos += 1
                if p["has_discussion"]:
                    known = st.get("discussion_id")
                    skip = disc_skip
                    if not skip:
                        if (self_contained and args.force and known
                                and st.get("discussion_updated")
                                and client.updated_at("discussion_topics", known) is None):
                            known = None   # deleted in Canvas: --force recreates it
                        st["discussion_id"] = client.upsert_discussion(
                            title, p["discussion_html"],
                            0 if p["extra_credit"] else p["points"],
                            p["due_at"], group_id, args.publish,
                            known_id=known,
                            unlock_at=p["unlock_at"], lock_at=p["lock_at"])
                        stamp(st, "discussion_updated", "discussion_topics",
                              st["discussion_id"])
                    if skip != "missing":
                        client.add_to_module(module_id, "Discussion", st["discussion_id"],
                                             position=pos)
                print(f"deployed: {p['module']}")
            except requests.HTTPError as e:
                raise SystemExit(f"deploy failed at '{p['module']}': {e}")

        if args.all:
            done = []
            if not guard("pages", state.get("syllabus_url"), state.get("syllabus_updated"),
                         "Syllabus"):
                state["syllabus_url"] = client.upsert_page(
                    "Syllabus", syllabus_html, args.publish,
                    known_url=state.get("syllabus_url"))
                stamp(state, "syllabus_updated", "pages", state["syllabus_url"])
                done.append("Syllabus page")
            if guide_html is not None and not guard(
                    "pages", state.get("guide_url"), state.get("guide_updated"), GUIDE_TITLE):
                # for the instructor only: never published, never in a module
                state["guide_url"] = client.upsert_page(
                    GUIDE_TITLE, guide_html, False, known_url=state.get("guide_url"))
                stamp(state, "guide_updated", "pages", state["guide_url"])
                done.append("Instructor Guide")

            other_group_id = client.upsert_assignment_group(cfg["assignment_groups"]["other"])
            av = cfg["activity_verification"]
            if av_is_live(av, now) and not args.force:
                print(f"[frozen] {av['name']} opened {av['open']} and is live; not updated")
            else:
                av_id = client.upsert_assignment(
                    av["name"], av["points"], due_at_utc(av["due"]), other_group_id,
                    ["online_url", "online_text_entry"], args.publish,
                    known_id=state.get("activity_verification_id"),
                    unlock_at=unlock_at_utc(av["open"]) if av.get("open") else None,
                    lock_at=(lock_at_utc(av["due"], grace_hours=late_hours)
                             if late_hours is not None else lock_at_utc(av["due"])))
                state["activity_verification_id"] = av_id
                done.append("Activity Verification")
            if done:
                print("deployed: " + ", ".join(done))
    finally:
        _save_state(state)

    return 0


if __name__ == "__main__":
    sys.exit(main())
