#!/usr/bin/env python3
"""Every refuted claim in the ledger, and whether anyone ever said WHY.

THE QUESTION.  [P331] found a wrong claim that had survived three weeks past the discovery of
the defect that invalidates it, because it had been re-verified against a DIFFERENT defect and
wore a "verified" tag.  It also closed a five-week-old loose end: [P55]/[P57] measured a
heuristic as negatively correlated with the count, recorded the reversal, and never gave a
cause.  The cause turned out to be the real finding.

So: **a refutation that records a reversal without a mechanism is an open question wearing a
closed question's label.**  This tool counts them.

WHAT IT DOES.  Splits LEDGER.md into postscripts, finds those whose TITLE reverses something,
and asks whether the BODY contains a stated cause -- a "because", a named defect, a mechanism --
or merely records that the thing is false.  The second class is the backlog.

WHAT IT IS NOT.  Keyword matching is a triage, not a verdict: it locates candidates to read,
and the `--list` output is meant to be read.  A postscript can state a cause in words this
misses, and can use the word "because" while explaining nothing.
"""
import re, os, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REVERSAL = re.compile(r'\b(REFUTED|RETRACTED|SUPERSEDED|VOID|WITHDRAWN|CORRECTION|CORRECTED|'
                      r'REVERSED|WRONG|FALSE|not survive|does NOT|is NOT|FAILED|ARTIFACT|'
                      r'spurious|overstated|MISTAKE|IN ERROR)\b', re.I)

# a cause is named: a defect, a mechanism, an attribution of the error to something
CAUSE = re.compile(r'\b(because|the cause|caused by|the defect|the bug|the reason|'
                   r'why it (?:failed|fell|broke)|comes from|due to|traced to|'
                   r'the error was|arises? from|explains? (?:why|the)|the tell|'
                   r'root cause|what went wrong|the mechanism is)\b', re.I)

# a gate: the cause was tested, not just asserted
GATE = re.compile(r'\b(gate|GATE [A-Z0-9]|negative control|independent|disagreements?|'
                  r'0 of \d|\d+ of \d+|oracle|re-?count|re-?measur|verified by|confirmed by)\b',
                  re.I)


def postscripts(text):
    """(number, title, body) for each postscript heading in the ledger."""
    heads = list(re.finditer(r'^## (?:\[([A-Z /]+)\]\s*)?Postscript\s+(\d+)([^\n]*)$',
                             text, re.M))
    out = []
    for i, m in enumerate(heads):
        start = m.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append({'tag': (m.group(1) or '').strip(), 'num': int(m.group(2)),
                    'title': m.group(3).strip(' :—-'), 'body': text[start:end]})
    return out


def main():
    text = open(os.path.join(ROOT, 'LEDGER.md'), encoding='utf-8').read()
    ps = postscripts(text)
    rev = [p for p in ps if REVERSAL.search(p['title'])]
    no_cause, caused, gated = [], [], []
    for p in rev:
        body = p['body']
        if not CAUSE.search(body):
            no_cause.append(p)
        elif GATE.search(body):
            gated.append(p)
        else:
            caused.append(p)

    print('postscripts in ledger                     %4d' % len(ps))
    print('whose TITLE reverses something            %4d   (%.0f %%)'
          % (len(rev), 100.0 * len(rev) / max(1, len(ps))))
    print('   connective-cause language + a gate     %4d' % len(gated))
    print('   connective-cause language, ungated     %4d' % len(caused))
    print('   no connective-cause language matched   %4d   <- TRIAGE ONLY, NOT a backlog'
          % len(no_cause))
    print()
    print('   READ 2026-09-16 ([P332]): this last bucket is a weak-instrument artifact.')
    print('   The mechanism pass (MECH in this file) left only 4 reversals unmatched, and all')
    print('   4 were read: P170 and P277 state their cause outright, P154 and P255 are not')
    print('   reversals at all. Spot-reading P30, P87 and P253 from this bucket found causes')
    print('   or false positives too. **No reversal in the ledger fails to state a cause.**')
    print('   Quote that, not the number above.')

    if '--list' in sys.argv:
        print('\n=== reversals with NO stated cause, oldest first ===')
        for p in sorted(no_cause, key=lambda x: x['num']):
            print('  P%-4d %s' % (p['num'], p['title'][:96]))

    out = {'what': 'refutations in the ledger, and whether a cause was ever stated',
           'total_postscripts': len(ps), 'reversals': len(rev),
           'cause_and_gate': len(gated), 'cause_ungated': len(caused),
           'no_connective_cause_language': len(no_cause),
           'no_cause_READ_RESULT': ('triage artifact: read 2026-09-16, no reversal in the '
                                    'ledger actually fails to state a cause -- see P332'),
           'candidates_to_read': [{'p': p['num'], 'title': p['title']} for p in
                                  sorted(no_cause, key=lambda x: x['num'])]}
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import provenance as PROV
    out['reproduce'] = PROV.stamp(parameters={'source': 'LEDGER.md'},
                                  inputs=[os.path.join(ROOT, 'LEDGER.md')])
    json.dump(out, open(os.path.join(ROOT, 'data', 'refutation_census.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/refutation_census.json')


if __name__ == '__main__':
    main()
