import sympy as sp
exec(open('derive2.py').read().split("print(\"\\n\\n=== grouping")[0])

axis_name = {0:'x',1:'y',2:'z'}
psi = sp.symbols('psi', positive=True)

cD_val = sp.Rational(-1,2)
sD_val = sp.sqrt(3)/2
target_gold = sp.atan(((1+sp.sqrt(5))/2)**2)
print('golden target deg', float(target_gold)*180/3.141592653589793)

for (a,b), lst in results.items():
    if set((a,b)) != {0,2}:
        continue
    for iA,sA,iB,sB,resid in lst:
        e = resid.subs({cD: cD_val, sD: sD_val, cP: sp.cos(psi), sP: sp.sin(psi)})
        vg = sp.nsimplify(sp.simplify(e.subs(psi, target_gold)))
        vg_s = sp.simplify(vg)
        print(axis_name[a]+axis_name[b], sA, sB, '->', vg_s, ' numeric=', float(vg_s.evalf()) if vg_s.is_number else None)
