---
layout: undergrad-page
title: "Module Six: Building with AI"
canvas:
  module: "Module Six: Building with AI"
  week_start: 2027-03-29
  do_start: 2027-04-05
  due: 2027-04-11
  points: 10
  discussion: true
  extra_credit: false
  unit: code
---

<span class="unit-badge unit-badge--code">Code</span>

## Think: Week 11 (March 29 - April 4)

Digital humanities has long valued *making* things, such as digital editions, archives, maps, and websites, as a way of thinking. In "On Building," Stephen Ramsay argues that building is itself a form of humanities scholarship: when you make a digital project, you're forced to decide what matters and how it fits together. Until recently, building usually meant learning to code. AI coding assistants have changed that, letting people describe what they want in plain language and get working software back.

That doesn't mean the human's job disappears. Simon Willison, a programmer who writes thoughtfully about AI tools, describes in "Here's how I use LLMs to help me write code" how he gets good results: giving the AI clear context, asking for specific changes, testing everything, and remembering that he, not the AI, is responsible for what the code does. You don't need any programming experience for this module, but you'll practice the same habits.

**To do this week:**

- Read [Ramsay](https://web.archive.org/web/20251228181813/https://stephenramsay.us/text/2011/01/11/on-building/) and [Willison](https://simonwillison.net/2025/Mar/11/using-llms-for-code/).
- Watch the lecture video in Webcourses and look through the [Module Six slides](slides/modulesix.html).
- Note: the university withdrawal deadline is **Friday, April 2**.

## Do: Week 12 (April 5 - 11)

### Watch First

Simon Willison, author of this module's reading, reviews a year of AI models by asking each one to write code that draws a pelican riding a bicycle. (You saw some of those pelicans in the lecture slides.)

<div class="ug-video" style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; overflow: hidden;"><iframe src="https://www.youtube.com/embed/YpY83-kA7Bo" title="2025 in LLMs so far, illustrated by Pelicans on Bicycles — Simon Willison" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

[2025 in LLMs so far, illustrated by Pelicans on Bicycles — Simon Willison](https://www.youtube.com/watch?v=YpY83-kA7Bo): Simon Willison (AI Engineer, 2025), about 18 minutes.

**As you watch:** Notice how Willison judges each result: what counts as "working," what he checks, and what he laughs at. Use the same eye on the exhibit your chatbot builds for you.

### Exercise: Build a Mini-Exhibit

You'll use an AI assistant to build a small, interactive web page: a mini-exhibit that presents material you've already worked with this semester. Most assistants can now write a complete web page and show it to you right in the chat:

- **Claude:** ask for an "artifact," which opens beside the chat, can be edited by further prompts, and can be published with a shareable link.
- **ChatGPT:** ask it to build in "canvas," which shows the code and can preview it.
- **Gemini:** choose "Canvas" from the tools menu, then preview and share the page.

#### Step 1: Plan Your Exhibit

Go back to your work from Module Three (your texts) or Module Five (your archival images) and choose one as the basis of your exhibit. Borrowing the way Posner described projects in Module Three, jot down:

- **What it is:** a one-sentence description of the exhibit and who it's for.
- **What goes in it:** the material it will include (5-8 items is plenty).
- **What a visitor can do:** browse a gallery, sort or compare items, follow a timeline, take a quiz?

#### Step 2: Write Your First Prompt

Describe the exhibit as specifically as you can, and paste in the information it needs (titles, dates, short descriptions, image links from the catalog pages, or quotations from your texts). For example:

> Build a single-page interactive web exhibit called "Cats in the Library of Congress." It should show these six images as a gallery, using the image links below. Clicking an image should open a panel with its title, date, and a two-sentence description. Add buttons to sort the gallery by date or by type (photograph, print, poster). Make it accessible, with alt text for every image. Here is my information: [paste]

If images from the archive won't load in the preview, that's OK: ask the AI to use placeholder boxes with the titles instead, and focus on the structure.

#### Step 3: Revise at Least Five Times

Your first result will be a starting point. Make **at least five** follow-up requests to improve it, and be specific: "make the text larger and use a dark background" works much better than "make it look better." Try adding a feature (a search box, a timeline, a short quiz), fixing something that doesn't work, or changing the design to suit your material. Test every change by clicking through the page yourself. **Keep a list of your first prompt and each revision prompt.**

#### Step 4: Look Under the Hood

Ask the AI: "Explain how this code works, section by section, for someone who has never programmed." Read the explanation, then find one part of the code that it describes. You don't have to understand everything, but you should be able to point to where your content lives in the code.

#### Step 5: Share It

Publish or share your exhibit so others can open it (Claude's **Publish** button, ChatGPT's **Share**, or Gemini's **Share** option). Open the link in a private browser window to make sure it works for someone who isn't you.

### Discussion

| Points | What to post |
|--------|--------------|
| 3 | **Evidence**, 1 point each: a working link to your exhibit, a screenshot of the finished exhibit, and your list of prompts (your first prompt plus at least five revisions) |
| 4 | **Reflection of at least 250 words** that answers the questions below |
| 1 | **One citation:** quote or point to a specific idea from Ramsay or Willison, naming the author |
| 2 | **Two replies** to classmates, 1 point each (at least 50 words each). Open their exhibits before you reply! |
| **10** | **Total** |

Questions to answer in your reflection:

- What did you build, and who is it for? What decisions did building it force you to make about your material that you hadn't made before?
- Which of Willison's habits did you end up using? Where did the AI do something you didn't ask for, or get something wrong?
- After looking under the hood, how much of the code do you feel responsible for? If someone found an error in your exhibit, whose error would it be?

**AI use:** use AI to build the exhibit (that's the whole exercise!), but write your reflection and your replies yourself, with no AI (see the [AI Use Policy](index.md#ai-use-policy)).

**Due Sunday, April 11 at 11:59 PM.** The discussion stays open until Monday, April 12 at 11:59 PM, then closes.
