import sys
sys.path.insert(0, '/Users/dmi/carroll')
from fractions import Fraction as Fr
from census_extract import *
from slide3_q2 import Q2, ZERO2, ONE2, exact_count_q2
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

# manually redo build_graph's inner loop but report on flagged arcs, sampling densely
nflag_checked = 0
nhidden = 0
for ck, gens in cross_circles.items():
    e1, e2 = make_basis(ck)
    for (i, j, a, b, s1) in gens:
        on_circle = []
        for cr, info in verts.items():
            if any(g == (ck, i, j, a, b, s1) for g in info['cross_inc']):
                alpha, beta = dot3(cr, e1), dot3(cr, e2)
                on_circle.append((alpha, beta, cr))
        if not on_circle:
            continue
        on_circle.sort(key=cmp_to_key(
            lambda P, Q_: (half(P[0], P[1]) - half(Q_[0], Q_[1]))
            or (-cross2(P[0], P[1], Q_[0], Q_[1]).sign())))
        m = len(on_circle)
        for idx in range(m):
            alpha_i, beta_i, cr_i = on_circle[idx]
            alpha_j, beta_j, cr_j = on_circle[(idx + 1) % m]
            cs = cross2(alpha_i, beta_i, alpha_j, beta_j).sign()
            if cs > 0:
                sa, sb = alpha_i + alpha_j, beta_i + beta_j
            elif cs < 0:
                sa, sb = -(alpha_i + alpha_j), -(beta_i + beta_j)
            else:
                sa, sb = -beta_i, alpha_i
            sample = vadd(vscale(e1, sa), vscale(e2, sb))
            act_s = {kk: active_faces(n, kk, sample) for kk in range(3)}
            if a in act_s[i] and b in act_s[j]:
                continue  # this arc is fine, not flagged
            # flagged arc -- densely sample between cr_i and cr_j using float interpolation
            nflag_checked += 1
            import math
            fa_i, fb_i = float(alpha_i), float(beta_i)
            fa_j, fb_j = float(alpha_j), float(beta_j)
            th_i = math.atan2(fb_i, fa_i)
            th_j = math.atan2(fb_j, fa_j)
            # unwrap forward from th_i to th_j (increasing)
            while th_j <= th_i:
                th_j += 2*math.pi
            found_hidden = False
            for t in [k/20 for k in range(1,20)]:
                th = th_i + t*(th_j-th_i)
                # rational-ish sample near this angle using floats -> just test activity with float dot (heuristic only)
                import numpy as np
                e1f = [float(c) for c in e1]; e2f=[float(c) for c in e2]
                pt = [math.cos(th)*0 for _ in range(3)]
                pt = [e1f[k]*math.cos(th)+e2f[k]*math.sin(th) for k in range(3)]
                # compute float active faces
                def factive(k):
                    vals = [ (sum(pt[q]*float(n[k][f][q]) for q in range(3)))**2 for f in range(3)]
                    mx = max(vals)
                    return [f for f in range(3) if abs(vals[f]-mx) < 1e-9*max(1,mx)]
                acti = factive(i); actj = factive(j)
                if a in acti and b in actj:
                    found_hidden = True
                    break
            if found_hidden:
                nhidden += 1
                print(f'HIDDEN VALID REGION within flagged arc (i={i},j={j},a={a},b={b},s1={s1}) '
                      f'between {cr_i} and {cr_j}  th_i={math.degrees(th_i):.1f} th_j={math.degrees(th_j):.1f}')

print(f'\nchecked {nflag_checked} flagged arcs, {nhidden} contain a hidden valid region (BUG indicator)')

print("\n--- probing home=0,a=0 vs faces1,2, hinge b=0(cube1),s1=1 ---")
for ap in (1,2):
    for s3 in (1,-1):
        v1 = vsub(n[0][0], vscale(n[1][0], 1))
        v2 = vsub(n[0][0], vscale(n[0][ap], s3))
        u = cross3(v1,v2)
        if is_zero_vec(u):
            print('zero', ap, s3); continue
        cr = canon_ray(u)
        act0 = active_faces(n,0,cr); act1 = active_faces(n,1,cr)
        print(f'ap={ap} s3={s3} cr={cr} act0={act0} act1={act1}  in cands={cr in cands}')

print("\n--- probing home=1,a=0(cube1) vs faces1,2, hinge a=0(cube0),s1=1 ---")
for bp in (1,2):
    for s3 in (1,-1):
        v1 = vsub(n[1][0], vscale(n[0][0], 1))
        v2 = vsub(n[1][0], vscale(n[1][bp], s3))
        u = cross3(v1,v2)
        if is_zero_vec(u):
            print('zero', bp, s3); continue
        cr = canon_ray(u)
        act0 = active_faces(n,0,cr); act1 = active_faces(n,1,cr)
        print(f'bp={bp} s3={s3} cr={cr} act0={act0} act1={act1}  in cands={cr in cands}')

print("\n--- checking new point (1,1/2,7/8) ---")
newpt = (Q2(1), Q2(1,2), Q2(7,8))
print('in verts?', newpt in verts)
if newpt in verts:
    info = verts[newpt]
    print('type', info['type'])
    print('active', info['active'])
    print('cross_inc', [g[1:] for g in info['cross_inc']])
    print('own_inc', [g[1:] for g in info['own_inc']])
# check on-circle
ck0 = canon_circle(vsub(n[0][0], n[1][0]))
print('dot with target circle', dot3(newpt, ck0))

print("\n--- redo directly, no manual transcription ---")
v1 = vsub(n[1][0], vscale(n[0][0], 1))
v2 = vsub(n[1][0], vscale(n[1][1], 1))
u = cross3(v1,v2)
cr2 = canon_ray(u)
print('cr2', cr2)
print('equal to newpt reconstruction?', cr2 == (Q2(1), Q2(1,2), Q2(7,8)))
print('in verts?', cr2 in verts)
ck0 = canon_circle(vsub(n[0][0], n[1][0]))
print('dot with circle', dot3(cr2, ck0))
if cr2 in verts:
    info = verts[cr2]
    print('type', info['type'], 'active', info['active'])
    print('cross_inc', [g[1:] for g in info['cross_inc']])
