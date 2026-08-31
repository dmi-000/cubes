#!/usr/bin/env python3
"""How many dimensions does the 2785 locus actually have?

Prompted by "so 2785 is also a 2-d region." The subset data in [P194] does NOT show
that — the 9-subset counting 2785 is the one that DROPS the moving tenth cube, so it
does not move and its constancy is forced. But [P184] predicts it independently:
preserving dimension = max(0, deficit - 1), and 2785 has deficit 4, predicting 3.

Every end solved for 2785 in [P187] traced ONE line (the k-family). If the locus is
3-dimensional, that line is a slice, and its "ends" are the ends of the slice.

Method as in `arc_eps.py`/`dim3917.py`: tangent candidates from the wall normals in
the last-cube slice, verified with eps both signs; then combinations, to tell a
surface from a node. Gated on 727 arc D, a known NODE.
"""
import sys
sys.path.insert(0, '.')
from arc_eps import tangents_eps, C6
from dim3917 import verdict          # reuses the combination test and its gate

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C9=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(56,56,55,56)]   # 2785, k=56

t = tangents_eps(C9, 'n=9 2785 (deficit 4; P184 predicts preserving dim 3)')
print('\nverified tangents at 2785: %s' % (t,))
if len(t) >= 2:
    verdict(C9, tuple(t[0]), tuple(t[1]), 'n=9 2785 — surface or node?')
elif len(t) == 1:
    print('only ONE tangent verified in this 3-dimensional slice: the locus is at least'
          ' 1-dimensional here. P184 predicts 3 over the full 24-dimensional space, so'
          ' the remaining directions would move EARLIER cubes and are invisible in this'
          ' slice.')
else:
    print('no tangent verified in this slice — see the rank note in arc_eps.py')
