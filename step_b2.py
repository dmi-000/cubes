#!/usr/bin/env python3
"""Step B, part 2: the singleton term as a function of the two pair counts.

From step_b.py the three-cube total decomposes exactly as

    T = 1 + sum_{ij} p_ij + sum_i s_i,     p_ij = comp((Ci^Cj)\\Ck) <= 6,

so 67 = 1 + 18 + 48 forces every p_ij = 6 AND every s_i = 16.  Central symmetry
makes every term even (a component of a class maps to a component under
x -> -x, and none is self-paired since the only fixed point, the origin, lies
in all three cubes), so T is odd and the terms move in steps of 2.

The point of this file: **s_i depends only on the two relative rotations at
cube i**, not on the third pair at all.  s_i = comp(box \\ (Cj u Ck)) with Cj,
Ck placed by R_ij and R_ik.  So it is a TWO-rotation quantity and can be
sampled with the two rotations chosen independently -- no consistent triple
needed, and the 13-locus can be hit directly by rejection instead of hoped for.

Define

    g(P, P') = max s over pairs of rotations whose two-cube counts are P, P'.

If g(13,13) = 16 and g <= 14 whenever either argument is below 13, then for any
label other than (13,13,13) at least two of the three cubes sit on a non-13
pair, and

    T <= 1 + 18 + 14 + 14 + 16 = 63 < 67,

while on (13,13,13) the same decomposition gives T <= 1 + 18 + 48 = 67, which
is attained.  That is max(3) = 67 -- a proof whose only remaining input is a
statement about TWO cubes.

    python3 step_b2.py table  [n]      random pairs, g table by (P,P')
    python3 step_b2.py probe  [n]      both rotations forced onto the 13-locus
"""
import random
import sys
from collections import defaultdict

from step_a2 import normals
from step_a3 import formula, red
from step_b import singleton_comp


def s_of(qa, qb):
    """comp(box \\ (Ca u Cb)) for two rotations given in the base cube's frame."""
    return singleton_comp(normals(qa), normals(qb))[0]


def rand_q(rng, h):
    while True:
        q = red(tuple(rng.randint(-h, h) for _ in range(4)))
        if any(q):
            return q


def rand_on(rng, want, h):
    """A rotation whose two-cube count is `want`, by rejection."""
    for _ in range(20000):
        q = rand_q(rng, h)
        if formula(q) == want:
            return q
    return None


def table(n):
    rng = random.Random(202608031)
    best = defaultdict(lambda: [0, 0, None])       # (P,P') -> [max s, seen, cfg]
    for t in range(n):
        h = rng.choice((2, 3, 5, 9, 17, 33, 65))
        qa, qb = rand_q(rng, h), rand_q(rng, h)
        key = tuple(sorted((formula(qa), formula(qb))))
        s = s_of(qa, qb)
        e = best[key]
        e[1] += 1
        if s > e[0]:
            e[0], e[2] = s, (qa, qb)
        if (t + 1) % 200 == 0:
            print('  ... %d pairs' % (t + 1), flush=True)
    show(best)


def probe(n):
    """Force both rotations onto the 13-locus, and onto 13 x (each other count).

    The random table almost never lands on 13 twice, and 16 is exactly the
    value that has to be pinned down, so it is sampled directly."""
    rng = random.Random(202608032)
    best = defaultdict(lambda: [0, 0, None])
    combos = [(13, 13), (13, 9), (13, 5), (13, 4), (9, 9), (9, 5), (9, 4),
              (5, 5), (5, 4), (4, 4)]
    for want in combos:
        for t in range(n):
            h = rng.choice((2, 3, 5, 9, 17, 33))
            qa = rand_on(rng, want[0], h)
            qb = rand_on(rng, want[1], h)
            if qa is None or qb is None:
                continue
            key = tuple(sorted(want))
            s = s_of(qa, qb)
            e = best[key]
            e[1] += 1
            if s > e[0]:
                e[0], e[2] = s, (qa, qb)
        e = best[tuple(sorted(want))]
        print('  %-8s max s = %2d over %d samples' % (str(want), e[0], e[1]),
              flush=True)
    show(best)


def show(best):
    print('\n%-10s %6s %8s   %s' % ('(P,P\')', 'max s', 'samples', 'witness'))
    for key in sorted(best, key=lambda k: -best[k][0]):
        e = best[key]
        print('%-10s %6d %8d   %s' % (','.join(map(str, key)), e[0], e[1],
                                      e[2] if e[0] >= 14 else ''))
    print('\nbound implied: T <= 1 + 18 + (three singleton terms)')
    g = {k: best[k][0] for k in best}
    if (13, 13) in g:
        off = max((v for k, v in g.items() if k != (13, 13)), default=0)
        print('   g(13,13) = %d ;  max g off (13,13) = %d' % (g[(13, 13)], off))
        print('   => label (13,13,13): T <= %d' % (19 + 3 * g[(13, 13)]))
        print('   => any other label:  T <= %d' % (19 + 2 * off + g[(13, 13)]))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'table'
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    (table if cmd == 'table' else probe)(n)
