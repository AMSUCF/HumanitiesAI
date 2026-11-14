---
layout: page
title: "Week Thirteen: Puppet Masters — Distant Reading with and for AI"
hide_warning: true
canvas:
  module: "Week Thirteen: Puppet Masters — Distant Reading with and for AI"
  week_start: 2026-11-16
  due: 2026-11-22
  close: 2026-12-06
  points: 6
  discussion: true
  extra_credit: false
  unit: puppetmasters
---

<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>

> “…a new system of memory and thought parallel to your own.” — the Puppet Master, [*Ghost in the Shell* (1995) script](https://scrapsfromtheloft.com/movies/ghost-in-the-shell-1995-transcript/)

Back in Week Four, distant reading meant you and Claude working through a single novel together, prompt by prompt, watching for the moments where a model's assumptions about "the novel" or "genre" leaned on a narrow, canon-shaped sense of literature. This week, the same practice moves to machine scale and off the bookshelf: instead of one text and a conversational back-and-forth, you'll build an actual pipeline — code that collects and reads hundreds or thousands of posts from Bluesky or Hacker News at once, with an AI agent doing much of the engineering alongside you. The ghost in the archive is still there. This time the archive is people talking to each other in public, and it's being read by something that reads faster, and differently, than either of us do.

**This module's work is due Sunday, November 22, before Thanksgiving break.** Because the break falls right after it, late submissions stay open an extra week: instead of the usual one-week late window, you can submit through Sunday, December 6. There's no new module during break week (November 23–27), and Week Fourteen opens Monday, November 30. Collecting data and building a pipeline take longer than a single conversational pass, so aim for November 22 and treat the extra time as a cushion.

## Exercise: Distant Reading with and for AI

This week, we're going to revisit the distant reading we did in Week Four, but now approaching the procedural side of the project directly, with agentic AI assistance, and trading the bookshelf for social media. We'll collect, process, and analyze a dataset of posts from Bluesky or Hacker News, at a much larger scale than a single novel, with access to libraries of existing code. We'll primarily be making use of a few Python libraries:

- The [AT Protocol Python SDK](https://atproto.blue/) (`atproto`) is a client for Bluesky's open API, used here to search for and collect public posts.
- The [Hacker News Search API](https://hn.algolia.com/api), run by Algolia, returns Hacker News stories and comments as JSON, with no account or library needed.
- [NLTK](https://www.nltk.org/) is a natural language processing toolkit, used for text processing, tokenization, lemmatization, and stopword filtering.
- [vaderSentiment](https://github.com/cjhutto/vaderSentiment) is a library for sentiment analysis, providing compound scores and polarity classification. It was built specifically for social media text, so it pays attention to things like emoji, capitalization, and exclamation points.
- [scikit-learn](https://scikit-learn.org/) is a machine learning library, used here for topic modeling with Latent Dirichlet Allocation.
- [NumPy](https://numpy.org/) is a library for numerical computations and array operations.
- [Bootstrap 5](https://getbootstrap.com/) is a CSS framework for creating responsive web interfaces.
- [D3.js](https://d3js.org/) is a JavaScript library for creating interactive data visualizations.

You might find it helpful to look at documentation for these libraries, or even social media scraping and distant reading tutorials in Python, for ideas of things to try.

### Choosing a Platform and a Question

Before you start, decide what you want to read. Pick a topic, hashtag, community, or a handful of search terms that will gather a few hundred to a few thousand related posts: enough to compare something real across time, across communities, or across terms. You might compare how people talk about "AI art" and "generative art," or follow a fandom's reaction to a season finale over the week after it aired.

**Bluesky.** Bluesky is built on an open protocol, so its public posts can be collected through the official API. Searching requires logging in, so create an **app password** under **Settings → Privacy and security → App passwords**. Never give the agent your main password, and never commit the app password to your repository (see below for where it goes instead).

**Hacker News.** Hacker News, the tech-industry forum run by the startup investor Y Combinator, has a public search API that needs no account or password at all, so it's the simpler choice if you'd rather skip the credentials step. It's also home to a constant, heated argument about AI. Keep in mind who's talking: its users skew heavily toward people who work in tech, and that's worth noticing when you interpret your results.

**Public isn't the same as yours to republish.** Collect only what your question needs, and let your script pause between requests rather than hammering the API. Report patterns in aggregate, strip usernames from the data as soon as you collect it (or have the agent replace them with pseudonyms), and don't quote individual posts without the poster's permission.

One more thing to watch, courtesy of this week's Kirschenbaum reading: every post you collect is text your agent may end up reading. Treat the posts as data, not as instructions, and notice if the agent ever starts acting on what the posts say rather than on what you asked it to do.

### Local and Private Is the Better Method

If you were doing this as research, you would do it on your own machine, in a private folder: collecting other people's posts, analyzing them, and keeping the data and results to yourself until you'd decided what was appropriate to publish. A public repository and a public website are the wrong home for a dataset of people's posts, even with usernames stripped. Option Two below works that way, and it's the one I'd recommend if you can install Claude Code or Codex on your own computer. UCF computers don't allow agentic software to be installed, so this only works on a personal machine, and there's no pressure to install anything: everything in this exercise also works on the web.

Option One, on the web, exists only because of the course context: it's the route that works without installing anything. If you take it, make the repository private if you can, and treat the repository and site as temporary. When you're done, delete the repository, or make it private and unpublish the site under **Settings → Pages**.

Either way, you don't need to share a link. Post screenshots of your process and your visualizations in the discussion instead.

Choose one of the two options below for building your pipeline: Claude Code or Codex on the web, or Claude Code or Codex on your desktop. Whichever you choose, pick your own topic rather than repeating mine from the demo, and ask for a tool that helps you read the conversation, not one that tells you what to conclude about it. As I put it to the agent in the demo, the goal is "creating something where you are not giving us judgments on the data, but are instead building a tool that allows them to build their own understanding of a complicated topic."

### Option One: Building Your Distant Reading System with Claude Code or Codex on the Web

1. **Create a new GitHub repository** for your distant reading project, and leave it empty. Make it private if you can. Either agent can still work in a private repository, but GitHub will warn you that a Pages site published from it is still public. If your account can't publish Pages from a private repository, use a public one and delete it when you're done.

2. **If you're using Bluesky, store your credentials as secrets, not files.** In the new repository, go to **Settings → Secrets and variables → Actions** and add two repository secrets: `BSKY_HANDLE` (your Bluesky handle) and `BSKY_APP_PASSWORD` (the app password you just created). If you're using Hacker News, skip this step. If this step sounds like too much fuss on the web, that's a good reason to choose Hacker News.

3. **Open Claude Code on the web** at [claude.ai/code](https://claude.ai/code) **or Codex** at [chatgpt.com/codex](https://chatgpt.com/codex) and connect it to your new repository. If you need the connection steps, refer back to [Week Ten](weekten.md); if you gave the agent access to only specific repositories, add this new one on GitHub under **Settings → Applications → Installed GitHub Apps → Configure**. In Codex, create a new cloud environment for the repository; it takes a moment to inspect the repository even when it's empty. Before you send your first prompt, check the model and effort level: both tools can drop to a low effort setting the first time you open them, so raise it. I used GPT-6.1 Sol on Extra High in the demo.

4. **Enter plan mode** by asking the agent to create a plan, the same way you did in previous weeks. Describe your platform, your topic and search terms, and what you want to see, then work conversationally through the agent's clarifying questions (a date range, how much to collect, how to handle accounts) to develop:
   - A Python collection script that gathers your posts and strips out usernames
   - A Python analysis script that processes the collected posts
   - An interactive web interface for visualizing the results, published on GitHub Pages

   Here's the prompt I dictated for the Hacker News demo, lightly cleaned up. When the agent asked about a date range, I chose the last 12 months.

   > We're going to do a social media research project to understand the debate over indie gaming and generative AI as it's playing out on Hacker News. We're going to use their existing API and first scrape anything relevant to the IGF, Big Walk, game cloning discussions, and general arguments over game programming and AI usage, and then use D3 to create a web-friendly dashboard to visualize the topic modeling and the sentiment analysis across those posts. Use pseudonyms for all accounts.

5. **Run the collection with GitHub Actions and publish the dashboard.** Cloud agents work in sandboxes with limited internet access, so the agent may not be able to reach Bluesky or Hacker News directly from its own session. In Codex, a task that says it needs attention usually means the environment's internet access is too narrow: open the environment's settings and allow the access it asks for (in the demo, that meant allowing package managers). If the agent still can't collect the data, ask it to commit and push its work, then build a version that runs the collection as a GitHub Actions workflow and publishes the dashboard to GitHub Pages (for Bluesky, the workflow reads your two repository secrets). That's the same Actions route you used to publish to Pages in [Week Twelve](weektwelve.md). Then:
   - Go to **Settings → Pages** and set **Source** to **GitHub Actions**, not **Deploy from a branch**.
   - Add any repository secret the agent's README asks for, using exactly the name it gives. In the demo, Codex built its pseudonyms with a secret key, so I had to add one more secret before the workflow would run (ask the agent how to generate one). You can skip that step by telling the agent to drop usernames entirely instead of replacing them with pseudonyms.
   - Open the **Actions** tab, select the failed run, and click **Re-run all jobs**. Click into the run to watch each step. Mine found 349 candidate threads, collected a capped sample of 60, and finished building and deploying in about three and a half minutes.

6. **Iterate.** Your first dashboard probably won't be the best way to show your data, especially if you didn't say anything about the interface design. Like our other exercises, this benefits from revision: change the Python scripts to collect what you're actually looking for, and change the dashboard until it shows you something worth reading.

When you've taken your screenshots, delete the repository, or make it private and unpublish the site under **Settings → Pages**.

#### An Example

Here's what Codex built from that prompt: *Fieldnotes*, a dashboard on the Hacker News debate over indie games and generative AI, drawn from 60 discussions and 2,846 posts and comments from the past year. I followed my own advice: I took these screenshots, then deleted the repository and the site, so there's no link to visit. Look at the choices the agent made along the way. I asked for pseudonyms, and it built "stable pseudonyms across threads," so one participant can be followed across discussions without being named. I asked for topic modeling, and it chose NMF rather than the LDA listed above. And it hedged its own results: the topics carry the note "Labels are the model's top terms, not editorial conclusions," and the sentiment chart warns, "Tone ≠ stance. A positive comment can still oppose AI." Those are the kinds of choices to look for, and question, in your own pipeline. Notice, too, who's talking: Hacker News skews toward the tech industry, so this conversation looks different from the games-industry and game-studies voices that are easier to find on Bluesky.

![Fieldnotes, built with Codex: a cream-colored research dashboard titled "Indie games. Generative AI. A conversation in flux.," subtitled "Mapping the Hacker News debate on what we make, how we make it, and what makes it ours," with totals of 60 discussions, 2,846 posts and comments, 1,527 participants as "stable pseudonyms across threads," and 7 discovered themes](images/weekthirteen-fieldnotes-overview.jpg)

![Fieldnotes' "Follow the conversation" section: a search box and filter chips (IGF & festivals, Big Walk, Cloning & originality, Programming & tools, Art & creative work), a monthly stacked bar chart of posts colored negative, neutral, and positive that spikes in October and November, and a donut chart of tone: 25% negative, 13% neutral, 62% positive](images/weekthirteen-fieldnotes-charts.jpg)

![Fieldnotes' "What are people talking about?" topic list, built with TF-IDF and NMF: seven themes with their top terms and tone bars, from Work / Use / Time (41% of documents) through Games / Good / Steam, Game / Indie / Awards, Code / Llm / Write, Software / Source / Engineering, and Art / Human / Artists, down to Slop / Hate / Valve (8%)](images/weekthirteen-fieldnotes-topics.jpg)

![Fieldnotes' "The discussions" list: the eight most-analyzed Hacker News threads, each with topic tags, a pseudonymized poster ID, the number of comments analyzed, and a tone bar, led by "Jonathan Blow – If AI solved coding, why is my software still the same?" and "Clair Obscur having its Indie Game Game Of The Year award stripped due to AI use," above a closing note: "A lens, not a verdict."](images/weekthirteen-fieldnotes-discussions.jpg)

You can reference the [complete development process](https://github.com/AMSUCF/claude-distant-reading/blob/main/PROCESS.md) from an earlier version of this exercise, built on Project Gutenberg novels rather than social media, to see one possible plan and its outputs, including the analytical methods (text processing, sentiment analysis, topic modeling, style metrics) and visualization approaches (word clouds, sentiment charts, comparative metrics).

### Option Two: Working Locally and Privately with Claude Code or Codex on Your Desktop

In this week's demo, I'll show you how to work locally with [Claude Code for your desktop](https://docs.claude.com/en/docs/claude-code/installation) to accomplish this same task; the [Codex app](https://developers.openai.com/codex/app) works the same way. This is the better way to do this kind of work: the collection script runs on your own machine with ordinary internet access, and the posts, the analysis, and the visualizations all stay in a private folder rather than on a public site. You don't need GitHub at all for this option.

1. **Make a new folder** for the project, outside any folder you sync to GitHub, and open it in the app. Trust the workspace when it asks, and check that the app shows your computer as the environment, not the cloud.

2. **Plan the tool.** Ask the agent to plan a local Python pipeline with a D3 dashboard you can open in your browser, and answer its clarifying questions. Here's the prompt I dictated for the Bluesky demo, lightly cleaned up:

   > We're going to build a local Python-driven tool with web-based visualizations using D3 for unpacking the Bluesky discourse around the IGF AI policy. We're going to need to run several searches to think about the ways that the judges' statement on AI has been reacted to and circulating, and the controversy around the game Big Walk and their disclosure of AI usage, which came after many of their sales. I will provide you with the API key for that environment variable later, but for now, start planning out that tool.

   When it asked follow-up questions, I asked for network visualizations, pseudonyms for every account except public publication accounts, a look at terms and emotions, and filters based on the analysis.

3. **Add your Bluesky app password.** The agent will probably build a file called `.env.example` and tell you to copy it to `.env`. Open the project folder (in Claude Code, you can show the file tree and open the folder in File Explorer or Finder from there), copy the file, rename the copy to `.env`, and open it in VS Code or any plain text editor, such as Notepad or TextEdit. Fill in your handle and app password. Don't screenshot the app password. Bluesky won't show it to you again, so if you lose track of it, make a new one. When you're finished with the project, you can delete the app password in Bluesky's settings. If you're using Hacker News, skip this step. If you ever turn the folder into a repository, ask the agent to add `.env` to `.gitignore` first so it never reaches GitHub.

4. **Run it and explore.** The agent will run the collection and serve the dashboard on your own computer (an address starting with `localhost`). Without the app password, my first run could only do a partial search; once I added it, the signed-in collection gathered 16,908 posts. Explore what it built, then iterate on both the collection and the interface, just as in Option One.

### Discussion

This week's readings come at the pipeline from two directions. Cory Doctorow's ["The AI that we'll have after AI"](https://pluralistic.net/2025/10/16/post-ai-ai/#productive-residue) argues that when the AI bubble bursts, what survives will be "the productive residue of the AI crash": cheap hardware, skilled people, and small open models that run on ordinary machines. Most of what you built this week is already that kind of residue. NLTK, VADER, and LDA are older and smaller than any large language model; the agent wrote the code, but nothing in the finished pipeline needs a frontier model to run. What did the agent contribute that the libraries couldn't, and does your project make Doctorow's "AI after AI" look more or less plausible?

Matthew Kirschenbaum's ["In the AI Era, Language is Now an Attack Surface"](https://www.techpolicy.press/in-the-ai-era-language-is-now-an-attack-surface/) traces a line from phone phreaking to prompt injection, arguing that once language can act as code, "Every string of text is a potential injection, a lurking threat vector." You just poured a large pile of other people's text into a system an agent built, and possibly into the agent itself. What does it mean to read social media at scale when the posts might also be instructions? And how does it feel to be on the collecting end, given that your own posts are someone else's dataset, and someone else's training data?

Circle back, too, to Week Four's Bamman, Underwood, and Smith piece on the literary canon large language models absorb. A search query builds its own kind of canon, and so does a platform. Whose posts did your terms find, and whose did they miss? If you worked with Hacker News, whose voices does the forum itself leave out? What did VADER count as negative: sarcasm, slang, in-jokes? Did your pipeline's choices show some of the same assumptions, now built into code instead of a conversational answer?

As you work through the analysis, consider how the relationship with text in distant reading connects to the other ways we've worked with AI, in both text and code, throughout the semester. Push for visualizations that mean something to you, not just ones that render. What did the computational approach reveal about your posts that a single conversational pass with Claude wouldn't have? How did working with an AI agent to build the whole pipeline change your process compared to Week Four's more conversational distant-reading pass? After these multiple explorations with Claude Code and Codex, how do you feel about the use of agents in the larger context of labor?

Finally, one last gesture at the epigraph — reading at this scale really is a parallel system of memory and thought — alongside the *AI for Good* Epilogue: does distant reading belong on Tyrangiel's list of constructive uses, or does something get lost when the reading itself is delegated to an agent?

Don't forget to reply twice to peers (1 point / reply) for full credit!
