#!/usr/bin/env python3
"""n=6 from the record construction, with one body diagonal REUSED.

[P225]: the records are a hub cube plus others sharing body diagonals with it (13-pairs),
remaining pairs kept axis-in-plane (9-pairs). Four diagonals exist, so the construction
saturates at n=5 (the 393 uses each exactly once). At n=6 a fifth non-hub cube must either
be generic or REUSE a diagonal -- and 727 does have two generic 4-pairs.

This enumerates the reuse branch: hub + five cubes on the four diagonals, one diagonal
carrying two cubes, angles swept over simple rationals. Target to beat: 727.

Angles are kept to small denominators because every optimum found so far sits at a simple
rational -- the n=4 record is exactly t = +-1/4, and moving 1/48 off it costs 12 regions,
so the optima are coincidence points and not smooth maxima.
"""
import itertools, json, subprocess, sys, time
from fractions import Fraction as F
from math import gcd

DIAG = [(1,1,1), (1,1,-1), (1,-1,1), (1,-1,-1)]

def q_axis(ax, t):
    p, d = t.numerator, t.denominator
    q = (d, p*ax[0], p*ax[1], p*ax[2])
    g = 0
    for v in q:
        g = gcd(g, abs(v))
    return tuple(v // (g or 1) for v in q)

def batch(cfgs, exe='./cube_regions_n'):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run([exe, '--quats-stdin'], input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try:
            out.append(json.loads(l).get('bounded'))
        except Exception:
            out.append(None)
    return out + [None] * (len(cfgs) - len(out))

if __name__ == '__main__':
    VALS = sorted({F(p, q) for q in (1,2,3,4,5) for p in range(-5,6) if p and gcd(abs(p), q) == 1})
    # assignment: each of the four diagonals once, plus one repeated -> 4 choices of which
    assigns = [tuple(list(range(4)) + [r]) for r in range(4)]
    print('n=6 reuse family: %d angles, %d diagonal assignments' % (len(VALS), len(assigns)), flush=True)
    print('target to beat: 727', flush=True)
    best = (0, None); t0 = time.time(); n = 0
    buf, meta = [], []
    def flush():
        global best, n
        for c, cf, m in zip(batch(buf), buf, meta):
            if not c: continue
            n += 1
            if c > best[0]:
                best = (c, cf)
                print('   %4d  assign %s  t %s  (%.0fs, %d evaluated)'
                      % (c, m[0], [str(x) for x in m[1]], time.time()-t0, n), flush=True)
    for asg in assigns:
        for ts in itertools.product(VALS, repeat=5):
            buf.append([(1,0,0,0)] + [q_axis(DIAG[a], t) for a, t in zip(asg, ts)])
            meta.append((asg, ts))
            if len(buf) >= 4000:
                flush(); buf, meta = [], []
    flush()
    print('\nevaluated %d ; best %d' % (n, best[0]), flush=True)
    if best[1]:
        print(';'.join(','.join(map(str, q)) for q in best[1]), flush=True)
