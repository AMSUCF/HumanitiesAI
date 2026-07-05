---
layout: page
title: "Week Eleven: Puppet Masters — Agentic Code"
hide_warning: true
canvas:
  module: "Week Eleven: Puppet Masters — Agentic Code"
  week_start: 2026-11-02
  due: 2026-11-08
  points: 6
  discussion: true
  extra_credit: false
  unit: puppetmasters
---

<span class="unit-badge unit-badge--puppetmasters">Puppet Masters</span>

> A phenomenon in which isolated actors, with no coordination and no original to imitate, produce behavior that looks like a single, unified pattern — a copycat effect with no first copy. — after *Ghost in the Shell: Stand Alone Complex* (2002)

Stand Alone Complex names something stranger than a conspiracy: coordinated-looking action with nobody actually coordinating it, and no originator you can point to and say "it started there." That's a useful, slightly unsettling frame for what an agentic coding tool does when you set it loose. Simon Willison's ["Designing agentic loops"](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) describes giving an agent a goal, a set of tools, and permission to plan, act, and check its own results across many steps without a human approving each one — the opposite of typing every line yourself, and also the opposite of a single click that does one thing. What comes out the other end is a real sequence of decisions that produced a working (or broken) result, but no one moment where you can say "I did that." This week's exercise puts you inside that loop directly: you'll hand Claude Code an open-ended brief and watch it plan, build, and iterate on a public website of your own design.

## Exercise: Agentic Code

Building on the experience you've gotten with generative code, we're now moving to use agentic AI systems that can plan, execute, and iterate on complex coding projects with your own larger project in mind. You'll be building more experience working with Claude Code for the web, which has full access to the files of a GitHub repository and can make changes directly — and this time, you can add content such as images and video for Claude Code to integrate. For this exercise, you can build any type of website — consider building a simple web game, educational resource, or something related to your own work.

### Setting Up Your Project

The mechanics here are the same as last week — [Week Ten](weekten.md) has the full walkthrough for connecting Claude Code for the web to GitHub, including how to generate a fine-grained personal access token, so refer back to it for any step you need in detail. For this week's project:

1. **Create a new GitHub repository** at [github.com](https://github.com/new) for this project (a fresh one, separate from last week's recommender)
   - Give it a descriptive name for your project
   - Make it public (required for GitHub Pages)
   - Initialize with a README if you'd like

2. **Open Claude Code for the web** at [code.claude.ai](https://code.claude.ai)
   - Select your new repository from the list (this is where your personal access token from Week Ten comes in — but since that token was scoped to "Only select repositories," you'll need to either edit its repository list on GitHub to add this new repo, or generate a fresh fine-grained token scoped to it, following Week Ten's steps)
   - In the big box, type `/init`
   - Start the project — this initializes Claude Code's tracking and project structure (more on [slash commands](https://docs.claude.com/en/docs/claude-code/slash-commands) if you're curious)

### Building Your Public-Facing Website

Envision a public-facing website that could serve an educational purpose, function as a personal portfolio, present a humanities project, or otherwise relate to your own work. Be ambitious — the point here is not to succeed at everything you try, the goal is to better understand what agentic systems are currently capable of producing (and where they fail). Claude Code will commit changes to your repository in a separate branch, so you can always revert if the agent moves in a direction you don't want.

**Step 1: Request a Project Plan**

Start by asking Claude Code to develop a project plan for your vision. Start your prompt with "Enter plan mode. Do not exit plan mode until I confirm the plan is ready. Ask clarifying questions until you understand the plan." then follow it with your initial description. For example:
- "I want to create an educational website about [your field of interest] that includes interactive demonstrations, animations, and user engagement features. Please create a project plan and initial file structure."
- "Help me plan a personal portfolio site that showcases my AI experiments with dynamic, interactive elements that demonstrate the capabilities of different AI tools."
- "Design a public humanities project website that makes [specific topic] accessible through interactive storytelling and multimedia presentations."

Claude Code should ask a set of questions. When you feel the project is sufficiently described, confirm the plan and let it proceed.

**Step 2: Develop the Core Website**

Work with Claude Code to build out your site iteratively. Use specific details, but don't worry too much about final content — think of this as a design exercise primarily. You might try asking for specific libraries and technologies, particularly if there are things you know or are interested in — for instance, you might ask for a D3.js data visualization, or a P5.js animation. Emphasize that the site is for deployment on GitHub Pages and should stick to native web technologies (HTML, CSS, JavaScript).

**Step 3: Incorporate Visual Materials**

Upload images to your GitHub repository (you can do this directly on GitHub.com by navigating to your repo and clicking "Add file" > "Upload files"). Then ask Claude Code to incorporate them into your design:
- "I've uploaded an image called [filename]. Please incorporate it into the homepage with appropriate styling."
- "Use the images I've uploaded to create a gallery section with lightbox functionality."
- "Create a header banner using [image file] with an overlay effect."

**Step 4: Test and Deploy**

Just like in Week Ten, deploy your site using GitHub Pages:
- Go to your repository Settings on GitHub.com
- Navigate to "Pages" in the left sidebar
- Under "Source," select your main branch
- Save and wait a few minutes for your site to deploy
- Your site will be available at `https://[your-username].github.io/[repository-name]`

Claude Code will typically commit its work to a branch and open a pull request rather than pushing straight to `main` — review the pull request on GitHub.com and merge it once you're happy with the result. Test your site, note what works and what needs refinement, and continue iterating with Claude Code to improve it.

The design of this entire course site is an example of this type of workflow — all the content is mine, but the layouts, header animation on the main page, and interactive features were all generated using agentic AI assistance (Copilot and Claude Code).

### Discussion

Share your deployed website link along with reflection on the agentic development process. How did you feel about your level of control? Where were the points of frustration? Would you make use of this for prototyping or managing digital projects in the future? Connect your experience to Meredith Martin's ["Command Lines for the Humanities"](https://www.cambridge.org/core/journals/pmla/article/command-lines-for-the-humanities/097F959E6971063D05B085E698354BA2) and to Willison's account of designing agentic loops — cite at least one of our readings.

Finally, connect this back to the epigraph. A Stand Alone Complex is coordinated-looking behavior with no single originator — an effect that emerges from many independent steps rather than one authored decision. When you put Claude Code into plan mode and let it work across many turns — planning, writing files, testing, committing — who authored the site that resulted: you, for the initial prompt and the plan you approved; Claude, for every individual file and commit; or neither, in the way a Stand Alone Complex has no first instigator? Does "agentic" feel like the right word for what happened, or does it overstate how much the system was actually deciding on its own?
