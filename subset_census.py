#!/usr/bin/env python3
"""Every subset of every record, counted exactly -- the base layer for topology.

The project knows a handful of subset counts (183's triples 63/63/63/55, 723's
5-subsets, the nesting chain 183 c 393 c 727 c 1217 c 1895 c 2785) but has never
enumerated them.  Characterising the topology of records AND of their subsets
needs this first: which subsets are themselves records, which are plateau
members, how the counts distribute, and how many distinct congruence types occur
at each level.

For each record and each k, every k-subset is counted with the exact engine in
one batched call.  Reported per (record, k):

    max / min / the full multiset of counts
    whether the max equals the level-k record (does the tower nest here?)
    the number of DISTINCT count values -- a lower bound on distinct types
    the pair-label multiset of each subset, which is a congruence invariant
      (necessary, not sufficient -- Postscript 61) and separates types cheaply

Subsets are not deduplicated by congruence here: the pair-label multiset is
recorded so that dedup can be done afterwards without recounting.

    python3 subset_census.py            # all records, all k
"""
import itertools
import json
import subprocess
import sys
from collections import Counter

ENG = '/Users/dmi/cube-compounds/cube_regions_n'
ENGW = '/Users/dmi/cube-compounds/cube_regions_q2w'

BASE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]

RECORDS = {
    2: [(1, 0, 0, 0), (3, 1, 1, 1)],
    3: None,                                   # irrational, handled separately
    4: [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)],
    5: list(BASE),
    6: BASE + [(7, 14, 1, -5)],
    7: BASE + [(7, 14, 1, -5), (4, -3, -4, -4)],
    8: BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61)],
    9: BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61),
               (56, 56, 55, 56)],
}

LEVEL_RECORD = {2: 13, 3: 67, 4: 183, 5: 393, 6: 727, 7: 1217, 8: 1895, 9: 2785}


def batch(cfgs):
    """count many configurations in one engine call; wide engine for big quats"""
    out = {}
    for group, cmd in ((
            [c for c in cfgs if max(abs(v) for q in c for v in q) <= 512],
            [ENG, '--quats-stdin']), (
            [c for c in cfgs if max(abs(v) for q in c for v in q) > 512],
            [ENGW, '--d', '0', '--quats-stdin'])):
        if not group:
            continue
        inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c)
                        for c in group) + '\n'
        p = subprocess.run(cmd, input=inp, capture_output=True, text=True)
        for line in p.stdout.splitlines():
            try:
                o = json.loads(line)
            except Exception:
                continue
            if 'quats' not in o or 'bounded' not in o:
                continue
            out[tuple(tuple(int(v) for v in q) for q in o['quats'])] = o['bounded']
    return out


def main():
    result = {}
    for n, Q in sorted(RECORDS.items()):
        if Q is None:
            continue
        # every subset of size >= 2, plus the pairs needed for pair labels
        subs = [list(c) for k in range(2, n + 1)
                for c in itertools.combinations(Q, k)]
        counts = batch(subs)
        pair = {}
        for i, j in itertools.combinations(range(n), 2):
            pair[(i, j)] = counts.get((tuple(Q[i]), tuple(Q[j])))
        rec = {}
        print('\n=== n = %d, record %d ===' % (n, LEVEL_RECORD[n]))
        for k in range(2, n + 1):
            vals, labels = [], []
            for idxs in itertools.combinations(range(n), k):
                c = counts.get(tuple(tuple(Q[i]) for i in idxs))
                if c is None:
                    continue
                vals.append(c)
                labels.append(tuple(sorted(
                    (pair[(a, b)] for a, b in itertools.combinations(idxs, 2)),
                    reverse=True)))
            if not vals:
                continue
            hi = max(vals)
            nests = (hi == LEVEL_RECORD.get(k))
            rec[k] = {'n_subsets': len(vals), 'max': hi, 'min': min(vals),
                      'distinct': len(set(vals)),
                      'spectrum': dict(sorted(Counter(vals).items(), reverse=True)),
                      'level_record': LEVEL_RECORD.get(k),
                      'nests': nests,
                      'label_types': len(set(labels))}
            print('  k=%d  %3d subsets | max %5d %-12s | min %5d | %2d distinct '
                  'counts | %2d label types'
                  % (k, len(vals), hi,
                     '(= record)' if nests else '(record %s)' % LEVEL_RECORD.get(k),
                     min(vals), len(set(vals)), len(set(labels))))
        result[n] = rec
    json.dump(result, open('/Users/dmi/cube-compounds/subset_census.json', 'w'),
              indent=1)
    print('\nwritten to subset_census.json')


if __name__ == '__main__':
    main()
