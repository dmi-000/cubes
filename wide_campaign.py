#!/usr/bin/env python3
"""Count the mixed strata with the WIDENED engine — including the 284 634
configurations the narrow budget rejected.

`mixed_q2_full.out` records the state of play: of 508 818 candidate
configurations on the mixed 2-plane + 1-quadric strata, the narrow ℚ(√d)
engine counted 224 184 and REJECTED 284 634 for exceeding its 2^112 chain
budget.  Rejected is not "checked and found wanting" — those configurations
are simply uncounted, and one of them could be above 727.
`cube_regions_q2w` (256-bit scalar, gated identical to the narrow engine on
1365 configurations across 33 fields) can count all of them.

This is a self-sequencing detached campaign, not an interactive job: it
enumerates once, shards, counts, and writes results as it goes, so nothing is
waiting on anything.  (The failure mode it avoids has a name in this project:
an agent that sets up a long computation and then parks to watch it.)

Usage:
    python3 wide_campaign.py enumerate       # sympy pass -> pickle (minutes)
    python3 wide_campaign.py count SHARD N   # count shard SHARD of N

INVARIANT: every config is counted by the widened engine, including the ones
the narrow engine already did — so the run doubles as an equivalence check at
scale, and a disagreement on any previously-counted configuration is a
failure of the widening, not a new result.  Results carry the shard id so a
partial campaign is still interpretable.
"""
import json
import os
import pickle
import subprocess
import sys
import tempfile
import time

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
FIXED = ';'.join(','.join('%d:0' % x for x in q) for q in FIVE)
ENGINE = './cube_regions_q2w'
BATCH = 400


def enumerate_configs():
    env = dict(os.environ, Q2_SKIP_COUNT='1')
    p = subprocess.run([sys.executable, 'mixed_q2_full.py'], env=env)
    print('enumeration exit %d' % p.returncode, flush=True)


def count(shard, nshards):
    bycls = pickle.load(open('mixed_q2_configs.pkl', 'rb'))
    work = []
    for sf in sorted(bycls):
        for q in sorted(bycls[sf]):
            work.append((sf, tuple(tuple(c) for c in q)))
    mine = [w for i, w in enumerate(work) if i % nshards == shard]
    print('shard %d/%d: %d of %d configurations'
          % (shard, nshards, len(mine), len(work)), flush=True)

    out = open('wide_campaign_shard_%d.jsonl' % shard, 'a')
    best = (0, None, None)
    done = rejected = 0
    t0 = time.time()
    bysf = {}
    for sf, q in mine:
        bysf.setdefault(sf, []).append(q)
    for sf in sorted(bysf, key=lambda k: -len(bysf[k])):
        cfgs = bysf[sf]
        for s in range(0, len(cfgs), BATCH):
            chunk = cfgs[s:s+BATCH]
            lines = [FIXED + ';' + ','.join('%d:%d' % c for c in q)
                     for q in chunk]
            p = subprocess.run([ENGINE, '--d', str(sf), '--quats-stdin'],
                               input='\n'.join(lines) + '\n',
                               capture_output=True, text=True)
            rows = [l for l in p.stdout.splitlines() if l.startswith('{')]
            for line, q in zip(rows, chunk):
                d = json.loads(line)
                if 'bounded' not in d:
                    rejected += 1
                    continue
                t = d['bounded']
                done += 1
                if t > best[0]:
                    best = (t, sf, q)
                if t >= 723:
                    out.write(json.dumps({'d': sf, 'total': t,
                                          'quat': [list(c) for c in q],
                                          'by_depth': d['by_depth']}) + '\n')
                    out.flush()
            print('  shard %d: d=%d %d counted, %d still rejected, best %s'
                  ' (%.0fs)' % (shard, sf, done, rejected, best[0],
                                time.time() - t0), flush=True)
    print('SHARD %d DONE: counted %d, rejected %d, best %s'
          % (shard, done, rejected, best), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'enumerate':
        enumerate_configs()
    else:
        count(int(sys.argv[2]), int(sys.argv[3]))
