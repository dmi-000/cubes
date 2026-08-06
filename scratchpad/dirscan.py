#!/usr/bin/env python3
"""Exhaustive EXACT single-cube direction scan.

Every direction is an integer triple u in the right-multiplication chart
q_i -> q_i*(1, eps*u), which is exact rational arithmetic and valid at every
rotation -- including the half-turn cube of the n=4 183, where the Cayley chart
is at infinity and every earlier probe of that cube was in the wrong chart.

A direction is reported only if it holds the count at EVERY eps tested; a
direction that holds at 1/16 but not at 1/1024 is a coincidence of scale, not a
tangent.  Controls with known tangents run first.
"""
import itertools, json, subprocess, sys
from fractions import Fraction as F
from math import gcd

ENG = "/Users/dmi/cube-compounds/cube_regions_n"
ENGW = "/Users/dmi/cube-compounds/cube_regions_q2w"

def qmul(p, q):
    w,x,y,z = p; e,f,g,h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g,
            w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)

def redq(q):
    L = 1
    for v in q: L = L*v.denominator//gcd(L, v.denominator)
    iq = [int(v*L) for v in q]
    g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def batch(cfgs):
    """one engine invocation for many configs; falls back to the wide engine"""
    out = []
    small = [c for c in cfgs if max(abs(v) for q in c for v in q) <= 512]
    big = [c for c in cfgs if max(abs(v) for q in c for v in q) > 512]
    for group, cmd in ((small, [ENG, "--quats-stdin"]),
                       (big, [ENGW, "--d", "0", "--quats-stdin"])):
        if not group: continue
        inp = "\n".join(";".join(",".join(map(str, q)) for q in c) for c in group)+"\n"
        p = subprocess.run(cmd, input=inp, capture_output=True, text=True)
        res = {}
        for line in p.stdout.splitlines():
            try: o = json.loads(line)
            except Exception: continue
            key = tuple(tuple(int(v) for v in q) for q in o["quats"])
            res[key] = o.get("bounded")
        for c in group:
            out.append((tuple(tuple(q) for q in c), res.get(tuple(tuple(q) for q in c))))
    return dict((k, v) for k, v in out)

DIRS = [u for u in itertools.product(range(-3, 4), repeat=3)
        if u != (0,0,0) and gcd(gcd(abs(u[0]), abs(u[1])), abs(u[2])) == 1]

def scan(qs, label, epss=(F(1,32), F(1,128), F(1,512))):
    base = batch([list(qs)])[tuple(tuple(q) for q in qs)]
    n = len(qs)
    survivors = []
    for ci in range(1, n):
        cfgs = []
        meta = []
        for u in DIRS:
            for e in epss:
                q = qmul(tuple(F(v) for v in qs[ci]), (F(1), e*u[0], e*u[1], e*u[2]))
                cfg = [tuple(qs[k]) if k != ci else redq(q) for k in range(n)]
                cfgs.append(cfg); meta.append((u, e))
        res = batch(cfgs)
        got = {}
        for cfg, (u, e) in zip(cfgs, meta):
            got.setdefault(u, []).append(res.get(tuple(tuple(q) for q in cfg)))
        for u, vals in got.items():
            if all(v == base for v in vals):
                survivors.append((ci, u))
    print('%-18s count=%-5s  %d directions x %d cubes x %d scales -> %d hold'
          % (label, base, len(DIRS), n-1, len(epss), len(survivors)))
    for ci, u in survivors:
        print('      cube %d  direction %s' % (ci, u))
    return survivors

I = (1,0,0,0)
BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

if __name__ == '__main__':
    print('=== controls ===')
    scan([I, (1,-12,-11,0)], 'n=2 mirror 13')
    scan([I, (10,3,3,3)], 'n=2 diagonal 13')
    print()
    print('=== open cells ===')
    scan([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
    scan(BASE, 'n=5 393')
