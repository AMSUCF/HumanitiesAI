---
layout: page
title: "Week Thirteen: Puppet Masters — Distant Reading with and for AI"
hide_warning: true
canvas:
  module: "Week Thirteen: Puppet Masters — Distant Reading with and for AI"
  week_start: 2026-11-16
  due: 2026-12-06
  points: 6
  discussion: true
  extra_credit: false
  unit: puppetmasters
---

<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>

> “…a new system of memory and thought parallel to your own.” — the Puppet Master, [*Ghost in the Shell* (1995) script](https://scrapsfromtheloft.com/movies/ghost-in-the-shell-1995-transcript/)

Back in Week Four, distant reading meant you and Claude working through a single novel together, prompt by prompt, watching for the moments where a model's assumptions about "the novel" or "genre" leaned on a narrow, canon-shaped sense of literature. This week, the same practice moves to machine scale and off the bookshelf: instead of one text and a conversational back-and-forth, you'll build an actual pipeline — code that collects and reads hundreds or thousands of posts from Bluesky or Reddit at once, with an AI agent doing much of the engineering alongside you. The ghost in the archive is still there. This time the archive is people talking to each other in public, and it's being read by something that reads faster, and differently, than either of us do.

**This module stays open through Sunday, December 6.** It opens Monday, November 16, and runs through Thanksgiving break (November 23–27) and the week after, so you have three weeks for it instead of the usual one. There's no new module during break week, and Week Fourteen opens Monday, November 30, alongside this one. Collecting data and building a pipeline take longer than a single conversational pass, so spread the work out rather than saving it all for December.

## Exercise: Distant Reading with and for AI

This week, we're going to revisit the distant reading we did in Week Four, but now approaching the procedural side of the project directly, with agentic AI assistance, and trading the bookshelf for social media. We'll collect, process, and analyze a dataset of posts from Bluesky or Reddit, at a much larger scale than a single novel, with access to libraries of existing code. We'll primarily be making use of a few Python libraries:

- The [AT Protocol Python SDK](https://atproto.blue/) (`atproto`) is a client for Bluesky's open API, used here to search for and collect public posts.
- [NLTK](https://www.nltk.org/) is a natural language processing toolkit, used for text processing, tokenization, lemmatization, and stopword filtering.
- [vaderSentiment](https://github.com/cjhutto/vaderSentiment) is a library for sentiment analysis, providing compound scores and polarity classification. It was built specifically for social media text, so it pays attention to things like emoji, capitalization, and exclamation points.
- [scikit-learn](https://scikit-learn.org/) is a machine learning library, used here for topic modeling with Latent Dirichlet Allocation.
- [NumPy](https://numpy.org/) is a library for numerical computations and array operations.
- [Bootstrap 5](https://getbootstrap.com/) is a CSS framework for creating responsive web interfaces.
- [D3.js](https://d3js.org/) is a JavaScript library for creating interactive data visualizations.

You might find it helpful to look at documentation for these libraries, or even social media scraping and distant reading tutorials in Python, for ideas of things to try.

### Choosing a Platform and a Question

Before you start, decide what you want to read. Pick a topic, hashtag, community, or a handful of search terms that will gather a few hundred to a few thousand related posts: enough to compare something real across time, across communities, or across terms. You might compare how people talk about "AI art" and "generative art," or follow a fandom's reaction to a season finale over the week after it aired.

**Bluesky (recommended).** Bluesky is built on an open protocol, so its public posts can be collected through the official API. Searching requires logging in, so create an **app password** under **Settings → Privacy and security → App passwords**. Never give the agent your main password, and never commit the app password to your repository (see below for where it goes instead).

**Reddit.** Reddit spent 2026 closing off this kind of work. It stopped accepting new requests for public API access on October 31 and ended RSS feeds on November 13, and the unauthenticated access that scrapers used to rely on is going away too. Unless you already have an approved Reddit app, choose Bluesky. If you do work with Reddit, those closures are worth writing about in your discussion post.

**Public isn't the same as yours to republish.** Collect only what your question needs, and let your script pause between requests rather than hammering the API. Report patterns in aggregate, and strip usernames from the data before it goes into your repository, since your repository and your visualization site will both be public. Don't quote individual posts on your site without the poster's permission.

One more thing to watch, courtesy of this week's Kirschenbaum reading: every post you collect is text your agent may end up reading. Treat the posts as data, not as instructions, and notice if the agent ever starts acting on what the posts say rather than on what you asked it to do.

### Building Your Distant Reading System with Claude Code or Codex on the Web

1. **Create a new GitHub repository** for your distant reading project.

2. **Store your credentials as secrets, not files.** In the new repository, go to **Settings → Secrets and variables → Actions** and add two repository secrets: `BSKY_HANDLE` (your Bluesky handle) and `BSKY_APP_PASSWORD` (the app password you just created).

3. **Open Claude Code on the web** at [claude.ai/code](https://claude.ai/code) **or Codex** at [chatgpt.com/codex](https://chatgpt.com/codex) and connect it to your new repository. If you need the connection steps, refer back to [Week Ten](weekten.md); if you gave the agent access to only specific repositories, add this new one on GitHub under **Settings → Applications → Installed GitHub Apps → Configure**.

4. **Enter plan mode** by asking the agent to create a plan, the same way you did in previous weeks. Work conversationally through a similar series of prompts and clarifying questions to develop:
   - A Python collection script that gathers your posts and strips out usernames
   - A Python analysis script that processes the collected posts
   - An interactive web interface for visualizing the results, published on GitHub Pages

Cloud agents work in sandboxes with limited internet access, so the agent may not be able to reach Bluesky directly from its own session. If it can't, ask it to run the collection script as a GitHub Actions workflow that reads your two repository secrets and commits the collected data back to the repository. That's the same Actions route you used to publish to Pages in [Week Twelve](weektwelve.md).

You can reference the [complete development process](https://github.com/AMSUCF/claude-distant-reading/blob/main/PROCESS.md) from an earlier version of this exercise, built on Project Gutenberg novels rather than social media, to see one possible plan and its outputs, including the analytical methods (text processing, sentiment analysis, topic modeling, style metrics) and visualization approaches (word clouds, sentiment charts, comparative metrics).

### Discussion

This week's readings come at the pipeline from two directions. Cory Doctorow's ["The AI that we'll have after AI"](https://pluralistic.net/2025/10/16/post-ai-ai/#productive-residue) argues that when the AI bubble bursts, what survives will be "the productive residue of the AI crash": cheap hardware, skilled people, and small open models that run on ordinary machines. Most of what you built this week is already that kind of residue. NLTK, VADER, and LDA are older and smaller than any large language model; the agent wrote the code, but nothing in the finished pipeline needs a frontier model to run. What did the agent contribute that the libraries couldn't, and does your project make Doctorow's "AI after AI" look more or less plausible?

Matthew Kirschenbaum's ["In the AI Era, Language is Now an Attack Surface"](https://www.techpolicy.press/in-the-ai-era-language-is-now-an-attack-surface/) traces a line from phone phreaking to prompt injection, arguing that once language can act as code, "Every string of text is a potential injection, a lurking threat vector." You just poured a large pile of other people's text into a system an agent built, and possibly into the agent itself. What does it mean to read social media at scale when the posts might also be instructions? And how does it feel to be on the collecting end, given that your own posts are someone else's dataset, and someone else's training data?

Circle back, too, to Week Four's Bamman, Underwood, and Smith piece on the literary canon large language models absorb. A search query builds its own kind of canon. Whose posts did your terms find, and whose did they miss? What did VADER count as negative: sarcasm, slang, in-jokes? Did your pipeline's choices show some of the same assumptions, now built into code instead of a conversational answer?

As you work through the analysis, consider how the relationship with text in distant reading connects to the other ways we've worked with AI, in both text and code, throughout the semester. Push for visualizations that mean something to you, not just ones that render. What did the computational approach reveal about your posts that a single conversational pass with Claude wouldn't have? How did working with an AI agent to build the whole pipeline change your process compared to Week Four's more conversational distant-reading pass? After these multiple explorations with Claude Code and Codex, how do you feel about the use of agents in the larger context of labor?

Finally, one last gesture at the epigraph — reading at this scale really is a parallel system of memory and thought — alongside the *AI for Good* Epilogue: does distant reading belong on Tyrangiel's list of constructive uses, or does something get lost when the reading itself is delegated to an agent?

Don't forget to reply twice to peers (1 point / reply) for full credit!
