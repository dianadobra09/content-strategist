---
name: voice-check
description: Check that a post preserves the author's meaning and voice, serves its reader, has evidence and fits its platform. Run after humanizer.
allowed-tools:
  - Bash(python3 scripts/voice_stats.py *)
  - Bash(python3 scripts/hook_check.py *)
---

# Voice check

Paths are relative to the workspace root. If `humanizer` has not run on this version, run it first.
Read the author's voice guide, kill list and relevant samples or raw notes.

1. **Meaning and facts.** Trace claims to the author's material or the Evidence section. Keep opinions distinct from findings and goals distinct from results.
2. **The author's voice.** Preserve their vocabulary, connected sentences, asides and supported uncertainty. Follow their explicit preferences over creator examples.
3. **Substance.** Apply the value check in `generate-content` step 3 to the finished draft, including its visual. Identify the actual passage or artifact that delivers the learning. A generic takeaway fails even when the writing sounds like the author. Keep the opening's promise consistent with the body and visual. **Feeling:** the first line creates the brief's feeling and the body delivers it; run the five checks in `references/psychology.md`. A post that triggers no feeling, or a feeling bigger than its point, goes back.
4. **Natural writing.** Remove kill-list patterns and padding. Do not add vulnerability, disagreement, humor or a closing question to meet a formula.
5. **Visual.** Check that any supplied asset matches the claim, has readable labels and alt text, and follows `strategy/visuals.md`.
6. **Platform.** Check the relevant channel limits. For LinkedIn, run `python3 scripts/hook_check.py <post-file>` and assess the estimated visible opening.

If essential evidence or the author's view is missing, ask for it. Do not call an unresolved draft ready.
Cut only material that weakens clarity or repeats a point. There is no required reduction or target sentence length.
Use `scripts/voice_stats.py` only when comparison helps diagnose a voice problem. Sample averages describe their writing; they are not quotas.

Return the text and one short check line with meaningful changes and unresolved facts.
For the author's own draft, list substantive edits so they can reject them. Respect existing approvals and scoped exceptions.
