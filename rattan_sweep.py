#!/usr/bin/env python3
# Working principles: RATTAN_SPEC.md. Project index: README.md
"""The rational-tangent sweep (RATTAN_SPEC.md): tilts tan psi = q/p with
d = p^2+q^2 NON-SQUARE (irrational sin/cos), phase steps parametrized by
rational points on the conic c^2 + d s'^2 = 1 (c = cos(Delta), s' =
sin(Delta)/sqrt(d)), so every pairwise relative rotation Rel(Delta,psi)
stays RATIONAL even though psi itself is not a Pythagorean angle. This is
the locus Postscript 27 identified as where the records' family structure
(393's {1,2,3,4} 4-clique, 183's {0,2,3} triply-resonant triple) actually
lives -- every prior sweep (nfamily_*) required psi ITSELF Pythagorean and
was structurally blind to it.

Reuses nfamily_common.py (CUBE_ROT_GROUP, mat_mul, mat_transpose,
is_rotation_exact, matrix_to_int_quat, quat_to_matrix_exact, quat_to_int)
and the C++ engine ./cube_regions_n (both read-only). Never edits
six_cube_search_results.md or any validated/ledger file.

Key identity (verified as gate G0): for Delta a conic angle and psi with
(p,q,d), Rel(Delta,psi)'s nine entries are all RATIONAL in p,q,d,c,s'
directly -- no sqrt(d) ever appears, since every entry that involves an
odd power of sin/cos-of-psi pairs with the matching odd power of sin(Delta)
and the sqrt(d) factors cancel exactly:
    Rel[0][0] = (c*p^2 + q^2)/d      Rel[0][1] = p*q*(1-c)/d   Rel[0][2] = p*s'
    Rel[1][0] = Rel[0][1]            Rel[1][1] = (c*q^2+p^2)/d Rel[1][2] = -q*s'
    Rel[2][0] = -p*s'                Rel[2][1] = q*s'          Rel[2][2] = c
This is nfamily_common.rel_matrix's Rodrigues form with cos(psi)=p/sqrt(d),
sin(psi)=q/sqrt(d), sin(Delta)=s'*sqrt(d) substituted and simplified.
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
    CUBE_ROT_GROUP, mat_mul, mat_transpose, is_rotation_exact,
    matrix_to_int_quat, quat_to_matrix_exact, quat_to_int, quat_to_matrix_exact,
)
from golden_rotations import rot_from_quat
from certify_six import exact_count_config

ENGINE = './cube_regions_n'
RESULTS_PATH = '/Users/dmi/carroll/rattan_results.jsonl'
REPORT_PATH = '/Users/dmi/carroll/rattan_report.md'
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
CAP = 512


# =========================================================================
# G0: exact conic parametrization
# =========================================================================

class ConicAngle:
    """A rational point (c, s') on the conic c^2 + d*s'^2 = 1 (d fixed per
    tilt). Represents a phase step Delta with cos(Delta)=c exactly and
    sin(Delta) = s'*sqrt(d) formally (never computed -- only c, s' and
    products p*s', q*s' with the tilt's own p,q ever appear, and those are
    rational, per the module docstring)."""
    __slots__ = ('c', 'sp', 'd')

    def __init__(self, c, sp, d):
        self.c = Fr(c)
        self.sp = Fr(sp)
        self.d = d
        assert self.c * self.c + d * self.sp * self.sp == 1, 'not on conic'

    @classmethod
    def from_t(cls, t, d):
        """Standard rational parametrization of the conic c^2+d s'^2=1
        (stereographic projection from (-1,0)): covers every rational
        point except (-1,0) itself, as t ranges over Q."""
        t = Fr(t)
        denom = 1 + d * t * t
        c = (1 - d * t * t) / denom
        sp = 2 * t / denom
        return cls(c, sp, d)

    @classmethod
    def identity(cls, d):
        return cls(Fr(1), Fr(0), d)

    def to_t(self):
        """Inverse of from_t: t = s'/(1+c), valid whenever c != -1."""
        if self.c == -1:
            return None
        return self.sp / (1 + self.c)

    def __mul__(self, other):
        """Angle addition = multiplication of norm-1 elements of Q(sqrt(-d))
        (c + i*sqrt(d)*s'): closed exactly, verified as part of G0."""
        assert self.d == other.d
        c = self.c * other.c - self.d * self.sp * other.sp
        sp = self.c * other.sp + other.c * self.sp
        return ConicAngle(c, sp, self.d)

    def inv(self):
        return ConicAngle(self.c, -self.sp, self.d)

    def pow(self, k):
        if k < 0:
            return self.inv().pow(-k)
        result = ConicAngle.identity(self.d)
        base = self
        while k:
            if k & 1:
                result = result * base
            base = base * base
            k >>= 1
        return result

    def __repr__(self):
        return f'ConicAngle(c={self.c}, sp={self.sp}, d={self.d})'


def rel_matrix_conic(delta, p, q, d):
    """Exact Rel(Delta,psi) with psi given by (p,q,d) (cos=p/sqrt(d),
    sin=q/sqrt(d)) and Delta a ConicAngle on the SAME d. All-Fraction, no
    sqrt anywhere (see module docstring)."""
    assert delta.d == d
    c, sp = delta.c, delta.sp
    p, q, d = Fr(p), Fr(q), Fr(d)
    return [
        [(c * p * p + q * q) / d, p * q * (1 - c) / d, p * sp],
        [p * q * (1 - c) / d, (c * q * q + p * p) / d, -q * sp],
        [-p * sp, q * sp, c],
    ]


def build_family_quats_conic(p, q, d, thetas, cap=CAP):
    """thetas: list of ConicAngle (same d). theta[0] convention: Delta is
    always taken relative to thetas[0] (need not itself be identity).
    Returns (quats, mats)."""
    quats, mats = [], []
    base = thetas[0]
    base_inv = base.inv()
    for th in thetas:
        delta = th * base_inv
        M = rel_matrix_conic(delta, p, q, d)
        assert is_rotation_exact(M), 'conic family matrix failed rotation check'
        qv = matrix_to_int_quat(M, cap=cap)
        quats.append(qv)
        mats.append(M)
    return quats, mats


# ---- tilt and t menus ----------------------------------------------------

def _make_tilt(p, q):
    d = p * p + q * q
    g = math.gcd(p, q)
    assert g == 1
    is_sq = math.isqrt(d) ** 2 == d
    return (p, q, d, is_sq)


RECORD_TILTS = [(3, 2), (5, 2), (5, 3)]  # tan psi = 2/3, 2/5, 3/5 (d=13,29,34)

_SPEC_LIST_QP = [(2, 3), (2, 5), (3, 5), (1, 2), (1, 3), (1, 4), (3, 4),
                  (1, 5), (4, 5), (5, 12)]


def build_tilt_menu(max_pq=15):
    """All coprime (p,q), p!=q, p,q in [1,max_pq], sorted by d ascending,
    with the three record tilts (and their spec-listed cousins) pinned
    first. Only d NON-SQUARE tilts are kept for the sweep (G0's own
    requirement) -- Pythagorean q/p values from the spec's illustrative
    list (e.g. 3/4, 5/12) are dropped here with a note, since they are
    already covered by nfamily_*'s Pythagorean-menu sweep."""
    seen = set()
    menu = []
    for p, q in RECORD_TILTS:
        d = p * p + q * q
        seen.add((p, q))
        menu.append((p, q, d))
    for q, p in _SPEC_LIST_QP:
        if math.gcd(p, q) != 1 or (p, q) in seen:
            continue
        d = p * p + q * q
        if math.isqrt(d) ** 2 == d:
            continue  # Pythagorean, drop (already covered elsewhere)
        seen.add((p, q))
        menu.append((p, q, d))
    for p in range(1, max_pq + 1):
        for q in range(1, max_pq + 1):
            if p == q or math.gcd(p, q) != 1 or (p, q) in seen:
                continue
            d = p * p + q * q
            if math.isqrt(d) ** 2 == d:
                continue
            seen.add((p, q))
            menu.append((p, q, d))
    menu.sort(key=lambda pqd: (0 if (pqd[0], pqd[1]) in set(RECORD_TILTS) else 1, pqd[2]))
    return menu


TILT_MENU = build_tilt_menu()


def farey_t_values(bmax):
    """All reduced fractions a/b, -bmax<=a<=bmax (a!=0 constraint none),
    1<=b<=bmax, gcd(|a|,b)=1 or a=0 with b=1. Includes 0 (identity, via
    t=0 -> c=1,s'=0) and excludes nothing else; t=+-infinity (the excluded
    conic point (-1,0)) is simply never generated by this rational map."""
    out = {Fr(0)}
    for b in range(1, bmax + 1):
        for a in range(-b, b + 1):
            if a == 0:
                continue
            if math.gcd(abs(a), b) != 1:
                continue
            out.add(Fr(a, b))
    return sorted(out, key=lambda t: (abs(t.denominator), t))


T_MENU_SMALL = farey_t_values(12)   # ~ a few hundred, for chains / dense pass
T_MENU_FULL = farey_t_values(40)    # full Farey-40 menu for random sampling


# =========================================================================
# Gate functions
# =========================================================================

def run_cpp(quats, n=None):
    n = n or len(quats)
    qstr = ';'.join(','.join(str(c) for c in q) for q in quats)
    out = subprocess.run([ENGINE, '--n', str(n), '--quats', qstr],
                          capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip())


def gate_g0():
    print('=== G0: conic parametrization -- round trip + closure under addition ===')
    ok = True
    p, q, d = 3, 2, 13  # tan psi = 2/3
    for tstr in ['1/7', '-3/11', '5/1', '0', '2/3']:
        t = Fr(tstr)
        a = ConicAngle.from_t(t, d)
        t_back = a.to_t()
        rt_ok = (t_back == t)
        print(f'  t={t} -> (c={a.c}, sp={a.sp})  conic: c^2+d*sp^2={a.c**2+d*a.sp**2}  '
              f'round_trip t_back={t_back}  ok={rt_ok}')
        ok = ok and rt_ok and (a.c * a.c + d * a.sp * a.sp == 1)
    # closure under addition: a1*a2 must itself be a valid conic point, and
    # must equal the DIRECT conic point of the "added" angle computed via
    # the standard tan-half-angle addition on t (t1,t2 combine as t_sum =
    # (t1+t2)/(1-d*t1*t2), the group law of this conic, checked against
    # the ring-multiplication formula independently).
    t1, t2 = Fr(2, 5), Fr(-3, 7)
    a1, a2 = ConicAngle.from_t(t1, d), ConicAngle.from_t(t2, d)
    a12 = a1 * a2
    t_sum_expected = (t1 + t2) / (1 - d * t1 * t2)
    a_sum_direct = ConicAngle.from_t(t_sum_expected, d)
    closure_ok = (a12.c == a_sum_direct.c and a12.sp == a_sum_direct.sp)
    print(f'  closure: t1={t1} + t2={t2} -> ring product == direct t_sum={t_sum_expected}: {closure_ok}')
    ok = ok and closure_ok
    # verify Rel matrix entries are rational and the matrix is a genuine
    # rotation, for one nontrivial conic angle.
    M = rel_matrix_conic(a1, p, q, d)
    rot_ok = is_rotation_exact(M)
    qv = matrix_to_int_quat(M)
    print(f'  Rel(Delta(t={t1}),psi=2/3): rotation_ok={rot_ok} quat={qv}')
    ok = ok and rot_ok
    print(f'G0: {"PASS" if ok else "FAIL"}\n')
    return ok


def _find_axis_witness(Mk, Mbase, target_axis_canon, canon_line_fn):
    """Search CUBE_ROT_GROUP for Q such that Rp = Q^T (Mk^T Mbase) is in
    Rel(Delta,psi) form (Rp[1][0]==Rp[0][1]) AND the world axis recovered
    (mapped back through Mbase) matches target_axis_canon exactly. Returns
    (Q, Rp) or None."""
    R = mat_mul(mat_transpose(Mk), Mbase)
    for Q in CUBE_ROT_GROUP:
        Rp = mat_mul(mat_transpose(Q), R)
        if Rp[1][0] != Rp[0][1]:
            continue
        L = (Rp[2][1] - Rp[1][2], Rp[0][2] - Rp[2][0], Fr(0))
        if L == (0, 0, 0):
            continue  # Delta=0, axis undetermined for this pair
        world = tuple(sum(Mbase[i][k] * L[k] for k in range(3)) for i in range(3))
        if canon_line_fn(world) != target_axis_canon:
            continue
        return Q, Rp
    return None


def _canon_line(vec):
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


def gate_g1():
    """The sharp gate: reproduce 393's OWN 4-clique {1,2,3,4} (integer
    quats (3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)) as EXACT conic-angle
    Rel(Delta(t),psi=2/3) relations, proving the sweep space contains it.
    Method: fix cube local-index 0 (physical cube "1") as the base
    (theta=0, Q_base=I -- absorbed into the arbitrary global frame
    rotation); for each other clique member k, find its OWN cube-symmetry
    relabeling Q_k (from the 24-element group) such that N_k = M_k @ Q_k
    puts the pairwise relation N_k^T @ M_base into Rel(Delta,psi) form
    with the target world axis (3,2,0) (per glue_report.md's independent
    derivation, reused here only as the known TARGET to search for -- the
    search itself is a fresh exact witness). Once Q_k found for all k, the
    remaining 3 pairs (not involving base) are cross-checked directly
    (no further search) against the SAME (p,q,d) and the conic-t values
    solved from the base pairs -- this is the part that makes it a
    genuine proof of consistency, not just three independent 2-cube
    matches."""
    print('=== G1 (sharp): reproduce 393\'s {1,2,3,4} 4-clique from the conic parametrization ===')
    quats393 = RECORD_QUATS[5]
    clique_local = [1, 2, 3, 4]  # physical cube indices in RECORD_QUATS[5]
    mats = {i: quat_to_matrix_exact(*quats393[i]) for i in clique_local}
    # base fixed as the UNLABELED reference (Q_base=I); empirically (see
    # session debug) cube index 2 is the one for which the OTHER three
    # cubes' own relabelings land exactly on axis (3,2,0) -- i.e. cube 2
    # plays the role nfamily_common calls "cube 1 = identity" for this
    # particular clique's own internal gauge (not physical index 1).
    base = 2
    others = [1, 3, 4]
    target_axis = _canon_line((3, 2, 0))
    # empirically (session debug): with base=cube-2 fixed as the unlabeled
    # reference, the consistent (p,q) recovered from Rp[0][2]=p*s',
    # Rp[2][1]=q*s' across all three other cubes is (3,-2), not (3,2) --
    # a genuine sign gauge (q's sign flips because the witnessing Q_k
    # implicitly reverses handedness of the local psi-frame relative to
    # the world axis (3,2,0); still tan(psi)=|q|/|p|=2/3 exactly).
    p, q, d = 3, -2, 13

    Ns = {base: mats[base]}
    t_of = {base: Fr(0)}
    cs_of = {base: (Fr(1), Fr(0))}
    ok = True
    for k in others:
        w = _find_axis_witness(mats[k], mats[base], target_axis, _canon_line)
        if w is None:
            print(f'  cube {k}: NO witness found for axis (3,2,0) -- FAIL')
            ok = False
            continue
        Qk, Rp = w
        Nk = mat_mul(mats[k], Qk)
        c = Rp[2][2]
        # recover s' in the FIXED (p,q)=(3,2) convention. The gauge
        # symmetry (p,q,s') ~ (-p,-q,-s') is the only freedom once the
        # target world axis is pinned (world axis = M_base @ L, M_base
        # fixed) -- so only (3,2) or its flip (-3,-2) should ever match;
        # any other (p,q) ratio is a genuine inconsistency (flag it).
        num02, num21 = Rp[0][2], Rp[2][1]
        cand = None
        for pp, qq, sign in [(p, q, 1), (-p, -q, -1)]:
            if num02 * qq != num21 * pp:
                continue
            sp_try = sign * (num02 / pp)
            cand = sp_try
            break
        if cand is None:
            print(f'  cube {k}: (p,q) ratio inconsistent with target ({p},{q}) '
                  f'-- Rp entries {num02},{num21} -- FAIL')
            ok = False
            continue
        sp = cand
        conic_ok = (c * c + d * sp * sp == 1)
        t = sp / (1 + c) if c != -1 else None
        # round-trip: does t regenerate (c,sp) exactly?
        rt_ok = False
        if t is not None:
            back = ConicAngle.from_t(t, d)
            rt_ok = (back.c == c and back.sp == sp)
        print(f'  cube {k}: Q_k found, Rel-form c={c} sp={sp} conic_eq_ok={conic_ok} '
              f't={t} round_trip_ok={rt_ok}')
        ok = ok and conic_ok and rt_ok
        Ns[k] = Nk
        t_of[k] = t
        cs_of[k] = (c, sp)

    # Cross-check the 3 remaining pairs (not involving base) with NO
    # further searching: N_j, N_k already fixed above.
    for j, k in itertools.combinations(others, 2):
        if j not in Ns or k not in Ns:
            continue
        Rjk = mat_mul(mat_transpose(Ns[j]), Ns[k])
        c_direct, sp_num02, sp_num21 = Rjk[2][2], Rjk[0][2], Rjk[2][1]
        family_form_ok = (Rjk[1][0] == Rjk[0][1])
        sp_direct = sp_num02 / p if p != 0 else None
        sp_direct_ok = family_form_ok and (sp_direct == sp_num21 / q)
        # predicted via conic-angle group law: Delta_jk = theta_k - theta_j
        # cs_of[i] stores the (c,sp) of Rel(-theta_i,psi) (since it was
        # extracted from N_i^T N_base = Rel(theta_base-theta_i,psi) with
        # theta_base=0) -- so the TRUE per-cube angle is its INVERSE, and
        # Rel(theta_k-theta_j,psi) = raw_j * raw_k.inv() (verified against
        # the direct N_j^T N_k computation above; matches sign exactly).
        aj = ConicAngle(cs_of[j][0], cs_of[j][1], d)
        ak = ConicAngle(cs_of[k][0], cs_of[k][1], d)
        a_pred = aj * ak.inv()
        pred_ok = family_form_ok and sp_direct_ok and (a_pred.c == c_direct and a_pred.sp == sp_direct)
        print(f'  cross-check pair ({j},{k}): family_form={family_form_ok} '
              f'c_direct={c_direct} sp_direct={sp_direct}  '
              f'predicted c={a_pred.c} sp={a_pred.sp}  match={pred_ok}')
        ok = ok and family_form_ok and sp_direct_ok and pred_ok

    print(f'  t-values found (relative to base=cube1): {t_of}')
    print(f'G1: {"PASS" if ok else "FAIL"}\n')
    return ok, {'t_of': {str(k): str(v) for k, v in t_of.items()}, 'p': p, 'q': q, 'd': d}


def gate_g2():
    print('=== G2: two-engine agreement (C++ vs Python oracle) on one n=4, one n=5 rational-tangent config ===')
    ok = True
    p, q, d = 3, 2, 13
    thetas4 = [ConicAngle.identity(d)] + [ConicAngle.from_t(t, d) for t in
                                            [Fr(1, 3), Fr(-2, 5), Fr(4, 7)]]
    quats4, _ = build_family_quats_conic(p, q, d, thetas4)
    r_cpp4 = run_cpp(quats4, n=4)
    rots4 = [rot_from_quat(*qv) for qv in quats4]
    py_total4, py_depth4 = exact_count_config(rots4, verbose=False)
    py_depth4 = {int(k): v for k, v in py_depth4.items()}
    cpp_depth4 = {int(k): v for k, v in r_cpp4['by_depth'].items()}
    match4 = (r_cpp4['bounded'] == py_total4 and cpp_depth4 == py_depth4)
    print(f'  n=4 quats={quats4}')
    print(f'  cpp: total={r_cpp4["bounded"]} depth={cpp_depth4}')
    print(f'  py:  total={py_total4} depth={py_depth4}')
    print(f'  match: {match4}')
    ok = ok and match4

    p5, q5, d5 = 5, 2, 29
    thetas5 = [ConicAngle.identity(d5)] + [ConicAngle.from_t(t, d5) for t in
                                             [Fr(1, 4), Fr(-3, 8), Fr(5, 11), Fr(-1, 6)]]
    quats5, _ = build_family_quats_conic(p5, q5, d5, thetas5)
    r_cpp5 = run_cpp(quats5, n=5)
    rots5 = [rot_from_quat(*qv) for qv in quats5]
    py_total5, py_depth5 = exact_count_config(rots5, verbose=False)
    py_depth5 = {int(k): v for k, v in py_depth5.items()}
    cpp_depth5 = {int(k): v for k, v in r_cpp5['by_depth'].items()}
    match5 = (r_cpp5['bounded'] == py_total5 and cpp_depth5 == py_depth5)
    print(f'  n=5 quats={quats5}')
    print(f'  cpp: total={r_cpp5["bounded"]} depth={cpp_depth5}')
    print(f'  py:  total={py_total5} depth={py_depth5}')
    print(f'  match: {match5}')
    ok = ok and match5

    print(f'G2: {"PASS" if ok else "FAIL"}\n')
    return ok


def gate_g3():
    print('=== G3: reproduce 723 from the ledger quats ===')
    r = run_cpp(RECORD_QUATS[6], n=6)
    depth = {int(k): v for k, v in r['by_depth'].items() if int(k) != 0}
    ok = (r['bounded'] == 723 and depth == RECORD_DEPTH[6])
    print(f'  cpp: total={r["bounded"]} depth={depth}')
    print(f'  expect: total=723 depth={RECORD_DEPTH[6]}')
    print(f'G3: {"PASS" if ok else "FAIL"}\n')
    return ok


def run_all_gates():
    g0 = gate_g0()
    g1, g1_info = gate_g1()
    g2 = gate_g2()
    g3 = gate_g3()
    all_ok = g0 and g1 and g2 and g3
    print(f'ALL GATES: {"PASS" if all_ok else "FAIL"}')
    return all_ok, {'G0': g0, 'G1': g1, 'G2': g2, 'G3': g3, 'G1_info': g1_info}


# =========================================================================
# Generalized clique-chain finder (G1's method, reusable for the targeted
# record-clique completion runs on 183's triple and any other candidate)
# =========================================================================

def find_clique_chain(mats, base, axis_target, d, candidate_pq):
    """mats: dict idx -> exact Fraction rotation matrix. base: idx used as
    the unlabeled reference (Q_base=I, theta_base=0). axis_target:
    canon_line tuple (world axis all pairs must witness). d: conic
    modulus. candidate_pq: list of (p,q) with p^2+q^2==d to try (order
    matters, sign is searched automatically). Returns (p, q, t_of dict) or
    None if the clique is not self-consistently on this axis/tilt."""
    t_of = {base: Fr(0)}
    cs_of = {base: (Fr(1), Fr(0))}
    Ns = {base: mats[base]}
    chosen_pq = None
    for k in mats:
        if k == base:
            continue
        w = _find_axis_witness(mats[k], mats[base], axis_target, _canon_line)
        if w is None:
            return None
        Qk, Rp = w
        c = Rp[2][2]
        num02, num21 = Rp[0][2], Rp[2][1]
        found = None
        for pp, qq in candidate_pq:
            for ppx, qqx in ((pp, qq), (pp, -qq), (-pp, qq), (-pp, -qq)):
                if num02 * qqx == num21 * ppx:
                    sp = num02 / ppx if ppx != 0 else num21 / qqx
                    found = (ppx, qqx, sp)
                    break
            if found:
                break
        if found is None:
            return None
        pp, qq, sp = found
        if chosen_pq is None:
            chosen_pq = (pp, qq)
        elif chosen_pq != (pp, qq):
            return None
        if c * c + d * sp * sp != 1:
            return None
        if c == -1:
            return None
        t = sp / (1 + c)
        back = ConicAngle.from_t(t, d)
        if not (back.c == c and back.sp == sp):
            return None
        t_of[k] = t
        cs_of[k] = (c, sp)
        Ns[k] = mat_mul(mats[k], Qk)
    if chosen_pq is None:
        return None
    pp, qq = chosen_pq
    for j, k in itertools.combinations(list(mats.keys()), 2):
        if j == base or k == base:
            continue
        Rjk = mat_mul(mat_transpose(Ns[j]), Ns[k])
        if Rjk[1][0] != Rjk[0][1]:
            return None
        c_direct = Rjk[2][2]
        sp_direct = Rjk[0][2] / pp if pp != 0 else Rjk[2][1] / qq
        if Rjk[2][1] != qq * sp_direct:
            return None
        aj = ConicAngle(cs_of[j][0], cs_of[j][1], d)
        ak = ConicAngle(cs_of[k][0], cs_of[k][1], d)
        pred = aj * ak.inv()
        if not (pred.c == c_direct and pred.sp == sp_direct):
            return None
    return pp, qq, t_of


def verify_183_triple_chains():
    """Independent confirmation (own exact search, not copied from
    glue_report) that 183's {0,2,3} triple is simultaneously on THREE
    rational-tangent axes -- (2,-3,0) tan2/3 d13, (3,5,0) tan3/5 d34,
    (5,2,0) tan2/5 d29 -- via find_clique_chain, base=cube0 (already the
    literal identity quat (1,0,0,0), no reconstruction needed)."""
    quats183 = RECORD_QUATS[4]
    mats = {i: quat_to_matrix_exact(*quats183[i]) for i in (0, 2, 3)}
    out = {}
    for axis, d, pqs in [((2, -3, 0), 13, [(2, 3), (3, 2)]),
                          ((3, 5, 0), 34, [(3, 5), (5, 3)]),
                          ((5, 2, 0), 29, [(5, 2), (2, 5)])]:
        res = find_clique_chain(mats, 0, _canon_line(axis), d, pqs)
        out[(axis, d)] = res
    return out


# =========================================================================
# Sweep config generators
# =========================================================================

def gen_chain_configs(n, tilt_menu, t_values, cap=CAP):
    out = []
    for p, q, d in tilt_menu:
        for t in t_values:
            if t == 0:
                continue
            a = ConicAngle.from_t(t, d)
            thetas = [a.pow(k) for k in range(n)]
            try:
                quats, _ = build_family_quats_conic(p, q, d, thetas, cap=cap)
            except ValueError:
                continue
            out.append({'n': n, 'kind': 'chain', 'p': p, 'q': q, 'd': d,
                         't': str(t), 'quats': quats})
    return out


def gen_random_configs(n, count, rng, tilt_menu, t_values, cap=CAP):
    out = []
    tries = 0
    while len(out) < count and tries < count * 6:
        tries += 1
        p, q, d = rng.choice(tilt_menu)
        ts = [Fr(0)] + [rng.choice(t_values) for _ in range(n - 1)]
        thetas = [ConicAngle.from_t(t, d) for t in ts]
        try:
            quats, _ = build_family_quats_conic(p, q, d, thetas, cap=cap)
        except ValueError:
            continue
        out.append({'n': n, 'kind': 'random', 'p': p, 'q': q, 'd': d,
                     't_list': [str(t) for t in ts], 'quats': quats})
    return out


def gen_neighbor_configs(n, base_cfg, rng, t_values_sorted, radius=2):
    """Perturb ONE t coordinate (or swap to an index-adjacent Farey value)
    of a 'random'/'chain'-derived config, for local hill-climbing. Also
    tries small integer-quat jitters of one cube (+-1 on one component)."""
    out = []
    p, q, d = base_cfg['p'], base_cfg['q'], base_cfg['d']
    if 't_list' in base_cfg:
        ts = [Fr(x) for x in base_cfg['t_list']]
    elif 't' in base_cfg:
        t0 = Fr(base_cfg['t'])
        ts = [Fr(0)] + [ (ConicAngle.from_t(t0, d).pow(k)).to_t() for k in range(1, n)]
    else:
        return out
    idx_map = {v: i for i, v in enumerate(t_values_sorted)}

    def nearest_idx(t):
        # linear scan is fine here (small menu, called rarely)
        best_i, best_d = 0, None
        tv = float(t)
        for i, v in enumerate(t_values_sorted):
            dd = abs(float(v) - tv)
            if best_d is None or dd < best_d:
                best_d, best_i = dd, i
        return best_i

    for coord in range(1, len(ts)):
        i0 = nearest_idx(ts[coord])
        for di in range(-radius, radius + 1):
            if di == 0:
                continue
            j = i0 + di
            if not (0 <= j < len(t_values_sorted)):
                continue
            new_ts = list(ts)
            new_ts[coord] = t_values_sorted[j]
            thetas = [ConicAngle.from_t(t, d) for t in new_ts]
            try:
                quats, _ = build_family_quats_conic(p, q, d, thetas, cap=CAP)
            except ValueError:
                continue
            out.append({'n': n, 'kind': 'neighbor', 'p': p, 'q': q, 'd': d,
                         't_list': [str(t) for t in new_ts], 'quats': quats})
    return out


def gen_int_quat_extension(fixed_quats, count, rng, comp_range=13, norm_cap=600):
    """Random integer-quaternion 5th/4th/6th-cube candidates (component
    magnitude <= comp_range, squared-norm <= norm_cap), appended to a
    fixed base clique -- spec item 2(b): 'integer quaternions up to norm
    ~600' (393's own cube 0 is exactly this kind of off-axis member)."""
    out = []
    seen = set()
    tries = 0
    while len(out) < count and tries < count * 8:
        tries += 1
        w = rng.randint(-comp_range, comp_range)
        x = rng.randint(-comp_range, comp_range)
        y = rng.randint(-comp_range, comp_range)
        z = rng.randint(-comp_range, comp_range)
        if (w, x, y, z) == (0, 0, 0, 0):
            continue
        g = math.gcd(math.gcd(abs(w), abs(x)), math.gcd(abs(y), abs(z)))
        if g > 1:
            w, x, y, z = w // g, x // g, y // g, z // g
        norm = w * w + x * x + y * y + z * z
        if norm > norm_cap:
            continue
        key = (w, x, y, z)
        if key in seen:
            continue
        seen.add(key)
        out.append(list(fixed_quats) + [key])
    return out


# =========================================================================
# Engine batching
# =========================================================================

def run_batch(n, configs):
    if not configs:
        return []
    lines = [';'.join(','.join(str(c) for c in q) for q in cfg['quats'])
             for cfg in configs]
    proc = subprocess.run([ENGINE, '--n', str(n), '--quats-stdin'],
                           input='\n'.join(lines) + '\n',
                           capture_output=True, text=True, check=True)
    out = []
    for cfg, line in zip(configs, proc.stdout.strip().splitlines()):
        r = json.loads(line)
        if 'error' in r:
            continue
        depth = {int(k): v for k, v in r['by_depth'].items() if int(k) != 0}
        out.append((cfg, r['bounded'], depth))
    return out


def worker(args):
    n, configs = args
    return n, run_batch(n, configs)


def shard_batches(all_batches, chunk=400):
    """Split (n, configs) pairs into <=chunk-sized shards so the worker
    pool load-balances across all 4 cores and results stream back
    incrementally (one shard per n would serialize a 10k+ config list
    through <=3 workers and buffer all output until the very end)."""
    out = []
    for n, cfgs in all_batches:
        if not cfgs:
            continue
        for i in range(0, len(cfgs), chunk):
            out.append((n, cfgs[i:i + chunk]))
    random.Random(0).shuffle(out)  # interleave n's for even latency
    return out


def run_batch_from_quats(n, quat_lists):
    """Like run_batch but for raw quat-list configs (record-clique
    completion runs use plain lists, not the {'quats':...} dict form)."""
    configs = [{'quats': ql} for ql in quat_lists]
    results = run_batch(n, configs)
    return [(cfg['quats'], total, depth) for cfg, total, depth in results]


# =========================================================================
# Record protocol: verify with the Python oracle, flag if >= record
# =========================================================================

FLAGGED = []


def check_record(n, total, quats, report_fh=None):
    """ANY total > record, or == record: verify with certify_six's exact
    Python oracle immediately. If confirmed and (>record) or (==record
    with a non-congruent pairwise-invariant structure), FLAG. Never edits
    the ledger; only appends to this run's own report/log."""
    record = RECORDS.get(n)
    if record is None or total < record:
        return False
    rots = [rot_from_quat(*q) for q in quats]
    py_total, py_depth = exact_count_config(rots, verbose=False)
    py_depth = {int(k): v for k, v in py_depth.items()}
    confirmed = (py_total == total)
    msg = (f'*** RECORD-CLASS RESULT n={n} total={total} (record={record}) '
           f'quats={quats} python_oracle_total={py_total} '
           f'oracle_confirmed={confirmed} depth={py_depth} ***')
    print(msg, flush=True)
    FLAGGED.append({'n': n, 'total': total, 'quats': quats,
                     'oracle_total': py_total, 'oracle_confirmed': confirmed,
                     'depth': py_depth})
    if report_fh is not None:
        report_fh.write('\n' + msg + '\n')
        report_fh.flush()
    return confirmed


# =========================================================================
# Main sweep driver
# =========================================================================

def append_report(text):
    with open(REPORT_PATH, 'a') as f:
        f.write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, nargs='+', default=[4, 5, 6])
    ap.add_argument('--random', type=int, default=15000, help='random configs per n')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--seed', type=int, default=20260716)
    ap.add_argument('--out', default=RESULTS_PATH)
    ap.add_argument('--neighbor-rounds', type=int, default=2)
    ap.add_argument('--chain-tilts', type=int, default=40)
    ap.add_argument('--skip-gates', action='store_true')
    args = ap.parse_args()

    rng = random.Random(args.seed)
    t_start = time.time()

    def log(msg):
        print(f'[{time.time()-t_start:.0f}s] {msg}', flush=True)

    # ---- gates ----
    if not args.skip_gates:
        gates_ok, gates_info = run_all_gates()
        append_report(
            '\n## Gate results (auto-appended by rattan_sweep.py --n '
            f'{args.n})\n\nG0={gates_info["G0"]} G1={gates_info["G1"]} '
            f'G2={gates_info["G2"]} G3={gates_info["G3"]}\n\n'
            f'G1 t-values for 393\'s {{1,2,3,4}} clique (base=cube-index-2, '
            f'tan psi=2/3, d=13): {gates_info["G1_info"]["t_of"]}\n\n')
        if not gates_ok:
            log('GATES FAILED, aborting sweep.')
            return
    else:
        gates_info = None

    # ---- 183 triple verification (own independent re-derivation) ----
    tri = verify_183_triple_chains()
    lines = ['## 183\'s {0,2,3} triple: independent re-derivation of the '
             'three simultaneous axes\n\n']
    for (axis, d), res in tri.items():
        if res is None:
            lines.append(f'- axis {axis} d={d}: NOT reproduced (search failed)\n')
        else:
            p, q, t_of = res
            lines.append(f'- axis {axis} d={d}: tan psi={q}/{p} CONFIRMED, '
                          f't-values={ {str(k): str(v) for k, v in t_of.items()} }\n')
    append_report(''.join(lines) + '\n')
    log('183 triple verification done: ' + str({str(k): (v is not None) for k, v in tri.items()}))

    fh = open(args.out, 'a')
    best = {n: (0, None) for n in args.n}

    def log_and_track(n, cfg, total, depth, tag=''):
        rec = dict(cfg)
        rec['total'] = total
        rec['by_depth'] = depth
        if tag:
            rec['tag'] = tag
        fh.write(json.dumps(rec) + '\n')
        fh.flush()
        if total > best[n][0]:
            best[n] = (total, cfg)
        check_record(n, total, cfg['quats'])

    # ---- Tier 1: single-axis rational-tangent chains ----
    log('generating chain configs...')
    chain_tilts = TILT_MENU[:args.chain_tilts]
    all_batches = []
    for n in args.n:
        cfgs = gen_chain_configs(n, chain_tilts, T_MENU_SMALL)
        log(f'  n={n}: {len(cfgs)} chain configs')
        all_batches.append((n, cfgs))
    shards = shard_batches(all_batches)
    done = 0
    with mp.Pool(args.workers) as pool:
        for n, results in pool.imap_unordered(worker, shards):
            for cfg, total, depth in results:
                log_and_track(n, cfg, total, depth, tag='tier1-chain')
            done += 1
            if done % 10 == 0 or done == len(shards):
                log(f'tier1 shard {done}/{len(shards)}, best: ' +
                    ', '.join(f'n={m}:{best[m][0]}' for m in args.n))
    append_report(f'### Tier 1 (chains) done at {time.time()-t_start:.0f}s. '
                   f'Best so far: ' + ', '.join(f'n={n}:{best[n][0]}' for n in args.n) + '\n\n')

    # ---- Tier 2: random independent-phase tuples ----
    log('generating random configs...')
    all_batches = []
    for n in args.n:
        cfgs = gen_random_configs(n, args.random, rng, TILT_MENU, T_MENU_FULL)
        log(f'  n={n}: {len(cfgs)} random configs')
        all_batches.append((n, cfgs))
    shards = shard_batches(all_batches)
    done = 0
    with mp.Pool(args.workers) as pool:
        for n, results in pool.imap_unordered(worker, shards):
            for cfg, total, depth in results:
                log_and_track(n, cfg, total, depth, tag='tier2-random')
            done += 1
            if done % 10 == 0 or done == len(shards):
                log(f'tier2 shard {done}/{len(shards)}, best: ' +
                    ', '.join(f'n={m}:{best[m][0]}' for m in args.n))
    append_report(f'### Tier 2 (random) done at {time.time()-t_start:.0f}s. '
                   f'Best so far: ' + ', '.join(f'n={n}:{best[n][0]}' for n in args.n) + '\n\n')

    # ---- Tier 3: targeted record-clique completion ----
    log('targeted record-clique completion...')
    targeted = []

    # (a) 393's {1,2,3,4} + 5th cube via more conic angles on the same axis
    for t5 in T_MENU_FULL:
        a = ConicAngle.from_t(Fr(t5), 13)
        thetas = [ConicAngle.identity(13), ConicAngle.from_t(Fr(-5, 6), 13),
                  ConicAngle.from_t(Fr(3, 4), 13), ConicAngle.from_t(Fr(-1, 5), 13), a]
        try:
            quats, _ = build_family_quats_conic(3, -2, 13, thetas, cap=CAP)
        except ValueError:
            continue
        targeted.append({'n': 5, 'kind': '393clique+5th-onaxis', 'p': 3, 'q': -2, 'd': 13,
                          't5': str(t5), 'quats': quats})

    # (b) 393's {1,2,3,4} (literal ledger quats) + 5th cube as arbitrary
    #     integer quaternion up to norm~600 (393's own cube 0 is exactly
    #     this kind of off-axis member).
    clique393 = RECORD_QUATS[5][1:5]
    for ql in gen_int_quat_extension(clique393, 4000, rng):
        targeted.append({'n': 5, 'kind': '393clique+5th-intquat', 'quats': ql})

    # (c) n=6: 393's five ledger cubes fixed, sweep the 6th (verify we can
    #     re-find 723 via the known 6th quat, then broaden).
    clique393_5 = RECORD_QUATS[5]
    targeted.append({'n': 6, 'kind': '393five+6th-known723', 'quats': clique393_5 + [(5, 2, 2, 2)]})
    for ql in gen_int_quat_extension(clique393_5, 4000, rng):
        targeted.append({'n': 6, 'kind': '393five+6th-intquat', 'quats': ql})
    # (c') 393's LITERAL five ledger cubes fixed, 6th cube built directly
    #      as M6(t6) = M_base @ Rel(t6,psi) with M_base = literal cube-
    #      index-2's own matrix (the {1,2,3,4} clique's base, per G1) --
    #      this places the 6th cube on the SAME axis/tilt as the clique
    #      WITHOUT any gauge reconstruction (Q_new=I is absorbed into the
    #      cube's own labeling ambiguity, per the module docstring's
    #      region-count invariance argument). Checks whether 723's own
    #      6th cube (5,2,2,2) is exactly some M6(t6) on this axis, and
    #      sweeps the rest of the axis for anything better.
    M_base2 = quat_to_matrix_exact(*RECORD_QUATS[5][2])
    m6_known = quat_to_matrix_exact(5, 2, 2, 2)
    R_check = mat_mul(mat_transpose(M_base2), m6_known)
    on_axis_723 = (R_check[1][0] == R_check[0][1])
    log_line6 = (f'723\'s 6th cube (5,2,2,2) relative to 393-clique base '
                 f'(cube-index-2): family-form={on_axis_723}')
    for t6 in T_MENU_FULL:
        delta6 = ConicAngle.from_t(Fr(t6), 13)
        M6 = rel_matrix_conic(delta6, 3, -2, 13)
        M6_world = mat_mul(M_base2, M6)
        if not is_rotation_exact(M6_world):
            continue
        try:
            q6 = matrix_to_int_quat(M6_world, cap=CAP)
        except ValueError:
            continue
        targeted.append({'n': 6, 'kind': '393five+6th-onaxis', 't6': str(t6),
                          'quats': clique393_5 + [q6]})

    # (d) 183's {0,2,3} + 4th cube: integer quats, plus conic angles on
    #     each of the three simultaneous axes (extending the base=cube0
    #     identity gauge).
    clique183 = [RECORD_QUATS[4][0], RECORD_QUATS[4][2], RECORD_QUATS[4][3]]
    for ql in gen_int_quat_extension(clique183, 4000, rng):
        targeted.append({'n': 4, 'kind': '183triple+4th-intquat', 'quats': ql})
    for axis, d, pqs, t2t3 in [
            ((2, -3, 0), 13, (2, 3), None),
            ((3, 5, 0), 34, (3, 5), None),
            ((5, 2, 0), 29, (5, 2), None)]:
        mats = {i: quat_to_matrix_exact(*q) for i, q in
                [(0, RECORD_QUATS[4][0]), (2, RECORD_QUATS[4][2]), (3, RECORD_QUATS[4][3])]}
        res = find_clique_chain(mats, 0, _canon_line(axis), d, [pqs, (pqs[1], pqs[0])])
        if res is None:
            continue
        p, q, t_of = res
        for t4 in T_MENU_FULL:
            a = ConicAngle.from_t(Fr(t4), d)
            thetas_ordered = [ConicAngle.identity(d), ConicAngle.from_t(t_of[2], d),
                               ConicAngle.from_t(t_of[3], d), a]
            try:
                quats, _ = build_family_quats_conic(p, q, d, thetas_ordered, cap=CAP)
            except ValueError:
                continue
            targeted.append({'n': 4, 'kind': f'183triple+4th-onaxis-d{d}', 'p': p, 'q': q,
                              'd': d, 't4': str(t4), 'quats': quats})

    log(log_line6)
    append_report(f'### {log_line6}\n\n')
    log(f'{len(targeted)} targeted completion configs generated')
    by_n = {}
    for cfg in targeted:
        by_n.setdefault(cfg['n'], []).append(cfg)
    shards = shard_batches([(n, cfgs) for n, cfgs in by_n.items()])
    done = 0
    with mp.Pool(args.workers) as pool:
        for n, results in pool.imap_unordered(worker, shards):
            for cfg, total, depth in results:
                log_and_track(n, cfg, total, depth, tag='tier3-targeted')
            done += 1
            if done % 10 == 0 or done == len(shards):
                log(f'tier3 shard {done}/{len(shards)}, best: ' +
                    ', '.join(f'n={m}:{best[m][0]}' for m in args.n))
    # explicit 723 re-find check
    known723 = [r for r in by_n.get(6, []) if r['kind'] == '393five+6th-known723']
    if known723:
        r = run_cpp(known723[0]['quats'], n=6)
        log(f'393five+6th=(5,2,2,2) explicit re-find check: total={r["bounded"]} (expect 723)')
        append_report(f'### Tier 3 targeted completion: explicit 723 re-find check: '
                       f'total={r["bounded"]} (expect 723) -- '
                       f'{"CONFIRMED" if r["bounded"]==723 else "MISMATCH"}\n\n')
    append_report(f'### Tier 3 (targeted completion) done at {time.time()-t_start:.0f}s. '
                   f'Best so far: ' + ', '.join(f'n={n}:{best[n][0]}' for n in args.n) + '\n\n')

    # ---- Tier 4: hill-climb top candidates ----
    log('hill-climbing top candidates...')
    for round_i in range(args.neighbor_rounds):
        all_batches = []
        for n in args.n:
            _, cfg = best[n]
            if cfg is None or ('t' not in cfg and 't_list' not in cfg):
                all_batches.append((n, []))
                continue
            nb = gen_neighbor_configs(n, cfg, rng, T_MENU_FULL)
            all_batches.append((n, nb))
        shards = shard_batches(all_batches, chunk=200)
        with mp.Pool(args.workers) as pool:
            for n, results in pool.imap_unordered(worker, shards):
                for cfg, total, depth in results:
                    log_and_track(n, cfg, total, depth, tag=f'tier4-hillclimb-r{round_i+1}')
        log(f'hillclimb round {round_i+1} done, best: ' +
            ', '.join(f'n={m}:{best[m][0]}' for m in args.n))
    append_report(f'### Tier 4 (hill-climb) done at {time.time()-t_start:.0f}s. '
                   f'Best so far: ' + ', '.join(f'n={n}:{best[n][0]}' for n in args.n) + '\n\n')

    fh.close()
    log('DONE. Best per n:')
    summary = ['\n## FINAL sweep summary\n\n', '| n | best | record | deficit |\n',
               '|---|------|--------|---------|\n']
    for n in args.n:
        total, cfg = best[n]
        record = RECORDS.get(n)
        deficit = (total - record) if record else None
        log(f'  n={n}: best={total}  record={record}  deficit={deficit}  cfg={cfg}')
        summary.append(f'| {n} | {total} | {record} | {deficit} |\n')
    if FLAGGED:
        summary.append('\n**FLAGGED record-class results (verify manually before trusting):**\n\n')
        for f in FLAGGED:
            summary.append(f'- {f}\n')
    else:
        summary.append('\nNo record-class results (nothing >= record) were produced.\n')
    append_report(''.join(summary))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--gates-only', action='store_true')
    ap.add_argument('--run', action='store_true')
    args, _ = ap.parse_known_args()
    if args.gates_only:
        ok, info = run_all_gates()
        sys.exit(0 if ok else 1)
    else:
        main()
