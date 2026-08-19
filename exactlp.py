#!/usr/bin/env python3
"""Exact rational replacement for isolation67._fm's strict homogeneous LP.

WHY `_fm` WAS REPLACED.  `_fm` is naive Fourier-Motzkin elimination: at each of
the (up to nv) elimination steps it replaces the row set with the set of all
pos-neg row combinations, so both the ROW COUNT and the coefficient BIT-LENGTH
can grow multiplicatively at every step, compounding across steps. A live
py-spy trace (arrangement.py, the 183 record, wall 10 of 12) caught `_fm` seven
recursion levels deep, still running after 9+ minutes of CPU on ONE candidate,
inside a single Fraction multiply in the row-combination step -- and that was
not a rare fluke: 51 of that case's 12 888 codimension-1 candidates (0.4%,
sampled directly) already cost >=3s each in isolation, against a <1ms typical
cost. The same routine is the shared bottleneck of two live campaigns
(ckpt_727, ckpt_393) whose candidate sets are of exactly this shape.

WHAT REPLACES IT.  `feasible_strict` decides the same question -- exact
rational strict feasibility of a homogeneous system c.y > 0 for every row c --
via a bounded-variable-free rational SIMPLEX instead of elimination. The
homogeneous strict-feasibility question is scale-invariant (if y works, so
does any positive multiple), so it is recast as a single BOUNDED linear
program that cannot itself blow up combinatorially:

    y = p - q,  p,q >= 0,  sum(p) + sum(q) <= 1      (y confined to the L1 ball)
    maximize t   s.t.   c_i . y - t >= 0  for every row c_i,   t >= 0

The original system is strictly feasible iff this LP's optimum is > 0: any
witness y with c_i.y > 0 for all i scales down into the L1 ball without
changing any sign, and conversely any (p,q,t) with t>0 feasible in the LP
hands back y=p-q with c_i.y >= t > 0 directly, no unscaling needed. Row count
stays FIXED at (m+1) for the life of the solve (m input rows plus the one
L1-ball row) -- there is no elimination step to compound. Solved by dense
tableau simplex over `fractions.Fraction`, entering variable chosen by the
largest-coefficient (Dantzig) rule for speed, with a hard fallback to Bland's
rule (smallest-index entering AND leaving, the classical anti-cycling
combination) once the pivot count exceeds a generous multiple of the tableau
size -- so termination in finitely many pivots is guaranteed regardless of
degeneracy, never just empirically observed.

MEASURED TAIL BEHAVIOUR (2026-08-20, this machine, see `exactlp_validation
_*.json` written alongside this file for the full numbers this run produced):
see the run report for the actual median/p99 speed ratios against `_fm` and
the real-checkpoint agreement counts -- filled in by every run of `python3
exactlp.py`, which is also this module's own validation harness. Do not
reintroduce `_fm` on the strength of a "just for this one case" argument
without rerunning this file: its whole point is the tail, not the median.

INTERFACE.  Drop-in replacement for `isolation67._fm(rows, nv)`: same
signature, same semantics (homogeneous, strict, `fractions.Fraction`
throughout, no floating point, no tolerances), same None-or-witness return.
"""
import sys
from fractions import Fraction as F

# Pivot budget past which we give up on Dantzig's rule and switch permanently
# to Bland's rule (smallest-index entering AND leaving) for the rest of the
# solve. Bland's rule alone guarantees termination in finitely many pivots for
# ANY LP (no cycling is possible), so this bound is a PERFORMANCE fallback,
# not a correctness one -- it exists so a pathological tie pattern degrades to
# "provably finite but slow" instead of silently returning a wrong answer
# from a truncated search.
_BLAND_AFTER_FACTOR = 50


def _pivot(T, row, col, ncols):
    piv = T[row][col]
    Trow = T[row]
    if piv != 1:
        T[row] = Trow = [x / piv for x in Trow]
    for i, Ti in enumerate(T):
        if i == row:
            continue
        f = Ti[col]
        if f != 0:
            T[i] = [a - f * b for a, b in zip(Ti, Trow)]


def _simplex_max(A, b, c, basis):
    """Maximize c.x s.t. Ax = b, x >= 0, given an initial basic feasible
    solution: `basis` is a list of len(A) column indices such that A
    restricted to those columns is the identity and b >= 0 (checked by the
    caller's construction, not re-verified here). Bland's-rule-guaranteed
    termination via a Dantzig-then-Bland hybrid (see module docstring).
    Returns the full solution vector x (length len(c)).
    """
    m = len(A)
    n = len(c)
    T = [list(A[i]) + [b[i]] for i in range(m)]
    T.append([-c[j] for j in range(n)] + [F(0)])
    basis = list(basis)
    pivot_budget = _BLAND_AFTER_FACTOR * (m + n) + 50
    pivots = 0
    use_bland = False
    while True:
        obj = T[m]
        if use_bland:
            enter = next((j for j in range(n) if obj[j] < 0), None)
        else:
            enter = None
            best = F(0)
            for j in range(n):
                if obj[j] < best:
                    best = obj[j]
                    enter = j
        if enter is None:
            break
        leave = None
        best_ratio = None
        for i in range(m):
            a = T[i][enter]
            if a > 0:
                ratio = T[i][n] / a
                if (best_ratio is None or ratio < best_ratio or
                        (ratio == best_ratio and basis[i] < basis[leave])):
                    best_ratio = ratio
                    leave = i
        if leave is None:
            raise RuntimeError('unbounded LP in feasible_strict -- should '
                                'not happen (the feasible region is the '
                                'bounded L1 ball); indicates a bug')
        _pivot(T, leave, enter, n)
        basis[leave] = enter
        pivots += 1
        if pivots > pivot_budget and not use_bland:
            use_bland = True
    x = [F(0)] * n
    for i in range(m):
        x[basis[i]] = T[i][n]
    return x


def feasible_strict(rows, nv):
    """Witness y with c.y > 0 for every row c (each row length nv), or None.

    Homogeneous strict feasibility, decided by exact rational simplex (see
    module docstring for the LP construction). Drop-in replacement for
    isolation67._fm: same signature and semantics.
    """
    if nv == 0:
        return [] if not rows else None
    if not rows:
        return [F(0)] * nv                # vacuously true; matches _fm's own
                                           # empty-rows convention exactly
    m = len(rows)
    for r in rows:
        if all(x == 0 for x in r):
            return None                   # "0 > 0" is unsatisfiable outright

    # variable layout: p_0..p_{nv-1}, q_0..q_{nv-1}, t, s_0..s_{m-1}, u
    n = 2 * nv + 1 + m + 1
    IDX_T = 2 * nv
    IDX_S0 = 2 * nv + 1
    IDX_U = IDX_S0 + m

    A = []
    b = []
    basis = []
    for i, c in enumerate(rows):
        row = [F(0)] * n
        for j in range(nv):
            cij = F(c[j])
            row[j] = -cij
            row[nv + j] = cij
        row[IDX_T] = F(1)
        row[IDX_S0 + i] = F(1)
        A.append(row)
        b.append(F(0))
        basis.append(IDX_S0 + i)
    row = [F(0)] * n
    for j in range(nv):
        row[j] = F(1)
        row[nv + j] = F(1)
    row[IDX_U] = F(1)
    A.append(row)
    b.append(F(1))
    basis.append(IDX_U)

    c_obj = [F(0)] * n
    c_obj[IDX_T] = F(1)

    x = _simplex_max(A, b, c_obj, basis)
    if x[IDX_T] <= 0:
        return None
    return [x[j] - x[nv + j] for j in range(nv)]


# ============================================================== validation
# Everything below runs only under `python3 exactlp.py <phase>` and writes its
# own report files (exactlp_report_<phase>.json) in this directory -- no
# existing file is read for writing and nothing in ckpt_727/, ckpt_393/ or
# arrangement_ckpt_183/ is ever opened for anything but reading.
HERE = None


def _here():
    global HERE
    if HERE is None:
        import os
        HERE = os.path.dirname(os.path.abspath(__file__))
    return HERE


class _Timeout(Exception):
    pass


def _with_timeout(fn, args, seconds):
    """Run fn(*args) under a wall-clock deadline. Returns (result, timed_out).
    SIGALRM-based (POSIX only, fine on this machine); never used inside
    feasible_strict itself, only in the validation harness to bound _fm."""
    import signal

    def _handler(signum, frame):
        raise _Timeout()

    old = signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        return fn(*args), False
    except _Timeout:
        return None, True
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def _peak_rss_mb():
    import resource
    # Darwin reports ru_maxrss in BYTES, Linux in KB -- this machine is Darwin.
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024)


def _percentile(sorted_vals, p):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p
    f, c = int(k), min(int(k) + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


# ------------------------------------------------------------- phase: random
def _rand_row(nv, mag, rnd):
    return [rnd.randint(-mag, mag) for _ in range(nv)]


def phase_random(n_trials, seed, fm_timeout, out_path):
    import random, time, json
    import isolation67 as iso

    rnd = random.Random(seed)
    mags = (1, 3, 20, 200, 5000)
    mismatches = []
    bad_witnesses = []
    old_timeouts = 0
    n_feasible = n_infeasible = 0
    new_times, old_times, ratios = [], [], []
    t_start = time.time()
    for trial in range(n_trials):
        nv = rnd.randint(2, 15)
        nrows = rnd.randint(1, 40)
        mag = rnd.choice(mags)
        rows = [_rand_row(nv, mag, rnd) for _ in range(nrows)]

        t0 = time.time()
        y_new = feasible_strict(rows, nv)
        t1 = time.time()
        new_times.append(t1 - t0)

        y_old, timed_out = _with_timeout(iso._fm, (rows, nv), fm_timeout)
        t2 = time.time()
        if timed_out:
            old_timeouts += 1
        else:
            old_times.append(t2 - t1)
            ratios.append((t1 - t0) / (t2 - t1) if (t2 - t1) > 0 else None)

        dec_new = y_new is not None
        if y_new is not None:
            n_feasible += 1
            for r in rows:
                v = sum(F(r[k]) * y_new[k] for k in range(nv))
                if v <= 0:
                    bad_witnesses.append({'rows': rows, 'nv': nv, 'y': [str(x) for x in y_new]})
        else:
            n_infeasible += 1

        if not timed_out:
            dec_old = y_old is not None
            if dec_new != dec_old:
                mismatches.append({'rows': rows, 'nv': nv, 'new': dec_new, 'old': dec_old})

        if (trial + 1) % 100 == 0:
            print('   random: %d/%d done, %d old_timeouts, %d mismatches so far, %.0fs' %
                  (trial + 1, n_trials, old_timeouts, len(mismatches), time.time() - t_start),
                  flush=True)

    ratios = [r for r in ratios if r is not None]
    ratios.sort()
    new_times.sort()
    report = {
        'n_trials': n_trials, 'seed': seed, 'fm_timeout_s': fm_timeout,
        'n_feasible': n_feasible, 'n_infeasible': n_infeasible,
        'old_timeouts': old_timeouts,
        'n_mismatches': len(mismatches), 'mismatches': mismatches,
        'n_bad_witnesses': len(bad_witnesses), 'bad_witnesses': bad_witnesses,
        'median_ratio_new_over_old': _percentile(ratios, 0.5),
        'p99_ratio_new_over_old': _percentile(ratios, 0.99),
        'median_new_time_s': _percentile(new_times, 0.5),
        'p99_new_time_s': _percentile(new_times, 0.99),
        'wall_s': time.time() - t_start,
        'peak_rss_mb': _peak_rss_mb(),
    }
    json.dump(report, open(out_path, 'w'), indent=1)
    print(json.dumps({k: v for k, v in report.items()
                       if k not in ('mismatches', 'bad_witnesses')}, indent=1))
    return report


# --------------------------------------------------------- phase: real ckpts
def _iter_ckpt(ckpt_dir):
    import glob, json, os
    for fn in sorted(glob.glob(os.path.join(ckpt_dir, 'worker_*.jsonl'))):
        with open(fn) as fh:                     # READ ONLY -- never write here
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue                      # a live writer's in-flight tail line


def _deser_sigma_local(s):
    return tuple(int(x) for x in s.split(',')) if s else ()


def _check_growth_ckpt(ckpt_dir, walls, ncols, label, out_path, max_check=None):
    """ckpt_727 / ckpt_393: max_codim=0 runs, every sigma is a growing
    +-1-only prefix of `walls` (see arrangement.run_parallel's chamber-stage
    loop / arrangement._test_sigma for `len(cand) < M`). Reconstruction: rows
    = the first len(sigma) walls, each row negated where sigma is -1."""
    import time, json
    n_checked = 0
    n_agree = 0
    disagreements = []
    t0 = time.time()
    for rec in _iter_ckpt(ckpt_dir):
        sigma = _deser_sigma_local(rec['sigma'])
        k = len(sigma)
        rows = [walls[t] if sigma[t] == 1 else [-x for x in walls[t]] for t in range(k)]
        y_new = feasible_strict(rows, ncols)
        recorded_feasible = rec['witness'] is not None
        new_feasible = y_new is not None
        n_checked += 1
        if recorded_feasible == new_feasible:
            n_agree += 1
            if y_new is not None:
                for r in rows:
                    v = sum(F(r[j]) * y_new[j] for j in range(ncols))
                    if v <= 0:
                        disagreements.append({'kind': 'bad_witness', 'sigma': list(sigma),
                                               'rows': rows})
        else:
            disagreements.append({'kind': 'decision_mismatch', 'sigma': list(sigma),
                                   'rows': rows, 'recorded_feasible': recorded_feasible,
                                   'new_feasible': new_feasible})
        if max_check and n_checked >= max_check:
            break
        if n_checked % 20000 == 0:
            print('   %s: %d checked, %d agree, %.0fs' %
                  (label, n_checked, n_agree, time.time() - t0), flush=True)
    report = {'label': label, 'n_checked': n_checked, 'n_agree': n_agree,
              'n_disagree': n_checked - n_agree, 'disagreements': disagreements,
              'wall_s': time.time() - t0, 'peak_rss_mb': _peak_rss_mb()}
    json.dump(report, open(out_path, 'w'), indent=1)
    print('%s: checked=%d agree=%d disagree=%d %.0fs' %
          (label, n_checked, n_agree, n_checked - n_agree, report['wall_s']), flush=True)
    return report


def phase_ckpt727(out_path, max_check=None):
    import sys, os
    sys.path.insert(0, _here())
    from growth727 import walls_of, BASE
    walls, ncols = walls_of(BASE + [(7, 14, 1, -5)])
    _check_growth_ckpt(os.path.join(_here(), 'ckpt_727'), walls, ncols,
                        '727', out_path, max_check=max_check)


def phase_ckpt393(out_path, max_check=None):
    import sys, os
    sys.path.insert(0, _here())
    from growth727 import walls_of, BASE
    walls, ncols = walls_of(BASE)
    _check_growth_ckpt(os.path.join(_here(), 'ckpt_393'), walls, ncols,
                        '393', out_path, max_check=max_check)


def phase_ckpt183(out_path):
    """arrangement_ckpt_183: max_codim=None, so sigmas of full length M can
    carry zeros (face candidates). len(sigma) < M -> same growing-prefix
    reconstruction as 727/393. len(sigma) == M with no zero -> a full
    chamber (all M walls signed). len(sigma) == M with zeros -> reconstruct
    exactly as arrangement._project_and_test: project onto the null space of
    the zeroed walls (D.nullspace, exact), then test the projected strict
    inequalities."""
    import sys, os, io, time, json
    sys.path.insert(0, _here())
    import dimension as D
    from arrangement import _record183_walls

    log = io.StringIO()
    walls, ncols = _record183_walls(log)
    M = len(walls)
    D.set_field(0)

    n_checked = n_agree = 0
    disagreements = []
    t0 = time.time()
    ckpt_dir = os.path.join(_here(), 'arrangement_ckpt_183')
    for rec in _iter_ckpt(ckpt_dir):
        sigma = _deser_sigma_local(rec['sigma'])
        k = len(sigma)
        recorded_feasible = rec['witness'] is not None
        if k < M:
            rows = [walls[t] if sigma[t] == 1 else [-x for x in walls[t]] for t in range(k)]
            nv = ncols
        else:
            zeros = [t for t in range(M) if sigma[t] == 0]
            if not zeros:
                rows = [walls[t] if sigma[t] == 1 else [-x for x in walls[t]] for t in range(M)]
                nv = ncols
            else:
                eqs = [walls[t] for t in zeros]
                ns = D.nullspace(eqs, ncols)
                if not ns:
                    n_checked += 1
                    if recorded_feasible:
                        disagreements.append({'kind': 'decision_mismatch', 'sigma': list(sigma),
                                               'reason': 'empty nullspace but recorded feasible',
                                               'recorded_feasible': True, 'new_feasible': False})
                    else:
                        n_agree += 1
                    continue
                nz = [(t, sigma[t]) for t in range(M) if sigma[t] != 0]
                rows = []
                for t, s in nz:
                    row = [sum(walls[t][c] * b[c] for c in range(ncols)) for b in ns]
                    if s == -1:
                        row = [-x for x in row]
                    rows.append(row)
                nv = len(ns)
        y_new = feasible_strict(rows, nv)
        new_feasible = y_new is not None
        n_checked += 1
        if recorded_feasible == new_feasible:
            n_agree += 1
            if y_new is not None:
                for r in rows:
                    v = sum(F(r[j]) * y_new[j] for j in range(nv))
                    if v <= 0:
                        disagreements.append({'kind': 'bad_witness', 'sigma': list(sigma), 'rows': rows})
        else:
            disagreements.append({'kind': 'decision_mismatch', 'sigma': list(sigma),
                                   'rows': rows, 'recorded_feasible': recorded_feasible,
                                   'new_feasible': new_feasible})
    report = {'label': '183', 'M': M, 'ncols': ncols, 'n_checked': n_checked,
              'n_agree': n_agree, 'n_disagree': n_checked - n_agree,
              'disagreements': disagreements, 'wall_s': time.time() - t0,
              'peak_rss_mb': _peak_rss_mb()}
    json.dump(report, open(out_path, 'w'), indent=1)
    print('183: checked=%d agree=%d disagree=%d %.0fs' %
          (n_checked, n_agree, n_checked - n_agree, report['wall_s']), flush=True)
    return report


# --------------------------------------------------------------- phase: hard
def phase_hard(out_path, fm_timeout=45, n_samples=8):
    """Deliberately hard instances: (a) the OUTSTANDING (not yet
    checkpointed) stage-14 candidates of the live ckpt_393 run -- the exact
    shape of system currently blocking that campaign -- and (b) large dense
    random systems at the top of the random-test range (nv=15, rows=40,
    large coefficients), which is where FM's row/bit-length blowup is worst.
    """
    import sys, os, time, json, random
    sys.path.insert(0, _here())
    from growth727 import walls_of, BASE
    import isolation67 as iso

    walls, ncols = walls_of(BASE)
    M = len(walls)
    ckpt_dir = os.path.join(_here(), 'ckpt_393')

    # length-13 feasible frontier and length-14 already-decided set, from the
    # live checkpoint (read only).
    by_len = {}
    for rec in _iter_ckpt(ckpt_dir):
        sigma = _deser_sigma_local(rec['sigma'])
        by_len.setdefault(len(sigma), {})[sigma] = rec['witness'] is not None
    frontier13 = [s for s, feas in by_len.get(13, {}).items() if feas]
    decided14 = set(by_len.get(14, {}).keys())

    outstanding = []
    for s in frontier13:
        for sgn in (1, -1):
            cand = s + (sgn,)
            if cand not in decided14:
                outstanding.append(cand)
    random.Random(0).shuffle(outstanding)
    outstanding = outstanding[:n_samples]

    results = []
    for sigma in outstanding:
        k = len(sigma)
        rows = [walls[t] if sigma[t] == 1 else [-x for x in walls[t]] for t in range(k)]
        t0 = time.time()
        y_new = feasible_strict(rows, ncols)
        t_new = time.time() - t0
        _, timed_out = _with_timeout(iso._fm, (rows, ncols), fm_timeout)
        t_old = time.time() - t0 - t_new
        results.append({'sigma': list(sigma), 'source': 'ckpt393-stage14-outstanding',
                         'new_feasible': y_new is not None, 't_new_s': t_new,
                         't_old_s': t_old, 'old_timed_out': timed_out,
                         'old_timeout_budget_s': fm_timeout})
        print('   sigma len=%d new=%.4fs feasible=%s  old %s' %
              (k, t_new, y_new is not None,
               ('TIMEOUT>%ss' % fm_timeout) if timed_out else '%.4fs' % t_old), flush=True)

    # large dense random systems, the adversarial corner of the random suite
    rnd = random.Random(999)
    for _ in range(6):
        nv = 15
        nrows = 40
        mag = rnd.choice((200, 5000))
        rows = [_rand_row(nv, mag, rnd) for _ in range(nrows)]
        t0 = time.time()
        y_new = feasible_strict(rows, nv)
        t_new = time.time() - t0
        _, timed_out = _with_timeout(iso._fm, (rows, nv), fm_timeout)
        t_old = time.time() - t0 - t_new
        results.append({'sigma': None, 'source': 'dense-random-nv15-rows40',
                         'nv': nv, 'nrows': nrows, 'mag': mag,
                         'new_feasible': y_new is not None, 't_new_s': t_new,
                         't_old_s': t_old, 'old_timed_out': timed_out,
                         'old_timeout_budget_s': fm_timeout})
        print('   dense nv=%d rows=%d mag=%d new=%.4fs feasible=%s  old %s' %
              (nv, nrows, mag, t_new, y_new is not None,
               ('TIMEOUT>%ss' % fm_timeout) if timed_out else '%.4fs' % t_old), flush=True)

    report = {'n_outstanding_stage14': len(outstanding),
              'n_outstanding_total': len(by_len.get(13, {})) and
              sum(1 for s in frontier13 for sgn in (1, -1) if (s + (sgn,)) not in decided14),
              'results': results, 'peak_rss_mb': _peak_rss_mb()}
    json.dump(report, open(out_path, 'w'), indent=1)
    return report


def main():
    import sys, os
    phase = sys.argv[1] if len(sys.argv) > 1 else 'random'
    out = os.path.join(_here(), 'exactlp_report_%s.json' % phase)
    if phase == 'random':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
        phase_random(n, seed=20260820, fm_timeout=3.0, out_path=out)
    elif phase == 'ckpt727':
        mc = int(sys.argv[2]) if len(sys.argv) > 2 else None
        phase_ckpt727(out, max_check=mc)
    elif phase == 'ckpt393':
        phase_ckpt393(out)
    elif phase == 'ckpt183':
        phase_ckpt183(out)
    elif phase == 'hard':
        phase_hard(out)
    else:
        raise SystemExit('unknown phase %r' % phase)


if __name__ == '__main__':
    main()
