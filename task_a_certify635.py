#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (Postscript 5) + golden_wall_report.md. Project index: README.md
"""Task (a): local-maximality certification of the 635 record under
single-component move radius 4.

For the current record quats, evaluate ALL single-component moves:
24 components (6 quats x 4 fields) x 8 deltas in {-4,-3,-2,-1,1,2,3,4},
re-gcd, skip zero-quat or |c|>512, evaluate exactly via cube_regions.
If no neighbor strictly exceeds current total, that's a certified local
max at radius 4. If one does, move there and repeat (greedy ascent),
recursing until a round with no improvement.

Logs all evaluations to hillclimb_log.jsonl (append-only, existing schema)
via the Evaluator class from phase_b_hillclimb.py (does not modify it).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from phase_b_hillclimb import canon, Evaluator, evaluate  # noqa: E402

RECORD_QUATS = [[129, -171, -137, -28], [382, 278, 63, -186],
                [200, 289, 312, -203], [314, 101, -391, 1],
                [124, -61, 26, -215], [276, 269, 33, 335]]

DELTAS = (-4, -3, -2, -1, 1, 2, 3, 4)


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
    return out


def main():
    logf = open(os.path.join(HERE, 'hillclimb_log.jsonl'), 'a')
    ev = Evaluator(8, logf, preload=os.path.join(HERE, 'hillclimb_log.jsonl'))

    cur = [list(q) for q in canon(RECORD_QUATS)]
    r0 = ev.eval_many([cur], 'taskA:start')[0]
    assert r0 is not None, 'record config degenerate?!'
    cur_total = r0['bounded']
    cur_r = r0
    print(f'start total={cur_total} by_depth={cur_r["by_depth"]}', flush=True)

    round_num = 0
    total_evals_before = ev.evals
    round_evals = []
    while True:
        round_num += 1
        nbrs = neighbors_r4(cur)
        # dedupe within round (canon may collide across (i,j,d))
        seen = set()
        uniq_nbrs = []
        for n in nbrs:
            k = tuple(tuple(q) for q in n)
            if k not in seen:
                seen.add(k)
                uniq_nbrs.append(n)
        pre_evals = ev.evals
        results = ev.eval_many(uniq_nbrs, f'taskA:round{round_num}')
        post_evals = ev.evals
        round_evals.append((round_num, len(uniq_nbrs), post_evals - pre_evals))
        print(f'round {round_num}: {len(uniq_nbrs)} candidate neighbors '
              f'(of {len(nbrs)} raw), {post_evals - pre_evals} new evals',
              flush=True)

        best_i, best_total = -1, cur_total
        for i, rr in enumerate(results):
            if rr is None:
                continue
            if rr['bounded'] > best_total:
                best_i, best_total = i, rr['bounded']

        if best_i < 0:
            print(f'round {round_num}: NO improving neighbor found. '
                  f'{cur_total} is a certified local max at radius 4.',
                  flush=True)
            break
        else:
            cur = uniq_nbrs[best_i]
            cur_r = results[best_i]
            cur_total = best_total
            print(f'round {round_num}: IMPROVEMENT found -> {cur_total} '
                  f'by_depth={cur_r["by_depth"]} quats={cur}', flush=True)

    total_evals_after = ev.evals
    print('\n=== FINAL RESULT ===')
    print(f'final total={cur_total}')
    print(f'final by_depth={cur_r["by_depth"]}')
    print(f'final quats={cur}')
    print(f'rounds={round_num}')
    print(f'per-round (round, candidates, new_evals): {round_evals}')
    print(f'total new evaluations (this script): '
          f'{total_evals_after - total_evals_before}')
    logf.close()


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
