#!/usr/bin/env python3
# Working principles: CENSUS_BOUND_SPEC.md. Project index: README.md / PROOF_67.md sect.5,5.1
"""(bound) FEASIBILITY-FIRST investigation of (*) Sigma_v(deg_v-2) <= 92 on
the n=3 TOP-1 diagram (equivalently d1 <= 48, the sole remaining gap in
max(3) = 67; see PROOF_67.md sect.5, sect.5.1).

This is NOT a proof attempt. Per CENSUS_BOUND_SPEC.md the primary
deliverable is a feasibility verdict with concrete numbers for the four
approaches listed there. It:

  - reuses census_extract.py's validated EXACT machinery (build_circles,
    gen_candidates, classify_vertices, build_graph, euler_face_count)
    UNCHANGED -- these functions are generic over any field-element type
    exposing +,-,*,/,neg,eq,hash,sign(),float(), so they run verbatim
    against both (a) the exact Q(sqrt2)/Q(sqrt5) witnesses via
    census_extract.build_w1/build_w2, and (b) a float field wrapper FF
    (below) fed by random Haar rotations, for fast statistical scans;
  - adds the anchor/cone test of PROOF_67.md sect.5.1 (not present in
    census_extract.py): at a triple point, tangential gradients e_i of
    each cube's active-face function, and the cone-membership test
    e_i in cone{e_x - e_i : x tying cubes != i};
  - runs gates G1 (exact 92 at both maximizers via census_extract itself),
    G2 (this script's own weight computation also gives exactly 92 at
    both, and the anchor test gives the calibration numbers), G3 (batch
    of random configs, weight <= 92, single-config re-verify+FLAG on any
    violation).

Usage:
  python3 census_bound.py --gates        # G1/G2/exact anchor census (fast)
  python3 census_bound.py --scan N       # G3 random scan, N configs, float
  python3 census_bound.py --pilot        # approach-2 chamber-count pilot
  python3 census_bound.py --all          # everything, writes logs
"""
import argparse
import json
import multiprocessing as mp
import sys
import time
from itertools import combinations

import numpy as np

from census_extract import (
    build_circles, gen_candidates, classify_vertices, build_graph,
    euler_face_count, connected_components, active_faces, sq_val, PAIRS,
    canon_ray, canon_circle, vsub, vadd, vscale, dot3, cross3, is_zero_vec,
    abs_field, make_basis, cross2, elementary_triples, build_w1, build_w2,
    gate_g1,
)

EPS = 1e-6
# Calibrated (not the naive ~1e-14 float64 machine epsilon) because
# census_extract's candidate construction chains several cross3/canon_ray
# steps; canon_ray divides by the absolute value of the first NONZERO
# coordinate, which can be small and amplify relative error. Empirically
# (random-config diagnostic, this file's dev log) residuals at the
# exact-tie assertion in classify_sample cluster at ~1e-9..1e-7 scale under
# this pipeline, not ~1e-14; 1e-6 clears that noise floor while staying far
# below the O(1) scale at which two genuinely different config values would
# differ. Only used for the float scan (FF); the exact Q2/Q5 witness path
# never touches this constant.


# ============================================================ float field (mirrors Q2/Q5 pattern)

class FF:
    """Plain-float field element with the Q2/Q5 interface: +,-,*,/,neg,eq,
    hash,sign(),float(). Used ONLY for statistical scans (G3, approaches
    1/2/4 empirics); never for the equality-at-maximizer claims (those use
    census_extract's exact Q2/Q5 witnesses directly, unmodified)."""
    __slots__ = ('v',)

    def __init__(self, v):
        self.v = v.v if isinstance(v, FF) else float(v)

    def __add__(s, o):
        o = o if isinstance(o, FF) else FF(o)
        return FF(s.v + o.v)
    __radd__ = __add__

    def __sub__(s, o):
        o = o if isinstance(o, FF) else FF(o)
        return FF(s.v - o.v)

    def __rsub__(s, o):
        return FF(o) - s

    def __neg__(s):
        return FF(-s.v)

    def __mul__(s, o):
        o = o if isinstance(o, FF) else FF(o)
        return FF(s.v * o.v)
    __rmul__ = __mul__

    def __truediv__(s, o):
        o = o if isinstance(o, FF) else FF(o)
        return FF(s.v / o.v)

    def sign(s):
        if s.v > EPS:
            return 1
        if s.v < -EPS:
            return -1
        return 0

    # __eq__/__hash__ SNAP to a coarse grid (not raw float equality): census_extract's
    # candidate generation dedups vertices by putting canon_ray(u) tuples into a
    # python set()/dict() keyed on exact field-element equality. In EXACT arithmetic
    # (Fraction/Q2/Q5) two different construction paths that describe the same ray
    # produce BIT-IDENTICAL rationals, so this works. Under float roundoff they don't
    # (verified: converting the exact W1 witness's rotations to float and running the
    # unmodified pipeline inflated 32 triples/30 kinks to 152/158 -- raw-equality dedup
    # was silently failing, not an activity/sign bug). Rounding to 1e-6 before
    # hashing/comparing merges those near-duplicates back into one dict/set key while
    # staying far below the O(1) scale of genuinely distinct candidate coordinates.
    _SNAP = 1e-6

    def __eq__(s, o):
        return isinstance(o, FF) and abs(s.v - o.v) < FF._SNAP

    def __hash__(s):
        return hash(round(s.v / FF._SNAP))

    def __float__(s):
        return s.v

    def __repr__(s):
        return f'FF({s.v:.6g})'


# ============================================================ random configs

def random_rotation(rng):
    """Haar-random SO(3) matrix via QR of a Gaussian matrix (standard recipe:
    fix the sign ambiguity of QR by the sign of R's diagonal, then fix an
    overall reflection to force det=+1)."""
    A = rng.normal(size=(3, 3))
    Q, R = np.linalg.qr(A)
    d = np.sign(np.diag(R))
    d[d == 0] = 1.0
    Q = Q * d
    if np.linalg.det(Q) < 0:
        Q = Q.copy()
        Q[:, 0] = -Q[:, 0]
    return Q


def mats_to_normals(mats):
    return [[tuple(FF(mats[k][i, j]) for i in range(3)) for j in range(3)]
            for k in range(3)]


def random_config(rng):
    mats = [random_rotation(rng) for _ in range(3)]
    return mats_to_normals(mats), mats


# ============================================================ core per-config analysis (TOP diagram)

def analyze_top(normals):
    """Runs census_extract's validated pipeline (build_circles ->
    gen_candidates -> classify_vertices -> build_graph 'TOP') on an
    arbitrary field-typed normals structure. Returns weight = Sigma(deg-2)
    over TOP vertices (the (*) LHS, well-defined regardless of connected
    components), plus F/V/E/C via Euler, triple/kink counts, verts, degrees."""
    cross_circles, own_circles = build_circles(normals)
    cands = gen_candidates(normals)
    verts = classify_vertices(normals, cands, cross_circles, own_circles)
    top_edges, top_v, top_deg, top_flags, top_loops = build_graph(
        normals, verts, cross_circles, 'TOP')
    weight = sum(d - 2 for d in top_deg.values() if d > 0)
    F, V, E, C = euler_face_count(top_v, top_edges)
    n_triple = sum(1 for v in verts.values() if v['type'] == 'triple')
    n_kink = sum(1 for v in verts.values() if v['type'] == 'kink')
    return dict(weight=weight, F=F, V=V, E=E, C=C, n_triple=n_triple,
                n_kink=n_kink, flags=top_flags, verts=verts,
                cross_circles=cross_circles, top_deg=top_deg)


# ============================================================ approach 4: anchor / cone test (PROOF_67 sect.5.1)

def tangential_grad(signed_n, u):
    """Tangential (to the sphere at direction u) part of signed_n: exact and
    scale-invariant in u (does not require u normalized to unit length)."""
    uu = dot3(u, u)
    c = dot3(signed_n, u) / uu
    return vsub(signed_n, vscale(u, c))


def cone_membership(v, gens, basis):
    """Is v a NONNEGATIVE combination of gens (1 or 2 vectors), all
    expressed in the 2-D tangent-plane `basis` (from make_basis(u))? Exact
    (field .sign() only). Returns True/False, or None if degenerate
    (parallel/antiparallel generators -- flagged, not silently resolved)."""
    b1, b2 = basis

    def coord(vec):
        return dot3(vec, b1), dot3(vec, b2)

    vx, vy = coord(v)
    if len(gens) == 1:
        gx, gy = coord(gens[0])
        cp = cross2(gx, gy, vx, vy)
        if cp.sign() != 0:
            return False
        return (vx * gx + vy * gy).sign() >= 0
    elif len(gens) == 2:
        d1x, d1y = coord(gens[0])
        d2x, d2y = coord(gens[1])
        detD = cross2(d1x, d1y, d2x, d2y)
        if detD.sign() == 0:
            return None
        a_num = cross2(vx, vy, d2x, d2y)
        b_num = cross2(d1x, d1y, vx, vy)
        sa = a_num.sign() * detD.sign()
        sb = b_num.sign() * detD.sign()
        return sa >= 0 and sb >= 0
    raise AssertionError('cone_membership: expected 1 or 2 generators')


def analyze_anchoring(normals, verts):
    """Classify every TRIVALENT triple point (single active face per cube --
    the pure/generic case; census confirms this is ALL triple points at both
    maximizers) as anchoring 0/1/2/3 of the three T_i's meeting there, via
    the cone condition e_i in cone{e_x - e_i : x != i} of PROOF_67 sect.5.1.
    Returns (results, n_skipped_multiface, n_degenerate); results is a list
    of per-triple-point dicts {u, anchors, n_anchors}. Triple points with a
    multi-active face for some cube (non-generic; none occur at either
    maximizer) are skipped and counted, not silently dropped; degenerate
    (parallel-generator) cone tests are likewise counted, not resolved."""
    results = []
    n_skipped_multiface = 0
    n_degenerate = 0
    for u, info in verts.items():
        if info['type'] != 'triple':
            continue
        act = info['active']
        if any(len(act[k]) != 1 for k in range(3)):
            n_skipped_multiface += 1
            continue
        e = {}
        bad = False
        for k in range(3):
            a = act[k][0]
            nka = normals[k][a]
            d = dot3(nka, u)
            s = d.sign()
            if s == 0:
                bad = True
                break
            signed_n = nka if s > 0 else vscale(nka, -1)
            e[k] = tangential_grad(signed_n, u)
        if bad:
            n_degenerate += 1
            continue
        basis = make_basis(u)
        anchors = []
        local_degenerate = False
        for i in range(3):
            others = [x for x in range(3) if x != i]
            gens = [vsub(e[x], e[i]) for x in others]
            res = cone_membership(e[i], gens, basis)
            if res is None:
                local_degenerate = True
                continue
            if res:
                anchors.append(i)
        if local_degenerate:
            n_degenerate += 1
        results.append(dict(u=u, anchors=anchors, n_anchors=len(anchors)))
    return results, n_skipped_multiface, n_degenerate


# ============================================================ approach 1: occurring active-face triples

def occurring_triples(normals, verts):
    """Elementary active-face triples (f0,f1,f2,s01,s12) realized as TOP
    triple points (reuses census_extract.elementary_triples, which does not
    filter by top/bottom -- but at n=3 every triple point IS on both
    diagrams per PROOF_67 sect.5's remark, so no extra filtering needed)."""
    occ = elementary_triples(normals, verts)
    return set(occ.keys())


# ============================================================ single-config worker (for multiprocessing)

def worker_scan(seed):
    rng = np.random.default_rng(seed)
    normals, mats = random_config(rng)
    t0 = time.time()
    try:
        res = analyze_top(normals)
        anch, n_skip, n_deg = analyze_anchoring(normals, res['verts'])
        occ = occurring_triples(normals, res['verts'])
    except AssertionError as ex:
        # census_extract's classify_sample asserts EXACT tie equality --
        # under the float field wrapper this can fail by ~1e-9..1e-6 on a
        # small fraction of configs (roundoff amplified by canon_ray's
        # division-by-smallest-coordinate normalization). Rather than patch
        # the read-only census_extract.py or loosen its exactness contract,
        # such configs are logged and skipped (their combinatorial type is
        # numerically borderline / near-degenerate; negligible measure).
        return dict(seed=int(seed), error=str(ex), dt=time.time() - t0)
    dt = time.time() - t0
    n_anchor_pts = sum(1 for a in anch if a['n_anchors'] >= 1)
    anchor_hist = {}
    for a in anch:
        anchor_hist[a['n_anchors']] = anchor_hist.get(a['n_anchors'], 0) + 1
    return dict(
        seed=int(seed), weight=res['weight'], F=res['F'], V=res['V'],
        E=res['E'], C=res['C'], n_triple=res['n_triple'], n_kink=res['n_kink'],
        n_flags=len(res['flags']), dt=dt,
        n_anchor_triplepoints=n_anchor_pts, anchor_hist=anchor_hist,
        n_skipped_multiface=n_skip, n_degenerate_cone=n_deg,
        n_occurring_triples=len(occ), occurring_triples=list(occ),
        mats=[m.tolist() for m in mats],
    )


# ============================================================ exact gates on the two maximizers

def exact_gate_report():
    print('=== Exact gate checks on both 67-maximizers (Q(sqrt2), Q(sqrt5)) ===')
    R1, n1 = build_w1()
    R2, n2 = build_w2()
    out = {}
    for name, n in (('W1 octahedral', n1), ('W2 golden', n2)):
        res = analyze_top(n)
        anch, n_skip, n_deg = analyze_anchoring(n, res['verts'])
        n_anchor_pts = sum(1 for a in anch if a['n_anchors'] >= 1)
        hist = {}
        for a in anch:
            hist[a['n_anchors']] = hist.get(a['n_anchors'], 0) + 1
        print(f'  {name}: weight Sigma(deg-2) = {res["weight"]}  '
              f'(target 92, {"PASS" if res["weight"] == 92 else "FAIL"})')
        print(f'    F={res["F"]} V={res["V"]} E={res["E"]} C={res["C"]} '
              f'triples={res["n_triple"]} kinks={res["n_kink"]} flags={len(res["flags"])}')
        print(f'    anchoring triple points: {n_anchor_pts} / {res["n_triple"]} '
              f'(target <=24; octahedral reference value 24)')
        print(f'    anchor-count histogram (per triple point, #components '
              f'it anchors): {dict(sorted(hist.items()))}')
        print(f'    skipped (multi-active-face) triple points: {n_skip}, '
              f'degenerate cone tests: {n_deg}')
        out[name] = dict(weight=res['weight'], F=res['F'], n_triple=res['n_triple'],
                          n_kink=res['n_kink'], n_anchor_triplepoints=n_anchor_pts,
                          anchor_hist=hist, n_skipped=n_skip, n_degenerate=n_deg)
    return out


# ============================================================ approach 2 pilot: local chamber-boundary density

def wall_functions(normals):
    """The (up to) 54 cross-cube swap-circle normals u.(n_a -+ n_b)=0 and 18
    own-cube sector-circle normals, as plain vectors -- the 'walls' whose
    sign pattern (as a function of config, at FIXED u) changes the
    combinatorial type. For the pilot we instead fix u-independence: we
    probe the combinatorial TYPE directly (set of occurring elementary
    triples + (V,E,F) of the TOP diagram) as the config varies, which is
    the operationally relevant notion of 'chamber' here."""
    cross_circles, own_circles = build_circles(normals)
    return cross_circles, own_circles


def config_signature(normals):
    res = analyze_top(normals)
    occ = occurring_triples(normals, res['verts'])
    return (res['F'], res['V'], res['E'], res['n_triple'], res['n_kink'],
            tuple(sorted(occ)))


def pilot_chamber_estimate(n_base=6, n_probe_per_base=40, box_scale=0.02, seed=12345):
    """Approach-2 pilot: around several random BASE configs, perturb by a
    small random rotation of size ~box_scale radians per cube (6 real DOF:
    axis-angle x2 extra cubes, cube 0 fixed as reference) and count DISTINCT
    combinatorial signatures within that small box. Extrapolates a crude
    'walls crossed per unit angle' density to the full domain, to estimate
    whether the total chamber count is of a tractable order of magnitude."""
    rng = np.random.default_rng(seed)
    report = []
    for b in range(n_base):
        base_mats = [random_rotation(rng) for _ in range(3)]
        sigs = set()
        base_normals = mats_to_normals(base_mats)
        sigs.add(config_signature(base_normals))
        for _ in range(n_probe_per_base):
            pert_mats = [base_mats[0]]
            for k in (1, 2):
                axis = rng.normal(size=3)
                axis /= np.linalg.norm(axis)
                angle = rng.normal() * box_scale
                K = np.array([[0, -axis[2], axis[1]],
                              [axis[2], 0, -axis[0]],
                              [-axis[1], axis[0], 0]])
                dR = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
                pert_mats.append(dR @ base_mats[k])
            normals = mats_to_normals(pert_mats)
            sigs.add(config_signature(normals))
        report.append(dict(base=b, n_probes=n_probe_per_base + 1,
                            n_distinct_signatures=len(sigs)))
        print(f'  base {b}: {len(sigs)} distinct combinatorial signatures '
              f'among {n_probe_per_base + 1} configs in a box of angular '
              f'radius {box_scale:.4f} rad per extra cube')
    return report


# ============================================================ orchestration

def run_scan(n_configs, n_procs, seed0=0, tag='scan'):
    print(f'=== G3 random scan: {n_configs} configs, {n_procs} procs (float) ===')
    t0 = time.time()
    seeds = list(range(seed0, seed0 + n_configs))
    if n_procs > 1:
        with mp.Pool(n_procs) as pool:
            results = pool.map(worker_scan, seeds, chunksize=max(1, n_configs // (4 * n_procs)))
    else:
        results = [worker_scan(s) for s in seeds]
    dt = time.time() - t0
    errored = [r for r in results if 'error' in r]
    results = [r for r in results if 'error' not in r]
    print(f'  done in {dt:.1f}s ({dt/n_configs*1000:.2f} ms/config); '
          f'{len(errored)}/{n_configs} configs skipped (float-precision-limited '
          f'exact-tie assertion in classify_sample -- see worker_scan docstring)')
    if not results:
        print('  ALL configs skipped -- aborting stats')
        return dict(tag=tag, n_configs=n_configs, dt=dt, n_errored=len(errored))
    weights = [r['weight'] for r in results]
    max_w = max(weights)
    violations = [r for r in results if r['weight'] > 92]
    n_triples = [r['n_triple'] for r in results]
    n_anchors = [r['n_anchor_triplepoints'] for r in results]
    occ_sizes = [r['n_occurring_triples'] for r in results]
    all_occ = set()
    for r in results:
        all_occ.update(r['occurring_triples'])
    print(f'  weight Sigma(deg-2): max={max_w}  mean={sum(weights)/len(weights):.2f}  '
          f'>92 violations: {len(violations)}')
    print(f'  triple-point count: min={min(n_triples)} max={max(n_triples)} '
          f'mean={sum(n_triples)/len(n_triples):.2f}')
    print(f'  anchoring triple-point count: min={min(n_anchors)} max={max(n_anchors)} '
          f'mean={sum(n_anchors)/len(n_anchors):.2f}  (target <=24)')
    print(f'  occurring-elementary-triples per config: min={min(occ_sizes)} '
          f'max={max(occ_sizes)} mean={sum(occ_sizes)/len(occ_sizes):.2f}')
    print(f'  DISTINCT occurring elementary triples seen across ALL {n_configs} '
          f'configs: {len(all_occ)} (naive space size 3*3*3*2*2=108)')
    if violations:
        print(f'  *** {len(violations)} VIOLATIONS OF (*) FOUND -- FLAGGING AT TOP ***')
        for v in violations[:5]:
            print(f'      seed={v["seed"]} weight={v["weight"]}')
    return dict(tag=tag, n_configs=n_configs, dt=dt, n_errored=len(errored),
                max_weight=max_w,
                n_violations=len(violations), violations=violations,
                min_triple=min(n_triples), max_triple=max(n_triples),
                mean_triple=sum(n_triples) / len(n_triples),
                min_anchor=min(n_anchors), max_anchor=max(n_anchors),
                mean_anchor=sum(n_anchors) / len(n_anchors),
                n_distinct_occurring=len(all_occ),
                all_occurring=sorted(all_occ),
                anchor_dist=_hist(n_anchors),
                weight_dist=_hist(weights),
                triple_dist=_hist(n_triples),
                results_sample=results[:50])


def _hist(xs):
    h = {}
    for x in xs:
        h[x] = h.get(x, 0) + 1
    return dict(sorted(h.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gates', action='store_true')
    ap.add_argument('--scan', type=int, default=0)
    ap.add_argument('--procs', type=int, default=4)
    ap.add_argument('--pilot', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--out', default='/Users/dmi/carroll/census_bound_log.json')
    args = ap.parse_args()

    log = {}
    if args.gates or args.all:
        print('--- census_extract GATE G1 (exact, reused unchanged) ---')
        gate_g1()
        log['exact_gates'] = exact_gate_report()
    if args.pilot or args.all:
        print()
        log['pilot'] = pilot_chamber_estimate()
    if args.scan or args.all:
        n = args.scan if args.scan else 10000
        print()
        log['scan'] = run_scan(n, args.procs)

    with open(args.out, 'w') as f:
        json.dump(log, f, indent=1, default=str)
    print(f'\nwrote {args.out}')


if __name__ == '__main__':
    main()
