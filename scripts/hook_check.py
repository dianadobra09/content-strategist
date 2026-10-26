#!/usr/bin/env python3
"""Estimate LinkedIn text wrapping before "...more" on mobile and desktop.

  python3 scripts/hook_check.py outputs/posts/drafts/slug.md   # a post: its ## LinkedIn text
  python3 scripts/hook_check.py - <<'EOF'                      # hooks on stdin, split by =====
  <hook 1>
  =====
  <hook 2>
  EOF

Width model from .claude/skills/linkedin-hook/references/width-model.md: 3 lines show, and the
last one is shorter because "...more" sits on it. A blank line uses a whole line. The
examples' 90 units a line on mobile (128 on desktop) is what wrapped lines fill on average;
a line can hold about 95 (133), and the last one about 80 (122). Those limits reproduce the
two mobile cuts observed in the examples to within a character. A post's hook is its first
line; a hook on stdin is all of it, and the post is assumed to go on after it.

For a post it also prints the first 50 words for an editorial clarity check, with / at line breaks.
This is a saved width model, not a live preview or a claim about ranking. Actual layouts can differ.
"""
import re
import sys

LAYOUTS = (('mobile', 95, 80), ('desktop', 133, 122))
SHOWN = 3
FIRST_WORDS = 50
EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿]')


def char_width(ch):
    if ch == ' ':
        return 1.2
    if ch in "il1!.,;:'’‘jftr/|":
        return 1.0
    if ch in '-()?$&@"“”IJL':
        return 1.5
    if ch in 'MW' or EMOJI.match(ch):
        return 4.0
    if ch in 'mw':
        return 2.8
    if ch.isupper():
        return 2.6
    return 2.2


def width(text):
    return sum(map(char_width, text))


def wrap(paragraph, budget):
    """Greedy word wrap: (start, end) of each line. A blank paragraph is one empty line."""
    words = [m.span() for m in re.finditer(r'\S+', paragraph)]
    if not words:
        return [(0, 0)]
    lines, (start, end) = [], words[0]
    for word_start, word_end in words[1:]:
        if width(paragraph[start:word_end]) > budget:
            lines.append((start, end))
            start = word_start
        end = word_end
    lines.append((start, end))
    return lines


def render(paragraphs, full, last, hook_paragraphs, more_follows):
    """The lines shown, the text around the cut ('' if the cut is at a line break), and whether the hook is all shown."""
    lines = [(p, s, e) for p, para in enumerate(paragraphs) for s, e in wrap(para, full)]
    if len(lines) < SHOWN or (len(lines) == SHOWN and not more_follows):
        return [paragraphs[p][s:e] for p, s, e in lines], '', True

    shown = [paragraphs[p][s:e] for p, s, e in lines[:SHOWN - 1]]
    p, start, _ = lines[SHOWN - 1]
    rest = paragraphs[p][start:]
    i, used = 0, 0.0
    while i < len(rest) and used + char_width(rest[i]) <= last:
        used += char_width(rest[i])
        i += 1
    shown.append(rest[:i].rstrip() + '…more')

    hidden = rest[i:]
    hook_shown = p >= hook_paragraphs or (p == hook_paragraphs - 1 and not hidden.strip())
    cut = ''
    if hidden.strip():
        after = re.match(r'.*?[.!?](?=\s|$)|.*', hidden).group()
        if len(after) > 70:
            after = after[:70] + '…'
        cut = f'…{rest[max(0, i - 20):i]}|{after}'
    return shown, cut, hook_shown


def first_words(text, n):
    """The first n words, with ' / ' where a line breaks, and how many there are."""
    lines, count = [], 0
    for line in text.split('\n'):
        words = line.split()[:n - count]
        if words:
            lines.append(' '.join(words))
            count += len(words)
        if count == n:
            break
    return ' / '.join(lines), count


def report(name, text, is_post):
    paragraphs = text.split('\n')
    hook = paragraphs[:1] if is_post else paragraphs
    hook_lines = [line for line in hook if line.strip()]
    chars = ', '.join(str(len(line)) for line in hook_lines)
    units = ', '.join(f'{width(line):.0f}' for line in hook_lines)

    views, shown_on = [], 0
    for layout, full, last in LAYOUTS:
        shown, cut, hook_shown = render(paragraphs, full, last, len(hook), more_follows=not is_post)
        shown_on += hook_shown
        views.append((layout, shown, cut))

    status = ('cut on mobile and desktop', 'cut on mobile, all shown on desktop',
              'all shown on mobile and desktop')[shown_on]
    print(name)
    print("Estimated layout; check the actual composer when available.")
    print(f"{'first line' if is_post else 'hook'}: {chars} characters ({units} units) · {status}")
    for layout, shown, cut in views:
        print(f'{layout}:')
        for line in shown:
            print(f'  {line}')
        if cut:
            print(f'  cut: {cut}')
    if is_post:
        words, count = first_words(text, FIRST_WORDS)
        label = f'first {FIRST_WORDS} words' if count == FIRST_WORDS else f'all {count} words'
        print(f'{label}: {words}')
    print()


def linkedin_text(path):
    """The ## LinkedIn section of a post file, without 'Other hook' lines; the whole file if it has none."""
    with open(path, encoding='utf-8') as f:
        text = f.read().replace('\r', '')
    section = re.search(r'^## LinkedIn[ \t]*\n(.*?)(?=^## |\Z)', text, flags=re.M | re.S)
    if section:
        text = '\n'.join(line for line in section.group(1).splitlines() if not line.startswith('Other hook'))
    return text.strip()


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args == ['-']:
        hooks = [h.strip() for h in re.split(r'^=====\s*$', sys.stdin.read().replace('\r', ''), flags=re.M)]
        for n, hook in enumerate(filter(None, hooks), 1):
            report(f'hook {n}', hook, is_post=False)
        return
    for path in args:
        text = linkedin_text(path)
        if text:
            report(path, text, is_post=True)
        else:
            print(f'{path}\nno LinkedIn text\n')


if __name__ == '__main__':
    main()
