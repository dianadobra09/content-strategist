/* Every visual state comes from seek(ms): no CSS animations, timers or random values,
   so the same time always gives the same frame. index.html is the finished state (the poster). */
(() => {
  const duration = 8000, posterMs = 6000;
  const firstStep = 800, stepLength = 1200, resultAt = 4500, resetAt = 7200, resetLength = 640;
  const rows = [...document.querySelectorAll('.step')];
  const marker = document.querySelector('.marker');
  const result = document.querySelector('.result');
  const rowHeight = rows[1].offsetTop - rows[0].offsetTop;
  marker.style.top = `${rows[0].offsetTop}px`;
  marker.style.height = `${rows[0].offsetHeight}px`;

  const clamp = value => Math.min(1, Math.max(0, value));
  const ease = value => value * value * (3 - 2 * value);
  const progress = (time, start, length) => ease(clamp((time - start) / length));
  const mix = (a, b, r) => a + (b - a) * r;

  // Opening: steps dim, nothing checked. Action: the marker moves down, checking each step. Then the result.
  function state(time) {
    const steps = rows.map((_, i) => {
      const enter = progress(time, firstStep + i * stepLength - 150, 300);
      const leave = progress(time, firstStep + (i + 1) * stepLength - 150, 300);
      return {reached: enter, active: enter * (1 - leave), done: leave};
    });
    const position = rows.slice(1).reduce((sum, _, i) => sum + progress(time, firstStep + (i + 1) * stepLength - 150, 300), 0);
    const markerOpacity = progress(time, firstStep - 150, 300) * (1 - progress(time, firstStep + rows.length * stepLength - 150, 300));
    return {steps, position, markerOpacity, result: progress(time, resultAt, 500)};
  }

  // Reset: fade from the finished state back to the opening, so the loop's last frame equals its first.
  function blend(a, b, r) {
    return {
      steps: a.steps.map((step, i) => ({
        reached: mix(step.reached, b.steps[i].reached, r),
        active: mix(step.active, b.steps[i].active, r),
        done: mix(step.done, b.steps[i].done, r),
      })),
      position: mix(a.position, b.position, r),
      markerOpacity: mix(a.markerOpacity, b.markerOpacity, r),
      result: mix(a.result, b.result, r),
    };
  }

  function apply(s) {
    rows.forEach((row, i) => {
      const step = s.steps[i];
      row.style.opacity = mix(0.35, 1, step.reached);
      row.style.backgroundColor = `rgba(243, 249, 224, ${step.active})`;
      const check = row.querySelector('.check');
      check.style.opacity = step.done;
      check.style.transform = `rotate(-45deg) scale(${mix(0.6, 1, step.done)})`;
    });
    marker.style.opacity = s.markerOpacity;
    marker.style.transform = `translateY(${s.position * rowHeight}px)`;
    result.style.opacity = s.result;
    result.style.transform = `translateY(${mix(24, 0, s.result)}px)`;
  }

  let current = 0, playing = false, frame = 0, origin = 0;
  function seek(ms) {
    current = Math.min(duration, Math.max(0, Number(ms) || 0));
    apply(current < resetAt ? state(current) : blend(state(resetAt), state(0), progress(current, resetAt, resetLength)));
  }
  function tick(now) {
    if (!playing) return;
    seek((now - origin) % duration);
    frame = requestAnimationFrame(tick);
  }
  function play() {
    if (playing) return;
    playing = true;
    origin = performance.now() - current;
    frame = requestAnimationFrame(tick);
  }
  function pause() {
    playing = false;
    cancelAnimationFrame(frame);
  }

  window.GraphicMotion = {duration, posterMs, ready: document.fonts.ready.then(() => {}), seek, pause, play};
  // Browser preview: plays from the start; click to pause or play.
  document.addEventListener('click', () => (playing ? pause() : play()));
  seek(0);
  play();
})();
