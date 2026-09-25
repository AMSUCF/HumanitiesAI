---
layout: page
title: "Week Seven: Shells — Videos and Animation"
hide_warning: true
canvas:
  module: "Week Seven: Shells — Videos and Animation"
  week_start: 2026-10-05
  due: 2026-10-11
  points: 6
  discussion: true
  extra_credit: false
  unit: shells
---

<span class="unit-badge unit-badge--shells">Shells</span>

> “What we see now is like a dim image in a mirror.” — the Puppet Master, echoing 1 Corinthians, [*Ghost in the Shell* (1995) script](https://scrapsfromtheloft.com/movies/ghost-in-the-shell-1995-transcript/)

The film borrows that line from scripture for a world where seeing is never direct. Generative video makes the mirror stranger still: it manufactures a moving image with no camera, no set, and no event behind it — footage of nothing, increasingly hard to tell apart from footage of something that happened. This week we make some moving images ourselves — first by having a model write an animation in code, then by comparing it to footage a video model generates outright — and turn a critical eye on a field that just watched one of its flagship tools disappear in under a year.

## Tutorial: Videos and Animation

Generative AI video is still a young technology, but it has already reshaped parts of the industry it's built to imitate — and it's already claimed a casualty. Relatively few models offer full image-to-video or text-to-video generation directly to consumers, and the roster of "current" tools turns over fast enough that any list of them is a snapshot, not a map. This week you'll choose between animating in code and generating video, then look at the larger claims — and one very public retraction of those claims — coming out of the companies building in this space.

### Case study: the Sora arc

In September 2025, OpenAI launched Sora 2 as "Sora 2 is here" — a flagship text-to-video model with its own social app, pitched as a major leap in realism and a glimpse of consumer video generation's future. Six months later, OpenAI announced the shutdown: the Sora app and web experience closed on April 26, 2026, and the API is scheduled to end on September 24, 2026. Reporting on the shutdown cited compute costs of roughly $1 million a day as a driver of the decision. (Historical artifact: OpenAI's original launch post, [openai.com/index/sora-2](https://openai.com/index/sora-2/); verified timeline: [Wikipedia, "Sora (text-to-video model)"](https://en.wikipedia.org/wiki/Sora_(text-to-video_model)).)

Read that arc against this week's *The AI Con* chapter, "Do You Believe in Hope After Hype?" A tool can be genuinely impressive — Sora's outputs were, by most accounts, striking — and still not survive contact with its own operating costs and a market that decided a social video app wasn't the product it needed. Hold that tension as you work through the exercise below: **Sora is discontinued and is not a tool for this assignment**, but the six months of hype that surrounded its launch are exactly the kind of claim this course asks you to interrogate.

### Inspiration: a music video written in code

This exercise was inspired by [a music video for *I'm Upping My P(doom)*](https://youtu.be/8j-hR4fJywU) made with Claude Opus 5.5. Every frame is drawn in code rather than generated as an image. According to the [project's source code and notes](https://github.com/JohnHeibel/PDoomVideo), no scene ideas were specified: the model was told to use Claude's Clawd character, give each lyric interesting visuals, use p5 brushstrokes, and make every scene transition into the next. The model wrote the storyboard and built the video shot by shot. The song, about raising one's p(doom) (the probability of AI-caused catastrophe), also connects back to last week's reading on doomers and boosters.

### Choose Your Method

For this exercise, choose **one** of two methods: animate a song with Claude or ChatGPT, or generate a video with Gemini or another video generation tool. Either way, you'll share the result.

#### Option 1: Animation with Claude or ChatGPT

Ask Claude or ChatGPT to build an animated music video, using this prompt:

> Make an artistic, silly symphony inspired, web animation using p5 brushstrokes and dynamic scenes to build a well-timed video that echoes the lyrics and timing.

Attaching a public domain song gives the model context and direction: lyrics to illustrate and a rhythm to time scenes against. It also lets you see what bias arises in the visual interpretation. Which characters, places, and bodies does the model imagine for a century-old song, and which does it leave out? To find one, look on the [Internet Archive](https://archive.org/details/audio): the [Great 78 Project](https://archive.org/details/georgeblood) is a good place to look, with tens of thousands of digitized 78 rpm records, many from the 1910s and 1920s. Choose a song with lyrics you can follow, check that the item is in the public domain, download it as an MP3, and attach it to a new chat along with the prompt.

Set the model to a higher effort level if you can (in Claude, Opus 5.5 at Extra effort; in ChatGPT, GPT-6 Sol with more thinking). Higher effort yields noticeably better results here: the model has to listen for the song's structure, plan scenes against the lyrics, and write a lot of drawing code. In Claude, ask for an artifact so you get something you can play and share with a link. Then iterate: ask the model to fix scenes that drift off the beat, change characters, or follow the lyrics more closely.

This prompt does not generate images or video. The model writes a program in [p5.js](https://p5js.org/), a JavaScript library for creative coding, and every frame is drawn from vector shapes and simulated brushstrokes as the song plays. Everything you see is code: shapes, colors, and motion timed against the audio. That makes it a very different kind of moving image from what a video model produces, even when the two look alike at a glance.

For my demonstration, I used "Take Me to the Land of Jazz" (1919), with music by Pete Wendling and words by Bert Kalmar and Edgar Leslie, from a 78 rpm recording on the Internet Archive. Claude Opus 5.5 at Extra effort built [*The Land of Jazz*](https://claude.ai/artifact/6HKYU628vbfCyUXggxsTbm): "A Brushstroke Jamboree" that opens on a vaudeville title card, then plays through a reel of timed scenes, with program notes on the song.

<video src="images/weekseven-land-of-jazz-claude.mp4" poster="images/weekseven-land-of-jazz-claude.png" controls></video>
*Figure 1. A screen recording of* The Land of Jazz*, a p5.js animation generated by Claude Opus 5.5 (Extra effort) from the prompt above, playing through the full song.*

I gave ChatGPT the same prompt and song, and it built [*Take Me to the Land of Jazz*](demos/WeekSeven/Take-Me-to-the-Land-of-Jazz/index.html): a painted sequence of a singing suitcase, a cabaret parade, a smiling riverboat, dancing shoes, a trombone tree, and a sleepy clock, with a storyboard timed to the lyrics. It came as a downloadable folder rather than a hosted link. Press Play to start the song.

#### Option 2: Video with Gemini or another video generation tool

A video model like Google's Veo 3.1 generates the footage directly, so every frame is a generated image. Here's what Gemini produced from the same song:

<video src="images/weekseven-land-of-jazz-gemini.mp4" controls></video>

Generate 2–3 short videos, working from text descriptions, a still image, or a song as I did. [Gemini](https://gemini.google.com/) (Veo 3.1) is one option; Google's student offer for [Google AI Pro](https://support.google.com/gemini/answer/16417758) currently includes a one-month free trial (US-only, with SheerID student verification), so check the current terms first. For other tools, this [list of free image-to-video tools](https://www.whytryai.com/p/free-ai-image-to-video-tools-tested) (updated February 2026) and the [Tom's Guide roundup of AI video generators](https://www.tomsguide.com/features/5-best-ai-video-generators-tested-and-compared) are good starting points; treat their rankings as dated and verify anything you rely on. Do not use Sora: it no longer exists as a working tool.

#### Comparing the methods

The styles are close: all three Land of Jazz examples reach for the rubber-hose look of 1920s and 1930s cartoons. The difference is in what's underneath. The Gemini clip is twenty seconds of pixels that can't be edited except by prompting again. The p5 animations run the full length of the song, and their code can be read, changed, and re-timed. Whichever method you choose, think about what the result borrows from, and from whom: the "silly symphony" in the prompt names a specific studio tradition and the animators who built it.

### Critiquing Generated Video and Animation

Now that you've explored the tools within some limitations, choose a generated video or animation to analyze and critique (your own, one of the examples above, or one you find elsewhere), with particular attention to the tensions of perception, vision, and labor drawn out through this week's readings. Keep in mind the concerns raised in Brett Halperin's talk, ["Hollywood Film Workers Strike Against AI: Understanding Algorithmic Resistance to Generative Cinematography"](https://stars.library.ucf.edu/elo2024/algorithmsandimaginaries/schedule/3/), as well as this week's reading from Tech Policy @ Duke Sanford, ["AI & the Film Industry: Production"](https://techpolicy.sanford.duke.edu/blog/ai-the-film-industry-production/), which lays out the production-labor stakes — deepfaked performers, displaced crew roles — behind the tools you've just been experimenting with. Animation has its own labor history, too: think about whose styles and techniques a prompt like "silly symphony inspired" calls up.

Contextualize the generation you've done in these larger debates: what do generated videos and animations suggest about the future of misinformation? Environmental and disaster communication? Conspiracy theories? Revenge pornography? How are people in your field using, or refusing to use, these tools? If this is your first time using them, were you surprised by the results — and does the Sora case study change how much you trust the next tool's launch-day claims?

### Discussion

For full credit (4 points), share the result of the method you chose: the link to your animation artifact (or its files), or your generated video. If you animated a song, include the Internet Archive link for it. Your post should combine what you learned from your own work with your observations about the form, drawing on the example you've selected for analysis. Also include a link (or attached file) for the video or animation you've selected to critique, as well as relevant context, so we can build a shared sense of the state of the field from the range of works critiqued.

If you're looking for more material to draw on: Science SARU's new *The Ghost in the Shell* series (dir. Mokochan, script EnJoe Toh) premieres July 7, 2026 on Prime Video and airs new episodes through the semester — fair game as supplemental viewing and discussion material if you're following along.

Finally: the Sora arc added plausible frames where no event existed, and for six months a lot of people found that convincing before the tool itself vanished. What does a hype cycle that ran from launch to shutdown in under seven months suggest about the gap between what these tools are claimed to do and what they can actually sustain?

Don't forget to reply twice to peers (1 point / reply) for the remaining 2 points!
