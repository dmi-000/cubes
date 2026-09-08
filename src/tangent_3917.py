#!/usr/bin/env python3
"""Re-solve the tangent AT the new n=10 record 3917, not at its predecessor.

[P190] solved the tangent at 3913 and a sweep along it found 3917 ([P191]). 3917 is a
DIFFERENT point: its active walls differ, so its locus may have a different tangent,
more than one, or none. Re-solving there is the natural next step and the one that
says whether the line that produced it is the whole story.

Same method as `arc_eps.py`: null spaces of rank-2 subsets of the wall normals in the
last-cube slice, verified with the eps engine (both signs, exact limit, no step size),
gated on recovering BOTH of 727 arc D's known tangents.
"""
import sys
sys.path.insert(0, '.')
from arc_eps import tangents_eps, C6

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C9 = BASE + [(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57)]
NEW = C9 + [(88787, -9061, 74275, 113786)]          # 3917, P191
OLD = C9 + [(19, -2, 15, 24)]                       # 3913, P181

tangents_eps(C6, 'GATE  n=6 727 (two known tangents)', expect=2)
t_old = tangents_eps(OLD, 'n=10 3913 (P190, for comparison)')
t_new = tangents_eps(NEW, 'n=10 3917 — the NEW record')

print('\ntangents at 3913: %s' % (t_old,))
print('tangents at 3917: %s' % (t_new,))
if not t_new:
    print('same locus? UNDETERMINED — no verified tangent at 3917; an empty result is '
          'not evidence of absence (see the rank note above)')
else:
    print('same locus? %s' % ('yes — identical tangent set' if t_old == t_new else
                              'NO — different tangents, so a different locus'))
