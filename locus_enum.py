#!/usr/bin/env python3
# Working principles: locus_probe.py (cached conditions, same parameterisation).
"""Exhaustive enumeration of three-wall strata on the 393 base.

Each coincidence condition is a quadric in the sixth cube's Cayley coordinates
(a,b,c), and a 9-pair locus is codimension 1 (Postscript 47 + locus_probe).
So picking one wall against each of three fixed cubes gives a DETERMINED
system -- three quadrics, at most 2^3 = 8 points by Bezout -- and both 723 and
727 arise this way.  Enumerating those systems is therefore an exhaustive
search of the three-wall family, not a sample of it.

Counts:  C(5,3) = 10 triples of fixed cubes x 144^3 wall choices = 3.0e7,
reduced by 12 because the cube's rotation group is transitive on the sixth
cube's 12 edges, so the FIRST wall's sixth-cube edge index can be fixed to a
representative: 2.5e6 systems, ~0.018 s each.

Method per system: lex Groebner -> triangular basis -> rational roots only
(ground_roots, exact) -> back-substitute -> clear denominators -> integer
quaternion.  Rational points are what the C++ engine counts directly; the
sampled census showed the interesting points ARE rational and small, and
irrational ones would need the ~20 s algebraic path anyway.

INVARIANT: candidates are deduplicated by their orbit under the cube's own 24
rotations before counting -- the same compound reached through different wall
triples must not be counted, or recounted, twice (the clique run's clone bug).

Usage: locus_enum.py SHARD NSHARDS [MAXHOURS]
"""
import itertools
import json
import math
import os
import pickle
import sys
import time

import sympy as sp

import record_hunt as R

a, b, c = sp.symbols('a b c', real=True)
FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1),
        (1, 1, 1, 1)]
REPORT_AT = 723
CAP = 512

SHARD = int(sys.argv[1]) if len(sys.argv) > 1 else 0
NSHARDS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
MAXH = float(sys.argv[3]) if len(sys.argv) > 3 else 9.0
# Optional 4th arg: comma-separated indices into the C(5,3) triple list, so a
# resumed run need not redo triples an earlier run already covered.  Indices:
#   0:(0,1,2) 1:(0,1,3) 2:(0,1,4) 3:(0,2,3) 4:(0,2,4)
#   5:(0,3,4) 6:(1,2,3) 7:(1,2,4) 8:(1,3,4) 9:(2,3,4)
ONLY = ({int(x) for x in sys.argv[4].split(',')} if len(sys.argv) > 4 else None)

per = pickle.load(open('locus_polys.pkl', 'rb'))
eng = R.Engine(6, 1)
OUT = open('locus_enum_%d.jsonl' % SHARD, 'a')


def qmul(p, q):
    w, x, y, z = p
    e, f, g, h = q
    return (w * e - x * f - y * g - z * h, w * f + x * e + y * h - z * g,
            w * g - x * h + y * e + z * f, w * h + x * g - y * f + z * e)


SYMS = list(dict.fromkeys(
    R.canon([t])[0] for t in
    [(w, x, y, z) for w in (-1, 0, 1) for x in (-1, 0, 1) for y in (-1, 0, 1)
     for z in (-1, 0, 1)
     if (w, x, y, z) != (0, 0, 0, 0) and w * w + x * x + y * y + z * z in (1, 2, 4)]))


def sym_key(q):
    return min(R.canon([qmul(tuple(q), h)])[0] for h in SYMS)


def rational_points(G):
    """All fully-rational solutions of a lex Groebner basis in (a,b,c)."""
    gs = list(G.exprs)
    if gs == [sp.Integer(1)]:
        return []
    uni = [g for g in gs if g.free_symbols <= {c} and g.free_symbols]
    if not uni:
        return []                                   # positive-dimensional
    out = []
    for c0 in sp.Poly(uni[0], c).ground_roots():
        bs = [sp.Poly(g.subs(c, c0), b) for g in gs
              if g.free_symbols <= {b, c} and b in g.free_symbols
              and g.subs(c, c0) != 0]
        if not bs:
            continue
        for b0 in bs[0].ground_roots():
            as_ = [sp.Poly(g.subs({c: c0, b: b0}), a) for g in gs
                   if a in g.free_symbols and g.subs({c: c0, b: b0}) != 0]
            if not as_:
                continue
            for a0 in as_[0].ground_roots():
                out.append((a0, b0, c0))
    return out


def to_quat(pt):
    a0, b0, c0 = [sp.Rational(v) for v in pt]
    den = sp.ilcm(a0.q, b0.q, c0.q)
    q = (int(den), int(a0 * den), int(b0 * den), int(c0 * den))
    g = math.gcd(*[abs(x) for x in q])
    q = tuple(x // g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= CAP else None


def main():
    t0 = time.time()
    triples = list(itertools.combinations(range(5), 3))
    seen, pending, best = set(), [], (0, None)
    nsys = nhit = 0

    def flush():
        nonlocal pending, best
        if not pending:
            return
        res = eng.count([[list(x) for x in FIVE] + [list(q)] for q in pending])
        for q, (tot, bd) in zip(pending, res):
            if tot > best[0]:
                best = (tot, q)
            if tot >= REPORT_AT:
                print('  total %d  sixth=%s' % (tot, q), flush=True)
                OUT.write(json.dumps({'total': tot, 'sixth': q,
                                      'by_depth': bd}) + '\n')
                OUT.flush()
        pending = []

    for ti, tri in enumerate(triples):
        if ONLY is not None and ti not in ONLY:
            continue
        j0, j1, j2 = tri
        # symmetry: fix the first wall's sixth-cube edge index to 0
        w0 = [P for P, tag in per[j0] if tag[0] == 0]
        for i0, P0 in enumerate(w0):
            if (ti * len(w0) + i0) % NSHARDS != SHARD:
                continue
            for P1, _ in per[j1]:
                for P2, _ in per[j2]:
                    nsys += 1
                    try:
                        G = sp.groebner([P0, P1, P2], a, b, c, order='lex')
                        pts = rational_points(G)
                    except Exception:
                        continue
                    for pt in pts:
                        q = to_quat(pt)
                        if q is None:
                            continue
                        k = sym_key(q)
                        if k in seen:
                            continue
                        seen.add(k)
                        pending.append(q)
                        nhit += 1
                        if len(pending) >= 400:
                            flush()
            flush()
            el = (time.time() - t0) / 3600
            print('[shard %d] triple %s wall %d/%d | %d systems, %d distinct '
                  'candidates, best %s | %.2f h'
                  % (SHARD, tri, i0 + 1, len(w0), nsys, len(seen), best, el),
                  flush=True)
            if el > MAXH:
                print('[shard %d] time budget reached' % SHARD, flush=True)
                flush()
                return
    flush()
    print('[shard %d] DONE %d systems, %d distinct, best %s'
          % (SHARD, nsys, len(seen), best), flush=True)


if __name__ == '__main__':
    main()
