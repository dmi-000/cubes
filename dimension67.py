#!/usr/bin/env python3
"""The two n = 3 maximisers, the only records no crossing-based census has ever
included, because both live outside Q.

max(3) = 67 is PROVED twice already (PROOF_67.md + PROOF_STEP_T.md, and
independently by Mayer-Vietoris + Alexander duality in Postscript 110).  This
run does NOT bear on maximality.  It settles a different question that the whole
project has been quoting without a measurement behind it: whether there are
EXACTLY TWO 67s.  By Postscript 80a's dichotomy a maximiser set is finite or
uncountable and never countably infinite, so if either 67 has a positive-
dimensional locus there are uncountably many 67s and "two" is wrong.

The lattice probe used until now cannot decide this: FAILURE_MODES 11d shows it
cannot separate an isolated point from a locus that misses the lattice.  This
solves for the locus instead of sampling around it.

Prerequisites, both of which must have passed:
    python3 qfield_gate.py       (the scalar layer)
    python3 dimension_gate.py 2  (the port, against the rational path)
"""
import json, os, sys, time
import provenance
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dimension as D
from qfield import Q

# Component (p, q) means p + q*sqrt(d); cube 0 is the identity in both records.
RECORDS = {
    2: ('octahedral', [((1, 0), (0, 0), (0, 0), (0, 0)),
                       ((1, 0), (1, 0), (0, 1), (0, 0)),
                       ((-1, 0), (1, 0), (0, 1), (0, 0))]),
    5: ('golden', [((1, 0), (0, 0), (0, 0), (0, 0)),
                   ((2, 0), (1, 1), (-1, 1), (0, 0)),
                   ((-2, 0), (1, 1), (-1, 1), (0, 0))]),
}


def main():
    only = int(sys.argv[1]) if len(sys.argv) > 1 else None
    out = []
    for d, (name, quats) in sorted(RECORDS.items()):
        if only and d != only:
            continue
        D.set_field(d)
        D.BUDGET[0] = 0
        qs = [tuple(Q(F(p), F(q), d) for p, q in quat) for quat in quats]
        D.QZERO[:] = [qs[0]]
        pt = []
        for q in qs[1:]:
            c = D.cayley_of(q)
            if c is None:
                print('%s: a cube is a half-turn -- at Cayley infinity' % name)
                continue
            pt += c
        label = '%s 67 (Q(sqrt%d))' % (name, d)
        print('=' * 70)
        print('%s   Cayley point %s' % (label, [str(x) for x in pt]))

        # KNOWN ANSWER FIRST, through the machinery's own count path -- not the
        # engine called directly, which qfield_gate already did.  If count_at
        # does not say 67 here, every number after it is measuring the apparatus.
        base = D.count_at(pt, 3)
        print('   count_at -> %s (must be 67)' % base, flush=True)
        if base != 67:
            print('   ABORT: the port does not reproduce the known count')
            out.append({'label': label, 'ABORT': 'count_at gave %s' % base})
            continue

        t0 = time.time()
        r = D.deltas_and_dimension(pt, 3, label, q0=qs[0])
        r['secs'] = round(time.time() - t0, 1)
        r['d'] = d
        r['name'] = name
        r['point'] = [str(x) for x in pt]
        out.append(r)
        json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         'dimension67.json'), 'w'), indent=1)

    provenance.stamp(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'dimension67.json'),
                     note='first-order wall data for both 67s over Q(sqrt d)')
    print('=' * 70)
    for r in out:
        if 'ABORT' in r:
            print('%-28s ABORTED: %s' % (r['label'], r['ABORT']))
            continue
        verdict = ('ISOLATED POINT' if r['candidate_dim'] == 0 else
                   'candidate dim %d -- NOT isolated to first order'
                   % r['candidate_dim'])
        print('%-28s count %d | %d walls (%d binding) | %s | verified %d | '
              'unevaluable %d | %.0fs'
              % (r['label'], r['count'], r['walls'], r['binding'], verdict,
                 r['verified'], r['budget_rejects'], r['secs']))


if __name__ == '__main__':
    main()
