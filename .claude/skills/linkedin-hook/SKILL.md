---
name: linkedin-hook
description: Choose a supported opening from a LinkedIn draft in one of four hook layouts. Use for hooks, first lines and mobile truncation checks. Writes hooks, not full posts.
allowed-tools:
  - Bash(python3 scripts/hook_check.py *)
---

# LinkedIn hook

Paths are relative to the workspace root. Read the voice guide, kill list and relevant hook feedback.

## Choose the opening

Read the finished draft and its visual before choosing the opening.
Find the strongest supported reader problem, consequence, result, claim or personal moment.
The opening creates the post's first feeling at once (`references/psychology.md`): recognition opens on the moment the reader knows, discomfort on the uncomfortable fact, curiosity on the gap between what the reader expects and what happens. Specific beats general: a real number, name, time or outcome. Two feelings at most.
Two openings from a creator's X and Threads playbook are worth a candidate when they fit (tests on LinkedIn, `references/formats.md`): the reader's group named in the first words (Group callout), or a short line naming a fear, hope or frustration the reader already has (Fear line), with the full post below it. "Unpopular opinion:" stays off LinkedIn.
For Broad → narrow → niche, make the opening accessible without hiding the subject. Narrow through the author's case into practical detail.
Broad means recognizable to the intended reader, not vague or interesting to everyone.

Use the author's wording where it works. Include their first line as a candidate, marked `(yours)`.
Do not replace an approved opening unless the author asks. Explain any proposed change briefly.
Add no fact, opinion or promise absent from the material. The body and visual must deliver the opening's promise.
If the material cannot support a useful opening, name the missing detail and ask for it.

## Four layouts

These are layout choices, not performance rankings. Character targets are rough guides; do not pad text to fill them.

- **Dense:** continuous text, often about 140–160 characters, for a point that needs its context together.
- **Punchy+Context:** a short first line, blank line, then context. Aim for about 50 characters in the first line.
- **Single-Line Bomb:** one specific short sentence, about 45 characters or fewer, then a blank line before the body.
- **Stacked:** two or three lines without a blank line between them. Each adds information; avoid mirrored phrases.

Keep the chosen layout name in `hook:`. The author's natural phrasing applies to every layout.
A technical visual can carry part of the explanation, but the opening still needs a recognizable subject.

## Preview

Run `python3 scripts/hook_check.py <post-file>` for the post, or pass hook candidates on stdin separated by `=====`.
The script estimates mobile and desktop wrapping from the width model in `.claude/skills/linkedin-hook/references/width-model.md`. It is not a live LinkedIn preview.
Device, font, media and interface changes can alter the cut. Inspect the actual composer when available.

Read the visible portion: does it name a subject and give a reason to continue?
A complete sentence at the cut is fine. Do not manufacture a cliffhanger or remove a necessary qualification to fit.
Review the first 50 words for clarity. This is an editorial check, not a claim about LinkedIn's ranking algorithm.

## Output

Show up to three distinct options, ranked. One is enough when it clearly fits.
For each, show the exact line breaks, layout, script character count, estimated cut, the feeling it creates and a short reason.
Save the options under `## LinkedIn hooks` and identify the one in the draft. `examples/ideas/used/2026-10-21-character-ai-bankruptcy.md` shows a finished set.
Record the author's corrections with `train-voice`.
