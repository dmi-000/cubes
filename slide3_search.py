#!/usr/bin/env python3
# Working principles: SLIDE3_SPEC_V2.md + slide3_report.md. Project index: README.md
"""SLIDE3_SPEC.md Section 1: overlay search over two sliding 3-cube triples.

X(theta1, theta2, R) = C(theta1) UNION R . C(theta2)
  C(theta) = { Rx(theta).cube, Ry(theta).cube, Rz(theta).cube }   (Section 0
  family: base rotation about x, B-conjugated by the shared octahedral/
  icosahedral 3-fold generator B = 120deg about (1,1,1), which cyclically
  permutes x->y->z->x -- see slide3_report.md Section 0 for the derivation
  and the exact proof that C(theta) always has 3 EQUAL pairwise relative-
  rotation traces, hence can never be congruent to a golden 3-subset,
  which never does; and that C(theta) is a rational-PLATEAU at 55 for
  every theta in (0,90) except the exact irrational wall theta=45deg
  (needs Q(sqrt2)), where it jumps to 67 -- IDENTICAL total and histogram
  to the golden triple's 67, {1:48,2:18,3:1}, despite NOT being congruent
  to it (proven separately).

Rational parameterization: tan(theta/2) = p/q gives quat (q,p,0,0) for
Rx(theta) etc (all-rational, Q5 b=0). Second triple's per-cube quats are
the SAME construction, then each is composed (Hamilton product) with a
global relative-rotation quat R=(rw,rx,ry,rz): still an integer quat
(Hamilton product of integers is integer), so the WHOLE 6-cube config
stays fully rational and can be counted by the FAST validated C++ engine
`./cube_regions --quats` (6 groups, ~7ms/eval, |component|<=512 after
gcd reduction).

Read-only: cube_regions[_n] binaries, certify_six.py, cube_compound_exact.py,
golden_rotations.py, qtower.py, six_cube_search_results.md,
exact_search_results.jsonl. All logging goes to slide3_search.jsonl only.
"""
import itertools
import json
import math
import random
import subprocess
import sys
import time

LOG_PATH = '/Users/dmi/carroll/slide3_search.jsonl'
ENGINE = '/Users/dmi/carroll/cube_regions'   # fixed 6-quat-group engine
MAXC = 512


# ------------------------------------------------------------- quat algebra
def gcd_reduce(ints):
    g = math.gcd(*[abs(i) for i in ints])
    if g > 1:
        ints = [i // g for i in ints]
    if not any(ints):
        ints = [1, 0, 0, 0]
    return ints


def hamilton(r, q):
    """Hamilton product r*q (apply q first, then r) -- integer quats."""
    w1, x1, y1, z1 = r
    w2, x2, y2, z2 = q
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return gcd_reduce([w, x, y, z])


def triple_quats(q, p):
    """C(theta) quats, tan(theta/2)=p/q: [Rx, Ry, Rz]."""
    return [gcd_reduce([q, p, 0, 0]), gcd_reduce([q, 0, p, 0]),
            gcd_reduce([q, 0, 0, p])]


def overlay_quats(q1, p1, q2, p2, R):
    """Full 6-cube config: triple1 quats ++ (R composed with triple2 quats)."""
    t1 = triple_quats(q1, p1)
    t2 = triple_quats(q2, p2)
    t2r = [hamilton(R, q) for q in t2]
    return t1 + t2r


def fits_cap(quats, cap=MAXC):
    return all(abs(c) <= cap for grp in quats for c in grp)


def theta_deg(q, p):
    return 2 * math.degrees(math.atan2(p, q))


# ------------------------------------------------------------- Farey grids
def farey(qmax, interior=True):
    seen = set()
    out = []
    for q in range(1, qmax + 1):
        for p in range(0, q + 1):
            g = math.gcd(p, q) if p else q
            pg, qg = (p // g, q // g) if g else (p, q)
            if (pg, qg) in seen:
                continue
            seen.add((pg, qg))
            out.append((pg, qg))
    out.sort(key=lambda pq: pq[0] / pq[1] if pq[1] else 0)
    if interior:
        out = [pq for pq in out if 0 < pq[0] < pq[1]]
    return out


# ------------------------------------------------------------ R candidates
def r_candidates(qmax_axis=4, n_random=20, rng_seed=2026):
    cands = []  # (tag, R quat)
    cands.append(('identity', (1, 0, 0, 0)))
    # shared 3-fold axis (1,1,1) and its 3 siblings, over a Farey angle grid
    diag_signs = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
    fa = farey(qmax_axis)
    for (s1, s2, s3) in diag_signs:
        for (p, q) in fa:
            cands.append((f'diag({s1},{s2},{s3})_p{p}q{q}',
                           gcd_reduce([q, p * s1, p * s2, p * s3])))
            cands.append((f'diag({s1},{s2},{s3})_p{-p}q{q}',
                           gcd_reduce([q, -p * s1, -p * s2, -p * s3])))
    # 90deg about face axes
    for i, ax in enumerate(['x', 'y', 'z']):
        q90 = [1, 0, 0, 0]
        q90[i + 1] = 1
        cands.append((f'90deg_{ax}', tuple(q90)))
    # 180deg about face-diagonal (2-fold) axes
    for (a, b) in [(1, 1, 0, 0), (1, -1, 0, 0), (1, 0, 1, 0), (1, 0, -1, 0),
                   (0, 0, 1, 1), (0, 0, 1, -1)][:0]:
        pass
    for combo in [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1),
                  (0, 1, 1), (0, 1, -1)]:
        cands.append((f'180deg_edge{combo}', (0,) + combo))
    # golden-adjacent rational approximants: axis ~ (phi,1,0)-ish via Fibonacci
    fibs = [1, 1]
    while len(fibs) < 16:
        fibs.append(fibs[-1] + fibs[-2])
    for k in (6, 8, 10):
        F1, F0 = fibs[k + 1], fibs[k]
        for (p, q) in [(1, 3), (1, 2), (2, 3), (1, 1), (1, 4)]:
            cands.append((f'nearico_F{k}_p{p}q{q}',
                           gcd_reduce([q, p * F1, p * F0, 0])))
    # random baseline
    rng = random.Random(rng_seed)
    for i in range(n_random):
        q = gcd_reduce([rng.randint(-40, 40) for _ in range(4)])
        cands.append((f'random{i}', tuple(q)))
    # dedupe + clamp
    out = []
    seen = set()
    for tag, r in cands:
        r = tuple(gcd_reduce(list(r)))
        if any(abs(c) > MAXC for c in r):
            continue
        if r in seen:
            continue
        seen.add(r)
        out.append((tag, r))
    return out


# ------------------------------------------------------------------ engine
def eval_batch(configs):
    """configs: list of (meta_dict, quats[6]). Returns list of
    (meta, total, by_depth, quats). Skips configs violating the |c|<=512
    cap (returns None for those -- caller must handle)."""
    ok_idx = []
    lines = []
    for i, (meta, quats) in enumerate(configs):
        if fits_cap(quats):
            ok_idx.append(i)
            lines.append(';'.join(','.join(map(str, g)) for g in quats))
    if not lines:
        return [None] * len(configs)
    inp = '\n'.join(lines) + '\n'
    proc = subprocess.run([ENGINE, '--quats-stdin'], input=inp,
                           capture_output=True, text=True)
    out_lines = proc.stdout.strip().split('\n') if proc.stdout.strip() else []
    assert len(out_lines) == len(lines), \
        f'engine returned {len(out_lines)} lines for {len(lines)} configs'
    results = [None] * len(configs)
    for oi, li in zip(out_lines, ok_idx):
        rec = json.loads(oi)
        meta, quats = configs[li]
        results[li] = (meta, rec['bounded'], rec['by_depth'], rec['quats'])
    return results


def log_results(results, tag=''):
    n_logged = 0
    with open(LOG_PATH, 'a') as f:
        for r in results:
            if r is None:
                continue
            meta, total, bd, quats = r
            rec = dict(meta)
            rec['quats'] = quats
            rec['total'] = total
            rec['by_depth'] = {int(k): v for k, v in bd.items()}
            if tag:
                rec['phase'] = tag
            f.write(json.dumps(rec) + '\n')
            n_logged += 1
    return n_logged


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    print('slide3_search.py library module -- see slide3_p1.py / slide3_p2.py '
          '/ slide3_p3.py for the actual phase drivers.')
