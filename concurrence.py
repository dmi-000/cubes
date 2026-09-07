#!/usr/bin/env python3
"""Plane-concurrence multiplicity: how many face planes meet at one point?

ALGEBRAIC_SEARCH.md's premise is that record configurations sit at HIGH-MULTIPLICITY POINT
incidences -- 723 has two 9-fold concurrences (nine face planes through one point) where
random configurations top out at 4 -- and that those 9-fold points are cubes sharing a
CORNER, i.e. sharing the axis through that corner.

Today's search found its best single-axis family on (3,0,-2), which is not a corner axis of
the cube, so those cubes share an axis without sharing a corner. If that configuration also
shows high concurrence, the premise holds and shared-axis is the right generalisation. If it
does NOT, the count can be bought without point incidence and the premise is too narrow.

Exact throughout: planes have integer coefficients, and concurrence is tested by solving
integer 3x3 systems and comparing exact rationals, never by proximity.
"""
import itertools, json, subprocess, sys
from fractions import Fraction as F
from collections import Counter

def planes(cfg):
    """the 6 face planes of each cube: COLUMNS of the rotation matrix, offset +-(w^2+|v|^2)"""
    out = []
    for (w, x, y, z) in cfg:
        n = w * w + x * x + y * y + z * z
        M = [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
             [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
             [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]
        # COLUMNS, not rows. A cube's face normals in WORLD coordinates are the columns
        # of its rotation matrix; the rows are the world axes in the cube's frame, i.e.
        # the INVERSE rotation. Using rows made every incidence statistic a property of
        # the quaternion SPELLING rather than of the compound: replacing a cube by an
        # octahedrally equivalent quaternion -- the same cube -- changed the signature in
        # 6 of 6 tries. With columns it changes in 0 of 6, and no normalisation is needed:
        # a global rotation moves the incidence points but preserves their multiplicities,
        # per-cube symmetry permutes the plane set without changing it, and cube order
        # never enters a histogram. See invariance_gate().
        for c in range(3):
            v = (M[0][c], M[1][c], M[2][c])
            for s in (1, -1):
                out.append((v[0], v[1], v[2], s * n))
    return out

def solve3(p, q, r):
    A = [list(p[:3]), list(q[:3]), list(r[:3])]; b = [p[3], q[3], r[3]]
    det = (A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])
         - A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])
         + A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))
    if det == 0:
        return None
    def rep(i):
        B = [row[:] for row in A]
        for k in range(3):
            B[k][i] = b[k]
        return (B[0][0]*(B[1][1]*B[2][2]-B[1][2]*B[2][1])
              - B[0][1]*(B[1][0]*B[2][2]-B[1][2]*B[2][0])
              + B[0][2]*(B[1][0]*B[2][1]-B[1][1]*B[2][0]))
    return (F(rep(0), det), F(rep(1), det), F(rep(2), det))

def multiplicity(cfg):
    P = planes(cfg)
    pts = Counter()
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is not None:
            pts[s] += 1
    # a point lying on m planes is produced by C(m,3) triples
    best = 0
    for s, c in pts.items():
        m = 3
        while m * (m - 1) * (m - 2) // 6 < c:
            m += 1
        best = max(best, m)
    return best, len(pts)

if __name__ == '__main__':
    CASES = {
        'Haar-random (typical)': [(1,0,0,0),(7,3,-2,5),(4,-5,3,1),(2,7,-3,4)],
        'our old plateau 141':   None,
        'shared axis (1,1,0) 161': [(1,0,0,0),(1,-8,-8,0),(6,-5,-5,0),(5,-4,-4,0)],
        'n=4 record 183':        [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)],
    }
    for name, cfg in CASES.items():
        if cfg is None:
            continue
        st = ';'.join(','.join(map(str, q)) for q in cfg)
        d = json.loads(subprocess.run(['./cube_regions_n','--quats',st],
                                      capture_output=True, text=True).stdout)
        m, npts = multiplicity(cfg)
        print('%-26s total %4d  depth-1 %3d   MAX plane-concurrence %d  (%d distinct points)'
              % (name, d['bounded'], int(d['by_depth'].get('1',0)), m, npts), flush=True)


def invariance_gate(trials=6, verbose=True):
    """A signature MUST NOT change when a cube is respelled. Run before trusting any
    incidence statistic; it is the check whose absence invalidated a two-day census."""
    import itertools, random
    from math import gcd
    def canon(t):
        g = 0
        for v in t: g = gcd(g, abs(int(v)))
        t = tuple(int(v) // (g or 1) for v in t)
        for v in t:
            if v > 0: break
            if v < 0: t = tuple(-x for x in t); break
        return t
    def qmul(p, r):
        w,x,y,z = p; e,f,g_,h = r
        return canon((w*e-x*f-y*g_-z*h, w*f+x*e+y*h-z*g_,
                      w*g_-x*h+y*e+z*f, w*h+x*g_-y*f+z*e))
    OCT = sorted({canon(t) for t in itertools.product((-1,0,1), repeat=4)
                  if any(t) and sum(v*v for v in t) in (1,2,4)})
    rng = random.Random(0)
    bad = 0; total = 0
    for _ in range(trials):
        cfg = [canon(tuple(rng.randint(-6,6) for _ in range(4))) for _ in range(4)]
        if any(q == (0,0,0,0) for q in cfg): continue
        base = multiplicity(cfg)
        for k in range(len(cfg)):
            for s in rng.sample(OCT, 4):
                alt = list(cfg); alt[k] = qmul(cfg[k], s)
                total += 1
                if multiplicity(alt) != base: bad += 1
    if verbose:
        print('invariance gate: %d of %d respellings changed the signature%s'
              % (bad, total, '' if bad == 0 else '   <-- BROKEN'))
    return bad == 0


if __name__ == '__main__':
    invariance_gate()
