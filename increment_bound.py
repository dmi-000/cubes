#!/usr/bin/env python3
"""An Euler-derived bound on the one-cube increment — E1 without the calibration.

E1 (Postscript 18) is T <= S_max + 336 at n=6, where 336 was MEASURED as the
largest increment seen.  The increment identity itself is exact:

    T = count(S_j) + Delta_j          for every cube j,

where S_j is the compound with cube j removed.  This module bounds Delta_j
from geometry instead of from a corpus.

THE ARGUMENT.  Every region created by re-adding cube j arises because the
surface dC_j cuts an existing region of S_j, and each connected PIECE of dC_j
splits at most one region into at most one extra part.  So

    Delta_j <= #pieces of dC_j cut by the other cubes' face planes.

dC_j is topologically a sphere; each other face plane meets it in a closed
curve; crossings have degree 4, so E = 2V and Euler gives F = 2 + V.  Hence

    Delta_j <= 2 + V_j,
    V_j = # points where two other-cube face planes cross on dC_j
        = 2 * #{plane pairs whose intersection line meets the interior of C_j}.

V_j is exactly computable, so this replaces a calibrated constant with a
quantity derived per configuration.  Whether it is TIGHT is the open part; this
script measures the gap.

INVARIANT: exact rational arithmetic throughout.  The line/interior test is a
1-D exact minimisation of the sup-norm in cube j's own frame, not a sampled
approximation — a wrong verdict there would silently weaken or break the bound.
"""
import itertools
import json
import subprocess
import sys
from fractions import Fraction as F


def mat(q):
    w, x, y, z = q
    n = F(w*w + x*x + y*y + z*z)
    return [[F(w*w+x*x-y*y-z*z)/n, F(2*(x*y-w*z))/n, F(2*(x*z+w*y))/n],
            [F(2*(x*y+w*z))/n, F(w*w-x*x+y*y-z*z)/n, F(2*(y*z-w*x))/n],
            [F(2*(x*z-w*y))/n, F(2*(y*z+w*x))/n, F(w*w-x*x-y*y+z*z)/n]]


def col(M, j):
    return (M[0][j], M[1][j], M[2][j])


def planes_of(q):
    """The 6 face planes of the cube R([-1,1]^3): normal . x = offset."""
    M = mat(q)
    out = []
    for a in range(3):
        n = col(M, a)
        out.append((n, F(1)))
        out.append((tuple(-v for v in n), F(1)))
    return out


def line_meets_interior(p, q, Rj):
    """Does the line {P=0} ^ {Q=0} meet the interior of cube j?

    In cube j's own frame the cube is [-1,1]^3, so the test is
    min_t max_k |(Rj^T (p0 + t d))_k| < 1 — a 1-D minimisation of a max of
    absolute affine functions, solved exactly at the breakpoints."""
    (n1, c1), (n2, c2) = p, q
    d = (n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2], n1[0]*n2[1]-n1[1]*n2[0])
    if not any(d):
        return False
    # a point on the line: solve the 2x2 system in the two largest coords of d
    k = max(range(3), key=lambda i: abs(d[i]))
    i, j = [t for t in range(3) if t != k]
    det = n1[i]*n2[j] - n1[j]*n2[i]
    if det == 0:
        return False
    p0 = [F(0), F(0), F(0)]
    p0[i] = (c1*n2[j] - c2*n1[j]) / det
    p0[j] = (n1[i]*c2 - n2[i]*c1) / det
    # transform to cube j's frame: u(t) = Rj^T p0 + t Rj^T d
    A = [sum(Rj[r][c]*p0[r] for r in range(3)) for c in range(3)]
    B = [sum(Rj[r][c]*d[r] for r in range(3)) for c in range(3)]
    # breakpoints where some |A_k + t B_k| changes slope, plus their crossings
    ts = set()
    for c in range(3):
        if B[c] != 0:
            ts.add(-A[c]/B[c])
            ts.add((1 - A[c])/B[c])
            ts.add((-1 - A[c])/B[c])
    for a, b in itertools.combinations(range(3), 2):
        for s1 in (1, -1):
            for s2 in (1, -1):
                den = s1*B[a] - s2*B[b]
                if den != 0:
                    ts.add((s2*A[b] - s1*A[a]) / den)
    if not ts:
        return max(abs(x) for x in A) < 1
    return min(max(abs(A[c] + t*B[c]) for c in range(3)) for t in ts) < 1


def V_of(cfg, j):
    """Crossings on dC_j of the other cubes' face planes."""
    Rj = mat(cfg[j])
    others = [pl for k, q in enumerate(cfg) if k != j for pl in planes_of(q)]
    v = 0
    for p, q in itertools.combinations(others, 2):
        if line_meets_interior(p, q, Rj):
            v += 2
    return v


def count(cfg):
    s = ';'.join(','.join(map(str, q)) for q in cfg)
    out = subprocess.run(['./cube_regions_n', '--quats', s],
                         capture_output=True, text=True).stdout
    return json.loads(out)['bounded'] if out.startswith('{') else None


CONFIGS = {
    '727 record': [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5)],
    '723':        [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(5,2,2,2)],
    '393 (n=5)':  [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)],
    '183 (n=4)':  [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)],
}


def main():
    print('%-12s %3s %6s %6s %8s %8s %7s' %
          ('config', 'j', 'T', 'S_j', 'Delta_j', 'bound', 'slack'))
    worst = 0.0
    for name, cfg in CONFIGS.items():
        T = count(cfg)
        for j in range(len(cfg)):
            sub = [c for k, c in enumerate(cfg) if k != j]
            Sj = count(sub)
            delta = T - Sj
            bound = 2 + V_of(cfg, j)
            ok = 'OK' if delta <= bound else 'VIOLATED'
            ratio = bound / delta if delta else float('inf')
            worst = max(worst, ratio if delta else 0)
            print('%-12s %3d %6d %6d %8d %8d %6.2fx %s'
                  % (name, j, T, Sj, delta, bound, ratio, ok), flush=True)
    print('\nworst looseness: %.2fx' % worst)
    print('E1 uses a flat 336 at n=6; this bound is per-configuration and derived.')


if __name__ == '__main__':
    main()
