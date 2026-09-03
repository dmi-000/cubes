#!/usr/bin/env python3
"""WHERE the engines refuse — the measurement that decides whether removing the
ceiling is worth building.

The proposal on the table is modular/CRT sign evaluation, which would remove the height
ceiling rather than raise it. Before building it, the question "what would this unlock"
has to be answered in the currency the project cares about. The first answer looked like
volume, and volume says almost nothing:

    Haar baseline, 30 000 exactly-Haar draws at n=3..10   0 unevaluated
    basin climbs, chambers along solved scan lines        0.4 - 1.7 % refused
    the n=9 record, chambers along solved scan lines      36 % refused

So the refusal set has essentially no volume, and a volume-based valuation would return
~0 and reject the build. That is the wrong metric: the refusals sit on the degenerate
strata, which are Haar-null by construction and are exactly where every record lives.

This script asks the sharper question -- do the refusals track CODIMENSION, or do they
track HEIGHT? The known records separate the two, because their heights are not ordered
by their codimension:

    n=5  393   height     7        n=9   2787  height 113786
    n=6  727   height    14        n=10  3925  height 113786
    n=7  1217  height    14
    n=8  1895  height    61

If refusal tracks codimension, the low-n records refuse too. If it tracks height, they
do not -- and then the cure is a better REPRESENTATIVE, not a better engine, which is
the cheaper fix by a wide margin and is what this project's own recorded principle
predicts: "if the failures and successes separate perfectly on input height, the method
chose badly; the question is still open."
"""
import sys, time
sys.path.insert(0, '.')
from solved_scan import best_on_lines, count
from haarsample import haar_config
import random

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C6 = BASE + [(7,14,1,-5)]
C7 = C6 + [(4,-3,-4,-4)]
C8 = C7 + [(24,-24,24,-61)]
N9 = C8 + [(88787,-9061,74275,113786)]
RECORDS = [(5, BASE), (6, C6), (7, C7), (8, C8)]

if __name__ == '__main__':
    nd = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print('%-26s %8s %8s %10s %10s %8s' % ('configuration', 'count', 'height',
                                           'chambers', 'refused', 'rate'))
    rows = []
    for n, cfg in RECORDS:
        h = max(abs(x) for q in cfg for x in q)
        t = time.time()
        (b, _), tot, unev = best_on_lines(cfg, ndir=nd, reach=6, seed=3, verbose=False)
        print('%-26s %8s %8d %10d %10d %7.2f%%'
              % ('RECORD n=%d' % n, count(cfg), h, tot, unev, 100.0 * unev / max(tot, 1)),
              flush=True)
        rows.append(('record', n, h, tot, unev))
        # matched control: a generic configuration of the SAME n
        rng = random.Random(4242 + n)
        g = haar_config(rng, n, 128, chart=True)
        hg = max(abs(x) for q in g for x in q)
        (bg, _), tg, ug = best_on_lines(g, ndir=nd, reach=6, seed=3, verbose=False)
        print('%-26s %8s %8d %10d %10d %7.2f%%'
              % ('  generic n=%d (control)' % n, count(g), hg, tg, ug,
                 100.0 * ug / max(tg, 1)), flush=True)
        rows.append(('generic', n, hg, tg, ug))
    print()
    print('For comparison, already measured: RECORD n=9 (height 113786) refused 137 of')
    print('384 chambers = 35.7%.')
