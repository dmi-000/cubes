#!/usr/bin/env python3
"""WHICH tight conditions does the n=6 record's tangent violate, and why?

At the record, D1 and D2 both hold 727 exactly, yet each violates 6 of the 204
tight Step-A gradients -- which is the whole reason the only multi-cube method
returns null dimension 1 where the truth is at least 2.  Six of 204 is small
enough to identify by name.  `tight_set.quantities` emits, per ordered pair
(i,j), six single-slab l1 norms then twelve slab-pair minima, so an index
decodes to exactly which condition it is.
"""
import os
import itertools, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tight_set import quantities
from tight2 import qmul, rot, chart_dir, BASE, I

FACE = ['+x','-x','+y','-y','+z','-z']
COMBOS = [(a,b) for a,b in itertools.combinations(range(6),2) if a^1 != b]

def decode(idx, n):
    per = 18
    pairs = list(itertools.permutations(range(n), 2))
    p, r = idx//per, idx % per
    i, j = pairs[p]
    if r < 6:
        return (i, j, 'slab %s' % FACE[r])
    a, b = COMBOS[r-6]
    return (i, j, 'pair %s|%s' % (FACE[a], FACE[b]))

def build(qs, p):
    o = [qs[0]]
    for i in range(1, len(qs)):
        d = p[3*(i-1):3*i]
        o.append(qmul(qs[i], (1.0, d[0], d[1], d[2])))
    return [rot(q) for q in o]

def analyse(qs, label, dirs):
    qs = [tuple(float(v) for v in q) for q in qs]
    n = len(qs); npar = 3*(n-1)
    q0 = quantities(build(qs, np.zeros(npar)))
    tight = [i for i, v in enumerate(q0) if abs(v-1.0) < 1e-9]
    J = np.zeros((len(tight), npar)); h = 1e-7
    for k in range(npar):
        e = np.zeros(npar); e[k] = h
        J[:, k] = (quantities(build(qs, e))[tight]-quantities(build(qs, -e))[tight])/(2*h)
    print('%s: %d tight of %d' % (label, len(tight), len(q0)))
    bad = set()
    for name, ci, d in dirs:
        u, _ = chart_dir(qs[ci], d)
        v = np.zeros(npar); v[3*(ci-1):3*ci] = u; v /= np.linalg.norm(v)
        g = J @ v
        tol = 1e-6*max(1.0, np.abs(J).max())
        idx = [k for k in range(len(g)) if abs(g[k]) > tol]
        print('  %s violates %d:' % (name, len(idx)))
        for k in idx:
            i, j, what = decode(tight[k], n)
            print('      cubes (%d,%d)  %-14s  dq = %+.4f' % (i, j, what, g[k]))
            bad.add(tight[k])
    return tight, J, bad, npar

REC = BASE+[(7,14,1,-5)]
D1 = ('D1', 5, [-1, -1/7, 3/14]); D2 = ('D2', 5, [-1, -4/21, 2/7])
tight, J, bad, npar = analyse(REC, 'n=6 727 RECORD', [D1, D2])

print()
print('=== does dropping exactly those conditions recover the tangents? ===')
keep = [k for k, t in enumerate(tight) if t not in bad]
U, S, Vt = np.linalg.svd(J[keep])
tol = 1e-6*max(S[0], 1e-30)
null = np.array([Vt[i] for i in range(npar) if i >= len(S) or S[i] <= tol])
print('dropped %d rows; rank %d of %d -> null dim %d' % (len(bad), int((S > tol).sum()), npar, len(null)))
for name, ci, d in (D1, D2):
    u, _ = chart_dir([float(v) for v in REC[ci]], d)
    v = np.zeros(npar); v[3*(ci-1):3*ci] = u; v /= np.linalg.norm(v)
    print('  %s now projects %.4f into the null space' % (name, np.linalg.norm(null.T @ (null @ v))))
