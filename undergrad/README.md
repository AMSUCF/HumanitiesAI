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
  slides, and the lecture video the GTA adds in Canvas) and a **Do** week
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
| `canvas/course.yml` | Deployer config, same schema as `../canvas/course.yml` plus the self-contained keys and a `units` block |
| `canvas/instructor-guide.md` | GTA-facing Instructor Guide page (never published) |
| `slides/<module>.pptx` | Lecture deck, uploaded to Files -> Lecture Slides and added to the module as a File item |
| `slides/<module>.html` | Web (reveal.js) version of the deck, used by the website only |

## Slides

The decks are generated from `slides/decks.yml`, which lists every slide
after the auto-generated title slide (quote, image, section, points, prompt,
question, and readings slides; the header comment documents each type).
Every quote was checked word for word against its source. Images are
referenced in place, mostly from the grad decks' `../slides/media/`, so
don't prune those files without checking `decks.yml`. To edit a deck,
change `decks.yml` and rebuild from `undergrad/slides/`:

```
../../.venv/Scripts/python build_decks.py   # web versions
../../.venv/Scripts/python build_pptx.py    # PowerPoint versions for Canvas
```

Speaker notes (`notes:`) show in reveal's speaker view (press `S`).

Front matter uses the same `canvas:` block as the grad week files, so the
shared deployer reads these directly. See "Canvas handoff" below for the
deploy.

## Canvas handoff

This course deploys **self-contained** (`self_contained: true` in
`canvas/course.yml`). The deployer uploads everything to Canvas: each deck goes
in as an editable `.pptx` under Files -> Lecture Slides, the images are
uploaded, and every link is rewritten to its Canvas target. Nothing in the
deployed course points back at the website, so a graduate teaching assistant
can run it with only Canvas and PowerPoint.

Each module's items, in order: the "<Module> Readings + Lecture" page, the deck
as a File item, the exercise page, and "Exercise Discussion: <module>". The
lecture page has a placeholder line, "The <Module> video lecture will be posted
here at the start of the week.", where the GTA drops the recording. The Do-week
YouTube embeds are plain iframes in the week files, so they deploy with the
exercise page. Discussions are due Sunday 11:59 PM ET and lock 24 hours later
(`late_window_hours: 24`); the final locks 24 hours after it is due.

`canvas/course.yml` also sets `expect_course_code: "3861"`, so the deployer
refuses to run against a course whose code doesn't match (this keeps it away
from the grad course ID), and `instructor_guide: instructor-guide.md`. The
guide is a GTA-facing page that the deployer creates as "Instructor Guide (not
visible to students)", always unpublished and outside every module. It is only
deployed on `--all` runs, and it should have no repo-relative links.

### Building the decks

Canvas gets PowerPoint files. Build them from `undergrad/slides/`:

```
../../.venv/Scripts/python build_pptx.py
```

`build_decks.py` still builds the reveal.js web versions, and both read
`decks.yml`. A deploy stops if a `.pptx` is older than `decks.yml` or than its
module's `.md` (the title slide shows the module name and dates from its front
matter), so rebuild after any edit. Builds are byte-for-byte reproducible, so
rebuilding an unchanged deck doesn't make the deployer upload it again. To review the PowerPoint versions, `export_pngs.ps1` renders
every slide to PNG through PowerPoint.

### Deploy order

Put the new course ID and a token in `undergrad/canvas/.env` (gitignored; the
deployer reads the `.env` in the working directory), then run from
`undergrad/canvas/`:

1. **Dry run:** `../../.venv/Scripts/python ../../canvas/deploy.py --all --dry-run`
   writes `preview/` with no network calls. Check that it prints no
   `[unresolved]` links and no `[broken anchor]` lines (a link to a syllabus
   heading that doesn't exist; the TOC anchors carry the term dates), and read
   the previews, including `preview/instructor-guide.html`.
2. **Deploy unpublished:** the same command without `--dry-run`.
3. **Review** the modules in Canvas. Anything edited in Canvas during the
   review (for example the Syllabus TBDs) is kept by the next step.
4. **Publish:** re-run with `--publish`. Items edited in Canvas are not
   redeployed, but they are still published, and print `[edited in Canvas]
   ...: kept your Canvas version, published it`.

Every later redeploy must also pass `--publish`; one without it sends items
back to unpublished.

**Back up `undergrad/canvas/.state.json` after each deploy** (it is
gitignored). It holds the Canvas ids and change markers the edit guard works
from. If it is lost, a live deploy to a course that already has this course's
modules, Syllabus, or Instructor Guide stops and asks for it back, rather than
overwriting the course unguarded.

### After the handoff, Canvas is the master copy

Once the GTA has the course, the repo should stop being edited for it. If a
redeploy finds that something changed in Canvas since the last deploy (a page,
a discussion, the Activity Verification assignment, or a deck replaced in
Files), it skips that item and prints `[edited in Canvas]` or `[missing in
Canvas]`. Modules the deployer already created keep the name and dates they
have in Canvas, their items are never reordered, and an item the GTA took out
of a module prints `[removed in Canvas]` and is not put back.
`--overwrite-canvas-edits` overrides all of this (the run says so on its first
line); `--force` only redeploys modules that have already opened.
The new `course.yml` keys (`self_contained`, `expect_course_code`,
`instructor_guide`, `late_window_hours`, `units`) do nothing when absent, so
the grad course is unaffected; they are documented in `../canvas/README.md`.
