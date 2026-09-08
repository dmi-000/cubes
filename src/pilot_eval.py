#!/usr/bin/env python3
"""Measure the true per-chamber cost of evaluating region counts on chambers.

Step 1 of the maximality route needs, for EVERY chamber of 727's neighbourhood:
a witness point (the stage files store sign vectors only -- the memory-saving
design of P146) and then an exact region count at that point.  Both costs are
unknown, and this session's estimates have been wrong repeatedly, so measure
before committing to anything multi-day.
"""
import sys, time, json
sys.path.insert(0, '.')
sys.argv = ['x']
from growth727 import walls_of, BASE
from exactlp import feasible_strict
import dimension as D

W, nc = walls_of(BASE + [(7, 14, 1, -5)])
svs = [l.strip() for l in open('sv200.txt') if len(l.strip()) == 26][:60]
print('%d sign vectors; ambient %d' % (len(svs), nc), flush=True)

t_lp = t_ev = 0.0
counts = []
for i, s in enumerate(svs):
    sig = [1 if c == '+' else -1 for c in s]
    rows = [[sg * W[j][t] for t in range(nc)] for j, sg in enumerate(sig)]
    a = time.time(); y = feasible_strict(rows, nc); t_lp += time.time() - a
    if y is None:
        print('  infeasible?!'); continue
    a = time.time(); c = D.count_at(list(y), 6); t_ev += time.time() - a
    counts.append(c)
n = len(counts)
print('\nper chamber: witness LP %.1f ms | region count %.1f ms | total %.1f ms'
      % (1000*t_lp/n, 1000*t_ev/n, 1000*(t_lp+t_ev)/n))
print('counts seen: %s' % sorted(set(c for c in counts if c is not None)))
print('None (unevaluable): %d of %d' % (sum(1 for c in counts if c is None), n))
tot = 4621728 * (t_lp+t_ev)/n
print('\nEXTRAPOLATED for 4,621,728 chambers: %.0f core-hours (%.1f days on 12 cores)'
      % (tot/3600, tot/3600/24/12))
