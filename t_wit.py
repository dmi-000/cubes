import sys, time, statistics as st; sys.path.insert(0,'.'); sys.argv=['x']
from fractions import Fraction as F
from growth727 import walls_of, BASE
from exactlp import feasible_strict
from witness import simplify, height, _inside
import dimension as D
W,nc = walls_of(BASE+[(7,14,1,-5)])
svs=[l.strip() for l in open('sv200.txt') if len(l.strip())==26][:40]
raw_ok=s_ok=n=0; hr=[]; hs=[]; ts=0.0
for s in svs:
    sig=[1 if c=='+' else -1 for c in s]
    rows=[[sg*W[j][t] for t in range(nc)] for j,sg in enumerate(sig)]
    y=feasible_strict(rows,nc)
    if y is None: continue
    n+=1
    a=time.time(); z=simplify(rows,list(y),nc); ts+=time.time()-a
    assert _inside(rows,z,nc), 'left the chamber'
    hr.append(height(y)); hs.append(height(z))
    raw_ok += D.count_at(list(y),6) is not None
    s_ok   += D.count_at(list(z),6) is not None
print('n=%d  evaluable RAW %d (%.0f%%)  ->  SIMPLIFIED %d (%.0f%%)'%(n,raw_ok,100*raw_ok/n,s_ok,100*s_ok/n))
print('median height %.3g -> %.3g   (simplify cost %.0f ms/chamber)'%(st.median(hr),st.median(hs),1000*ts/n))
