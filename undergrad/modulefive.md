---
layout: undergrad-page
title: "Module Five: Archives and Collections"
canvas:
  module: "Module Five: Archives and Collections"
  week_start: 2027-03-08
  due: 2027-03-28
  points: 10
  discussion: true
  extra_credit: false
  unit: images
---

<span class="unit-badge unit-badge--images">Images</span>

**Note on timing:** this module spans Spring Break (March 15 - 21). Nothing is due over the break, and the module closes on Sunday, March 28. Plan to do the readings before the break and the exercise after, or get ahead if you prefer.

Last module we made new images. This module turns to images that already exist: the photographs, prints, posters, and maps held by libraries, archives, and museums. Digitizing these collections has been one of the central projects of digital humanities. Once those images are online, though, they can be searched, described, sorted, and (increasingly) used to train AI.

Kate Crawford and Trevor Paglen's "Excavating AI" digs into the training sets behind image recognition systems and shows how the *labels* attached to images (what a picture "is," or what kind of person appears in it) carry assumptions and sometimes outright harm. "The Santa Barbara Statement on Collections as Data," written by librarians and archivists, makes the case for opening cultural collections to computational use, while insisting that this be done responsibly, with attention to the people and communities represented. Read them together: one shows what can go wrong when images become data, and the other describes what doing it well might look like.

## Tutorial: Describing the Archive

Archives depend on **metadata**: the descriptions, dates, subjects, and other information attached to each item that make it possible to find. Writing good metadata, and good **alt text** for people using screen readers, is slow, skilled work, and it's one of the tasks institutions are now asking AI to help with. In this exercise, you'll test how well an AI assistant does it.

### Step 1: Build a Small Collection

Choose 5-8 related images from one of these free, public-domain sources:

- [Library of Congress: Free to Use and Reuse](https://www.loc.gov/free-to-use/), which is organized into themed sets (for example, Baseball Cards, Bicycles, or Cats)
- [Smithsonian Open Access](https://www.si.edu/openaccess)
- [Internet Archive: Images](https://archive.org/details/image)

Choose images that share a theme and include at least one that's complicated: a crowded scene, a document with handwriting, an image with text in another language, or something whose meaning depends on historical context. For each image, download it and **save the item's catalog record** (the title, date, description, and subjects listed on its page).

### Step 2: Ask the AI to Describe, Without the Record

Upload your images to ChatGPT, Claude, Gemini, or Copilot (one at a time, or a few at a time if your free tier limits uploads). **Don't** give it the catalog information. For each image, ask:

> Describe this image in detail. Then write alt text for it (under 150 characters), and suggest a title, an approximate date, and five subject keywords as if you were cataloging it for a library.

### Step 3: Compare with the Catalog

Put the AI's description next to the archive's catalog record. For each image, note:

- What the AI got right
- What it got wrong, especially dates, places, and people's identities
- What it *assumed* or invented that isn't visible in the image
- What the catalog record knows that no one could tell from the image alone

### Step 4: Ask It to Sort

Finally, upload your whole set (or describe it, if uploading is limited) and ask the AI to **group the images into categories and explain its groupings**. Compare its categories with the way the archive organized them. Keep Crawford and Paglen's point about labels in mind: what does the AI's way of classifying reveal?

### Discussion

Share your collection (with links to each item's catalog page), the AI's descriptions for at least three images, and your comparison notes. A table works well for this. Then reflect:

- Where was the AI most and least reliable as a cataloger? Would you trust its alt text if you depended on a screen reader?
- Crawford and Paglen argue that labeling images is never neutral. Did you see that in your AI's descriptions or categories? Give a specific example.
- The Santa Barbara Statement asks institutions to make collections usable as data *responsibly*. If a library used AI to describe your collection, what would you want it to do (or not do)?

Make sure to reference both of the module's readings. Your post is worth 8 points; then reply to two classmates (1 point per reply) for full credit.
