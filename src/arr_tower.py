#!/usr/bin/env python3
"""Arrangement rows for the top of the tower, including n=10 — reproducibly.

[P172] fitted a linear law from n=7 up: +24 walls, +3 ambient, +2 rank per added
cube, over three consecutive rungs.  Extended to n=10 it predicted 123 walls; the
measurement returned 101 (ambient 27, rank 22 as predicted).  That run was launched
from an inline heredoc and was never saved, so its number was not reproducible and
its INPUT was not recorded either — which matters here, because:

    R[9]  = ... + (56,56,55,56)      the recorded n=9 rung, k=56
    P181's n=10 = ... + (57,57,56,57) + (19,-2,15,24)      built on k=57

**The n=10 configuration is not an extension of the n=9 row.**  [P178] showed 2785
is a continuum in k and [P181] extended k=57 because it scored better, so the two
rows sit on different continuum members.  A wall-count law fitted along the tower
was therefore never tested by that measurement.

This script decides it, by computing the k=57 member's own n=9 row.  If k=57 at n=9
already differs from 99 walls, the +2 is a change of base, not a break in the law.

GATE: the recorded n=9 row must reproduce [P172]'s walls 99 / ambient 24 / rank 20
before either new row is believed.  Deficit is ambient - rank (= lineality), not an
independent quantity; and by [P175] it is NOT a plateau dimension, since the count
drops immediately along null directions.
"""
import json, os, sys, time
sys.path.insert(0, '.')
from wallcount import walls_of, R
from growth727 import BASE

C9_REC = R[9]                                              # k = 56, the recorded rung
C9_K57 = R[8] + [(57, 57, 56, 57)]                         # the member P181 extended
C10    = C9_K57 + [(19, -2, 15, 24)]                       # P181's n=10 = 3913

ROWS = [('n=9 recorded k=56', C9_REC, dict(walls=99, ambient=24, rank=20)),
        ('n=9 member  k=57',  C9_K57, None),
        ('n=10 (P181, on k=57)', C10,  None)]

out = []
for name, cfg, expect in ROWS:
    t0 = time.time()
    r = walls_of(cfg)
    r['name'], r['secs'], r['n'] = name, time.time() - t0, len(cfg)
    r['deficit'] = r['ambient'] - r['rank']
    out.append(r)
    print('%-22s count %-6s walls %4d  ambient %3d  rank %3d  deficit %d  (%.0fs)'
          % (name, r['count'], r['walls'], r['ambient'], r['rank'],
             r['deficit'], r['secs']), flush=True)
    if expect:
        bad = {k: (v, r[k]) for k, v in expect.items() if r[k] != v}
        if bad:
            sys.exit('GATE FAILED, expected vs got: %s' % bad)
        print('   gate: reproduces P172 row for n=9   OK', flush=True)
    json.dump(out, open('arr_tower.json', 'w'), indent=1)

w9, w9b, w10 = out[0]['walls'], out[1]['walls'], out[2]['walls']
print('\nP172 predicted n=10 walls = 99 + 24 = 123;  measured %d' % w10, flush=True)
print('n=9 walls: recorded k=56 -> %d, member k=57 -> %d  (%s)'
      % (w9, w9b, 'SAME, so the base is not the explanation'
         if w9 == w9b else 'DIFFERENT, so the rows sit on different members'), flush=True)
print('step from the row n=10 actually extends: %d -> %d = %+d'
      % (w9b, w10, w10 - w9b), flush=True)
