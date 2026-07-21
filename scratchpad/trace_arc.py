import sys, math
sys.path.insert(0, '/Users/dmi/carroll')
from fractions import Fraction as Fr
from census_extract import *
from slide3_q2 import Q2
from golden_rotations import Rot
from functools import cmp_to_key

def Q(a,b=0): return Q2(Fr(a),Fr(b))
def rot_x(c,s): return Rot([[Q(1),Q(0),Q(0)],[Q(0),Q(c),Q(-s)],[Q(0),Q(s),Q(c)]])
def rot_y(c,s): return Rot([[Q(c),Q(0),Q(s)],[Q(0),Q(1),Q(0)],[Q(-s),Q(0),Q(c)]])
def rot_z(c,s): return Rot([[Q(c),Q(-s),Q(0)],[Q(s),Q(c),Q(0)],[Q(0),Q(0),Q(1)]])

R1 = rot_z(Fr(3,5), Fr(4,5))
R2 = rot_x(Fr(5,13), Fr(12,13))
R3 = rot_y(Fr(8,17), Fr(15,17))
n = [[tuple(R.m[i][j] for i in range(3)) for j in range(3)] for R in (R1,R2,R3)]

cross_circles, own_circles = build_circles(n)
cands = gen_candidates(n)
verts = classify_vertices(n, cands, cross_circles, own_circles)

# find first flagged arc, print detailed activity along it
for ck, gens in cross_circles.items():
    e1, e2 = make_basis(ck)
    n1sq, n2sq = dot3(e1,e1), dot3(e2,e2)
    for (i, j, a, b, s1) in gens:
        on_circle = []
        for cr, info in verts.items():
            if any(g == (ck, i, j, a, b, s1) for g in info['cross_inc']):
                alpha, beta = dot3(cr, e1), dot3(cr, e2)
                on_circle.append((alpha, beta, cr))
        if not on_circle:
            continue
        on_circle.sort(key=cmp_to_key(
            lambda P, Qv: (half(P[0], P[1]) - half(Qv[0], Qv[1]))
            or (-cross2(P[0], P[1], Qv[0], Qv[1]).sign())))
        m = len(on_circle)
        for idx in range(m):
            alpha_i, beta_i, cr_i = on_circle[idx]
            alpha_j, beta_j, cr_j = on_circle[(idx + 1) % m]
            cs = cross2(alpha_i, beta_i, alpha_j, beta_j).sign()
            if cs > 0:
                sample = vadd(cr_i, cr_j)
            elif cs < 0:
                sample = tuple(-c for c in vadd(cr_i, cr_j))
            else:
                sample = vadd(vscale(e1, -(beta_i * n1sq)), vscale(e2, alpha_i * n2sq))
            act_s = {kk: active_faces(n, kk, sample) for kk in range(3)}
            if a in act_s[i] and b in act_s[j]:
                continue
            # flagged: detail
            print(f'FLAGGED arc gen (i={i},j={j},a={a},b={b},s1={s1}) ck={ck}')
            print(f'  m={m} on circle')
            for al,be,cr in on_circle:
                ang = math.degrees(math.atan2(float(be)/float(n2sq), float(al)/float(n1sq)))%360
                print(f'    chart_ang={ang:7.2f}  cr={cr}  act={verts[cr]["active"]}')
            ang_i = math.degrees(math.atan2(float(beta_i)/float(n2sq), float(alpha_i)/float(n1sq)))%360
            ang_j = math.degrees(math.atan2(float(beta_j)/float(n2sq), float(alpha_j)/float(n1sq)))%360
            angs = math.degrees(math.atan2(float(dot3(sample,e2))/float(n2sq), float(dot3(sample,e1))/float(n1sq)))%360
            print(f'  arc from {ang_i:.2f} to {ang_j:.2f} (cs={cs}), sample at {angs:.2f}')
            print(f'  sample act: {act_s}')
            sys.exit(0)
