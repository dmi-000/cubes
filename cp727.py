#!/usr/bin/env python3
"""Characteristic polynomial of the 727 arrangement — the structure question.

P154 established: 393's arrangement sits inside 727's verbatim (18 of 27 walls,
projecting exactly), 1 wall is purely in the 3 new dimensions, and 8 walls COUPLE
the blocks -- so there is no product structure, yet chambers factor as exactly
62 x 74 544.

The well-posed question that leaves: does chi_393(t) divide chi_727(t)?  Both are
degree 15 (393's arrangement inflates by t^3), so the quotient would be a cubic g
with |g(-1)| = 62.  If it divides, "add one cube to the 393 configuration" has a
computable effect and n=7 becomes arithmetic rather than a campaign.

Memory, not time, is the risk here: `chambers` stores one int per (index, flat)
state and peaked at 0.15 GB over 3 390 547 states; `charpoly` stores a tuple of
Whitney counts per state instead.  Run where there is headroom.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from zaslavsky import charpoly

W, nc = walls_of(BASE + [(7, 14, 1, -5)])
w, tot = charpoly(W, label='727:')
json.dump({'label': '727', 'ambient': nc, 'whitney': list(w), 'chambers': tot},
          open(os.path.join(HERE, 'charpoly_727.json'), 'w'), indent=1)
print('chambers %s  (must equal 4,621,728: %s)'
      % ('{:,}'.format(tot), 'PASS' if tot == 4621728 else 'FAIL'))
