#!/usr/bin/env python3
"""Exact arithmetic in Q(sqrt3, sqrt5), basis (1, r3, r5, r15).  [P334]

Written for the K4 corner-sharing compound, whose coordinates are p,q = (sqrt3 +- sqrt15)/6.

ZERO-TESTING IS EXACT: 1, sqrt3, sqrt5, sqrt15 are linearly independent over Q, so an element
is zero iff all four rational coordinates are zero -- a tuple comparison, no tolerance.
SIGN of a nonzero element comes from a numeric evaluation, which is safe precisely because
nonzero-ness was certified exactly first.  This is the division of labour the float path got
wrong: it used a tolerance to decide equality, below its own noise floor.

COST OF LEARNING THIS, in one afternoon.  A 50-digit float version of the same triple-point
count returned T3 = 8 for the new compound.  Its oracle -- the same code on the n = 4 record,
where T3 = 128 is known -- returned 38, then 90 after a containment fix, and never 128:
`Matrix.inv()` on Float entries loses far more than the 1e-30 tolerance the test assumed.
Rewritten over this field the oracle returns 128 exactly and the compound returns 74.
**The tolerance had been set below the noise floor of the arithmetic underneath it.**
"""
from fractions import Fraction as F
import mpmath as mp
mp.mp.dps = 60
R3, R5, R15 = mp.sqrt(3), mp.sqrt(5), mp.sqrt(15)

class K:
    __slots__=('a','b','c','d')
    def __init__(self,a=0,b=0,c=0,d=0):
        self.a,self.b,self.c,self.d=F(a),F(b),F(c),F(d)
    def __add__(s,o): o=K.lift(o); return K(s.a+o.a,s.b+o.b,s.c+o.c,s.d+o.d)
    __radd__=__add__
    def __neg__(s): return K(-s.a,-s.b,-s.c,-s.d)
    def __sub__(s,o): return s+(-K.lift(o))
    def __rsub__(s,o): return K.lift(o)+(-s)
    def __mul__(s,o):
        o=K.lift(o)
        # (a+b r3+c r5+d r15)(a'+b' r3+c' r5+d' r15)
        a=s.a*o.a+3*s.b*o.b+5*s.c*o.c+15*s.d*o.d
        b=s.a*o.b+s.b*o.a+5*(s.c*o.d+s.d*o.c)
        c=s.a*o.c+s.c*o.a+3*(s.b*o.d+s.d*o.b)
        d=s.a*o.d+s.d*o.a+s.b*o.c+s.c*o.b
        return K(a,b,c,d)
    __rmul__=__mul__
    def conj3(s): return K(s.a,-s.b,s.c,-s.d)
    def conj5(s): return K(s.a,s.b,-s.c,-s.d)
    def inv(s):
        t=s.conj3()*s.conj5()*(s.conj3().conj5())      # product of the three conjugates
        n=(s*t)                                        # rational
        assert n.b==0 and n.c==0 and n.d==0, n
        return t*K(F(1,1)/n.a)
    def __truediv__(s,o): return s*K.lift(o).inv()
    def __eq__(s,o):
        o=K.lift(o); return (s.a,s.b,s.c,s.d)==(o.a,o.b,o.c,o.d)
    def __hash__(s): return hash((s.a,s.b,s.c,s.d))
    def is_zero(s): return s.a==0 and s.b==0 and s.c==0 and s.d==0
    def num(s):
        f=lambda x: mp.mpf(x.numerator)/mp.mpf(x.denominator)
        return f(s.a)+f(s.b)*R3+f(s.c)*R5+f(s.d)*R15
    def sign(s):
        if s.is_zero(): return 0                        # EXACT
        v=s.num()
        if abs(v) < mp.mpf('1e-40'):
            raise AssertionError('nonzero element too small to sign at 60 dps: %s'%(s,))
        return 1 if v>0 else -1
    def __repr__(s): return 'K(%s,%s,%s,%s)'%(s.a,s.b,s.c,s.d)
    @staticmethod
    def lift(o): return o if isinstance(o,K) else K(o)

def sq3(): return K(0,1,0,0)
def sq5(): return K(0,0,1,0)
