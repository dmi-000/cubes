#!/usr/bin/env python3
"""How small must a probe step be to SEE a plateau that is known to exist?

map_shapes2.py reported 0-dimensional for every record -- including 727, which
dim2785.log shows sits on arcs, and 2787, which was measured here holding along a
line for t in [0,24].  So the probe is too coarse, and its 183 "gate" was
uninformative: a probe returning 0 everywhere passes a gate expecting 0.

The n=9 plateau has a KNOWN direction: A and B differ only in the ninth cube,
d = B9 - A9 = (-61, 107, -201, 174), and every point between them counts 2787.
So step along exactly that direction, from the largest step down, and find where
the count starts holding.  That calibrates what any probe needs -- and if the
required step is finer than integer quaternions can express at this height, the
answer is that integer probing CANNOT map this shape and the eps engine is required.
"""
import math, subprocess, os
HERE=os.path.dirname(os.path.abspath(__file__)); ENG=os.path.join(HERE,"cube_regions_n")
def count(qs):
    spec=";".join(",".join(str(v) for v in q) for q in qs)
    o=subprocess.run([ENG,"--quats",spec],capture_output=True,text=True).stdout
    i=o.find('"bounded":')
    return int(o[i+10:o.find(",",i)]) if i>=0 else None
def red(q):
    g=0
    for v in q: g=math.gcd(g,abs(v))
    return tuple(v//g for v in q) if g else q
BASE8=[(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),(7,14,1,-5),
       (4,-3,-4,-4),(168,-168,168,-415)]
A9=(88787,-9061,74275,113786); D=(-61,107,-201,174)      # the known plateau direction
print("stepping the n=9 record along its KNOWN plateau direction")
print(f"{'step':>12} {'ninth cube height':>18} {'count':>7}")
for K in (1, 2, 4, 8, 16, 64, 256):
    q=red(tuple(a*K+d for a,d in zip(A9,D)))          # step 1/K of the full A->B move
    c=count(BASE8+[q])
    print(f"{'1/'+str(K):>12} {max(abs(v) for v in q):>18} {str(c):>7}"
          f"{'   holds 2787' if c==2787 else ''}")
print("\nfor reference the full A->B move is 0.2% of the quaternion, and a tangent")
print("probe at K=64 displaces ~1/64 -- about 100x the width of the whole plateau.")
