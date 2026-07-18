#!/usr/bin/env python3
# Working principles: EVENTS_SPEC.md. Project index: README.md
"""EVENTS_SPEC.md executor -- the exact create-vs-merge event catalogue.

Tests the conjectured "+-1 region per coincidence" law across:
  - the n=3 dihedral family (Postscript 25 + addenda 1-4): the staircase
    25/31/43/55, the two 67-spikes (octahedral 35.264deg, golden 69.095deg
    + its mirror 20.905deg), the face-diagonal 49 (45deg), and the two
    band-edge walls (~9.5deg, and the psi=0 shared-axis point).
  - the n=4 resonance pair (Postscript 26/28): family plateau 175 vs the
    151 resonance vs the 143 chain variant.
  - the n=5 387 plateau (Postscript 29): the exact t5 interval and its two
    Farey-adjacent neighbors.

READ-ONLY validated engines (never edited, only imported/cloned patterns):
  q3_count.py    (Q(sqrt3) region counter -- dihedral-family Pythagorean psi)
  q6_count.py    (Q(sqrt6) region counter -- the 45deg face-diagonal point)
  slide3_q2.py   (Q(sqrt2) region counter -- octahedral 35.264/54.736deg)
  cube_compound_exact.py (Q5 = Q(sqrt5) field arithmetic + PHI_H/IPHI_H)
  certify_six.py (CN-interval + Q5-exact region counter -- golden points)
  golden_rotations.py (Rot wrapper)
  nfamily_common.py (PyAngle/quat exact arithmetic + exact_pair_crossings,
                      the validated RATIONAL interior-crossing counter --
                      reused here as a second-engine cross-check wherever
                      the config is rational; the golden dihedral matrices
                      derived below are NEW hand algebra, checked against
                      it below).

NEW code in this file (not previously validated, so self-tested against
known ledger numbers before being trusted for new claims -- see
`self_test()`):
  - a field-agnostic exact edge-edge coincidence census
    (`pair_census`) that generalizes nfamily_common.exact_pair_crossings
    two ways: (a) works over ANY field object exposing +,-,*,/ and
    .sign() (Fraction, or the Q2-pattern classes of slide3_q2/q3_count/
    q6_count, or cube_compound_exact.Q5), not just Fraction; (b) also
    classifies CORNER (|t|==1 or |s|==1) contacts and, via a set() over
    the field's own hashable tuples, dedupes them to physical points
    (exact equality, no tolerance) -- reproducing the golden census
    (18 interior + 54 corner label-pairs = 6 physical points, Postscript
    25 addendum 4) from scratch as its own validation.
  - hand-derived exact matrices for the two 67-spikes' MIRROR partners
    (54.736deg octahedral-mirror, 20.905deg golden-mirror) in the
    family's own frame, verified orthonormal + S^3=I in exact arithmetic
    before use.

Usage: python3 events_extract.py            # runs everything, writes
       events.jsonl, prints the law table to stdout.
       python3 events_extract.py selftest   # gates only.
"""
import json
import math
import sys
import time
from fractions import Fraction as Fr
from itertools import combinations, product

from golden_rotations import Rot
import q3_count
import q6_count
import slide3_q2
import cube_compound_exact as cce
import certify_six
import nfamily_common as nf

# --------------------------------------------------------------------------
# Field-agnostic exact edge-edge coincidence census (NEW, self-tested below)
# --------------------------------------------------------------------------

def fsign(x):
    """Exact sign, for Fraction (native ordering) or any Q2/Q5-pattern
    object exposing .sign()."""
    if hasattr(x, 'sign'):
        return x.sign()
    return (x > 0) - (x < 0)


def cube_edges(one, zero):
    """The 12 edges of [-1,1]^3 as (corner, direction) tuples of FIELD
    elements, identical convention to nfamily_common.EDGES_FR (edge class
    `a` = free axis; corner fixed at (+-1,+-1) on the other two axes).
    `one`/`zero` are the field's own 1 and 0 objects (so this works for
    Fraction, Q2-pattern classes, or Q5 uniformly)."""
    edges = []
    for a in range(3):
        o = [i for i in range(3) if i != a]
        for s1, s2 in product((-1, 1), repeat=2):
            c = [zero, zero, zero]
            c[o[0]] = one if s1 == 1 else -one
            c[o[1]] = one if s2 == 1 else -one
            d = [zero, zero, zero]
            d[a] = one
            edges.append((tuple(c), tuple(d), a))
    return edges


def _mat_vec(M, v, zero):
    out = []
    for i in range(3):
        s = zero
        for k in range(3):
            s = s + M[i][k] * v[k]
        out.append(s)
    return tuple(out)


def _cross(u, v):
    return (u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0])


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def pair_census(Mi, Mj, edges, zero):
    """Exact classification of every edge-edge coincidence between cube i
    and cube j (Mi, Mj: 3x3 field-element matrices; `edges`: cube_edges()
    output; `zero`: field zero, used as the running-sum seed).

    Returns (interior, corner):
      interior: list of (edge_i, edge_j, class_i, class_j) with the
        crossing strictly inside BOTH segments (-1<t<1 and -1<s<1) --
        same semantics as nfamily_common.exact_pair_crossings.
      corner: list of (edge_i, edge_j, class_i, class_j, point) where the
        crossing point is exact and within [-1,1] on both segments but
        touches a boundary (|t|==1 or |s|==1) -- a vertex-vertex or
        vertex-edge contact. `point` is a hashable tuple of field
        elements -- dedupe with set() to get physical (not label-pair)
        contact-point counts, exactly (field __eq__/__hash__, no
        tolerance).

    Method identical to nfamily_common.exact_pair_crossings (coplanarity
    via triple product, Cramer's rule on the two rows of D1xD2 with a
    nonzero component), generalized from Python-native `<`/`>` ordering
    (Fraction-only) to `fsign()` so it works over any ordered field with
    an exact .sign()."""
    ei_t = [(_mat_vec(Mi, c, zero), _mat_vec(Mi, d, zero), a) for c, d, a in edges]
    ej_t = [(_mat_vec(Mj, c, zero), _mat_vec(Mj, d, zero), a) for c, d, a in edges]
    interior, corner = [], []
    for ii, (C1, D1, ca) in enumerate(ei_t):
        for jj, (C2, D2, cb) in enumerate(ej_t):
            n = _cross(D1, D2)
            if all(fsign(x) == 0 for x in n):
                continue  # parallel
            w = _sub(C2, C1)
            if fsign(_dot(w, n)) != 0:
                continue  # not coplanar
            idx = next(k for k in range(3) if fsign(n[k]) != 0)
            r0, r1 = [k for k in range(3) if k != idx]
            a11, a12 = D1[r0], -D2[r0]
            a21, a22 = D1[r1], -D2[r1]
            b1, b2 = w[r0], w[r1]
            det = a11 * a22 - a12 * a21
            assert fsign(det) != 0, 'degenerate 2x2 despite nonzero n component'
            t = (b1 * a22 - a12 * b2) / det
            s = (a11 * b2 - b1 * a21) / det
            assert fsign(t * D1[idx] - s * D2[idx] - w[idx]) == 0, 'coplanar solve sanity failed'
            st_lo, st_hi = fsign(t + 1), fsign(t - 1)
            ss_lo, ss_hi = fsign(s + 1), fsign(s - 1)
            if not (st_lo >= 0 and st_hi <= 0 and ss_lo >= 0 and ss_hi <= 0):
                continue  # lines meet, but outside one or both segments
            if st_lo > 0 and st_hi < 0 and ss_lo > 0 and ss_hi < 0:
                interior.append((ii, jj, ca, cb))
            else:
                P = tuple(C1[k] + t * D1[k] for k in range(3))
                corner.append((ii, jj, ca, cb, P))
    return interior, corner


def census_compound(mats, zero, one, ref_fraction_check=False):
    """All-pairs census for a compound. Returns
    (interior_total, corner_label_pairs, corner_points_set, per_pair dict)."""
    edges = cube_edges(one, zero)
    per_pair = {}
    corner_points = set()
    tot_i = tot_c = 0
    for i, j in combinations(range(len(mats)), 2):
        inter, corn = pair_census(mats[i], mats[j], edges, zero)
        if ref_fraction_check:
            ref = nf.exact_pair_crossings(mats[i], mats[j])
            assert ref == len(inter), f'cross-check FAILED pair ({i},{j}): nfamily_common={ref} vs pair_census={len(inter)}'
        per_pair[(i, j)] = (len(inter), len(corn))
        tot_i += len(inter)
        tot_c += len(corn)
        for rec in corn:
            corner_points.add(rec[4])
    return tot_i, tot_c, len(corner_points), per_pair


# --------------------------------------------------------------------------
# Matrix builders -- n=3 dihedral family, named points
# --------------------------------------------------------------------------
# S(psi) = -I/2 + (3/2) n n^T + (sqrt3/2) [n]_x, n=(sin psi, cos psi, 0)
# (Postscript 25). Entry-by-entry (general s=sin psi, c=cos psi):
#   S00=-1/2+3s^2/2  S01=3sc/2        S02=sqrt3 c/2
#   S10=3sc/2        S11=-1/2+3c^2/2  S12=-sqrt3 s/2
#   S20=-sqrt3 c/2   S21=sqrt3 s/2    S22=-1/2
# q3_count.S_of(p,q,r) builds this for Pythagorean psi (s=p/r,c=q/r) in
# Q(sqrt3). For the irrational named points the field changes (Q(sqrt2)
# at the two octahedral points, Q(sqrt5) at the two golden points,
# Q(sqrt6) at 45deg); those are hand-derived below directly from the
# same S(psi) formula and CHECKED (orthonormal + S^3=I, exact) before use.

def mm(A, B, zero):
    return [[sum((A[i][k] * B[k][j] for k in range(3)), zero) for j in range(3)]
            for i in range(3)]


def check_S(S, one, zero, name):
    """Orthonormal + S^3=I, exact. Raises AssertionError on failure."""
    St = [[S[j][i] for j in range(3)] for i in range(3)]
    P = mm(St, S, zero)
    for i in range(3):
        for j in range(3):
            want = one if i == j else zero
            assert fsign(P[i][j] - want) == 0, f'{name}: not orthonormal at ({i},{j})'
    S2 = mm(S, S, zero)
    S3 = mm(S, S2, zero)
    for i in range(3):
        for j in range(3):
            want = one if i == j else zero
            assert fsign(S3[i][j] - want) == 0, f'{name}: S^3 != I at ({i},{j})'
    return S2


def triple_for_psi_pythagorean(p, q, r):
    """(I, S, S^2) at Pythagorean psi (Q(sqrt3)). Returns (mats, zero, one)."""
    S = q3_count.S_of(p, q, r)
    q3_count.assert_orthonormal(S)
    Z, O = q3_count.ZERO2, q3_count.ONE2
    S2 = mm(S.m, S.m, Z)
    IDENT = [[O if i == j else Z for j in range(3)] for i in range(3)]
    return [IDENT, S.m, S2], Z, O


def triple_octahedral():
    """psi = arcsin(1/sqrt3) = 35.264deg (Q(sqrt2)), hand-derived from
    S(psi) with sin=1/sqrt3, cos=sqrt2/sqrt3 (verified: every sqrt3
    cancels, leaving Q(sqrt2))."""
    Z, O, H = slide3_q2.ZERO2, slide3_q2.ONE2, slide3_q2.HALF2
    R = slide3_q2.R2_2  # sqrt2/2
    S = [[Z, R, R], [R, H, -H], [-R, H, -H]]
    S2 = check_S(S, O, Z, 'octahedral 35.264deg')
    IDENT = [[O if i == j else Z for j in range(3)] for i in range(3)]
    return [IDENT, S, S2], Z, O


def triple_octahedral_mirror():
    """psi = arctan(sqrt2) = 54.736deg (Q(sqrt2), mirror of the above:
    sin<->cos swapped, sin=sqrt2/sqrt3, cos=1/sqrt3)."""
    Z, O, H = slide3_q2.ZERO2, slide3_q2.ONE2, slide3_q2.HALF2
    R = slide3_q2.R2_2
    S = [[H, R, H], [R, Z, -R], [-H, R, -H]]
    S2 = check_S(S, O, Z, 'octahedral-mirror 54.736deg')
    IDENT = [[O if i == j else Z for j in range(3)] for i in range(3)]
    return [IDENT, S, S2], Z, O


def triple_facediag45():
    """psi = 45deg (Q(sqrt6)): S = (1/4)[[1,3,r6],[3,1,-r6],[-r6,r6,-2]]
    (Postscript 25's exact witness, reproduced here via the general S(psi)
    formula at sin=cos=1/sqrt2)."""
    Z, O = q6_count.ZERO2, q6_count.ONE2
    Q6 = q6_count.Q2
    S = [[Q6(Fr(1, 4)), Q6(Fr(3, 4)), Q6(0, Fr(1, 4))],
         [Q6(Fr(3, 4)), Q6(Fr(1, 4)), Q6(0, Fr(-1, 4))],
         [Q6(0, Fr(-1, 4)), Q6(0, Fr(1, 4)), Q6(Fr(-1, 2))]]
    S2 = check_S(S, O, Z, '45deg face-diagonal')
    IDENT = [[O if i == j else Z for j in range(3)] for i in range(3)]
    return [IDENT, S, S2], Z, O


def triple_golden():
    """tan psi = phi^2 = 69.095deg (Q(sqrt5)): S(psi) hand-derived using
    sin=phi/sqrt3, cos=1/(phi sqrt3), phi^2=phi+1, 1/phi^2=2-phi -- every
    sqrt3 cancels, leaving the classical golden matrix
    (1/2)[[phi,1,1/phi],[1,-1/phi,-phi],[-1/phi,phi,-1]] (Postscript 25)."""
    Z, O, H = cce.ZERO, cce.ONE, cce.HALF
    PHI_H, IPHI_H = cce.PHI_H, cce.IPHI_H
    S = [[PHI_H, H, IPHI_H], [H, -IPHI_H, -PHI_H], [-IPHI_H, PHI_H, -H]]
    S2 = check_S(S, O, Z, 'golden 69.095deg')
    IDENT = [[O if i == j else Z for j in range(3)] for i in range(3)]
    return [IDENT, S, S2], Z, O


def triple_golden_mirror():
    """psi = 90 - arctan(phi^2) = 20.905deg (Q(sqrt5), mirror: sin/cos
    swapped relative to triple_golden). Theorem M predicts identical
    counts to the golden point; verified below, not assumed."""
    Z, O, H = cce.ZERO, cce.ONE, cce.HALF
    PHI_H, IPHI_H = cce.PHI_H, cce.IPHI_H
    S = [[-IPHI_H, H, PHI_H], [H, PHI_H, -IPHI_H], [-PHI_H, IPHI_H, -H]]
    S2 = check_S(S, O, Z, 'golden-mirror 20.905deg')
    IDENT = [[O if i == j else Z for j in range(3)] for i in range(3)]
    return [IDENT, S, S2], Z, O


def region_count(mats, field='q3'):
    IDENT, S, S2 = mats
    if field == 'q3':
        total, bd = q3_count.exact_count_q2([Rot(IDENT), Rot(S), Rot(S2)])
    elif field == 'q2':
        total, bd = slide3_q2.exact_count_q2([Rot(IDENT), Rot(S), Rot(S2)])
    elif field == 'q6':
        total, bd = q6_count.exact_count_q2([Rot(IDENT), Rot(S), Rot(S2)])
    elif field == 'q5':
        total, bd = certify_six.exact_count_config([Rot(IDENT), Rot(S), Rot(S2)], verbose=False)
    else:
        raise ValueError(field)
    return total, {k: v for k, v in bd.items() if k > 0}


def small_pyth(m, n):
    """Pythagorean triple (2mn, m^2-n^2, m^2+n^2) reduced -- used to reach
    arbitrarily small nonzero psi (menu triples bottom out ~5.7deg)."""
    p, q, r = 2 * m * n, m * m - n * n, m * m + n * n
    g = math.gcd(math.gcd(p, q), r)
    return p // g, q // g, r // g


# --------------------------------------------------------------------------
# n=4 and n=5: rational integer-quaternion configs (Fraction field)
# --------------------------------------------------------------------------

def mats_from_quats(quats):
    return [nf.quat_to_matrix_exact(*q) for q in quats]


N4_CONFIGS = {
    '175_plateau': [(1, 0, 0, 0), (7, 3, 4, 0), (12, 21, 28, 0), (-91, 183, 244, 0)],
    '151_resonance': [(1, 0, 0, 0), (-1, 2, 1, 0), (2, 2, 1, 0), (7, -2, -1, 0)],
    '143_chain': [(1, 0, 0, 0), (15, 4, 3, 0), (20, 12, 9, 0), (45, 52, 39, 0)],
}

N5_CONFIGS = {
    't5=1/5_below':      [[1,0,0,0],[-6,-10,15,0],[4,-6,9,0],[5,2,-3,0],[5,-2,3,0]],
    't5=8/39_edge_lo':    [[1,0,0,0],[-6,-10,15,0],[4,-6,9,0],[5,2,-3,0],[39,-16,24,0]],
    't5=3/14_edge_hi':    [[1,0,0,0],[-6,-10,15,0],[4,-6,9,0],[5,2,-3,0],[14,-6,9,0]],
    't5=2/9_above':       [[1,0,0,0],[-6,-10,15,0],[4,-6,9,0],[5,2,-3,0],[9,-4,6,0]],
}


# --------------------------------------------------------------------------
# Self-test / gates
# --------------------------------------------------------------------------

def self_test():
    print('=== G1: staircase totals + spikes (field engines) ===')
    Z, O = q3_count.ZERO2, q3_count.ONE2

    # Central plateau (two Pythagorean witnesses, mirror pair)
    for p, q, r, want in [(3, 4, 5, 55), (4, 3, 5, 55)]:
        mats, *_ = triple_for_psi_pythagorean(p, q, r)
        total, bd = region_count(mats, 'q3')
        assert total == want, (p, q, r, total)
        assert bd == {1: 36, 2: 18, 3: 1}, bd
    print('  central plateau psi=36.87/53.13deg: 55={36,18,1}  PASS (both mirror witnesses)')

    # shared-axis point psi=0 (isolated)
    mats, *_ = triple_for_psi_pythagorean(0, 1, 1)
    total, bd = region_count(mats, 'q3')
    assert (total, bd) == (25, {1: 12, 2: 12, 3: 1}), (total, bd)
    print('  shared-axis psi=0: 25={12,12,1}  PASS')

    # 31-plateau: generic small psi (both very close to 0 and near 9.5deg)
    for p, q, r in [small_pyth(1000, 1), (13, 84, 85)]:
        mats, *_ = triple_for_psi_pythagorean(p, q, r)
        total, bd = region_count(mats, 'q3')
        assert (total, bd) == (31, {1: 18, 2: 12, 3: 1}), (p, q, r, total, bd)
    print('  31-plateau (generic small psi, both near 0 and near 9.5deg): 31={18,12,1}  PASS')

    # 43-plateau
    for p, q, r in [(11, 60, 61), (12, 35, 37)]:
        mats, *_ = triple_for_psi_pythagorean(p, q, r)
        total, bd = region_count(mats, 'q3')
        assert (total, bd) == (43, {1: 24, 2: 18, 3: 1}), (p, q, r, total, bd)
    print('  43-plateau: 43={24,18,1}  PASS')

    # spikes
    mats, Z2, O2 = triple_octahedral()
    total, bd = region_count(mats, 'q2')
    assert (total, bd) == (67, {1: 48, 2: 18, 3: 1}), (total, bd)
    print('  octahedral 35.264deg: 67={48,18,1}  PASS')

    mats, *_ = triple_octahedral_mirror()
    total, bd = region_count(mats, 'q2')
    assert (total, bd) == (67, {1: 48, 2: 18, 3: 1}), (total, bd)
    print('  octahedral-mirror 54.736deg: 67={48,18,1}  PASS')

    mats, *_ = triple_facediag45()
    total, bd = region_count(mats, 'q6')
    assert (total, bd) == (49, {1: 30, 2: 18, 3: 1}), (total, bd)
    print('  face-diagonal 45deg: 49={30,18,1}  PASS')

    mats, *_ = triple_golden()
    total, bd = region_count(mats, 'q5')
    assert (total, bd) == (67, {1: 48, 2: 18, 3: 1}), (total, bd)
    print('  golden 69.095deg: 67={48,18,1}  PASS')

    mats, *_ = triple_golden_mirror()
    total, bd = region_count(mats, 'q5')
    assert (total, bd) == (67, {1: 48, 2: 18, 3: 1}), (total, bd)
    print('  golden-mirror 20.905deg: 67={48,18,1}  PASS')

    print('\n=== G2: crossing counter reproduces known censuses ===')
    mats, Z, O = triple_for_psi_pythagorean(3, 4, 5)
    ti, tc, tp, _ = census_compound(mats, Z, O)
    assert (ti, tc) == (18, 0), (ti, tc)
    print('  core-18 (mid-band, psi=36.87deg): interior=18 corner=0  PASS')

    mats, Z2, O2 = triple_octahedral()
    ti, tc, tp, _ = census_compound(mats, Z2, O2)
    assert (ti, tc) == (30, 0), (ti, tc)
    print('  octahedral 35.264deg: interior=30 corner=0  PASS')

    mats, Z6, O6 = triple_facediag45()
    ti, tc, tp, _ = census_compound(mats, Z6, O6)
    assert (ti, tc) == (24, 0), (ti, tc)
    print('  45deg: interior=24 corner=0  PASS')

    mats, Z5, O5 = triple_golden()
    ti, tc, tp, _ = census_compound(mats, Z5, O5)
    assert (ti, tc, tp) == (18, 54, 6), (ti, tc, tp)
    print('  golden 69.095deg: interior=18 corner_label_pairs=54 physical_points=6'
          ' (18+6=24 total contacts)  PASS')

    print('\nALL GATES PASS\n')


# --------------------------------------------------------------------------
# Main: build the full event catalogue
# --------------------------------------------------------------------------

def n3_side(name, triple, field):
    mats, zero, one = triple
    total, bd = region_count(mats, field)
    ti, tc, tp, per_pair = census_compound(mats, zero, one)
    return dict(name=name, total=total, by_depth=bd, interior=ti,
                corner_label_pairs=tc, corner_points=tp, per_pair=per_pair)


def make_event(name, family, engine, sideA, sideB, note=''):
    dcount = sideB['total'] - sideA['total']
    all_depths = sorted(set(sideA['by_depth']) | set(sideB['by_depth']))
    ddepth = {d: sideB['by_depth'].get(d, 0) - sideA['by_depth'].get(d, 0) for d in all_depths}
    dint = sideB['interior'] - sideA['interior']
    dcorner_lp = sideB['corner_label_pairs'] - sideA['corner_label_pairs']
    dcorner_pt = sideB['corner_points'] - sideA['corner_points']
    dcoin_total = dint + dcorner_pt  # "coincidence units": interior crossings + physical corner points
    ratio = (dcount / dcoin_total) if dcoin_total != 0 else None
    return dict(
        event=name, family=family, engine=engine,
        sideA=dict(total=sideA['total'], by_depth=sideA['by_depth'],
                   interior=sideA['interior'], corner_label_pairs=sideA['corner_label_pairs'],
                   corner_points=sideA['corner_points']),
        sideB=dict(total=sideB['total'], by_depth=sideB['by_depth'],
                   interior=sideB['interior'], corner_label_pairs=sideB['corner_label_pairs'],
                   corner_points=sideB['corner_points']),
        delta_count=dcount, delta_depth=ddepth,
        delta_interior=dint, delta_corner_label_pairs=dcorner_lp,
        delta_corner_points=dcorner_pt, delta_coincidence_units=dcoin_total,
        ratio_count_per_coincidence=ratio, note=note)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        self_test()
        return

    t0 = time.time()
    self_test()

    events = []

    # ---------------- n=3 dihedral family ----------------
    print('=== n=3 dihedral family event catalogue ===')
    Z3, O3 = q3_count.ZERO2, q3_count.ONE2

    side_psi0 = n3_side('psi=0 (shared-axis, isolated)', triple_for_psi_pythagorean(0, 1, 1), 'q3')
    side_gen_small = n3_side('psi->0+ (generic, 31-plateau)', triple_for_psi_pythagorean(*small_pyth(1000, 1)), 'q3')
    side_31 = n3_side('psi=8.797deg (31-plateau)', triple_for_psi_pythagorean(13, 84, 85), 'q3')
    side_43 = n3_side('psi=10.389deg (43-plateau)', triple_for_psi_pythagorean(11, 60, 61), 'q3')
    side_55 = n3_side('psi=36.87deg (55-plateau, core)', triple_for_psi_pythagorean(3, 4, 5), 'q3')

    side_oct = n3_side('psi=35.264deg (octahedral spike)', triple_octahedral(), 'q2')
    side_octm = n3_side('psi=54.736deg (octahedral-mirror spike)', triple_octahedral_mirror(), 'q2')

    side_45 = n3_side('psi=45deg (face-diagonal)', triple_facediag45(), 'q6')

    side_gold = n3_side('psi=69.095deg (golden spike)', triple_golden(), 'q5')
    side_goldm = n3_side('psi=20.905deg (golden-mirror spike)', triple_golden_mirror(), 'q5')

    events.append(make_event('shared-axis point (psi=0, negative mega-spike)', 'n3-dihedral',
                              'q3_count.py', side_gen_small, side_psi0,
                              note='psi=0 is an ISOLATED point (measure zero), not the left end '
                                   'of an open plateau -- CORRECTS Postscript 25 addendum 3\'s '
                                   'table entry "(0,~9.6deg): 25", which is only the single point '
                                   'psi=0/90 itself; the generic value immediately surrounding it '
                                   'is 31 (verified down to psi=0.0002deg). Huge coincidence GAIN '
                                   '(interior 12->48) with a count LOSS -- merge-dominated.'))
    events.append(make_event('band-edge wall ~9.5deg (31->43, no-coincidence)', 'n3-dihedral',
                              'q3_count.py + nfamily_common-pattern census', side_31, side_43,
                              note='Interior crossing count UNCHANGED (12->12) across this wall '
                                   '-- a pure d1/d2 combinatorial (top/bottom-diagram) event with '
                                   'ZERO coincidence change, confirming Postscript 25 addendum 3 '
                                   'point 4. Law EXCEPTION (denominator zero).'))
    events.append(make_event('band-edge wall (43->55, = golden-mirror spike)', 'n3-dihedral',
                              'q3_count.py -> Q5 exact at the spike', side_43, side_goldm,
                              note='This "wall" is not a separate no-coincidence event: it '
                                   'coincides exactly with the golden-mirror spike at '
                                   'psi=20.905deg -- see that event below.'))
    events.append(make_event('octahedral spike (55->67, interior +12)', 'n3-dihedral',
                              'slide3_q2.py (Q(sqrt2))', side_55, side_oct,
                              note='Pure interior-crossing creation: 18->30 (+12), Delta d1=+12, '
                                   'Delta d2=Delta d3=0. Exactly +1 region per crossing, and the '
                                   'entire effect lands in d1.'))
    events.append(make_event('octahedral-mirror spike (55->67, interior +12)', 'n3-dihedral',
                              'slide3_q2.py (Q(sqrt2))', side_55, side_octm,
                              note='Mirror of the above under psi<->90-psi (Theorem M): identical '
                                   'mechanism and ratio.'))
    events.append(make_event('face-diagonal 45deg (55->49, interior +6, MERGE)', 'n3-dihedral',
                              'q6_count.py (Q(sqrt6))', side_55, side_45,
                              note='Interior crossings 18->24 (+6) but count DROPS 55->49 (-6): '
                                   'exactly -1 region per crossing. Same coincidence-count '
                                   'magnitude as the octahedral spike, opposite sign.'))
    events.append(make_event('golden spike (55->67, corner-docking, +12 via 6 points)', 'n3-dihedral',
                              'certify_six.py (Q5 exact)', side_55, side_gold,
                              note='Interior crossings UNCHANGED (18->18); the +12 is bought '
                                   'entirely by 54 new corner label-pairs = 6 physical vertex-'
                                   'vertex contact points (+2 count per new corner point). A '
                                   'DIFFERENT mechanism from the octahedral spike reaching the '
                                   'same total 67 via the same Delta d1=+12.'))
    events.append(make_event('golden-mirror spike (43->67, mixed mechanism)', 'n3-dihedral',
                              'certify_six.py (Q5 exact)', side_43, side_goldm,
                              note='Approaching from the 43-plateau side (not 55): interior '
                                   '12->18 (+6) AND 6 new corner points appear simultaneously '
                                   '(0->54 label-pairs); Delta count=+24 lands entirely in d1. '
                                   'This is the true location of the crossing-SET change '
                                   'Postscript 25 addendum 2 places at psi=20.905deg.'))

    # ---------------- n=4 resonance pair ----------------
    print('=== n=4 resonance-pair event catalogue ===')
    ZF, OF = Fr(0), Fr(1)
    n4_sides = {}
    for name, quats in N4_CONFIGS.items():
        mats = mats_from_quats(quats)
        ti, tc, tp, per_pair = census_compound(mats, ZF, OF, ref_fraction_check=True)
        # region count for these already established in the ledger
        # (nfamily_report.md / resonance4_report.md / nfamily_gates.out);
        # recompute here with the C++/py oracle pattern via certify_six's
        # sibling: reuse nfamily's own validated engine indirectly by
        # trusting the ledger total (both engines already agreed there)
        # but ALSO independently recompute with q3_count's generic
        # exact_count_q2 core (field-agnostic at Fraction b=0) as a second
        # engine for this script's own claim:
        rots = [Rot(m) for m in mats]
        # slide3_q2.exact_count_q2 works over its own Q2 class; for pure
        # rationals we can feed Fraction-valued Rot objects directly into
        # q3_count.exact_count_q2 (it only uses +,-,*,/,.sign() through
        # Q2 objects -- so wrap each Fraction entry as Q2(x,0)):
        def wrapQ(v):
            return q3_count.Q2(v, 0)
        rots_q = [Rot([[wrapQ(m[i][j]) for j in range(3)] for i in range(3)]) for m in mats]
        total, bd = q3_count.exact_count_q2(rots_q)
        bd = {k: v for k, v in bd.items() if k > 0}
        n4_sides[name] = dict(name=name, total=total, by_depth=bd, interior=ti,
                               corner_label_pairs=tc, corner_points=tp, per_pair=per_pair)
        print(f'  {name}: total={total} by_depth={bd} interior={ti} corner_lp={tc} corner_pts={tp}')

    events.append(make_event('n=4 family plateau -> 151 resonance (175->151, MERGE)', 'n4-resonance',
                              'nfamily_common (Fraction, cross-checked) + q3_count.exact_count_q2 '
                              '(second engine, Fraction-as-Q2(.,0))',
                              n4_sides['175_plateau'], n4_sides['151_resonance'],
                              note='Delta total=-24 (matches resonance4_report.md exactly). '
                                   'Delta interior=+2 (36->38), corner structure UNCHANGED '
                                   '(54 label-pairs / 6 points both sides). The ENTIRE -24 lands '
                                   'in d1 (92->68); d2=58,d3=24,d4=1 all identical both sides. '
                                   'The n=3 "+1 per crossing" law is FALSIFIED here even in SIGN: '
                                   'coincidences went UP (+2) while count went DOWN (-24).'))
    events.append(make_event('n=4 family plateau -> 143 chain variant (175->143, MERGE)', 'n4-resonance',
                              'nfamily_common (Fraction, cross-checked) + q3_count.exact_count_q2',
                              n4_sides['175_plateau'], n4_sides['143_chain'],
                              note='Delta total=-32. Delta interior=-6 (36->30), Delta corner '
                                   'points=-6 (6->0, i.e. -54 label-pairs). Using PHYSICAL '
                                   'coincidence units (interior + corner points): Delta=-12 for '
                                   'Delta count=-32, ratio -2.67/unit -- still not +-1.'))

    # ---------------- n=5 387 plateau edges ----------------
    print('=== n=5 387-plateau-edge event catalogue ===')
    n5_sides = {}
    for name, quats in N5_CONFIGS.items():
        mats = mats_from_quats(quats)
        ti, tc, tp, per_pair = census_compound(mats, ZF, OF, ref_fraction_check=True)
        def wrapQ(v):
            return q3_count.Q2(v, 0)
        rots_q = [Rot([[wrapQ(m[i][j]) for j in range(3)] for i in range(3)]) for m in mats]
        total, bd = q3_count.exact_count_q2(rots_q)
        bd = {k: v for k, v in bd.items() if k > 0}
        n5_sides[name] = dict(name=name, total=total, by_depth=bd, interior=ti,
                               corner_label_pairs=tc, corner_points=tp, per_pair=per_pair)
        print(f'  {name}: total={total} by_depth={bd} interior={ti} corner_lp={tc} corner_pts={tp}')

    events.append(make_event('n=5 387-plateau lower edge (t5: 1/5 -> 8/39, MERGE outward)', 'n5-rattan',
                              'nfamily_common (Fraction, cross-checked) + q3_count.exact_count_q2',
                              n5_sides['t5=1/5_below'], n5_sides['t5=8/39_edge_lo'],
                              note='Delta total=+4 (383->387) entering the plateau. Interior '
                                   'UNCHANGED (58->58) the whole way; the event is purely a '
                                   'corner-point LOSS: 8->6 physical vertex-vertex points '
                                   '(cube0-cube4 contact vanishes, -18 label-pairs). Losing a '
                                   'coincidence GAINS 4 regions here: ratio -2/point.'))
    events.append(make_event('n=5 387-plateau upper edge (t5: 3/14 -> 2/9, MERGE outward)', 'n5-rattan',
                              'nfamily_common (Fraction, cross-checked) + q3_count.exact_count_q2',
                              n5_sides['t5=3/14_edge_hi'], n5_sides['t5=2/9_above'],
                              note='Delta total=-8 (387->379) leaving the plateau on the other '
                                   'side. Interior again UNCHANGED (58->58); a DIFFERENT '
                                   'corner-point gain appears (cube3-cube4 contact, +18 label-'
                                   'pairs, +2 points), and here count DROPS by 8: ratio -4/point '
                                   '-- the SAME coincidence-unit magnitude (2 points) as the lower '
                                   'edge but a DIFFERENT count consequence (-4 vs -2 per point), '
                                   'depending on WHICH pair of cubes touches.'))

    # ---------------- write outputs ----------------
    with open('events.jsonl', 'w') as f:
        for ev in events:
            f.write(json.dumps(ev, default=str) + '\n')

    print(f'\nWrote {len(events)} events to events.jsonl ({time.time()-t0:.1f}s total)')

    print('\n=== LAW TABLE SUMMARY ===')
    print(f"{'event':60s} {'dcount':>7s} {'dint':>6s} {'dcorner_pt':>11s} {'dcoin':>6s} {'ratio':>8s}")
    for ev in events:
        r = ev['ratio_count_per_coincidence']
        rs = f'{r:+.3f}' if r is not None else 'undef(0)'
        print(f"{ev['event'][:60]:60s} {ev['delta_count']:+7d} {ev['delta_interior']:+6d} "
              f"{ev['delta_corner_points']:+11d} {ev['delta_coincidence_units']:+6d} {rs:>8s}")


if __name__ == '__main__':
    main()
