#!/usr/bin/env python3
"""Two shared axes instead of one — a strictly richer structured ensemble.

Attempt 8 in EXPLORATION_141.md. One shared axis reaches 161 and stops: attempt 6 showed a
generic climb from there gains nothing, and attempt 7 is checking whether the family can
even hold depth-2 at its cap. Either way the one-axis family buys depth-1 by spending
depth-2, and the record spends nothing.

The obvious generalisation is more than one axis: cubes partitioned between two shared
axes, so some pairs share an axis and others do not. This contains the one-axis family
(both axes equal) so it cannot do worse, and it is still a random search under a
constructible measure -- axis pairs and the partition are sampled, not chosen from
knowledge of what the record looks like.

Sampled rather than swept because the axis pairs alone are 145*146/2 = 10 585 and each
needs many angle draws; a sweep would cost hours for a question a sample answers in
minutes. If a promising pair shows up it can be swept densely afterwards, which is the
same two-stage shape that worked for the single axis.
"""
import itertools, json, random, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
from symmetrize import canon, axes

def q_axis(axis, t):
    a, b, c = axis
    p, d = t.numerator, t.denominator
    return canon((d, p * a, p * b, p * c))

def batch(cfgs):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                       capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try:
            d = json.loads(l)
            out.append((d['bounded'], int(d['by_depth'].get('1', 0)), int(d['by_depth'].get('2', 0))))
        except Exception:
            out.append((None, None, None))
    return out + [(None, None, None)] * (len(cfgs) - len(out))

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    TRIES = int(sys.argv[2]) if len(sys.argv) > 2 else 30000
    AX = axes(3)
    rng = random.Random(31337)
    vals = [F(p, q) for q in (1, 2, 3, 4, 5, 6, 7, 8) for p in range(-8, 9)
            if p and gcd(abs(p), q) == 1] + [F(0)]
    print('two-axis ensemble, %d random configurations, n=%d' % (TRIES, n), flush=True)
    print('(one axis reaches 161 with depth-2 at 56; the record is 183 with depth-2 at its cap 66)',
          flush=True)
    best = (0, None, None)
    bestcap = (0, None, None)          # best depth-1 among those holding depth-2 = 66
    buf, meta = [], []
    for i in range(TRIES):
        u, v = rng.choice(AX), rng.choice(AX)
        which = [rng.randint(0, 1) for _ in range(n - 1)]
        cfg = [(1, 0, 0, 0)] + [q_axis(u if w else v, rng.choice(vals)) for w in which]
        buf.append(cfg); meta.append((u, v, which))
        if len(buf) >= 3000:
            for (c, d1, d2), cf, m in zip(batch(buf), buf, meta):
                if not c:
                    continue
                if c > best[0]:
                    best = (c, cf, m)
                    print('   total %4d  depth-1 %3d  depth-2 %3d   axes %s/%s' % (c, d1, d2, m[0], m[1]), flush=True)
                if d2 == 66 and d1 > bestcap[0]:
                    bestcap = (d1, cf, c)
                    print('   *** depth-2 AT CAP 66 with depth-1 %3d (total %d)' % (d1, c), flush=True)
            buf, meta = [], []
    print('\nBEST total %d' % best[0], flush=True)
    if best[1]:
        print(';'.join(','.join(map(str, q)) for q in best[1]), flush=True)
    print('BEST with depth-2 at its cap: depth-1 %d, total %s' % (bestcap[0], bestcap[2]), flush=True)
    if bestcap[1]:
        print(';'.join(','.join(map(str, q)) for q in bestcap[1]), flush=True)
