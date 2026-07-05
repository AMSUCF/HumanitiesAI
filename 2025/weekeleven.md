---
layout: page
title: "Week Eleven: Deploying to GitHub Pages"
hide_warning: true
---

## Exercise: Deploying to GitHub Pages

This week, you'll be either building a new version of the recommendation system, or upgrading your previous attempt developed in Week Nine. Instead of keeping it in Claude Artifacts, we're going to use the newly-launched Claude Code web interface to deploy it to GitHub Pages so that others can access and interact with it on the web directly. This process will introduce you to version control with Git, web hosting, and the development workflow that many programmers and scholars use for sharing their work online. This will set up our tools for the next stage so you have a chance to get familiar with the interfaces before we try something more complex.

Note that Claude Code for Web launched last week, so this exercise has been completely redesigned. If you looked at the previous version, you might have installed other software - 

### Setting Up Your Development Environment

Before we can deploy your recommendation system, you'll need to set up the necessary tools for web development and version control. This part might be painful if you haven't worked with these environments before, but it's going to give you much more control of the code objects we're generating and playing with over the next few weeks.

#### Step 1: Get a GitHub Education Account

As a student, you can access GitHub's education benefits, which include free access to GitHub Pro and other developer tools I'll demonstrate later:

1. **Visit GitHub Education**: Go to [education.github.com](https://education.github.com/) and click "Get benefits"
2. **Sign up or sign in**: Create a GitHub account if you don't have one, or sign in to your existing account
3. **Verify your student status**: Upload documentation proving your student status (student ID, transcript, or enrollment verification)
4. **Wait for approval**: GitHub will review your application, which usually takes a few days - it's OK, you don't need it for this first project!
5. **Access your benefits**: Once approved, you'll have access to GitHub Copilot, which is an option to try out for the next exercises - don't worry about having access now

#### Step 2: Create a GitHub Repository

1. **Create a new repository**: Open GitHub.com, log in, and click the green "New Repository" button.
2. **Fill in repository details**:
   - Repository name: Choose something descriptive like "sci-fi-recommender" or "book-recommendation-system"
   - Initialize with README: Check this box
   - Ignore the other options for now
3. **Create the repository**: Click the green "Create Repository" button

#### Step 3: Launch Claude Code for the web

1. **Open Claude Code**:
   - You'll find Claude Code on your Claude sidebar: select it. You'll need to authorize the connection to your GitHub account - use the account you made for class rather than any personal or professional account you might otherwise maintain.
2. **Select the repository you just made**
3. **Enter a prompt**: 
   - I recommend working through a modified version of our previous process: start by making the JSON file, then ask for the HTML, JavaScript, and CSS files for the interface. This will allow you to construct a full site with smaller files that are easier to iterate on than our previous project.
   - You'll need to accept "Yes" to installing the GitHub application to continue working with Claude Code
   - I recommend selecting "Enable notifications" - this way, you can give Claude a task and go work on something else.

#### Step 4: Enable GitHub Pages

1. **Go to your repository on GitHub.com**: Go back to GitHub, and select the new repository you creted earlier. You'll see a branch Claude created waiting for approval to pull - this will bring in the changes to your main project. Accept the changes.
2. **Access Settings**: Click on the "Settings" tab in your repository
3. **Find Pages section**: Scroll down to the "Pages" section in the left sidebar
4. **Configure source**: 
   - Source: Select "Deploy from a branch"
   - Branch: Select "main" 
   - Folder: Select "/ (root)"
5. **Save settings**: Click "Save"
6. **Get your URL**: In the side settings on your repository, select "Use GitHub Pages site" to get the URL of your page. Load that page in another tab to test it. 

If you need changes, go back to Claude Code and request them. Iterate through, merging the changes into your main branch and testing the live site.

### Discussion

Share the GitHub Pages URL of your deployed recommendation system (the GitHub pages link) along with any questions or challenges you ran into along the way. Speculate: how might these interfaces change in the near future given what you've experienced and read, particularly in *Code to Joy*?
