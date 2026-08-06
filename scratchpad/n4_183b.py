#!/usr/bin/env python3
"""n=4, 183 aligned probe in CAYLEY coordinates (chart 2 for the half-turn cube)."""
import sys
from math import gcd
from fractions import Fraction as F
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from sweep import run

REC = [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]

def intq(fq):
    L = 1
    for v in fq:
        L = L * v.denominator // gcd(L, v.denominator)
    iq = [int(v*L) for v in fq]
    g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def perturb(ci, coord, delta):
    """coord 0,1,2 = Cayley x,y,z (for w!=0) ; for w==0 cube use w-chart offset."""
    q = [F(v) for v in REC[ci]]
    if q[0] == 0:
        # chart 2: scale so the varied slot moves; treat Cayley coords as x/w -> use
        # inverted chart (w/x, y/x, z/x) around x-normalisation
        pass
    w = q[0]
    cay = [q[1]/w, q[2]/w, q[3]/w]
    cay[coord] += delta
    return intq([F(1), cay[0], cay[1], cay[2]])

base_cnt, base_pl = run(list(REC), wide=True)
print("base", base_cnt)

for eps_den in (64, 256, 1024):
    eps = F(1, eps_den)
    surv = []
    line = []
    for ci in (2, 3):
        for coord in range(3):
            for sgn in (1,-1):
                cfg = [REC[0], REC[1]] + [perturb(k, coord, sgn*eps) if k==ci else REC[k] for k in (2,3)]
                c, pl = run(cfg, wide=True)
                tag = "%d.%s%s" % (ci, "xyz"[coord], "+-"[sgn<0])
                line.append("%s=%s" % (tag, c))
                if c == base_cnt: surv.append((tag, pl==base_pl))
    # cube 1: half turn, chart w
    for sgn in (1,-1):
        for coord in range(4):
            q = [F(v) for v in REC[1]]
            q[coord] += sgn*eps*F(max(abs(v) for v in REC[1]))
            cfg = [REC[0], intq(q), REC[2], REC[3]]
            c, pl = run(cfg, wide=True)
            tag = "1.%s%s" % ("wxyz"[coord], "+-"[sgn<0])
            line.append("%s=%s" % (tag, c))
            if c == base_cnt: surv.append((tag, pl==base_pl))
    print("eps=1/%d" % eps_den, " ".join(line))
    print("   survivors:", surv)
