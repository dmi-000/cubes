#!/usr/bin/env python3
"""'Isn't every cube antipodal to itself?'  Yes -- and that is not the same as
every COMPONENT being antipodal to itself.  This exhibits the difference.

-I maps each cube to ITSELF (cubes are centrally symmetric about the common
centre), hence maps each pairwise curve dA_i n dA_j to itself, hence maps the
whole depth-ell level graph to itself.  So the graph is -I-invariant AS A SET.

But -I has NO FIXED POINT on the graph: p = -p forces p = 0, and the origin is
interior to every cube, so it is on no boundary curve.  A free involution on a
graph makes it a genuine DOUBLE COVER of its quotient, and a double cover permutes
components: over each component Q of the quotient the preimage is either ONE
component (cover nontrivial over Q) or TWO swapped ones (cover trivial over Q).
Invariance of the whole is not invariance of the parts.

Three things are checked here rather than asserted:
  (a) the vertex set is -I-closed and even -- the free-action prediction;
  (b) on a c=1 case, some node p has -p in the SAME component (self-antipodal);
  (c) on a c=2 case, EVERY node p has -p in the OTHER component and none in its
      own -- an exhibited witness, not a set-equality lookup.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_level import parse, shares_plane
from c_antipodal import components_with_nodes

CASES = [
    ("n=4 record 183, ell=1  (c=1)", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4", 1),
    ("non-degenerate c=2, ell=1", "1,0,0,0;-23,-90,43,22;72,-37,-17,-2;-4,4,-79,25", 1),
    ("non-degenerate c=2, ell=1", "1,0,0,0;1,5,10,15;1,2,4,6;8,7,14,21", 1),
]

for label, spec, ell in CASES:
    qs = parse(spec)
    comps = components_with_nodes(qs, ell)
    allnodes = set().union(*comps) if comps else set()
    neg = {tuple(-x for x in P) for P in allnodes}
    closed = (neg == allnodes)
    fixed = [P for P in allnodes if tuple(-x for x in P) == P]
    owner = {}
    for i, c in enumerate(comps):
        for P in c:
            owner[P] = i
    same = other = missing = 0
    witness = None
    for P in allnodes:
        Q = tuple(-x for x in P)
        if Q not in owner:
            missing += 1
        elif owner[Q] == owner[P]:
            same += 1
            if witness is None:
                witness = ("SAME", P, Q, owner[P])
        else:
            other += 1
            if witness is None or witness[0] == "SAME":
                witness = ("OTHER", P, Q, (owner[P], owner[Q]))
    print(f"{label}")
    print(f"  {spec}")
    print(f"  shares a face plane : {shares_plane(qs)}")
    print(f"  components          : {[len(c) for c in comps]}   (|V| = {len(allnodes)}, "
          f"even: {len(allnodes) % 2 == 0})")
    print(f"  vertex set is -I-closed : {closed}      fixed points of -I : {len(fixed)}"
          f"   (must be 0 -- the action is FREE)")
    print(f"  nodes with -p in the SAME component  : {same}")
    print(f"  nodes with -p in a DIFFERENT one     : {other}")
    print(f"  nodes whose -p is absent             : {missing}   (must be 0)")
    if witness:
        kind, P, Q, who = witness
        print(f"  witness ({kind}): p = {tuple(str(x) for x in P)}")
        print(f"               -p = {tuple(str(x) for x in Q)}   component(s) {who}")
    print()
print("Every cube is antipodal to itself; the level graph is antipodal to itself;")
print("its COMPONENTS need not be.  Both outcomes occur above, on configurations")
print("that differ in nothing else -- neither shares a face plane.")
