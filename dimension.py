#!/usr/bin/env python3
"""SOLVE for the local dimension of a locus, in the FULL moduli space.

Every dimension figure in this project comes from PROBING -- perturb and see what
survives -- and `FAILURE_MODES.md` 11d shows a zero reading then means "not
aligned", never "isolated".  Worse, every probe moves ONE cube, so a locus that is
positive-dimensional only via directions moving several cubes together is
invisible to all of them.  That is the largest standing gap in
`MAXIMISER_TAXONOMY.md`.

Solving does not have that problem, and for a structural reason: enumerating
multi-cube directions is exponential, computing a NULL SPACE is not.

    local dim = 3(n-1) - rank J,    J = Jacobian of the BINDING conditions.

WHY THE PREVIOUS ATTEMPT FAILED, and what is different here.  `multicube2.py`
treated every concurrence as binding and drove the rank to full.  `tight_set.py`
fixed the principle -- a strict inequality constrains nothing, only equalities
bind -- but still returns null dimension 1 at the n = 6 record where TWO
independent tangents are verified ([Postscript 100](LEDGER.md#p100), [102](LEDGER.md#p102)).  Three changes:

  * TIGHT IS NOT BINDING.  A tight condition binds only if crossing it changes
    the count.  Here every candidate is tested: take a direction in the null
    space of the OTHERS that violates this one, step, and ask the engine.  A
    condition whose crossing changes nothing is dropped.
  * EXACT ARITHMETIC.  `tight_set.py` builds its matrices in floating point and
    then decides EQUALITY with them, which is the failure mode this project has
    logged more than once.  Everything here is Fraction/sympy over Q.
  * THE CONDITION LIST IS BIGGER.  Step A's pair conditions are not the whole
    story: Step B ([Postscript 78](LEDGER.md#p78)) shows the count also depends on SINGLETON terms,
    which are two-rotation quantities -- conditions on TRIPLES (i; j,k), never in
    anyone's Jacobian before.  Both are included.

Every condition has one form: with normals n_t of other cubes expressed in cube
i's frame,

    f = min over the simplex of || sum_t lam_t n_t ||_1  =  1,

size 1 giving Step A's "slab nonempty", size 2 both Step A's "slabs meet" (same
cube) and Step B's 36-cell conditions (different cubes).  At a tight point the
minimiser lam* and the sign pattern are locally constant, so by the ENVELOPE
THEOREM the gradient is the partial derivative of the objective at fixed lam* --
exact, and no subdifferential needed.

STATUS 2026-08-13: **PASSES ITS CONTROLS.**

    n2       dim 1, tangent (1,1,1)      the body-diagonal 13-family
    n2edge   dim 1, tangent (1,1,0)      the edge-axis arc
    arcA     dim 1, recovered as alpha=2 the 727 arc, in FULL 15-dim moduli space
                                         -- the control tight_set.py fails

HOW IT WORKS.  Tight conditions -> exact rational Jacobian -> null space (first
order) -> the walls are QUADRICS, so staying on them is the exact condition
d'Hd = 0 (second order, no differential equation) -> one polynomial per condition
in the direction parameter -> their GCD -> rational roots -> engine verification.

SEVEN APPARATUS FAULTS, ZERO MATHEMATICAL ONES (2026-08-12/13), in order:
  1 differentiation  discarded every condition whose minimiser sits at a
                     breakpoint -- which is where it ALWAYS sits
  2 gauge            re-gauging by conjugation is Moebius in Cayley coordinates,
                     so it curved a straight arc and no tangent could survive
  3 verification     unevaluable scored as "count changed" (FAILURE_MODES' own trap)
  4 candidates       four hand-picked combinations of an arbitrary basis, missing
                     a direction that was inside the span
  5 stale variable   a print referencing a removed name
  6 Hessians         43 200 symbolic second derivatives for 3 numbers per
                     condition; evaluation and interpolation replace all of it
  7 root extraction  handled only degrees 1 and 2, silently skipping the cubics
                     that actually occur -- all 132 vanished at the true root

THE PROBE THAT FOUND IT: express the KNOWN tangent in the computed basis, then
evaluate the machinery's own intermediate objects at that exact point.  Two
minutes to write; it localised fault 7 immediately and would have caught 4 of the
7.  METHODS section 4 says choose a control that is hard for the method; the
addition is that when a known answer exists, test the INTERMEDIATE objects
against it, not only the final output.

    python3 dimension.py <case>      cases: n2, n2edge, all
"""
import itertools
import json
import subprocess
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, '/Users/dmi/cube-compounds')
from solve_ends import q_of

ENG = '/Users/dmi/cube-compounds/cube_regions_n'
ENGW = '/Users/dmi/cube-compounds/cube_regions_q2w'
QZERO = []   # cube 0's frozen quaternion, set per case


def cayley_matrix(c):
    """Rotation matrix as a sympy expression in the 3 Cayley coordinates c."""
    x, y, z = c
    N = 1 + x * x + y * y + z * z
    M = sp.Matrix([[1 + x * x - y * y - z * z, 2 * (x * y - z), 2 * (x * z + y)],
                   [2 * (x * y + z), 1 - x * x + y * y - z * z, 2 * (y * z - x)],
                   [2 * (x * z - y), 2 * (y * z + x), 1 - x * x - y * y + z * z]])
    return M / N


def frames(vars_, q0=None):
    """Cube 0 is FROZEN at its actual world rotation; cubes 1.. are the variables.

    The gauge must not be fixed by conjugating the configuration to put cube 0 at
    the identity: that map is Moebius in Cayley coordinates, not affine, so it
    turns a straight maximiser arc into a curve and every tangent then fails
    verification by stepping (measured on arc A, 2026-08-12).  Freezing cube 0
    where it is selects one representative per global-rotation orbit just as
    well, and keeps the world-frame straightness that line-solving relies on."""
    R0 = sp.eye(3) if q0 is None else sp.Matrix(
        [[sp.Rational(x.numerator, x.denominator) for x in row]
         for row in _mat0(q0)])
    Rs = [R0]
    for k in range(0, len(vars_), 3):
        Rs.append(cayley_matrix(vars_[k:k + 3]))
    return Rs


def _mat0(q):
    from step_a2 import mat
    return mat(q)


def normals_sym(Rs, i, j):
    """Face normals of cube j in cube i's frame: columns of R_i^T R_j."""
    A = Rs[i].T * Rs[j]
    return [list(A[:, k]) for k in range(3)]


def l1_signs(v):
    return [1 if t > 0 else (-1 if t < 0 else 0) for t in v]


def min_l1_argmin(N):
    """(value, lam*) for min over conv(N) of ||v||_1, exactly (adapted from
    step_b.min_l1_hull, which returns only the value)."""
    r = len(N)
    best = None
    for size in range(1, r + 1):
        for S in itertools.combinations(range(r), size):
            for A in itertools.combinations(range(3), size - 1):
                rows = [[F(1)] * size + [F(1)]]
                for k in A:
                    rows.append([N[i][k] for i in S] + [F(0)])
                lam = _solve(rows)
                if lam is None or any(x < 0 for x in lam):
                    continue
                v = [sum(lam[t] * N[S[t]][k] for t in range(size))
                     for k in range(3)]
                val = sum(abs(t) for t in v)
                if best is None or val < best[0]:
                    full = [F(0)] * r
                    for t, idx in enumerate(S):
                        full[idx] = lam[t]
                    best = (val, full, v)
    return best


def _solve(rows):
    """exact solve of a small linear system given as [coeffs..., rhs]"""
    import copy
    A = [r[:] for r in rows]
    nvar = len(A[0]) - 1
    if len(A) < nvar:
        return None
    piv = []
    r = 0
    for c in range(nvar):
        p = next((k for k in range(r, len(A)) if A[k][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = F(1) / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for k in range(len(A)):
            if k != r and A[k][c] != 0:
                f = A[k][c]
                A[k] = [A[k][t] - f * A[r][t] for t in range(nvar + 1)]
        piv.append(c)
        r += 1
    if len(piv) < nvar:
        return None
    for k in range(r, len(A)):
        if all(x == 0 for x in A[k][:nvar]) and A[k][nvar] != 0:
            return None
    out = [F(0)] * nvar
    for idx, c in enumerate(piv):
        out[c] = A[idx][nvar]
    return out



def qmul(a, b):
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2, w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2, w1*z2 + x1*y2 - y1*x2 + z1*w2)


def regauge(quats):
    """global rotation putting cube 0 at the identity -- the count is invariant"""
    c = (quats[0][0], -quats[0][1], -quats[0][2], -quats[0][3])
    return [qmul(c, q) for q in quats]


def quats_of(point, q0=None):
    """the configuration's quaternions; cube 0 frozen at q0 (identity if None)"""
    qs = [q0 if q0 is not None else (1, 0, 0, 0)]
    for k in range(0, len(point), 3):
        qs.append(q_of(point[k:k + 3]))
    return qs


def mat_num(qi, qj):
    """R_i^T R_j exactly, as Fractions"""
    from step_a2 import mat
    Mi, Mj = mat(qi), mat(qj)
    return [[sum(Mi[t][r] * Mj[t][c] for t in range(3)) for c in range(3)]
            for r in range(3)]


def conditions(Rs, n, vars_, point, quats):
    """All Step A and Step B conditions, with the tight ones' exact gradients."""
    subs = {v: sp.Rational(p.numerator, p.denominator) for v, p in zip(vars_, point)}
    tight, loose = [], 0
    for i in range(n):
        others = [j for j in range(n) if j != i]
        # normals of every other cube in frame i, evaluated exactly
        # Values EXACTLY in Fractions (sympy only for the tight groups' gradients):
        # substituting 15 variables into hundreds of symbolic normals is what made
        # this unusable at n > 2.
        Nsym, Nval = {}, {}
        for j in others:
            ns = normals_sym(Rs, i, j)
            Rij = mat_num(quats[i], quats[j])
            for k in range(3):
                col_val = [Rij[r][k] for r in range(3)]
                for sgn in (1, -1):
                    key = (j, k, sgn)
                    Nsym[key] = [sgn * e for e in ns[k]]
                    Nval[key] = [sgn * e for e in col_val]
        keys = list(Nsym)
        groups = [(kk,) for kk in keys]
        groups += [(k1, k2) for k1, k2 in itertools.combinations(keys, 2)]
        for g in groups:
            got = min_l1_argmin([Nval[k] for k in g])
            if got is None:
                continue
            val, lam, v = got
            if val != 1:
                loose += 1
                continue
            sig = l1_signs(v)
            Z = [c for c in range(3) if sig[c] == 0]
            if len(g) == 1 and Z:
                # ||n||_1 with a vanishing coordinate is a genuine KINK: the wall
                # is piecewise smooth there and the tangent object is a cone, not
                # a space.  Counted, not used.
                tight.append({'frame': i, 'group': g, 'degenerate': True})
                continue
            if len(g) == 2 and len(Z) == 1:
                # THE CASE THAT MATTERS, and the one v1 wrongly discarded.  The
                # minimiser of min_lam ||lam n1 + (1-lam) n2||_1 sits AT the
                # breakpoint where coordinate c0 vanishes -- that is where it
                # always sits -- so lam* is not an interior optimum and the
                # envelope theorem does not apply.  But v_c0 is LINEAR in lam, so
                # lam* has a closed form and can be substituted BEFORE
                # differentiating: differentiate through the active constraint
                # rather than around it.
                c0 = Z[0]
                n1, n2 = Nsym[g[0]], Nsym[g[1]]
                lam_star = n2[c0] / (n2[c0] - n1[c0])
                # No sp.simplify: only the VALUE at a rational point is ever
                # used, and simplification cannot change a value.  Profiling the
                # n=7 k=4 build: simplify was 139.4s of 150s -- 93% of the whole
                # conditions step -- for no effect on any number produced.
                vv = [lam_star * n1[c] + (1 - lam_star) * n2[c]
                      for c in range(3)]
                expr = sum(sig[c] * vv[c] for c in range(3) if c != c0)
            elif not Z:
                expr = sum(sig[c] * sum(sp.Rational(lam[t].numerator, lam[t].denominator)
                                        * Nsym[g[t]][c] for t in range(len(g)))
                           for c in range(3))
            else:
                tight.append({'frame': i, 'group': g, 'degenerate': True})
                continue
            grad = [sp.diff(expr, v_).subs(subs) for v_ in vars_]
            tight.append({'frame': i, 'group': g, 'degenerate': False,
                          'expr': expr, 'sig': sig, 'c0': (Z[0] if Z else None),
                          'grad': [F(sp.Rational(x)) for x in grad]})
    return tight, loose


def nullspace(rows, ncols):
    """Exact null space basis of the matrix with the given rows."""
    if not rows:
        return [[F(1) if t == c else F(0) for t in range(ncols)]
                for c in range(ncols)]
    M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r]
                   for r in rows])
    return [[F(sp.Rational(x)) for x in list(b)] for b in M.nullspace()]


def count_at(point, n, eps_dir=None, eps=F(1, 64)):
    """exact count of the configuration at `point` (+ eps*dir), gauge cube 0 = I"""
    c = list(point)
    if eps_dir is not None:
        c = [c[t] + eps * eps_dir[t] for t in range(len(c))]
    quats = [QZERO[0] if QZERO else (1, 0, 0, 0)]
    for k in range(0, len(c), 3):
        quats.append(q_of(c[k:k + 3]))
    s = ';'.join(','.join(map(str, q)) for q in quats)
    # The integer engine caps components at 512, and stepping in Cayley
    # coordinates clears denominators well past that -- at arc A a step of 1/32
    # from (53/6, -29/2, -26) lands in the thousands.  Returning None there and
    # scoring it as "count not preserved" is FAILURE_MODES' unevaluable-as-change
    # trap; the wide engine evaluates it instead.
    cmd = ([ENG, '--quats', s]
           if max(abs(v) for q in quats for v in q) <= 512
           else [ENGW, '--d', '0', '--quats', s])
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])['bounded']
    except Exception:
        return None


def solve_dimension(point, n, label, verify_eps=(F(1, 32), F(1, 128)), q0=None):
    """tight conditions -> null space -> engine-verified dimension"""
    vars_ = sp.symbols('c0:%d' % (3 * (n - 1)))
    Rs = frames(vars_, q0)
    base = count_at(point, n)
    tight, loose = cached_conditions(Rs, n, vars_, point,
                                     quats_of(point, q0), q0)
    good = [t for t in tight if not t['degenerate']]
    degen = len(tight) - len(good)
    rows = [t['grad'] for t in good]
    ncols = 3 * (n - 1)
    ns = nullspace(rows, ncols)
    rank = ncols - len(ns)
    print('%s: count %s | %d tight conditions (%d degenerate, %d loose) | '
          'rank %d of %d | candidate dim %d'
          % (label, base, len(tight), degen, loose, rank, ncols, len(ns)), flush=True)

    verified = []
    for d in ns:
        vals = [count_at(point, n, sgn(d), e)
                for e in verify_eps for sgn in (lambda v: v, lambda v: [-x for x in v])]
        if all(v is None for v in vals):
            print('   direction %-40s UNEVALUABLE (not scored as a change)'
                  % str([str(x) for x in d])[:40], flush=True)
            continue
        ok = all(v == base for v in vals if v is not None)
        print('   direction %-40s count preserved: %s'
              % (str([str(x) for x in d])[:40], ok), flush=True)
        if ok:
            verified.append(d)

    if not verified and good:
        # TIGHT IS NOT BINDING: try dropping one condition at a time
        print('   no verified tangent; testing which tight conditions actually BIND',
              flush=True)
        for idx in range(len(good)):
            sub = [rows[t] for t in range(len(rows)) if t != idx]
            for d in nullspace(sub, ncols):
                if all(count_at(point, n, d, e) == base for e in verify_eps):
                    print('   condition %d is NOT binding: direction %s preserves '
                          'the count' % (idx, [str(x) for x in d][:3]), flush=True)
                    verified.append(d)
                    break
            if verified:
                break
    print('%s: VERIFIED DIMENSION >= %d\n' % (label, len(verified)), flush=True)
    return {'label': label, 'count': base, 'tight': len(tight),
            'degenerate': degen, 'rank': rank, 'ncols': ncols,
            'candidate_dim': len(ns), 'verified_dim': len(verified)}





def _polydivmod(a, b):
    a = list(a)
    out = [F(0)] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and any(a):
        while a and a[-1] == 0:
            a.pop()
        if len(a) < len(b):
            break
        k = len(a) - len(b)
        c = a[-1] / b[-1]
        out[k] = c
        for i in range(len(b)):
            a[k + i] -= c * b[i]
        while a and a[-1] == 0:
            a.pop()
    return out, a


def _polygcd(a, b):
    a, b = list(a), list(b)
    while b and any(b):
        _, r = _polydivmod(a, b)
        a, b = b, r
    while a and a[-1] == 0:
        a.pop()
    if a and a[-1] != 0:
        a = [x / a[-1] for x in a]
    return a


def _rational_roots(poly):
    """exact rational roots of a polynomial with Fraction coefficients"""
    if len(poly) < 2:
        return set()
    den = 1
    for c in poly:
        den = den * c.denominator // __import__('math').gcd(den, c.denominator)
    ic = [int(c * den) for c in poly]
    while ic and ic[0] == 0:              # x = 0 is a root
        ic.pop(0)
    out = set()
    if len(ic) < 2:
        return {F(0)}
    a0, an = abs(ic[0]), abs(ic[-1])
    def divisors(m):
        return [d for d in range(1, abs(m) + 1) if m % d == 0] or [1]
    for pnum in divisors(a0):
        for q in divisors(an):
            for sgn in (1, -1):
                r = F(sgn * pnum, q)
                if sum(c * r ** k for k, c in enumerate(poly)) == 0:
                    out.add(r)
    return out


def branch_value(cond, point, n, q0=None):
    """The condition's frozen branch, evaluated EXACTLY in Fractions.

    No symbolic differentiation: the wall is a quadric, so f(point + t d) is a
    low-degree rational function of t, and everything the second-order condition
    needs can be read off exact evaluations.  Forming a 15x15 Hessian per
    condition -- 43 200 symbolic second derivatives for 3 numbers per condition --
    was the wrong algorithm, not a language problem.

    The BRANCH is frozen at the base point: the sign pattern sigma and the active
    coordinate c0 are held fixed, so this is the analytic continuation of the
    piece of f the point sits on, which is exactly what the wall is.
    """
    quats = quats_of(point, q0)
    i = cond['frame']
    N = {}
    for (j, k, sgn) in cond['group']:
        R = mat_num(quats[i], quats[j])
        N[(j, k, sgn)] = [sgn * R[r][k] for r in range(3)]
    g = cond['group']
    sig, c0 = cond['sig'], cond['c0']
    if len(g) == 1:
        v = N[g[0]]
    else:
        n1, n2 = N[g[0]], N[g[1]]
        den = n2[c0] - n1[c0]
        if den == 0:
            return None
        lam = n2[c0] / den
        v = [lam * n1[c] + (1 - lam) * n2[c] for c in range(3)]
    return sum(sig[c] * v[c] for c in range(3) if c != c0)


def _interp(xs, ys):
    """exact Lagrange interpolation -> coefficient list, low degree first"""
    m = len(xs)
    coeffs = [F(0)] * m
    for a in range(m):
        basis = [F(1)]
        denom = F(1)
        for b in range(m):
            if b == a:
                continue
            basis = [F(0)] + basis if False else _polymul(basis, [-xs[b], F(1)])
            denom *= (xs[a] - xs[b])
        for k, c in enumerate(basis):
            coeffs[k] += ys[a] * c / denom
    return coeffs


def _polymul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for a, x in enumerate(p):
        for b, y in enumerate(q):
            out[a + b] += x * y
    return out


def second_order_alphas(good, keep_idx, point, n, v0, v1, q0=None):
    """alpha values for which d = v0 + alpha*v1 stays on EVERY binding wall.

    Per condition: evaluate the frozen branch along the line at 5 exact t values,
    interpolate to get the coefficient of t^2 (the first-order term vanishes for
    every direction in null(J) by construction), then interpolate that in alpha to
    get one binary quadratic.  The tangent directions are the common roots.
    """
    ts = [F(x, 8) for x in (-2, -1, 1, 2, 3)]
    alphas = [F(0), F(1), F(-1), F(2)]
    quads = []
    for idx in keep_idx:
        cond = good[idx]
        qvals = []
        for al in alphas:
            d = [v0[k] + al * v1[k] for k in range(len(v0))]
            ys = []
            for t in ts:
                pt = [point[k] + t * d[k] for k in range(len(point))]
                val = branch_value(cond, pt, n, q0)
                if val is None:
                    ys = None
                    break
                ys.append(val - 1)
            if ys is None:
                qvals = None
                break
            co = _interp(ts, ys)
            qvals.append(co[2] if len(co) > 2 else F(0))
        if qvals is None:
            continue
        qc = _interp(alphas, qvals)
        while qc and qc[-1] == 0:
            qc.pop()
        if len(qc) >= 2:
            quads.append(qc)
    return quads



CACHE = '/Users/dmi/cube-compounds/dimension_cache'


def _cache_key(point, n, q0):
    import hashlib
    raw = repr((n, [str(x) for x in point], q0)).encode()
    return hashlib.sha1(raw).hexdigest()[:16]


def cached_conditions(Rs, n, vars_, point, quats, q0):
    """Conditions are the only expensive step (symbolic, minutes per class), and
    every later analysis -- dimension, wall classification, the boundary cone --
    needs the SAME gradients.  Recomputing them per analysis is what made the
    first census pass unrepeatable; cache them keyed by configuration."""
    import os, pickle
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, _cache_key(point, n, q0) + '.pkl')
    if os.path.exists(f):
        with open(f, 'rb') as fh:
            tight, loose = pickle.load(fh)
        return tight, loose
    tight, loose = conditions(Rs, n, vars_, point, quats)
    slim = [{k: v for k, v in t.items() if k != 'expr'} for t in tight]
    tmp = f + '.%d.tmp' % os.getpid()          # atomic: shards share this cache
    with open(tmp, 'wb') as fh:
        pickle.dump((slim, loose), fh)
    os.replace(tmp, f)
    return tight, loose


def boundary_cone(wall_rows, ncols):
    """The exact directions that keep the count, as a POLYHEDRAL CONE.

    Sampling a fixed direction list measures the sampler, not the configuration:
    the first topology tranche used 7 directions (3 axes + this project's 4 known
    tangents), all small-integer and mostly axis-aligned, so its "on-wall
    fraction" was a lower bound on the outward cone rather than a measurement of
    it.  The cone is computable exactly from the binding walls' gradients, which
    are already in hand:

        C = { d : g_i . d >= 0 for every binding wall i }

        lineality  {d : g_i.d = 0 for all i} = null(J) -- directions preserving
                   the count BOTH ways, i.e. the locus dimension
        facets     the binding walls themselves -- the wall classification, exact
        full-dim   whether the configuration sits on the BOUNDARY of a
                   full-dimensional constant-count region
    """
    lin = nullspace(wall_rows, ncols)
    return {'facets': len(wall_rows), 'lineality_dim': len(lin),
            'ambient': ncols,
            'full_dimensional': len(wall_rows) > 0 and len(lin) < ncols}


def deltas_and_dimension(point, n, label, q0=None, eps=(F(1, 64), F(1, 256))):
    """Solve for constant-COUNT directions, not for wall-preserving ones.

    The previous design took null(J) over every tight condition -- the directions
    along which EVERY condition stays satisfied -- and then searched inside it by
    stepping.  That set is wrong in both directions.  It is too strong, because
    freezing every condition forbids all crossings when only the NET change must
    vanish, and this project already knows most crossings are inert (about a
    quarter of interior crossings move the count; 39 of 39 chamber walls are
    bracketed by coincidences while most coincidences are not boundaries).  And
    it is too weak, being a linearisation: at arc A the true tangent is provably
    IN null(J) while another basis direction of the same 2-space is not
    count-preserving.

    The missing primitive is the per-condition DELTA.  Crossing condition i alone
    changes the count by an integer delta_i, so along a direction d the change is
    sum_i delta_i(sign(grad f_i . d)), and the constant-count directions are the
    sign-chambers where that sum vanishes.  Two things follow for free: BINDING
    stops being a test and becomes a computation (delta_i = 0 IS non-binding, so
    the drop-one-at-a-time fallback disappears), and directions whose crossings
    CANCEL become reachable instead of excluded by construction.

    A direction crossing condition i alone lives in null(J without i) with
    grad f_i . d nonzero; where no such direction exists the condition is
    entangled and is kept, conservatively, as binding.
    """
    vars_ = sp.symbols('c0:%d' % (3 * (n - 1)))
    Rs = frames(vars_, q0)
    base = count_at(point, n)
    tight, loose = cached_conditions(Rs, n, vars_, point,
                                     quats_of(point, q0), q0)
    good = [t for t in tight if not t['degenerate']]
    rows = [t['grad'] for t in good]
    ncols = 3 * (n - 1)
    print('%s: count %s | %d tight (%d degenerate, %d loose) | full null dim %d'
          % (label, base, len(tight), len(tight) - len(good), loose,
             len(nullspace(rows, ncols))), flush=True)

    # CLASSIFY WALLS, NOT CONDITIONS.  Many conditions define the SAME hyperplane,
    # and with 192 conditions of rank 13 no single condition is independent of the
    # rest, so null(J without i) never widens and every condition came back
    # "entangled" -- the delta test never fired.  Grouping by gradient up to scale
    # gives the distinct walls, and a wall's delta is the meaningful quantity.
    def _norm(g):
        piv = next((x for x in g if x != 0), None)
        return tuple(x / piv for x in g) if piv is not None else None
    walls = {}
    for i, r in enumerate(rows):
        k = _norm(r)
        if k is not None:
            walls.setdefault(k, []).append(i)
    print('   %d conditions -> %d DISTINCT WALLS' % (len(rows), len(walls)),
          flush=True)
    wall_rows = [rows[v[0]] for v in walls.values()]
    wall_members = list(walls.values())

    binding, inert, entangled = [], [], []
    for i in range(len(wall_rows)):
        rows_i = wall_rows
        sub = [rows_i[t] for t in range(len(rows_i)) if t != i]
        cross = None
        for d in nullspace(sub, ncols):
            if sum(wall_rows[i][k] * d[k] for k in range(ncols)) != 0:
                cross = d
                break
        if cross is None:
            entangled.append(i)
            continue
        vals = [count_at(point, n, cross, e) for e in eps]
        vals += [count_at(point, n, [-x for x in cross], e) for e in eps]
        seen = [v for v in vals if v is not None]
        if not seen:
            entangled.append(i)                 # unevaluable, not "no change"
        elif all(v == base for v in seen):
            inert.append(i)
        else:
            binding.append(i)
    print('   walls: %d BINDING (delta != 0), %d inert (delta = 0), '
          '%d entangled/unevaluable (kept)' % (len(binding), len(inert),
                                               len(entangled)), flush=True)

    keep = [wall_rows[i] for i in binding + entangled]
    ns = nullspace(keep, ncols)
    print('   binding rank %d of %d -> candidate dim %d'
          % (ncols - len(ns), ncols, len(ns)), flush=True)

    # SOLVE the direction space, do not sample it (METHODS section 1, applied one
    # level up).  Testing a handful of arbitrary combinations of an arbitrary
    # basis is a search, and it MISSES: at arc A the true tangent lies in the
    # 2-space and four hand-picked combinations did not find it.  Within
    # null(J), write d(theta) = v0 + theta*v1; each condition's gradient gives an
    # exact breakpoint grad f_i . d(theta) = 0, the sign vector is constant
    # between consecutive breakpoints, so one representative per interval
    # decides the whole interval.
    verified = []
    cand = list(ns)
    if len(ns) == 2:
        v0, v1 = ns[0], ns[1]
        # SECOND ORDER, and it is EXACT -- by EVALUATION, not differentiation.
        # Every direction in null(J) is orthogonal to every gradient by
        # construction, so nothing is crossed to first order and the count change
        # is second order, i.e. CURVATURE.  But the walls are quadrics
        # (Postscripts 95, 104), so f(x + t d) terminates and the tangent
        # directions solve a QUADRATIC, not a differential equation.  Those
        # quadratics come from exact Fraction evaluations of the frozen branch
        # along the line -- see second_order_alphas.  Forming a Hessian per
        # condition (43 200 symbolic second derivatives for 3 numbers each) was
        # the wrong algorithm; sympy was not the problem.
        v0, v1 = ns
        keep_conditions = [wall_members[i][0] for i in binding + entangled]
        quads = second_order_alphas(good, keep_conditions, point, n,
                                    v0, v1, q0)
        # COMMON ROOTS BY GCD, not by degree cases.  The t^2 coefficient is a
        # rational function of alpha, so these polynomials are NOT generally
        # quadratic -- interpolating over four samples returns cubics.  An
        # extractor that handled only degrees 1 and 2 silently skipped every one
        # of them and reported "no common root" while all 132 vanished at
        # alpha = 2, which is the true tangent (verified 2026-08-13).
        gcd = None
        for qc in quads:
            gcd = qc if gcd is None else _polygcd(gcd, qc)
            if len(gcd) <= 1:
                break
        roots = _rational_roots(gcd) if gcd and len(gcd) > 1 else set()
        reps = sorted(roots) if roots else [F(0), F(1), F(-1)]
        print('   second order: %d quadratics -> %d common rational tangent '
              'direction(s)' % (len(quads), len(roots) if roots else 0), flush=True)
        cand = [[v0[k] + th * v1[k] for k in range(ncols)] for th in reps]
    for d in cand:
        vals = [count_at(point, n, d, e) for e in eps]
        vals += [count_at(point, n, [-x for x in d], e) for e in eps]
        seen = [v for v in vals if v is not None]
        if seen and all(v == base for v in seen):
            if not any(_dependent(v, d, verified) for v in [d]):
                verified.append(d)
    print('%s: candidate dim %d, VERIFIED %d independent count-preserving '
          'directions\n' % (label, len(ns), len(verified)), flush=True)
    cone = boundary_cone(keep, ncols)
    print('   cone: %d facets, lineality dim %d of %d ambient, full-dimensional %s'
          % (cone['facets'], cone['lineality_dim'], cone['ambient'],
             cone['full_dimensional']), flush=True)
    return {'label': label, 'count': base, 'tight': len(good), 'cone': cone,
            'walls': len(walls), 'binding': len(binding), 'inert': len(inert),
            'entangled': len(entangled), 'candidate_dim': len(ns),
            'verified': len(verified)}


def _dependent(v, d, have):
    if not have:
        return False
    M = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in r]
                   for r in have + [d]])
    return M.rank() <= len(have)


CASES = {
    # n = 2: 13 holds on a continuum -> dimension MUST come out >= 1.
    # NB Cayley (1,1,1) is quaternion (1,1,1,1), a 120 deg turn about the
    # diagonal = a cube SELF-SYMMETRY, so the cubes coincide and the count is 1.
    # (1/3,1/3,1/3) is quaternion (3,1,1,1), a genuine 13-pair.
    'n2': ([F(1, 3), F(1, 3), F(1, 3)], 2),
    # n = 2 edge-axis arc, interior: quaternion (4,3,3,0), axis (1,1,0)
    'n2edge': ([F(3, 4), F(3, 4), F(0)], 2),
}


def cayley_of(q):
    w, x, y, z = q
    return None if w == 0 else [F(x, w), F(y, w), F(z, w)]


def point_of(quats):
    """world-frame Cayley coordinates of cubes 1.., cube 0 frozen (see frames)"""
    qs = list(quats)
    pt = []
    for q in qs[1:]:
        c = cayley_of(q)
        if c is None:
            return None            # a half-turn: at Cayley infinity, unreachable
        pt += c
    return pt


BASE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
# arc A: 727 with the sixth cube on the arc; the tangent (1,-3,-6) is verified
# independently, so dim >= 1 here is the control tight_set.py FAILS.
NAMED = {'arcA': BASE + [(6, 53, -87, -156)],
         'record727': BASE + [(7, 14, 1, -5)],
         'n5_393': list(BASE),
         'n4_183': [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'n2'
    out = []
    for k in ('n2', 'n2edge'):
        if which in (k, 'all'):
            pt, n = CASES[k]
            out.append(deltas_and_dimension(pt, n, k))
    for k, quats in NAMED.items():
        if which in (k, 'all'):
            pt = point_of(quats)
            if pt is None:
                print('%s: a cube is a half-turn (w=0) -- at Cayley infinity, '
                      'skipped rather than silently dropped' % k, flush=True)
                continue
            QZERO[:] = [quats[0]]
            out.append(deltas_and_dimension(pt, len(quats), k, q0=quats[0]))
    json.dump(out, open('/Users/dmi/cube-compounds/dimension_%s.json' % which, 'w'),
              indent=1)


if __name__ == '__main__':
    main()
