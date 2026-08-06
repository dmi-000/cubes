#!/usr/bin/env python3
"""tight_set.py's method, re-parametrised in QUATERNIONS so it works at n=4.

Each free cube i is perturbed as q_i * (1, d1, d2, d3) -- a right multiplication
by a small rotation, which is a chart valid everywhere, unlike Cayley
coordinates (the n=4 183 has a half-turn cube, Cayley-infinite).

A ZERO reading is only believable if the controls reproduce their known
tangents, so every configuration with a verified tangent runs first.
"""
import sys
sys.path.insert(0, "/Users/dmi/cube-compounds")
import numpy as np
from tight_set import quantities

def qmul(p, q):
    w,x,y,z = p; e,f,g,h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g,
            w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)

def rot(q):
    w,x,y,z = q
    n = w*w+x*x+y*y+z*z
    return np.array([[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
                     [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                     [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]])/n

def tangent(qs, label, expect=None, verbose=True):
    qs = [tuple(float(v) for v in q) for q in qs]
    npar = 3*(len(qs)-1)
    def build(p):
        out = [qs[0]]
        for i in range(1, len(qs)):
            d = p[3*(i-1):3*i]
            out.append(qmul(qs[i], (1.0, d[0], d[1], d[2])))
        return [rot(q) for q in out]
    q0 = quantities(build(np.zeros(npar)))
    tight = [i for i, v in enumerate(q0) if abs(v-1.0) < 1e-9]
    if not tight:
        print('%-26s %5d quantities, 0 TIGHT -> unconstrained' % (label, len(q0)))
        return None, None
    J = np.zeros((len(tight), npar)); h = 1e-7
    for k in range(npar):
        e = np.zeros(npar); e[k] = h
        J[:, k] = (quantities(build(e))[tight]-quantities(build(-e))[tight])/(2*h)
    U, S, Vt = np.linalg.svd(J)
    tol = 1e-6*max(S[0], 1e-30)
    rank = int((S > tol).sum())
    null = [Vt[i] for i in range(npar) if i >= len(S) or S[i] <= tol]
    print('%-26s %5d quantities, %4d TIGHT, rank %2d of %2d -> tangent dim %d'
          % (label, len(q0), len(tight), rank, npar, len(null)))
    if expect is not None:
        e = np.array(expect, float); e /= np.linalg.norm(e)
        if null:
            N = np.array(null)
            print('%-26s   CONTROL: known tangent recovered %.4f (1.0 = fully)'
                  % ('', float(np.linalg.norm(N.T @ (N @ e)))))
        else:
            print('%-26s   CONTROL FAILED: null space empty' % '')
    if verbose:
        for v in null[:4]:
            v = v/np.max(np.abs(v))
            print('%-26s   dir %s' % ('', np.array2string(
                v, precision=3, suppress_small=True, max_line_width=250)))
    return len(null), null

I = (1,0,0,0)
BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]

def cq(c):
    """Cayley point -> quaternion"""
    return (1.0, c[0], c[1], c[2])

# a Cayley-chart direction d at Cayley point c, expressed in the right-mult chart
def chart_dir(c, d):
    q = np.array(cq(c)); dq = np.array((0.0, d[0], d[1], d[2]))
    # q*(1,u) = q + q*(0,u)  =>  u solves qmul(q,(0,u)) = dq  (up to the w-part)
    A = np.zeros((4, 3))
    for k in range(3):
        u = [0.0]*3; u[k] = 1.0
        A[:, k] = qmul(tuple(q), (0.0, u[0], u[1], u[2]))
    sol, *_ = np.linalg.lstsq(A, dq, rcond=None)
    return list(sol)

print('=== CONTROLS: configurations with verified tangents ===')
tangent([I, cq([-12., -11., 0.])], 'n=2 mirror-plane 13',
        chart_dir([-12., -11., 0.], [1, 1, 0]))
tangent([I, cq([1., 1., 1.])], 'n=2 body-diagonal 13',
        chart_dir([1., 1., 1.], [1, 1, 1]))
c723 = [.9, .9, .9]
tangent(BASE+[cq(c723)], 'n=6 723 at s=1/2', [0]*12+chart_dir(c723, [1, 1, 1]))
a0 = np.array([19/3, -7., -11.]); dA = [1., -3., -6.]
cA = list(a0+2.5*np.array(dA))
tangent(BASE+[cq(cA)], 'n=6 727 arc A mid', [0]*12+chart_dir(cA, dA))
cR = [14/7, 1/7, -5/7]
tangent(BASE+[cq(cR)], 'n=6 727 record', [0]*12+chart_dir(cR, [-1, -1/7, 3/14]))

print()
print('=== the maximisers ===')
r2 = 2**.5
tangent([I, (1, 1, r2, 0), (-1, 1, r2, 0)], 'n=3 67 octahedral')
r5 = 5**.5
tangent([I, (2, 1+r5, -1+r5, 0), (-2, 1+r5, -1+r5, 0)], 'n=3 67 golden')
tangent([(1,0,0,0), (0,5,3,2), (1,-4,-1,1), (1,1,-1,-4)], 'n=4 183')
tangent(BASE, 'n=5 393')
tangent(BASE+[cq(c723)], 'n=6 723')
tangent(BASE+[cq(cR)], 'n=6 727 record')
tangent(BASE+[(7,14,1,-5)], 'n=7 1217 (base+c6)')
tangent(BASE+[(7,14,1,-5), (4,-3,-4,-4)], 'n=7 1217')
tangent(BASE+[(7,14,1,-5), (4,-3,-4,-4), (3,-3,3,-8)], 'n=8 1891')
