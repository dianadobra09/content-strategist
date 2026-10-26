---
name: train-voice
description: Teach the content strategist the author's voice. Use when the author shares posts, a profile, a data export or other writing of their own (Slack messages, emails, voice memos); pastes or edits the version actually posted; or corrects a draft ("too corporate", "I'd never say that"). Updates samples, voice guide, kill list and feedback log.
allowed-tools:
  - Bash(python3 scripts/voice_stats.py *)
  - Bash(python3 scripts/compare.py *)
  - Bash(curl -s -G https://public.api.bsky.app/*)
---

# Train voice

Paths are relative to the workspace root. Only the author's own writing trains the voice. Other people's profiles go to `study-creator`.

## A. New samples

1. Get the text:
   - Pasted posts or files: as given.
   - LinkedIn data export: posts are in `Shares.csv`, column `ShareCommentary`.
   - X archive: `data/tweets.js` (`tweet.js` in older archives). Skip replies and reposts unless the author wants them.
   - Bluesky: `curl -s -G https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed -d actor=<handle> -d filter=posts_no_replies -d limit=100`. Text is in `feed[].post.record.text`; skip items that have `reason` (reposts).
   - Threads: ask the author to paste them.
   - LinkedIn and X profile pages need a login: ask the author to paste posts or export them.
2. Save verbatim to `voice/samples/<platform>.md` (format in `voice/samples/README.md`). Keep line breaks. Skip duplicates. Ask the author which are the best and mark them `best`. Add results if the author has them.
3. Run `python3 scripts/voice_stats.py voice/samples/<platform>.md`.
4. Read the samples. Update "Observed patterns" in `voice/voice-guide.md` for that platform: the script's numbers, openers, closers, recurring phrases, things the author never does, with 1-2 short quotes as evidence.
5. Propose changes to the point of view, rules and kill list. Add them only after the author approves.
6. Report what you learned in 5-8 bullets.

## B. Draft vs what the author posted

1. Get both: the draft from the post file, and the author's final (pasted, or edited in the file).
2. Run `python3 scripts/compare.py` with the draft, a line `=====`, then the final, on stdin.
3. Name each change as a pattern: "cut the setup line", "'crucial' → 'important'", "list turned into a story", "added a personal detail".
4. Add a row to `voice/feedback-log.md`.
5. Repeated edits can suggest a preference. Record their context; do not turn a one-post choice into a universal ban. Apply explicit feedback directly. Ask before generalizing an uncertain pattern.
6. Add eligible final text to `voice/samples/<platform>.md` using `voice/samples/README.md`. Publication or approval alone does not turn an AI draft into author-written voice evidence. Keep its edits in the feedback log instead.

## C. Direct feedback

"Too corporate", "I'd never say X", "shorter": add the rule now, log it in `voice/feedback-log.md`, redo the draft.

## Progress

Use draft-versus-final similarity only as a description of text overlap. It does not measure voice accuracy or prove that learning is complete.
Track recurring corrections and the author's own assessment over time. Preserve context and allow their preferences to evolve.
Report scores only when useful, alongside what changed. Do not optimize for a score or an arbitrary sentence-length target.
