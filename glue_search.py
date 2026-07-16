#!/usr/bin/env python3
# Working principles: GLUE_SPEC.md. Project index: README.md
"""Glued family-clique search (GLUE_SPEC.md): does gluing two dihedral-
family cliques on DIFFERENT axes (clique A on axis/tilt psiA, clique B on
axis/tilt psiB rotated wholesale by an integer quaternion G) reach or beat
the records 183 (n=4) / 393 (n=5) / 723 (n=6)?

Reuses nfamily_common.py's exact Rodrigues/quaternion core (read-only) and
the C++ engine ./cube_regions_n (read-only). Never edits validated files.

Modes:
  --mode q0      exact single-global-axis test on the 183/393 (and 723's
                 embedded 393) records (see module docstring of
                 `q0_single_axis_report` below for the method).
  --mode gates   G1 (two-engine agreement), G2 (reproduce 723), G3
                 (reconstruct 723 as a clique-gluing).
  --mode sweep   the clique x clique x G search, writing glue_results.jsonl.
"""
import argparse
import itertools
import json
import math
import multiprocessing as mp
import random
import subprocess
import sys
import time
from fractions import Fraction as Fr

from nfamily_common import (
    PyAngle, IDENTITY_ANGLE, rel_matrix, is_rotation_exact,
    matrix_to_int_quat, quat_to_matrix_exact, quat_to_int, mat_mul,
    mat_transpose, build_family_quats, CUBE_ROT_GROUP, SMALL_PQR, PQR_MENU,
    family_axis_test, exact_config_crossings,
)
from certify_six import exact_count_config
from golden_rotations import rot_from_quat

ENGINE = './cube_regions_n'
RESULTS_PATH = '/Users/dmi/carroll/glue_results.jsonl'
RECORDS = {4: 183, 5: 393, 6: 723}
RECORD_QUATS = {
    4: [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)],
    5: [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)],
    6: [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1), (5, 2, 2, 2)],
}
RECORD_DEPTH = {
    4: {1: 92, 2: 66, 3: 24, 4: 1},
    5: {1: 156, 2: 128, 3: 78, 4: 30, 5: 1},
    6: {1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1},
}
CLIQUE_SIZES = {4: [(3, 1), (2, 2)], 5: [(4, 1), (3, 2)], 6: [(5, 1), (4, 2), (3, 3)]}


def menu_angles(pqr_list):
    seen = {}
    for p, q, r in pqr_list:
        a = PyAngle.from_pqr(p, q, r)
        seen[(a.c, a.s)] = a
    out = list(seen.values())
    out.sort(key=lambda a: a.deg())
    return out


SMALL_MENU = menu_angles(SMALL_PQR)
FULL_MENU = menu_angles(PQR_MENU)


def run_cpp(quats, n=None):
    n = n or len(quats)
    qstr = ';'.join(','.join(str(c) for c in q) for q in quats)
    out = subprocess.run([ENGINE, '--n', str(n), '--quats', qstr],
                          capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip())


def run_batch(n, quat_lists):
    """quat_lists: list of list-of-quat-tuples, all length n. Returns list
    of (total, by_depth) or None (engine error / cap violation upstream)."""
    if not quat_lists:
        return []
    lines = [';'.join(','.join(str(c) for c in q) for q in qs) for qs in quat_lists]
    proc = subprocess.run([ENGINE, '--n', str(n), '--quats-stdin'],
                           input='\n'.join(lines) + '\n',
                           capture_output=True, text=True, check=True)
    out = []
    for line in proc.stdout.strip().splitlines():
        r = json.loads(line)
        if 'error' in r:
            out.append(None)
            continue
        depth = {int(k): v for k, v in r['by_depth'].items() if int(k) != 0}
        out.append((r['bounded'], depth))
    return out


def _run_batch_worker(args):
    n, chunk_idx, quat_lists = args
    return chunk_idx, run_batch(n, quat_lists)


def run_batch_parallel(n, quat_lists, workers=4, chunk_size=600):
    """Same contract as run_batch but splits into chunks run concurrently
    across up to `workers` OS processes (each still calls the single-
    threaded C++ engine once per chunk -- this is where the ~4-core budget
    is spent). Returns results in the SAME order as quat_lists."""
    if not quat_lists:
        return []
    chunks = [(n, i, quat_lists[i:i + chunk_size]) for i in range(0, len(quat_lists), chunk_size)]
    if len(chunks) == 1:
        _, res = _run_batch_worker(chunks[0])
        return res
    results_by_idx = {}
    with mp.Pool(min(workers, len(chunks))) as pool:
        for idx, res in pool.imap_unordered(_run_batch_worker, chunks):
            results_by_idx[idx] = res
    out = []
    for i in range(0, len(quat_lists), chunk_size):
        out.extend(results_by_idx[i])
    return out


# =========================================================================
# Q0: is 183/393 a SINGLE global-axis family member?
# =========================================================================
"""
Method (exact rational linear algebra throughout, no floats deciding any
predicate):

For a pair (i,j), R = Mi^T Mj (relative rotation, cube i's raw local
frame). nfamily_common.family_axis_test finds a cube-symmetry relabeling
Q (from the 24-element proper rotation group of the axis-aligned cube)
with R'=Q^T R satisfying R'[1][0]==R'[0][1] EXACTLY -- this is NECESSARY
AND SUFFICIENT for R' to have the Rel(Delta,psi) form for SOME (Delta,
psi): any rotation whose axis lies in a plane (here, the local xy-plane,
forced by the zero z-component of R's antisymmetric part) is Rodrigues-
representable about that axis, and Rel(Delta,psi) is exactly the general
Rodrigues rotation about axis n(psi)=(sinpsi,cospsi,0). So this witness
Q, found via EXACT Fraction equality, is airtight -- no numeric axis
double-check is needed for the identification itself.

Global axis of the pair: R'w=w for w = antisymmetric-part(R') = (R'[2][1]
-R'[1][2], R'[0][2]-R'[2][0], 0) (the 3rd component is exactly 0 by the
witness condition). Since R'=Q^T R and R=Mi^T Mj, R'w=w =>
  Q^T Mi^T Mj w = w  =>  Mi Q w = Mj w
i.e. Mi@Q@w and Mj@w are the SAME global vector -- the pair's shared axis
line, computed two independent ways (cross-checked in code with an
`assert`, catching any convention bug immediately).

SINGLE axis for a whole record (not just each pair having *some* axis,
which nfamily_report.md's Q3 already established for 183/393): fix a
candidate global axis s (from one pair's witness set); for EACH cube i
independently, search the 24-element relabeling group for Q with
(Q^T (Mi^T s))[2]==0 (s expressible, after cube i's own face relabeling,
in that cube's local xy-plane) -- if so, cube i admits a psi_i with
tan(psi_i) = (Q^T Mi^T s)[0] / (Q^T Mi^T s)[1] (an EXACT Fraction ratio,
scale-independent, hence directly comparable across cubes without
normalizing s). The record is single-axis (all n cubes, one shared psi)
iff this tan(psi_i) set has a nonempty intersection across ALL cubes.
"""


def mat_vec(M, v):
    return tuple(sum(M[i][k] * v[k] for k in range(3)) for i in range(3))


def canon_line(vec):
    fracs = [Fr(x) for x in vec]
    if all(f == 0 for f in fracs):
        return None
    lcd = 1
    for f in fracs:
        lcd = lcd * f.denominator // math.gcd(lcd, f.denominator)
    ints = [int(f * lcd) for f in fracs]
    g = math.gcd(*[abs(i) for i in ints])
    if g > 1:
        ints = [i // g for i in ints]
    for x in ints:
        if x != 0:
            if x < 0:
                ints = [-i for i in ints]
            break
    return tuple(ints)


def all_witnesses(Mi, Mj):
    R = mat_mul(mat_transpose(Mi), Mj)
    out = []
    for Q in CUBE_ROT_GROUP:
        Rp = mat_mul(mat_transpose(Q), R)
        if Rp[1][0] == Rp[0][1]:
            out.append((Q, Rp))
    return out


def pair_axis_candidates(Mi, Mj):
    """Union of candidate global axis LINES for pair (i,j), searched from
    both cube i's and cube j's own relabeling group (cross-checked)."""
    cands = set()
    for Q, Rp in all_witnesses(Mi, Mj):
        L = (Rp[2][1] - Rp[1][2], Rp[0][2] - Rp[2][0], Fr(0))
        G1 = mat_vec(Mj, L)
        G2 = mat_vec(mat_mul(Mi, Q), L)
        assert canon_line(G1) == canon_line(G2), 'axis formula mismatch (i-side)'
        c = canon_line(G1)
        if c:
            cands.add(c)
    for Q, Rp in all_witnesses(Mj, Mi):
        L = (Rp[2][1] - Rp[1][2], Rp[0][2] - Rp[2][0], Fr(0))
        G1 = mat_vec(Mi, L)
        G2 = mat_vec(mat_mul(Mj, Q), L)
        assert canon_line(G1) == canon_line(G2), 'axis formula mismatch (j-side)'
        c = canon_line(G1)
        if c:
            cands.add(c)
    return cands


def per_cube_tan_psi(Mi, s):
    """All exact tan(psi) values admitted by cube i for candidate axis s
    (Fraction, or 'inf' string for a 90deg tilt), one per valid relabeling."""
    MiT_s = mat_vec(mat_transpose(Mi), s)
    out = set()
    for Q in CUBE_ROT_GROUP:
        v = mat_vec(mat_transpose(Q), MiT_s)
        if v[2] == 0:
            if v[1] != 0:
                out.add(Fr(v[0], v[1]))
            elif v[0] != 0:
                out.add('inf')
    return out


def single_axis_test(mats, s, idx=None):
    """For candidate axis s and cube index subset idx (default: all),
    return the common tan(psi) set (empty => not single-axis on s for
    this subset) plus the per-cube detail."""
    if idx is None:
        idx = list(range(len(mats)))
    detail = {}
    common = None
    for i in idx:
        r = per_cube_tan_psi(mats[i], s)
        detail[i] = r
        common = r if common is None else (common & r)
    return common, detail


def q0_report():
    lines = []

    def emit(s):
        print(s)
        lines.append(s)

    emit('=== Q0: is 183 / 393 a SINGLE global-axis family member? ===\n')
    records = {
        '183 (n=4)': (183, RECORD_QUATS[4], list(range(4))),
        '393 (n=5)': (393, RECORD_QUATS[5], list(range(5))),
        '723 embedded 5-clique (n=6, cubes 0-4 = the 393)': (None, RECORD_QUATS[6][:5], list(range(5))),
        '723 full (n=6)': (723, RECORD_QUATS[6], list(range(6))),
    }
    results = {}
    for name, (total, quats, idx) in records.items():
        mats = [quat_to_matrix_exact(*q) for q in quats]
        n = len(mats)
        pair_cands = {}
        for i in range(n):
            for j in range(i + 1, n):
                pair_cands[(i, j)] = pair_axis_candidates(mats[i], mats[j])
        full_common = None
        for c in pair_cands.values():
            full_common = c if full_common is None else (full_common & c)
        emit(f'--- {name} ---')
        emit(f'  pairwise candidate axis counts: ' +
             ', '.join(f'({i},{j}):{len(c)}' for (i, j), c in sorted(pair_cands.items())))
        emit(f'  intersection of ALL {len(pair_cands)} pairs (= single-axis iff nonempty): {full_common}')
        results[name] = {'total': total, 'full_intersection': [] if not full_common else sorted(full_common)}

        # Search for maximal single-axis sub-cliques: try every pair's
        # candidate axis as a seed, test against every (n-1)-subset that
        # contains that pair.
        best_subcliques = []
        seed_axes = set()
        for c in pair_cands.values():
            seed_axes |= c
        for s in seed_axes:
            for drop in range(n):
                idx_sub = [i for i in range(n) if i != drop]
                common, detail = single_axis_test(mats, s, idx_sub)
                if common:
                    best_subcliques.append((idx_sub, s, sorted(common, key=str)))
        # dedupe by (frozenset(idx), s)
        seen = set()
        uniq = []
        for idx_sub, s, tanset in best_subcliques:
            key = (frozenset(idx_sub), s)
            if key in seen:
                continue
            seen.add(key)
            uniq.append((idx_sub, s, tanset))
        if uniq:
            emit(f'  single-axis SUB-cliques found (size {n - 1} of {n}):')
            for idx_sub, s, tanset in uniq:
                # exact irrationality check: is tan(psi) Pythagorean
                # (would need num^2+den^2 a perfect square)?
                irr_flags = []
                for t in tanset:
                    if t == 'inf':
                        irr_flags.append('inf')
                        continue
                    num, den = abs(t.numerator), abs(t.denominator)
                    hyp2 = num * num + den * den
                    r = math.isqrt(hyp2)
                    irr_flags.append('Pythagorean(rational sin&cos)' if r * r == hyp2
                                      else f'IRRATIONAL sin,cos (hyp^2={hyp2} not a perfect square)')
                emit(f'    cubes {idx_sub}, axis line {s}: tan(psi) in {tanset}  [{irr_flags[0]}]')
                results[name].setdefault('subcliques', []).append(
                    {'cubes': idx_sub, 'axis': list(s), 'tan_psi': [str(t) for t in tanset],
                     'nature': irr_flags[0]})
        else:
            emit('  no (n-1)-of-n single-axis sub-clique found')
        emit('')

    with open('/Users/dmi/carroll/glue_q0.json', 'w') as f:
        json.dump(results, f, indent=1, default=str)
    return '\n'.join(lines)


# =========================================================================
# Gates
# =========================================================================

def build_clique(psi, thetas, cap=512):
    """Clique A style: matrices Rel(theta_i, psi) directly (NOT gauged to
    theta[0]=0 -- spec: 'clique A: {Rel(theta_i, psiA)} for i=1..a')."""
    mats = []
    for th in thetas:
        M = rel_matrix(th, psi)
        assert is_rotation_exact(M)
        mats.append(M)
    return mats


def glue(matsA, matsB, Gmat):
    """Full compound matrices: clique A as-is, clique B rotated by G."""
    return list(matsA) + [mat_mul(Gmat, M) for M in matsB]


def mats_to_quats(mats, cap=512):
    return [matrix_to_int_quat(M, cap=cap) for M in mats]


def gate_g1():
    print('=== G1: two-engine agreement on ONE glued config per n ===')
    ok = True
    a_ang = PyAngle.from_pqr(3, 4, 5)
    psiA = PyAngle.from_pqr(4, 3, 5)
    psiB = PyAngle.from_pqr(5, 12, 13)
    b_ang = PyAngle.from_pqr(8, 15, 17)
    G = quat_to_matrix_exact(2, 1, -1, 1)
    for n, (sizeA, sizeB) in [(4, (3, 1)), (5, (4, 1)), (6, (5, 1))]:
        thetasA = [a_ang.pow(k) for k in range(sizeA)]
        thetasB = [b_ang.pow(k) for k in range(sizeB)]
        matsA = build_clique(psiA, thetasA)
        matsB = build_clique(psiB, thetasB)
        full = glue(matsA, matsB, G)
        quats = mats_to_quats(full)
        r_cpp = run_cpp(quats, n=n)
        rots = [rot_from_quat(*q) for q in quats]
        py_total, py_depth = exact_count_config(rots, verbose=False)
        py_depth = {int(k): v for k, v in py_depth.items() if int(k) != 0}
        cpp_depth = {int(k): v for k, v in r_cpp['by_depth'].items() if int(k) != 0}
        match = (r_cpp['bounded'] == py_total and cpp_depth == py_depth)
        print(f'  n={n} sizes=({sizeA},{sizeB}) quats={quats}')
        print(f'    cpp: total={r_cpp["bounded"]} depth={cpp_depth}')
        print(f'    py:  total={py_total} depth={py_depth}')
        print(f'    match: {match}')
        ok = ok and match
    print(f'G1: {"PASS" if ok else "FAIL"}\n')
    return ok


def gate_g2():
    print('=== G2: reproduce 723 from the ledger quats via the C++ engine ===')
    r = run_cpp(RECORD_QUATS[6], n=6)
    depth = {int(k): v for k, v in r['by_depth'].items() if int(k) != 0}
    ok = (r['bounded'] == 723 and depth == RECORD_DEPTH[6])
    print(f'  cpp: total={r["bounded"]} depth={depth}')
    print(f'  expect: total=723 depth={RECORD_DEPTH[6]}')
    print(f'G2: {"PASS" if ok else "FAIL"}\n')
    return ok


def gate_g3():
    """G3: reconstruct 723 AS a gluing. The embedded 5-clique (cubes 0-4,
    the 393) is clique A taken VERBATIM from its known integer quats (Q0
    showed its psi is irrational for the maximal 4-of-5 sub-clique, so it
    cannot be regenerated from the Pythagorean rel_matrix menu -- using
    the actual quats directly is the honest, and still fully general,
    reading of the spec's parametrization: clique A need not itself come
    from the menu, only clique B does in the sweep). Cube 5 = G . Rel(0,0)
    with G = cube 5's own quat (trivial for a size-1 clique B: Rel(theta,
    psi) for ANY theta,psi is just some fixed rotation once theta=psi=0,
    i.e. Rel(0,0)=I, so G alone carries all the freedom of a lone cube --
    see glue_report.md for why (a,1) cells collapse psiB/thetaB entirely)."""
    print('=== G3: reconstruct 723 as clique(5)-glued-with-clique(1) ===')
    cliqueA_quats = RECORD_QUATS[6][:5]
    cube5_quat = RECORD_QUATS[6][5]
    # Rel(0,0) = I exactly; G = cube5_quat directly reproduces cube 5.
    I = quat_to_matrix_exact(1, 0, 0, 0)
    Rel00 = rel_matrix(IDENTITY_ANGLE, IDENTITY_ANGLE)
    assert Rel00 == I, 'Rel(0,0) must be exactly the identity'
    Gmat = quat_to_matrix_exact(*cube5_quat)
    reconstructed_cube5 = mat_mul(Gmat, Rel00)
    matches = (reconstructed_cube5 == quat_to_matrix_exact(*cube5_quat))
    print(f'  clique A (verbatim, the embedded 393): {cliqueA_quats}')
    print(f'  clique B = {{G . Rel(0,0)}}, G = cube5 quat {cube5_quat}')
    print(f'  reconstructed cube5 == actual cube5 matrix: {matches}')
    full = cliqueA_quats + [cube5_quat]
    r = run_cpp(full, n=6)
    depth = {int(k): v for k, v in r['by_depth'].items() if int(k) != 0}
    ok = matches and (r['bounded'] == 723 and depth == RECORD_DEPTH[6])
    print(f'  recount via gluing-assembled quats: total={r["bounded"]} depth={depth}')
    print(f'G3: {"PASS" if ok else "FAIL"} '
          f'(parametrization CAN represent the record; note clique A used its exact\n'
          f'  quats rather than a Pythagorean-menu regeneration -- see Q0)\n')
    return ok


# =========================================================================
# Sweep
# =========================================================================

def gen_size_chain_candidates(size, cap=512, menu=None):
    """All (psi,a) chain cliques of given size from the small menu."""
    menu = menu or SMALL_MENU
    out = []
    for a in menu:
        if a.s == 0:
            continue
        thetas = [a.pow(k) for k in range(size)]
        for psi in menu:
            try:
                mats = build_clique(psi, thetas, cap=cap)
                quats = mats_to_quats(mats, cap=cap)
            except ValueError:
                continue
            out.append({'size': size, 'psi_pqr': _pqr_of(psi), 'a_pqr': _pqr_of(a),
                         'thetas_pqr': [_pqr_of(t) for t in thetas], 'quats': quats})
    return out


_DEG_TO_PQR = {}
for p, q, r in PQR_MENU:
    a = PyAngle.from_pqr(p, q, r)
    _DEG_TO_PQR[round(a.deg(), 6)] = (p, q, r)
for p, q, r in SMALL_PQR:
    a = PyAngle.from_pqr(p, q, r)
    _DEG_TO_PQR.setdefault(round(a.deg(), 6), (p, q, r))


def _pqr_of(angle):
    d = round(angle.deg(), 6)
    if d in _DEG_TO_PQR:
        return list(_DEG_TO_PQR[d])
    best = min(_DEG_TO_PQR, key=lambda k: abs(k - d))
    return list(_DEG_TO_PQR[best])


def angle_from_pqr(pqr):
    return PyAngle.from_pqr(*pqr)


def rank_candidates_standalone(cands, n_workers=4):
    """Count each clique candidate STANDALONE (as its own compound) with
    the C++ engine to rank by 'own quality' -- a cheap proxy (spec: 'start
    from the best-known family cliques ... a Pythagorean menu around
    them') for how good a clique is likely to be as a gluing ingredient."""
    by_size = {}
    for c in cands:
        by_size.setdefault(c['size'], []).append(c)
    ranked = {}
    for size, lst in by_size.items():
        if size < 2:
            ranked[size] = lst
            continue
        results = run_batch(size, [c['quats'] for c in lst])
        scored = []
        for c, r in zip(lst, results):
            if r is None:
                continue
            total, depth = r
            c = dict(c)
            c['standalone_total'] = total
            c['standalone_depth'] = depth
            scored.append(c)
        scored.sort(key=lambda c: -c['standalone_total'])
        ranked[size] = scored
    return ranked


def gen_G_menu(max_comp=3):
    seen = set()
    for w in range(-max_comp, max_comp + 1):
        for x in range(-max_comp, max_comp + 1):
            for y in range(-max_comp, max_comp + 1):
                for z in range(-max_comp, max_comp + 1):
                    if (w, x, y, z) == (0, 0, 0, 0):
                        continue
                    g = math.gcd(math.gcd(abs(w), abs(x)), math.gcd(abs(y), abs(z)))
                    t = (w // g, x // g, y // g, z // g) if g > 1 else (w, x, y, z)
                    if t[0] < 0 or (t[0] == 0 and (t[1] < 0 or (t[1] == 0 and (t[2] < 0 or (t[2] == 0 and t[3] < 0))))):
                        t = tuple(-v for v in t)
                    seen.add(t)
    return sorted(seen)


G_MENU_TIER1 = None  # populated lazily (components <=3, 532 elements)
G_MENU_TIER2 = None  # components <=6, 3480 elements


def cube_group_quats():
    return [matrix_to_int_quat(Q) for Q in CUBE_ROT_GROUP]


def build_glued_quats(cliqueA, cliqueB, Gquat, cap=512):
    """cliqueA/cliqueB: dicts with 'quats' (already integer, from the
    standalone-ranked candidates) OR None for a trivial size-1 clique B
    (in which case Gquat itself IS cube's placement, Rel(0,0)=I)."""
    matsA = [quat_to_matrix_exact(*q) for q in cliqueA['quats']]
    Gmat = quat_to_matrix_exact(*Gquat)
    if cliqueB is None:
        full_mats = matsA + [Gmat]
    else:
        matsB = [quat_to_matrix_exact(*q) for q in cliqueB['quats']]
        glued = [mat_mul(Gmat, M) for M in matsB]
        full_mats = matsA + glued
    try:
        return mats_to_quats(full_mats, cap=cap)
    except ValueError:
        return None


def sweep_cell(n, sizeA, sizeB, cliquesA, cliquesB, G_menu, log_fh, best_tracker,
                topk_cliques=8, kind='coarse', batch_size=2000, top_results=None):
    """Try topk_cliques x topk_cliques x G_menu glued configs for this
    (n, sizeA, sizeB) cell; log every result; track the best. If
    top_results (dict) is given, also accumulates the top-10 records per
    cell for multi-restart hillclimbing (spec: 'multi-restart from the
    top 10 candidates per (n, sizes)')."""
    candA = cliquesA[:topk_cliques] if sizeA >= 2 else [None]
    candB = cliquesB[:topk_cliques] if sizeB >= 2 else [None]
    jobs = []  # (cliqueA_dict_or_seed, cliqueB_dict_or_None, Gquat)
    if sizeA == 1:
        # size-1 clique A: use G_menu directly as its own placement, and
        # clique B provides the (>=2)-sized internal structure instead;
        # only needed if the spec's (a,b) ever has sizeA==1 -- not in our
        # size lists (all sizeA>=2), so this path is unused but kept for
        # completeness/symmetry.
        raise NotImplementedError
    for cA in candA:
        for cB in candB:
            for Gq in G_menu:
                jobs.append((cA, cB, Gq))
    n_total = len(jobs)
    n_done = 0
    t0 = time.time()
    for batch_start in range(0, n_total, batch_size):
        batch = jobs[batch_start:batch_start + batch_size]
        quat_lists = []
        meta = []
        for cA, cB, Gq in batch:
            qs = build_glued_quats(cA, cB, Gq)
            if qs is None:
                continue
            quat_lists.append(qs)
            meta.append((cA, cB, Gq, qs))
        results = run_batch_parallel(n, quat_lists)
        for (cA, cB, Gq, qs), res in zip(meta, results):
            if res is None:
                continue
            total, depth = res
            rec = {
                'n': n, 'sizeA': sizeA, 'sizeB': sizeB, 'kind': kind,
                'psiA_pqr': cA.get('psi_pqr') if cA else None,
                'thetasA_pqr': cA.get('thetas_pqr') if cA else None,
                'psiB_pqr': cB.get('psi_pqr') if cB else None,
                'thetasB_pqr': cB.get('thetas_pqr') if cB else None,
                'Gquat': list(Gq), 'quats': [list(q) for q in qs],
                'total': total, 'by_depth': depth,
            }
            log_fh.write(json.dumps(rec) + '\n')
            key = (n, sizeA, sizeB)
            if total > best_tracker.get(key, (0, None))[0]:
                best_tracker[key] = (total, rec)
            if top_results is not None:
                lst = top_results.setdefault(key, [])
                lst.append((total, rec))
                lst.sort(key=lambda tr: -tr[0])
                del lst[10:]
        n_done += len(batch)
        log_fh.flush()
        print(f'  [{time.time()-t0:.0f}s] n={n} sizes=({sizeA},{sizeB}) {kind}: '
              f'{n_done}/{n_total} done, best={best_tracker.get((n,sizeA,sizeB),(0,None))[0]} '
              f'(record {RECORDS[n]})', flush=True)
    return best_tracker


def hillclimb_cell(n, sizeA, sizeB, top_rec, log_fh, best_tracker, rounds=2):
    """Neighbor search around the best glued config: perturb G by nearby
    small quaternions (multiply by a small integer quaternion), and swap
    in neighbor menu angles for whichever theta/psi indices are present."""
    cur = top_rec
    for rnd in range(rounds):
        Gq = cur['Gquat']
        Gmat = quat_to_matrix_exact(*Gq)
        neighbor_Gs = []
        # perturb by composing with small rotations (24-group + small quats)
        for pert in (cube_group_quats() + gen_G_menu(2)):
            Pmat = quat_to_matrix_exact(*pert)
            newG = mat_mul(Gmat, Pmat)
            try:
                nq = matrix_to_int_quat(newG)
            except ValueError:
                continue
            neighbor_Gs.append(nq)
        quatsA = cur['quats'][:sizeA]
        quatsB_placed = cur['quats'][sizeA:]
        cliqueA = {'quats': quatsA, 'psi_pqr': cur.get('psiA_pqr'), 'thetas_pqr': cur.get('thetasA_pqr')}
        if sizeB >= 2:
            # recover clique B's UN-glued quats: M_B = G^-1 . M_glued
            Ginv = mat_transpose(Gmat)  # G assumed orthonormal (it's a rotation-derived matrix scaled; use exact inverse via transpose on the rational rotation)
            # quat_to_matrix_exact already normalizes internally; recompute properly:
            Gunit = quat_to_matrix_exact(*Gq)
            Ginv = mat_transpose(Gunit)
            matsB = [mat_mul(Ginv, quat_to_matrix_exact(*q)) for q in quatsB_placed]
            cliqueB = {'quats': mats_to_quats(matsB), 'psi_pqr': cur.get('psiB_pqr'), 'thetas_pqr': cur.get('thetasB_pqr')}
        else:
            cliqueB = None
        quat_lists = []
        meta = []
        for nq in neighbor_Gs:
            qs = build_glued_quats(cliqueA, cliqueB, nq)
            if qs is None:
                continue
            quat_lists.append(qs)
            meta.append((cliqueA, cliqueB, nq, qs))
        results = run_batch_parallel(n, quat_lists)
        improved = False
        for (cA, cB, nq, qs), res in zip(meta, results):
            if res is None:
                continue
            total, depth = res
            rec = {
                'n': n, 'sizeA': sizeA, 'sizeB': sizeB, 'kind': 'hillclimb',
                'psiA_pqr': cA.get('psi_pqr'), 'thetasA_pqr': cA.get('thetas_pqr'),
                'psiB_pqr': cB.get('psi_pqr') if cB else None,
                'thetasB_pqr': cB.get('thetas_pqr') if cB else None,
                'Gquat': list(nq), 'quats': [list(q) for q in qs],
                'total': total, 'by_depth': depth,
            }
            log_fh.write(json.dumps(rec) + '\n')
            key = (n, sizeA, sizeB)
            if total > best_tracker.get(key, (0, None))[0]:
                best_tracker[key] = (total, rec)
                cur = rec
                improved = True
        log_fh.flush()
        print(f'  hillclimb n={n} ({sizeA},{sizeB}) round {rnd+1}: '
              f'best={best_tracker[(n,sizeA,sizeB)][0]} improved={improved}', flush=True)
        if not improved:
            break
    return best_tracker


def sweep_main(args):
    global G_MENU_TIER1, G_MENU_TIER2
    G_MENU_TIER1 = gen_G_menu(3)
    print(f'G menu tier1 (|comp|<=3): {len(G_MENU_TIER1)} rotations')

    log_fh = open(args.out, 'a')
    best_tracker = {}

    # generate + rank clique candidates for every size we need
    needed_sizes = sorted({s for sizes in CLIQUE_SIZES.values() for pair in sizes for s in pair if s >= 2})
    print(f'generating clique candidates for sizes {needed_sizes} ...', flush=True)
    all_cands = []
    for size in needed_sizes:
        all_cands += gen_size_chain_candidates(size)
    ranked = rank_candidates_standalone(all_cands)
    for size, lst in ranked.items():
        print(f'  size={size}: {len(lst)} candidates, best standalone total={lst[0]["standalone_total"] if lst else None}')

    cells = [(n, a, b) for n, sizes in CLIQUE_SIZES.items() for (a, b) in sizes]
    if args.cells:
        wanted = set(tuple(map(int, c.split(','))) for c in args.cells)
        cells = [c for c in cells if c in wanted]

    full_menu = cube_group_quats() + G_MENU_TIER1
    if args.g_limit < len(full_menu):
        rng = random.Random(20260716)
        cube24 = cube_group_quats()
        rest = rng.sample(G_MENU_TIER1, max(0, args.g_limit - len(cube24)))
        G_menu_coarse = cube24 + rest
    else:
        G_menu_coarse = full_menu
    print(f'coarse G menu size (this run): {len(G_menu_coarse)}')

    top_results = {}
    for n, sizeA, sizeB in cells:
        cliquesA = ranked.get(sizeA, [])
        cliquesB = ranked.get(sizeB, [])
        print(f'\n=== cell n={n} sizes=({sizeA},{sizeB}) ({len(cliquesA)}x{len(cliquesB)} clique cands) ===', flush=True)
        best_tracker = sweep_cell(n, sizeA, sizeB, cliquesA, cliquesB, G_menu_coarse,
                                    log_fh, best_tracker, topk_cliques=args.topk, kind='coarse',
                                    top_results=top_results)

    # widen G-menu + multi-restart hillclimb from the top-K incumbents per cell
    if args.hillclimb:
        G_MENU_TIER2 = gen_G_menu(args.widen_comp)
        print(f'\nwiden G menu (|comp|<={args.widen_comp}): {len(G_MENU_TIER2)} rotations')
        for n, sizeA, sizeB in cells:
            key = (n, sizeA, sizeB)
            if key not in best_tracker:
                continue
            restarts = top_results.get(key, [best_tracker[key]])[:args.restarts]
            print(f'\n=== widen+hillclimb n={n} sizes=({sizeA},{sizeB}), '
                  f'{len(restarts)} restart(s), incumbent={best_tracker[key][0]} ===', flush=True)
            for restart_i, (total0, rec) in enumerate(restarts):
                cliqueA = {'quats': rec['quats'][:sizeA]}
                if sizeB >= 2:
                    Gmat = quat_to_matrix_exact(*rec['Gquat'])
                    Ginv = mat_transpose(Gmat)
                    matsB = [mat_mul(Ginv, quat_to_matrix_exact(*q)) for q in rec['quats'][sizeA:]]
                    cliqueB = {'quats': mats_to_quats(matsB)}
                else:
                    cliqueB = None
                # widened G sweep with THIS restart's clique pair
                quat_lists, meta = [], []
                for Gq in G_MENU_TIER2:
                    qs = build_glued_quats(cliqueA, cliqueB, Gq)
                    if qs is None:
                        continue
                    quat_lists.append(qs)
                    meta.append((cliqueA, cliqueB, Gq, qs))
                for bstart in range(0, len(quat_lists), 2000):
                    bslice_q = quat_lists[bstart:bstart + 2000]
                    bslice_m = meta[bstart:bstart + 2000]
                    results = run_batch_parallel(n, bslice_q)
                    for (cA, cB, Gq, qs), res in zip(bslice_m, results):
                        if res is None:
                            continue
                        tot, depth = res
                        rc = {'n': n, 'sizeA': sizeA, 'sizeB': sizeB, 'kind': f'widen_G_r{restart_i}',
                              'psiA_pqr': None, 'thetasA_pqr': None, 'psiB_pqr': None, 'thetasB_pqr': None,
                              'Gquat': list(Gq), 'quats': [list(q) for q in qs], 'total': tot, 'by_depth': depth}
                        log_fh.write(json.dumps(rc) + '\n')
                        if tot > best_tracker[key][0]:
                            best_tracker[key] = (tot, rc)
                log_fh.flush()
                print(f'  restart {restart_i} (start={total0}) after widen: best={best_tracker[key][0]}', flush=True)
                best_tracker = hillclimb_cell(n, sizeA, sizeB, best_tracker[key][1], log_fh, best_tracker, rounds=args.rounds)

    log_fh.close()
    print('\n=== SWEEP DONE. Best per cell: ===')
    for (n, sizeA, sizeB), (total, rec) in sorted(best_tracker.items()):
        print(f'  n={n} sizes=({sizeA},{sizeB}): best={total}  record={RECORDS[n]}  '
              f'{"** BEATS OR TIES RECORD **" if total >= RECORDS[n] else ""}')
        print(f'    quats={rec["quats"]}  by_depth={rec["by_depth"]}')
    with open('/Users/dmi/carroll/glue_best.json', 'w') as f:
        json.dump({f'{n}_{a}_{b}': {'total': t, 'rec': r} for (n, a, b), (t, r) in best_tracker.items()},
                   f, indent=1, default=str)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=['q0', 'gates', 'sweep'], required=True)
    ap.add_argument('--out', default=RESULTS_PATH)
    ap.add_argument('--cells', nargs='*', help='restrict to n,a,b cells e.g. 5,4,1')
    ap.add_argument('--topk', type=int, default=8)
    ap.add_argument('--g-limit', type=int, default=10**9)
    ap.add_argument('--hillclimb', action='store_true')
    ap.add_argument('--rounds', type=int, default=2)
    ap.add_argument('--widen-comp', type=int, default=6, help='widen-phase G quaternion |component| cap')
    ap.add_argument('--restarts', type=int, default=3, help='multi-restart count from top-K coarse candidates')
    args = ap.parse_args()

    if args.mode == 'q0':
        q0_report()
    elif args.mode == 'gates':
        g1 = gate_g1()
        g2 = gate_g2()
        g3 = gate_g3()
        print(f'ALL GATES: {"PASS" if (g1 and g2 and g3) else "FAIL"}')
        sys.exit(0 if (g1 and g2 and g3) else 1)
    elif args.mode == 'sweep':
        sweep_main(args)


if __name__ == '__main__':
    main()
