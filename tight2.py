#!/usr/bin/env python3
"""Tight-set tangent spaces, controls done properly.

The chart is q_i -> q_i*(1,u): a right multiplication, valid even where the
Cayley chart is not (the n=4 183 has a half-turn cube).  Converting a Cayley
direction d at Cayley point c into this chart needs the PROJECTIVE freedom --
qmul(q,(0,u)) = (0,d) + lambda*q -- because q*(1,tu) does not keep w = 1.
Dropping lambda is what made the earlier control readings look like failures.
"""
import os
import json, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from tight_set import quantities
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

ENG = HERE + "/cube_regions_n"
ENGW = HERE + "/cube_regions_q2w"

def qmul(p, q):
    w,x,y,z = p; e,f,g,h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g,
            w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)

def rot(q):
    w,x,y,z = q; n = w*w+x*x+y*y+z*z
    return np.array([[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
                     [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                     [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]])/n

def redq(q):
    L = 1
    for v in q: L = L*v.denominator//gcd(L, v.denominator)
    iq = [int(v*L) for v in q]
    g = 0
    for v in iq: g = gcd(g, abs(v))
    return tuple(v//g for v in iq)

def count(cfg):
    s = ";".join(",".join(str(v) for v in q) for q in cfg)
    m = max(abs(v) for q in cfg for v in q)
    cmd = [ENG, "--quats", s] if m <= 512 else [ENGW, "--d", "0", "--quats", s]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0: return None
    try: return json.loads(p.stdout)["bounded"]
    except Exception: return None

def chart_dir(q, d):
    """Cayley-chart direction d at integer quaternion q -> right-mult chart u."""
    q = np.array([float(v) for v in q]); w = q[0]
    dq = np.array([0.0, d[0], d[1], d[2]])*w   # Cayley c = (x,y,z)/w
    A = np.zeros((4, 4))
    for k in range(3):
        u = [0.0]*3; u[k] = 1.0
        A[:, k] = qmul(tuple(q), (0.0, u[0], u[1], u[2]))
    A[:, 3] = -q
    sol, res, *_ = np.linalg.lstsq(A, dq, rcond=None)
    return list(sol[:3]), float(np.linalg.norm(A@sol - dq))

def null_of(qs):
    qsf = [tuple(float(v) for v in q) for q in qs]
    npar = 3*(len(qs)-1)
    def build(p):
        o = [qsf[0]]
        for i in range(1, len(qsf)):
            dd = p[3*(i-1):3*i]
            o.append(qmul(qsf[i], (1.0, dd[0], dd[1], dd[2])))
        return [rot(q) for q in o]
    q0 = quantities(build(np.zeros(npar)))
    tight = [i for i, v in enumerate(q0) if abs(v-1.0) < 1e-9]
    J = np.zeros((len(tight), npar)); h = 1e-7
    for k in range(npar):
        e = np.zeros(npar); e[k] = h
        J[:, k] = (quantities(build(e))[tight]-quantities(build(-e))[tight])/(2*h)
    U, S, Vt = np.linalg.svd(J)
    tol = 1e-6*max(S[0], 1e-30)
    null = np.array([Vt[i] for i in range(npar) if i >= len(S) or S[i] <= tol])
    return len(q0), len(tight), int((S > tol).sum()), null, npar

def walk(qs, u, epss=(F(1,16), F(1,64), F(1,256), F(1,1024))):
    """u a list of 3(n-1) Fractions; returns list of (eps, count)"""
    out = []
    for e in epss:
        for sgn in (1, -1):
            cfg = [tuple(F(v) for v in qs[0])]
            for i in range(1, len(qs)):
                uu = [F(u[3*(i-1)+j])*e*sgn for j in range(3)]
                cfg.append(qmul(tuple(F(v) for v in qs[i]), (F(1), uu[0], uu[1], uu[2])))
            out.append((('+' if sgn > 0 else '-')+str(e), count([redq(c) for c in cfg])))
    return out

def report(qs, label, known=()):
    """known: list of (name, cayley-direction on the LAST cube) or full charts"""
    base = count(list(qs))
    nq, nt, rank, null, npar = null_of(qs)
    print('%-22s count=%-5s %4d quantities %4d tight  rank %2d/%-2d  NULL DIM %d'
          % (label, base, nq, nt, rank, npar, len(null)))
    for name, ci, d in known:
        u, resid = chart_dir(qs[ci], d)
        full = np.zeros(npar); full[3*(ci-1):3*ci] = u
        fr = [F(x).limit_denominator(10**6) for x in full]
        w = walk(qs, fr)
        holds = all(c == base for _, c in w)
        cos = 0.0
        if len(null):
            e = full/np.linalg.norm(full)
            cos = float(np.linalg.norm(null.T @ (null @ e)))
        print('   known %-14s engine: %s   in null space: %.4f'
              % (name, 'HOLDS' if holds else 'FAILS '+str(w), cos))
    return base, null, npar

I = (1,0,0,0)
BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

if __name__ == '__main__':
    print('=== CONTROLS: the five configurations with verified tangents ===')
    report([I, (1,-12,-11,0)], 'n=2 mirror 13', [('(1,1,0)', 1, [1,1,0])])
    report([I, (10,3,3,3)], 'n=2 diagonal 13', [('(1,1,1)', 1, [1,1,1])])
    report(BASE+[(10,9,9,9)], 'n=6 723', [('(1,1,1)', 5, [1,1,1])])
    report(BASE+[(6,113,-135,-231)], 'n=6 727 arc A', [('(1,-3,-6)', 5, [1,-3,-6])])
    report(BASE+[(7,14,1,-5)], 'n=6 727 record',
           [('D1 (-1,-1/7,3/14)', 5, [-1, -1/7, 3/14]),
            ('D2 (-1,-4/21,2/7)', 5, [-1, -4/21, 2/7])])
    print()
    print('=== the maximisers ===')
    r2 = 2**.5; r5 = 5**.5
    report([I, (1,1,r2,0), (-1,1,r2,0)], 'n=3 67 octahedral')
    report([I, (2,1+r5,-1+r5,0), (-2,1+r5,-1+r5,0)], 'n=3 67 golden')
    report([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
    report(BASE, 'n=5 393')
    report(BASE+[(7,14,1,-5),(4,-3,-4,-4)], 'n=7 1217')
    report(BASE+[(7,14,1,-5),(4,-3,-4,-4),(3,-3,3,-8)], 'n=8 1891')
