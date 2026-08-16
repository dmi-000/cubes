#!/usr/bin/env python3
"""Staleness triage for RESULTS.md against LEDGER.md.

THE FAILURE THIS EXISTS TO CATCH, measured on 2026-08-17: the ledger holds 122
postscripts with 389 cross-references between them but exactly ONE link back out
to RESULTS.md.  Supersession therefore propagates perfectly INSIDE the record and
not at all OUT of it.  A correction arrives as a new postscript, which is a
complete act in the ledger's own terms, while the summary document that gets read
keeps the superseded claim.  That is how "(2,1,1) and (1,1,1,1) were never
enumerated" survived in RESULTS.md for two weeks after Postscript 62 enumerated
one of each -- and survived longest of all in the SUPERSEDED-CLAIMS TABLE, the
mechanism built to stop exactly this.

THE SIGNAL.  If a RESULTS claim cites Postscript k, and some LATER postscript
cross-references k, then the project revisited k after that claim was written and
the claim may not have been revisited with it.  Cheap, mechanical, and aimed at
the actual hole in the link graph.

WHAT THIS IS NOT.  A later reference is not a refutation -- most are ordinary
citations.  This tool produces CANDIDATES FOR REVIEW and ranks them; it does not
decide, and it must not be read as deciding.  A claim it does not flag is a claim
it has said nothing about, not a claim it has verified.  Claims citing NOTHING
are reported separately and are the worse category: unfalsifiable by this method
rather than cleared by it.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, 'LEDGER.md')
RESULTS = os.path.join(HERE, 'RESULTS.md')


def ledger_graph():
    """(postscript order, {k: [later postscripts referencing k]})"""
    text = open(LEDGER).read()
    heads = [(m.start(), m.group(1))
             for m in re.finditer(r'^## Postscript (\d+[a-z]?)', text, re.M)]
    order = {name: i for i, (_, name) in enumerate(heads)}
    bounds = [(heads[i][0], heads[i + 1][0] if i + 1 < len(heads) else len(text),
               heads[i][1]) for i in range(len(heads))]
    refs = {}
    for start, end, name in bounds:
        body = text[start:end]
        for m in re.finditer(r'\(#p(\d+[a-z]?)\)', body):
            tgt = m.group(1)
            if tgt == name or tgt not in order:
                continue
            if order[name] > order.get(tgt, -1):
                refs.setdefault(tgt, []).append(name)
    return order, refs


def results_claims():
    """(claim text, [cited postscripts], line number) for each claim block"""
    lines = open(RESULTS).read().split('\n')
    out, cur, start = [], None, 0
    for i, ln in enumerate(lines):
        if ln.startswith('- **') or (ln.startswith('| ') and ln.count('|') >= 3):
            if cur is not None:
                out.append((cur, start))
            cur, start = ln, i + 1
        elif cur is not None and (ln.startswith('- ') or ln.startswith('## ')):
            out.append((cur, start))
            cur = None
        elif cur is not None:
            cur += ' ' + ln.strip()
    if cur is not None:
        out.append((cur, start))
    claims = []
    for text, ln in out:
        cited = re.findall(r'LEDGER\.md#p(\d+[a-z]?)', text)
        claims.append((text.strip(), sorted(set(cited), key=lambda x: int(re.sub(r'\D', '', x))), ln))
    return claims


def main():
    order, refs = ledger_graph()
    claims = results_claims()
    flagged, uncited = [], []
    for text, cited, ln in claims:
        if not cited:
            uncited.append((ln, text))
            continue
        later = set()
        for k in cited:
            later.update(refs.get(k, []))
        if later:
            newest = max(later, key=lambda n: order[n])
            flagged.append((len(later), order[newest], ln, cited, sorted(
                later, key=lambda n: order[n])[-4:], text))
    flagged.sort(key=lambda r: (-r[1], -r[0]))

    print('LEDGER: %d postscripts | RESULTS: %d claim blocks' % (len(order), len(claims)))
    print('%d claims cite a postscript that a LATER postscript revisits '
          '-- CANDIDATES, not verdicts\n' % len(flagged))
    for nlater, _, ln, cited, latest, text in flagged:
        print('RESULTS.md:%-4d cites P%s | revisited by %d later, newest P%s'
              % (ln, ','.join(cited), nlater, latest[-1]))
        print('   %s' % text[:150].replace('**', ''))
        print()
    print('-' * 70)
    print('%d claim blocks cite NOTHING -- this tool can say nothing about them, '
          'which is worse than being flagged, not better:' % len(uncited))
    for ln, text in uncited[:40]:
        print('   RESULTS.md:%-4d %s' % (ln, text[:110].replace('**', '')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
