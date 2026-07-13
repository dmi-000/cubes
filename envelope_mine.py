#!/usr/bin/env python3
# Working principles: six_cube_search_results.md Postscript 19 (ceiling law)
# and the branch-and-bound discussion. Project index: README.md
"""Mine the deficit-propagation envelope: how does a 6-config's total T
relate to the totals/deep-profiles of its five-cube subsets?

The bound that would make blueprint search a true branch-and-BOUND is a
lemma of the form: if every 5-subset has total <= S (or deep deficits
delta), then T <= f(S, delta). This script measures the empirical
envelope: sample configs across the full total spectrum (stratified from
campaign_results.jsonl + the records), count all six 5-subsets of each
exactly, and log (T, subset totals, subset deep profiles) to
envelope_mine.jsonl for envelope fitting.

Usage: nohup python3 envelope_mine.py [N_PER_BIN=60] >> envelope_mine.out 2>&1 &
"""
import json
import random
import subprocess
import sys


def count(quats):
    n = len(quats)
    s = ';'.join(','.join(map(str, q)) for q in quats)
    o = subprocess.run(['./cube_regions_n', '--n', str(n), '--quats', s],
                       capture_output=True, text=True, timeout=120).stdout
    r = json.loads(o)
    return r['bounded'], r['by_depth']


def main(per_bin):
    # stratified sample: bins of 25 across the total spectrum
    bins = {}
    rng = random.Random(0)
    for line in open('campaign_results.jsonl'):
        try:
            r = json.loads(line)
        except Exception:
            continue
        b = r['bounded'] // 25 * 25
        bins.setdefault(b, [])
        # reservoir sample per bin
        L = bins[b]
        if len(L) < per_bin:
            L.append(r['quats'])
        elif rng.random() < per_bin / (per_bin + len(L)):
            L[rng.randrange(per_bin)] = r['quats']
    # add the records / structured tops explicitly
    extra = [
        [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5], [2, 1, 1, 1],
         [1, 1, 1, 1], [5, 2, 2, 2]],                                # 723
        [[5, 2, 2, 2], [-2, -2, 2, 5], [-2, 5, -2, 2], [-2, 2, 5, -2],
         [2, 1, 1, 1], [1, 0, 0, 0]],                                # 717
        [[3, 1, 0, 0], [3, 0, 1, 0], [3, 0, 0, 1], [41, 28, 22, 14],
         [41, 14, 28, 22], [41, 22, 14, 28]],                        # 699
    ]
    todo = extra + [q for b in sorted(bins) for q in bins[b]]
    print(f'{len(todo)} configs to profile', flush=True)
    with open('envelope_mine.jsonl', 'a') as out:
        for i, q in enumerate(todo):
            try:
                T, bd = count(q)
                subs = []
                for k in range(6):
                    sq = [q[j] for j in range(6) if j != k]
                    st, sbd = count(sq)
                    subs.append({'t': st, 'bd': sbd})
                out.write(json.dumps({'quats': q, 'T': T, 'bd': bd,
                                      'subs': subs}) + '\n')
                out.flush()
            except Exception as e:
                print(f'skip {i}: {e}', flush=True)
            if i % 50 == 0:
                print(f'{i}/{len(todo)}', flush=True)
    print('DONE', flush=True)


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__); raise SystemExit(0)
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
