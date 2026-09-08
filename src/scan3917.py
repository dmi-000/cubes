#!/usr/bin/env python3
"""Map the 3917 region in its 2-plane, wide enough to see every side.

The first scan (17x17) showed a filled region with a straight lower-left boundary
near 2*k1 + k2 = -2, and 3913 reappearing at the top-left — so at least two walls,
i.e. a polygon. This widens the window to find them all.

Coordinates: tenth cube = (D, -9061+k1+5*k2, 74275-14*k1, 113786+14*k2), D = 88787,
reduced by gcd. The record is (k1,k2) = (0,0).
"""
import json, subprocess
from math import gcd
BASE=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C9=BASE+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61),(57,57,56,57)]
D=88787
def cube(k1,k2):
    c=(D,-9061+k1+5*k2,74275-14*k1,113786+14*k2); g=0
    for v in c: g=gcd(g,abs(v))
    return tuple(v//g for v in c)
def cnt(k1,k2):
    cfg=C9+[cube(k1,k2)]; st=";".join(",".join(map(str,x)) for x in cfg)
    m=max(abs(v) for x in cfg for v in x)
    cmd=(['./cube_regions_n','--quats',st] if m<=512 else ['./cube_regions_q2w','--d','0','--quats',st])
    try: return json.loads(subprocess.run(cmd,capture_output=True,text=True).stdout)['bounded']
    except Exception: return None
R=range(-40,61,4)
print('rows k2, cols k1, step 4;  # = 3917,  . = 3913,  o = other,  ? = unevaluated')
print('      '+''.join('%3d'%(k//4%10) for k in R))
grid={}
for k2 in R:
    row=''
    for k1 in R:
        c=cnt(k1,k2); grid[(k1,k2)]=c
        row += '  #' if c==3917 else '  .' if c==3913 else '  ?' if c is None else '  o'
    print('%5d '%k2+row, flush=True)
ins=[k for k,v in grid.items() if v==3917]
print('\n3917 at %d of %d points'%(len(ins),len(grid)))
if ins:
    print('   k1 range %d..%d, k2 range %d..%d'%(min(k[0] for k in ins),max(k[0] for k in ins),
                                                 min(k[1] for k in ins),max(k[1] for k in ins)))
best=max((v for v in grid.values() if v), default=None)
print('   max count on the plane: %s'%best)
