#!/usr/bin/env python3
# Working principles: LEDGER.md is APPEND-ONLY and ordered by
# write time, not by postscript number (numbers get reserved when work is
# delegated and land whenever the report comes back -- see Postscript 9's
# "Postscript 6 still reserved...").  This script does not reorder anything;
# it only regenerates a numeric index so lookup by number is possible.
"""Regenerate the postscript index block at the top of the ledger.

Run after appending a postscript:  python3 index_ledger.py

The index lives between the INDEX markers and is replaced wholesale each run,
so the ledger body is never touched.

LINKS PREFER THE EXPLICIT ANCHOR.  Most postscripts carry an `<a id="pN">` tag
immediately above the heading, and that is what every cross-reference in every
other document points at (`LEDGER.md#p227`).  Use it when present; fall back to
the GitHub heading slug only for the few blocks that have no tag.  The reason is
not cosmetic: a slug is a function of the heading TEXT, so editing a heading --
which this project does, e.g. re-tagging one `[PARTLY RETRACTED]` after a
correction -- silently breaks its link.  The explicit anchor survives that.

INVARIANT (for the fallback): anchor slugs must match GitHub's slugger exactly
-- lowercase, drop everything that is not a letter/digit/space/hyphen, spaces to
hyphens, and de-duplicate repeats with -1, -2, ... in order of appearance.

STATUS TAGS.  Headings may open with a bracketed tag: `## [VERIFIED] Postscript
229: ...`.  These arrived long after this script and it did not know about them,
so on 2026-09-07 a regeneration silently DROPPED every tagged postscript --
which by then was all of 220 onward -- and replaced 146 working `#pN` links with
slugs.  Strip the tag before matching, and gate the result: the entry count must
not fall.
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
    lines_body = body.splitlines()
    # explicit anchors: <a id="pN"></a> sits above its heading, so remember the
    # most recent one and attach it to the next heading we meet.
    pending = None
    for li, line in enumerate(lines_body):
        am = re.match(r'^\s*<a id="([^"]+)">', line)
        if am:
            pending = am.group(1)
            continue
        if not re.match(r'^#{2,3} ', line):
            continue
        title = line.lstrip('#').strip()
        tm = re.match(r'^\[([A-Z][A-Z ]*)\]\s*', title)
        # The tag is stripped for slug/number matching but CARRIED into the entry. An index
        # reading "filtering before counting is dead" for a postscript headed [REVERSED] is
        # the stale-summary failure this project keeps paying for: the correction lands in
        # the body and the line people scan still asserts the retracted claim.
        status = tm.group(1).strip() if tm else ''
        if status in ('VERIFIED', ''):
            status = ''                       # the default; only exceptions are worth ink
        title = re.sub(r'^\[[A-Z][A-Z ]*\]\s*', '', title)
        a = slug(title)
        n = seen.get(a, 0)
        seen[a] = n + 1
        anchor = a if n == 0 else '%s-%d' % (a, n)
        if pending:
            anchor, pending = pending, None
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
        if status:
            gloss = '**[%s]** %s' % (status, gloss)
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
    # GATE: an index regeneration must never index FEWER blocks than the file has
    # postscript headings. The 2026-09-07 incident dropped 10 of them silently
    # because a heading format had changed, and the run reported success.
    total = len([l for l in body.splitlines()
                 if re.match(r'^#{2,3} (?:\[[A-Z][A-Z ]*\]\s*)?Postscript\b', l)])
    if len(heads) < total:
        print('GATE FAILED: %d headings in the file, only %d indexed -- not writing'
              % (total, len(heads)), file=sys.stderr)
        sys.exit(1)
    open(LEDGER, 'w').write(text)
    explicit = sum(1 for h in heads if re.fullmatch(r'p\d+[a-z]?', h[4]))
    print('indexed %d of %d postscript blocks; %d distinct anchors (%d explicit <a id>, %d slugs)'
          % (len(heads), total, len(set(h[4] for h in heads)), explicit, len(heads) - explicit))
    if len(set(h[4] for h in heads)) != len(heads):
        print('WARNING: duplicate anchors', file=sys.stderr)


if __name__ == '__main__':
    main()
