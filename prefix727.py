#!/usr/bin/env python3
"""Exact chamber count of a PREFIX of the 727 wall list, by the P152 recursion.

WHY.  P153 gives c_27 = 4 621 728 = 62 x 74 544 and the enumeration gives
c_24 = 20 x 74 544, c_25 = 40 x 74 544, all integer multiples of 393's total.
That forces b_26 + b_27 = 22 x 74 544 but does not split it.  The live
enumeration's measured split fraction at wall 26 (~0.2517) suggests
b_26 = 10 x 74 544 exactly, i.e. c_26 = 3 727 200 and s_26 = 1/4 -- a
CONJECTURE resting on b_26 being an integer multiple of 74 544, which is
motivated but unproven.  This settles it by derivation instead of waiting for
the enumeration's stage 26.

Usage: prefix727.py K     -- chambers of the arrangement of the first K walls.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from zaslavsky import chambers

k = int(sys.argv[1])
W, nc = walls_of(BASE + [(7, 14, 1, -5)])
if not 1 <= k <= len(W):
    raise SystemExit('K must be in 1..%d' % len(W))
n, st, fl, secs = chambers(W[:k], label='727 first %d walls:' % k)
pred = {26: 3727200}.get(k)
if pred is not None:
    print('  prediction %s -> %s' % ('{:,}'.format(pred),
                                     'CONFIRMED' if n == pred else 'REFUTED'))
    print('  n / 74544 = %s' % (n / 74544))
json.dump({'k': k, 'chambers': n, 'states': st, 'flats': fl, 'secs': secs},
          open(os.path.join(HERE, 'prefix727_%d.json' % k), 'w'), indent=1)
