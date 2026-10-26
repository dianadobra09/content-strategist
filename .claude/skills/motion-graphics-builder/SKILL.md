---
name: motion-graphics-builder
description: Build a short looping animated graphic for a post from editable HTML, and export an inspected MP4, GIF and still PNG. Use for "animate this", "make it move", "make a GIF", a motion graphic or an animated diagram. Not for screen recordings or edits of real footage.
allowed-tools:
  - Bash(node .claude/skills/motion-graphics-builder/scripts/render.mjs *)
---

# Motion graphics builder

Paths are relative to the workspace root. Rule 10 in `CLAUDE.md` and `strategy/visuals.md` apply: the animation explains a real process or change from the author's material. It never imitates a product screen, a result or a measurement.

## When motion helps

Use it when change is the point: input becoming output, steps completing, a before and after, cause and effect. A list, a quote or a single number stays a still.
Show one main action per graphic. If the idea needs two, split it or make a still.

## 1. The still

State the one thing the reader should understand after watching.
Copy `template/` (index.html, motion.js, animation.json, fonts/) into `outputs/visuals/<post-slug>/`. It uses the brand guidelines of BlinkWrite, the product of the workspace's original author: its fonts, colours and margins, without a logo or product name. Change them in `index.html` to your own brand's. If the folder already has an `index.html`, give the scene another name and set `entry`.
Replace every placeholder, including the `aria-label`. Write `index.html` in its finished state: that page is the poster, so it must work as a still on its own and stay readable at phone size (body text near 32 px at 1080 wide).

## 2. The motion

Read `references/motion.md`. Plan the timeline: opening, one action, a 2–3 s hold on the finished state, reset; 6–10 s in total.
Write it in `motion.js`: every visual state comes from the time passed to `seek(ms)`.
Set `animation.json`:
- `duration` and `posterMs`, the same as in `motion.js`; the poster time falls in the hold
- `reviewTimes`: one per phase
- `seamless` when the last frame equals the first
- `gif`: `null` for no GIF
- `name` when the exports shouldn't take the folder's name
- `motionClipClasses` for elements that hide text on purpose during the motion

## 3. Render

The first time on a machine: `npm ci --prefix .claude/skills/motion-graphics-builder/scripts`, then `npx --prefix .claude/skills/motion-graphics-builder/scripts playwright install chromium`. ffmpeg comes from Homebrew.

```
node .claude/skills/motion-graphics-builder/scripts/render.mjs outputs/visuals/<post-slug>/animation.json
```

The exports go next to the source: `<name>.mp4` (1080 × 1350, 30 fps), `<name>.gif` (720 × 900, 20 fps) and `<name>.png` (the poster). `review/` gets a contact sheet, a phone-size poster, the review frames and `report.json`; git ignores it.
The render stops and keeps the old exports when text falls back to another font, leaves the canvas or is cut off; a file is missing or online; seeking to the same time twice changes the frame; a seamless loop doesn't end where it started; or an encoded file doesn't match the settings.

## 4. Review and fix, up to three passes

Look at `review/contact-sheet.png` and `review/poster-phone.png`, and answer from what you see:
- What does the eye land on first, and is it the main point?
- Can the reader follow the action from the large labels alone?
- Does the motion show the change, or only reveal items one by one?
- Is the poster useful once the motion stops?
- Can every label be read at phone size?

Fix the biggest problem, render again and look again. After three passes, show the author the MP4 and the poster with what is still open. A clean render report means the export worked, not that the design is good.

## 5. Deliver

In the post's Visual section, link the MP4, GIF and PNG, and write alt text that says what changes and what the result is. Record the sources, what is illustrative, the timeline and the render command in `asset-sources.json`, like the other visual folders.
Attach the MP4 on every channel (`schedule-posts`). The GIF is an option: X takes one GIF up to 15 MB and 1280 × 1080 (checked 2026-10-19). Check another channel's GIF limits before using it there.
