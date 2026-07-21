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

cross_circles, own_circles = build_circles(n)
cands = gen_candidates(n)
verts = classify_vertices(n, cands, cross_circles, own_circles)

top_edges, top_v, top_deg, top_flags, top_loops = build_graph(n, verts, cross_circles, 'TOP')
bot_edges, bot_v, bot_deg, bot_flags, bot_loops = build_graph(n, verts, cross_circles, 'BOTTOM')

both = [v for v in top_v & bot_v if verts.get(v,{}).get('type')=='kink']
tri_both = [v for v in top_v & bot_v if verts.get(v,{}).get('type')=='triple']
print('kinks in BOTH graphs:', len(both))
print('triples in BOTH graphs:', len(tri_both))
print('kinks total:', sum(1 for v in verts.values() if v['type']=='kink'))
print('top-only kinks:', len([v for v in top_v - bot_v if verts.get(v,{}).get('type')=='kink']))
print('bot-only kinks:', len([v for v in bot_v - top_v if verts.get(v,{}).get('type')=='kink']))

from collections import Counter
print('top degree spectrum (kinks):', Counter(top_deg[v] for v in top_v if verts.get(v,{}).get('type')=='kink'))
print('top degree spectrum (triples):', Counter(top_deg[v] for v in top_v if verts.get(v,{}).get('type')=='triple'))
print('bot degree spectrum (kinks):', Counter(bot_deg[v] for v in bot_v if verts.get(v,{}).get('type')=='kink'))
print('bot degree spectrum (triples):', Counter(bot_deg[v] for v in bot_v if verts.get(v,{}).get('type')=='triple'))

if both:
    v = both[0]
    print('\nexample kink in both:', v)
    print(' active:', verts[v]['active'])
    print(' cross_inc:', [(g[1:]) for g in verts[v]['cross_inc']])
    print(' own_inc:', [(g[1:]) for g in verts[v]['own_inc']])
    print(' top edges at v:')
    for e in top_edges:
        if e[0]==v or e[1]==v: print('   ', e[0], '<->', e[1], 'ck', e[2])
    print(' bottom edges at v:')
    for e in bot_edges:
        if e[0]==v or e[1]==v: print('   ', e[0], '<->', e[1], 'ck', e[2])
