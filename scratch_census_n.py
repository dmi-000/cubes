#!/usr/bin/env python3
# Working principles: NPLUS_SPEC.md. Project index: README.md
"""Per-n census over a campaign_n<K>.jsonl (+ optional hillclimb log):
record total, frozen deep-depth sums near the top, generic (most-common)
per-depth values with their frequency (the T1(l,n) census numbers,
available directly from per_label/by_depth -- no spherical code needed),
mod-4 exception rate, and top-spectrum value gaps.

Usage: python3 scratch_census_n.py N [extra.jsonl ...]
  (always reads campaign_n<N>.jsonl if present; extra files are merged,
  deduped by quats since hill-climb records have no seed)
"""
import glob
import json
import sys
from collections import Counter


def load(n, extra):
    seen_keys = set()
    recs = []
    paths = [f'campaign_n{n}.jsonl'] + extra
    for p in paths:
        try:
            f = open(p)
        except FileNotFoundError:
            continue
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if 'bounded' not in r:
                continue
            key = tuple(tuple(q) for q in r['quats']) if 'quats' in r else (r.get('seed'),)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            recs.append(r)
    return recs


def main():
    n = int(sys.argv[1])
    extra = sys.argv[2:]
    recs = load(n, extra)
    print(f'n={n}: {len(recs)} distinct configs loaded')
    if not recs:
        return

    totals = [r['bounded'] for r in recs]
    best = max(totals)
    print(f'record total = {best}')
    top = sorted(recs, key=lambda r: -r['bounded'])
    print('top 10 totals:', [r['bounded'] for r in top[:10]])

    # frozen deep sums: depths n, n-1, n-2, n-3 among the top-K records
    K = min(20, len(top))
    for d in range(n, max(n - 4, 0), -1):
        vals = set()
        for r in top[:K]:
            bd = {int(k): v for k, v in r['by_depth'].items()}
            vals.add(bd.get(d, 0))
        print(f'  depth-{d} among top {K}: {sorted(vals, reverse=True)}'
              + ('  FROZEN' if len(vals) == 1 else ''))

    # generic per-depth values across the WHOLE dataset (T1(l,n) census
    # numbers; l = n - d, l=1 is the outermost nontrivial depth n-1)
    print('\nper-depth generic-value census (whole dataset):')
    for d in range(1, n + 1):
        c = Counter()
        for r in recs:
            bd = {int(k): v for k, v in r['by_depth'].items()}
            c[bd.get(d, 0)] += 1
        mc = c.most_common(3)
        top_val, top_cnt = mc[0]
        l = n - d
        print(f'  depth-{d} (l={l}): generic value {top_val} '
              f'({top_cnt}/{len(recs)} = {top_cnt/len(recs):.1%})  top3={mc}')

    # mod-4 law
    predicted = (2 * n - 1) % 4
    exc = [r for r in recs if r['bounded'] % 4 != predicted]
    print(f'\nmod-4 law: bounded == {predicted} (mod 4) predicted; '
          f'{len(exc)}/{len(recs)} exceptions ({len(exc)/len(recs):.4%})')
    if exc:
        print('  example exceptions:', [(r.get('seed'), r['bounded']) for r in exc[:10]])

    # top-spectrum gaps: distinct totals in the top decile
    cutoff = sorted(totals, reverse=True)[max(0, len(totals)//10)]
    top_vals = sorted(set(t for t in totals if t >= cutoff))
    gaps = [v for v in range(top_vals[0], top_vals[-1]+1)
            if v not in top_vals and (v % 2 == top_vals[0] % 2)]
    print(f'\ntop-decile totals (>= {cutoff}): {top_vals}')
    print(f'  same-parity gaps in that range: {gaps}')

    # per-cube depth-1 / per-pair depth-2 extremes (per_label)
    per_cube_max = 0
    per_pair_max = 0
    for r in recs:
        pl = {int(k): v for k, v in r.get('per_label', {}).items()}
        for k in range(n):
            per_cube_max = max(per_cube_max, pl.get(1 << k, 0))
        from itertools import combinations
        for i, j in combinations(range(n), 2):
            per_pair_max = max(per_pair_max, pl.get((1 << i) | (1 << j), 0))
    print(f'\nper-cube depth-1 max observed: {per_cube_max}')
    print(f'per-pair depth-2 max observed: {per_pair_max}')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
