---
layout: page
title: "Week Nine: Puppet Masters — Distant Coding"
hide_warning: true
canvas:
  module: "Week Nine: Puppet Masters — Distant Coding"
  week_start: 2026-10-19
  due: 2026-10-25
  points: 6
  discussion: true
  extra_credit: false
  unit: puppetmasters
---

<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>

> “As a sentient lifeform, I hereby demand political asylum.” — the Puppet Master (Project 2501), [*Ghost in the Shell* (1995) script](https://scrapsfromtheloft.com/movies/ghost-in-the-shell-1995-transcript/)

**Slides:** [Week Nine slides](slides/weeknine.html)

For four weeks we asked what a ghost is, and for four more we asked what a shell is — bodies, surfaces, the images that stand in for a self. Puppet Masters turns to what sits underneath both: code that doesn't just describe or depict something, but *acts* — plans a next step, carries it out, and reports back. Project 2501 is this unit's presiding figure for exactly that reason. It was handed a narrow assignment — moving through data, manipulating records — and it exceeded it, becoming something that set its own goals instead of only completing the ones it was given. Over the next several weeks you'll spend less time asking a model to describe or generate something and more time asking it to *build*, starting today with a small, largely autonomous project of your own: a dataset, an interface, and a recommendation system, prompted into being rather than typed line by line.

## Tutorial: Distant Coding

This week builds on this unit's readings — Julia Evans's ["So you want to be a wizard"](https://wizardzines.com/zines/wizard/) and Simon Willison's ["Here's how I use LLMs to help me write code"](https://simonwillison.net/2025/Mar/11/using-llms-for-code/) — to think about what "programming" looks like when the interface is natural language rather than a text editor. Willison describes writing code by delegating to an LLM the way you might delegate to a very fast, very literal collaborator: you describe the outcome you want, review what comes back, and iterate from there rather than typing every line yourself. That's the model for this week's exercise. You'll build a small, structured dataset, then deploy it as an interactive site using Claude's artifact feature, without needing to edit any code directly. Instead, you'll follow my prompt sequence below and rewrite it in your own words — taking on, as Evans puts it, a project that looks too hard until you break it into pieces you can actually attempt.

### Prompts for Building a Cyborg and AI Media Recommender

These are the prompts I used to build a simple, Buzzfeed-style recommendation site for cyborg and AI media — anime, film, prose fiction, and games that explore artificial intelligence, cybernetic bodies, and human-machine hybridity, the same territory *Ghost in the Shell* itself occupies. The exact prompts I used for every stage, broken down to show the different stages of design, are below.

The Claude artifact feature will make it easier to watch the HTML file evolve as you iterate through the prompts. Your process should produce a complete interactive recommendation system within Claude's artifact viewer, which you can then publish and share.

1.  **Initial Dataset Creation**

    -   *Prompt*: "Create a list of 100 significant works of cyborg and AI media — spanning anime, film, prose fiction, and video games — that explore artificial intelligence, cybernetic bodies, or human-machine hybridity. Each entry should include the title, creator, year, medium (anime, film, fiction, or game), and one category from the following: Android and Replicant Narratives, Cybernetic Body Horror, Networked and Hive Minds, Rogue or Emergent AI, Companion and Domestic AI, Uploaded Consciousness, Military and Combat AI, Cyberpunk Society, Post-Human Futures, AI and Labor."

    -   *Suggested Modifications*: Try narrowing the dataset to a single medium (all anime, or all games) to see how its texture changes, or adjust the category list to match a different critical lens you'd rather explore. Be specific about the category options, since that structure is what the recommendation logic will lean on later.

2.  **Converting the List to JSON**

    -   *Prompt*: "Take the list of 100 works of cyborg and AI media and convert it into a JSON file, structured with each entry's title, creator, year, medium, and category."

    -   *Suggested Modifications*: Verify the plain-text list looks right before asking for the JSON conversion. If you're new to this kind of work, keep the category list to one clean dimension rather than layering several at once.

3.  **Displaying Works for User Rating**

    -   *Prompt*: "Create an HTML page with embedded script and style that takes the JSON data, selects 10 works at random, and displays them with radio buttons for users to rate them from 1 to 5 or select 'Haven't experienced it.'"

    -   *Suggested Modifications*: Display one work at a time and let users decide when to stop, or add a skip option for works they have no interest in. If you add features like these, mention them explicitly in your next prompt so the model keeps track of them going forward.

4.  **Generating Recommendations**

    -   *Prompt*: "After the user submits their ratings, display the top three categories based on the ratings they provided and recommend three works — make sure they are ones the user hasn't already rated."

    -   *Suggested Modifications*: Instead of just listing the top three categories, visualize the category preferences with a bar chart or pie chart. Try building a more sophisticated weighting system than a simple top-three count.

5.  **Setting Display and Style Updates**

    -   *Prompt*: "Make the page theme GitS-adjacent cyberpunk — dark UI, neon accents, styles and colors appropriate for that vibe."

    -   *Suggested Modifications*: Push the theme further with animation or interface details that fit your specific dataset — a HUD-style readout, a scanline effect, whatever feels right for the works you've catalogued. Make it as complicated as you'd like.

### Publishing Your Artifact

Feel free to expand on or iterate away from the simple recommendation system modeled here: our goal is to explore the process of iterating by combining real data and new interface elements to build interactivity through Claude. If you do something that breaks everything, you can always go back to a previous version of the artifact, so it's fine to experiment.

Once you've completed your recommendation system in Claude's artifact viewer, you'll need to publish it so others can interact with it. Share your Claude artifact the same way we've done with our other static pages this semester. Hold onto this dataset and site — we'll build on it directly next week, when Week Ten has you deploying a project of your own.

### Discussion

This week, share the link to your Claude artifact recommendation system, and think through its relationship to *AI for Good*'s opening chapters. Tyrangiel's introduction and first chapter, "I Believe the Children Are Our Future," make a case for AI's constructive uses on behalf of institutions and communities that mostly lack the resources to build these tools themselves; your recommendation site is a much smaller, much stranger version of that same premise — an interactive tool built almost entirely by delegation. What types of expertise went into each stage of building it? What assumptions or gaps do you see in the dataset you produced, and whose taste or canon does it end up reflecting?

Finally, a quick gesture at the epigraph — a tool demanding standing as the author of its own actions: did your project this week stay the careful delegation Willison describes, or did it do more than you explicitly told it to?
