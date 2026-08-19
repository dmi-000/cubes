#!/usr/bin/env python3
"""How big is the LOCAL chamber problem for extending the 393 base?

Extension-climbing is 3-dimensional: the walls of the base lift into the larger
configuration as cylinders and do not constrain the new cube at all, so the only
walls that matter are the free cube's own, and against a FIXED base those form a
finite catalogue (Postscript 57): 424 real triple points -> 2 544 W4 walls,
360 crossing lines -> 4 320 W3 walls.

Enumerating all ~6 900 in R^3 is hopeless.  But the climbing question is LOCAL —
which chambers are adjacent to the current record — and that needs only the walls
INCIDENT AT the record's free cube.  This measures that number, which decides
whether local chamber enumeration is minutes or intractable.

Incidence is exact: a W4 wall is active iff a face plane of the free cube passes
exactly through a base triple point; a W3 wall is active iff a free-cube edge
meets a base crossing line.  No tolerance anywhere.
"""
import collections, itertools, json, os, sys
from fractions import Fraction as F
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from base_points import FIVE, mat, planes, solve3, in_cube

FREE = (7, 14, 1, -5)          # the sixth cube of the 727 record


def base_arrangement():
    P = planes(FIVE)
    mats = [mat(q) for q in FIVE]
    trans = [[[M[k][i] for k in range(3)] for i in range(3)] for M in mats]
    pts = collections.defaultdict(set)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is None or max(abs(x) for x in s) > 4:
            continue
        pts[s] |= {i, j, k}
    real = []
    for s in pts:
        on = [t for t in range(len(P))
              if sum(P[t][0][u]*s[u] for u in range(3)) == P[t][1]]
        cubes = {P[t][2] for t in on}
        if all(in_cube(s, trans[c]) for c in cubes):
            real.append(s)
    lines = []
    for a, b in itertools.combinations(range(len(P)), 2):
        if P[a][2] == P[b][2]:
            continue
        n1, n2 = P[a][0], P[b][0]
        d = [n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2], n1[0]*n2[1]-n1[1]*n2[0]]
        if all(t == 0 for t in d):
            continue
        lines.append((a, b, d))
    return real, lines, P


def free_faces_edges(q):
    M = mat(q)
    faces = []
    for a in range(3):
        nrm = [M[i][a] for i in range(3)]
        for s in (1, -1):
            faces.append([s*t for t in nrm])
    edges = []
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        for sb in (1, -1):
            for sc in (1, -1):
                Ppt = [M[i][b]*sb + M[i][c]*sc - M[i][a] for i in range(3)]
                D = [M[i][a]*2 for i in range(3)]
                edges.append((Ppt, D))
    return faces, edges


def main():
    real, lines, P = base_arrangement()
    faces, edges = free_faces_edges(FREE)
    print('base 393: %d real triple points, %d crossing lines'
          % (len(real), len(lines)), flush=True)
    print('catalogue size: %d W4 + %d W3 = %d walls in the free cube\'s R^3'
          % (6*len(real), 12*len(lines), 6*len(real)+12*len(lines)), flush=True)

    w4 = 0
    for pt in real:
        for f in faces:
            if sum(f[i]*pt[i] for i in range(3)) == 1:
                w4 += 1
    # W3: does a free-cube edge segment meet a base crossing line?
    w3 = 0
    for a, b, d in lines:
        # a point on the line: solve the two plane equations plus one normalisation
        n1, n2 = P[a][0], P[b][0]
        base_pt = None
        for k in range(3):
            e = [1 if t == k else 0 for t in range(3)]
            s = solve3((n1, P[a][1], 0), (n2, P[b][1], 0), (e, F(0), 0))
            if s is not None:
                base_pt = s; break
        if base_pt is None:
            continue
        for Ppt, D in edges:
            W = [base_pt[i]-Ppt[i] for i in range(3)]
            det = (D[0]*(d[1]*W[2]-d[2]*W[1]) - D[1]*(d[0]*W[2]-d[2]*W[0])
                   + D[2]*(d[0]*W[1]-d[1]*W[0]))
            if det == 0:
                w3 += 1
    print('\nWALLS INCIDENT AT THE 727 SIXTH CUBE:', flush=True)
    print('   W4 (free face plane through a base triple point): %d' % w4, flush=True)
    print('   W3 (free edge coplanar with a base crossing line): %d' % w3, flush=True)
    k = w4 + w3
    print('   TOTAL incident: %d of %d catalogue walls' % (k, 6*len(real)+12*len(lines)),
          flush=True)
    print('\nlocal chamber bound: k surfaces through a point in R^3 give at most', flush=True)
    print('   k(k-1)+2 = %d chambers if they were PLANES (they are quadrics, so more)'
          % (k*(k-1)+2), flush=True)
    json.dump({'w4': w4, 'w3': w3, 'total': k, 'catalogue': 6*len(real)+12*len(lines),
               'plane_chamber_bound': k*(k-1)+2},
              open(os.path.join(HERE, 'size_local.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
