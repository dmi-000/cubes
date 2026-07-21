import numpy as np, itertools, math

def branches(P,Q,R, psis):
    """For linear-in-(cD,sD) form P*cD+Q*sD+R=0 with cD^2+sD^2=1, return
    for each psi the set of real Delta roots in [0,360)."""
    out = []
    for ps in psis:
        p = P(ps); q = Q(ps); r = R(ps)
        # solve p*cos(D)+q*sin(D) = -r  => amplitude*cos(D-phi) = -r
        amp = math.hypot(p,q)
        sols = []
        if amp < 1e-12:
            out.append(sols); continue
        rhs = -r/amp
        if abs(rhs) > 1+1e-9:
            out.append(sols); continue
        rhs = max(-1,min(1,rhs))
        phi = math.atan2(q,p)
        base = math.acos(rhs)
        for s in (base, -base):
            D = (phi + s) % (2*math.pi)
            # verify
            if abs(p*math.cos(D)+q*math.sin(D)+r) < 1e-8:
                sols.append(math.degrees(D))
        out.append(sorted(set(round(x,4) for x in sols)))
    return out

# rebuild the raw residuals list for all ordered types/signs using sympy once, extract P,Q,R as python funcs
import sympy as sp
cD, sD, cP, sP = sp.symbols('cD sD cP sP', real=True)
exec(open('derive2.py').read().split("print(\"\\n\\n=== grouping")[0])

psis_deg = [10,20,30,40,50,60,70,80]
psis = [math.radians(x) for x in psis_deg]

axis_name={0:'x',1:'y',2:'z'}
cluster_summary = {}
for (a,b), lst in results.items():
    entries = []
    for iA,sA,iB,sB,resid in lst:
        poly = sp.Poly(resid, cD, sD)
        # linear form: coefficient of cD, sD, const
        d = poly.as_dict()
        Pc = d.get((1,0), 0)
        Qc = d.get((0,1), 0)
        Rc = d.get((0,0), 0)
        Pf = sp.lambdify(cP,Pc.subs(sP, sp.sqrt(1-cP**2)) if Pc!=0 else 0,'math')
        # instead lambdify with both cP,sP as psi funcs directly
        Pfun = sp.lambdify((cP,sP), Pc, 'math')
        Qfun = sp.lambdify((cP,sP), Qc, 'math')
        Rfun = sp.lambdify((cP,sP), Rc, 'math')
        def Pw(ps, f=Pfun): return f(math.cos(ps), math.sin(ps))
        def Qw(ps, f=Qfun): return f(math.cos(ps), math.sin(ps))
        def Rw(ps, f=Rfun): return f(math.cos(ps), math.sin(ps))
        br = branches(Pw,Qw,Rw, psis)
        entries.append((sA,sB,tuple(tuple(x) for x in br)))
    # cluster by identical branch-signature
    groups = {}
    for sA,sB,sig in entries:
        groups.setdefault(sig, []).append((sA,sB))
    cluster_summary[(a,b)] = groups
    print(f'=== {axis_name[a]}{axis_name[b]}: {len(groups)} distinct branch-signatures among 16 ===')
    for sig, memb in groups.items():
        nonempty = sum(1 for s in sig if s)
        print(f'   members={memb}  nonempty_psis={nonempty}/8  sample={sig[:3]}')
