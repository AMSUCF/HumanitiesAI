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

> Drifting through the city by boat, Kusanagi passes shop windows lined with mannequins — blank-faced, dressed, waiting — and for a moment her own reflection folds into theirs, one more crafted body on display among a row of crafted bodies. — after [*Ghost in the Shell* (1995)](https://en.wikipedia.org/wiki/Ghost_in_the_Shell_(1995_film))

Last week we generated shells; this week we go looking for the ones already sitting in archives, waiting to be described. The mannequin-window sequence is the hinge: Kusanagi's shell was manufactured to be looked at, and so is every doll, gynoid, and posed figure in the image collections we're about to turn a model loose on. *The AI Con*'s chapter on doomers and boosters and Noble's chapter on searching are both, in their way, about who gets to decide what an image "shows" and whose interests that framing serves — worth keeping close as you ask an LLM to describe, caption, and visualize a set of images it has never seen before and has no stake in getting right.

## Tutorial: Archival Images

This week, we're going to think about the challenges of translation from one medium to another, and explore how LLMs process or "see" complex images. For this project, I recommend working with images you find interesting that are related to your work in some way — assemble these as a collection that speaks to a theme or subject that has significant complexity. If you need ideas, consider working from an existing archive, such as image collections within the [Internet Archive](https://archive.org/details/image) or the [Library of Congress](https://www.loc.gov/pictures/). Consider the work discussed in this week's reading on Refik Anadol — his [*Archive Dreaming*](https://refikanadol.com/works/archive-dreaming/) trains a model on roughly 1.7 million archival documents and lets visitors move through the resulting associations as a physical, architectural space — and ask how generative AI might change your approach to a larger visual cultural dataset. While we won't be working at that scale for this exercise, consider the broader projects that might build on these methods.

[Louis Jebb's *Art Newspaper* interview with Anadol](https://www.theartnewspaper.com/2024/04/05/on-process-refik-anadol-seeks-to-demystify-ai-art-by-showing-how-it-is-put-together) is useful here for demystifying the "art" side of this process: Anadol is unusually candid about the pipeline of data collection, model training, and human curatorial choice that sits behind a piece that otherwise reads as pure spectacle. If you want a sharper critical counterweight, this week's optional reading — Gabriel Menotti's *[**"The model is the museum," AI & Society (2025)**](https://link.springer.com/article/10.1007/s00146-025-02290-1)* — argues that projects like this can also be read as a kind of expropriation of cultural heritage, training on collections whose original communities have no say in how their material gets remixed. *(Recommended and optional; PDF in Webcourses.)*

### Image to Text Translation

Iterate through a series of prompts to build from analyzing single images to a larger set. You will need your Claude.ai subscription to provide a sufficient number of images at once (through the upload function — just select multiple files in a folder) to see patterns. Work from simpler images (with or without text) to more complex and potentially confusing images. These can be photographs or, as with our readings, not-photographs of any kind — a set of screenshots, archival scans, hand-written documents, etc.

Here's a few examples of questions to ask about single sets and images to prompt different types of translation:

- **Describe what you see in this image.** Follow up about material elements and specific details in the image. If there's an art or craft depicted, ask about the process or construction.
- **Write alt-text for this image.** Keep in mind accessibility standards. To work more broadly, ask it to extrapolate and provide introductory descriptive text for the set of images.
- **Pull out and describe key features.** Start with a single image, and work up to a larger set. See if it can assist in drawing out or recognizing patterns of details, composition, etc. that might be of interest.
- **Visualize the set.** Ask it to use the file names of the images, and put them into a meaningful relationship: you could ask for a visualization positioning them in relationship to one another based on key characteristics. For my demonstration, I worked across a set of [comic covers](https://www.coverbrowser.com/covers/punisher). The [outputted artifact visualizing those covers is here](https://claude.ai/public/artifacts/5daa035e-6fab-4f9c-b8aa-e9b0a60f4cdb). Try building similar artifacts or asking for something more complex — you're free to work from that same demonstration set or to build one of your own from the archives linked above.

As you work, think about how this might change your approach to text-to-image prompting (like we did last week). Consider what other uses this might have for investigating material culture, and where the weaknesses are in the translations.

### Discussion

Take screenshots of highlights (particularly visualizations and other analysis) or links to artifacts generated to share out in the discussion. You should be able to submit a large number of images at once using your Claude.ai subscription, so try to push the limits and see what type of results you can get working towards analysis at scale. Stick with Claude Sonnet 5 to avoid quickly running into usage caps. While it will be easier to analyze the accuracy of the results with images you are familiar with, consider branching out as you experiment to see how useful you find the translations provided.

Finally, bring this back to the epigraph and the mannequin-window sequence. When Claude writes alt-text or a description for an archival image, it is producing a new surface for that artifact — a shell of language wrapped around whatever the original object was, the same way Kusanagi's chassis is a shell wrapped around whatever the Major is. Whose reading is that description: the archive's, the photographer's or maker's, yours for choosing the prompt and the image, or the model's, drawing on however it learned to talk about images like this one? And if a machine-generated caption becomes the way most future viewers encounter that artifact — the way a wall label outlives the object it describes — has authorship of the piece quietly shifted to whoever wrote (or prompted) the description?
