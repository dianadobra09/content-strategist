---
name: generate-content
description: Develop useful posts from the author's notes, work, questions or a source. Use for content ideas and post requests without a named platform. Select material, collect evidence and route to the channel skills.
allowed-tools:
  - WebSearch
  - WebFetch
---

# Generate content

Paths are relative to the workspace root. Shared rules and the post template are in `CLAUDE.md`.

## 1. Read the context

Read `strategy/positioning.md` (with the ICP and its problems), `strategy/product.md`, the voice guide and kill list, `references/formats.md` and `references/psychology.md`.
For planning, also read open ideas, open angles, the ready queue and the last ten published entries per platform.
Use `references/reach.md` for optional angle tags, not predicted performance.

## 2. Find material

If the author supplied a clear topic and purpose, work on it directly. Do not make them select it again.
Otherwise, start with their notes and real work: a decision, failure, useful explanation, personal moment or result. Prefer material on a problem from the ICP list in `strategy/positioning.md`.
Consult used ideas and published posts for follow-ups with new evidence. Keep each follow-up separate and link its source.
Use `repurpose` for a long source. Research external material only when it serves the author's question or experience.
News and trends are optional. Check their dates and relevance; a later hands-on result can still be useful.

## 3. Check the value

For each candidate, identify:

- One reader in a specific situation.
- One useful takeaway: a choice, explanation, method, result or personal observation.
- The author's contribution, in their words: what they experienced, believe, tried or decided.
- A concrete example or verified finding that supports it.
- The feeling it triggers: one for the first line, one for the body (`references/psychology.md`). Every post has one.
- Would the author send it to someone from the ICP? If not, it isn't useful enough yet.

For an insight or learning post, state what the reader can understand, judge or do afterward.
Point to the passage or artifact that delivers it: an explanation, usable method, failure condition, trade-off or evidence-backed observation.
A slogan such as “review AI output” is insufficient without what to check, why it matters or a concrete failure.
An anecdote or statistic alone is not the learning. Explain what it supports and where the conclusion stops.
If the takeaway stays generic after the polished wording is removed, ask for the missing substance or park the idea.
Do not manufacture a surprising conclusion. A clear explanation of a familiar problem can be valuable.
Personal posts can share a specific, meaningful experience without forcing an instructional lesson.

A familiar subject qualifies when the author adds a useful example, explanation or trade-off.
Reject copied summaries, unsupported advice and generic slogans. Check the worn-out topics in `voice/kill-list.md`.
A new opening alone does not make a follow-up. New evidence or a changed decision does.
Apply the personal-account and product rules in `CLAUDE.md`.

## 4. Collect evidence

Use the author's supplied material or relevant files they have authorized you to inspect. Never invent their experience or opinion.
For external claims, read the primary source and record its link, date and the exact claim it supports.
Verify facts that can change when drafting. Search to check facts, not to require an unprecedented opinion.
When the author's notes get a fact wrong (a date, a name, a number), correct it in the post and say so in Evidence.

For a case, comparison or result claim, collect:

- Starting problem or input.
- What the author changed or compared; common criteria for comparisons.
- Actual output and supporting artifact.
- Limits and, for measured change, the observation period.

Separate a goal, work in progress and an observed result. A personal story does not require a number or experiment.
If essential material is missing, ask up to three short questions together and wait before drafting.
Save incomplete ideas in `ideas/open/` with the missing evidence. Do not fill the gaps with invented text.

## 5. Select

When the author wants options, show up to three strong candidates. Do not pad the list.
For each, give the reader and situation, takeaway, the author's contribution, evidence available or needed, feeling, category, format and visual direction.
Rank relevance, evidence and fit with the author first. Use category balance and timing to choose among strong candidates.
A useful follow-up has no automatic penalty. Keep the existing ready queue unless the author asks to change it.
Recommend one. Let the author choose unless they have already chosen or delegated the choice.

## 6. Draft and save

Use `linkedin-post` by default. Create X, Bluesky and Threads versions when requested or included in the agreed plan.
Use the chosen channel skill and `strategy/visuals.md`. A visual can supply part of the explanation or evidence.
Each version receives one `humanizer` pass followed by `voice-check`; do not repeat finished passes at each routing step.
Save the post and its brief using `CLAUDE.md`. Keep only the requested platform sections.
Move the source idea to `ideas/used/` with a dated link to the draft. Save unchosen useful angles without duplicates.
The author approves ready posts and publishes them. `content-plan` logs publication; `train-voice` records their edits.
