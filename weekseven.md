---
layout: page
title: "Week Seven: Shells — Video and Realism"
hide_warning: true
canvas:
  module: "Week Seven: Shells — Video and Realism"
  week_start: 2026-10-05
  due: 2026-10-11
  points: 6
  discussion: true
  extra_credit: false
  unit: shells
---

<span class="unit-badge unit-badge--shells">Shells</span>

> For an instant the light bends wrong around her — a seam in the air where a woman should be standing — and then even the seam is gone, street traffic and pedestrians passing through the space she just occupied as though it had only ever been pavement and a doorway. — after [*Ghost in the Shell* (1995)](https://en.wikipedia.org/wiki/Ghost_in_the_Shell_(1995_film))

Thermoptic camouflage doesn't paint a false image over the Major; it erases the true one, letting whatever's behind her show through until she simply isn't there to see. Generative video is doing something adjacent, at a much larger and stranger scale: it isn't erasing anything, but it is manufacturing a moving image with no camera, no set, and no event behind it — footage of nothing, increasingly hard to tell apart from footage of something that happened. This week we generate some of that footage ourselves, then turn a critical eye on a field that just watched one of its flagship tools disappear in under a year.

## Tutorial: Video and Realism

Generative AI video is still a young technology, but it has already reshaped parts of the industry it's built to imitate — and it's already claimed a casualty. Relatively few models offer full image-to-video or text-to-video generation directly to consumers, and the roster of "current" tools turns over fast enough that any list of them is a snapshot, not a map. We'll run a small experiment with generative video this week, then look at the larger claims — and one very public retraction of those claims — coming out of the companies building in this space.

### Case study: the Sora arc

In September 2025, OpenAI launched Sora 2 as "Sora 2 is here" — a flagship text-to-video model with its own social app, pitched as a major leap in realism and a glimpse of consumer video generation's future. Six months later, OpenAI announced the shutdown: the Sora app and web experience closed on April 26, 2026, and the API is scheduled to end on September 24, 2026. Reporting on the shutdown cited compute costs of roughly $1 million a day as a driver of the decision. (Historical artifact: OpenAI's original launch post, [openai.com/index/sora-2](https://openai.com/index/sora-2/); verified timeline: [Wikipedia, "Sora (text-to-video model)"](https://en.wikipedia.org/wiki/Sora_(text-to-video_model)).)

Read that arc against this week's *The AI Con* chapter, "Do You Believe in Hope After Hype?" A tool can be genuinely impressive — Sora's outputs were, by most accounts, striking — and still not survive contact with its own operating costs and a market that decided a social video app wasn't the product it needed. Hold that tension as you work through the exercise below: **Sora is discontinued and is not a tool for this assignment**, but the six months of hype that surrounded its launch are exactly the kind of claim this course asks you to interrogate.

### Image to Video Exploration

For this exercise, try either working from static images or from specific text descriptions. For instance, this sample was created using Google's **Veo 3.1** — currently Google DeepMind's released video model (native audio, up to 1080p/4K, prompt-driven scene extension; no Veo 4 has been officially announced as of this writing) — with the prompt: "a retrofuturist alien spaceship lands on memory mall at the University of Central Florida":

<video src="images/Veo3.mp4" controls></video>

Compare this to a second iteration of the same prompt (using the same model on the same day), but with additional information from this [Wikimedia photo](https://commons.wikimedia.org/wiki/File:UCF_Memory_Mall_(30395273585).jpg) of the UCF memory mall:

<video src="images/VeoWithReference.mp4" controls></video>

For contrast, here's a 2025 archival sample generated from the exact same prompt and source image using Sora — the tool discussed in the case study above, since discontinued. It's kept here as a documented artifact of the hype-cycle moment, not as a tool recommendation:

<video src="images/Sora.mp4" controls></video>

For this exercise, you can try Google's current student offer for [Google AI Pro](https://support.google.com/gemini/answer/16417758): a one-month free trial, US-only, requiring SheerID student verification (with a discounted student rate otherwise) — a considerably shorter offer than the free year Google ran in 2025, so verify the current terms before you count on it. If you don't have a Google account, don't qualify for the trial, or want a wider comparison, this [list of free image-to-video tools](https://www.whytryai.com/p/free-ai-image-to-video-tools-tested) (tested and updated as of February 2026) and the [Tom's Guide roundup of AI video generators](https://www.tomsguide.com/features/5-best-ai-video-generators-tested-and-compared) are both still live — treat the specific rankings as dated even where the tool names are current, and verify anything you rely on. Generate 2–3 short videos to share with your peers, using Veo 3.1, one of the free tools listed, or a range of both. Do not use Sora — it no longer exists as a working tool.

### Critiquing Generated Video

Now that you've explored the tools within some limitations, choose a generated video to analyze and critique, with particular attention to the tensions of perception, vision, and labor drawn out through this week's readings. Keep in mind the concerns raised in Brett Halperin's talk, ["Hollywood Film Workers Strike Against AI: Understanding Algorithmic Resistance to Generative Cinematography"](https://stars.library.ucf.edu/elo2024/algorithmsandimaginaries/schedule/3/), as well as this week's reading from Tech Policy @ Duke Sanford, ["AI & the Film Industry: Production"](https://techpolicy.sanford.duke.edu/blog/ai-the-film-industry-production/), which lays out the production-labor stakes — deepfaked performers, displaced crew roles — behind the tools you've just been experimenting with.

Contextualize the generation you've done in these larger debates: what does the video you've generated suggest about the future of misinformation? Environmental and disaster communication? Conspiracy theories? Revenge pornography? How are people in your field using, or refusing to use, these tools? If this is your first time using them, were you surprised by the results — and does the Sora case study change how much you trust the next tool's launch-day claims?

### Discussion

Your discussion post should combine your knowledge (and samples) from your own exploration of generative video with your observations about the form, drawing on the example you've selected for analysis. Make sure to include a link (or attached file) for the video you've selected, as well as relevant context, so we can build a shared sense of the state of the field from the range of works critiqued.

If you're looking for more material to draw on: Science SARU's new *The Ghost in the Shell* series (dir. Mokochan, script EnJoe Toh) premieres July 7, 2026 on Prime Video and airs new episodes through the semester — fair game as supplemental viewing and discussion material if you're following along.

Finally, connect this back to the epigraph. Thermoptic camouflage hides the Major by erasing her from the frame, in plain sight, with nothing added; the Sora arc suggests generative video works differently — it doesn't erase anything, it adds a plausible frame where there was no event at all, and for six months a lot of people found that convincing before the tool itself vanished. Is synthetic video "hiding in plain sight" the way the Major does, or is its bluff easier to call than thermoptic camouflage's? And what does a hype cycle that ran from launch to shutdown in under seven months suggest about the gap between what these tools are claimed to do and what they can actually sustain?
