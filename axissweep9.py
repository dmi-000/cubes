#!/usr/bin/env python3
"""n=9 Cayley-axis re-sweep — the procedure that caught the n=8 record.

WHY. [P101] found 1895 sitting inside a window an earlier sweep had already
covered: that sweep recorded WHERE A KNOWN VALUE HELD rather than the MAXIMUM over
the line, so a rise read as a dropout. The fix was to re-sweep reporting the
maximum, and P101 states it did so "at n = 5, 6, 7, 8". **n = 9 was not included**,
and 2785 already existed when P101 was written. [P179](#p179) names this as the
highest-prior untried check against the n=9 record; this runs it.

METHOD. For each free cube and each of its three Cayley coordinates, displace by
s over [-1/2, 1/2] and report the MAXIMUM over the line, never the indicator of
2785. Two resolutions are combined because a coarse step can bridge a thin chamber
(METHODS 8): a uniform grid at 1/256, plus every fraction of denominator <= 24,
which is where small-representative records actually sit -- the n=9 ninth cube is
(56,56,55,56), Cayley (1, 55/56, 1).

Unevaluable points are COUNTED, never treated as "no change".
"""
import json, os, subprocess, sys, time
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from growth727 import BASE

ENG = os.path.join(HERE, 'cube_regions_n')
C9 = BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61), (56, 56, 55, 56)]


def quat_of(c):
    den = 1
    for x in c:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    q = (den, int(F(c[0]) * den), int(F(c[1]) * den), int(F(c[2]) * den))
    g = 0
    for v in q:
        g = gcd(g, abs(v))
    return tuple(v // (g or 1) for v in q)


def batch(cfgs):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run([ENG, '--quats-stdin'], input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l)['bounded'])
        except Exception: out.append(None)
    return out + [None] * (len(cfgs) - len(out))


def main():
    steps = sorted({F(k, 256) for k in range(-128, 129)} |
                   {F(a, b) for b in range(1, 25) for a in range(-b // 2, b // 2 + 1)})
    print('n=9 axis re-sweep: %d displacements per line, %d lines'
          % (len(steps), 8 * 3), flush=True)
    base_c = [[F(q[1], q[0]), F(q[2], q[0]), F(q[3], q[0])] for q in C9[1:]]
    t0, tried, unev, best, where = time.time(), 0, 0, 2785, None
    for i in range(8):
        for j in range(3):
            cfgs, tags = [], []
            for s in steps:
                c = [list(v) for v in base_c]
                c[i][j] = c[i][j] + s
                cfg = [C9[0]] + [quat_of(v) for v in c]
                if max(abs(x) for q in cfg for x in q) > 512:
                    continue
                cfgs.append(cfg); tags.append(s)
            vals = []
            for k in range(0, len(cfgs), 400):
                vals += batch(cfgs[k:k+400])
            tried += len(cfgs)
            unev += sum(1 for v in vals if v is None)
            ok = [(v, s) for v, s in zip(vals, tags) if v is not None]
            m, sm = max(ok) if ok else (None, None)
            if m is not None and m > best:
                best, where = m, (i + 1, j, sm)
            print('   cube %d axis %d: %4d pts, %3d unevaluable, MAX %s at s=%s%s'
                  % (i + 1, j, len(cfgs), sum(1 for v in vals if v is None), m, sm,
                     '   *** BEATS 2785 ***' if m and m > 2785 else ''), flush=True)
    print('\n%d evaluations, %d unevaluable, best over all lines: %d'
          % (tried, unev, best), flush=True)
    if where: print('   BEATEN at cube %d axis %d s=%s' % where, flush=True)
    json.dump({'evaluations': tried, 'unevaluable': unev, 'best': best,
               'where': str(where), 'secs': time.time() - t0},
              open(os.path.join(HERE, 'axissweep9.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
