#!/usr/bin/env python3
"""Evaluate the count exactly ON the walls, not just in the chambers between them.

Every walk in this project steps ACROSS a wall and counts on the far side, so every count
it has ever produced is a count at a point of codimension 0 within its own stratum. But
the constraint-price argument says the opposite is where to look: a configuration ON a
wall satisfies one more condition than either neighbour, and [P204]'s 0-dimensional
maximisers show the extreme case -- 183 is not in any chamber, it IS an intersection.

So the question the walks cannot answer: is the count on the wall higher than the count
on either side? If it is, records are on the walls and the climb has been stepping over
them.

This is evaluable exactly and needs no new engine. A W4 wall along a single-cube ray is a
root of a rational QUADRATIC, so it lies in Q(sqrt d), and `solve_more_ends.count_at`
counts a configuration whose free cube sits at a0 + r*dv for r = rp + rq*sqrt(d) using
the Q(sqrt d) engine. No rational approximation of the root is involved, so this is the
count AT the wall and not near it.

W3 walls are quartic roots and are NOT generally in Q(sqrt d); they are skipped and
COUNTED as skipped.
"""
import sys, json
from fractions import Fraction as F
sys.path.insert(0, '.')
import dimension as D
from catcache import catalogue
from n78_ends import w4_polys
from solve_more_ends import exact_roots, count_at, root_values
from solved_scan import count

def on_walls(cfg, j, dv, reach=8):
    """counts exactly AT each W4 wall the single-cube ray meets, nearest first"""
    base = list(cfg[:j]) + list(cfg[j + 1:])
    a0 = D.cayley_of(cfg[j])
    pts, lines = catalogue(base)
    here = count(cfg)
    out = []
    seen = set()
    for p in w4_polys(a0, dv, pts):
        for r in exact_roots(p):
            rp, rq, d = r
            v = float(rp) + float(rq) * (float(d) ** 0.5)
            if abs(v) > 1 or v == 0:
                continue
            k = (str(rp), str(rq), d)
            if k in seen:
                continue
            seen.add(k)
            out.append((abs(v), v, r))
    out.sort()
    res = []
    unev = 0
    for _, v, r in out[:reach]:
        c, mag = count_at(base, a0, dv, r)
        if c is not None:
            try:
                c = int(c)              # count_at returns a str on some paths
            except (TypeError, ValueError):
                c = None
        if c is None:
            unev += 1
        res.append((v, c, r[2]))
    return here, res, unev

if __name__ == '__main__':
    # TEST THE HYPOTHESIS WHERE IT IS CHEAP. The n=9 version burned 51 CPU-hours without
    # emerging from its first 8-cube catalogue; the question -- is the count ON a wall
    # higher than on either side? -- is the same question at n=5, where a catalogue costs
    # under a second. Pay n=9 prices only if the cheap answer says there is something there.
    RECORDS = {
        5: [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)],
        6: [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5)],
        9: [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
            (4,-3,-4,-4),(9,-9,9,-22),(109,-11,91,140)],
    }
    N9 = RECORDS[int(sys.argv[1]) if len(sys.argv) > 1 else 5]
    import random
    rng = random.Random(7)
    best = (0, None)
    tot = unevt = 0
    for j in range(1, len(N9)):
        for _ in range(2):
            dv = [F(rng.randint(-6, 6)) for _ in range(3)]
            if not any(dv):
                continue
            here, res, unev = on_walls(N9, j, dv)
            tot += len(res); unevt += unev
            for v, c, d in res:
                if c is not None and c > best[0]:
                    best = (c, (j, dv, v, d))
            hi = [c for _, c, _ in res if c is not None]
            print('cube %d dv=%s : count here %s, ON-WALL counts %s'
                  % (j, [str(x) for x in dv], here, sorted(set(hi), reverse=True)[:6]), flush=True)
    print('\n%d wall points evaluated, %d UNEVALUATED' % (tot, unevt))
    here0 = count(N9)
    print('highest ON-WALL count found: %s  (the configuration itself counts %s)'
          % (best[0], here0))
    if best[0] > here0:
        print('ABOVE THE RECORD at %s' % (best[1],))
    else:
        print('no wall carries a higher count than the record itself, on these lines')
