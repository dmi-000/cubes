#!/usr/bin/env python3
"""Are the NON-body-diagonal weight-10 pairs genuine, or near-misses?

pair10.py classified 45 weight-10 pairs as 36 body-diagonal, 8 generic, 1
coordinate-plane, using a 1e-6 float tolerance on the O-reduced axis.  A pair
whose axis is very close to (1,1,1) would land in "generic" and kill the
four-diagonal argument spuriously.  So the actual axes are printed here, with
their angular distance from the nearest body diagonal, instead of a label.

This is the [P276] question: if weight 10 REQUIRES a body-diagonal axis, then a
cube's four diagonals cap the number of weight-10 pairs and T = 60 is impossible,
putting max(4) below 195.  One genuine generic weight-10 pair refutes that.
"""
import collections, itertools, math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import parse, shares_plane, engine
from twobody_pairs import twobody_by_pair
from pair10 import axis_of

DIAG = [x / math.sqrt(3) for x in (1, 1, 1)]


def dist_to_diagonal(ax):
    """angle (deg) from the O-reduced axis to (1,1,1)/sqrt3, both taken unsigned"""
    d = sum(a * b for a, b in zip(sorted(ax, reverse=True), DIAG))
    return math.degrees(math.acos(min(1.0, max(-1.0, abs(d)))))


rnd = random.Random(5)
SEED = parse("1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4")
pool = [SEED]
for _ in range(200):
    sc = rnd.choice((1, 2, 4))
    pool.append([SEED[0]] + [tuple(v * sc + rnd.randint(-3, 3) for v in q) for q in SEED[1:]])
for _ in range(200):
    h = rnd.choice((6, 12, 40))
    pool.append([(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(3)])

rows = []
for qs in pool:
    if any(not any(q) for q in qs) or shares_plane(qs):
        continue
    if max(abs(v) for q in qs for v in q) > 512:
        continue
    try:
        w = twobody_by_pair(qs)
    except Exception:
        continue
    for p in itertools.combinations(range(4), 2):
        if w.get(p, 0) >= 10:
            ang, ax = axis_of(qs[p[0]], qs[p[1]])
            rows.append((dist_to_diagonal(ax), ang, ax, p,
                         ";".join(",".join(str(x) for x in q) for q in qs)))
rows.sort(key=lambda r: -r[0])
print(f"{len(rows)} weight-10 pairs found; sorted by DISTANCE FROM A BODY DIAGONAL (deg)\n")
print(f"{'dist':>7} {'O-red angle':>12}  axis (sorted, unsigned)")
for d, ang, ax, p, spec in rows[:12]:
    print(f"{d:>7.2f} {ang:>12.3f}  [{ax[0]:.4f}, {ax[1]:.4f}, {ax[2]:.4f}]  pair {p}")
    if d > 1.0:
        print(f"          {spec}")
far = [r for r in rows if r[0] > 1.0]
print(f"\nweight-10 pairs MORE than 1 deg from a body diagonal: {len(far)} of {len(rows)}")
print("if that is 0, weight 10 needs a body diagonal and T=60 is impossible (max(4) < 195).")
print("if it is > 0, the four-diagonal argument fails and 195 stays live.")
