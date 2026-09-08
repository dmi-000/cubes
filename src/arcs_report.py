#!/usr/bin/env python3
"""Aggregate the sharded arc extension, and evaluate the GATE globally.

A shard sees only its own members, so the gate -- arc D must rediscover 1217 -- cannot be
decided inside one. It is decided here, over the union of the checkpoints, and it decides
whether the other arcs' numbers mean anything at all: if the menu cannot rediscover the
known record from the known point, a negative on arcs A, B, C is void rather than
informative ([P186]).
"""
import glob, json
from collections import defaultdict
rows=defaultdict(list)
for f in glob.glob('arcs_extend_s*.jsonl'):
    for l in open(f):
        try: d=json.loads(l)
        except Exception: continue
        rows[d['arc']].append(d)
gate=None
for arc in sorted(rows):
    ds=rows[arc]
    best=max(ds,key=lambda d:d['best'])
    print('%-24s %3d members done, best n=7 = %d at s=%s with seventh cube %s'
          %(arc,len(ds),best['best'],best['s'],best['seventh']))
    if arc.startswith('D'): gate=best['best']
print()
if gate is None:
    print('GATE: arc D not yet reached -- every other arc\'s number is UNJUDGED until it is.')
elif gate>=1217:
    print('GATE PASSED: arc D rediscovered %d >= 1217, so negatives on A, B, C are real.'%gate)
else:
    print('GATE FAILED so far: arc D best is %d < 1217. If it stays below, every negative'%gate)
    print('on arcs A, B and C is VOID, not evidence of absence.')
