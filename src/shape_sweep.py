#!/usr/bin/env python3
"""Falsify s <= a + b + m - 2 across SHAPES, not just cubes.

The 1 930-pair test behind Postscript 106 was cubes only, and Postscript 107
showed the constant is the facet count F rather than 6 -- so the inequality's
real content is shape-generic and has never been attacked outside cubes.  One
violation kills the target of METHODS path 1 before anyone spends a day proving
it, which is the outcome worth buying with unattended machine time.

Cells are centrally symmetric convex bodies {x : |n.x| <= 1}, given by F/2 facet
normals; `cells.counts` returns (a, b, s, m) exactly by Fourier-Motzkin over Q.
Triples are drawn from cubes, hexagonal and octagonal prisms, and MIXED triples
(the three cells need not be congruent for the inequality to be meaningful --
Step B's decomposition never used congruence).

    python3 shape_sweep.py <seed> [seconds]

Writes shape_sweep_<seed>.json incrementally, so an interrupted run still leaves
data.  Any violation is logged loudly and kept in `violations`.
"""
import json
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, HERE)
from cells import counts, cube_normals, prism_normals, rotate
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 1
BUDGET = float(sys.argv[2]) if len(sys.argv) > 2 else 20000.0
OUT = HERE + '/shape_sweep_%d.json' % SEED

SHAPES = {'cube': (cube_normals(), 6),
          'hex_prism': (prism_normals(3), 8),
          'oct_prism': (prism_normals(4), 10)}


def main():
    rng = random.Random(SEED)
    t0 = time.time()
    res = {'seed': SEED, 'tested': 0, 'violations': [], 'by_shape': {},
           'equalities': 0, 'm_equals_F': 0, 'm_less_F': 0}
    names = list(SHAPES)
    n = 0
    while time.time() - t0 < BUDGET:
        mixed = rng.random() < 0.3
        pick = [rng.choice(names) for _ in range(3)] if mixed else [rng.choice(names)] * 3
        cells3 = []
        for nm in pick:
            N, Fc = SHAPES[nm]
            h = rng.choice([2, 3, 5])
            q = tuple(rng.randint(-h, h) for _ in range(4))
            if not any(q):
                q = (1, 0, 0, 0)
            cells3.append((rotate(N, q), Fc, nm, q))
        (Ni, Fi, ni, qi), (Nj, Fj, nj, qj), (Nk, Fk, nk, qk) = cells3
        try:
            a, b, s, m = counts(Ni, Nj, Nk)
        except Exception as e:
            continue
        n += 1
        res['tested'] = n
        key = '%s|%s|%s' % (ni, nj, nk)
        d = res['by_shape'].setdefault(key, {'n': 0, 'viol': 0, 'eq': 0,
                                             'max_s': 0, 'F_i': Fi})
        d['n'] += 1
        d['max_s'] = max(d['max_s'], s)
        bound = a + b + m - 2
        if s == bound:
            d['eq'] += 1
            res['equalities'] += 1
        if m == Fi:
            res['m_equals_F'] += 1
        else:
            res['m_less_F'] += 1
        if s > bound:
            d['viol'] += 1
            v = {'shapes': pick, 'quats': [list(qi), list(qj), list(qk)],
                 'a': a, 'b': b, 'm': m, 's': s, 'bound': bound, 'F_i': Fi}
            res['violations'].append(v)
            print('*** VIOLATION *** %r' % v, flush=True)
        if n % 10 == 0:
            res['elapsed_s'] = round(time.time() - t0, 1)
            json.dump(res, open(OUT, 'w'), indent=1)
            print('[%6.0fs] %d tested, %d violations, %d equalities, m=F in %d'
                  % (time.time() - t0, n, len(res['violations']),
                     res['equalities'], res['m_equals_F']), flush=True)
    res['elapsed_s'] = round(time.time() - t0, 1)
    json.dump(res, open(OUT, 'w'), indent=1)
    print('done: %d tested, %d violations' % (n, len(res['violations'])), flush=True)


if __name__ == '__main__':
    main()
