# Fall 2026 Humanities AI Course — Design

**Course:** ENG 6806: Humanities in the Age of AI (Fall 2026, fully asynchronous online)
**Date:** July 5, 2026
**Status:** Approved section-by-section in brainstorming; pending final user review

## Goals

Rebuild the Fall 2025 course for Fall 2026 with:

1. An agentic-AI theme refresh framed by *Ghost in the Shell* (Mamoru Oshii, 1995)
2. The UCF Fall 2026 academic calendar
3. Updated readings (one book swap + refreshed article layer)
4. A currency pass on all exercises (models, tools, setup flows)
5. A Python app that deploys the markdown course directly to Canvas (Webcourses)
6. A site theme refresh: light-mode-first GitS aesthetic with dark toggle

The GitHub Pages Jekyll site remains the public canonical version; Canvas mirrors it. Markdown files are the single source of truth for both.

## 1. Repo layout

- All current root course content (index.md, week files, exercise images, sample files) moves to `2025/`, preserved unmodified.
- The 2026 course is built fresh at root: `index.md`, 14 week files, `finalreflection.md`, updated `_layouts/` and `assets/`.
- New `canvas/` directory holds the Python deployer (see §5).
- Shared non-course directories (`character/`, `model/`, `ranker/`, `WeekOne/`) move under `2025/` if they are 2025 exercise artifacts; verified during implementation.

## 2. Calendar and week structure

UCF Fall 2026 (verified against calendar.ucf.edu July 2026):

- Classes: Monday, August 24 – Thursday, December 3, 2026
- Finals: December 4–10; grades due in myUCF December 15 (noon)
- Labor Day: September 7 (async course proceeds; noted in module)
- Thanksgiving: **full week off, November 23–27** (change from prior years)
- Withdrawal deadline: Friday, October 30

This yields **14 module Mondays** (vs. 15 in 2025). Resolution: merge 2025's Week Ten (Coding AI Interfaces) and Week Eleven (Deploying to GitHub Pages) into one double-weight week, since Claude Code for web now makes build-and-deploy one motion.

### Week map

| # | Monday | Module (2025 source) | Unit |
|---|--------|----------------------|------|
| 1 | Aug 24 | Eliza and Bots + required GitS (1995) viewing (W1) | Ghosts |
| 2 | Aug 31 | Interfaces (W2) | Ghosts |
| 3 | Sep 7 | Research and Sources (W3) — Labor Day note | Ghosts |
| 4 | Sep 14 | Reading Across Texts (W4) | Ghosts |
| 5 | Sep 21 | Image Generation (W5) | Shells |
| 6 | Sep 28 | Archival Images (W6) | Shells |
| 7 | Oct 5 | Video (W7) | Shells |
| 8 | Oct 12 | Images as Information (W8) | Shells |
| 9 | Oct 19 | Distant Coding (W9) | Puppet Masters |
| 10 | Oct 26 | **Merged double week:** AI Interfaces + GitHub Pages deploy (W10+W11) | Puppet Masters |
| 11 | Nov 2 | Agentic Code (W12) | Puppet Masters |
| 12 | Nov 9 | Local Models (W13) | Puppet Masters |
| 13 | Nov 16 | Distant Reading with and for AI (W14) — due Sun Nov 22, before break | Puppet Masters |
| — | Nov 23 | Thanksgiving break — no module | — |
| 14 | Nov 30 | Custom Bots, extra credit (W15) | Coda |

Weekly work due Sundays 11:59 PM ET; one-week no-penalty late window (unchanged policy).

### Grading (totals 100)

| Points | Item | Due |
|--------|------|-----|
| 6 | Activity Verification | Friday, August 28 |
| 72 | 12 regular exercises × 6 | Weekly (Sundays) |
| 12 | Merged Week 10 double exercise | Sunday, November 1 |
| 10 | Final Reflection (750–1000 words) | Thursday, December 10 |

Week 14 remains tiered extra credit: Claude Skills (up to 6), subagents (up to 6), fine-tuning (up to 10).

## 3. Ghost in the Shell thematic thread

Full thematic integration. The course keeps its official title; GitS (1995) is a **required Week One viewing** and presiding frame: what remains of the "ghost" (mind, voice, authorship) when the "shell" (body, medium, interface) is synthetic. The Puppet Master — an agent "born in a sea of information" that exceeds its task — frames the agentic turn.

### Unit renames (Textual/Visual/Procedural architecture preserved)

- **Unit 1 — Ghosts (Textual, weeks 1–4):** voice and mind in the machine; ELIZA as proto-ghost; generated language, synthetic sources, machine reading.
- **Unit 2 — Shells (Visual, weeks 5–8):** body, surface, image; the shelling sequence frames image generation; Haraway's cyborg meets generated imagery.
- **Unit 3 — Puppet Masters (Procedural/Agentic, weeks 9–13):** agents that plan, act, iterate. The *Stand Alone Complex* concept (emergent coordinated behavior without an originating agent) frames multi-agent material.
- **Coda — "The Net Is Vast and Infinite" (week 14 + final reflection).**

### Week-level texture

Each week opens with a short GitS epigraph/concept tied to that week's question (e.g., W1: "There is no program called 'me'" vs. ELIZA; W7: thermoptic camouflage and synthetic video; W12: ghosts that live off-network). Exercises stay tool-focused; discussion questions carry the thematic connection.

### Project and corpus refreshes

- **Weeks 9–10 running project:** retro sci-fi recommender becomes a **cyborg cinema/media recommender** (~100-work dataset of cyborg/AI media; same build → AI-app → deploy arc, now with deploy inside the merged double week).
- **Week 14 fine-tuning corpus:** Wizard of Oz corpus replaced by **"Ghosts Before the Shell"** public-domain proto-cyborg corpus: *Frankenstein*, Čapek's *R.U.R.*, von Harbou's *Metropolis*, Bierce's "Moxon's Master," Hoffmann's "The Sandman," Villiers' *Tomorrow's Eve*. ELIZA still bookends the course.

### Viewing availability (as of July 2026; syllabus carries a "check current availability" caveat)

- **GitS (1995):** free with ads on Tubi, Plex, Hoopla (library card); streaming on Prime Video, Hulu, Netflix; rentable on Apple TV/Amazon.
- **Recommended running supplemental text:** Science SARU's *The Ghost in the Shell* (2026 series, dir. Mokochan, composition EnJoe Toh) premieres July 7, 2026, streaming worldwide on **Prime Video** — new episodes air during the semester. Recommended in the syllabus; occasionally invoked in discussion prompts.

## 4. Readings

### Books

- **Keep:** Bender & Hanna, *The AI Con* — chapters 1–7, weeks 1–7 (unchanged).
- **Keep, moved earlier:** Mitchell, *Artificial Intelligence: A Guide for Thinking Humans* — Parts I–V now weeks 1–5 (historical framing front-loaded).
- **Keep, compressed and moved earlier:** Noble, *Algorithms of Oppression* — weeks 4–8: Power of Algorithms (W4); A Society, Searching (W5); Searching for Black Girls (W6); Future of Knowledge in Public (W7); Future of Information Culture + Conclusion (W8).
- **Replace:** Littman, *Code to Joy* → **Tyrangiel, *AI for Good*** — chapters across weeks 9–14; specific chapter mapping set during build once TOC is checked.

### Article layer by week (⚠ = verify/select during build)

| Wk | Keep | Add / Replace |
|----|------|---------------|
| 1 | Berry on Weizenbaum/ELIZA | ⚠ Add GitS 30th-anniversary critical essay (2–3 candidates surfaced at build) |
| 2 | Emerson "Interfaced"; Underwood "A More Interesting Upside of AI" | — |
| 3 | Kirschenbaum "Textpocalypse" | ⚠ Add Karen Hao (*Empire of AI* excerpt or 2025–26 reporting) |
| 4 | Underwood "Genealogy of Distant Reading" | ⚠ Add newer Underwood on LLMs and literary study |
| 5 | Demsky "My Month with Midjourney" | Add Haraway, "A Cyborg Manifesto" (excerpt) — Shells unit theory anchor |
| 6 | Anadol piece | ⚠ Refresh if stronger 2026 archival-AI-art piece exists |
| 7 | — | ⚠ Replace 2025 news links (El Eternauta, expired Gemini offer) with current gen-video coverage + labor responses |
| 8 | Farrell "After software eats the world" | ⚠ Refresh AI-images-in-communities news links |
| 9 | Evans wizard zine | **Willison, "Here's how I use LLMs to help me write code"** |
| 10 | — | **Willison, "Vibe engineering"** |
| 11 | Martin "Command Lines for the Humanities" (moved from old W12) | **Willison, "Designing agentic loops"** |
| 12 | — | **Willison, "The lethal trifecta for AI agents"** ⚠ + current local-model piece |
| 13 | — | ⚠ Updated DH scholarship on AI-assisted computational literary study (recent Underwood, Klein/D'Ignazio, DHQ/CA LLM special-issue essays — 2–3 candidates at build) |
| 14 | ELIZA/Puppet Master callbacks; HF/Unsloth tutorials | New corpus per §3 |

All ⚠ items are verified (links live, dates right) during the build; substitutions logged for user review.

## 5. Canvas deployer (Python app)

A local CLI in `canvas/` — no server, no web app.

```
canvas/
  deploy.py          # CLI entry point
  course.yml         # manifest: week order, course-level settings
  converter.py       # markdown + front matter → Canvas-ready HTML
  canvas_client.py   # thin wrapper over Canvas REST API
  requirements.txt   # python-frontmatter, markdown-it-py, PyYAML, requests, python-dotenv
  .env.example       # CANVAS_API_URL, CANVAS_API_TOKEN, CANVAS_COURSE_ID
```

Credentials in untracked `.env` only (`.gitignore` updated); default API base `https://webcourses.ucf.edu`. User provides token later; everything except live deploy is testable without it.

### Content model

Each week file carries a `canvas:` front-matter block (Jekyll ignores it):

```yaml
canvas:
  module: "Week One: Ghosts — Histories"
  week_start: 2026-08-24
  due: 2026-08-30
  points: 6            # 12 for merged W10; 0/extra-credit flags for W14
  discussion: true
```

`course.yml` holds ordered week list, timezone (America/New_York), assignment-group names, and syllabus/final-reflection/activity-verification entries.

### Per-week deploy behavior

1. Parse front matter + body; convert markdown → HTML (markdown-it-py); rewrite relative image/page links to absolute GitHub Pages URLs (site hosts all assets — no Canvas file uploads).
2. Upsert module named for the week.
3. Upsert content page (readings + tutorial/exercise) into the module.
4. Split at the `### Discussion` heading; upsert a graded discussion with that prompt — points and Sunday 11:59 PM due date from front matter, in an "Exercises" assignment group.
5. Course-level: syllabus page from `index.md`; Final Reflection graded discussion (10 pts, due Dec 10); Activity Verification shell (6 pts, due Aug 28); assignment groups.

### Behaviors

- **Idempotent:** items matched by title and updated in place; a local state file maps files → Canvas IDs as backstop against title edits. Re-running a week syncs edits without duplicates.
- **Flags:** `--all`, `--week <name>`, `--dry-run` (render HTML + print planned API calls, no network), `--publish` (default is unpublished).
- **Aesthetic carryover:** converted HTML carries inline-styled elements (Canvas strips stylesheets): unit-colored header band, unit badge, epigraph styling — a light visual echo of the site theme inside Canvas.
- **Testing without credentials:** dry-run HTML previews for every week; unit tests on converter (front-matter parsing, link rewriting, discussion splitting). First live run against sandbox/dev shell or unpublished modules.

### Simple Syllabus (post-deploy, no API)

UCF's Simple Syllabus is an LTI tool with no public write API. The deployer gains `--simple-syllabus`, generating a **paste-ready package** from `index.md`: syllabus decomposed into the component blocks Simple Syllabus templates expect (description, objectives, materials, grading table, schedule, policies) as clean rich-text/HTML in one preview file. Then:

1. **Primary: supervised browser session.** User logs into Webcourses via UCF SSO in Chrome; Claude drives the browser (Claude-in-Chrome tools) to fill instructor-editable components from the package while the user watches and reviews before submit.
2. **Fallback: manual paste,** section by section from the same package, if the LTI rich-text editors resist automation.

Runs **last**: content → Canvas deploy → verify modules → Simple Syllabus. Confirm which template components are instructor-editable at that point.

## 6. Exercise currency pass

During the week-by-week build, audit every exercise for out-of-date model and tool references (2025 pages name Claude Sonnet 4/4.5, Opus 4, DeepSeek-R1, Veo 3, GPT Image 1, time-limited offers, etc.). Update to current-generation equivalents and remove expired promotions.

**Claude Code Web setup walkthrough (new, required):** Claude Code Web is now established, but first-run setup needs explicit instructions for selecting the **"personal access token"** option and generating that token on GitHub (fine-grained PAT: where to create it, required repo scopes, expiration guidance, where to paste it). This walkthrough lands in the first week that uses Claude Code Web (Week 10) and is referenced by later weeks.

## 7. Site theme refresh

Reskin of the existing Jekyll theme (two layouts, `style.scss`, animation JS survive structurally):

- **Light mode is the default, with a dark-mode toggle.** The GitS palette is designed light-first: sea-glass/pale teal grounds with deep teal-green and rust/amber accents; dark mode inverts into the film's murky Newport City greens. Toggle persists (localStorage) and respects `prefers-color-scheme` as initial hint.
- **Header art:** circuit-board SVG becomes a falling-data / thermoptic-shimmer motif with a subtle ghost-silhouette reveal; respects `prefers-reduced-motion`.
- **Typography:** compact technical sans for headers (replacing Orbitron) with a katakana-inflected display touch used sparingly (week numbers, unit badges); Roboto Mono stays for body.
- **Unit badges:** Ghosts / Shells / Puppet Masters each get a mark + accent color used on their weeks' pages and echoed in Canvas header bands (§5).
- **Footer tagline:** "the net is vast and infinite."
- `THEME_README.md` rewritten for the new theme.

## Build order

1. Repo reorg (2025 archive) + Jekyll theme refresh
2. 2026 `index.md` (syllabus) with new calendar, grading, materials (incl. viewing availability)
3. Week files 1–14 with GitS framing, reading updates, exercise currency pass (⚠ verifications happen here)
4. Canvas deployer + `course.yml` + front matter across week files; dry-run verification
5. Live Canvas deploy when credentials provided (unpublished → user review → publish)
6. Simple Syllabus browser session

## Error handling and risks

- **Canvas API:** client surfaces HTTP errors with the failing item named; dry-run catches malformed content before any network call; idempotent upserts make partial-failure re-runs safe.
- ***AI for Good* chapter mapping** depends on its TOC — checked at build; if chapter count doesn't fit six weeks, chapters double up rather than restructuring weeks.
- **Streaming availability drift:** syllabus language says "as of August 2026" with a check-current note.
- **Simple Syllabus automation** may fail against the LTI editor; manual-paste fallback is designed in, not an afterthought.

## Testing

- Converter unit tests (front matter, link rewriting, discussion split, inline-style injection).
- Jekyll build passes locally/on Pages for the reorganized repo (2025 archive links intact at `/2025/`).
- Full dry-run over all 14 weeks reviewed as HTML before first live deploy.
- Live deploy lands unpublished; user reviews in Canvas before `--publish`.
