#!/usr/bin/env python3
"""Gate on the Q(sqrt d) port of `dimension.py`, run before any 67 result.

THE CONTROL, and why this one.  A rational configuration embedded in Q(sqrt d)
with zero sqrt-part is the same geometry with the same answer, but it reaches
that answer down a completely different path: Q elements instead of Fractions,
exact-sign comparisons instead of Fraction ordering, sympy expressions carrying
sqrt(d) through every gradient, and cube_regions_q2w --d 2 instead of
cube_regions_n.  The two sides are therefore genuinely different code, not two
spellings of one routine -- the failure mode where a gate's two sides are the
same string and it passes in implausibly little time.

It is also chosen to be HARD for the port rather than convenient: n2edge sits on
a genuine 1-parameter continuum (13 regions hold along an edge-axis arc), so its
lineality is nonzero and the field path has to reproduce a positive-dimensional
answer, not the trivial "isolated point" that any broken Jacobian also returns.

Passing means: identical count, identical tight/wall/binding/inert/entangled
counts, identical candidate dimension, identical verified dimension, identical
cone.  Anything less is not a pass and is reported as a failure.
"""
import json, os, sys, time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dimension as D
from qfield import Q

KEYS = ('count', 'tight', 'walls', 'binding', 'inert', 'entangled',
        'candidate_dim', 'verified')


def run(case, d):
    pt, n = D.CASES[case]
    D.set_field(d)
    D.QZERO[:] = []
    D.BUDGET[0] = 0
    if d:
        pt = [Q(F(x), 0, d) for x in pt]
    t0 = time.time()
    out = D.deltas_and_dimension(pt, n, '%s d=%d' % (case, d))
    out['_secs'] = round(time.time() - t0, 1)
    out['_budget_rejects'] = D.BUDGET[0]
    return out


def main():
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    report, fails = {}, []
    for case in ('n2', 'n2edge'):
        a = run(case, 0)
        b = run(case, d)
        same = {k: (a.get(k), b.get(k)) for k in KEYS if a.get(k) != b.get(k)}
        cone_same = (a['cone']['lineality_dim'] == b['cone']['lineality_dim']
                     and a['cone']['facets'] == b['cone']['facets']
                     and a['cone']['full_dimensional'] == b['cone']['full_dimensional'])
        ok = not same and cone_same
        if not ok:
            fails.append(case)
        print('\n%-8s Q vs Q(sqrt%d): %s%s' %
              (case, d, 'AGREE' if ok else 'DISAGREE ' + str(same),
               '' if cone_same else '  CONE DIFFERS'))
        print('         timing %.1fs vs %.1fs; field-path budget rejects %d'
              % (a['_secs'], b['_secs'], b['_budget_rejects']))
        report[case] = {'Q': a, 'Qsqrt%d' % d: b, 'agree': ok}

    # The continuum is an INDEPENDENT oracle: 13 regions are known to hold along
    # the edge-axis arc, so a lineality of 0 at n2edge would be wrong in both
    # arithmetics and agreement alone would not catch it.
    lin = report['n2edge']['Qsqrt%d' % d]['cone']['lineality_dim']
    if lin < 1:
        fails.append('n2edge continuum')
        print('n2edge lineality %d < 1 -- contradicts the known 13-continuum' % lin)
    else:
        print('n2edge lineality %d >= 1, consistent with the known continuum' % lin)

    json.dump(report, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'dimension_gate.json'), 'w'), indent=1)
    print('\n%s' % ('PORT GATE PASSES' if not fails else 'FAILED: ' + ', '.join(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
