---
layout: page
title: "Week Thirteen: Local Models"
hide_warning: true
---

## Exercise: Local Models

Moving beyond cloud-based AI systems, this week we'll explore running AI models directly on your local hardware. This exercise introduces you to locally-hosted models that can run privately on your computer without internet access: this allows us to think about how a workflow that uses generative AI doesn't necessarily have to involve sending your personal data to corporations or resource-intensive, cloud-hosted tools. You'll install Ollama, download a local model, and experiment with its reasoning processes to think about how different models can offer dramatically different outputs (particularly around contentious subjects!)

### Installing Ollama and Setting Up Your Local Environment

For this exercise, you'll need to install Ollama, a tool that makes running large language models locally accessible with a simple graphical interface not unlike the browser-based chatbots we've been using:

1. **Download and Install Ollama**: Visit [https://ollama.ai/](https://ollama.ai/) and download the appropriate version for your operating system
2. **Model Selection**: For the demo, I used DeepSeek-R1, but your choice will depend on your system's storage capacity and GPU capabilities. Consider these factors:
   - **Storage**: Models range from 1GB (small models) to 70GB+ (large models)
   - **RAM/GPU**: Larger models require more system memory and benefit from GPU acceleration
   - **Performance**: Smaller models run faster but may have reduced capabilities

Make sure to note which model(s) you experimented with when discussing your outputs - take a look at the overview to understand whose model it is, and how that might impact the results you get.

Once you have Ollama installed and a model downloaded, you'll be able to chat with it. If you are able to load a reasoning model (such as DeepSeek-R1, shown in the screenshot), a partial narrative of the model's "thought" process will be available as well, providing a user-facing summary of the steps taken:

![Ollama GUI](ollama.png)

Notice here how a controversial question (for a model developed in China) is handled differently in the output versus the reasoning workflow. Try different queries and see if you can find other contentious or unexpected points of friction.

### Discussion

Share your experience with local AI models, including which model(s) you chose and why. Reflect on the differences between local and cloud-based AI interactions. What did you observe about the model's reasoning process? How might widespread access to powerful local AI change the landscape of human-computer interaction, creative work, and intellectual labor? Does this answer some of the concerns raised by our readings this semester around privacy, control, and accessibility - or raise others? Connect your observations to our course themes about AI democratization, education, and the future of creative and scholarly work.

Consider the implications for your own field: What could local, private AI agents mean for humanities research, creative practice, or educational work?
