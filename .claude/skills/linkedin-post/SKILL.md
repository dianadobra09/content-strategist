---
name: linkedin-post
description: Draft or edit a LinkedIn post from the author's material, with a fitting structure, hook and visual. Preserve their voice, ask for missing evidence and save a reviewable draft.
---

# LinkedIn post

Paths are relative to the workspace root. Shared rules and the post template are in `CLAUDE.md`.

## 1. Read

Read the voice guide, kill list, positioning, relevant formats and `references/psychology.md`.
Read two or three `best` LinkedIn samples when available, otherwise the author's own samples or raw notes.
Without samples, use their explicit preferences and supplied words. Do not promise an accurate voice match or default to generic copy.
Read `strategy/product.md` when the post touches the product.

## 2. Check the material

Apply `generate-content` steps 3–4: reader and situation, useful takeaway, the author's contribution and supporting evidence.
For a title-only idea, ask for a few raw sentences or a voice memo before drafting.
Ask only for missing information, up to three questions together. Never compose an opinion for the author to approve.
Record the short brief, pillar, category, format and feeling in the post file. Reach tags are optional.

## 3. Draft with a visual in mind

Choose the format that fits from `references/formats.md`: what goes in, and in what order. Do not force a universal narrative. Step 4 sets the layout.
For an accessible technical explanation, consider Broad → narrow → niche: reader problem, the author's case, useful detail.
A personal scene, direct result or short artifact-led post can start more specifically.

- Make the reader feel the brief's feeling: the first line creates the first one, the body adds the second (`references/psychology.md`). Run its five checks before finishing.
- Preserve the author's sentences, asides and meaning. Edit their supplied draft minimally.
- Follow the voice guide on case and openings. Use connected sentences, laid out as in step 4.
- Make the opening understandable to the intended reader. Give a problem, consequence, scene or result before unnecessary terminology.
- Keep necessary uncertainty. Do not turn a limited finding into an absolute claim or manufacture disagreement.
- Use names and news only when they help explain the point, not as mandatory first-line ingredients.
- Keep the author's closing question. Without one, end with a short question about the reader's own experience if there is a real one to ask (examples 01 and 02), or stop when the point is made (example 03). No generic engagement question.
- Let length follow the material. A screenshot-led post can be shorter than 80 words. Keep LinkedIn text within 3,000 characters.
- No links in the first comment. Name a source there only when readers will want it, and keep the URLs under `## Sources` in the ready file, which is never posted. LinkedIn hasn't published a rule on this; outside estimates of the reach cost vary.
- No hashtags. Mention only people whose work or role is relevant.

The product can be named once, plainly, where it fits the post's problem, in any category. `strategy/product.md` still applies.
A useful technical resource can support the post; it does not require a sales ending.

Read `strategy/visuals.md`. Choose a photo, artifact, diagram, chart, carousel, recording or no attachment for a stated purpose.
For each visual, record its source, the point it shows, creation or capture instructions, and alt text.
If the author asks for a finished visual and the source is available, create and inspect it using that workflow.

## 4. Lay it out

Use the layout of the example posts in `examples/outputs/posts/published/linkedin/` (examples 01–03 below). It comes from creator posts studied for structure only (`references/formats.md`, List explainer).

- **Opening.** The claim, the number or the moment, in a short first line. `linkedin-hook` sets the final opening in step 5.
- **Context.** One to three sentences after it: the reader's problem, or what is happening and why it matters to them.
- **Short paragraphs.** One or two sentences each, one point each, with a blank line between them.
- **Lists.** Put each real list in the material on → lines under a label line: steps, a plan, facts from a source, reasons, parts of a setup, examples.
  - The label names what follows and ends with a colon: "how it works:", "the plan:", "the setup:", "why that matters:". The author's own sentence can end with the colon instead. No "Here's what..." or "Here's why:" labels.
  - One point per line, concrete: a number, a name or a date where the source has one. Lowercase unless the line starts with a name, and no full stop at the end. When the items are named things (tools, layers, options), start each with the name and a colon.
  - No blank line between the label and the list. Use the real number of items. A second list is fine when there is a second real list.
  - Arrows only: no numbered items, no emoji bullets (1️⃣ ✅ ❌), no bold.
- **After a list.** One line with the detail that matters or what it adds up to: "researchers call this mode collapse." (example 01).
- **A worked example.** After a general point, one concrete case with its numbers, like the random number between 1 and 10 in example 01. A too-broad and a specific version of the same example also work, as two → lines instead of ❌ and ✅. A made-up case reads as one ("think about...", "take...") and never as something that happened.
- **The reader's next question.** A question the reader would ask can get its own line, answered right below it: "so what should we do?". Never as the first line.
- **The author's part.** Their view, open doubt or the limit of the finding, in their words, usually after the facts: "I've never used it, but I am interested in what's going on." (example 03).
- **Ending.** The closing question on its own line. If the first comment names a source, a last line says what is there: "the repo in comments".
- **Leave out:** hashtags, "save this" or "send this to..." lines, "tell me in the comments", 👇 or any emoji the author didn't write, words in capitals for emphasis, and a sources or disclaimer block. Sources go under `## Sources` in the file, or are named in the first comment.

Short personal posts keep the author's own layout. A post without a real list gets no label or list.
In the author's own draft, re-line their sentences and keep their words; only a label line is new. Show it as an edit they can reject.

## 5. Set the hook

Run `linkedin-hook` on the draft and visual concept. Keep the author's first line among the candidates.
Select the strongest supported opening for the intended reader, one that creates the brief's first feeling, not merely the biggest number.
Save up to three genuinely different options under `## LinkedIn hooks` and set `hook:` to the selected layout.
Respect an already approved opening. Offer an alternative without silently replacing it.

## 6. Finish

Run `humanizer`, then `voice-check`, once. If edits change the opening, repeat the hook preview.
Save using the post template in `CLAUDE.md`. Show the post, selected hook, visual or asset link, and any unresolved facts.
Keep alternative hooks concise. Offer other platforms only when useful; do not generate them unless requested.
