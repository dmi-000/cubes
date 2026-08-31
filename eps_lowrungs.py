#!/usr/bin/env python3
"""OUT-OF-SAMPLE test of [P184]'s formula, at the rungs it was NOT fitted on.

[P184] measured, with eps a positive infinitesimal, that the count-preserving null
directions form a hyperplane of dimension **max(0, deficit - 1)** — 0 of 1 at n=6,
1 of 2 at n=7, 2 of 3 at n=8, 3 of 4 at n=9. Four rungs, and the formula was read off
those same four. That is a fit, not a test.

The cheap rungs below are the hard control ([METHODS 4](METHODS.md)): n=3, 4 and 5
all have deficit 1 ([P172]'s table), so the formula predicts **0 preserving
directions** at every one of them — a prediction that can fail outright, unlike the
n=6..9 rows it was fitted to. If any low rung shows a preserving direction, the
formula is wrong; if none does, it has survived a test it could have failed.

Tower members below n=6 are identified by COUNT rather than assumed: [P162] recorded
that the n=4 member is the subset {0,1,2,4}, not the contiguous one, so subsets are
enumerated and matched to the known record instead of guessed.
"""
import itertools, sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
WANT = {3: 63, 4: 183, 5: 393}


def primitive(v):
    from math import gcd
    den = 1
    for x in v:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    iv = [int(F(x) * den) for x in v]
    g = 0
    for x in iv:
        g = gcd(g, abs(x))
    return [x // (g or 1) for x in iv]


print('identifying the tower members below n=6 by COUNT, not by assumption:', flush=True)
members = {}
for k, target in WANT.items():
    hit = None
    for idx in itertools.combinations(range(5), k):
        cubes = [BASE[i] for i in idx]
        D.set_field(0); D.QZERO[:] = [cubes[0]]
        c = D.count_at(D.point_of(cubes), len(cubes))
        if c == target:
            hit = (idx, cubes); break
    if hit is None:
        print('   n=%d: NO %d-subset of BASE counts %d — skipped' % (k, k, target), flush=True)
    else:
        members[k] = hit
        print('   n=%d = %d  subset %s' % (k, target, hit[0]), flush=True)

print('\nprediction from P184: deficit 1 at each of these, so ZERO preserving directions',
      flush=True)
for k in sorted(members):
    idx, cubes = members[k]
    pt, walls, null, ncols = walls_and_null(cubes)
    rec = D.count_at(pt, len(cubes))
    z = count_eps(pt, [Q(0, 0, 0)] * ncols, 0, cubes[0])
    wg = count_eps(pt, [Q(F(x), 0, 0) for x in walls[0]], 0, cubes[0])
    if wg is None:
        wg = count_eps(pt, [Q(F(x), 0, 0) for x in walls[0]], 0, cubes[0], wide=True)
    ok = (z == rec) and (wg is not None and wg != rec)
    print('\nn=%d  record %d  walls %d  ambient %d  nullity %d   CONTROLS zero->%s wall->%s  %s'
          % (k, rec, len(walls), ncols, len(null), z, wg, 'OK' if ok else 'FAIL'), flush=True)
    if not ok:
        print('   controls failed — rows below would be meaningless'); continue
    hold = chg = unev = 0
    for i, v0 in enumerate(null):
        v = primitive(v0)
        vals = []
        for sgn in (1, -1):
            c = count_eps(pt, [Q(F(sgn * x), 0, 0) for x in v], 0, cubes[0])
            if c is None:
                c = count_eps(pt, [Q(F(sgn * x), 0, 0) for x in v], 0, cubes[0], wide=True)
            vals.append(c)
        if None in vals:
            unev += 1; tag = 'UNEVALUATED — not a negative'
        elif vals[0] == rec and vals[1] == rec:
            hold += 1; tag = 'HOLDS both sides'
        elif rec in vals:
            hold += 1; tag = 'holds ONE side'
        else:
            chg += 1; tag = 'changes'
        print('   b%d |v|max %-6d +eps %-6s -eps %-6s  %s'
              % (i, max(abs(x) for x in v), vals[0], vals[1], tag), flush=True)
    pred = max(0, len(null) - 1)
    print('   n=%d: %d hold, %d change, %d unevaluated | predicted %d holding  -> %s'
          % (k, hold, chg, unev, pred,
             'CONFIRMS' if (hold == pred and unev == 0) else
             'INCONCLUSIVE (unevaluated)' if unev else 'REFUTES P184'), flush=True)
