---
layout: page
title: "Week Thirteen: Local Models"
hide_warning: true
---

## Exercise: Local Models or Agentic Applications

Moving beyond cloud-based AI systems, this week's exercise has two options: if you are interested in thinking about how we might use AI without being subject to the surveillance of cloud-based platforms and with lesser environmental impact, I recommend trying the local model exercise. This exercise introduces you to locally-hosted models that can run privately on your computer without internet access: this allows us to think about how a workflow that uses generative AI doesn't necessarily have to involve sending your personal data to corporations or resource-intensive, cloud-hosted tools. You'll install Ollama, download a local model, and experiment with its reasoning processes to think about how different models can offer dramatically different outputs (particularly around contentious subjects!)

The second option is to continue working with Claude Code, but on non-code applications. This is also an option that doesn't require installing any software, so if you don't have a setup where you have that access, choose this exercise. Both are demoed in the video and explained below.

### Local Models: Installing Ollama and Setting Up Your Local Environment

For this exercise, you'll need to install Ollama, a tool that makes running large language models locally accessible with a simple graphical interface not unlike the browser-based chatbots we've been using:

1. **Download and Install Ollama**: Visit [https://ollama.ai/](https://ollama.ai/) and download the appropriate version for your operating system
2. **Model Selection**: For the demo, I used DeepSeek-R1, but your choice will depend on your system's storage capacity and GPU capabilities. Consider these factors:
   - **Storage**: Models range from 1GB (small models) to 70GB+ (large models)
   - **RAM/GPU**: Larger models require more system memory and benefit from GPU acceleration
   - **Performance**: Smaller models run faster but may have reduced capabilities

Make sure to note which model(s) you experimented with when discussing your outputs - take a look at the overview to understand whose model it is, and how that might impact the results you get.

Once you have Ollama installed and a model downloaded, you'll be able to chat with it. If you are able to load a reasoning model (such as DeepSeek-R1, shown in the screenshot), a partial narrative of the model's "thought" process will be available as well, providing a user-facing summary of the steps taken:

![Ollama GUI](ollama.png)

Notice here how a controversial question (for a model developed in China) is handled differently in the output versus the reasoning workflow. Try different queries and see if you can find other contentious or unexpected points of friction. Think about how this compares to working with the cloud, and whether this approach can start to answer some of the concerns raised in this week's news readings.

### Agentic Applications: Claude Code for Non-Code

Agentic tools are being brought into a wide range of workflows for daily labor in all sorts of institutions, and Claude Code is one of the interfaces that is particularly popular for data-based tasks. Lenny Rachitsky has [curated a list](https://www.lennysnewsletter.com/p/everyone-should-be-using-claude-code) of some of the use cases for Claude Code: a few you might consider trying this week include building presentations; doing social media research; resizing and creating metadata for images; organizing notes for a large project; reformatting citations or papers to a different style; and other document-driven tasks. (More examples are listed in Canvas, but feel free to try something not on the list!)

For this exercise, I recommend continuing to work with Claude Code for the Web as we've been working with it: put the files you want to manipulate in a repository. Set the repository to "private" instead of "public" when creating it to avoid making the files public (this will still go through Anthropic's servers, so pick something to test for that that doesn't include any sensitive data.)

Upload all the relevant files before you use /init to start your Claude Code interations with that repository: this will let Claude Code review what you already have, and result in better subbestions for the process. Use the planning mode we learned next week to iterate through a solution to your task. Execute the task and iterate to see if you can get results that are useful for your non-code goals.

### Discussion

If you selected option one:

Share your experience with local AI models, including which model(s) you chose and why. Reflect on the differences between local and cloud-based AI interactions. What did you observe about the model's reasoning process? How might widespread access to powerful local AI change the landscape of human-computer interaction, creative work, and intellectual labor? Does this answer some of the concerns raised by our readings this semester around privacy, control, and accessibility - or raise others? Connect your observations to our course themes about AI democratization, education, and the future of creative and scholarly work.

If you selected option two:

Share your experience with Claude Code for a non-code task. How does this compare to working with files in our previous exercises through the main chatbot interface? Do you notice any differences in the processing, handling of context, and outcomes? Connect your observations to our readings about programming and control, and think about the implications for software more broadly.

For both, consider the implications for your own field: What could AI agents (whether local or cloud-based) mean for humanities research, creative practice, or educational work?
