#!/usr/bin/env python3
"""Close the bracket: locate the n=10 extension wall by SIMPLEST-RATIONAL bisection.

The wall sits in t in (3,6) on the line q(t) = (12-t)A + tB.  Ordinary bisection
fails on cost, not on content: t = 9/2 doubles the quaternion height to ~2.7M and
the engine's budget stops around 1e6.  That is the failure mode the project already
diagnosed -- "a refusal may be about your representative, not about the question" --
and the fix is its own: take the SIMPLEST rational in the interval (lowest
denominator, by Stern-Brocot descent) rather than the midpoint, since the cost of
the representative is a free choice and not a property of the object.

Each step narrows the bracket and reports the height actually used, so the point at
which cost (not geometry) stops the descent is visible rather than inferred.

This still yields a BRACKET, tighter -- the wall is an algebraic number and the
exact locus needs its polynomial.  What the tight bracket buys is the ability to
identify WHICH coincidence is going tight, which is what that polynomial is.
"""
import math, subprocess, os
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__)); ENG=os.path.join(HERE,"cube_regions_q2w")   # wide: cube_regions_n refuses these heights
NARROW=os.path.join(HERE,"cube_regions_n")
BASE8=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
       (4,-3,-4,-4),(168,-168,168,-415)]
A=(88787,-9061,74275,113786); B=(88726,-8954,74074,113960); TENTH=(6555,6555,6497,6555)

def red(q):
    g=0
    for v in q: g=math.gcd(g,abs(v))
    return tuple(v//g for v in q) if g else q

def at(t):
    """the tenth-cube configuration at parameter t (Fraction), cleared to integers"""
    num=t.numerator; den=t.denominator
    q=red(tuple((12*den-num)*a+num*b for a,b in zip(A,B)))
    return q, max(abs(v) for v in q)

def count(t):
    """count at t, or (None, h) if genuinely UNEVALUATED.

    The narrow engine returns "degenerate plane triple" at some of these points --
    an engine refusal, NOT a budget limit and NOT a negative.  An earlier version
    guarded on height and recorded such points as stops, which is the
    "unevaluable is not a negative result" trap: t = 13/3 was scored as budget-
    stopped when the wide engine counts it as 3925.
    """
    q,h=at(t)
    spec=";".join(",".join(str(v) for v in x) for x in BASE8+[q,TENTH])
    o=subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i=o.find('"bounded":')
    return (int(o[i+10:o.find(",",i)]) if i>=0 else None), h

def simplest_between(lo, hi):
    """simplest rational STRICTLY between lo and hi; hi=None means +infinity.

    Stern-Brocot descent.  The earlier version divided by (lo - floor(lo)) and so
    failed whenever lo was an integer -- it reported "no simpler rational inside
    (4,5)" when 9/2 sits there.  An integer endpoint is the COMMON case here, since
    every accepted probe becomes an endpoint.
    """
    fl = math.floor(lo)
    if hi is None:
        return F(fl + 1)
    if fl + 1 < hi:
        return F(fl + 1)
    a, b = lo - fl, hi - fl                 # 0 <= a < b <= 1
    inner = simplest_between(F(1) / b, None if a == 0 else F(1) / a)
    return fl + F(1) / inner

lo,hi=F(3),F(6)
print(f"{'bracket':>26} {'probe t':>10} {'height':>10} {'count':>7}")
for step in range(14):
    t=simplest_between(lo,hi)
    if t<=lo or t>=hi: print("  no simpler rational strictly inside; descent exhausted"); break
    c,h=count(t)
    print(f"({lo}, {hi})".rjust(26)+f" {str(t):>10} {h:>10} {str(c):>7}"
          + ("  BUDGET" if c is None else ""))
    if c is None:
        print(f"  stopped by engine budget at height {h}, not by geometry"); break
    if c==3925: lo=t
    else: hi=t
print(f"\nfinal bracket for the wall: t in ({lo}, {hi})   width {hi-lo}")
print("the wall is an algebraic number; this is a rational bracket, not the locus.")
