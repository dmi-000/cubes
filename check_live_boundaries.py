#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (Postscript 4 ceilings). Project index: README.md
"""Standalone checker (does NOT touch run_campaign.py) for the SIX live
conjecture boundaries, applied to a seed range of campaign_results.jsonl:

  total <= 635
  d1 (depth-1) <= 118
  d2 (depth-2) <= 214
  d3 (depth-3) <= 164
  d4 (depth-4) <= 102
  d5 (depth-5) <= 36
  d6 (depth-6) == 1  (theorem; != 1 signals a counter bug)

Usage: python3 check_live_boundaries.py SEED_LO SEED_HI [FILE]
Scans campaign_results.jsonl (or FILE) for seeds in [SEED_LO, SEED_HI),
reports count scanned, best total seen, and any genuine breaches.
"""
import json
import sys

LIVE = {'total': 635, 1: 118, 2: 214, 3: 164, 4: 102, 5: 36}


def main():
    lo = int(sys.argv[1])
    hi = int(sys.argv[2])
    path = sys.argv[3] if len(sys.argv) > 3 else 'campaign_results.jsonl'
    n = 0
    best = -1
    best_rec = None
    breaches = []
    with open(path) as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            s = r.get('seed')
            if s is None or not (lo <= s < hi):
                continue
            n += 1
            b = r['bounded']
            if b > best:
                best = b
                best_rec = r
            bd = {int(k): v for k, v in r.get('by_depth', {}).items()}
            bad = []
            if b > LIVE['total']:
                bad.append(f'total {b} > {LIVE["total"]}')
            for d in (1, 2, 3, 4, 5):
                v = bd.get(d, 0)
                if v > LIVE[d]:
                    bad.append(f'd{d} {v} > {LIVE[d]}')
            if bd.get(6) != 1:
                bad.append(f'd6 = {bd.get(6)} != 1 (theorem violation!)')
            if bad:
                breaches.append((s, bad, r))
    print(f'scanned {n} seeds in [{lo},{hi}) from {path}')
    print(f'best total in range: {best} (seed {best_rec["seed"] if best_rec else None})')
    if best_rec:
        print(f'  by_depth: {best_rec["by_depth"]}')
    if breaches:
        print(f'*** {len(breaches)} GENUINE BOUNDARY BREACHES (live six) ***')
        for s, bad, r in breaches:
            print(f'  seed {s}: {"; ".join(bad)}')
            print(f'    quats={r.get("quats")} bounded={r["bounded"]} by_depth={r["by_depth"]}')
    else:
        print('no breaches of the six live boundaries in this range')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
