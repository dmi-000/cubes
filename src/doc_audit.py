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
# ROOT is the repository root: the .md documents stayed there when the code moved
# into src/ on 2026-09-08 (MOVE_LOG.json).  Resolves correctly whether this file is
# run from src/ or from the root, so it needs no further change if the layout moves.
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
LEDGER = os.path.join(ROOT, 'LEDGER.md')
RESULTS = os.path.join(ROOT, 'RESULTS.md')
OPENQ = os.path.join(ROOT, 'OPEN_QUESTIONS.md')


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


def results_claims(path=None):
    """(claim text, [cited postscripts], line number) for each claim block"""
    lines = open(path or RESULTS).read().split('\n')
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
        # A claim may cite a PROOF or METHODS file instead of a postscript.  That
        # is a source, and counting it as "cites nothing" overstated the backlog:
        # max(2) = 13 cites METHODS.md, max(3) = 67 cites PROOF_67.md.  Tracked
        # separately, because only a postscript citation can be staleness-checked
        # against the ledger's own cross-reference graph.
        other = re.findall(r'\b([A-Z_0-9]+\.md|`[a-z_0-9]+\.py`)', text)
        claims.append((text.strip(), sorted(set(cited), key=lambda x: int(re.sub(r'\D', '', x))), ln, sorted(set(other))))
    return claims


def dead_anchors():
    """Cross-document links whose target anchor does not exist.

    THE FAILURE THIS EXISTS TO CATCH, measured on 2026-09-12: the sixteen
    postscripts P288-P303 were appended to the ledger without their
    `<a id="pNNN"></a>` lines, so every link written to them -- including the two
    in INTERVENTIONS A11 -- resolved to the top of a 21 000-line file.  The
    postscripts existed; the ANCHORS did not, which reads to an auditor as a
    citation of something that does not exist.  Nine more links into METHODS and
    FAILURE_MODES had been dead longer, because those headings carry a
    `[PRACTICE]` / `[FACT]` prefix that the hand-written slug omitted.

    INVARIANT TO MAINTAIN: a link is checked against an EXPLICIT `<a id>` first
    and only then against the GitHub heading slug.  Relying on the slug alone is
    what broke the METHODS links -- retitling a section silently kills every link
    to it, while an explicit anchor survives retitling.  New sections should get
    an explicit anchor, not a slug link.
    """
    dead = []
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith('.md'):
            continue
        text = open(os.path.join(ROOT, name), encoding='utf-8', errors='replace').read()
        for tgt, anc in re.findall(r'\]\(([A-Za-z0-9_./-]*\.md)#([A-Za-z0-9_-]+)\)', text):
            path = os.path.join(ROOT, tgt)
            if not os.path.exists(path):
                dead.append((name, tgt + '#' + anc, 'target file missing'))
                continue
            t = open(path, encoding='utf-8', errors='replace').read()
            if '<a id="%s"' % anc in t:
                continue
            slugs = {re.sub(r'[^a-z0-9 -]', '', h.lower()).replace(' ', '-')
                     for h in re.findall(r'^#+ (.+)$', t, re.M)}
            if anc.lower() not in slugs:
                dead.append((name, tgt + '#' + anc, 'no anchor and no matching heading'))
    return dead


def main():
    order, refs = ledger_graph()
    claims = results_claims()
    flagged, uncited = [], []
    for text, cited, ln, other in claims:
        if not cited:
            uncited.append((ln, text, other))
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
    # OPEN_QUESTIONS.md carries ELIMINATIONS -- the expensive, rarely-recorded
    # kind of knowledge.  An elimination whose evidence a later postscript
    # revisited may no longer hold, and a ruled-out explanation wrongly believed
    # dead is worse than an untested one: nobody looks at it again.
    if os.path.exists(OPENQ):
        # SECTION-level parse.  OPEN_QUESTIONS.md is prose under '## ' headings,
        # and the claim-block parser used for RESULTS.md caught only its one
        # table -- 3 of 15 citations.  A question is the natural unit here.
        raw = open(OPENQ).read().split('\n')
        oq, cur, start = [], None, 0
        for i, ln_ in enumerate(raw):
            if ln_.startswith('## '):
                if cur is not None:
                    oq.append((cur, sorted(set(re.findall(r'LEDGER\.md#p(\d+[a-z]?)', cur)),
                                           key=lambda x: int(re.sub(r'\D','',x))), start, []))
                cur, start = ln_, i + 1
            elif cur is not None:
                cur += ' ' + ln_.strip()
        if cur is not None:
            oq.append((cur, sorted(set(re.findall(r'LEDGER\.md#p(\d+[a-z]?)', cur)),
                                   key=lambda x: int(re.sub(r'\D','',x))), start, []))
        flag = []
        for text, cited, ln, other in oq:
            later = set()
            for k in cited:
                later.update(refs.get(k, []))
            if later:
                flag.append((ln, cited, sorted(later, key=lambda n: order[n])[-1], text))
        print('-' * 70)
        print('OPEN_QUESTIONS.md: %d questions, %d citing a postscript, %d citing '
              'one a LATER postscript revisits'
              % (len(oq), sum(1 for _, c, _, _ in oq if c), len(flag)))
        for ln, cited, newest, text in flag:
            print('   OPEN_QUESTIONS.md:%-4d cites P%s, revisited by P%s | %s'
                  % (ln, ','.join(cited), newest, text[:70].replace('**', '')))

    print('-' * 70)
    dead = dead_anchors()
    if dead:
        print('%d DEAD ANCHOR LINK(S) -- the cited entry may well exist; the link '
              'does not reach it:' % len(dead))
        for src, link, why in dead:
            print('   %-22s -> %-46s %s' % (src, link, why))
    else:
        print('0 dead anchor links.')

    print('-' * 70)
    hard = [u for u in uncited if not u[2]]
    soft = [u for u in uncited if u[2]]
    print('%d claim blocks cite NO POSTSCRIPT. Of those, %d cite another source '
          '(a proof or methods file) and %d cite NOTHING AT ALL -- the latter '
          'cannot be checked against anything:' % (len(uncited), len(soft), len(hard)))
    print('\n-- no source of any kind (%d):' % len(hard))
    for ln, text, _ in hard[:40]:
        print('   RESULTS.md:%-4d %s' % (ln, text[:108].replace('**', '')))
    print('\n-- cites a file but no postscript (%d):' % len(soft))
    for ln, text, oth in soft[:20]:
        print('   RESULTS.md:%-4d %-70s -> %s' % (ln, text[:70].replace('**', ''), ','.join(oth[:2])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
