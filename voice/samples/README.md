# Samples

The author's own writing, verbatim. The source of truth for their voice. Only text the author wrote goes here: no AI drafts, even edited ones, unless the author rewrote them and says they're their own.

## Format

One entry per post, under a `## ` header. Keep line breaks exactly.

```
## 2026-09-12 | best
<the post, exactly as published>
> results: 4,200 impressions, 31 reactions, 9 comments
```

- `best` marks posts the author is proud of. Skills read these first.
- Lines starting with `> ` are notes; `scripts/voice_stats.py` ignores them.

## Files

- `linkedin.md`, `x.md`, `bluesky.md`, `threads.md`: posts per platform.
- `other.md`: Slack messages, emails, PR descriptions, talk or voice memo transcripts. Useful when there aren't many posts yet; spoken voice is a good reference.

## Getting posts out

- LinkedIn: Settings & Privacy > Data privacy > Get a copy of your data. Posts are in `Shares.csv`. Or paste them.
- X: Settings > Your account > Download an archive of your data. Posts are in `data/tweets.js`. Or paste them.
- Bluesky: give the handle; `train-voice` reads public posts from the Bluesky API.
- Threads: paste them.
