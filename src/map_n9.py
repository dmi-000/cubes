#!/usr/bin/env python3
"""Map the n = 9 region -- CONTINUUM_MAP has only a single LINE through it.

The n = 9 record's neighbourhood is 4-dimensional (RESULTS' n=9 row) and the map
covers one line: the extension line solve_wall.py brackets.  This measures the
region itself: walls, lineality, the coincidence variety, and the count plateau.

REPRESENTATIVE.  The SIMPLIFIED one, `109,-11,91,140` (height 140), not the
original `88787,-9061,74275,113786` (height 113 786).  Both count 2787 with the
same by_depth at every depth.  They are NOT interchangeable under extension
([P285](LEDGER.md#p285)) -- 3925 versus 3921 -- so anything measured here is
about the simplified representative and must not be carried to the n=10 chain
without re-deriving it.  That is the whole content of P285 and it is the trap
this file is closest to.
"""
import json, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
ROOT=os.path.dirname(HERE) if os.path.basename(HERE)=='src' else HERE
import sympy as sp, dimension as D, wall_keys as W

B5=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
SIMPLE = B5+[(7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415),(109,-11,91,140)]
ORIG   = B5+[(7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415),(88787,-9061,74275,113786)]

def run(label, quats):
    D.set_field(0); D.QZERO[:]=[quats[0]]
    pt=D.point_of(quats); n=len(quats); nc=3*(n-1)
    cnt=D.count_at(pt,n)
    print('%s: count %s, ambient %d'%(label,cnt,nc),flush=True)
    v=sp.symbols('c0:%d'%nc); Rs=D.frames(v,quats[0])
    tight,loose=D.cached_conditions(Rs,n,v,pt,D.quats_of(pt,quats[0]),quats[0])
    good=[t for t in tight if not t['degenerate']]
    degen=len(tight)-len(good)
    ns=D.nullspace([t['grad'] for t in good],nc)
    _,walls=W.walls_of(quats)
    print('%s: %d tight (%d degenerate, %d loose) | %d distinct walls | lineality %d'
          %(label,len(tight),degen,loose,len(walls),len(ns)),flush=True)
    st,dirs=D.variety_incremental(good,list(range(len(good))),pt,n,ns,quats[0],
                                  progress=False)
    print('%s: second-order variety %s, %d directions'%(label,st,len(dirs)),flush=True)
    return {'count':str(cnt),'ambient':nc,'tight':len(tight),'degenerate':degen,
            'loose':loose,'distinct_walls':len(walls),'lineality':len(ns),
            'variety':st,'variety_dirs':len(dirs),
            'directions':[[str(x) for x in d] for d in dirs],
            'quats':[list(q) for q in quats],'point':[str(x) for x in pt],
            'keys':[{'frame':w['frame'],'group':[list(x) for x in w['group']],
                     'sig':list(w['sig']),'c0':w['c0'],
                     'grad':[str(x) for x in w['grad']]} for w in walls]}

out={'what':'the n=9 region (2787), both representatives',
     'WARNING':('the two representatives are NOT interchangeable under extension '
                '(P285: 3925 vs 3921) even though they agree in count and by_depth '
                'at every depth. Nothing here transfers to n=10 without re-deriving.'),
     'records':{}}
for lab,q in (('simplified_h140',SIMPLE),('original_h113786',ORIG)):
    try:
        out['records'][lab]=run(lab,q)
    except Exception as e:
        out['records'][lab]={'error':type(e).__name__+': '+str(e)[:120]}
        print('%s FAILED %s: %s'%(lab,type(e).__name__,str(e)[:90]),flush=True)
    json.dump(out,open(os.path.join(ROOT,'data','n9_region_map.json'),'w'),indent=1)
print('written data/n9_region_map.json')
