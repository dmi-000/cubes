#!/usr/bin/env python3
"""Draw starts from a STRUCTURED ensemble instead of the Haar one.

Attempt 3 in EXPLORATION_141.md. Attempt 1 showed the best depth-1 in 4 000 Haar draws is
46 while the record needs 92, so the Haar ensemble does not contain the neighbourhood we
need. Rather than search harder inside it, change the ensemble.

The structure searched here is the cheapest non-trivial one available: all cubes sharing a
single rotation AXIS. It is constructible from the geometry with no lookup -- a rotation
by angle t (as a Cayley parameter) about an integer axis (a,b,c) is the integer quaternion
(1, t*a, t*b, t*c) cleared of denominators -- and it is a genuinely random search, just
under a different measure. WHICH axis is good is not assumed: every primitive integer axis
with components in [-3,3] is swept, and the angles are drawn at random.

What this does and does not import from the repository: it uses the general fact that
cubes sharing an axis are a special family, which is geometry, not a stored answer. No
recorded configuration is read, and the sweep is free to report that the best axis is one
nobody has written down.

Honest limitation stated up front: this ensemble is Haar-NULL. It cannot be reached by
perturbing a random configuration, so if it wins, the finding is "the target is on a
structured set", not "climbing from random starts gets there".
"""
import itertools, json, subprocess, sys, random
from math import gcd
from fractions import Fraction as F

def q_axis(axis, t):
    """integer quaternion for a rotation about `axis` with Cayley parameter t"""
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
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    per = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rng = random.Random(4242)
    axes = []
    for t in itertools.product(range(-3, 4), repeat=3):
        if not any(t):
            continue
        g = 0
        for v in t:
            g = gcd(g, abs(v))
        a = tuple(v // g for v in t)
        for v in a:
            if v > 0: break
            if v < 0: a = tuple(-x for x in a); break
        if a not in axes:
            axes.append(a)
    print('%d primitive axes with components in [-3,3]; %d random angle-sets each; n=%d'
          % (len(axes), per, n), flush=True)
    print('(climbing from Haar starts plateaus at 141; best Haar depth-1 is 46)', flush=True)
    best = (0, 0, None, None)
    for ax in axes:
        cfgs = []
        for _ in range(per):
            ts = [F(rng.randint(-40, 40), rng.randint(1, 40)) for _ in range(n)]
            cfgs.append([q_axis(ax, t) for t in ts])
        res = batch(cfgs)
        ok = [(c, d1, cf) for (c, d1), cf in zip(res, cfgs) if c]
        if not ok:
            continue
        top = max(ok)
        if top[0] > best[0]:
            best = (top[0], top[1], ax, top[2])
            print('   axis %-12s best total %4d  depth-1 %3d' % (str(ax), top[0], top[1]), flush=True)
    print('\nBEST over the shared-axis ensemble: total %d, depth-1 %d, axis %s'
          % (best[0], best[1], best[2]), flush=True)
    if best[3]:
        print(';'.join(','.join(map(str, q)) for q in best[3]), flush=True)
