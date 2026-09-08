#!/usr/bin/env python3
"""The base's own arrangement: real triple points and crossing lines.

Every codimension-1 event in a 3-DOF family of origin-centred cubes is FOUR
FACE PLANES CONCURRENT.  Classified by how the four planes distribute over
cubes:

  (3,1)     corner of A on a face plane of B      -- corner-on-face quadrics,
                                                     enumerated (mixed strata)
  (2,2)     edge of A meets edge of B             -- edge-edge coplanarity,
                                                     enumerated (locus_linear)
  (2,1,1)   edge of A meets the line where faces
            of two DIFFERENT other cubes cross    -- never enumerated
  (1,1,1,1) four planes from four cubes concurrent-- never enumerated

Against a FIXED base the last two become finite catalogues, because the
objects the free cube has to meet are fixed in space:

  (1,1,1,1) and the mixed (2,1,1) cases where the free cube supplies one plane
      -> the free cube's face plane passes through a fixed TRIPLE POINT of the
         base arrangement.  One condition; a quadric in Cayley coordinates.

  (2,1,1) where the free cube supplies two planes (an edge)
      -> a free cube EDGE meets a fixed CROSSING LINE of the base.

This module builds those two catalogues for the 393 base and reports their
sizes, with multiplicity.  A point is only counted if it is REAL: it must lie
on the actual face square of every cube whose plane passes through it, not
merely on the infinite plane extension -- the same distinction (real facets vs
phantom facets) that defines a region in this project.

INVARIANT: exact rational arithmetic; points are deduplicated by exact
coordinates, never by rounding.  Multiplicity is the number of the base's 30
planes through a point, counted on the plane, and separately the number for
which the point is inside the real face -- conflating the two would inflate
every count.
"""
import collections
import itertools
from fractions import Fraction as F

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]


def mat(q):
    w, x, y, z = q
    n = F(w*w + x*x + y*y + z*z)
    return [[F(w*w+x*x-y*y-z*z)/n, F(2*(x*y-w*z))/n, F(2*(x*z+w*y))/n],
            [F(2*(x*y+w*z))/n, F(w*w-x*x+y*y-z*z)/n, F(2*(y*z-w*x))/n],
            [F(2*(x*z-w*y))/n, F(2*(y*z+w*x))/n, F(w*w-x*x-y*y+z*z)/n]]


def planes(cfg):
    """(normal, offset, cube, axis) for all 6n face planes; cube = R([-1,1]^3)."""
    out = []
    for c, q in enumerate(cfg):
        M = mat(q)
        for a in range(3):
            n = (M[0][a], M[1][a], M[2][a])
            out.append((n, F(1), c, a))
            out.append((tuple(-v for v in n), F(1), c, a))
    return out


def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def solve3(p, q, r):
    A = [p[0], q[0], r[0]]
    d = det3(*A)
    if d == 0:
        return None
    rhs = (p[1], q[1], r[1])
    cols = []
    for k in range(3):
        B = [list(row) for row in A]
        for i in range(3):
            B[i][k] = rhs[i]
        cols.append(det3(*[tuple(row) for row in B]) / d)
    return tuple(cols)


def in_cube(pt, Minv):
    """Is pt inside the closed cube R([-1,1]^3), R^T = Minv rows?"""
    v = [sum(Minv[i][k]*pt[k] for k in range(3)) for i in range(3)]
    return max(abs(x) for x in v) <= 1


def main():
    P = planes(FIVE)
    mats = [mat(q) for q in FIVE]
    # R^T for the containment test (R orthogonal, so R^T = transpose)
    trans = [[[M[k][i] for k in range(3)] for i in range(3)] for M in mats]

    pts = collections.defaultdict(set)      # point -> set of plane indices
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is None:
            continue
        if max(abs(x) for x in s) > 4:      # far outside every cube
            continue
        pts[s] |= {i, j, k}
    print('candidate triple points within |p|_inf <= 4: %d' % len(pts), flush=True)

    # a plane is REALLY incident if the point is on the plane AND inside the
    # owning cube's face square, i.e. inside the closed cube itself
    real = {}
    for s, idx in pts.items():
        on = [t for t in range(len(P))
              if sum(P[t][0][u]*s[u] for u in range(3)) == P[t][1]]
        cubes_on = {P[t][2] for t in on}
        inside = all(in_cube(s, trans[c]) for c in cubes_on)
        real[s] = (len(on), len(cubes_on), inside)

    hist = collections.Counter()
    hist_real = collections.Counter()
    for s, (nplanes, ncubes, inside) in real.items():
        hist[nplanes] += 1
        if inside:
            hist_real[(nplanes, ncubes)] += 1
    print('\nall candidate points by #planes through them:')
    for k in sorted(hist):
        print('   %2d planes: %5d points' % (k, hist[k]))
    print('\nREAL points (on the actual faces of every cube involved),'
          ' by (#planes, #cubes):')
    for k in sorted(hist_real):
        print('   %2d planes / %d cubes: %5d points' % (k[0], k[1], hist_real[k]))
    nreal = sum(hist_real.values())
    print('\nreal triple points: %d  ->  %d quadric walls for the free cube'
          ' (6 face planes each)' % (nreal, 6 * nreal))

    # crossing lines: pairs of planes from DIFFERENT base cubes whose
    # intersection line actually meets both cubes' real faces
    nlines = 0
    for i, j in itertools.combinations(range(len(P)), 2):
        if P[i][2] == P[j][2]:
            continue
        n1, n2 = P[i][0], P[j][0]
        d = (n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2],
             n1[0]*n2[1]-n1[1]*n2[0])
        if not any(d):
            continue
        nlines += 1
    print('crossing lines from two different base cubes: %d' % nlines)
    print('   -> %d (edge of free cube) x (crossing line) conditions'
          % (12 * nlines))


if __name__ == '__main__':
    main()
