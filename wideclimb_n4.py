#!/usr/bin/env python3
"""Aggressive wide-perturbation-escape campaign for n = 4 -- is 183 beatable?

THE LEAD (LEDGER.md Postscript 15): the current n=4 record 183 was found by
a chain of SIX basin escapes (159 -> 171 -> 173 -> 175 -> 179 -> 183), each
found by perturbing SEVERAL cubes at once and re-climbing narrowly. A 200k
random campaign only reached 137; plain +-1/+-2 greedy climbing stalls below
177. There is no principled reason the sixth escape was the last one
possible -- this campaign re-runs that technique much more aggressively,
from many independent random restarts, and reports the FULL distribution of
local maxima reached, not only the best.

Algorithm per restart (as specified):
  1. random start: cube 0 fixed at (1,0,0,0) (global rotation is gauge); the
     other 3 cubes get uniform-random integer components in [-cap, cap],
     cap drawn per restart from {2,3,4,6,9,12,20} -- MENU SHAPE matters more
     than menu size (ledger's finding), so it is varied, not fixed.
  2. narrow climb: steepest-ascent on one component of one FREE cube by
     +-1 or +-2 at a time, to a local maximum.
  3. wide escape: perturb 2 or 3 of the free cubes SIMULTANEOUSLY, each by a
     random vector with every component in +-1..+-4, then re-climb
     narrowly; accept if the new local max beats the old.
  4. repeat 3 until 15 consecutive wide escapes fail to improve; record the
     final value, its configuration, and how many escapes actually improved
     (the "chain length") before the run stalled.

Restarts run in parallel (one OS process per engine call, so N_WORKERS
independent restart loops keep all cores busy) until BUDGET_SECONDS elapses.

Engine contract: cube_regions_n refuses (returns a JSON line with no
'bounded' field, or -- degenerate case -- no parseable line at all) when a
config exceeds its |component| <= 512 overflow budget. Since every
candidate is pre-filtered by `ok()` to respect that same 512 cap, refusals
should be near-zero in practice, but they are counted separately and never
scored as a low total (an unevaluated config is not a bad one).
"""
import concurrent.futures
import json
import math
import os
import random
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BIN_N = os.path.join(HERE, 'cube_regions_n')
BIN_Q2W = os.path.join(HERE, 'cube_regions_q2w')
CAP = 512
FIXED = (1, 0, 0, 0)
RECORD = 183
RECORD_QUATS = [[1, 0, 0, 0], [0, 5, 3, 2], [1, -4, -1, 1], [1, 1, -1, -4]]

CAP_MENU = [2, 3, 4, 6, 9, 12, 20]
STALL_LIMIT = 15
N_WORKERS = 8
DEFAULT_BUDGET = 40 * 60

LOG_PATH = os.path.join(HERE, 'wideclimb_n4.log')
OUT_PATH = os.path.join(HERE, 'wideclimb_n4.json')

T0 = None
log_lock = threading.Lock()
log_fh = None


def log(msg):
    line = '[%7.1fs] %s' % (time.time() - T0, msg)
    with log_lock:
        print(line, flush=True)
        log_fh.write(line + '\n')
        log_fh.flush()


def canon(quats):
    """gcd-reduce each quaternion and fix its sign (q and -q are one rotation)."""
    out = []
    for q in quats:
        g = math.gcd(*[abs(c) for c in q])
        qq = [c // g for c in q] if g > 1 else list(q)
        for c in qq:
            if c:
                if c < 0:
                    qq = [-x for x in qq]
                break
        out.append(tuple(qq))
    return tuple(out)


def ok(quats):
    """Engine-admissible: no zero quaternion, every component within CAP."""
    return all(any(q) and all(abs(c) <= CAP for c in q) for q in canon(quats))


def fmt(quats):
    return ';'.join(','.join(str(c) for c in q) for q in quats)


class Stats:
    def __init__(self):
        self.lock = threading.Lock()
        self.histogram = {}       # final peak (per restart) -> count
        self.chain_lengths = {}   # number of improving escapes -> count
        self.refusals = 0
        self.engine_calls = 0
        self.restarts_done = 0
        self.reached_exactly_183 = 0
        self.reached_at_least_183 = 0
        self.exceeded_183 = 0
        self.best = (0, None)

    def record_restart(self, peak, cfg, chain_len):
        with self.lock:
            self.histogram[peak] = self.histogram.get(peak, 0) + 1
            self.chain_lengths[chain_len] = self.chain_lengths.get(chain_len, 0) + 1
            self.restarts_done += 1
            if peak == RECORD:
                self.reached_exactly_183 += 1
            if peak >= RECORD:
                self.reached_at_least_183 += 1
            if peak > RECORD:
                self.exceeded_183 += 1
            if peak > self.best[0]:
                self.best = (peak, [list(q) for q in cfg])

    def record_refusals(self, n):
        if n:
            with self.lock:
                self.refusals += n

    def record_calls(self, n):
        with self.lock:
            self.engine_calls += n


def engine_batch(configs, binary=BIN_N, extra_args=()):
    """Evaluate a batch of configs with ONE subprocess call.

    Returns a list of (total_or_None, by_depth, refused_bool) aligned
    index-for-index with `configs`. Any line that fails to parse as JSON, or
    parses but carries no 'bounded' field (an explicit engine refusal, e.g.
    an overflow-budget rejection), or is simply missing (alignment loss) is
    reported as refused -- never scored as a low total.
    """
    lines = [fmt(c) for c in configs]
    cmd = [binary] + list(extra_args) + ['--n', '4', '--quats-stdin']
    p = subprocess.run(cmd, input='\n'.join(lines) + '\n',
                        capture_output=True, text=True)
    rows = p.stdout.splitlines()
    out = []
    for i in range(len(configs)):
        if i < len(rows) and rows[i].startswith('{'):
            try:
                d = json.loads(rows[i])
            except json.JSONDecodeError:
                out.append((None, {}, True))
                continue
            if 'bounded' in d:
                out.append((d['bounded'], d['by_depth'], False))
            else:
                out.append((None, {}, True))
        else:
            out.append((None, {}, True))
    return out


def narrow_neighbors(cfg):
    """+-1/+-2 on one component of one of the FREE cubes (indices 1..3)."""
    out = []
    for i in range(1, len(cfg)):
        for j in range(4):
            for d in (-2, -1, 1, 2):
                c = [list(q) for q in cfg]
                c[i][j] += d
                if ok(c):
                    out.append(c)
    return out


def narrow_climb(cfg, cur_total, stats):
    """Steepest ascent to a +-1/+-2 local max. Returns (cfg, total, steps)."""
    cur = [list(q) for q in cfg]
    best = cur_total
    steps = 0
    while steps < 300:
        cand = narrow_neighbors(cur)
        if not cand:
            break
        results = engine_batch(cand)
        stats.record_calls(len(cand))
        refused = sum(1 for r in results if r[2])
        stats.record_refusals(refused)
        valid = [(r[0], c) for r, c in zip(results, cand) if not r[2]]
        if not valid:
            break
        top_total, top_cfg = max(valid, key=lambda x: x[0])
        if top_total <= best:
            break
        cur, best = top_cfg, top_total
        steps += 1
    return cur, best, steps


def wide_perturb(cfg, rng):
    """Perturb 2 or 3 of the free cubes at once, each component in +-1..4."""
    free_idx = [1, 2, 3]
    num = rng.choice([2, 3])
    chosen = rng.sample(free_idx, num)
    for _ in range(20):
        c = [list(q) for q in cfg]
        for i in chosen:
            for j in range(4):
                c[i][j] += rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        if ok(c):
            return c
    return None


def random_start(rng, cap):
    while True:
        free = []
        for _ in range(3):
            while True:
                q = tuple(rng.randint(-cap, cap) for _ in range(4))
                if any(q):
                    break
            free.append(list(q))
        cfg = [list(FIXED)] + free
        if ok(cfg):
            return cfg


def run_restart(idx, rng, stats):
    cap = rng.choice(CAP_MENU)
    cfg = random_start(rng, cap)
    r0 = engine_batch([cfg])
    stats.record_calls(1)
    if r0[0][2]:
        stats.record_refusals(1)
        log('restart %4d cap=%2d: initial config REFUSED by engine -- skipped' % (idx, cap))
        return
    cur, narrow_peak, steps0 = narrow_climb(cfg, r0[0][0], stats)
    best = narrow_peak
    chain = 0
    consec_fail = 0
    escapes = 0
    while consec_fail < STALL_LIMIT:
        cand = wide_perturb(cur, rng)
        escapes += 1
        if cand is None:
            consec_fail += 1
            continue
        r = engine_batch([cand])
        stats.record_calls(1)
        if r[0][2]:
            stats.record_refusals(1)
            consec_fail += 1
            continue
        climbed_cfg, climbed_total, _steps = narrow_climb(cand, r[0][0], stats)
        if climbed_total > best:
            cur, best = climbed_cfg, climbed_total
            chain += 1
            consec_fail = 0
        else:
            consec_fail += 1
    stats.record_restart(best, cur, chain)
    flag = ''
    if best > RECORD:
        flag = '  *** EXCEEDS RECORD 183 ***'
    elif best == RECORD:
        flag = '  (matches record 183)'
    log('restart %4d cap=%2d: narrow=%3d (%d steps) -> final peak=%3d  '
        'chain=%d escapes=%d%s'
        % (idx, cap, narrow_peak, steps0, best, chain, escapes, flag))
    # RECORD THE CONFIGURATION, not only its value.  The first run kept just the
    # single best, so when 183 turned out to be a PLATEAU (Postscript 133) the
    # other three 183-reaching configurations were already gone and the plateau's
    # size could not be measured.  Fourth instance in one day of keeping an
    # aggregate and discarding per-item data; standing rule is Postscript 127.
    if best >= RECORD - 8:
        log('CFG peak=%d %s'
            % (best, ';'.join(','.join(map(str, q)) for q in cur)))


def main():
    global T0, log_fh
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BUDGET
    T0 = time.time()
    log_fh = open(LOG_PATH, 'w')
    log('=== wideclimb_n4.py starting, budget=%ds, workers=%d ===' % (budget, N_WORKERS))

    # --- KNOWN-ANSWER GATE (mandatory, run first) ---
    r = engine_batch([RECORD_QUATS])
    if r[0][2] or r[0][0] != RECORD:
        log('GATE FAILED: got %r, expected %d -- STOPPING, no campaign run' % (r[0], RECORD))
        print('GATE FAILED -- see wideclimb_n4.log', file=sys.stderr)
        sys.exit(1)
    log('GATE PASSED: 1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4 counts %d (by_depth=%s)'
        % (r[0][0], r[0][1]))

    stats = Stats()
    deadline = T0 + budget
    seed_base = 20260818
    idx_counter = [0]
    idx_lock = threading.Lock()

    def worker_loop():
        while True:
            with idx_lock:
                if time.time() > deadline:
                    return
                idx = idx_counter[0]
                idx_counter[0] += 1
            rng = random.Random(seed_base + idx * 7919 + 104729)
            try:
                run_restart(idx, rng, stats)
            except Exception as e:
                log('restart %4d CRASHED: %r' % (idx, e))

    t_campaign = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=N_WORKERS) as ex:
        futs = [ex.submit(worker_loop) for _ in range(N_WORKERS)]
        concurrent.futures.wait(futs)
    campaign_secs = time.time() - t_campaign

    log('=== campaign done: %d restarts, %d engine calls, %d refusals, %.0fs ==='
        % (stats.restarts_done, stats.engine_calls, stats.refusals, campaign_secs))

    # --- independent re-verification if anything beat the record ---
    reverify = None
    if stats.best[0] > RECORD:
        cfg = stats.best[1]
        log('*** candidate above 183 found: %d -- re-verifying independently ***' % stats.best[0])
        rn = engine_batch([cfg], binary=BIN_N)
        rq = engine_batch([cfg], binary=BIN_Q2W, extra_args=['--d', '0'])
        log('cube_regions_n      re-check: %r' % (rn[0],))
        log('cube_regions_q2w --d0 re-check: %r' % (rq[0],))
        reverify = {
            'quats': cfg,
            'cube_regions_n': {'bounded': rn[0][0], 'by_depth': rn[0][1], 'refused': rn[0][2]},
            'cube_regions_q2w_d0': {'bounded': rq[0][0], 'by_depth': rq[0][1], 'refused': rq[0][2]},
            'agree': (not rn[0][2] and not rq[0][2] and rn[0][0] == rq[0][0]),
        }
        if reverify['agree']:
            log('*** BOTH ENGINES AGREE: %d > 183 -- NEW n=4 RECORD ***' % rn[0][0])
        else:
            log('*** ENGINES DISAGREE OR ONE REFUSED -- DO NOT CLAIM A RECORD ***')

    report = {
        'budget_seconds': budget,
        'campaign_seconds': round(campaign_secs, 1),
        'n_workers': N_WORKERS,
        'stall_limit': STALL_LIMIT,
        'cap_menu': CAP_MENU,
        'restarts_done': stats.restarts_done,
        'engine_calls': stats.engine_calls,
        'engine_refusals': stats.refusals,
        'histogram_final_peak': {str(k): v for k, v in sorted(stats.histogram.items())},
        'escape_chain_length_distribution': {str(k): v for k, v in sorted(stats.chain_lengths.items())},
        'restarts_reaching_exactly_183': stats.reached_exactly_183,
        'restarts_reaching_at_least_183': stats.reached_at_least_183,
        'restarts_exceeding_183': stats.exceeded_183,
        'best_total': stats.best[0],
        'best_quats': stats.best[1],
        'reverification': reverify,
    }
    tmp = OUT_PATH + '.tmp'
    json.dump(report, open(tmp, 'w'), indent=2)
    os.replace(tmp, OUT_PATH)
    log('wrote %s' % OUT_PATH)

    print('\n=== SUMMARY ===')
    print('restarts: %d   engine calls: %d   refusals: %d'
          % (stats.restarts_done, stats.engine_calls, stats.refusals))
    print('histogram of final local maxima:')
    for k in sorted(stats.histogram):
        print('  %4d : %d' % (k, stats.histogram[k]))
    print('escape-chain-length distribution:')
    for k in sorted(stats.chain_lengths):
        print('  chain=%2d : %d restarts' % (k, stats.chain_lengths[k]))
    print('reached exactly 183: %d   reached >=183: %d   exceeded 183: %d'
          % (stats.reached_exactly_183, stats.reached_at_least_183, stats.exceeded_183))
    print('best found: %d' % stats.best[0])
    print('best config: %s' % fmt(stats.best[1]) if stats.best[1] else 'none')
    if stats.best[0] > RECORD:
        print('*** ABOVE 183 -- see reverification block in wideclimb_n4.json ***')


if __name__ == '__main__':
    main()
