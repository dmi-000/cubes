#!/usr/bin/env python3
"""Task 1(a): octahedral triple (Q sqrt2) overlaid with R*itself, R = exact
rotation about (1,1,1).  120 deg (=B, rational) and 60 deg (=(3,1,1,1)
rational) both stay in Q(sqrt2), counted with slide3_q2.exact_count_q2.
Plus gates.  90 deg (needs sqrt3) handled in run_tower.py."""
import sys, time
from fractions import Fraction as Fr
sys.path.insert(0, '/Users/dmi/carroll')
from slide3_q2 import Q2, ONE2, ZERO2, Rx45, exact_count_q2
from golden_rotations import Rot

def q2(x): return Q2(Fr(x))

# B = 120 about (1,1,1), rational permutation, Q2 entries
B = Rot([[ZERO2, ZERO2, ONE2],[ONE2, ZERO2, ZERO2],[ZERO2, ONE2, ZERO2]])
# R60 = 60 about (1,1,1) = rot_from_quat(3,1,1,1), rational
R60 = Rot([[q2(Fr(2,3)), q2(Fr(-1,3)), q2(Fr(2,3))],
           [q2(Fr(2,3)), q2(Fr(2,3)),  q2(Fr(-1,3))],
           [q2(Fr(-1,3)), q2(Fr(2,3)), q2(Fr(2,3))]])

S = Rx45()
def orbit(seed): return [seed, B*seed, B*(B*seed)]
tri_oct = orbit(S)

def show(name, rots):
    t0=time.time(); tot,bd=exact_count_q2(rots); dt=time.time()-t0
    print(f'{name}: total={tot} by_depth={dict(sorted(bd.items()))} ({dt:.1f}s)', flush=True)
    return tot,bd

print('=== GATES (Q sqrt2) ===')
show('single octahedral triple', tri_oct)                     # expect 67
show('coincident pair R=identity', tri_oct + tri_oct)         # expect 67
show('R=120(=B) octahedral (degenerate coincidence)', tri_oct + [B*r for r in tri_oct])  # expect 67

print('\n=== TASK 1(a): octahedral + R*octahedral, R about (1,1,1) ===')
show('R=60 about (1,1,1) [rational, Q sqrt2]', tri_oct + [R60*r for r in tri_oct])
