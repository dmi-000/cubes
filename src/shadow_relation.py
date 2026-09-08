#!/usr/bin/env python3
"""What exactly is an irrational configuration's relationship to its shadow?

Postscript 60: every irrational 727 sits at k = 4 active walls -- two rational
edge-edge planes (which cut a RATIONAL line in Cayley space) plus one
corner-on-face condition (a quadric, counted twice as a +- pair). So the
picture ought to be:

    the irrational configuration is a point of a RATIONAL one-parameter
    family, at the parameter value where one extra coincidence snaps into
    place -- and that value is irrational.

Its "rational shadows" would then be nothing exotic: they are its own
NEIGHBOURS along that same line, sharing its two edge-edge coincidences and
differing only in where they sit along it.

This checks that picture and then asks the question it raises.  If the
irrational point is a chamber boundary, is its combinatorial type
  (a) equal to a neighbour's -- the extra coincidence changes nothing, and the
      point is combinatorially a member of a rational continuum; or
  (b) different from BOTH neighbours -- a genuine zero-width type, attained at
      that algebraic point and nowhere near it?

GATE: the recovered line must pass through the irrational point EXACTLY, in
Z[sqrt d].  Without that check the sampled neighbours could belong to some
other line entirely and every comparison below would be meaningless.
"""
import collections
import json
import math
import pickle
import subprocess
import sys
from fractions import Fraction as F

import sympy

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
FIXED_N = ';'.join(','.join(map(str, q)) for q in FIVE)
FIXED_Q2 = ';'.join(','.join('%d:0' % x for x in q) for q in FIVE)


def make_field(D):
    class Q:
        __slots__ = ('p', 'q')
        def __init__(s, p, q=0): s.p = F(p); s.q = F(q)
        def __add__(s, o): o = cv(o); return Q(s.p+o.p, s.q+o.q)
        __radd__ = __add__
        def __sub__(s, o): o = cv(o); return Q(s.p-o.p, s.q-o.q)
        def __rsub__(s, o): return cv(o).__sub__(s)
        def __mul__(s, o):
            o = cv(o); return Q(s.p*o.p + D*s.q*o.q, s.p*o.q + s.q*o.p)
        __rmul__ = __mul__
        def __truediv__(s, o):
            o = cv(o); n = o.p*o.p - D*o.q*o.q
            return Q((s.p*o.p - D*s.q*o.q)/n, (s.q*o.p - s.p*o.q)/n)
        def zero(s): return s.p == 0 and s.q == 0
        def val(s): return float(s.p) + float(s.q)*math.sqrt(D)
        def __repr__(s):
            return '%s%+s√%d' % (s.p, s.q, D) if s.q else str(s.p)
    def cv(o): return o if isinstance(o, Q) else Q(o)
    return Q


def line_of(p, q):
    n1, n2 = p[:3], q[:3]
    d = (n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2],
         n1[0]*n2[1]-n1[1]*n2[0])
    if not any(d):
        return None
    k = max(range(3), key=lambda i: abs(d[i]))
    i, j = [t for t in range(3) if t != k]
    det = n1[i]*n2[j] - n1[j]*n2[i]
    if det == 0:
        return None
    pt = [F(0)]*3
    pt[i] = F(-p[3]*n2[j] + q[3]*n1[j], det)
    pt[j] = F(-n1[i]*q[3] + n2[i]*p[3], det)
    return tuple(pt), tuple(F(x) for x in d)


def to_quat(pt, cap=60000000):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0]*den), int(pt[1]*den), int(pt[2]*den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x//g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= cap else None


def rational_types(quats):
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


def algebraic_type(D, quat):
    line = FIXED_Q2 + ';' + ','.join('%d:%d' % tuple(c) for c in quat)
    out = subprocess.run(['./cube_regions_q2', '--d', str(D), '--quats-stdin'],
                         input=line + '\n', capture_output=True,
                         text=True).stdout
    for l in out.splitlines():
        if l.startswith('{'):
            d = json.loads(l)
            return (d.get('bounded'),
                    tuple(sorted((int(k), v) for k, v in
                                 d.get('per_label', {}).items())))
    return (None, None)


def main():
    planes = pickle.load(open('locus_planes.pkl', 'rb'))
    plist = [p for k in sorted(planes) for p in planes[k]]

    hits = [r for r in (json.loads(l) for l in open('mixed_q2_hits.jsonl'))
            if r['total'] == 727]
    byd = collections.defaultdict(set)
    for r in hits:
        byd[r['d']].add(tuple(tuple(c) for c in r['quat']))

    print('%-9s %-28s %8s %10s %10s' %
          ('field', 't* (irrational parameter)', 'gate', 'left', 'right'))
    tally = collections.Counter()
    for D in sorted(byd):
        Q = make_field(D)
        for quat in sorted(byd[D])[:2]:
            w, x, y, z = [Q(p, q) for p, q in quat]
            if w.zero():
                continue
            a, b, c = x/w, y/w, z/w
            act = [i for i, (A, B, C, Dd) in enumerate(plist)
                   if (A*a + B*b + C*c + Dd).zero()]
            if len(act) != 2:
                tally['not a 2-plane line'] += 1
                continue
            L = line_of(plist[act[0]], plist[act[1]])
            if L is None:
                tally['degenerate line'] += 1
                continue
            p0, dd = L
            k = next(i for i in range(3) if dd[i] != 0)
            tstar = (([a, b, c][k]) - Q(p0[k])) / Q(dd[k])
            # GATE: the line must pass through the point exactly
            ok = all((Q(p0[u]) + tstar*Q(dd[u]) - [a, b, c][u]).zero()
                     for u in range(3))
            if not ok:
                tally['GATE FAILED'] += 1
                print('  d=%d GATE FAILED -- line does not contain the point' % D)
                continue
            tally['gate ok'] += 1
            _, irr_type = algebraic_type(D, quat)

            tv = tstar.val()
            left = right = None
            # finest step FIRST: we want the NEAREST rational neighbours,
            # falling back to a coarser grid only when the finer one produces
            # components above the engine's cap.  Taking the coarsest that
            # works samples a point that may be several chambers away, which
            # answers a different question.
            for den in (99991, 9973, 991, 97):
                lo = F(math.floor(tv*den) - 1, den)
                hi = F(math.ceil(tv*den) + 1, den)
                for r, side in ((lo, 'L'), (hi, 'R')):
                    pt = tuple(F(p0[u]) + r*F(dd[u]) for u in range(3))
                    qq = to_quat(pt)
                    if qq is None:
                        continue
                    tot, typ = rational_types([qq])[0]
                    if side == 'L' and left is None:
                        left = (r, tot, typ)
                    if side == 'R' and right is None:
                        right = (r, tot, typ)
                if left and right:
                    break

            def verdict(nb):
                if nb is None:
                    return 'n/a'
                if nb[1] != 727:
                    return '%d' % nb[1]
                return 'SAME type' if nb[2] == irr_type else '727 diff type'
            print('%-9s %-28s %8s %10s %10s'
                  % ('Q(√%d)' % D, '%s%+s\u221a%d' % (tstar.p, tstar.q, D), 'ok',
                     verdict(left), verdict(right)), flush=True)
            key = (verdict(left), verdict(right))
            tally[key] += 1
    print('\nsummary:', dict(tally))


if __name__ == '__main__':
    main()
