#!/usr/bin/env python3
"""Step B, part 4: is g(P,P') = 16 only for (13,13)?

g(P,P') = max over pairs of rotations with two-cube counts P, P' of

    s = comp(box \\ (Ca u Cb)),

the singleton term of step_b.py.  Random sampling reaches a cell's typical
value, not its ceiling -- the mistake the n=4 census made, where the record's
own cell read 165 against a true 183.  So this hill-climbs s inside each
(P,P') combination, holding the counts fixed by rejection.

WHY THE CLIMB IS SHAPED THE WAY IT IS.  The first version accepted equal-value
moves and rescaled the quaternion at every step, and its witnesses came back
with 59-digit coordinates.  Those digits meant nothing: the reported (13,9)
witness has exactly the same (counts, s) as the height-12 pair
((1,0,-3,-4), (-3,1,-12,-3)), and a lattice probe at that small point keeps
26 of 728 neighbours -- 3^3 - 1, a **three-dimensional plateau**.  The climb
was not converging on anything; it was drifting inside a level set, paying for
it with unbounded arithmetic.  Huge coordinates out of a plateau-drifting
search are a symptom, not a discovery.

Two consequences, both implemented here:

  * HEIGHT CAP.  A move that inflates the reduced height past HCAP is refused.
    Anything reachable on the plateau is reachable at small height, and small
    integers keep the exact arithmetic fast.

  * RESTART ON PLATEAU.  After STALL fruitless moves the climb abandons the
    plateau and reseeds.  Drifting inside a level set costs budget and returns
    nothing; a plateau's interior is uniform by definition, so its INTERIOR is
    the one place a search should not linger (Postscript 75).

The best point of each combination is then measured for plateau dimension by
the 3^6 - 1 lattice probe, so the result carries the shape of its optimum and
not just its value.

    python3 step_b4.py [tries] [climb_steps]
"""
import itertools
import math
import random
import sys

from step_a2 import normals
from step_a3 import formula, red
from step_b import singleton_comp

HCAP = 4000        # refuse moves beyond this reduced height
STALL = 50         # fruitless moves before abandoning the plateau


def s_of(qa, qb):
    return singleton_comp(normals(qa), normals(qb))[0]


def height(q):
    return max(abs(x) for x in q)


def rand_q(rng, h):
    while True:
        q = red(tuple(rng.randint(-h, h) for _ in range(4)))
        if any(q):
            return q


def on(rng, want, h, tries=1500):
    for _ in range(tries):
        q = rand_q(rng, h)
        if formula(q) == want:
            return q
    return None


def jiggle(rng, q, want, scale):
    """A nearby rotation with the same count, at finer resolution but bounded
    height -- the cap is what stops the plateau drift."""
    for _ in range(120):
        c = [x * scale for x in q]
        for _ in range(rng.randint(1, 2)):
            c[rng.randrange(4)] += rng.randint(-3, 3)
        c = red(tuple(c))
        if any(c) and height(c) <= HCAP and formula(c) == want:
            return c
    return q


def seed(rng, want):
    for h in (2, 3, 5, 9, 17, 33):
        qa = on(rng, want[0], h)
        qb = on(rng, want[1], h)
        if qa and qb:
            return qa, qb
    return None


def plateau_dim(qa, qb, den=64):
    """Lattice-cardinality dimension of the level set {counts, s} at (qa,qb).
    A d-dimensional component contributes 3^d - 1 of the 3^6 - 1 neighbours."""
    base = (formula(qa), formula(qb), s_of(qa, qb))
    keep = 0
    for d in itertools.product((-1, 0, 1), repeat=6):
        if not any(d):
            continue
        cs, okc = [], True
        for j, q in enumerate((qa, qb)):
            w, x, y, z = q
            num = (w*den, x*den + d[3*j]*w, y*den + d[3*j+1]*w,
                   z*den + d[3*j+2]*w)
            if not any(num):
                okc = False
                break
            cs.append(red(num))
        if not okc:
            continue
        if formula(cs[0]) != base[0] or formula(cs[1]) != base[1]:
            continue
        if s_of(cs[0], cs[1]) == base[2]:
            keep += 1
    return keep, (math.log(keep + 1, 3) if keep else 0.0)


def best_for(rng, want, tries, steps):
    bs, bq = -1, None
    for _ in range(tries):
        sd = seed(rng, want)
        if sd is None:
            continue
        s = s_of(*sd)
        if s > bs:
            bs, bq = s, sd
    cur, cq = bs, bq
    stall = 0
    for _ in range(steps):
        if stall >= STALL:                      # plateau: reseed, keep record
            sd = seed(rng, want)
            if sd is None:
                break
            cur, cq, stall = s_of(*sd), sd, 0
            continue
        qa, qb = cq
        scale = rng.choice((1, 1, 2, 3, 5))
        if rng.random() < 0.5:
            qa = jiggle(rng, qa, want[0], scale)
        else:
            qb = jiggle(rng, qb, want[1], scale)
        s = s_of(qa, qb)
        if s > cur:
            cur, cq, stall = s, (qa, qb), 0
            if s > bs:
                bs, bq = s, (qa, qb)
                print('      climbed to %d  height %d' % (s, max(map(height, bq))),
                      flush=True)
        else:
            stall += 1
    return bs, bq


def main():
    tries = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    steps = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(20260803)
    combos = [(13, 13), (13, 9), (13, 5), (13, 4), (9, 9), (9, 5), (9, 4),
              (5, 5), (5, 4), (4, 4)]
    got = {}
    for want in combos:
        s, q = best_for(rng, want, tries, steps)
        got[want] = s
        keep, d = plateau_dim(*q)
        print('%-8s  g = %2d   dim %.2f (%d of 728)   height %d   %s'
              % (str(want), s, d, keep, max(map(height, q)), q), flush=True)
    print()
    off = max(v for k, v in got.items() if k != (13, 13))
    print('g(13,13) = %d ;  max g off (13,13) = %d' % (got[(13, 13)], off))
    print('=> T <= 19 + 3*%d = %d on (13,13,13)'
          % (got[(13, 13)], 19 + 3 * got[(13, 13)]))
    print('=> T <= 19 + 2*%d + %d = %d on every other cell'
          % (off, got[(13, 13)], 19 + 2 * off + got[(13, 13)]))


if __name__ == '__main__':
    main()
