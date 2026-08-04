#!/usr/bin/env python3
# Working principles: LEDGER.md is APPEND-ONLY and ordered by
# write time, not by postscript number (numbers get reserved when work is
# delegated and land whenever the report comes back -- see Postscript 9's
# "Postscript 6 still reserved...").  This script does not reorder anything;
# it only regenerates a numeric index so lookup by number is possible.
"""Regenerate the postscript index block at the top of the ledger.

Run after appending a postscript:  python3 index_ledger.py

The index lives between the INDEX markers and is replaced wholesale each run,
so the ledger body is never touched.  Links are GitHub heading anchors, which
makes every entry clickable in the rendered file on GitHub.

INVARIANT: anchor slugs must match GitHub's slugger exactly -- lowercase,
drop everything that is not a letter/digit/space/hyphen, spaces to hyphens,
and de-duplicate repeats with -1, -2, ... in order of appearance.  A wrong
slug produces a link that silently goes nowhere, so slug generation is
verified against the file's own headings (every anchor must be unique).
"""
import re
import sys
import unicodedata

LEDGER = 'LEDGER.md'
START = '<!-- INDEX:START (regenerate with index_ledger.py; do not hand-edit) -->'
END = '<!-- INDEX:END -->'


def slug(text):
    s = text.strip().lower()
    out = []
    for ch in s:
        if ch.isalnum() or ch in ' -_':
            out.append(ch)
        elif unicodedata.category(ch).startswith('L'):
            out.append(ch)
        # everything else (: — ≤ , . ( ) / = " ') is dropped, per GitHub
    return ''.join(out).replace(' ', '-')


def main():
    text = open(LEDGER).read()
    body = text.split(END, 1)[1] if END in text else text

    heads = []           # (number, is_addendum, gloss, anchor)
    seen = {}
    for line in body.splitlines():
        if not re.match(r'^#{2,3} ', line):
            continue
        title = line.lstrip('#').strip()
        a = slug(title)
        n = seen.get(a, 0)
        seen[a] = n + 1
        anchor = a if n == 0 else '%s-%d' % (a, n)
        # The very first postscript predates numbering ("## Postscript: exact
        # certification overturns the ranking"); it is entry 1 in every later
        # cross-reference, so index it as 1 rather than dropping it.
        m = re.match(r'^Postscript (\d+)([a-z]?)\b(.*)$', title)
        if m:
            num, suf, rest = int(m.group(1)), m.group(2), m.group(3)
        elif title.startswith('Postscript'):
            num, suf, rest = 1, '', title[len('Postscript'):]
        else:
            continue
        add = 'addendum' in rest.split(':')[0].lower()
        gloss = rest.split(':', 1)[1].strip() if ':' in rest else rest.strip()
        if len(gloss) > 96:
            gloss = gloss[:93].rsplit(' ', 1)[0] + '…'
        heads.append((num, suf, add, gloss, anchor))

    lines = [START, '',
             '## Postscript index',
             '',
             'The ledger is **append-only and ordered by write time, not by number** —',
             'a postscript number is reserved when the work is delegated and the text',
             'lands when the report comes back, so e.g. 31 sits after 41 and the 29',
             'addendum after that. This index is the lookup by number; regenerate it',
             'with `index_ledger.py` after appending.', '']
    for num, suf, add, gloss, anchor in sorted(heads, key=lambda h: (h[0], h[1], h[2])):
        label = 'Postscript %d%s%s' % (num, suf, ' addendum' if add else '')
        lines.append('- [%s](#%s) — %s' % (label, anchor, gloss) if gloss
                     else '- [%s](#%s)' % (label, anchor))
    lines += ['', END]
    index = '\n'.join(lines)

    if START in text:
        text = re.sub(re.escape(START) + '.*?' + re.escape(END), index,
                      text, flags=re.S)
    else:
        # insert after the opening title paragraph, before the first section
        i = text.index('\n## ')
        text = text[:i] + '\n' + index + '\n' + text[i:]
    open(LEDGER, 'w').write(text)
    print('indexed %d postscript blocks; %d distinct anchors'
          % (len(heads), len(set(h[4] for h in heads))))
    if len(set(h[4] for h in heads)) != len(heads):
        print('WARNING: duplicate anchors', file=sys.stderr)


if __name__ == '__main__':
    main()
