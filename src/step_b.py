#!/usr/bin/env python3
"""Step B, part 1: the three-cube count as exact convex geometry.

Step A (step_a3.py) reduced the TWO-cube count to slabs:

    total = 1 + comp(A\\B) + comp(B\\A),   A\\B = union of six convex slabs.

The same decomposition works for three cubes, by containment class.  Writing
X_S for the set of points lying in exactly the cubes of S,

    T = comp(X_123) + sum_{ij} comp(X_ij) + sum_i comp(X_i)
      =      1      + sum_{ij} comp((Ci^Cj)\\Ck) + sum_i comp(Ci\\(Cj u Ck))

  * X_123 is an intersection of convex bodies, hence convex, hence ONE
    component -- and nonempty, since all cubes share the origin.

  * X_ij = (Ci^Cj)\\Ck is a convex body minus a convex body: exactly step A's
    situation with a 12-facet base instead of a cube.  Six convex slabs, so
    **comp(X_ij) <= 6 with no hypotheses at all.**

  * X_i = Ci\\(Cj u Ck) is covered by the 36 convex pieces
    Ci ^ {n.x > 1} ^ {m.x > 1}, one per (face of Cj, face of Ck) -- a point
    outside both cubes violates at least one facet of each.

A finite union of convex sets has as many components as its intersection
graph, so every comp() above is a union-find over exact emptiness tests.

THE TWO EMPTINESS PRIMITIVES, both exact and both cheap:

  (a) base = the cube [-1,1]^3 (used for X_i).  A cell {x in box : n_t.x > 1
      for t in T} is nonempty iff min over the simplex of ||sum lam_t n_t||_1
      > 1 -- LP duality on the box, |T| <= 4 here.  Minimising a convex
      piecewise-linear function over a simplex: the optimum sits at a vertex
      of the subdivision cut out by the three coordinate hyperplanes, so a
      finite candidate list solves it exactly (min_l1_hull).

  (b) base = a general polytope P given by its vertices (used for X_ij).
      max_{x in P} min(f,g) = min_{lam in [0,1]} max_{v in vertices} (lam f +
      (1-lam) g)(v), again piecewise-linear in one variable (max_min_over).

Everything is Fractions; nothing is sampled.  This file's job is to VALIDATE
the decomposition against the engine, and to report the split of every total
into its 1 + (three pair terms) + (three singleton terms), which is what a
bound in terms of the pair label has to be built out of.

    python3 step_b.py [nconfigs] [seed]
"""
import itertools
import json
import math
import random
import subprocess
import sys
from fractions import Fraction as F

from step_a2 import l1, max_min, normals
from step_a3 import formula, red

BOX = [[F(1), F(0), F(0)], [F(-1), F(0), F(0)],
       [F(0), F(1), F(0)], [F(0), F(-1), F(0)],
       [F(0), F(0), F(1)], [F(0), F(0), F(-1)]]


def qmul(a, b):
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return (w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2)


def rel(a, b):
    """b as seen from a's frame: the quaternion of R_a^-1 R_b."""
    return red(qmul((a[0], -a[1], -a[2], -a[3]), b))


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def solve(rows):
    """Exact square solve; None if singular."""
    n = len(rows)
    M = [r[:] for r in rows]
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return None
        M[c], M[p] = M[p], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [M[r][k] - f * M[c][k] for k in range(n + 1)]
    return [M[r][n] for r in range(n)]


def min_l1_hull(N):
    """min over conv(N) of ||v||_1, exactly.  N: up to 4 points of R^3.

    f(lam) = ||sum lam_i N_i||_1 is convex and piecewise linear on the simplex,
    linear on each cell of the subdivision cut by the coordinate hyperplanes
    v_k = 0.  Its minimum is attained at a vertex of that subdivision: a point
    where some face of the simplex (support S) meets |S|-1 of the coordinate
    hyperplanes.  Enumerating those candidates is exact and needs no LP.
    """
    r = len(N)
    best = None
    for size in range(1, r + 1):
        for S in itertools.combinations(range(r), size):
            for A in itertools.combinations(range(3), size - 1):
                rows = [[F(1)] * size + [F(1)]]
                for k in A:
                    rows.append([N[i][k] for i in S] + [F(0)])
                lam = solve(rows)
                if lam is None or any(x < 0 for x in lam):
                    continue
                v = [sum(lam[t] * N[S[t]][k] for t in range(size))
                     for k in range(3)]
                val = l1(v)
                if best is None or val < best:
                    best = val
    return best


def vertices(halfs):
    """Vertices of {x : h.x <= 1 for all h}, exactly."""
    V = []
    for tri in itertools.combinations(range(len(halfs)), 3):
        x = solve([list(halfs[t]) + [F(1)] for t in tri])
        if x is None:
            continue
        if all(dot(h, x) <= 1 for h in halfs) and x not in V:
            V.append(x)
    return V


def max_min_over(V, ns):
    """max over the polytope with vertex set V of min_t n_t.x, for |ns| <= 2."""
    if len(ns) == 1:
        return max(dot(ns[0], v) for v in V)
    a = [dot(ns[0], v) for v in V]
    b = [dot(ns[1], v) for v in V]
    cands = [F(0), F(1)]
    for p, q in itertools.combinations(range(len(V)), 2):
        d = (a[p] - b[p]) - (a[q] - b[q])
        if d != 0:
            t = (b[q] - b[p]) / d
            if 0 < t < 1:
                cands.append(t)
    return min(max(t * a[v] + (1 - t) * b[v] for v in range(len(V)))
               for t in cands)


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.p[a] = b

    def count(self):
        return len({self.find(i) for i in range(len(self.p))})


def singleton_comp(nj, nk):
    """comp(box \\ (Cj u Ck)), with Cj, Ck given by their normals in this frame."""
    pieces = [(a, b) for a in range(6) for b in range(6)
              if max_min(nj[a], nk[b]) > 1]
    uf = UF(len(pieces))
    for p, q in itertools.combinations(range(len(pieces)), 2):
        if uf.find(p) == uf.find(q):
            continue
        (a, b), (c, d) = pieces[p], pieces[q]
        if (a ^ 1) == c or (b ^ 1) == d:
            continue                       # opposite facets: cell is empty
        N = []
        for v in (nj[a], nk[b], nj[c], nk[d]):
            if v not in N:
                N.append(v)
        if min_l1_hull(N) > 1:
            uf.union(p, q)
    return uf.count(), len(pieces)


def pair_comp(V, nk):
    """comp(P \\ Ck) for the polytope P with vertex set V."""
    live = [t for t in range(6) if max_min_over(V, [nk[t]]) > 1]
    uf = UF(len(live))
    for p, q in itertools.combinations(range(len(live)), 2):
        if uf.find(p) == uf.find(q) or (live[p] ^ 1) == live[q]:
            continue
        if max_min_over(V, [nk[live[p]], nk[live[q]]]) > 1:
            uf.union(p, q)
    return uf.count(), len(live)


def predict(qs):
    """Exact three-cube total, plus its decomposition."""
    s, sn = [], []
    for i in range(3):
        j, k = [t for t in range(3) if t != i]
        c, n = singleton_comp(normals(rel(qs[i], qs[j])),
                              normals(rel(qs[i], qs[k])))
        s.append(c)
        sn.append(n)
    p, pn = [], []
    for i, j in itertools.combinations(range(3), 2):
        k = 3 - i - j
        V = vertices(BOX + normals(rel(qs[i], qs[j])))
        c, n = pair_comp(V, normals(rel(qs[i], qs[k])))
        p.append(c)
        pn.append(n)
    return 1 + sum(p) + sum(s), p, s, pn, sn


def engine(cfgs):
    out = []
    for i in range(0, len(cfgs), 500):
        ch = cfgs[i:i+500]
        inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c)
                        for c in ch) + '\n'
        r = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                           capture_output=True, text=True)
        rows = [json.loads(l).get('bounded') for l in r.stdout.splitlines()
                if l.startswith('{')]
        if len(rows) != len(ch):
            raise SystemExit('engine returned %d of %d' % (len(rows), len(ch)))
        out += rows
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 11
    rng = random.Random(seed)
    cfgs = []
    while len(cfgs) < n:
        h = rng.choice((2, 3, 5, 9, 17, 33))
        c = [(1, 0, 0, 0)] + [red(tuple(rng.randint(-h, h) for _ in range(4)))
                              for _ in range(2)]
        if all(any(q) for q in c):
            cfgs.append(c)
    truth = engine(cfgs)
    agree = dis = 0
    print('%-9s %-6s %-6s  %-14s %-14s %s'
          % ('label', 'engine', 'formula', 'pair terms', 'single terms', ''))
    rows = []
    for c, t in zip(cfgs, truth):
        lab = tuple(sorted(formula(rel(c[i], c[j]))
                           for i, j in itertools.combinations(range(3), 2)))
        tot, p, s, pn, sn = predict(c)
        ok = (tot == t)
        agree += ok
        dis += not ok
        rows.append((lab, t, tot, p, s, sn))
        print('%-9s %-6s %-6s  %-14s %-14s %s'
              % (','.join(map(str, lab)), t, tot, str(p), str(s),
                 '' if ok else '   <-- DISAGREE'))
    print('\nagree %d   disagree %d' % (agree, dis))
    if dis:
        raise SystemExit('decomposition is wrong; nothing below is meaningful')

    print('\nsingleton term comp(Ci \\ (Cj u Ck)) by pair label')
    print('%-12s %6s %6s %8s' % ('label', 'max s', 'max p', 'configs'))
    by = {}
    for lab, t, tot, p, s, sn in rows:
        e = by.setdefault(lab, {'s': 0, 'p': 0, 'n': 0, 'tot': 0})
        e['s'] = max(e['s'], max(s))
        e['p'] = max(e['p'], max(p))
        e['tot'] = max(e['tot'], tot)
        e['n'] += 1
    for lab in sorted(by, key=lambda k: -by[k]['tot']):
        e = by[lab]
        print('%-12s %6d %6d %8d' % (','.join(map(str, lab)), e['s'], e['p'],
                                     e['n']))
    print('\nover all configs: max pair term %d (proved <= 6), max singleton '
          'term %d' % (max(max(r[3]) for r in rows), max(max(r[4]) for r in rows)))


if __name__ == '__main__':
    main()
