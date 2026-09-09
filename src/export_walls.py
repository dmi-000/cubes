#!/usr/bin/env python3
"""Record the WALL data for each record -- it was being computed and thrown away.

arc_eps/tangents_eps builds the walls at each record (880s at n=6, 1498s at n=7),
uses them for a yes/no tangent verdict, and discards them.  That is the project's
own "cache the expensive step" lesson being violated by the analysis rather than
by the machinery: dimension.cached_conditions DOES cache (587 entries, 15MB in
dimension_cache/), so the conditions survive -- but nothing ever wrote them out in
a form a reader or a later analysis can use.

This exports, per record: the distinct wall GRADIENTS at the record point, the
ambient dimension, the null space dimension, and the tight/degenerate counts.

WHAT THESE ARE, stated precisely so they are not over-read: each wall gradient is
the LINEARISATION of a coincidence condition AT the record point -- a linear form
in the 3(n-1) local coordinates, not the condition's polynomial. They are exactly
what a tangent test needs, and exactly NOT enough to solve a wall's locus. Closing
a bracket needs the underlying quadric restricted to the line; that is a further
step and this file does not claim to be it.
"""
import json, sys, os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D

B5=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
REC={4:[B5[i] for i in (0,1,2,4)], 5:B5, 6:B5+[(7,14,1,-5)],
     7:B5+[(7,14,1,-5),(4,-3,-4,-4)],
     8:B5+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]}
out={"what":"wall gradients at each record, exported from dimension_cache",
     "caveat":("each entry is the LINEARISATION of a coincidence condition at the record "
               "point -- a linear form in 3(n-1) coordinates, NOT the condition's polynomial. "
               "Sufficient for tangent tests; NOT sufficient to solve a wall locus."),
     "records":{}}
for n,q in sorted(REC.items()):
    try:
        D.set_field(0); D.QZERO[:]=[q[0]]
        pt=D.point_of(q)
        if pt is None:
            out["records"][n]={"error":"at Cayley infinity; needs degauge"}; print(n,"infinity"); continue
        ncols=3*(len(q)-1)
        vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,q[0])
        tight,loose=D.cached_conditions(Rs,len(q),vars_,pt,D.quats_of(pt,q[0]),q[0])
        good=[t for t in tight if not t['degenerate']]
        seen,walls=set(),[]
        for t in good:
            g=t['grad']; piv=next((x for x in g if x!=0),None)
            if piv is None: continue
            k=tuple(str(x/piv) for x in g)
            if k not in seen: seen.add(k); walls.append([str(x) for x in g])
        ns=D.nullspace([t['grad'] for t in good],ncols)
        out["records"][n]={"count":D.count_at(pt,len(q)),"ambient":ncols,
            "tight_total":len(tight),"tight_nondegenerate":len(good),
            "distinct_walls":len(walls),"nullspace_dim":len(ns),
            "wall_gradients":walls}
        print(f"n={n}: {len(walls)} distinct walls, ambient {ncols}, nullspace {len(ns)}",flush=True)
    except Exception as e:
        out["records"][n]={"error":type(e).__name__+": "+str(e)[:80]}
        print(f"n={n}: FAILED {type(e).__name__}",flush=True)
json.dump(out,open("data/record_walls.json","w"),indent=1)
print("written data/record_walls.json")
