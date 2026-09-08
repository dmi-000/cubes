#!/usr/bin/env python3
"""Do the 727 configurations sit on the (2,1,1) and (1,1,1,1) walls?

base_points.py catalogues the two coincidence types no search in this project
has ever enumerated, as finite catalogues against the fixed 393 base:

  W4  the free cube's face plane passes through a REAL TRIPLE POINT of the
      base arrangement (424 points).  Equivalently the point lies on the free
      cube's boundary: |R^T p|_inf == 1.
  W3  an EDGE of the free cube meets a CROSSING LINE of two different base
      cubes (360 lines), the two lines being coplanar and crossing inside both
      real segments.

Before enumerating either stratum it is worth knowing whether the 727 plateau
already lives on it.  If the record configurations satisfy many W3/W4
conditions, those walls are where to search; if they satisfy none, the
strata are new territory but not obviously the productive kind.

Control: a generic rational configuration must score 0 on both.  Without that
the counts would be meaningless -- any predicate loose enough to fire
everywhere proves nothing.

INVARIANT: exact rational arithmetic, and every incidence is tested REAL --
on the actual face square or inside the actual segment, never on the infinite
plane or line extension.  The phantom/real distinction is what makes a
coincidence a wall of the region complex rather than a coincidence of
algebra.
"""
import collections
import itertools
import json
from fractions import Fraction as F

from base_points import FIVE, det3, mat, planes, solve3


def base_catalogue():
    P = planes(FIVE)
    mats = [mat(q) for q in FIVE]
    trans = [[[M[k][i] for k in range(3)] for i in range(3)] for M in mats]

    def in_cube(pt, Minv):
        v = [sum(Minv[i][k]*pt[k] for k in range(3)) for i in range(3)]
        return max(abs(x) for x in v) <= 1

    pts = collections.defaultdict(set)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is None or max(abs(x) for x in s) > 4:
            continue
        pts[s] |= {i, j, k}
    real_pts = []
    for s in pts:
        on = [t for t in range(len(P))
              if sum(P[t][0][u]*s[u] for u in range(3)) == P[t][1]]
        cubes_on = {P[t][2] for t in on}
        if all(in_cube(s, trans[c]) for c in cubes_on):
            real_pts.append((s, len(on), len(cubes_on)))

    # crossing lines of two DIFFERENT base cubes, as (point, direction),
    # kept only if the line actually meets both cubes' real faces
    lines = []
    for i, j in itertools.combinations(range(len(P)), 2):
        if P[i][2] == P[j][2]:
            continue
        n1, n2 = P[i][0], P[j][0]
        d = (n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2],
             n1[0]*n2[1]-n1[1]*n2[0])
        if not any(d):
            continue
        k = max(range(3), key=lambda u: abs(d[u]))
        u1, u2 = [t for t in range(3) if t != k]
        det = n1[u1]*n2[u2] - n1[u2]*n2[u1]
        if det == 0:
            continue
        p0 = [F(0)]*3
        p0[u1] = (P[i][1]*n2[u2] - P[j][1]*n1[u2]) / det
        p0[u2] = (n1[u1]*P[j][1] - n2[u1]*P[i][1]) / det
        lines.append((tuple(p0), d, P[i][2], P[j][2]))
    return real_pts, lines


def cube_edges(M):
    """The 12 edges of R([-1,1]^3) as (endpoint, direction) in world coords."""
    out = []
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        for sb in (1, -1):
            for sc in (1, -1):
                p = [F(0)]*3
                for i in range(3):
                    p[i] = M[i][b]*sb + M[i][c]*sc - M[i][a]
                d = tuple(2*M[i][a] for i in range(3))
                out.append((tuple(p), d))
    return out


def w4_count(q, pts):
    """Base triple points lying on the free cube's boundary (real faces)."""
    M = mat(q)
    T = [[M[k][i] for k in range(3)] for i in range(3)]   # R^T
    hits = []
    for s, npl, ncub in pts:
        v = [sum(T[i][k]*s[k] for k in range(3)) for i in range(3)]
        if max(abs(x) for x in v) == 1:
            hits.append((npl, ncub))
    return hits


def w3_count(q, lines):
    """Free-cube edges meeting a base crossing line, inside both segments."""
    M = mat(q)
    hits = 0
    for p1, d1 in cube_edges(M):
        for p0, d2, ca, cb in lines:
            w = tuple(p0[i] - p1[i] for i in range(3))
            if det3(d1, d2, w) != 0:
                continue
            # coplanar: solve p1 + s d1 = p0 + t d2 in the best-conditioned pair
            cr = (d1[1]*d2[2]-d1[2]*d2[1], d1[2]*d2[0]-d1[0]*d2[2],
                  d1[0]*d2[1]-d1[1]*d2[0])
            if not any(cr):
                continue
            k = max(range(3), key=lambda u: abs(cr[u]))
            u1, u2 = [t for t in range(3) if t != k]
            det = d1[u1]*(-d2[u2]) - (-d2[u1])*d1[u2]
            if det == 0:
                continue
            s = (w[u1]*(-d2[u2]) - (-d2[u1])*w[u2]) / det
            if 0 <= s <= 1:          # inside the free cube's real edge
                hits += 1
    return hits


CONFIGS = {
    '727 record': (7, 14, 1, -5),
    '723': (5, 2, 2, 2),
    '727 rep A': (153, -289, -197, -13),
    '727 rep B': (1, -5, -7, -14),
    '727 rep C': (5, -92, -36, -57),
    'control (generic)': (7, 3, 5, 11),
    'control 2 (generic)': (13, 9, -4, 6),
}


def main():
    pts, lines = base_catalogue()
    print('base catalogue: %d real triple points, %d crossing lines\n'
          % (len(pts), len(lines)), flush=True)
    print('%-20s %6s %8s %8s %10s' %
          ('config', 'W4', 'W4 4-pl', 'W4 6-pl', 'W3 edges'))
    for name, q in CONFIGS.items():
        h = w4_count(q, pts)
        n4 = sum(1 for npl, _ in h if npl == 4)
        n6 = sum(1 for npl, _ in h if npl == 6)
        w3 = w3_count(q, lines)
        print('%-20s %6d %8d %8d %10d' % (name, len(h), n4, n6, w3), flush=True)


if __name__ == '__main__':
    main()
