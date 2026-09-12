#!/usr/bin/env python3
"""Build the n = 10 conditions -- the tower's top row, never measured.

GAP 2 of the register: n = 10 has a count and nothing else. No wall count, no tight
count, no rank, no lineality, no variety. Its conditions have never been built, so
none of those is a hard question -- they are all one expensive step away.

COST. `conditions` is symbolic and grows steeply: ambient 27 here against 24 at
n = 9. It caches on completion (dimension_cache, content-keyed), so this is paid
once and every later analysis reads it. That is the whole reason the cache exists.

REPRESENTATIVE. The n = 10 record is reached from the ORIGINAL n = 9 representative
(height 113 786), not the simplified one -- P285: the simplified one extends to
3921, not 3925. Using the wrong one here would measure a different configuration.
"""
import sys, os, time
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
ROOT=os.path.dirname(HERE) if os.path.basename(HERE)=='src' else HERE
import sympy as sp, json
import dimension as D, wall_keys as W

B5=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
ORIG9=B5+[(7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415),(88787,-9061,74275,113786)]
REC10=ORIG9+[(6555,6555,6497,6555)]

D.set_field(0); D.QZERO[:]=[REC10[0]]
pt=D.point_of(REC10)
n=len(REC10); nc=3*(n-1)
print('n=%d ambient %d, count %s'%(n,nc,D.count_at(pt,n)),flush=True)
t0=time.time()
v=sp.symbols('c0:%d'%nc); Rs=D.frames(v,REC10[0])
tight,loose=D.cached_conditions(Rs,n,v,pt,D.quats_of(pt,REC10[0]),REC10[0])
good=[t for t in tight if not t['degenerate']]
ns=D.nullspace([t['grad'] for t in good],nc)
_,walls=W.walls_of(REC10)
el=time.time()-t0
print('n=10: %d tight (%d degenerate, %d loose) | %d distinct walls | rank %d | lineality %d | %.0fs'
      %(len(tight),len(tight)-len(good),loose,len(walls),nc-len(ns),len(ns),el),flush=True)
json.dump({'n':10,'count':str(D.count_at(pt,n)),'ambient':nc,'tight':len(tight),
           'degenerate':len(tight)-len(good),'loose':loose,'distinct_walls':len(walls),
           'rank':nc-len(ns),'lineality':len(ns),'seconds':el,
           'representative':'ORIGINAL n=9 (h 113786) + 6555,6555,6497,6555',
           'quats':[list(q) for q in REC10]},
          open(os.path.join(ROOT,'data','n10_measured.json'),'w'),indent=1)
print('written data/n10_measured.json',flush=True)
