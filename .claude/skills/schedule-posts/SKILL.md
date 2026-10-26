---
name: schedule-posts
description: Schedule the author's approved posts in Zernio and keep the per-channel calendar. Use when the author says "schedule", "schedule the posts", "what's scheduled?", "move this post", or asks whether posts went out. Plans each channel's ready queue with scripts/schedule_plan.py, creates the Zernio posts with the approved text, LinkedIn first comments, Threads topic tags, Bluesky threads and visuals, and records each one in its file.
---

# Schedule posts

Paths are relative to the workspace root. Rule 14 in `CLAUDE.md` applies: approved text only, never published immediately. Scheduling uses the Zernio MCP server (`claude mcp add --transport http zernio https://mcp.zernio.com/mcp`, then `/mcp` → zernio → Authenticate).

## Rules

- **What:** only files in `outputs/posts/ready/<channel>/` (`linkedin`, `x`, `threads`, `bluesky`). Never files with `hold:`; they wait until the author releases them.
- **LinkedIn first:** never post on X, Threads or Bluesky a LinkedIn post's visual, or a post that is the core of a LinkedIn post (any version of it), before that LinkedIn post is scheduled to go out. It goes out on the LinkedIn post's day or later, and only once that LinkedIn post is scheduled in Zernio. While a LinkedIn post is on hold, all its versions and its visual wait. A link card counts as a visual. The planner enforces this and warns when a scheduled post breaks it; fix those in Zernio first.
- **Order:** LinkedIn posts its queue in number order (the author's order). X, Threads and Bluesky follow the order rule in `strategy/positioning.md`: the day's LinkedIn post on LinkedIn days, in the version with the visual so the visual goes out on every channel the same day, otherwise queue order, never a post with a version among the channel's previous 5 posts. A `planned_for` post doesn't go before its date, then goes first. The planner applies all of this; after the author adds or reorders posts, run it with `--renumber` so the X, Threads and Bluesky file numbers follow the posting order.
- **When:** the cadence and time zone in `strategy/positioning.md`. `scripts/schedule_plan.py` holds a copy of them (`TZ`, `TIMES`, `EVENING`, `CADENCE`); change both together.
- **Text:** exactly the approved text. Markdown links become bare URLs; nothing else changes. No link goes in the body as a visual: attach the video file, cut to a clip when it is over a network's limit (Zernio: LinkedIn personal 10 minutes, Bluesky 60 seconds). The planner still appends the URL of a "link card for <URL>" visual, so replace that visual with the file first.
- **First comments:** LinkedIn's `## First comment` goes in `firstComment`; it never has a link, and `## Sources` is never posted.
- **Carousels:** a LinkedIn carousel is one PDF, sent as a `document` media item with no image beside it, and `documentTitle` from the file's `Document title:` line (LinkedIn requires a title). X, Threads and Bluesky get the pages as images, in order (Bluesky takes 1 MB and 2000 px per image), with `Alt text:` for page 1 and `Alt text 2:` for page 2. Bluesky thread parts after `1/` make a thread (`threadItems`). X, Threads and Bluesky get no first reply; the planner doesn't send a `First reply:` line and warns about it.
- **Topic tags:** a Threads file's `Topic tag:` goes in `topic_tag` (1 to 50 characters, no `.` or `&`; the planner warns).
- **Visuals:** the file named in `Visual:` or `## Visual`, with its `Alt text:`.
- **Limits:** LinkedIn 3,000 characters (first comment 1,250), X 280 (a link counts 23), Threads 500, Bluesky 300 per part. Never schedule a post over its limit; tell the author.
- **Product:** posts follow `strategy/product.md`.
- **Never publish now:** every post gets an explicit future `scheduledFor` with its UTC offset. Never use `posts_publish_now` or `publishNow`, and never the core `posts_create`: it schedules minutes from now (60 by default).
- **No silent changes:** settle the planner's warnings with the author. Reorder a queue only when they ask. When they allow a post inside the 5-post window, add `repeat_ok: <date> (<why>)` to its frontmatter. When a post's text in Zernio differs from its file, ask the author which one is current before changing either.

## 1. Check

1. The Zernio tools are loaded (`accounts_list` answers). If not, ask the author to run `/mcp`, choose zernio and Authenticate, and stop.
2. Accounts: use the ids on the "Zernio accounts" line in `strategy/positioning.md`. If it still says TODO, call `accounts_list`, show the author the LinkedIn (personal profile), X, Threads and Bluesky accounts, and record the ids there once they confirm.
3. Compare Zernio with the files: `posts_get` for each `zernio_id` in `ready/` whose `scheduled:` date has come or is near, and `posts_list` with status `failed`.
   - Published: run the publication steps in `content-plan` for that file (Zernio's status counts as the author's confirmation).
   - Failed: tell the author with Zernio's reason. Retry (`posts_retry`) only when they say so.
   - Text differs from the file: ask the author which one is current, then update the other.
   - A `zernio_id` that Zernio no longer has, or a different time: ask the author before changing anything.

## 2. Plan

Run `python3 scripts/schedule_plan.py --json`. It rewrites `outputs/schedule.md` (by day and by channel) and prints the unscheduled slots with channel, `publish_at`, file, message, comments, topic, media and alt text.

Settle every warning with the author before scheduling the post it names. If a `publish_at` is already in the past, the plan is stale: rerun with `--start` set to tomorrow.

## 3. Schedule

Two generated tools do the work, run with `call_tool` (`search_tools` shows their schemas): `posts_create_post` and `media_get_media_presigned_url`. Their top-level arguments are snake_case (`content`, `scheduled_for`, `timezone`, `platforms`, `media_items`); keys inside `platforms` and `media_items` stay camelCase (`accountId`, `platformSpecificData`, `altText`).

For each unscheduled slot, in date order, create one post per file (the text differs per channel):

1. **Visual.** `media_get_media_presigned_url` (`filename`, `content_type`, e.g. `image/png`, `size`), then `PUT` the file to `uploadUrl` with `curl --data-binary @<file>` and the same `Content-Type` (no auth header; 200 means done), and use `publicUrl`. An upload expires after 7 days unless a post uses it; reuse its `publicUrl` for the other channels' posts of the same visual.
2. **Post.** `posts_create_post` with:
   - `content`: the slot's message
   - `scheduled_for`: the slot's `publish_at` (it carries the UTC offset), and `timezone`: the `TZ` in `scripts/schedule_plan.py`
   - `platforms`: one entry with `platform` (`linkedin`, `twitter`, `threads` or `bluesky`), `accountId` and, when needed, `platformSpecificData`:
     - LinkedIn: `firstComment`, the slot's comment
     - Threads: `topic_tag`, the slot's topic
     - Bluesky with comments: `threadItems`, the message and then each comment, in order, as `{"content": ...}`; the visual goes in the first item's `mediaItems` (Zernio doesn't publish the top-level `content` of a thread)
   - `media_items`: `[{"type": "image" or "video", "url": <publicUrl>, "altText": <alt text>}]`, when there is a visual
3. **Check** the stored post that the create call returns (or `posts_get`): status scheduled, `scheduledFor` at the right instant (Zernio returns UTC), the full text with its line breaks, the first comment or thread, the topic tag, the visual and its alt text.
4. **Record** it in the file's frontmatter (add the `---` block if the file has none): `scheduled: <publish_at>` and `zernio_id: <the post's _id>`.

X charges each post at its API price, passed through by Zernio: $0.015, or $0.20 for a post with a link (checked October 2026).

When done, rerun the planner so `outputs/schedule.md` shows the ✓ marks.

## Changes

- **The author edits the file of a scheduled post:** `posts_update` with the new `content`, then check with `posts_get` that the first comment, topic tag and visual are still there.
- **The author moves or removes a scheduled post:** `posts_update` with the new `scheduled_for` (ISO 8601 with the offset), or `posts_delete`, and check with `posts_get`. Change or remove its `scheduled:` and `zernio_id:` lines, then rerun the planner.
- **New ready posts:** they join each queue as `CLAUDE.md` describes. Rerun the planner and schedule the new slots.
- **A hold ends** (the author says so): with their OK, remove the `hold:` lines, rerun and schedule.

## Report

Per channel: how many posts were scheduled and their date range, anything not scheduled and why, and what the author should check in Zernio.
