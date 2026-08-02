#!/usr/bin/env python3
"""Find claims a new result may have invalidated.

This does NOT update anything and cannot tell truth from falsehood.  It only
answers "where else does the project talk about this?", so that the discipline
— when a result changes, go correct what it contradicts — costs a few seconds
instead of a grep-and-hope.

Why it exists: on 2026-08-01 an audit found ten stale claims across PROJECT.md
and JOURNEY.md, including two theorems still listed as open weeks after being
proved.  Every one was in a SUMMARY position — an opening paragraph, an
open-questions list, a file footer, a table-of-contents description — never in
the body prose, which the dated-annotation convention had kept honest.  Those
positions are where a fact gets restated away from the place it is maintained,
and restatements are what rot.

Usage:
    python3 stale_check.py 723 1207 1879        # superseded record values
    python3 stale_check.py "proven maximal" "still open"
    python3 stale_check.py --records            # every record value, old and new
"""
import glob
import os
import re
import sys

# Positions where a restated fact is most likely to rot, by how the line looks.
SUMMARY_HINTS = (
    (re.compile(r'^\s*#{1,3}\s'), 'heading'),
    (re.compile(r'^\s*\d+\.\s+\*\*'), 'numbered claim (open-questions style)'),
    (re.compile(r'^\s*\|'), 'table row'),
    (re.compile(r'^\s*\*[^*]'), 'italic note / footer'),
    (re.compile(r'Last updated|updated \d{4}-\d{2}-\d{2}'), 'dated header'),
)

RECORDS = ['13', '67', '183', '393', '723', '727', '1207', '1211', '1217',
           '1879', '1889', '1891']


def classify(line):
    for pat, what in SUMMARY_HINTS:
        if pat.search(line):
            return what
    return None


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    terms = RECORDS if args[0] == '--records' else args
    docs = sorted(f for f in glob.glob('*.md')
                  if not os.path.basename(f)[:4].isdigit())   # skip transcripts
    for term in terms:
        hits = []
        for doc in docs:
            for i, line in enumerate(open(doc, errors='ignore'), 1):
                if term in line:
                    hits.append((doc, i, line.rstrip(), classify(line)))
        if not hits:
            continue
        summary = [h for h in hits if h[3]]
        print('\n=== %r: %d mentions in %d files (%d in summary positions)'
              % (term, len(hits), len({h[0] for h in hits}), len(summary)))
        for doc, i, line, what in summary:
            print('  [%s] %s:%d  %s' % (what, doc, i, line.strip()[:96]))
        rest = len(hits) - len(summary)
        if rest:
            print('  (%d further mentions in body prose — usually fine if the'
                  ' document annotates rather than restates)' % rest)
    print('\nThis tool finds mentions, not errors. Deciding which are now false'
          '\nis the part that has to be done by hand.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
