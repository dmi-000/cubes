#!/usr/bin/env python3
"""Dimension for every (count, profile) class of the subset census.

`dimension.py` passes its controls ([Postscript 113](LEDGER.md#p113)) -- n=2 both arcs, and arc A in
the full 15-dimensional moduli space, the control `tight_set.py` fails.  Nothing
in the method is specific to records, so the same solver gives the one invariant
of the five that no probe could reach, for every subset class of [Postscript 111](LEDGER.md#p111).

Also reports the WALL CLASSIFICATION that falls out of it: how many distinct
walls the configuration sits on, and how many of them BIND.

    python3 census_dimension.py [seconds]
"""
import itertools, json, sys, time
sys.path.insert(0, HERE)
import dimension as D
from subset_topology import RECORDS as _R6_7, classes
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

BASE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
RECORDS = dict(_R6_7)
RECORDS[8] = BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61)]
RECORDS[9] = RECORDS[8] + [(56, 56, 55, 56)]
# Classes repeat across records -- the n=7 record CONTAINS the n=6 one, so their
# shared subsets are the same configurations and hit the cache rather than
# recomputing.  That is the caching rule paying off across campaigns, not just
# across restarts.

T0 = time.time()
SHARD = int(sys.argv[2]) if len(sys.argv) > 2 else 0
NSHARD = int(sys.argv[3]) if len(sys.argv) > 3 else 1
SUF = '' if NSHARD == 1 else '_%d' % SHARD
OUT = HERE + '/census_dimension%s.json' % SUF
LOG = open(HERE + '/census_dimension%s.log' % SUF, 'w')


def log(m):
    line = '[%7.1fs] %s' % (time.time() - T0, m)
    print(line, flush=True); LOG.write(line + '\n'); LOG.flush()


def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 60000.0
    out = []
    # Classes are independent, so this shards trivially.  Assignment is
    # ROUND-ROBIN, not block: cost grows with k (an n=7 k=6 class has 18
    # variables and runs ~558s against a ~319s median), so a block split would
    # hand one worker every expensive class.
    todo = [(n, rep) for n, Q in sorted(RECORDS.items()) for rep in classes(Q, n)]
    for idx, (n, rep) in enumerate(todo):
        if idx % NSHARD != SHARD:
            continue
        if True:
            if time.time() - T0 > budget:
                log('budget reached'); break
            cfg = rep['cfg']
            pt = D.point_of(cfg)
            if pt is None:
                log('n=%d k=%d count=%d: a cube is a half-turn (w=0), at Cayley '
                    'infinity -- skipped' % (n, rep['k'], rep['count']))
                continue
            D.QZERO[:] = [cfg[0]]
            log('n=%d k=%d count=%d idxs=%s' % (n, rep['k'], rep['count'], rep['idxs']))
            try:
                r = D.deltas_and_dimension(pt, len(cfg),
                                           'n%d k%d c%d' % (n, rep['k'], rep['count']),
                                           q0=cfg[0])
            except Exception as e:
                log('   CRASH %s' % type(e).__name__); continue
            r.update(n=n, k=rep['k'], subset_count=rep['count'],
                     profile=list(rep['profile']), idxs=list(rep['idxs']))
            out.append(r)
            json.dump(out, open(OUT, 'w'), indent=1)
    json.dump(out, open(OUT, 'w'), indent=1)
    log('done: %d classes' % len(out))


if __name__ == '__main__':
    main()
