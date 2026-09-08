#!/usr/bin/env python3
"""What are the golden 67's 12 EXTRA walls?

`wall_sharing.py`: the octahedral 67's 60 tight condition labels are ALL tight at
the golden 67 too, which has 72. The difference of 12 is the first structural
quantity all session to separate the two maximisers -- symmetry, size,
codimension and field each failed to (Postscripts 127, 129).

Both are 3-cube with cube 0 the identity, so the label spaces coincide and the
comparison is meaningful (unlike the off-diagonal entries between differently
indexed configurations, which understate sharing).

A label is (frame i, group of (cube j, normal k, sign s)):
  group size 1  -> a single face normal has L1 norm 1, i.e. a face direction of
                   cube j lies along an axis of cube i: ALIGNMENT
  group size 2  -> two normals meet the L1 unit ball together: a pair coincidence
"""
import itertools, sys
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from fractions import Fraction as F
import dimension as D
from qfield import Q
from wall_sharing import labels

OCT=[((1,0),(0,0),(0,0),(0,0)),((1,0),(1,0),(0,1),(0,0)),((-1,0),(1,0),(0,1),(0,0))]
GOL=[((1,0),(0,0),(0,0),(0,0)),((2,0),(1,1),(-1,1),(0,0)),((-2,0),(1,1),(-1,1),(0,0))]
lo=labels(OCT,2); lg=labels(GOL,5)
print('octahedral %d labels, golden %d labels'%(len(lo),len(lg)))
print('octahedral \\ golden : %d   (must be 0 if containment holds)'%len(lo-lg))
extra=sorted(lg-lo)
print('golden EXTRA          : %d'%len(extra))
print()
from collections import Counter
print('extra by group size :',dict(Counter(len(g) for _,g in extra)))
print('extra by frame      :',dict(Counter(i for i,_ in extra)))
print('extra by cubes named:',dict(Counter(tuple(sorted({i}|{x[0] for x in g})) for i,g in extra)))
print()
print('the 12 extra labels:')
for i,g in extra:
    print('   frame %d  group %s'%(i,' + '.join('cube%d n%d %+d'%(c,k,s) for c,k,s in g)))
print()
sh_o=Counter(len(g) for _,g in lo); sh_g=Counter(len(g) for _,g in lg)
print('octahedral by group size:',dict(sh_o))
print('golden     by group size:',dict(sh_g))
