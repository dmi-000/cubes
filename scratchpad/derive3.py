import sympy as sp
from itertools import product
exec(open('derive2.py').read().split("print(\"\\n\\n=== grouping")[0])  # reuse setup+results

# pick one representative per ordered type: signs (-1,-1)-(-1,-1)
reps = {}
for (a,b), lst in results.items():
    for iA, sA, iB, sB, resid in lst:
        if sA == (-1,-1) and sB == (-1,-1):
            reps[(a,b)] = resid
            break

axis_name = {0:'x',1:'y',2:'z'}
for k,v in reps.items():
    print(axis_name[k[0]], axis_name[k[1]], ':', sp.factor(v))

print()
print("--- test: swap A,B (Delta -> -Delta) relation between (a,b) and (b,a) reps ---")
for a in range(3):
    for b in range(3):
        if a==b: continue
        e1 = reps[(a,b)]
        e2 = reps[(b,a)]
        # substitute Delta -> -Delta in e1: sD -> -sD
        e1_neg = e1.subs(sD, -sD, simultaneous=True)
        diff_plus = reduce_rel(e1_neg - e2)
        diff_minus = reduce_rel(e1_neg + e2)
        print(f'{axis_name[a]}{axis_name[b]} vs {axis_name[b]}{axis_name[a]}: e1(-D)-e2 -> {diff_plus}   e1(-D)+e2 -> {diff_minus}')
