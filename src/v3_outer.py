#!/usr/bin/env python3
"""V3 on the OUTER boundary, and whether the n=3 theorem can be applied per triple.

METHODS 11 proves  d1 = V3/2 + c + 1  with V3 the triple points on d(A_1 u ... u A_n),
then bounds V3 <= 216*C(n,3) -- one face plane from each of three cubes, 6^3 per triple.
It also records that 216 is loose "even at n = 3, where the true cap implied by d1 <= 48 is
V3 <= 92", and then keeps using 216 at n >= 4.

THE SUBSTITUTION THIS TESTS. Every triple point of {A,B,C} on the outer boundary of a LARGER
configuration is in particular a triple point of {A,B,C} lying outside every other body, so
it is a triple point on d(A u B u C) as well -- adding cubes can only DELETE such points, by
swallowing them. If that holds,

    V3(n)  <=  sum over triples of V3(triple alone)  <=  92 * C(n,3)

replacing 216 by 92 with no new geometry, and at n=4 giving d1 <= 186 rather than 434.

Numerical, not a proof: the claim is checked on configurations before any argument is built
on it, because the inequality is exactly the kind that is obvious and false at coincidences.
"""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cellcomplex import on_bdry_params
from euler3 import rowsT, frames, segments


def triple_points(qs, restrict=None):
    """the triple points of the arrangement, each tagged with the set of bodies it lies on.

    `restrict` limits which bodies' pairwise curves are traced (so a sub-triple can be
    examined inside a larger configuration); membership is still tested against ALL bodies,
    which is what makes the outer-boundary test meaningful.
    """
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    idxs = range(n) if restrict is None else restrict
    node = {}
    for i, j in itertools.combinations(idxs, 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    node.setdefault(P, set()).update((i, j))
    for P, on in node.items():
        for k in range(n):
            if k in on:
                continue
            v = [abs(sum(Ms[k][q][z] * P[z] for z in range(3))) for q in range(3)]
            if all(x <= 1 for x in v) and any(x == 1 for x in v):
                on.add(k)
    return Ms, node


def strictly_inside(P, M):
    return all(abs(sum(M[q][z] * P[z] for z in range(3))) < 1 for q in range(3))


def v3_outer(qs, restrict=None):
    """triple points of the (restricted) bodies that lie on the OUTER boundary of ALL of qs"""
    Ms, node = triple_points(qs, restrict)
    n = len(qs)
    out = 0
    for P, on in node.items():
        if len(on) < 3:
            continue
        if any(strictly_inside(P, Ms[k]) for k in range(n) if k not in on):
            continue                      # swallowed by another body: not on the union boundary
        out += 1
    return out


def count_and_depth(qs):
    s = ';'.join(','.join(map(str, q)) for q in qs)
    d = json.loads(subprocess.run([HERE + '/cube_regions_n', '--quats', s],
                                  capture_output=True, text=True).stdout)
    return d['bounded'], d['by_depth']


if __name__ == '__main__':
    CASES = {
        'n=4 record 183': [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)],
        'n=4 tower layer': [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1)],
        'n=4 haar':        [(1,0,0,0),(7,3,-2,5),(4,-5,3,1),(2,7,-3,4)],
        'n=5 record 393':  [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)],
    }
    print('%-18s %5s %6s %8s %10s %12s' % ('case', 'd1', 'V3', 'V3/2+2', 'sum-triples', '92*C(n,3)'))
    for name, qs in CASES.items():
        n = len(qs)
        cnt, dep = count_and_depth(qs)
        d1 = dep['1']
        v3 = v3_outer(qs)
        st = sum(v3_outer(qs, restrict=t) for t in itertools.combinations(range(n), 3))
        cap = 92 * (n * (n-1) * (n-2) // 6)
        print('%-18s %5d %6d %8s %10d %12d' % (name, d1, v3, v3 // 2 + 2, st, cap))
    print()
    print('identity is d1 = V3/2 + c + 1; c = 1 for a connected curve arrangement')


def outer_curve_components(qs):
    """c = connected components of the pairwise-curve arrangement ON the outer boundary.

    The identity d1 = V3/2 + c + 1 carries c, and METHODS' bound d1 <= 108*C(n,3) + 2
    reports the constant 2, i.e. it takes c = 1. Whether c is 1 in general is not a
    statement about plane-triples and is not implied by any cap on V3, so it is computed
    here rather than assumed.
    """
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    node = {}
    arcs = []
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                # keep the arc only if its interior lies on the OUTER boundary
                if any(strictly_inside(mid, Ms[k]) for k in range(n) if k not in (i, j)):
                    continue
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    node.setdefault(P, len(node))
                    ends.append(node[P])
                arcs.append(tuple(ends))
    par = list(range(len(node)))
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in arcs:
        par[f(a)] = f(b)
    seen = {f(x) for x in range(len(node))}
    return len(seen), len(node), len(arcs)
