#!/usr/bin/env python3
"""Test the conditional prediction: is every inner chamber cut into exactly |g(-1)|?

`quotient.py` predicts chambers(1217) = 4 621 728 x 279 ASSUMING X_727 is modular
in L(A_1217).  That assumption is unverified and, unlike at the previous rung,
cannot be checked exhaustively: 1217 has 51 walls and its lattice is far beyond
the 1 192 678 flats that were swept for 727.

Modularity forces UNIFORM subdivision: every chamber of the inner arrangement must
be cut into exactly |g(-1)| by the new walls -- not on average, every time.  A
single chamber cut into any other number refutes the modularity hypothesis and
therefore the predicted count, while leaving intact everything that was computed
rather than assumed.  That is the whole value of running it: it can come back NO.

This generalises `modular62.py`, which confirmed 62 on 25 of 393's chambers.
"""
import json, os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from exactlp import feasible_strict

TARGET = 279
C6 = BASE + [(7, 14, 1, -5)]
C7 = C6 + [(4, -3, -4, -4)]
n_sample = int(sys.argv[1]) if len(sys.argv) > 1 else 6

W7, n7 = walls_of(C7)
W6, n6 = walls_of(C6)
old = [i for i, w in enumerate(W7) if all(x == 0 for x in w[n6:])]
new = [i for i in range(len(W7)) if i not in old]
print('1217: %d walls ambient %d | inner(727) %d | new %d | target %d'
      % (len(W7), n7, len(old), len(new), TARGET), flush=True)

# inner chambers: sign vectors on the 27 old walls, taken from the 727 enumeration
import glob
paths = sorted(glob.glob(os.path.join(HERE, 'stream_727', 'stage_26.part0*')))
sigs = []
with open(paths[0]) as fh:
    for line in fh:
        line = line.strip()
        if len(line) == 26:
            sigs.append(line)
print('%d partial (26-wall) chambers available; sampling %d' % (len(sigs), n_sample), flush=True)
rnd = random.Random(20260824)
counts, t0 = [], time.time()
for idx, s in enumerate(rnd.sample(sigs, n_sample)):
    sig = [1 if c == '+' else -1 for c in s]
    base = [[sg * W7[old[j]][t] for t in range(n7)] for j, sg in enumerate(sig)]
    # complete the 27th old wall, then extend over the new walls
    frontier = [[]]
    for k in old[len(sig):] + new:
        nxt = []
        for ext in frontier:
            rows = base + [[e * W7[m][t] for t in range(n7)]
                           for e, m in zip(ext, (old[len(sig):] + new)[:len(ext)])]
            for sgn in (1, -1):
                if feasible_strict(rows + [[sgn * W7[k][t] for t in range(n7)]], n7) is not None:
                    nxt.append(ext + [sgn])
        frontier = nxt
    # each surviving extension splits into (27th old wall choice) x (new-wall pattern)
    counts.append(len(frontier))
    print('   %d/%d -> %d leaves%s (%.0fs)'
          % (idx + 1, n_sample, len(frontier),
             '' if len(frontier) % TARGET == 0 else '  <<< not a multiple of %d' % TARGET,
             time.time() - t0), flush=True)

print('\ncounts: %s' % counts)
json.dump({'target': TARGET, 'counts': counts, 'secs': time.time() - t0},
          open(os.path.join(HERE, 'uniform_1217.json'), 'w'), indent=1)
