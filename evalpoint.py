#!/usr/bin/env python3
"""The adapter from ARRANGEMENT COORDINATES to a cube configuration — gated.

This is the component that was never gated and produced tens of thousands of wrong
region counts (FAILURE_MODES 21, P163 retracted). Two defects, both here:

  1. The arrangement lives in DISPLACEMENT coordinates. `walls_of` takes gradients
     at pt = point_of(config), so a chamber witness y denotes the configuration
     pt + y. Evaluating count_at(y) measures a different family entirely -- its
     origin is the all-identity compound, which counts 13.
  2. The gauge quaternion is D.QZERO[0] (here (4,1,1,-1)), not the identity. The
     broken scripts hardcoded (1,0,0,0).

Both are fixed in ONE place so no caller can reintroduce either, and `gate()` is
called at import: count at y = 0 must equal the record, or nothing runs.

Batching is why this exists rather than calling `dimension.count_at` per point --
one engine process per configuration dominates otherwise. Bypassing count_at is
also how both defects entered (and, separately, how the wide-engine fallback was
lost), so `agrees_with_count_at()` checks this module against it on sample points.
"""
import json, os, subprocess, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dimension as D
from growth727 import walls_of, BASE, qmul

ENG = os.path.join(HERE, 'cube_regions_n')
ENGW = os.path.join(HERE, 'cube_regions_q2w')


def setup(cfg, expected):
    """(walls, ncols, pt, n). Calls walls_of, which sets D.QZERO as a side effect."""
    W, nc = walls_of(cfg)
    q = cfg
    for g in ((1, 0, 0, 0), (2, 1, 0, 0), (3, 1, 1, 0), (5, 1, 2, 1)):
        o = [qmul(g, x) for x in cfg]
        if all(y[0] != 0 for y in o):
            q = o
            break
    pt = [F(x) for x in D.point_of(q)]
    got = D.count_at(list(pt), len(cfg))
    if got != expected:
        raise SystemExit('ADAPTER GATE FAILED: count at the record point is %s, '
                         'expected %s. The point-to-configuration map is wrong; '
                         'refusing to run.' % (got, expected))
    return W, nc, pt, len(cfg)


def line(pt, y, nc):
    """Engine input for the configuration at displacement y from the record."""
    c = [pt[i] + F(y[i]) for i in range(nc)]
    quats = [D.QZERO[0]] + [D.q_of(c[k:k + 3]) for k in range(0, nc, 3)]
    big = max(abs(v) for q in quats for v in q) > 512
    return ';'.join(','.join(map(str, q)) for q in quats), big


def run_batch(lines, wide=False):
    eng = [ENGW, '--d', '0', '--quats-stdin'] if wide else [ENG, '--quats-stdin']
    p = subprocess.run(eng, input='\n'.join(lines) + '\n',
                       capture_output=True, text=True)
    out = []
    for ln in [l for l in p.stdout.splitlines() if l.startswith('{')]:
        try:
            out.append(json.loads(ln)['bounded'])
        except Exception:
            out.append(None)
    return out + [None] * (len(lines) - len(out))


def agrees_with_count_at(pt, nc, n, samples):
    """This module's batch path must match dimension.count_at point for point."""
    bad = 0
    for y in samples:
        ln, big = line(pt, y, nc)
        mine = run_batch([ln], wide=big)[0]
        theirs = D.count_at([pt[i] + F(y[i]) for i in range(nc)], n)
        if mine != theirs:
            bad += 1
            print('   DISAGREE: batch %s vs count_at %s' % (mine, theirs))
    return bad


if __name__ == '__main__':
    import random
    W, nc, pt, n = setup(BASE + [(7, 14, 1, -5)], 727)
    print('adapter gate PASSED: count at record point = 727')
    print('pt[:4] =', [str(x) for x in pt[:4]], '| QZERO =', D.QZERO[0])
    rnd = random.Random(1)
    samples = [[F(rnd.randint(-3, 3), rnd.choice([1, 2, 4, 8])) for _ in range(nc)]
               for _ in range(6)]
    bad = agrees_with_count_at(pt, nc, n, samples)
    print('batch path vs count_at on %d random displacements: %d disagreements -> %s'
          % (len(samples), bad, 'PASS' if bad == 0 else 'FAIL'))
