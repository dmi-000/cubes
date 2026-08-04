#!/usr/bin/env python3
"""Which of the five n=2 counts are epsilon-neighbours of which?

Postscript 69 maps the values: generic 4, then 5 and 9, the maximum 13 on
curves, and 1 at the 24 points where the cubes coincide. This builds the
adjacency: for a representative of each count, which counts occur arbitrarily
close to it, and does the count occur near ITSELF?

The self-adjacency test is the useful one, and it is the user's criterion:
if points of count X are arbitrarily close to other points of count X, the
X-set is positive-dimensional -- a continuum -- and if not, X is attained only
at isolated points.

SAMPLING NOTE, which is the whole method. Walls here are rational, so points
ON them have SMALL DENOMINATORS. Random real-ish sampling (large random
integer quaternions) essentially never lands on a wall -- that is exactly the
bias that made an earlier reading of this same question wrong. So the
neighbourhood is probed with a LATTICE of rationals p + (i,j,k)/D, which hits
the walls precisely because it is arithmetically special. The bias is the
instrument here, not the error.

INVARIANT: every neighbourhood count is exact; and the ball radius is shrunk
by a factor of 4 and the neighbour set recomputed, so a count that appears
only at coarse radius is not reported as a neighbour.
"""
import collections
import json
import math
import subprocess
import sys
from fractions import Fraction as F


def to_q(pt, cap=10**7):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0]*den), int(pt[1]*den), int(pt[2]*den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x//g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= cap else None


def batch(qs):
    inp = '\n'.join('1,0,0,0;' + ','.join(map(str, q)) for q in qs) + '\n'
    out = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                         capture_output=True, text=True).stdout
    rows = [json.loads(l).get('bounded') for l in out.splitlines()
            if l.startswith('{')]
    assert len(rows) == len(qs), (len(rows), len(qs))
    return rows


def ball(pt, D, R):
    """lattice points pt + (i,j,k)/D with 0 < max|i,j,k| <= R."""
    out = []
    for i in range(-R, R+1):
        for j in range(-R, R+1):
            for k in range(-R, R+1):
                if i == j == k == 0:
                    continue
                p = (pt[0] + F(i, D), pt[1] + F(j, D), pt[2] + F(k, D))
                q = to_q(p)
                if q:
                    out.append(q)
    return out


REPS = {
    4:  (F(37, 100), F(-23, 100), F(61, 100)),      # generic
    5:  None,                                        # filled in below
    9:  None,
    13: (F(5, 7), F(-5, 7), F(5, 7)),                # body-diagonal curve
    1:  (F(0), F(0), F(0)),                          # cubes coincide
}


def main():
    # locate a 5 and a 9 by walking a coordinate from the generic point
    base = REPS[4]
    for target in (5, 9):
        found = None
        for num in range(1, 400):
            for sgn in (1, -1):
                p = (base[0] + sgn*F(num, 200), base[1], base[2])
                q = to_q(p)
                if q and batch([q])[0] == target:
                    found = p
                    break
            if found:
                break
        REPS[target] = found
    print('representatives:')
    for c, p in sorted(REPS.items()):
        print('   count %-3s at (a,b,c) = %s' % (c, tuple(str(x) for x in p)))

    print('\nneighbour sets, at shrinking lattice spacing:')
    adj = {}
    for c, p in sorted(REPS.items()):
        row = {}
        for D in (24, 96, 384):
            qs = ball(p, D, 2)
            if not qs:
                continue
            vals = collections.Counter(batch(qs))
            row[D] = vals
        stable = None
        for D in sorted(row):
            keys = set(row[D])
            stable = keys if stable is None else (stable & keys)
        adj[c] = stable
        print('   count %-3s : %s' % (c, ' | '.join(
            '1/%d: %s' % (D, dict(sorted(row[D].items(),
                                         key=lambda t: (t[0] is None, t[0]))))
            for D in sorted(row))))
    print('\nadjacency (counts present at EVERY radius tested):')
    for c in sorted(adj):
        others = sorted(x for x in adj[c] if x is not None)
        self_adj = c in adj[c]
        print('   %-3s -> %-18s   self-adjacent: %-5s  =>  %s'
              % (c, str(others), self_adj,
                 'CONTINUUM' if self_adj else 'isolated points only'))


if __name__ == '__main__':
    main()
