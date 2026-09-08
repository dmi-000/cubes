#!/usr/bin/env python3
"""d1 as a FILTER, not a ranker.

Measured over 170 sixth cubes on the 393 base, the incidence-derived d1 correlates
with the total at r = +0.973 -- excellent for pruning, and NOT a ranking: the
configuration (4,-4,4,1) has d1 = 216 against the record's 214 and counts 717,
ten fewer.  Every cheap quantity this project has tried behaves that way, strong
in bulk and inverted in the last few units, which is exactly where a record is
decided.  So the filter admits everything plausible and orders nothing; the exact
engine decides.

Every record saturates d_{n-1} = 6n and has d_n = 1, both proved tight, so a
better record must gain in the shallow layers.  And d1 is not a proxy here — it
is computable exactly from incidence data,

    d1 = V3/2 + c + 1 + excess/2

with V3 the triple points on the outer boundary and the excess the extra degree
carried by coincident vertices.  So the objective is an identity, not a
heuristic: rank candidates by the incidence-derived d1 and spend region counts
only on the top of the ranking.

Run: python3 hunt_v3.py [n] [seed]      appends to hunt_v3.log
"""
import collections, itertools, json, os, random, subprocess, sys, time
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments, clip_outside

BASE5 = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

def d1_from_incidence(qs):
    """(V3, excess, predicted d1) for the outer graph"""
    Ms = [rowsT(R) for R in frames(qs)]; n = len(qs)
    pts = {}; links = []
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            parts = [(lo, hi)]
            for k in range(n):
                if k in (i, j): continue
                nxt = []
                for a, b in parts: nxt += clip_outside(p, d, a, b, Ms[k])
                parts = nxt
            for a, b in parts:
                if a >= b: continue
                e = []
                for t in (a, b):
                    P = tuple(p[z]+t*d[z] for z in range(3))
                    pts.setdefault(P, len(pts)); e.append(pts[P])
                links.append(tuple(e))
    deg = collections.Counter()
    for a, b in links: deg[a] += 1; deg[b] += 1
    def onb(M, P):
        h = 0
        for r in range(3):
            v = sum(M[r][k]*P[k] for k in range(3))
            if v > 1 or v < -1: return False
            if v == 1 or v == -1: h += 1
        return h >= 1
    v3 = 0; excess = 0
    for P, idx in pts.items():
        trip = sum(1 for M in Ms if onb(M, P)) >= 3
        if trip: v3 += 1
        excess += deg[idx] - (3 if trip else 2)
    par = list(range(len(pts)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in links: par[f(a)] = f(b)
    c = len({f(x) for x in range(len(pts))}) if pts else 0
    return v3, excess, F(v3, 2) + c + 1 + F(excess, 2)

def count(cfg):
    m = max(abs(v) for q in cfg for v in q)
    eng = ["./cube_regions_n"] if m <= 512 else ["./cube_regions_q2w", "--d", "0"]
    p = subprocess.run(eng+["--quats", ";".join(",".join(map(str,q)) for q in cfg)],
                       capture_output=True, text=True, cwd=HERE)
    try:
        o = json.loads(p.stdout); return o["bounded"], o["by_depth"]
    except Exception: return None, None

def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 20260809)
    log = open(os.path.join(HERE, "hunt_v3.log"), "a")
    base = BASE5
    known_d1, known = 210, 727   # FILTER threshold, not a ranking: r=0.973 with the total
    best = (0, None); tried = 0; t0 = time.time()
    batch = []
    while True:
        h = rng.choice([4, 8, 16, 40, 100, 250, 512])
        q = tuple(rng.randint(-h, h) for _ in range(4))
        if not any(q): continue
        import math
        g = 0
        for v in q: g = math.gcd(g, abs(v))
        q = tuple(v//g for v in q)
        if max(abs(v) for v in q) > 512: continue
        try: v3, ex, pred = d1_from_incidence(base+[q])
        except Exception: continue
        tried += 1
        if pred >= known_d1:            # a FILTER: everything surviving gets an exact count,
            batch.append((pred, q))     # and nothing is ordered by pred
        if tried % 250 == 0:
            got = []
            for pred, q in batch:
                c, bd = count(base+[q])
                if c: got.append((c, q, pred, bd))
            batch = []
            for c, q, pred, bd in got:
                if c > best[0]: best = (c, q)
                if c > known:
                    print("*** BEATS 727: %d  sixth cube %s  predicted d1 %s  %s"
                          % (c, q, pred, bd), file=log, flush=True)
            print("[%5.0fs] tried %6d | predicted-d1 >= %d in %d | best counted %s %s"
                  % (time.time()-t0, tried, known_d1, len(got), best[0], best[1]),
                  file=log, flush=True)

if __name__ == '__main__':
    main()
