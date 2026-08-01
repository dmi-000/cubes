#!/usr/bin/env python3
# Working principles: locus_probe.py / locus_linear.py.  This covers the
# stratum type those miss: corner-on-face-plane incidences.
"""Corner-wall strata on the 393 base: are they rich, and are they irrational?

The edge-edge coplanarity conditions factor into pairs of rational PLANES, so
their strata are all rational -- an artifact of that condition type, not a
fact about the problem (Postscript 49).  Corner-on-face-plane conditions are
IRREDUCIBLE QUADRICS, so three of them meet in up to 8 points that may be
genuinely irrational.  This is the stratum type records are associated with:
Postscript 12 found records at high-multiplicity corner concurrences, and 723
is corner-dominated (48 interior crossings against 727's 18).

Two condition families, both one equation (codimension 1, hence walls):
  TYPE A  a corner of the free cube lies on a face plane of a fixed cube:
          col_k(R_j) . (R_6 s) = +-1        8 corners x 3 normals x 2 signs
  TYPE B  a corner of a fixed cube lies on a face plane of the free cube:
          col_k(R_6) . (R_j t) = +-1        likewise

This samples triples (one condition against each of three distinct fixed
cubes) and reports: the count distribution, and the rational/irrational split
of the solution points.  It decides whether a full enumeration is worth its
cost -- which is real here, since linear algebra does not apply and irrational
points need the ~20 s algebraic counters.

INVARIANT: irrational points are classified by the exact degree of their
minimal polynomial and NEVER counted numerically; only rational points within
the height cap go to the integer engine.
"""
import collections
import itertools
import json
import os
import pickle
import random
import sys
import time

import sympy as sp

import record_hunt as R

a, b, c = sp.symbols('a b c', real=True)
FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1),
        (1, 1, 1, 1)]
CACHE = 'corner_conds.pkl'
CAP = 512


def rot(q):
    w, x, y, z = q
    n = w * w + x * x + y * y + z * z
    return sp.Matrix([[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
                      [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                      [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]]) / n


def build():
    M6 = rot((1, a, b, c))
    corners6 = [M6 * sp.Matrix(s) for s in itertools.product((1, -1), repeat=3)]
    per = {}
    for j, q in enumerate(FIVE):
        t0 = time.time()
        Rj = rot(q)
        cj = [Rj * sp.Matrix(t) for t in itertools.product((1, -1), repeat=3)]
        conds = set()
        for k in range(3):
            for sign in (1, -1):
                for cor in corners6:                       # TYPE A
                    e = (Rj[:, k].T * cor)[0, 0] - sign
                    P = sp.expand(sp.together(sp.simplify(e)).as_numer_denom()[0])
                    if P != 0:
                        conds.add(sp.factor(P))
                for v in cj:                               # TYPE B
                    e = (M6[:, k].T * v)[0, 0] - sign
                    P = sp.expand(sp.together(sp.simplify(e)).as_numer_denom()[0])
                    if P != 0:
                        conds.add(sp.factor(P))
        per[j] = sorted(conds, key=sp.default_sort_key)
        print('  cube %d: %d distinct corner conditions (%.0fs)'
              % (j, len(per[j]), time.time() - t0), flush=True)
    return per


if os.path.exists(CACHE):
    per = pickle.load(open(CACHE, 'rb'))
    print('loaded cached corner conditions', flush=True)
else:
    print('building corner conditions', flush=True)
    per = build()
    pickle.dump(per, open(CACHE, 'wb'))

TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 200
rng = random.Random(20260731)
eng = R.Engine(6, 2)
kind = collections.Counter()
degs = collections.Counter()
counts = collections.Counter()
best = (0, None)
t0 = time.time()

for trial in range(TRIALS):
    js = rng.sample(range(5), 3)
    S = [sp.expand(rng.choice(per[j])) for j in js]
    try:
        G = sp.groebner(S, a, b, c, order='lex')
    except Exception:
        kind['groebner-failed'] += 1
        continue
    gs = list(G.exprs)
    if gs == [sp.Integer(1)]:
        kind['inconsistent'] += 1
        continue
    uni = [g for g in gs if g.free_symbols <= {c} and g.free_symbols]
    if not uni:
        kind['positive-dimensional'] += 1
        continue
    kind['solved'] += 1
    P = sp.Poly(uni[0], c)
    try:
        roots = P.real_roots()
    except Exception:
        kind['real_roots-failed'] += 1
        continue
    for r in roots:
        if not r.is_rational:
            try:
                mp = sp.minimal_polynomial(r, sp.Symbol('t'))
                degs[sp.degree(mp, sp.Symbol('t'))] += 1
            except Exception:
                degs['unknown'] += 1
            continue
        degs[1] += 1
        # rational root: back-substitute for b then a, count if fully rational
        bs = [sp.Poly(g.subs(c, r), b) for g in gs
              if g.free_symbols <= {b, c} and b in g.free_symbols
              and g.subs(c, r) != 0]
        if not bs:
            continue
        for b0 in bs[0].ground_roots():
            as_ = [sp.Poly(g.subs({c: r, b: b0}), a) for g in gs
                   if a in g.free_symbols and g.subs({c: r, b: b0}) != 0]
            if not as_:
                continue
            for a0 in as_[0].ground_roots():
                den = sp.ilcm(sp.Rational(a0).q, sp.Rational(b0).q,
                              sp.Rational(r).q)
                qt = (int(den), int(a0 * den), int(b0 * den), int(r * den))
                if not any(qt) or max(abs(x) for x in qt) > CAP:
                    kind['rational-but-too-big'] += 1
                    continue
                tot = eng.count([[list(x) for x in FIVE] + [list(qt)]])[0][0]
                counts[tot] += 1
                if tot > best[0]:
                    best = (tot, qt)
                if tot >= 723:
                    print('  *** total %d  sixth=%s' % (tot, qt), flush=True)

print('\n%d trials in %.0fs' % (TRIALS, time.time() - t0))
print('system kinds:', dict(kind))
print('root degrees:', dict(sorted((k, v) for k, v in degs.items()
                                   if isinstance(k, int))))
tot_r = sum(v for k, v in degs.items() if isinstance(k, int))
irr = sum(v for k, v in degs.items() if isinstance(k, int) and k > 1)
print('real roots: %d, of which IRRATIONAL: %d (%.1f%%)'
      % (tot_r, irr, 100.0 * irr / tot_r if tot_r else 0))
print('count distribution (rational points only):',
      {k: counts[k] for k in sorted(counts)[-12:]})
print('best:', best)
json.dump({'kinds': dict(kind), 'degrees': {str(k): v for k, v in degs.items()},
           'counts': {str(k): v for k, v in counts.items()},
           'best': [best[0], list(best[1]) if best[1] else None]},
          open('corner_probe.json', 'w'), indent=1)
