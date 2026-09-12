#!/usr/bin/env python3
"""Count-plateau tangents in the FULL ambient, not the last cube's slice.

GAP 1 of the register. `arc_eps.tangents_eps` projects every wall gradient onto
`tail = slice(ncols-3, ncols)` and forms candidates there, so every tangent it can
return is supported on the LAST CUBE. The published 0, 0, 2, 1, 1 at n = 4..8 are
therefore last-cube counts that have been read as plateau dimensions -- and at
n = 7 a base direction does exist, found only because a drawing forced the
question.

METHOD, and it is a solve. A direction that leaves a wall crosses it, so a
first-order tangent must lie in EVERY wall: the candidate space is the null space
of all wall gradients in the full ambient -- which is the lineality, already
computed. Each basis direction, and each small integer combination of them, is
then tested with the INFINITESIMAL engine: no step size, so no step-size artefact
of the kind that made the 1217 plateau look like a point (P295).

CONTROLS, both able to fail: the zero direction must return the record, and a wall
gradient used as a direction must NOT. If either fails nothing below is reported.
"""
import sys, os, json, itertools
from fractions import Fraction as F
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
ROOT=os.path.dirname(HERE) if os.path.basename(HERE)=='src' else HERE
import dimension as D
from qfield import Q
from epscount import count_eps
from eps_null import walls_and_null
import wall_keys as W


def primitive(v):
    from math import gcd
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]
    g=0
    for x in iv: g=gcd(g,abs(x))
    return [x//(g or 1) for x in iv]


def probe(pt, v, q0):
    d=[Q(F(x),0,0) for x in v]
    r=count_eps(pt, d, 0, q0)
    if r is None:
        r=count_eps(pt, d, 0, q0, wide=True)
    return r


def run(cubes, label):
    pt, walls, null, ncols = walls_and_null(cubes)
    rec = D.count_at(pt, len(cubes))
    z  = probe(pt,[0]*ncols,cubes[0])
    wg = probe(pt,[F(x) for x in walls[0]],cubes[0])
    ok = (z==rec) and (wg is not None and wg!=rec)
    print('%-12s record %-5s ambient %-3d walls %-4d lineality %-2d  CONTROLS zero→%s wall→%s %s'
          %(label,rec,ncols,len(walls),len(null),z,wg,'OK' if ok else 'FAIL'),flush=True)
    if not ok:
        return {'label':label,'status':'CONTROLS FAILED'}
    cands=[]
    for b in null:
        p=primitive(b)
        if p and p not in cands: cands.append(p)
    for a,b in itertools.combinations(null,2):
        for x,y in ((1,1),(1,-1),(2,1),(1,2)):
            p=primitive([x*F(u)+y*F(v) for u,v in zip(a,b)])
            if p and p not in cands: cands.append(p)
    held, lost, uneval = [], 0, 0
    for c in cands:
        r=probe(pt,c,cubes[0])
        if r is None: uneval+=1
        elif r==rec:
            tailonly = all(F(x)==0 for x in c[:ncols-3])
            held.append({'dir':[str(x) for x in c],'last_cube_only':tailonly})
        else: lost+=1
    print('   %d candidates | %d HOLD the count | %d lose it | %d unevaluated'
          %(len(cands),len(held),lost,uneval),flush=True)
    for h in held:
        print('      %s%s'%(h['dir'],'' if h['last_cube_only'] else '   <-- HAS A BASE COMPONENT'),flush=True)
    return {'label':label,'record':str(rec),'ambient':ncols,'walls':len(walls),
            'lineality':len(null),'candidates':len(cands),'holding':held,
            'losing':lost,'unevaluated':uneval,
            'CAVEAT':('candidates are the lineality basis and small integer combinations '
                      'of it -- a tangent needing a large-coefficient combination would '
                      'be missed. This is a lower bound on the tangent space.')}


def main():
    B5=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
    REC={4:[B5[i] for i in (0,1,2,4)],5:B5,6:B5+[(7,14,1,-5)],
         7:B5+[(7,14,1,-5),(4,-3,-4,-4)],
         8:B5+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]}
    want=[int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(REC)
    out={'what':'count-plateau tangents in the FULL ambient',
         'supersedes':('arc_eps.tangents_eps, which searches the last-cube slice only; '
                       'its 0,0,2,1,1 at n=4..8 are last-cube counts'),
         'levels':{}}
    p=os.path.join(ROOT,'data','tangents_full.json')
    if os.path.exists(p):
        try:
            prev=json.load(open(p))
            if isinstance(prev.get('levels'),dict): out['levels'].update(prev['levels'])
        except Exception: pass
    for n in want:
        out['levels'][str(n)]=run(REC[n],'n=%d'%n)
        json.dump(out,open(p,'w'),indent=1)
    print('written data/tangents_full.json')

if __name__=='__main__':
    main()
