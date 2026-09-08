#!/usr/bin/env python3
"""Is a record's tall representative FORCED, or just the one the climb happened to land on?

[P211] concluded the n=9 record's height 113 786 is forced by its codimension, on two
pieces of evidence: no dyadic rounding of its coordinates recovers 2787 (tested to
1/2^24), and conjugating by each of the nine cubes in turn leaves the height unchanged.
[P216] showed why that is weak. Dyadic rounding is the wrong lattice -- it forces one
denominator on all 3(n-1) coordinates -- and conjugating by the configuration's own
cubes is a search of size n.

The user's argument for expecting a cheaper one: a record is a tightly constrained
subset of the rotation space, cut out by wall equations whose coefficients come from
cube geometry and a combinatorial type. That is bounded data, so the region ought to
contain a rational point of bounded height, and the height we hold ought not to grow
much faster than the description does. Against that, the recorded heights are

    n=5   7      n=8   61
    n=6  14      n=9   113786
    n=7  14      n=10  113786

and a jump of 1865x between n=8 and n=9 is exactly what that argument says should not
happen -- so either the argument fails, or 113 786 is an artifact of how the point was
found (a simplest-rational along ONE ray, inside a region of dimension 4).

METHOD. The region is not full-dimensional, so `simplify_box` cannot help: moving one
coordinate leaves the stratum and the count drops. The search has to happen INSIDE the
region, whose tangent space is the eps-verified preserving basis already computed by
`climb` (rank 4 at n=9, 5 at n=10). LLL-reduce that basis, then walk small rational
combinations of it and keep any point that still counts 2787, reporting the lowest
height found. Every candidate is checked by the count itself, so a point that has left
the region is rejected rather than trusted.

This is a LOWER-BOUND search: it can prove a cheaper representative exists, never that
none does.
"""
import sys, itertools
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
import climb as C
import dimension as D
from eps_null import walls_and_null
from lll import lll
from qfield import Q
from epscount import count_eps

def preserving_basis(cubes):
    """the eps-verified directions that keep the count -- the region's tangent space"""
    pt, walls, null, ncols = walls_and_null(cubes)
    rec = D.count_at(pt, len(cubes))
    B = [C.prim(b) for b in lll([list(C.prim(v)) for v in null])]
    good = []
    for b in B:
        ok = True
        for sgn in (1, -1):
            c = count_eps(pt, [Q(sgn * F(x), 0, 0) for x in b], 0, cubes[0])
            if c is None:
                c = count_eps(pt, [Q(sgn * F(x), 0, 0) for x in b], 0, cubes[0], wide=True)
            if c != rec:
                ok = False; break
        if ok:
            good.append(b)
    return pt, rec, good, ncols

def search(cubes, label, span=3, dens=(1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 64, 128, 256)):
    pt, rec, good, ncols = preserving_basis(cubes)
    h0 = max(abs(x) for q in cubes for x in q)
    print('%s: count %d, preserving rank %d, ambient %d, height %d'
          % (label, rec, len(good), ncols, h0), flush=True)
    if not good:
        print('   no preserving directions; nothing to search'); return
    best = (h0, None)
    tried = kept = 0
    for den in dens:
        for coef in itertools.product(range(-span, span + 1), repeat=min(len(good), 4)):
            if not any(coef):
                continue
            tried += 1
            p2 = list(pt)
            for a, b in zip(coef, good):
                if a:
                    for i in range(ncols):
                        p2[i] += F(a, den) * b[i]
            cf = C.cfg_at(p2, cubes[0])
            h = max(abs(x) for q in cf for x in q)
            if h >= best[0]:
                continue
            if C.cnt(cf) == rec:
                kept += 1
                best = (h, cf)
                print('   height %d  (%.1fx smaller)  %s'
                      % (h, h0 / h, ';'.join(','.join(map(str, q)) for q in cf)), flush=True)
    print('   searched %d combinations, %d improved; best height %d (was %d)'
          % (tried, kept, best[0], h0), flush=True)
    return best

if __name__ == '__main__':
    search(C.N9, 'n=9 record 2787')
