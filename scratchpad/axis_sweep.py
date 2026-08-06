#!/usr/bin/env python3
"""Sweep every free cube along every Cayley axis, far past the known plateau.

This is the move that turned up 1895: the n=8 sweep along cube 7's z had been
reported as "1891 on [0,3/32] and again on [15/64,3/8]", but continuing it finds
1895 sitting just beyond the first interval.  A sweep that stops where the
count first drops reports the chamber, not the line.
"""
import json, subprocess, sys
from fractions import Fraction as F
from math import gcd

ENG = "/Users/dmi/cube-compounds/cube_regions_n"
ENGW = "/Users/dmi/cube-compounds/cube_regions_q2w"

def q_of(c):
    L = 1
    for v in c: L = L*v.denominator//gcd(L, v.denominator)
    iq = [L]+[int(v*L) for v in c]
    g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def cay(q):
    w, x, y, z = q
    return [F(x, w), F(y, w), F(z, w)]

def batch(cfgs):
    small = [c for c in cfgs if max(abs(v) for q in c for v in q) <= 512]
    big = [c for c in cfgs if max(abs(v) for q in c for v in q) > 512]
    res = {}
    for group, cmd in ((small, [ENG, "--quats-stdin"]),
                       (big, [ENGW, "--d", "0", "--quats-stdin"])):
        if not group: continue
        inp = "\n".join(";".join(",".join(map(str, q)) for q in c) for c in group)+"\n"
        p = subprocess.run(cmd, input=inp, capture_output=True, text=True)
        for line in p.stdout.splitlines():
            try: o = json.loads(line)
            except Exception: continue
            res[tuple(tuple(int(v) for v in q) for q in o["quats"])] = o["bounded"]
    return [res.get(tuple(tuple(q) for q in c)) for c in cfgs]

def sweep(cubes, label, D=64, R=32):
    base = batch([list(cubes)])[0]
    print('%s   base %s' % (label, base), flush=True)
    top = base
    for ci in range(1, len(cubes)):
        c0 = cay(cubes[ci])
        for ax in range(3):
            svals = [F(k, D) for k in range(-R, R+1)]
            cfgs = []
            for s in svals:
                c = list(c0); c[ax] += s
                cfgs.append([cubes[k] if k != ci else q_of(c) for k in range(len(cubes))])
            res = batch(cfgs)
            m = max((r for r in res if r is not None), default=None)
            hits = [str(s) for s, r in zip(svals, res) if r == base]
            mark = ''
            if m is not None and m > base:
                mark = '   *** BEATS THE RECORD: %d at s = %s ***' % (
                    m, [str(s) for s, r in zip(svals, res) if r == m][0])
                top = max(top, m)
            print('   cube %d axis %s: max %s over s in [-%s,%s]; base held at %d of %d samples%s'
                  % (ci, 'xyz'[ax], m, F(R, D), F(R, D), len(hits), len(svals), mark), flush=True)
    print('   best seen: %s' % top, flush=True)

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
if __name__ == '__main__':
    which = sys.argv[1]
    if which == '6':
        sweep(BASE+[(7,14,1,-5)], 'n=6 727 record')
    elif which == '7':
        sweep(BASE+[(7,14,1,-5),(4,-3,-4,-4)], 'n=7 1217')
    elif which == '8':
        sweep(BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)], 'n=8 1895 (new)')
    elif which == '5':
        sweep(BASE, 'n=5 393')
    elif which == '4':
        sweep([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
