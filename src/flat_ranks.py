#!/usr/bin/env python3
"""Flats of the 727 arrangement BY RANK — the stratum sizes, with progress.

WHY NOT THE FULL FACE COUNT.  `facecount.py` sums chambers(A^X) over every flat,
giving the total face count. Estimated at 3.2 core-hours by scaling 183's
per-flat rate; killed at 9h16m with no output, because that scaling was wrong --
183's restricted arrangements have <=12 walls in <=8 dimensions, 727's have up to
27 in 14, so per-flat cost is not a constant of the family (METHODS 20).

WHAT THE STRATUM WALK ACTUALLY NEEDS is the number of FLATS at each rank, not the
number of faces. That is a by-product of the lattice BFS alone -- no restricted
chamber count per flat -- and the same BFS ran in 2h06m inside the chamber
derivation (P152). High-rank flats are the high-codimension coincidence loci where
records sit; for 183 the top ranks hold 1 and 60 flats against 264 in the middle.

PROGRESS IS PRINTED PER RANK and the running totals are checkpointed, so this can
be read while it runs -- the failure that killed its predecessor.
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from zaslavsky import Flats

W, nc = walls_of(BASE + [(7, 14, 1, -5)])
L = Flats(W)
m = L.m
t0 = time.time()
seen = {L.empty: 0}
frontier = [L.empty]
rank_counts = {0: 1}
out = os.path.join(HERE, 'flat_ranks_727.json')
print('727: %d walls, ambient %d' % (m, nc), flush=True)
r = 0
while frontier:
    r += 1
    nxt = []
    for Fm in frontier:
        for j in range(m):
            if Fm >> j & 1:
                continue
            G = L.extend(Fm, j)
            if G not in seen:
                seen[G] = r
                nxt.append(G)
    if not nxt:
        break
    rank_counts[r] = len(nxt)
    frontier = nxt
    print('   rank %2d: %9d flats   (total %9d, %.0fs)'
          % (r, len(nxt), len(seen), time.time() - t0), flush=True)
    json.dump({'rank_counts': rank_counts, 'total': len(seen),
               'complete': False, 'secs': time.time() - t0},
              open(out, 'w'), indent=1)
json.dump({'rank_counts': rank_counts, 'total': len(seen),
           'complete': True, 'secs': time.time() - t0}, open(out, 'w'), indent=1)
print('TOTAL %d flats in %.0fs' % (len(seen), time.time() - t0), flush=True)
