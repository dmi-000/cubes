#!/usr/bin/env python3
"""CONTROL: is arc D different from A, B, C -- or is the RECORD different?

Measured: arcs A, B, C each give 20 walls / lineality 2 / variety 2, and arc D
gives 27 / 1 / empty.  That reads as "the record's arc is the constrained one",
but arc D's representative was s = 0, and s = 0 IS the 727 record.  The other
three were interior points of their arcs, chosen as the simplest rational inside
the solved extent.  So the comparison confounds TWO differences at once:

    arc D versus arcs A, B, C          (which arc)
    the record versus a generic point  (where on the arc)

This measures arc D at a NON-RECORD s inside its own extent (-1/8, 1/4).  If it
comes back 20 / 2 / 2, the node has one structural class and the record is simply
the special point on it.  If it stays 27 / 1 / empty, arc D really is different.

Either answer is worth having; the point is that the two-class reading was not
yet entitled.
"""
import sys, os, json
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
ROOT=os.path.dirname(HERE) if os.path.basename(HERE)=='src' else HERE
import map_arcs as M

a0, vv, lo, hi = M.ARCS['D']
out={'what':'arc D at non-record parameters, controlling for record-vs-generic',
     'extent':[str(lo),str(hi)],'record_s':'0','points':{}}
p=os.path.join(ROOT,'data','arcD_control.json')
for s in (F(1,8), F(-1,16)):
    c=[a0[i]+s*vv[i] for i in range(3)]
    q6=M.q_of(c); quats=M.BASE+[q6]
    try:
        m,walls,pt,dirs=M.measure('D@%s'%s, quats)
    except Exception as e:
        out['points'][str(s)]={'error':type(e).__name__+': '+str(e)[:90]}
        print('s=%s FAILED %s'%(s,type(e).__name__),flush=True); continue
    m.update({'s':str(s),'sixth_cube':list(q6),
              'height':max(abs(x) for x in q6),'GATE_727':m['count']=='727'})
    out['points'][str(s)]=m
    print('D s=%-6s cube %-22s h=%-5d count %-5s %s | %d walls | lineality %d | variety %s %d'
          %(s,str(q6),m['height'],m['count'],
            'GATE OK' if m['GATE_727'] else 'GATE **FAIL**',
            m['distinct_walls'],m['lineality'],m['variety'],m['variety_dirs']),flush=True)
    json.dump(out,open(p,'w'),indent=1)
print('written data/arcD_control.json')
