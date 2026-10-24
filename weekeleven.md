---
layout: page
title: "Week Eleven: Puppet Masters — Agentic Code"
hide_warning: true
canvas:
  module: "Week Eleven: Puppet Masters — Agentic Code"
  week_start: 2026-11-02
  due: 2026-11-08
  points: 6
  discussion: true
  extra_credit: false
  unit: puppetmasters
---

<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>

> “Who knew that copies could still be produced despite the absence of the original?” — the Laughing Man, [*Ghost in the Shell: Stand Alone Complex*](https://en.wikiquote.org/wiki/Ghost_in_the_Shell:_Stand_Alone_Complex)

Stand Alone Complex names something stranger than a conspiracy: coordinated-looking action with nobody actually coordinating it, and no originator you can point to and say "it started there." That's a useful, slightly unsettling frame for a coding agent that dispatches subagents, fresh copies of itself sent off to explore, test, or build part of a project and report back. Last week you made one thing in one pass. This week you'll keep going: plan a larger project, then revise it five times, and see what accumulates in the history when an agent and its copies do most of the building.

## Exercise: Iteration and Subagents

This week's reading is Simon Willison's ["Battle Drones—a vibe coded RTS with audio-based multiplayer"](https://simonwillison.net/2026/Oct/20/battledrones/), the story of a real-time strategy game built over "12 major iterations" and 321 commits by coding agents. Willison started by asking Claude for an MVP design ("Let's start with a MVP design, ask me some questions"), and it wasn't fun to play until a later version, after he prompted "This game isn't fun enough yet. Make it a LOT more fun." That run used dynamic workflows, which orchestrate "many subagents at once," and it went on overnight. You can [play the game](https://simonw.github.io/battledrones/), open the early versions he kept online, and read his [commit history](https://github.com/simonw/battledrones/commits/main/). Notice, too, what he admits along the way: "I was beginning to feel guilty at how little actual design input I had into the game."

Your task is to take on a **complex, interactive web project** of your own and develop it through **five distinct revisions** with Claude Code on the web or Codex. A game is a great choice, but anything substantial and interactive works: an interactive story, a simulation, an educational tool, a visualization you can explore, or something tied to your own research. In the video, I use plan mode and iterate through five revisions of a game inspired by our conversations this semester about AI and *Ghost in the Shell*.

For an example of what this kind of project can become, look at my *Kairos* piece, [AI Admin: Provocations Through Generated Play](https://anastasiasalter.net/KairosAIAdmin/). It holds two iterations of the same p5.js game, a 2024 Writing Program Edition and a 2025 Digital Humanities Edition, built over about a hundred prompts with much earlier models (ChatGPT 4.0, Claude Opus 4.0 and Sonnet 4.0, and DALL-E 3). Play them in sequence and notice what changed between versions. Today's agents can go much further in five revisions.

### Setting Up Your Project

The mechanics are the same as last week, so look back at [Week Ten](weekten.md) for any step you need in detail.

1. **Create a new public GitHub repository** for this project, separate from last week's.
2. **Open Claude Code on the web** at [claude.ai/code](https://claude.ai/code) **or Codex** at [chatgpt.com/codex](https://chatgpt.com/codex), and select the new repository. If you gave the agent access to only last week's repository, add this one on GitHub under **Settings → Applications → Installed GitHub Apps → Configure**.
3. **Give the agent standing notes.** In Claude Code, type `/init` to create a CLAUDE.md file describing the project. In Codex, make your first task "Look over this repository and create an AGENTS.md file describing the project."
4. If you have images, sound, a dataset, or other files you want in the project, upload them now: **Add file → Upload files**.

### Revision 1: Plan, then build

Start in plan mode. In Claude Code, you can switch into plan mode as I do in the video, or start your prompt with: "Enter plan mode. Do not exit plan mode until I confirm the plan is ready. Ask clarifying questions until you understand the plan." (The same prompt works in Codex.) Then describe your idea, and say that it's for GitHub Pages and should stick to native web technologies (HTML, CSS, JavaScript) with no build step. If you have a library in mind, such as p5.js, Three.js, or D3.js, name it.

Answer the agent's questions, push back on the parts of the plan you don't like, and confirm it only when it describes what you want. Then let it build a first playable version.

### Revisions 2–5: Iterate

Each revision is a new round: play or test the current version, decide what it needs, prompt, review what the agent changed, and merge. Some approaches to try, borrowed from Willison:

- **Specific feedback from testing:** "The second level is too easy and the controls don't work on my phone. Fix both."
- **An open-ended push:** "This isn't fun enough yet. Make it a LOT more fun." See what the agent decides "fun" means.
- **Critique before building:** "First research and then critique this design. Only build after we have agreed on any modifications."
- **New materials:** upload images or sounds to the repository and ask the agent to work them in.
- **Subagents:** use at least one revision for this. In Claude Code, ask for them directly, for example: "Use subagents to playtest this game from three different kinds of players' perspectives, then fix the biggest problems they find," or "Use subagents to review the code, the accessibility, and the visual design in parallel, then combine their recommendations." If you're using Codex, ask the same thing and note how it handles the request. Watch the progress view while it works: what did each copy do, and what came back?

Keep the revisions distinct: each should change something you could describe in a sentence, not just fix a typo. Jot a line or two after each round (what you asked for, what changed, what surprised you) so you have material for your reflection. If you'd like to keep earlier versions playable, as Willison did, ask the agent to save each one in its own folder (`v1/`, `v2/`, and so on).

### Commits and Deploying

Both agents usually commit to a separate branch and open a pull request. When you merge, choose **Create a merge commit** rather than **Squash and merge**, so that each revision's commits stay visible in your repository's history. Turn on GitHub Pages under **Settings → Pages** (deploy from the `main` branch, `/ (root)` folder), as in Week Ten, so your classmates can try what you made.

**For full credit, your discussion post must include:**

-   the link to your GitHub repository, with at least five distinct commits reflecting your five revisions;
-   a reflection on your iteration (see the discussion questions below);
-   and replies to two peers (1 point / reply).

Please share your GitHub Pages link too, so we can all play or try each other's projects.

### Discussion

Share your repository link (and your Pages link) and reflect on your five revisions:

- How did your project change from the plan to the fifth revision? Which revision made the biggest difference, and was that your idea or the agent's?
- Willison felt guilty "at how little actual design input" he had into his game. How much of your project's design came from you? Read your commit history as a record: whose decisions does it show?
- What did the subagents do in your project, and could you tell what each one contributed? How did it feel to direct copies of the agent you couldn't fully watch?
- Connect your experience to at least one of our readings: Willison, Meredith Martin's ["Command Lines for the Humanities"](https://www.cambridge.org/core/journals/pmla/article/command-lines-for-the-humanities/097F959E6971063D05B085E698354BA2), or chapter 3 of *AI for Good*.

Finally, the epigraph in one question: after five revisions, several subagents, and a stack of commits, is there an "original" in your project, and is it you?

Don't forget to reply twice to peers (1 point / reply) for full credit!
