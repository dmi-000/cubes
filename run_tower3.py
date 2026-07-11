#!/usr/bin/env python3
"""Depth-3 tower Q(sqrt2,sqrt3,sqrt5) = T5 adjoin sqrt3, for task 1(b) at
R=90deg about (1,1,1) (octahedral Qsqrt2 + golden Qsqrt5, mixed, on the 90deg
wall).  Tests whether the exact 90deg wall point BEATS the 699 tie found at
60deg."""
import sys, time
from fractions import Fraction as Fr
sys.path.insert(0, '/Users/dmi/carroll'); sys.path.insert(0, '/tmp')
from slide3_q2 import Q2, ONE2, ZERO2, Rx45
from golden_rotations import Rot, B
from golden_six import golden_five
from tower2 import make_tower, exact_count, embed_rot_q2, embed_rot_q5

T5 = make_tower(5)

class E:
    """a + b*sqrt3, a,b in T5.  Q(sqrt2,sqrt3,sqrt5)."""
    __slots__ = ('a','b'); D = 3
    def __init__(s, a, b=None):
        s.a = a if isinstance(a, T5) else T5(a)
        s.b = (b if isinstance(b, T5) else T5(b)) if b is not None else T5(0)
    def __add__(s,o):
        o=o if isinstance(o,E) else E(o); return E(s.a+o.a, s.b+o.b)
    __radd__=__add__
    def __sub__(s,o):
        o=o if isinstance(o,E) else E(o); return E(s.a-o.a, s.b-o.b)
    def __neg__(s): return E(-s.a,-s.b)
    def __mul__(s,o):
        o=o if isinstance(o,E) else E(o)
        return E(s.a*o.a + 3*(s.b*o.b), s.a*o.b + s.b*o.a)
    __rmul__=__mul__
    def __truediv__(s,o):
        o=o if isinstance(o,E) else E(o)
        den=o.a*o.a - 3*(o.b*o.b)
        return E((s.a*o.a-3*(s.b*o.b))/den, (s.b*o.a-s.a*o.b)/den)
    def sign(s):
        sa,sb=s.a.sign(),s.b.sign()
        if sb==0: return sa
        if sa==0: return sb
        if sa==sb: return sa
        t=s.a*s.a-3*(s.b*s.b); st=t.sign()
        assert st!=0,'sqrt3 fell into Q(sqrt2,sqrt5)'
        return st if sa>0 else -st
    def coords(s): return s.a.coords()+s.b.coords()
    def __eq__(s,o): return isinstance(o,E) and s.a==o.a and s.b==o.b
    def __hash__(s): return hash(s.coords())
    def __float__(s): return float(s.a)+float(s.b)*3**0.5

def emb5(t5): return E(t5, T5(0))
def orbit(seed,C): return [seed, C*seed, C*(C*seed)]

B_q2 = Rot([[ZERO2,ZERO2,ONE2],[ONE2,ZERO2,ZERO2],[ZERO2,ONE2,ZERO2]])
oct_q2 = orbit(Rx45(), B_q2)
oct_E = [Rot([[emb5(embed_rot_q2(R,T5).m[i][j]) for j in range(3)] for i in range(3)]) for R in oct_q2]
g = golden_five()
dod_q5 = orbit(g[1], B)
dod_E = [Rot([[emb5(embed_rot_q5(R,T5).m[i][j]) for j in range(3)] for i in range(3)]) for R in dod_q5]

# R90 about (1,1,1): entries 1/3 +- sqrt3/3
th = E(T5(Q2(Fr(1,3))), T5(0))
s3 = E(T5(0), T5(Q2(Fr(1,3))))
R90 = Rot([[th, th-s3, th+s3],[th+s3, th, th-s3],[th-s3, th+s3, th]])
# orthonormality quick check
for i in range(3):
    for j in range(3):
        d=sum((R90.m[k][i]*R90.m[k][j] for k in range(3)), E(0)) - (E(1) if i==j else E(0))
        assert d.sign()==0
print('R90 orthonormal OK', flush=True)

# gate: single octahedral in E
t0=time.time(); tot,bd=exact_count(oct_E, E); print(f'gate single octahedral (E): {tot} {dict(sorted(bd.items()))} ({time.time()-t0:.1f}s)', flush=True)

t0=time.time()
cfg = oct_E + [R90*r for r in dod_E]
tot,bd=exact_count(cfg, E)
print(f'TASK 1(b) R=90 about (1,1,1) [Q(sqrt2,sqrt3,sqrt5)]: total={tot} by_depth={dict(sorted(bd.items()))} ({time.time()-t0:.1f}s)', flush=True)
