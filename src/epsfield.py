#!/usr/bin/env python3
"""An ordered field containing an infinitesimal, for exact "just outside this point" tests.

METHODS: an infinitesimal is exact; a small number is a sample. Displacing a configuration
by 2^-20 answers "what is the signature AT 2^-20", not "what is it just outside the
stratum" -- and the two differ whenever the geometry is narrower than the step. Worse, a
sweep over 2^-4, 2^-8, 2^-14, 2^-20 that returns the same value at every scale cannot
distinguish convergence from CO-LOCATION: all four displacements may sit in one cell.

Elements are polynomials in a positive infinitesimal e over Z, ordered by the sign of the
LOWEST-degree nonzero coefficient -- p > 0 iff p(e) > 0 for all sufficiently small e > 0.
No truncation is used: the degree bound below shows nothing ever grows, so the arithmetic is
exact rather than approximate.

DEGREE BOUND, verified before use because truncation that discards a nonzero leading term
makes the sign predicate answer 0 for a nonzero quantity -- a wrong answer, not a crash:

    quaternion q + e*v                      degree 1
    face-plane coefficients (quadratic in q)       2
    3x3 determinant of those                       6
    Cramer numerators                              6
    point identity, cross-multiplied              12
    face test  M.num  vs  n*det                    8

Bounded at 12. Degrees never exceed that, so exact arithmetic stays cheap -- and cheaper
than the integers it replaces, which reach ~10^54 at 2^-20.
"""
from fractions import Fraction as F
from math import gcd

ZERO = ()


def trim(c):
    i = len(c)
    while i and c[i-1] == 0:
        i -= 1
    return tuple(c[:i])


def const(n):
    return trim((int(n),))


def padd(a, b):
    n = max(len(a), len(b))
    return trim([ (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n) ])


def pneg(a):
    return tuple(-x for x in a)


def psub(a, b):
    return padd(a, pneg(b))


def pmul(a, b):
    if not a or not b:
        return ZERO
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i+j] += x * y
    return trim(out)


def psign(a):
    """sign of a(e) for all sufficiently small e > 0: the lowest nonzero coefficient"""
    for c in a:
        if c:
            return 1 if c > 0 else -1
    return 0


def pgcd(a, b):
    """monic gcd over Q, returned as a primitive integer polynomial"""
    A = [F(x) for x in a]; B = [F(x) for x in b]
    while B:
        while B and B[-1] == 0:
            B.pop()
        if not B:
            break
        # A mod B
        while len(A) >= len(B) and any(A):
            while A and A[-1] == 0:
                A.pop()
            if len(A) < len(B):
                break
            f = A[-1] / B[-1]; s = len(A) - len(B)
            for i in range(len(B)):
                A[s+i] -= f * B[i]
            while A and A[-1] == 0:
                A.pop()
        A, B = B, A
    if not A:
        return const(1)
    den = 1
    for x in A:
        den = den * x.denominator // gcd(den, x.denominator)
    ints = [int(x * den) for x in A]
    g = 0
    for x in ints:
        g = gcd(g, abs(x))
    ints = [x // (g or 1) for x in ints]
    if ints[-1] < 0:
        ints = [-x for x in ints]
    return trim(ints)


def pdivexact(a, b):
    """a // b where the division is known to be exact"""
    if not a:
        return ZERO
    A = [F(x) for x in a]; B = [F(x) for x in b]
    q = [F(0)] * (len(A) - len(B) + 1)
    for i in range(len(q) - 1, -1, -1):
        c = A[i + len(B) - 1] / B[-1]
        q[i] = c
        if c:
            for j in range(len(B)):
                A[i+j] -= c * B[j]
    assert not any(A), 'pdivexact: remainder is nonzero'
    return trim([int(x) for x in q])


def canon_point(t):
    """canonical form of a projective 4-tuple of polynomials -- so equal points hash equal.

    Dividing only by the integer content is NOT enough: two triples meeting at the same
    point can produce tuples differing by a POLYNOMIAL factor, which would split one point
    into several and undercount its multiplicity. The polynomial gcd is the whole reason
    this function exists.
    """
    g = ZERO
    for p in t:
        g = pgcd(g, p) if g else p
    if len(g) > 1:
        t = tuple(pdivexact(p, g) for p in t)
    ic = 0
    for p in t:
        for c in p:
            ic = gcd(ic, abs(c))
    if ic > 1:
        t = tuple(trim([c // ic for c in p]) for p in t)
    if psign(t[3]) < 0:                 # fix the sign via the denominator
        t = tuple(pneg(p) for p in t)
    return t
