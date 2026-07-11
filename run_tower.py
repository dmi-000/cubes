#!/usr/bin/env python3
import sys, time
from fractions import Fraction as Fr
sys.path.insert(0, '/Users/dmi/carroll')
sys.path.insert(0, '/tmp')
from slide3_q2 import Q2, ONE2, ZERO2, Rx45
from golden_rotations import Rot
from golden_six import golden_five
from tower2 import (make_tower, exact_count, embed_q2, embed_q5,
                    embed_rot_q2, embed_rot_q5, assert_orthonormal)

def q2(x): return Q2(Fr(x))
# rational rotations built with Q2 entries (b=0)
B_q2 = Rot([[ZERO2, ZERO2, ONE2],[ONE2, ZERO2, ZERO2],[ZERO2, ONE2, ZERO2]])
R60_q2 = Rot([[q2(Fr(2,3)), q2(Fr(-1,3)), q2(Fr(2,3))],
              [q2(Fr(2,3)), q2(Fr(2,3)),  q2(Fr(-1,3))],
              [q2(Fr(-1,3)), q2(Fr(2,3)), q2(Fr(2,3))]])

def orbit(seed, C): return [seed, C*seed, C*(C*seed)]

def show(name, rots, T):
    t0=time.time(); tot,bd=exact_count(rots, T); dt=time.time()-t0
    ok = (tot%2==1 or True)
    print(f'{name}: total={tot} by_depth={dict(sorted(bd.items()))} ({dt:.1f}s)', flush=True)
    return tot,bd

# ---------------- Q(sqrt2, sqrt3): task 1(a) 90 deg ----------------
T3 = make_tower(3)
oct_q2 = orbit(Rx45(), B_q2)
oct_T3 = [embed_rot_q2(R, T3) for R in oct_q2]
# gate
print('=== Q(sqrt2,sqrt3) gates ===')
show('single octahedral triple (embed T3)', oct_T3, T3)      # expect 67
# R90 = 90 about (1,1,1): entries 1/3 +- sqrt3/3, sqrt3-part coeff = 1/3
th = T3(Q2(Fr(1,3)), Q2(0))          # 1/3
s3 = T3(Q2(0), Q2(Fr(1,3)))          # sqrt3/3 = 1/sqrt3
R90 = Rot([[th,      th - s3,  th + s3],
           [th + s3, th,       th - s3],
           [th - s3, th + s3,  th]])
assert_orthonormal(R90, T3)
print('\n=== TASK 1(a): octahedral + 90deg-about-(1,1,1)*octahedral, Q(sqrt2,sqrt3) ===')
show('R=90 about (1,1,1)', oct_T3 + [R90*r for r in oct_T3], T3)

# ---------------- Q(sqrt2, sqrt5): task 1(b) octahedral+golden ------------
T5 = make_tower(5)
g = golden_five()
dod_q5 = orbit(g[1], __import__('golden_rotations').B)   # C-orbit of golden cube1
oct_T5 = [embed_rot_q2(R, T5) for R in oct_q2]
dod_T5 = [embed_rot_q5(R, T5) for R in dod_q5]
R60_T5 = embed_rot_q2(R60_q2, T5)
print('\n=== Q(sqrt2,sqrt5) gates ===')
show('single octahedral triple (embed T5)', oct_T5, T5)      # 67
show('single golden C-orbit (embed T5)', dod_T5, T5)         # 67
print('\n=== TASK 1(b): octahedral(Qsqrt2) + golden(Qsqrt5), R about (1,1,1), Q(sqrt2,sqrt5) ===')
show('R=identity (direct overlay)', oct_T5 + dod_T5, T5)
show('R=60 about (1,1,1)', oct_T5 + [R60_T5*r for r in dod_T5], T5)
