import sympy as sp
cD, sD, cP, sP = sp.symbols('cD sD cP sP', real=True)
resid1 = -cD*cP*sP + cD*sP**2 + cD - cP*sD + cP*sP - sP**2 + 1
resid2 = cD*cP*sP + cD*sP**2 + cD + cP*sD - cP*sP - sP**2 + 1

circ = [cD**2+sD**2-1, cP**2+sP**2-1]
gb = sp.groebner([resid1]+circ, cD,sD,cP,sP, order='lex')
q,r = sp.reduced(resid2, gb.polys, cD,sD,cP,sP, order='lex')
print('resid2 mod <resid1,circ> (lex):', r.as_expr() if hasattr(r,'as_expr') else r)

gb2 = sp.groebner([resid1]+circ, cD,sD,cP,sP, order='grevlex')
q2,r2 = sp.reduced(resid2, gb2.polys, cD,sD,cP,sP, order='grevlex')
print('resid2 mod <resid1,circ> (grevlex):', r2.as_expr() if hasattr(r2,'as_expr') else r2)
