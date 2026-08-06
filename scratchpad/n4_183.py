#!/usr/bin/env python3
"""n=4, 183: aligned probe, then sweep each surviving direction for extent+types."""
import sys, json, subprocess
from fractions import Fraction as F
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from sweep import run, quat_of

REC = [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
# quaternion-space probe: perturb one component of one free quaternion.
# cube 1 has w=0 so Cayley is unusable; work in quaternion components directly,
# normalising by keeping the quaternion integral.

base_cnt, base_pl = run(list(REC))
print("base", base_cnt, base_pl)

EPS = F(1, 64)
surv = []
for ci in (1, 2, 3):
    for comp in range(4):
        for sgn in (1, -1):
            q = list(F(v) for v in REC[ci])
            q[comp] += sgn * EPS
            L = 1
            from math import gcd
            for v in q:
                L = L * v.denominator // gcd(L, v.denominator)
            iq = [int(v * L) for v in q]
            g = 0
            for v in iq: g = gcd(g, abs(v))
            iq = tuple(v // g for v in iq)
            cfg = [REC[0]] + [iq if k == ci else REC[k] for k in (1,2,3)]
            c, pl = run(cfg)
            tag = "%d.%s%s" % (ci, "wxyz"[comp], "+" if sgn > 0 else "-")
            if c == base_cnt:
                surv.append((ci, comp, sgn))
            print(tag, c, "SAME-TYPE" if pl == base_pl else "")
print("survivors:", surv)
