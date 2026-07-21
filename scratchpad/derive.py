#!/usr/bin/env python3
"""Symbolic derivation of cross-class edge-line coplanarity conditions
g_type(Delta, psi) for the dihedral family Rel-gauge pair (cube A = I,
cube B = Rel(Delta,psi)). Uses sympy, exact rational/trig arithmetic,
c^2+s^2=1 side relations applied by hand (reduce cD^2->1-sD^2 etc. is NOT
what we want -- keep cD,sD,cP,sP as 4 vars with 2 relations, used only to
simplify/verify, not eliminate, so that later Groebner work over
(sD,cD,sP,cP) is a well-posed ideal with the two quadrics as generators).
"""
import sympy as sp
from itertools import product

cD, sD, cP, sP = sp.symbols('cD sD cP sP', real=True)

def Rel():
    return sp.Matrix([
        [cD*cP**2 + sP**2,      cP*sP*(1-cD),        cP*sD],
        [cP*sP*(1-cD),          cD*sP**2 + cP**2,     -sD*sP],
        [-cP*sD,                sD*sP,                 cD],
    ])

R = Rel()

# sanity: R should be orthonormal modulo cD^2+sD^2=1, cP^2+sP^2=1.
_GB = sp.groebner([cD**2+sD**2-1, cP**2+sP**2-1], cD, sD, cP, sP, order='grevlex')

def reduce_rel(expr):
    """Reduce a polynomial in cD,sD,cP,sP modulo the ideal (cD^2+sD^2-1,
    cP^2+sP^2-1) via Groebner normal form -- exact, order-independent."""
    e = sp.expand(expr)
    if e == 0:
        return sp.Integer(0)
    q, r = sp.reduced(e, _GB.polys, cD, sD, cP, sP, order='grevlex')
    if hasattr(r, 'as_expr'):
        r = r.as_expr()
    return sp.expand(r)

# check orthonormality columns
Rt = R.T
M = sp.expand(Rt*R - sp.eye(3))
maxdeg=0
allzero = True
for i in range(3):
    for j in range(3):
        val = reduce_rel(M[i,j])
        if sp.simplify(val) != 0:
            allzero = False
            print('nonzero at', i,j, val)
print('orthonormal check (mod circle relations):', allzero)

det = sp.expand(R.det())
print('det reduced:', reduce_rel(det - 1))
