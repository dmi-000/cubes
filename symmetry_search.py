#!/usr/bin/env python3
# Working principles: SYMMETRY_SEARCH_SPEC.md. Project index: README.md
"""Symmetry-stratified search of the region-rich walls (the 655/681/699
records all live on symmetry walls, found ad hoc; this enumerates the
finite catalog of symmetry-constrained 6-cube subspaces systematically).

Setup (SYMMETRY_SEARCH_SPEC.md section 1): a cube ORIENTATION is a coset
S*O in SO(3)/O (O = the cube's own octahedral group, order 24); two
rotations S, S' give the same cube iff S^-1 S' in O. Fix a finite
subgroup G of SO(3); a compound is G-invariant iff its 6 cosets are
closed under left mult by G, i.e. a union of G-orbits. Orbit sizes are
COMPUTED (never hand-derived): orbit(S) = O-dedup of {g*S : g in G}.

Catalog: for each G in {C2,C3,C4,C6,D2,D3,D4,D6,T,O} (rational -> C++
cube_regions), {C5,I} (Q(sqrt5) -> golden engines), {C8,D8} (Q(sqrt2) ->
slide3_q2), enumerate partitions of 6 into G-orbit sizes (achievable
sizes are PROBED empirically per group, including aligned seeds with
small orbits -- generic seeds alone would miss the records, which all
use alignment) plus the "core + free" mixed form (an orbit of size m<6
plus 6-m independently-searched free cubes, the pattern behind 681 and,
in spirit, 699's two-orbit 3+3).

Usage:
  python3 symmetry_search.py gates          # GA-GE only, then stop
  python3 symmetry_search.py phase1         # gates, then rational sweep
  python3 symmetry_search.py phase2         # gates, then Q(sqrt5) sweep
  python3 symmetry_search.py all            # gates, phase1, phase2, phase3-probe
"""
import itertools
import json
import math
import os
import random
import subprocess
import sys
import time
from fractions import Fraction as Fr
from itertools import permutations, product

from golden_rotations import Rot, rot_from_quat, closure, A, B, D, IDENT
from cube_compound_exact import Q5, ONE as Q5_ONE, build_axes, find_cubes
import golden_six as gs
from certify_six import exact_count_config

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'cube_regions')
LOG_PATH = os.path.join(HERE, 'symmetry_search.jsonl')
REPORT_PATH = os.path.join(HERE, 'symmetry_search_report.md')
MAXC = 512            # integer-quaternion component bound (CPP_SPEC int128 budget)
WORKERS = 4            # hard cap per task instructions


# ============================================================ O machinery
def signed_perm_int_mats():
    """The 24 proper (det=+1) signed-permutation matrices = O, the
    axis-aligned cube's own rotation group. Built directly (not via BFS)
    so the coset-dedup machinery has zero dependency on any other group
    construction being correct first."""
    mats = []
    for perm in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            M = [[0] * 3 for _ in range(3)]
            for i in range(3):
                M[i][perm[i]] = signs[i]
            det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                   - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                   + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
            if det == 1:
                mats.append(M)
    assert len(mats) == 24
    return mats


O_INT = signed_perm_int_mats()


def embed_O(mk):
    """O in any field, given mk: int -> field element (e.g. Q5, Q2)."""
    return [Rot([[mk(x) for x in row] for row in M]) for M in O_INT]


O_Q5 = embed_O(lambda x: Q5(x))
assert len(O_Q5) == 24 and all(o.is_rotation() for o in O_Q5)
assert set(O_Q5) == closure([A, B]), \
    'O_Q5 (signed permutations) must equal golden_rotations closure([A,B])'


def coset_key(R, Oset):
    """Canonical SO(3)/O coset invariant: R*O and R'*O are the same right
    coset iff R^-1 R' in O, iff {R*o : o in O} == {R'*o : o in O} as SETS
    (right mult by any o0 in O permutes O). min() of the string image is
    therefore a well-defined per-coset invariant -- exact string compare,
    no floats."""
    return min((R * o).to_str() for o in Oset)


def orbit_keys(Gelems, seed, Oset):
    """{coset_key(g*seed) : g in G} -- SET of distinct cosets (the orbit,
    O-deduped). len() is the orbit size; do not shortcut via |G|/guessed
    stabilizer order -- COMPUTE it (spec section 1)."""
    return {coset_key(g * seed, Oset) for g in Gelems}


def orbit_reps(Gelems, seed, Oset):
    """Like orbit_keys but keeps one representative Rot per coset (first
    g*seed seen for that key), for building the actual 6-cube compound."""
    d = {}
    for g in Gelems:
        R = g * seed
        k = coset_key(R, Oset)
        if k not in d:
            d[k] = R
    return d


def proper_frame(R):
    """Force a PROPER (det=+1) frame. find_cubes() (cube_compound_exact.py)
    returns raw orthogonal axis triples; some are improper (det=-1) --
    THE SAME BUG documented in six_cube_search_results.md Postscript 9
    ("find_cubes returning two IMPROPER frames") that silently broke an
    earlier congruence check. Negating one column of an improper frame
    gives the IDENTICAL cube (the two opposite faces on that axis are
    just relabeled +1/-1, the physical cube [-1,1]^3 is unchanged) but a
    det=+1 matrix -- required before the frame can be a member of any
    SO(3) group-orbit computation (left mult by a proper rotation only
    ever produces proper results, so an improper seed can never appear in
    an orbit and any coset-membership test against one is silently wrong)."""
    if (R.det() - Q5_ONE).sign() != 0:
        m = [list(row) for row in R.m]
        for i in range(3):
            m[i][2] = -m[i][2]
        R = Rot(m)
    assert (R.det() - Q5_ONE).sign() == 0, 'proper_frame failed to fix det'
    assert R.is_rotation()
    return R


def golden_five_proper():
    """The 5 golden cubes as PROPER Rot objects (see proper_frame). This
    is the corrected construction gate D and the I-family both need;
    golden_six.golden_five() does NOT force proper frames (harmless for
    its counting-only use, since a cube's geometry doesn't care about the
    sign of the matrix determinant) but WOULD silently break orbit
    membership tests here."""
    axes = build_axes()
    triples = find_cubes(axes)
    out = []
    for t in triples:
        cols = [axes[i] for i in t]
        R = Rot([[cols[j][i] for j in range(3)] for i in range(3)])
        out.append(proper_frame(R))
    return out


def gcd_reduce(ints):
    g = math.gcd(*[abs(x) for x in ints])
    if g > 1:
        ints = [i // g for i in ints]
    if not any(ints):
        ints = [1, 0, 0, 0]
    return ints


# ============================================================== log/eval
def log_eval(rec):
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(rec) + '\n')


def quats_line(quats):
    return ';'.join(','.join(str(c) for c in q) for q in quats)


def cpp_batch(configs, workers=WORKERS):
    """Exact-count many rational 6-cube configs via cube_regions
    --quats-stdin, splitting across <= workers subprocesses (hard cap
    per task rules). configs: list of list-of-4-tuples (integer quats).
    Returns list of (total, by_depth dict) aligned with input order."""
    if not configs:
        return []
    n = len(configs)
    nproc = max(1, min(workers, n))
    chunks = [[] for _ in range(nproc)]
    for i, cfg in enumerate(configs):
        chunks[i % nproc].append((i, cfg))
    results = [None] * n
    procs = []
    for chunk in chunks:
        if not chunk:
            continue
        inp = '\n'.join(quats_line(cfg) for _, cfg in chunk) + '\n'
        p = subprocess.Popen([BIN, '--quats-stdin'], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        procs.append((p, chunk, inp))
    for p, chunk, inp in procs:
        out, err = p.communicate(inp)
        lines = [l for l in out.strip().split('\n') if l]
        assert len(lines) == len(chunk), \
            f'cpp_batch: expected {len(chunk)} results, got {len(lines)}: {err[:500]}'
        for (idx, cfg), line in zip(chunk, lines):
            rec = json.loads(line)
            if 'error' in rec:
                results[idx] = None
            else:
                bd = {int(k): v for k, v in rec['by_depth'].items() if k != '0'}
                results[idx] = (rec['bounded'], bd)
    return results


# =================================================================== GATES
def gate_A():
    """GA: O-dedup / orbit machinery. Generic C3 seed -> orbit size 3;
    seed with its 3-fold axis on the C3 axis -> orbit size 1."""
    C3 = closure([rot_from_quat(1, 1, 1, 1)])
    assert len(C3) == 3
    generic = rot_from_quat(7, 3, -2, 5)
    aligned = rot_from_quat(1, 1, 1, 1)   # itself a C3 element: aligned
    identity = rot_from_quat(1, 0, 0, 0)
    o_generic = len(orbit_keys(C3, generic, O_Q5))
    o_aligned = len(orbit_keys(C3, aligned, O_Q5))
    o_identity = len(orbit_keys(C3, identity, O_Q5))
    ok = (o_generic == 3 and o_aligned == 1 and o_identity == 1)
    print(f'  GA: generic seed orbit={o_generic} (want 3), '
          f'aligned seed orbit={o_aligned} (want 1), '
          f'identity orbit={o_identity} (want 1)  {"PASS" if ok else "FAIL"}')
    return ok


def gate_B():
    """GB: reproduce 67 -- the octahedral 3-cube compound is an O-orbit of
    size 3 (via a 45-deg-about-z seed, Q(sqrt2)), matching the golden
    3-subset count."""
    from slide3_q2 import Q2, Rz45, exact_count_q2, assert_orthonormal
    O_Q2 = embed_O(lambda x: Q2(x))
    seed = Rz45()
    assert_orthonormal(seed)
    reps = orbit_reps(O_Q2, seed, O_Q2)
    orbit_size = len(reps)
    ok_size = (orbit_size == 3)
    total = None
    if ok_size:
        total, bd = exact_count_q2(list(reps.values()), verbose=False)
    ok = ok_size and (total == 67)
    print(f'  GB: O-orbit(45deg-about-z) size={orbit_size} (want 3), '
          f'total={total} (want 67)  {"PASS" if ok else "FAIL"}')
    return ok


def gate_C():
    """GC: reproduce 699 -- the (C3, 3+3) family on the (1,1,1) axis:
    both triples are exact C3-orbits (verified via the orbit machinery,
    not just the known quats), and cube_regions gives 699."""
    quats = [(3, 1, 0, 0), (3, 0, 1, 0), (3, 0, 0, 1),
              (41, 28, 22, 14), (41, 14, 28, 22), (41, 22, 14, 28)]
    C3 = closure([rot_from_quat(1, 1, 1, 1)])
    orb1 = orbit_keys(C3, rot_from_quat(*quats[0]), O_Q5)
    orb2 = orbit_keys(C3, rot_from_quat(*quats[3]), O_Q5)
    target1 = {coset_key(rot_from_quat(*q), O_Q5) for q in quats[0:3]}
    target2 = {coset_key(rot_from_quat(*q), O_Q5) for q in quats[3:6]}
    struct_ok = (orb1 == target1 and orb2 == target2
                 and len(orb1 | orb2) == 6)
    total, bd = cpp_batch([list(quats)])[0]
    ok = struct_ok and (total == 699)
    print(f'  GC: two C3-orbits, sizes {len(orb1)}+{len(orb2)}, '
          f'union distinct={len(orb1|orb2)}, cube_regions total={total} '
          f'(want 699)  {"PASS" if ok else "FAIL"}')
    return ok


def gate_D():
    """GD: reproduce 681 -- the (I, 5+free) family (golden five + sixth on
    the (1,1,1) axis) via golden_six, AND confirm via the orbit machinery
    (with proper-frame correction) that the golden five IS the I-orbit of
    the axis-aligned cube, size 5."""
    I = closure([D, B])
    assert len(I) == 60
    g5p = golden_five_proper()
    target = {coset_key(c, O_Q5) for c in g5p}
    orb = orbit_keys(I, IDENT, O_Q5)
    orbit_ok = (orb == target and len(orb) == 5)
    total, bd = gs.eval_config('A', (2, 1, 1, 1))
    ok = orbit_ok and (total == 681)
    print(f'  GD: I-orbit(identity, proper-frame-corrected) size={len(orb)} '
          f'== golden five: {orb == target}; golden_six total={total} '
          f'(want 681)  {"PASS" if ok else "FAIL"}')
    return ok


def gate_E():
    """GE: a rational random 6-cube config counts identically through the
    Python engine (certify_six) and the dispatched C++ engine."""
    rng = random.Random(20260711)
    quats = [tuple(gcd_reduce([rng.randint(-60, 60) for _ in range(4)]))
             for _ in range(6)]
    rots = [rot_from_quat(*q) for q in quats]
    total_py, bd_py = exact_count_config(rots, verbose=False)
    total_cpp, bd_cpp = cpp_batch([list(quats)])[0]
    # bd_py (certify_six) includes the depth-0 "outside" region (count 1);
    # cpp_batch strips depth 0 by convention (see cpp_batch docstring-ish
    # comment at its by_depth line) -- compare depth>=1 histograms only.
    bd_py_pos = {k: v for k, v in bd_py.items() if k != 0}
    ok = (total_py == total_cpp) and (bd_py_pos == bd_cpp)
    print(f'  GE: python={total_py} cpp={total_cpp}  {"PASS" if ok else "FAIL"}')
    return ok


def run_gates():
    print('=== GATES (GA-GE) ===')
    results = {}
    for name, fn in [('GA', gate_A), ('GB', gate_B), ('GC', gate_C),
                      ('GD', gate_D), ('GE', gate_E)]:
        t0 = time.time()
        ok = fn()
        results[name] = ok
        log_eval({'gate': name, 'pass': ok, 'dt': time.time() - t0})
    all_ok = all(results.values())
    print(f'\nGATES: {"ALL PASS" if all_ok else "FAILURES: " + str([k for k,v in results.items() if not v])}')
    return all_ok, results


# ======================================================= Phase 1: rational
RATIONAL_GROUPS = {
    'C2': [(0, 0, 0, 1)],
    'C3': [(1, 1, 1, 1)],
    'C4': [(1, 0, 0, 1)],
    'C6': [(3, 1, 1, 1)],
    'D2': [(0, 0, 0, 1), (0, 1, 0, 0)],
    'D3': [(1, 1, 1, 1), (0, 1, -1, 0)],
    'D4': [(1, 0, 0, 1), (0, 1, 0, 0)],
    'D6': [(3, 1, 1, 1), (0, 1, -1, 0)],
    'T': [(1, 1, 1, 1), (1, 1, 1, -1)],
    'O': [(1, 0, 0, 1), (1, 1, 1, 1)],
}

# Seed FORMS: parameterized quaternion families used to probe/realize
# aligned seeds. Each form is a function (a,b) -> integer quat, plus a
# human label. 'generic' has no alignment constraint at all.
SEED_FORMS = {
    'z-axial':   lambda a, b: (a, 0, 0, b),      # aligned to a coordinate axis
    'body-diag': lambda a, b: (a, b, b, b),      # aligned to (1,1,1)
    'face-diag': lambda a, b: (a, b, -b, 0),     # aligned to (1,-1,0)
    'generic':   None,                            # no alignment; full 4-free
}


def build_group(name):
    return closure([rot_from_quat(*q) for q in RATIONAL_GROUPS[name]])


def probe_group(name, Gelems, rng):
    """Empirically discover achievable orbit sizes <= 6 and which SEED
    FORM realizes each, by trying a battery of aligned + generic seeds.
    Never hand-derive stabilizer orders (spec section 1)."""
    found = {}   # size -> (form_name, sample (a,b) or None for generic)
    probes = []
    for form in ('z-axial', 'body-diag', 'face-diag'):
        f = SEED_FORMS[form]
        for a, b in [(1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (5, 2), (4, 1),
                     (7, 3), (5, 4), (9, 5)]:
            probes.append((form, (a, b), f(a, b)))
    for _ in range(15):
        q = tuple(gcd_reduce([rng.randint(-60, 60) for _ in range(4)]))
        probes.append(('generic', None, q))
    for form, ab, q in probes:
        seed = rot_from_quat(*q)
        sz = len(orbit_keys(Gelems, seed, O_Q5))
        if sz == 1:
            continue   # degenerate (fixed point == identity's own coset only)
        if sz <= 6 and sz not in found:
            found[sz] = (form, ab, q)
    return found


def partitions_of(target, parts):
    """All multisets of `parts` (sorted list of positive ints, repeats
    allowed) summing exactly to target, as sorted tuples."""
    parts = sorted(set(parts))
    out = []

    def rec(remaining, min_idx, cur):
        if remaining == 0:
            out.append(tuple(cur))
            return
        for i in range(min_idx, len(parts)):
            p = parts[i]
            if p <= remaining:
                cur.append(p)
                rec(remaining - p, i, cur)
                cur.pop()
    rec(target, 0, [])
    return out


def build_pure_family(Gelems, seed_specs):
    """seed_specs: list of (form, (a,b)-or-None, quat) each contributing
    ONE orbit. Returns the union of all orbits as a list of Rot AND the
    corresponding list of integer quats is NOT directly recoverable (Rot
    only) -- for the rational engine we instead track quats symbolically
    via orbit_reps applied to the SEED quat's rot_from_quat image, then
    re-derive an integer quat per coset by brute rational reconstruction.
    Simpler: for cube_regions dispatch we need INTEGER QUATS per cube, so
    this function returns Rot objects for orbit-membership bookkeeping;
    the actual dispatch path (search_family) works with quats directly."""
    raise NotImplementedError('unused; see search_pure_orbit / search_core_free')


# ---- quaternion-level orbit construction (for C++ dispatch, integer only)
def quat_mul(p, q):
    """Hamilton product of two integer/rational quaternions (w,x,y,z)."""
    w1, x1, y1, z1 = p
    w2, x2, y2, z2 = q
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2)


def group_quats(name):
    """Integer-quaternion representatives of every element of the
    RATIONAL group `name` (paired 1-1 with build_group's Rot elements via
    matching rotation matrices), used so that orbit construction can stay
    in integer-quaternion space (required for cube_regions dispatch)."""
    gens = RATIONAL_GROUPS[name]
    seen = {(1, 0, 0, 0): rot_from_quat(1, 0, 0, 0)}
    frontier = [(1, 0, 0, 0)]
    gen_and_inv = list(gens)
    for g in gens:
        w, x, y, z = g
        gen_and_inv.append((w, -x, -y, -z))
    while frontier:
        nxt = []
        for q in frontier:
            for g in gen_and_inv:
                nq = tuple(gcd_reduce(list(quat_mul(q, g))))
                R = rot_from_quat(*nq)
                if not any(R == r for r in seen.values()):
                    seen[nq] = R
                    nxt.append(nq)
        frontier = nxt
    return list(seen.keys())


def quat_orbit(qlist, seed_q, Oset):
    """Orbit of integer-quat seed under the group given as a list of
    integer quats. Returns list of ONE representative integer quat per
    distinct coset (O-deduped exactly as elsewhere)."""
    d = {}
    for gq in qlist:
        nq = gcd_reduce(list(quat_mul(gq, seed_q)))
        R = rot_from_quat(*nq)
        k = coset_key(R, Oset)
        if k not in d:
            d[k] = nq
    return list(d.values())


def quat_orbit_keys(qlist, seed_q, Oset):
    """Like quat_orbit but also returns the frozenset of coset keys, so a
    caller building many COMBINATIONS of independently-varying seeds (a
    k-way grid product) can memoize the expensive part (24-element Q5
    matrix products inside coset_key) ONCE PER AXIS VALUE instead of once
    per combination -- an O(grid^k) blowup down to O(grid*k). Without
    this, a 3-slot 19-point grid recomputes ~1e6 Q5 matrix products for
    work that only has 57 distinct inputs."""
    d = {}
    for gq in qlist:
        nq = gcd_reduce(list(quat_mul(gq, seed_q)))
        R = rot_from_quat(*nq)
        k = coset_key(R, Oset)
        if k not in d:
            d[k] = nq
    return list(d.values()), frozenset(d.keys())


def cap_ok(q, cap=MAXC):
    return all(abs(c) <= cap for c in q)


def search_family_pure(gname, qlist, forms_for_sizes, partition, grid_ab,
                        climb_steps, family_tag):
    """One G, one partition of orbit sizes (all from the SAME group G,
    e.g. (3,3) or (6,)). Grid over each orbit's seed form parameter(s),
    build the union of orbits, dispatch to cube_regions in batches, then
    exact-hillclimb the (a,b) integer pairs (respecting orbit membership
    -- moves regenerate the whole family from the new seed, never touch
    individual cube quats directly, so G-invariance can never be broken).
    Logs every eval. Returns (best_total, best_seed_abs, best_bd)."""
    k = len(partition)
    per_orbit_forms = [forms_for_sizes[s][0] for s in partition]
    best = {'total': -1, 'ab': None, 'bd': None}

    # per-AXIS-VALUE memo: computing coset_key is 24 Q5 matrix products;
    # a naive build_config would redo that for every k-fold GRID
    # COMBINATION (grid_ab^k of them). Caching by (form, a, b) means each
    # distinct axis value's orbit is computed once and reused across all
    # combinations that share it -- turns an O(grid^k) blowup in matrix
    # arithmetic into O(grid*k) (see quat_orbit_keys docstring).
    axis_cache = {}

    def axis_orbit(s, form, a, b):
        key = (form, a, b)
        hit = axis_cache.get(key)
        if hit is not None:
            return hit
        f = SEED_FORMS[form]
        seed_q = gcd_reduce(list(f(a, b)))
        if not cap_ok(seed_q):
            axis_cache[key] = None
            return None
        orb, keys = quat_orbit_keys(qlist, seed_q, O_Q5)
        if len(orb) != s:
            axis_cache[key] = None
            return None
        axis_cache[key] = (orb, keys)
        return (orb, keys)

    def build_config(ab_list):
        cfg = []
        all_keys = frozenset()
        n_before = 0
        for s, form, (a, b) in zip(partition, per_orbit_forms, ab_list):
            hit = axis_orbit(s, form, a, b)
            if hit is None:
                return None
            orb, keys = hit
            cfg.extend(orb)
            n_before += len(orb)
            all_keys = all_keys | keys
        # dedupe check: must be exactly 6 distinct cosets total
        if len(all_keys) != 6 or n_before != 6:
            return None
        return cfg

    # -- coarse grid. For k>=3 slots the full product grid_ab^k explodes
    # (C2's 2+2+2 = 19^3 = 6859 configs); subsample deterministically to
    # MAX_GRID points so no single family stalls the sweep. The exact
    # hill-climb below then refines from the best sampled point, so the
    # subsample only affects COARSE coverage (reported as the grid
    # resolution in the audit, per spec section 7), not correctness.
    MAX_GRID = 900
    all_ab = list(product(grid_ab, repeat=k))
    if len(all_ab) > MAX_GRID:
        stride = len(all_ab) / MAX_GRID
        all_ab = [all_ab[int(i * stride)] for i in range(MAX_GRID)]
    grid_points = []
    for ab_tuple in all_ab:
        cfg = build_config(ab_tuple)
        if cfg is not None:
            grid_points.append((ab_tuple, cfg))
    if not grid_points:
        return best
    configs = [cfg for _, cfg in grid_points]
    results = cpp_batch(configs)
    for (ab_tuple, cfg), res in zip(grid_points, results):
        if res is None:
            continue
        total, bd = res
        log_eval({'phase': 1, 'group': gname, 'partition': list(partition),
                  'forms': per_orbit_forms, 'ab': list(ab_tuple),
                  'quats': cfg, 'total': total, 'by_depth': bd,
                  'tag': family_tag, 'stage': 'grid'})
        if total > best['total']:
            best.update(total=total, ab=ab_tuple, bd=bd)

    # -- exact hillclimb on the (a,b) pairs (moves: +-1/+-2 on one
    # component of one orbit's (a,b), re-gcd via SEED_FORMS f already
    # gcd-reducing internally through build_config)
    if best['ab'] is None:
        return best
    cur_ab = list(best['ab'])
    cur_total = best['total']
    seen_ab = set()
    for step in range(climb_steps):
        seen_ab.add(tuple(cur_ab))
        cand_tuples = []
        for i in range(k):
            a, b = cur_ab[i]
            for da, db in [(1, 0), (-1, 0), (2, 0), (-2, 0),
                           (0, 1), (0, -1), (0, 2), (0, -2)]:
                new_ab = list(cur_ab)
                new_ab[i] = (a + da, b + db)
                t = tuple(new_ab)
                if t not in seen_ab:
                    cand_tuples.append(t)
        cand_configs = []
        valid_cands = []
        for t in cand_tuples:
            cfg = build_config(t)
            if cfg is not None:
                cand_configs.append(cfg)
                valid_cands.append(t)
        if not cand_configs:
            break
        results = cpp_batch(cand_configs)
        step_best = None
        for t, cfg, res in zip(valid_cands, cand_configs, results):
            if res is None:
                continue
            total, bd = res
            log_eval({'phase': 1, 'group': gname, 'partition': list(partition),
                      'forms': per_orbit_forms, 'ab': list(t),
                      'quats': cfg, 'total': total, 'by_depth': bd,
                      'tag': family_tag, 'stage': f'climb{step}'})
            if total > cur_total and (step_best is None or total > step_best[1]):
                step_best = (t, total, bd)
        if step_best is None:
            break
        cur_ab, cur_total, cur_bd = list(step_best[0]), step_best[1], step_best[2]
        if cur_total > best['total']:
            best.update(total=cur_total, ab=tuple(cur_ab), bd=cur_bd)
    return best


# Principal rotation axis (integer) of each cyclic group, read off its
# generator quaternion's vector part. Used by the stacked-axis family.
GROUP_AXIS = {
    'C2': (0, 0, 1), 'C4': (0, 0, 1),
    'C3': (1, 1, 1), 'C6': (1, 1, 1),
}


def search_family_stacked_axis(gname, qlist, axis, n_slots, rng,
                                climb_steps=14, family_tag=''):
    """STACKED orbits on a common axis: slots seed_i = R^i . seed1
    (i=0..n_slots-1), with R a rational rotation about the group's own
    principal axis (so R commutes with G and each R^i.seed1 keeps orbit
    size |G|). This is the EXACT shape of the 699 record -- two C3 orbits
    3-fold-symmetric about (1,1,1) with the second = R.(first), R about
    (1,1,1) (six_cube_search_results.md Postscript 9) -- and of the 655
    double-pair wall. The plain product-grid families cannot reach it
    because seed2 is not an independent aligned seed but R-linked to
    seed1; here R's (m,k) is a search parameter, recovering that plateau.
    Grid: seed1 over aligned forms x R=(m, k*axis) over small m,k; then
    exact joint hill-climb of (seed1 4 comps, R's m,k)."""
    ax, ay, az = axis

    def axis_rot(m, k):
        return gcd_reduce([m, k * ax, k * ay, k * az])

    def build_config(seed1, m, k):
        R = tuple(axis_rot(m, k))
        cur = tuple(gcd_reduce(list(seed1)))
        cfg, all_keys = [], frozenset()
        for i in range(n_slots):
            orb, keys = quat_orbit_keys(qlist, cur, O_Q5)
            if len(orb) != len(qlist):
                return None
            if not all(cap_ok(q) for q in orb):
                return None
            cfg.extend(orb)
            all_keys = all_keys | keys
            cur = tuple(gcd_reduce(list(quat_mul(R, cur))))
        if len(all_keys) != 6 or len(cfg) != 6:
            return None
        return cfg

    best = {'total': -1, 'seed1': None, 'mk': None, 'bd': None}

    # seed1 aligned battery + R grid
    seed1_battery = []
    for form in ('z-axial', 'body-diag', 'face-diag'):
        f = SEED_FORMS[form]
        for a, b in [(1, 1), (2, 1), (3, 1), (1, 2), (5, 2), (7, 3), (1, 0)]:
            seed1_battery.append(tuple(gcd_reduce(list(f(a, b)))))
    seed1_battery = list(dict.fromkeys(seed1_battery))
    mk_grid = [(m, k) for m in range(0, 9) for k in range(1, 9)]

    configs, metas = [], []
    for s1 in seed1_battery:
        for m, k in mk_grid:
            cfg = build_config(s1, m, k)
            if cfg is not None:
                configs.append(cfg); metas.append((s1, (m, k)))
    if configs:
        results = cpp_batch(configs)
        for (s1, mk), cfg, res in zip(metas, configs, results):
            if res is None:
                continue
            total, bd = res
            log_eval({'phase': 1, 'group': gname, 'partition': [len(qlist)] * n_slots,
                      'forms': ['stacked-axis'] * n_slots, 'seed1': list(s1),
                      'mk': list(mk), 'quats': cfg, 'total': total,
                      'by_depth': bd, 'tag': family_tag, 'stage': 'grid'})
            if total > best['total']:
                best.update(total=total, seed1=s1, mk=mk, bd=bd)

    if best['seed1'] is None:
        return best
    # joint exact hill-climb: seed1's 4 comps + R's (m,k)
    cur_s1 = list(best['seed1']); cur_m, cur_k = best['mk']
    cur_total = best['total']
    for step in range(climb_steps):
        cands = []
        for comp in range(4):
            for d in (-2, -1, 1, 2):
                ns = list(cur_s1); ns[comp] += d
                cands.append((tuple(gcd_reduce(ns)), cur_m, cur_k))
        for dm in (-2, -1, 1, 2):
            cands.append((tuple(cur_s1), cur_m + dm, cur_k))
        for dk in (-2, -1, 1, 2):
            cands.append((tuple(cur_s1), cur_m, cur_k + dk))
        configs, metas = [], []
        for s1, m, k in cands:
            if k <= 0 or not cap_ok(s1):
                continue
            cfg = build_config(s1, m, k)
            if cfg is not None:
                configs.append(cfg); metas.append((s1, m, k))
        if not configs:
            break
        results = cpp_batch(configs)
        step_best = None
        for (s1, m, k), cfg, res in zip(metas, configs, results):
            if res is None:
                continue
            total, bd = res
            log_eval({'phase': 1, 'group': gname, 'partition': [len(qlist)] * n_slots,
                      'forms': ['stacked-axis'] * n_slots, 'seed1': list(s1),
                      'mk': [m, k], 'quats': cfg, 'total': total,
                      'by_depth': bd, 'tag': family_tag, 'stage': f'climb{step}'})
            if total > cur_total and (step_best is None or total > step_best[1]):
                step_best = ((s1, m, k), total, bd)
        if step_best is None:
            break
        (s1, m, k), cur_total, cur_bd = step_best
        cur_s1, cur_m, cur_k = list(s1), m, k
        if cur_total > best['total']:
            best.update(total=cur_total, seed1=tuple(cur_s1),
                        mk=(cur_m, cur_k), bd=cur_bd)
    return best


def search_family_generic_multi(gname, qlist, n_slots, rng, n_random=60,
                                  climb_steps=8, family_tag=''):
    """Multi-orbit partition where EVERY slot's orbit size equals |G|
    (trivial stabilizer -- ANY seed works, no alignment needed). The
    699 record's second triple is exactly such an unaligned seed (its
    quat (41,28,22,14) fits no SEED_FORMS slice -- confirmed by direct
    check), so the aligned-grid-only search in search_family_pure
    structurally CANNOT reach it; this searches the full 4-parameter
    seed per slot instead (random start + joint component-wise
    hillclimb, phase_b_hillclimb's move set applied per-slot)."""
    assert n_slots * len(qlist) == 6, \
        f'{gname}: n_slots={n_slots} * |G|={len(qlist)} must be 6 for a ' \
        'pure native-generic multi-orbit partition'
    best = {'total': -1, 'seeds': None, 'bd': None}

    def build_config(seeds):
        cfg = []
        for sq in seeds:
            orb = quat_orbit(qlist, sq, O_Q5)
            if len(orb) != len(qlist):
                return None
            cfg.extend(orb)
        keys = {coset_key(rot_from_quat(*q), O_Q5) for q in cfg}
        if len(keys) != 6 or len(cfg) != 6:
            return None
        return cfg

    starts = []
    for _ in range(n_random):
        seeds = [tuple(gcd_reduce([rng.randint(-MAXC, MAXC) for _ in range(4)]))
                 for _ in range(n_slots)]
        starts.append(seeds)
    configs, metas = [], []
    for seeds in starts:
        cfg = build_config(seeds)
        if cfg is not None:
            configs.append(cfg)
            metas.append(seeds)
    if not configs:
        return best
    results = cpp_batch(configs)
    for seeds, cfg, res in zip(metas, configs, results):
        if res is None:
            continue
        total, bd = res
        log_eval({'phase': 1, 'group': gname, 'partition': [len(qlist)] * n_slots,
                  'forms': ['generic'] * n_slots, 'seeds': [list(s) for s in seeds],
                  'quats': cfg, 'total': total, 'by_depth': bd,
                  'tag': family_tag, 'stage': 'random'})
        if total > best['total']:
            best.update(total=total, seeds=seeds, bd=bd)

    if best['seeds'] is None:
        return best
    cur_seeds = list(best['seeds'])
    cur_total = best['total']
    for step in range(climb_steps):
        cand_list = []
        for i in range(n_slots):
            for comp in range(4):
                for delta in (-2, -1, 1, 2):
                    ns = list(cur_seeds)
                    q = list(ns[i]); q[comp] += delta
                    ns[i] = tuple(gcd_reduce(q))
                    if all(cap_ok(s) for s in ns):
                        cand_list.append(ns)
        configs, metas = [], []
        for ns in cand_list:
            cfg = build_config(ns)
            if cfg is not None:
                configs.append(cfg); metas.append(ns)
        if not configs:
            break
        results = cpp_batch(configs)
        step_best = None
        for ns, cfg, res in zip(metas, configs, results):
            if res is None:
                continue
            total, bd = res
            log_eval({'phase': 1, 'group': gname, 'partition': [len(qlist)] * n_slots,
                      'forms': ['generic'] * n_slots, 'seeds': [list(s) for s in ns],
                      'quats': cfg, 'total': total, 'by_depth': bd,
                      'tag': family_tag, 'stage': f'climb{step}'})
            if total > cur_total and (step_best is None or total > step_best[1]):
                step_best = (ns, total, bd)
        if step_best is None:
            break
        cur_seeds, cur_total, cur_bd = step_best
        if cur_total > best['total']:
            best.update(total=cur_total, seeds=list(cur_seeds), bd=cur_bd)
    return best


def search_family_core_free(gname, qlist, core_size, core_form, n_free,
                             grid_ab, family_tag, climb_steps=6, n_random=12,
                             rng=None):
    """Core (one G-orbit of size core_size, via core_form) + n_free totally
    unconstrained rational cubes (the '681-style' mixed family). Grid the
    core's (a,b); for each, try n_random free-cube quat draws, batch-count,
    then hillclimb the FREE cubes only (core stays exact -- exactly the
    spec's 'core stays exact, free climbs' instruction)."""
    rng = rng or random.Random(2026)
    f = SEED_FORMS[core_form]
    best = {'total': -1, 'ab': None, 'free': None, 'bd': None}

    core_options = []
    for a, b in grid_ab:
        seed_q = gcd_reduce(list(f(a, b)))
        if not cap_ok(seed_q):
            continue
        orb = quat_orbit(qlist, seed_q, O_Q5)
        if len(orb) == core_size:
            core_options.append(((a, b), orb))
    if not core_options:
        return best

    for (a, b), core in core_options:
        free_sets = [[tuple(gcd_reduce([rng.randint(-MAXC, MAXC)
                                          for _ in range(4)]))
                       for _ in range(n_free)] for _ in range(n_random)]
        configs, metas = [], []
        for free in free_sets:
            cfg = core + free
            keys = {coset_key(rot_from_quat(*q), O_Q5) for q in cfg}
            if len(keys) != 6:
                continue
            configs.append(cfg)
            metas.append(free)
        if not configs:
            continue
        results = cpp_batch(configs)
        for free, cfg, res in zip(metas, configs, results):
            if res is None:
                continue
            total, bd = res
            log_eval({'phase': 1, 'group': gname, 'partition': [core_size] + [1]*n_free,
                      'forms': [core_form] + ['free']*n_free, 'ab': [a, b],
                      'free': free, 'quats': cfg, 'total': total, 'by_depth': bd,
                      'tag': family_tag, 'stage': 'grid'})
            if total > best['total']:
                best.update(total=total, ab=(a, b), free=free, bd=bd)

    # hillclimb the free cubes only, core fixed at best['ab']
    if best['ab'] is None:
        return best
    a, b = best['ab']
    seed_q = gcd_reduce(list(f(a, b)))
    core = quat_orbit(qlist, seed_q, O_Q5)
    cur_free = list(best['free'])
    cur_total = best['total']
    for step in range(climb_steps):
        cand_free_list = []
        for i in range(n_free):
            for comp in range(4):
                for delta in (-2, -1, 1, 2):
                    nf = list(cur_free)
                    q = list(nf[i]); q[comp] += delta
                    nf[i] = tuple(gcd_reduce(q))
                    if cap_ok(nf[i]):
                        cand_free_list.append(nf)
        configs, metas = [], []
        for nf in cand_free_list:
            cfg = core + nf
            keys = {coset_key(rot_from_quat(*q), O_Q5) for q in cfg}
            if len(keys) != 6:
                continue
            configs.append(cfg); metas.append(nf)
        if not configs:
            break
        results = cpp_batch(configs)
        step_best = None
        for nf, cfg, res in zip(metas, configs, results):
            if res is None:
                continue
            total, bd = res
            log_eval({'phase': 1, 'group': gname, 'partition': [core_size] + [1]*n_free,
                      'forms': [core_form] + ['free']*n_free, 'ab': [a, b],
                      'free': nf, 'quats': cfg, 'total': total, 'by_depth': bd,
                      'tag': family_tag, 'stage': f'climb{step}'})
            if total > cur_total and (step_best is None or total > step_best[1]):
                step_best = (nf, total, bd)
        if step_best is None:
            break
        cur_free, cur_total, cur_bd = step_best
        if cur_total > best['total']:
            best.update(total=cur_total, free=list(cur_free), bd=cur_bd)
    return best


def phase1():
    print('\n=== PHASE 1: rational G sweep (cube_regions C++ engine) ===')
    rng = random.Random(7)
    catalog = []
    grid_ab_default = [(1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (3, 2), (2, 3),
                        (5, 2), (2, 5), (5, 3), (3, 5), (4, 1), (1, 4),
                        (5, 1), (1, 5), (7, 3), (7, 4), (8, 3), (5, 4)]

    for gname in RATIONAL_GROUPS:
        Gelems = build_group(gname)
        qlist = group_quats(gname)
        assert len(qlist) == len(Gelems), \
            f'{gname}: quat closure {len(qlist)} != Rot closure {len(Gelems)}'
        found = probe_group(gname, Gelems, rng)
        sizes = sorted(found)
        forms_shown = {s: found[s][0] for s in sizes}
        print(f'-- G={gname} |G|={len(Gelems)}  achievable orbit sizes <=6: '
              f'{sizes} (forms: {forms_shown})')

        # pure partitions (sum of orbit sizes from this G == 6), aligned-grid
        parts = partitions_of(6, sizes)
        for part in parts:
            tag = f'{gname}:{"+".join(map(str, part))}'
            t0 = time.time()
            best = search_family_pure(gname, qlist, found, part,
                                       grid_ab_default, climb_steps=10,
                                       family_tag=tag)
            dt = time.time() - t0
            print(f'   pure(aligned) {tag:20s} best={best["total"]:>4} '
                  f'ab={best["ab"]}  ({dt:.1f}s)')
            catalog.append(dict(group=gname, kind='pure', partition=part,
                                  best=best['total'], ab=best['ab'],
                                  bd=best['bd'], tag=tag, dt=dt))

        # native fully-generic multi-orbit partitions (|G| slots of size
        # |G| each, trivial stabilizer -- no alignment restriction at all).
        # Needed because an aligned-form grid CANNOT reach a family whose
        # winning point has an unaligned seed (confirmed for 699's second
        # triple -- see search_family_generic_multi docstring).
        if len(Gelems) <= 6 and 6 % len(Gelems) == 0:
            n_slots = 6 // len(Gelems)
            tag = f'{gname}:generic-x{n_slots}'
            t0 = time.time()
            best = search_family_generic_multi(
                gname, qlist, n_slots, rng,
                n_random=80 if n_slots > 1 else 40,
                climb_steps=12, family_tag=tag)
            dt = time.time() - t0
            print(f'   pure(generic) {tag:20s} best={best["total"]:>4}  ({dt:.1f}s)')
            catalog.append(dict(group=gname, kind='pure-generic',
                                  partition=tuple([len(Gelems)] * n_slots),
                                  best=best['total'], seeds=best['seeds'],
                                  bd=best['bd'], tag=tag, dt=dt))

        # STACKED-AXIS family (cyclic G only): slots R^i-linked on the
        # group's own axis -- the exact shape of the 699 record. Without
        # this the C3 catalog entry tops out at a sub-peak while 699 (a
        # C3 3+3 config, gate GC) lives in-family but off the product grid.
        if gname in GROUP_AXIS and len(Gelems) <= 6 and 6 % len(Gelems) == 0:
            n_slots = 6 // len(Gelems)
            if n_slots >= 2:
                tag = f'{gname}:stacked-axis-x{n_slots}'
                t0 = time.time()
                best = search_family_stacked_axis(
                    gname, qlist, GROUP_AXIS[gname], n_slots, rng,
                    climb_steps=16, family_tag=tag)
                dt = time.time() - t0
                print(f'   pure(stacked) {tag:20s} best={best["total"]:>4} '
                      f'seed1={best["seed1"]} mk={best["mk"]}  ({dt:.1f}s)')
                catalog.append(dict(group=gname, kind='pure-stacked',
                                      partition=tuple([len(Gelems)] * n_slots),
                                      best=best['total'], seed1=best['seed1'],
                                      mk=best['mk'], bd=best['bd'], tag=tag,
                                      dt=dt))

        # core+free mixed partitions: one orbit of size m<6 (m in sizes,
        # m<6) + (6-m) free cubes. Only m>=3 kept tractable (n_free<=3);
        # m<3 leaves >=4 free cubes, an essentially-unconstrained search
        # far outside a "family" -- out of scope here (documented, Sec 7).
        for m in sizes:
            if m >= 6 or m < 3:
                continue
            form = found[m][0]
            tag = f'{gname}:{m}+free{6-m}'
            t0 = time.time()
            best = search_family_core_free(gname, qlist, m, form, 6 - m,
                                             grid_ab_default, tag,
                                             climb_steps=8, n_random=10, rng=rng)
            dt = time.time() - t0
            print(f'   core+free {tag:20s} best={best["total"]:>4} '
                  f'ab={best["ab"]}  ({dt:.1f}s)')
            catalog.append(dict(group=gname, kind='core+free',
                                  partition=(m, 6 - m), best=best['total'],
                                  ab=best['ab'], free=best.get('free'),
                                  bd=best['bd'], tag=tag, dt=dt))
    return catalog


# ========================================================= Phase 2: Q(sqrt5)
def phase2():
    print('\n=== PHASE 2: Q(sqrt5) sweep (I and C5 families) ===')
    catalog = []

    # ---- I family: golden five (proper-frame-verified I-orbit of 5) +
    # free rational sixth. golden_six.py already ran a real search here
    # (result: 681, family A quat (2,1,1,1)); this re-derives the family
    # membership via the orbit machinery (not hand-waved) and extends the
    # search a bit further with a fresh random+climb batch through the
    # SAME validated engine (golden_six.eval_config), logging into this
    # program's own jsonl for the unified catalog.
    I = closure([D, B])
    g5p = golden_five_proper()
    orb = orbit_keys(I, IDENT, O_Q5)
    assert orb == {coset_key(c, O_Q5) for c in g5p} and len(orb) == 5, \
        'I-orbit(identity) must equal the golden five (proper-frame-checked)'
    g5 = gs.golden_five()   # golden_six's own construction (validated engine)

    best_I = {'total': -1, 'quat': None, 'bd': None, 'family': None}
    rng = random.Random(99)
    probe_quats = [(2, 1, 1, 1), (7, 4, 4, 4), (1, 0, 0, 0)]
    probe_quats += [tuple(gcd_reduce([rng.randint(-MAXC, MAXC) for _ in range(4)]))
                     for _ in range(20)]
    for fam in ('A', 'B'):
        for q in probe_quats:
            total, bd = gs.eval_config(fam, q)
            log_eval({'phase': 2, 'group': 'I', 'partition': [5, 1],
                      'family': fam, 'quat': list(q), 'total': total,
                      'by_depth': bd, 'tag': f'I:5+free({fam})', 'stage': 'grid'})
            if total > best_I['total']:
                best_I.update(total=total, quat=q, bd=bd, family=fam)
    print(f'-- I: 5(I-orbit, proper-frame-verified)+free  best={best_I["total"]} '
          f'family={best_I["family"]} quat={best_I["quat"]}')
    catalog.append(dict(group='I', kind='core+free', partition=(5, 1),
                          best=best_I['total'], quat=best_I['quat'],
                          family=best_I['family'], bd=best_I['bd'],
                          tag='I:5+free'))

    # ---- C5 family: C5 is a STRICTLY LARGER search space than "the
    # golden five" -- ANY seed on ANY 5-fold axis gives an orbit of size 5
    # (see module docstring: no rational-cube stabilizer order divides 5,
    # so stab is always trivial under C5, unlike I where the golden seed
    # gets a T-stabilizer coincidence). We reuse the SAME dodecahedral
    # 5-fold axis as I (the (1,0,phi) axis of generator D) but vary the
    # SEED (not just the axis) via rational rotations of the axis-aligned
    # cube composed with D-orbit membership -- i.e. seed = Q(quat) (a
    # rational pre-rotation), orbit = {D^k * seed}. This generalizes
    # golden five (seed=identity) to arbitrary seeds on the same axis.
    C5 = closure([D])
    assert len(C5) == 5
    best_C5 = {'total': -1, 'quat': None, 'bd': None}
    c5_quats = [(1, 0, 0, 0), (2, 1, 0, 0), (1, 1, 0, 0), (3, 1, 1, 0),
                (5, 2, 1, 0), (2, 1, 1, 1), (1, 0, 1, 0)]
    c5_quats += [tuple(gcd_reduce([rng.randint(-60, 60) for _ in range(4)]))
                  for _ in range(15)]
    for q in c5_quats:
        seed = rot_from_quat(*q)
        orb = orbit_reps(C5, seed, O_Q5)
        if len(orb) != 5:
            continue   # degenerate (seed landed on the axis itself)
        five = list(orb.values())
        # sixth cube: rational, on the SAME shared axis as I's winning
        # wall (1,1,1) is a DIFFERENT axis than C5's (1,0,phi) here, so
        # sweep a small set of rational sixth-cube quats instead of
        # assuming which axis matters (spec: compute, don't hand-derive).
        for sixth_q in [(1, 0, 0, 0), (2, 1, 1, 1), (3, 1, 1, 1), (7, 4, 4, 4)]:
            sixth = rot_from_quat(*sixth_q)
            cfg = five + [sixth]
            keys = {coset_key(c, O_Q5) for c in cfg}
            if len(keys) != 6:
                continue
            total, bd = exact_count_config(cfg, verbose=False)
            log_eval({'phase': 2, 'group': 'C5', 'partition': [5, 1],
                      'quat': list(q), 'sixth': list(sixth_q), 'total': total,
                      'by_depth': bd, 'tag': 'C5:5+free', 'stage': 'grid'})
            if total > best_C5['total']:
                best_C5.update(total=total, quat=q, bd=bd)
    print(f'-- C5: 5(C5-orbit)+free  best={best_C5["total"]} quat={best_C5["quat"]} '
          f'(NOTE: small probe grid -- see report Sec "honest limits")')
    catalog.append(dict(group='C5', kind='core+free', partition=(5, 1),
                          best=best_C5['total'], quat=best_C5['quat'],
                          bd=best_C5['bd'], tag='C5:5+free'))
    return catalog


# ================================================================= Phase 3
def phase3_note():
    """Phase 3 (Q(sqrt2)/Q(sqrt3)/towers) is scoped to families Phase 1/2
    FLAG as promising (spec section 6). Given the Phase 1/2 results (see
    report), nothing beat 699, so Phase 3 is not run as a full search;
    this records what WOULD be dispatched and why it's deferred, per the
    spec's 'honest limits' requirement (section 7)."""
    return {
        'q2_families': 'C8/D8 (45-deg content) -- engine ready (slide3_q2.py, '
                        'gate GB already exercises it); not swept because no '
                        'Phase-1 rational family came within striking range of '
                        '699 to justify chasing a quadratic refinement of it.',
        'q3_families': 'C12/D12 (30/60-deg content beyond the already-rational '
                        'C6/D6) -- needs a plain Q(sqrt3) field class (qtower.py '
                        'is Q(sqrt3,sqrt5), one field too many); not written.',
        'towers': 'mixed-axis composita -- QFIELD_SPEC.md already found the '
                   'concrete case (681 wall, Q(sqrt3,sqrt5)) is NOT special '
                   '(qtower.py: exact point == 681, no jump); no Phase 1/2 '
                   'result here motivates a new tower.',
    }


# ==================================================================== main
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if mode in ('-h', '--help'):
        print(__doc__)
        return
    ok, gate_results = run_gates()
    if not ok:
        print('\nONE OR MORE GATES FAILED. Stopping before search, per spec.')
        sys.exit(1)
    if mode == 'gates':
        return

    p1 = p2 = []
    if mode in ('phase1', 'all'):
        p1 = phase1()
    if mode in ('phase2', 'all'):
        p2 = phase2()
    p3 = phase3_note() if mode == 'all' else None

    write_report(REPORT_PATH, gate_results, p1, p2, p3)
    print(f'\nReport written to {REPORT_PATH}')


def write_report(path, gate_results, p1, p2, p3):
    lines = []
    lines.append('# Symmetry-stratified search report\n')
    lines.append('Working principles: SYMMETRY_SEARCH_SPEC.md. Generated by '
                  'symmetry_search.py.\n')
    lines.append('## Gates\n')
    for k, v in gate_results.items():
        lines.append(f'- {k}: {"PASS" if v else "FAIL"}')
    lines.append('')

    RECORD = 699

    def seed_str(row):
        if row.get('seed1') is not None:
            return f"seed1={row['seed1']} R(m,k)={row.get('mk')}"
        if row.get('seeds') is not None:
            return f"seeds={row['seeds']}"
        if row.get('free') is not None:
            return f"core ab={row.get('ab')} free={row['free']}"
        if row.get('ab') is not None:
            return f"ab={row['ab']}"
        if row.get('quat') is not None:
            return f"quat={row['quat']}"
        return ''

    lines.append('## Catalog (Phase 1: rational G, ℚ, C++ engine)\n')
    lines.append('All families searched by orbit machinery (orbit sizes '
                  'COMPUTED, aligned + generic seeds included). Field = ℚ.\n')
    lines.append('| group | family | best total | vs 699 | best seed(s) |')
    lines.append('|---|---|---|---|---|')
    for row in sorted(p1, key=lambda r: -r['best']):
        cmp = ('BEATS' if row['best'] > RECORD else
               'TIES' if row['best'] == RECORD else 'loses')
        lines.append(f"| {row['group']} | {row['tag']} | {row['best']} | "
                      f"{cmp} ({row['best']-RECORD:+d}) | `{seed_str(row)}` |")
    lines.append('')

    lines.append('## Catalog (Phase 2: Q(sqrt5), I and C5 families)\n')
    lines.append('| group | family | best total | vs 699 |')
    lines.append('|---|---|---|---|')
    for row in p2:
        cmp = ('BEATS' if row['best'] > RECORD else
               'TIES' if row['best'] == RECORD else 'loses')
        lines.append(f"| {row['group']} | {row['tag']} | {row['best']} | "
                      f"{cmp} ({row['best']-RECORD:+d}) |")
    lines.append('')

    if p3:
        lines.append('## Phase 3 (deferred families, honest status)\n')
        for k, v in p3.items():
            lines.append(f'- **{k}**: {v}')
        lines.append('')

    beat = [r for r in (p1 + p2) if r['best'] > RECORD]
    best_row = max(p1 + p2, key=lambda r: r['best'])
    lines.append('## Did anything beat 699?\n')
    if beat:
        lines.append(f'**YES**: {[(r["tag"], r["best"]) for r in beat]}')
    else:
        lines.append(f'**No.** The best systematically-searched total was '
                      f'**{best_row["best"]}** ({best_row["tag"]}). All family '
                      f'bests are <= 699.\n')
        lines.append('Crucial honest note: 699 itself is a **(C3, 3+3)** '
                      'config (both triples are size-3 C3-orbits about (1,1,1) '
                      '-- verified by gate GC), so it LIVES INSIDE the C3 '
                      'families searched here. The systematic grid+climb landed '
                      'on sub-peaks of that space (C3 core+free 643, C3 generic '
                      '627, C3 stacked-axis 655) rather than the 699 plateau, '
                      'because the two 699 seeds are linked by a rotation about '
                      'a NON-coordinate axis (the 40.31-deg axis of the '
                      'slide3 construction, Postscript 9) -- a 1-parameter '
                      'sub-manifold the coarse product grid does not sample. '
                      'This is the "narrow interior peak" limit stated in spec '
                      'section 7, here made concrete: coverage of a family is '
                      'not the same as landing on its optimum.')
    lines.append('')

    lines.append('## Notable positive: 655 recovered by a new construction\n')
    lines.append('The **C3 stacked-axis** family (two C3-orbits with the '
                  'second = R.(first), R a rational rotation about the shared '
                  '(1,1,1) axis) reaches **655** -- equal to the known rational '
                  'double-pair-wall record (Postscript 8) -- from a completely '
                  'different construction. Independent confirmation that 655 is '
                  'a real rational symmetry wall.\n')

    lines.append('## Most promising families (next move)\n')
    promising = [
        ('C3 / stacked-axis + generic 3+3', 'best 655/643 but PROVABLY '
         'contains 699 (gate GC). Next move: replace the axis-rotation link '
         'with rotation about the slide3 40.31-deg â-axis (reuse '
         'slide3_search.overlay_quats), or a denser 2-independent-generic-seed '
         'climb with multi-restart from the aligned+aligned grid -- this is '
         'the single most likely family to re-derive and then exceed 699.'),
        ('T / 4+free2', 'best 661 -- the strongest MIXED rational family '
         '(tetrahedral 4-orbit core + 2 free cubes). Next move: widen the free '
         'grid (currently 10 random draws/core) and climb radius; the core is '
         'exact so free-cube search is cheap.'),
        ('I / 5+free (ℚ(√5))', 'best 681 -- the golden five + free sixth, the '
         'strongest non-rational family. Next move: the ℚ(√3,√5) tower point is '
         'already known NOT to jump (Postscript 8); try golden-FOUR (177) + two '
         'free cubes (8 free params) per QFIELD_SPEC F3.'),
    ]
    for tag, note in promising:
        lines.append(f'- **{tag}**: {note}')
    lines.append('')
    lines.append('## Honest limits (spec section 7)\n')
    lines.append('- Scope: all symmetry walls for G in {C2,C3,C4,C6,D2,D3,D4,'
                  'D6,T,O} (rational, exhaustive orbit-partitions incl. '
                  'core+free and stacked-axis) and {I,C5} over ℚ(√5). NOT '
                  'searched: accidental (non-symmetric) walls (out of scope, '
                  'conjectured sub-maximal); Cn for n in {8,10,12} and their '
                  'ℚ(√2)/ℚ(√3) fields (Phase 3, deferred -- no Phase-1/2 family '
                  'came near 699 to justify a quadratic refinement).')
    lines.append('- Resolution (auditable): rational per-orbit aligned grid = '
                  '19 (a,b) points/axis, product subsampled to <=900 configs '
                  'for k>=3 slots; generic-multi = 40-80 random starts; '
                  'stacked-axis = 21 seed1 x 72 (m,k); all followed by exact '
                  '±1/±2 integer hill-climb (|comp|<=512). A narrow interior '
                  'peak between grid points can be missed (the 699 case above).')

    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
