#!/usr/bin/env python3
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

_GB = sp.groebner([cD**2+sD**2-1, cP**2+sP**2-1], cD, sD, cP, sP, order='grevlex')

def reduce_rel(expr):
    e = sp.expand(expr)
    if e == 0:
        return sp.Integer(0)
    q, r = sp.reduced(e, _GB.polys, cD, sD, cP, sP, order='grevlex')
    if hasattr(r, 'as_expr'):
        r = r.as_expr()
    return sp.expand(r)

# cube edges: axis a (0,1,2), other two coords s1,s2 in {-1,1}
def cube_edges():
    edges = []
    for a in range(3):
        o = [i for i in range(3) if i != a]
        for s1, s2 in product((-1, 1), repeat=2):
            c = [0,0,0]
            c[o[0]], c[o[1]] = s1, s2
            d = [0,0,0]
            d[a] = 1
            edges.append({'axis': a, 'corner': sp.Matrix(c), 'dir': sp.Matrix(d), 'signs': (s1,s2)})
    return edges

EDGES = cube_edges()

def cross(u,v):
    return u.cross(v)

# cube A = identity, cube B = R applied
edgesA = EDGES
edgesB = []
for e in EDGES:
    edgesB.append({'axis': e['axis'], 'corner': R*e['corner'], 'dir': R*e['dir'], 'signs': e['signs']})

# collect residuals by ordered type (alphaA, betaB)
results = {}
for iA, eA in enumerate(edgesA):
    for iB, eB in enumerate(edgesB):
        a, b = eA['axis'], eB['axis']
        if a == b:
            continue
        CA, DA = eA['corner'], eA['dir']
        CB, DB = eB['corner'], eB['dir']
        resid = (CB - CA).dot(cross(DA, DB))
        resid_r = reduce_rel(resid)
        results.setdefault((a,b), []).append((iA, eA['signs'], iB, eB['signs'], resid_r))

axis_name = {0:'x',1:'y',2:'z'}
for (a,b), lst in sorted(results.items()):
    print(f'=== type {axis_name[a]}(A)-{axis_name[b]}(B): {len(lst)} edge pairs ===')
    # print distinct residuals up to sign/scalar (just print raw factored forms)
    seen = []
    for iA, sA, iB, sB, resid in lst:
        fac = sp.factor(resid)
        seen.append((sA, sB, fac))
    for sA, sB, fac in seen:
        print(f'  A-signs={sA} B-signs={sB}:  {fac}')

print("\n\n=== grouping by polynomial up to overall sign ===")
for (a,b), lst in sorted(results.items()):
    groups = {}
    for iA, sA, iB, sB, resid in lst:
        # canonical: pick sign so that the coefficient tuple (sorted monomials) is lexicographically smallest
        p = sp.Poly(resid, cD, sD, cP, sP)
        coeffs = tuple(p.all_coeffs()) if p.is_univariate else tuple(p.terms())
        neg_resid = sp.expand(-resid)
        key1 = sp.srepr(resid)
        key2 = sp.srepr(neg_resid)
        key = min(key1, key2)
        groups.setdefault(key, []).append((sA, sB))
    print(f'type {axis_name[a]}(A)-{axis_name[b]}(B): {len(groups)} distinct curves (up to overall sign) among 16 pairs')
    for key, memb in groups.items():
        print(f'   size {len(memb)}: {memb}')
