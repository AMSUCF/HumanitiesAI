---
layout: page
title: "Week Thirteen: Puppet Masters — Distant Reading with and for AI"
hide_warning: true
canvas:
  module: "Week Thirteen: Puppet Masters — Distant Reading with and for AI"
  week_start: 2026-11-16
  due: 2026-11-22
  points: 6
  discussion: true
  extra_credit: false
  unit: puppetmasters
---

<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>

> The Puppet Master didn't emerge from any one archive — it emerged from reading all of them, at a scale and speed no human investigator could match, until the reading itself started to look like a kind of ghost. Section 9 never fully settled whether that made Project 2501 a mind, or only the shape of everything it had processed. — after [*Ghost in the Shell* (1995)](https://en.wikipedia.org/wiki/Ghost_in_the_Shell_(1995_film))

Back in Week Four, distant reading meant you and Claude working through a single novel together, prompt by prompt, watching for the moments where a model's assumptions about "the novel" or "genre" leaned on a narrow, canon-shaped sense of literature. This week, the same practice moves to machine scale: instead of one text and a conversational back-and-forth, you'll build an actual pipeline — code that processes a small library of texts at once, with an AI agent doing much of the engineering alongside you. The ghost in the archive is still there. It's just being read, this time, by something that reads faster, and differently, than either of us do.

**This module's work is due Sunday, November 22 — before Thanksgiving break.** You'll then have a full week off, November 23–27: no new module, no readings, and no discussion post during break week. Week Fourteen — an extra-credit-only coda — doesn't open until Monday, November 30. Plan your pipeline work accordingly; there's no catching up on this module during the break itself.

## Exercise: Distant Reading with and for AI

This week, we're going to revisit the distant reading we did in Week Four, but now approaching the procedural side of the project directly, with agentic AI assistance. We'll revisit collecting, processing, and analyzing a dataset of texts, but now at a much larger scale, with access to libraries of existing code. We'll primarily be making use of a few Python libraries:

- [NLTK](https://www.nltk.org/) is a natural language processing toolkit, used for text processing, tokenization, lemmatization, and stopword filtering.
- [vaderSentiment](https://github.com/cjhutto/vaderSentiment) is a library for sentiment analysis, providing compound scores and polarity classification.
- [scikit-learn](https://scikit-learn.org/) is a machine learning library, used here for topic modeling with Latent Dirichlet Allocation.
- [NumPy](https://numpy.org/) is a library for numerical computations and array operations.
- [Bootstrap 5](https://getbootstrap.com/) is a CSS framework for creating responsive web interfaces.
- [D3.js](https://d3js.org/) is a JavaScript library for creating interactive data visualizations.

You might find it helpful to look at documentation for these libraries, or even web scraping and distant reading tutorials in Python, for ideas of things to try. Choose one of the two options below for building your pipeline: Claude Code for the web, or Claude Code for your desktop.

### Option One: Building Your Distant Reading System with Claude Code Web

Before you start, choose five to ten related texts for your analysis and download them as .txt files from [Project Gutenberg](https://www.gutenberg.org/). Download them individually rather than scripting bulk downloads — Project Gutenberg has [rules about robots](https://www.gutenberg.org/policy/robot_access.html). Consider selecting texts that share a common theme, genre, author, or time period, so your comparative analysis has something real to say.

Once you have your texts:

1. **Create a new GitHub repository** for your distant reading project.

2. **Upload your Project Gutenberg texts** to the repository.

3. **Open Claude Code Web** at [claude.ai/code](https://claude.ai/code) and connect it to your new repository. If you need the full walkthrough for generating a fine-grained personal access token and the rest of the connection mechanics, refer back to [Week Ten](weekten.md) — that page has the complete steps, and they haven't changed since then.

4. **Enter plan mode** by asking Claude to create a plan, the same way you did in previous weeks. Work conversationally through a similar series of prompts and clarifying questions to develop:
   - A Python analysis script that processes your texts
   - An interactive web interface for visualizing the results

You can reference the [complete development process](https://github.com/AMSUCF/claude-distant-reading/blob/main/PROCESS.md) used in the demo to see one possible plan and resulting outputs, including the analytical methods (text processing, sentiment analysis, topic modeling, style metrics) and visualization approaches (word clouds, sentiment charts, comparative metrics).

### Option Two: Working Locally with Claude Code for Desktop

In this week's demo, I'll show you how to work locally with [Claude Code for your desktop](https://docs.claude.com/en/docs/claude-code/installation) to accomplish this same task. Installing Claude Code is not required, but it's recommended if you're interested in exploring computational work, or the kind of subagent workflows described in some of this week's readings — there's an option to continue working with subagents in next week's extra-credit module.

### Discussion

This week's readings turn the distant-reading question back on the tool doing the reading. ["Generative AI & Fictionality: How Novels Power Large Language Models"](https://arxiv.org/pdf/2603.01220) and ["AI as a Tool for Simulation-Based Experiments in Literary Studies"](https://arxiv.org/pdf/2606.02293) are recent scholarship on how digital humanists are actually using — and critiquing — LLMs for literary study right now, not in the abstract. Read them alongside your own pipeline results: where do these authors see LLMs opening up genuinely new kinds of literary analysis, and where are they skeptical? Does your experience building a sentiment/topic/style pipeline this week match their optimism, their skepticism, or some mix of both? And circle back to Week Four's Bamman, Underwood, and Smith piece on the literary canon large language models absorb — did your pipeline's choices (which texts got flagged as "on-topic," which stylistic patterns got treated as significant) show any of the same canon-shaped assumptions, now baked into code instead of a conversational answer?

As you work through the analysis, consider how the relationship with text in distant reading connects to the other ways we've worked with AI, in both text and code, throughout the semester. Push for visualizations that mean something to you, not just ones that render. What did the computational approach reveal about your chosen texts that a single conversational pass with Claude wouldn't have? How did working with an AI agent to build the whole pipeline change your process compared to Week Four's more conversational distant-reading pass? After these multiple explorations with Claude Code, how do you feel about the use of agents in the larger context of labor, particularly given the tensions raised in this week's readings on AI and literary scholarship?

Finally, connect this back to the epigraph, and to the *AI for Good* Epilogue you're reading this week. When an agent reads a shelf of novels for you, at a speed and scale you couldn't match by hand, what does the "ghost" of that corpus look like on the other side — a word cloud, a topic model, a sentiment curve? And who is actually doing the reading: you, for choosing the texts and the questions; Claude, for writing the pipeline; or the pipeline itself, once it starts surfacing patterns you didn't ask it to look for? Tyrangiel's Epilogue closes out a book built around AI's constructive uses — does distant reading at this scale belong on that list, or does something get lost, whose reading, whose attention, when the reading itself is delegated to an agent?
