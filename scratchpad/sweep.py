#!/usr/bin/env python3
"""Generic line sweep: base cubes fixed, one free cube walks a Cayley line.

count + per-label profile at each sample; report runs of constant count and
runs of constant type (chambers).
"""
import json
import subprocess
import sys
from fractions import Fraction as F

ENG = "/Users/dmi/cube-compounds/cube_regions_n"
ENGW = "/Users/dmi/cube-compounds/cube_regions_q2w"


def quat_of(cayley):
    """(a,b,c) Fractions -> integer quaternion (w,x,y,z), gcd-reduced."""
    from math import gcd
    dens = [F(c).denominator for c in cayley]
    L = 1
    for d in dens:
        L = L * d // gcd(L, d)
    w = L
    xs = [int(F(c) * L) for c in cayley]
    g = w
    for v in xs:
        g = gcd(g, abs(v))
    return (w // g, xs[0] // g, xs[1] // g, xs[2] // g)


def run(quats, wide=False, d=0):
    s = ";".join(",".join(str(v) for v in q) for q in quats)
    eng = ENGW if wide else ENG
    cmd = [eng, "--quats", s]
    if wide:
        cmd = [eng, "--d", str(d), "--quats", s]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return None, None
    try:
        o = json.loads(p.stdout)
    except Exception:
        return None, None
    pl = tuple(o["per_label"][str(k)] for k in range(2 ** len(quats)))
    return o["bounded"], pl


def sweep(base, p0, dirv, svals, wide=False):
    """base: list of integer quats. p0,dirv: 3-tuples of Fractions."""
    out = []
    for s in svals:
        c = tuple(F(p0[i]) + F(s) * F(dirv[i]) for i in range(3))
        q = quat_of(c)
        m = max(abs(v) for v in q)
        w = wide or m > 512
        cnt, pl = run(base + [q], wide=w)
        out.append((s, q, cnt, pl))
    return out


def runs(rows, key):
    """collapse consecutive equal key values"""
    res = []
    for r in rows:
        k = key(r)
        if res and res[-1][0] == k:
            res[-1][2] = r[0]
            res[-1][3] += 1
        else:
            res.append([k, r[0], r[0], 1])
    return res
