#!/usr/bin/env python3
"""Dense sweep of the body-diagonal family — 3 angles, solved on a grid of simple rationals.

Attempt 4 in EXPLORATION_141.md. Attempt 3's random sweep over 145 axes found the body
diagonal (1,1,1) reaching total 145 with depth-1 72, immediately past the 141 plateau and
well past the best depth-1 the Haar ensemble ever produced (46). That was 400 random
angle-sets; this sweeps the family properly.

With cube 0 fixed and all four cubes sharing the axis, the family has exactly THREE free
parameters -- one Cayley angle per remaining cube -- so it can be gridded rather than
sampled. Simple rationals are used for the grid because they keep the quaternions short,
which is the same representative discipline that mattered everywhere else in this project.

A grid is still a sample of a continuum: whatever it finds is a LOWER bound on the family's
maximum, and the exact maximum would need the walls of the 3-parameter slice solved. That
is the honest reading and it is why the next step after this is to CLIMB from the best
point found, not to declare the family's maximum.
"""
import itertools, json, subprocess, sys
from fractions import Fraction as F
from math import gcd

AXIS = tuple(int(x) for x in (sys.argv[1].split(',') if len(sys.argv)>1 else '1,1,0'.split(',')))

def q_axis(t, axis=AXIS):
    a, b, c = axis
    num, den = t.numerator, t.denominator
    q = (den, num * a, num * b, num * c)
    g = 0
    for v in q:
        g = gcd(g, abs(v))
    return tuple(v // (g or 1) for v in q)

def batch(cfgs):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                       capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try:
            d = json.loads(l)
            out.append((d['bounded'], int(d['by_depth'].get('1', 0))))
        except Exception:
            out.append((None, None))
    return out + [(None, None)] * (len(cfgs) - len(out))

if __name__ == '__main__':
    # simple rationals, both signs, plus 0 (cube coincident with cube 0 -- kept so the
    # sweep can tell us if degeneracy helps rather than assuming it does not)
    vals = [F(0)] + [F(p, q) for q in (1, 2, 3, 4, 5, 6, 7, 8) for p in range(-8, 9)
                     if p and gcd(abs(p), q) == 1]
    vals = sorted(set(vals))
    print('shared-axis family, axis %s: %d angle values, %d sorted triples' % (AXIS,
             len(vals), len(vals) * (len(vals) + 1) * (len(vals) + 2) // 6), flush=True)
    best = (0, 0, None)
    buf, meta = [], []
    done = 0
    # THE COMPOUND IS A SET. Permuting the three free angles permutes the cubes and gives
    # the same compound, so only sorted triples need evaluating: 658 503 products become
    # 117 480 combinations, a 5.6x cut for nothing. The same observation cut the arc menu
    # 7.2x ([P219]) -- enumerating labelled objects where the object is unlabelled.
    for t1, t2, t3 in itertools.combinations_with_replacement(vals, 3):
        buf.append([q_axis(F(0)), q_axis(t1), q_axis(t2), q_axis(t3)])
        meta.append((t1, t2, t3))
        if len(buf) >= 2000:
            for (c, d1), cf, m in zip(batch(buf), buf, meta):
                if c and c > best[0]:
                    best = (c, d1, cf)
                    print('   total %4d  depth-1 %3d   angles %s' % (c, d1, str(m)), flush=True)
            done += len(buf); buf, meta = [], []
            print('   ... %d evaluated' % done, flush=True)
    for (c, d1), cf, m in zip(batch(buf), buf, meta):
        if c and c > best[0]:
            best = (c, d1, cf)
            print('   total %4d  depth-1 %3d   angles %s' % (c, d1, str(m)), flush=True)
    print('\nBEST in the shared-axis family: total %d, depth-1 %d' % (best[0], best[1]), flush=True)
    print(';'.join(','.join(map(str, q)) for q in best[2]), flush=True)
