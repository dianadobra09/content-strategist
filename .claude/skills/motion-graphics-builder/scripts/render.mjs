// Renders an animated HTML scene to MP4, GIF and a still PNG after checking fonts, layout, seeking and the loop.
// Adapted from brand/render-animation.mjs and brand/browser.mjs in OXYGEN-CRO's open-source content engine
// (commit 4bb350c, MIT; see ../LICENSE).
// Usage: node render.mjs <scene folder>/animation.json [--keep-frames]
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {chromium} from 'playwright';

const args = process.argv.slice(2);
const configArg = args.find(arg => !arg.startsWith('--'));
if (!configArg) throw Error('Usage: node render.mjs <scene folder>/animation.json [--keep-frames]');
const configFile = await fs.realpath(path.resolve(configArg));
const root = path.dirname(configFile);
const config = JSON.parse(await fs.readFile(configFile, 'utf8'));
const ffmpeg = process.env.FFMPEG || 'ffmpeg';
const inside = (dir, file) => file.startsWith(dir + path.sep);
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

const entry = await fs.realpath(path.resolve(root, config.entry || 'index.html'));
if (!inside(root, entry)) throw Error('entry must be inside the scene folder.');
for (const field of ['width', 'height', 'duration', 'fps', 'posterMs']) {
  if (!Number.isInteger(config[field]) || config[field] <= 0) throw Error(`${field} must be a positive whole number.`);
}
if (config.width % 2 || config.height % 2) throw Error('width and height must be even for H.264.');
if (config.posterMs > config.duration) throw Error('posterMs is after the end of the animation.');
const frameCount = config.duration * config.fps / 1000;
if (!Number.isInteger(frameCount)) throw Error('duration must hold a whole number of frames at fps.');
const gif = config.gif || null;
if (gif) {
  // GIF frame delays are whole hundredths of a second.
  if (![10, 20, 25].includes(gif.fps)) throw Error('gif.fps must be 10, 20 or 25.');
  if (!Number.isInteger(gif.width) || gif.width <= 0 || gif.width > config.width) throw Error('gif.width must be a whole number no wider than the scene.');
  if (!Number.isInteger(config.duration * gif.fps / 1000)) throw Error('duration must hold a whole number of frames at gif.fps.');
}
if (!Array.isArray(config.fontFamilies) || !config.fontFamilies.length) throw Error('List the fonts the scene uses in fontFamilies.');
const name = config.name || path.basename(root);
const selector = config.selector || '.art';
const gifHeight = gif && Math.round(config.height * gif.width / config.width);
await run(['-version']).catch(() => { throw Error(`ffmpeg not found at "${ffmpeg}". Install it with "brew install ffmpeg" or set FFMPEG.`); });

const temp = await fs.mkdtemp(path.join(os.tmpdir(), 'motion-graphics-'));
await fs.mkdir(path.join(temp, 'frames'));
await fs.mkdir(path.join(temp, 'review'));
const errors = [], requested = new Set();
const browser = await chromium.launch({headless: true});
// Chrome's raster can differ by a few colour levels between identical frames; a real state bug differs by far more.
const tolerance = 12;
let success = false;
try {
  const scratch = await browser.newPage();
  const difference = (a, b) => scratch.evaluate(async ([a, b]) => {
    const pixels = async base64 => {
      const bitmap = await createImageBitmap(await (await fetch(`data:image/png;base64,${base64}`)).blob());
      const context = new OffscreenCanvas(bitmap.width, bitmap.height).getContext('2d');
      context.drawImage(bitmap, 0, 0);
      return context.getImageData(0, 0, bitmap.width, bitmap.height).data;
    };
    const [p, q] = await Promise.all([pixels(a), pixels(b)]);
    if (p.length !== q.length) return 255;
    let max = 0;
    for (let i = 0; i < p.length; i++) if (i % 4 !== 3) max = Math.max(max, Math.abs(p[i] - q[i]));
    return max;
  }, [a.toString('base64'), b.toString('base64')]);
  const page = await browser.newPage({viewport: {width: config.width, height: config.height}, deviceScaleFactor: 1});
  await page.context().setOffline(true);
  page.on('pageerror', error => errors.push(error.message));
  page.on('request', request => {
    const url = new URL(request.url());
    if (url.protocol === 'file:') requested.add(fileURLToPath(url));
    else if (!['data:', 'blob:'].includes(url.protocol)) errors.push(`Online file (save it in the scene folder): ${url.href}`);
  });
  const entryUrl = pathToFileURL(entry).href;
  page.on('requestfailed', request => {
    // The font check makes DevTools read the page again, which fails offline; the page itself has loaded.
    if (request.url() === entryUrl && request.resourceType() === 'other') return;
    errors.push(`Missing file: ${request.url()}`);
  });
  await page.goto(entryUrl);
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(image => image.decode()));
    if (!window.GraphicMotion) throw Error('The page does not define window.GraphicMotion.');
    await GraphicMotion.ready;
    GraphicMotion.pause();
  });
  const art = page.locator(selector);
  const timeline = await page.evaluate(() => ({duration: GraphicMotion.duration, posterMs: GraphicMotion.posterMs}));
  if (timeline.duration !== config.duration || timeline.posterMs !== config.posterMs) {
    throw Error(`The page's timeline (${timeline.duration} ms, poster at ${timeline.posterMs} ms) differs from animation.json (${config.duration} ms, poster at ${config.posterMs} ms).`);
  }
  const box = await art.boundingBox();
  if (!box || box.width !== config.width || box.height !== config.height) throw Error(`${selector} is not ${config.width} × ${config.height}.`);
  const seek = ms => page.evaluate(ms => GraphicMotion.seek(ms), ms);
  const shot = file => art.screenshot(file ? {path: file} : {});

  await seek(config.posterMs);
  const fonts = await glyphFonts(page, selector);
  // Chrome reports a static weight file by its full name, such as "Onest Medium" for Onest 500.
  const listed = font => config.fontFamilies.some(family => font.familyName === family || font.familyName.startsWith(`${family} `));
  const unexpected = fonts.filter(font => !font.isCustomFont || !listed(font));
  if (!fonts.length || unexpected.length) throw Error(`Text renders in a font that isn't loaded from fontFamilies: ${JSON.stringify(unexpected)}`);
  const posterFile = path.join(temp, `${name}.png`);
  const poster = await shot(posterFile);

  const reviewTimes = [...new Set([0, ...(config.reviewTimes || []), config.posterMs, config.duration])].sort((a, b) => a - b);
  const layout = [], intentionalClips = [], reviewShots = [];
  for (const [i, ms] of reviewTimes.entries()) {
    if (ms < 0 || ms > config.duration) throw Error(`Review time ${ms} ms is outside the animation.`);
    await seek(ms);
    const problems = (await textBounds(page, selector)).filter(problem => {
      // Masks may hide text on purpose mid-motion, never in the poster.
      const declared = ms !== config.posterMs && (problem.clippedBy || []).some(cls => (config.motionClipClasses || []).includes(cls));
      if (declared) intentionalClips.push({ms, ...problem});
      return !declared;
    });
    if (problems.length) layout.push({ms, problems});
    reviewShots.push(await shot(path.join(temp, 'review', `${String(i).padStart(2, '0')}.png`)));
  }
  if (layout.length) throw Error(`Text outside the canvas or cut off: ${JSON.stringify(layout)}`);

  // Arrive at every review time again from elsewhere in the timeline: the frame must not change.
  let repeatDifference = 0;
  for (const [i, ms] of [...reviewTimes.entries()].reverse()) {
    await seek(config.duration - ms);
    await seek(ms);
    repeatDifference = Math.max(repeatDifference, await difference(reviewShots[i], await shot()));
  }
  if (repeatDifference > tolerance) {
    throw Error(`Seeking to the same time twice changes the frame (up to ${repeatDifference} of 255 per colour): some state does not come from seek(ms), or a moving element lacks will-change: opacity, transform.`);
  }
  const loopDifference = await difference(reviewShots[0], reviewShots.at(-1));
  if (config.seamless && loopDifference > tolerance) throw Error('seamless is set, but the last frame differs from the first.');

  for (let i = 0; i < frameCount; i++) {
    await seek(i * 1000 / config.fps);
    await shot(path.join(temp, 'frames', `${String(i).padStart(5, '0')}.png`));
    if (i % config.fps === 0) console.log(`Frames: ${i / config.fps} s of ${config.duration / 1000} s`);
  }
  if (errors.length) throw Error(errors.join('\n'));
  const loaded = [];
  for (const file of [...requested].sort()) {
    const real = await fs.realpath(file);
    if (!inside(root, real) && real !== root) throw Error(`Uses a file outside the scene folder: ${real}`);
    loaded.push({file: path.relative(root, real), sha256: digest(await fs.readFile(real))});
  }

  const input = ['-y', '-framerate', String(config.fps), '-i', path.join(temp, 'frames', '%05d.png')];
  const mp4File = path.join(temp, `${name}.mp4`);
  // Limited-range BT.709, so players don't shift the colours.
  await run([...input, '-frames:v', String(frameCount), '-an',
    '-vf', 'scale=out_color_matrix=bt709:out_range=limited,format=yuv420p',
    '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-movflags', '+faststart', mp4File]);
  const gifFile = gif && path.join(temp, `${name}.gif`);
  if (gif) {
    // One palette for the whole sequence; ordered dithering keeps flat colours steady between frames.
    const filter = `fps=${gif.fps},scale=${gif.width}:${gifHeight}:flags=lanczos,split[a][b];[a]palettegen=max_colors=256:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle`;
    await run([...input, '-filter_complex', filter, '-loop', '0', gifFile]);
  }
  await run(['-y', '-i', posterFile, '-vf', 'scale=360:-1:flags=lanczos', '-frames:v', '1', path.join(temp, 'review', 'poster-phone.png')]);
  const columns = Math.min(4, reviewTimes.length), rows = Math.ceil(reviewTimes.length / columns);
  await run(['-y', '-framerate', '1', '-i', path.join(temp, 'review', '%02d.png'),
    '-vf', `scale=360:-1:flags=lanczos,tile=${columns}x${rows}:padding=12:color=0x1e1e1e`, '-frames:v', '1',
    path.join(temp, 'review', 'contact-sheet.png')]);

  const mp4 = await decoded(mp4File);
  matches('MP4', mp4, [config.width, config.height], frameCount);
  const gifMeta = gif && await decoded(gifFile);
  if (gif) matches('GIF', gifMeta, [gif.width, gifHeight], config.duration * gif.fps / 1000);

  // Every check passed: replace the exports and the review folder.
  for (const file of [posterFile, mp4File, ...(gif ? [gifFile] : [])]) await fs.copyFile(file, path.join(root, path.basename(file)));
  const review = path.join(root, 'review');
  await fs.mkdir(review, {recursive: true});
  for (const old of await fs.readdir(review)) if (/^\d{2}\.png$/.test(old)) await fs.rm(path.join(review, old));
  for (const file of await fs.readdir(path.join(temp, 'review'))) await fs.copyFile(path.join(temp, 'review', file), path.join(review, file));
  const exports = {
    [`${name}.mp4`]: {...mp4, bytes: (await fs.stat(mp4File)).size},
    ...(gif ? {[`${name}.gif`]: {...gifMeta, bytes: (await fs.stat(gifFile)).size}} : {}),
    [`${name}.png`]: {dimensions: [config.width, config.height], bytes: poster.length},
  };
  const report = {
    rendered: new Date().toISOString(),
    config: path.relative(root, configFile),
    exports,
    checks: {fonts, tolerance, repeatSeekDifference: repeatDifference, loopEndDifference: loopDifference, textInBounds: true, intentionalClips, localFilesOnly: true},
    reviewTimes,
    files: loaded,
  };
  await fs.writeFile(path.join(review, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({folder: root, exports, review: ['review/contact-sheet.png', 'review/poster-phone.png', 'review/report.json']}, null, 2));
  success = true;
} finally {
  await browser.close();
  if (success && !args.includes('--keep-frames')) await fs.rm(temp, {recursive: true});
  else console.log(`Frames kept in ${temp}`);
}

function run(ffmpegArgs) {
  return new Promise((resolve, reject) => {
    const child = spawn(ffmpeg, ['-hide_banner', '-loglevel', 'error', ...ffmpegArgs], {stdio: ['ignore', 'pipe', 'pipe']});
    let stdout = '', stderr = '';
    child.stdout.on('data', chunk => { stdout += chunk; });
    child.stderr.on('data', chunk => { stderr += chunk; });
    child.on('error', reject);
    child.on('close', code => code === 0 ? resolve(stdout) : reject(Error(stderr || `ffmpeg exited ${code}`)));
  });
}

// Decodes every frame to count them and measure the real size and running time.
async function decoded(file) {
  const result = await run(['-i', file, '-map', '0:v:0', '-fps_mode', 'passthrough', '-f', 'framemd5', '-']);
  const timebase = result.match(/#tb 0:\s*(\d+)\/(\d+)/);
  const dimensions = result.match(/#dimensions 0:\s*(\d+)x(\d+)/);
  const rows = result.split('\n').filter(line => /^0,/.test(line)).map(line => line.split(',').map(part => part.trim()));
  if (!timebase || !dimensions || !rows.length) throw Error(`Cannot read the frames of ${file}`);
  const last = rows.at(-1);
  const durationSeconds = (Number(last[2]) + Number(last[3]) - Number(rows[0][2])) * Number(timebase[1]) / Number(timebase[2]);
  return {dimensions: dimensions.slice(1).map(Number), frames: rows.length, durationSeconds};
}

function matches(format, meta, dimensions, frames) {
  if (String(meta.dimensions) !== String(dimensions) || meta.frames !== frames || Math.abs(meta.durationSeconds - config.duration / 1000) > 0.025) {
    throw Error(`The encoded ${format} doesn't match the settings: ${JSON.stringify(meta)}`);
  }
}

// The fonts Chrome actually drew the text with, from the DevTools protocol.
async function glyphFonts(page, selector) {
  const session = await page.context().newCDPSession(page);
  await session.send('DOM.enable');
  await session.send('CSS.enable');
  const {root: doc} = await session.send('DOM.getDocument');
  // CDP reports only direct text children, so ask for every element in the subtree.
  const {nodeIds} = await session.send('DOM.querySelectorAll', {nodeId: doc.nodeId, selector: `${selector}, ${selector} *`});
  const results = await Promise.all(nodeIds.map(nodeId => session.send('CSS.getPlatformFontsForNode', {nodeId})));
  const combined = new Map();
  for (const result of results) {
    for (const font of result.fonts) {
      const key = `${font.postScriptName}|${font.isCustomFont}`;
      if (combined.has(key)) combined.get(key).glyphCount += font.glyphCount;
      else combined.set(key, {...font});
    }
  }
  await session.detach();
  return [...combined.values()];
}

// Text that leaves the canvas, or is cut off by an element that hides overflow.
function textBounds(page, selector) {
  return page.evaluate(selector => {
    const art = document.querySelector(selector), outer = art.getBoundingClientRect(), problems = [];
    const outside = (r, box) => r.left < box.left - 2 || r.right > box.right + 2 || r.top < box.top - 2 || r.bottom > box.bottom + 2;
    const walker = document.createTreeWalker(art, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const text = node.textContent.trim();
      if (!text || ['SCRIPT', 'STYLE', 'TITLE'].includes(node.parentElement.tagName)) continue;
      const range = document.createRange();
      range.selectNodeContents(node);
      for (const r of range.getClientRects()) {
        if (!r.width || !r.height) continue;
        if (outside(r, outer)) problems.push({text, reason: 'outside the canvas'});
        for (let parent = node.parentElement; parent && parent !== art; parent = parent.parentElement) {
          const style = getComputedStyle(parent);
          const hides = ['hidden', 'clip'].includes(style.overflowX) || ['hidden', 'clip'].includes(style.overflowY);
          if (hides && outside(r, parent.getBoundingClientRect())) problems.push({text, reason: 'cut off', clippedBy: [...parent.classList]});
        }
      }
    }
    return problems;
  }, selector);
}
