#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (Postscript 4). Project index: README.md
"""Phase C: breakdown analysis over everything found (campaign + oracle +
hill-climb log). Reports:
  - conjecture violation scan (C1..C6) over all exact results
  - distribution of totals, depth-5 anomaly stats (sub-36) and their
    correlation with totals
  - per-cube depth-1 and per-pair depth-2 distributions of top configs
  - whether depth-3/4 sums 164/102 are ever exceeded, and how often they
    are attained (conserved-at-max question)

Usage: python3 phase_c_analysis.py
"""
import glob
import json
import os
from collections import Counter
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
CEILS = {1: 116, 2: 212, 3: 164, 4: 102, 5: 36}   # post-631 observed maxima
OLD_CEILS = {1: 112, 2: 208, 3: 164, 4: 102, 5: 36}


def load_all():
    """Everything with exact counts. Returns list of dicts with keys
    seed (may be None), bounded, by_depth (int keys), per_label (int keys,
    may be None), quats (may be None), source."""
    out = {}
    order = []

    def add(r, source):
        key = ('seed', r['seed']) if r.get('seed') is not None else \
              ('quats', json.dumps(r.get('quats')))
        bd = {int(k): v for k, v in r['by_depth'].items()}
        pl = ({int(k): v for k, v in r['per_label'].items()}
              if r.get('per_label') else None)
        rec = dict(seed=r.get('seed'), bounded=r['bounded'], by_depth=bd,
                   per_label=pl, quats=r.get('quats'), source=source)
        if key not in out or (pl and not out[key]['per_label']):
            if key not in out:
                order.append(key)
            out[key] = rec

    for path, src in [('campaign_results.jsonl', 'campaign'),
                      ('hillclimb_log.jsonl', 'climb'),
                      ('exact_search_results.jsonl', 'oracle')]:
        p = os.path.join(HERE, path)
        if not os.path.exists(p):
            continue
        with open(p) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if 'bounded' in r:
                    add(r, src)
    for p in sorted(glob.glob(os.path.join(HERE, 'campaign_shard_*.jsonl'))):
        with open(p) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if 'bounded' in r:
                    add(r, 'campaign')
    return [out[k] for k in order]


def violations(recs):
    viol = []
    for r in recs:
        bd = r['by_depth']
        bad = []
        if r['bounded'] > 623:
            bad.append(f'total={r["bounded"]}>623')
        for d, c in OLD_CEILS.items():
            if bd.get(d, 0) > c:
                bad.append(f'd{d}={bd[d]}>{c}')
        if bd.get(6) != 1:
            bad.append(f'd6={bd.get(6)}!=1 (BUG?)')
        if bad:
            viol.append((r, bad))
    return viol


def main():
    recs = load_all()
    print(f'{len(recs)} distinct exact configurations loaded')
    seeds = [r['seed'] for r in recs if r['seed'] is not None]
    print(f'  seeds covered: {len(set(seeds))} '
          f'(range {min(seeds)}..{max(seeds)})')
    nq = sum(1 for r in recs if r['seed'] is None)
    print(f'  explicit-quat configs (hill-climb): {nq}')

    totals = Counter(r['bounded'] for r in recs)
    best = max(totals)
    print(f'\ntotal bounded: max {best}, '
          f'top counts {sorted(totals.items(), reverse=True)[:8]}')

    viol = violations(recs)
    print(f'\n=== violations of ORIGINAL conjectures '
          f'(C1 total<=623, C2 d1<=112, C3 d2<=208, C4 d3<=164, '
          f'C5 d4<=102, C6 d5<=36 & d6==1) ===')
    print(f'{len(viol)} violating configs')
    for r, bad in sorted(viol, key=lambda x: -x[0]['bounded'])[:12]:
        print(f'  seed={r["seed"]} src={r["source"]} '
              f'bounded={r["bounded"]}: {", ".join(bad)}')
        if r['quats']:
            print(f'    quats={r["quats"]}')

    # depth-wise maxima
    print('\n=== per-depth maxima observed (all sources) ===')
    for d in range(1, 7):
        m = max(r['by_depth'].get(d, 0) for r in recs)
        winners = [r['seed'] for r in recs
                   if r['by_depth'].get(d, 0) == m][:6]
        print(f'  depth-{d}: max {m}   (e.g. seeds {winners})')

    # depth-5 anomaly
    d5 = Counter(r['by_depth'].get(5, 0) for r in recs)
    print(f'\n=== depth-5 distribution === {dict(sorted(d5.items()))}')
    sub = [r for r in recs if r['by_depth'].get(5, 0) < 36]
    if sub:
        subt = [r['bounded'] for r in sub]
        allt = [r['bounded'] for r in recs]
        print(f'  sub-36 configs: {len(sub)} '
              f'({100.0 * len(sub) / len(recs):.2f}%)')
        print(f'  their totals: min {min(subt)} max {max(subt)} '
              f'mean {sum(subt)/len(subt):.1f} '
              f'(ensemble mean {sum(allt)/len(allt):.1f})')

    # d3/d4 sum attainment
    for d, cap in ((3, 164), (4, 102)):
        vals = Counter(r['by_depth'].get(d, 0) for r in recs)
        n_at = vals.get(cap, 0)
        n_over = sum(v for k, v in vals.items() if k > cap)
        print(f'\ndepth-{d}: attain {cap} in {n_at} configs '
              f'({100.0 * n_at / len(recs):.1f}%), exceed it in {n_over}')

    # per-cube / per-pair breakdowns of the top configs with per_label
    withpl = [r for r in recs if r['per_label']]
    withpl.sort(key=lambda r: -r['bounded'])
    print(f'\n=== per-subset structure of top configs '
          f'({len(withpl)} configs carry per_label) ===')
    cube_max = 0
    pair_max = 0
    cube22 = Counter()   # count of cubes >=22 per config
    for r in withpl:
        pl = r['per_label']
        pc = [pl.get(1 << k, 0) for k in range(6)]
        cube_max = max(cube_max, max(pc))
        prs = [pl.get((1 << i) | (1 << j), 0)
               for i, j in combinations(range(6), 2)]
        pair_max = max(pair_max, max(prs))
        cube22[sum(1 for c in pc if c >= 22)] += 1
    print(f'per-cube depth-1 max anywhere: {cube_max}')
    print(f'per-pair depth-2 max anywhere: {pair_max}')
    print(f'configs by number of >=22-cubes: {dict(sorted(cube22.items()))}')
    for r in withpl[:6]:
        pl = r['per_label']
        pc = [pl.get(1 << k, 0) for k in range(6)]
        prs = sorted((pl.get((1 << i) | (1 << j), 0)
                      for i, j in combinations(range(6), 2)), reverse=True)
        d3s = sum(pl.get(sum(1 << i for i in c), 0)
                  for c in combinations(range(6), 3))
        d4s = sum(pl.get(sum(1 << i for i in c), 0)
                  for c in combinations(range(6), 4))
        print(f'  seed={r["seed"]} bounded={r["bounded"]} d1/cube={pc} '
              f'd2/pair={prs} d3sum={d3s} d4sum={d4s}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
