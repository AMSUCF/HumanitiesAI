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


OVERWRITE_FLAG = "--overwrite-canvas-edits"
# stored when an item's change marker could not be read back after a deploy:
# it never matches Canvas, so the next run treats the item as edited (safe)
UNREAD_STAMP = "unread"


def edited_in_canvas(client, kind, ref, stored, overwrite, title,
                     quiet=False) -> str | None:
    """Edit guard: "edited" or "missing" when `ref` was changed or deleted
    in Canvas since our last upsert recorded `stored`, else None (deploy).

    Once someone edits an item in Canvas, Canvas is its master copy, so it
    is left alone unless --overwrite-canvas-edits. `quiet` leaves the
    "edited" notice to the caller (it publishes the item and says so).
    """
    if overwrite or not ref or not stored:
        return None
    live = client.updated_at(kind, ref)
    if live is None:
        print(f"[missing in Canvas] {title} was deleted in Canvas; "
              f"not recreated (pass {OVERWRITE_FLAG} to recreate it)")
        return "missing"
    if live != stored:
        if not quiet:
            print(f"[edited in Canvas] {title} was edited in Canvas; "
                  f"not redeployed (pass {OVERWRITE_FLAG} to override)")
        return "edited"
    return None


def check_lost_state(client, cfg, root) -> None:
    """Self-contained live runs with no deploy state: refuse to deploy over a
    course that already has this course's modules or pages, since without
    the state every Canvas edit there would be overwritten unguarded."""
    labels = {assets._label(root, s) for s in cfg["weeks"] + cfg.get("extra", [])}
    found = [f"module '{n}'" for n in client.module_names()
             if n.split(":")[0].strip() in labels]
    found += [f"page '{t}'" for t in ("Syllabus", GUIDE_TITLE) if client.find_page(t)]
    if found:
        raise SystemExit(
            f"the deploy state for this course is missing ({STATE_FILE.resolve()} is "
            f"missing or empty) but the course already has {', '.join(found)}: restore "
            f".state.json from backup (undergrad/canvas/.state.json for ENG 3861), or "
            f"pass {OVERWRITE_FLAG} to deploy over what is in Canvas")


_HEADING_ID_RE = re.compile(r'<h[1-6][^>]*\sid="([^"]+)"')


def broken_anchors(sources, syllabus_html, syllabus_href) -> list[tuple[str, str]]:
    """(label, fragment) for each link to a syllabus heading that does not
    exist: `#frag` links inside the syllabus (`own`) and `<syllabus>#frag`
    links anywhere. sources: (label, html, own) triples."""
    ids = set(_HEADING_ID_RE.findall(syllabus_html))
    to_syllabus = re.compile(r'href="' + re.escape(syllabus_href) + r'#([^"]+)"')
    out = []
    for label, html, own in sources:
        frags = to_syllabus.findall(html) + (re.findall(r'href="#([^"]+)"', html)
                                             if own else [])
        out += [(label, f) for f in frags if f not in ids]
    return list(dict.fromkeys(out))


def _load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    text = STATE_FILE.read_text(encoding="utf-8").strip()
    return json.loads(text) if text else {}


def _save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def _course_root(cfg: dict) -> Path:
    # week files live one directory above canvas/ when run in-place,
    # or in cwd when tests fabricate a flat layout
    for base in (Path("."), Path("..")):
        if (base / (cfg["weeks"][0] + ".md")).exists():
            return base
    raise FileNotFoundError("week files not found relative to cwd")


ENV_KEYS = ("CANVAS_API_URL", "CANVAS_API_TOKEN", "CANVAS_COURSE_ID")


def _load_env() -> None:
    env = Path.cwd() / ".env"
    load_dotenv(env)
    lacking = [k for k in ENV_KEYS if not os.environ.get(k)]
    if lacking:
        where = env if env.exists() else f"{env} (there is no such file)"
        raise SystemExit(f"{', '.join(lacking)} not set: put "
                         f"{'it' if len(lacking) == 1 else 'them'} in {where}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--week")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--simple-syllabus", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="also redeploy modules (and Activity Verification) that "
                         "have already opened")
    ap.add_argument(OVERWRITE_FLAG, action="store_true",
                    help="self-contained courses: also overwrite items edited, "
                         "replaced, removed or deleted in Canvas since the last "
                         "deploy, and deploy even if .state.json is lost")
    args = ap.parse_args(argv)
    overwrite = args.overwrite_canvas_edits
    if overwrite:
        print(f"[overwrite] {OVERWRITE_FLAG}: edits made in Canvas to anything this "
              f"run deploys will be overwritten")

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
        _load_env()
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
                    "in .env" if code == 401
                    else "; no such course: check CANVAS_COURSE_ID in .env" if code == 404
                    else "")
            raise SystemExit(f"could not read the Canvas course (HTTP {code}){hint}")
        print(f"deploying to: {info.get('name')} ({info.get('course_code')})")
        want = cfg.get("expect_course_code")
        if want and str(want) not in (info.get("course_code") or ""):
            raise SystemExit(f"course_code {info.get('course_code')!r} does not contain "
                             f"{str(want)!r}; wrong CANVAS_COURSE_ID?")
        state = _load_state()
        if self_contained:
            if not state and not overwrite:
                try:
                    check_lost_state(client, cfg, root)
                except requests.HTTPError as e:
                    raise SystemExit(f"could not check the course for existing content: {e}")
            try:
                files, pages, missing_files = assets.sync_assets(
                    client, cfg, root, state, overwrite=overwrite)
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
    broken = []
    if self_contained:
        # links into the syllabus must land on a heading: its TOC anchors
        # carry term dates, so a date change can silently break them
        syl_ids_html = (syllabus_html if syllabus_html is not None
                        else _render_page(syllabus_md, cfg, link_map, "", []))
        sources = [(p["stem"], html, False) for p in plans
                   for html in (p["page_html"], p["discussion_html"], p["lecture_html"])]
        if syllabus_html is not None:
            sources.append((cfg["syllabus_file"], syllabus_html, True))
        if guide_html is not None:
            sources.append((cfg["instructor_guide"], guide_html, False))
        broken = broken_anchors(sources, syl_ids_html, link_map["index.html"])
    if (unresolved or broken) and not args.dry_run:
        problems = []
        if unresolved:
            problems.append("links with no Canvas target; fix them before deploying:\n"
                            + "\n".join(f"  {f}: {path}" for f, path in unresolved))
        if broken:
            problems.append("links to syllabus headings that don't exist; fix them "
                            "before deploying:\n"
                            + "\n".join(f"  {f}: #{frag}" for f, frag in broken))
        raise SystemExit("\n".join(problems))
    for f, path in unresolved:
        print(f"[unresolved] {f}: {path}")
    for f, frag in broken:
        print(f"[broken anchor] {f}: #{frag}")

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
    def guard(kind, ref, stored, title, publishable=False):
        return (edited_in_canvas(client, kind, ref, stored, overwrite, title,
                                 quiet=publishable and args.publish)
                if self_contained else None)

    def publish_kept(publish, title):
        # --publish on an item kept as edited: publish it as it is in Canvas,
        # without re-stamping (it stays the instructor's version)
        publish()
        print(f"[edited in Canvas] {title}: kept your Canvas version, published it")

    def record(target, ref_key, ref, stamp_key, kind, title):
        # store a deployed item's ref; in a self-contained course, always
        # with its fresh change marker, never without one
        target[ref_key] = ref
        if not self_contained:
            return
        try:
            marker, why = client.updated_at(kind, ref), "Canvas returned none"
        except requests.HTTPError as e:
            marker, why = None, str(e)
        if marker is None:
            target[stamp_key] = UNREAD_STAMP
            raise SystemExit(
                f"deployed {title} but could not read back its change marker ({why}). "
                f"The next deploy will report it as [edited in Canvas]; pass "
                f"{OVERWRITE_FLAG} then if nobody has edited it in Canvas since")
        target[stamp_key] = marker

    def place(module_id, st, kind, ref, title, pos):
        # put an item in its module at `pos`; returns the next free position.
        # Self-contained (R16): items already there are never moved, and an
        # item the instructor took out of the module is not put back.
        if not self_contained:
            client.add_to_module(module_id, kind, ref, position=pos)
            return pos + 1
        key, ours = f"{kind}:{ref}", st.setdefault("module_items", [])
        if not client.add_to_module(module_id, kind, ref, position=pos, reposition=False,
                                    add_missing=overwrite or key not in ours):
            print(f"[removed in Canvas] {title} was removed from its module in Canvas; "
                  f"not re-added (pass {OVERWRITE_FLAG} to re-add it)")
            return pos
        if key not in ours:
            ours.append(key)
        return pos + 1

    group_id = client.upsert_assignment_group(cfg["assignment_groups"]["exercises"])
    lecture_stems = set(cfg["weeks"])
    try:
        for p in plans:
            try:
                st = state.setdefault(p["stem"], {})
                title = f"Exercise Discussion: {p['module']}"
                # guards are read before the module is published: publishing a
                # module can publish its items in Canvas and bump their updated_at
                lecture_skip = (guard("pages", st.get("lecture_url"),
                                      st.get("lecture_updated"), p["lecture_title"], True)
                                if p["stem"] in lecture_stems else None)
                page_skip = guard("pages", st.get("page_url"), st.get("page_updated"),
                                  p["module"], True)
                disc_skip = (guard("discussion_topics", st.get("discussion_id"),
                                   st.get("discussion_updated"), title, True)
                             if p["has_discussion"] else None)
                known_module = st.get("module_id")
                if self_contained and known_module and not overwrite:
                    # R16: the instructor may rename or redate a module in
                    # Canvas, so a known module only ever gets published
                    module_id = known_module
                    if args.publish:
                        client.publish_module(module_id)
                else:
                    module_id = client.upsert_module(p["module"], unlock_at=p["unlock_at"],
                                                     published=args.publish or None,
                                                     known_id=known_module)
                st["module_id"] = module_id
                pos = 1
                # an item skipped as edited keeps its module slot; a deleted one
                # is not re-added and gives up its position
                if p["stem"] in lecture_stems:
                    skip = lecture_skip
                    if skip == "edited" and args.publish:
                        publish_kept(lambda: client.publish_page(st["lecture_url"]),
                                     p["lecture_title"])
                    if not skip:
                        lecture_html = p["lecture_html"]
                        live = (client.get_page_body(st["lecture_url"])
                                if st.get("lecture_url") else None)
                        video = VIDEO_EMBED_RE.search(live) if live else None
                        if video:
                            lecture_html = lecture_html.replace(
                                p["lecture_placeholder"], video.group(0))
                        record(st, "lecture_url",
                               client.upsert_page(p["lecture_title"], lecture_html,
                                                  args.publish,
                                                  known_url=st.get("lecture_url")),
                               "lecture_updated", "pages", p["lecture_title"])
                    if skip != "missing":
                        pos = place(module_id, st, "Page", st["lecture_url"],
                                    p["lecture_title"], pos)
                    deck = f"slides/{p['stem']}.pptx"
                    if slide_ids and deck not in missing_files:
                        pos = place(module_id, st, "File", slide_ids[p["stem"]], deck, pos)
                skip = page_skip
                if skip == "edited" and args.publish:
                    publish_kept(lambda: client.publish_page(st["page_url"]), p["module"])
                if not skip:
                    record(st, "page_url",
                           client.upsert_page(p["module"], p["page_html"], args.publish,
                                              known_url=st.get("page_url")),
                           "page_updated", "pages", p["module"])
                if skip != "missing":
                    pos = place(module_id, st, "Page", st["page_url"], p["module"], pos)
                if p["has_discussion"]:
                    known = st.get("discussion_id")
                    skip = disc_skip
                    if skip == "edited" and args.publish:
                        publish_kept(lambda: client.publish_discussion(known), title)
                    if not skip:
                        if (self_contained and overwrite and known
                                and st.get("discussion_updated")
                                and client.updated_at("discussion_topics", known) is None):
                            known = None   # deleted in Canvas: the override recreates it
                        record(st, "discussion_id",
                               client.upsert_discussion(
                                   title, p["discussion_html"],
                                   0 if p["extra_credit"] else p["points"],
                                   p["due_at"], group_id, args.publish,
                                   known_id=known,
                                   unlock_at=p["unlock_at"], lock_at=p["lock_at"]),
                               "discussion_updated", "discussion_topics", title)
                    if skip != "missing":
                        pos = place(module_id, st, "Discussion", st["discussion_id"],
                                    title, pos)
                print(f"deployed: {p['module']}")
            except requests.HTTPError as e:
                raise SystemExit(f"deploy failed at '{p['module']}': {e}")

        if args.all:
            done = []
            skip = guard("pages", state.get("syllabus_url"), state.get("syllabus_updated"),
                         "Syllabus", True)
            if skip == "edited" and args.publish:
                publish_kept(lambda: client.publish_page(state["syllabus_url"]), "Syllabus")
            if not skip:
                record(state, "syllabus_url",
                       client.upsert_page("Syllabus", syllabus_html, args.publish,
                                          known_url=state.get("syllabus_url")),
                       "syllabus_updated", "pages", "Syllabus")
                done.append("Syllabus page")
            if guide_html is not None and not guard(
                    "pages", state.get("guide_url"), state.get("guide_updated"), GUIDE_TITLE):
                # for the instructor only: never published, never in a module
                record(state, "guide_url",
                       client.upsert_page(GUIDE_TITLE, guide_html, False,
                                          known_url=state.get("guide_url")),
                       "guide_updated", "pages", GUIDE_TITLE)
                done.append("Instructor Guide")

            other_group_id = client.upsert_assignment_group(cfg["assignment_groups"]["other"])
            av = cfg["activity_verification"]
            av_id = state.get("activity_verification_id")
            if av_is_live(av, now) and not args.force:
                print(f"[frozen] {av['name']} opened {av['open']} and is live; not updated")
            else:
                skip = guard("assignments", av_id, state.get("av_updated"), av["name"], True)
                if skip == "edited" and args.publish:
                    publish_kept(lambda: client.publish_assignment(av_id), av["name"])
                if not skip:
                    if (self_contained and overwrite and av_id and state.get("av_updated")
                            and client.updated_at("assignments", av_id) is None):
                        av_id = None   # deleted in Canvas: the override recreates it
                    record(state, "activity_verification_id",
                           client.upsert_assignment(
                               av["name"], av["points"], due_at_utc(av["due"]),
                               other_group_id, ["online_url", "online_text_entry"],
                               args.publish, known_id=av_id,
                               unlock_at=unlock_at_utc(av["open"]) if av.get("open") else None,
                               lock_at=(lock_at_utc(av["due"], grace_hours=late_hours)
                                        if late_hours is not None
                                        else lock_at_utc(av["due"]))),
                           "av_updated", "assignments", av["name"])
                    done.append("Activity Verification")
            if done:
                print("deployed: " + ", ".join(done))
    finally:
        _save_state(state)

    return 0


if __name__ == "__main__":
    sys.exit(main())
