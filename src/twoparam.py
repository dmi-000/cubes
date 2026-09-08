#!/usr/bin/env python3
"""SOLVE for which continuum members admit a degenerate extension locus.

METHODS 12: a 13-pair between a new cube and base cube b is not a predicate but a
CURVE, q = b.(1, t*a) for a a body diagonal -- so the new cube's locus is the line
through b with direction b*(0,a), i.e. the 2-plane span{b, b*(0,a)}.

Two such conditions generically meet TRANSVERSALLY, giving isolated points; METHODS
12 measured those as WORSE than random search (best 2737). The prize is the
DEGENERATE case, where the two curves coincide and a one-parameter family survives
-- that is where the 2785 ninth cube was found, as q(227/889) on one of three
coincident systems.

`member723.py` samples the continuum (8 points, four distinct answers). This solves
it instead. With the base member free, the coincidence condition is

    rank [ b_i | b_i*(0,a1) | b6(u) | b6(u)*(0,a2) ] <= 2

whose 3x3 minors are polynomials in u alone. The members admitting a degenerate
extension locus are exactly their common roots -- finitely many, exact, no sweep.

CAVEAT CARRIED FORWARD FROM METHODS 12: a solver that reports "no unique solution"
discards precisely the cases worth having. Degenerate branches are the output here,
not an error. And this LOCATES; it does not SCORE -- every root still needs the
engine, because coincidence count ranks candidates wrongly (METHODS 6).
"""
import sys
import sympy as sp

B = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
DIAG = [(1,1,1),(1,1,-1),(1,-1,1),(-1,1,1)]


def qmul(x, y):
    a,b,c,d = x; e,f,g,h = y
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)


def plane(b, a):
    """span{b, b*(0,a)} — the 2-plane of the 13-pair locus about axis a."""
    return [sp.Matrix(4,1,list(b)), sp.Matrix(4,1,list(qmul(b,(0,)+tuple(a))))]


def solve_members(u, base=None, member=None):
    """Parameter values where some (base cube, axis, axis) pair gives coincident
    loci for the NEXT cube.

    base   : the fixed cubes (default the 723 five)
    member : callable p -> the continuum member's quaternion (default 723's
             half-line (1,u,u,u)). For 2785 the continuum is
             q(t) = (3,3,7,3).(1, t*(-1,-1,1)), verified by reproducing the
             recorded ninth cube (56,56,55,56) at t = 227/889 (METHODS 12).
    """
    B_ = base if base is not None else B
    b6 = member(u) if member is not None else (1, u, u, u)
    hits = []
    for i, bi in enumerate(B_):
        for a1 in DIAG:
            P = plane(bi, a1)
            for a2 in DIAG:
                Q = plane(b6, a2)
                M = sp.Matrix.hstack(P[0], P[1], Q[0], Q[1])
                minors = [M[rs, cs].det()
                          for rs in [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]
                          for cs in [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]]
                minors = [sp.expand(m) for m in minors if sp.expand(m) != 0]
                if not minors:
                    hits.append(('IDENTICALLY coincident', i, a1, a2, None))
                    continue
                sol = sp.solve(minors, u, dict=True)
                for srt in sol:
                    val = srt.get(u)
                    if val is not None and val.is_real:
                        hits.append(('coincident at u', i, a1, a2, sp.nsimplify(val)))
    return hits


if __name__ == '__main__':
    u = sp.Symbol('u')
    hits = solve_members(u)
    print('degenerate (coincident-locus) members of the 723 continuum:')
    if not hits:
        print('   none — every (base, axis, axis) pair meets transversally')
    seen = set()
    for kind, i, a1, a2, val in hits:
        k = (i, a1, a2, val)
        if k in seen: continue
        seen.add(k)
        print('   base cube %d  axes %s / %s   ->  %s %s'
              % (i, a1, a2, kind, '' if val is None else val))
