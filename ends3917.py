#!/usr/bin/env python3
"""Endpoints of the n=10 record 3917's locus, along both solved tangents.

`tangent_3917.py` found TWO verified tangents at 3917 — (1,-14,0) and (5,0,14) —
where 3913 had one. The locus is therefore at least 2-dimensional in the last-cube
slice, consistent with 3917's deficit of 6 and [P184]'s max(0, deficit-1) = 5.

Ends are solved per tangent line with the corrected machinery ([P192]): value-deduped
roots, BOTH wall types, unevaluable probes skipped and counted rather than treated as
stops, and the exact Z[sqrt d] form recovered only for the endpoint itself.
"""
import sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from solve_more_ends import ends_of

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C9=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57)]
Q=(88787,-9061,74275,113786)
a0=[F(Q[1],Q[0]), F(Q[2],Q[0]), F(Q[3],Q[0])]
for dv,lbl in (([F(1),F(-14),F(0)], 'tangent (1,-14,0)'),
               ([F(5),F(0),F(14)], 'tangent (5,0,14)')):
    ends_of(C9, a0, dv, 3917, 'n=10 3917, %s' % lbl)
