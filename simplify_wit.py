import sys; sys.path.insert(0,'.'); sys.argv=['x']
from fractions import Fraction as F
from math import gcd, lcm
from functools import reduce
from growth727 import walls_of, BASE
from exactlp import feasible_strict
import dimension as D
W,nc = walls_of(BASE+[(7,14,1,-5)])
svs=[l.strip() for l in open('sv200.txt') if len(l.strip())==26][:40]
def clear(y):
    """A chamber is a CONE: scale to integers and divide by the gcd. Free."""
    ys=[F(v) for v in y]
    L=reduce(lcm,[v.denominator for v in ys],1)
    ints=[int(v*L) for v in ys]
    g=reduce(gcd,[abs(i) for i in ints if i],0) or 1
    return [F(i//g) for i in ints]
raw_ok=simp_ok=n=0
import statistics as st
hraw,hsimp=[],[]
for s in svs:
    sig=[1 if c=='+' else -1 for c in s]
    rows=[[sg*W[j][t] for t in range(nc)] for j,sg in enumerate(sig)]
    y=feasible_strict(rows,nc)
    if y is None: continue
    n+=1
    z=clear(y)
    # verify z is still strictly inside (exact sign test)
    assert all(sum(r[t]*z[t] for t in range(nc))>0 for r in rows), 'scaling left the chamber!'
    hraw.append(max(max(abs(F(v).numerator),abs(F(v).denominator)) for v in y))
    hsimp.append(max(abs(int(v)) for v in z))
    raw_ok += D.count_at(list(y),6) is not None
    simp_ok+= D.count_at(list(z),6) is not None
print('n=%d  evaluable RAW %d (%.0f%%)  ->  SCALED %d (%.0f%%)'%(n,raw_ok,100*raw_ok/n,simp_ok,100*simp_ok/n))
print('median height raw %.3g -> scaled %.3g'%(st.median(hraw),st.median(hsimp)))
