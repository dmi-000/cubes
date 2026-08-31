#!/usr/bin/env python3
"""The n=9 2785 upper end, solved — the last unsolved end of the k-family line.

In the parametrisation ninth cube = (1, 1, 55/56 + s, 1) the level set is ONE
interval punctured at s = 1/56, not [P178]'s "two rays k >= 56 and k <= -69":

    s = -4.029245e-6   W4 wall, 2783 AT it            lower end, solved
    s = 1/56           PUNCTURE, ninth cube = (1,1,1,1) = base cube 4, count 1895
    upper end          bracketed by 2785 at s=125/3864 and 2781 at s=31/952

The general walk in `solve_more_ends.py` cannot reach this end from s=0: it would
stop at the puncture, which is a DEGENERACY (a duplicated cube) and not a wall, and
report the last root before it as an end. So the bracket is supplied directly and
every W4 root inside it is evaluated exactly.
"""
import os, sys, json, subprocess
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catcache import catalogue
from n78_ends import w4_polys, squarefree, qstr, run
from solve_more_ends import exact_roots, val, approx, count_at, simplest_between

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C8 = BASE + [(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]
a0 = [F(1), F(55,56), F(1)]
dv = [F(0), F(1), F(0)]
LO, HI = F(125,3864), F(31,952)          # 2785 at LO, 2781 at HI (verified)

def q_of(s):
    c = [a0[i] + s*dv[i] for i in range(3)]
    L = 1
    for v in c: L = L*v.denominator//gcd(L, v.denominator)
    iq = [L] + [int(v*L) for v in c]; g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def cnt_rat(s):
    cfg = C8 + [q_of(s)]
    st = ";".join(",".join(map(str, q)) for q in cfg)
    m = max(abs(v) for q in cfg for v in q)
    cmd = (['./cube_regions_n','--quats',st] if m <= 512
           else ['./cube_regions_q2w','--d','0','--quats',st])
    try: return json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)['bounded']
    except Exception: return None

# gate: the bracket must actually bracket
assert cnt_rat(LO) == 2785 and cnt_rat(HI) == 2781, 'bracket does not bracket'
print('gate: 2785 at s=%s, 2781 at s=%s  OK' % (LO, HI), flush=True)

pts, _ = catalogue(C8)
roots = []
for p in w4_polys(a0, dv, pts):
    roots.extend(exact_roots(p))
inside = sorted({approx(r): r for r in roots if LO < approx(r) < HI}.values(), key=val)
print('%d W4 roots strictly inside the bracket' % len(inside), flush=True)

prev = LO
end = None
for r in inside:
    a = approx(r)
    c = cnt_rat(simplest_between(prev, a))
    if c is None:
        print('   UNEVALUATED probe — stopping, not scored as a change'); break
    if c != 2785:
        end = prevr if 'prevr' in dir() else None
        break
    prev, prevr = a, r
else:
    end = inside[-1] if inside else None

if end is None:
    print('no W4 root separates 2785 from 2781 in this bracket — the end is W3 (quartic)')
else:
    rp, rq, d = end
    c, mag = count_at(C8, a0, dv, end)
    print('   UPPER END s = (%s) + (%s)sqrt(%d) = %.12f   height %d   count AT end: %s'
          % (rp, rq, d, val(end), mag, c), flush=True)
