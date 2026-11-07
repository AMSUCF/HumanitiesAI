---
layout: page
title: "Week Twelve: Puppet Masters — Local Ghosts"
hide_warning: true
canvas:
  module: "Week Twelve: Puppet Masters — Local Ghosts"
  week_start: 2026-11-09
  due: 2026-11-15
  points: 6
  discussion: true
  extra_credit: false
  unit: puppetmasters
---

<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>

> “Overspecialize and you breed in weakness. It’s slow death.” — Major Kusanagi, [*Ghost in the Shell* (1995) script](https://scrapsfromtheloft.com/movies/ghost-in-the-shell-1995-transcript/)

Kusanagi's warning about overspecialization is also an argument about infrastructure: a monoculture — one network, one provider, one way of running a mind — breeds in weakness. Every model we've used this semester has lived in someone else's data center. This week we bring a ghost home: a language model running on your own machine or inside your own browser, sending nothing out once it's downloaded.

Sam Altman would rather you didn't. As Mike Masnick reports in ["Sam Altman's Case Against Your RAM Is Efficient. That's the Problem."](https://www.techdirt.com/2026/11/02/sam-altmans-case-against-your-ram-is-efficient-thats-the-problem/), Altman argues that memory sitting in personal computers is "quite terrible" from a "global allocation perspective" because it is used only a fraction of the time. Masnick's answer is about control, not efficiency: "we've seen what happens when a central provider controls key parts of our stack, and the results are very, very, very bad." Running open-weight models locally "may not be the most efficient," but it "leads to much more actual user empowerment by people who want to use these tools, but without outsourcing control to someone like Altman."

In *AI for Good*, Tyrangiel makes a related point about literacy: "Just as important as what you begin to do with AI is what you decide not to do," because "user behavior is the most powerful feedback mechanism." You can only make those decisions well if you understand the tradeoffs, and running a model yourself makes them visible in a way the cloud hides. You'll see how much memory a model needs, how much a smaller model gives up, how long the download takes, and what it feels like when nothing leaves your machine.

## Exercise: Local Models

Choose **one** of two options. Option One installs software and runs a model on your own computer. Option Two runs a small model inside a web browser, using a tool you build with Claude or ChatGPT, so it needs no installation. If your computer can't run a model, or you can't install software on it, choose Option Two.

### Option One: Ollama and Local Model Testing

[Ollama](https://ollama.com/) is a free application for downloading open-weight models and running them on your own computer, with a chat window not unlike the browser-based chatbots we've been using.

1. **Find your specs.** Look up your operating system, processor (or Apple chip), amount of RAM, graphics card and its memory (VRAM) if you have one, and free disk space. On a Mac, open the Apple menu → **About This Mac**. On Windows, go to **Settings → System → About**, and check **Task Manager → Performance** for your GPU.
2. **Ask for a recommendation.** Give those specs to Claude or ChatGPT and ask it to suggest a model to run in Ollama. Turn on web search and ask it to check [Ollama's model library](https://ollama.com/library), since chatbots' knowledge of newer models can be out of date. Ask why it chose that model, what size it is, and what you give up compared to a larger one. Models range from about 1GB to well over 40GB, and the rough rule is that a model needs to fit in your RAM (or VRAM) with room to spare.
3. **Install Ollama** from [ollama.com](https://ollama.com/) and download the recommended model, either from the model menu in Ollama's chat window or with `ollama run <model name>` in a terminal. Large downloads can take a while, so start early.
4. **Test it.** Turn off your Wi-Fi and confirm the model still answers. Then put it through its paces: try the kinds of prompts you've used in earlier weeks, and give a few of the same prompts to Claude or ChatGPT to compare speed, quality, and refusals. Look up the model card on Hugging Face or Ollama to see whose model it is, how it was trained, and under what license. A model trained in one country or by one company may handle contentious questions very differently from another, so see if you can find points of friction. If you chose a reasoning model, read the "thinking" it shows before its answer.

**For full credit**, share screenshots of the model-recommendation conversation and of your local model interactions (at least two).

### Option Two: A Character in the Browser with Transformers.js

[Transformers.js](https://huggingface.co/docs/transformers.js) is a JavaScript library from Hugging Face that runs models directly in a web browser. A page built with it downloads a small model once, stores it in the browser, and then generates text on your own device: after the download, nothing you type is sent anywhere. In this option you'll use Claude or ChatGPT to build a web page that runs a small model to voice a character, then deploy it and talk to your character.

1. **Choose a character.** An original character, a figure from a public domain text, or a ghost of your own design all work. Write a short description of who they are, how they speak, and what they know.
2. **Build the interface.** Ask Claude or ChatGPT to build a single-page web app that uses Transformers.js to run a small instruct model in the browser and voice your character. It should recommend a minimal model that will run on an ordinary laptop (look for ONNX versions of small models in Hugging Face's [onnx-community](https://huggingface.co/onnx-community) collection), and the page should include a button to download the model with a progress bar, a short explanation for visitors of what is being downloaded and how big it is, and a chat window. Here's a starting prompt; adjust it to your character:

   > Build a single-page HTML app that uses Transformers.js to run a small instruct language model entirely in the browser, preferring WebGPU and falling back to WASM. The model voices this character: [your character description]. Recommend the smallest model that can hold the character's voice, and tell me its download size. Include a "Download model" button with a progress bar, a short note explaining to visitors that the model is downloaded once and then runs entirely on their device, and a chat window styled to fit the character. Keep the conversation history short so the model doesn't run out of context.

3. **Deploy it.** Put the page in a public GitHub repository and turn on GitHub Pages, as you did in [Week Ten](weekten.md); you can also build it directly in Claude Code on the web or Codex there. Pages that load models need to be served from a web address rather than opened as a file, and WebGPU works best in a current version of Chrome or Edge.
4. **Test it.** Download the model and chat with your character. How well does a tiny model hold a voice? When does it break character, repeat itself, or make things up? Try asking for a slightly larger model and compare the download size, speed, and quality. This is the tradeoff the cloud hides from you.

**For full credit**, share screenshots of your interactions with the character (at least two) and the link to your deployed page.

### Discussion

Share which option you chose, which model you ran and why, and your screenshots (plus your page link for Option Two). Then reflect:

- What did you learn about the tradeoffs of running a model yourself — in memory, download size, speed, quality, and privacy — that the cloud tools hide? Tyrangiel argues that "what you decide not to do" with AI is part of how users shape it. Did this week change what you'd decide to use, or not use?
- Altman frames local inference as an inefficient use of scarce memory; Masnick frames it as a question of control. Which argument persuades you more after this week, and what did you give up, in capability, convenience, or context, to keep the model on your own device?
- Tyrangiel's fourth chapter, "Only Connect," frames AI's value around fostering human connection. Does a model that runs off-network, connected to nothing, fit inside that framing, or work against it? What could local models mean for humanities research, creative practice, or teaching?

### Grading

- **4 points:** your discussion post with your screenshots (at least two of your model interactions) and reflection, plus your page link for Option Two.
- **2 points:** two replies to peers (1 point each).
