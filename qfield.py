#!/usr/bin/env python3
"""Exact arithmetic in Q(sqrt d), enough to run the coincidence machinery on the
two 67s -- the only maximisers every crossing-based result so far has skipped,
because `crossing_set` is rational-only.

An element is a + b*sqrt(d) with a, b exact Fractions.  What the crossing test
needs beyond the ring operations is EXACT SIGN, since it asks whether a
determinant is zero and whether a parameter lies in [0,1]; comparing a + b*sqrt(d)
to zero reduces to comparing a^2 with b^2*d once the signs of a and b differ.
"""
from fractions import Fraction as F

class Q:
    __slots__ = ('a', 'b', 'd')
    def __init__(self, a=0, b=0, d=0):
        self.a = F(a); self.b = F(b); self.d = d
    def __repr__(self):
        return '%s+%s√%d' % (self.a, self.b, self.d)
    def _w(self, o):
        return o if isinstance(o, Q) else Q(o, 0, self.d)
    def __add__(s, o):
        o = s._w(o); return Q(s.a+o.a, s.b+o.b, s.d or o.d)
    __radd__ = __add__
    def __neg__(s): return Q(-s.a, -s.b, s.d)
    def __sub__(s, o): return s + (-s._w(o))
    def __rsub__(s, o): return s._w(o) + (-s)
    def __mul__(s, o):
        o = s._w(o); d = s.d or o.d
        return Q(s.a*o.a + s.b*o.b*d, s.a*o.b + o.a*s.b, d)
    __rmul__ = __mul__
    def inv(s):
        n = s.a*s.a - s.b*s.b*s.d
        if n == 0: raise ZeroDivisionError
        return Q(s.a/n, -s.b/n, s.d)
    def __truediv__(s, o): return s * s._w(o).inv()
    def __rtruediv__(s, o): return s._w(o) * s.inv()
    def is_zero(s): return s.a == 0 and s.b == 0
    def sign(s):
        """exact sign of a + b*sqrt(d)"""
        if s.b == 0: return (s.a > 0) - (s.a < 0)
        if s.a == 0: return (s.b > 0) - (s.b < 0)
        if s.a > 0 and s.b > 0: return 1
        if s.a < 0 and s.b < 0: return -1
        # opposite signs: compare a^2 with b^2 d, sign follows the larger term
        lhs = s.a*s.a; rhs = s.b*s.b*s.d
        if lhs == rhs: return 0
        bigger_is_a = lhs > rhs
        return (1 if s.a > 0 else -1) if bigger_is_a else (1 if s.b > 0 else -1)
    def __eq__(s, o): return (s - s._w(o)).is_zero()
    def __lt__(s, o): return (s - s._w(o)).sign() < 0
    def __le__(s, o): return (s - s._w(o)).sign() <= 0
    def __gt__(s, o): return (s - s._w(o)).sign() > 0
    def __ge__(s, o): return (s - s._w(o)).sign() >= 0
    def __float__(s): return float(s.a) + float(s.b)*(s.d ** 0.5)
    def __hash__(s): return hash((s.a, s.b, s.d))

def rot(q):
    """rotation matrix over Q(sqrt d) from a quaternion of Q elements"""
    w, x, y, z = q
    n = w*w + x*x + y*y + z*z
    return [[(w*w+x*x-y*y-z*z)/n, 2*(x*y-w*z)/n, 2*(x*z+w*y)/n],
            [2*(x*y+w*z)/n, (w*w-x*x+y*y-z*z)/n, 2*(y*z-w*x)/n],
            [2*(x*z-w*y)/n, 2*(y*z+w*x)/n, (w*w-x*x-y*y+z*z)/n]]

def edges(R):
    out = []
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        for sb in (1, -1):
            for sc in (1, -1):
                P = [R[i][b]*sb + R[i][c]*sc - R[i][a] for i in range(3)]
                D = [R[i][a]*2 for i in range(3)]
                out.append((P, D))
    return out

def det3(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))

def real_crossing(P1, D1, P2, D2, d):
    W = [P2[i]-P1[i] for i in range(3)]
    if not det3(D1, D2, W).is_zero():
        return False
    one = Q(1, 0, d); zero = Q(0, 0, d)
    for i, j in ((0,1), (0,2), (1,2)):
        den = D1[i]*(zero-D2[j]) - (zero-D2[i])*D1[j]
        if den.is_zero(): continue
        s = (W[i]*(zero-D2[j]) - (zero-D2[i])*W[j]) / den
        t = (D1[i]*W[j] - W[i]*D1[j]) / den
        return zero <= s <= one and zero <= t <= one
    return False

def crossing_set(quats, d):
    import itertools, collections
    Rs = [rot(q) for q in quats]
    Es = [edges(R) for R in Rs]
    out = []
    for i, j in itertools.combinations(range(len(quats)), 2):
        for ei, (P1, D1) in enumerate(Es[i]):
            for ej, (P2, D2) in enumerate(Es[j]):
                if real_crossing(P1, D1, P2, D2, d):
                    out.append((i, ei, j, ej))
    return out
