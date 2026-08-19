#!/usr/bin/env python3
"""Rank added to the wall Jacobian by the (1,1,1,1) wall type.

`dimension.py` builds every wall condition (Step A "slab" conditions and
Step B's 36-cell triple conditions) from PAIRS and TRIPLES of cubes -- see its
own docstring.  A structurally different codimension-1 wall exists at the
records: four face planes belonging to four DIFFERENT cubes, concurrent at a
point.  No pair/triple construction can express "four planes meet", so
`dimension.py`'s Jacobian is structurally blind to it, and every rank/dimension
figure it has ever produced is a rank computed WITHOUT these rows -- a lower
bound on the true rank, not the rank.

This script measures how much that blind spot costs: for each record n, it
builds the exact gradient of the (1,1,1,1) concurrence condition at every real
quadruple-point (from check_4cube_walls.json, already enumerated -- this script
does not re-enumerate concurrency, only differentiates the condition at the
points already found), adds those rows to the existing <=3-cube Jacobian, and
reports

    delta = rank(old rows + new rows) - rank(old rows)

i.e. exactly the rank the (1,1,1,1) walls add on top of what dimension.py could
already see.  It is proved that delta <= 1 (lineality at n=6 is 1 and cannot go
negative under added rows), so delta >= 2 at any n is not a valid result -- it
is a signal the construction below has a bug, and is reported as such rather
than as a number.

THE CONDITION.  A face plane of cube c has equation m.x = 1 where m is a signed
column of cube c's rotation matrix (6 planes per cube).  Four planes with
normals m1..m4 are concurrent at a common point iff

    det [[m1,-1],[m2,-1],[m3,-1],[m4,-1]]   (each mi a row [mix,miy,miz], the
                                              4th column all -1s)  ==  0.

That determinant, as a function of the free Cayley coordinates, IS the wall
condition; its gradient at the record is the row added to the Jacobian.

WHICH four planes: at each of the 12 known quadruple-points (identical across
n, since they involve only the frozen BASE cubes 0..4 and check_4cube_walls.py
already verified there are exactly 12 for every n it covers) and its 4 named
cubes, the plane through that point is found by exact-rational dot product
m.P == 1 -- never floats.  Every point/cube pair checked here has exactly one
matching signed normal (verified separately), so there is one condition per
point, not several from a combinatorial explosion; the code still handles the
general case (a cube touching a point along an edge/corner would offer more
than one matching normal, and every combination is then a separate condition)
because nothing rules it out a priori.

PERFORMANCE NOTE.  sympy's Matrix.det() on a 4x4 matrix whose 18-ish entries
are unevaluated rational FUNCTIONS in up to 9 free Cayley variables (from
cayley_matrix's 1/(1+x^2+y^2+z^2) denominators) does not finish in a reasonable
time for these records; timed out past 120s on a single n=7 point.  The
determinant used here is instead differentiated by JACOBI'S FORMULA, an exact
algebraic identity (not an approximation):

    d(det M)/dv = sum_{i,j} cofactor_{ij}(M) * dM_{ij}/dv

Only the ROW belonging to the cube that owns v ever depends on v, so this
reduces to a dot of one cofactor-matrix row (computed once, numerically, from
the already-substituted 4x4 matrix -- fast) against that row's 3 derivatives
(computed symbolically, on a single 3x1 column of a single cube's rotation
matrix -- cheap).  Cross-checked against fully independent single-variable
symbolic differentiation (freeze every other coordinate, differentiate the
resulting single-variable determinant analytically) at one n=7 point; agreed
exactly (-300/2527).  Mathematically this is the identical gradient the spec's
naive `sp.diff(det(M), v).subs(subs)` would produce -- only the computation
path differs, not the result.
"""
import itertools
import json
import os
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dimension as D

BASE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
REC = {5: BASE, 6: BASE + [(7, 14, 1, -5)]}
REC[7] = REC[6] + [(4, -3, -4, -4)]
REC[8] = REC[7] + [(24, -24, 24, -61)]
REC[9] = REC[8] + [(56, 56, 55, 56)]

QUAD_JSON = os.path.join(HERE, 'check_4cube_walls.json')
OUT_JSON = os.path.join(HERE, 'quad_walls.json')
LOG_PATH = os.path.join(HERE, 'quad_walls.log')

_LOG_FH = None


def log(msg):
    print(msg, flush=True)
    if _LOG_FH is not None:
        _LOG_FH.write(msg + '\n')
        _LOG_FH.flush()


def _norm(g):
    """dedupe key for a gradient row, invariant under scaling by any nonzero
    scalar (copied verbatim from the task spec's reference snippet)."""
    piv = next((x for x in g if x != 0), None)
    return tuple(str(x / piv) for x in g) if piv is not None else None


def dedupe_rows(rows):
    seen = set()
    out = []
    for g in rows:
        key = _norm(g)
        if key is None or key in seen:
            continue
        seen.add(key)
        out.append(g)
    return out


def load_quad_points(n, data):
    """The 12 quadruple-points, identical across n (BACKGROUND says keys run
    "5".."9"; the file on disk in fact only has "7","8","9" -- but the points
    involve only cubes 0..4 (the frozen BASE cubes, present unchanged at every
    n >= 5) and are byte-identical across the keys that ARE present, so the
    n=7 (or any present) list is reused for n=6.  Logged, not silent."""
    key = str(n)
    if key in data:
        return data[key]['quad'], key
    for fallback in ('7', '8', '9', '6', '5'):
        if fallback in data:
            log('  [n=%d] no "%s" key in %s -- reusing quad list from key "%s" '
                '(points involve only cubes 0..4, identical across n=7,8,9 by '
                'direct comparison)' % (n, key, os.path.basename(QUAD_JSON), fallback))
            return data[fallback]['quad'], fallback
    raise RuntimeError('no quad data available in %s' % QUAD_JSON)


def cube_owner(vi):
    """vars_[vi] belongs to cube 1 + vi // 3 (D.frames' own convention)."""
    return 1 + vi // 3


def cube_signed_normals(Rs, subs, cube_idx):
    """The 6 signed face normals of cube_idx, evaluated exactly at the record
    (world frame, columns of Rs[cube_idx].subs(subs)); each as (k, sign, vec)."""
    Rc = Rs[cube_idx].subs(subs)
    out = []
    for k in range(3):
        col = [Rc[r, k] for r in range(3)]
        out.append((k, 1, col))
        out.append((k, -1, [-x for x in col]))
    return out


def matching_normals(normals, P):
    """signed normals (k, sign) whose plane m.x = 1 passes exactly through P."""
    return [(k, sgn) for (k, sgn, col) in normals
            if sum(col[i] * P[i] for i in range(3)) == 1]


def combo_gate_and_gradient(combo, Rs, subs, vars_):
    """combo: list of (cube, k, sign), one per plane. Returns (gate_ok, det_value,
    grad) where grad is a list of Fraction, one per var, via Jacobi's formula."""
    rows_num, rows_sym = [], []
    for (c, k, sgn) in combo:
        col_sym = [Rs[c][r, k] for r in range(3)]
        m_sym = [sgn * x for x in col_sym]
        rows_sym.append(m_sym + [-1])
        col_num = [Rs[c][r, k].subs(subs) for r in range(3)]
        m_num = [sgn * x for x in col_num]
        rows_num.append(m_num + [-1])
    M_num = sp.Matrix(rows_num)
    det_val = M_num.det()
    if det_val != 0:
        return False, det_val, None

    C = M_num.cofactor_matrix()
    combo_cube_to_rows = {}
    for i, (c, k, sgn) in enumerate(combo):
        combo_cube_to_rows.setdefault(c, []).append(i)

    grad = []
    for vi, v in enumerate(vars_):
        oc = cube_owner(vi)
        rows_i = combo_cube_to_rows.get(oc)
        if not rows_i:
            grad.append(F(0))
            continue
        total = sp.Integer(0)
        for i in rows_i:
            drow = [sp.diff(rows_sym[i][j], v).subs(subs) for j in range(4)]
            total += sum(C[i, j] * drow[j] for j in range(4))
        grad.append(F(sp.Rational(total)))
    return True, det_val, grad


def process_n(n, data):
    quats = REC[n]
    D.set_field(0)
    D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    ncols = 3 * (len(quats) - 1)
    vars_ = sp.symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, quats[0])
    subs = {v: sp.Rational(p.numerator, p.denominator)
            for v, p in zip(vars_, pt)}

    # --- existing (<=3-cube) walls, for the rank comparison ---------------
    tight, _loose = D.cached_conditions(
        Rs, len(quats), vars_, pt, D.quats_of(pt, quats[0]), quats[0])
    good = [t for t in tight if not t['degenerate']]
    rows_old = dedupe_rows([t['grad'] for t in good])
    ns_old = D.nullspace(rows_old, ncols)
    rank_old = ncols - len(ns_old)
    lineality_old = len(ns_old)

    # --- the (1,1,1,1) quad-wall conditions --------------------------------
    quad, used_key = load_quad_points(n, data)
    n_conditions = 0
    n_zero_grad = 0
    new_rows = []
    for pi, entry in enumerate(quad):
        P = [sp.Rational(s) for s in entry['point']]
        cubes = entry['cubes']
        per_cube = []
        for c in cubes:
            normals = cube_signed_normals(Rs, subs, c)
            m = matching_normals(normals, P)
            if not m:
                raise RuntimeError(
                    'n=%d point %d: cube %d has NO face plane through P=%s -- '
                    'normal-matching is broken' % (n, pi, c, P))
            per_cube.append([(c, k, sgn) for (k, sgn) in m])
        for combo in itertools.product(*per_cube):
            n_conditions += 1
            gate_ok, det_val, grad = combo_gate_and_gradient(
                list(combo), Rs, subs, vars_)
            if not gate_ok:
                raise RuntimeError(
                    'n=%d point %d combo %s: GATE FAILED, det = %s '
                    '(expected exactly 0) -- wrong planes, stopping'
                    % (n, pi, combo, det_val))
            if all(x == 0 for x in grad):
                n_zero_grad += 1
                continue
            new_rows.append(grad)

    # --- rank with the quad-wall rows added ---------------------------------
    rows_new = rows_old + new_rows
    ns_new = D.nullspace(rows_new, ncols)
    rank_new = ncols - len(ns_new)
    lineality_new = len(ns_new)
    delta = rank_new - rank_old

    return {
        'n': n,
        'quad_key_used': used_key,
        'ambient': ncols,
        'conditions_built': n_conditions,
        'zero_gradient': n_zero_grad,
        'rank_old': rank_old,
        'lineality_old': lineality_old,
        'rank_new': rank_new,
        'lineality_new': lineality_new,
        'delta': delta,
    }


def main():
    global _LOG_FH
    _LOG_FH = open(LOG_PATH, 'w')
    try:
        with open(QUAD_JSON) as fh:
            data = json.load(fh)

        results = {}
        prev_delta = None
        for n in (6, 7, 8, 9):
            log('=== n=%d ===' % n)
            r = process_n(n, data)
            results[str(n)] = r
            log('n=%d: conditions_built=%d zero_gradient=%d '
                'rank_old=%d rank_new=%d ambient=%d '
                'lineality_old=%d lineality_new=%d delta=%d'
                % (r['n'], r['conditions_built'], r['zero_gradient'],
                   r['rank_old'], r['rank_new'], r['ambient'],
                   r['lineality_old'], r['lineality_new'], r['delta']))

            if r['delta'] >= 2:
                log('  *** ORACLE VIOLATION: delta = %d >= 2 at n=%d. '
                    'Proved bound is delta <= 1. THIS CODE IS WRONG. ***'
                    % (r['delta'], n))
            if prev_delta is not None and r['delta'] > prev_delta:
                log('  *** MONOTONICITY VIOLATION: delta(%d)=%d > delta(prev)=%d; '
                    'expected delta(6) >= delta(7) >= delta(8) >= delta(9). ***'
                    % (n, r['delta'], prev_delta))
            prev_delta = r['delta']

        with open(OUT_JSON, 'w') as fh:
            json.dump(results, fh, indent=1)

        log('\n=== SUMMARY ===')
        for n in (6, 7, 8, 9):
            r = results[str(n)]
            log('n=%d: %d conditions (%d zero-gradient) | rank %d -> %d of %d '
                '(lineality %d -> %d) | delta = %d'
                % (n, r['conditions_built'], r['zero_gradient'],
                   r['rank_old'], r['rank_new'], r['ambient'],
                   r['lineality_old'], r['lineality_new'], r['delta']))
    finally:
        _LOG_FH.close()
        _LOG_FH = None


if __name__ == '__main__':
    main()
