#!/usr/bin/env python3
"""How many pairs can reach two-body weight 10 at once, and does 10 need a body diagonal?

[P276]: max(4) <= 195 requires T = 60, i.e. ALL SIX pairs at [P237]'s cap of 10.
The record manages three (its hub pairs, body-diagonal axes) and 6 on the other
three.  A cube has only four body diagonals, so if weight 10 needs one, six is
impossible and the true max(4) is below 195.

Measured here: the per-pair weight distribution, how many pairs hit 10 together,
and the O-reduced axis of every weight-10 pair -- classified as body diagonal,
coordinate-plane, or neither, using the project's own pair rules.
"""
import collections, itertools, math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import parse, shares_plane, engine
from twobody_pairs import twobody_by_pair
from congruent import OCT, qmul, qconj


def axis_of(qa, qb):
    """O-reduced relative rotation: (angle deg, unit axis) minimising the angle"""
    r = qmul(qb, qconj(qa))
    best = None
    for g in OCT:
        s = qmul(g, r)
        n2 = sum(float(v) * v for v in s)
        if n2 == 0:
            continue
        n = math.sqrt(n2)
        w = abs(float(s[0]) / n)
        ang = 2 * math.acos(min(1.0, w))
        if best is None or ang < best[0]:
            v = [float(x) / n for x in s[1:]]
            m = math.sqrt(sum(x * x for x in v)) or 1.0
            best = (ang, [abs(x) / m for x in v])
    return math.degrees(best[0]), sorted(best[1], reverse=True)


def classify(ax):
    a, b, c = ax
    if abs(a - b) < 1e-6 and abs(b - c) < 1e-6:
        return "body diagonal (1,1,1)"
    if c < 1e-6:
        return "coordinate plane"
    if b < 1e-6:
        return "face axis"
    return "generic"


rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 220
hist = collections.Counter()
n10 = collections.Counter()
kinds = collections.Counter()
best = None
SEED = parse("1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4")
pool = [SEED]
for _ in range(N):
    sc = rnd.choice((1, 2, 4))
    pool.append([SEED[0]] + [tuple(v * sc + rnd.randint(-3, 3) for v in q) for q in SEED[1:]])
for _ in range(N):
    h = rnd.choice((6, 12, 40))
    pool.append([(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(3)])
for qs in pool:
    if any(not any(q) for q in qs) or shares_plane(qs):
        continue
    if max(abs(v) for q in qs for v in q) > 512:
        continue
    try:
        w = twobody_by_pair(qs)
        e = engine(qs)
    except Exception:
        continue
    vals = [w.get(p, 0) for p in itertools.combinations(range(4), 2)]
    for v in vals:
        hist[v] += 1
    k = sum(1 for v in vals if v >= 10)
    n10[k] += 1
    for p, v in zip(itertools.combinations(range(4), 2), vals):
        if v >= 10:
            ang, ax = axis_of(qs[p[0]], qs[p[1]])
            kinds[classify(ax)] += 1
    T = sum(vals)
    if best is None or T > best[0]:
        best = (T, e["bounded"], vals, ";".join(",".join(str(x) for x in q) for q in qs))
print("per-pair two-body weight histogram:", dict(sorted(hist.items())))
print("configurations by #pairs at weight >= 10:", dict(sorted(n10.items())))
print("axis type of every weight-10 pair:", dict(kinds))
print(f"\nbest total T found: {best[0]} (count {best[1]}) pairs {best[2]}")
print(f"  {best[3]}")
print("T = 60 (all six at 10) is what max(4) = 195 would need.")
