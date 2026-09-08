#!/usr/bin/env python3
"""Component count for a given total, by line extraction + exact orbit dedup.

Same method as Postscript 84, applied to any recorded total.  Each Q(sqrt d)
configuration names a rational Cayley line; the same physical arc recurs 72
times (the free cube's own 24 rotations, times the base's C3), and the dedup is
exact because q -> g.q.u is linear in q.
"""
import glob, itertools, json, math, sys
from fractions import Fraction as F

G = []
for i in range(4):
    q = [0]*4; q[i] = 1; G.append(tuple(q))
for s in itertools.product([1, -1], repeat=4):
    G.append(s)
for pos in itertools.combinations(range(4), 2):
    for sg in itertools.product([1, -1], repeat=2):
        q = [0]*4; q[pos[0]] = sg[0]; q[pos[1]] = sg[1]; G.append(tuple(q))
def canonq(q):
    g = 0
    for x in q: g = math.gcd(g, abs(x))
    if g: q = tuple(x//g for x in q)
    for x in q:
        if x:
            if x < 0: q = tuple(-y for y in q)
            break
    return q
G = sorted({canonq(q) for q in G})
def qm(a, b):
    return (a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3], a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
            a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1], a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0])
GRP = [(g, u) for g in [(1,0,0,0), (1,1,1,1), (-1,1,1,1)] for u in G]

def rref(rows):
    M = [[F(x) for x in r] for r in rows]; piv = []; r = 0
    for c in range(4):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]; M[r] = [x/pv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [M[i][k]-f*M[r][k] for k in range(4)]
        piv.append(c); r += 1
    return tuple(tuple(row) for row in M[:r])

def cayley(q, d):
    (w0, w1) = q[0]; den = w0*w0 - d*w1*w1
    a, b = [], []
    for (c0, c1) in q[1:]:
        a.append(F(c0*w0-d*c1*w1, den)); b.append(F(c1*w0-c0*w1, den))
    return a, b

def canon_line(a, b):
    nz = next((i for i in range(3) if b[i] != 0), None)
    if nz is None: return None
    v = [x/b[nz] for x in b]
    if v[nz] < 0: v = [-x for x in v]
    dot = sum(a[i]*v[i] for i in range(3)); nn = sum(v[i]*v[i] for i in range(3))
    return (tuple(v), tuple(a[i]-dot/nn*v[i] for i in range(3)))

def orbits_for(total):
    reps = {}
    for f in glob.glob('wide_campaign_shard_*.jsonl'):
        for l in open(f):
            r = json.loads(l)
            if r['total'] != total: continue
            a, b = cayley([tuple(c) for c in r['quat']], r['d'])
            k = canon_line(a, b)
            if k and k not in reps: reps[k] = (a, b)
    planes = {}
    for k in reps:
        v, p = k
        planes[k] = rref([[F(1)]+[F(x) for x in p], [F(0)]+[F(x) for x in v]])
    back = {v: k for k, v in planes.items()}
    seen, orbs = set(), []
    for k in reps:
        if k in seen: continue
        orb = {k}
        for g, u in GRP:
            rows = []
            for row in planes[k]:
                den = 1
                for x in row: den = den*x.denominator//math.gcd(den, x.denominator)
                qi = tuple(int(x*den) for x in row)
                rows.append([F(x) for x in qm(qm(g, qi), u)])
            img = rref(rows)
            if img in back: orb.add(back[img])
        orbs.append(orb); seen |= orb
    return len(reps), orbs

if __name__ == '__main__':
    from collections import Counter
    for total in (int(x) for x in sys.argv[1:]) if len(sys.argv) > 1 else (727, 725, 723):
        n, orbs = orbits_for(total)
        print('total %d : %4d chart lines -> %2d orbits   sizes %s'
              % (total, n, len(orbs), dict(sorted(Counter(len(o) for o in orbs).items()))),
              flush=True)
