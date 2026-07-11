#!/usr/bin/env python3
# Working principles: CPP_SPEC.md + six_cube_search_results.md (Postscript 4). Project index: README.md
"""Parallel falsification campaign driver for cube_regions (C++).

Splits a seed range across worker processes (seeds are independent and
deterministic, so parallelism cannot affect results), shards output,
merges, and watches for violations of the ceiling conjectures:

  C1 total<=623  C2 d1<=112  C3 d2<=208  C4 d3<=164  C5 d4<=102
  C6 d5<=36 and d6==1
(All ceilings are UPPER bounds: undershoot is normal - depth-5 is 36
generically but rare chambers give 34/32 via face-patch merging; d6=1 is
a theorem (convex core), so d6 != 1 signals a counter bug, not a finding.)

Usage:
  python3 run_campaign.py START END [WORKERS=8]
  # e.g. detached:
  # nohup caffeinate -i python3 run_campaign.py 3000 200000 8 \
  #       >> campaign.out 2>&1 &

Shards: campaign_shard_<i>.jsonl ; merged: campaign_results.jsonl (appended,
deduped by seed). Never touches exact_search_results.jsonl.
"""
import json
import subprocess
import sys
import time

CEILS = {1: 112, 2: 208, 3: 164, 4: 102}


def main(start, end, workers):
    t0 = time.time()
    n = end - start
    step = (n + workers - 1) // workers
    procs = []
    for i in range(workers):
        a = start + i * step
        b = min(end, a + step)
        if a >= b:
            break
        f = open(f'campaign_shard_{i}.jsonl', 'w')
        procs.append((subprocess.Popen(
            ['./cube_regions', '--seeds', str(a), str(b)],
            stdout=f, stderr=subprocess.DEVNULL), f, a, b))
        print(f'worker {i}: seeds [{a},{b})', flush=True)
    for p, f, a, b in procs:
        p.wait()
        f.close()
    seen = set()
    try:
        for line in open('campaign_results.jsonl'):
            seen.add(json.loads(line)['seed'])
    except FileNotFoundError:
        pass
    best, viol, kept = 0, [], 0
    with open('campaign_results.jsonl', 'a') as out:
        for i in range(len(procs)):
            for line in open(f'campaign_shard_{i}.jsonl'):
                r = json.loads(line)
                if r['seed'] in seen:
                    continue
                seen.add(r['seed'])
                out.write(line)
                kept += 1
                bd = {int(k): v for k, v in r['by_depth'].items()}
                best = max(best, r['bounded'])
                bad = (r['bounded'] > 623 or bd.get(5, 0) > 36
                       or bd.get(6) != 1
                       or any(bd.get(d, 0) > c for d, c in CEILS.items()))
                if bad:
                    viol.append(r)
    dt = time.time() - t0
    print(f'\n{kept} new configs in {dt:.0f}s '
          f'({kept / max(dt, 1):.1f}/s total), best total = {best}')
    if viol:
        print(f'*** {len(viol)} CEILING VIOLATIONS ***')
        for r in viol[:20]:
            print(json.dumps(r))
    else:
        print('no ceiling violations: C1-C6 survive this range')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 13000
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    main(start, end, workers)
