---
layout: page
title: "Week Eleven: Deploying to GitHub Pages"
hide_warning: true
---

## Exercise: Deploying to GitHub Pages

This week, you'll be taking the recommendation system you built in Week Nine and deploying it to GitHub Pages so that others can access and interact with it on the web. This process will introduce you to version control with Git, web hosting, and the development workflow that many programmers and digital humanists use for sharing their work online. This will set up our tools for the next stage so you have a chance to get familiar with the interfaces before we try something more complex.

### Setting Up Your Development Environment

Before we can deploy your recommendation system, you'll need to set up the necessary tools for web development and version control. This part might be painful if you haven't worked with these environments before, but it's going to give you much more control of the code objects we're generating and playing with over the next few weeks.

#### Step 1: Get a GitHub Education Account

As a student, you can access GitHub's education benefits, which include free access to GitHub Pro and other developer tools:

1. **Visit GitHub Education**: Go to [education.github.com](https://education.github.com/) and click "Get benefits"
2. **Sign up or sign in**: Create a GitHub account if you don't have one, or sign in to your existing account
3. **Verify your student status**: Upload documentation proving your student status (student ID, transcript, or enrollment verification)
4. **Wait for approval**: GitHub will review your application, which usually takes a few days - it's OK, you don't need it for this first project!
5. **Access your benefits**: Once approved, you'll have access to GitHub Copilot, which we'll be using for the next exercises

#### Step 2: Install Visual Studio Code

Visual Studio Code is a free, widely-used code editor that will make it easier to manage your project files:

1. **Download VS Code**: Visit [code.visualstudio.com](https://code.visualstudio.com/) and download the version for your operating system
2. **Install the application**: Follow the installation instructions for your platform
3. **Install useful extensions**: Once VS Code is running, consider installing these helpful extensions:
   - Live Server (for local testing)
   - GitHub Pull Requests and Issues
   - HTML CSS Support

#### Step 3: Install GitHub Desktop

GitHub Desktop provides a user-friendly interface for managing Git repositories - that is to say, it helps us store and keep track of project versions, and provides a Dropbox-esque place to store things locally and in the cloud:

1. **Download GitHub Desktop**: Go to [desktop.github.com](https://desktop.github.com/) and download the application
2. **Install and sign in**: Install the application and sign in with your GitHub account
3. **Configure Git**: GitHub Desktop will help you configure Git with your name and email

#### Step 4: Get Your Simple Recommendation System Code

1. **Access your Week Nine artifact**: Go back to your Claude conversation from Week Nine and find your recommendation system
2. **Find the HTML code**: Click on the artifact and switch to code view. 

#### Step 5: Create a GitHub Repository

1. **Create a new repository**: Open GitHub Desktop and click "File > New Repository"
2. **Fill in repository details**:
   - Repository name: Choose something descriptive like "sci-fi-recommender" or "book-recommendation-system"
   - Description: Brief description of your project
   - Local path: Choose where to save the project on your computer
   - Initialize with README: Check this box
3. **Create the repository**: Click "Create Repository"

#### Step 6: Set Up Your Project Files

1. **Open in VS Code**: In GitHub Desktop, click "Open in Visual Studio Code"
2. **Create index.html**: In VS Code, create a new file called `index.html` in your repository folder
3. **Paste your code**: Copy your Claude artifact code into the `index.html` file
4. **Create supporting files**: If your system uses separate JSON, CSS or JavaScript files, create those as well - by default, Claude usually puts everytihng into one HTML file
5. **Test locally**: If you installed the Live Server extension, right-click on `index.html` and select "Open with Live Server" to test your site locally

#### Step 7: Commit and Push Your Changes

1. **Review changes**: Go back to GitHub Desktop, and you should see your new files listed
2. **Write a commit message**: In the commit message field, write something descriptive like "Add recommendation system from Week Nine"
3. **Commit to main**: Click "Commit to main"
4. **Publish repository**: Click "Publish repository" to upload it to GitHub.com
5. **Make it public**: Make sure to uncheck "Keep this code private" so others can access your site

#### Step 8: Enable GitHub Pages

1. **Go to your repository on GitHub.com**: Click "View on GitHub" in GitHub Desktop
2. **Access Settings**: Click on the "Settings" tab in your repository
3. **Find Pages section**: Scroll down to the "Pages" section in the left sidebar
4. **Configure source**: 
   - Source: Select "Deploy from a branch"
   - Branch: Select "main" 
   - Folder: Select "/ (root)"
5. **Save settings**: Click "Save"
6. **Get your URL**: In the side settings on your repository, select "Use GitHub Pages site" to get the URL of your page.

Once your site is live, test it by loading 

### Discussion

Share the GitHub Pages URL of your deployed recommendation system (the GitHub pages link) along with any questions or challenges you ran into along the way. Speculate: how might these interfaces change in the near future given what you've experienced and read, particularly in *Code to Joy*?
