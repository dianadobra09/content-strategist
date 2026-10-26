"""Builds index.html: the Figma-to-React flow in the BlinkWrite brand kit style (2.19, light layout).

python3 build-animation.py, then render-animation.cjs for the PNG and MP4.
Pre-launch: kit colours, type and character style only; no BlinkWrite logo, name or link.
"""
from pathlib import Path
import base64

root = Path(__file__).resolve().parent

W, H, M = 1080, 1350, 72
BG, INK, MUTED, LINE = '#FAFAFB', '#1F2223', '#596165', '#D4D9D5'
LIME, LIGHT_LIME, PALE_LIME, GREEN_LABEL = '#90BF00', '#E0FF82', '#F3F9E0', '#526D00'

HEAD_X, HEAD_SIZE, HEAD_Y, HEAD_STEP = 68, 84, 150, 96
HEADLINE = ['Can designers replace', '80% of Figma with', 'Claude code?']
EMPHASIS_LINE, EMPHASIS = 1, '80% of Figma'  # ink on a light lime highlight, like selected text
LIST_TOP, ROW_H = HEAD_Y + 2 * HEAD_STEP + 90, 192
ICON, ICON_GAP, ICON_COL = 52, 14, 118  # icon column: x 72-190
TEXT_X = 230
TITLE_DY, CAPTION_DY = 84, 130
CHECK_X, CHECK_R = W - M - 18, 18  # the check replaces the step number once a step is done
FOOT_Y = 1266

# Seconds. Whole plan, then one step at a time (each gets its check when the highlight moves on), then the whole plan, all checked.
INTRO, STEP, HOLD, BLINK = 0.5, 1.5, 2.0, 0.53
DURATION = INTRO + 4 * STEP + HOLD
STILL_AT = INTRO + 4 * STEP + 2.5 * BLINK  # in the hold, while the cursor shows

ROWS = [
    ('Figma', 'Ideation & prototyping', ['figma']),
    ('React + Tailwind', 'Reusable components in a repo', ['react', 'tailwind']),
    ('Claude or Codex', 'Build screens from those components', ['claude', 'openai']),
    ('Designer review', 'Check the screens and ask for changes', None),
]
# Simple Icons ship without a fill; give these marks their brand colour.
FILLS = {'claude': '#D97757'}


def data_uri(mime, raw):
    return f'data:{mime};base64,{base64.b64encode(raw).decode()}'


def logo(name, x, y):
    svg = (root / 'assets' / f'{name}.svg').read_text()
    if name in FILLS:
        svg = svg.replace('<path ', f'<path fill="{FILLS[name]}" ', 1)
    href = data_uri('image/svg+xml', svg.encode())
    return f'<image href="{href}" x="{x}" y="{y}" width="{ICON}" height="{ICON}"/>'


def icons(names, y):
    cy = y + ROW_H // 2
    if names is None:  # the designer, from the kit's approved human cast
        r, cx = 44, M + ICON_COL // 2
        href = data_uri('image/png', (root / 'assets' / 'designer.png').read_bytes())
        return (f'<clipPath id="avatar"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
                f'<image href="{href}" x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" clip-path="url(#avatar)"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    width = len(names) * ICON + (len(names) - 1) * ICON_GAP
    x0 = M + (ICON_COL - width) // 2
    return ''.join(logo(n, x0 + i * (ICON + ICON_GAP), cy - ICON // 2) for i, n in enumerate(names))


def esc(text):
    return text.replace('&', '&amp;')


rules, rows = [], []
for i, (title, caption, names) in enumerate(ROWS):
    y = LIST_TOP + i * ROW_H
    rules.append(f'<line x1="{M}" y1="{y}" x2="{W-M}" y2="{y}" stroke="{LINE}" stroke-width="1"/>')
    rows.append(f'''<g class="row">
  {icons(names, y)}
  <text class="row-title" x="{TEXT_X}" y="{y+TITLE_DY}" font-size="42" font-weight="500" fill="{INK}">{esc(title)}</text>
  <text x="{TEXT_X}" y="{y+CAPTION_DY}" font-size="30" font-weight="400" fill="{MUTED}">{esc(caption)}</text>
  <text class="step-number" x="{W-M}" y="{y+TITLE_DY}" text-anchor="end" font-family="Geist Mono" font-size="20" font-weight="500" fill="{MUTED}">0{i+1}</text>
  <g class="check" data-y="{y+TITLE_DY-9}" opacity="0"><circle r="{CHECK_R}" fill="{LIME}"/><path d="M-7.5 0.5 L-2.5 5.5 L8 -5" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></g>
</g>''')

ids = {EMPHASIS_LINE: ' id="head-emphasis"', len(HEADLINE) - 1: ' id="head-last"'}
headline = '\n'.join(
    f'<text{ids.get(i, "")} x="{HEAD_X}" y="{HEAD_Y+i*HEAD_STEP}" '
    f'font-size="{HEAD_SIZE}" font-weight="500" fill="{INK}">{line}</text>'
    for i, line in enumerate(HEADLINE))
head_last_y = HEAD_Y + (len(HEADLINE) - 1) * HEAD_STEP

title = 'Can designers replace 80% of Figma with Claude code?'
desc = ('The plan, as a four-step flow: Figma for ideation and prototyping, reusable React and Tailwind '
        'components in a repo, Claude or Codex building screens from those components, then a designer '
        'checking the screens and asking for changes. Each step gets a check as the flow moves on.')

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<style>
@font-face{{font-family:"Onest";font-weight:400;src:url(fonts/Onest-400.ttf) format("truetype")}}
@font-face{{font-family:"Onest";font-weight:500;src:url(fonts/Onest-500.ttf) format("truetype")}}
@font-face{{font-family:"Geist Mono";font-weight:500;src:url(fonts/GeistMono-500.ttf) format("truetype")}}
*{{box-sizing:border-box}}
body{{margin:0;background:#E8EBE7;display:flex;min-height:100vh;align-items:center;justify-content:center}}
body.capture{{background:{BG}}}
svg{{display:block;width:min(100vw,80vh);height:auto;max-height:100vh;font-family:"Onest",sans-serif}}
</style></head><body>
<svg id="artboard" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">{desc}</desc>
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect id="emphasis" x="{HEAD_X-8}" y="{HEAD_Y+EMPHASIS_LINE*HEAD_STEP-66}" width="0" height="86" rx="8" fill="{LIGHT_LIME}"/>
{headline}
<rect id="head-caret" x="0" y="{head_last_y-66}" width="7" height="84" fill="{LIME}"/>
<rect id="band" x="52" y="{LIST_TOP+12}" width="{W-104}" height="{ROW_H-24}" rx="16" fill="{PALE_LIME}" opacity="0"/>
{chr(10).join(rules)}
{chr(10).join(rows)}
<rect id="row-caret" x="0" y="0" width="4" height="44" fill="{LIME}" opacity="0"/>
<line x1="{M}" y1="{FOOT_Y}" x2="{W-M}" y2="{FOOT_Y}" stroke="{LINE}" stroke-width="1"/>
<rect x="{W-M-20}" y="{FOOT_Y-16}" width="4" height="32" fill="{LIME}"/>
</svg>
<script>
const T={DURATION},STILL={STILL_AT},INTRO={INTRO},STEP={STEP},OUTRO=INTRO+4*STEP,FADE=.18,SLIDE=.2,POP=.2,BLINK={BLINK};
const LIST_TOP={LIST_TOP},ROW_H={ROW_H},TEXT_X={TEXT_X},TITLE_DY={TITLE_DY},HEAD_X={HEAD_X},CHECK_X={CHECK_X};
const clamp=x=>Math.min(1,Math.max(0,x));
const smooth=x=>{{x=clamp(x);return x*x*(3-2*x)}};
const popOut=x=>{{x=clamp(x);const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const blinkOn=(t,since)=>Math.floor(Math.max(0,t-since)/BLINK)%2===0;
const rows=[...document.querySelectorAll('.row')];
const titles=rows.map(r=>r.querySelector('.row-title'));
const numbers=rows.map(r=>r.querySelector('.step-number'));
const checks=rows.map(r=>r.querySelector('.check'));
const band=document.getElementById('band'),rowCaret=document.getElementById('row-caret');
const headCaret=document.getElementById('head-caret'),headLast=document.getElementById('head-last');
const emphasis=document.getElementById('emphasis'),emphasisLine=document.getElementById('head-emphasis');
function renderAt(seconds){{
 const t=((seconds%T)+T)%T;
 emphasis.setAttribute('width',emphasisLine.getSubStringLength(0,{len(EMPHASIS)})+16);
 let slide=0;
 for(let i=1;i<4;i++)slide+=smooth((t-INTRO-i*STEP)/SLIDE);
 band.setAttribute('y',LIST_TOP+12+slide*ROW_H);
 band.setAttribute('opacity',smooth((t-INTRO)/FADE)*(1-smooth((t-OUTRO)/FADE)));
 rows.forEach((r,i)=>{{
  const dim=i===0?0:smooth((t-INTRO)/FADE)*(1-smooth((t-INTRO-i*STEP)/FADE));
  r.setAttribute('opacity',1-.7*dim);
  // a step is done when the highlight moves on: its number turns into a check
  const done=(t-INTRO-(i+1)*STEP)/POP;
  checks[i].setAttribute('transform',`translate(${{CHECK_X}} ${{checks[i].dataset.y}}) scale(${{.4+.6*popOut(done)}})`);
  checks[i].setAttribute('opacity',smooth(done*2));
  numbers[i].setAttribute('opacity',1-smooth(done*2));
 }});
 let active=-1;
 if(t>=INTRO&&t<OUTRO){{active=0;for(let i=1;i<4;i++)if(t>=INTRO+i*STEP+SLIDE)active=i}}
 numbers.forEach((n,i)=>n.setAttribute('fill',i===active?'{GREEN_LABEL}':'{MUTED}'));
 if(active>=0){{
  const since=active===0?INTRO:INTRO+active*STEP+SLIDE;
  rowCaret.setAttribute('x',TEXT_X+titles[active].getComputedTextLength()+8);
  rowCaret.setAttribute('y',LIST_TOP+active*ROW_H+TITLE_DY-35);
  rowCaret.setAttribute('opacity',blinkOn(t,since)?1:0);
  headCaret.setAttribute('opacity',0);
 }}else{{
  rowCaret.setAttribute('opacity',0);
  headCaret.setAttribute('x',HEAD_X+headLast.getComputedTextLength()+10);
  headCaret.setAttribute('opacity',blinkOn(t,t>=OUTRO?OUTRO:0)?1:0);
 }}
}}
window.renderAt=renderAt;
window.timing={{duration:T,still:STILL}};
const capture=new URLSearchParams(location.search).has('capture');
if(capture)document.body.classList.add('capture');
document.fonts.ready.then(()=>{{
 if(capture||matchMedia('(prefers-reduced-motion: reduce)').matches){{renderAt(STILL);return}}
 const start=performance.now();
 const animate=now=>{{renderAt((now-start)/1000);requestAnimationFrame(animate)}};
 requestAnimationFrame(animate);
}});
</script></body></html>'''
(root / 'index.html').write_text(html)
print(f'Built index.html: {DURATION:g} s loop.')
