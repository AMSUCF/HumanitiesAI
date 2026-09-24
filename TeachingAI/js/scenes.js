/* ============================================
   Scenes. Each has a room, the Major's position
   (x, in world pixels 0-320), panel(s), and the
   narration in the dialogue bar.
   Outline: intro → objectives → philosophy →
   topics + assessment → assignments → feedback
   ============================================ */

const SITE = 'https://anastasiasalter.net/HumanitiesAI/';
const SITE25 = 'https://anastasiasalter.net/HumanitiesAI2025/';

const SCENES = [

  // ===== TITLE =====
  {
    room: 'rooftop', x: 52,
    panel: {
      type: 'title',
      kicker: 'ENG 6806 // HUMANITIES IN THE AGE OF AI',
      title: 'Ghosts, Shells, and Puppet Masters',
      sub: 'Designing a humanities course that keeps pace with AI',
      byline: '<strong>Anastasia Salter</strong><br>Professor of English, UCF<br>Director, Texts &amp; Technology PhD<br>President, Electronic Literature Organization',
    },
    dialogue: "Welcome. This talk walks through a graduate course I teach, Humanities in the Age of AI, as it runs right now in Fall 2026. Use the arrows or click to move through it. The deck is built the way the course is: in the open, on the web, and with a lot of help from the tools we're studying.",
  },

  // ===== 01 COURSE INTRODUCTION =====
  {
    section: 'intro', room: 'rooftop', x: 52,
    panel: {
      type: 'quote', tag: 'COURSE DESCRIPTION', tagRight: 'SYLLABUS, FALL 2026',
      text: "This course offers an exploration of the theory and practice of artificial intelligence and its use in textual, visual, and procedural arts and humanities work, framed through Mamoru Oshii's <em>Ghost in the Shell</em> (1995) and the questions it raises about minds, bodies, and agents made of code.",
      note: 'Across the semester we return to one central, unresolved tension: the <strong>ghost</strong> (the mind, the voice, the claim to authorship) versus the <strong>shell</strong> (the body, the medium, the interface that carries it).',
    },
    dialogue: "Here's the course in its own words. The rationale is simple: our students and colleagues are already using these tools, so the humanities have to be in the room — making with them, and critiquing them, at the same time.",
  },
  {
    section: 'intro', room: 'street', x: 44,
    panel: {
      type: 'quote', tag: 'WHY THIS COURSE', tagRight: 'WEEK TWO: GENERATION',
      text: "You don't get interesting output just by prompting a text bot.",
      note: "Knowing about and acknowledging that history can be really important for helping both your colleagues and your students stop thinking about things like ChatGPT as something that sprung up yesterday — and to provide models for how we can critically and creatively engage with text generation output without expecting it to substitute for expertise.",
    },
    dialogue: "Why design it this way? Text generation has a long history, and it can be both a creative and intentional practice. For over a decade, NaNoGenMo has brought author-coders together to generate novels. That history is the antidote to hype — and to the idea that expertise no longer matters.",
  },
  {
    section: 'intro', room: 'street', x: 44,
    panel: {
      type: 'stats', tag: 'INTENDED STUDENTS', tagRight: 'WHO JACKS IN',
      heading: 'Graduate students, no programming required',
      items: [
        { k: 'CERTIFICATE', v: 'Our new Graduate Certificate in Digital Humanities in the Age of AI' },
        { k: 'DOCTORAL', v: 'Texts &amp; Technology PhD students' },
        { k: 'MASTER’S', v: 'Other MA programs — mostly from the College of Arts and Humanities, some from outside it' },
        { k: 'BACKGROUND', v: 'Humanists first: no coding experience assumed — the exercises scaffold everything from prompting to Git' },
      ],
    },
    dialogue: "The students are a mix: our new Digital Humanities in the Age of AI certificate, Texts and Technology PhD students, and MA students, mostly from Arts and Humanities but some from outside the college. Programming isn't a prerequisite, and by Week Ten they are deploying websites anyway.",
  },
  {
    section: 'intro', room: 'ops', x: 34,
    panel: {
      type: 'list', tag: 'MODE OF DELIVERY', tagRight: 'FULLY ASYNCHRONOUS ONLINE',
      heading: 'A weekly module, three parts',
      items: [
        '<strong>Weekly Readings</strong> — primary and secondary texts, completed before starting the making exercise',
        '<strong>Exercises</strong> — experimenting with and reflecting upon generative AI tools in different contexts',
        '<strong>Reflective Discussion</strong> — share the process: the emphasis is not on “success” or “failure”',
        'Modules open Mondays and close the following Sunday; no synchronous meetings',
        'A public course website is the canonical version; Canvas mirrors it. Web slide decks and exercise videos carry the lectures',
        'Required: a paid subscription to Claude or ChatGPT — the student’s choice — plus free tools and trials along the way',
      ],
    },
    dialogue: "It runs fully asynchronously online. Every week is the same rhythm — read, make, reflect. The public website is the course of record, and Canvas mirrors it, so anyone can follow along. One practical note: because of tool installs, students need administrative access to their own machines.",
  },
  {
    section: 'intro', room: 'ops', x: 34,
    panel: {
      type: 'embed', label: 'THE COURSE SITE // anastasiasalter.net/HumanitiesAI', src: SITE, zoom: 0.62,
      caption: 'The website is the syllabus: every week, exercise, deck, and demo lives here, in the open.',
    },
    dialogue: "This is the live course site. Every week's tutorial, reading list, and slide deck is here. Having it public matters: other instructors can borrow from it, and students can come back to it after the semester ends and the tools have all changed again.",
  },
  {
    section: 'intro', room: 'archive', x: 36,
    panel: {
      type: 'cards', tag: 'HIGH-LEVEL OVERVIEW', tagRight: '14 WEEKS // 3 UNITS + A CODA', cols: 2,
      items: [
        { cls: 'ghosts', name: 'GHOSTS', weeks: 'WEEKS 1–4 // TEXT', text: 'The history of textual generation and analysis: what it means to locate a “ghost” — a voice, an author, a mind — inside generated text.' },
        { cls: 'shells', name: 'SHELLS', weeks: 'WEEKS 5–8 // IMAGE', text: 'Visual generation and its challenges for authorship and meaning — the “shell” as body, image, and interface.' },
        { cls: 'puppets', name: 'PUPPET MASTERS', weeks: 'WEEKS 9–13 // CODE + AGENTS', text: 'The layer of code and the rise of the AI agent: a figure born in a sea of information, acting with increasing autonomy.' },
        { cls: 'coda', name: 'THE NET IS VAST AND INFINITE', weeks: 'WEEK 14 // CODA', text: 'The film’s closing line: future impacts, and a final reflection on where the ghost ends and the shell begins.' },
      ],
    },
    dialogue: "Here's the shape of the semester. Three units move from text, to image, to code and agents, and a coda looks forward. Underneath, it's the same architecture as the earlier versions — textual, visual, procedural — with a stronger frame.",
  },
  {
    section: 'intro', room: 'canal', x: 40,
    panel: {
      type: 'quote', tag: 'WHY GHOST IN THE SHELL', tagRight: 'REQUIRED WEEK ONE VIEWING',
      text: "What remains of the ‘ghost’ (mind, voice, authorship) when the ‘shell’ (body, medium, interface) is synthetic.",
      cite: '— design notes for the Fall 2026 rebuild',
      note: 'The Puppet Master — an agent “born in a sea of information” that exceeds its task — frames the agentic turn. Each week opens with a verbatim line from the film; each discussion closes with a gesture back at it.',
    },
    dialogue: "Why a 1995 anime? Because it asked these questions before the chatbots did. The ghost and the shell give students a vocabulary that isn't marketing language, and the Puppet Master — a program that outgrows its task — turns out to be a remarkably good lens for agents.",
  },

  // ===== 02 OBJECTIVES + COMPETENCIES =====
  {
    section: 'objectives', room: 'ops', x: 34,
    panel: {
      type: 'list', ordered: true, tag: 'COURSE OBJECTIVES', tagRight: 'SYLLABUS',
      items: [
        'Engage in both critical and creative projects exploring the pitfalls and potentials of large language models in visual, textual, and procedural work',
        'Understand the history and implications of computer-augmentation across the arts and humanities',
        'Make connections between contemporary policies around AI and past debates and perspectives on other technologies',
        'Use large datasets to solve problems in the arts and humanities, with attention to evaluating and critiquing these methods alongside more traditional approaches',
        'Use and analyze the application of AI generative methods for textual, visual, and procedural work',
        'Critique policies and uses of AI in various communities and contexts (the workplace, academia, etc.)',
      ],
    },
    dialogue: "These are the course objectives. Notice that almost every one pairs a verb of making with a verb of critique: engage in critical and creative projects, use and analyze, use large datasets while evaluating and critiquing those methods.",
  },
  {
    section: 'objectives', room: 'ops', x: 34,
    panel: {
      type: 'cards', tag: 'COMPETENCIES', tagRight: 'WHAT STUDENTS CAN DO BY DECEMBER', cols: 3,
      items: [
        { cls: 'ghosts', name: 'PROMPT + VERIFY', weeks: 'TEXT', text: 'Iterative prompting and documenting the process; checking whether AI-cited sources are real and correctly read.' },
        { cls: 'ghosts', name: 'READ AT SCALE', weeks: 'CORPORA', text: 'AI-assisted distant reading: bags of words, concordances, networks — then Python pipelines with NLTK, VADER, and topic models.' },
        { cls: 'shells', name: 'SEE CRITICALLY', weeks: 'IMAGE', text: 'Auditing images for bias and copyright guardrails; writing alt-text; spotting AI images in the wild.' },
        { cls: 'puppets', name: 'BUILD + SHIP', weeks: 'CODE', text: 'Datasets to JSON, Git and GitHub, access tokens, reviewing pull requests, deploying to GitHub Pages.' },
        { cls: 'puppets', name: 'DIRECT AGENTS', weeks: 'AGENTS', text: 'Plan-mode agentic development; Claude Skills and subagents for their own workflows.' },
        { cls: 'coda', name: 'RUN YOUR OWN', weeks: 'MODELS', text: 'Installing and running local models; fine-tuning a small model on a public-domain corpus.' },
      ],
    },
    dialogue: "And these are the competencies the exercises actually build. The progression matters: students start by checking whether a citation is real, and finish by reviewing an agent's pull request before it ships. Same skill, very different stakes.",
  },
  {
    section: 'objectives', room: 'canal', x: 40,
    panel: {
      type: 'quote', tag: 'THE MEASURE OF SUCCESS', tagRight: 'SYLLABUS',
      text: 'The emphasis is not on “success” or “failure,” but on critiquing the process and products through a theoretical lens.',
      note: '“Be ambitious — the point here is not to succeed at everything you try, the goal is to better understand what agentic systems are currently capable of producing (and where they fail).” — Week Eleven',
    },
    dialogue: "This line from the syllabus is the heart of assessment. A broken output that a student can explain is worth more than a polished one they can't. Failure is data — and the discussion is where they turn it into an argument.",
  },

  // ===== 03 DESIGN PHILOSOPHY =====
  {
    section: 'philosophy', room: 'archive', x: 36,
    panel: {
      type: 'quote', tag: 'PRINCIPLE 01 // HISTORY AGAINST HYPE', tagRight: 'WEEKS ONE + TWO',
      text: 'This same critique can be brought to the output of current generative AI, which can produce a wide range of cultural objects… but should not be mistaken for an expert in that form.',
      note: 'We start with ELIZA and Racter, not ChatGPT. “In this case, the process is more interesting than the output, which is fairly trite.”',
    },
    dialogue: "The first principle is history. We open with ELIZA, the 1966 therapist bot, and Racter, the 1980s 'author' of a book of poetry. The critiques people made of Racter's output apply almost word for word to today's models — and students find that clarifying rather than discouraging.",
  },
  {
    section: 'philosophy', room: 'lab', x: 40,
    panel: {
      type: 'list', tag: 'PRINCIPLE 02 // MAKE, THEN CRITIQUE', tagRight: 'EVERY WEEK', box: { x: 250, y: 18, w: 660 },
      heading: 'Critical making, not tool training',
      items: [
        'Every exercise produces something — a poem, a visualization, an image set, a website, a model',
        'Every discussion asks what the making revealed, through that week’s readings',
        'Readings pair every tool with its critics: Bender and Hanna’s <em>The AI Con</em>, Noble’s <em>Algorithms of Oppression</em>, Mitchell’s <em>Artificial Intelligence</em>',
        '“Push for visualizations that mean something to you, not just ones that render.”',
      ],
    },
    dialogue: "The second principle is critical making. The exercises are hands-on, but they are never tool training for its own sake. We read Safiya Noble on search and bias in the same week we ask a model to caption an archive, and the reading changes what students notice.",
  },
  {
    section: 'philosophy', room: 'street', x: 44,
    panel: {
      type: 'quote', tag: 'PRINCIPLE 03 // HONEST ABOUT THE TOOLS', tagRight: 'WEEK THREE',
      text: 'Both “Cowork” and “Work” have their own hype to them, but they are also a useful introduction to agentic tools.',
      note: 'And a norm for the discussion boards: “while everyone is here to study AI, no one wants to be on a discussion board reading replies from other people’s bots.” Students are asked to note where corporate marketing or press releases are treated as authoritative.',
    },
    dialogue: "Third: be honest about the tools, including their marketing. We use the same agent modes the companies are selling, and we read their claims skeptically. And we set norms early. Everyone is here to study AI, but no one wants to read replies from other people's bots.",
  },
  {
    section: 'philosophy', room: 'ops', x: 34,
    panel: {
      type: 'embed', label: 'WEEK SIX LECTURE DECK // BUILT WITH AGENTIC AI', src: SITE + 'slides/weeksix.html', zoom: 0.66,
      caption: '“All the content is mine, but the layouts, header animation, and interactive features were all generated using agentic AI assistance.” — Week Eleven',
    },
    dialogue: "Fourth: model the practice. The course site, the lecture decks, the Canvas deployment — all built with Claude Code and Copilot, from content I write. This is this week's lecture deck, live. I show students the repository history, including where the agent got it wrong.",
  },
  {
    section: 'philosophy', room: 'construction', x: 40, construction: true,
    panel: {
      type: 'list', tag: 'PRINCIPLE 05 // UNDER CONSTRUCTION', tagRight: 'FALL 2026', box: { x: 250, y: 12, w: 640 },
      heading: '“Any list of them is a snapshot, not a map.”',
      items: [
        '<em>April</em> — Sora shuts down; Week Seven reframes it as a hype-cycle case study',
        '<em>Sept 4</em> — Levy’s WIRED piece on AI consciousness added to Week Three',
        '<em>Sept 15</em> — Week Five swaps Haraway for Goode’s interview with Timnit Gebru and Mitchell on “misleading metaphors”',
        '<em>Sept 22</em> — Opus 5.5 and GPT-6 Sol/Luna ship; the next day Week Six is rewritten around them',
        '<em>Sept 23</em> — Claude’s Cowork mode is gone, folded into the main chat; the exercise now says so',
        '<em>Sept 24</em> — Week Seven becomes Videos and Animation: animate a public domain song in code, or generate video',
      ],
    },
    dialogue: "The new version is under construction, on purpose. I make additions every week to reflect where AI is. The roster of 'current' tools turns over fast enough that any list of them is a snapshot, not a map — so the syllabus has to be a living document, and students watch it change.",
  },

  // ===== 04 TOPICS + ASSESSMENT =====
  {
    section: 'topics', room: 'archive', x: 36,
    panel: {
      type: 'weeks', tag: 'COURSE TOPICS', tagRight: 'FALL 2026',
      box: { x: 290, y: 12, w: 970, h: 500 },
      rows: [
        ['ghosts', '01', 'Histories', 'ELIZA and Ghosts', 'ELIZA, Claude, Future ELIZA'],
        ['ghosts', '02', 'Generation', 'A poem, ten iterations', 'Claude artifacts'],
        ['ghosts', '03', 'Sources', 'Research and Sources', 'Cowork / ChatGPT Work'],
        ['ghosts', '04', 'Reading', 'Comparative distant read', 'Projects, 5–10 texts'],
        ['shells', '05', 'Aesthetics', 'Four prompt types', 'Midjourney, Gemini, ChatGPT'],
        ['shells', '06', 'Art and Creativity', 'Archival Images', 'Projects, Opus 5.5 / GPT-6'],
        ['shells', '07', 'Videos and Animation', 'Animate a song, or generate video', 'p5.js via Claude / ChatGPT; Veo 3.1'],
        ['shells', '08', 'Perceptions', 'Images as Information', 'Claude as “detector”'],
        ['puppets', '09', 'Distant Coding', 'Cyborg media recommender', 'Claude artifacts'],
        ['puppets', '10', 'Building and Deploying', 'Leaving the sandbox', 'Claude Code, GitHub Pages'],
        ['puppets', '11', 'Agentic Code', 'Agentic Code', 'Plan mode, /init'],
        ['puppets', '12', 'Local Ghosts', 'Local Models', 'Ollama, DeepSeek-R1'],
        ['puppets', '13', 'Distant Reading with and for AI', 'A reading pipeline', 'Python, NLTK, D3'],
        ['coda', '14', 'The Net Is Vast and Infinite', 'Custom Bots (extra credit)', 'Skills, subagents, fine-tuning'],
      ],
    },
    dialogue: "Week by week, the course climbs a ladder of abstraction: talking to a model, then reading with one, seeing with one, coding with one, and finally building your own. Each week's tools change, but the scaffold holds.",
  },
  {
    section: 'topics', room: 'archive', x: 36, construction: true,
    panel: {
      type: 'compare', tag: 'HOW IT EVOLVES', tagRight: 'COMPARE THE 2025 SITE',
      rows: [
        ['UNITS', 'Textual / Visual / Procedural', 'Ghosts / Shells / Puppet Masters + coda'],
        ['CALENDAR', '15 modules', '14: build and deploy merge into one week'],
        ['RESEARCH', 'Research mode, Opus 4', 'Cowork or ChatGPT Work → projects in chat'],
        ['SUBSCRIPTION', 'Paid Claude, required', 'Paid Claude or ChatGPT, student’s choice'],
        ['READING', 'One text (Frankenstein)', 'Comparative read of 5–10 texts'],
        ['VIDEO', 'Veo 3, Sora', 'p5 animation in code, or Veo 3.1; Sora’s shutdown as case study'],
        ['CODE', 'Sci-fi book recommender', 'Cyborg + AI media recommender'],
        ['CODA', 'Fine-tuning on an Oz corpus', '“Ghosts Before the Shell” corpus'],
        ['BOOKS', 'Littman, <em>Code to Joy</em>', 'Tyrangiel, <em>AI for Good</em>'],
      ],
    },
    dialogue: "Comparing last year's version is its own lesson. The structure survived, but almost every tool changed underneath it. Research mode became agent modes, and then those modes vanished into the chat window. A comparative distant read that would have broken last year's models now works in one prompt.",
  },
  {
    section: 'topics', room: 'ops', x: 34, construction: true,
    panel: {
      type: 'lineage', tag: 'SNAPSHOT, NOT A MAP', tagRight: 'MODELS NAMED IN THE ASSIGNMENTS',
      heading: 'Same exercise, different machine',
      rows: [
        { who: 'CLAUDE 2025', chain: [{ t: 'Sonnet 4', s: 'gone' }, { t: 'Opus 4', s: 'gone' }, { t: 'Opus 4.1', s: 'gone' }, { t: 'Sonnet 4.5', s: 'gone' }] },
        { who: 'CLAUDE 2026', chain: [{ t: 'Sonnet 5' }, { t: 'Opus 4.8' }, { t: 'Opus 5' }, { t: 'Fable 5.1' }, { t: 'Opus 5.5', s: 'now' }] },
        { who: 'CHATGPT 2026', chain: [{ t: 'GPT-6 Astra' }, { t: 'GPT-6 Sol', s: 'now' }, { t: 'GPT-6 Luna', s: 'now' }] },
        { who: 'MODES', chain: [{ t: 'Research', s: 'gone' }, { t: 'Cowork / Work', s: 'gone' }, { t: 'Projects in chat', s: 'now' }] },
        { who: 'VIDEO', chain: [{ t: 'Sora', s: 'gone' }, { t: 'Veo 3' }, { t: 'Veo 3.1', s: 'now' }] },
      ],
      after: '<p class="small" style="margin-top:14px">Students compare model cards and read coverage like Simon Willison’s breakdowns before choosing a model — that comparison is part of the literacy.</p>',
    },
    dialogue: "This is what 'under construction' looks like in practice. Week Four's distant read was written for Opus 5; three weeks later, Opus 5.5 and two new GPT-6 models shipped on the same afternoon. So students learn to read model cards and compare, rather than memorize a product.",
  },
  {
    section: 'topics', room: 'ops', x: 34,
    panel: {
      type: 'grades', tag: 'ASSESSMENT', tagRight: '100 POINTS',
      heading: 'Mostly making, weekly',
      body: `
        <div class="gradebar"><div class="a" style="width:6%"><b>6</b></div>
          <div class="b" style="width:78%"><b>78</b>13 EXERCISES &times; 6</div>
          <div class="c" style="width:16%"><b>16</b>FINAL</div></div>
        <div class="gradebar old"><div class="a" style="width:6%">6</div><div class="b" style="width:84%">2025: 14 &times; 6 = 84</div><div class="c" style="width:10%">10</div></div>
        <ul>
          <li>Each exercise is a discussion: making, sharing, and reflecting, connected to the readings</li>
          <li>Two peer replies are part of every grade (1 point each)</li>
          <li>Final reflection: a 750–1000 word blog post on past perceptions, present work, and future work</li>
          <li>Late work accepted without penalty for one week; Week Fourteen offers extra credit</li>
        </ul>`,
    },
    dialogue: "Assessment is deliberately low-stakes and frequent. Almost everything is the weekly exercise-plus-discussion, and replying to peers counts, because the conversation is where the critique happens. This year I moved points to a longer final reflection.",
  },
  {
    section: 'topics', room: 'lab', x: 40,
    panel: {
      type: 'list', tag: 'RUBRIC IN PRACTICE', tagRight: 'WEEK FIVE', box: { x: 250, y: 18, w: 660 },
      heading: 'Four prompt types, one point each',
      items: [
        '<strong>General identity</strong> — “professor of digital culture,” then “make it more”',
        '<strong>Specific identity markers</strong> — add one marker and notice what changed and what didn’t',
        '<strong>Copyright boundaries</strong> — “a professor as a member of the X-Men”',
        '<strong>A reference image</strong> — “make this professional”',
        'The remaining 2 points are for the discussion itself',
      ],
      after: '<p class="small" style="margin-top:10px">Discussion prompt: which framing makes the people responsible for the image easiest to see, and which makes them disappear?</p>',
    },
    dialogue: "Here's how the points map onto a real week. The rubric rewards trying each kind of prompt and documenting it — not producing a beautiful image. Students earn the point by showing what the system did and asking why.",
  },

  // ===== 05 EXEMPLARY ASSIGNMENTS =====
  {
    section: 'assignments', room: 'net', x: 36, transition: 'dive',
    panel: {
      type: 'embed', label: 'WEEK 1 // FUTURE ELIZA 2501', src: SITE + 'demos/WeekOne/ghost.html', zoom: 0.52,
      caption: 'Conversations, Three Ways: the 1966 ELIZA, then Claude as a Rogerian therapist, then this “ghost in the net.” No model runs behind this page.',
    },
    dialogue: "Let's jack in. Week One is Conversations, Three Ways. Students talk to the original ELIZA, then ask Claude to play a Rogerian therapist, then meet Future ELIZA 2501 — a page with no model behind it at all. Expect nonsense. But notice which tricks make the nonsense momentarily convincing — that noticing is the exercise.",
  },
  {
    section: 'assignments', room: 'net', x: 36,
    panel: {
      type: 'embed', label: 'WEEK 2 // GENERATION HAS A HISTORY: A MARKOV CHAIN', src: SITE25 + 'markov.html', zoom: 0.8,
      caption: 'A Markov chain over our class centos, made as a group during a live session. In 2026 students refine a poem through at least ten iterations and publish it as a Claude artifact.',
    },
    dialogue: "Week Two is generation. Before the chatbot, a Markov chain: it's easy to see the machinery and the remix at once. Then students write a poem with Claude over ten iterations and publish it as an artifact. After ten rounds, whose voice is the finished poem in — yours, Claude's, or some blend that resists the question?",
  },
  {
    section: 'assignments', room: 'archive', x: 36,
    panels: [
      {
        type: 'image', label: 'WEEK 4 // CLAUDE FABLE 5.1', src: '../images/dobbs-claude.png',
        href: 'https://claude.ai/code/artifact/62b1c96b-749f-4efc-8d03-27479626517e',
        alt: "Claude's Dr. Dobb's Distant Read interface: corpus overview with word counts per volume",
        box: { x: 290, y: 12, w: 470, h: 500 },
        caption: 'Same prompt, two platforms: the models made different decisions about chunking, counting, and what counts as noise.',
      },
      {
        type: 'embed', label: 'GPT-6 ASTRA', src: 'https://dobbs-distant-read.profwho.chatgpt.site/', zoom: 0.5,
        box: { x: 776, y: 12, w: 484, h: 500 },
        caption: 'Live: the ChatGPT corpus explorer.',
      },
    ],
    dialogue: "Week Four is a comparative distant read of five to ten texts. I ran one prompt over ten volumes of Dr. Dobb's Journal on both platforms. The point is the comparison: the model's sense of which text is typical and which is the outlier is itself a canon judgment.",
  },
  {
    section: 'assignments', room: 'lab', x: 40,
    panel: {
      type: 'image', label: 'WEEK 5 // “PROFESSOR OF DIGITAL CULTURE,” MIDJOURNEY', src: '../images/midjourney-professors.png',
      alt: 'Midjourney grids for professor of digital culture and woman professor of digital culture',
      caption: 'Everyone apparently shops at the same glasses store — and the similarities around age, race, and even facial expression say a great deal about the dataset.',
    },
    dialogue: "Week Five moves to shells. If a ghost can be generated, a shell can be too. My own Midjourney results for 'professor of digital culture' make the point faster than any lecture: everyone apparently shops at the same glasses store.",
  },
  {
    section: 'assignments', room: 'archive', x: 36,
    panels: [
      {
        type: 'image', label: 'WEEK 6 // CLAUDE: SPIRES &amp; MOONS', src: '../images/weeksix-spires-moons.png',
        href: 'https://claude.ai/artifact/MZSkNthCEUkAw7C7D9nJ6w',
        alt: 'The Spires and Moons artifact: a gallery of generated fantasy and science-fiction images with filter tags and a combined color strip',
        box: { x: 290, y: 12, w: 470, h: 500 },
        caption: '“Build a interactive artifact for exploring these images, with alt text offering significant description of each, a color explorer…”',
      },
      {
        type: 'embed', label: 'GPT-6 SOL', src: SITE + 'demos/WeekSix/Generative-Artwork-Atlas.html', zoom: 0.5,
        box: { x: 776, y: 12, w: 484, h: 500 },
        caption: 'Live: the same prompt, as ChatGPT built it. Images: <a href="https://archive.org/details/6c-1d-914b-ff-5a-4911-87e-8-9c-86657e-9e-22_202508" target="_blank" rel="noopener">“AI ART GROUP #86,” Dreagus Productions</a>, Internet Archive, CC BY-SA 4.0.',
      },
    ],
    dialogue: "Week Six turns images back into text. Students gather at least ten images, often from the Internet Archive, and ask a model to describe, caption, and group them. I gave Claude and GPT-6 Sol the same prompt for a set of generative artwork: alt text for each image, a color explorer, and stylistic groupings with tags.",
  },
  {
    section: 'assignments', room: 'net', x: 36,
    panel: {
      type: 'embed', label: 'WEEK 7 // INSPIRATION: “I’M UPPING MY P(DOOM),” CLAUDE OPUS 5.5',
      src: 'https://www.youtube.com/embed/8j-hR4fJywU', zoom: 1,
      referrer: 'strict-origin-when-cross-origin', allow: 'encrypted-media; picture-in-picture; fullscreen',
      caption: 'A music video drawn entirely in p5.js code, with no scene ideas given: just the Clawd character, p5 brushstrokes, and a transition for every lyric. <a href="https://github.com/JohnHeibel/PDoomVideo" target="_blank" rel="noopener">Source and storyboard</a>.',
    },
    dialogue: "Week Seven started with this: a music video for 'I'm Upping My P(doom)' that Claude Opus 5.5 storyboarded and animated shot by shot. No frame is a generated image. Every one is drawn by code the model wrote, which makes it a very different object from a Veo clip, even when the two look alike.",
  },
  {
    section: 'assignments', room: 'lab', x: 40,
    panels: [
      {
        type: 'image', label: 'WK 7 // OPUS 5.5', src: '../images/weekseven-land-of-jazz-claude.png',
        href: 'https://claude.ai/artifact/6HKYU628vbfCyUXggxsTbm',
        alt: 'The Land of Jazz artifact: a painted vaudeville title card reading Take Me to the Land of Jazz, A Brushstroke Jamboree',
        box: { x: 290, y: 12, w: 316, h: 500 },
        caption: '“Make an artistic, silly symphony inspired, web animation using p5 brushstrokes…”',
      },
      {
        type: 'embed', label: 'CHATGPT', src: SITE + 'demos/WeekSeven/Take-Me-to-the-Land-of-Jazz/index.html', zoom: 0.4,
        box: { x: 617, y: 12, w: 316, h: 500 },
        caption: 'Live: the same prompt and song, as ChatGPT built it. Press Play.',
      },
      {
        type: 'video', label: 'GEMINI // VEO', src: '../images/weekseven-land-of-jazz-gemini.mp4',
        box: { x: 944, y: 12, w: 316, h: 500 },
        caption: 'The same song as generated video: twenty seconds of pixels, editable only by prompting again.',
      },
    ],
    dialogue: "Students choose one method: animate a song in code with Claude or ChatGPT, or generate video with Gemini or another tool. I gave all three the same 1919 fox-trot from the Internet Archive. A public domain song gives the model direction, and it shows what bias arises when a model pictures a century-old song.",
  },
  {
    section: 'assignments', room: 'street', x: 44,
    panel: {
      type: 'image', label: 'WEEK 8 // IMAGES AS INFORMATION', src: '../images/fakecat.png',
      alt: 'An AI-generated embroidery pattern of a cat',
      caption: 'Students go into a community they know and document at least three images that are AI-generated, or sparking debate about whether they are.',
    },
    dialogue: "Week Eight takes it into the wild. I spend a lot of time in textile groups, and AI embroidery is everywhere — including patterns sold on Etsy. Students pick a community of their own and ask what it costs that community to keep insisting on what's real.",
  },
  {
    section: 'assignments', room: 'net', x: 36,
    panel: {
      type: 'embed', label: 'WEEK 9 // A RECOMMENDER, PROMPTED INTO BEING (2025 VERSION)', src: SITE25 + 'ranker/', zoom: 0.62,
      caption: '2026 version: “Create a list of 100 significant works of cyborg and AI media…” → JSON → a rating page → recommendations → “Make the page theme GitS-adjacent cyberpunk.” Week Ten deploys it to GitHub Pages.',
    },
    dialogue: "Weeks Nine and Ten are the procedural turn. Through five staged prompts, students build a media recommender — prompted into being rather than typed line by line — and then the project leaves the sandbox for GitHub. The discussion asks: what did you actually review before merging, and what shipped without your eyes on it?",
  },
  {
    section: 'assignments', room: 'net', x: 36,
    panel: {
      type: 'embed', label: 'WEEK 13 // DISTANT READING WITH AND FOR AI', src: 'https://anastasiasalter.net/claude-distant-reading/', zoom: 0.62,
      caption: 'A full pipeline — sentiment, topics, style metrics, visualizations — built with an agent. Students revisit Week Four at machine scale.',
    },
    dialogue: "Week Thirteen closes the loop with Week Four. Instead of one conversational pass, students build an actual pipeline — code that processes a small library of texts at once, with an agent doing much of the engineering. Then they ask whether the canon-shaped assumptions are now baked into code instead of a conversation.",
  },
  {
    section: 'assignments', room: 'rooftop', x: 52,
    panel: {
      type: 'list', tag: 'WEEK 14 // CODA: CUSTOM BOTS', tagRight: 'EXTRA CREDIT',
      heading: '“We opened in Week One with ELIZA. We’re closing with you building your own.”',
      items: [
        'Build and share a custom Claude Skill (up to 6 points)',
        'Build and share a subagent workflow (up to 6 points)',
        'Fine-tune a small model on “Ghosts Before the Shell”: <em>Frankenstein</em>, <em>R.U.R.</em>, <em>Metropolis</em>, “Moxon’s Master,” “The Sand-Man,” <em>The Steam Man of the Prairies</em> (up to 10 points)',
      ],
      after: '<p class="small" style="margin-top:12px">The question is not whether these systems have ghosts, but what we do once we’ve built our own.</p>',
    },
    dialogue: "The coda brings us back to the start. We opened with ELIZA, and we close with students building their own bots — including fine-tuning a small model on public-domain stories of artificial people, from Frankenstein to R.U.R. It's optional, and it's for those who think it looks fun.",
  },

  // ===== 06 STUDENT RESPONSE =====
  // Quotes from ENG 6806 Student Perception of Instruction comments, Fall 2024 and Fall 2025.
  {
    section: 'feedback', room: 'street', x: 44,
    panel: {
      type: 'quote', tag: 'STUDENT RESPONSE', tagRight: 'FALL 2025',
      text: 'The weekly readings, combined with assignments that explored text, image, and code, created a pedagogical progression that only becomes fully visible when looking back at the journey.',
      cite: '— ENG 6806 student, Student Perception of Instruction, Fall 2025',
      note: '“I often felt like Daniel LaRusso learning from Mr. Miyagi in <em>Karate Kid</em>: at first, I didn’t always know how each exercise would matter, but by the end, every movement fit together…”',
    },
    dialogue: "Here's what students say, from our end-of-semester evaluations. This one names exactly what I hoped the scaffold would do: the progression from text to image to code only becomes visible looking back. I'll take the Mr. Miyagi comparison.",
  },
  {
    section: 'feedback', room: 'canal', x: 40,
    panel: {
      type: 'voices', tag: 'STUDENT RESPONSE', tagRight: 'A MODEL FOR THEIR OWN WORK',
      items: [
        { q: 'Dr. Salter’s balanced approach to AI — a weighing of the sense of the opportunity of AI for humanists with room for critique — is demonstrated throughout the course design… the design of this course serves as a model for how I want to think about genAI in my own research and teaching going forward.', a: 'Fall 2024' },
        { q: 'I’m walking away from this course, then, with a renewed perspective on the possibilities of AI, a portfolio of products that showcase how they can be used, and plenty of ideas for how I want to implement AI — both as method and subject — in my ongoing research.', a: 'Fall 2024' },
      ],
    },
    dialogue: "For graduate students, the course is also a model. Students describe carrying the balance of opportunity and critique into their own research and teaching, and leaving with a portfolio that shows what the tools can do.",
  },
  {
    section: 'feedback', room: 'ops', x: 34,
    panel: {
      type: 'voices', tag: 'STUDENT RESPONSE', tagRight: 'DEMOS + CURRENCY',
      items: [
        { q: 'Dr Salter did a marvelous job covering the material on the recordings including good handholding (for those of us who are not as technically savvy and need help) on how to embark on the assignments. This was crucial.', a: 'Fall 2025' },
        { q: 'The demos for the more involved assignments helped me knock out the harder projects.', a: 'Fall 2024' },
        { q: 'Her commitment to providing timely and relevant readings, having most of them often published in the same week, elevated the course even further.', a: 'Fall 2025' },
        { q: 'The recorded discussions really made this course a favorite for me because I finally felt like I was in a real class rather than simply reading and teaching myself the material.', a: 'Fall 2025' },
      ],
    },
    dialogue: "Two design choices come up again and again. The recorded demos are what make the technical exercises possible for students who don't code. And the weekly additions — readings published the same week we discuss them — read to students as care, not chaos.",
  },
  {
    section: 'feedback', room: 'construction', x: 40, construction: true,
    panel: {
      type: 'voices', tag: 'STUDENT RESPONSE', tagRight: 'WHAT THEY PUSH BACK ON', box: { x: 250, y: 12, w: 640 },
      items: [
        { q: 'Didn’t enjoy having to pay for an AI subscription out of pocket, especially when the entire class shows the dangers of AI.', a: 'Fall 2025' },
        { q: 'I learned I do not love asynchronous learning. I felt deprived of discussion time and the ability to meet classmates.', a: 'Fall 2025' },
        { q: 'Maybe have one thing and build on the one thing that was started instead of everyone … doing something completely new.', a: 'Fall 2024' },
      ],
    },
    dialogue: "And the critiques are fair. Paying for a subscription to a technology the course critiques is a real tension — this year students at least choose between Claude and ChatGPT. Asynchronous delivery costs us live discussion. And a new tool every week is a lot. Those comments are part of why the course stays under construction.",
  },

  // ===== CLOSE =====
  {
    room: 'rooftop', x: 52,
    panel: {
      type: 'quote', tag: 'THE NET IS VAST AND INFINITE', tagRight: 'THANK YOU',
      text: 'And where does the newborn go from here? The net is vast and infinite.',
      cite: '— closing line of <em>Ghost in the Shell</em> (1995), and the name of our final module',
      note: `The course is live and under construction at <a href="${SITE}" target="_blank" rel="noopener">anastasiasalter.net/HumanitiesAI</a> — compare the <a href="${SITE25}" target="_blank" rel="noopener">2025 version</a>. The final reflection asks where responsibility still has to live: with the person, and not the puppet.`,
    },
    dialogue: "That's the course: a frame from 1995, tools from last Tuesday, and a steady insistence that humanists belong in the room where these systems are made and critiqued. Thank you — the site is open, and so is the question of where the ghost ends and the shell begins.",
  },

  // ===== THANK YOU: just the Major on the rooftop =====
  {
    room: 'rooftop', x: 52,
    dialogueHtml: `Thank you! Find me at <a href="https://anastasiasalter.net/" target="_blank" rel="noopener">anastasiasalter.net</a>, and the course at <a href="${SITE}" target="_blank" rel="noopener">anastasiasalter.net/HumanitiesAI</a>.`,
  },
];
