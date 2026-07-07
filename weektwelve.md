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

Kusanagi's warning about overspecialization is also an argument about infrastructure: a monoculture — one network, one provider, one way of running a mind — breeds in weakness. This week's exercise asks what a ghost looks like when it refuses that condition entirely: a language model running on your own machine, answerable to no one, sending nothing out. Simon Willison's ["The lethal trifecta for AI agents"](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) names a more mundane version of the same worry that animates the film's ghost-hacking plot: an agent that can read private data, process untrusted content, and communicate externally has, in combination, everything it needs to leak what it shouldn't — no cyberbrain hacking required, just three ordinary capabilities meeting inside one system. Local models and careful agent design are two different answers to that worry. One keeps the ghost off the network altogether; the other tries to keep the trifecta's three legs from ever lining up inside a single agent. This week, choose one of two options to explore that territory hands-on.

## Exercise: Local Models or Agentic Applications

Moving beyond cloud-based AI systems, this week's exercise has two options: if you are interested in thinking about how we might use AI without being subject to the surveillance of cloud-based platforms and with lesser environmental impact, I recommend trying the local model exercise. This exercise introduces you to locally-hosted models that can run privately on your computer without internet access: this allows us to think about how a workflow that uses generative AI doesn't necessarily have to involve sending your personal data to corporations or resource-intensive, cloud-hosted tools. You'll install Ollama, download a local model, and experiment with its reasoning processes to think about how different models can offer dramatically different outputs (particularly around contentious subjects!)

The second option is to continue working with Claude Code, but on non-code applications. This is also an option that doesn't require installing any software, so if you don't have a setup where you have that access, choose this exercise. Both are explained below.

### Local Models: Installing Ollama and Setting Up Your Local Environment

For this exercise, you'll need to install Ollama, a tool that makes running large language models locally accessible with a simple graphical interface not unlike the browser-based chatbots we've been using:

1. **Download and Install Ollama**: Visit [https://ollama.ai/](https://ollama.ai/) and download the appropriate version for your operating system
2. **Model Selection**: For the demo, I used [DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1) — still a solid open-weight choice as of this writing: it's MIT-licensed, ships in distilled sizes from 1.5B up to 70B parameters, and runs well through Ollama. (DeepSeek's own frontier has moved on since — the company's newer V3.2 and V4 Preview lines are its current flagship models — but R1's distills remain the practical pick for running a reasoning model locally rather than in a data center.) Your choice will depend on your system's storage capacity and GPU capabilities. Consider these factors:
   - **Storage**: Models range from 1GB (small models) to 70GB+ (large models)
   - **RAM/GPU**: Larger models require more system memory and benefit from GPU acceleration
   - **Performance**: Smaller models run faster but may have reduced capabilities

Make sure to note which model(s) you experimented with when discussing your outputs - take a look at the model card to understand whose model it is, and how that might impact the results you get.

Once you have Ollama installed and a model downloaded, you'll be able to chat with it. If you are able to load a reasoning model (such as DeepSeek-R1, shown in the screenshot), a partial narrative of the model's "thought" process will be available as well, providing a user-facing summary of the steps taken:

![Ollama GUI](images/ollama.png)

Notice here how a controversial question (for a model developed in China) is handled differently in the output versus the reasoning workflow. Try different queries and see if you can find other contentious or unexpected points of friction. Think about how this compares to working with the cloud, and whether running the model entirely off-network changes what you're willing to ask it, or what you trust about what comes back.

### Agentic Applications: Claude Code for Non-Code

Agentic tools are being brought into a wide range of workflows for daily labor in all sorts of institutions, and Claude Code is one of the interfaces that is particularly popular for data-based tasks. Lenny Rachitsky has [curated a list](https://www.lennysnewsletter.com/p/everyone-should-be-using-claude-code) of some of the use cases for Claude Code: a few you might consider trying this week include building presentations; doing social media research; resizing and creating metadata for images; organizing notes for a large project; reformatting citations or papers to a different style; and other document-driven tasks. (More examples are listed in Canvas, but feel free to try something not on the list!)

For this exercise, I recommend continuing to work with Claude Code for the Web the way you set it up in [Week Ten](weekten.md) — that page has the full walkthrough for connecting a repository, generating a fine-grained personal access token, and the rest of the mechanics, so refer back to it for any step you need in detail. Put the files you want to manipulate in a repository, and set the repository to "private" instead of "public" when creating it, to avoid making the files public. Keep Willison's lethal trifecta in mind here even in this comparatively low-stakes setting: a private repo, an uploaded file you didn't write yourself, and an agent that can act back out onto the web are the same three ingredients — private data, untrusted content, external communication — that make agentic systems risky in general, just at a much smaller scale, so pick something to test with that doesn't include anything genuinely sensitive.

Upload all the relevant files before you use `/init` to start your Claude Code interactions with that repository: this will let Claude Code review what you already have, and result in better suggestions for the process. Use the plan mode you practiced in [Week Eleven](weekeleven.md) to iterate through a solution to your task. Execute the task and iterate to see if you can get results that are useful for your non-code goals.

### Discussion

If you selected option one:

Share your experience with local AI models, including which model(s) you chose and why. Reflect on the differences between local and cloud-based AI interactions. What did you observe about the model's reasoning process? How might widespread access to powerful local AI change the landscape of human-computer interaction, creative work, and intellectual labor? Does running a model entirely off-network answer some of the concerns raised by our readings this semester around privacy, control, and accessibility — or raise others? Connect your observations to our course themes about AI democratization, education, and the future of creative and scholarly work.

If you selected option two:

Share your experience with Claude Code for a non-code task. How does this compare to working with files in our previous exercises through the main chatbot interface? Do you notice any differences in the processing, handling of context, and outcomes? Connect your observations to our readings about programming and control, and think about the implications for software more broadly.

For both, connect your experience to Willison's lethal trifecta: a local model removes the ghost from the network entirely, while an agent like Claude Code stays on it but (ideally) keeps private data, untrusted content, and outbound communication from lining up at once. Which answer did you end up trusting more this week, and what did you give up — in capability, convenience, or context — to get it? Tyrangiel's fourth chapter, "Only Connect," frames AI's value around fostering human connection rather than replacing it — does a local model that runs off-network, answerable to no one and connected to nothing, sit comfortably inside that framing, or does "only connect" start to sound like the opposite of this week's whole point? Finally, what could AI agents — whether local or cloud-based — mean for humanities research, creative practice, or educational work?
