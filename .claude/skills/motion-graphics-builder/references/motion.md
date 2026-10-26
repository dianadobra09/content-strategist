# Motion rules

Adapted from `skills/graphics-designer/references/motion-and-export.md` in OXYGEN-CRO's open-source content engine (commit 4bb350c, MIT; see `../LICENSE`).

## Timeline

- Plan four phases: opening, action, hold, reset. For a feed graphic, 6–10 s with a 2–3 s hold on the finished state is a starting point, not a platform rule.
- Make the first frame work without the motion: headline and layout readable, the main object in its starting state. A viewer may scroll on before the action starts.
- Animate one main action. Keep the headline, labels and takeaway still. No competing loops, moving backgrounds or pulsing calls to action.
- Keep objects continuous: the same item travels from input to output, a selected field becomes a filter, a row passes a check and lands in the result. Don't swap in new objects mid-action.
- Give moving, arriving and resting different timing: about 300–600 ms per move, eased in and out, with a pause after each arrival.
- Show a missing or failed case as missing or failed; never animate it into a success. Timing is illustrative unless it comes from a measured run; say so when the post could read it as a benchmark.
- Hold the finished state long enough to read every label, then reset quickly. Call the loop seamless only when the last frame equals the first.
- Revealing tiny labels one at a time doesn't make a dense graphic readable. Cut content or split the graphic.

## Same frame for the same time

The page defines `window.GraphicMotion = {duration, posterMs, ready, seek, pause, play}`. `seek(ms)` sets every visual property from `ms` alone: positions, opacity, colours, counters, classes. No CSS transitions or animations, `setTimeout`, `Date.now()` or `Math.random()`. The renderer checks that seeking back to a time gives the same pixels.
Give every element that moves or fades `will-change: opacity, transform`. Without it, Chrome draws the same frame slightly differently depending on the frame before.
Write the HTML in its finished state, so the page without motion is the poster; `motion.js` sets only what differs earlier in the timeline. `play()` loops the preview in a browser (click to pause); the renderer pauses it and seeks each frame.

## Encoding

- MP4: H.264, 1080 × 1350 at 30 fps, limited-range BT.709 so players don't shift the colours, no audio.
- GIF: 720 × 900 at 20 fps, one palette for the whole sequence, ordered dithering so flat colours stay steady. GIF frame timing is in hundredths of a second, so only 10, 20 or 25 fps keep exact timing.
- A GIF that's too large: first remove changing pixels that carry no meaning (moving shadows, gradients, texture), then shorten it, then lower its size or fps. Check readability after each cut and report the real file size.
- The PNG poster is the still for alt text and for places where motion doesn't play.
