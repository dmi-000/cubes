#!/usr/bin/env python3
"""Enumerate a chamber's facets by walking its BOUNDARY, not by casting rays into it.

User's observation: "finding any wall allows walking along the wall to find surrounding
walls."  That is the difference between sampling the facet list and traversing it.
Isotropic rays find a facet only in proportion to the solid angle it subtends, so the
small facets -- which are exactly the ones a climb needs, since they are where the
count can change -- are the ones most often missed.  A facet already found, by
contrast, tells you where to look next: tilt the ray that found it, and as the tilt
grows past the facet's angular extent the first crossing hands you a NEIGHBOURING
facet.  Each discovery seeds more probes, so the walk spreads over the boundary's
adjacency graph instead of over the sphere of directions.

Facets are named by the (n-1)-subset SIGNATURE (METHODS 22) -- the subsets whose count
is unchanged just outside -- so "new facet" is decided by an exact invariant and not by
a distance comparison.

THE CONTROL IS THE POINT.  "Found more facets" is worthless unless the budget is held
fixed, so `compare()` spends the SAME number of ray probes isotropically and reports
both counts.  The walk has to win at equal cost or it is not an improvement.

Both halves report their refusals separately: a probe the engines will not evaluate is
neither a facet nor evidence against one.
"""
import random, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
import climb as C
import dimension as D

def prim(v):
    g = 0
    for x in v:
        g = gcd(g, abs(int(x)))
    return tuple(int(x) // (g or 1) for x in v)

RBALL = 1000

def rand_dir(rng, m, R=RBALL):
    while True:
        v = [rng.randint(-R, R) for _ in range(m)]
        s = sum(x * x for x in v)
        if 0 < s <= R * R:
            return prim(v)

def _setup(cfg):
    D.set_field(0); D.QZERO[:] = [cfg[0]]
    pt = D.point_of(cfg)
    n = len(cfg); ncols = 3 * (n - 1)
    base = C.cfg_at(pt, cfg[0])
    rec = C.cnt(base)
    bsub = tuple(C.cnt([base[i] for i in range(n) if i != j]) for j in range(n))
    den = (max(abs(v) for v in cfg[-1]) or 1) * C.M
    return pt, n, ncols, rec, bsub, den

def walk(cfg, budget=200, seeds=6, tilts=(1024, 256, 64, 16, 4), ntilt=4, seed=0):
    """tilt-driven boundary walk; returns (facets, stats) after `budget` ray probes"""
    pt, n, ncols, rec, bsub, den = _setup(cfg)
    rng = random.Random(seed)
    q = [rand_dir(rng, ncols) for _ in range(seeds)]
    facets, used = {}, 0
    why = {}
    while used < budget:
        if not q:
            # REFILL. Without this the walk stops when its queue empties -- 18 probes
            # against the control's 160 -- and the comparison silently stops being
            # equal-budget. Measured cost of the bug: on one configuration the walk
            # reported 1 facet and the isotropic control 9, which reads as the walk
            # losing when it had simply gone home early.
            q = [rand_dir(rng, ncols) for _ in range(seeds)]
        v = q.pop(0); used += 1
        r = C.first_crossing(pt, v, den, rec, cfg[0], ncols, n, bsub)
        why[r['why']] = why.get(r['why'], 0) + 1
        if r['why'] != 'crossed':
            continue
        sig = r['sig']
        if sig in facets:
            continue
        facets[sig] = (r['t'], r['count'])
        for K in tilts:                       # a NEW facet seeds probes around itself
            for _ in range(ntilt):
                u = rand_dir(rng, ncols)
                w = prim([K * v[i] + u[i] for i in range(ncols)])
                # RESCALE. K*v+u has components ~K*RBALL, and the probe step is v/den,
                # so a large direction is a tall configuration: unrescaled, 76 of 160
                # probes were refused by both engines while the isotropic control had 0.
                # Only the DIRECTION matters, so scaling back to the control's magnitude
                # costs nothing and is not a change of method -- it is the same ray.
                m = max(abs(x) for x in w)
                if m > RBALL:
                    k = -(-m // RBALL)
                    w = prim([x // k if x % k == 0 else round(x / k) for x in w])
                q.append(w)
    return facets, {'probes': used, 'why': why, 'rec': rec}

def isotropic(cfg, budget=200, seed=0):
    """the control: the same number of probes, directions drawn isotropically"""
    pt, n, ncols, rec, bsub, den = _setup(cfg)
    rng = random.Random(seed + 99991)
    facets, why = {}, {}
    for _ in range(budget):
        v = rand_dir(rng, ncols)
        r = C.first_crossing(pt, v, den, rec, cfg[0], ncols, n, bsub)
        why[r['why']] = why.get(r['why'], 0) + 1
        if r['why'] == 'crossed':
            facets.setdefault(r['sig'], (r['t'], r['count']))
    return facets, {'probes': budget, 'why': why, 'rec': rec}

def compare(cfg, budget=200, seed=0):
    fw, sw = walk(cfg, budget=budget, seed=seed)
    fi, si = isotropic(cfg, budget=budget, seed=seed)
    hi_w = max([c for _, c in fw.values()] + [sw['rec']])
    hi_i = max([c for _, c in fi.values()] + [si['rec']])
    print('   count %d, budget %d probes each' % (sw['rec'], budget))
    print('   boundary walk : %3d facets, best neighbour %d   %s' % (len(fw), hi_w, sw['why']))
    print('   isotropic     : %3d facets, best neighbour %d   %s' % (len(fi), hi_i, si['why']))
    return (len(fw), hi_w), (len(fi), hi_i)

if __name__ == '__main__':
    from haarsample import haar_config
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(770001 + 131 * n + 7919 * 0)
    for k in range(int(sys.argv[3]) if len(sys.argv) > 3 else 2):
        cfg = haar_config(rng, n, 128, chart=True)
        print('n=%d config %d' % (n, k), flush=True)
        compare(cfg, budget=budget, seed=k)
