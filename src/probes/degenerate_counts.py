#!/usr/bin/env python3
"""Region counts of the degenerate (shared face plane) compounds the band climbs met.  [P411]

Item 2 of the plan (make 195 unconditional) is refuted by a degenerate compound whose count beats
195, or beats every nearby generic count.  The two climb caches store the shared-plane
configurations they excluded (m = null), with their quaternions.  This counts each with the
engine (retried under rotations when the engine refuses), reports the highest, and leaves the
cross-check of the top ones to sphere_count.  Engine refusals are counted as unevaluated, never
as low counts.  Output: data/degenerate_counts.json.
"""
import os, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import qmul

ROOT = os.path.dirname(os.path.dirname(HERE))


def total(qs):
    for r in [(1, 0, 0, 0), (3, 1, 1, 1), (5, 1, 2, 3), (7, 2, -3, 1)]:
        e = CL.engine([qmul(r, q) for q in qs])
        if 'by_depth' in e:
            return e.get('bounded'), e['by_depth']
    return None, None


def main():
    seen = set()
    for f in ('band_cslack_cache.jsonl', 'band_climb2_cache.jsonl'):
        for line in open(os.path.join(ROOT, 'data', f)):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if r['m'] is None:
                seen.add(r['k'])
    out, unev = [], 0
    for k in sorted(seen):
        qs = [tuple(map(int, g.split(','))) for g in k.split(';')]
        if any(not any(q) for q in qs) or not CL.shares_plane(qs):
            continue
        t, d = total(qs)
        if t is None:
            unev += 1
            continue
        out.append({'qs': qs, 'total': t, 'by_depth': d})
    out.sort(key=lambda r: -r['total'])
    hist = collections.Counter(r['total'] // 10 * 10 for r in out)
    print('%d shared-plane compounds counted, %d unevaluated' % (len(out), unev))
    print('highest:', [(r['total'], r['by_depth']) for r in out[:5]])
    print('by decade:', dict(sorted(hist.items())))
    json.dump({'unevaluated': unev, 'rows': out}, open(os.path.join(ROOT, 'data', 'degenerate_counts.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
