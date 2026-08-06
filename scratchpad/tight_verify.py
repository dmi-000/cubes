#!/usr/bin/env python3
"""Candidate tangents from the tight Step-A set, VERIFIED by walking them.

The tight-set null space is a candidate only: Step A's pair conditions are
necessary for the count but at n>=4 they are not the whole story, so the null
space CONTAINS the true tangent space and can be strictly larger.  Every
direction reported here is therefore walked with the exact engine at several
scales; only those that hold the count are counted.

Rational directions are used where the null space is visibly rational, so the
walk is exact, not a float round-trip.
"""
import json, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, "/Users/dmi/cube-compounds")
import numpy as np
from tight_set import quantities

ENG = "/Users/dmi/cube-compounds/cube_regions_n"
ENGW = "/Users/dmi/cube-compounds/cube_regions_q2w"

def qmulf(p, q):
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
    if p.returncode != 0: return None, None
    try: o = json.loads(p.stdout)
    except Exception: return None, None
    pl = o["per_label"]
    return o["bounded"], tuple(pl.get(str(k), 0) for k in range(2**len(cfg)))

def step(qs, d, eps):
    """qs integer quats, d list of 3(n-1) Fractions, eps Fraction"""
    out = [tuple(F(v) for v in qs[0])]
    for i in range(1, len(qs)):
        u = [F(d[3*(i-1)+j])*eps for j in range(3)]
        out.append(qmulf(tuple(F(v) for v in qs[i]), (F(1), u[0], u[1], u[2])))
    return [redq(q) for q in out]

def nullspace(qs, label):
    qsf = [tuple(float(v) for v in q) for q in qs]
    npar = 3*(len(qs)-1)
    def build(p):
        o = [qsf[0]]
        for i in range(1, len(qsf)):
            dd = p[3*(i-1):3*i]
            o.append(qmulf(qsf[i], (1.0, dd[0], dd[1], dd[2])))
        return [rot(q) for q in o]
    q0 = quantities(build(np.zeros(npar)))
    tight = [i for i, v in enumerate(q0) if abs(v-1.0) < 1e-9]
    J = np.zeros((len(tight), npar)); h = 1e-7
    for k in range(npar):
        e = np.zeros(npar); e[k] = h
        J[:, k] = (quantities(build(e))[tight]-quantities(build(-e))[tight])/(2*h)
    U, S, Vt = np.linalg.svd(J)
    tol = 1e-6*max(S[0], 1e-30)
    null = [Vt[i] for i in range(npar) if i >= len(S) or S[i] <= tol]
    return len(tight), int((S > tol).sum()), null, npar

def rationalise(v, maxden=64):
    v = v/np.max(np.abs(v))
    fr = [F(float(x)).limit_denominator(maxden) for x in v]
    L = 1
    for f in fr: L = L*f.denominator//gcd(L, f.denominator)
    iv = [int(f*L) for f in fr]
    g = 0
    for x in iv: g = gcd(g, abs(x))
    if g: iv = [x//g for x in iv]
    err = max(abs(float(iv[i])/max(abs(np.array(iv)))*np.max(np.abs(v)) - v[i])
              for i in range(len(v)))
    return iv, err

def verify(qs, label, epss=(F(1,16), F(1,64), F(1,256), F(1,1024))):
    base, bpl = count(list(qs))
    nt, rank, null, npar = nullspace(qs, label)
    print('%s  count=%s  %d tight, rank %d of %d, null dim %d'
          % (label, base, nt, rank, npar, len(null)))
    good = []
    for idx, v in enumerate(null):
        iv, err = rationalise(np.array(v))
        res = []
        ok = True
        for e in epss:
            for sgn in (1, -1):
                cfg = step(qs, [F(x) for x in iv], sgn*e)
                c, pl = count(cfg)
                res.append('%s%s:%s' % ('+-'[sgn < 0], e, c))
                if c != base: ok = False
        print('   dir%d %s  rational-err %.2e' % (idx, iv, err))
        print('        %s   %s' % (' '.join(res), 'HOLDS' if ok else 'fails'))
        if ok: good.append(iv)
    print('   VERIFIED tangent dimension >= %d (of %d candidates)' % (len(good), len(null)))
    return good

I = (1,0,0,0)
BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('all', 'ctl'):
        print('=== CONTROLS ===')
        verify([I, (1,-12,-11,0)], 'n=2 mirror 13   ')
        verify([I, (10,3,3,3)], 'n=2 diagonal 13 ')
        verify(BASE+[(10,9,9,9)], 'n=6 723         ')
        verify(BASE+[(6,113,-135,-231)], 'n=6 727 arcA mid')
        verify(BASE+[(7,14,1,-5)], 'n=6 727 record  ')
    if which in ('all', 'max'):
        print()
        print('=== maximisers ===')
        verify([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183         ')
        verify(BASE, 'n=5 393         ')
        verify(BASE+[(7,14,1,-5),(4,-3,-4,-4)], 'n=7 1217        ')
        verify(BASE+[(7,14,1,-5),(4,-3,-4,-4),(3,-3,3,-8)], 'n=8 1891        ')
