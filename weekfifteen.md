---
layout: page
title: "Week Fifteen: Custom Bots"
hide_warning: true
---

## Exercise: Custom Bots

As we're approaching the end of the semester, this exercise is optional: it is a complicated workflow, and can be frustrating to get to work, but I hope you'll try it as the results can be a lot of fun and give you control over a model at a next level compared with our previous projects. This workflow also introduces [Hugging Face](https://huggingface.co/), a platform that hosts machine learning models and datasets, making it easier to access and fine-tune pre-trained language models for custom applications. If you want to, you can even push your model to the cloud.

Recall the Eliza Bot we "spoke" with at the beginning of the class: Eliza's code uses the same fundamental structures as you've been reading about over the last few weeks in *Code to Joy.* Her set of replies is thus fundamentally very limited to what is pre-scripted. We could easily build our own version of Eliza at this stage, but instead of working with an "old-school" bot, we're going to add on by using the skills you've gained with scraping and preparing datasets to fine-tune a story generation bot that remixes public domain material.

### Hugging Face

For this exercise, you'll use the same collection of novels you selected for Week Fourteen's distant reading exercise. Having already worked with these texts computationally, you now have a sense of their patterns and characteristics, which makes them ideal candidates for fine-tuning a custom model. Before you begin, you'll need to create a free Hugging Face account and get an access token:

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

This token allows the notebook to access Hugging Face's model hub and optionally upload your fine-tuned model to share with others.

### Working with the Notebooks

This exercise uses two separate notebooks for the complete workflow:

**Step 1 - Dataset Building**: [Build Training Dataset](https://colab.research.google.com/drive/1A992B26TZHyNbmeM2WCNWXj6gOIIg6oH?usp=sharing)

This first notebook will help you:
- Process your Project Gutenberg texts from Week Fourteen
- Clean and format the text data for training
- Create a structured dataset suitable for fine-tuning
- Export the prepared dataset for use in training

For reference, here's an example of a completed dataset based on Oz books: [Oz Fragments Dataset](https://huggingface.co/datasets/anasalter/oz-fragments). This shows you what your final processed dataset might look like when uploaded to Hugging Face.

**Step 2 - Model Training**: [Fine-Tune Custom Bot](https://colab.research.google.com/drive/1suRh2g6x78X-shCaaF3Im2ktoVSRxvbt?usp=sharing)

This second notebook will guide you through:
- Loading your prepared dataset
- Setting up Hugging Face's transformers and Unsloth for efficient fine-tuning
- Fine-tuning a language model on your literary collection
- Testing your custom-trained model to see how it generates text in the style of your chosen works

For reference, here's an example of a completed fine-tuned model based on the Oz dataset: [Oz Completion Model](https://huggingface.co/anasalter/oz-completion-model). This model is ready for use in Ollama and shows you what your final trained model might look like when completed.

Work through both notebooks in order - the dataset building notebook prepares the foundation, and the training notebook creates your custom bot. The process builds directly on your distant reading work - instead of analyzing patterns in the texts, you're now teaching a model to generate new text that follows those same patterns. 

### Reflecting on Chat

Compare this experience to the bot interactions we had at the start of the semester: how has your understanding of, and expectation of, these bots changed? Where do the limitations of the dataset and the model come out, and how can you understand that through the lens of the readings and experiments we've done across the semester?

### Extra Credit Reminders

This exercise is fully extra credit: you can choose to engage part or all of the prompt depending on your goals and current grade. 