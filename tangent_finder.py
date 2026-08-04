#!/usr/bin/env python3
"""Find the tangent to a maximiser locus, when the locus is a curve.

WHY THIS EXISTS.  The lattice dimension probe (perturb each coordinate by 0,+-e
and read the dimension off 3^d - 1 survivors) is blind to any locus that is not
aligned with the coordinate directions: a curve in general position contains no
lattice neighbour at any e, so the probe reads 0 and the configuration gets
written down as isolated.  Demonstrated on a 727 locus known to be
1-dimensional, which reads 0 of 26 (FAILURE_MODES 11d).  Detecting a curve
requires moving ALONG it, so the tangent must be found first -- and random or
axis-aligned directions never find it, because a curve is measure zero in the
sphere of directions.

THE METHOD.  A curve inside a maximiser locus lies INSIDE the wall surfaces
through its point: crossing a wall changes the count, so a direction that keeps
the count must be tangent to every active wall.  Hence

    tangent  ⊥  gradient of every wall active at the point.

One active wall cuts the search from the 2-sphere of directions to a circle,
which is a finite scan.  The walls used here are the 119 enumerated locus planes
(`locus_planes.pkl`, the edge-edge conditions of Postscript 49, which factor
into rational planes); the point's active set is found exactly, by substitution.

VALIDATED, then applied (2026-08-04):

  * 727 at the midpoint of the arc through the d=13/1093/2741 classes: one
    active plane, and exactly 2 of 96 in-plane directions preserve 727 --
    (1/6,-1/2,-1) and its negative, i.e. (1,-3,-6), the tangent already known
    from two independent Q(sqrt d) solutions.  The method recovers it.
  * 723 at (5,2,2,2), tangent previously unknown: six active planes, and
    exactly 2 of 96 in-plane directions preserve 723 -- **(1,1,1)**.  That is
    the sixth cube sliding along the shared C3 axis, which is the family
    Postscript 12 built 723 from in the first place.

LIMITATION.  It only sees walls that are in the catalogue.  Arc A lies in just
ONE catalogue plane, so its second defining wall is of the never-enumerated
W3/W4 type (Postscript 58) -- the scan still succeeds because one plane is
enough to reduce the search to a circle, but a point lying on NO catalogue plane
is out of reach of this version.

    python3 tangent_finder.py                # runs the validation and the 723 case
"""
import json
import math
import pickle
import subprocess
import sys
from fractions import Fraction as F

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
ENGINE = './cube_regions_n'


def counts(points):
    """Exact counts for a list of sixth-cube Cayley points on the 393 base."""
    lines = []
    for p in points:
        den = 1
        for x in p:
            den = den * x.denominator // math.gcd(den, x.denominator)
        q = (den,) + tuple(int(x * den) for x in p)
        lines.append(';'.join(','.join(map(str, c)) for c in FIVE) + ';'
                     + ','.join(map(str, q)))
    r = subprocess.run([ENGINE, '--quats-stdin'], input='\n'.join(lines) + '\n',
                       capture_output=True, text=True)
    rows = [json.loads(l).get('bounded') for l in r.stdout.splitlines()
            if l.startswith('{')]
    if len(rows) != len(points):
        raise SystemExit('engine returned %d of %d' % (len(rows), len(points)))
    return rows


def active_planes(pt, catalogue='locus_planes.pkl'):
    """The catalogue wall planes passing exactly through pt."""
    out = []
    for cube, planes in pickle.load(open(catalogue, 'rb')).items():
        for pl in planes:
            a, b, c, e = [F(x) for x in pl]
            if a + b*pt[0] + c*pt[1] + e*pt[2] == 0:
                out.append((cube, pl, (b, c, e)))
    return out


def in_plane_directions(normal, reach=6):
    """A finite scan of directions orthogonal to `normal`, normalised."""
    n = [F(x) for x in normal]
    k = max(range(3), key=lambda i: abs(n[i]))
    o = [i for i in range(3) if i != k]
    b1, b2 = [F(0)]*3, [F(0)]*3
    b1[o[0]], b1[k] = n[k], -n[o[0]]
    b2[o[1]], b2[k] = n[k], -n[o[1]]
    seen = []
    for i in range(-reach, reach + 1):
        for j in range(-reach, reach + 1):
            if i == 0 and j == 0:
                continue
            d = [i*b1[t] + j*b2[t] for t in range(3)]
            m = max(abs(x) for x in d)
            d = [x / m for x in d]
            if d not in seen:
                seen.append(d)
    return seen


def find_tangent(pt, target, eps=F(1, 64), verbose=True):
    """Directions at pt that preserve `target`, searched inside active walls."""
    act = active_planes(pt)
    if verbose:
        print('  %d active catalogue wall plane(s)' % len(act))
    if not act:
        if verbose:
            print('  no enumerated wall here -- this version cannot reduce the '
                  'search; the active wall is of the unenumerated W3/W4 type')
        return []
    for cube, pl, normal in act:
        dirs = in_plane_directions(normal)
        res = counts([[pt[t] + eps*d[t] for t in range(3)] for d in dirs])
        good = [d for d, c in zip(dirs, res) if c == target]
        if verbose:
            print('  plane %-18s %d of %d in-plane directions preserve %d'
                  % (str(pl), len(good), len(dirs), target))
        if good:
            return good
    return []


def sweep(pt, direction, target, lo=-40, hi=41, den=32):
    """Walk the tangent and report the runs of constant count."""
    ss = [F(n, den) for n in range(lo, hi)]
    res = counts([[pt[i] + s*direction[i] for i in range(3)] for s in ss])
    runs = []
    for s, c in zip(ss, res):
        if runs and runs[-1][0] == c:
            runs[-1][2] = s
        else:
            runs.append([c, s, s])
    return runs


if __name__ == '__main__':
    print('VALIDATION: 727 at the midpoint of arc A, tangent (1,-3,-6) known')
    a0, v = [F(19, 3), F(-7), F(-11)], [F(1), F(-3), F(-6)]
    mid = [a0[i] + F(5, 2)*v[i] for i in range(3)]
    for d in find_tangent(mid, 727)[:2]:
        print('    tangent %s' % [str(x) for x in d])

    print('\n723 at (5,2,2,2), tangent previously unknown')
    pt = [F(2, 5)]*3
    good = find_tangent(pt, 723)
    for d in good[:2]:
        print('    tangent %s' % [str(x) for x in d])
    if good:
        print('\n  walking it:')
        for c, lo, hi in sweep(pt, good[0], 723):
            print('    %-5s s in [%s, %s]%s'
                  % (c, lo, hi, '   <== 723' if c == 723 else ''))
