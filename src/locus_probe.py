#!/usr/bin/env python3
# Working principles: eliminate729.py (same Cayley parameterisation and exact
# conditions).  Question: are the pair-relation loci codimension 1, and what
# do their triple intersections count?
"""Pair-relation loci on the 393 base, and the payoff of enumerating them.

Postscript 47 left the structural route: 727 is the intersection of three
9-pair loci (with fixed cubes 0, 1, 3).  Two facts decide whether enumerating
those loci is worth doing.

  A. CODIMENSION.  If a 9-locus is codim 1 (a surface), then three of them in
     the sixth cube's 3-DOF space meet in finitely many points -- perfectly
     determined, and 727 is one.  If it is codim 2 (a curve), three curves is
     codim 6 and the intersection is a coincidence needing explanation.
     Evidence for codim 1: perturbing a 13-pair off its locus drops it to 9,
     not to the generic 4, so 9 is the wall and 13 sits deeper.

  B. PAYOFF.  Sample triples of walls (one from each of three fixed cubes),
     solve the 3-quadric system exactly, and look at the real points: what
     pair profile and what region count do they carry?  If they cluster near
     727, systematic enumeration is worth its cost; if they are generic, the
     three-9-pair family is barren away from the known point.

Polynomials are cached to locus_polys.pkl -- rebuilding them costs ~45 s per
fixed cube and every later run needs the same 720.

INVARIANT: exact throughout.  A solution point is only counted when it is
rational (then cube_regions_n applies, after clearing denominators);
irrational points are reported with their degree, never counted numerically.
"""
import itertools
import os
import pickle
import random
import sys
import time
from fractions import Fraction as F

import sympy as sp

a, b, c = sp.symbols('a b c', real=True)
FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1),
        (1, 1, 1, 1)]
KNOWN = (7, 14, 1, -5)
CACHE = 'locus_polys.pkl'


def rot_sym(q):
    w, x, y, z = q
    n = w * w + x * x + y * y + z * z
    return sp.Matrix([
        [w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]
    ]) / n


def edge_list(M):
    out = []
    for ax in range(3):
        o1, o2 = [t for t in range(3) if t != ax]
        for s in (-1, 1):
            for t in (-1, 1):
                out.append((s * M[:, o1] + t * M[:, o2], M[:, ax]))
    return out


def build():
    M6 = rot_sym((1, a, b, c))
    e6 = edge_list(M6)
    per = {}
    for j, q in enumerate(FIVE):
        t0 = time.time()
        ef = edge_list(rot_sym(q))
        ps = []
        for (i1, x1), (i2, x2) in itertools.product(enumerate(e6), enumerate(ef)):
            d = sp.Matrix.hstack(x1[1], x2[1], x2[0] - x1[0]).det()
            P = sp.expand(sp.together(sp.simplify(d)).as_numer_denom()[0])
            if P != 0:
                ps.append((P, (i1, i2)))
        per[j] = ps
        print('  cube %d: %d conditions (%.0fs)' % (j, len(ps), time.time() - t0),
              flush=True)
    return per


if os.path.exists(CACHE):
    per = pickle.load(open(CACHE, 'rb'))
    print('loaded cached conditions', flush=True)
else:
    print('building conditions (cached afterwards)', flush=True)
    per = build()
    pickle.dump(per, open(CACHE, 'wb'))

subs = {a: sp.Rational(KNOWN[1], KNOWN[0]), b: sp.Rational(KNOWN[2], KNOWN[0]),
        c: sp.Rational(KNOWN[3], KNOWN[0])}

# ---- A: codimension of one cube's active set at the known point
print('\nA. codimension of the 9-locus', flush=True)
for j in (0, 1, 3):
    act = [P for P, _ in per[j] if sp.simplify(P.subs(subs)) == 0]
    G = sp.groebner(act, a, b, c, order='grevlex')
    print('  cube %d: %d active conditions, zero-dimensional=%s, |G|=%d'
          % (j, len(act), G.is_zero_dimensional, len(G.exprs)), flush=True)

# ---- B: payoff of sampled triple-wall intersections
print('\nB. sampled triple-wall intersections', flush=True)
rng = random.Random(4747)
seen_counts = {}
trials = int(sys.argv[1]) if len(sys.argv) > 1 else 60
for trial in range(trials):
    js = rng.sample(range(5), 3)
    sysp = [rng.choice(per[j])[0] for j in js]
    try:
        sol = sp.solve(sysp, [a, b, c], dict=True)
    except Exception as e:
        continue
    for s in sol:
        # solve() returns a partial dict when the system is dependent and the
        # solution set is positive-dimensional (a curve or surface of sixth
        # cubes sharing these three coincidences).  Those are worth counting
        # as their own category -- they are continuous families, not points.
        if not all(v in s for v in (a, b, c)):
            seen_counts['positive-dimensional'] = \
                seen_counts.get('positive-dimensional', 0) + 1
            continue
        if not all(v.is_real for v in s.values()):
            continue
        vals = [s[a], s[b], s[c]]
        if all(v.is_rational for v in vals):
            den = sp.ilcm(*[sp.Rational(v).q for v in vals])
            q = (int(den), int(vals[0] * den), int(vals[1] * den),
                 int(vals[2] * den))
            if max(abs(x) for x in q) > 512 or not any(q):
                seen_counts.setdefault('rational-but-too-big', 0)
                seen_counts['rational-but-too-big'] += 1
                continue
            import record_hunt as R
            cfg = [list(x) for x in FIVE] + [list(q)]
            tot = R.Engine(6, 2).count([cfg])[0][0]
            seen_counts[tot] = seen_counts.get(tot, 0) + 1
            if tot >= 723:
                print('  *** cubes %s -> total %d  q=%s' % (js, tot, q),
                      flush=True)
        else:
            deg = max(sp.degree(sp.minimal_polynomial(v, sp.Symbol('t')),
                                sp.Symbol('t')) for v in vals)
            k = 'algebraic-deg-%d' % deg
            seen_counts[k] = seen_counts.get(k, 0) + 1
print('\nsolution-point census over %d sampled wall triples:' % trials,
      flush=True)
for k in sorted(seen_counts, key=lambda x: str(x)):
    print('   %-24s %d' % (k, seen_counts[k]), flush=True)
