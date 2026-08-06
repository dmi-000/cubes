#!/usr/bin/env python3
"""What is the MAXIMUM on each known line -- not where a known value holds.

1895 was missed because its sweep recorded the indicator of 1891 rather than the
maximum over the line, and sat in the gap between two reported intervals.  The
same reporting habit was applied to every line in the catalogue, so every line is
re-read here for its maximum: solve all W3/W4 roots, evaluate once strictly
between each consecutive pair, take the max.  Chambers whose midpoint overflows
the engine are counted and reported, never silently skipped.
"""
import os
import json, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import incidence2 as I, wall_params as W

ENG = "/Users/dmi/cube-compounds/cube_regions_n"
ENGW = "/Users/dmi/cube-compounds/cube_regions_q2w"
BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

def q_of(c):
    L = 1
    for v in c: L = L*v.denominator//gcd(L, v.denominator)
    iq = [L]+[int(v*L) for v in c]
    g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def between(a, b):
    for k in range(1, 60):
        D = 2**k
        m = F(int(float(a+b)/2*D), D)
        if a < m < b: return m
    return (a+b)/2

def evaluate(cfgs, chunk=4000):
    out = {}
    small = [c for c in cfgs if max(abs(v) for q in c for v in q) <= 512]
    big = [c for c in cfgs if max(abs(v) for q in c for v in q) > 512]
    for group, cmd in ((small, [ENG, "--quats-stdin"]),
                       (big, [ENGW, "--d", "0", "--quats-stdin"])):
        for i in range(0, len(group), chunk):
            part = group[i:i+chunk]
            inp = "\n".join(";".join(",".join(map(str, q)) for q in c) for c in part)+"\n"
            p = subprocess.run(cmd, input=inp, capture_output=True, text=True)
            for line in p.stdout.splitlines():
                try: o = json.loads(line)
                except Exception: continue
                if "quats" not in o or "bounded" not in o: continue
                out[tuple(tuple(int(v) for v in q) for q in o["quats"])] = o["bounded"]
    return [out.get(tuple(tuple(q) for q in c)) for c in cfgs]

def maxline(a0, d, lo, hi, label, known):
    pts, lines = I.base_catalogue()
    roots = sorted(s for s in set(W.w4_params(a0, d, pts)) | set(W.w3_params(a0, d, lines))
                   if lo < s < hi)
    pos = [lo]+roots+[hi]
    mids = [between(pos[i], pos[i+1]) for i in range(len(pos)-1)]
    cfgs = [BASE+[q_of([a0[k]+m*d[k] for k in range(3)])] for m in mids]
    vals = evaluate(cfgs)
    good = [(v, m) for v, m in zip(vals, mids) if v is not None]
    dead = len(vals)-len(good)
    if not good:
        print('%-5s no chamber evaluable' % label, flush=True); return
    mx = max(v for v, _ in good)
    where = [str(m) for v, m in good if v == mx][:3]
    hi_ct = sorted({v for v, _ in good}, reverse=True)[:6]
    print('%-5s %5d chambers (%d unevaluable)  MAX = %d%s  top counts %s'
          % (label, len(vals), dead, mx,
             '  *** ABOVE %d ***' % known if mx > known else '  (= known %d)' % known,
             hi_ct), flush=True)
    if mx > known:
        print('        at s = %s' % ', '.join(where), flush=True)

if __name__ == '__main__':
    W_ = {
     '723': ([F(0),F(0),F(0)], [F(1),F(1),F(1)], F(-7,2), F(26883566786478,10**12), 723),
     'A':  ([F(19,3),F(-7),F(-11)], [F(1),F(-3),F(-6)], F(-20), F(20), 727),
     'B':  ([F(4,35),F(2,5),F(-41,35)], [F(1),F(1),F(-4)], F(-20), F(20), 727),
     'C':  ([F(245,29),F(-295,29),F(428,29)], [F(1),F(-3,2),F(9,4)], F(-20), F(60), 727),
     'D1': ([F(2),F(1,7),F(-5,7)], [F(-1),F(-1,7),F(3,14)], F(-20), F(20), 727),
     'D2': ([F(2),F(1,7),F(-5,7)], [F(-1),F(-4,21),F(2,7)], F(-20), F(20), 727),
    }
    for k in sys.argv[1:]:
        a0, d, lo, hi, kn = W_[k]
        maxline(a0, d, lo, hi, k, kn)
