#!/usr/bin/env python3
"""Which of the lines through 727 configurations are actually ARCS?

Every Q(sqrt d) configuration at 727 has Cayley coordinates a + b*sqrt(d) with
a, b RATIONAL, so it names a rational line P(t) = a + t*b and sits on it at
t = sqrt(d).  That is how arcs A, B and C were found.  But naming a line is not
the same as 727 holding ALONG it: the count might hold only at the conjugate
pair, in which case the "line" is an artefact of the parametrisation and not a
component of the maximiser set at all.

This sweeps each distinct line around its own sqrt(d) and reports the runs where
727 actually holds.  A line whose only 727s are isolated samples is NOT an arc.
"""
import collections
import json
import math
import subprocess
import sys
from fractions import Fraction as F

BASE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]


def cayley(q, d):
    (w0, w1) = q[0]
    den = w0*w0 - d*w1*w1
    a, b = [], []
    for (c0, c1) in q[1:]:
        a.append(F(c0*w0 - d*c1*w1, den))
        b.append(F(c1*w0 - c0*w1, den))
    return a, b


def canon(a, b):
    nz = next((i for i in range(3) if b[i] != 0), None)
    if nz is None:
        return None
    v = [x / b[nz] for x in b]
    if v[nz] < 0:
        v = [-x for x in v]
    dot = sum(a[i]*v[i] for i in range(3))
    nn = sum(v[i]*v[i] for i in range(3))
    return (tuple(v), tuple(a[i] - dot/nn*v[i] for i in range(3)))


def counts(pts):
    lines = []
    for p in pts:
        den = 1
        for x in p:
            den = den * x.denominator // math.gcd(den, x.denominator)
        q = (den,) + tuple(int(x*den) for x in p)
        lines.append(';'.join(','.join(map(str, c)) for c in BASE) + ';'
                     + ','.join(map(str, q)))
    out = []
    for i in range(0, len(lines), 2000):
        r = subprocess.run(['./cube_regions_n', '--quats-stdin'],
                           input='\n'.join(lines[i:i+2000]) + '\n',
                           capture_output=True, text=True)
        out += [json.loads(l).get('bounded') for l in r.stdout.splitlines()
                if l.startswith('{')]
    return out


def main():
    reps = {}
    for f in __import__('glob').glob('wide_campaign_shard_*.jsonl'):
        for l in open(f):
            r = json.loads(l)
            if r['total'] != 727:
                continue
            a, b = cayley([tuple(c) for c in r['quat']], r['d'])
            k = canon(a, b)
            if k and k not in reps:
                reps[k] = (a, b, r['d'])
    print('distinct lines: %d' % len(reps), flush=True)
    STEP, REACH = F(1, 16), 40          # t within +-2.5 of sqrt(d)
    arcs, isolated, dead = [], [], 0
    for idx, (k, (a, b, d)) in enumerate(sorted(reps.items(), key=lambda x: str(x[0]))):
        t0 = F(int(math.isqrt(d * 10**8)), 10**4)      # rational near sqrt(d)
        ts = [t0 + STEP*n for n in range(-REACH, REACH+1)]
        res = counts([[a[i] + t*b[i] for i in range(3)] for t in ts])
        runs = []
        for t, c in zip(ts, res):
            if runs and runs[-1][0] == c:
                runs[-1][2] = t
            else:
                runs.append([c, t, t])
        good = [r for r in runs if r[0] == 727]
        width = sum(1 for c in res if c == 727)
        if not good:
            dead += 1
        elif width >= 3:
            arcs.append((k, d, width, good))
        else:
            isolated.append((k, d, width))
        if (idx+1) % 20 == 0:
            print('  ... %d/%d   arcs %d  isolated %d  none %d'
                  % (idx+1, len(reps), len(arcs), len(isolated), dead), flush=True)
    print('\nRESULT over %d lines, sweeping t in sqrt(d) +- 2.5 at step 1/16:' % len(reps))
    print('  genuine ARCS (727 on >=3 consecutive samples): %d' % len(arcs))
    print('  727 only at isolated samples:                  %d' % len(isolated))
    print('  no 727 found on the swept range:               %d' % dead)
    arcs.sort(key=lambda x: -x[2])
    print('\nwidest arcs:')
    for k, d, w, good in arcs[:15]:
        print('  dir %-24s d=%-6d samples %3d  runs %s'
              % (','.join(str(x) for x in k[0]), d, w,
                 ' '.join('[%s,%s]' % (r[1], r[2]) for r in good[:3])))


if __name__ == '__main__':
    main()
