#!/usr/bin/env python3
# Working principles: NPLUS_SPEC.md. Project index: README.md
"""Parallel falsification campaign driver for cube_regions_n (C++), any n.

Generalization of run_campaign.py (which stays untouched and keeps writing
campaign_results.jsonl for n=6 continuity) per NPLUS_SPEC.md section 3.
Splits a seed range across worker processes (seeds are independent and
deterministic, so parallelism cannot affect results), shards output,
merges into campaign_n<K>.jsonl (deduped by seed), and watches C1-C6 ONLY
for n=6 (those ceilings are empirical facts about n=6, not general-n
predictions -- for n!=6 we don't yet have a ceiling to falsify, so the
driver just reports the best total/depth histogram seen).

Usage:
  python3 run_campaign_n.py --n K START END [WORKERS=8]
  # e.g. detached:
  # nohup caffeinate -i python3 run_campaign_n.py --n 7 3000 53000 4 \
  #       >> campaign_n7.out 2>&1 &

Shards: campaign_n<K>_shard_<i>.jsonl (own namespace -- never touches the
n=6 campaign_shard_*.jsonl files a concurrent n=6 run may be writing);
merged: campaign_n<K>.jsonl.
"""
import argparse
import json
import subprocess
import sys
import time

CEILS_N6 = {1: 112, 2: 208, 3: 164, 4: 102}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('start', type=int)
    ap.add_argument('end', type=int)
    ap.add_argument('workers', type=int, nargs='?', default=8)
    args = ap.parse_args()

    n, start, end, workers = args.n, args.start, args.end, args.workers
    out_path = f'campaign_n{n}.jsonl'
    shard_tpl = f'campaign_n{n}_shard_{{}}.jsonl'

    t0 = time.time()
    span = end - start
    step = (span + workers - 1) // workers
    procs = []
    for i in range(workers):
        a = start + i * step
        b = min(end, a + step)
        if a >= b:
            break
        f = open(shard_tpl.format(i), 'w')
        procs.append((subprocess.Popen(
            ['./cube_regions_n', '--n', str(n), '--seeds', str(a), str(b)],
            stdout=f, stderr=subprocess.DEVNULL), f, a, b))
        print(f'worker {i}: seeds [{a},{b})', flush=True)
    for p, f, a, b in procs:
        p.wait()
        f.close()

    seen = set()
    try:
        for line in open(out_path):
            seen.add(json.loads(line)['seed'])
    except FileNotFoundError:
        pass

    best, viol, kept = 0, [], 0
    best_by_depth = {}
    with open(out_path, 'a') as out:
        for i in range(len(procs)):
            for line in open(shard_tpl.format(i)):
                r = json.loads(line)
                if 'error' in r:
                    continue
                if r['seed'] in seen:
                    continue
                seen.add(r['seed'])
                out.write(line)
                kept += 1
                bd = {int(k): v for k, v in r['by_depth'].items()}
                if r['bounded'] > best:
                    best = r['bounded']
                    best_by_depth = bd
                if n == 6:
                    bad = (r['bounded'] > 623 or bd.get(5, 0) > 36
                           or bd.get(6) != 1
                           or any(bd.get(d, 0) > c for d, c in CEILS_N6.items()))
                    if bad:
                        viol.append(r)
    dt = time.time() - t0
    print(f'\nn={n}: {kept} new configs in {dt:.0f}s '
          f'({kept / max(dt, 1):.2f}/s total), best total = {best} '
          f'depth={dict(sorted(best_by_depth.items()))}')
    if n == 6:
        if viol:
            print(f'*** {len(viol)} CEILING VIOLATIONS (C1-C6) ***')
            for r in viol[:20]:
                print(json.dumps(r))
        else:
            print('no ceiling violations: C1-C6 survive this range')
    else:
        print(f'n={n}: no established ceiling to check against (n=6-specific '
              f'C1-C6 do not apply) -- record this range\'s best in the '
              f'per-n census table instead')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
