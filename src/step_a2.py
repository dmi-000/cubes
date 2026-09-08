#!/usr/bin/env python3
"""Step A, derived rather than sampled: an exact criterion for the count.

Conjecture A1 (13 => axis in a mirror plane) is refuted, so the locus must be
characterised algebraically, not by where it sits in the symmetry arrangement.

THE ARGUMENT.  A \ B is covered by the six slabs A ^ {n_i . x > 1}, one per
face normal n_i of B; each is convex, so A \ B has at most six components, and
13 = 1 + 6 + 6 needs all six nonempty AND pairwise disjoint, both ways round.

  * NONEMPTY: max_{x in A} n_i.x = ||n_i||_1 > 1, true unless n_i is a signed
    basis vector (the cubes are then face-aligned).

  * DISJOINT: slabs i and j overlap iff some x in A has both n_i.x > 1 and
    n_j.x > 1, i.e. iff max_{x in A} min(n_i.x, n_j.x) > 1. By LP duality on
    the box,

        max_{x in [-1,1]^3} min(f, g) = min_{lambda in [0,1]} || lambda n_i
                                                    + (1-lambda) n_j ||_1

    a one-dimensional minimisation of a piecewise-linear convex function,
    solvable exactly at its breakpoints.

So the whole criterion is a finite set of exact inequalities in the rotation's
entries -- no sampling, and differentiable structure visible.  This validates
it against measured counts before anything is built on top.
"""
import itertools, json, math, random, subprocess
from fractions import Fraction as F

def mat(q):
    w,x,y,z = q
    n = F(w*w+x*x+y*y+z*z)
    return [[F(w*w+x*x-y*y-z*z)/n, F(2*(x*y-w*z))/n, F(2*(x*z+w*y))/n],
            [F(2*(x*y+w*z))/n, F(w*w-x*x+y*y-z*z)/n, F(2*(y*z-w*x))/n],
            [F(2*(x*z-w*y))/n, F(2*(y*z+w*x))/n, F(w*w-x*x-y*y+z*z)/n]]

def l1(v): return sum(abs(c) for c in v)

def max_min(a, b):
    """min over lambda in [0,1] of ||lambda*a + (1-lambda)*b||_1, exactly.
    Breakpoints are where a component changes sign."""
    cands = [F(0), F(1)]
    for k in range(3):
        d = a[k] - b[k]
        if d != 0:
            t = -b[k]/d
            if 0 < t < 1: cands.append(t)
    return min(l1([t*a[k] + (1-t)*b[k] for k in range(3)]) for t in cands)

def normals(q):
    M = mat(q)
    out = []
    for c in range(3):
        v = [M[r][c] for r in range(3)]
        out.append(v); out.append([-x for x in v])
    return out

def predict(q):
    """(#nonempty slabs, #disjoint non-opposite pairs) both ways round."""
    res = []
    for A_is_base in (True, False):
        ns = normals(q) if A_is_base else normals((q[0],-q[1],-q[2],-q[3]))
        ne = sum(1 for v in ns if l1(v) > 1)
        dis = 0
        for i, j in itertools.combinations(range(6), 2):
            if ns[i] == [-x for x in ns[j]]:
                continue                      # opposite faces never overlap
            if max_min(ns[i], ns[j]) <= 1:
                dis += 1
        res.append((ne, dis))
    return res

def count(q):
    o = subprocess.run(['./cube_regions_n','--quats','1,0,0,0;'+','.join(map(str,q))],
                       capture_output=True, text=True).stdout
    d = json.loads(o)
    return d.get('bounded'), {int(k):v for k,v in d['by_depth'].items() if int(k)}

def main():
    rng = random.Random(5)
    def red(t):
        g=0
        for x in t: g=math.gcd(g,abs(x))
        return tuple(x//g for x in t) if g>1 else t
    seen = {}
    print('%-22s %-7s %-16s %s' % ('quaternion','count','depth profile','(nonempty, disjoint pairs) each way'))
    tests = [(1,1,1,1),(0,1,1,1),(1,2,3,0),(2,3,5,7),(1,0,0,0),(5,2,0,0),(12,5,0,0),
             (1,1,2,0),(1,1,-1,2),(3,1,0,0),(1,-9,4,0)]
    while len(tests) < 22:
        q = red(tuple(rng.randint(-6,6) for _ in range(4)))
        if any(q): tests.append(q)
    for q in tests:
        c, bd = count(q)
        p = predict(q)
        print('%-22s %-7s %-16s %s' % (str(q), c, str(bd), p))


if __name__ == '__main__':
    main()
