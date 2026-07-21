import sys, math
sys.path.insert(0, '/Users/dmi/carroll')
from fractions import Fraction as Fr
from census_extract import *
from slide3_q2 import Q2
from golden_rotations import Rot

def Q(a,b=0): return Q2(Fr(a),Fr(b))
def rot_x(c,s): return Rot([[Q(1),Q(0),Q(0)],[Q(0),Q(c),Q(-s)],[Q(0),Q(s),Q(c)]])
def rot_y(c,s): return Rot([[Q(c),Q(0),Q(s)],[Q(0),Q(1),Q(0)],[Q(-s),Q(0),Q(c)]])
def rot_z(c,s): return Rot([[Q(c),Q(-s),Q(0)],[Q(s),Q(c),Q(0)],[Q(0),Q(0),Q(1)]])

R1 = rot_z(Fr(3,5), Fr(4,5))
R2 = rot_x(Fr(5,13), Fr(12,13))
R3 = rot_y(Fr(8,17), Fr(15,17))
n = [[tuple(R.m[i][j] for i in range(3)) for j in range(3)] for R in (R1,R2,R3)]
nf = [[[float(c) for c in n[k][f]] for f in range(3)] for k in range(3)]

def reaches(pt):
    out=[]
    for k in range(3):
        vals = [abs(sum(pt[q]*nf[k][f][q] for q in range(3))) for f in range(3)]
        out.append(max(vals))  # 1/r ~ max |n.u|; bigger dot = smaller reach
    return out

v = ( 1.0, -1.0, 0.2)   # the kink
w = ( 1.0, -1.0, -0.6)  # top edge partner on ck=(1,1,0)
u2 = (-1.0, -3.0, 0.6)  # bottom edge partner on ck=(0,1,5)

import numpy as np
def norm(p): 
    l = math.sqrt(sum(c*c for c in p)); return [c/l for c in p]
def slerp(p,q,t):
    p,q = np.array(norm(p)), np.array(norm(q))
    d = np.dot(p,q); th = math.acos(max(-1,min(1,d)))
    return list((math.sin((1-t)*th)*p + math.sin(t*th)*q)/math.sin(th))

print('arc v->w (claimed TOP, on circle (1,1,0)):')
for t in [0.05,0.25,0.5,0.75,0.95]:
    pt = slerp(v,w,t)
    r = reaches(pt)
    ranked = sorted(range(3), key=lambda k: r[k])  # ascending dot = descending reach
    print(f'  t={t}: dots={[f"{x:.4f}" for x in r]}  (cube order by reach desc: {ranked})')

print('arc u2->v (claimed BOTTOM, on circle (0,1,5)):')
for t in [0.05,0.25,0.5,0.75,0.95]:
    pt = slerp(u2,v,t)
    r = reaches(pt)
    ranked = sorted(range(3), key=lambda k: r[k])
    print(f'  t={t}: dots={[f"{x:.4f}" for x in r]}  (cube order by reach desc: {ranked})')
