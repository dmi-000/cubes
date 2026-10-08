#!/usr/bin/env python3
"""The per-triple split of every margin-minimal endpoint of the band climbs.  [P410]

band_climb2 records the margin and budget but not d2(S).  This recomputes band_components' split
for every run's best configuration (band_climb.json, band_climb2.json), so that a statement about
WHICH triples carry the slack at the margin floor rests on measured d2(S).
Output: data/band_floor_split.json.
"""
import os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from band_components import split

ROOT = os.path.dirname(os.path.dirname(HERE))
ends = []
for f in ('band_climb.json', 'band_climb2.json'):
    for r in json.load(open(os.path.join(ROOT, 'data', f))):
        ends.append((f, r['best']))
out, pat = [], collections.Counter()
for f, qs in ends:
    qs = [tuple(q) if not isinstance(q, str) else tuple(map(int, q.strip('()').split(','))) for q in qs]
    s = split(qs)
    d2s = sorted((t['d2'] for t in s['triples']), reverse=True)
    pat[(s['margin'], tuple(d2s))] += 1
    out.append({'source': f, 'margin': s['margin'], 'd2S_sorted': d2s, 'cS': [t['c'] for t in s['triples']],
                'component_slack': s['component_slack'], 'identity': s['identity'], 'qs': qs})
for (m, d), k in sorted(pat.items()):
    print('margin %2d  d2(S) %s  x%d' % (m, list(d), k))
json.dump(out, open(os.path.join(ROOT, 'data', 'band_floor_split.json'), 'w'), indent=1)
