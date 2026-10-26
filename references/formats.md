# Formats

Post structures. A format is a skeleton, not wording. Choose one that fits the source; never invent a detail to complete it. `study-creator` adds structures from creators the author studies, and `outputs/log.md` shows which ones work. Many structures below came from creator studies: structure only, never their wording, voice or opinions.

| Format | Skeleton | Category |
|---|---|---|
| What broke | What happened (specific) → why → the fix → what I do differently now | authority, conversion |
| Under the hood | One claim about how X works → the 2-4 steps that make it true → what it means for you | authority |
| My setup | The tool or workflow → one specific trick → what it changed (a number, if real) | growth, authority |
| The puzzle | The big goal → the steps in order → the step people skip, and why it matters | authority |
| Before / after | A real message or artifact before → after → the one principle behind the change | growth |
| One rule | A rule → a real example → why it works | growth |
| What we cut | The feature → why we cut it → what it cost → what's there instead | conversion |
| What users do | Something real users did (anonymized) → what surprised us → what we changed | authority, conversion |
| Opinion with a reason | The claim → the evidence from my work → where I might be wrong | growth |
| Scene | Where I was and with whom → the detail that surprised me → a concrete detail → what it means → what I keep thinking about | personal, conversion |
| Customer pull | What we started with → what users kept asking for, in their words → the insight → what we built | conversion |
| Credit with receipts | Who → one dated story per person, with a quote → what it says about the team → invite others to add a note | personal |
| Before / now | For years, X meant Y → what's different now, with evidence → what it changes for you → how small the fix is | growth |
| Backstory | A hard moment from my past, with the hour, place or age → what it changed in how I work → how it shows up in the team now | personal |
| Honest update | Where we are, plainly → what we're improving, as a short list → no hype, the unglamorous work | personal, conversion |
| Unexpected room | Where I went that isn't my world → 2-4 things I learned there → what it changes for us | growth, personal |
| Then and now | A small memory from early on → what happened since, with a number → why it matters now | personal, conversion |
| How they work | A person and their path → 3-4 things about how they work that stuck with me → the result | growth |
| The whole system | What I built and why → the relevant parts in order, with artifacts or a factual diagram → what it produces (a number, if real) → the part people skip, or what I'd change | growth, authority |
| Newsjack | What just broke, with the date → what actually changed, from the primary source → one real use case or consequence from my work → what I do about it | growth, authority |
| Brandjack | What a known brand just did → what it shows, in plain words → what it means for the reader, from my work | growth |
| Namejack | Who said or did what, in their exact words → where I agree or don't, and why, from my work → the one thing readers can use | growth |
| Hot take | My actual belief → the evidence and its limits → what I do about it | growth |
| Trend | The format going around, with a subject from my pillars → my evidence → what I do instead | growth |

The last five each need the author's own use case or view. Check timeliness for news and trends; a later test can supply fresh value. Rules: `references/reach.md`.

## List explainer

The default LinkedIn layout in `linkedin-post` step 4, from a creator's posts studied for structure only. Examples 01 and 02 in `examples/outputs/posts/published/linkedin/` use it.

- **List explainer** (growth, authority): what's changing, in one line → how it works now → the plan, steps or facts as a → list → the one detail that matters → the author's view or open doubt → a short question.

Taken into the layout: the label line and list, named items ("Compute: GPUs, data centers..."), one worked example with numbers, a too-broad and a specific version of the same example, the reader's next question on its own line, and the downside or limit before the end.
Left out, because the kill list rules them out: emoji on the first line and as bullets (1️⃣ ✅ ❌), capitals for emphasis, fragment triples ("No shares. No control. No takeover."), "not X, it's Y" openers, "Here's how..." labels, mirrored closers, either/or questions, "Tell me in the comments 👇", save and send lines, hashtags, and a sources block at the end.

## Broad → narrow → niche

An optional structure, not a reach guarantee. Usually growth or authority.

- **Broad:** open with a problem or consequence the intended reader recognizes without specialist context.
- **Narrow:** show the author's actual situation and the point they want to make.
- **Niche:** explain the test, artifact, decision or fix, with its useful detail and limits.

Broad means accessible to the intended reader, not generic or aimed at everyone.
Keep the subject visible. Skip phrases such as “you need to read this” and invented suspense.
Choose a hook layout separately with `linkedin-hook`. The opening need not consume exactly two rendered lines.
A personal scene or direct technical result can use another format.

## Text-only LinkedIn posts

A test since October 2026: a pasted article says LinkedIn is trying bigger text posts (`references/reach.md`).

- **The tweet** (growth, personal): one hot take, POV ("pov: ..."), joke or small observation from the author's own material, short enough to show in full with no "...more" (about 2 lines on a phone), no visual, and no explanation of the joke. Their reasons go in their replies, as on X (`CLAUDE.md` rule 1). A retold AI exchange read as AI in the first test.
- **Instead of list** (growth): words the reader's field overuses, each with its plain word, as `word → word` lines right under the opening, no visual; keep the left side short. Columns lined up with spaces don't hold in LinkedIn's font, so arrows instead.
- **Story with a twist** (personal, growth): a long text post whose first lines set the story up and stop on the surprise right before "...more", without summing it up. Not tested yet.

## Tested structures

Testable structures from creator studies, not proven performance rules. Use the author's own material and real visuals.

- **Tested choice** (growth, authority): one real task and its criteria → options tested on the same input → visible results → choice for that task → limit. Needs the author's actual test; no universal model rankings from someone else's post.
- **Claim checked against evidence** (growth, authority): a familiar claim the author has a view on → one concrete case that tests it → what the case supports → the practical consequence. Show the artifact; distinguish evidence from opinion.
- **Decision with a concrete cost** (personal, authority): actual alternatives → what each costs in time, money or effort → the author's choice and reason → observed outcome or what remains unknown. Never invent a result to finish the story.
- **Objection tested through a case** (authority, growth): a real hesitation → starting conditions → what the author tried → visible result → what this case can and cannot answer. Never invent a common objection; take it from the author's notes or a real conversation.
- **Measured follow-up** (authority): earlier approach or published experiment → what changed since → results over a stated period → what the author will keep or change. Distinguish the intended outcome from an achieved result, and keep measurement windows consistent.

## Launch posts

- **Launch with a bet** (conversion, launch day): what launches today, in one line → how tools usually handle the problem → the bet the team made instead, and why → one thing it does, shown in a real recording → where it started, in one line → availability in one plain line. Needs the author's own words for the bet. No "X won't replace Y", app lists or capitals for emphasis. A reason to join now only when it's real (no invented scarcity).
- **Launch story** (personal, launch week only): the launch as the reason to tell the story, in the first line → each step of the path: what it was, one concrete detail, and what made the author move on → how the product started → what it does, in one plain line → the team → what they'll share from now on; the link in the first comment. The reasons to move on come from the author; a step without one gets cut, not filled.

## For X and Threads

From a creator's X and Threads playbook (`references/reach.md`).

- **Group callout** (growth): the reader's group named in the first words (people who write at work in a second language, engineers who...) → the situation they share, from the author's work → the author's view, or their own short question about the readers' experience. A broad group or a question built only for replies breaks the kill list. The author can put themselves in the group when it's true ("like me", "people like us"), and the best questions give repliers something beyond agreeing: their own case or a recommendation to share. When a group responds, come back to it with a new angle.
- **Fear line** (growth): one or two short lines that name a fear the reader already has (privacy, losing their voice, costs, a deadline) → the author's own view or a finding they have already used → no explanation; their reasons go in their replies. The same shape works for hope (a verified fact that says it can still work) and frustration (a shared annoyance, while people are talking about it). Never doom the author doesn't hold.
- **Pick a side** (growth): two groups who both read the author → their real view on which one has it right → their reason in one line. Only for a view they hold; no invented rivalry.
- **Opinion as a number**, in any of these: a ratio is fine only when it plainly reads as the author's estimate ("for me it's 90% distribution"), never as a statistic or a finding.
