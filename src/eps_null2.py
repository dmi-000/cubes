#!/usr/bin/env python3
"""The count-preserving subset of the null space, with a SIZE-REDUCED basis.

`eps_null.py` left one direction at n=8 unevaluated, the engine refusing it.  Its
tell was METHODS 15's: every direction that HELD had |v|max 1 and the refusal had
|v|max 9 960 — a clean split by input height, not by anything about the object.  A
null SPACE has no canonical basis, so a long basis vector is a bad representative
and not a hard case: size-reduce it against the short ones.

Then the real question, which a basis cannot answer: is the count-preserving set a
SUBSPACE?  If v and w each hold, testing v+w and v-w says whether "the directions
along which the count survives infinitesimally" is a linear object or merely a set.
"""
import sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from math import gcd
from qfield import Q
import dimension as D
from wallcount import R
from epscount import count_eps
from eps_null import walls_and_null


def primitive(v):
    den = 1
    for x in v:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    iv = [int(F(x) * den) for x in v]
    g = 0
    for x in iv:
        g = gcd(g, abs(x))
    return [x // (g or 1) for x in iv]


def size_reduce(basis):
    """Greedy: repeatedly shorten each vector by integer multiples of the others."""
    B = [primitive(v) for v in basis]
    for _ in range(40):
        changed = False
        B.sort(key=lambda v: sum(x * x for x in v))
        for i in range(len(B)):
            for j in range(len(B)):
                if i == j:
                    continue
                nj = sum(x * x for x in B[j])
                if nj == 0:
                    continue
                mu = sum(a * b for a, b in zip(B[i], B[j]))
                k = (2 * mu + nj) // (2 * nj)          # round(mu/nj), floor-safe
                if k:
                    cand = primitive([a - k * b for a, b in zip(B[i], B[j])])
                    if any(cand) and sum(x * x for x in cand) < sum(x * x for x in B[i]):
                        B[i] = cand; changed = True
        if not changed:
            break
    return B


def ev(pt, q0, v, rec):
    out = []
    for sgn in (1, -1):
        out.append(count_eps(pt, [Q(F(sgn * x), 0, 0) for x in v], 0, q0))
    return out


for n in (7, 8):
    quats = R[n]
    pt, walls, null, ncols = walls_and_null(quats)
    rec = D.count_at(pt, len(quats))
    B = size_reduce(null)
    print('\nn=%d  record %d  nullity %d   heights before %s  after %s'
          % (n, rec, len(null),
             [max(abs(x) for x in primitive(v)) for v in null],
             [max(abs(x) for x in v) for v in B]), flush=True)
    hold, unev = [], 0
    for i, v in enumerate(B):
        r = ev(pt, quats[0], v, rec)
        if None in r:
            unev += 1; tag = 'UNEVALUATED — refused, NOT a negative'
        elif r[0] == rec and r[1] == rec:
            hold.append(v); tag = 'HOLDS both sides'
        elif rec in r:
            tag = 'holds ONE side — boundary'
        else:
            tag = 'changes'
        print('   b%d |v|max %-6d  +eps %-6s  -eps %-6s  %s'
              % (i, max(abs(x) for x in v), r[0], r[1], tag), flush=True)
    print('   %d of %d hold, %d unevaluated' % (len(hold), len(B), unev), flush=True)

    if len(hold) >= 2:
        print('   --- is the holding set a SUBSPACE? ---', flush=True)
        for (a, b, lbl) in ((1, 1, 'v+w'), (1, -1, 'v-w'), (2, 1, '2v+w')):
            c = primitive([a * x + b * y for x, y in zip(hold[0], hold[1])])
            r = ev(pt, quats[0], c, rec)
            print('   %-5s |v|max %-6d +eps %-6s -eps %-6s  %s'
                  % (lbl, max(abs(x) for x in c), r[0], r[1],
                     'UNEVALUATED' if None in r else
                     'holds' if r == [rec, rec] else 'CHANGES — not a subspace'),
                  flush=True)
