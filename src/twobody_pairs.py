#!/usr/bin/env python3
"""Where does 183 actually come from?  Not the three-body structure.

Three configurations all have W0 = 84, d2 = 66, d3 = 24 -- the entire three-body
structure saturated identically -- yet count 183, 135, 135.  By the level-1
anatomy ([P272])  d1 = W0/2 + (two-body weight) + c + 1 = 42 + T + 2, so the whole
difference is T, the TWO-BODY weight: 48 for the record, 0 for the other two.
183 - 135 = 48 exactly.

[P237] proves T <= 10 per pair, so T <= 60 at n=4, and the record sits at 48 --
8 per pair.  That leaves 12 unclaimed, and

    183 + 12 = 195 = the conjectured max(4).

So the gap between the record and the conjectured maximum is EXACTLY the
unattained two-body budget, and a 195 would need all six pairs at weight 10 with
the three-body structure still saturated.  This measures the per-pair weights to
see whether 10 is reached at all, and by what kind of pair.
"""
import collections, itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import strictly_inside, parse, engine, shares_plane


def twobody_by_pair(qs, ell=1):
    """two-body weight (deg/2 - 1) at level ell, attributed to the pair it lies on"""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    deg = collections.Counter()
    pair = {}
    on = collections.defaultdict(set)
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j) and strictly_inside(mid, Ms[k]))
                if s + 1 != ell:
                    continue
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    deg[P] += 1
                    on[P].update((i, j))
                    pair[P] = (i, j)
    for P in list(on):
        for k in range(n):
            if k in on[P]:
                continue
            v = [abs(sum(Ms[k][q][z] * P[z] for z in range(3))) for q in range(3)]
            if all(x <= 1 for x in v) and any(x == 1 for x in v):
                on[P].add(k)
    w = collections.Counter()
    for P in on:
        if len(on[P]) == 2:
            w[pair[P]] += deg[P] // 2 - 1
    return w


CASES = [("record 183", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4"),
         ("135 (climb)", "1,0,0,0;-49,60,-97,43;13,-18,-59,27;15,47,58,37"),
         ("135 (sweep)", "1,0,0,0;-3,-19,-8,-23;-26,-10,-23,-2;-12,-11,-5,-26")]
rnd = random.Random(303)
for _ in range(12):
    qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-40, 40) for _ in range(4)) for _ in range(3)]
    if not any(not any(q) for q in qs) and not shares_plane(qs):
        CASES.append(("random", ";".join(",".join(str(v) for v in q) for q in qs)))

print(f"{'case':13s} {'total':>6} {'d1':>4} {'T':>4}  per-pair two-body weight (cap 10 each, [P237])")
best = 0
for label, spec in CASES:
    qs = parse(spec)
    e = engine(qs)
    w = twobody_by_pair(qs)
    T = sum(w.values())
    vals = [w.get(p, 0) for p in itertools.combinations(range(4), 2)]
    best = max(best, max(vals) if vals else 0)
    print(f"{label:13s} {e['bounded']:>6} {e['by_depth'].get('1',0):>4} {T:>4}  {vals}")
print(f"\nmax per-pair weight observed: {best}   ([P237] cap is 10)")
print("a 195 needs all six pairs at 10 with W0 = 84, d2 = 66, d3 = 24 held.")
