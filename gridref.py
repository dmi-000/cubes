#!/usr/bin/env python3
"""Reference (independent) counts of a, b, s, m by exact integer sphere sampling.

`cells.py` computes these by Fourier-Motzkin on cones; this computes them by BFS
on the integer grid {u : ||u||_inf = R} -- the sphere as the surface of a cube --
with membership decided by exact integer comparisons of max_N |n.u| after clearing
denominators.  No solver, no floats, and no shared code with cells.py, so the two
are genuinely independent.

It exists because `cells.py`'s m was wrong twice ([Postscript 110](LEDGER.md#p110)): once by
under-counting (non-strict conditions fed to a strict solver) and, after that fix,
by over-counting (adjacent sector pieces glued only on interior overlap).  a, b
and s agreed with this reference in every case tested; m did not.

NOT A REFERENCE -- A BIASED CROSS-CHECK.  Proposed as the trustworthy oracle and
demoted within the hour: a lattice grid BRIDGES THIN SEPARATIONS.  Where the true
set has several components divided by narrow walls, neighbouring grid points
straddle the wall and BFS merges them, so this UNDER-counts.  Measured: on a
13-pair it returns a = 1 where the truth is 6 (13 = 1 + 6 + 6, and
`step_a3.components` agrees), and it misses s in the same cases.  It also cannot
see components joined by a measure-zero sliver, so it under-counts from both ends.

What it is good for, and what it actually did: flagging WHICH quantity is wrong
when an exact method disagrees with a theorem.  It isolated m as faulty while
a, b, s matched, on a configuration where its bias did not bite -- and that
diagnosis held up ([Postscript 110](LEDGER.md#p110)).  Use it to localise a bug, never to settle a
count.

    python3 gridref.py            # gate: cubes, against innermost.py
"""
import sys
from math import gcd

import numpy as np
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

sys.path.insert(0, HERE)


def counts_grid(Ni, Nj, Nk, R=110):
    D = 1
    for N in (Ni, Nj, Nk):
        for n in N:
            for c in n:
                D = D * c.denominator // gcd(D, c.denominator)
    A = [np.array([[int(c * D) for c in n] for n in N], dtype=np.int64)
         for N in (Ni, Nj, Nk)]
    rr = range(-R, R + 1)
    pts = [(x, y, z) for x in rr for y in rr for z in rr
           if max(abs(x), abs(y), abs(z)) == R]
    P = np.array(pts, dtype=np.int64)
    f = [np.max(np.abs(P @ Ax.T), axis=1) for Ax in A]
    K, L = f[1] > f[0], f[2] > f[0]
    sets = {'a': K, 'b': L, 's': K & L, 'm': (~K) & (~L)}
    idx = {p: i for i, p in enumerate(pts)}
    steps = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))

    def comps(mask):
        seen = np.zeros(len(P), bool)
        n = 0
        for st in range(len(P)):
            if not mask[st] or seen[st]:
                continue
            n += 1
            stk = [st]
            seen[st] = True
            while stk:
                u = stk.pop()
                x, y, z = pts[u]
                for d in steps:
                    v = idx.get((x + d[0], y + d[1], z + d[2]))
                    if v is not None and mask[v] and not seen[v]:
                        seen[v] = True
                        stk.append(v)
        return n
    return tuple(comps(sets[k]) for k in ('a', 'b', 's', 'm'))


if __name__ == '__main__':
    from cells import cube_normals, counts
    from innermost import comp_innermost
    from step_a2 import normals
    cases = [((-2, -2, -2, -3), (3, -4, 4, 3)), ((1, 2, 1, 1), (-2, 1, 0, -1)),
             ((2, 1, 1, 1), (2, -1, -2, 0)), ((-1, 0, 2, 2), (-2, 1, -2, 0))]
    print('%-26s %-22s %-22s %s' % ('quats', 'grid (a,b,s,m)', 'cells.py', 'innermost m'))
    ok = True
    for qa, qb in cases:
        g = counts_grid(cube_normals(), cube_normals(qa), cube_normals(qb))
        c = counts(cube_normals(), cube_normals(qa), cube_normals(qb))
        im = comp_innermost(normals(qa), normals(qb))
        ok &= (g == c and g[3] == im)
        print('%-26s %-22s %-22s %-3d %s' % ('%s %s' % (qa, qb), str(g), str(c), im,
                                             'ok' if (g == c and g[3] == im) else 'MISMATCH'))
    print('GATE %s' % ('PASS' if ok else 'FAIL'))
