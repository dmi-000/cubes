#!/usr/bin/env python3
"""The n-1 images of the 3917 region: which 9-subsets move, and do their walls agree?

As the tenth cube moves over the 2-dimensional 3917 region, the ten 9-subsets behave
differently: the one that DROPS the tenth cube is the fixed base C9 = 2785, constant
everywhere. The other nine each contain the moving cube and are functions on the
region.

Two questions. (1) Are those nine also constant on the region, or do they vary inside
it? (2) At the region's boundary, WHICH subsets change — i.e. is the n=10 wall
inherited from a subset's wall, or does it belong only to the full compound?
"""
import json, subprocess, itertools
from math import gcd
BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C9=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57)]
D=88787
def cube(k1,k2):
    c=(D,-9061+k1+5*k2,74275-14*k1,113786+14*k2); g=0
    for v in c: g=gcd(g,abs(v))
    return tuple(v//g for v in c)
def cnt(cfg):
    st=";".join(",".join(map(str,x)) for x in cfg)
    m=max(abs(v) for x in cfg for v in x)
    cmd=(['./cube_regions_n','--quats',st] if m<=512 else ['./cube_regions_q2w','--d','0','--quats',st])
    try: return json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)['bounded']
    except Exception: return None
# points: deep inside, two more inside, and two just OUTSIDE across the lower-left wall
PTS=[('record        (0,0)',0,0), ('inside        (12,4)',12,4),
     ('inside        (3,-1) cheap',3,-1), ('inside        (20,20)',20,20),
     ('OUTSIDE       (-4,0)',-4,0), ('OUTSIDE       (-8,10)',-8,10)]
print('%-28s %6s | 9-subset counts, by cube dropped (0..9)'%('point','n=10'))
rows={}
for lbl,k1,k2 in PTS:
    full=C9+[cube(k1,k2)]
    tot=cnt(full)
    subs=[cnt([full[i] for i in range(10) if i!=j]) for j in range(10)]
    rows[lbl]=(tot,subs)
    print('%-28s %6s | %s'%(lbl,tot,' '.join('%5s'%s for s in subs)), flush=True)
base=rows['record        (0,0)'][1]
print('\nwhich 9-subsets DIFFER from their value at the record:')
for lbl,(tot,subs) in rows.items():
    d=[j for j in range(10) if subs[j]!=base[j]]
    print('   %-28s n=10 %-6s  subsets differing: %s'%(lbl,tot,d if d else 'none'))
