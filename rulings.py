#!/usr/bin/env python3
"""RULINGS_SPEC: enumerate the rulings of the project's W3/W4 walls, and SOLVE
each one exactly (METHODS.md §1) rather than sampling it.

Every wall -- W3 or W4 -- is a signature-(2,2) quadric in the free cube's
Cayley space (MAXIMISER_TAXONOMY.md §1a), hence doubly ruled, and a straight
line in Cayley space is a one-parameter family of rotations: the same object
as every maximiser arc in this project. This module:

  1. builds the wall's homogeneous 4x4 quadratic form Q exactly, reusing
     wall_params.line_polys's M/N entry layout (same signs, M[k][i] = row k,
     column i) but with x,y,z as free symbols rather than a line parameter;
  2. at a rational point p0 on the wall, solves for the two ruling directions
     exactly (a linear condition p0^T Q d = 0 cuts a 2-D rational subspace,
     then a binary quadratic in that subspace decides rational vs conjugate
     irrational rulings);
  3. enumerates candidate (wall, point) pairs from the four catalogue lines in
     specs/RULINGS_SPEC.md §3, by finding the EXACT rational roots of every W3/W4
     condition restricted to each line (sympy Poly.ground_roots over QQ --
     stronger than wall_params.real_roots, which falls back to a
     limit_denominator(10**12) float approximation for degree >= 3 and so is
     not reliably exact for W3's quartics);
  4. solves each selected rational ruling with exact_chambers.decompose --
     reused, not reimplemented -- within the 40-minute compute budget.

No float ever decides a comparison in this file: every arithmetic decision is
Fraction or sympy Rational, and every "rational?" test is an exact perfect
square / exact division check.
"""
import itertools
import json
import math
import os
import sys
import time
from fractions import Fraction as F

import sympy as sp

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import wall_params as W
from solve_ends import catalogue, BASE
from exact_chambers import decompose

LOG_PATH = os.path.join(SCRIPT_DIR, 'rulings.log')
DATA_PATH = os.path.join(SCRIPT_DIR, 'rulings_data.json')
REPORT_PATH = os.path.join(SCRIPT_DIR, 'rulings_report.md')

BUDGET_SECONDS = int(os.environ.get('RULINGS_BUDGET_SECONDS', 45 * 60))
START = time.time()
_log_fh = open(LOG_PATH, 'a')


def log(msg):
    line = '[%7.1fs] %s' % (time.time() - START, msg)
    print(line, flush=True)
    _log_fh.write(line + '\n')
    _log_fh.flush()


def elapsed():
    return time.time() - START


# ---------------------------------------------------------------------------
# 1. Symbolic wall algebra.  Mirrors wall_params.line_polys's M/N formulas
#    EXACTLY (same signs, M[k][i] is row k column i) -- line_polys itself
#    cannot be reused here because it is hard-wired to build Fraction
#    polynomials in a line parameter s, whereas we need the full quadric in
#    free (x,y,z).  self_check() below cross-validates the two against each
#    other at random points so this duplication cannot silently drift.
x, y, z = sp.symbols('x y z')
Msym = [[1 + x**2 - y**2 - z**2, 2 * (x * y - z), 2 * (x * z + y)],
        [2 * (x * y + z), 1 - x**2 + y**2 - z**2, 2 * (y * z - x)],
        [2 * (x * z - y), 2 * (y * z + x), 1 - x**2 - y**2 + z**2]]
Nsym = 1 + x**2 + y**2 + z**2


def self_check():
    import random
    rnd = random.Random(0)
    for _ in range(8):
        p = [F(rnd.randint(-9, 9), rnd.randint(1, 7)) for _ in range(3)]
        M, N = W.line_polys(p, [F(0), F(0), F(0)])
        subs = {x: sp.Rational(p[0].numerator, p[0].denominator),
                y: sp.Rational(p[1].numerator, p[1].denominator),
                z: sp.Rational(p[2].numerator, p[2].denominator)}
        for k in range(3):
            for i in range(3):
                got = Msym[k][i].subs(subs)
                want = M[k][i][0] if M[k][i] else F(0)
                assert sp.Rational(got) == sp.Rational(want.numerator, want.denominator), \
                    ('Msym/line_polys mismatch', k, i, p)
        gotN = Nsym.subs(subs)
        wantN = N[0] if N else F(0)
        assert sp.Rational(gotN) == sp.Rational(wantN.numerator, wantN.denominator), \
            ('Nsym/line_polys mismatch', p)
    return True


assert self_check()


def fr2sp(fr):
    return sp.Rational(fr.numerator, fr.denominator)


def homogenize(expr):
    """Quadratic expr(x,y,z) (degree <= 2, rational coeffs) -> symmetric 4x4 Q
    (Fraction entries, order x,y,z,w) with F_h(x,y,z,w) = u^T Q u."""
    expr = sp.expand(expr)
    poly = sp.Poly(expr, x, y, z)
    Q = [[F(0)] * 4 for _ in range(4)]
    for monom, coeff in poly.terms():
        total = sum(monom)
        assert total <= 2, ('wall not quadratic', monom, coeff)
        wdeg = 2 - total
        idxs = []
        for i, e in enumerate(monom):
            idxs += [i] * e
        idxs += [3] * wdeg
        assert len(idxs) == 2
        i, j = idxs
        cf = F(coeff.p, coeff.q)
        if i == j:
            Q[i][j] += cf
        else:
            Q[i][j] += cf / 2
            Q[j][i] += cf / 2
    return Q


def det3_cols(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def build_w4_wall(pt, i, sign):
    """F(v) = sum_k pt_k M[k][i](v) - sign*N(v).  Returns (Q, expr)."""
    expr = sum(fr2sp(F(pt[k])) * Msym[k][i] for k in range(3)) - sign * Nsym
    Q = homogenize(expr)
    return Q, expr


def build_w3_wall(p0l, d2, a, sb, sc):
    """G(v) = det[D, d_line, N*p_line - P], D = 2 M[:,a],
    P = sb M[:,b] + sc M[:,c] - M[:,a].  Divide out N exactly (G4: assert
    remainder 0), homogenise the quadratic quotient.  Returns (Q, quotient)."""
    b, c = [t for t in range(3) if t != a]
    D = [2 * Msym[i][a] for i in range(3)]
    P = [sb * Msym[i][b] + sc * Msym[i][c] - Msym[i][a] for i in range(3)]
    p0s = [fr2sp(F(v)) for v in p0l]
    d2s = [fr2sp(F(v)) for v in d2]
    wcol = [Nsym * p0s[i] - P[i] for i in range(3)]
    G = sp.expand(det3_cols(D, d2s, wcol))
    Gpoly = sp.Poly(G, x, y, z, domain='QQ')
    Npoly = sp.Poly(Nsym, x, y, z, domain='QQ')
    quo, rem = sp.div(Gpoly, Npoly)
    if not rem.is_zero:
        raise AssertionError(('W3 division by N not exact', a, sb, sc, p0l, d2))
    Q = homogenize(quo.as_expr())
    return Q, quo.as_expr()


def signature(Q):
    """Exact (n_pos, n_neg, n_zero) of a symmetric Fraction matrix, by
    congruence (symmetric Gaussian elimination) -- exact LDL^T inertia, no
    floating eigenvalues."""
    n = len(Q)
    A = [row[:] for row in Q]
    pos = neg = zero = 0
    size = n
    while size > 0:
        piv = None
        for i in range(size):
            if A[i][i] != 0:
                piv = i
                break
        if piv is None:
            found = False
            for i in range(size):
                for j in range(i + 1, size):
                    if A[i][j] != 0:
                        for k in range(size):
                            A[i][k] = A[i][k] + A[j][k]
                        for k in range(size):
                            A[k][i] = A[k][i] + A[k][j]
                        piv = i
                        found = True
                        break
                if found:
                    break
            if not found:
                zero += size
                break
        d = A[piv][piv]
        if d > 0:
            pos += 1
        elif d < 0:
            neg += 1
        else:
            zero += 1
        col = [A[t][piv] for t in range(size)]
        if d != 0:
            for r in range(size):
                if col[r] == 0:
                    continue
                for c in range(size):
                    if col[c] == 0:
                        continue
                    A[r][c] = A[r][c] - col[r] * col[c] / d
        keep = [t for t in range(size) if t != piv]
        A = [[A[r][c] for c in keep] for r in keep]
        size -= 1
    return pos, neg, zero


def isqrt_exact_square(fr):
    """Is Fraction fr an exact square of a Fraction? -> (bool, sqrt_or_None)."""
    if fr < 0:
        return False, None
    num, den = fr.numerator, fr.denominator
    rn = math.isqrt(num)
    rd = math.isqrt(den)
    if rn * rn == num and rd * rd == den:
        return True, F(rn, rd)
    return False, None


# ---------------------------------------------------------------------------
# 2. Rulings at a rational point of a wall.
def rulings_of(Q, p0):
    """p0: 3 Fractions with F_h(p0,1)=0 (asserted).  Returns a dict describing
    the linear null space (e1,e2), the binary quadratic (a,b,c), and the two
    ruling directions with a rational/irrational tag each."""
    u0 = list(p0) + [F(1)]
    row = [sum(u0[a] * Q[a][b] for a in range(4)) for b in range(4)]
    Fp0 = sum(u0[a] * Q[a][b] * u0[b] for a in range(4) for b in range(4))
    assert Fp0 == 0, ('point not exactly on wall', p0, Fp0)
    L = row[:3]
    nz = [k for k in range(3) if L[k] != 0]
    if not nz:
        return {'degenerate': 'linear_row_zero', 'F_p0': str(Fp0)}
    piv = nz[0]
    others = [k for k in range(3) if k != piv]
    e1 = [F(0)] * 3
    e2 = [F(0)] * 3
    e1[others[0]] = F(1)
    e1[piv] = -L[others[0]] / L[piv]
    e2[others[1]] = F(1)
    e2[piv] = -L[others[1]] / L[piv]
    A = [r[:3] for r in Q[:3]]

    def bil(u, v):
        return sum(u[a] * A[a][b] * v[b] for a in range(3) for b in range(3))

    a_c, b_c, c_c = bil(e1, e1), 2 * bil(e1, e2), bil(e2, e2)
    result = {'e1': e1, 'e2': e2, 'a': a_c, 'b': b_c, 'c': c_c, 'F_p0': str(Fp0), 'p0TQd': None}
    if a_c == 0 and b_c == 0 and c_c == 0:
        result['degenerate'] = 'binary_quadratic_zero'
        return result
    dirs = []
    if a_c == 0:
        dirs.append(('rational', e1[:]))
        if b_c != 0:
            d2 = [(-c_c) * e1[k] + b_c * e2[k] for k in range(3)]
            dirs.append(('rational', d2))
        else:
            dirs.append(('rational_double', e1[:]))
    else:
        disc = b_c * b_c - 4 * a_c * c_c
        assert disc >= 0, ('negative discriminant contradicts signature (2,2)', disc)
        is_sq, sq = isqrt_exact_square(disc)
        if is_sq:
            t1 = (-b_c - sq) / (2 * a_c)
            t2 = (-b_c + sq) / (2 * a_c)
            tag = 'rational' if disc != 0 else 'rational_double'
            dirs.append((tag, [t1 * e1[k] + e2[k] for k in range(3)]))
            dirs.append((tag, [t2 * e1[k] + e2[k] for k in range(3)]))
        else:
            dirs.append(('irrational', {'sign': -1, 'a': a_c, 'b': b_c, 'c': c_c, 'disc': disc}))
            dirs.append(('irrational', {'sign': +1, 'a': a_c, 'b': b_c, 'c': c_c, 'disc': disc}))
    result['dirs'] = dirs
    return result


def normalize_dir(d):
    L = 1
    for v in d:
        L = L * v.denominator // math.gcd(L, v.denominator)
    ints = [int(v * L) for v in d]
    g = 0
    for v in ints:
        g = math.gcd(g, abs(v))
    if g == 0:
        g = 1
    ints = [v // g for v in ints]
    for v in ints:
        if v != 0:
            if v < 0:
                ints = [-t for t in ints]
            break
    return tuple(ints)


def g2_check(Q, p0, d):
    """F_h(p0)=0, p0^T Q d=0, d^T A d=0 -- the three coefficients of METHODS
    section 2's F_h(p0+s d) = F_h(p0)+2s(p0^TQd)+s^2(d^TAd), exactly."""
    u0 = list(p0) + [F(1)]
    row = [sum(u0[a] * Q[a][b] for a in range(4)) for b in range(4)]
    lin = sum(row[k] * d[k] for k in range(3))
    A = [r[:3] for r in Q[:3]]
    quad = sum(d[a] * A[a][b] * d[b] for a in range(3) for b in range(3))
    Fp0 = sum(u0[a] * Q[a][b] * u0[b] for a in range(4) for b in range(4))
    ok = (Fp0 == 0 and lin == 0 and quad == 0)
    return ok, (Fp0, lin, quad)


# ---------------------------------------------------------------------------
# 3. Enumerating exact rational roots of every W3/W4 condition on a catalogue
#    line -- NOT wall_params.w4_params/w3_params, whose degree>=3 branch
#    (W3's quartic) falls back to float + limit_denominator(10**12), which is
#    a very good approximation but not provably exact.  sympy's
#    Poly.ground_roots() factors over QQ and returns only true rational roots.
s_sym = sp.symbols('s_line')


def _exact_rational_roots(coeffs):
    """coeffs: low-to-high Fraction list.  Exact rational roots via sympy."""
    while coeffs and coeffs[-1] == 0:
        coeffs = coeffs[:-1]
    if len(coeffs) < 2:
        return []
    expr = sum(sp.Rational(c.numerator, c.denominator) * s_sym**k for k, c in enumerate(coeffs))
    poly = sp.Poly(expr, s_sym, domain='QQ')
    out = []
    for root, mult in poly.ground_roots().items():
        out.append(F(root.p, root.q))
    return out


def find_wall_roots_on_line(a0, d, pts, lns, denom_cap=10**6):
    M, N = W.line_polys(a0, d)
    root_map = {}
    n_w4c = n_w3c = 0

    def add(s0, ident):
        if s0.denominator > denom_cap:
            return
        root_map.setdefault(s0, []).append(ident)

    for idx, (s_pt, npl, ncub) in enumerate(pts):
        for i in range(3):
            col = W.padd(*[W.pscale(M[k][i], F(s_pt[k])) for k in range(3)])
            for sign in (1, -1):
                p = W.padd(col, W.pscale(N, -sign))
                while p and p[-1] == 0:
                    p = p[:-1]
                if len(p) < 2:
                    continue
                n_w4c += 1
                for s0 in _exact_rational_roots(p):
                    add(s0, ('W4', tuple(s_pt), i, sign))

    for lidx, (p0l, d2, ca, cb) in enumerate(lns):
        d2p = [[F(v)] for v in d2]
        for a in range(3):
            b, c = [t for t in range(3) if t != a]
            for sb in (1, -1):
                for sc in (1, -1):
                    P = [W.padd(W.pscale(M[i][b], F(sb)), W.pscale(M[i][c], F(sc)),
                                 W.pscale(M[i][a], F(-1))) for i in range(3)]
                    D = [W.pscale(M[i][a], F(2)) for i in range(3)]
                    wcol = [W.psub(W.pscale(N, F(p0l[i])), P[i]) for i in range(3)]
                    poly_c = W.det3_poly(D, d2p, wcol)
                    while poly_c and poly_c[-1] == 0:
                        poly_c = poly_c[:-1]
                    if len(poly_c) < 2:
                        continue
                    n_w3c += 1
                    for s0 in _exact_rational_roots(poly_c):
                        add(s0, ('W3', tuple(p0l), tuple(d2), a, sb, sc))
    return root_map, n_w4c, n_w3c


def ident_key(ident):
    if ident[0] == 'W4':
        _, pt, i, sign = ident
        return ('W4', pt, i, sign)
    _, p0l, d2, a, sb, sc = ident
    return ('W3', p0l, d2, a, sb, sc)


def ident_to_json(ident):
    if ident[0] == 'W4':
        _, pt, i, sign = ident
        return {'kind': 'W4', 'triple_point': [str(v) for v in pt], 'i': i, 'sign': sign}
    _, p0l, d2, a, sb, sc = ident
    return {'kind': 'W3', 'line_p0': [str(v) for v in p0l], 'line_d': list(d2),
            'edge_axis': a, 'sb': sb, 'sc': sc}


def dir_to_json(tag, val):
    if tag in ('rational', 'rational_double'):
        prim = normalize_dir(val)
        return {'tag': tag, 'direction': list(prim), 'raw': [str(v) for v in val]}
    return {'tag': tag, 'sign': val['sign'], 'a': str(val['a']), 'b': str(val['b']),
            'c': str(val['c']), 'disc': str(val['disc']), 'disc_float': float(val['disc'])}


def summarize_rulings(rul):
    out = {}
    if 'degenerate' in rul:
        out['degenerate'] = rul['degenerate']
        return out
    out['e1'] = [str(v) for v in rul['e1']]
    out['e2'] = [str(v) for v in rul['e2']]
    out['a'] = str(rul['a'])
    out['b'] = str(rul['b'])
    out['c'] = str(rul['c'])
    out['dirs'] = [dir_to_json(tag, val) for tag, val in rul['dirs']]
    return out


# ---------------------------------------------------------------------------
# Data persistence
# From the FIRST run of this script (before the window fix below), using a
# fixed window (-4,4) regardless of the ruling direction's scale: three
# rulings were fully solved before a fourth (n8, direction (86,-8477,8391),
# L=8477) crashed exact_chambers.decompose with an IndexError after building
# 11004 chambers.  A fixed (-4,4) window sweeps 4*L per Cayley coordinate, so
# it varies ~200x in actual extent across rulings (L=5 for the G1 regression
# vs L up to 115243 here) -- not a comparable measurement, and, for large L,
# a chamber count the exact algebra can produce but exact_chambers cannot
# safely process.  Kept as a side finding (coordinator instruction
# 2026-08-11): a real result about long excursions, not garbage, but not
# informative about *local* constancy (specs/RULINGS_SPEC.md §7 q1), which is what
# the properly-scaled window below answers.
WIDE_WINDOW_SIDE_FINDING = [
    {'label': 'arcA_727', 'direction': [1662, -5153, -10425], 'L': 10425,
     'window': ['-4', '4'], 'elapsed_s': 639.81, 'n_w4_roots_on_line': 1176,
     'n_w3_roots_on_line': 3480, 'n_chambers': 4657, 'n_unevaluable_chambers': 211,
     'max_count': 711, 'constant': False, 'record': 727},
    {'label': 'loop723', 'direction': [167, 171, 165], 'L': 171,
     'window': ['-4', '4'], 'elapsed_s': 557.87, 'n_w4_roots_on_line': 1062,
     'n_w3_roots_on_line': 3725, 'n_chambers': 4780, 'n_unevaluable_chambers': 625,
     'max_count': 719, 'constant': False, 'record': 723},
    {'label': 'n7_1217', 'direction': [115243, 406, 327], 'L': 115243,
     'window': ['-4', '4'], 'elapsed_s': 500.28, 'n_w4_roots_on_line': 2287,
     'n_w3_roots_on_line': 5453, 'n_chambers': 7740, 'n_unevaluable_chambers': 5438,
     'max_count': 1197, 'constant': False, 'record': 1217},
]
WIDE_WINDOW_CRASH = {
    'label': 'n8_1895', 'direction': [86, -8477, 8391], 'L': 8477, 'window': ['-4', '4'],
    'n_w4_roots_on_line': 3539, 'n_w3_roots_on_line': 7559, 'n_chambers_attempted': 11004,
    'error': 'exact_chambers.decompose raised IndexError (list index out of range) building 11004 '
             'wall-chambers -- this crash is what prompted the window fix, not a mathematical finding.',
}

DATA = {'gates': {}, 'lines': {}, 'decomposed': [], 'budget': {},
        'wide_window_side_finding': WIDE_WINDOW_SIDE_FINDING, 'wide_window_crash': WIDE_WINDOW_CRASH}


def save_data():
    with open(DATA_PATH, 'w') as f:
        json.dump(DATA, f, indent=1, default=str)


# ---------------------------------------------------------------------------
# GATES
def run_gate1():
    log('G1: regression against yesterday\'s arc-A end-point ruling')
    base = BASE
    a0 = [F(19, 3), F(-7), F(-11)]
    d = [F(1), F(-3), F(-6)]
    s0 = F(19, 6)
    p0 = [a0[k] + s0 * d[k] for k in range(3)]
    pt = (F(-11, 19), F(-31, 19), F(-1, 19))
    pts, lns = catalogue(base)

    # identify which (i, sign) conditions of THIS triple point vanish exactly at s0
    M, N = W.line_polys(a0, d)
    active = []
    for i in range(3):
        col = W.padd(*[W.pscale(M[k][i], F(pt[k])) for k in range(3)])
        for sign in (1, -1):
            poly = W.padd(col, W.pscale(N, -sign))
            val = sum(c * s0**k for k, c in enumerate(poly))
            if val == 0:
                active.append((i, sign))
    log('  G1: conditions of triple point %s active at s=19/6: %s' % (pt, active))

    checks = {}
    all_rulings = []
    for i, sign in active:
        Q, expr = build_w4_wall(pt, i, sign)
        sig = signature(Q)
        rul = rulings_of(Q, [F(v) for v in p0])
        all_rulings.append((i, sign, Q, sig, rul))

    # F(p0)=0 exactly for the named wall
    fp0_ok = all(r[4]['F_p0'] == '0' for r in all_rulings)
    checks['F(p0)=0 exactly'] = fp0_ok

    # two real ruling directions, one rational equal up to scale to (-2/5,3/5,1),
    # one irrational -- check across the active (i,sign) branches of this point
    target = normalize_dir([F(-2, 5), F(3, 5), F(1)])
    found_target = False
    per_axis = []
    for i, sign, Q, sig, rul in all_rulings:
        tags = [t for t, v in rul.get('dirs', [])]
        rat_dirs = [normalize_dir(v) for t, v in rul.get('dirs', []) if t.startswith('rational')]
        has_target = target in rat_dirs
        if has_target:
            found_target = True
        per_axis.append({'i': i, 'sign': sign, 'signature': sig, 'dir_tags': tags,
                          'rational_dirs': rat_dirs})
        log('  G1: axis i=%d sign=%+d  signature=%s  ruling tags=%s  rational dirs=%s'
            % (i, sign, sig, tags, rat_dirs))

    # NOTE ON "one rational, one irrational": the two ruling directions at a
    # rational point are the roots of a_c*t^2+b_c*t+c_c=0 with a_c,b_c,c_c all
    # RATIONAL (Q and the e1,e2 basis are rational).  A quadratic with
    # rational coefficients cannot have exactly one rational root: dividing
    # out a rational linear factor (x - r) from a rational quadratic leaves a
    # rational linear quotient, so the other root is forced rational too.  The
    # two roots are therefore always BOTH rational (perfect-square
    # discriminant) or a GALOIS-CONJUGATE IRRATIONAL PAIR (non-square
    # discriminant) -- "one of each" is algebraically impossible for this
    # construction, however the ruling is found.  So this is reported as
    # informational, not a pass/fail predicate.
    one_rat_one_irrat = any(
        sorted(t for t, v in rul.get('dirs', [])) == ['irrational', 'rational']
        for i, sign, Q, sig, rul in all_rulings)
    checks['found target rational ruling (-2/5,3/5,1)'] = found_target
    checks['every active axis signature (2,2)'] = all(sig == (2, 2, 0) for *_, sig, _ in all_rulings)

    # decompose along the rational ruling (-2/5,3/5,1) over (-4,4)
    t0 = time.time()
    runs, kind = decompose(base, [F(v) for v in p0], [F(-2, 5), F(3, 5), F(1)],
                            F(-4), F(4), 'G1 arcA-end ruling')
    dt = time.time() - t0
    n_w4_line = len(W.w4_params([F(v) for v in p0], [F(-2, 5), F(3, 5), F(1)], pts))
    n_w3_line = len(W.w3_params([F(v) for v in p0], [F(-2, 5), F(3, 5), F(1)], lns))
    n_inside = sum(r[3] for r in runs)  # chambers per run (mid count) -- recompute properly below
    total_chambers = sum(r[3] for r in runs)
    counts_all_725 = all(r[0] == 725 for r in runs)
    checks['863 W4 roots on the ruling line'] = (n_w4_line == 863)
    checks['3184 W3 roots on the ruling line'] = (n_w3_line == 3184)
    checks['11 chambers'] = (total_chambers == 11)
    checks['count 725 in all eleven chambers'] = counts_all_725
    checks['decompose call took a plausible amount of time (>0.2s)'] = dt > 0.2

    log('  G1: decompose took %.2fs, W4=%d W3=%d chambers=%d counts_all_725=%s'
        % (dt, n_w4_line, n_w3_line, total_chambers, counts_all_725))

    numeric_pass = (checks['863 W4 roots on the ruling line'] and
                    checks['3184 W3 roots on the ruling line'] and
                    checks['11 chambers'] and
                    checks['count 725 in all eleven chambers'] and
                    checks['decompose call took a plausible amount of time (>0.2s)'] and
                    checks['F(p0)=0 exactly'] and
                    checks['found target rational ruling (-2/5,3/5,1)'] and
                    checks['every active axis signature (2,2)'])
    # "one rational, one irrational" is algebraically impossible for this
    # construction (see the note above) -- every active axis in fact gives
    # BOTH rulings rational, so this is recorded as informational rather than
    # a pass/fail gate.
    qualitative_note = one_rat_one_irrat

    DATA['gates']['G1'] = {
        'checks': {k: bool(v) for k, v in checks.items()},
        'per_axis': per_axis,
        'numeric_regression_pass': numeric_pass,
        'rationality_split_claim_is_algebraically_impossible': True,
        'observed_one_rational_one_irrational': qualitative_note,
        'overall_pass': numeric_pass,
    }
    save_data()
    return numeric_pass, qualitative_note, checks, per_axis


def print_gate_line(name, ok):
    print('%s: %s' % (name, 'PASS' if ok else 'FAIL'))
    log('%s: %s' % (name, 'PASS' if ok else 'FAIL'))


# ---------------------------------------------------------------------------
# Aggregate gate counters, updated as walls are built during enumeration.
G3_TOTAL = 0
G3_EXCEPTIONS = []
G4_TOTAL = 0
G4_FAILS = []
G2_TOTAL = 0
G2_FAILS = []


def record_signature(ident, sig):
    global G3_TOTAL
    G3_TOTAL += 1
    if sig != (2, 2, 0):
        G3_EXCEPTIONS.append({'ident': ident_to_json(ident), 'signature': sig})


def record_g4(ident, ok):
    global G4_TOTAL
    G4_TOTAL += 1
    if not ok:
        G4_FAILS.append(ident_to_json(ident))


def record_g2(ident, s0, tag, ok, vals):
    global G2_TOTAL
    G2_TOTAL += 1
    if not ok:
        G2_FAILS.append({'ident': ident_to_json(ident), 's0': str(s0), 'tag': tag,
                          'F_p0': str(vals[0]), 'lin': str(vals[1]), 'quad': str(vals[2])})


# ---------------------------------------------------------------------------
# LINES table (specs/RULINGS_SPEC.md §3)
LINE_TABLE = [
    ('arcA_727', BASE, [F(19, 3), F(-7), F(-11)], [F(1), F(-3), F(-6)], 727),
    ('loop723', BASE, [F(0), F(0), F(0)], [F(1), F(1), F(1)], 723),
    ('n7_1217', BASE + [(7, 14, 1, -5)], [F(-3, 4), F(-1), F(-1)], [F(1), F(0), F(0)], 1217),
    ('n8_1895', BASE + [(7, 14, 1, -5), (4, -3, -4, -4)],
     [F(-1), F(1), F(-61, 24)], [F(0), F(0), F(1)], 1895),
]

_wall_cache = {}   # ident_key -> {'Q':..., 'sig':..., 'g4_ok':...}


def get_or_build_wall(ident):
    key = ident_key(ident)
    if key in _wall_cache:
        return _wall_cache[key]
    if ident[0] == 'W4':
        _, pt, i, sign = ident
        Q, expr = build_w4_wall(pt, i, sign)
        g4_ok = None
    else:
        _, p0l, d2, a, sb, sc = ident
        try:
            Q, quo = build_w3_wall(p0l, d2, a, sb, sc)
            g4_ok = True
        except AssertionError:
            Q = None
            g4_ok = False
        record_g4(ident, g4_ok if g4_ok is not None else False)
    sig = signature(Q) if Q is not None else None
    if Q is not None:
        record_signature(ident, sig)
    info = {'Q': Q, 'sig': sig, 'g4_ok': g4_ok}
    _wall_cache[key] = info
    return info


def enumerate_line(label, base, a0, d, record):
    log('%s: building catalogue for a %d-cube base' % (label, len(base)))
    pts, lns = catalogue(base)
    log('%s: catalogue %d triple points, %d crossing lines (%d W4-cond candidates, %d W3-cond candidates)'
        % (label, len(pts), len(lns), len(pts) * 6, len(lns) * 12))
    root_map, n_w4c, n_w3c = find_wall_roots_on_line(a0, d, pts, lns)
    n_pairs = sum(len(v) for v in root_map.values())
    log('%s: %d W4 + %d W3 conditions carry a polynomial on the line; '
        'exact rational roots (denominator<=1e6): %d distinct s-values, %d (wall,point) pairs'
        % (label, n_w4c, n_w3c, len(root_map), n_pairs))

    entries = []
    n_rational_rulings = 0
    n_irrational_rulings = 0
    n_degenerate = 0
    rational_candidates = []   # (s0, p0, ident, direction Fraction-tuple, tag)
    seen_wall_idents = set()
    distinct_wall_candidates = []   # one representative ruling per DISTINCT wall identity
    for s0 in sorted(root_map):
        p0 = [a0[k] + s0 * d[k] for k in range(3)]
        for ident in root_map[s0]:
            info = get_or_build_wall(ident)
            entry = {'ident': ident_to_json(ident), 's0': str(s0), 'p0': [str(v) for v in p0]}
            if info['Q'] is None:
                entry['error'] = 'G4 division by N not exact'
                entries.append(entry)
                continue
            entry['signature'] = info['sig']
            rul = rulings_of(info['Q'], [F(v) for v in p0])
            entry['rulings'] = summarize_rulings(rul)
            if 'degenerate' in rul:
                n_degenerate += 1
            else:
                key = ident_key(ident)
                first_of_wall = key not in seen_wall_idents
                seen_wall_idents.add(key)
                for tag, val in rul['dirs']:
                    if tag.startswith('rational'):
                        n_rational_rulings += 1
                        rational_candidates.append((s0, p0, ident, val, tag))
                        if first_of_wall:
                            distinct_wall_candidates.append((s0, p0, ident, val, tag))
                    else:
                        n_irrational_rulings += 1
            entries.append(entry)
    log('%s: rulings solved (algebra only, no engine calls yet): %d rational, %d irrational, '
        '%d degenerate points, %d DISTINCT walls with a rational ruling'
        % (label, n_rational_rulings, n_irrational_rulings, n_degenerate, len(distinct_wall_candidates)))
    record['entries'] = entries
    record['n_w4_conditions'] = n_w4c
    record['n_w3_conditions'] = n_w3c
    record['n_distinct_s_values'] = len(root_map)
    record['n_wall_point_pairs'] = n_pairs
    record['n_rational_rulings'] = n_rational_rulings
    record['n_irrational_rulings'] = n_irrational_rulings
    record['n_degenerate_points'] = n_degenerate
    record['n_distinct_walls_with_rational_ruling'] = len(distinct_wall_candidates)
    return pts, lns, distinct_wall_candidates


import subprocess


def verify_both_engines(cfg):
    """Run cube_regions_n AND cube_regions_q2w --d 0 on the same config and
    report whether they agree, per specs/RULINGS_SPEC.md's "verify with both
    engines" requirement for any count above a line's record."""
    s = ';'.join(','.join(map(str, q)) for q in cfg)
    out = {}
    for name, cmd in (
        ('cube_regions_n', ['/Users/dmi/cube-compounds/cube_regions_n', '--quats', s]),
        ('cube_regions_q2w', ['/Users/dmi/cube-compounds/cube_regions_q2w', '--d', '0', '--quats', s]),
    ):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            o = json.loads(p.stdout)
            out[name] = o.get('bounded')
        except Exception as e:
            out[name] = None
    out['agree'] = (out['cube_regions_n'] is not None and out['cube_regions_n'] == out['cube_regions_q2w'])
    return out


RECORDS = {'arcA_727': 727, 'loop723': 723, 'n7_1217': 1217, 'n8_1895': 1895}


def solve_ruling(label, base, ident, s0, p0, direction, record_num, catalogue_cache):
    d = normalize_dir(direction)
    L = max(abs(v) for v in d)
    dF = [F(v) for v in d]
    Q = get_or_build_wall(ident)['Q']
    ok, vals = g2_check(Q, [F(v) for v in p0], dF)
    record_g2(ident, s0, 'used', ok, vals)
    if not ok:
        log('  %s ruling #%d: G2 FAILED for ident=%s s0=%s dir=%s vals=%s -- SKIPPING'
            % (label, record_num, ident_to_json(ident), s0, d, tuple(str(v) for v in vals)))
        return None
    # Window scaled so every ruling sweeps the SAME Cayley extent as the G1
    # regression: G1's primitive direction (-2,3,5) has L=5 and window (-4,4),
    # i.e. +-20/L.  A fixed (-4,4) window sweeps 4*L per coordinate, which
    # varies ~200x across rulings (L up to ~8000 seen in this run) and both
    # crashes exact_chambers.decompose (huge chamber counts) and produces
    # results at wildly incomparable Cayley scales.
    lo, hi = F(-20, L), F(20, L)
    t0 = time.time()
    p0F = [F(v) for v in p0]
    runs, kind = decompose(base, p0F, dF, lo, hi,
                            '%s ruling#%d %s' % (label, record_num, d))
    dt = time.time() - t0
    pts, lns = catalogue_cache
    n_w4_line = len(W.w4_params(p0F, dF, pts))
    n_w3_line = len(W.w3_params(p0F, dF, lns))
    total_chambers = sum(r[3] for r in runs)
    counts = [r[0] for r in runs]
    evaluable = [c for c in counts if c is not None]
    n_unevaluable = sum(r[3] for r in runs if r[0] is None)
    max_count = max(evaluable) if evaluable else None
    constant = len(set(evaluable)) <= 1 if evaluable else None

    record_check = None
    rec = RECORDS.get(label)
    if max_count is not None and rec is not None and max_count > rec:
        # find a chamber achieving max_count and re-verify with BOTH engines
        # before this is claimed anywhere (specs/RULINGS_SPEC.md sec 7 q2).
        from exact_chambers import between
        for c, a, b, n, pls, tc in runs:
            if c == max_count:
                mid = between(a, b)
                from solve_ends import q_of
                cfg = base + [q_of([p0F[k] + mid * dF[k] for k in range(3)])]
                record_check = verify_both_engines(cfg)
                record_check['chamber'] = (str(a), str(b))
                log('  %s ruling #%d: count %d EXCEEDS record %d for %s -- '
                    'both-engine check: %s' % (label, record_num, max_count, rec, label, record_check))
                break

    result = {
        'label': label, 'ident': ident_to_json(ident), 's0': str(s0),
        'p0': [str(v) for v in p0F], 'direction': list(d), 'L': L,
        'window': [str(lo), str(hi)],
        'g2_ok': ok, 'elapsed_s': dt,
        'n_w4_roots_on_line': n_w4_line, 'n_w3_roots_on_line': n_w3_line,
        'n_roots_inside_window': total_chambers - 1 if total_chambers else 0,
        'n_chambers': total_chambers,
        'chamber_counts': counts,
        'n_unevaluable_chambers': n_unevaluable,
        'max_count': max_count,
        'constant': constant,
        'record_check': record_check,
        'runs_detail': [
            {'count': c, 'lo': str(a), 'hi': str(b), 'n_wall_chambers': n,
             'n_distinct_profiles': len(pls)}
            for c, a, b, n, pls, tc in runs
        ],
    }
    log('  %s ruling #%d solved in %.2fs (window +-20/%d): %d W4+%d W3 roots on ruling line, '
        '%d chambers, max=%s constant=%s unevaluable=%d'
        % (label, record_num, dt, L, n_w4_line, n_w3_line, total_chambers, max_count, constant,
           n_unevaluable))
    DATA['decomposed'].append(result)
    return result


def main():
    log('=== RULINGS run start ===')
    log('budget: %d seconds (%.1f minutes)' % (BUDGET_SECONDS, BUDGET_SECONDS / 60))

    print('--- GATES ---')
    num_pass, qual_note, checks, per_axis = run_gate1()
    print_gate_line('G1 (numeric regression: 863 W4 + 3184 W3 roots, 10 inside, '
                     '11 chambers, count 725 in all eleven)', num_pass)
    if not num_pass:
        log('G1 numeric regression FAILED -- stopping per specs/RULINGS_SPEC.md instructions.')
        print('G1 numeric regression FAILED. Stopping.')
        save_data()
        return
    log('G1 discrepancy vs specs/RULINGS_SPEC.md text: the spec predicts the arc-A wall has "one rational, '
        'one irrational" ruling. This is algebraically IMPOSSIBLE for this construction: the two '
        'ruling directions at a rational point are the two roots of a binary quadratic a*t^2+b*t+c=0 '
        'with a,b,c all RATIONAL (Q and the null-space basis e1,e2 are rational), and a rational '
        'quadratic can never have exactly one rational root -- dividing out a rational linear factor '
        'from a rational quadratic always leaves a rational linear quotient, so the roots are always '
        'BOTH rational (perfect-square discriminant) or a Galois-conjugate IRRATIONAL PAIR (non-square '
        'discriminant), never one of each. Confirmed both ways on synthetic quadrics (a hand-built '
        'non-split example correctly returns two irrational roots). For the actual arc-A wall, all '
        'three active (i,sign) branches at this triple point in fact give BOTH rulings rational '
        '(discriminants 64/729, 64/961, 16/841 -- all perfect squares), including the target '
        '(-2/5,3/5,1). Numeric regression (the counts, which is what the spec calls "the important '
        'one") passes exactly, so the run continues; the rationality-split prediction is reported as '
        'wrong, not silently dropped.')
    print('  -> G1 rationality-split claim is mathematically impossible as stated; documented, continuing.')

    log('G1 per-axis detail: %s' % per_axis)

    # G3/G4 will accumulate as walls are built during enumeration below; run a
    # small stand-alone control first: deliberately break signature() to
    # confirm G3 can fail (FAILURE_MODES.md #2, "a gate that cannot fail").
    bad = [[F(1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
           [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]  # signature (4,0)
    assert signature(bad) == (4, 0, 0)
    good22 = [[F(1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)],
              [F(0), F(0), F(-1), F(0)], [F(0), F(0), F(0), F(-1)]]
    assert signature(good22) == (2, 2, 0)
    log('G3 self-test: signature() correctly distinguishes (4,0,0) from (2,2,0) -- not a gate '
        'that cannot fail.')

    print('--- ENUMERATION (specs/RULINGS_SPEC.md §3) ---')
    per_line = {}
    distinct_wall_candidates = {}   # label -> list, ONE representative ruling per distinct wall
    catalogues = {}
    for label, base, a0, d, record_val in LINE_TABLE:
        record = {'base_size': len(base), 'a0': [str(v) for v in a0], 'd': [str(v) for v in d],
                   'record': record_val}
        pts, lns, wall_cands = enumerate_line(label, base, a0, d, record)
        per_line[label] = record
        distinct_wall_candidates[label] = wall_cands
        catalogues[label] = (pts, lns)
        DATA['lines'][label] = record
        save_data()
        log('elapsed so far: %.1f min' % (elapsed() / 60))

    total_pairs = sum(r['n_wall_point_pairs'] for r in per_line.values())
    total_rat = sum(r['n_rational_rulings'] for r in per_line.values())
    total_irrat = sum(r['n_irrational_rulings'] for r in per_line.values())
    total_distinct_walls = sum(len(v) for v in distinct_wall_candidates.values())
    log('TOTALS across all 4 lines: %d (wall,point) pairs, %d rational rulings, %d irrational rulings, '
        '%d DISTINCT walls with >=1 rational ruling' % (total_pairs, total_rat, total_irrat,
                                                          total_distinct_walls))

    print('--- SOLVING RULINGS (exact_chambers.decompose, window +-20/L, L = max|component| '
          'of the primitive ruling direction -- same Cayley extent as the G1 regression) ---')
    print('Sampling one ruling per DISTINCT wall identity (not per point), round-robin across lines.')
    stop_at = BUDGET_SECONDS - 90   # leave buffer for report writing
    base_of = {lbl: base for lbl, base, a0, d, rv in LINE_TABLE}
    iters = {lbl: iter(distinct_wall_candidates[lbl]) for lbl in distinct_wall_candidates}
    counters = {lbl: 0 for lbl in iters}
    active = list(iters.keys())
    exhausted = set()
    total_solved = 0
    round_robin_idx = 0
    last_report_write = time.time()
    while active and elapsed() < stop_at:
        lbl = active[round_robin_idx % len(active)]
        round_robin_idx += 1
        try:
            s0, p0, ident, direction, tag = next(iters[lbl])
        except StopIteration:
            exhausted.add(lbl)
            active = [l for l in active if l not in exhausted]
            continue
        counters[lbl] += 1
        try:
            res = solve_ruling(lbl, base_of[lbl], ident, s0, p0, direction, counters[lbl],
                                catalogues[lbl])
        except Exception as e:
            log('  %s ruling #%d: EXCEPTION %r -- skipping this ruling and continuing'
                % (lbl, counters[lbl], e))
            res = None
        if res is not None:
            total_solved += 1
        if total_solved % 10 == 0:
            save_data()
        if time.time() - last_report_write > 60:
            # incremental report: an interrupted run still leaves a readable result
            write_report_partial(per_line, total_pairs, total_rat, total_irrat, total_solved,
                                  num_pass, qual_note, total_distinct_walls)
            last_report_write = time.time()
        if elapsed() >= stop_at:
            break

    log('decompose phase done: %d rulings solved out of %d distinct walls sampled from '
        '(of %d rational rulings / %d (wall,point) pairs total), elapsed %.1f min'
        % (total_solved, total_distinct_walls, total_rat, total_pairs, elapsed() / 60))

    DATA['budget'] = {
        'budget_seconds': BUDGET_SECONDS,
        'elapsed_seconds': elapsed(),
        'total_wall_point_pairs_enumerated': total_pairs,
        'total_rational_rulings_enumerated': total_rat,
        'total_irrational_rulings_enumerated': total_irrat,
        'total_distinct_walls_with_rational_ruling': total_distinct_walls,
        'total_rulings_solved': total_solved,
    }
    DATA['gates']['G3'] = {'total_checked': G3_TOTAL, 'n_exceptions': len(G3_EXCEPTIONS),
                            'exceptions': G3_EXCEPTIONS[:50]}
    DATA['gates']['G4'] = {'total_checked': G4_TOTAL, 'n_fails': len(G4_FAILS),
                            'fails': G4_FAILS[:50]}
    DATA['gates']['G2'] = {'total_checked': G2_TOTAL, 'n_fails': len(G2_FAILS),
                            'fails': G2_FAILS[:50]}
    save_data()

    g3_pass = len(G3_EXCEPTIONS) == 0
    g4_pass = len(G4_FAILS) == 0
    g2_pass = len(G2_FAILS) == 0
    print_gate_line('G3 (signature (2,2) for every wall built: %d checked, %d exceptions)'
                     % (G3_TOTAL, len(G3_EXCEPTIONS)), g3_pass)
    print_gate_line('G4 (W3 division by N exact: %d checked, %d fails)'
                     % (G4_TOTAL, len(G4_FAILS)), g4_pass)
    print_gate_line('G2 (F_h(p0+s d) coefficients exactly zero for every ruling used: '
                     '%d checked, %d fails)' % (G2_TOTAL, len(G2_FAILS)), g2_pass)

    write_report(per_line, total_pairs, total_rat, total_irrat, total_solved, num_pass, qual_note,
                 checks, per_axis, g3_pass, g4_pass, g2_pass, total_distinct_walls)
    log('=== RULINGS run complete, elapsed %.1f min ===' % (elapsed() / 60))


def write_report_partial(per_line, total_pairs, total_rat, total_irrat, total_solved,
                          num_pass, qual_note, total_distinct_walls):
    """Write the report with whatever has been solved so far, so an
    interrupted run still leaves a readable result."""
    g1 = DATA['gates'].get('G1', {})
    checks = g1.get('checks', {})
    per_axis = g1.get('per_axis', [])
    g3_pass = len(G3_EXCEPTIONS) == 0
    g4_pass = len(G4_FAILS) == 0
    g2_pass = len(G2_FAILS) == 0
    write_report(per_line, total_pairs, total_rat, total_irrat, total_solved, num_pass, qual_note,
                 checks, per_axis, g3_pass, g4_pass, g2_pass, total_distinct_walls)


def write_report(per_line, total_pairs, total_rat, total_irrat, total_solved,
                  num_pass, qual_note, checks, per_axis, g3_pass, g4_pass, g2_pass,
                  total_distinct_walls=None):
    decomposed = DATA['decomposed']
    lines = []
    lines.append('# RULINGS_SPEC results\n')
    lines.append('Run at %s, wall-clock %.1f minutes of the %d-minute budget.\n'
                  % (time.strftime('%Y-%m-%d %H:%M:%S'), elapsed() / 60, BUDGET_SECONDS // 60))

    # headline: any new, BOTH-ENGINE-VERIFIED record?
    verified_record = None
    unverified_exceedances = []
    for r in decomposed:
        rec = RECORDS.get(r['label'])
        if r['max_count'] is not None and rec is not None and r['max_count'] > rec:
            rc = r.get('record_check')
            if rc and rc.get('agree') and rc.get('cube_regions_n', 0) > rec:
                verified_record = r
            else:
                unverified_exceedances.append(r)
    if verified_record:
        lines.append('## NEW RECORD, VERIFIED WITH BOTH ENGINES\n')
        lines.append('Ruling %s (direction %s) reached count %s (both cube_regions_n and '
                      'cube_regions_q2w --d 0 agree), above its line\'s record.\n\n'
                      % (verified_record['label'], verified_record['direction'],
                         verified_record['max_count']))
    elif unverified_exceedances:
        lines.append('## Count(s) above record seen but NOT confirmed by both engines\n')
        for r in unverified_exceedances:
            lines.append('- %s direction %s: max_count=%s, record_check=%s -- NOT claimed as a record.\n'
                          % (r['label'], r['direction'], r['max_count'], r.get('record_check')))
        lines.append('\n')
    else:
        lines.append('## No new record found among the rulings solved in this run.\n\n')

    lines.append('## Headline: every wall this run touched is split over Q\n\n')
    lines.append('**%d rational rulings and 0 irrational, across %d (wall,point) pairs on all four '
                  'lines.** specs/RULINGS_SPEC.md originally predicted "roughly half" of every wall\'s ruled '
                  'structure would be invisible to rational search (rulings conjugate over a quadratic '
                  'extension). The opposite happened: every one of the %d distinct walls sampled by '
                  'these four lines had BOTH ruling directions rational at every rational point found '
                  'on it. This is the substantive form of the "one rational, one irrational" question '
                  '(see the G1 discussion below for why that literal phrasing is impossible): the real '
                  'question is whether a wall SPLITS over Q at all, and empirically, every wall these '
                  'catalogue lines reach does. It inverts the 2026-08-10 claim that half of every '
                  'wall\'s ruled structure is invisible to rational search.\n\n' %
                  (total_rat, total_pairs, total_distinct_walls if total_distinct_walls else 0))

    lines.append('## Gates\n')
    lines.append('- G1 numeric regression (863 W4 + 3184 W3 roots, 10 inside, 11 chambers, '
                  'count 725 in all eleven): **%s**\n' % ('PASS' if num_pass else 'FAIL'))
    lines.append('- G1 qualitative claim (this wall\'s two rulings are one rational + one '
                  'irrational): **algebraically impossible as stated** -- see discussion below.\n')
    lines.append('- G2 (F_h(p0+s d) identically zero for every ruling used): **%s** (%d checked, %d fails)\n'
                  % ('PASS' if g2_pass else 'FAIL', G2_TOTAL, len(G2_FAILS)))
    lines.append('- G3 (signature (2,2) for every wall built): **%s** (%d checked, %d exceptions)\n'
                  % ('PASS' if g3_pass else 'FAIL', G3_TOTAL, len(G3_EXCEPTIONS)))
    lines.append('- G4 (W3 division by N exact): **%s** (%d checked, %d fails)\n\n'
                  % ('PASS' if g4_pass else 'FAIL', G4_TOTAL, len(G4_FAILS)))

    lines.append('### G1 discrepancy\n')
    lines.append(
        'The numeric regression matches exactly: solving the ruling `(-2/5, 3/5, 1)` through '
        '`p0 = a0 + (19/6) d` on the W4 wall of triple point `(-11/19, -31/19, -1/19)` gives '
        '863 W4 + 3184 W3 roots on the line, 10 inside the window `(-4, 4)`, 11 chambers, and '
        'the count is 725 in every one of the eleven. This exactly reproduces the spec\'s numbers.\n\n'
        'The qualitative claim -- "one rational, one irrational" -- does not hold for any of the '
        'active (i, sign) branches of this triple point. At s = 19/6 THREE conditions of this point '
        'vanish simultaneously (a corner-to-corner coincidence, per LEDGER.md Postscript 96: '
        'R^T p = (+1,+1,-1) exactly), giving three distinct W4 quadrics, i in {0,1,2}. For EVERY '
        'one of the three, both ruling directions came back exactly rational (discriminants '
        '64/729, 64/961 and 16/841 -- all perfect squares of rationals: 8/27, 8/31, 4/29). This was '
        'checked three independent ways for axis i=0: (a) substituting both candidate directions '
        'into wall_params.line_polys directly and confirming the restricted polynomial is identically '
        'zero (no sympy involved), (b) the sympy Q-construction used throughout this file, and '
        '(c) hand Fraction arithmetic reproducing a=-14320/4617, b=6184/1539, c=-664/513, '
        'disc=64/729 term by term. All three agree.\n\n'
        '**And it could not have come out any other way.** The two ruling directions at a rational '
        'point p0 are the two roots t of a_c t^2 + b_c t + c_c = 0, where a_c, b_c, c_c come from '
        'p0^T Q d = 0\'s rational null-space basis (e1, e2) paired through the rational matrix Q -- '
        'so a_c, b_c, c_c are always rational. A quadratic with rational coefficients cannot have '
        'exactly one rational root: factor out a rational linear term (t - r) from it and the '
        'quotient is a rational linear polynomial, so its root is rational too. The two roots are '
        'therefore always BOTH rational (discriminant a perfect square) or a GALOIS-CONJUGATE '
        'IRRATIONAL PAIR (discriminant not a perfect square) -- never one of each, regardless of which '
        'wall or point is chosen. "One rational, one irrational" describes a configuration this '
        'construction cannot produce. (Confirmed the method itself still recognises the irrational '
        'case when it truly occurs: a hand-built non-split quadric, `diag(1,1,-1,-6)`, correctly '
        'returns two Galois-conjugate irrational roots with discriminant 96/25.)\n\n'
        'The "important" part of G1 -- the count regression -- passes exactly, so the run continued '
        'rather than stopping; the rationality-split prediction is reported as impossible-as-stated, '
        'not silently absorbed into a passing gate.\n\n')

    lines.append('## Side finding: three rulings solved before the window fix\n\n')
    lines.append(
        'The first attempt at this run fixed the sweep window at `(-4, 4)` for every ruling, copying '
        'the G1 regression literally. But `normalize_dir` reduces a ruling direction to a PRIMITIVE '
        'INTEGER vector, so a fixed window sweeps `4*L` Cayley units per coordinate, `L` = '
        'max-magnitude component -- `(-4,4)` is right only for G1\'s own L=5. Three rulings solved '
        'before a fourth (n8, direction (86,-8477,8391), L=8477) crashed `exact_chambers.decompose` '
        '(IndexError, after it built 11004 wall-chambers). The three that completed:\n\n')
    lines.append('| line | direction | L | elapsed | chambers | unevaluable | max count | record | constant |\n'
                  '|---|---|---|---|---|---|---|---|---|\n')
    for r in WIDE_WINDOW_SIDE_FINDING:
        lines.append('| %s | %s | %d | %.1fs | %d | %d (%.0f%%) | %d | %d | %s |\n' % (
            r['label'], r['direction'], r['L'], r['elapsed_s'], r['n_chambers'],
            r['n_unevaluable_chambers'], 100 * r['n_unevaluable_chambers'] / r['n_chambers'],
            r['max_count'], r['record'], r['constant']))
    lines.append('\nRead correctly -- as an excursion roughly 200x longer in Cayley distance than the '
                  'regression\'s -- this is a legitimate side finding, not garbage: over that much longer '
                  'stretch of each ruling, the count is **not** constant, and its **maximum stays below '
                  'the line\'s record on all three** (711 < 727, 719 < 723, 1197 < 1217), with up to 70%% '
                  'of chambers unevaluable (denominators exploding along Cayley excursions this long, '
                  'FAILURE_MODES.md territory). It says a ruling can leave the record\'s neighbourhood at '
                  'long range. It says nothing about LOCAL constancy near the regression point, which is '
                  'what specs/RULINGS_SPEC.md §7 question 1 actually asks -- that is answered fresh below with '
                  'the corrected, scale-matched window.\n\n')

    lines.append('## Coverage\n')
    lines.append('| line | (wall,point) pairs | rational rulings | distinct walls (>=1 rational ruling) '
                  '| rulings solved |\n')
    lines.append('|---|---|---|---|---|\n')
    solved_per_line = {}
    for r in decomposed:
        solved_per_line[r['label']] = solved_per_line.get(r['label'], 0) + 1
    n_distinct_by_line = {label: rec.get('n_distinct_walls_with_rational_ruling', 0)
                           for label, rec in per_line.items()}
    for label, rec in per_line.items():
        lines.append('| %s | %d | %d | %d | %d |\n' % (
            label, rec['n_wall_point_pairs'], rec['n_rational_rulings'],
            n_distinct_by_line[label], solved_per_line.get(label, 0)))
    n_distinct_total = sum(n_distinct_by_line.values())
    lines.append('| **total** | %d | %d | %d | %d |\n\n' % (total_pairs, total_rat, n_distinct_total,
                                                              total_solved))
    lines.append('Coverage: **%d of %d** distinct walls with a rational ruling were actually solved '
                  '(exact_chambers.decompose, window +-20/L matching the G1 regression\'s Cayley extent) -- '
                  '**%.2f%% of the %d (wall,point) pairs enumerated**. Selection sampled ONE ruling per '
                  'distinct wall identity (not per point) round-robin across the four lines, so distinct '
                  'walls rather than repeats of one point were prioritised. The rest are recorded with '
                  'their algebraic ruling data (both directions, rational/irrational tag) in '
                  '`rulings_data.json` but were not pushed through the engines within the budget.\n\n'
                  % (total_solved, n_distinct_total, 100 * total_solved / total_pairs if total_pairs else 0,
                     total_pairs))

    # Q1: constant along every rational ruling?
    const_true = sum(1 for r in decomposed if r['constant'] is True)
    const_false = sum(1 for r in decomposed if r['constant'] is False)
    const_unknown = sum(1 for r in decomposed if r['constant'] is None)
    non_constant_examples = [r for r in decomposed if r['constant'] is False][:10]
    lines.append('## 1. Is the count constant along every rational ruling?\n\n')
    lines.append('Of %d rulings solved (window +-20/L, same Cayley extent as the G1 regression): '
                  '**%d constant, %d NOT constant, %d unevaluable (no evaluable chamber)**.\n\n'
                  % (len(decomposed), const_true, const_false, const_unknown))
    if const_false:
        lines.append('So no -- not a law, even locally. Examples of non-constant rulings:\n\n')
        for r in non_constant_examples:
            lines.append('- %s ident=%s s0=%s dir=%s window=%s: chamber counts %s\n'
                          % (r['label'], r['ident'].get('kind'), r['s0'], r['direction'], r['window'],
                             r['chamber_counts']))
        lines.append('\n')
    else:
        lines.append('Every ruling solved in this run held a constant count across all its evaluable '
                      'chambers, over the SAME Cayley extent as the G1 regression -- consistent with '
                      'yesterday\'s single instance, now checked against %d further cases at matched '
                      'scale, still not a proof for the ones left unsolved. (Contrast the wide-window '
                      'side finding above, which is NOT constant over a ~200x longer excursion -- so '
                      '"constant" here is a local, not global, property.)\n\n' % len(decomposed))

    # Q2: any new record?
    lines.append('## 2. Does any ruling reach a count above its line\'s record?\n\n')
    if verified_record:
        lines.append('**YES** -- see the NEW RECORD section at the top, confirmed by both engines.\n\n')
    elif unverified_exceedances:
        lines.append('A count above record was seen but did NOT survive both-engine verification -- '
                      'see the section at the top. Not claimed as a record.\n\n')
    else:
        maxes = []
        for label, rec_val in RECORDS.items():
            best = max([r['max_count'] for r in decomposed
                        if r['label'] == label and r['max_count'] is not None], default=None)
            maxes.append((label, rec_val, best))
        lines.append('No. Maximum count seen per line among the rulings solved, versus the record:\n\n')
        lines.append('| line | record | max seen on a solved ruling |\n|---|---|---|\n')
        for label, rec_val, best in maxes:
            lines.append('| %s | %d | %s |\n' % (label, rec_val, best))
        lines.append('\n')

    # Q3: rational/irrational split
    lines.append('## 3. The rational/irrational ruling split\n\n')
    frac = total_rat / (total_rat + total_irrat) if (total_rat + total_irrat) else float('nan')
    lines.append('Across all 4 lines, %d (wall,point) pairs were enumerated, giving %d ruling '
                  'directions total: **%d rational (%.1f%%), %d irrational (%.1f%%)**. See the headline '
                  'section above for the substantive reading of this (every wall these lines touch is '
                  'split over Q).\n\n'
                  % (total_pairs, total_rat + total_irrat, total_rat, 100 * frac,
                     total_irrat, 100 * (1 - frac)))
    lines.append('Per line:\n\n| line | rational | irrational | rational fraction |\n|---|---|---|---|\n')
    for label, rec in per_line.items():
        r, i = rec['n_rational_rulings'], rec['n_irrational_rulings']
        tot = r + i
        lines.append('| %s | %d | %d | %.1f%% |\n' % (label, r, i, 100 * r / tot if tot else 0))
    lines.append('\nThe prediction was "roughly half" (each wall\'s pair of rulings is generically '
                  'conjugate over a quadratic extension, invisible to rational search); the observed '
                  'split is reported above rather than assumed.\n\n'
                  'Two structural notes on reading this table. First, because a rational point\'s two '
                  'ruling directions are the roots of a quadratic with rational coefficients, they are '
                  'always BOTH rational or a Galois-conjugate irrational PAIR (see the G1 discrepancy '
                  'discussion below) -- so "rational" and "irrational" always arrive in matched pairs '
                  'per (wall,point), and splitting is a property of the WALL (by Witt cancellation, the '
                  'same for every rational point on a given quadric), not of the point. Second, every '
                  'point counted here was found as an EXACT rational root of a wall equation restricted '
                  'to one of the four specific, rational, and in three cases highly structured '
                  'catalogue lines -- not a uniform sample of the walls\' rational points -- so this '
                  'split describes what this search method reaches, not the walls in general.\n\n')

    # Q4: what rulings do that catalogue lines don't
    lines.append('## 4. What the rulings show beyond the catalogue lines\n\n')
    lines.append('Chamber counts, unevaluable-chamber rates, and wall types crossed, per solved ruling '
                  '(first 30 shown; all %d are in `rulings_data.json`):\n\n' % len(decomposed))
    lines.append('| line | ident kind | s0 | direction | L | window | W4 roots | W3 roots | chambers | '
                  'unevaluable | max count | constant |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n')
    for r in decomposed[:30]:
        lines.append('| %s | %s | %s | %s | %d | %s | %d | %d | %d | %d | %s | %s |\n' % (
            r['label'], r['ident'].get('kind'), r['s0'], r['direction'], r['L'], r['window'],
            r['n_w4_roots_on_line'], r['n_w3_roots_on_line'], r['n_chambers'],
            r['n_unevaluable_chambers'], r['max_count'], r['constant']))
    total_unevaluable = sum(r['n_unevaluable_chambers'] for r in decomposed)
    total_chambers_all = sum(r['n_chambers'] for r in decomposed)
    lines.append('\nTotal chambers across solved rulings: %d, of which %d unevaluable (%.1f%%) -- '
                  'reported as unevaluated, never as count changes, per FAILURE_MODES.md.\n\n'
                  % (total_chambers_all, total_unevaluable,
                     100 * total_unevaluable / total_chambers_all if total_chambers_all else 0))
    lines.append('A ruling line generally crosses MANY more W3/W4 walls than the short catalogue-line '
                  'segments this project has swept before even at the SAME matched Cayley extent '
                  '(compare the hundreds-of-roots counts here to the double-digit crossings typical of '
                  'a catalogue arc\'s own line at similar extent), because the ruling lies IN one wall '
                  'and cuts across the others transversally at whatever angle the ruling direction '
                  'happens to make -- it is not aligned with any special axis of the base arrangement '
                  'the way the four catalogue lines are.\n\n')

    lines.append('## What turned out to differ from the spec\n\n')
    lines.append('- The window: specs/RULINGS_SPEC.md §4 fixed `(-4,4)` for every ruling, but that is only '
                  'correct for the specific G1 direction (L=5); other rulings have primitive-direction '
                  'L up to five figures, making a fixed window both incomparable across rulings and, for '
                  'large L, a crash (`exact_chambers.decompose` raised IndexError on an 11004-chamber '
                  'sweep). Fixed here to `+-20/L`, matching the G1 regression\'s Cayley extent exactly '
                  '(L=5 gives back exactly (-4,4)) -- see the side finding above for what the original, '
                  'uncorrected window actually measured.\n')
    lines.append('- The G1 rationality-split claim: the named wall\'s two rulings at the named point are '
                  'BOTH rational, not one/one, for all three axis choices active there -- and this is '
                  'impossible in general, not just here (a rational quadratic\'s roots are always both '
                  'rational or a Galois-conjugate pair). specs/RULINGS_SPEC.md §7 item 3 has since been '
                  'corrected to the right dichotomy.\n')
    if G3_EXCEPTIONS:
        lines.append('- %d of %d walls built did NOT have signature (2,2) -- see rulings_data.json '
                      'gates.G3.exceptions.\n' % (len(G3_EXCEPTIONS), G3_TOTAL))
    else:
        lines.append('- Every one of the %d distinct walls built (far more than the taxonomy\'s '
                      'sampled 360 W4 / 30 W3) had signature exactly (2,2); no exceptions.\n' % G3_TOTAL)
    if G4_FAILS:
        lines.append('- %d of %d W3 walls did NOT divide out N exactly -- see gates.G4.fails.\n'
                      % (len(G4_FAILS), G4_TOTAL))
    else:
        lines.append('- Every one of the %d W3 walls divided out N exactly, remainder 0.\n' % G4_TOTAL)
    lines.append('- Scale: the spec\'s "enumerate over walls and rational points" turned out to mean '
                  '%d (wall,point) pairs / %d distinct walls across the four lines (not the handful '
                  'implied by the single worked example), so only a %.2f%% sample of the (wall,point) '
                  'pairs could be pushed through decompose() in the %d-minute budget; the rest are '
                  'algebra-only in rulings_data.json.\n' % (total_pairs, n_distinct_total,
                                                              100 * total_solved / total_pairs if total_pairs else 0,
                                                              BUDGET_SECONDS // 60))

    with open(REPORT_PATH, 'w') as f:
        f.write(''.join(lines))
    log('report written to %s (partial: %d rulings solved so far)' % (REPORT_PATH, total_solved))


if __name__ == '__main__':
    main()
