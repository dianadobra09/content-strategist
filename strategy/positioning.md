# Positioning

Fill this in first; every skill reads it. Ask Claude "help me fill in my positioning" and answer its questions. The category mix, platform roles and long-term approach below are working defaults from the original setup: keep, change or delete them.

## Position

TODO: one or two sentences. Who you are and what you share. Example: "Senior engineer building an AI product from zero, sharing what I learn about AI, engineering and shipping along the way."

Focus: TODO (subjects you post about)

## Pillars

| # | Pillar | Covers | Role |
|---|---|---|---|
| 1 | TODO | TODO | Authority. Lead with it. |
| 2 | TODO | TODO | Signature angle |
| 3 | TODO | TODO | Reach: broad enough for people who don't know you |
| 4 | TODO, e.g. building your product in public | Launch, what users do, what you cut, what went wrong | Conversion |

## Post categories

Every post is one of four, set as `category:` in the post file. Whatever the category, the post says what the author really thinks or what happened to them (`CLAUDE.md` rule 1).

| Category | Share | Its job | The post | Ending |
|---|---|---|---|---|
| growth | 40% | Catch the attention of people who don't know the author yet | Needs no context: one thing the reader can use, or a supported point relevant to their work | No ask |
| authority | 30% | Show what the author knows | A framework or method they use, how something works inside, a trade-off, or a real result, measured when relevant | Optional: the doc, spec or repo named in the LinkedIn first comment, without a link |
| personal | 20% | Make readers remember the author as a person | Their own moment, mistake, habit or lesson, with the details only they know | No ask |
| conversion | 10% | Show readers the door | A real lesson, decision or user finding from the product, with the product visible | One plain line about the product |

Check the mix over the last 10 posts on each platform: 4 growth, 3 authority, 2 personal, 1 conversion. It is a guide, not a quota.

## Audience

- TODO: who reads, and which pillars they care about

## ICP

TODO: the one reader the posts are for, in your own words: their role, team, tools, what they're asked all day, what they want.

Pick post topics from the problems below and write for this reader. Test each post: would the author send it to someone like this?

| # | The reader's problem | What you know or build that helps | Posts |
|---|---|---|---|
| 1 | TODO | TODO | none yet |

## Platforms

Starting assumption; adjust from `outputs/log.md`.

| Platform | Role | Best pillars |
|---|---|---|
| LinkedIn | Main. Every idea starts here. | All |
| X | Tech and builder crowd: opinions and one point per post | TODO |
| Bluesky | Engineering and practical discussion with peers: what broke, privacy, internals. AI-tooling posts go to LinkedIn and X. | TODO |
| Threads | Short, conversational posts of one or two paragraphs: personal points, thought leadership, building in public, founder insights | TODO |

## Long-term approach

This is a long game, and the content needs to sound like the author.
Most content must give valuable insights or real learnings, not generic statements that only read nicely.
Growth and authority posts deliver a concrete understanding, decision aid or useful action backed by specific material.
Personal posts keep room for meaningful experiences without a forced lesson or a product pitch.
Build recognition through recurring work, judgment, interests and language. Let new evidence create follow-ups.
A plain account of unfinished work can be useful when its status and limits are clear.
Choose a sustainable cadence and evaluate useful conversations, voice fit and effort alongside reach.
Each post serves one reader in one situation. It need not appeal to all audiences at once.

## Cadence

The defaults below are copied in `scripts/schedule_plan.py` (`TZ`, `TIMES`, `EVENING`, `CADENCE`); change both together.

- LinkedIn Tuesday, Wednesday and Thursday at 15:00. X and Threads Monday to Friday, Bluesky Monday to Thursday, at 19:00. Time zone: Europe/Bucharest.
- Each channel has its own `ready/<channel>/` queue. LinkedIn posts in its queue order.
- On a LinkedIn day, X, Threads and Bluesky post their version of that day's LinkedIn post, the one with the visual, so the visual goes out on every channel the same day. On other days, or when a channel has no version of it, the next post in the channel's queue.
- Nothing goes out on X, Threads or Bluesky before its LinkedIn post: neither a version of it nor its visual. A link card counts as a visual.
- A post never goes out while a version of the same post is among the channel's previous 5 posts.

## To fill (Claude asks when a task needs it)

- Zernio accounts (ids): TODO (`schedule-posts` fills them in from `accounts_list`)
- Handles: LinkedIn TODO · X TODO · Bluesky TODO · Threads TODO
- X Premium (long posts)? TODO
- Topics, people or companies never to post about: TODO
- Bluesky custom feeds to reach: TODO
