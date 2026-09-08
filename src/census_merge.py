#!/usr/bin/env python3
"""Union-merge the census and report what it says. Never reduces to a max.

Three outputs, in the order they matter:
  1. the global maximum, and whether it changed -- the only thing that needs to be timely,
     because a new maximum moves the filter's operating point AND is a test of the
     signature model: if it turns up in a signature whose ceiling was low, that ceiling
     was wrong and every skip justified the same way is suspect;
  2. the signature -> count relation, as (n, min, max, spread) per signature, which is the
     measurement of how incomplete the signature is;
  3. the signatures seen only once, which are where an unrecorded combination can still be.
"""
import glob, json, sys
from collections import defaultdict

if __name__ == '__main__':
    rows = []
    for f in glob.glob('census_n*_*.jsonl'):
        for l in open(f):
            try:
                rows.append(json.loads(l))
            except Exception:
                pass
    if not rows:
        sys.exit('no census rows yet')
    by = defaultdict(list)
    for r in rows:
        by[tuple(tuple(t) for t in r['sig'])].append(r['count'])
    best = max(rows, key=lambda r: r['count'])
    print('%d configurations, %d distinct signatures, from %s'
          % (len(rows), len(by), sorted(set(r['ens'] for r in rows))))
    print()
    print('GLOBAL MAX %d   ensemble %s   signature %s'
          % (best['count'], best['ens'], [tuple(t) for t in best['sig']]))
    print('   ' + ';'.join(','.join(map(str, q)) for q in best['cfg']))
    print()
    multi = {s: v for s, v in by.items() if len(v) > 1}
    if multi:
        sp = sorted((max(v) - min(v)) for v in multi.values())
        det = sum(1 for v in multi.values() if min(v) == max(v))
        print('SIGNATURE -> COUNT: %d signatures seen more than once' % len(multi))
        print('   %d of them pin the count exactly; spreads median %d, max %d'
              % (det, sp[len(sp)//2], sp[-1]))
        print('   widest:')
        for s, v in sorted(multi.items(), key=lambda kv: -(max(kv[1]) - min(kv[1])))[:4]:
            print('      n=%-3d %4d..%-4d spread %3d   %s' % (len(v), min(v), max(v), max(v)-min(v), s))
    once = [(max(v), s) for s, v in by.items() if len(v) == 1]
    once.sort(reverse=True)
    print()
    print('SEEN ONCE (%d of %d) -- highest first, these are the unexplored combinations:' % (len(once), len(by)))
    for c, s in once[:6]:
        print('   count %4d   %s' % (c, s))
