#!/usr/bin/env python3
"""The corner-sharing family, done properly: WHICH corner each cube lands on is a choice.

A 9-fold plane concurrence is three cubes sharing a corner ([ALGEBRAIC_SEARCH.md]), and
the n=4 record has exactly two of them, at the antipodal points (1,-1,-1) and (-1,1,1),
involving cubes 0, 1 and 2.

A first attempt built all three as rotations about that corner's axis. That reaches two
9-folds 50.8% of the time -- against essentially never in 2.58M random draws, so
constructing the stratum works -- but it topped out at 163 and never produced the record's
signature. The structural check said why: **the record's cube 2 is NOT a rotation about
that axis.** "Sharing a corner" only forces a common axis when the cubes map the SAME
corner there. Cube 2 maps a different one of its eight corners to the same point, which is
the identical incidence reached by a different rotation.

So each cube contributes a DISCRETE choice (which of its 8 corners lands on p) and a
CONTINUOUS one (a rotation about p afterwards). The first attempt fixed the discrete
choice at the identity corner and therefore searched one eighth of the family.

For corner c and target p, the quaternion (1 + c.p, c x p) carries c to p -- exact in
integers, since c and p have entries +-1 -- and the general solution is that composed with
a rotation about p. Both are integer quaternion products, so nothing leaves Q.
"""
import itertools, json, random, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
from signature import signature

CORNERS = [c for c in itertools.product((1, -1), repeat=3)]

def canon(t):
    g = 0
    for v in t:
        g = gcd(g, abs(int(v)))
    t = tuple(int(v) // (g or 1) for v in t)
    for v in t:
        if v > 0: break
        if v < 0: t = tuple(-x for x in t); break
    return t

def qmul(p, r):
    w, x, y, z = p; e, f, g, h = r
    return canon((w*e - x*f - y*g - z*h, w*f + x*e + y*h - z*g,
                  w*g - x*h + y*e + z*f, w*h + x*g - y*f + z*e))

def carry(c, p):
    """integer quaternion rotating corner direction c onto p: (1 + c.p, c x p) scaled"""
    dot = sum(a*b for a, b in zip(c, p))
    cr = (c[1]*p[2] - c[2]*p[1], c[2]*p[0] - c[0]*p[2], c[0]*p[1] - c[1]*p[0])
    if cr == (0, 0, 0):
        return (1, 0, 0, 0) if dot > 0 else None      # antipodal: any 180 deg, skip
    return canon((3 + dot, cr[0], cr[1], cr[2]))      # |c|^2 = 3 for a cube corner

def about(p, t):
    return canon((t.denominator, t.numerator*p[0], t.numerator*p[1], t.numerator*p[2]))

def draw(rng, p, vals, nshare=3, n=4):
    """nshare cubes share the corner point p; the rest are free rotations about p"""
    out = [(1, 0, 0, 0)]
    while len(out) < n:
        if len(out) < nshare:
            c = rng.choice(CORNERS)
            q0 = carry(c, p)
            if q0 is None:
                continue
            out.append(qmul(about(p, rng.choice(vals)), q0))
        else:
            out.append(canon(tuple(rng.randint(-9, 9) for _ in range(4))) or (1, 0, 0, 0))
    return out

def cnt(cfg):
    s = ';'.join(','.join(map(str, q)) for q in cfg)
    try:
        return json.loads(subprocess.run(['./cube_regions_n', '--quats', s],
                                         capture_output=True, text=True).stdout).get('bounded')
    except Exception:
        return None

if __name__ == '__main__':
    TARGET = ((4, 96), (6, 8), (9, 2))
    TRIES = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    rng = random.Random(17)
    vals = [F(p, q) for q in (1,2,3,4,5,6,7,8) for p in range(-8,9) if p and gcd(abs(p), q) == 1]
    P = (1, -1, -1)                                    # the record's own shared corner
    best = {}
    nine = tgt = n = 0
    for _ in range(TRIES):
        cfg = draw(rng, P, vals)
        c = cnt(cfg)
        if not c:
            continue
        n += 1
        sg = signature(cfg)
        if dict(sg).get(9, 0) >= 2:
            nine += 1
        if sg == TARGET:
            tgt += 1
        if c > best.get(sg, (0,))[0]:
            best[sg] = (c, cfg)
    print('corner-sharing family, all 8 corner choices, %d configurations' % n)
    print('  two or more 9-fold points : %d (%.1f%%)' % (nine, 100.0*nine/max(n,1)))
    print('  the RECORD signature      : %d' % tgt)
    print('  distinct signatures       : %d' % len(best))
    print()
    for c, s in sorted(((v[0], s) for s, v in best.items()), reverse=True)[:6]:
        print('     %3d   %s' % (c, s))
    top = max(best.values(), key=lambda t: t[0])
    print()
    print('  best configuration: %s' % ';'.join(','.join(map(str, q)) for q in top[1]))
