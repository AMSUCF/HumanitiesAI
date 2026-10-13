---
layout: undergrad-page
title: "Module Three: Reading at Scale"
canvas:
  module: "Module Three: Reading at Scale"
  week_start: 2027-02-08
  due: 2027-02-21
  points: 10
  discussion: true
  extra_credit: false
  unit: words
---

<span class="unit-badge unit-badge--words">Words</span>

English classes usually teach **close reading**: slowing down to look carefully at a single passage. Digital humanities added another option, often called **distant reading**: using computers to count and compare patterns across more text than any one person could read. This module tries both, using a classic DH tool and an AI assistant side by side.

Ted Underwood's "Seven ways humanists are using computers to understand text" is a friendly tour of what text analysis can do, from simply counting words to building statistical models, and it makes the point that many of these methods are older and simpler than they sound. Miriam Posner's "How did they make that?" gives you a way to look at any digital project and break it down into three parts: its **sources** (what material it starts with), its **processes** (what was done to that material), and its **presentation** (how the results are shown). Use Posner's three parts to describe what you build this module.

## Tutorial: Distant Reading with Voyant and AI

[Voyant Tools](https://voyant-tools.org/) is a free, browser-based text analysis environment that has been a DH classroom staple for over a decade. Unlike a chatbot, Voyant doesn't generate anything: it counts, and it shows you exactly what it counted. That makes it a useful check on what an AI assistant tells you about a text.

### Step 1: Pick Your Texts

Choose two or three related texts from [Project Gutenberg](https://www.gutenberg.org/), which offers free, public-domain books. Pick texts you want to compare: two novels by the same author, two poets from the same period, a novel and its sequel, or several works in the same genre (for example, three early detective stories or three ghost stories). On each book's page, find the **Plain Text UTF-8** version and copy its link (or download the .txt file). For example, *Frankenstein* is [here as plain text](https://www.gutenberg.org/cache/epub/41445/pg41445.txt).

### Step 2: Explore in Voyant

Go to [voyant-tools.org](https://voyant-tools.org/), paste your plain text links into the box (one per line) or upload your .txt files, and click **Reveal**. Spend some time with the default tools (the [Voyant documentation](https://voyant-tools.org/docs/) explains each one):

- **Cirrus** (the word cloud): Which words dominate? Try clicking the settings icon to add words to the stopword list if things like "said" or character names crowd everything else out.
- **Terms** and **Trends**: Click a word to see how often it appears and where it rises and falls across the texts.
- **Contexts**: See every appearance of a word with the words around it (this is called "keyword in context").

Note that Project Gutenberg adds license text to the beginning and end of each file, which will show up in your counts. Notice whether it affects your results.

### Step 3: Ask an AI Assistant the Same Questions

Now open ChatGPT, Claude, Gemini, or Copilot and ask it about the same texts. If your tool lets you upload files, upload the plain text files; if not (or if the files are too large for your free tier), ask about the texts by title. Try prompts like:

> What are the most common meaningful words in [title], and what do they tell us about its themes?

> Compare [title] and [title]. What words or themes appear much more often in one than the other?

> Find three passages where the word "[a word you explored in Voyant]" appears, and explain what it means in each.

Then check its answers against Voyant. Did the chatbot's "most common words" match the actual counts? Did the passages it quoted really exist? (Search for them in Voyant's Contexts tool to find out.)

### Discussion

Share your texts, at least two screenshots from Voyant (Cirrus, Trends, or Contexts), and at least one screenshot of your AI conversation. Then reflect:

- What is one pattern you found across your texts that you wouldn't have noticed from close reading alone?
- Where did the AI assistant agree with Voyant, and where did it get the numbers, quotes, or patterns wrong? Why do you think a text-generating tool might be worse at counting than a tool built only to count?
- Using Posner's three parts (sources, processes, presentation), describe what you did this module. Which part did you have the most control over with Voyant, and which with the chatbot?
- Underwood describes many ways humanists use computers to understand text. Which one comes closest to what you did?

Make sure to reference both of the module's readings. Your post is worth 8 points; then reply to two classmates (1 point per reply) for full credit.
