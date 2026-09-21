#!/usr/bin/env python3
"""A vectorised arrangement census — same answer as `n3_arc.census_n`, ~1000x faster.

WHY.  The n = 8 dimension test needs six censuses.  Measured, one census at n = 8 takes about an
HOUR: `C(48,3) = 17 296` plane triples, each a determinant and three Cramer solves at 45 digits,
followed by an **O(P^2)** deduplication over thousands of points.  The other stages together are
96 seconds.  Two runs were killed at the wall-clock limit inside this one function.

WHAT CHANGES, and what does not.

  * **Double precision instead of 45 digits.**  Every decision here is a sign test on an O(1)
    quantity, and the margins measured at n = 4 run 0.013 to 0.05 -- fourteen orders of
    magnitude above double's noise.  The high precision was guarding against a risk the
    measurements say is absent.  **A margin guard is returned anyway**, and a caller that sees a
    small margin should escalate rather than trust the answer ([P334], in the direction that
    matters here).
  * **Spatial-hash dedup instead of O(P^2).**  Round to a grid and use a dict.
  * **Vectorised over triples and over planes.**  numpy, not Python loops.

**GATED.**  `--gate` runs both this and the exact `census_n` at n = 3 and n = 4, where the slow
one is affordable, and requires identical censuses.  A faster routine that has not been checked
against the slow one on a known answer is worth nothing.
"""
import sys, os, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)


def census(qlist, tol=1e-9):
    """(signature census, skipped, margin) for concentric cubes given as quaternions."""
    import numpy as np
    Q = np.array([[float(t) for t in q] for q in qlist], dtype=float)
    n = len(Q)
    F = np.empty((n, 3, 3))
    for k in range(n):
        w, x, y, z = Q[k]
        nn = w*w + x*x + y*y + z*z
        M = np.array([[w*w+x*x-y*y-z*z, 2*(x*y-w*z),     2*(x*z+w*y)],
                      [2*(x*y+w*z),     w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                      [2*(x*z-w*y),     2*(y*z+w*x),     w*w-x*x-y*y+z*z]]) / nn
        F[k] = M.T                      # rows = FACE NORMALS (the columns of the rotation)

    normals = F.reshape(-1, 3)                       # 3n rows
    owner = np.repeat(np.arange(n), 3)
    planes = np.concatenate([normals, -normals])     # 6n, with signs
    powner = np.concatenate([owner, owner])

    idx = np.array(list(itertools.combinations(range(len(planes)), 3)), dtype=int)
    keep = (powner[idx[:, 0]] != powner[idx[:, 1]]) | \
           (powner[idx[:, 0]] != powner[idx[:, 2]]) | \
           (powner[idx[:, 1]] != powner[idx[:, 2]])
    idx = idx[keep]
    A = planes[idx]                                   # (T,3,3)
    det = np.linalg.det(A)
    good = np.abs(det) > tol
    skipped = int((~good).sum())
    A = A[good]; det = det[good]
    rhs = np.ones((A.shape[0], 3, 1))
    try:
        pts = np.linalg.solve(A, rhs)[:, :, 0]
    except np.linalg.LinAlgError:
        return None, skipped, 0.0

    keyed = np.round(pts / (tol * 100)).astype(np.int64)
    _, uniq = np.unique(keyed, axis=0, return_index=True)
    P = pts[uniq]

    H = P @ normals.T                                 # (P, 3n)
    absH = np.abs(H)
    on = np.abs(absH - 1.0) < tol
    outside = absH > 1.0 + tol
    onc = on.reshape(len(P), n, 3).sum(axis=2)
    outc = outside.reshape(len(P), n, 3).any(axis=2)

    off = absH[~on]
    margin = float(np.min(np.abs(off - 1.0))) if off.size else 1.0

    sig = {}
    for r in range(len(P)):
        s = tuple(sorted(int(onc[r, k]) for k in range(n)
                         if not outc[r, k] and onc[r, k] > 0))
        if len(s) >= 2 and sum(s) >= 3:
            sig[s] = sig.get(s, 0) + 1
    return sig, skipped, margin


def gate():
    import mpmath as mp
    import n3_arc as N3
    import wall_keys as WK
    import sympy as sp
    mp.mp.dps = 45
    cases = [('n=3 67 Q(sqrt2)',
              [tuple(float(sp.N(sp.Integer(a) + sp.Integer(b) * sp.sqrt(2), 40))
                     for (a, b) in q) for q in WK.Q67[2]]),
             ('n=3 67 Q(sqrt5)',
              [tuple(float(sp.N(sp.Integer(a) + sp.Integer(b) * sp.sqrt(5), 40))
                     for (a, b) in q) for q in WK.Q67[5]]),
             ('n=4 RECORD 183', [tuple(float(t) for t in q) for q in WK.REC[4]])]
    import time
    ok = True
    for name, qs in cases:
        t = time.time(); fast, fskip, fmar = census(qs); tf = time.time() - t
        t = time.time()
        slow, sskip = N3.census_n(mp, [tuple(mp.mpf(t2) for t2 in q) for q in qs],
                                  tol_exp=12)
        ts = time.time() - t
        same = (fast == slow)
        ok = ok and same
        print('   %-18s fast %7.3f s   exact %7.2f s   speedup %5.0fx   %s'
              % (name, tf, ts, ts / max(tf, 1e-6), 'MATCH' if same else 'DIFFER'))
        if not same:
            print('      fast  %s' % dict(sorted(fast.items())))
            print('      exact %s' % dict(sorted(slow.items())))
        else:
            print('      %s   margin %.4g' % (dict(sorted(fast.items())), fmar))
    print('\n   GATE %s' % ('PASS' if ok else 'FAIL — do not use the fast census'))
    return ok


if __name__ == '__main__':
    gate()
