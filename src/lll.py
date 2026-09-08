#!/usr/bin/env python3
"""Integer LLL, to pick a SHORT basis of a null space instead of an arbitrary one.

Why this exists: at the n=10 record 3917 the null space is 6-dimensional and sympy's
basis has heights [1, 1, 1, 884318520, 1095277680, 884318520]. The eps engine refuses
the three big ones, so `map_geometry.py` could verify only a 5-dimensional subspace
and left the deficit-6 question open ([P195]). The subspace is the same either way —
the heights are an artefact of the basis, which is a free choice ([METHODS 15]).

A crude greedy size-reduction was tried earlier (`eps_null2.py`) and shortened
nothing, because it only subtracts multiples of one vector from another and these
vectors are nearly orthogonal in the wrong order. LLL swaps as well as reduces.
"""
from fractions import Fraction as F


def lll(B, delta=F(99, 100)):
    """LLL-reduce a list of integer vectors (rows). Exact rational Gram-Schmidt."""
    B = [list(map(F, b)) for b in B]
    n = len(B)

    def gso(B):
        Bs, mu = [], [[F(0)] * n for _ in range(n)]
        for i in range(n):
            v = list(B[i])
            for j in range(i):
                d = sum(x * x for x in Bs[j])
                mu[i][j] = (sum(a * b for a, b in zip(B[i], Bs[j])) / d) if d else F(0)
                v = [x - mu[i][j] * y for x, y in zip(v, Bs[j])]
            Bs.append(v)
        return Bs, mu

    Bs, mu = gso(B)
    k = 1
    guard = 0
    while k < n and guard < 20000:
        guard += 1
        for j in range(k - 1, -1, -1):
            q = mu[k][j]
            r = int(q + F(1, 2)) if q >= 0 else -int(-q + F(1, 2))
            if r:
                B[k] = [x - r * y for x, y in zip(B[k], B[j])]
                Bs, mu = gso(B)
        nk = sum(x * x for x in Bs[k])
        nk1 = sum(x * x for x in Bs[k - 1])
        if nk >= (delta - mu[k][k - 1] ** 2) * nk1:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gso(B)
            k = max(k - 1, 1)
    return [[int(x) for x in b] for b in B]


if __name__ == '__main__':
    import sys, itertools
    sys.path.insert(0, '.')
    from math import gcd
    from eps_null import walls_and_null
    BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
    C10=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),
              (88787,-9061,74275,113786)]
    pt,walls,null,ncols=walls_and_null(C10)
    def prim(v):
        den=1
        for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
        iv=[int(F(x)*den) for x in v]; g=0
        for x in iv: g=gcd(g,abs(x))
        return [x//(g or 1) for x in iv]
    B0=[prim(v) for v in null]
    print('before LLL, heights:', [max(abs(x) for x in b) for b in B0])
    B1=[prim(b) for b in lll(B0)]
    print('after  LLL, heights:', [max(abs(x) for x in b) for b in B1])
    import sympy as sp
    print('rank preserved: %d -> %d'%(sp.Matrix(B0).rank(), sp.Matrix(B1).rank()))
