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
via a rational SIMPLEX (phase-1 only) instead of elimination. The homogeneous
strict-feasibility question is scale-invariant (if y works, so does any
positive multiple), so "c_i.y > 0 for every row" is exactly equivalent to
"c_i.y >= 1 for every row" (scale any witness of the first by the reciprocal
of its smallest row value to get a witness of the second, and the second
trivially implies the first). That turns it into a standard phase-1 LP
feasibility question with NO objective to optimize past zero:

    y = p - q,  p,q >= 0     c_i.(p-q) - s_i + a_i = 1,  s_i,a_i >= 0
    minimize sum(a_i)   -- feasible iff the minimum is exactly 0

An EARLIER version of this routine bounded y into an L1 ball and maximized a
slack variable t directly (c_i.y - t >= 0, sum|y_j| <= 1) -- correct, but
measured to take up to 13.8s and 5219 pivots on an 15-variable/35-row random
instance, because that formulation puts EVERY row through the origin
(c_i.0 = 0 for all i, homogeneous), an m-fold degenerate starting vertex that
stalled the simplex in thousands of zero-progress pivots before any real
step. The >=1 reformulation starts instead from a_i=1 for every row (b=1, not
0) -- a non-degenerate basic feasible solution -- and the same instance that
took 5219 pivots under the L1 formulation dropped to well under 200. Row/
column count is FIXED at m rows, 2nv+2m columns for the life of the solve --
there is no elimination step to compound, unlike `_fm`.

Solved by dense tableau simplex over `fractions.Fraction`: entering variable
by the largest-coefficient (Dantzig) rule for speed, with a hard fallback to
Bland's rule (smallest-index entering AND leaving, the classical anti-cycling
pair) once the pivot count exceeds a generous multiple of the tableau size --
so termination in finitely many pivots is guaranteed regardless of
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
    caller's construction, not re-verified here). The initial basis may have
    NONZERO cost (needed for phase-1: the artificial variables start basic
    with cost -1) -- the objective row is canonicalised against that basis
    before the first pivot. Bland's-rule-guaranteed termination via a
    Dantzig-then-Bland hybrid (see module docstring). Returns the full
    solution vector x (length len(c)).
    """
    m = len(A)
    n = len(c)
    T = [list(A[i]) + [b[i]] for i in range(m)]
    T.append([-c[j] for j in range(n)] + [F(0)])
    # canonicalise the objective row against the initial basis (no-op when
    # every initial basic variable has cost 0, as in a pure box/slack start)
    for i in range(m):
        cb = c[basis[i]]
        if cb != 0:
            T[m] = [T[m][k] + cb * T[i][k] for k in range(n + 1)]
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
                                'not happen (minimize sum(a_i), a_i >= 0, is '
                                'bounded below by 0 for any input); indicates '
                                'a bug')
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

    Homogeneous strict feasibility, decided by exact rational phase-1 simplex
    on the equivalent system c_i.y >= 1 for all i (see module docstring for
    why that's exactly equivalent, and why it's the non-degenerate choice).
    Drop-in replacement for isolation67._fm: same signature and semantics.
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

    # variable layout: p_0..p_{nv-1}, q_0..q_{nv-1}, s_0..s_{m-1}, a_0..a_{m-1}
    n = 2 * nv + 2 * m
    IDX_S0 = 2 * nv
    IDX_A0 = IDX_S0 + m

    A = []
    b = []
    basis = []
    for i, c in enumerate(rows):
        row = [F(0)] * n
        for j in range(nv):
            cij = F(c[j])
            row[j] = cij
            row[nv + j] = -cij
        row[IDX_S0 + i] = F(-1)
        row[IDX_A0 + i] = F(1)
        A.append(row)
        b.append(F(1))
        basis.append(IDX_A0 + i)

    c_obj = [F(0)] * n
    for i in range(m):
        c_obj[IDX_A0 + i] = F(-1)          # maximize -sum(a_i), i.e. minimize sum(a_i)

    x = _simplex_max(A, b, c_obj, basis)
    if any(x[IDX_A0 + i] != 0 for i in range(m)):
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
    feasible_strict itself, only in the validation harness to bound _fm.

    The alarm can legitimately fire AFTER fn(*args) has already returned but
    BEFORE the cancelling setitimer(0) call runs (fn finishing right at the
    deadline) -- a first version of this let that race raise _Timeout out of
    its own `finally` block, past the `except` that was supposed to catch it,
    crashing the whole harness. The disarm call is wrapped in its own
    try/except here so no timing of the race can escape uncaught; landing in
    that narrow window is scored as a timeout even though fn nearly finished,
    which is a harmless conservative bias (never a false SUCCESS)."""
    import signal

    def _handler(signum, frame):
        raise _Timeout()

    old = signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    timed_out = False
    result = None
    try:
        result = fn(*args)
    except _Timeout:
        timed_out = True
    finally:
        try:
            signal.setitimer(signal.ITIMER_REAL, 0)
        except _Timeout:
            timed_out = True
        signal.signal(signal.SIGALRM, old)
    return (None, True) if timed_out else (result, False)


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


# The sampling distribution of `phase_random`, as DATA rather than as literals
# buried in the loop.
#
# WHY THESE ARE PARAMETERS.  Every value here changes a reported number, and a
# value that changes a reported number and lives only in the source is exactly
# the `census_variety` failure `provenance.py` exists to prevent: the data
# survives, the settings that produced it do not.  `fm_timeout` was already a
# CLI argument and duly appears in the report as `fm_timeout_s`; these were
# hardcoded and appeared nowhere, so the distribution behind
# `exactlp_report_random.json` would have been unrecoverable after one more
# edit.  They are now overridable at run time AND echoed into the report.
#
# WHY THEY ARE WEIGHTED TOWARD SMALL, stated plainly because it is a bias:
# `(1, 3, 20, 200, 5000)` with uniform nv 2..15 / rows 1..40 was tried first and
# made `_fm` the bottleneck of the VALIDATION -- 6+ CPU-minutes for 300 trials
# at a 2 s timeout, because most trials landed in _fm's blowup zone.  Weighting
# toward sizes _fm can usually finish keeps a thousands-of-trials sweep
# tractable, at the cost of under-representing the tail.
#
# THIS IS NOT A MODEL OF THE WORKLOAD, and no speed claim should rest on it.
# The tail is the reason this module exists.  `phase_hard` targets it
# deliberately, and the `ckpt*` phases run the REAL decided instances, which
# need no sampling distribution at all.  Read `phase_random` as a broad
# agreement check over many cheap cases and nothing more.
SAMPLING_DEFAULT = {
    'mags': (1, 1, 3, 3, 10, 50),   # coefficient magnitudes, sampled uniformly
    'small_frac': 0.75,             # share of trials drawn from the small band
    'small_nv': (2, 8),             # small band: variables, inclusive
    'small_rows': (1, 15),          # small band: constraint rows, inclusive
    'large_nv': (9, 15),            # large band: the task's full stated range
    'large_rows': (16, 40),         # large band: rows, where _fm blows up
}


def phase_random(n_trials, seed, fm_timeout, out_path, sampling=None):
    import random, time, json
    import isolation67 as iso

    cfg = dict(SAMPLING_DEFAULT)
    cfg.update(sampling or {})
    rnd = random.Random(seed)
    mags = tuple(cfg['mags'])
    mismatches = []
    bad_witnesses = []
    old_timeouts = 0
    n_compared = 0
    n_feasible = n_infeasible = 0
    new_times, old_times, ratios = [], [], []
    t_start = time.time()
    for trial in range(n_trials):
        # Calibration measured the large band timing out at fm_timeout=0.3 s on
        # ~43% of trials by itself, dominated by nv/rows rather than magnitude
        # (even mag <= 50 sufficed). It is therefore the minority share -- see
        # SAMPLING_DEFAULT for why that bias is acceptable here and where it is
        # not.
        if rnd.random() < cfg['small_frac']:
            nv = rnd.randint(*cfg['small_nv'])
            nrows = rnd.randint(*cfg['small_rows'])
        else:
            nv = rnd.randint(*cfg['large_nv'])
            nrows = rnd.randint(*cfg['large_rows'])
        mag = rnd.choice(mags)
        rows = [_rand_row(nv, mag, rnd) for _ in range(nrows)]

        t0 = time.time()
        y_new = feasible_strict(rows, nv)
        t1 = time.time()
        new_times.append(t1 - t0)

        y_old, timed_out = _with_timeout(iso._fm_fourier_motzkin, (rows, nv), fm_timeout)
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
            n_compared += 1
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
        # The sampling distribution, echoed so this report is self-describing.
        'sampling': {k: (list(v) if isinstance(v, tuple) else v)
                     for k, v in cfg.items()},
        'n_feasible': n_feasible, 'n_infeasible': n_infeasible,
        'old_timeouts': old_timeouts,
        # n_compared, NOT n_trials, is the denominator of the agreement claim.
        # `_fm` returns no verdict when it times out, so a timed-out trial
        # yields no comparison at all. Reporting "0 mismatches in n_trials"
        # silently credits those to agreement: at fm_timeout=0.3 s on
        # 2026-08-20, 978 of 2500 trials timed out, so the honest statement was
        # 0 mismatches in 1522 comparisons, not in 2500.
        'n_compared': n_compared,
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
        _, timed_out = _with_timeout(iso._fm_fourier_motzkin, (rows, ncols), fm_timeout)
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
        _, timed_out = _with_timeout(iso._fm_fourier_motzkin, (rows, nv), fm_timeout)
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


USAGE = """exactlp.py <phase> [args] [key=value ...]

phases:
  random [n_trials] [fm_timeout_s]   broad agreement sweep (NOT a workload model)
  ckpt727 [max_check]                real decided candidates from ckpt_727/
  ckpt393                            real decided candidates from ckpt_393/
  ckpt183                            real decided candidates, the known-answer case
  hard                               the _fm tail, deliberately expensive

`random` also accepts key=value overrides of the sampling distribution; every
key of SAMPLING_DEFAULT is settable and the effective values are written into
the report. Tuples are comma-separated:

  python3 exactlp.py random 400 5.0 mags=1,3,20,200,5000 small_frac=0.0

`out=PATH` redirects the report. USE IT FOR ANY EXPLORATORY RUN: the default
path is the one a real campaign writes, and overwriting it destroys that data.

That example restores the original unweighted-toward-hard distribution, which
is the honest tail sweep; it is slow, which is why it is not the default.
Defaults are documented at SAMPLING_DEFAULT with the bias they carry."""


def _parse_overrides(args):
    """key=value CLI overrides for SAMPLING_DEFAULT. Unknown keys are refused
    rather than ignored: a silently-dropped override would be reported in the
    output as though it had been applied."""
    cfg = {}
    for a in args:
        if '=' not in a:
            raise SystemExit('not a key=value override: %r\n\n%s' % (a, USAGE))
        k, v = a.split('=', 1)
        if k not in SAMPLING_DEFAULT:
            raise SystemExit('unknown sampling key %r (known: %s)'
                             % (k, ', '.join(sorted(SAMPLING_DEFAULT))))
        parts = [x for x in v.split(',') if x != '']
        vals = [float(x) if '.' in x else int(x) for x in parts]
        cfg[k] = vals[0] if len(vals) == 1 and not isinstance(
            SAMPLING_DEFAULT[k], tuple) else tuple(vals)
    return cfg


def _assert_reference_is_fm():
    """The comparison must run against Fourier-Motzkin, NOT against whatever
    `isolation67._fm` currently dispatches to.

    After the 2026-08-20 swap `_fm` IS this module, so comparing against it
    would compare the LP with itself and agree on everything forever -- mode 2,
    a gate whose two sides are identical strings. Every phase here calls
    `_fm_fourier_motzkin` explicitly; this checks the name still means what it
    says rather than trusting that it does."""
    import isolation67 as iso
    fn = getattr(iso, '_fm_fourier_motzkin', None)
    if fn is None:
        raise SystemExit('isolation67._fm_fourier_motzkin is missing: the '
                         'independent reference implementation is gone, so '
                         'nothing here would be a comparison. Refusing to run.')
    src = fn.__doc__ or ''
    if 'exactlp' in (fn.__module__ or ''):
        raise SystemExit('the reference resolves into exactlp: self-comparison. '
                         'Refusing to run.')
    return fn


def main():
    import sys, os
    _assert_reference_is_fm()
    argv = sys.argv[1:]
    if argv and argv[0] in ('-h', '--help'):
        print(USAGE)
        return 0
    phase = argv[0] if argv else 'random'
    pos = [a for a in argv[1:] if '=' not in a]
    kv = [a for a in argv[1:] if '=' in a]
    # `out=` exists because the default path was itself an unparameterised magic
    # value, and on 2026-08-20 a 120-trial smoke test of the CLI overwrote the
    # 2500-trial report at that path. A throwaway run must be able to write
    # somewhere throwaway; without that, every test of this program endangers
    # the last result of it. Data files are immutable -- FAILURE_MODES 20.
    out = os.path.join(_here(), 'exactlp_report_%s.json' % phase)
    for a in list(kv):
        if a.startswith('out='):
            out = a[4:]
            kv.remove(a)
    if phase == 'random':
        n = int(pos[0]) if len(pos) > 0 else 2500
        fmt = float(pos[1]) if len(pos) > 1 else 0.3
        phase_random(n, seed=20260820, fm_timeout=fmt, out_path=out,
                     sampling=_parse_overrides(kv))
    elif phase == 'ckpt727':
        mc = int(pos[0]) if pos else None
        phase_ckpt727(out, max_check=mc)
    elif phase == 'ckpt393':
        phase_ckpt393(out)
    elif phase == 'ckpt183':
        phase_ckpt183(out)
    elif phase == 'hard':
        phase_hard(out)
    else:
        raise SystemExit('unknown phase %r\n\n%s' % (phase, USAGE))
    return 0


if __name__ == '__main__':
    main()
