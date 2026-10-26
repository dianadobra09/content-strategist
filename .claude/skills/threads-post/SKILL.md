---
name: threads-post
description: Write Threads posts from one of the author's LinkedIn posts, a draft or their material. Use whenever the author mentions Threads, asks for a Threads version, or wants a LinkedIn post repurposed for Threads (Meta's app, not an X thread). Writes one short, conversational post per point, in their words, within 500 characters each, with no first reply.
---

# Threads post

Paths are relative to the workspace root. Apply `linkedin-post` steps 1–2 with Threads samples and the shared rules in `CLAUDE.md`.
If Threads samples are absent, use the approved LinkedIn text, the author's raw notes and their stated voice preferences.
Read the Summary and "What this means" in `references/threads.md`; the rest holds the evidence and its limits.

## Pick the points

By default, Threads leans on personal points, thought leadership, building in public and founder insights (the Threads row in `strategy/positioning.md`).
Start from the post file: Source, Brief, Evidence and the LinkedIn version. Write the Threads posts separately from the X posts. They can share a sentence, but not as the rule: never reword the author's line only to make the two differ.
If its `channels:` line leaves Threads out, say why and ask before writing it.
If the author pastes a LinkedIn post that has no post file, create one in `outputs/posts/drafts/` with their text verbatim under `## Source`.
Write one post per point a Threads reader can use without the LinkedIn context. A point is usually the author's moment, their opinion or one concrete observation from their work, with the detail that makes it theirs: the number, the example, what someone said. A post with one point gets one post.
Leave out the setup and supporting research unless a point needs them.
Threads readers are more skeptical of AI than X's: AI posts here lead with the limits or the human side, and builder or tooling angles go to X (a creator's X and Threads playbook, `references/reach.md`). Pick points a stranger cares about, not inside talk only their circle would get.
Keep the author's sentences where they work. Choose what to keep rather than squeezing every LinkedIn paragraph into fewer words.
No sentence appears in two posts of the set, so each one tells a follower something new.
If nothing in the post stands on its own in a few sentences, say so and suggest skipping Threads for it.

## Write

Write each post for Threads rather than pasted from LinkedIn. The limit is 500 characters, emojis included. Most posts that did well were under 200, but length alone didn't decide it, so let the point set the length.
Use one or two paragraphs at most, with a blank line between them. The author's question ends the last paragraph. No list or header unless the material is a real sequence.
Open with the point. The feed shows the whole post, so there is no cut-off line to write toward.
The point carries one feeling from `references/psychology.md`, created in the first line.
When the reader is a clear group, name it in the first words (Group callout in `references/formats.md`). A one-line opinion the author holds, or a Fear line, can be the whole post, and "unpopular opinion:" can open a belief they hold that really splits people (a test).
Stop when the point is made, or end with the author's own short question. Questions drew replies in the study but not more engagement overall, so don't add one.
Skip Threads' reply-bait formats: "let's connect" lists, "Dear algo" posts, "drop your link" or "drop your product", "what are you building?" and "comment X". Meta limits engagement bait, and they break the kill list's ending rules.
Use a chain only when each post adds a distinct step or detail, as on X.
Don't move the LinkedIn text into a text attachment unless the author asks: readers have to tap to open it, and the post should stand on its own.

## Links, tags and visuals

No first reply with links or sources. Leave links out of the post too unless the author asks: Meta says links aren't downranked, but people like and reply to them less, and posts with a link in the post did worse in the study.
Add one topic tag when an existing tag fits the reader, for example AI Threads, Tech Threads or Software Engineering. Threads allows one per post; never a hashtag block.
Text alone is the default. Put the post file's visual on the one post it supports: the author's photo, a real screenshot, a meme they picked or a factual diagram, with alt text. Follow `strategy/visuals.md`.
Don't make a quote post the main version; quote posts did worst in the study.

## Finish

Product mentions follow `strategy/product.md`. Keep any `hold:` line.
Run `humanizer`, then `voice-check`, once.
Save under `## Threads` as `### Post 1`, `### Post 2` and so on, with each post's topic tag and visual below it. A set replaces an earlier single post.
Threads posts written for a ready post wait for the author's approval; note that in Check. Once they approve them, mix them into `ready/threads/` as `CLAUDE.md` describes. Leave the other platforms as they are.
Show each post with its character count, topic tag and visual or asset link. Check the composer when emoji or links make the count uncertain. Suggest mixing a set with other topics rather than posting it in a row.
