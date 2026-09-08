#!/usr/bin/env python3
"""How are configurations within one per-label type related to each other?

The 727 plateau on the 393 base holds 161 configurations (after quotienting by
the free cube's own 24 rotations AND the base's C3) in 54 per-label types.
Members of a type share every combinatorial invariant the project can compute
yet are not congruent, so something else relates them — or nothing does.

Candidates tested here:
  * PROVENANCE   — do members come from the same wall line, or different ones?
  * PAIR SIGNATURE — do they form the same pair counts against the five base
    cubes (9,9,9,4,4 for the record itself)?
  * GEOMETRY     — how far apart are they as rotations, modulo the symmetries?

Mirror symmetry was ruled out separately: the base is chiral (its only
improper "symmetries" are the central inversion times C3, and -I acts
trivially on cubes because cubes are centrally symmetric), so reflecting a
configuration lands it over a different base.
"""
import collections
import itertools
import json
import math
import pickle
import subprocess
from fractions import Fraction as F

import record_hunt as R

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
FIVES = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"


def qmul(p, q):
    w, x, y, z = p
    e, f, g, h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)


SYM = list(dict.fromkeys(
    R.canon([t])[0] for t in
    [(w, x, y, z) for w in (-1, 0, 1) for x in (-1, 0, 1) for y in (-1, 0, 1)
     for z in (-1, 0, 1)
     if (w, x, y, z) != (0, 0, 0, 0) and w*w+x*x+y*y+z*z in (1, 2, 4)]))
C3 = [(1, 0, 0, 0), (1, 1, 1, 1), (1, -1, -1, -1)]


def sk(q):
    return min(R.canon([qmul(tuple(q), h)])[0] for h in SYM)


def fullkey(q):
    return min(sk(qmul(g, tuple(q))) for g in C3)


def line_of(p, q):
    n1, n2 = p[:3], q[:3]
    d = (n1[1]*n2[2]-n1[2]*n2[1], n1[2]*n2[0]-n1[0]*n2[2], n1[0]*n2[1]-n1[1]*n2[0])
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


def to_quat(pt):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0]*den), int(pt[1]*den), int(pt[2]*den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x//g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= 512 else None


def unit(q):
    n = math.hypot(*q)
    u = [v/n for v in q]
    return u if u[0] >= 0 else [-v for v in u]


SYMF = [tuple(x/math.sqrt(sum(v*v for v in t)) for x in t)
        for t in itertools.product([-1, 0, 1], repeat=4)
        if sum(v*v for v in t) in (1, 2, 4)]


def geodist(a, b):
    """Angle between two rotations, modulo the cube's own symmetries and C3."""
    best = 0.0
    for g in C3:
        gb = unit(qmul(g, b))
        for h in SYMF:
            d = abs(sum(p*q for p, q in zip(unit(a), qmul(gb, h))))
            best = max(best, min(1.0, d))
    return 2*math.degrees(math.acos(best))


def main():
    planes = pickle.load(open('locus_planes.pkl', 'rb'))
    P = json.load(open('provenance_727.json'))
    data, seen = {}, set()
    for rec in P:
        k = (tuple(rec['cubes_planes']), tuple(rec['plane_idx']))
        if k in seen:
            continue
        seen.add(k)
        pi, pj = rec['cubes_planes']
        i1, i2 = rec['plane_idx']
        L = line_of(planes[pi][i1], planes[pj][i2])
        if L is None:
            continue
        p0, dd = L
        qs = []
        for num in range(-500, 501):
            for den in (1, 2, 3, 4, 5, 7, 9):
                q = to_quat(tuple(p0[u] + F(num, den)*dd[u] for u in range(3)))
                if q:
                    qs.append(q)
        qs = list(dict.fromkeys(qs))
        out = subprocess.run(['./cube_regions_n', '--quats-stdin'],
                             input='\n'.join(FIVES+';'+','.join(map(str, q))
                                             for q in qs)+'\n',
                             capture_output=True, text=True).stdout
        for ln, q in zip([l for l in out.splitlines() if l.startswith('{')], qs):
            d = json.loads(ln)
            if d.get('bounded') == 727:
                data.setdefault(fullkey(q),
                                (q, tuple(sorted(d['per_label'].items())), k))
    print('configurations: %d' % len(data), flush=True)
    types = collections.defaultdict(list)
    for key, (q, lab, prov) in data.items():
        types[lab].append((q, prov))
    print('per-label types: %d' % len(types), flush=True)
    sizes = collections.Counter(len(v) for v in types.values())
    print('type sizes: %s\n' % dict(sorted(sizes.items())), flush=True)

    def pairsig(q):
        s = []
        for b in FIVE:
            o = subprocess.run(['./cube_regions_n', '--quats',
                                ','.join(map(str, b))+';'+','.join(map(str, q))],
                               capture_output=True, text=True).stdout
            s.append(json.loads(o)['bounded'] if o.startswith('{') else 0)
        return tuple(sorted(s, reverse=True))

    same_line = diff_line = 0
    same_sig = diff_sig = 0
    dists = []
    for lab, members in types.items():
        if len(members) < 2:
            continue
        sigs = [pairsig(m[0]) for m in members]
        for i, j in itertools.combinations(range(len(members)), 2):
            if members[i][1] == members[j][1]:
                same_line += 1
            else:
                diff_line += 1
            if sigs[i] == sigs[j]:
                same_sig += 1
            else:
                diff_sig += 1
            dists.append(geodist(members[i][0], members[j][0]))
    print('WITHIN-TYPE pairs of configurations: %d' % len(dists), flush=True)
    print('  from the SAME wall line      : %d' % same_line, flush=True)
    print('  from DIFFERENT wall lines    : %d' % diff_line, flush=True)
    print('  same pair-count signature    : %d' % same_sig, flush=True)
    print('  different pair signature     : %d' % diff_sig, flush=True)
    if dists:
        ds = sorted(dists)
        print('  geodesic separation (deg): min %.3f  median %.3f  max %.3f'
              % (ds[0], ds[len(ds)//2], ds[-1]), flush=True)
    # for contrast: separation between configurations of DIFFERENT types
    reps = [v[0][0] for v in types.values()]
    cross = [geodist(reps[i], reps[j])
             for i, j in itertools.combinations(range(min(len(reps), 25)), 2)]
    if cross:
        cs = sorted(cross)
        print('  ACROSS types, for contrast: min %.3f  median %.3f  max %.3f'
              % (cs[0], cs[len(cs)//2], cs[-1]), flush=True)


if __name__ == '__main__':
    main()
