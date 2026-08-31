#!/usr/bin/env python3
"""Does a maximiser locus have a TANGENT here? Candidates solved, verified with eps.

Closes [OQ 13](OPEN_QUESTIONS.md)'s two remaining rows: 183 (n=4) and 3913 (n=10)
have no path established, so it is not known whether they are continua at all.

METHOD. A curve in the locus lies inside every wall it does not cross, so its tangent
is orthogonal to those walls' normals. The full active set OVER-CONSTRAINS — most
coincidence crossings do not change the count ([METHODS 7](METHODS.md)) — so
`tangent_finder.py` takes null spaces of rank-2 SUBSETS of the active normals and
verifies each. That part is reused wholesale.

WHAT IS CHANGED. `tangent_finder.subset_tangents` verifies by stepping +-1/64 and
+-1/1024. Both are finite, and today established what that costs: 1217's plateau is
0.00078 wide along its line, so a step of 1/64 or even 1/1024 can leave a genuine
plateau and reject a real tangent ([P188](LEDGER.md#p188)). Verification here is the
eps ENGINE instead — count(pt + eps*v) with eps a positive infinitesimal, both signs,
which is the exact limit and has no step to choose ([P184](LEDGER.md#p184)).

SCOPE, stated because a negative depends on it: only the LAST cube moves, a
3-dimensional slice of the 3(n-1)-dimensional gauge-fixed space. A locus needing
earlier cubes to move is invisible. This is the same slice in which 727's arc D was
found, so the gate below is like-for-like.

GATE: at the 727 record the naive full-rank test reports "0-dimensional" and is
WRONG — two independent directions preserve 727 there (arc D is a node). The method
must recover BOTH before any new answer counts.
"""
import itertools, sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from math import gcd
from qfield import Q
import dimension as D
from epscount import count_eps
from eps_null import walls_and_null

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C6 = BASE + [(7,14,1,-5)]
C4 = [BASE[i] for i in (0,1,2,4)]                     # n=4 = 183 (P162/P189)
C10 = BASE + [(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),(19,-2,15,24)]


def primitive(v):
    den = 1
    for x in v:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    iv = [int(F(x) * den) for x in v]
    g = 0
    for x in iv:
        g = gcd(g, abs(x))
    iv = [x // (g or 1) for x in iv]
    for x in iv:
        if x > 0: break
        if x < 0: iv = [-y for y in iv]; break
    return tuple(iv)


def null2(u, w):
    """the 1-dim null space of two 3-vectors, as a primitive integer direction"""
    c = (u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0])
    return primitive(c) if any(c) else None


def tangents_eps(cubes, label, expect=None):
    pt, walls, null, ncols = walls_and_null(cubes)
    rec = D.count_at(pt, len(cubes))
    tail = slice(ncols - 3, ncols)                      # last cube's coordinates
    # controls, both able to fail
    z = count_eps(pt, [Q(0,0,0)]*ncols, 0, cubes[0])
    if z is None:                       # narrow engine refuses on height, not on content
        z = count_eps(pt, [Q(0,0,0)]*ncols, 0, cubes[0], wide=True)
    wg = count_eps(pt, [Q(F(x),0,0) for x in walls[0]], 0, cubes[0])
    if wg is None:
        wg = count_eps(pt, [Q(F(x),0,0) for x in walls[0]], 0, cubes[0], wide=True)
    ok = (z == rec) and (wg is not None and wg != rec)
    print('\n%s: record %d, %d walls, ambient %d   CONTROLS zero->%s wall->%s  %s'
          % (label, rec, len(walls), ncols, z, wg, 'OK' if ok else 'FAIL'), flush=True)
    if not ok:
        print('   controls failed — nothing below would mean anything'); return []

    proj = []
    for g in walls:
        t = primitive(list(g)[tail])
        if t and t not in proj:
            proj.append(t)
    cands = []
    for u, w in itertools.combinations(proj, 2):
        c = null2(u, w)
        if c and c not in cands:
            cands.append(c)
    # If the normals in the slice span rank < 2, no PAIR has a 1-dimensional null
    # space and the loop above yields nothing — which is a limitation of the method,
    # not a negative. The orthogonal complement is then 2- or 3-dimensional, so a
    # basis of it is supplied directly. This is exactly the 3917 case: 2 normals,
    # parallel, complement of dimension 2, and "0 candidates" read as "no tangent".
    if not cands and proj:
        import sympy as sp
        M = sp.Matrix([list(v) for v in proj])
        for b in M.nullspace():
            d = primitive([sp.Rational(x) for x in b])
            if d and d not in cands:
                cands.append(d)
        print('   normals span rank %d < 2: using the %d-dimensional orthogonal '
              'complement directly' % (M.rank(), len(cands)), flush=True)
    if not cands and not proj:
        print('   NO wall normals in this slice — every direction is a candidate; '
              'not tested here', flush=True)
    print('   %d distinct wall normals in the last-cube slice, %d rank-2 candidates'
          % (len(proj), len(cands)), flush=True)

    good, unev = [], 0
    for c in cands:
        full = [F(0)]*(ncols-3) + [F(x) for x in c]
        vals = []
        for sgn in (1, -1):
            v = count_eps(pt, [Q(sgn*x, 0, 0) for x in full], 0, cubes[0])
            if v is None:
                v = count_eps(pt, [Q(sgn*x, 0, 0) for x in full], 0, cubes[0], wide=True)
            vals.append(v)
        if None in vals:
            unev += 1
        elif vals[0] == rec and vals[1] == rec:
            good.append(c)
    print('   VERIFIED tangents: %d   (%d candidates, %d UNEVALUATED — not negatives)'
          % (len(good), len(cands), unev), flush=True)
    for c in good:
        print('      %s' % (c,), flush=True)
    if expect is not None:
        print('   GATE: expected >= %d verified, got %d -> %s'
              % (expect, len(good), 'OK' if len(good) >= expect else 'FAILED'), flush=True)
        if len(good) < expect:
            sys.exit('gate failed — method cannot recover a known answer')
    return good


if __name__ == '__main__':
    tangents_eps(C6, 'GATE  n=6 727 (arc D is a node: TWO tangents known)', expect=2)
    tangents_eps(C4, 'n=4 183 — is it a continuum at all?')
    tangents_eps(C10, 'n=10 3913 — is it a continuum at all?')
