// Exports figma-to-react.png (the full plan, all steps checked) and figma-to-react-linkedin.mp4 (30 fps, silent) from index.html.
// The loop length and the still's moment come from the page (build-animation.py).
// Run with PLAYWRIGHT_PATH pointing to a Playwright installation if needed.
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const { spawn } = require('node:child_process');
const { once } = require('node:events');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const FPS = 30;

(async () => {
  const browser = await chromium.launch({headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
    const errors=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href+'?capture');
    const missing=await page.evaluate(async()=>{
      const faces=['400 30px Onest','500 84px Onest','500 20px "Geist Mono"'];
      await Promise.all(faces.map(f=>document.fonts.load(f)));
      await document.fonts.ready;
      await Promise.all([...document.querySelectorAll('svg image')].map(e=>new Promise((resolve,reject)=>{const img=new Image();img.onload=resolve;img.onerror=reject;img.src=e.getAttribute('href')})));
      return faces.filter(f=>!document.fonts.check(f));
    });
    if(missing.length)throw Error(`Fonts not loaded: ${missing.join(', ')}`);
    const {duration,still}=await page.evaluate(()=>window.timing);
    await page.evaluate(t=>renderAt(t),still);
    await page.screenshot({path:path.join(__dirname,'figma-to-react.png')});
    // Lossless PNG frames, converted to the usual limited-range BT.709 so players don't shift the colours.
    const ffmpeg=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-vcodec','png','-i','pipe:0','-an','-vf','scale=out_color_matrix=bt709:out_range=limited,format=yuv420p','-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:v','libx264','-preset','medium','-crf','18','-movflags','+faststart',path.join(__dirname,'figma-to-react-linkedin.mp4')],{stdio:['pipe','inherit','inherit']});
    const done=once(ffmpeg,'close');
    const frames=Math.round(FPS*duration);
    for(let frame=0;frame<frames;frame++){
      await page.evaluate(t=>renderAt(t),frame/FPS);
      const buf=await page.screenshot({type:'png'});
      if(!ffmpeg.stdin.write(buf))await once(ffmpeg.stdin,'drain');
      if(frame%(FPS*4)===0)console.log(`Rendered ${frame}/${frames} frames`);
    }
    ffmpeg.stdin.end();
    const [code]=await done;
    if(code!==0)throw Error(`ffmpeg exited ${code}`);
    if(errors.length)throw Error(errors.join('\n'));
    console.log(`Exported ${duration}-second 1080 × 1350 MP4 and PNG. No browser errors.`);
  } finally {await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
