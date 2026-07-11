#!/usr/bin/env python3
# Working principles: golden_wall_report.md + QFIELD_SPEC.md. Project index: README.md
"""Golden five-cube compound + a RATIONAL sixth cube: does it beat/match/miss
the six-all-rational-cube record of 635 bounded regions?

Background (see six_cube_search_results.md Postscripts 4-5 for the full
record derivation, and cube_compound_exact.py for the golden-five machinery):
  - the golden five-cube compound (icosahedral symmetry, faces on the 15
    two-fold axes of the icosahedron, coordinates in Q(sqrt5)) alone gives
    exactly 351 bounded regions;
  - the best known RATIONAL six-congruent-cube compound (found by unrestricted
    search over rational rotations, no golden structure) gives 635, with
    per-depth histogram {1:118, 2:214, 3:164, 4:102, 5:36, 6:1} (verified
    against six_cube_search_results.md Postscript 4, "Updated observed
    ceilings: total <= 635, d1 <= 118, d2 <= 214"; d3/d4/d5 ceilings 164/102/36
    "survive" as conjectures per Postscript 4's conjecture-status table).

This script attaches a SIXTH congruent cube to the golden five under a
rational rotation (so its face normals stay in Q(sqrt5), keeping everything
in exact arithmetic) and searches for the best resulting 6-cube total, in two
families:
  Family A: sixth cube's matrix = Q(quat)            (world-axis-relative)
  Family B: sixth cube's matrix = Q(quat) * G2        (relative to golden cube 2)
Both compositions stay in Q(sqrt5): rot_from_quat(*ints) always returns an
all-rational (b=0 on every entry) Q5 matrix, and Q5 is closed under
+,-,*,/ (see cube_compound_exact.Q5.__mul__: no sqrt5*sqrt5 cross-term
survives division by field elements, since the class -- not any single
operand -- is closed), so Q(quat) composed with G2's Q(sqrt5) entries lands
back in Q(sqrt5) exactly.

Why G2 and not G1 (the task brief said G1): golden cube index 0 in
find_cubes()'s triple ordering IS the axis-aligned cube (build_axes()'s
first three axes are literally the standard basis, and combinations()
visits (0,1,2) first), so G1's matrix is the IDENTITY. Consequence,
confirmed empirically on all 114 quaternions evaluated in both families
before this fix: family B as originally specified (Q * G1 = Q * I = Q) is
IDENTICAL to family A -- every (A, q) / (B, q) pair in the first 228 log
lines of golden_search.jsonl has equal totals and equal by_depth. Family B
is therefore anchored on golden cube 2, whose matrix is genuinely
irrational (nonzero sqrt5 parts), giving a genuinely distinct orbit.
Post-fix family-B log records carry "anchor": "G2"; pre-fix B records
(no anchor field) mean Q * G1 = Q and exactly duplicate their A partner.

Usage:
  python3 golden_six.py gates              # run V1/V2/V3 only, then stop
  python3 golden_six.py search             # gates, then full search + hillclimb
  python3 golden_six.py resume             # skip gates/probe, dedupe against
                                           # the existing log, run remaining
                                           # batch + hillclimbs
"""
import itertools
import json
import math
import random
import sys
import time
from multiprocessing import Pool

import cube_compound_exact as cce
from cube_compound_exact import build_axes, find_cubes
from certify_six import exact_count_config, rationalize
from golden_rotations import Rot, rot_from_quat
from six_cube_search import random_mats

LOG_PATH = '/Users/dmi/carroll/golden_search.jsonl'
MAXC = 512          # |quaternion component| bound, matches exact_search.py's
                     # rationalize(..., N=512) convention (see certify_six.py)


# --------------------------------------------------------------- geometry
def golden_five():
    """The 5 golden cubes as Rot objects (.m populated, Q(sqrt5) entries) --
    IDENTICAL construction to exact_search.py's validate(), which is the
    already-validated pattern for handing golden-compound cubes to
    exact_count_config. No extra wrapper class is needed: Rot.m is already
    the (row, col) nested-tuple structure exact_count_config indexes via
    R.m[i][j]."""
    axes = build_axes()
    triples = find_cubes(axes)
    rots5 = []
    for t in triples:
        cols = [axes[i] for i in t]
        rots5.append(Rot([[cols[j][i] for j in range(3)] for i in range(3)]))
    return rots5


def gcd_reduce(ints):
    g = math.gcd(*ints)
    if g > 1:
        ints = [i // g for i in ints]
    if not any(ints):
        ints = [1, 0, 0, 0]
    return ints


def sixth_cube(family, quat, g5):
    """Build the sixth cube's Rot for the given family and integer
    quaternion. family 'A': sixth = Q(quat) directly (rational rotation
    relative to world axes -- and to golden cube 1, whose matrix is the
    identity). family 'B': sixth = Q(quat) * G2 (rational rotation of
    golden cube 2, an irrational Q(sqrt5) orientation, so this orbit is
    disjoint from A except at coincidences)."""
    Q = rot_from_quat(*quat)
    if family == 'A':
        return Q
    if family == 'B':
        return Q * g5[1]
    raise ValueError(family)


def eval_config(family, quat):
    """Exact total + by_depth for golden-five + rational sixth cube."""
    g5 = golden_five()
    sixth = sixth_cube(family, quat, g5)
    total, bd = exact_count_config(g5 + [sixth], verbose=False)
    return total, {int(k): v for k, v in bd.items()}


def log_line(family, quat, total, bd):
    rec = dict(family=family, quat=list(quat), total=total, by_depth=bd)
    if family == 'B':
        rec['anchor'] = 'G2'    # distinguishes post-fix B from pre-fix B=Q*G1
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(rec) + '\n')
        f.flush()


def _worker(args):
    family, quat = args
    t0 = time.time()
    total, bd = eval_config(family, quat)
    return family, quat, total, bd, time.time() - t0


# ------------------------------------------------------------------ gates
def run_gates():
    """V1/V2/V3 as specified in the task brief. Returns True iff all pass.
    Prints full detail; does NOT weaken any check to force a pass."""
    all_ok = True

    print('=== GATE V1: golden-five sub-compound totals ===')
    g5 = golden_five()
    expect = [1, 13, 67, 177, 351]
    v1_ok = True
    for N in range(1, 6):
        r = cce.run(N)                      # cube_compound_exact's own path
        total, bd = exact_count_config(g5[:N], verbose=False)
        match = (r == total == expect[N - 1])
        print(f'  N={N}: cube_compound_exact.run={r}  '
              f'exact_count_config={total}  expected={expect[N - 1]}  '
              f'{"OK" if match else "FAIL"}')
        v1_ok = v1_ok and match
    print(f'V1: {"PASS" if v1_ok else "FAIL"}')
    all_ok = all_ok and v1_ok

    print('\n=== GATE V2: reproduce exact_search_results.jsonl seed 40 ===')
    # seed 40 is the FIRST record in the file (exact_search.py's search()
    # defaults start=40); reproduced independently through this file's own
    # import path (certify_six.rationalize + exact_count_config) to confirm
    # no discrepancy vs. the validated exact_search.py pipeline.
    expected_total = 575
    expected_bd = {0: 1, 1: 90, 2: 184, 3: 162, 4: 102, 5: 36, 6: 1}
    rats = rationalize(random_mats(40), 512)
    t0 = time.time()
    total, bd = exact_count_config(rats, verbose=False)
    dt = time.time() - t0
    bd = {int(k): v for k, v in bd.items()}
    v2_ok = (total == expected_total and bd == expected_bd)
    print(f'  seed 40: total={total} (expected {expected_total})  '
          f'by_depth={bd}')
    print(f'  expected by_depth={expected_bd}  ({dt:.1f}s)')
    print(f'V2: {"PASS" if v2_ok else "FAIL"}')
    all_ok = all_ok and v2_ok

    print('\n=== GATE V3: golden-five + exact duplicate of a golden cube ===')
    # Sixth = G1 exactly (identity rotation composed with golden cube 1,
    # per the task brief). This exercises the coincident-plane bookkeeping
    # (plane_key/owners_of in certify_six.py) -- ALL 6 faces of the sixth
    # cube exactly coincide with cube 1's faces, so every crossing there
    # must flip BOTH cubes' bits together, and the total must be unchanged
    # at 351 (the sixth cube adds no new geometry, only relabels existing
    # regions to depth+1). Note G1's matrix is the identity (see module
    # docstring), so this is simultaneously family A's identity point.
    sixth = g5[0]           # IDENT * G1 = G1, constructed directly
    t0 = time.time()
    total3, bd3 = exact_count_config(g5 + [sixth], verbose=False)
    dt = time.time() - t0
    v3a_ok = (total3 == 351)
    print(f'  dup G1: total={total3} (expected 351)  '
          f'by_depth={dict(sorted(bd3.items()))}  ({dt:.1f}s)')
    # Same invariant on an IRRATIONAL coincident-plane stack: family B with
    # the identity quaternion now duplicates G2 (matrix entries with nonzero
    # sqrt5 parts). Coincident-plane handling must be exact in the full
    # field, not just on rational planes.
    sixthB = sixth_cube('B', (1, 0, 0, 0), g5)
    t0 = time.time()
    total3b, bd3b = exact_count_config(g5 + [sixthB], verbose=False)
    dt = time.time() - t0
    v3b_ok = (total3b == 351)
    print(f'  dup G2: total={total3b} (expected 351)  '
          f'by_depth={dict(sorted(bd3b.items()))}  ({dt:.1f}s)')
    v3_ok = v3a_ok and v3b_ok
    print(f'V3: {"PASS" if v3_ok else "FAIL"}')
    all_ok = all_ok and v3_ok

    return all_ok


# ----------------------------------------------------------------- search
def fib_pairs(k_max=14):
    fibs = [1, 1]
    while len(fibs) <= k_max + 1:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs


def symmetric_candidates():
    """Hand-picked quaternions: identity, 90/180 about coordinate axes,
    60/120 about the body diagonals -- 60 and 120 deg about (1,1,1) are
    EXACTLY rational-quaternion-representable ((3,1,1,1) and (1,1,1,1):
    Rodrigues with cos=1/2 and axis (1,1,1)/sqrt3 gives all-rational
    entries; 90 deg about a diagonal is NOT, cos(45)=1/sqrt2 escapes Q, so
    sqrt3-convergent quaternions (a/b -> sqrt3 makes the half-angle -> 45
    deg) approximate it, tag 'near90diag'), and near-icosahedral-ratio
    quaternions built from Fibonacci convergents to phi (inexact
    approximations to a true icosahedral direction, since icosahedral
    rotations need sqrt5 and rot_from_quat only ever returns RATIONAL
    matrices)."""
    cands = []  # list of (tag, quat)
    cands.append(('identity', (1, 0, 0, 0)))
    for i, ax in enumerate(['x', 'y', 'z']):
        q90 = [1, 0, 0, 0]
        q90[i + 1] = 1
        cands.append((f'90deg_{ax}', tuple(q90)))
        qm90 = [1, 0, 0, 0]
        qm90[i + 1] = -1
        cands.append((f'-90deg_{ax}', tuple(qm90)))
        q180 = [0, 0, 0, 0]
        q180[i + 1] = 1
        cands.append((f'180deg_{ax}', tuple(q180)))
    # 120 deg about all 4 body diagonals (1,+-1,+-1): exact, rational
    for s1, s2 in itertools.product((1, -1), repeat=2):
        cands.append((f'120deg_(1,{s1},{s2})', (1, 1, s1, s2)))
        cands.append((f'240deg_(1,{s1},{s2})', (1, -1, -s1, -s2)))
    # 60 deg about the body diagonals: EXACT rational rotations
    for s1, s2 in itertools.product((1, -1), repeat=2):
        cands.append((f'60deg_(1,{s1},{s2})', (3, 1, s1, s2)))
        cands.append((f'-60deg_(1,{s1},{s2})', (3, -1, -s1, -s2)))
    # sqrt3-convergent approximants to 90 deg about (1,1,1) -- see docstring
    for (a, b) in [(2, 1), (7, 4), (12, 7), (26, 15)]:
        cands.append((f'near90diag_a{a}b{b}', (a, b, b, b)))
    # near-icosahedral-ratio quaternions: Fibonacci convergents to phi as an
    # axis direction (phi, 1, 0)-ish, small rational half-angle
    fibs = fib_pairs(14)
    for k in (6, 8, 10, 12):
        F1, F0 = fibs[k + 1], fibs[k]   # F1/F0 -> phi
        for a in (F0, F1, 1):
            cands.append((f'nearico_F{k}_a{a}', gcd_reduce([a, F1, F0, 0])))
            cands.append((f'nearico_F{k}b_a{a}', gcd_reduce([a, F1, 0, F0])))
    # dedupe + clamp
    out = []
    seen = set()
    for tag, q in cands:
        q = tuple(gcd_reduce(list(q)))
        if any(abs(c) > MAXC for c in q):
            continue
        if q in seen:
            continue
        seen.add(q)
        out.append((tag, q))
    return out


def random_candidates(n, seed):
    rng = random.Random(seed)
    out = []
    seen = set()
    while len(out) < n:
        ints = tuple(gcd_reduce([rng.randint(-MAXC, MAXC) for _ in range(4)]))
        if ints in seen:
            continue
        seen.add(ints)
        out.append(ints)
    return out


def load_done():
    """Read the append-only log into a cache {(family, quat): (total, bd)}.

    Pre-fix family-B records (no 'anchor' field) were Q * G1 = Q, i.e.
    literally family A evaluations -- they are cached under 'A', and do NOT
    satisfy a family-B (anchor G2) lookup. Post-fix B records carry
    anchor='G2' and cache under 'B'."""
    done = {}
    try:
        with open(LOG_PATH) as f:
            for line in f:
                rec = json.loads(line)
                fam = rec['family']
                if fam == 'B' and rec.get('anchor') != 'G2':
                    fam = 'A'
                key = (fam, tuple(rec['quat']))
                done[key] = (rec['total'],
                             {int(k): v for k, v in rec['by_depth'].items()})
    except FileNotFoundError:
        pass
    return done


def run_pool_batch(jobs, pool, best_tracker, done, tag_map=None):
    """jobs: list of (family, quat). Skips already-done ones (cache hit,
    still feeds best_tracker), evaluates the rest in parallel, logs each
    fresh result, updates best_tracker and done. Returns nothing (results
    live in `done`)."""
    fresh = []
    for family, quat in jobs:
        hit = done.get((family, quat))
        if hit is not None:
            total, bd = hit
            if total > best_tracker['total']:
                best_tracker.update(total=total, family=family, quat=quat,
                                    bd=bd)
        else:
            fresh.append((family, quat))
    if not fresh:
        return
    for family, quat, total, bd, dt in pool.imap_unordered(_worker, fresh):
        log_line(family, quat, total, bd)
        done[(family, quat)] = (total, bd)
        tag = ''
        if tag_map is not None:
            tag = tag_map.get((family, quat), '')
        mark = ''
        if total > best_tracker['total']:
            best_tracker.update(total=total, family=family, quat=quat, bd=bd)
            mark = '  <-- NEW BEST'
        print(f'  [{family}] quat={quat}  {tag:24s} total={total:4d}  '
              f'({dt:5.1f}s){mark}', flush=True)


def neighbors(quat):
    out = []
    for i in range(4):
        for delta in (-2, -1, 1, 2):
            q = list(quat)
            q[i] += delta
            q = tuple(gcd_reduce(q))
            if all(abs(c) <= MAXC for c in q) and q != tuple(quat):
                out.append(q)
    # dedupe
    return sorted(set(out))


def hillclimb(family, start_quat, pool, best_tracker, done, max_steps=8):
    """Exact greedy hill-climb: evaluate all neighbors in parallel (cache
    hits skipped), move to the best-improving one, repeat. Stops at a local
    max or max_steps."""
    cur = tuple(start_quat)
    if (family, cur) in done:
        cur_total, cur_bd = done[(family, cur)]
    else:
        cur_total, cur_bd = eval_config(family, cur)
        log_line(family, cur, cur_total, cur_bd)
        done[(family, cur)] = (cur_total, cur_bd)
    print(f'  hillclimb[{family}] start quat={cur} total={cur_total}',
          flush=True)
    path = [(cur, cur_total, cur_bd)]
    for step in range(max_steps):
        nbrs = neighbors(cur)
        fresh = [(family, q) for q in nbrs if (family, q) not in done]
        for fam, q, total, bd, dt in pool.imap_unordered(_worker, fresh):
            log_line(fam, q, total, bd)
            done[(fam, q)] = (total, bd)
            if total > best_tracker['total']:
                best_tracker.update(total=total, family=fam, quat=q, bd=bd)
        best_q, best_total, best_bd = None, cur_total, cur_bd
        for q in nbrs:
            total, bd = done[(family, q)]
            if total > best_total:
                best_q, best_total, best_bd = q, total, bd
        if best_q is None:
            print(f'  hillclimb[{family}] step {step}: LOCAL MAX at '
                  f'{cur} total={cur_total}', flush=True)
            break
        cur, cur_total, cur_bd = best_q, best_total, best_bd
        path.append((cur, cur_total, cur_bd))
        print(f'  hillclimb[{family}] step {step}: moved to {cur} '
              f'total={cur_total}', flush=True)
    return path


# --------------------------------------------------------------- driver
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'search'

    if mode != 'resume':
        ok = run_gates()
        if not ok:
            print('\nONE OR MORE GATES FAILED. Stopping before search, per '
                  'task instructions.')
            sys.exit(1)
        print('\nAll gates PASS.\n')
        if mode == 'gates':
            return
    else:
        print('resume mode: gates were run and PASSED earlier this session '
              '(V1/V2/V3, see golden_wall_report.md); skipping straight to '
              'the deduped search.\n')

    if mode != 'resume':
        # ---- timing probe
        print('=== timing probe ===')
        probe_quats = [(1, 2, 3, 4), (37, -19, 8, 251),
                       (129, -171, -137, -28)]
        times = []
        for q in probe_quats:
            t0 = time.time()
            total, bd = eval_config('A', q)
            dt = time.time() - t0
            times.append(dt)
            print(f'  probe quat={q} total={total} ({dt:.1f}s)')
        avg = sum(times) / len(times)
        print(f'measured avg {avg:.1f}s/eval single-threaded; with an 8-way '
              f'pool, effective throughput ~{8/avg:.2f} eval/s\n')

    best = {'total': 0, 'family': None, 'quat': None, 'bd': None}
    done = load_done()
    print(f'loaded {len(done)} cached evaluations from {LOG_PATH}')

    with Pool(8) as pool:
        print('=== symmetric candidates (both families) ===')
        sym = symmetric_candidates()
        tag_map = {}
        jobs = []
        for tag, q in sym:
            for fam in ('A', 'B'):
                jobs.append((fam, q))
                tag_map[(fam, q)] = tag
        run_pool_batch(jobs, pool, best, done, tag_map)

        print(f'\n=== random search (seed=1729, {MAXC=}) ===')
        rand_quats = random_candidates(75, seed=1729)
        jobs = []
        for q in rand_quats:
            jobs.append(('A', q))
            jobs.append(('B', q))
        run_pool_batch(jobs, pool, best, done, None)

        print(f'\ncurrent best after symmetric+random: family={best["family"]} '
              f'quat={best["quat"]} total={best["total"]}', flush=True)

        # ---- hillclimb from best-so-far per family
        print('\n=== hillclimb ===')
        by_family_best = {'A': (0, None), 'B': (0, None)}
        for (fam, q), (total, bd) in done.items():
            if total > by_family_best[fam][0]:
                by_family_best[fam] = (total, q)
        for fam in ('A', 'B'):
            total0, q0 = by_family_best[fam]
            if q0 is None:
                continue
            print(f'-- hillclimb family {fam} from quat={q0} total={total0}',
                  flush=True)
            hillclimb(fam, q0, pool, best, done, max_steps=6)

    print(f'\n=== FINAL BEST === family={best["family"]} quat={best["quat"]} '
          f'total={best["total"]} by_depth={best["bd"]}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
