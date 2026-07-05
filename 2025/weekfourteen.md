---
layout: page
title: "Week Fourteen: Distant Reading with and for AI"
hide_warning: true
---

## Exercise: Distant Reading with AI

This week, we're going to revisit the distant reading we did earlier this semester, but now we'll be approaching the procedural aspects of the project more directly with agentic AI assistance. We'll revisit collecting, processing, and analyzing a dataset of texts, but now we can work at a much larger scale with access to libraries of existing code. We'll primarily be making use of a few Python libraries:

- [NLTK](https://www.nltk.org/) is a natural language processing toolkit, used for text processing, tokenization, lemmatization, and stopword filtering.
- [vaderSentiment](https://github.com/cjhutto/vaderSentiment) is a library for sentiment analysis, providing compound scores and polarity classification.
- [scikit-learn](https://scikit-learn.org/) is a machine learning library, used here for topic modeling with Latent Dirichlet Allocation.
- [NumPy](https://numpy.org/) is a library for numerical computations and array operations.
- [Bootstrap 5](https://getbootstrap.com/) is a CSS framework for creating responsive web interfaces.
- [D3.js](https://d3js.org/) is a JavaScript library for creating interactive data visualizations.

You might find it helpful to look at documentation of these libraries, or even web scraping and distant reading tutorials in Python, for ideas of things to try. For this exercise, you'll be using [Claude Code Web](https://claude.ai/code) to develop your analysis system through a conversational interface with Claude. 

### Option One: Building Your Distant Reading System with Claude Code Web

Before you start, choose five to ten related texts for your analysis and download them as .txt files from [Project Gutenberg](https://www.gutenberg.org/). We're downloading them individually because Project Gutenberg has [rules about robots](https://www.gutenberg.org/policy/robot_access.html). Consider selecting texts that share a common theme, genre, author, or time period to make your comparative analysis more meaningful.

Once you have your texts:

1. **Create a new GitHub repository** for your distant reading project.

2. **Upload your Project Gutenberg texts** to the repository.

3. **Open Claude Code Web** at [claude.ai/code](https://claude.ai/code) and connect it to your new GitHub repository.

4. **Enter planning mode**  by asking Claude to create a plan, just as you did in previous weeks. Work conversationally with Claude through a similar series of prompts and clarifying questions to develop:
   - A Python analysis script that processes your texts
   - An interactive web interface for visualizing the results

You can reference the [complete development process](https://github.com/AMSUCF/claude-distant-reading/blob/main/PROCESS.md) used in the demo to see one possible plan and resulting outputs, including the analytical methods (text processing, sentiment analysis, topic modeling, style metrics) and visualization approaches (word clouds, sentiment charts, comparative metrics).

### Option Two: Working Locally with Claude Code for Desktop

In this week's demo, I will show you how to work locally with [Claude Code for your desktop](https://docs.claude.com/en/docs/claude-code/installation) to accomplish this same task. Installing Claude Code is not required, but it is recommended for students interested in exploring computational work or the type of subagents described in some of this week's readings. There will be an option to continue with subagents in next week's bonus exercise.

### Discussion

As you work through the analysis, consider how the relationship with text in distant reading connects to the other ways we've been working with AI (both in text and code) throughout the semester. Try to push for visualizations that are meaningful to you. What did the computational approach reveal about your chosen novels? How did working with an AI agent change your process compared to our earlier distant reading experiments? After these multiple explorations with Claude Code, how do you feel about the use of agents in the larger context of labor - particularly given the tensions reflected in this week's readings?

