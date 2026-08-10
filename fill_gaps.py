#!/usr/bin/env python3
"""Count the chambers the engines refused, on the five 727 arc lines.

The six-line max sweep (maxline.py) left 1 727 of 20 308 chambers unevaluated --
8.5% overall, 20% on arc C -- because a rational strictly between two very close
wall roots has a denominator past the wide engine's budget.  The incidence
identity has no such limit: its cost is combinatorial, flat in coefficient size.

The engine is never called.  A midpoint is sent to the identity exactly when its
quaternion exceeds what the engines accept, so this fills the holes and touches
nothing that was already counted.
"""
import json, os, sys, time
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import incidence2 as I, wall_params as W
from maxline import q_of, between, BASE
from extend_c import Base

LINES = {
 'A':  ([F(19,3),F(-7),F(-11)], [F(1),F(-3),F(-6)], F(-20), F(20)),
 'B':  ([F(4,35),F(2,5),F(-41,35)], [F(1),F(1),F(-4)], F(-20), F(20)),
 'C':  ([F(245,29),F(-295,29),F(428,29)], [F(1),F(-3,2),F(9,4)], F(-20), F(60)),
 'D1': ([F(2),F(1,7),F(-5,7)], [F(-1),F(-1,7),F(3,14)], F(-20), F(20)),
 'D2': ([F(2),F(1,7),F(-5,7)], [F(-1),F(-4,21),F(2,7)], F(-20), F(20)),
}
BUDGET = 10**6          # beyond this the wide engine rejects; identity does not

def main():
    log = open(os.path.join(HERE, "fill_gaps.log"), "a")
    S = Base(BASE)
    pts, lines = I.base_catalogue()
    for name, (a0, d, lo, hi) in LINES.items():
        t0 = time.time()
        roots = sorted(s for s in set(W.w4_params(a0, d, pts)) | set(W.w3_params(a0, d, lines))
                       if lo < s < hi)
        pos = [lo] + roots + [hi]
        mids = [between(pos[i], pos[i+1]) for i in range(len(pos)-1)]
        gaps = []
        for m in mids:
            q = q_of([a0[k] + m*d[k] for k in range(3)])
            if max(abs(v) for v in q) > BUDGET: gaps.append((m, q))
        print("arc %s: %d chambers, %d beyond the engines' budget" % (name, len(mids), len(gaps)),
              file=log, flush=True)
        best = 0; hist = {}
        for i, (m, q) in enumerate(gaps):
            try: c = S.C(q)
            except Exception: continue
            hist[c] = hist.get(c, 0) + 1
            if c > best: best = c
            if c > 727:
                print("   *** %d at s = %s  cube %s" % (c, m, q), file=log, flush=True)
            if (i+1) % 100 == 0:
                print("   [%5.0fs] %d/%d filled, best %d, counts %s"
                      % (time.time()-t0, i+1, len(gaps), best,
                         sorted(hist.items(), reverse=True)[:5]), file=log, flush=True)
        print("   arc %s DONE: %d filled, max %d, distribution %s"
              % (name, len(gaps), best, sorted(hist.items(), reverse=True)[:8]), file=log, flush=True)

if __name__ == '__main__':
    main()
