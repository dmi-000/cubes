#!/usr/bin/env python3
"""Does c=2 go with SMALL O-reduced pair angles?  A prediction, not a fishing trip.

At ell=1 the level graph lives on d(union), a sphere on which -I acts freely, so
the quotient is RP^2 and c=2 means NO cycle of the arrangement is essential there
-- no chain of arcs runs from a point to its antipode ([P269] addendum 2).

An arc chain fails to reach halfway around when the seams dA_i n dA_j are
LOCALISED: two cubes at a small relative angle meet in small loops near their
edges, two at a large angle meet in seams that sweep around.  So the reading
PREDICTS c=2 at small O-reduced pair angles.  That is falsifiable and is what is
measured here; the n=4 record, which has c=1, sits at 43.0 deg and 46.8 deg,
near the top of the O-reduced range.
"""
import itertools, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from congruent import OCT, qmul, qconj
from c_level import parse, shares_plane, level_graph, engine


def oreduced_angle(qa, qb):
    """the relative rotation angle of the pair, minimised over the octahedral group"""
    r = qmul(qb, qconj(qa))
    best = math.pi
    for g in OCT:
        s = qmul(g, r)
        n = math.sqrt(sum(float(v) * v for v in s))
        if n == 0:
            continue
        w = abs(float(s[0]) / n)
        best = min(best, 2 * math.acos(min(1.0, w)))
    return math.degrees(best)


def angles(qs):
    return sorted(oreduced_angle(qs[i], qs[j])
                  for i, j in itertools.combinations(range(len(qs)), 2))


def c_of(qs, ell=1):
    if shares_plane(qs) or max(abs(v) for q in qs for v in q) > 512:
        return None
    lv = level_graph(qs).get(ell)
    if lv is None:
        return None
    d = engine(qs)["by_depth"].get(str(ell), 0)
    if lv["E"] - lv["V"] + lv["c"] + 1 != d:
        return None
    return lv["c"], d


KNOWN_C2 = [l.strip() for l in open("c2_configs.txt") if l.strip()]

print("n=4 record (c=1):", [round(a, 1) for a in angles(parse(
    "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"))])
print()
print("KNOWN c=2 configurations -- O-reduced pair angles (deg):")
c2ang, c2max = [], []
for spec in KNOWN_C2:
    qs = parse(spec)
    r = c_of(qs)
    if not r or r[0] != 2:
        continue
    a = angles(qs)
    c2ang += a
    c2max.append(max(a))
    print(f"  d1={r[1]:>3}  max={max(a):5.1f}  mean={sum(a)/len(a):5.1f}   {[round(x,1) for x in a]}")
print()
rnd = random.Random(4)
c1ang, c1max = [], []
tries = 0
while len(c1max) < 60 and tries < 400:
    tries += 1
    n = rnd.choice((4, 4, 5))
    h = rnd.choice((9, 30, 120))
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-h, h) for _ in range(4)) for _ in range(n - 1)]
    if any(not any(q) for q in qs):
        continue
    try:
        r = c_of(qs)
    except Exception:
        continue
    if r and r[0] == 1:
        a = angles(qs)
        c1ang += a
        c1max.append(max(a))
if c2ang and c1ang:
    print(f"c=2  : {len(c2max)} configs, {len(c2ang)} pairs   "
          f"mean angle {sum(c2ang)/len(c2ang):5.1f}   mean MAX-per-config {sum(c2max)/len(c2max):5.1f}"
          f"   largest max {max(c2max):5.1f}")
    print(f"c=1  : {len(c1max)} configs, {len(c1ang)} pairs   "
          f"mean angle {sum(c1ang)/len(c1ang):5.1f}   mean MAX-per-config {sum(c1max)/len(c1max):5.1f}"
          f"   largest max {max(c1max):5.1f}")
