#!/usr/bin/env python3
"""Level-1 two-body weight T, exactly, for any 4-compound over Q(sqrt3, sqrt5).  [RESULTS 3b]

THE QUESTION.  RESULTS 3b rests `max(4) = 183` on three hypotheses; the first is
"Hypothesis T: T <= 48 at n = 4", T = the two-body weight at LEVEL 1,
    T = sum over level-1 two-body vertices of (deg/2 - 1)
      = #(edge-edge crossings on level 1) + 2 * #(shared corners on level 1).
The golden 177 has TOTAL two-body weight 60 (EE 36, SC2 12, [P370]).  Whether that refutes T
depends only on how much of it lies on level 1, i.e. inside NO other cube.  The existing level
tools (`w1_tau.py`) are rational-only, so it had never been measured.

METHOD.  A two-body vertex of cubes a, b lies on two facets of a and two of b (edge-edge), or
three of each (shared corner).  Enumerate: two planes of a, one of b, solved exactly; keep points
on >= 2 facets of each and inside-or-on both, then classify against the other cubes:
    strictly inside some other cube   -> deeper than level 1
    on another cube's boundary        -> not a two-body vertex (a 3-body one), excluded
    outside every other cube          -> level 1
No tolerances: every decision is a sign test in `kfield`.

GATES, known answers, run first:  the golden's TOTAL two-body weight must be 60 ([P370]); the n = 4
record's level-1 T must be 48 ([P282]) and must agree with the rational tool `w1_tau.tau_and_c`.
"""
import sys, os, itertools, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from kfield import K
from golden_a4 import rot, solve3, R5

ROOT = os.path.dirname(os.path.dirname(HERE))


def facets(M, P):
    """(inside_or_on, number of facets P lies on) for cube M -- exact."""
    cnt = 0
    for r in range(3):
        h = sum([M[r][t] * P[t] for t in range(3)], K(0))
        if h == K(1) or h == K(-1):
            cnt += 1
        elif (K(1) - h).sign() < 0 or (K(1) + h).sign() < 0:
            return False, 0
    return True, cnt


def strictly_inside(M, P):
    ok, m = facets(M, P)
    return ok and m == 0


def twobody(CUB):
    """{point: (a, b, kind, level1)} for every two-body vertex."""
    pts = {}
    n = len(CUB)
    for a, b in itertools.permutations(range(n), 2):
        for (ra, rb) in itertools.combinations(range(3), 2):
            for rc in range(3):
                for sg in itertools.product([1, -1], repeat=3):
                    rows = [[K.lift(sg[0]) * CUB[a][ra][t] for t in range(3)],
                            [K.lift(sg[1]) * CUB[a][rb][t] for t in range(3)],
                            [K.lift(sg[2]) * CUB[b][rc][t] for t in range(3)]]
                    P = solve3(rows, [K(1), K(1), K(1)])
                    if P is None:
                        continue
                    oka, ma = facets(CUB[a], P)
                    okb, mb = facets(CUB[b], P)
                    if not (oka and okb) or ma < 2 or mb < 2:
                        continue
                    others = [c for c in range(n) if c not in (a, b)]
                    fc = [facets(CUB[c], P) for c in others]
                    on_other = any(ok and m > 0 for ok, m in fc)
                    if on_other:
                        continue                     # a 3-body vertex, not two-body
                    kind = 'SC2' if (ma, mb) == (3, 3) else ('EE' if (ma, mb) == (2, 2) else '%d%d' % (ma, mb))
                    lvl1 = not any(ok and m == 0 for ok, m in fc)   # strictly inside none
                    key = tuple((t.a, t.b, t.c, t.d) for t in P)
                    pts[key] = (tuple(sorted((a, b))), kind, lvl1)
    return pts


def weights(pts):
    w = {'EE': 1, 'SC2': 2}
    tot = sum(w.get(k, 0) for _, k, _ in pts.values())
    lv1 = sum(w.get(k, 0) for _, k, l in pts.values() if l)
    kinds = {}
    for _, k, l in pts.values():
        kinds.setdefault(k, [0, 0])[0 if l else 1] += 1
    return tot, lv1, kinds


def main():
    out = {}
    # the n = 4 record, rational: the tower's 183 (393 base, cubes 0,1,2,4)
    rec = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (1, 1, 1, 1)]
    CR = [rot(tuple(K(x) for x in q)) for q in rec]
    t, l1, kinds = weights(twobody(CR))
    print('n = 4 RECORD      total two-body %3d   level-1 T %3d   {kind: [level1, deeper]} %s' % (t, l1, kinds))
    out['record'] = {'total': t, 'level1_T': l1, 'kinds': kinds}
    try:
        from w1_tau import tau_and_c
        tau1 = tau_and_c(rec, 1)[0]
        print('   cross-check  w1_tau.tau_and_c(record, level 1) = %s' % tau1)
        out['record']['w1_tau'] = tau1
    except Exception as e:                            # report, never score as agreement
        print('   cross-check  w1_tau UNEVALUATED: %r' % (e,))
        out['record']['w1_tau'] = 'UNEVALUATED'
    # the golden 177, in Q(sqrt5)
    CG = [rot(q) for q in [(R5, K(1), K(1), K(1)), (R5, K(1), K(-1), K(-1)),
                           (R5, K(-1), K(1), K(-1)), (R5, K(-1), K(-1), K(1))]]
    t, l1, kinds = weights(twobody(CG))
    print('GOLDEN 177        total two-body %3d   level-1 T %3d   {kind: [level1, deeper]} %s' % (t, l1, kinds))
    out['golden'] = {'total': t, 'level1_T': l1, 'kinds': kinds}
    print('\nGATES:  golden total must be 60 [P370];  record level-1 T must be 48 [P282] and match w1_tau')
    json.dump(out, open(os.path.join(ROOT, 'data', 'level1_twobody.json'), 'w'), indent=1, default=str)
    print('wrote data/level1_twobody.json')


if __name__ == '__main__':
    main()
