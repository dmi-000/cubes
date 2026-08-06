#!/usr/bin/env python3
"""Is the tangent set a CONE rather than a subspace?

A tight Step-A quantity sits exactly at 1: the slab (or slab pair) is degenerate,
so it bounds no open region.  Pushing it ABOVE 1 opens a region and the count
goes up; pushing it BELOW 1 leaves it empty and the count is unchanged.  So the
count-preserving directions are {v : J v <= 0}, a polyhedral CONE, and the null
space {v : J v = 0} is only its lin
eality space -- a LOWER bound on the tangent
directions, never an upper one.

Test: the n=6 record carries two verified tangents that the null space misses.
If the cone reading is right, J@D1 and J@D2 must be <= 0 componentwise.
"""
import sys
import numpy as np
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from tight2 import null_of, chart_dir, walk, count, BASE, I, qmul, rot
sys.path.insert(0, "/Users/dmi/cube-compounds")
from tight_set import quantities

def jac(qs):
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
    return J, tight

def probe(qs, label, dirs):
    J, tight = jac(qs)
    print('%s  %d tight' % (label, len(tight)))
    for name, ci, d in dirs:
        u, _ = chart_dir(qs[ci], d)
        v = np.zeros(J.shape[1]); v[3*(ci-1):3*ci] = u
        v = v/np.linalg.norm(v)
        g = J @ v
        tolg = 1e-6*max(1.0, np.abs(J).max())
        pos = int((g > tolg).sum()); neg = int((g < -tolg).sum())
        zer = len(g)-pos-neg
        print('   %-20s Jv:  %3d positive  %3d zero  %3d negative   max=%+.4f min=%+.4f'
              % (name, pos, zer, neg, g.max(), g.min()))

if __name__ == '__main__':
    print('=== the n=6 record: two verified tangents the null space misses ===')
    probe(BASE+[(7,14,1,-5)], 'n=6 727 record',
          [('D1 (-1,-1/7,3/14)', 5, [-1, -1/7, 3/14]),
           ('D2 (-1,-4/21,2/7)', 5, [-1, -4/21, 2/7]),
           ('random (1,0,0)', 5, [1, 0, 0]),
           ('random (0,1,0)', 5, [0, 1, 0])])
    print()
    print('=== controls where the null space DID contain the tangent ===')
    probe([I, (1,-12,-11,0)], 'n=2 mirror 13', [('(1,1,0)', 1, [1,1,0]),
                                                ('(1,0,0)', 1, [1,0,0])])
    probe(BASE+[(6,53,-87,-156)], 'n=6 727 arc A', [('(1,-3,-6)', 5, [1,-3,-6]),
                                                    ('(1,0,0)', 5, [1,0,0])])
