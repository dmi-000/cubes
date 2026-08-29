import sys, time; sys.path.insert(0,'.'); sys.argv=['x']
from fractions import Fraction as F
from growth727 import walls_of, BASE
from exactlp import feasible_strict
import dimension as D
W,nc = walls_of(BASE+[(7,14,1,-5)])
svs=[l.strip() for l in open('sv200.txt') if len(l.strip())==26][:40]
ok_h, bad_h = [], []
for s in svs:
    sig=[1 if c=='+' else -1 for c in s]
    rows=[[sg*W[j][t] for t in range(nc)] for j,sg in enumerate(sig)]
    y=feasible_strict(rows,nc)
    if y is None: continue
    h=max(max(abs(v.numerator),abs(v.denominator)) for v in map(F,y))
    (ok_h if D.count_at(list(y),6) is not None else bad_h).append(h)
import statistics as st
f=lambda L:'n=%d median=%s max=%s'%(len(L), st.median(L) if L else '-', max(L) if L else '-')
print('EVALUABLE   witness height:', f(ok_h))
print('UNEVALUABLE witness height:', f(bad_h))
print('clean split by size?', (min(bad_h) > max(ok_h)) if ok_h and bad_h else 'n/a')
