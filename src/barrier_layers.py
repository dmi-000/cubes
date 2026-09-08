#!/usr/bin/env python3
"""Is the valley deep in the TOTAL but shallow -- or uphill -- in some other measure?

User's observation: two local maxima may be separated by a deep valley in one measure and
a shallow one in another, and if so the shallow measure is the one to walk in.

That is exactly the recorded frustration (JOURNEY Act IV) turned into a search strategy:
the depth layers fight each other, so the total is a sum of competing terms and its dips
need not be dips of the parts. The question has a precise form:

    along the path from one maximum to another, is there a vector of weights w over the
    depth layers such that  w . (p_{i+1} - p_i) > 0  for every step i ?

If such a w exists, the objective  w . profile  increases monotonically along the path:
walking on it crosses the valley WITHOUT a single downhill move, and the anneal budget
that the total demands is not needed at all. That is a linear feasibility problem in the
step-difference vectors, solved here as an LP.

If no w exists, the valley is deep in every linear measure of the profile, and 0 lies in
the convex hull of the step differences -- a much stronger statement than "the total
dips", and one that would say the layers cannot be played off against each other along
this path.

Per-layer drops are reported alongside, since a layer that merely dips LESS is still
useful even when no exactly-monotone w exists.
"""
import json, glob, sys
from fractions import Fraction as F
sys.path.insert(0, '.')
import numpy as np
from scipy.optimize import linprog
import dimension as D
import climb as C
from barrier import align
from frustrate import full

def path_profiles(A, B, steps=32):
    A, B = align(A, B)
    D.set_field(0); D.QZERO[:] = [A[0]]
    pa, pb = D.point_of(A), D.point_of(B)
    if pa is None or pb is None:
        return None, 0
    prof, unev = [], 0
    for k in range(steps + 1):
        t = F(k, steps)
        cf = C.cfg_at([pa[i] + t * (pb[i] - pa[i]) for i in range(len(pa))], A[0])
        d = full(cf)
        if d is None:
            unev += 1; continue
        prof.append((d['bounded'], d['by_depth']))
    return prof, unev

def monotone_weights(prof, n):
    """is there w with w.(p_{i+1}-p_i) > 0 for every step?  LP feasibility."""
    P = np.array([[float(d.get(str(k), 0)) for k in range(n + 1)] for _, d in prof])
    Dif = P[1:] - P[:-1]
    Dif = Dif[np.abs(Dif).sum(axis=1) > 0]
    if len(Dif) == 0:
        return None, None
    m = Dif.shape[1]
    # maximise s subject to  Dif . w >= s,  |w| <= 1,  s <= 1
    c = np.zeros(m + 1); c[-1] = -1.0
    A_ub = np.hstack([-Dif, np.ones((len(Dif), 1))])
    b_ub = np.zeros(len(Dif))
    bounds = [(-1, 1)] * m + [(None, 1)]
    r = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    if not r.success:
        return None, None
    return r.x[-1], r.x[:m]

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    npair = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    seen, cfgs = set(), []
    for f in glob.glob('basin_n*_d*_s*.jsonl'):
        for l in open(f):
            d = json.loads(l)
            if len(d['cfg0']) != n: continue
            c = d.get('end') if d.get('end') is not None else d.get('best_evaluable')
            key = tuple(map(tuple, d['cfg1']))
            if c is None or key in seen: continue
            seen.add(key); cfgs.append((c, [tuple(q) for q in d['cfg1']]))
    cfgs.sort(key=lambda t: -t[0])
    print('n=%d: %d local maxima\n' % (n, len(cfgs)), flush=True)
    for i in range(min(npair, len(cfgs) - 1)):
        A, B = cfgs[i], cfgs[i + 1]
        prof, unev = path_profiles(A[1], B[1])
        if not prof or len(prof) < 5:
            print('%d -> %d : too few evaluable points (%d unevaluable)' % (A[0], B[0], unev)); continue
        tot = [p[0] for p in prof]
        print('%d -> %d  (%d points, %d unevaluable)' % (A[0], B[0], len(prof), unev), flush=True)
        print('   TOTAL      : min %d, drop %d' % (min(tot), min(A[0], B[0]) - min(tot)))
        for k in range(1, n + 1):
            v = [d.get(str(k), 0) for _, d in prof]
            print('   depth-%-4d : min %-5d drop %-5d  ends %d..%d'
                  % (k, min(v), max(v[0], v[-1]) - min(v), v[0], v[-1]))
        s, w = monotone_weights(prof, n)
        if s is None:
            print('   monotone weights: LP failed')
        elif s > 0:
            print('   *** MONOTONE OBJECTIVE EXISTS: margin %.3f, weights %s' % (s, np.round(w, 3)))
            print('       walking on it crosses this valley with NO downhill step.')
        else:
            print('   no linear combination of the depth layers is monotone here'
                  ' (best margin %.3f <= 0)' % s)
        print(flush=True)
