#!/usr/bin/env python3
"""Plan the posting calendar from the ready queues and write outputs/schedule.md.

  python3 scripts/schedule_plan.py                     # plan from tomorrow
  python3 scripts/schedule_plan.py --start 2026-10-20  # first day that may get a post
  python3 scripts/schedule_plan.py --json              # also print the unscheduled slots for schedule-posts
  python3 scripts/schedule_plan.py --renumber          # renumber the X, Threads and Bluesky files in posting order

LinkedIn posts its outputs/posts/ready/linkedin/ queue in number order (the author's order). X, Threads and
Bluesky follow the rule in strategy/positioning.md, copied in CADENCE, TIMES, EVENING and WINDOW below (change both
together): on a LinkedIn day each channel posts its version of that day's LinkedIn post, the one with the
visual (an image, video or link card) first; on other days, or when it has no version, the next post in
its queue; never a post with a version among the channel's previous five posts. Nothing goes out on X,
Threads or Bluesky before its LinkedIn post: neither a version of it nor its visual (the post's slug and
its visual's outputs/visuals/<slug>/ folder both wait for that LinkedIn post's day, or for a hold to end). A file with a `scheduled:`
line keeps its slot. `hold:` files are skipped. `planned_for` files don't go
before their date, then go first. The warnings list what to settle with the author before scheduling: length
limits, missing visuals, posts that found no day.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
READY = ROOT / 'outputs/posts/ready'
PUBLISHED = ROOT / 'outputs/posts/published'
OUT = ROOT / 'outputs/schedule.md'
TZ = ZoneInfo('Europe/Bucharest')  # the author's time zone; keep it, TIMES, EVENING and CADENCE in step with strategy/positioning.md
TIMES = {1: dt.time(15, 0), 2: dt.time(15, 0), 3: dt.time(15, 0)}  # LinkedIn, by weekday, Monday = 0
EVENING = dt.time(19, 0)  # X, Threads and Bluesky, every day they post
CHANNELS = ('linkedin', 'x', 'threads', 'bluesky')
WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
NAMES = {'linkedin': 'LinkedIn', 'x': 'X', 'threads': 'Threads', 'bluesky': 'Bluesky'}
CADENCE = {'linkedin': {1, 2, 3}, 'x': {0, 1, 2, 3, 4}, 'threads': {0, 1, 2, 3, 4}, 'bluesky': {0, 1, 2, 3}}
LIMITS = {'linkedin': 3000, 'x': 280, 'threads': 500, 'bluesky': 300}
COMMENT_LIMITS = {'linkedin': 1250, 'x': 280, 'threads': 500, 'bluesky': 300}
LINK = re.compile(r'https?://|www\.|\b[\w-]+\.(?:ai|com|io|co|org|net|eu|dev|app|so|me|ly)\b', re.I)  # LinkedIn comments carry no links
WINDOW = 5  # a post can't go out while a version of it is among the channel's previous 5 posts
HORIZON = 730  # days to look ahead for a day that fits
LABELS = ('First reply', 'Topic tag', 'Visual', 'Alt text', 'Alt text 2', 'Link card')  # labeled lines after the post text
MONTHS = {m: i for i, m in enumerate(
    ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
     'september', 'october', 'november', 'december'], 1)}


def plain(text):
    """Markdown links to bare URLs, as the networks show them; mailto links to their text."""
    text = re.sub(r'\[([^\]]*)\]\(mailto:[^)\s]+\)', r'\1', text)
    return re.sub(r'\[([^\]]*)\]\((https?://[^)\s]+)\)', r'\2', text).strip()


def x_length(text):
    for url in re.findall(r'https?://\S+', text):
        text = text.replace(url, 'x' * 23, 1)
    return len(text)


def parse(path, channel, linkedin_slugs):
    raw = path.read_text()
    meta, body = {}, raw
    m = re.match(r'---\n(.*?)\n---\n', raw, re.S)
    if m:
        body = raw[m.end():]
        for line in m.group(1).splitlines():
            key, _, value = line.partition(':')
            meta[key.strip()] = value.strip()
    num, stem = path.stem.split('-', 1)
    slug, version = stem, 1
    v = re.match(r'(.+)-(\d+)$', stem)
    if v and v.group(1) in linkedin_slugs:
        slug, version = v.group(1), int(v.group(2))
    sections = re.split(r'(?m)^## ', body)
    named = {s.split('\n', 1)[0].strip(): s.split('\n', 1)[1] if '\n' in s else '' for s in sections[1:]}
    labels = '|'.join(LABELS)
    first_label = re.search(rf'(?m)^(?:{labels}):', sections[0])
    text = sections[0][:first_label.start()] if first_label else sections[0]
    fields = {}
    for block in (sections[0][first_label.start():] if first_label else '', named.get('Visual', '')):
        for m in re.finditer(rf'(?ms)^({labels}):[ \t]*(.*?)(?=^(?:{labels}):|\Z)', block):
            fields.setdefault(m.group(1), m.group(2).strip())
    visual = fields.get('Visual') or named.get('Visual', '')
    parts = [plain(p) for p in re.split(r'(?m)^\d+/\s*$', text) if p.strip()]
    card = re.search(r'link card for (https?://[^\s,)]+)', plain(visual)) or re.search(r'(https?://\S+)', plain(fields.get('Link card', '')))
    if card and parts:  # the URL goes in the post so the network shows the card; it's in the length count
        parts[0] += '\n\n' + card.group(1)
    comments = parts[1:] if channel == 'bluesky' else []
    if channel == 'linkedin' and named.get('First comment', '').strip():
        comments.append(plain(named['First comment']))
    link = re.search(r'\]\(([^)\s]+\.(?:png|jpe?g|gif|webp|mp4|mov|pdf))\)', visual, re.I)
    if link:
        visual_file = (path.parent / link.group(1)).resolve()
    if not link:
        named_file = re.search(r'([\w./-]+\.(?:png|jpe?g|gif|webp|mp4|mov|pdf))', visual, re.I)
        visual_file = (path.parent / named_file.group(1)).resolve() if named_file and '/' in named_file.group(1) else None
    media = visual_file if link or visual_file else None
    alt = plain(fields['Alt text']) if fields.get('Alt text') else None
    topic = re.match(r'(.+)', fields.get('Topic tag', ''))
    return {
        'channel': channel, 'num': num, 'file': str(path.relative_to(ROOT)), 'slug': slug, 'version': version,
        'hold': meta.get('hold'), 'planned_for': meta.get('planned_for'),
        'scheduled': meta.get('scheduled'), 'zernio_id': meta.get('zernio_id'), 'repeat_ok': meta.get('repeat_ok'),
        'message': parts[0] if parts else '', 'comments': comments, 'first_reply': bool(fields.get('First reply')),
        'topic': topic.group(1).strip() if topic else None,
        'media': str(media) if media else None, 'media_missing': bool(media and not media.exists()), 'alt': alt,
        'visual': bool(media or card),
        'visual_slug': media.parent.name if media and media.parent.parent.name == 'visuals' else None,
        'raw': raw,
    }


def anchor(planned_for, channel):
    text = planned_for.lower()
    end = re.search(r'end of (\d{4})', text)
    if end:
        d = dt.date(int(end.group(1)), 12, 30)
        while d.weekday() not in CADENCE[channel]:
            d -= dt.timedelta(days=1)
        return d
    iso = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
    if iso:
        return dt.date(*map(int, iso.groups()))
    words = re.search(r'(\d{1,2}) ([a-z]+) (\d{4})', text)
    if words and words.group(2) in MONTHS:
        return dt.date(int(words.group(3)), MONTHS[words.group(2)], int(words.group(1)))
    return None


def next_day(d, channel, taken):
    while d.weekday() not in CADENCE[channel] or d in taken:
        d += dt.timedelta(days=1)
    return d


def scheduled_date(post):
    return dt.datetime.fromisoformat(post['scheduled']).date()


def plan(start):
    linkedin_slugs = {p.stem.split('-', 1)[1] for p in (READY / 'linkedin').glob('*.md')}
    linkedin_slugs |= {p.stem.split('-', 1)[1] for p in (PUBLISHED / 'linkedin').glob('*.md')}
    queues = {c: sorted((parse(p, c, linkedin_slugs) for p in (READY / c).glob('*.md')), key=lambda p: int(p['num']))
              for c in CHANNELS}
    held = {c: [p for p in queues[c] if p['hold']] for c in CHANNELS}
    after_launch = {c: sorted((READY / c / 'after-launch').glob('*.md')) for c in CHANNELS}
    slots = {c: {} for c in CHANNELS}  # date -> post
    gaps = {c: [] for c in CHANNELS}  # cadence days no post fits
    waiting = {c: [] for c in CHANNELS}  # versions of held LinkedIn posts
    warnings = []

    # LinkedIn: the author's order; planned posts take their day first
    taken = slots['linkedin']
    for p in queues['linkedin']:
        if p['scheduled'] and not p['hold']:
            taken[scheduled_date(p)] = p
    todo = [p for p in queues['linkedin'] if not (p['hold'] or p['scheduled'])]
    for p in todo:
        if p['planned_for']:
            a = anchor(p['planned_for'], 'linkedin')
            if a is None:
                warnings.append(f"{p['file']}: can't read `planned_for: {p['planned_for']}`; not planned")
            else:
                taken[next_day(a, 'linkedin', taken)] = p
    cursor = start
    for p in todo:
        if not p['planned_for']:
            d = next_day(cursor, 'linkedin', taken)
            taken[d], cursor = p, d + dt.timedelta(days=1)

    linkedin_day = {d: p['slug'] for d, p in slots['linkedin'].items()}
    linkedin_date = {s: d for d, s in linkedin_day.items()}
    held_slugs = {p['slug'] for p in held['linkedin']}  # the visual goes out with LinkedIn, the rest after it
    for c in CHANNELS[1:]:
        taken = slots[c]
        past = [(scheduled_date(p), p['slug']) for p in (parse(f, c, linkedin_slugs) for f in (PUBLISHED / c).glob('*.md'))
                if p['scheduled']]
        for p in queues[c]:
            if p['scheduled'] and not p['hold']:
                taken[scheduled_date(p)] = p
        todo, earliest = [], {}
        for p in queues[c]:
            if p['hold'] or p['scheduled']:
                continue
            if {p['slug'], p['visual_slug']} & held_slugs:
                waiting[c].append(pathlib.Path(p['file']).stem)
                continue
            if p['planned_for']:
                earliest[p['file']] = anchor(p['planned_for'], c)
                if earliest[p['file']] is None:
                    warnings.append(f"{p['file']}: can't read `planned_for: {p['planned_for']}`; not planned")
                    continue
            todo.append(p)

        def fits(p, d):
            timeline = sorted(past + [(e, q['slug']) for e, q in taken.items()])
            near = [s for e, s in timeline if e < d][-WINDOW:] + [s for e, s in timeline if e > d][:WINDOW]
            return p['slug'] not in near

        d = start
        while todo and d <= start + dt.timedelta(days=HORIZON):
            if d.weekday() in CADENCE[c] and d not in taken:
                ready = [p for p in todo if earliest.get(p['file'], d) <= d and fits(p, d)
                         and linkedin_date.get(p['visual_slug'], d) <= d]
                same = [p for p in ready if p['slug'] == linkedin_day.get(d)]
                pick = min(same, key=lambda p: (not p['visual'], int(p['num'])), default=None)  # the visual goes out with LinkedIn
                if pick is None:  # queue order; planned posts first once their date has come
                    free = [p for p in ready if linkedin_date.get(p['slug'], d) <= d]
                    pick = min(free, key=lambda p: (p['file'] not in earliest, int(p['num'])), default=None)
                if pick:
                    taken[d] = pick
                    todo.remove(pick)
                else:
                    gaps[c].append(d)
            d += dt.timedelta(days=1)
        gaps[c] = [g for g in gaps[c] if taken and g < max(taken)]
        warnings += [f"{p['file']}: no day fits within {HORIZON} days; not planned" for p in todo]

    for c in CHANNELS:
        ordered = sorted(slots[c].items())
        for i, (d, p) in enumerate(ordered):
            limit = LIMITS[c]
            length = x_length(p['message']) if c == 'x' else len(p['message'])
            if length > limit:
                note = ' (needs X Premium)' if c == 'x' else ''
                warnings.append(f"{p['file']}: {length} characters, over {NAMES[c]}'s {limit}{note}")
            for comment in p['comments']:
                n = x_length(comment) if c == 'x' else len(comment)
                if n > COMMENT_LIMITS[c]:
                    warnings.append(f"{p['file']}: a first comment or thread part has {n} characters, over {COMMENT_LIMITS[c]}")
                if c == 'linkedin' and LINK.search(comment):
                    warnings.append(f"{p['file']}: the first comment has a link; LinkedIn comments carry none")
            if p['first_reply'] and not p['scheduled']:
                warnings.append(f"{p['file']}: has a First reply line; X, Threads and Bluesky posts get none, so it isn't sent")
            if c == 'threads' and p['topic'] and (len(p['topic']) > 50 or set(p['topic']) & {'.', '&'}):
                warnings.append(f"{p['file']}: topic tag \"{p['topic']}\" must be 1 to 50 characters, without . or &")
            if p['media_missing']:
                warnings.append(f"{p['file']}: visual not found at {p['media']}")
            early = [s for s in {p['slug'], p['visual_slug']} - {None}
                     if c != 'linkedin' and (s in held_slugs or linkedin_date.get(s, d) > d)]
            if early:
                warnings.append(f"{NAMES[c]} {d:%d %b}: {p['file']} goes out before its LinkedIn post ({', '.join(early)})")
            if p['slug'] in [q['slug'] for _, q in ordered[max(0, i - WINDOW):i]] and not p['repeat_ok']:
                warnings.append(f"{NAMES[c]} {d:%d %b}: {p['file']} has another version among the previous {WINDOW} posts")
    return queues, slots, gaps, held, waiting, after_launch, warnings


def renumber(queues, slots):
    """Rename the X, Threads and Bluesky files so their numbers follow the posting order."""
    for c in CHANNELS[1:]:
        first = max((int(p.stem.split('-', 1)[0]) for p in (PUBLISHED / c).glob('*.md')), default=0) + 1
        order = [p['file'] for _, p in sorted(slots[c].items())]
        order += [p['file'] for p in queues[c] if p['file'] not in order]
        moves = []
        for n, f in enumerate(order, first):
            old = ROOT / f
            new = old.with_name(f"{n:02d}-{old.stem.split('-', 1)[1]}.md")
            if new != old:
                moves.append((old, new))
        for old, _ in moves:
            old.rename(old.with_suffix('.renumber'))
        for old, new in moves:
            old.with_suffix('.renumber').rename(new)
        print(f'{NAMES[c]}: renumbered {len(moves)} files')


def publish_at(d, channel):
    return dt.datetime.combine(d, TIMES[d.weekday()] if channel == 'linkedin' else EVENING, TZ).isoformat()


def write(slots, gaps, held, waiting, after_launch, warnings, today):
    def cell(p):
        return p['num'] + (' ✓' if p['scheduled'] else '') if p else ''

    days = sorted(set().union(*[slots[c].keys() for c in CHANNELS]))
    lines = [
        '# Posting calendar', '',
        f'Generated by `scripts/schedule_plan.py` on {today:%-d %B %Y} from the `posts/ready/<channel>/` queues and the cadence '
        'in `../strategy/positioning.md`. Don\'t edit by hand: a post\'s `scheduled:` line is the record. Rerun the script after any change.',
        f'Times ({TZ.key}): LinkedIn ' + ', '.join(f'{WEEKDAYS[d]} {t:%H:%M}' for d, t in sorted(TIMES.items()))
        + f'; X, Threads and Bluesky {EVENING:%H:%M}. ✓ = scheduled in Zernio; no mark = planned.', '',
        '## By day', '',
        '| Date | LinkedIn | X | Threads | Bluesky |', '|---|---|---|---|---|',
    ]
    for d in days:
        lines.append(f'| {d:%a %d %b} | ' + ' | '.join(cell(slots[c].get(d)) for c in CHANNELS) + ' |')
    for c in CHANNELS:
        lines += ['', f'## {NAMES[c]}', '', '| Date | Post | Status |', '|---|---|---|']
        for d, p in sorted(slots[c].items()):
            status = f"scheduled ({p['zernio_id']})" if p['scheduled'] else 'planned'
            lines.append(f"| {d:%a %d %b} | {pathlib.Path(p['file']).stem} | {status} |")
    lines += ['', '## Not scheduled', '']
    for c in CHANNELS:
        if gaps[c]:
            lines.append(f"- {NAMES[c]}, empty days (every remaining post has a version among the previous {WINDOW} posts "
                         "or waits for its LinkedIn day): " + ', '.join(f'{g:%a %d %b}' for g in gaps[c]))
        if held[c]:
            lines.append(f"- {NAMES[c]}, held: " + ', '.join(f"{p['num']} {p['slug']}" for p in held[c]))
        if c != 'linkedin' and waiting[c]:
            lines.append(f"- {NAMES[c]}, waiting for their held LinkedIn post: " + ', '.join(waiting[c]))
        if after_launch[c]:
            lines.append(f"- {NAMES[c]}, `after-launch/`: {len(after_launch[c])} posts")
    lines += ['', '## Check before scheduling', '']
    lines += [f'- {w}' for w in warnings] or ['- Nothing to check.']
    OUT.write_text('\n'.join(lines) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=dt.date.fromisoformat, help='first day that may get a post (default: tomorrow)')
    ap.add_argument('--json', action='store_true', help='print unscheduled slots as JSON')
    ap.add_argument('--renumber', action='store_true', help='renumber the X, Threads and Bluesky files in posting order')
    args = ap.parse_args()
    today = dt.datetime.now(TZ).date()
    start = args.start or today + dt.timedelta(days=1)
    queues, slots, gaps, held, waiting, after_launch, warnings = plan(start)
    if args.renumber:
        renumber(queues, slots)
        queues, slots, gaps, held, waiting, after_launch, warnings = plan(start)
    write(slots, gaps, held, waiting, after_launch, warnings, today)
    counts = ', '.join(f"{NAMES[c]} {len(slots[c])}" for c in CHANNELS)
    print(f'{OUT.relative_to(ROOT)}: {counts} slots; {len(warnings)} to check')
    for w in warnings:
        print(f'  - {w}')
    if args.json:
        todo = [{'channel': c, 'publish_at': publish_at(d, c), 'file': p['file'], 'message': p['message'],
                 'comments': p['comments'], 'topic': p['topic'], 'media': p['media'], 'alt': p['alt']}
                for c in CHANNELS for d, p in sorted(slots[c].items()) if not p['scheduled']]
        print(json.dumps(sorted(todo, key=lambda s: (s['publish_at'], CHANNELS.index(s['channel']))),
                         ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
