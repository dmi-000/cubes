#!/usr/bin/env python3
"""OQ 15: why does an added cube contribute rank 2 to the wall matrix instead of 3?

A cube has 3 degrees of freedom. Its contribution to the wall matrix's rank is how many
of them the tight coincidences actually constrain. So restrict the wall gradients to
that cube's OWN three columns and take the rank:

    rank 3  ->  the cube is fully constrained, contributes 3
    rank 2  ->  ONE direction in its 3-space is orthogonal to every wall gradient:
                an infinitesimal motion of that cube alone crossing NO wall

The question "why 2 not 3" is therefore "what is that direction, and why does it
exist". This computes it per cube per record, and reports the direction whenever the
rank is deficient.

Watch for: [P174](LEDGER.md#p174) claimed such free axes are BODY DIAGONALS, with the
axes computed correctly and only the interpretation withdrawn ([P175](LEDGER.md#p175),
itself corrected by [P184](LEDGER.md#p184)). If the deficient directions come back
(+-1,+-1,+-1), that claim is recovered as a fact about the wall matrix.
"""
import sys
sys.path.insert(0,'.')
from fractions import Fraction as F
from math import gcd
import sympy as sp
from eps_null import walls_and_null

BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
CASES=[('393  n=5', BASE),
       ('727  n=6', BASE+[(7,14,1,-5)]),
       ('1217 n=7', BASE+[(7,14,1,-5),(4,-3,-4,-4)]),
       ('1895 n=8', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]),
       ('2785 n=9', BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(56,56,55,56)]),
       ('2787 n=9', BASE+[(7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415),(88787,-9061,74275,113786)]),
       ('3913 n=10',BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57),(19,-2,15,24)]),
       ('3925 n=10',BASE+[(7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415),(6555,6555,6497,6555),(88787,-9061,74275,113786)])]

def prim(v):
    den=1
    for x in v: den=den*F(x).denominator//gcd(den,F(x).denominator)
    iv=[int(F(x)*den) for x in v]; g=0
    for x in iv: g=gcd(g,abs(x))
    iv=[x//(g or 1) for x in iv]
    for x in iv:
        if x>0: break
        if x<0: iv=[-y for y in iv]; break
    return tuple(iv)

def isdiag(v):
    return len({abs(x) for x in v})==1 and all(x for x in v)

for label,cubes in CASES:
    pt,walls,null,ncols=walls_and_null(cubes)
    W=sp.Matrix([[sp.Rational(x) for x in w] for w in walls])
    R=W.rank()
    print('\n%s   ambient %d  walls %d  rank %d  deficit %d'
          %(label,ncols,len(walls),R,ncols-R),flush=True)
    tot=0
    for j in range(1,len(cubes)):
        sub=W[:,3*(j-1):3*j]
        rj=sub.rank()
        tot+=rj
        tag=''
        if rj<3:
            ns=sub.nullspace()
            dirs=[prim([sp.Rational(x) for x in b]) for b in ns]
            tag='   free direction(s) %s%s'%(dirs,
                 '  <== BODY DIAGONAL' if any(isdiag(d) for d in dirs) else '')
        print('   cube %d  rank of walls on its own 3 columns = %d%s'%(j,rj,tag),flush=True)
    print('   sum of per-cube ranks %d   vs total rank %d   (excess %d = cross-cube coupling)'
          %(tot,R,tot-R),flush=True)
