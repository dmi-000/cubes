#!/usr/bin/env python3
"""Step A toward a constructive max(3): complete the n = 2 13-locus.

L13 = { R in SO(3) : the pair {I, R} cuts 13 regions }, the two-cube maximum.

Postscript 70 described it as four body-diagonal circles plus six edge arcs.
Postscript 76 showed that is INCOMPLETE -- the octahedral 67's pairs are
13-pairs whose axes are neither, lying instead inside mirror planes. Every
13 observed so far, however, has had its axis in one of the cube's nine
mirror planes (3 coordinate + 6 diagonal), and body diagonals and edge axes
are themselves intersections of mirror planes.

CONJECTURE A1:  count = 13  =>  the rotation axis lies in a mirror plane.

If true, L13 is confined to a 2-parameter family (axis within a plane, times
angle) rather than the full 3, which is what makes the later enumeration
finite and checkable. This tests A1 against generic axes, then maps the locus
inside one mirror plane.

INVARIANT: "generic axis" means provably off all nine planes -- checked
exactly in integer arithmetic, not by eyeball. An axis accidentally lying in a
plane would produce a 13 and appear to refute the conjecture.
"""
import collections, json, math, random, subprocess
from fractions import Fraction as F

MIRRORS = [(1,0,0),(0,1,0),(0,0,1),(1,-1,0),(1,1,0),(0,1,-1),(0,1,1),(1,0,-1),(1,0,1)]

def on_mirror(a):
    return any(sum(a[i]*m[i] for i in range(3)) == 0 for m in MIRRORS)

def red(q):
    g = 0
    for x in q: g = math.gcd(g, abs(x))
    return tuple(x//g for x in q) if g > 1 else tuple(q)

def batch(qs):
    out = []
    for i in range(0, len(qs), 2000):
        ch = qs[i:i+2000]
        inp = '\n'.join('1,0,0,0;' + ','.join(map(str,q)) for q in ch) + '\n'
        p = subprocess.run(['./cube_regions_n','--quats-stdin'], input=inp,
                           capture_output=True, text=True)
        r = [json.loads(l).get('bounded') for l in p.stdout.splitlines()
             if l.startswith('{')]
        if len(r) != len(ch): raise SystemExit('truncated: %d/%d'%(len(r),len(ch)))
        out += r
    return out

def fam(axis, ts):
    out = []
    for t in ts:
        num = [F(1)] + [t*F(x) for x in axis]
        den = 1
        for v in num: den = den*v.denominator//math.gcd(den, v.denominator)
        out.append(red(tuple(int(v*den) for v in num)))
    return out

TS = [F(k, 60) for k in range(1, 300)]     # 299 angles per axis

print('=== A1: do axes OFF every mirror plane ever reach 13? ===', flush=True)
rng = random.Random(11)
tested = worst = 0
best = collections.Counter()
for _ in range(60):
    while True:
        a = tuple(rng.randint(-9, 9) for _ in range(3))
        if any(a) and not on_mirror(a): break
    v = batch(fam(a, TS))
    tested += 1
    best[max(x for x in v if x)] += 1
    if 13 in v:
        print('   COUNTEREXAMPLE: axis %s reaches 13' % (a,), flush=True)
        worst += 1
print('   %d generic axes x %d angles = %d configurations' % (tested, len(TS), tested*len(TS)))
print('   best count reached, by axis: %s' % dict(sorted(best.items())))
print('   counterexamples to A1: %d' % worst)

print('\n=== the 13-locus inside one mirror plane (z = 0: axes (p, q, 0)) ===',
      flush=True)
print('   %-14s %s' % ('axis', 'angles t with count 13'))
for p in range(1, 9):
    for q in range(-8, 9):
        if math.gcd(abs(p), abs(q)) != 1: continue
        a = (p, q, 0)
        v = batch(fam(a, TS))
        hits = [t for t, c in zip(TS, v) if c == 13]
        if hits:
            print('   %-14s %s' % (str(a), ', '.join(str(t) for t in hits[:8])),
                  flush=True)
