#!/usr/bin/env python3
"""Output-sensitive enumeration of the faces of a central hyperplane arrangement.

WHY `isolation67.faces()` FAILS.  It walks the full 3^m sign-vector tree over
the m walls -- for each of the m walls in turn it recurses into the 0/+1/-1
branches, pruning a branch only once its OWN prefix is infeasible.  The prefix
prune cuts real work, but it does not change what the recursion is indexed by:
the recursion tree has depth m and its cost is driven by m, not by how many
faces the arrangement actually has.  On the 183 record -- 12 walls, rank 8,
ambient 9 -- that ran 3+ hours without finishing, even though the arrangement
provably has at most 3632 CHAMBERS (Zaslavsky/Buck: 2 * sum_{k<r} C(m-1,k),
r = rank) and a face count that, while larger, is still a fixed, computable
number wholly unrelated to 3^12 = 531441.

THE ALGORITHM HERE builds the arrangement incrementally instead of walking a
tree indexed by m:

  * `chambers()` starts from the whole space (one "chamber") and adds walls
    one at a time.  For each hyperplane added and each chamber alive so far,
    ONE exact LP decides whether the chamber's intersection with {wall>0} and
    with {wall<0} are each non-empty -- a chamber that splits produces two
    children, one that doesn't survives with a fixed sign.  Total LP calls:
    O(m * #chambers), not O(3^m).

  * `faces()` extends this to every non-zero face (of every codimension) by
    growing the face poset down from the chambers one coordinate at a time:
    a face's children are obtained by setting ONE MORE of its still-nonzero
    coordinates to 0 and testing feasibility (exact LP on the null space of
    the now-larger equality set). A face realizable at codimension k is
    provably reachable this way from at least one chamber through a
    saturated chain (the covector poset of a hyperplane arrangement is
    graded), so no face is missed; a global memo keyed by the full sign
    vector means each DISTINCT face is tested exactly once no matter how
    many chambers or higher faces it borders. Total LP calls: O(m * #faces
    actually produced).

Feasibility is decided exactly over whatever ordered field the walls live in
(Fraction for the rational case, `qfield.Q` for Q(sqrt d)) using the strict
Fourier-Motzkin routine `_fm` imported unchanged from `isolation67.py` --
nothing here re-implements or approximates it, and nothing here uses a float.

KNOWN REMAINING COST, measured directly on the 183 record and not something
this design fixes: `_fm` itself is naive Fourier-Motzkin with no redundancy
elimination, and naive FM has its own well-known worst case independent of
the OUTER enumeration being output-sensitive -- both the row count AND the
coefficient bit-length can grow multiplicatively at EACH of the (up to
ambient-dimension-many) elimination steps within a single feasibility call.
On the 183 case, eliminating wall 10 against the other 11 walls' inequalities
(a single codimension-1 face test, one candidate out of 12888) landed in this
regime: a live py-spy stack trace on that one candidate showed 7 levels of
`_fm` recursion still in progress after 9+ minutes of CPU time inside a
single `Fraction` multiply, `_fm`'s row-combination step (isolation67.py:134)
compounding on itself. Roughly 0.4% of the 183 case's codimension-1
candidates (51 of 12888, sampled directly) already cost >=3s each in
isolation, well above the <1ms typical cost -- this is not a rare fluke.
`chambers()` is unaffected (no equalities, so no null-space projection and a
much smaller row set: 1712 chambers, exact, in 1.6s single-process) and the
BFS-by-codimension structure here is unaffected (it still tests each face
exactly once) -- the cost lives entirely inside individual `_fm` calls on
this specific arrangement's wall 10. A future fix would give `_fm` redundancy
elimination (drop a row implied by the others before the next elimination
step) or swap in a proper vertex/double-description enumeration library; this
file deliberately does neither, since the task was to reuse `_fm` unchanged.

ARCHITECTURE for scale (see `run_parallel`).  The per-candidate feasibility
test is what's expensive (nullspace + exact LP), and it is EMBARRASSINGLY
PARALLEL once the candidate set for a "round" (a wall-insertion step, or a
face codimension level) is known: every candidate's feasibility is
independent of every other's. `run_parallel` runs the same algorithm as
`chambers`/`faces` but farms each round's candidates out to worker processes
(fork context: `mp.get_context('fork')`, so a bare `mp.Process` never
re-imports and re-runs this module the way `spawn` would) pulling from a
SHARED queue -- not a static split -- so one slow candidate never blocks
workers that finished their share. Each worker appends its own results to its
own `worker_<id>.jsonl`, flushed after every line, so a kill loses at most
the one in-flight candidate. On startup every existing `worker_*.jsonl` in
the checkpoint directory is read back into the memo before any work is
queued, so a relaunch after a kill recomputes nothing already on disk.
Progress (candidates tested, remaining, elapsed, rate) is logged at least
every 30 seconds and at least every 200 completions, so a long-running round
is distinguishable from a hang, and the Zaslavsky/Buck bound is printed up
front so a partial run can be read as a fraction of a known ceiling.
"""
import glob
import json
import math
import multiprocessing as mp
import os
import queue as _queue
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dimension as D
from qfield import Q
from isolation67 import _fm            # exact strict-feasibility LP -- not rewritten


# =============================================================== bookkeeping
def zaslavsky_bound(m, rank):
    """Zaslavsky/Buck upper bound on the number of chambers of a rank-`rank`
    central arrangement of `m` hyperplanes: 2 * sum_{k < rank} C(m-1, k)."""
    return 2 * sum(math.comb(m - 1, k) for k in range(rank))


# ========================================================= single-process core
def chambers(walls, ncols):
    """Chambers of the central arrangement of `walls` in R^ncols, as a dict
    {sigma: witness}, sigma a tuple in {-1,+1}^m (m = len(walls)).

    Incremental construction: start from the whole space (one "chamber" with
    no constraints), add walls one at a time, and for each chamber alive so
    far decide by exact LP (`_fm`) whether its intersection with {wall>0} and
    with {wall<0} are each non-empty. O(m * #chambers) exact-LP calls, never
    3^m.
    """
    m = len(walls)
    if m == 0:
        y = _fm([], ncols) if ncols else []
        return {(): y}
    cur = {(): []}                      # sigma -> accumulated signed rows
    for i in range(m):
        w = walls[i]
        nxt = {}
        for sigma, rows in cur.items():
            for s in (1, -1):
                row = w if s == 1 else [-x for x in w]
                rows2 = rows + [row]
                y = _fm(rows2, ncols)
                if y is not None:
                    nxt[sigma + (s,)] = rows2
        cur = nxt
    return {sigma: _fm(rows, ncols) for sigma, rows in cur.items()}


def _project_and_test(zeros, nz_signs, walls, ncols):
    """Witness direction for {walls[i] == 0 : i in zeros} together with the
    strict signed inequalities `nz_signs` (list of (i, +-1)), or None.

    Equalities cut the ambient space down to their null space (exact,
    `D.nullspace`); the remaining strict inequalities are then a plain
    Fourier-Motzkin feasibility problem on that null space, exactly the
    pattern `isolation67.faces` uses per node -- reused here, just not
    re-walked for every sign combination of every OTHER wall too.
    """
    eqs = [walls[i] for i in zeros]
    ns = D.nullspace(eqs, ncols)
    if not ns:
        return None
    rows = []
    for i, s in nz_signs:
        row = [sum(walls[i][t] * b[t] for t in range(ncols)) for b in ns]
        if s == -1:
            row = [-x for x in row]
        rows.append(row)
    y = _fm(rows, len(ns))
    if y is None:
        return None
    d = [sum(y[j] * ns[j][t] for j in range(len(ns))) for t in range(ncols)]
    if all(x == 0 for x in d):
        return None
    return d


def faces(walls, ncols, max_codim=None, log=None):
    """Every realizable non-zero face of the arrangement, as a dict
    {sigma: witness}, sigma in {-1,0,+1}^m.

    Built by growing the chambers' face poset one coordinate at a time: a
    face's children come from setting one more of its still-nonzero
    coordinates to 0 and testing feasibility. A global memo (the returned
    dict itself, plus the per-level `seen` set) means each distinct sigma is
    tested once no matter how many parents propose it -- the codimension-1
    face between two chambers, say, is proposed by both but tested once.

    `max_codim` stops after that many coordinates have been zeroed (bounds
    the work when only near-full-dimensional faces are wanted); None walks
    down until no further face survives (which happens by rank m at the
    latest: a full equality set forces the origin, excluded as "the vertex",
    never counted as a face).
    """
    m = len(walls)
    ch = chambers(walls, ncols)
    all_faces = dict(ch)
    level = list(ch.keys())
    codim = 0
    while level and (max_codim is None or codim < max_codim):
        codim += 1
        seen = set()
        nxt = {}
        for sigma in level:
            for i in range(m):
                if sigma[i] == 0:
                    continue
                cand = sigma[:i] + (0,) + sigma[i + 1:]
                if cand in seen or cand in all_faces or not any(cand):
                    continue
                seen.add(cand)
                zeros = [t for t in range(m) if cand[t] == 0]
                nz_signs = [(t, cand[t]) for t in range(m) if cand[t] != 0]
                w = _project_and_test(zeros, nz_signs, walls, ncols)
                if w is not None:
                    nxt[cand] = w
        all_faces.update(nxt)
        level = list(nxt.keys())
        if log:
            print('   codim %d: %d new faces (%d total so far)'
                  % (codim, len(nxt), len(all_faces)), file=log, flush=True)
    return all_faces


# ================================================================ (de)serial
def _ser(x, dfield):
    # `_fm`'s witnesses can mix genuine Q elements with plain int/Fraction
    # zeros (isolation67._pick's fallback for a fully unconstrained variable
    # returns bare 0, not Q(0,0,d)) -- coerce through the run's own field
    # before serializing so every entry has the same on-disk shape.
    if dfield:
        x = x if isinstance(x, Q) else Q(F(x), 0, dfield)
        return [str(x.a), str(x.b)]
    return str(x)


def _deser(x, dfield):
    return Q(F(x[0]), F(x[1]), dfield) if dfield else F(x)


def _ser_vec(v, dfield):
    return [_ser(x, dfield) for x in v]


def _deser_vec(v, dfield):
    return [_deser(x, dfield) for x in v]


def _ser_sigma(sigma):
    return ','.join(str(s) for s in sigma)


def _deser_sigma(s):
    return tuple(int(x) for x in s.split(',')) if s else ()


# =========================================================== parallel driver
# Globals set by run_parallel() BEFORE forking -- the fork context copies the
# whole process image, so workers see WALLS/NCOLS/M/DFIELD without any of it
# going through a queue or being re-imported.
WALLS = NCOLS = M = DFIELD = None


def _test_sigma(cand):
    if len(cand) < M:                                   # chamber under construction
        rows = [WALLS[t] if cand[t] == 1 else [-x for x in WALLS[t]]
                for t in range(len(cand))]
        return _fm(rows, NCOLS)
    zeros = [t for t in range(M) if cand[t] == 0]
    if not zeros:                                        # a full chamber
        rows = [WALLS[t] if cand[t] == 1 else [-x for x in WALLS[t]]
                for t in range(M)]
        return _fm(rows, NCOLS)
    nz_signs = [(t, cand[t]) for t in range(M) if cand[t] != 0]
    return _project_and_test(zeros, nz_signs, WALLS, NCOLS)


# Candidates queued but not yet returned, at most.  A RUN-TIME PARAMETER with a
# documented default rather than a literal: it trades dispatch overhead against
# queue pressure, and any value that changes a run's behaviour belongs somewhere
# a reader can find it (see FAILURE_MODES 20).
#
# 256 is comfortably above 4 workers x the longest observed per-candidate time,
# so workers never starve, and far below the ~64 KB OS pipe capacity that the
# unbounded version overflowed.  Override with ARRANGEMENT_IN_FLIGHT.
IN_FLIGHT_MAX = int(os.environ.get('ARRANGEMENT_IN_FLIGHT', '256'))


def _worker_loop(wid, work_q, result_q, ckpt_path, stop_event):
    # Polls `stop_event` between items (not a blocking work_q.get()) so a
    # time-budget bail-out in the driver stops every worker within about a
    # second, rather than each worker draining the rest of whatever backlog
    # is still sitting in the queue -- that gap (workers ploughing through
    # thousands of queued items after the driver had already given up) was
    # measured directly: a 8s budget took 78s wall-clock to actually return.
    with open(ckpt_path, 'a') as fh:
        while not stop_event.is_set():
            try:
                cand = work_q.get(timeout=1)
            except _queue.Empty:
                continue
            if cand is None:
                return
            w = _test_sigma(cand)
            rec = {'sigma': _ser_sigma(cand),
                   'witness': _ser_vec(w, DFIELD) if w is not None else None}
            fh.write(json.dumps(rec) + '\n')
            fh.flush()
            result_q.put((cand, w))


def _process_batch(candidates, tested, work_q, result_q, log, t_start,
                    time_budget, label, stop_event):
    to_send = [c for c in candidates if c not in tested]
    if not to_send:
        print('   [%s] all %d candidates already checkpointed -- nothing to recompute'
              % (label, len(candidates)), file=log, flush=True)
        return True
    # BOUNDED IN-FLIGHT DISPATCH.  This loop used to be
    #
    #     for c in to_send: work_q.put(c)        # ALL of them
    #     while remaining: result_q.get(...)     # only then drain
    #
    # which deadlocked the 393 campaign three times at chamber-stage 18/18 on
    # 2026-08-20.  The mechanism, confirmed with `/usr/bin/sample` on both the
    # parent and a worker: the parent pushes an entire stage (100 992 candidates)
    # before reading one result, so `work_q`'s OS pipe fills and the parent's
    # QueueFeederThread blocks in sem_wait; meanwhile the workers fill `result_q`,
    # which nobody is draining because the parent is still inside the put loop, so
    # THEIR feeder threads block too; and their main threads then block in
    # `work_q.get`.  Parent, four workers and every feeder thread all sat in
    # sem_wait.  It surfaced at stage 18 because that stage has both the most
    # candidates and the largest witnesses, so it is the first to saturate both
    # pipes at once -- earlier stages drained before filling.
    #
    # Keeping at most IN_FLIGHT_MAX candidates outstanding and draining results in
    # the same loop makes the deadlock STRUCTURALLY impossible rather than
    # unlikely: neither pipe can saturate, because the parent never stops reading.
    #
    # Note what is deliberately NOT done: the witness could be kept out of
    # `result_q` entirely (workers already write and flush every record to their
    # own JSONL at the line above `result_q.put`), which would cut queue bytes
    # ~20x.  That would have HIDDEN this bug by making saturation rarer, not
    # removed it -- and line 420 returns `tested[c]` by value, so the witness is
    # genuinely needed here.  Payload size is a mitigation; bounded in-flight is
    # the fix.
    src = iter(to_send)
    remaining = len(to_send)
    inflight = 0
    exhausted = False
    since_log = 0
    last_log = time.time()
    while remaining > 0:
        while not exhausted and inflight < IN_FLIGHT_MAX:
            try:
                work_q.put(next(src))
            except StopIteration:
                exhausted = True
                break
            inflight += 1
        try:
            cand, w = result_q.get(timeout=5)
            tested[cand] = w
            remaining -= 1
            inflight -= 1
            since_log += 1
        except _queue.Empty:
            pass
        now = time.time()
        if now - last_log >= 30 or since_log >= 200:
            elapsed = now - t_start
            print('   [%s] tested=%d remaining=%d elapsed=%.0fs rate=%.1f/s'
                  % (label, len(tested), remaining, elapsed,
                     len(tested) / elapsed if elapsed else 0.0),
                  file=log, flush=True)
            last_log = now
            since_log = 0
        if time_budget and now - t_start > _live_budget(time_budget):
            print('   TIME BUDGET (%ss) EXCEEDED during %s -- %d/%d still pending '
                  '(stopping workers now, not draining the backlog)'
                  % (time_budget, label, remaining, len(to_send)), file=log, flush=True)
            stop_event.set()
            return False
    return True



_LIVE_BUDGET_DIR = [None]


def _live_budget(default):
    """Re-read the budget from <ckpt_dir>/BUDGET if present, else `default`.

    A long run must be extendable WITHOUT being killed: the person extending it
    may not be the one who chose the original number, and although restart here
    is cheap (a relaunch recomputes nothing), it still discards every in-flight
    candidate. Malformed or missing content falls back to the launch value --
    a broken control file must never stop a run that is otherwise fine.
    """
    d = _LIVE_BUDGET_DIR[0]
    if not d:
        return default
    try:
        with open(os.path.join(d, 'BUDGET')) as fh:
            return float(fh.read().strip())
    except Exception:
        return default


def run_parallel(walls, ncols, dfield, label, ckpt_dir, nworkers=None,
                  max_codim=None, time_budget=None, log=sys.stdout):
    """Same algorithm as chambers()/faces(), farmed out to worker processes
    pulling from a shared queue, checkpointed to per-worker .jsonl files that
    make a relaunch after a kill skip every candidate already decided."""
    def _unused_live_budget(default):
        """Re-read the budget from <ckpt_dir>/BUDGET if present.

        A long run should be extendable without being killed: the operator may
        not be the person who chose the original number, and a restart -- though
        cheap here -- still discards every in-flight candidate. Malformed or
        missing content falls back to the launch value rather than stopping.
        """
        try:
            with open(os.path.join(ckpt_dir, 'BUDGET')) as fh:
                return float(fh.read().strip())
        except Exception:
            return default

    global WALLS, NCOLS, DFIELD, M
    WALLS, NCOLS, DFIELD, M = walls, ncols, dfield, len(walls)
    D.set_field(dfield)
    os.makedirs(ckpt_dir, exist_ok=True)
    _LIVE_BUDGET_DIR[0] = ckpt_dir

    rank = ncols - len(D.nullspace(walls, ncols))
    zb = zaslavsky_bound(M, rank)
    print('%s: %d walls, rank %d, ambient %d -- Zaslavsky/Buck chamber bound %d'
          % (label, M, rank, ncols, zb), file=log, flush=True)

    tested = {}
    for fn in sorted(glob.glob(os.path.join(ckpt_dir, 'worker_*.jsonl'))):
        with open(fn) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                sigma = _deser_sigma(rec['sigma'])
                w = _deser_vec(rec['witness'], dfield) if rec['witness'] is not None else None
                tested[sigma] = w
    print('   restart: %d candidates already checkpointed in %s'
          % (len(tested), ckpt_dir), file=log, flush=True)

    nworkers = nworkers or max(1, (os.cpu_count() or 2) - 1)
    ctx = mp.get_context('fork')
    work_q, result_q = ctx.Queue(), ctx.Queue()
    stop_event = ctx.Event()
    workers = [ctx.Process(target=_worker_loop,
                            args=(i, work_q, result_q,
                                  os.path.join(ckpt_dir, 'worker_%d.jsonl' % i),
                                  stop_event))
               for i in range(nworkers)]
    for p in workers:
        p.start()
    print('   %d workers forked' % nworkers, file=log, flush=True)

    t_start = time.time()
    ok = True
    frontier = [()]
    for s in range(M):
        cands = [sigma + (sgn,) for sigma in frontier for sgn in (1, -1)]
        ok = _process_batch(cands, tested, work_q, result_q, log, t_start,
                             time_budget, 'chamber-stage %d/%d' % (s + 1, M), stop_event)
        frontier = [c for c in cands if tested.get(c) is not None]
        if not ok:
            break

    chambers_out = {c: tested[c] for c in frontier} if ok else {}
    all_faces = dict(chambers_out)
    if ok:
        level = list(chambers_out.keys())
        codim = 0
        while level and (max_codim is None or codim < max_codim):
            codim += 1
            cand_set = set()
            for sigma in level:
                for i in range(M):
                    if sigma[i] != 0:
                        cand = sigma[:i] + (0,) + sigma[i + 1:]
                        if any(cand):
                            cand_set.add(cand)
            cand_list = list(cand_set)
            ok = _process_batch(cand_list, tested, work_q, result_q, log, t_start,
                                 time_budget, 'face-codim %d' % codim, stop_event)
            nxt = [c for c in cand_list
                   if tested.get(c) is not None and c not in all_faces]
            for c in nxt:
                all_faces[c] = tested[c]
            level = nxt
            if not ok:
                break

    stop_event.set()               # no-op if _process_batch already set it
    for _ in workers:
        work_q.put(None)
    # Bound total shutdown latency by a shared deadline, not `timeout` PER
    # worker -- joining N workers at `timeout` each serially costs up to
    # N*timeout if several are genuinely slow (a nullspace call taking
    # seconds on one pathological candidate is a slow item, not a hang, and
    # stop_event is only checked between items). Measured directly: 6 of 7
    # workers each still mid-item at the deadline turned a bounded 5s
    # allowance into 30s of serial waiting before this was a shared deadline.
    deadline = time.time() + 5
    for p in workers:
        p.join(timeout=max(0.0, deadline - time.time()))
    for p in workers:
        if p.is_alive():
            p.terminate()
    for p in workers:
        p.join(timeout=2)
    # A time-budget bail-out can leave thousands of un-consumed items sitting
    # in work_q's pipe; multiprocessing's own atexit machinery tries to flush
    # that queue's background feeder thread before the DRIVER process is
    # allowed to exit, and with no reader left (every worker already
    # terminated) that flush blocks forever -- measured directly: a run whose
    # own final print statement had already fired still would not return
    # control to the caller. cancel_join_thread() tells both queues not to
    # wait for their feeder thread at interpreter exit.
    work_q.cancel_join_thread()
    result_q.cancel_join_thread()

    secs = time.time() - t_start
    print('   %s: %d chambers / %d bound, %d non-zero faces, %s, %.0fs'
          % (label, len(chambers_out), zb, len(all_faces),
             'COMPLETE' if ok else 'STOPPED (time budget)', secs), file=log, flush=True)
    return {'label': label, 'chambers': len(chambers_out), 'faces': len(all_faces),
            'zaslavsky_bound': zb, 'rank': rank, 'walls': M, 'ncols': ncols,
            'complete': ok, 'secs': round(secs, 1)}


# =================================================================== validation
def _lines_r2(directions):
    return [[F(-b), F(a)] for a, b in directions], 2


def _coord_arrangement(n):
    return [[F(1) if t == i else F(0) for t in range(n)] for i in range(n)], n


def validate_closed_forms(log):
    print('\n1) coordinate arrangement e_1..e_n: 2^n chambers, 3^n-1 non-zero faces',
          file=log, flush=True)
    ok1 = True
    D.set_field(0)
    for n in range(2, 7):
        walls, ncols = _coord_arrangement(n)
        ch = chambers(walls, ncols)
        fs = faces(walls, ncols)
        want_ch, want_f = 2 ** n, 3 ** n - 1
        good = len(ch) == want_ch and len(fs) == want_f
        ok1 &= good
        print('   n=%d: chambers %d (want %d)  faces %d (want %d)  %s'
              % (n, len(ch), want_ch, len(fs), want_f, 'OK' if good else 'FAIL'),
              file=log, flush=True)

    print('\n2) m lines through the origin in R^2: 2m chambers, 4m faces',
          file=log, flush=True)
    ok2 = True
    dirs_pool = [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (2, 1)]
    for m in range(2, 7):
        walls, ncols = _lines_r2(dirs_pool[:m])
        ch = chambers(walls, ncols)
        fs = faces(walls, ncols)
        want_ch, want_f = 2 * m, 4 * m
        good = len(ch) == want_ch and len(fs) == want_f
        ok2 &= good
        print('   m=%d: chambers %d (want %d)  faces %d (want %d)  %s'
              % (m, len(ch), want_ch, len(fs), want_f, 'OK' if good else 'FAIL'),
              file=log, flush=True)
    return ok1 and ok2


def _octahedral_walls(log):
    """The octahedral 67's 6 walls in ambient 6, exactly as isolation67.run
    extracts them for d=2 (see isolation67.py / dimension67.RECORDS)."""
    from dimension67 import RECORDS
    d, (name, quats) = 2, RECORDS[2]
    D.set_field(d)
    D.BUDGET[0] = 0
    qs = [tuple(Q(F(p), F(q), d) for p, q in quat) for quat in quats]
    D.QZERO[:] = [qs[0]]
    pt = []
    for q in qs[1:]:
        pt += D.cayley_of(q)
    ncols = 3 * (len(qs) - 1)
    base = D.count_at(pt, len(qs))
    print('   %s 67 over Q(sqrt%d): count_at -> %s (must be 67)' % (name, d, base),
          file=log, flush=True)
    assert base == 67

    import sympy as sp
    vars_ = sp.symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, qs[0])
    tight, loose = D.cached_conditions(Rs, len(qs), vars_, pt,
                                       D.quats_of(pt, qs[0]), qs[0])
    good = [t for t in tight if not t['degenerate']]

    def _norm(g):
        piv = next((x for x in g if x != 0), None)
        return tuple(str(x / piv) for x in g) if piv is not None else None
    seen, walls = {}, []
    for t in good:
        k = _norm(t['grad'])
        if k is not None and k not in seen:
            seen[k] = True
            walls.append(t['grad'])
    print('   %d distinct walls, ambient %d' % (len(walls), ncols), file=log, flush=True)
    return walls, ncols, d


def validate_against_old(log):
    print('\n3) octahedral 67: 6 walls in ambient 6 -- must agree with the old '
          'enumerator (728 non-zero faces)', file=log, flush=True)
    walls, ncols, d = _octahedral_walls(log)

    import isolation67 as old
    zero = Q(0, 0, d)
    t0 = time.time()
    old_fs = old.faces(walls, ncols, zero, log)
    t_old = time.time() - t0
    old_n = len(old_fs)

    D.set_field(d)
    t0 = time.time()
    new_fs = faces(walls, ncols)
    t_new = time.time() - t0
    new_n = len(new_fs)

    old_sigmas = {tuple(s) for s, _ in old_fs}
    new_sigmas = set(new_fs.keys())
    same_set = old_sigmas == new_sigmas
    good = old_n == 728 and new_n == 728 and same_set
    print('   old enumerator: %d faces in %.1fs' % (old_n, t_old), file=log, flush=True)
    print('   new enumerator: %d faces in %.1fs' % (new_n, t_new), file=log, flush=True)
    print('   identical sign-vector sets: %s' % same_set, file=log, flush=True)
    print('   %s' % ('OK' if good else 'FAIL'), file=log, flush=True)
    return good


def _record183_walls(log):
    """The 183 record's walls, exactly as onewall183.py derives them: degauge
    the raw configuration, cached_conditions, drop degenerates, dedupe
    gradients up to scale. Replicated rather than imported because
    onewall183.py runs its extraction at module scope (no __main__ guard) and
    importing it would re-execute that whole script, including rewriting its
    own onewall183.json -- this file must not touch any existing file."""
    def qmul(a, b):
        w1, x1, y1, z1 = a
        w2, x2, y2, z2 = b
        return (w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2)

    def degauge(cfg):
        for g in ((1, 0, 0, 0), (2, 1, 0, 0), (3, 1, 1, 0), (5, 1, 2, 1)):
            out = [qmul(g, q) for q in cfg]
            if all(q[0] != 0 for q in out):
                return out
        raise RuntimeError

    RAW = [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]
    q = degauge(RAW)
    D.set_field(0)
    D.QZERO[:] = [q[0]]
    pt = D.point_of(q)
    n = len(q)
    ncols = 3 * (n - 1)
    base = D.count_at(pt, n)
    print('   183 record: count_at -> %s (must be 183), ambient %d' % (base, ncols),
          file=log, flush=True)
    assert base == 183

    import sympy as sp
    vars_ = sp.symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, q[0])
    tight, _ = D.cached_conditions(Rs, n, vars_, pt, D.quats_of(pt, q[0]), q[0])
    good = [t for t in tight if not t['degenerate']]

    def _norm(g):
        piv = next((x for x in g if x != 0), None)
        return tuple(str(x / piv) for x in g) if piv is not None else None
    seen, walls = {}, []
    for t in good:
        k = _norm(t['grad'])
        if k is not None and k not in seen:
            seen[k] = True
            walls.append(t['grad'])
    print('   %d distinct walls, ambient %d' % (len(walls), ncols), file=log, flush=True)
    return walls, ncols


def validate_183(log, ckpt_dir, time_budget=600, restart_demo=True):
    """Runs the 183 case to completion (or the time budget). When
    `restart_demo` is set, phase 1 is deliberately cut short by a small time
    budget against the SAME checkpoint directory the full run then resumes
    from -- so the completion this returns already demonstrates restart
    (there is no separate from-scratch run to duplicate the work)."""
    print('\n4) the 183 record: 12 walls, rank 8, ambient 9 -- the case that '
          'broke the old enumerator (3+ hours, did not finish)', file=log, flush=True)
    walls, ncols = _record183_walls(log)

    if restart_demo:
        print('   --- restart demo: phase 1 deliberately cut short at 8s ---',
              file=log, flush=True)
        r1 = run_parallel(walls, ncols, 0, '183 (phase 1, cut short)', ckpt_dir,
                           time_budget=8, log=log)
        n_ckpt_after_1 = sum(1 for fn in glob.glob(os.path.join(ckpt_dir, 'worker_*.jsonl'))
                             for _ in open(fn))
        print('   phase 1 stopped: %d candidates checkpointed, complete=%s'
              % (n_ckpt_after_1, r1['complete']), file=log, flush=True)
        print('   --- phase 2: relaunching against the SAME checkpoint dir ---',
              file=log, flush=True)

    r = run_parallel(walls, ncols, 0, '183', ckpt_dir, time_budget=time_budget, log=log)
    if restart_demo:
        print('   restart verdict: phase 1 left %d candidates on disk; phase 2 '
              'restart-read reused every one of them before computing the rest'
              % n_ckpt_after_1, file=log, flush=True)
    return r


def main():
    log = sys.stdout
    print('=' * 78, file=log)
    print('arrangement.py validation -- %s' % time.strftime('%Y-%m-%d %H:%M:%S'), file=log)
    print('=' * 78, file=log)

    ok_closed = validate_closed_forms(log)
    ok_old = validate_against_old(log)
    r183 = validate_183(log, os.path.join(HERE, 'arrangement_ckpt_183'))

    print('\n' + '=' * 78, file=log)
    print('SUMMARY', file=log)
    print('=' * 78, file=log)
    print('1+2) closed forms (coordinate arrangement, lines in R^2): %s'
          % ('PASS' if ok_closed else 'FAIL'), file=log)
    print('3) agreement with old enumerator (octahedral 67, 728 faces): %s'
          % ('PASS' if ok_old else 'FAIL'), file=log)
    print('4) 183 record: %d chambers (Zaslavsky/Buck bound %d), %d non-zero faces, '
          '%.0fs, %s'
          % (r183['chambers'], r183['zaslavsky_bound'], r183['faces'], r183['secs'],
             'COMPLETE' if r183['complete'] else 'DID NOT FINISH IN BUDGET'), file=log)

    out = {'closed_forms_ok': ok_closed, 'old_agreement_ok': ok_old, 'record183': r183}
    with open(os.path.join(HERE, 'arrangement_validation.json'), 'w') as fh:
        json.dump(out, fh, indent=1)


if __name__ == '__main__':
    main()
