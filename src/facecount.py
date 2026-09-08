#!/usr/bin/env python3
"""Total FACE count by derivation — size the face enumeration before running it.

P142 stopped the face descent because it was quadratic in output (the same face
re-tested from every bordering chamber, no deduplication) and recorded it as "not
sound". The defect is COMPLEXITY, not correctness -- worth stating precisely,
because it decides whether repair is worthwhile.

Before repairing it, size it. Every face of a real central arrangement is a
relatively open cell whose affine hull is a flat X, and the faces with hull X are
exactly the chambers of the RESTRICTED arrangement A^X. So

    total faces = sum over X in L(A) of chambers(A^X)

Each term is the same NBC recursion already used for chambers (P152). A^X is the
arrangement induced on X by the walls NOT containing X, which in the closed-set
representation means: quotient by X's own walls, keep the rest.

This is P142's own advice applied one level up -- it told the 727 run to compute
the exact chamber count from the matroid before committing cores, which turned
"probably fits" into a number. The same question is now open for faces.

GATE: the coordinate arrangement in R^n has 3^n faces (every sign vector), 3^n - 1
excluding the origin, and 2^n chambers. Both must come out exactly.
"""
import sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
from zaslavsky import Flats, chambers


def restricted_walls(W, flat_mask, m, ncols):
    """Walls of A^X: the walls NOT containing X, restricted to X.

    X is the common zero set of the walls in flat_mask. Restricting to X means
    expressing each remaining wall on a basis of X; a wall meeting X in all of X
    would be in flat_mask already, so every survivor cuts X properly."""
    import itertools
    L = Flats(W)
    # basis of X = null space of the flat's walls
    rows = [W[j] for j in range(m) if flat_mask >> j & 1]
    # nullspace by elimination over Q
    A = [[F(x) for x in r] for r in rows]
    piv, где = [], {}
    r = 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(A)) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        pv = A[r][c]
        A[r] = [v / pv for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        где[c] = r; piv.append(c); r += 1
    free = [c for c in range(ncols) if c not in где]
    basis = []
    for fc in free:
        v = [F(0)] * ncols
        v[fc] = F(1)
        for c in piv:
            v[c] = -A[где[c]][fc]
        basis.append(v)
    out = []
    for j in range(m):
        if flat_mask >> j & 1:
            continue
        row = [sum(F(W[j][t]) * b[t] for t in range(ncols)) for b in basis]
        if any(row):
            out.append(row)
    return out, len(basis)


def total_faces(W, ncols, log=sys.stdout, label=''):
    t0 = time.time()
    m = len(W)
    L = Flats(W)
    memo = {}
    sys.setrecursionlimit(10000)

    def N(i, flat):
        if i < 0:
            return 1
        k = (i, flat)
        if k in memo:
            return memo[k]
        if flat >> i & 1:
            memo[k] = 0; return 0
        r = N(i - 1, flat) + N(i - 1, L.extend(flat, i))
        memo[k] = r
        return r
    N(m - 1, L.empty)
    flats = sorted(L._basis)
    tot = 0
    for fm in flats:
        rw, dim = restricted_walls(W, fm, m, ncols)
        if not rw:
            tot += 1                      # X itself is one face (its own interior)
            continue
        c, _, _, _ = chambers(rw, log=open('/dev/null', 'w'))
        tot += c
    print('%s flats %d -> TOTAL FACES %s  (%.1fs)'
          % (label, len(flats), '{:,}'.format(tot), time.time() - t0), file=log, flush=True)
    return tot, len(flats)


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    W = [[F(1) if t == i else F(0) for t in range(n)] for i in range(n)]
    tot, nf = total_faces(W, n, label='coordinate R^%d:' % n)
    print('  expect %d (3^%d)  -> %s' % (3**n, n, 'PASS' if tot == 3**n else 'FAIL'))
