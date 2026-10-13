---
layout: undergrad-page
title: "Module Six: Building with AI"
canvas:
  module: "Module Six: Building with AI"
  week_start: 2027-03-29
  due: 2027-04-11
  points: 10
  discussion: true
  extra_credit: false
  unit: code
---

<span class="unit-badge unit-badge--code">Code</span>

Digital humanities has long valued *making* things, such as digital editions, archives, maps, and websites, as a way of thinking. In "On Building," Stephen Ramsay argues that building is itself a form of humanities scholarship: when you make a digital project, you're forced to decide what matters and how it fits together. Until recently, building usually meant learning to code. AI coding assistants have changed that, letting people describe what they want in plain language and get working software back.

That doesn't mean the human's job disappears. Simon Willison, a programmer who writes thoughtfully about AI tools, describes in "Here's how I use LLMs to help me write code" how he gets good results: giving the AI clear context, asking for specific changes, testing everything, and remembering that he, not the AI, is responsible for what the code does. You don't need any programming experience for this module, but you'll practice the same habits.

## Tutorial: Build a Mini-Exhibit

In this exercise, you'll use an AI assistant to build a small, interactive web page: a mini-exhibit that presents material you've already worked with this semester. Most assistants can now write a complete web page and show it to you right in the chat:

- **Claude:** ask for an "artifact," which opens beside the chat, can be edited by further prompts, and can be published with a shareable link.
- **ChatGPT:** ask it to build in "canvas," which shows the code and can preview it.
- **Gemini:** choose "Canvas" from the tools menu, then preview and share the page.

### Step 1: Plan Your Exhibit

Go back to your work from Module Three (your texts) or Module Five (your archival images) and choose one as the basis of your exhibit. Using Posner's three parts from Module Three, jot down:

- **Sources:** what material will the exhibit include? (5-8 items is plenty.)
- **Processes:** what do you want to do with that material: group it, compare it, put it on a timeline, quiz the visitor?
- **Presentation:** what should a visitor see and click on?

### Step 2: Write Your First Prompt

Describe the exhibit as specifically as you can, and paste in the information it needs (titles, dates, short descriptions, image links from the catalog pages, or quotations from your texts). For example:

> Build a single-page interactive web exhibit called "Cats in the Library of Congress." It should show these six images as a gallery, using the image links below. Clicking an image should open a panel with its title, date, and a two-sentence description. Add buttons to sort the gallery by date or by type (photograph, print, poster). Make it accessible, with alt text for every image. Here is my information: [paste]

If images from the archive won't load in the preview, that's OK: ask the AI to use placeholder boxes with the titles instead, and focus on the structure.

### Step 3: Revise at Least Five Times

Your first result will be a starting point. Make **at least five** follow-up requests to improve it, and be specific: "make the text larger and use a dark background" works much better than "make it look better." Try adding a feature (a search box, a timeline, a short quiz), fixing something that doesn't work, or changing the design to suit your material. Test every change by clicking through the page yourself.

### Step 4: Look Under the Hood

Ask the AI: "Explain how this code works, section by section, for someone who has never programmed." Read the explanation, then find one part of the code that it describes. You don't have to understand everything, but you should be able to point to where your content lives in the code.

### Step 5: Share It

Publish or share your exhibit so others can open it (Claude's **Publish** button, ChatGPT's **Share**, or Gemini's **Share** option). Open the link in a private browser window to make sure it works for someone who isn't you.

### Discussion

Share the link to your exhibit, a screenshot, and your list of prompts (first prompt plus at least five revisions). Then reflect:

- Ramsay argues that building is a way of thinking. What decisions did building this exhibit force you to make about your material that you hadn't made before?
- Which of Willison's habits did you end up using? Where did the AI do something you didn't ask for, or get something wrong?
- After Step 4, how much of the code do you feel responsible for? If someone found an error in your exhibit, whose error would it be?

Make sure to reference both of the module's readings. Your post is worth 8 points; then reply to two classmates (1 point per reply) for full credit.
