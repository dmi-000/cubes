#!/usr/bin/env python3
"""Refine the integer-offset hits from shapes.py to rational resolution.

shapes.py sweeps last_cube + t*dir over INTEGER t, so it can only see loci that are
wide in the integer lattice.  A hit of k consecutive offsets is a LOWER bound on a
locus; a hit of 1 is not evidence of anything.  Here each hit is re-swept over
rational t on the WIDE engine, which is required: fine offsets canonicalise above
the narrow engine's 512 cap (FAILURE_MODES 16c).
"""
import json, subprocess
from fractions import Fraction as F
from math import gcd
from growth727 import BASE

TOWER = {
    727:  BASE + [(7, 14, 1, -5)],
    1217: BASE + [(7, 14, 1, -5), (4, -3, -4, -4)],
    1895: BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61)],
    2785: BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61),
                  (56, 56, 55, 56)],
}
# rung -> (direction, integer t range reported by shapes.py)
HITS = [(1217, (0, 1, 0, 0), -60, -45),
        (1895, (0, 0, 0, 1), 0, 4),
        (1895, (1, -1, 1, 1), -59, -53),
        (2785, (0, 0, 1, 0), -5, -1)]


def canon(q):
    den = 1
    for x in q:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    w = [int(F(x) * den) for x in q]
    g = 0
    for v in w:
        g = gcd(g, abs(v))
    w = [v // (g or 1) for v in w]
    for v in w:
        if v > 0:
            break
        if v < 0:
            w = [-x for x in w]
            break
    return tuple(w)


def batch(cfgs):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run(['./cube_regions_q2w', '--d', '0', '--quats-stdin'],
                       input=inp, capture_output=True, text=True)
    out = []
    for line in p.stdout.splitlines():
        try:
            out.append(json.loads(line).get('bounded'))
        except Exception:
            out.append(None)
    return out + [None] * (len(cfgs) - len(out))


for rung, d, lo, hi in HITS:
    cubes = TOWER[rung]
    c = cubes[-1]
    STEP = 12
    ts = [F(k, STEP) for k in range(lo * STEP, hi * STEP + 1)]
    cfgs = [cubes[:-1] + [canon(tuple(ci + t * di for ci, di in zip(c, d)))]
            for t in ts]
    vals = batch(cfgs)
    runs, cur = [], None
    for t, v in zip(ts, vals):
        if v == rung:
            cur = [t, t] if cur is None else [cur[0], t]
        elif cur:
            runs.append(tuple(cur)); cur = None
    if cur:
        runs.append(tuple(cur))
    nun = sum(1 for v in vals if v is None)
    print('%-5d dir %-12s  t in [%d,%d] step 1/%d : %d pts, %d unevaluable'
          % (rung, str(d), lo, hi, STEP, len(ts), nun))
    for a, b in runs:
        print('        holds on [%s, %s]  width %s  (%d pts)'
              % (a, b, b - a, int((b - a) * STEP) + 1))
    if not runs:
        print('        holds nowhere at this resolution')
