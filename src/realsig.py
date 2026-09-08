#!/usr/bin/env python3
"""REAL incidences: does the coincidence fall inside the actual faces, or off their edges?

The user's question -- when identical signatures give different counts, what distinguishes
the configurations? -- and the user's own answer: something must align to split regions in
one and merge them in the other.

The mechanism is face-boundedness. `signature.py` counts points where face PLANES meet.
But a region boundary is a face SQUARE, so an incidence only does geometric work if it
lies within the faces themselves; on the planes' extensions beyond the squares it is
algebraically identical and geometrically inert. Two configurations can therefore share a
plane-incidence signature exactly and differ in how many of those incidences are real.

For an integer quaternion q the plane rows M_i satisfy |M_i . x| <= n on the cube, with
n = w^2+x^2+y^2+z^2, so "p is inside cube k" and "p lies on cube k's actual face" are both
exact integer tests -- no tolerance anywhere.

Reported as (total incidences, REAL incidences) so the two can be compared directly: if
same-signature pairs differ in the real count, that is the missing ingredient.
"""
import itertools, sys
from collections import Counter
from fractions import Fraction as F
sys.path.insert(0, '.')
from concurrence import planes, solve3

def cube_data(cfg):
    out = []
    for (w, x, y, z) in cfg:
        n = w*w + x*x + y*y + z*z
        M = [[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
             [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
             [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]]
        out.append((M, n))
    return out

def on_face(p, M, n):
    """p lies on this cube's actual surface: one row saturates, the others are inside"""
    vals = [sum(F(M[i][k]) * p[k] for k in range(3)) for i in range(3)]
    sat = sum(1 for v in vals if abs(v) == n)
    return sat >= 1 and all(abs(v) <= n for v in vals)

def real_and_total(cfg):
    P = planes(cfg)
    cubes = cube_data(cfg)
    owner = [i // 6 for i in range(len(P))]
    pts = {}
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is None:
            continue
        pts.setdefault(s, set()).update((owner[i], owner[j], owner[k]))
    total = len(pts)
    real = 0
    for p, owners in pts.items():
        if all(on_face(p, cubes[o][0], cubes[o][1]) for o in owners):
            real += 1
    return total, real

if __name__ == '__main__':
    import json, random, subprocess
    from collections import defaultdict
    from math import gcd
    from signature import signature, count
    from sharedaxis import q_axis
    from symmetrize import axes
    from haarsample import haar_config
    rng = random.Random(4); AX = axes(3)
    vals = [F(p, q) for q in (1,2,3,4,5,6) for p in range(-6,7) if p and gcd(abs(p), q) == 1]
    groups = defaultdict(list)
    for i in range(70):
        cfg = (haar_config(rng, 4, 64, chart=True) if i % 2 else
               [(1,0,0,0)] + [q_axis(rng.choice(AX), rng.choice(vals)) for _ in range(3)])
        c = count(cfg)
        if c:
            groups[signature(cfg)].append((c, cfg))
    print('Same plane-incidence signature, different count: do the REAL incidences differ?')
    print()
    print('  count A  count B   total A/B      REAL A/B      real explains it?')
    agree = tested = 0
    for sg, v in groups.items():
        if len(v) < 2:
            continue
        for (c1, f1), (c2, f2) in itertools.combinations(v, 2):
            if c1 == c2:
                continue
            t1, r1 = real_and_total(f1); t2, r2 = real_and_total(f2)
            tested += 1
            ok = (r1 > r2) == (c1 > c2) and r1 != r2
            agree += ok
            if tested <= 8:
                print('   %4d    %4d     %5d/%-5d    %4d/%-4d      %s'
                      % (c1, c2, t1, t2, r1, r2, 'YES' if ok else ('tied' if r1 == r2 else 'no')))
            if tested >= 30:
                break
        if tested >= 30:
            break
    print()
    print('real-incidence count orders the pair correctly in %d of %d (%.0f%%)'
          % (agree, tested, 100.0 * agree / max(tested, 1)))
