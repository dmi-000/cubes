#!/usr/bin/env python3
"""Step B, part 3: bound the singleton term by counting cells, not components.

WHY THIS IS THE CHEAP QUANTITY.  Every cube here is centred at the origin, so
along a ray from the origin each cube contributes one interval [0, r(u)].
Hence for X = A \\ (B u C),

    X = { r u : m(u) < r <= rA(u) },    m = max(rB, rC),

which fibres over the open set U = {u in S^2 : rA(u) > rB(u), rA(u) > rC(u)}
with connected fibres.  So comp(X) = comp(U): the singleton term is a
TWO-DIMENSIONAL count on the sphere.

Radially projecting step A's slabs, U_B = {rA > rB} is the union of six sets

    K_i = { u : n_i.u > |u_1|, |u_2|, |u_3| },

each an intersection of six halfspaces -- a CONVEX cone, and the six come in
three antipodal pairs.  Likewise U_C = union of L_j.  Therefore

    comp(X) = comp( union over (i,j) of K_i ^ L_j ) <= #{(i,j) nonempty},

because each K_i ^ L_j is convex, hence connected.  Counting nonempty cells
needs only step A's max_min primitive (36 of them per pair of rotations) and no
union-find and no four-normal LP, so it samples hundreds of times faster than
step_b2 -- and it is an UPPER bound for the singleton term, which is all the
max(3) argument needs.

    python3 step_b3.py [n] [seed]
"""
import random
import sys
from collections import defaultdict

from step_a2 import max_min, normals
from step_a3 import formula, red


def cells(qa, qb):
    """Number of nonempty cells K_i ^ L_j among the 36."""
    na, nb = normals(qa), normals(qb)
    return sum(1 for a in range(6) for b in range(6)
               if max_min(na[a], nb[b]) > 1)


def rand_q(rng, h):
    while True:
        q = red(tuple(rng.randint(-h, h) for _ in range(4)))
        if any(q):
            return q


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    rng = random.Random(seed)
    best = defaultdict(lambda: [0, 0, None])
    # A mix of plain random rotations and rotations forced onto a given count:
    # 13 x 13 is far too rare to reach by chance, and it is the case that
    # decides the whole bound.
    pool = defaultdict(list)
    for _ in range(4000):
        q = rand_q(rng, rng.choice((2, 3, 5, 9, 17, 33, 65)))
        pool[formula(q)].append(q)
    print('pool sizes by two-cube count: %s'
          % {k: len(v) for k, v in sorted(pool.items())}, flush=True)
    keys = sorted(pool)
    for t in range(n):
        if t % 3 == 0:                       # forced combinations
            ka = rng.choice(keys)
            kb = rng.choice(keys)
            qa, qb = rng.choice(pool[ka]), rng.choice(pool[kb])
        else:                                # free random pairs
            h = rng.choice((2, 3, 5, 9, 17, 33, 65, 129))
            qa, qb = rand_q(rng, h), rand_q(rng, h)
        key = tuple(sorted((formula(qa), formula(qb))))
        c = cells(qa, qb)
        e = best[key]
        e[1] += 1
        if c > e[0]:
            e[0], e[2] = c, (qa, qb)
    print('\n%-10s %6s %9s   %s' % ("(P,P')", 'max', 'samples', 'witness'))
    for key in sorted(best, key=lambda k: (-best[k][0], k)):
        e = best[key]
        print('%-10s %6d %9d   %s' % (','.join(map(str, key)), e[0], e[1],
                                      e[2] if e[0] >= 14 else ''))
    g = {k: best[k][0] for k in best}
    top = max(g.values())
    off = max((v for k, v in g.items() if k != (13, 13)), default=0)
    print('\nmax cells overall            %d' % top)
    print('max cells with a non-13 pair %d' % off)
    print('\nimplied three-cube bounds (T <= 1 + 18 + three singleton terms):')
    print('   on (13,13,13):  T <= %d' % (19 + 3 * g.get((13, 13), top)))
    print('   any other cell: T <= %d' % (19 + 2 * off + g.get((13, 13), top)))


if __name__ == '__main__':
    main()
