#!/usr/bin/env python3
"""n=9 axis re-sweep, WIDE — recovering the points the first pass skipped.

P179 Addendum 1 swept 24 Cayley-axis lines but skipped any displacement whose
cleared quaternion exceeded the narrow engine's 512-component cap: ~3 600 of
10 392 points, concentrated on cubes 7 and 8 (the two most recently added, and
arguably where a new record would most plausibly hide). Those are the real
coverage gap; the 4 outright refusals are geometric degeneracies no engine reaches.

This sweeps every line at full resolution, routing each point to the engine that
can take it: narrow below 512, `cube_regions_q2w` above. Reports the MAXIMUM over
each line, never the indicator of 2785 — the distinction that cost P101 the n=8
record the first time.
"""
import json, os, subprocess, sys, time
from fractions import Fraction as F
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from growth727 import BASE

ENG = os.path.join(HERE, 'cube_regions_n')
ENGW = os.path.join(HERE, 'cube_regions_q2w')
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


def batch(cfgs, wide):
    if not cfgs:
        return []
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    cmd = ([ENGW, '--d', '0', '--quats-stdin'] if wide else [ENG, '--quats-stdin'])
    p = subprocess.run(cmd, input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l)['bounded'])
        except Exception: out.append(None)
    return out + [None] * (len(cfgs) - len(out))


def main():
    steps = sorted({F(k, 256) for k in range(-128, 129)} |
                   {F(a, b) for b in range(1, 25) for a in range(-b // 2, b // 2 + 1)})
    base_c = [[F(q[1], q[0]), F(q[2], q[0]), F(q[3], q[0])] for q in C9[1:]]
    t0, tot, nwide, unev, best, where = time.time(), 0, 0, 0, 2785, None
    for i in range(8):
        for j in range(3):
            narrow, wide, tagn, tagw = [], [], [], []
            for s in steps:
                c = [list(v) for v in base_c]
                c[i][j] = c[i][j] + s
                cfg = [C9[0]] + [quat_of(v) for v in c]
                if max(abs(x) for q in cfg for x in q) > 512:
                    wide.append(cfg); tagw.append(s)
                else:
                    narrow.append(cfg); tagn.append(s)
            vals = []
            for k in range(0, len(narrow), 400):
                vals += list(zip(batch(narrow[k:k+400], False), tagn[k:k+400]))
            for k in range(0, len(wide), 200):
                vals += list(zip(batch(wide[k:k+200], True), tagw[k:k+200]))
            tot += len(narrow) + len(wide); nwide += len(wide)
            u = sum(1 for v, _ in vals if v is None); unev += u
            ok = [(v, s) for v, s in vals if v is not None]
            m, sm = max(ok) if ok else (None, None)
            if m is not None and m > best:
                best, where = m, (i + 1, j, sm)
            print('   cube %d axis %d: %3d narrow + %3d WIDE = %3d pts, %d unevaluable, '
                  'MAX %s at s=%s%s'
                  % (i + 1, j, len(narrow), len(wide), len(narrow) + len(wide), u, m, sm,
                     '   *** BEATS 2785 ***' if m and m > 2785 else ''), flush=True)
    print('\n%d evaluations (%d via the wide engine), %d unevaluable, best %d (%.0fs)'
          % (tot, nwide, unev, best, time.time() - t0), flush=True)
    if where: print('   BEATEN at cube %d axis %d s=%s' % where, flush=True)
    json.dump({'evaluations': tot, 'wide': nwide, 'unevaluable': unev,
               'best': best, 'where': str(where), 'secs': time.time() - t0},
              open(os.path.join(HERE, 'axissweep9w.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
