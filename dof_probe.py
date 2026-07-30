#!/usr/bin/env python3
# Working principles: record_hunt.py (exact engine).  Question: do LARGE
# k-cube configurations have count-preserving continuous degrees of freedom,
# or only the k=2 (pair) level?
"""Probe for count-preserving one-parameter families.

The project's earlier "DOF openness" statistic perturbs randomly and asks
whether the count survives -- that measures whether a config sits in an OPEN
set, which is false for every wall, and it is why the 13-pair was recorded as
"rigid, near-isolated" until 2026-07-29, when it turned out to hold 13 at
EVERY angle about a body diagonal (Postscript 44).  A wall can be
measure-zero and still be a continuum.

This probe instead sweeps structured one-parameter families: cube i is
composed with a rotation of varying angle about a fixed axis, exactly, via
integer quaternion multiplication.  A count that survives a RUN of
consecutive angles indicates a continuous family; a count that survives only
at the identity indicates rigidity.

POSITIVE CONTROL (must pass, or the negatives are meaningless): the 13-pair
about a body diagonal has to show a full-length run.

INVARIANT: composition is exact integer quaternion arithmetic, gcd-reduced,
and any product exceeding the engine's |component| <= 512 budget is DROPPED,
never rescaled -- a rescaled quaternion is a different rotation.
"""
import math

import record_hunt as R

CAP = 512
AXES = {'face(0,0,1)': (0, 0, 1), 'edge(0,1,1)': (0, 1, 1),
        'body(1,1,1)': (1, 1, 1), 'generic(1,2,3)': (1, 2, 3)}
# a-values give angle 2*atan(b|u|/a): large a = small angle, a=0 = 180 degrees
AVALS = [40, 20, 12, 8, 6, 5, 4, 3, 2, 1, 0]


def qmul(p, q):
    a, b, c, d = p
    e, f, g, h = q
    return (a * e - b * f - c * g - d * h,
            a * f + b * e + c * h - d * g,
            a * g - b * h + c * e + d * f,
            a * h + b * g - c * f + d * e)


def reduce_q(q):
    g = math.gcd(*[abs(c) for c in q])
    return tuple(c // g for c in q) if g > 1 else tuple(q)


def sweep(cfg, i, axis, label, eng):
    """Counts along cube i rotated about `axis`; returns [(angle, count)]."""
    out = []
    for a in AVALS:
        p = reduce_q((a, axis[0], axis[1], axis[2]))
        new = reduce_q(qmul(tuple(cfg[i]), p))
        if max(abs(c) for c in new) > CAP or not any(new):
            continue
        trial = [list(q) for q in cfg]
        trial[i] = list(new)
        ang = 2 * math.degrees(math.atan2(math.hypot(*axis), a))
        out.append((round(ang, 1), eng.count([trial])[0][0]))
    return out


def probe(name, cfg, expect):
    eng = R.Engine(len(cfg), 2)
    base = eng.count([cfg])[0][0]
    print('\n=== %s: n=%d, count=%d (expected %d)'
          % (name, len(cfg), base, expect), flush=True)
    best_run = 0
    for i in range(len(cfg)):
        for label, axis in AXES.items():
            res = sweep(cfg, i, axis, label, eng)
            keep = [ang for ang, c in res if c == base]
            if len(keep) >= 2:
                best_run = max(best_run, len(keep))
                print('  cube %d about %-14s preserves %d at %d/%d angles: %s'
                      % (i, label, base, len(keep), len(res), keep), flush=True)
    print('  --> %s' % ('CONTINUOUS family found (run length %d)' % best_run
                        if best_run >= 3 else
                        'no continuous family detected (longest run %d)'
                        % best_run), flush=True)
    return best_run


CORE183 = [[1, 0, 0, 0], [0, 5, 3, 2], [1, -4, -1, 1], [1, 1, -1, -4]]
REC727 = [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5], [2, 1, 1, 1],
          [1, 1, 1, 1], [7, 14, 1, -5]]
CFG393 = REC727[:5]
TRIPLE63 = [REC727[0], REC727[1], REC727[3]]     # a 63-triple of the record
PAIR13 = [[1, 0, 0, 0], [3, 1, 1, 1]]            # positive control

for name, cfg, exp in [('CONTROL 13-pair', PAIR13, 13),
                       ('63-triple (k=3)', TRIPLE63, 63),
                       ('183 core (k=4)', CORE183, 183),
                       ('393 (k=5)', CFG393, 393),
                       ('727 record (k=6)', REC727, 727)]:
    probe(name, cfg, exp)
