#!/usr/bin/env python3
"""Walk the SPARSE directions of the tight-set null space.

A generic basis vector of the null space is a rotation of the true tangent
mixed with whatever else the space contains, and it fails the engine walk even
when the true tangent lies in the space (n=6 723: known tangent projects 1.0000,
every basis vector fails).  The tangents that exist are SPARSE -- supported on
one or two cubes -- so intersect the null space with each coordinate subspace
"only cubes S move" and walk what survives.  Positive results self-certify.
"""
import sys, itertools
import numpy as np
from fractions import Fraction as F
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from tight2 import null_of, walk, count, BASE

EPS = (F(1,64), F(1,256), F(1,1024))

def sub_intersect(null, keep, npar):
    """directions in span(null) vanishing outside the coordinate set `keep`"""
    drop = [i for i in range(npar) if i not in keep]
    if not drop:
        return list(null)
    A = null[:, drop]                      # (k, |drop|)
    U, S, Vt = np.linalg.svd(A.T @ np.eye(len(null)) if False else A, full_matrices=False)
    # coefficients c with c @ A == 0
    k = null.shape[0]
    M = A.T                                # (|drop|, k)
    U2, S2, V2t = np.linalg.svd(M, full_matrices=True)
    tol = 1e-8*max(S2[0] if len(S2) else 1.0, 1e-30)
    cs = [V2t[i] for i in range(k) if i >= len(S2) or S2[i] <= tol]
    return [c @ null for c in cs]

def test(qs, label, known=None):
    base = count(list(qs))
    nq, nt, rank, null, npar = null_of(qs)
    ncube = len(qs)-1
    print('%-16s count=%-5s  %d tight, rank %d/%d, null dim %d'
          % (label, base, nt, rank, npar, len(null)))
    if len(null) == 0:
        print('   -> null space empty')
        return 0, []
    cands = []
    for r in (1, 2, 3):
        for S in itertools.combinations(range(1, ncube+1), r):
            keep = [3*(i-1)+j for i in S for j in range(3)]
            for v in sub_intersect(null, keep, npar):
                if np.max(np.abs(v)) > 1e-9:
                    cands.append(('cubes'+str(S), v))
    for i, v in enumerate(null):
        cands.append(('basis%d' % i, v))
    hits = []
    seen = []
    for name, v in cands:
        v = v/np.linalg.norm(v)
        if any(abs(abs(v @ s)-1) < 1e-6 for s in seen):
            continue
        seen.append(v)
        u = [F(float(x)).limit_denominator(10**6) for x in v/np.max(np.abs(v))]
        w = walk(qs, u, EPS)
        if all(c == base for _, c in w):
            hits.append(v)
            print('   HOLDS %-12s %s' % (name, np.array2string(
                v/np.max(np.abs(v)), precision=4, suppress_small=True, max_line_width=250)))
    if hits:
        s = np.linalg.svd(np.array(hits), compute_uv=False)
        print('   -> VERIFIED tangent dimension >= %d' % int((s > 1e-6*s[0]).sum()))
    else:
        print('   -> nothing in the null space verifies')
    return len(null), hits

if __name__ == '__main__':
    print('=== controls ===')
    test([(1,0,0,0),(1,-12,-11,0)], 'n=2 mirror 13')
    test(BASE+[(10,9,9,9)], 'n=6 723')
    test(BASE+[(6,53,-87,-156)], 'n=6 727 arcA')
    test(BASE+[(7,14,1,-5)], 'n=6 727 record')
    print()
    print('=== open cells ===')
    test([(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)], 'n=4 183')
    test(BASE, 'n=5 393')
    test(BASE+[(7,14,1,-5),(4,-3,-4,-4)], 'n=7 1217')
    test(BASE+[(7,14,1,-5),(4,-3,-4,-4),(3,-3,3,-8)], 'n=8 1891')
