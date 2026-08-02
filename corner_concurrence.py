#!/usr/bin/env python3
"""Search the 9-plane corner-concurrence stratum on the 393 base.

Postscript 12 found that records concentrate at high-multiplicity CORNER
concurrences — three cubes sharing a corner, nine face planes through one
point — and 723 is corner-dominated.  Every enumeration in this project so far
used edge-edge coplanarity and corner-on-face conditions; the corner-to-corner
stratum was never encoded, and it is the one records actually favour.

On the 393 base it is directly enumerable.  Cubes 3 = (2,1,1,1) and
4 = (1,1,1,1) are both rotations about (1,1,1), so both FIX that direction and
both have a corner at exactly (1,1,1) — a 6-plane concurrence already present
in the base.  A free cube with a corner there makes it 9-plane.

The free cubes that do so form four rational one-parameter families: a corner s
maps to (1,1,1) under R0 * Rot((1,1,1), theta), where R0 is any rotation taking
s to (1,1,1).  For s = (1,1,1), R0 = identity.  For the other corners a
180-degree rotation about the bisector works and is rational — e.g. (0,1,1,0)
takes (1,1,-1) to (1,1,1) — so all four families are integer-quaternion
sweepable.  (Corners come in antipodal pairs and a cube is centrally
symmetric, so eight corners give four distinct families.)

INVARIANT: every configuration is checked to actually HAVE a corner at (1,1,1)
before counting, in exact rational arithmetic — the point of the search is that
stratum, so a sweep that drifts off it silently would prove nothing.
"""
import collections
import json
import math
import subprocess
from fractions import Fraction as F

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
FIVES = ';'.join(','.join(map(str, q)) for q in FIVE)
CAP = 512


def qmul(p, q):
    w, x, y, z = p
    e, f, g, h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)


def red(q):
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    return tuple(x//g for x in q) if g > 1 else tuple(q)


def mat(q):
    w, x, y, z = q
    n = F(w*w + x*x + y*y + z*z)
    return [[F(w*w+x*x-y*y-z*z)/n, F(2*(x*y-w*z))/n, F(2*(x*z+w*y))/n],
            [F(2*(x*y+w*z))/n, F(w*w-x*x+y*y-z*z)/n, F(2*(y*z-w*x))/n],
            [F(2*(x*z-w*y))/n, F(2*(y*z+w*x))/n, F(w*w-x*x-y*y+z*z)/n]]


def has_corner_at_111(q):
    M = mat(q)
    for s in [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]:
        v = tuple(sum(M[i][j]*s[j] for j in range(3)) for i in range(3))
        if v == (1, 1, 1):
            return True
    return False


# R0 for each corner class: identity, and 180-degree turns about the bisectors
R0S = [(1, 0, 0, 0), (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1)]
LIMIT = 160


def main():
    cands, seen = [], set()
    for R0 in R0S:
        for a in range(-LIMIT, LIMIT + 1):
            for b in range(1, LIMIT + 1):
                if math.gcd(abs(a), b) != 1:
                    continue
                q = red(qmul(R0, (a, b, b, b)))
                if not any(q) or max(abs(x) for x in q) > CAP:
                    continue
                if q in seen:
                    continue
                seen.add(q)
                cands.append(q)
    print('candidates on the 9-plane corner-concurrence stratum: %d' % len(cands),
          flush=True)
    bad = [q for q in cands[:200] if not has_corner_at_111(q)]
    print('gate — sampled 200, off-stratum: %d (must be 0)' % len(bad), flush=True)
    if bad:
        print('GATE FAILED', flush=True)
        return
    hist = collections.Counter()
    best = (0, None)
    out = open('corner_concurrence_hits.jsonl', 'a')
    B = 400
    for s in range(0, len(cands), B):
        chunk = cands[s:s+B]
        res = subprocess.run(['./cube_regions_n', '--quats-stdin'],
                             input='\n'.join(FIVES+';'+','.join(map(str, q))
                                             for q in chunk)+'\n',
                             capture_output=True, text=True).stdout
        for ln, q in zip([l for l in res.splitlines() if l.startswith('{')], chunk):
            d = json.loads(ln)
            t = d.get('bounded')
            if t is None:
                continue
            hist[t] += 1
            if t > best[0]:
                best = (t, q)
            if t >= 723:
                out.write(json.dumps({'total': t, 'quat': list(q),
                                      'by_depth': d['by_depth']})+'\n')
                out.flush()
                if t > 727:
                    print('*** ABOVE 727: %d  %s' % (t, q), flush=True)
        print('  counted %d/%d, best %s' % (min(s+B, len(cands)), len(cands), best),
              flush=True)
    print('\nDONE. best = %s' % (best,), flush=True)
    print('top of the distribution:',
          {k: hist[k] for k in sorted(hist)[-14:]}, flush=True)


if __name__ == '__main__':
    main()
