import sys
sys.path.insert(0, '/Users/dmi/carroll')
from fractions import Fraction as Fr
from census_extract import *
from slide3_q2 import Q2, ZERO2, ONE2, exact_count_q2
from golden_rotations import Rot

def Q(a,b=0): return Q2(Fr(a),Fr(b))

def rot_x(c,s):  # c^2+s^2=1 rational
    return Rot([[Q(1),Q(0),Q(0)],[Q(0),Q(c),Q(-s)],[Q(0),Q(s),Q(c)]])
def rot_y(c,s):
    return Rot([[Q(c),Q(0),Q(s)],[Q(0),Q(1),Q(0)],[Q(-s),Q(0),Q(c)]])
def rot_z(c,s):
    return Rot([[Q(c),Q(-s),Q(0)],[Q(s),Q(c),Q(0)],[Q(0),Q(0),Q(1)]])

# generic-ish rational rotations: 3-4-5 about z, 5-12-13 about x, 8-15-17 about y
R1 = rot_z(Fr(3,5), Fr(4,5))
R2 = rot_x(Fr(5,13), Fr(12,13))
R3 = rot_y(Fr(8,17), Fr(15,17))

total, bd = exact_count_q2([R1,R2,R3])
print('generic config: total', total, 'by_depth', bd)

n = [[tuple(R.m[i][j] for i in range(3)) for j in range(3)] for R in (R1,R2,R3)]

cross_circles, own_circles = build_circles(n)
print('cross circles', len(cross_circles), 'own circles', len(own_circles))
cands = gen_candidates(n)
print('candidates', len(cands))
verts = classify_vertices(n, cands, cross_circles, own_circles)
ntri = sum(1 for v in verts.values() if v['type']=='triple')
nkink = sum(1 for v in verts.values() if v['type']=='kink')
print('verts', len(verts), 'triple', ntri, 'kink', nkink)

top_edges, top_v, top_deg, top_flags, top_loops = build_graph(n, verts, cross_circles, "TOP")
bot_edges, bot_v, bot_deg, bot_flags, bot_loops = build_graph(n, verts, cross_circles, "BOTTOM")
Ftop,Vtop,Etop,Ctop = euler_face_count(top_v, top_edges)
Fbot,Vbot,Ebot,Cbot = euler_face_count(bot_v, bot_edges)
print(f'TOP: V={Vtop} E={Etop} C={Ctop} F={Ftop}  target={bd.get(1)}')
print(f'BOTTOM: V={Vbot} E={Ebot} C={Cbot} F={Fbot}  target={bd.get(2)}')
print('top flags', len(top_flags), 'bottom flags', len(bot_flags))

print("\n--- per-circle vertex counts ---")
from collections import Counter
counts = Counter()
for ck, gens in cross_circles.items():
    for g in gens:
        full = (ck,) + g
        cnt = sum(1 for cr,info in verts.items() if full in info['cross_inc'])
        counts[cnt]+=1
print(dict(sorted(counts.items())))

print("\n--- checking the zero-vertex circles for hidden activity ---")
zero_circles = []
for ck, gens in cross_circles.items():
    for g in gens:
        full = (ck,) + g
        cnt = sum(1 for cr,info in verts.items() if full in info['cross_inc'])
        if cnt == 0:
            zero_circles.append((ck,g))
print(f"{len(zero_circles)} zero-vertex circles")
import random
random.seed(0)
hidden_active = 0
for ck,g in zero_circles:
    i,j,a,b,s1 = g
    e1,e2 = make_basis(ck)
    # sample several points around the circle
    found=False
    for alpha,beta in [(1,0),(0,1),(1,1),(2,3),(-1,2),(3,-1),(1,-2),(-2,-1)]:
        pt = vadd(vscale(e1,Q2(alpha)), vscale(e2,Q2(beta)))
        act = {k: active_faces(n,k,pt) for k in range(3)}
        if a in act[i] and b in act[j]:
            found=True
            break
    if found:
        hidden_active+=1
print(f"hidden-active zero-vertex circles (BUG if >0): {hidden_active}")
