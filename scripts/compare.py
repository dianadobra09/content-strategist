#!/usr/bin/env python3
"""How close a draft was to what the author posted.

  python3 scripts/compare.py draft.txt final.txt
  python3 scripts/compare.py <<'EOF'
  <draft>
  =====
  <final>
  EOF
"""
import difflib
import re
import sys


def load():
    if len(sys.argv) == 3:
        texts = []
        for path in sys.argv[1:]:
            with open(path, encoding='utf-8') as f:
                texts.append(f.read())
        return texts
    parts = re.split(r'^=====\s*$', sys.stdin.read(), maxsplit=1, flags=re.M)
    if len(parts) != 2:
        sys.exit(__doc__)
    return parts


def main():
    draft, final = (text.split() for text in load())
    matcher = difflib.SequenceMatcher(None, draft, final, autojunk=False)
    print(f'similarity: {matcher.ratio():.0%}')
    print(f'words: {len(draft)} -> {len(final)}')
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        old, new = ' '.join(draft[i1:i2]), ' '.join(final[j1:j2])
        if op == 'delete':
            print(f'- cut: {old}')
        elif op == 'insert':
            print(f'+ added: {new}')
        elif op == 'replace':
            print(f'~ {old} -> {new}')


if __name__ == '__main__':
    main()
