#!/usr/bin/env python3
"""The shadow relation over EVERY irrational 727, not a sample of sixteen.

`shadow_relation.py` tested 16 of the 183 (two per field) and found 14 with
their per-label type identical at the irrational point and at both rational
neighbours.  That is a sample, and the conclusion drawn from it -- "they are
part of continua" -- deserves the whole set before it is stated as a property
of anything.

Reported separately, because they are different claims with different scopes:

  1. STRUCTURAL, and checkable for all 183: does the configuration lie on a
     RATIONAL line?  It does iff exactly two of its active conditions are
     edge-edge planes (which are rational), the third being the quadric whose
     root is irrational.  If this holds for all 183 then every one of them has
     rational neighbours by construction, independently of any sampling.

  2. EMPIRICAL, per configuration: is the per-label type the SAME at the
     irrational point and at its two nearest rational neighbours?

INVARIANT: the line must contain the point exactly in Z[sqrt d] (gate), and
neighbours are taken at the finest denominator whose quaternion fits the
engine's cap -- a coarse step samples a different chamber and answers a
different question.
"""
import collections
import json
import math
import pickle
import subprocess
from fractions import Fraction as F

import sympy
import sys

DENS = ([int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1
        else [99991, 9973, 991, 97])

from shadow_relation import (FIXED_N, FIXED_Q2, line_of, make_field, to_quat)


def catalogue():
    planes = pickle.load(open('locus_planes.pkl', 'rb'))
    plist = [p for k in sorted(planes) for p in planes[k]]
    raw = pickle.load(open('corner_conds.pkl', 'rb'))
    syms = set()
    for k in raw:
        for e in raw[k]:
            syms |= e.free_symbols
    sa, sb, sc = sorted(syms, key=str)
    quads = []
    for k in sorted(raw):
        for e in raw[k]:
            p = sympy.Poly(e, sa, sb, sc)
            quads.append({tuple(m): int(v) for m, v in
                          zip(p.monoms(), p.coeffs())})
    return plist, quads


def batch_rational(quats):
    inp = '\n'.join(FIXED_N + ';' + ','.join(map(str, q)) for q in quats) + '\n'
    out = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                         capture_output=True, text=True).stdout
    res = []
    for l in out.splitlines():
        if l.startswith('{'):
            d = json.loads(l)
            res.append((d.get('bounded'),
                        tuple(sorted((int(k), v) for k, v in
                                     d.get('per_label', {}).items()))))
    return res


def batch_algebraic(D, quats):
    lines = [FIXED_Q2 + ';' + ','.join('%d:%d' % tuple(c) for c in q)
             for q in quats]
    out = subprocess.run(['./cube_regions_q2', '--d', str(D), '--quats-stdin'],
                         input='\n'.join(lines) + '\n',
                         capture_output=True, text=True).stdout
    res = []
    for l in out.splitlines():
        if l.startswith('{'):
            d = json.loads(l)
            res.append((d.get('bounded'),
                        tuple(sorted((int(k), v) for k, v in
                                     d.get('per_label', {}).items()))))
    return res


def main():
    plist, quads = catalogue()
    hits = [r for r in (json.loads(l) for l in open('mixed_q2_hits.jsonl'))
            if r['total'] == 727]
    byd = collections.defaultdict(set)
    for r in hits:
        byd[r['d']].add(tuple(tuple(c) for c in r['quat']))

    split = collections.Counter()
    verdicts = collections.Counter()
    total = 0
    for D in sorted(byd):
        Q = make_field(D)
        cfgs = sorted(byd[D])
        alg = batch_algebraic(D, cfgs)
        pending = []
        for quat, (tot, irr_type) in zip(cfgs, alg):
            total += 1
            w, x, y, z = [Q(p, q) for p, q in quat]
            if w.zero():
                split['w = 0 (chart edge)'] += 1
                continue
            a, b, c = x/w, y/w, z/w
            act_p = [i for i, (A, B, C, Dd) in enumerate(plist)
                     if (A*a + B*b + C*c + Dd).zero()]
            nq = 0
            for m in quads:
                s = Q(0)
                for (i, j, l), v in m.items():
                    t = Q(1)
                    for _ in range(i): t = t*a
                    for _ in range(j): t = t*b
                    for _ in range(l): t = t*c
                    s = s + v*t
                if s.zero():
                    nq += 1
            split['%d planes + %d quadrics' % (len(act_p), nq)] += 1
            if len(act_p) != 2:
                continue
            L = line_of(plist[act_p[0]], plist[act_p[1]])
            if L is None:
                split['degenerate line'] += 1
                continue
            p0, dd = L
            k = next(i for i in range(3) if dd[i] != 0)
            tstar = (([a, b, c][k]) - Q(p0[k])) / Q(dd[k])
            if not all((Q(p0[u]) + tstar*Q(dd[u]) - [a, b, c][u]).zero()
                       for u in range(3)):
                split['GATE FAILED'] += 1
                continue
            tv = tstar.val()
            nb = []
            # the rational engine accepts components up to ~1e8, so the
            # neighbour step can go far finer than 1e-5 -- which matters,
            # because a 727 stretch narrower than the step reads as "no
            # continuum" when it is only unresolved
            for den in DENS:
                cand = []
                for r in (F(math.floor(tv*den) - 1, den),
                          F(math.ceil(tv*den) + 1, den)):
                    pt = tuple(F(p0[u]) + r*F(dd[u]) for u in range(3))
                    qq = to_quat(pt)
                    cand.append(qq)
                if all(cand):
                    nb = cand
                    break
            if not nb:
                split['no usable neighbour'] += 1
                continue
            pending.append((irr_type, nb))
        if pending:
            flat = [q for _, nb in pending for q in nb]
            res = batch_rational(flat)
            for idx, (irr_type, nb) in enumerate(pending):
                l = res[2*idx]
                r = res[2*idx+1]
                def v(x):
                    if x[0] != 727:
                        return 'not 727 (%s)' % x[0]
                    return 'same type' if x[1] == irr_type else '727, other type'
                verdicts[(v(l), v(r))] += 1

    print('irrational 727 configurations: %d' % total)
    print('\nactive-condition split (structural -- decides whether the point'
          ' lies on a RATIONAL line):')
    for k in sorted(split, key=str):
        print('   %-28s %d' % (k, split[k]))
    print('\nper-label type at the point vs at its two nearest rational'
          ' neighbours:')
    for k in sorted(verdicts, key=str):
        print('   %-42s %d' % (str(k), verdicts[k]))
    same_both = verdicts[('same type', 'same type')]
    tested = sum(verdicts.values())
    print('\nsame type on BOTH sides: %d of %d tested' % (same_both, tested))


if __name__ == '__main__':
    main()
