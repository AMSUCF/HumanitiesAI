# ENG 3861: Digital Humanities Approaches to AI (undergraduate)

Undergraduate adaptation of ENG 6806 *Humanities in the Age of AI*, drafted for
**Spring 2027** (UCF calendar: classes Jan 11 - Apr 26, spring break Mar 15 - 21,
withdrawal Apr 2, finals Apr 28 - May 4). Instructor, email, and office hours are TBD.

Published at `https://anastasiasalter.net/HumanitiesAI/undergrad/` through the
same Jekyll site as the grad course, using its own layouts
(`_layouts/undergrad.html`, `_layouts/undergrad-page.html`) without the
*Ghost in the Shell* framing.

## Differences from the grad version

- Seven two-week modules, one exercise each (10 pts: 8 post + 2 replies), plus
  Activity Verification (5) and a Final Portfolio and Reflection (25).
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

Front matter uses the same `canvas:` block as the grad week files, so the
existing deployer reads these unchanged. `deploy.py --all --dry-run` was run
against this folder with the units patched in, and all eight modules plan
correctly.

## Before the first Canvas deploy

The deployer in `../canvas/` needs three small changes:

1. **Units.** `converter.py` hardcodes `UNIT_COLORS`/`UNIT_LABELS` for
   ghosts/shells/puppetmasters/coda. Have it merge in the `units` block from
   `course.yml`.
2. **`.env` lookup. Do this one first.** `deploy.py` calls `load_dotenv()` with
   no path. Run from `undergrad/canvas/` as `python ../../canvas/deploy.py`, it
   searches upward from the *script's* folder and would load
   `canvas/.env`, which holds the **grad course ID**. Change it to load
   `.env` from the working directory before running anything without
   `--dry-run`.
3. **Slides.** Each Readings + Lecture page embeds
   `{site_base}/slides/<module>.html`. Those decks don't exist yet, so
   either build them or make the slides iframe optional.

After that, put the new course ID and a token in `undergrad/canvas/.env`
(gitignored) and follow the same dry-run, unpublished, review, `--publish`
order as the grad course.
