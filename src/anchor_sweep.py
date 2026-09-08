#!/usr/bin/env python3
"""Make every postscript reference a LINK, against stable short anchors.

The ledger's index already links, but by HEADING SLUG -- an anchor that encodes
the whole heading, so editing a heading silently breaks every link into it.  This
project rewrites headings whenever a claim is corrected, so slugs are the wrong
anchor.  Instead each postscript gets `<a id="pN"></a>` immediately above its
heading, and every reference in prose becomes `[Postscript N](LEDGER.md#pN)`.

Why bother: it makes "see Postscript 96" CHECKABLE.  An unlinked reference to a
postscript that does not exist, or is misnumbered, is invisible; as a link it
falls to the same broken-link check that validated the specs/ move.  Same
principle as a report naming paths instead of basenames.

Handled: plurals and lists ("Postscripts 55, 57"), ranges ("Postscripts 25-29"),
the two `addendum` headings (anchors p11a, p17a), and the unnumbered first
postscript (p1).  A number is linked ONLY if its anchor exists, which is what
stops "Postscript 46 and 727 configs" from linking 727.

Skipped: fenced code blocks, the ledger's own index (rewritten separately),
session transcripts, bak/, and the github/ publication repo.

    python3 anchor_sweep.py            # dry run, reports what it would do
    python3 anchor_sweep.py --apply
"""
import json
import os
import re
import sys
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(ROOT, 'LEDGER.md')

HEAD_NUM = re.compile(r'^## Postscript (\d+)( addendum)?[:\s]', re.M)
HEAD_FIRST = re.compile(r'^## Postscript: ', re.M)
ANCHOR_LINE = re.compile(r'^<a id="p\d+a?"></a>$', re.M)


def anchors_in_ledger(text):
    """anchor id -> heading line, in file order."""
    out = {}
    for line in text.splitlines():
        m = re.match(r'^## Postscript (\d+)( addendum)?[:\s]', line)
        if m:
            out['p%s%s' % (m.group(1), 'a' if m.group(2) else '')] = line
        elif line.startswith('## Postscript: '):
            out['p1'] = line
    return out


def add_anchors(text):
    """Insert <a id="pN"></a> above each postscript heading, idempotently."""
    lines = text.splitlines(keepends=True)
    out = []
    added = 0
    for i, line in enumerate(lines):
        m = re.match(r'^## Postscript (\d+)( addendum)?[:\s]', line)
        aid = None
        if m:
            aid = 'p%s%s' % (m.group(1), 'a' if m.group(2) else '')
        elif line.startswith('## Postscript: '):
            aid = 'p1'
        if aid:
            prev = out[-1].strip() if out else ''
            if prev != '<a id="%s"></a>' % aid:
                out.append('<a id="%s"></a>\n' % aid)
                added += 1
        out.append(line)
    return ''.join(out), added


def rewrite_index(text):
    """Point the ledger's own index at the short anchors."""
    def sub(m):
        return '- [Postscript %s](#p%s)%s' % (m.group(1), m.group(1), m.group(3))
    new, n = re.subn(r'^- \[Postscript (\d+)\]\(#([^)]+)\)(.*)$', sub, text, flags=re.M)
    # the unnumbered first one
    new, n1 = re.subn(r'^- \[Postscript 1\]\(#p1\)', '- [Postscript 1](#p1)', new, flags=re.M)
    return new, n


def linkify(text, anchors, target):
    """Link plain-text postscript references.  `target` is '' inside the ledger,
    else the relative path to it."""
    # a run is "Postscript(s) N" plus any comma/and/range-joined numbers after it
    run = re.compile(r'\bPostscripts?\b\s+\d+(?:\s*(?:,|and|–|-|to)\s*\d+)*'
                     r'(?:\s+addendum)?')
    num = re.compile(r'\b(\d+)\b')
    out_lines = []
    fence = False
    changed = 0
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith('```'):
            fence = not fence
            out_lines.append(line)
            continue
        # leave code blocks, the index, and already-linked lines alone
        # headings must never be linkified: the heading text IS the anchor target,
        # and a link inside it corrupts both the heading and its slug
        if (fence or line.startswith('    ') or stripped.startswith('#')
                or stripped.startswith('<a id=')
                or stripped.startswith('- [Postscript')):
            out_lines.append(line)
            continue

        def do_run(m):
            nonlocal changed
            seg = m.group(0)

            # "Postscript 11 addendum" is its own heading, anchor p11a
            add = seg.rstrip().endswith('addendum')

            def do_num(mn):
                nonlocal changed
                n = mn.group(1)
                aid = 'p%s%s' % (n, 'a' if add else '')
                if aid not in anchors:
                    aid = 'p' + n
                    if aid not in anchors:
                        return mn.group(0)
                changed += 1
                return '[%s](%s#%s)' % (n, target, aid)
            return num.sub(do_num, seg)

        # never touch a reference already inside a markdown link
        if '](' in line and 'Postscript' in line and re.search(r'\[[^\]]*Postscript', line):
            out_lines.append(line)
            continue
        out_lines.append(run.sub(do_run, line))
    return ''.join(out_lines), changed


def main():
    apply = '--apply' in sys.argv
    led = open(LEDGER, encoding='utf-8').read()
    anchors = anchors_in_ledger(led)
    print('%d postscript headings found (anchors p1..p105 + addenda)' % len(anchors))

    led2, added = add_anchors(led)
    led3, idx = rewrite_index(led2)
    print('anchors to insert: %d ; index entries to repoint: %d' % (added, idx))

    targets = [os.path.join(ROOT, f) for f in sorted(os.listdir(ROOT))
               if f.endswith('.md')]
    sd = os.path.join(ROOT, 'specs')
    targets += [os.path.join(sd, f) for f in sorted(os.listdir(sd)) if f.endswith('.md')]

    report = {}
    for path in targets:
        rel = os.path.relpath(path, ROOT)
        src = led3 if path == LEDGER else open(path, encoding='utf-8').read()
        tgt = '' if path == LEDGER else (
            '../LEDGER.md' if rel.startswith('specs/') else 'LEDGER.md')
        new, n = linkify(src, anchors, tgt)
        if n:
            report[rel] = n
        if apply:
            open(path, 'w', encoding='utf-8').write(new)
        elif path == LEDGER:
            pass
    print('references to link: %d across %d files' % (sum(report.values()), len(report)))
    for k, v in sorted(report.items(), key=lambda x: -x[1])[:10]:
        print('   %-32s %d' % (k, v))
    if apply:
        # POST-CONDITIONS.  The first run of this script linkified the ledger's own
        # HEADINGS -- 106 of them -- because the unit tests covered every input I
        # thought of as content and none of the structure the tool builds.  These
        # three checks refuse the write instead of trusting the author again.
        after = open(LEDGER, encoding='utf-8').read()
        heads_before = re.findall(r'^## Postscript.*$', led, re.M)
        heads_after = re.findall(r'^## Postscript.*$', after, re.M)
        assert heads_before == heads_after, (
            'HEADINGS CHANGED: %d before, %d after -- refusing'
            % (len(heads_before), len(heads_after)))
        assert after.count('[[') == led.count('[['), 'nested links introduced'
        assert set(anchors) == set(re.findall(r'<a id="(p\d+a?)"></a>', after)), \
            'anchor set changed'
        print('post-conditions: headings unchanged, no nested links, anchors intact')
        json.dump({'when': datetime.datetime.now().isoformat(timespec='seconds'),
                   'anchors_inserted': added, 'index_entries_repointed': idx,
                   'references_linked': report,
                   'total_references_linked': sum(report.values())},
                  open(os.path.join(ROOT, 'anchor_sweep_log.json'), 'w'), indent=1)
        print('APPLIED; log in anchor_sweep_log.json')
    else:
        print('(dry run -- rerun with --apply)')


if __name__ == '__main__':
    main()
