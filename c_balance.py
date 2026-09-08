#!/usr/bin/env python3
"""GATE on the exact characterisation of c_ell = 2.

Claim: the level graph G carries the free involution -I, so G -> G/+- is a double
cover, and over each quotient component the cover is trivial (2 lifted components)
or not (1).  In signed-graph language: give each quotient edge the sign '-' if
its lift swaps sheets, '+' if not; then

    c_ell  =  sum over quotient components of (2 if BALANCED else 1)

where balanced means every cycle has an even number of '-' edges (Harary).  This
is not asserted here -- it is computed independently of the component count in G
and required to agree.

Signing procedure: pick one lift for each quotient vertex; an edge {u,v} is '+'
if the chosen lifts are adjacent in G, '-' if the chosen lift of u is adjacent to
-  (the other lift of) v.  Balance is then tested by 2-colouring the quotient
component and checking no edge violates its sign.
"""
import collections, itertools, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import strictly_inside, parse, level_graph, shares_plane


def level_edges(qs, want_ell):
    """the depth-ell graph as (vertex set, edge set) over exact points"""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    V, E = set(), set()
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j) and strictly_inside(mid, Ms[k]))
                if s + 1 != want_ell:
                    continue
                P = tuple(tuple(p[z] + t * d[z] for z in range(3)) for t in (a, b))
                V.update(P)
                E.add(frozenset(P))
    return V, E


def neg(P):
    return tuple(-x for x in P)


def balance_count(qs, ell):
    """c predicted from signed-quotient balance, computed WITHOUT counting G's components"""
    V, E = level_edges(qs, ell)
    if not V:
        return None
    # quotient vertices: canonical representative of each antipodal pair
    rep = {}
    for P in V:
        r = min(P, neg(P))
        rep[P] = r
    qverts = set(rep.values())
    # quotient adjacency, carrying the sign
    adj = collections.defaultdict(list)
    for e in E:
        u, v = tuple(e)
        ru, rv = rep[u], rep[v]
        # sign '+' iff the chosen lifts (the canonical reps) are the endpoints used
        sign = 1 if ((u == ru) == (v == rv)) else -1
        adj[ru].append((rv, sign))
        adj[rv].append((ru, sign))
    seen, total = set(), 0
    for s in qverts:
        if s in seen:
            continue
        colour = {s: 1}
        stack = [s]
        seen.add(s)
        balanced = True
        while stack:
            x = stack.pop()
            for y, sg in adj[x]:
                want = colour[x] * sg
                if y not in colour:
                    colour[y] = want
                    seen.add(y)
                    stack.append(y)
                elif colour[y] != want:
                    balanced = False
        total += 2 if balanced else 1
    return total


CASES = [("n=4 record 183", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4", (1, 2, 3)),
         ("c=2 case A", "1,0,0,0;1,5,10,15;1,2,4,6;8,7,14,21", (1, 2)),
         ("c=2 case B", "1,0,0,0;-23,-90,43,22;72,-37,-17,-2;-4,4,-79,25", (1, 2)),
         ("c=2 case C", "1,0,0,0;1,14,-21,-7;8,10,-15,-5;1,16,-24,-8", (1, 2))]

print(f"{'case':16s} {'ell':>3} {'c (components of G)':>21} {'c (signed balance)':>20}  agree")
ok = True
for label, spec, ells in CASES:
    qs = parse(spec)
    lv = level_graph(qs)
    for ell in ells:
        if ell not in lv:
            continue
        direct = lv[ell]["c"]
        pred = balance_count(qs, ell)
        agree = direct == pred
        ok &= agree
        print(f"{label:16s} {ell:>3} {direct:>21} {pred:>20}  {'OK' if agree else '*** MISMATCH ***'}")
print()
print("AGREE EVERYWHERE" if ok else "CHARACTERISATION FAILS -- do not use it")
