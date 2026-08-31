#!/usr/bin/env python3
"""Where did n=10's walls go?  Census of tight conditions, INCLUDING the discarded.

`walls_of` counts distinct gradients among tight conditions that are not flagged
degenerate.  Degenerate ones are dropped silently, so a rung with many of them
reports few walls for a reason that is about the FILTER, not the geometry — and
[P172]'s +24-walls-per-cube law collapsed to +2 exactly at n=10 (99 -> 101) while
rank kept its +2, meaning every new wall added rank.  That is the signature a
filter spike would produce.

Reports total tight, degenerate, kept, and distinct walls at each rung, so the
discarded count is visible next to the number derived from it rather than implied
by its absence.
"""
import sys
sys.path.insert(0, '.')
import sympy as sp, dimension as D
from wallcount import R

R10 = R[8] + [(57, 57, 56, 57), (19, -2, 15, 24)]
ROWS = [(6, R[6]), (7, R[7]), (8, R[8]), (9, R[9]), (10, R10)]

print('%-4s %7s %8s %7s %7s %7s %7s' %
      ('n', 'count', 'tight', 'degen', 'kept', 'walls', 'rank'), flush=True)
prev = None
for n, quats in ROWS:
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    ncols = 3 * (len(quats) - 1)
    vars_ = sp.symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, quats[0])
    tight, loose = D.cached_conditions(Rs, len(quats), vars_, pt,
                                       D.quats_of(pt, quats[0]), quats[0])
    degen = sum(1 for t in tight if t['degenerate'])
    good = [t for t in tight if not t['degenerate']]
    seen, walls = set(), []
    for t in good:
        g = t['grad']
        piv = next((x for x in g if x != 0), None)
        if piv is None:
            continue
        k = tuple(str(x / piv) for x in g)
        if k not in seen:
            seen.add(k); walls.append(g)
    rank = ncols - len(D.nullspace(walls, ncols))
    print('%-4d %7d %8d %7d %7d %7d %7d %s' %
          (n, D.count_at(pt, len(quats)), len(tight), degen, len(good),
           len(walls), rank,
           '' if prev is None else '(walls %+d, degen %+d)' % (len(walls) - prev[0],
                                                              degen - prev[1])),
          flush=True)
    prev = (len(walls), degen)
