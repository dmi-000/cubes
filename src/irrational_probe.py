#!/usr/bin/env python3
# Working principles: locus_enum.py (same systems); this measures the gap that
# enumeration deliberately leaves open.
"""How many real solution points of the three-wall systems are IRRATIONAL?

locus_enum.py keeps only rational roots, because those are what the fast C++
engine counts.  The 500-trial census (Postscript 48) returned no irrational
real points at all, which suggests the gap is thin -- but a sample is not a
proof, and the cost of closing it depends entirely on how many there are.

This pass keeps EVERY real root (exact CRootOf: minimal polynomial plus
isolating interval) and classifies by the degree of that minimal polynomial.
Degree 1 is the rational case the enumeration already covers; degree >= 2 is
the gap, and its size decides whether closing it is trivial (count them with
opencount.py at ~20 s each) or a project in itself.

Nothing is counted here -- this measures the SIZE and DEGREE of the gap only.

INVARIANT: roots are exact algebraic numbers throughout; a root is classified
rational only when sympy proves it so, never by float inspection.
"""
import collections
import itertools
import json
import pickle
import random
import sys
import time

import sympy as sp

a, b, c = sp.symbols('a b c', real=True)
per = pickle.load(open('locus_polys.pkl', 'rb'))
rng = random.Random(20260731)
TRIALS = int(sys.argv[1]) if len(sys.argv) > 1 else 400

deg_hist = collections.Counter()
kind = collections.Counter()
t0 = time.time()

for trial in range(TRIALS):
    js = rng.sample(range(5), 3)
    S = [rng.choice(per[j])[0] for j in js]
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
    P = sp.Poly(uni[0], c)
    try:
        roots = P.real_roots()          # exact, includes irrational ones
    except Exception:
        kind['real_roots-failed'] += 1
        continue
    kind['systems-with-real-roots'] += 1
    for r in roots:
        if r.is_rational:
            deg_hist[1] += 1
            continue
        try:
            mp = sp.minimal_polynomial(r, sp.Symbol('t'))
            deg_hist[sp.degree(mp, sp.Symbol('t'))] += 1
        except Exception:
            deg_hist['unknown'] += 1

el = time.time() - t0
tot = sum(v for k, v in deg_hist.items() if isinstance(k, int))
irr = sum(v for k, v in deg_hist.items() if isinstance(k, int) and k > 1)
print('%d systems in %.0fs' % (TRIALS, el))
print('system kinds:', dict(kind))
print('root degree histogram (in the eliminated variable c):',
      dict(sorted((k, v) for k, v in deg_hist.items() if isinstance(k, int))))
print('\nreal roots: %d total, %d rational, %d IRRATIONAL (%.1f%%)'
      % (tot, deg_hist.get(1, 0), irr, 100.0 * irr / tot if tot else 0.0))
json.dump({'kinds': dict(kind),
           'degrees': {str(k): v for k, v in deg_hist.items()},
           'trials': TRIALS},
          open('irrational_probe.json', 'w'), indent=1)
