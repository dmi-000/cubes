#!/usr/bin/env python3
"""Step A complete: an exact formula for the two-cube region count.

From step_a2: A \\ B is covered by six convex slabs A ^ {n_i.x > 1}, one per
face normal of B.  A slab is nonempty iff ||n_i||_1 > 1, and slabs i, j overlap
iff min over lambda in [0,1] of ||lambda n_i + (1-lambda) n_j||_1 > 1 (LP
duality on the box).  Components of A \\ B are then the CONNECTED COMPONENTS of
the graph whose nodes are the nonempty slabs and whose edges are overlapping
pairs, so

    total = 1 + comp(A\\B) + comp(B\\A)

with no sampling anywhere: every ingredient is an exact rational inequality in
the rotation's entries.  This tests that formula against the engine.
"""
import itertools, json, math, random, subprocess
from fractions import Fraction as F
from step_a2 import mat, l1, max_min, normals

def components(ns):
    live = [i for i in range(6) if l1(ns[i]) > 1]
    parent = {i: i for i in live}
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for i, j in itertools.combinations(live, 2):
        if ns[i] == [-x for x in ns[j]]:
            continue
        if max_min(ns[i], ns[j]) > 1:            # overlap -> same component
            a, b = find(i), find(j)
            if a != b: parent[a] = b
    return len({find(i) for i in live})

def formula(q):
    a = components(normals(q))
    b = components(normals((q[0], -q[1], -q[2], -q[3])))
    return 1 + a + b

def red(t):
    g = 0
    for x in t: g = math.gcd(g, abs(x))
    return tuple(x//g for x in t) if g > 1 else t

def batch(qs):
    out = []
    for i in range(0, len(qs), 2000):
        ch = qs[i:i+2000]
        inp = '\n'.join('1,0,0,0;' + ','.join(map(str, q)) for q in ch) + '\n'
        p = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                           capture_output=True, text=True)
        out += [json.loads(l).get('bounded') for l in p.stdout.splitlines()
                if l.startswith('{')]
    return out

rng = random.Random(31)
qs = []
for h in (2, 3, 5, 9, 17, 33, 65, 129, 257):
    for _ in range(240):
        q = red(tuple(rng.randint(-h, h) for _ in range(4)))
        if any(q): qs.append(q)
truth = batch(qs)
agree = dis = 0
bad = []
for q, t in zip(qs, truth):
    f = formula(q)
    if t is None: continue
    if f == t: agree += 1
    else:
        dis += 1
        if len(bad) < 6: bad.append((q, t, f))
print('exact formula vs engine, %d random rotations across 9 height scales' % len(qs))
print('   agree: %d    disagree: %d' % (agree, dis))
for q, t, f in bad:
    print('      %s engine %s formula %s' % (str(q), t, f))
if dis == 0:
    print('\nCOROLLARY (step A): the 13-locus is exactly')
    print('   L13 = { R : ||n_i||_1 > 1 for all six face normals, and')
    print('               min_lambda ||l n_i + (1-l) n_j||_1 <= 1 for all 12')
    print('               non-opposite pairs }')
    print('   i.e. all six slabs nonempty and pairwise disjoint.')
