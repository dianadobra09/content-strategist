# Content Strategist

A Claude Code workspace that turns your raw notes into posts for LinkedIn, X, Threads and Bluesky that sound like you, with visuals, and schedules them through Zernio. It works in Codex too: `AGENTS.md` and `.agents/skills` point to the same files.

Built by Diana Dobra on the setup of Maja Voje's [GTM Strategist skills](https://github.com/GTM-Strategist/gtm-strategist-skills): skills in `.claude/skills/`, context files you fill in once, and every output saved in the repo.

<img src="examples/outputs/visuals/content-workflow/content-workflow.png" alt="How does a post get made? Before the first post, you give it your old posts and a few voice memos, so it learns how you write and talk. Then, for each post: you send your notes, it asks for what's missing and checks each fact, it drafts the LinkedIn post, it runs a humanizer and a voice check, it writes the X, Threads and Bluesky versions, and you approve it while Zernio schedules it. When you edit a draft, it learns from your changes." width="540">

## How it works

**Train it first.** Before it can write like you, it needs your writing and the way you speak. Give `train-voice` your posts, messages and emails, and transcripts of voice memos or talks: spoken words show how you explain things when you aren't polishing them. It fills `voice/samples/`, writes the patterns into `voice/voice-guide.md` and keeps learning from every edit you make. `examples/voice/` shows what Diana's voice files look like after a few weeks.

**LinkedIn is the primary channel.** Every idea starts as a LinkedIn post:

1. **Idea.** Say "idea: ..." and it's saved word for word in `ideas/open/`. Nothing gets written yet.
2. **Brief and evidence.** `generate-content` picks one reader and one takeaway, and asks you for what's missing instead of inventing it. Every fact is checked against its primary source and saved in the post file with the line it supports. If your notes get a fact wrong, the post corrects it and says so.
3. **Draft.** The post uses your words, a structure from `references/formats.md` and one feeling from `references/psychology.md`. `linkedin-hook` proposes up to three openings and estimates where LinkedIn cuts each one on mobile.
4. **Humanize and check.** Every version goes through `humanizer` (blader/humanizer) and then `voice-check`, against your voice guide, kill list and samples.
5. **You approve.** Nothing goes out without you. Approved posts move to `outputs/posts/ready/<channel>/`.

**X, Threads and Bluesky come second.** `x-post`, `threads-post`, `bluesky-post` and `repurpose` adapt LinkedIn posts for them: one point per post, within each platform's limits, using publicly known formats and each platform's published guidance. The time goes into LinkedIn; these channels get the repurposed version.

**Visuals** are made from real material: a diagram, a chart, excerpts from a source document, a two-page carousel (`outputs/visuals/carousel-kit/`) or a short animation. `motion-graphics-builder` builds the animation as editable HTML and renders an MP4, a GIF and a still. The carousels and animations use the brand guidelines of BlinkWrite, Diana's product: its fonts, colours and margins. Replace them with your brand's.

**Scheduling** goes through the Zernio MCP server. `schedule-posts` plans each channel's queue with `scripts/schedule_plan.py` (LinkedIn first: nothing goes out on the other channels before its LinkedIn post), creates the posts in Zernio with the approved text, first comments, topic tags and visuals, and never publishes immediately.

**Learning from other creators.** `study-creator` reads another creator's posts and extracts their formats: hooks, post shapes, layout, visuals. It never copies their content, phrasing or voice; only the structures go into `references/formats.md`.

**It learns from you.** Paste what you actually posted, or correct a draft ("too corporate", "I'd never say that"). `train-voice` compares the versions and updates your voice guide, kill list and feedback log. `content-plan` logs what you published and reviews what works.

## Setup

You need Claude Code (or Codex) and Python 3. Optional: Node 18+ and ffmpeg for animations, Google Chrome on macOS for carousels, and a Zernio account for scheduling.

1. Clone the repo, or use it as a GitHub template, and open the folder in Claude Code.
2. Train your voice: paste 10–20 of your own posts (or give your LinkedIn export, X archive or Bluesky handle), plus a few messages, emails and voice memo transcripts, and say "train my voice with these". Mark your favorite posts `best`.
3. Fill in `strategy/positioning.md`: your position, pillars, category mix, audience, ICP, platforms and cadence. Say "help me fill in my positioning" and answer the questions.
4. If you're building a product, fill in `strategy/product.md`: what posts can say, what they must not claim, and your launch status.
5. Read `voice/kill-list.md` and add the words and phrases you never use.
6. For scheduling, connect Zernio: `claude mcp add --transport http zernio https://mcp.zernio.com/mcp`, then `/mcp` → zernio → Authenticate. The first "schedule the posts" asks which accounts to use and saves their ids in `strategy/positioning.md`.
7. Put your own brand's colours and fonts in `outputs/visuals/carousel-kit/kit.css` and `.claude/skills/motion-graphics-builder/template/index.html`.

## Daily use

| Say | What happens |
|---|---|
| "idea: ..." | saved as is in `ideas/open/` |
| "write a post about ..." or paste notes, a link or a voice memo transcript | brief, evidence, LinkedIn draft and hooks in `outputs/posts/drafts/` |
| "what should I post next?" | a short list ranked by reader value, evidence and your category mix |
| "put this on X / Threads / Bluesky" | versions for those platforms, in the same post file |
| "does this sound like me?", "humanize this" | small edits to your own draft, each listed so you can reject it |
| "make a visual", "make a carousel", "animate this" | an editable source and a checked export in `outputs/visuals/<post>/` |
| "schedule the posts", "what's scheduled?" | the calendar in `outputs/schedule.md` and the posts created in Zernio |
| "here's what I actually posted" | your edits go into the feedback log and the voice guide |
| "I posted it" | the files move to `published/` and get a row in `outputs/log.md` |
| "study this creator" | their formats in `references/creators/` and `references/formats.md`, never their content |

## What's in the repo

```
CLAUDE.md                 the rules, the skill table and the post file template (AGENTS.md links to it)
.claude/skills/           generate-content, linkedin-post, linkedin-hook, x-post, threads-post, bluesky-post,
                          repurpose, humanizer, voice-check, train-voice, study-creator, content-plan,
                          motion-graphics-builder, schedule-posts
strategy/                 positioning and cadence, product facts, how visuals are made
voice/                    your voice guide, kill list, feedback log and samples
references/               post formats, feelings, reach tags, what works on Threads, creator studies
ideas/                    your raw ideas: open/, used/, files/
outputs/                  drafts, ready and published posts per channel, visuals, carousel kit, schedule, log, angles
scripts/                  voice_stats.py, compare.py, hook_check.py, schedule_plan.py
examples/                 Diana's voice files, published and approved posts, the ideas behind them and their visuals
```

## Examples

`examples/` shows real results from Diana's account. The skills treat it as reference only; your own posts start in the empty `ideas/` and `outputs/` folders, and your voice in `voice/`.

- `voice/`: Diana's voice guide, kill list and a selection from the feedback log, learned from her notes and her edits to drafts.
- Four published posts with their X, Threads and Bluesky versions: an explainer built on four studies, a post on a design team moving from Figma to a React repo, with its animation and the HTML it was built from, a short post built on one paper, and a research post on Character.AI's bankruptcy.
- Three approved posts in the ready queue, each with its X, Threads and Bluesky set: subscription or usage pricing for AI products and the EU rule on detectable AI text, each with a two-page carousel, and a question to founders about Google Ads.
- The research post's idea file keeps the whole trail: the raw notes, the brief, the facts checked against court filings, the hooks with their mobile cut, and the edit log. Its visual crops the quoted lines straight from the court PDFs.

## Credits and licenses

- Setup: Maja Voje's [GTM Strategist skills](https://github.com/GTM-Strategist/gtm-strategist-skills), MIT.
- `humanizer`: [blader/humanizer](https://github.com/blader/humanizer) v3.1.0, © 2025 Siqi Chen, MIT (`.claude/skills/humanizer/LICENSE`).
- `motion-graphics-builder`: its render script and motion notes are adapted from OXYGEN-CRO's open-source content engine, MIT (`.claude/skills/motion-graphics-builder/LICENSE`).
- Fonts: Onest and Geist Mono, SIL Open Font License 1.1, with their licence files.
- Some formats and the feelings method come from studies of other creators' posts: their structures only, never their wording.

The skills, scripts and templates are MIT (`LICENSE`). Everything in `examples/` is © Diana Dobra, included as examples, and not covered by the MIT license.
