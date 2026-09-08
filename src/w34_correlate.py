#!/usr/bin/env python3
"""Do the unmodelled walls W3/W4 predict a high region count?

base_points.py identifies the two codimension-1 coincidence types no search
in this project has enumerated, as finite catalogues against the fixed 393
base: W4, a free-cube face plane through one of the base's 424 real triple
points; W3, a free-cube edge meeting one of the base's 360 crossing lines.

incidence2.py showed that the known records sit on a couple of these but so
do generic controls, so the raw hit count is not by itself a discriminator.
The question that decides whether the strata are worth enumerating is
statistical: among configurations counted on the SAME base, does a larger
W3/W4 signature go with a larger region count?

This samples integer quaternions, counts them with the C++ engine, computes
both signatures exactly, and reports the count distribution per signature
bucket.

INVARIANT: the sample must not be selected on the count, or the correlation
is guaranteed by construction.  Quaternions are drawn from a height ladder
only -- nothing about the region count or the incidence structure enters the
draw.
"""
import collections
import json
import math
import random
import statistics
import subprocess
import sys

from base_points import FIVE, mat
from incidence2 import base_catalogue, w3_count, w4_count

FIVES = ';'.join(','.join(map(str, q)) for q in FIVE)
HEIGHTS = [4, 8, 16, 40, 100, 250, 512]


def draw(rng):
    h = rng.choice(HEIGHTS)
    while True:
        q = tuple(rng.randint(-h, h) for _ in range(4))
        if any(q):
            g = 0
            for x in q:
                g = math.gcd(g, abs(x))
            return tuple(x // g for x in q)


def counts(quats):
    inp = '\n'.join(FIVES + ';' + ','.join(map(str, q)) for q in quats) + '\n'
    out = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                         capture_output=True, text=True).stdout
    rows = [json.loads(l) for l in out.splitlines() if l.startswith('{')]
    return [r.get('bounded') for r in rows]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
    rng = random.Random(20260802)
    pts, lines = base_catalogue()
    print('base: %d real triple points, %d crossing lines' % (len(pts), len(lines)),
          flush=True)

    quats = []
    seen = set()
    while len(quats) < n:
        q = draw(rng)
        if q not in seen:
            seen.add(q)
            quats.append(q)
    tot = counts(quats)
    print('counted %d configurations' % sum(1 for t in tot if t), flush=True)

    rows = []
    for q, t in zip(quats, tot):
        if t is None:
            continue
        h4 = w4_count(q, pts)
        rows.append((t, len(h4), sum(1 for a, _ in h4 if a >= 4),
                     w3_count(q, lines), q))
    rows.sort(key=lambda r: -r[0])

    def bucket(rows, key, name):
        by = collections.defaultdict(list)
        for r in rows:
            by[key(r)].append(r[0])
        print('\ncount distribution by %s:' % name)
        print('  %-8s %6s %8s %8s %8s' % (name, 'n', 'mean', 'median', 'max'))
        for k in sorted(by):
            v = by[k]
            print('  %-8s %6d %8.1f %8d %8d'
                  % (k, len(v), statistics.mean(v), statistics.median(v), max(v)))

    bucket(rows, lambda r: r[1], 'W4')
    bucket(rows, lambda r: r[2], 'W4>=4pl')
    bucket(rows, lambda r: min(r[3], 20), 'W3')

    print('\ntop 12 configurations by count:')
    print('  %6s %5s %8s %5s  %s' % ('total', 'W4', 'W4>=4pl', 'W3', 'quat'))
    for t, a, b, c, q in rows[:12]:
        print('  %6d %5d %8d %5d  %s' % (t, a, b, c, ','.join(map(str, q))))
    hi = [r for r in rows if r[0] >= 700]
    lo = [r for r in rows if r[0] < 650]
    if hi and lo:
        print('\ncount >= 700 (n=%d): mean W4 %.2f, mean W3 %.2f'
              % (len(hi), statistics.mean([r[1] for r in hi]),
                 statistics.mean([r[3] for r in hi])))
        print('count <  650 (n=%d): mean W4 %.2f, mean W3 %.2f'
              % (len(lo), statistics.mean([r[1] for r in lo]),
                 statistics.mean([r[3] for r in lo])))


if __name__ == '__main__':
    main()
