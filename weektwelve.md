---
layout: page
title: "Week Twelve: Agentic Code"
hide_warning: true
---

## Exercise: Agentic Code

Building on the experience you've gotten with generative code, we're now moving to use agentic AI systems that can plan, execute, and iterate on complex coding projects with your own larger project in mind. You'll be building more experience working with Claude Code for the web, which has full access to the files of a GitHub repository and can make changes directly - and this time, you can add content such as images and video for Claude Code to integrate. For this exercise, you can build any type of website - consider building a simple web game, educational resource, or something related to your own work.

### Setting Up Your Project

Start by creating a new repository on GitHub.com (just like you did in Week Eleven):

1. **Create a new GitHub repository** at [github.com](https://github.com/new)
   - Give it a descriptive name for your project
   - Make it public (required for GitHub Pages)
   - Initialize with a README if you'd like
   - No need to add .gitignore or license yet

2. **Open Claude Code for the web** at [code.claude.ai](https://code.claude.ai)
   - Open Claude Code through the sidebar
   - Select your new repository from the list
   - In the big box, type /init
   - Start the project - this will initialize Claude Code's tracking and project structure (we'll do more with [slash commands](https://docs.claude.com/en/docs/claude-code/slash-commands) later, but here's a guide if you are interested!)

### Building Your Public-Facing Website

Envision a public-facing website that could serve an educational purpose, function as a personal portfolio, present a humanities project, or otherwise related to your own work. Be ambitious - the point here is not to succeed at everything you try, the goal is to better understand what agentic systems are currently capable of producing (and where it fails). Claude Code will commit changes to your repository in a separate branch, so you can always revert if the agent moves in a direction you don't want.

**Step 1: Request a Project Plan**

Start by asking Claude Code to develop a project plan for your vision. Start your prompt with "Enter plan mode. Do not exit plan mode until I confirm the plan is ready. Ask clarifying questions until you understand the plan." then follow it with your initial description. For example:
- "I want to create an educational website about [your field of interest] that includes interactive demonstrations, animations, and user engagement features. Please create a project plan and initial file structure."
- "Help me plan a personal portfolio site that showcases my AI experiments with dynamic, interactive elements that demonstrate the capabilities of different AI tools."
- "Design a public humanities project website that makes [specific topic] accessible through interactive storytelling and multimedia presentations."

Claude Code should ask a set of questions. When you feel the project is sufficiently described, reply "

**Step 2: Develop the Core Website**

Work with Claude Code to build out your site iteratively. Use specific details, but don't worry too much about final content - think of this as a design exercise primarily. You might try asking for specific libraries and technologies, particularly if there are things you know or are interested in - for instance, you might ask for a D3.js data visualization, or a P5.js animation. Emphasize that the site is for deployment on GitHub Pages and should stick to native web technologies (HTML, CSS, Javascript).

**Step 3: Incorporate Visual Materials**

Upload images to your GitHub repository (you can do this directly on GitHub.com by navigating to your repo and clicking "Add file" > "Upload files"). Then ask Claude Code to incorporate them into your design:
- "I've uploaded an image called [filename]. Please incorporate it into the homepage with appropriate styling."
- "Use the images I've uploaded to create a gallery section with lightbox functionality."
- "Create a header banner using [image file] with an overlay effect."

**Step 4: Test and Deploy**

Just like in Week Eleven, you'll deploy your site using GitHub Pages:
- Go to your repository Settings on GitHub.com
- Navigate to "Pages" in the left sidebar
- Under "Source," select your main branch
- Save and wait a few minutes for your site to deploy
- Your site will be available at `https://[your-username].github.io/[repository-name]`

Test your site, note what works and what needs refinement, and continue iterating with Claude Code to improve it.

The design of this entire course site is an example of this type of workflow - all the content is mine, but the layouts, header animation on the main page, and interactive features were all generated using agentic AI assistance (Copilot and Claude Code). I also used Claude Code to do the first pass of updating this text to describe the new web interface instead of the previous tools we were going to use (Github Copilot) - it did OK, though I had to rewrite several steps, which you can see if you look at the repository history.

### Discussion

Share your deployed website link along with reflection on the agentic development process. How did you feel about your level of control? Where were the points of frustration? Would you make use of this for prototyping or managing digital projects in the future? Connect your experience to our broader course themes about AI tools, creativity, and the changing landscape of human-computer collaboration in creative and intellectual work. Cite at least one of our readings.
