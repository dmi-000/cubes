import sympy as sp
exec(open('derive2.py').read().split("print(\"\\n\\n=== grouping")[0])

axis_name = {0:'x',1:'y',2:'z'}
psi = sp.symbols('psi', positive=True)

cD_val = sp.Rational(-1,2)   # cos(120deg)
sD_val = sp.sqrt(3)/2        # sin(120deg)

target_oct = sp.asin(1/sp.sqrt(3))
target_gold = sp.atan(sp.Rational(1)*((1+sp.sqrt(5))/2)**2)  # arctan(phi^2)

print("target octahedral psi (deg):", sp.deg(target_oct).evalf() if False else float(target_oct)*180/3.141592653589793)
print("target golden psi (deg):", float(target_gold)*180/3.141592653589793)

for (a,b), lst in results.items():
    tname = axis_name[a]+axis_name[b]
    if set((a,b)) not in ({1,2},{0,2}):
        continue
    for iA,sA,iB,sB,resid in lst:
        e = resid.subs({cD: cD_val, sD: sD_val, cP: sp.cos(psi), sP: sp.sin(psi)})
        e = sp.simplify(e)
        # check root at octahedral and golden psi
        vo = sp.simplify(e.subs(psi, target_oct))
        vg = sp.simplify(e.subs(psi, target_gold))
        if vo == 0 or vg == 0:
            print(tname, sA, sB, 'oct_zero=', vo==0, 'gold_zero=', vg==0, ' resid=', sp.factor(resid))
