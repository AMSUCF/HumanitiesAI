---
layout: page
title: "Week Ten: Puppet Masters — Building and Deploying"
hide_warning: true
canvas:
  module: "Week Ten: Puppet Masters — Building and Deploying"
  week_start: 2026-10-26
  due: 2026-11-01
  points: 6
  discussion: true
  extra_credit: false
  unit: puppetmasters
---

<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>

> "A complete commingling and fusion of our separate beings to create a new and unique entity." — the Puppet Master, proposing a unification with Major Kusanagi, [*Ghost in the Shell* (1995)](https://scrapsfromtheloft.com/movies/ghost-in-the-shell-1995-transcript/)

Last week you built inside a chat window, and the results lived on Claude's or ChatGPT's servers. This week you'll work a different way: you hand a coding agent a repository of your own, and everything it does there is recorded in version control, so you can read it, undo it, and publish it to the open web.

## Exercise: Building and Deploying

This week you'll set up **Claude Code on the web** or **Codex on the web** (OpenAI's coding agent), whichever matches your subscription. Connect it to a GitHub repository, and prompt it to build a web-based object that runs on GitHub Pages. You can make a variant of last week's tracker or something entirely new. The point is to get used to this way of working and to see what version control looks like when an agent is doing the committing.

Our reading is sections 2.2 and 2.3 of Simon Willison's [*Agentic Engineering Patterns*](https://simonwillison.net/guides/agentic-engineering-patterns/). In ["Using Git with coding agents"](https://simonwillison.net/guides/agentic-engineering-patterns/using-git-with-coding-agents/), he describes a repository as a folder that tracks its own changes and commits as "timestamped bundles of changes" with a message and an author. He also argues that you don't need to memorize Git so long as you know what's possible. ["Subagents"](https://simonwillison.net/guides/agentic-engineering-patterns/subagents/) explains why an agent sometimes sends a fresh copy of itself off to explore your files. Watch for both this week.

### Step 1: Make a repository

1. Sign in to [GitHub](https://github.com/) or create a free account. You don't need the Student Developer Pack for this, though it's worth applying for at [education.github.com](https://education.github.com/). If you already use GitHub for work or other projects and would rather not connect that account to a coding agent, it's fine to create a separate, throwaway account just for this class.
2. Click **New repository**, give it a descriptive name, make it **public** (free GitHub Pages sites need a public repository), check **Add a README**, and click **Create repository**.
3. If you're building on last week's tracker, upload your JSON file now: **Add file → Upload files**, then commit. That's your first commit, and you made it yourself.

### Step 2: Connect your coding agent

- **Claude Code on the web:** go to [claude.ai/code](https://claude.ai/code), connect your GitHub account, and give Claude access to the repository you just made (only that one, not all of them).
- **Codex on the web:** go to [chatgpt.com/codex](https://chatgpt.com/codex), connect GitHub, and set up an environment for your repository.

Both tools send you to a GitHub authorization screen. When it asks which repositories to allow, choose **Only select repositories** and pick the one you just made rather than granting access to everything. You can add more repositories later: on GitHub, go to **Settings → Applications → Installed GitHub Apps**, then **Configure** next to the Claude or Codex app. Both interfaces change often, so if a button has moved, follow the on-screen equivalent. Either way, you are giving an agent permission to read and write one repository.

### Step 3: Prompt something new

Write one prompt, in your own words, for something that runs entirely in the browser. Here's a starting point to adapt:

> **"Build a static web page for GitHub Pages: index.html at the root of the repository, with plain HTML, CSS, and JavaScript and no build step. Use the JSON file in this repository to make [your idea]. Commit as you go with clear commit messages."**

Some directions: last week's tracker with a new interface, a timeline, a map, a quiz, or a small game built from your dataset. Or skip the dataset and make something entirely new. Keep it small enough to finish this week.

While the agent works, watch what it does: which files it reads, whether it sends out a subagent to explore, and what commands it runs.

### Step 4: Read the version control

This is the new part, so slow down here. Before you merge anything, look at what the agent left behind on GitHub:

- **Commits:** open the commit history. Who's listed as the author, and what do the commit messages say?
- **Branch and pull request:** both tools usually work on a separate branch and offer to open a pull request rather than changing `main` directly. Open the pull request and look at the **Files changed** tab, which is the diff: green lines added, red lines removed.
- **One Willison prompt:** in a follow-up, try one of the Git prompts from section 2.2, such as "Review changes made today," "Combine last three commits with a better commit message," or "Undo last commit," and see what happens to the history.

When you're happy, merge the pull request into `main`.

### Step 5: Turn on GitHub Pages

1. In your repository, go to **Settings → Pages**.
2. Under **Source**, choose **Deploy from a branch**, set the branch to `main` and the folder to `/ (root)`, and click **Save**.
3. After a minute or two, GitHub shows your site's URL (`https://yourname.github.io/your-repo/`). Open it to make sure it works.

Want a change? Prompt again, review the new pull request, merge, and reload. Each round adds to the history.

**For full credit, your discussion post must include:**

-   the link to your live GitHub Pages site;
-   the link to your repository;
-   at least one screenshot of the version control (the commit history, a pull request, or a diff);
-   your responses to the discussion questions below;
-   and replies to two peers (1 point / reply).

### Discussion

Share your Pages link, your repository link, and your screenshot, then reflect:

- What did version control look like in practice? What did the agent commit, branch, or open as a pull request, and did reading the diffs change your sense of what it had built?
- Willison suggests treating Git history as "a deliberately authored story" rather than a permanent record of what happened. Read your repository's history as a story: who wrote it, you or the agent? What does it leave out?
- Did you see the agent explore your repository or dispatch subagents? How did working with an agent in a repository compare with last week's chat window?

Don't forget to reply twice to peers (1 point / reply) for full credit!
