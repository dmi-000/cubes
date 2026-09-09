#!/usr/bin/env python3
"""SOLVE the local dimension of every record, instead of probing for it.

Three probes were run before this and all three were wrong, in ways dimension.py's
own docstring predicts:

  * n4_183_extent.py -- Cayley probe, inert at half-turns ([P287]): 26 "survivors"
    were the unperturbed record.
  * map_all_shapes.py -- quaternion-component probe including the gauge direction.
  * map_shapes2.py -- tangent-basis probe: returned 0-dimensional for EVERY record,
    including 727 (arcs, dim2785.log) and 2787 (a plateau measured here across
    t in [0,24]).  Its 183 gate "passed" only because a probe that returns 0
    everywhere passes a gate expecting 0.

dimension.py states the reason: "a zero reading means 'not aligned', never
'isolated'" (FAILURE_MODES 11d), and "every probe moves ONE cube, so a locus that
is positive-dimensional only via directions moving several cubes together is
invisible to all of them".  A 1-dimensional plateau inside a 3-dimensional tangent
space is almost never axis-aligned, which is exactly what was hit.

This drives the SOLVER, reusing isolate183.py's proven sequence: degauge so no cube
is a half-turn (a global rotation is a congruence, so counts are preserved),
build the tight conditions, take the nullspace for first-order lineality, then the
second-order variety.  Applied to each record in turn, cheapest first, so partial
results survive if the larger ones do not finish.
"""
import sys, time, os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
import sympy as sp, dimension as D
from isolate183 import degauge

B5=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
TARGETS=[("393 n=5",B5),
         ("727 n=6",B5+[(7,14,1,-5)]),
         ("1217 n=7",B5+[(7,14,1,-5),(4,-3,-4,-4)]),
         ("1895 n=8",B5+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)])]

for name,cfg in TARGETS:
    try:
        q,g=degauge(cfg)
        D.set_field(0); D.QZERO[:]=[q[0]]
        pt=D.point_of(q)
        if pt is None:
            print('%-12s STILL at Cayley infinity'%name,flush=True); continue
        n=len(q); ncols=3*(n-1)
        base=D.count_at(pt,n)
        vars_=sp.symbols('c0:%d'%ncols); Rs=D.frames(vars_,q[0])
        t0=time.time()
        tight,loose=D.cached_conditions(Rs,n,vars_,pt,D.quats_of(pt,q[0]),q[0])
        good=[t for t in tight if not t['degenerate']]
        ns=D.nullspace([t['grad'] for t in good],ncols)
        print('%-12s count %s | %d tight | LINEALITY %d of %d | setup %.0fs'
              %(name,base,len(good),len(ns),ncols,time.time()-t0),flush=True)
        if not ns:
            print('%-12s    lineality 0 -> ISOLATED at first order'%'',flush=True); continue
        st,dirs=D.variety_incremental(good,list(range(len(good))),pt,n,ns,q[0],progress=False)
        print('%-12s    second-order: %s, %d directions -> %s'
              %('',st,len(dirs),'ISOLATED' if st=='empty' else 'NOT isolated'),flush=True)
    except Exception as e:
        print('%-12s FAILED: %s'%(name,type(e).__name__+': '+str(e)[:90]),flush=True)
