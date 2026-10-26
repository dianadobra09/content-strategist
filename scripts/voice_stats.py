#!/usr/bin/env python3
"""Writing stats for the author's samples or for one draft.

  python3 scripts/voice_stats.py voice/samples/linkedin.md   # one post per '## ' entry
  python3 scripts/voice_stats.py - <<'EOF'                   # one draft on stdin
  <draft>
  EOF
"""
import re
import statistics
import sys

EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿]')
LIST_LINE = re.compile(r'([-*•→]|\d+[.)])\s')
MEDIANS = ('words', 'characters', 'words per sentence', 'paragraphs', 'first line characters')


def split_posts(text):
    """Posts are the bodies under '## ' headers. Lines starting with '>' are notes."""
    posts, body = [], None
    for line in text.splitlines():
        if line.startswith('## '):
            if body is not None:
                posts.append('\n'.join(body).strip())
            body = []
        elif body is not None and not line.startswith('>'):
            body.append(line)
    if body is not None:
        posts.append('\n'.join(body).strip())
    return [p for p in posts if p]


def measure(post):
    words = post.split()
    sentences = [s for s in re.split(r'(?<=[.!?])\s+|\n+', post) if s.strip()]
    lines = [line.strip() for line in post.splitlines() if line.strip()]
    return {
        'words': len(words),
        'characters': len(post),
        'words per sentence': round(len(words) / max(len(sentences), 1), 1),
        'paragraphs': len(re.split(r'\n\s*\n', post.strip())),
        'first line characters': len(lines[0]),
        'emoji': len(EMOJI.findall(post)),
        'em or en dashes': post.count('—') + post.count('–'),
        'exclamation marks': post.count('!'),
        'hashtags': len(re.findall(r'(?<![\w/&])#\w+', post)),
        'links': len(re.findall(r'https?://\S+', post)),
        'list lines': sum(bool(LIST_LINE.match(line)) for line in lines),
        'a question at the end': int(lines[-1].endswith('?')),
        'a lowercase start': int(lines[0][:1].islower()),
    }


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    if sys.argv[1] == '-':
        draft = sys.stdin.read().strip()
        if not draft:
            sys.exit('empty draft')
        for key, value in measure(draft).items():
            print(f'{key}: {value}')
        return

    with open(sys.argv[1], encoding='utf-8') as f:
        posts = split_posts(f.read())
    if not posts:
        sys.exit('no posts found: put each post under a "## " header')

    rows = [measure(p) for p in posts]
    print(f'posts: {len(posts)}')
    for key in rows[0]:
        values = [row[key] for row in rows]
        if key in MEDIANS:
            print(f'{key}: median {statistics.median(values):g} (range {min(values):g}-{max(values):g})')
        else:
            print(f'posts with {key}: {sum(1 for v in values if v) / len(values):.0%}')

    print('\nopeners:')
    for p in posts[:15]:
        print('  ' + p.splitlines()[0][:100])
    print('\nclosers:')
    for p in posts[:15]:
        print('  ' + [line for line in p.splitlines() if line.strip()][-1][:100])


if __name__ == '__main__':
    main()
