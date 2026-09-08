#!/usr/bin/env python3
"""Pool for anchor_split_n.py at arbitrary n, same hard-case weighting as
anchor_pool.py: low height (anchors eaten, components merged), the shared-normal
locus (hardest for ANCHOR), and record neighbourhoods (the tight end)."""
import random, sys

REC = {3: [(1,0,0,0),(1,1,1,1),(1,-1,-1,1)],
       4: [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)],
       5: [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4),(2,1,3,0)]}

def rq(rnd, h):
    while True:
        q = tuple(rnd.randint(-h, h) for _ in range(4))
        if any(q):
            return q

n = int(sys.argv[1]); seed = int(sys.argv[2]); N = int(sys.argv[3])
rnd = random.Random(seed)
out = []
for h in (1, 2, 3, 5):
    for _ in range(N):
        out.append([(1,0,0,0)] + [rq(rnd, h) for _ in range(n-1)])
for _ in range(N):
    cfg = [(1,0,0,0)]
    for _ in range(n-1):
        ax = rnd.randrange(3); q = [rnd.randint(1,6),0,0,0]; q[1+ax] = rnd.randint(-6,6)
        cfg.append(tuple(q))
    out.append(cfg)
rec = REC[n]
for scale in (1, 4, 16):
    for _ in range(N):
        out.append([rec[0]] + [tuple(c*scale + rnd.randint(-2,2) for c in q) for q in rec[1:]])
for _ in range(N):
    out.append([(1,0,0,0)] + [rq(rnd, 60) for _ in range(n-1)])
for cfg in out:
    print(";".join(",".join(str(v) for v in q) for q in cfg))
