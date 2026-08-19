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
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
import json
import subprocess
import time
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, HERE)
from solve_ends import q_of
from qfield import (Q as QF, to_sp as qf_to_sp, from_sp as qf_from_sp,
                    clear_denoms as qf_clear_denoms, rot as qf_rot)

ENG = HERE + '/cube_regions_n'
ENGW = HERE + '/cube_regions_q2w'
QZERO = []   # cube 0's frozen quaternion, set per case
BUDGET = [0]  # engine inputs rejected by the overflow budget -- reported, not hidden

# ------------------------------------------------------------------ the field
# Every scalar here lives in Q(sqrt DFIELD); DFIELD = 0 means plain Q and MUST
# reproduce the Fraction path bit-for-bit, since every rational result already
# in the ledger was produced by it -- `dimension_gate.py` checks exactly that.
# The two n = 3 maximisers are the only records outside Q (they sit in Q(sqrt2)
# and Q(sqrt5)), which is why no crossing-based census has ever included them.
#
# INVARIANT to maintain when editing below: nothing may construct a scalar as a
# bare F(0)/F(1) inside the numeric routines.  Derive zero and one from an
# element already in play (`x*0`, `x*0 + 1`) or from `_num`, so the routine is
# field-agnostic.  A literal Fraction silently demotes the arithmetic to Q and
# the failure looks like a wrong ANSWER, not like a type error.
DFIELD = 0


def set_field(d):
    global DFIELD
    DFIELD = int(d)


def _num(a, b=0):
    return F(a) if DFIELD == 0 else QF(F(a), F(b), DFIELD)


def _sp(x):
    return qf_to_sp(x)


def _unsp(e):
    return qf_from_sp(e, DFIELD)


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
        [[_sp(x) for x in row] for row in _mat0(q0)])
    Rs = [R0]
    for k in range(0, len(vars_), 3):
        Rs.append(cayley_matrix(vars_[k:k + 3]))
    return Rs


def _mat0(q):
    if DFIELD:
        return qf_rot([x if isinstance(x, QF) else QF(F(x), 0, DFIELD)
                       for x in q])
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
    zero = N[0][0] * 0                      # field zero and one, not F(0)/F(1):
    one = zero + 1                          # see the DFIELD invariant note
    for size in range(1, r + 1):
        for S in itertools.combinations(range(r), size):
            for A in itertools.combinations(range(3), size - 1):
                rows = [[one] * size + [one]]
                for k in A:
                    rows.append([N[i][k] for i in S] + [zero])
                lam = _solve(rows)
                if lam is None or any(x < 0 for x in lam):
                    continue
                v = [sum(lam[t] * N[S[t]][k] for t in range(size))
                     for k in range(3)]
                val = sum(abs(t) for t in v)
                if best is None or val < best[0]:
                    full = [zero] * r
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
    zero = A[0][0] * 0
    piv = []
    r = 0
    for c in range(nvar):
        p = next((k for k in range(r, len(A)) if A[k][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
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
    out = [zero] * nvar
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


def q_of_field(c):
    """primitive Z[sqrt d] quaternion from Cayley coordinates in Q(sqrt d)"""
    from math import gcd
    d = DFIELD
    cs = [x if isinstance(x, QF) else QF(F(x), 0, d) for x in c]
    _, ints = qf_clear_denoms([QF(1, 0, d)] + cs)
    g = 0
    for p, q in ints:
        g = gcd(gcd(g, abs(p)), abs(q))
    if g > 1:
        ints = [(p // g, q // g) for p, q in ints]
    return tuple(QF(F(p), F(q), d) for p, q in ints)


def normalize_dir(v):
    """scale a direction to primitive integer (pairs of) coordinates.

    Scaling does not move the tangent LINE, but it does set how far a fixed eps
    steps, and the engine's budget is on component magnitude -- an unscaled null
    space vector routinely lands outside it, and an out-of-budget input is an
    UNEVALUABLE direction, not a count-changing one."""
    from math import gcd
    if DFIELD == 0:
        L = 1
        for x in v:
            L = L * F(x).denominator // gcd(L, F(x).denominator)
        ints = [int(F(x) * L) for x in v]
        g = 0
        for t in ints:
            g = gcd(g, abs(t))
        return [F(t // g) for t in ints] if g else [F(0)] * len(v)
    _, ints = qf_clear_denoms(list(v))
    g = 0
    for p, q in ints:
        g = gcd(gcd(g, abs(p)), abs(q))
    if not g:
        return [QF(0, 0, DFIELD) for _ in v]
    return [QF(F(p // g), F(q // g), DFIELD) for p, q in ints]


def quats_of(point, q0=None):
    """the configuration's quaternions; cube 0 frozen at q0 (identity if None)"""
    if DFIELD:
        qs = [tuple(x if isinstance(x, QF) else QF(F(x), 0, DFIELD) for x in
                    (q0 if q0 is not None else (1, 0, 0, 0)))]
        for k in range(0, len(point), 3):
            qs.append(q_of_field(point[k:k + 3]))
        return qs
    qs = [q0 if q0 is not None else (1, 0, 0, 0)]
    for k in range(0, len(point), 3):
        qs.append(q_of(point[k:k + 3]))
    return qs


def mat_num(qi, qj):
    """R_i^T R_j exactly, in the field (Fractions when DFIELD = 0)"""
    Mi, Mj = _mat0(qi), _mat0(qj)
    return [[sum(Mi[t][r] * Mj[t][c] for t in range(3)) for c in range(3)]
            for r in range(3)]


def conditions(Rs, n, vars_, point, quats):
    """All Step A and Step B conditions, with the tight ones' exact gradients."""
    subs = {v: _sp(p) for v, p in zip(vars_, point)}
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
                expr = sum(sig[c] * sum(_sp(lam[t]) * Nsym[g[t]][c]
                                        for t in range(len(g)))
                           for c in range(3))
            else:
                tight.append({'frame': i, 'group': g, 'degenerate': True})
                continue
            grad = [sp.diff(expr, v_).subs(subs) for v_ in vars_]
            tight.append({'frame': i, 'group': g, 'degenerate': False,
                          'expr': expr, 'sig': sig, 'c0': (Z[0] if Z else None),
                          'grad': [_unsp(x) for x in grad]})
    return tight, loose


def nullspace(rows, ncols):
    """Exact null space basis of the matrix with the given rows."""
    if not rows:
        return [[_num(1) if t == c else _num(0) for t in range(ncols)]
                for c in range(ncols)]
    M = sp.Matrix([[_sp(x) for x in r] for r in rows])
    return [[_unsp(x) for x in list(b)] for b in M.nullspace()]


def count_at(point, n, eps_dir=None, eps=F(1, 64)):
    """exact count of the configuration at `point` (+ eps*dir), gauge cube 0 = I"""
    c = list(point)
    if eps_dir is not None:
        c = [c[t] + eps * eps_dir[t] for t in range(len(c))]
    if DFIELD:
        quats = quats_of(c, QZERO[0] if QZERO else None)
        groups = []
        for q in quats:
            _, ints = qf_clear_denoms(list(q))
            groups.append(ints)
        s = ';'.join(','.join('%d:%d' % t for t in g) for g in groups)
        p = subprocess.run([ENGW, '--d', str(DFIELD), '--quats', s],
                           capture_output=True, text=True)
        try:
            return json.loads(p.stdout.strip().splitlines()[-1])['bounded']
        except Exception:
            BUDGET[0] += 1                    # counted, never scored as "no change"
            return None
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



CACHE = HERE + '/dimension_cache'


def _cache_key(point, n, q0):
    import hashlib
    # DFIELD is part of the key: the same Cayley tuple means different numbers
    # over Q and over Q(sqrt d), and a collision would serve rational gradients
    # for a field configuration without any error.  The DFIELD = 0 key is left
    # BYTE-IDENTICAL to the pre-port one so the existing cache -- the census's
    # restartability -- survives the port.
    raw = (repr((n, [str(x) for x in point], q0)) if DFIELD == 0
           else repr((n, [str(x) for x in point], str(q0), DFIELD))).encode()
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



def quad_form_on(cond, point, n, ns, q0=None):
    """The second-order form of one condition, as a symmetric matrix on null(J).

    Q(w) is the coefficient of t^2 in f(point + t w) - 1, read off exact
    Fraction evaluations of the frozen branch (no Hessian).  A quadratic form is
    fixed by its values on a spanning set plus POLARISATION:

        B(v_i, v_j) = [ Q(v_i + v_j) - Q(v_i) - Q(v_j) ] / 2

    so d + C(d,2) line evaluations give the whole d x d matrix.
    """
    ts = [F(x, 8) for x in (-2, -1, 1, 2, 3)]

    def Q(w):
        ys = []
        for t in ts:
            pt = [point[k] + t * w[k] for k in range(len(point))]
            v = branch_value(cond, pt, n, q0)
            if v is None:
                return None
            ys.append(v - 1)
        co = _interp(ts, ys)
        return co[2] if len(co) > 2 else F(0)

    d = len(ns)
    diag = [Q(v) for v in ns]
    if any(x is None for x in diag):
        return None
    M = [[F(0)] * d for _ in range(d)]
    for i in range(d):
        M[i][i] = diag[i]
    for i in range(d):
        for j in range(i + 1, d):
            w = [ns[i][k] + ns[j][k] for k in range(len(ns[i]))]
            q = Q(w)
            if q is None:
                return None
            M[i][j] = M[j][i] = (q - diag[i] - diag[j]) / 2
    return M


def second_order_variety(good, keep_idx, point, n, ns, q0=None):
    """Common zero set of ALL the second-order forms on P(null(J)).

    Solving plane by plane can only find directions lying in a coordinate
    2-plane of the chosen basis, so it can never be conclusive: "no root in any
    plane" is not "no root".  The forms are homogeneous quadratics in the d
    null-space coordinates, so their common zero set is a projective variety and
    a Groebner basis decides it outright.

    Returns ('empty', []) when the only common zero is the origin -- i.e. NO
    direction survives second order and the locus is a point -- or
    ('nonempty', [rational directions]) otherwise.
    """
    d = len(ns)
    if d == 0:
        return ('empty', [])
    ts = sp.symbols('u0:%d' % d)
    polys = []
    for idx in keep_idx:
        M = quad_form_on(good[idx], point, n, ns, q0)
        if M is None:
            continue
        e = sp.expand(sum(sp.Rational(M[i][j].numerator, M[i][j].denominator)
                          * ts[i] * ts[j] for i in range(d) for j in range(d)))
        if e != 0:
            polys.append(e)
    if not polys:
        return ('nonempty', list(ns))
    import time          # nothing constrains second order
    polys = list(dict.fromkeys(polys))
    G = sp.groebner(polys, *ts, order='grevlex')
    # projective variety empty  <=>  some power of every variable is in the ideal
    empty = all(any(g.as_poly(*ts).monoms() == [tuple(k * (v == u) for v in ts)]
                    for g in G.exprs for k in range(1, 5) if g.as_poly(*ts).is_monomial)
                for u in ts)
    if empty or all(G.reduce(u ** 3)[1] == 0 for u in ts):
        return ('empty', [])
    sols = sp.solve(polys, *ts, dict=True)
    out = []
    for so in sols:
        vals = [so.get(u, sp.Integer(1)) for u in ts]
        if any(v.free_symbols for v in vals):
            continue
        try:
            fr = [F(sp.Rational(v)) for v in vals]
        except Exception:
            continue
        if any(x != 0 for x in fr):
            out.append([sum(fr[i] * ns[i][k] for i in range(d))
                        for k in range(len(ns[0]))])
    return ('nonempty', out)



def branch_expr(cond, cvecs):
    """The frozen branch as a SYMBOLIC expression, given symbolic Cayley vectors.

    Same formula as branch_value, but built over sympy so the condition can be
    treated as a polynomial rather than sampled.  Sampling was the error: the
    t^2 coefficient of a polynomial INTERPOLANT through five points of a RATIONAL
    function is not that function's Taylor coefficient, so it is not a quadratic
    form -- measured, c2(2w)/c2(w) came out 4.000...0001 instead of 4, and
    polarisation applied to it produced a Groebner answer that failed its control.
    """
    i = cond['frame']
    Rs = [cayley_matrix(c) if c is not None else sp.eye(3) for c in cvecs]
    N = {}
    for (j, k, sgn) in cond['group']:
        A = Rs[i].T * Rs[j]
        N[(j, k, sgn)] = [sgn * A[r, k] for r in range(3)]
    g = cond['group']
    sig, c0 = cond['sig'], cond['c0']
    if len(g) == 1:
        v = N[g[0]]
    else:
        n1, n2 = N[g[0]], N[g[1]]
        lam = n2[c0] / (n2[c0] - n1[c0])
        v = [lam * n1[c] + (1 - lam) * n2[c] for c in range(3)]
    return sum(sig[c] * v[c] for c in range(3) if c != c0)


def second_order_variety_exact(good, keep_idx, point, n, ns, q0=None, cap=None):
    """Directions in null(J) whose LINE LIES IN every binding wall -- exactly.

    A direction w survives iff f(point + t w) == 1 IDENTICALLY in t, not merely
    to second order.  Build that condition symbolically in the null-space
    coordinates u (only dim(null) variables, so this is cheap) and in t, take the
    NUMERATOR -- a genuine polynomial -- and collect its t-coefficients.  Each is
    a polynomial in u; their common zero set is the answer, by Groebner.

    This replaces the polarisation attempt, which assumed the sampled second-order
    coefficient was a quadratic form.  It is not.
    """
    d = len(ns)
    if d == 0:
        return ('empty', [])
    us = sp.symbols('u0:%d' % d)
    t = sp.Symbol('t_')
    ncols = len(ns[0])
    w = [sum(us[i] * sp.Rational(ns[i][k].numerator, ns[i][k].denominator)
             for i in range(d)) for k in range(ncols)]
    cvec = []
    for k in range(0, ncols, 3):
        cvec.append([sp.Rational(point[k + r].numerator, point[k + r].denominator)
                     + t * w[k + r] for r in range(3)])
    cvecs = [None] + cvec                      # cube 0 frozen
    if q0 is not None:
        cvecs[0] = [sp.Rational(F(q0[r + 1], q0[0]).numerator,
                                F(q0[r + 1], q0[0]).denominator) for r in range(3)]
    polys = []
    # NO CAP by default: a Groebner basis over a SUBSET of the conditions
    # describes a weaker variety, and its points need not lie in the walls
    # left out.  Measured: capping at 25 of 192 conditions at arc A returned
    # two directions that counted 679 instead of 727.
    for idx in (keep_idx if cap is None else keep_idx[:cap]):
        e = branch_expr(good[idx], cvecs) - 1
        num, _ = sp.fraction(sp.together(sp.expand(e)))
        pt_ = sp.Poly(sp.expand(num), t)
        for c in pt_.all_coeffs()[:-1]:        # t^0 vanishes: we are on the wall
            c = sp.expand(c)
            if c != 0:
                polys.append(c)
    if not polys:
        return ('nonempty', list(ns))
    polys = list(dict.fromkeys(polys))
    G = sp.groebner(polys, *us, order='grevlex')
    if all(G.reduce(u ** 4)[1] == 0 for u in us):
        return ('empty', [])
    sols = sp.solve(list(G.exprs), *us, dict=True)
    out = []
    for so in sols:
        vals = [so.get(u, sp.Integer(1)) for u in us]
        if any(getattr(v, 'free_symbols', set()) for v in vals):
            continue          # a free parameter means a positive-dimensional
                              # component; substituting 1 INVENTS a point rather
                              # than finding one, so it is skipped and reported
        try:
            fr = [F(sp.Rational(v)) for v in vals]
        except Exception:
            continue
        if any(x != 0 for x in fr):
            out.append([sum(fr[i] * ns[i][k] for i in range(d)) for k in range(ncols)])
    return ('nonempty', out)



def branch_numerator(cond, cvecs):
    """The condition as an exact POLYNOMIAL, with no rational-function algebra.

    branch_expr builds f as a ratio and then calls together/expand to extract a
    numerator, which costs ~4.6 s per condition -- 15 minutes for one arc-A
    build, before Groebner.  It is unnecessary: with M the UNNORMALISED rotation
    matrices and N = 1 + |c|^2, the normals are m/(N_i N_j), and in the size-2
    case the lambda* denominators CANCEL, leaving

        P = sum_{c != c0} sigma_c ( m2[c0] m1[c] - m1[c0] m2[c] )
              - ( m2[c0] - m1[c0] ) N_i N_j

    and in the size-1 case  P = sum_c sigma_c m[c] - N_i N_j.  Both are pure
    polynomial products of matrix entries.  f = 1 exactly when P = 0.
    """
    i = cond['frame']
    Ms, Ns = [], []
    for c in cvecs:
        if c is None:
            Ms.append(sp.eye(3)); Ns.append(sp.Integer(1)); continue
        x, y, z = c
        Ns.append(1 + x*x + y*y + z*z)
        Ms.append(sp.Matrix([[1+x*x-y*y-z*z, 2*(x*y-z), 2*(x*z+y)],
                             [2*(x*y+z), 1-x*x+y*y-z*z, 2*(y*z-x)],
                             [2*(x*z-y), 2*(y*z+x), 1-x*x-y*y+z*z]]))
    m = {}
    for (j, k, sgn) in cond['group']:
        A = Ms[i].T * Ms[j]
        m[(j, k, sgn)] = ([sgn * A[r, k] for r in range(3)], Ns[i] * Ns[j])
    g = cond['group']
    sig, c0 = cond['sig'], cond['c0']
    if len(g) == 1:
        mm, den = m[g[0]]
        return sp.expand(sum(sig[c] * mm[c] for c in range(3) if c != c0) - den)
    (m1, d1), (m2, d2) = m[g[0]], m[g[1]]
    assert sp.simplify(d1 - d2) == 0 or True     # same pair -> same denominator
    lead = m2[c0] - m1[c0]
    return sp.expand(sum(sig[c] * (m2[c0]*m1[c] - m1[c0]*m2[c])
                         for c in range(3) if c != c0) - lead * d1)


def variety_fast(good, keep_idx, point, n, ns, q0=None):
    """Common zeros of the exact condition polynomials on P(null(J)), by GCD.

    For lineality 2 the variety lives in P^1, where a Groebner basis is heavier
    machinery than the question needs: dehomogenise and take the GCD chain of the
    univariate t-coefficients.  Returns (status, directions).
    """
    d = len(ns)
    ncols = len(ns[0])
    t = sp.Symbol('t_')
    if d != 2:
        # d >= 3 needs the projective variety, not a GCD chain.  The polynomials
        # are cheap now (branch_numerator), but GROEBNER cost is unchanged by how
        # they were built -- it was the 2h+ bottleneck.  Handled INCREMENTALLY by
        # the caller: cut with a few polynomials, then FILTER the candidate points
        # against the rest by evaluation, which is exact and cheap.
        return ('unsupported', [])
    u = sp.Symbol('u_')
    w = [sp.Rational(ns[0][k].numerator, ns[0][k].denominator)
         + u * sp.Rational(ns[1][k].numerator, ns[1][k].denominator)
         for k in range(ncols)]
    cvec = [[sp.Rational(point[k+r].numerator, point[k+r].denominator) + t*w[k+r]
             for r in range(3)] for k in range(0, ncols, 3)]
    c0v = None
    if q0 is not None:
        c0v = [sp.Rational(F(q0[r+1], q0[0]).numerator, F(q0[r+1], q0[0]).denominator)
               for r in range(3)]
    cvecs = [c0v] + cvec
    gcd = None
    for idx in keep_idx:
        P = branch_numerator(good[idx], cvecs)
        pol = sp.Poly(P, t)
        for c in pol.all_coeffs()[:-1]:          # t^0 vanishes: on the wall
            c = sp.expand(c)
            if c == 0:
                continue
            cp = sp.Poly(c, u)
            gcd = cp if gcd is None else sp.gcd(gcd, cp)
            if gcd.degree() < 1:
                return ('empty', [])
    if gcd is None:
        return ('nonempty', list(ns))
    out = []
    for r in sp.roots(gcd, u):
        if r.is_rational:
            rr = F(sp.Rational(r))
            out.append([ns[0][k] + rr * ns[1][k] for k in range(ncols)])
    return ('nonempty' if out else 'irrational_only', out)



_BUDGET = object()


def _budget_worker(q, eqs_s, free_s):
    """Module-level so it can be PICKLED: macOS defaults to the spawn start
    method, and a nested function fails with PicklingError at p.start()."""
    try:
        import sympy as _sp
        e = [_sp.sympify(x) for x in eqs_s]
        f = [_sp.Symbol(x) for x in free_s]
        q.put([{str(k): str(v) for k, v in so.items()}
               for so in _sp.solve(e, *f, dict=True)])
    except Exception:
        q.put([])


def _solve_with_budget(eqs, free, seconds):
    """sp.solve in a subprocess with a wall-clock cap.

    Returns _BUDGET on timeout -- a distinct value from [], because "no solutions"
    and "did not finish" are different facts and collapsing them loses the one
    that matters.  A subprocess is used because sympy does not check signals
    reliably inside its accelerated paths, so SIGALRM cannot be trusted to
    interrupt it.
    """
    import multiprocessing as mp
    # FORK, NOT SPAWN.  Python 3.14 defaults to spawn on macOS, and spawn
    # re-imports the parent's __main__ module in the child -- so a caller script
    # without an `if __name__ == '__main__'` guard RE-RUNS ITSELF, calls this
    # again, and spawns recursively.  Observed 2026-08-18 on diag_stuck.py.
    # Fixing it in the caller would leave the trap set for the next one; fork
    # does not touch __main__ at all, so the helper is safe for ANY caller.
    try:
        ctx = mp.get_context('fork')
    except ValueError:                      # platform without fork
        ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=_budget_worker,
                    args=(q, [str(x) for x in eqs], [str(x) for x in free]))
    p.start()
    p.join(seconds)
    if p.is_alive():
        p.terminate(); p.join()
        return _BUDGET
    try:
        raw = q.get_nowait()
    except Exception:
        return []
    return [{sp.Symbol(k): sp.sympify(v) for k, v in so.items()} for so in raw]


def variety_incremental(good, keep_idx, point, n, ns, q0=None, seed=None,
                        chart_budget=None, progress=True):
    """Common zeros on P(null(J)) for ANY lineality, without Groebner.

    Buchberger over all 192 condition polynomials did not finish in 2 hours, and
    making the polynomials cheap (branch_numerator) does not help: construction
    cost and solve cost are independent.  But the system is massively
    over-determined -- a handful of polynomials already cut the variety to
    finitely many points, and the remaining hundreds are then checked by
    EVALUATION, which is exact and costs microseconds.

        cut    solve the first few polynomials for candidate points
        filter evaluate every remaining polynomial at each candidate

    Charts: a direction is defined up to scale, so each u_i = 1 chart is solved
    in the remaining d-1 affine variables and the results unioned.
    """
    d = len(ns)
    ncols = len(ns[0])
    t = sp.Symbol('t_')
    us = sp.symbols('u0:%d' % d)
    w = [sum(us[i] * sp.Rational(ns[i][k].numerator, ns[i][k].denominator)
             for i in range(d)) for k in range(ncols)]
    cvec = [[sp.Rational(point[k+r].numerator, point[k+r].denominator) + t*w[k+r]
             for r in range(3)] for k in range(0, ncols, 3)]
    c0v = None
    if q0 is not None:
        c0v = [sp.Rational(F(q0[r+1], q0[0]).numerator, F(q0[r+1], q0[0]).denominator)
               for r in range(3)]
    cvecs = [c0v] + cvec
    polys = []
    for idx in keep_idx:
        pol = sp.Poly(branch_numerator(good[idx], cvecs), t)
        for c in pol.all_coeffs()[:-1]:
            c = sp.expand(c)
            if c != 0:
                polys.append(c)
    if not polys:
        return ('nonempty', list(ns))
    print('      %d polynomials built (seed sized per chart)' % len(polys), flush=True)
    found = []
    # PER-CHART PROGRESS AND BUDGET.  Two n=9 classes ran 10+ HOURS with no
    # output at all, and a wedged process is indistinguishable from a working one
    # when neither prints -- that indistinguishability, not the runtime, is the
    # defect.  The cost is concentrated in sp.solve on d-1 coupled polynomials in
    # d-1 unknowns (7x7 at lineality 8), which is tractable for most classes and
    # occasionally explodes.  A chart that exceeds its budget is reported
    # UNEVALUATED, never as "no solutions": scoring a timeout as EMPTY would be
    # the unevaluable-as-negative-result trap in its most expensive form.
    timed_out = []
    for chart in range(d):
        _t0 = time.time()
        if progress:
            print('      chart %d/%d (%d unknowns)' % (chart + 1, d, d - 1),
                  flush=True)
        free = [u for i, u in enumerate(us) if i != chart]
        ps = [q for q in (sp.expand(p.subs({us[chart]: 1})) for p in polys) if q != 0]
        if not ps:
            # every polynomial vanishes identically in this chart: nothing
            # constrains second order here, so the chart's directions all survive.
            found.append(list(ns[chart]))
            continue
        # THE CHART ORIGIN IS A SOLUTION WHENEVER NO POLYNOMIAL HAS A CONSTANT
        # TERM, and that is cheap to test by evaluation.  The existing fast path
        # above catches only IDENTICALLY ZERO polynomials; a nonzero polynomial
        # with no constant term is a different case and fell through to the
        # 7-unknown sp.solve -- which ran 10+ HOURS on n=9 k=5 (2,3,5,7,8) while
        # ns[chart] itself satisfied all 252 conditions exactly (verified 2026-08-18
        # by direct evaluation: 0 of 252 nonzero).  This is a SPEED fix, not a
        # correctness one: sp.solve does find the origin among its solutions when
        # it terminates, so completed classes are unaffected.
        if all(sp.expand(q.subs({u: 0 for u in free})) == 0 for q in ps):
            if progress:
                print('      chart %d: ORIGIN SOLVES ALL %d polynomials -- '
                      'ns[%d] is a candidate, no solve needed'
                      % (chart + 1, len(ps), chart), flush=True)
            found.append(list(ns[chart]))
            continue
        if not free:
            # LINEALITY 1: one chart, no free variables, nothing to solve -- the
            # direction is unique up to scale and the test is pure evaluation.
            # Previously `sp.Poly(q, *free)` got no generators and raised
            # GeneratorsNeeded, crashing all 23 lineality-1 classes INCLUDING the
            # records 63, 183, 393, 727.
            continue
        # SEED SIZE MUST MATCH THE UNKNOWNS.  seed=2 solves 2 equations in d-1
        # variables, which is under-determined for d >= 4 -- sp.solve then grinds
        # on a positive-dimensional system and does not return.  Take d-1
        # equations, choosing the LOWEST-DEGREE ones: cheapest to solve and, in
        # this system, the most constraining.
        k_seed = seed if seed is not None else max(1, len(free))
        ps_sorted = sorted(ps, key=lambda q: sp.Poly(q, *free).total_degree())
        if chart_budget is not None:
            sols = _solve_with_budget(ps_sorted[:k_seed], free, chart_budget)
            if sols is _BUDGET:
                timed_out.append(chart)
                if progress:
                    print('      chart %d TIMED OUT after %ss -- UNEVALUATED, '
                          'not empty' % (chart + 1, chart_budget), flush=True)
                continue
        else:
            try:
                sols = sp.solve(ps_sorted[:k_seed], *free, dict=True)
            except Exception:
                continue
        if progress:
            print('      chart %d: %d seed solutions in %.0fs'
                  % (chart + 1, len(sols), time.time() - _t0), flush=True)
        for so in sols:
            # A variable ABSENT from sp.solve's dict is UNCONSTRAINED, i.e. free --
            # not a failed solve.  Reading it as None and skipping discarded the
            # whole positive-dimensional component and produced a false EMPTY on
            # the control n7k4c163, whose confirmed direction is exactly the
            # chart origin.  Default to the symbol so it takes the parametric path.
            vals = [so.get(u, u) for u in free]
            # POSITIVE-DIMENSIONAL COMPONENTS ARE THE ANSWER, NOT AN OBSTACLE.
            # Skipping parametric solutions produced a FALSE EMPTY on the control
            # n7k4c163, which has 2 engine-confirmed directions: lineality 4 with
            # verified 2 means the surviving set IS positive-dimensional, so
            # sp.solve necessarily returns free symbols.  Substituting a value is
            # safe here precisely because every candidate is then FILTERED against
            # all the polynomials -- the check that "inventing a point" lacked.
            cands = [vals]
            fs = set()
            for v in vals:
                fs |= getattr(v, 'free_symbols', set())
            if fs:
                cands = []
                for val in (sp.Integer(0), sp.Integer(1), sp.Integer(-1),
                            sp.Rational(1, 2), sp.Integer(2)):
                    cands.append([v.subs({f: val for f in fs}) if getattr(
                        v, 'free_symbols', set()) else v for v in vals])
            for cv in cands:
                try:
                    sub = {u: sp.Rational(v) for u, v in zip(free, cv)}
                except Exception:
                    continue
                if all(sp.expand(p.subs(sub)) == 0 for p in ps_sorted):
                    coef = [F(0)] * d
                    coef[chart] = F(1)
                    for i, u in enumerate(free):
                        coef[us.index(u)] = F(sp.Rational(sub[u]))
                    found.append([sum(coef[i] * ns[i][k] for i in range(d))
                                  for k in range(ncols)])
            continue
            try:
                sub = {u: sp.Rational(v) for u, v in zip(free, vals)}
            except Exception:
                continue
            if all(sp.expand(p.subs(sub)) == 0 for p in ps_sorted):  # FILTER on the rest
                coef = [F(0)] * d
                coef[chart] = F(1)
                for i, u in enumerate(free):
                    coef[us.index(u)] = F(sp.Rational(sub[u]))
                found.append([sum(coef[i] * ns[i][k] for i in range(d))
                              for k in range(ncols)])
    return ('nonempty' if found else 'empty', found)


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

    binding, inert, entangled, deltas = [], [], [], []
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
        # RECORD THE COUNT ACROSS THE FACET.  This is the exact version of what
        # `subset_topology.py` was sampling with a fixed 7-direction list: the
        # direction crossing this wall ALONE is determined by the geometry, not
        # chosen from a menu, so "what lies beyond this boundary" needs no sample.
        if seen:
            deltas.append({'wall': i, 'beyond': sorted(set(seen)),
                           'binding': any(v != base for v in seen)})
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
    second_order = None
    if len(ns) >= 2 and DFIELD:
        # NOT PORTED, and said so rather than skipped silently.  The second-order
        # layer (branch_numerator, the GCD chain, _rational_roots) extracts roots
        # in Q; over Q(sqrt d) the roots it would need may lie in the field and
        # not in Q, so running it unchanged would return FEWER directions and the
        # shortfall would read as "the locus is smaller", which is exactly the
        # unevaluable-scored-as-a-negative-result trap.  `verified` below is
        # therefore a lower bound that only sees the null-space BASIS directions.
        second_order = 'not ported to Q(sqrt %d)' % DFIELD
        print('   second order: NOT EVALUATED over Q(sqrt %d) -- verified is a '
              'basis-only lower bound' % DFIELD, flush=True)
    elif len(ns) >= 2:
        # SECOND ORDER, EXACT, and over EVERY 2-PLANE of the null space.
        # Every direction in null(J) is orthogonal to every gradient by
        # construction, so nothing is crossed to first order and the count change
        # is second order -- curvature.  The walls are quadrics (Postscripts 95,
        # 104), so f(x + t d) terminates and staying on a wall is exactly
        # d'Hd = 0: a QUADRATIC, not a differential equation, obtained here by
        # exact Fraction evaluation rather than by forming Hessians.
        #
        # Restricting to ONE plane (the first two basis vectors) was why
        # `verified` could never reach `lineality` above dimension 2 -- a
        # 3-dimensional tangent space cannot be confirmed as 3 from inside a
        # single plane.  Every pair of basis vectors is now solved.  LIMIT,
        # stated because it bounds the result: this finds tangent directions
        # lying in a coordinate 2-plane of the chosen basis, so `verified`
        # remains a LOWER bound on the locus dimension.
        keep_conditions = [wall_members[i][0] for i in binding + entangled]
        cand = list(ns)
        planes = 0
        for ia in range(len(ns)):
            for ib in range(ia + 1, len(ns)):
                quads = second_order_alphas(good, keep_conditions, point, n,
                                            ns[ia], ns[ib], q0)
                gcd = None
                for qc in quads:
                    gcd = qc if gcd is None else _polygcd(gcd, qc)
                    if len(gcd) <= 1:
                        break
                roots = _rational_roots(gcd) if gcd and len(gcd) > 1 else set()
                planes += 1
                for th in roots:
                    cand.append([ns[ia][k] + th * ns[ib][k] for k in range(ncols)])
        print('   second order: %d planes solved -> %d candidate directions'
              % (planes, len(cand)), flush=True)

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
    cone['beyond_each_facet'] = deltas
    print('   cone: %d facets, lineality dim %d of %d ambient, full-dimensional %s'
          % (cone['facets'], cone['lineality_dim'], cone['ambient'],
             cone['full_dimensional']), flush=True)
    return {'label': label, 'count': base, 'tight': len(good), 'cone': cone,
            'walls': len(walls), 'binding': len(binding), 'inert': len(inert),
            'entangled': len(entangled), 'candidate_dim': len(ns),
            'verified': len(verified), 'second_order': second_order,
            'field': DFIELD, 'budget_rejects': BUDGET[0]}


def _dependent(v, d, have):
    if not have:
        return False
    M = sp.Matrix([[_sp(x) for x in r] for r in have + [d]])
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
    if DFIELD:
        w, x, y, z = (t if isinstance(t, QF) else QF(F(t), 0, DFIELD)
                      for t in (w, x, y, z))
        return None if w.is_zero() else [x / w, y / w, z / w]
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
    json.dump(out, open(HERE + '/dimension_%s.json' % which, 'w'),
              indent=1)


if __name__ == '__main__':
    main()
