#!/usr/bin/env python3
"""Exact chamber decomposition of a line, by solving instead of sampling.

The count and the per-label profile are constant between consecutive wall
crossings, so solving for every W3/W4 root on the line and evaluating ONCE
strictly between each consecutive pair gives the decomposition exactly: no grid,
no chamber narrower than the step, and the ends are named as roots rather than
bracketed.  A sampled chamber count is a lower bound; this one is not.
"""
import os
import json, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solve_ends import catalogue, q_of, BASE
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wall_params as W

ENG = "/Users/dmi/cube-compounds/cube_regions_n"
ENGW = "/Users/dmi/cube-compounds/cube_regions_q2w"

def evaluate(cfgs):
    small = [c for c in cfgs if max(abs(v) for q in c for v in q) <= 512]
    big = [c for c in cfgs if max(abs(v) for q in c for v in q) > 512]
    res = {}
    for group, cmd in ((small, [ENG, "--quats-stdin"]), (big, [ENGW, "--d", "0", "--quats-stdin"])):
        if not group: continue
        inp = "\n".join(";".join(",".join(map(str, q)) for q in c) for c in group)+"\n"
        p = subprocess.run(cmd, input=inp, capture_output=True, text=True)
        for line in p.stdout.splitlines():
            try: o = json.loads(line)
            except Exception: continue
            if "quats" not in o or "bounded" not in o: continue
            k = tuple(tuple(int(v) for v in q) for q in o["quats"])
            pl = o["per_label"]
            res[k] = (o["bounded"], tuple(pl.get(str(i), 0) for i in range(2**len(k))))
    return [res.get(tuple(tuple(q) for q in c), (None, None)) for c in cfgs]

def between(a, b):
    for k in range(1, 60):
        D = 2**k
        m = F(int(float(a+b)/2*D), D)
        if a < m < b: return m
    return (a+b)/2

def decompose(base, a0, d, lo, hi, label, target=None):
    pts, lines = catalogue(base)
    w4 = W.w4_params(a0, d, pts)
    w3 = W.w3_params(a0, d, lines)
    kind = {}
    for s in w3: kind[s] = 'W3'
    for s in w4: kind[s] = 'W4'
    roots = sorted(s for s in set(w3) | set(w4) if lo <= s <= hi)
    pos = [lo]+roots+[hi]
    mids = [between(pos[i], pos[i+1]) for i in range(len(pos)-1)]
    cfgs = [base+[q_of([a0[k]+m*d[k] for k in range(3)])] for m in mids]
    vals = evaluate(cfgs)
    print('%s  window (%.9f, %.9f): %d W4 + %d W3 roots on the line, '
          '%d inside -> %d chambers'
          % (label, float(lo), float(hi), len(w4), len(w3), len(roots), len(mids)), flush=True)
    prev = None
    runs = []
    for i, (m, (c, pl)) in enumerate(zip(mids, vals)):
        left = pos[i]; right = pos[i+1]
        if c != prev:
            runs.append([c, left, right, 1, [pl], 1])
            prev = c
        else:
            runs[-1][2] = right; runs[-1][3] += 1
            if pl not in runs[-1][4]: runs[-1][4].append(pl)
            if pl != runs[-1][4][-1] or vals[i-1][1] != pl: runs[-1][5] += 1
    for c, a, b, n, pls, tc in runs:
        ka = kind.get(a, 'window'); kb = kind.get(b, 'window')
        ra = 'exact %s' % a if a.denominator < 10**6 else ''
        rb = 'exact %s' % b if b.denominator < 10**6 else ''
        print('   count %-6s on (%.12f, %.12f)  %2d wall-chambers, %d TYPE-chambers,'
              ' %d distinct profiles   ends: %s %s / %s %s'
              % (c, float(a), float(b), n, tc, len(pls), ka, ra, kb, rb), flush=True)
    return runs, kind

if __name__ == '__main__':
    which = sys.argv[1]
    if which == '7':
        decompose(BASE+[(7,14,1,-5)], [F(-3,4), F(-1), F(-1)], [F(1), F(0), F(0)],
                  F(-1,8), F(1,64), 'n=7 1217, cube 7 Cayley x')
    elif which == '8':
        decompose(BASE+[(7,14,1,-5),(4,-3,-4,-4)], [F(-1), F(1), F(-61,24)],
                  [F(0), F(0), F(1)], F(-1,8), F(1,8), 'n=8 1895, cube 8 Cayley z')
    elif which == '723':
        decompose(BASE, [F(0), F(0), F(0)], [F(1), F(1), F(1)],
                  F(-5), F(-3), 'n=6 723 line u(1,1,1), lower end')
        decompose(BASE, [F(0), F(0), F(0)], [F(1), F(1), F(1)],
                  F(26), F(30), 'n=6 723 line u(1,1,1), upper end')
