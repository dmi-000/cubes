#!/usr/bin/env python3
"""Ends of the n=10 3913 continuum, along the tangent solved in `arc_eps.py`.

`arc_eps.py` found 3913 has exactly one verified tangent in the last-cube slice,
(15, 220, 86) — so n=10 is a continuum, the last row of [OQ 13] with no path. This
solves its ends the way [P187]/[P189] solved the others: every W4 quadratic on the
line, exact roots, walk outward probing the simplest rational between consecutive
roots, then build the end exactly in Z[sqrt d] and count there.

Watch for: the other six tower ends all drop by EXACTLY 2 ([P189]). Two more data
points either extend that census or break it.
"""
import sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from solve_more_ends import ends_of

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C9 = BASE + [(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57)]
# tenth cube (19,-2,15,24) -> Cayley (-2/19, 15/19, 24/19)
a0 = [F(-2,19), F(15,19), F(24,19)]
dv = [F(15), F(220), F(86)]

ends_of(C9, a0, dv, 3913, 'n=10 3913, tangent (15,220,86)')
