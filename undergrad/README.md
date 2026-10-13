# ENG 3861: Digital Humanities Approaches to AI (undergraduate)

Undergraduate adaptation of ENG 6806 *Humanities in the Age of AI*, drafted for
**Spring 2027** (UCF calendar: classes Jan 11 - Apr 26, spring break Mar 15 - 21,
withdrawal Apr 2, finals Apr 28 - May 4). Instructor, email, and office hours are TBD.

Published at `https://anastasiasalter.net/HumanitiesAI/undergrad/` through the
same Jekyll site as the grad course, but with its own retro-desktop theme
(bright primaries, chunky window frames, Bungee / Atkinson Hyperlegible /
VT323 / Press Start 2P): layouts `_layouts/undergrad.html` and
`_layouts/undergrad-page.html`, styles in `assets/undergrad.css`. None of the
grad site's *Ghost in the Shell* styling or framing is used.

## Differences from the grad version

- Seven two-week modules, each split into a **Think** week (readings, lecture
  slides, and the lecture video the GTA adds in Webcourses) and a **Do** week
  (a YouTube video embedded at the top of the exercise, then the exercise and
  discussion).
- One exercise per module, 10 points each, graded with an explicit points
  table on every page: screenshots/evidence (1 point each), a 250-word
  minimum reflection, one citation from the readings, and two replies (1
  point each). Plus Activity Verification (5) and a Final Portfolio and
  Reflection (25, its own table).
- Discussions close 24 hours after the Sunday deadline (Monday 11:59 PM), so
  late work stays manageable for the GTA.
- AI policy: AI can and should be used for the exercise tasks, but not for
  reflections or replies to classmates.
- Units are Words (modules 1-3), Images (4-5), Code (6), and Futures (7 + final).
  The code section is a single module: a mini-exhibit built in a chat
  artifact/canvas, with no GitHub, terminal, or agents.
- No required books. Readings are open access foundational DH pieces plus a few
  accessible public essays. No paid AI subscription is required.

## Files

| File | Becomes in Canvas |
| --- | --- |
| `index.md` | Syllabus page; its `### Module ...` sections feed each module's Readings + Lecture page |
| `moduleone.md` ... `moduleseven.md` | One module each: exercise page + graded discussion (split at `### Discussion`) |
| `finalreflection.md` | Finals module with a hard-closing discussion |
| `canvas/course.yml` | Deployer config, same schema as `../canvas/course.yml` plus a `units` block |
| `slides/<module>.html` | Lecture deck embedded on each Readings + Lecture page |

## Slides

The decks are generated from `slides/decks.yml`, which lists every slide
after the auto-generated title slide (quote, image, section, points, prompt,
question, and readings slides; the header comment documents each type).
Every quote was checked word for word against its source. Images are
referenced in place, mostly from the grad decks' `../slides/media/`, so
don't prune those files without checking `decks.yml`. To edit a deck,
change `decks.yml` and rebuild from `undergrad/slides/`:

```
../../.venv/Scripts/python build_decks.py
```

Speaker notes (`notes:`) show in reveal's speaker view (press `S`).

Front matter uses the same `canvas:` block as the grad week files, so the
existing deployer reads these unchanged. `deploy.py --all --dry-run` was run
against this folder with the units patched in, and all eight modules plan
correctly.

## Before the first Canvas deploy

The deployer in `../canvas/` needs these small changes:

1. **Units.** `converter.py` hardcodes `UNIT_COLORS`/`UNIT_LABELS` for
   ghosts/shells/puppetmasters/coda. Have it merge in the `units` block from
   `course.yml`.
2. **`.env` lookup. Do this one first.** `deploy.py` calls `load_dotenv()` with
   no path. Run from `undergrad/canvas/` as `python ../../canvas/deploy.py`, it
   searches upward from the *script's* folder and would load
   `canvas/.env`, which holds the **grad course ID**. Change it to load
   `.env` from the working directory before running anything without
   `--dry-run`.
3. **24-hour close.** `converter.lock_at_utc` hardcodes a 7-day late window.
   Read `late_window_hours: 24` from `course.yml` instead, for discussions
   and the final alike (the final no longer uses `hard_close`).
4. *(Optional)* **Do-week unlock.** Each week file has a `do_start` date. The
   discussion could unlock then instead of at `week_start`. Leaving it open
   from the start of Think week also works.

The Think-week lecture page (Readings + Lecture) still has its placeholder
for the lecture video, where the GTA drops the Canvas upload, and the
deployer keeps that upload on redeploys. The Do-week YouTube embeds are
plain iframes in the week files, so they deploy with the exercise page.

The lecture pages embed `{site_base}/slides/<module>.html`, which now exists
for all seven modules.

After that, put the new course ID and a token in `undergrad/canvas/.env`
(gitignored) and follow the same dry-run, unpublished, review, `--publish`
order as the grad course.
