#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (Postscript 5). Project index: README.md
"""Task (c): deeper hill-climbing, move radius up to +-4.

Gathers the top-50 configs by `bounded` from ALL exact logs:
  - campaign_results.jsonl (has quats directly)
  - hillclimb_log.jsonl (has quats directly; extends scan_records()'s
    logic to also read this file, deduping by canon(quats) not by seed)
  - exact_search_results.jsonl (read-only; only has 'seed', so quats are
    resolved via sim_quats_for_seed() lazily, only for entries that make
    the top-50 cut)

From each of the 50 starting configs, runs a greedy hill climb using
neighbors_r4() (radius 4, deltas in {-4,...,-1,1,...,4}) on the `total`
objective until no improving move exists or an iteration cap is hit.
Every evaluation (not just improving ones) is logged via the Evaluator
class from phase_b_hillclimb.py to hillclimb_log.jsonl (append, memoized
dedup via preload).
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from phase_b_hillclimb import (canon, Evaluator, sim_quats_for_seed)  # noqa: E402

DELTAS = (-4, -3, -2, -1, 1, 2, 3, 4)
TOPK = 50
MAX_ITERS = 150


def neighbors_r4(quats):
    out = []
    for i in range(6):
        for j in range(4):
            for d in DELTAS:
                q = [list(x) for x in quats]
                q[i][j] += d
                if all(c == 0 for c in q[i]):
                    continue
                cq = canon(q)
                if any(abs(c) > 512 for qq in cq for c in qq):
                    continue
                out.append([list(x) for x in cq])
    # dedupe within neighbor set
    seen = set()
    uniq = []
    for n in out:
        k = tuple(tuple(q) for q in n)
        if k not in seen:
            seen.add(k)
            uniq.append(n)
    return uniq


def gather_top50():
    """Return list of (bounded, quats) for the top-50 distinct (by canon)
    configs across campaign_results.jsonl, hillclimb_log.jsonl, and
    exact_search_results.jsonl (seed-only -> quats resolved lazily)."""
    best_by_canon = {}  # canon key -> (bounded, quats)

    def consider(bounded, quats):
        k = canon(quats)
        cur = best_by_canon.get(k)
        if cur is None or bounded > cur[0]:
            best_by_canon[k] = (bounded, [list(q) for q in k])

    # 1) campaign_results.jsonl -- has quats directly
    p = os.path.join(HERE, 'campaign_results.jsonl')
    with open(p) as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'bounded' in r and 'quats' in r:
                consider(r['bounded'], r['quats'])

    # 2) hillclimb_log.jsonl -- has quats directly; skip error/degenerate
    p = os.path.join(HERE, 'hillclimb_log.jsonl')
    with open(p) as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'bounded' in r and 'quats' in r:
                consider(r['bounded'], r['quats'])

    # 3) exact_search_results.jsonl -- seed-only; find candidate seeds
    #    that could plausibly enter the top 50 by bounded value, then
    #    resolve their quats via sim_quats_for_seed (subprocess call),
    #    only for those that actually make the cut after merging.
    p = os.path.join(HERE, 'exact_search_results.jsonl')
    seed_bounded = []  # (bounded, seed)
    with open(p) as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'bounded' in r and 'seed' in r:
                seed_bounded.append((r['bounded'], r['seed']))
    # current threshold: the TOPK-th best bounded value among what we have
    # so far (from files 1+2); only resolve exact_search seeds that could
    # beat that (or all, if fewer than TOPK entries so far).
    def current_threshold():
        vals = sorted((b for b, _ in best_by_canon.values()), reverse=True)
        if len(vals) < TOPK:
            return -1  # resolve everything, we don't have enough yet
        return vals[TOPK - 1]

    seed_bounded.sort(key=lambda t: -t[0])
    resolved = 0
    for bounded, seed in seed_bounded:
        thr = current_threshold()
        if bounded < thr and len(best_by_canon) >= TOPK:
            break  # sorted descending; no further seed can beat threshold
        quats, _ = sim_quats_for_seed(seed)
        resolved += 1
        consider(bounded, quats)
    print(f'resolved {resolved} exact_search_results seeds to quats '
          f'(of {len(seed_bounded)} total)', flush=True)

    ranked = sorted(best_by_canon.values(), key=lambda t: -t[0])
    return ranked[:TOPK]


def climb_r4(ev, start_quats, tag, max_iters=MAX_ITERS):
    cur = [list(q) for q in canon(start_quats)]
    r = ev.eval_many([cur], tag + ':start')[0]
    if r is None:
        return None, None, 'degenerate-start', 0
    cur_total = r['bounded']
    cur_r = r
    it = 0
    hit_cap = False
    while it < max_iters:
        it += 1
        nbrs = neighbors_r4(cur)
        results = ev.eval_many(nbrs, tag + f':it{it}')
        best_i, best_total = -1, cur_total
        for i, rr in enumerate(results):
            if rr is None:
                continue
            if rr['bounded'] > best_total:
                best_i, best_total = i, rr['bounded']
        if best_i < 0:
            return cur, cur_r, 'local_max', it
        cur = nbrs[best_i]
        cur_r = results[best_i]
        cur_total = best_total
    hit_cap = True
    return cur, cur_r, 'iter_cap', it


def main():
    print('gathering top-50 starting configs...', flush=True)
    top50 = gather_top50()
    print(f'got {len(top50)} distinct starts, best={top50[0][0]}, '
          f'50th={top50[-1][0]}', flush=True)
    for i, (b, q) in enumerate(top50):
        print(f'  start {i}: bounded={b} quats={q}', flush=True)

    logf = open(os.path.join(HERE, 'hillclimb_log.jsonl'), 'a')
    ev = Evaluator(8, logf, preload=os.path.join(HERE, 'hillclimb_log.jsonl'))
    evals_before = ev.evals

    results_summary = []
    best_overall = (-1, None, None)
    n_local_max = 0
    n_iter_cap = 0
    n_degenerate = 0

    for i, (b0, q0) in enumerate(top50):
        tag = f'taskC:start{i}'
        print(f'== climb {i}/{len(top50)} (start bounded={b0}) ==', flush=True)
        cur, cur_r, status, iters = climb_r4(ev, q0, tag)
        if status == 'degenerate-start':
            n_degenerate += 1
            print(f'  start {i}: degenerate, skipped', flush=True)
            continue
        if status == 'local_max':
            n_local_max += 1
        else:
            n_iter_cap += 1
        final_total = cur_r['bounded']
        print(f'  start {i}: {status} after {iters} iters, '
              f'final total={final_total} '
              f'by_depth={cur_r["by_depth"]}', flush=True)
        results_summary.append((i, b0, final_total, status, iters))
        if final_total > best_overall[0]:
            best_overall = (final_total, cur, cur_r)

    evals_after = ev.evals
    print('\n=== TASK C SUMMARY ===')
    print(f'climbs run: {len(top50)}; local_max={n_local_max} '
          f'iter_cap={n_iter_cap} degenerate={n_degenerate}')
    print(f'total NEW evaluations logged: {evals_after - evals_before}')
    print(f'best total found: {best_overall[0]}')
    if best_overall[1] is not None:
        print(f'best quats: {best_overall[1]}')
        print(f'best by_depth: {best_overall[2]["by_depth"]}')
    print('\nper-climb results (idx, start_bounded, final_total, status, iters):')
    for row in results_summary:
        print(' ', row)
    logf.close()


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
