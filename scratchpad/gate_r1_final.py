import sympy as sp

cD, sD, cP, sP = sp.symbols('cD sD cP sP', real=True)
gYZ = -cD*cP*sP + cD*sP**2 + cD - cP*sD + cP*sP - sP**2 + 1
gXZ = cD*cP - cD*sP - cP - sD + sP

cD0, sD0 = sp.Rational(-1,2), sp.sqrt(3)/2
psi_oct = sp.asin(1/sp.sqrt(3))
psi_gold = sp.atan(((1+sp.sqrt(5))/2)**2)

v1 = sp.simplify(gYZ.subs({cD:cD0, sD:sD0, cP: sp.cos(psi_oct), sP: sp.sin(psi_oct)}))
v2 = sp.simplify(gXZ.subs({cD:cD0, sD:sD0, cP: sp.cos(psi_gold), sP: sp.sin(psi_gold)}))
print("gYZ(120deg, oct) exact simplify ->", v1)
print("gXZ(120deg, gold) exact simplify ->", v2)
assert v1 == 0 and v2 == 0
print("GATE R1: PASS (sympy, exact symbolic)")
