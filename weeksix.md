---
layout: page
title: "Week Six: Shells — Art and Creativity"
hide_warning: true
canvas:
  module: "Week Six: Shells — Art and Creativity"
  week_start: 2026-09-28
  due: 2026-10-04
  points: 6
  discussion: true
  extra_credit: false
  unit: shells
---

<span class="unit-badge unit-badge--shells">Shells</span>

> “I collect information to use in my own way.” — Major Kusanagi, [*Ghost in the Shell* (1995) script](https://scrapsfromtheloft.com/movies/ghost-in-the-shell-1995-transcript/)

Last week we generated shells; this week we go looking for the ones already sitting in archives, waiting to be described. Kusanagi collects information to use in her own way; so does every archive — and so, in its own opaque way, does the model we're about to turn loose on one. *The AI Con*'s chapter on doomers and boosters and Noble's chapter on searching are both, in their way, about who gets to decide what an image "shows" and whose interests that framing serves — worth keeping close as you ask an LLM to describe, caption, and visualize a set of images it has never seen before and has no stake in getting right.

## Tutorial: Archival Images

This week, we're going to think about the challenges of translation from one medium to another, and explore how LLMs process or "see" complex images. For this exercise, you'll be working in a project in either Claude or ChatGPT's Work mode, just as we did with the distant read in Week Four. For this project, I recommend working with images you find interesting that are related to your work in some way — assemble these as a collection of at least 10 images or imagetexts that speaks to a theme or subject that has significant complexity. The [Internet Archive](https://archive.org/details/image) is my recommended source: its image collections, scanned books, magazines, and comics give you plenty of material to choose from, and it's easy to download a set as individual files. The [Library of Congress](https://www.loc.gov/pictures/) is another good option if you need ideas. Consider the work discussed in this week's reading on Refik Anadol — his [*Archive Dreaming*](https://refikanadol.com/works/archive-dreaming/) trains a model on roughly 1.7 million archival documents and lets visitors move through the resulting associations as a physical, architectural space — and ask how generative AI might change your approach to a larger visual cultural dataset. While we won't be working at that scale for this exercise, consider the broader projects that might build on these methods.

[Louis Jebb's *Art Newspaper* interview with Anadol](https://www.theartnewspaper.com/2024/04/05/on-process-refik-anadol-seeks-to-demystify-ai-art-by-showing-how-it-is-put-together) is useful here for demystifying the "art" side of this process: Anadol is unusually candid about the pipeline of data collection, model training, and human curatorial choice that sits behind a piece that otherwise reads as pure spectacle. If you want a sharper critical counterweight, this week's optional reading — Gabriel Menotti's *[**"The model is the museum," AI & Society (2025)**](https://link.springer.com/article/10.1007/s00146-025-02290-1)* — argues that projects like this can also be read as a kind of expropriation of cultural heritage, training on collections whose original communities have no say in how their material gets remixed. *(Recommended and optional; PDF in Webcourses.)*

### Image to Text Translation

Iterate through a series of prompts to build from analyzing single images to a larger set. Start by setting up a project: in Claude, create a new project and upload your images to it; in ChatGPT, create a project and select Work mode. Upload at least 10 images or imagetexts to the project for best results (just select multiple files in a folder) — the model needs enough of a set to see patterns. Work from simpler images (with or without text) to more complex and potentially confusing images. These can be photographs or, as with our readings, not-photographs of any kind — a set of screenshots, archival scans, hand-written documents, etc.

A note if you're using Claude: Cowork no longer exists as a separate mode. Its capacities are now integrated into the main Claude chat, so work from a chat inside your project. Make sure to ask for an artifact as your output whenever you want a visualization or interface, so that you get something you can open, explore, and share with a link.

Here's a few examples of questions to ask about single sets and images to prompt different types of translation:

- **Describe what you see in this image.** Follow up about material elements and specific details in the image. If there's an art or craft depicted, ask about the process or construction.
- **Write alt-text for this image.** Keep in mind accessibility standards. To work more broadly, ask it to extrapolate and provide introductory descriptive text for the set of images.
- **Pull out and describe key features.** Start with a single image, and work up to a larger set. See if it can assist in drawing out or recognizing patterns of details, composition, etc. that might be of interest.
- **Visualize the set.** Ask it to use the file names of the images, and put them into a meaningful relationship: you could ask for an artifact positioning them in relationship to one another based on key characteristics. For my demonstration, I worked across a set of [comic covers](https://www.coverbrowser.com/covers/punisher). Try building similar artifacts or asking for something more complex — you're free to work from that same demonstration set or to build one of your own from the archives linked above.

As you work, think about how this might change your approach to text-to-image prompting (like we did last week). Consider what other uses this might have for investigating material culture, and where the weaknesses are in the translations.

### Discussion

Take screenshots of highlights (particularly visualizations and other analysis) or links to artifacts generated to share out in the discussion. With your images in a project, you should be able to work across a large number of them at once, so try to push the limits and see what type of results you can get working towards analysis at scale. I recommend using the newest models: Claude Opus 5.5 ([model card](https://www-cdn.anthropic.com/fc1b44717c85dc068bc6ba5024219938094694bd/Claude%20Opus%205.5%20System%20Card.pdf)) or ChatGPT's GPT-6 Sol or GPT-6 Luna ([model cards](https://deploymentsafety.openai.com/gpt-6-astra/sec%3Aappendix-sol-luna)), all released on September 22. Simon Willison's post ["Claude Opus 5.5, GPT-6 Sol, GPT-6 Luna, and a new price war"](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/) breaks down the differences between them, and it's on this week's reading list. While it will be easier to analyze the accuracy of the results with images you are familiar with, consider branching out as you experiment to see how useful you find the translations provided.

Finally, a gesture back at the epigraph: a machine-written caption is a model collecting an archive's information to use in its own way. Whose reading is that description — and does it matter, if it becomes the way most future viewers encounter the artifact?

Don't forget to reply twice to peers (1 point / reply) for full credit!
