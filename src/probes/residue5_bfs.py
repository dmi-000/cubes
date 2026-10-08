#!/usr/bin/env python3
"""Every face of a placement's arrangement, found by walking it with an exact LP.  [P440]

The per-vertex slack of H1′ depends on the circle configuration only through the ORDER TYPE: the
cyclic order, with ties, of the critical directions (points, antipodes, bisectors and their
antipodes). Every distance comparison at a critical direction or a midpoint is a comparison of a
critical direction with a bisector. Each order type is a face of the arrangement of the conditions
"two critical directions coincide". The 3-parameter patterns of [P439] have too many planes for
cell sampling (≈ 9 M triple intersections). They have few faces, though: ≈ 350 cells were seen by
random sampling.

**The walk.**
- Label 0 sits at 0, which fixes the rotation. A face is the sequence, in [0, 360), of blocks of
  critical forms that are equal there. Each form carries the wrap integer at its witness.
- Neighbours of a cell: for each adjacent pair of blocks, including the pair across 360, the tie
  face; from the tie, the swapped cell.
- Lower faces: merge adjacent blocks of any face.
- **Feasibility is an exact LP.** Ties are eliminated by exact Gaussian elimination. Then
  maximise the margin s of the strict inequalities, with θ in [120, 180] and the offsets free, by
  a two-phase simplex over Fractions (Bland's rule). The face is feasible iff the maximum is
  > 0, and the optimum is an exact witness.
- The graph of cells and facets of an arrangement over a convex domain is connected, so the walk
  reaches every cell. Every lower face lies in some cell's closure and is reached by successive
  merges.

**Evaluation.** At each face's witness, the FULL slack (h1_shared_local.slack2) for every c, or
'unrealisable_merge' when two cubes would co-own two points.

**Control** (`--control`): on the patterns with at most 2 parameters, the walk's order types must
include every order type found by [P439]'s cell sampler, and the slacks must agree.

Output: data/residue5_bfs.json (data/residue5_bfs_control.json for the control).

**Restartable.** The unit of work is one (pattern, placement). Each finished unit is written to
data/residue5_bfs_units/ and never redone; an unfinished walk pickles its state to
data/residue5_bfs_ckpt/ every CKPT_EVERY seconds and resumes from it. Kill and relaunch freely.
`--workers N` sets the pool size (default 6, for an 8-core machine shared with other work).
"""
import os, sys, json, pickle, zlib, itertools, collections, time, multiprocessing as mp
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ.setdefault(_v, '1')    # one thread per pool worker: the pool is the parallelism
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import residue5_patterns as RP
import residue5_exact as RX
import residue_exact as RE

ROOT = os.path.dirname(os.path.dirname(HERE))
RP.UMAX = 3


# ---------------------------------------------------------------- exact LP

def simplex_max(c, A, b):
    """maximise c·y s.t. A y <= b, y >= 0 (two-phase, Bland). Returns (value, y) or None if
    infeasible. Unbounded is not expected here (the margin is capped)."""
    m, n = len(A), len(c)
    # phase 1: rows with b < 0 get an artificial variable
    rows = []
    for i in range(m):
        if b[i] >= 0:
            rows.append(([Fr(v) for v in A[i]], Fr(b[i]), 1))
        else:
            rows.append(([-Fr(v) for v in A[i]], -Fr(b[i]), -1))
    # tableau columns: y (n), slack per row (m), artificial per negative row
    art = [i for i, r in enumerate(rows) if r[2] == -1]
    N = n + m + len(art)
    T = []
    basis = []
    for i, (a, bi, sg) in enumerate(rows):
        row = a + [Fr(0)] * (m + len(art)) + [bi]
        row[n + i] = Fr(sg)                     # slack (+1) or surplus (−1)
        if sg == -1:
            k = art.index(i)
            row[n + m + k] = Fr(1)
            basis.append(n + m + k)
        else:
            basis.append(n + i)
        T.append(row)

    def pivot(r, col):
        pv = T[r][col]
        T[r] = [v / pv for v in T[r]]
        for i in range(len(T)):
            if i != r and T[i][col] != 0:
                f = T[i][col]
                T[i] = [vi - f * vr for vi, vr in zip(T[i], T[r])]
        basis[r] = col

    def run(obj, allowed):
        while True:
            # reduced costs: obj − cB B^{-1} A
            rc = []
            for j in range(N):
                if j not in allowed:
                    rc.append(Fr(0)); continue
                z = sum(obj[basis[i]] * T[i][j] for i in range(len(T)))
                rc.append(obj[j] - z)
            enter = next((j for j in range(N) if rc[j] > 0 and j in allowed), None)
            if enter is None:
                return True
            best, r = None, None
            for i in range(len(T)):
                if T[i][enter] > 0:
                    q = T[i][-1] / T[i][enter]
                    if best is None or q < best or (q == best and basis[i] < basis[r]):
                        best, r = q, i
            if r is None:
                return False                    # unbounded
            pivot(r, enter)

    if art:
        obj1 = [Fr(0)] * N
        for k in range(len(art)):
            obj1[n + m + k] = Fr(-1)
        run(obj1, set(range(N)))
        if sum(T[i][-1] for i in range(len(T)) if basis[i] >= n + m) > 0:
            return None
        # drive artificials out of the basis where possible
        for i in range(len(T)):
            if basis[i] >= n + m:
                col = next((j for j in range(n + m) if T[i][j] != 0), None)
                if col is not None:
                    pivot(i, col)
    obj2 = [Fr(v) for v in c] + [Fr(0)] * (m + len(art))
    if not run(obj2, set(range(n + m))):
        return None
    y = [Fr(0)] * n
    for i, bcol in enumerate(basis):
        if bcol < n:
            y[bcol] = T[i][-1]
    return sum(cv * yv for cv, yv in zip(c, y)), y


# ---------------------------------------------------------------- certified LP
#
# The LPs have at most 4 variables (≤ 3 free parameters and the margin s). HiGHS solves each in
# floating point; the result is then CERTIFIED exactly: take D = #variables rows that are tight
# at the float optimum, solve them exactly as a vertex z_B, and check (i) every row holds at z_B
# (primal feasibility) and (ii) the multipliers y_B with A_B^T y_B = c are >= 0 (dual feasibility).
# Together they prove that c·z_B is the exact optimum, by weak duality, whatever the float
# answer was. When no candidate basis certifies (or HiGHS reports infeasible) the exact simplex
# decides instead, so floating point can make the walk slower but never wrong. Infeasibility is
# certified the same way, through an auxiliary LP whose certified optimum is negative.

LPSTAT = collections.Counter()      # 'cert' / 'fallback' per call, reported per unit
# RESIDUE5_LPCHECK=1: also run the exact simplex on every LP and require the same value (an
# environment variable, because pool workers are spawned and do not inherit module globals)
LP_CHECK = os.environ.get('RESIDUE5_LPCHECK') == '1'
LP_CHECK_EVERY = 8                  # --control cross-checks every 8th unit (it costs the exact simplex)
LP_CHECK_MAX = 2000                 # ... on its first 2000 LPs only: the exact simplex is ~10x slower
LP_CHECKED = [0]                    # LPs cross-checked in the current unit


def _solve_exact(M, r):
    """M z = r for square Fraction M; None if singular"""
    D = len(M)
    T = [list(M[i]) + [r[i]] for i in range(D)]
    for col in range(D):
        piv = next((i for i in range(col, D) if T[i][col] != 0), None)
        if piv is None:
            return None
        T[col], T[piv] = T[piv], T[col]
        pv = T[col][col]
        T[col] = [v / pv for v in T[col]]
        for i in range(D):
            if i != col and T[i][col] != 0:
                f = T[i][col]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[col])]
    return [T[i][D] for i in range(D)]


def _solve_any(M, r, n):
    """some solution of M z = r (k equations, n unknowns, free unknowns set to 0) or None if
    inconsistent; exact"""
    T = [list(M[i]) + [r[i]] for i in range(len(M))]
    piv_cols, row = [], 0
    for col in range(n):
        p = next((i for i in range(row, len(T)) if T[i][col] != 0), None)
        if p is None:
            continue
        T[row], T[p] = T[p], T[row]
        pv = T[row][col]
        T[row] = [v / pv for v in T[row]]
        for i in range(len(T)):
            if i != row and T[i][col] != 0:
                f = T[i][col]
                T[i] = [a - f * bb for a, bb in zip(T[i], T[row])]
        piv_cols.append(col); row += 1
    if any(T[i][n] != 0 for i in range(row, len(T))):
        return None
    z = [Fr(0)] * n
    for i, col in enumerate(piv_cols):
        z[col] = T[i][n]
    return z


def lp_cert(c, A, b):
    """max c·z s.t. A z <= b, z free (the rows must bound the region).  Returns (value, z) exactly
    certified, or None when the float guess did not certify.

    Certificate = exact y >= 0 with A^T y = c and exact feasible z with c·z = b·y (weak duality
    then makes c·z the optimum).  The optimum need not be a vertex here (max s = 1 is attained on
    a whole region), so z is built from the dual's support rows as equalities, completed by the
    float coordinates rounded to rationals; a vertex basis among the tight rows is tried last."""
    from scipy.optimize import linprog
    D, m = len(c), len(A)
    r = linprog([-float(v) for v in c], A_ub=[[float(v) for v in row] for row in A], b_ub=[float(v) for v in b],
                bounds=[(None, None)] * D, method='highs')
    if r.status != 0:
        return None
    z = r.x
    slack = [float(b[i]) - sum(float(A[i][k]) * z[k] for k in range(D)) for i in range(m)]
    duals = [-float(v) for v in r.ineqlin.marginals]
    S = [i for i in range(m) if duals[i] > 1e-9]

    def check(zz, yS, Sset):
        if zz is None or any(sum(A[i][k] * zz[k] for k in range(D)) > b[i] for i in range(m)):
            return None
        val = sum(c[k] * zz[k] for k in range(D))
        if val != sum(yS[q] * b[i] for q, i in enumerate(Sset)):
            return None
        return val, zz

    # dual: A_S^T y = c, y >= 0
    yS = _solve_any([[A[i][k] for i in S] for k in range(D)], list(c), len(S)) if S else (
        [] if not any(c) else None)
    if yS is not None and all(v >= 0 for v in yS):
        for den in (10 ** 6, 10 ** 9):
            eqM = [A[i] for i in S]
            eqr = [b[i] for i in S]
            for k in range(D):
                e = [Fr(0)] * D; e[k] = Fr(1)
                eqM.append(e); eqr.append(Fr(z[k]).limit_denominator(den))
            # keep only the coordinate equations that the support rows leave free
            zz = None
            base = _solve_any([A[i] for i in S], [b[i] for i in S], D) if S else [Fr(0)] * D
            if base is not None:
                rows, rr = [A[i] for i in S], [b[i] for i in S]
                for k in range(D):
                    e = [Fr(0)] * D; e[k] = Fr(1)
                    trial = _solve_any(rows + [e], rr + [Fr(z[k]).limit_denominator(den)], D)
                    if trial is not None:
                        rows.append(e); rr.append(Fr(z[k]).limit_denominator(den))
                zz = _solve_any(rows, rr, D)
            out = check(zz, yS, S)
            if out is not None:
                return out
    # last resort: vertex bases among the tightest rows
    order = sorted(range(m), key=lambda i: (duals[i] <= 1e-9, slack[i]))
    for B in itertools.combinations(order[:D + 4], D):
        AB = [A[i] for i in B]
        zB = _solve_exact(AB, [b[i] for i in B])
        if zB is None:
            continue
        yB = _solve_exact([[AB[i][k] for i in range(D)] for k in range(D)], list(c))
        if yB is None or any(v < 0 for v in yB):
            continue
        out = check(zB, yB, list(B))
        if out is not None:
            return out
    return None


def lp_max(c, A, b, F):
    """the LP of feasible(): z = (x_1..x_F, s) with rows A z <= b.  Returns (value, z) or None if
    infeasible, exactly.  The exact simplex runs on the split form x = y+ − y− only when the
    certificate fails."""
    check = LP_CHECK and LP_CHECKED[0] < LP_CHECK_MAX
    if check:
        LP_CHECKED[0] += 1
    res = lp_cert(c, A, b)
    if res is not None and not check:
        LPSTAT['cert'] += 1
        return res
    infeasible = False
    if res is None:
        # infeasibility, certified: max −u s.t. A z − u <= b is always feasible and bounded (the
        # rows 0 <= s <= 1 give u >= −1/2); its exact optimum is < 0 iff A z <= b has no solution
        aux = lp_cert([Fr(0)] * len(c) + [Fr(-1)], [row + [Fr(-1)] for row in A], b)
        infeasible = aux is not None and aux[0] < 0
        if infeasible and not check:
            LPSTAT['cert_infeasible'] += 1
            return None
    As = [row[:F] + [-v for v in row[:F]] + row[F:] for row in A]
    cs = list(c[:F]) + [-v for v in c[:F]] + list(c[F:])
    ex = simplex_max(cs, As, b)
    exz = None if ex is None else (ex[0], [ex[1][k] - ex[1][F + k] for k in range(F)] + ex[1][2 * F:])
    if infeasible:
        LPSTAT['cert_infeasible'] += 1
        if exz is not None:
            raise AssertionError('certified infeasible, exact simplex found %s' % (exz[0],))
        return None
    if res is None:
        LPSTAT['fallback'] += 1
        return exz
    LPSTAT['cert'] += 1
    if (exz is None) or exz[0] != res[0]:
        raise AssertionError('certified LP value %s != exact simplex %s' % (res[0], exz and exz[0]))
    return res


# ---------------------------------------------------------------- faces

def lin(f, params):
    return [f.get(p, Fr(0)) for p in params], f.get('1', Fr(0))


def feasible(cf, params, blocks, ks, weak=False, objective=None):
    """blocks: list of tuples of form indices in increasing order on [0, 360); ks: wrap per form.
    g_i(x) = f_i(x) − 360 k_i. Ties within blocks; strict increase between blocks; first block's
    value >= 0, last < 360 (the 0-block, holding the constant-0 form, is pinned first).
    Returns a witness {param: value} or None."""
    P = len(params)
    G = []
    for i in range(len(cf)):
        a, c0 = lin(cf[i], params)
        G.append((a, c0 - 360 * ks[i]))
    # equalities: g_i = g_j within blocks -> eliminate variables exactly
    eqs = []
    for blk in blocks:
        for i, j in zip(blk, blk[1:]):
            a = [x - y for x, y in zip(G[i][0], G[j][0])]
            eqs.append((a, G[j][1] - G[i][1]))          # a·x = rhs
    # Gaussian elimination: express pivot vars in terms of free ones
    sub = {}                                            # var index -> (coeffs over vars, const)
    rowsE = [(list(a), r) for a, r in eqs]
    free = list(range(P))
    for a, r in rowsE:
        # apply existing substitutions
        a2, r2 = [Fr(0)] * P, r
        for v in range(P):
            if a[v] == 0:
                continue
            if v in sub:
                ca, cc = sub[v]
                for w in range(P):
                    a2[w] += a[v] * ca[w]
                r2 -= a[v] * cc
            else:
                a2[v] += a[v]
        piv = next((v for v in range(P) if a2[v] != 0), None)
        if piv is None:
            if r2 != 0:
                return None
            continue
        # x_piv = (r2 − Σ_{w≠piv} a2[w] x_w) / a2[piv]
        ca = [Fr(0)] * P
        for w in range(P):
            if w != piv:
                ca[w] = -a2[w] / a2[piv]
        cc = r2 / a2[piv]
        for v in list(sub):
            sa, sc = sub[v]
            if sa[piv] != 0:
                k = sa[piv]
                sub[v] = ([sa[w] + k * ca[w] if w != piv else Fr(0) for w in range(P)], sc + k * cc)
        sub[piv] = (ca, cc)
    freev = [v for v in range(P) if v not in sub]

    def expr(a, c0):
        """a·x + c0 in terms of free vars: (coeffs over freev, const)"""
        out = {v: Fr(0) for v in freev}
        const = c0
        for v in range(P):
            if a[v] == 0:
                continue
            if v in sub:
                ca, cc = sub[v]
                for w in freev:
                    out[w] += a[v] * ca[w]
                const += a[v] * cc
            else:
                out[v] += a[v]
        return [out[w] for w in freev], const
    # inequalities h(x) >= s (strict ones) or >= 0 (domain); written as −h + s <= 0
    strict, weakc = [], []
    reps = [blk[0] for blk in blocks]
    bnd = []                                                         # boundary j: block j | j+1; last: wrap
    for i, j in zip(reps, reps[1:]):
        a = [x - y for x, y in zip(G[j][0], G[i][0])]
        bnd.append(expr(a, G[j][1] - G[i][1]))
    first, last = reps[0], reps[-1]
    weakc.append(expr(G[first][0], G[first][1]))                    # g_first >= 0
    bnd.append(expr([-x for x in G[last][0]], 360 - G[last][1]))     # 360 − g_last > 0
    if weak:
        weakc += bnd
    else:
        strict += bnd
    if 't' in params:
        ti = params.index('t')
        e = [Fr(0)] * P; e[ti] = Fr(1)
        weakc.append(expr(e, Fr(-120)))                             # θ − 120 >= 0
        e2 = [Fr(0)] * P; e2[ti] = Fr(-1)
        weakc.append(expr(e2, Fr(180)))                             # 180 − θ >= 0
    # variables z = (free vars, s): s in [0, 1]; the free vars boxed to |x| <= 10^4 (offsets are
    # periodic, so the box is ample) to keep every LP bounded
    F = len(freev)
    A, b = [], []
    for (a, c0), isstrict in [(x, True) for x in strict] + [(x, False) for x in weakc]:
        # −(a·x + c0) + s <= 0  (strict),  −(a·x + c0) <= 0 (weak)
        A.append([-v for v in a] + [Fr(1) if isstrict else Fr(0)]); b.append(c0)
    A.append([Fr(0)] * F + [Fr(1)]); b.append(Fr(1))
    A.append([Fr(0)] * F + [Fr(-1)]); b.append(Fr(0))
    for k in range(F):
        for sg in (1, -1):
            r = [Fr(0)] * (F + 1); r[k] = Fr(sg)
            A.append(r); b.append(Fr(10 ** 4))
    if objective is not None:
        oa, oc = bnd[objective]
        res = lp_max(list(oa) + [Fr(0)], A, b, F)
        if res is None:
            return None
        return res[0] + oc                                           # max of that boundary's gap
    res = lp_max([Fr(0)] * F + [Fr(1)], A, b, F)
    if res is None or res[0] <= 0:
        return None
    z = res[1]
    xs = {freev[k]: z[k] for k in range(F)}
    vals = {}
    for v in range(P):
        if v in sub:
            ca, cc = sub[v]
            vals[v] = cc + sum(ca[w] * xs[w] for w in freev)
        else:
            vals[v] = xs[v]
    return {params[v]: vals[v] for v in range(P)}


def face_of(cf, vals):
    """blocks and wraps at a parameter point"""
    v = [RE.evalf(dict(f), vals) for f in cf]
    ks = [int((x // 360)) for x in v]
    m = [x - 360 * k for x, k in zip(v, ks)]
    order = sorted(set(m))
    blocks = [tuple(i for i in range(len(cf)) if m[i] == val) for val in order]
    return blocks, ks


def key(blocks):
    return tuple(tuple(sorted(b)) for b in blocks)


def merge(blocks, ks, j):
    """merge boundary j (block j with j+1; j = len−1 is the wrap: last block into the 0-block)"""
    nb = len(blocks)
    if j < nb - 1:
        return blocks[:j] + [tuple(blocks[j] + blocks[j + 1])] + blocks[j + 2:], ks
    up = list(ks)
    for i in blocks[-1]:
        up[i] += 1
    return [tuple(blocks[0] + blocks[-1])] + blocks[1:-1], up


def float_forced(cf, params, bl, kk):
    """GUESS (floating point, HiGHS) the boundaries that cannot be strict on the face (blocks bl,
    wraps kk). Every guess is confirmed exactly by the caller; a wrong guess only costs time."""
    import numpy as np
    from scipy.optimize import linprog
    P = len(params)
    G = [([float(cf[i].get(p_, 0)) for p_ in params], float(cf[i].get('1', 0)) - 360 * kk[i]) for i in range(len(cf))]
    reps = [b_[0] for b_ in bl]
    bnd = []
    for i, j in zip(reps, reps[1:]):
        bnd.append(([x - y for x, y in zip(G[j][0], G[i][0])], G[j][1] - G[i][1]))
    bnd.append(([-x for x in G[reps[-1]][0]], 360 - G[reps[-1]][1]))
    nq = len(bnd)
    nv = P + nq
    Aeq, beq = [], []
    for blk in bl:
        for i, j in zip(blk, blk[1:]):
            Aeq.append([G[i][0][k] - G[j][0][k] for k in range(P)] + [0] * nq)
            beq.append(G[j][1] - G[i][1])
    Aub, bub = [], []
    first = reps[0]
    Aub.append([-v for v in G[first][0]] + [0] * nq); bub.append(G[first][1])       # g_first >= 0
    bounds = []
    for p_ in params:
        bounds.append((120, 180) if p_ == 't' else (-1e4, 1e4))
    active = set(range(nq))
    forced = set()
    for _ in range(6):
        A2, b2 = list(Aub), list(bub)
        for q, (a, c0) in enumerate(bnd):
            row = [-v for v in a] + [0] * nq
            if q in active:
                row[P + q] = 1.0                       # −(a·x + c0) + s_q <= 0
            A2.append(row); b2.append(c0)
        cvec = [0] * P + [-1.0 if q in active else 0 for q in range(nq)]
        bd = bounds + [(0, 1) if q in active else (0, 0) for q in range(nq)]
        r = linprog(cvec, A_ub=A2, b_ub=b2, A_eq=Aeq or None, b_eq=beq or None, bounds=bd, method='highs')
        if r.status != 0:
            return None
        sv = r.x[P:]
        newly = {q for q in active if sv[q] > 1e-9}
        if not newly:
            forced = set(active)
            break
        active -= newly
        if not active:
            forced = set()
            break
    return forced


def closure_face(cf, params, blocks, ks, j):
    """the face of the closure of (blocks, ks) where boundary j ties, with every tie that forces:
    returns (blocks, ks, witness) or None"""
    bl, kk = merge(blocks, ks, j)
    w = feasible(cf, params, bl, kk)
    if w is not None:
        return bl, kk, w
    # fast path: guess the forced set in floating point, confirm each member exactly
    guess = float_forced(cf, params, bl, kk)
    if guess:
        ok = all(feasible(cf, params, bl, kk, weak=True, objective=q) == 0 for q in guess)
        if ok:
            b2, k2 = bl, kk
            # merge from the highest boundary index down so indices stay valid (wrap = last)
            for q in sorted(guess, reverse=True):
                b2, k2 = merge(b2, k2, q if q < len(b2) else len(b2) - 1)
            w = feasible(cf, params, b2, k2)
            if w is not None:
                return b2, k2, w
    while True:
        w = feasible(cf, params, bl, kk)
        if w is not None:
            return bl, kk, w
        forced = None
        for q in range(len(bl)):
            m = feasible(cf, params, bl, kk, weak=True, objective=q)
            if m is None:
                return None                                         # empty even weakly
            if m == 0:
                forced = q
                break
        if forced is None:
            return None
        bl, kk = merge(bl, kk, forced)


GENERIC = [(Fr(1), Fr(1, 7), Fr(1, 53)), (Fr(1, 11), Fr(1), Fr(1, 3)), (Fr(1, 5), Fr(1, 17), Fr(1))]


def perturbed_face(cf, params, w, dirs):
    """the order type at w + ε d1 + ε² d2 + ..., exactly (lexicographic)"""
    keys = []
    for f in cf:
        v = RE.evalf(dict(f), w)
        lins = [sum(f.get(p, Fr(0)) * d[i] for i, p in enumerate(params)) for d in dirs]
        k = v // 360
        r = v - 360 * k
        if r == 0:
            first = next((x for x in lins if x != 0), 0)
            if first < 0:
                k -= 1; r = Fr(360)
        keys.append(((r,) + tuple(lins), int(k)))
    order = sorted(set(kk[0] for kk in keys))
    blocks = [tuple(i for i in range(len(cf)) if keys[i][0] == o) for o in order]
    ks = [kk[1] for kk in keys]
    # the 0-block (constant-0 forms) must come first; values r = 360 sort last, as wanted
    return blocks, ks


CKPT_EVERY = 120          # seconds between walk checkpoints


def _save(path, state):
    tmp = path + '.tmp'
    with open(tmp, 'wb') as fh:
        pickle.dump(state, fh)
    os.replace(tmp, path)                                           # atomic: a kill never leaves half a file


def walk(forms, params, ckpt=None, label=''):
    """every face of the arrangement: {key: exact witness}.  With `ckpt` (a file path) the state
    is pickled every CKPT_EVERY seconds and a later call resumes from it; the result does not depend
    on where it was interrupted, because both phases are worklists over a set of visited keys."""
    cfn = RE.crit_forms(forms)
    cf = [dict(f) for f in cfn]
    P = len(params)
    gens = [tuple(g[:P]) for g in GENERIC][:P]
    if ckpt and os.path.exists(ckpt):
        with open(ckpt, 'rb') as fh:
            st = pickle.load(fh)
    else:
        start = {p: (Fr(151, 1) + Fr(1, 7) if p == 't' else Fr(37 + 11 * i, 1) + Fr(1, 13)) for i, p in enumerate(params)}
        b0, k0 = face_of(cf, start)
        st = {'phase': 1, 'cells': {}, 'faces': {}, 'todo': [(b0, k0)], 'stack': None, 'done': set(),
              'closure': {}, 'nlp': 0, 'secs': 0.0}
    cells, faces, closure = st['cells'], st['faces'], st['closure']
    t_last = t_start = time.time()
    secs0 = st['secs']

    def tick():
        nonlocal t_last
        if ckpt and time.time() - t_last > CKPT_EVERY:
            st['secs'] = secs0 + time.time() - t_start
            _save(ckpt, st)
            t_last = time.time()
            if label:
                print('  [%s] phase %d: cells %d, faces %d, queue %d, LPs %d, %.0f s'
                      % (label, st['phase'], len(cells), len(faces),
                         len(st['todo']) if st['phase'] == 1 else len(st['stack']), st['nlp'], st['secs']), flush=True)

    def closed(blocks, ks, kb, j):
        # closure faces are shared by both phases: phase 2 starts from the cells phase 1 visited
        if (kb, j) not in closure:
            closure[(kb, j)] = closure_face(cf, params, blocks, ks, j); st['nlp'] += 1
        return closure[(kb, j)]

    # tick() runs only between items: a cell is entered in `cells` before its boundaries are
    # explored, so a checkpoint taken mid-item would make a resumed walk skip those boundaries.
    while st['phase'] == 1 and st['todo']:
        tick()
        blocks, ks = st['todo'].pop()
        kc = key(blocks)
        if kc in cells:
            continue
        w = feasible(cf, params, blocks, ks); st['nlp'] += 1
        if w is None:
            continue
        cells[kc] = (blocks, ks, w)
        faces[kc] = w
        for j in range(len(blocks)):
            r = closed(blocks, ks, kc, j)
            if r is None:
                continue
            fb, fk, fw = r
            faces.setdefault(key(fb), fw)
            # step across: −gradient of boundary j's gap, then generic directions
            if j < len(blocks) - 1:
                a_i, a_j = cf[blocks[j][0]], cf[blocks[j + 1][0]]
            else:
                a_i, a_j = cf[blocks[-1][0]], cf[blocks[0][0]]
            n = tuple(a_i.get(p, Fr(0)) - a_j.get(p, Fr(0)) for p in params)
            if not any(n):
                continue
            nb, nk = perturbed_face(cf, params, fw, [n] + gens)
            st['todo'].append((nb, nk))
    # lower faces: from every cell, recursively impose one more boundary tie (with forced ties)
    if st['phase'] == 1:
        st['phase'] = 2
        st['stack'] = [(b, k) for b, k, w in cells.values()]
    done = st['done']
    while st['stack']:
        tick()
        blocks, ks = st['stack'].pop()
        kb = key(blocks)
        if kb in done:
            continue
        done.add(kb)
        for j in range(len(blocks)):
            r = closed(blocks, ks, kb, j)
            if r is None:
                continue
            fb, fk, fw = r
            kf = key(fb)
            if kf not in faces:
                faces[kf] = fw
            if kf not in done:
                st['stack'].append((fb, fk))
    return cf, faces, st['nlp']


def point_check(cf, params, seen, rnd, n_each=300):
    """completeness check of a walk at exact rational points: random points of the domain, and
    random points ON one, two and three coincidence planes (where lower faces live).  Every order
    type met must be a walk face.  Returns {stratum: (points, missed)} and up to 5 missed points.
    A sampled check is a lower bound on what the walk missed, never a proof of completeness."""
    P = len(params)

    def rand_val(p):
        if p == 't':
            return Fr(120) + Fr(rnd.randrange(0, 60 * 997), 997)
        return Fr(rnd.randrange(0, 360 * 991), 991)

    def in_dom(v):
        return all(120 <= v[p] <= 180 for p in params if p == 't')

    diffs = []
    for i in range(len(cf)):
        for j in range(i + 1, len(cf)):
            a = [cf[i].get(p, Fr(0)) - cf[j].get(p, Fr(0)) for p in params]
            if any(a):
                diffs.append((a, cf[i].get('1', Fr(0)) - cf[j].get('1', Fr(0))))
    out, bad = {}, []
    for q in range(0, min(P, 3) + 1):            # number of planes imposed
        tot = miss = 0
        tries = 0
        while tot < n_each and tries < 20 * n_each:
            tries += 1
            v = {p: rand_val(p) for p in params}
            if q:
                pl = rnd.sample(diffs, q)
                # solve the q planes a·x + c = 360 k for q of the parameters, the rest fixed at v
                solve_for = rnd.sample(range(P), q)
                ks = [rnd.randrange(-3, 4) for _ in range(q)]
                M = [[a[w] for w in solve_for] for a, c in pl]
                rhs = [360 * k - c - sum(a[w] * v[params[w]] for w in range(P) if w not in solve_for)
                       for (a, c), k in zip(pl, ks)]
                x = _solve_exact(M, rhs)
                if x is None:
                    continue
                for w, xv in zip(solve_for, x):
                    v[params[w]] = xv
                if not in_dom(v):
                    continue
            tot += 1
            if key(face_of(cf, v)[0]) not in seen:
                miss += 1
                if len(bad) < 5:
                    bad.append({p: str(x) for p, x in v.items()})
        out[q] = (tot, miss)
    return out, bad


UNITS = os.path.join(ROOT, 'data', 'residue5_bfs_units')         # one JSON per finished unit
CKPTS = os.path.join(ROOT, 'data', 'residue5_bfs_ckpt')          # walk state of unfinished units


def unit_name(mode, t, owners, idx):
    return '%s_t%d_%s_p%d' % (mode, t, '-'.join(''.join(map(str, sorted(o))) for o in owners), idx)


def run_unit(args):
    """one (pattern, placement): walk it, evaluate (mode 'main') or compare with the cell sampler
    (mode 'control'), and write the result.  A unit whose result file exists is never redone; an
    interrupted one resumes from its walk checkpoint."""
    global LP_CHECK
    mode, t, owners, idx, *opt = args
    if opt:
        LP_CHECK = opt[0]
    name = unit_name(mode, t, owners, idx)
    out_path = os.path.join(UNITS, name + '.json')
    if os.path.exists(out_path):
        return json.load(open(out_path))
    forms, params = list(RX.placements_forms(t, owners))[idx]
    ck = os.path.join(CKPTS, name + '.pkl')
    t0 = time.time()
    lp0 = dict(LPSTAT)
    LP_CHECKED[0] = 0
    cf, seen, nlp = walk(forms, params, ckpt=ck, label=name)
    out = {'mode': mode, 't': t, 'owners': [sorted(o) for o in owners], 'placement': idx,
           'params': list(params), 'faces': len(seen), 'lps': nlp, 'lp_check': LP_CHECK, 'lp_checked': LP_CHECKED[0],
           'lp_paths': {k: LPSTAT[k] - lp0.get(k, 0) for k in LPSTAT}}
    if mode == 'main':
        import random
        pc, bad = point_check(cf, params, seen, random.Random(zlib.crc32(name.encode())))
        out['point_check'] = {str(q): v for q, v in pc.items()}
        out['point_check_missed'] = bad
        out.update({'min': {}, 'fails': [], 'status': collections.Counter()})
        for k0, w in seen.items():
            r = RX.evaluate(t, owners, forms, w)
            if isinstance(r, str):
                out['status'][r] += 1
                continue
            for c, (s2, an) in r.items():
                out['min'][str(c)] = min(out['min'].get(str(c), 10 ** 9), s2)
                if s2 < 0 and len(out['fails']) < 10:
                    out['fails'].append({'vals': {k: str(v) for k, v in w.items()}, 'c': c, 'twice_slack': s2})
        out['status'] = dict(out['status'])
    else:
        # every order type the cell sampler finds must be a walk face
        miss, tot = 0, 0
        for vals in RX.all_samples(forms, params):
            if 't' in vals and not (120 <= vals['t'] <= 180):
                continue
            tot += 1
            if key(face_of(cf, vals)[0]) not in seen:
                miss += 1
        out.update({'sampler_points': tot, 'missed': miss})
    out['secs'] = round(time.time() - t0, 1)
    tmp = out_path + '.tmp'
    json.dump(out, open(tmp, 'w'), indent=1, default=str)
    os.replace(tmp, out_path)
    if os.path.exists(ck):
        os.remove(ck)
    return out


def main():
    os.makedirs(UNITS, exist_ok=True); os.makedirs(CKPTS, exist_ok=True)
    nw = int(sys.argv[sys.argv.index('--workers') + 1]) if '--workers' in sys.argv else 6
    pats = [(t, o) for t in range(3, 6) for o, u in RP.patterns(t)]
    pl = {(t, str(o)): [len(p) for f, p in RX.placements_forms(t, o)] for t, o in pats}
    if '--control' in sys.argv:
        mode = 'control'
        sel = [(t, o) for t, o in pats if pl[(t, str(o))] and 1 <= max(pl[(t, str(o))]) <= 2]
        a = sys.argv[sys.argv.index('--control') + 1:]
        k = int(a[0]) if a and a[0].isdigit() else len(sel)
        sel = sel[::max(1, len(sel) // k)][:k]
        units = [(mode, t, o, i) for t, o in sel for i, d in enumerate(pl[(t, str(o))]) if 1 <= d <= 2]
        units = [u + (n % LP_CHECK_EVERY == 0,) for n, u in enumerate(units)]
    else:
        mode = 'main'
        sel = [(t, o) for t, o in pats if pl[(t, str(o))] and max(pl[(t, str(o))]) == 3]
        units = [(mode, t, o, i) for t, o in sel for i, d in enumerate(pl[(t, str(o))]) if d >= 1]
    have = sum(os.path.exists(os.path.join(UNITS, unit_name(*u[:4]) + '.json')) for u in units)
    print('%s: %d patterns, %d units, %d already done; %d workers' % (mode, len(sel), len(units), have, nw), flush=True)
    t0 = time.time()
    rs = []
    with mp.Pool(nw) as p:
        for r in p.imap_unordered(run_unit, units):
            rs.append(r)
            extra = ('missed %d of %d sampler points' % (r['missed'], r['sampler_points']) if mode == 'control'
                     else 'min 2·slack %s, fails %d, skipped %s, point check (planes: points, missed) %s'
                     % (r['min'], len(r['fails']), r['status'], r['point_check']))
            print('%d/%d %s p%d (%d params): faces %d, LPs %d %s, %s (%.0f s; %.0f s total)'
                  % (len(rs), len(units), r['owners'], r['placement'], len(r['params']), r['faces'], r['lps'],
                     r.get('lp_paths'), extra, r['secs'], time.time() - t0), flush=True)
    if mode == 'control':
        print('control: %d patterns, %d units (%d with up to LP_CHECK_MAX LPs cross-checked against the exact simplex, %d LPs in all); '
              'sampler points %d; points whose order type the walk missed: %d'
              % (len(sel), len(rs), sum(1 for r in rs if r['lp_check']), sum(r.get('lp_checked', sum(r['lp_paths'].values()) if r['lp_check'] else 0) for r in rs),
                 sum(r['sampler_points'] for r in rs),
                 sum(r['missed'] for r in rs)), flush=True)
        for r in rs:
            if r['missed']:
                print('   MISSED', r, flush=True)
    else:
        bad = sorted({str(r['owners']) for r in rs if r['fails']})
        pm = sum(v[1] for r in rs for v in r['point_check'].values())
        print('%d three-parameter patterns, %d units, %d faces; patterns with a negative slack: %d; '
              'point-check points the walk missed: %d' % (len(sel), len(rs), sum(r['faces'] for r in rs), len(bad), pm),
              flush=True)
    json.dump(rs, open(os.path.join(ROOT, 'data', 'residue5_bfs%s.json' % ('_control' if mode == 'control' else '')), 'w'),
              indent=1, default=str)


if __name__ == '__main__':
    main()
