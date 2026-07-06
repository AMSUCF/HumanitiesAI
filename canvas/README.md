# Canvas Deployer

Canvas course content deployer for Humanities in the Age of AI. Converts the
Jekyll week files (`weekone.md` … `weekfourteen.md`, `finalreflection.md`,
`index.md`) into Canvas pages, discussions, modules, and assignments, and
builds a paste-ready package for the Simple Syllabus tool.

## Setup

Run these commands from the **repository root** (not from `canvas/`):

```
python -m venv .venv
.venv\Scripts\pip install -r canvas/requirements.txt
```

Then create your local environment file:

```
copy canvas\.env.example canvas\.env
```

Edit `canvas/.env` and fill in three values:

```
CANVAS_API_URL=https://webcourses.ucf.edu
CANVAS_API_TOKEN=paste-token-here
CANVAS_COURSE_ID=000000
```

**Getting a Canvas API token:** in Webcourses, go to **Account → Settings**,
scroll to **Approved Integrations**, and click **+ New Access Token**. Copy
the token immediately — Canvas only shows it once. `CANVAS_COURSE_ID` is the
numeric ID in the course URL (e.g. `.../courses/1234567`).

`canvas/.env` is gitignored and must never be committed.

All commands below (`deploy.py ...`) are run **from `canvas/`**, using the
venv at the repo root:

```
cd canvas
..\.venv\Scripts\python deploy.py --all --dry-run
```

## Commands

`deploy.py` accepts five flags:

| Flag | Effect |
| --- | --- |
| `--all` | Operate on every week in `course.yml` (`weeks` + `extra`), plus the syllabus page and Activity Verification assignment. |
| `--week NAME` | Operate on a single week only, e.g. `--week weekfive`. Mutually exclusive in practice with `--all` (pass one or the other). |
| `--dry-run` | Don't call the Canvas API. Render each page/discussion to `preview/*.html` and print a one-line summary per week. Safe to run repeatedly with no credentials required. |
| `--publish` | When actually deploying (no `--dry-run`), create/update pages, discussions, and assignments as **published** instead of the default unpublished. |
| `--simple-syllabus` | Ignore `--all`/`--week`. Read `index.md`, split it into `## `-headed sections, and write `preview/simple_syllabus.html` as a paste-ready package. Requires no Canvas credentials. |

Examples:

```
..\.venv\Scripts\python deploy.py --all --dry-run
..\.venv\Scripts\python deploy.py --week weekthree --dry-run
..\.venv\Scripts\python deploy.py --all
..\.venv\Scripts\python deploy.py --all --publish
..\.venv\Scripts\python deploy.py --simple-syllabus
```

## Deploy order

1. **Dry run first.** `deploy.py --all --dry-run` writes every page and
   discussion to `preview/` with no network calls. Skim the HTML previews and
   confirm the printed module/points/due-date summary looks right for all 15
   entries (14 weeks + `finalreflection`).
2. **Deploy unpublished.** With `canvas/.env` filled in, run
   `deploy.py --all` (no `--publish`). This creates/updates modules, pages,
   discussions, the Syllabus page, and the Activity Verification assignment
   in Canvas, all left **unpublished** so students can't see them yet.
3. **Review in Canvas.** Open Webcourses and check the modules, page content,
   discussion prompts, due dates, and points in the actual course UI.
4. **Publish.** Once everything looks right, re-run with `--publish`
   (`deploy.py --all --publish`) to flip the same content to published. This
   is the same idempotent upsert as step 2, so it's safe to run again even if
   nothing changed.

## Simple Syllabus procedure

`deploy.py --simple-syllabus` regenerates `preview/simple_syllabus.html` from
`index.md`: each `## Heading` in the syllabus becomes a
`<section data-component="Heading">` block, in order, separated by `<hr>`.

**Primary method — supervised browser session.** With the instructor logged
into Webcourses in Chrome and the course's Simple Syllabus editor open,
Claude (via Claude-in-Chrome) drives the browser to fill in the
instructor-editable components using the matching sections from
`preview/simple_syllabus.html`, one component at a time. The instructor
reviews the filled-in editor before submitting. Confirm at the start of the
session which components are instructor-editable in this course's Simple
Syllabus configuration — not all sections may be exposed.

**Fallback — manual paste.** Open `preview/simple_syllabus.html`, and for
each `<section data-component="...">` block, copy its rendered content into
the matching component in the Simple Syllabus editor by hand.

**Note:** the generated package includes a `Contents` section (from
`index.md`'s table of contents heading). This duplicates Canvas/Simple
Syllabus's own generated table of contents — **skip pasting the Contents
section** under either method.

## The state file

`canvas/.state.json` (gitignored) maps each deployed week's stem (e.g.
`weekfive`) to the Canvas IDs the deployer created for it — module ID, page
URL, and discussion ID — plus a top-level `activity_verification_id`. It's
written after every successful `--all`/`--week` run (not `--dry-run`).

The deployer doesn't strictly need this file to avoid duplicates: every
`upsert_*` call in `canvas_client.py` also falls back to searching Canvas by
title/name when no known ID is passed. The state file just makes repeat runs
faster (skips the search) and is where `known_id` comes from on discussions
and the Activity Verification assignment.

If Canvas content and the local file ever disagree about IDs — e.g. after
manually deleting/renaming something in Canvas — **delete `.state.json`** and
re-run. The next deploy falls back to fresh title-matching against whatever
exists in Canvas, rather than trusting stale IDs.

## Running the tests

From `canvas/` (uses the `pytest.ini` in this directory, which sets
`pythonpath = .` and `testpaths = tests`):

```
cd canvas
..\.venv\Scripts\python -m pytest -v
```

All 21 tests should pass. The suite covers the converter (front matter
parsing, HTML rendering, link rewriting, discussion splitting, due-date
conversion), the Canvas API client (upsert logic against mocked responses),
the deploy CLI (dry-run behavior, argument handling), and the Simple
Syllabus package builder.

## Troubleshooting

- **401 Unauthorized** — `CANVAS_API_TOKEN` is missing, expired, or wrong.
  Generate a new token (Account → Settings → **+ New Access Token**) and
  update `canvas/.env`.
- **404 Not Found** — `CANVAS_COURSE_ID` is wrong, or the token's account
  doesn't have access to that course. Double check the numeric ID in the
  course's Webcourses URL.
- **Deploy fails partway through** — this is safe. Every Canvas write is an
  idempotent upsert (look up by title/ID, then create-or-update), so simply
  re-running `deploy.py --all` (or `--week NAME` for a single one) picks up
  where it left off without creating duplicates.
- **Windows / `zoneinfo` errors** — Windows doesn't ship an IANA timezone
  database, which `converter.py` needs (`America/New_York` due-date
  conversion). `tzdata` is already listed in `requirements.txt` for this
  reason; if you see a timezone lookup error, re-run the `pip install -r
  canvas/requirements.txt` step.
