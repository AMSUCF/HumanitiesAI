---
layout: page
title: "Week Fourteen: The Net Is Vast and Infinite — Custom Bots (Extra Credit)"
hide_warning: true
canvas:
  module: "Week Fourteen: The Net Is Vast and Infinite — Custom Bots (Extra Credit)"
  week_start: 2026-11-30
  due: 2026-12-06
  points: 0
  discussion: true
  extra_credit: true
  unit: coda
---

<span class="unit-badge unit-badge--coda">The Net Is Vast and Infinite</span>

> "And where does the newborn go from here? The net is vast and infinite." — the merged Kusanagi/Puppet Master entity, closing line of *Ghost in the Shell* (1995)

Kusanagi spent the whole film asking whether there was "a program called 'me.'" By the closing line she isn't asking anymore — she's answered the question by becoming something neither Kusanagi nor the Puppet Master was on its own, and all that's left to wonder is where that newborn thing goes from here. This coda asks the same question of the bots you've built and talked to all semester. We opened in Week One with ELIZA, a scripted ghost running Weizenbaum's old pattern-matching script, mouthing sympathy it didn't have. We're closing with you building your own: a Skill, a subagent, or a small fine-tuned model trained on texts you choose — something that, like the Puppet Master, might exceed the instructions you gave it.

**This module is entirely extra credit, and it is the last content module of the semester.** It opens Monday, November 30, right after Thanksgiving break, and is due Sunday, December 6. There are three independent tiers below, worth different point values, and you can attempt one, two, or all three: **Option One, Claude Skills, is worth up to 6 points; Option Two, Claude Code subagents, is worth up to 6 points; Option Three, fine-tuning your own model, is worth up to 10 points.** None of it is required — engage as much or as little as fits your goals and your current grade. Once this module closes, the only work left is the **Final Reflection, due Thursday, December 10,** during finals week.

## Exercise: Custom Bots

As we're approaching the end of the semester, this exercise is optional, and there are three options of increasing complexity: I recommend watching through the demo videos first, and deciding which appeals — or trying more than one.

### Option One: Claude Skills (Extra Credit up to 6 points)

For this option, you will be working through the main Claude chatbot interface. First, go to settings and make sure you've enabled "skill-creator" under Capabilities->Skills.

Next, use an initial prompt that starts with "Use the skill-creator skill to help me create a new skill for..."

As with your previous work with Claude, make sure to be as precise as possible. Follow the suggestions in [this discussion of frontend design in Claude](https://www.claude.com/blog/improving-frontend-design-through-skills) and think about areas of frustration you've experienced: you could provide a detailed style guide for writing; a set of preferences for the styling of HTML pages; etc.

Once Claude creates the skill, it will provide the file as a .zip. Save that and return to the settings page: select "Upload Skill" under settings, and upload your file. Make sure the skill is activated, and return to the chatbot. Prompt your own skill tool using the name listed in "skills," and test some outputs. Did it change the defaults you typically get from Claude? Was your intention realized?

### Option Two: Claude Code Subagents (Extra Credit up to 6 points)

This option requires Claude Code to be installed on your computer: unfortunately, it takes advantage of capabilities that the web version doesn't have, as the agents and their instructions are stored on your own hard drive. For this exercise, first open your terminal or command line and navigate to an empty folder, then type "claude" to start.

Type "/agents" and press enter to launch the agents interface. Select "Create new agent" and press enter. I recommend adding the agent to "Personal" so that you can make use of it in the future, particularly if you have a concept for some customization that might be useful: for instance, you might build an agent dedicated to fixing the front-end design of a site, rather like the Skills option above. For examples, check out [this collection of Claude Code subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) and [this collection of quality-assurance agents, including "reality check Karen"](https://github.com/darcyegb/ClaudeCodeAgents).

To run the agent in the future, invoke it in your prompts by using the name under which your agent was saved. Iterate and test your results, and consider refining the agent's description (stored on your computer as a Markdown file in the directory you specified). As before, try it out: was your intention realized?

### Option Three: Fine-Tuning (Extra Credit up to 10 points)

Remember, this is totally optional, and it is intended for those who think it looks fun. It is a complicated workflow, and can be frustrating to get to work, but in exchange it gives you control over a model at a next level compared with our previous projects. This workflow also introduces [Hugging Face](https://huggingface.co/), a platform that hosts machine learning models and datasets, making it easier to access and fine-tune pre-trained language models for custom applications. If you want to, you can even push your model to the cloud.

Recall the ELIZA bot we "spoke" with at the beginning of the class: ELIZA's code uses the same fundamental structures you've been reading about all semester in the Ghosts unit. Her set of replies is fundamentally limited to what's pre-scripted. We could easily build our own version of ELIZA at this stage, but instead of working with an "old-school" bot, we're going to use the skills you've gained with scraping and preparing datasets to fine-tune a basic story-generation bot — one trained not on Oz, this time, but on a shelf of texts that were imagining machine minds and artificial bodies long before Major Kusanagi ever asked whether she had a ghost.

#### Hugging Face

For this exercise, you'll use a large number of texts — the six-text "Ghosts Before the Shell" corpus described below. Before you begin, you'll need to create a free Hugging Face account and get an access token, then bring that into the notebooks below:

1. **Create an Account**: Go to [Hugging Face](https://huggingface.co/) and sign up for a free account
2. **Generate a Token**:
   - Click on your profile picture in the top right corner
   - Select "Settings" from the dropdown menu
   - Click on "Access Tokens" in the left sidebar
   - Click "New token" and give it a name (like "Colab Fine-tuning")
   - Set the role to "Write" (this allows you to upload models if you choose)
   - Copy the generated token
3. **Add to Colab Secrets**:
   - In your Google Colab notebook, click the key icon (🔑) in the left sidebar
   - Click "Add new secret"
   - Name it `HF_TOKEN`
   - Paste your Hugging Face token as the value
   - Make sure to enable notebook access for this secret

This token allows the notebook to access Hugging Face's model hub and optionally upload your fine-tuned model to use through your local Ollama interface.

#### The Corpus: Ghosts Before the Shell

Rather than the Oz books used in previous versions of this exercise, this year's fine-tuning corpus is "Ghosts Before the Shell" — six public-domain texts, spanning more than a century, that imagine artificial minds and artificial bodies long before *Ghost in the Shell* gave that idea a name. Read together, they're a rough prehistory of the Puppet Master: proof that the anxiety this course has spent fourteen weeks on is much older than generative AI, or even computers. All six are confirmed public domain in the USA and downloadable as plain text directly from Project Gutenberg at `https://www.gutenberg.org/ebooks/<ID>.txt.utf-8`, substituting the ID from the table below.

| Text | Author / Translation | Gutenberg ID | Notes |
|---|---|---|---|
| *Frankenstein; or, The Modern Prometheus* | Mary Shelley (1818 first edition) | **41445** | The 1831 revised edition is a separate Gutenberg ID (#42324); this corpus uses the 1818 text. |
| *R.U.R. (Rossum's Universal Robots)* | Karel Čapek, trans. Nigel Playfair and Paul Selver (1920) | **59112** | The English acting version — the play that coined the word "robot." |
| *Metropolis* | Thea von Harbou (English translation of the 1925/26 novel) | **73727** | Gutenberg marks it explicitly public domain in the USA; the translator is uncredited. |
| "Moxon's Master" | Ambrose Bierce | in **4366** (*Can Such Things Be?*) | No standalone Gutenberg edition — the story lives inside this short-story collection. Extract just this one story for your dataset. |
| "The Sand-Man" | E.T.A. Hoffmann, trans. J.T. Bealby | in **31377** (*Weird Tales, Vol. 1 of 2*) | Also no standalone English edition — it's the opening story of Bealby's *Weird Tales* Vol. 1. Extract just this one story. |
| *The Huge Hunter; or, The Steam Man of the Prairies* | Edward S. Ellis (1868) | **7506** | A dime-novel proto-robot story, decades before either Čapek or von Harbou. |

For the two texts that don't have their own Gutenberg edition — "Moxon's Master" and "The Sand-Man" — you'll need to pull just that story out of the full collection text before feeding it to the dataset-building notebook; both stories are clearly marked and easy to isolate by hand.

#### Working with the Notebooks

This exercise uses two separate notebooks for the complete workflow — these notebooks are on Google Colab, and in my video I walk through each step:

**Step 1 - Dataset Building**: [Build Training Dataset](https://colab.research.google.com/drive/1YHkYvyiAGDygPCY2Vdz4PTqcS8s3ZVxL?usp=sharing)

This first notebook will take you through the prep of uploading and processing your six Project Gutenberg texts (downloaded per the table above) and breaking them into story-esque fragments for the dataset. You'll need the Hugging Face token to complete the upload and easily reference the dataset you create from your second notebook. You might name your uploaded dataset something like `ghosts-before-the-shell`. For reference, here's an example of a completed dataset from a previous run of this course, built from the Wizard of Oz books rather than this year's corpus: [Oz Fragments Dataset](https://huggingface.co/datasets/anasalter/oz-fragments) — the theme is different, but it shows you the general shape your own processed dataset will take once it's uploaded.

**Step 2 - Model Training**: [Fine-Tune Custom Bot](https://colab.research.google.com/drive/1-13FhqtVw2ZUB79cL-SQ59Y-i3QZGfGL?usp=sharing)

This second notebook will fine-tune the model: this is a notebook that I've lightly customized from [Unsloth](https://unsloth.ai/), a tool for lowering the time and GPU requirements for training. You might name your finished model something like `proto-ghost-completion-model` — a small nod to the century of machine-mind anxiety it was trained on, before there was ever a "ghost in a shell" to name it. For reference, here's an example of a completed fine-tuned model from that same previous, Oz-based run: [Oz Completion Model](https://huggingface.co/anasalter/oz-completion-model). Again, the theme won't match this year's corpus, but it's ready for use in Ollama and shows you the general shape your own trained model will take once it's finished.

Work through both notebooks in order - the dataset-building notebook prepares the foundation, and the training notebook creates your custom bot. There are some places to test the output directly in the notebook; however, if you want to run the model yourself, you'll need to load up your terminal or command prompt and install your model to Ollama after it is uploaded to Hugging Face. The command to run your model is:

    ollama run hf.co/user_name/model_name

It might take some time to install your model, but after it downloads, you can run it like any other model through the local interface.

### Discussion

However far you got this week, connect it back to two points from earlier in the semester: the ELIZA conversation you had in Week One, and the Puppet Master presiding over the whole Puppet Masters unit.

- If you built a **Skill**: did it change the defaults you typically get from Claude? Was your intention realized, or did Claude's read of your instructions surprise you?
- If you built a **subagent**: what did you name it, what did you ask it to do, and did it stay inside those instructions or wander outside them the way the Puppet Master eventually did?
- If you **fine-tuned a model**: what did training on a century of pre-Kusanagi machine-mind anxiety — Shelley's Creature, Čapek's robots, von Harbou's Maria, Bierce's chess automaton, Hoffmann's Olimpia, Ellis's steam man — produce, once it started generating its own sentences? Did it sound like any one of those six texts in particular, or like something new stitched out of all of them?

Compare whichever experience you chose to the bot interactions we had at the start of the semester. ELIZA's replies were fully pre-scripted; the Puppet Master's were not, and by the film's end it isn't clear that "scripted" and "not scripted" is even the right line to draw anymore. Where does your own custom bot fall on that line — closer to ELIZA's script, or closer to something that occasionally does what you didn't tell it to?

Remember, this exercise is extra credit: you can choose to engage part or all of the prompt depending on your goals and current grade. And as you close out this last module, carry the epigraph with you into the Final Reflection: the net is vast and infinite, and so, it turns out, was the semester's real question — not whether these systems have ghosts, but what we do once we've built our own.
