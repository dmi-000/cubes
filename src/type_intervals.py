#!/usr/bin/env python3
"""Are the members of a per-label type one interval of one wall line?

Measured so far (Postscript 52 addendum 6): members of a type share their pair
counts against the base exactly (416/416), sit a median 0.285 degrees apart
against 5.598 between types, and 69% of within-type pairs come from the same
wall line.  That suggests a sharper statement than "they are close":

    a type is a CHAMBER of the wall line — the stretch between two
    consecutive crossings, on which the count and the whole combinatorial
    type are constant.

The two planes cut a rational line; moving along it preserves both conditions,
so the count can only change where the line crosses a further wall.  If the
hypothesis holds, then ordering a type's members by their line parameter t
should show them CONSECUTIVE, with every sampled rational point between them
also counting 727 and carrying the same per-label vector.

This walks each line finely, records the count and type at every sampled
point, and reports the runs.
"""
import collections
import json
import math
import pickle
import subprocess
from fractions import Fraction as F

FIVES = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"


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


def to_quat(pt, cap=512):
    den = 1
    for v in pt:
        den = den * v.denominator // math.gcd(den, v.denominator)
    q = (den, int(pt[0]*den), int(pt[1]*den), int(pt[2]*den))
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    q = tuple(x//g for x in q) if g > 1 else q
    return q if any(q) and max(abs(x) for x in q) <= cap else None


def main():
    planes = pickle.load(open('locus_planes.pkl', 'rb'))
    P = json.load(open('provenance_727.json'))
    lines, seen = [], set()
    for rec in P:
        k = (tuple(rec['cubes_planes']), tuple(rec['plane_idx']))
        if k in seen:
            continue
        seen.add(k)
        pi, pj = rec['cubes_planes']
        i1, i2 = rec['plane_idx']
        L = line_of(planes[pi][i1], planes[pj][i2])
        if L:
            lines.append((k, L))
    print('727-producing lines: %d' % len(lines), flush=True)

    runs_all = []
    for idx, (tag, (p0, dd)) in enumerate(lines[:12]):
        pts = []
        for num in range(-600, 601):
            t = F(num, 6)
            q = to_quat(tuple(p0[u] + t*dd[u] for u in range(3)))
            if q:
                pts.append((t, q))
        # dedup consecutive identical quaternions, keep order along the line
        uniq = []
        for t, q in pts:
            if not uniq or uniq[-1][1] != q:
                uniq.append((t, q))
        out = subprocess.run(['./cube_regions_n', '--quats-stdin'],
                             input='\n'.join(FIVES+';'+','.join(map(str, q))
                                             for _, q in uniq)+'\n',
                             capture_output=True, text=True).stdout
        rows = [json.loads(l) for l in out.splitlines() if l.startswith('{')]
        seq = []
        for (t, q), d in zip(uniq, rows):
            tot = d.get('bounded')
            lab = tuple(sorted(d['per_label'].items())) if tot == 727 else None
            seq.append((t, tot, lab))
        # runs of consecutive sampled points that are 727 with the same type
        runs = []
        cur = None
        for t, tot, lab in seq:
            if tot == 727:
                if cur and cur[0] == lab:
                    cur[2] += 1
                    cur[3] = t
                else:
                    if cur:
                        runs.append(cur)
                    cur = [lab, t, 1, t]
            else:
                if cur:
                    runs.append(cur)
                cur = None
        if cur:
            runs.append(cur)
        n727 = sum(1 for _, tot, _ in seq if tot == 727)
        print('  line %2d: %4d sampled points, %3d count 727, in %d maximal runs'
              ' of one type; run lengths %s'
              % (idx, len(seq), n727, len(runs),
                 sorted((r[2] for r in runs), reverse=True)[:8]), flush=True)
        runs_all.extend(runs)
    if runs_all:
        L = [r[2] for r in runs_all]
        print('\nacross the sampled lines: %d runs, lengths min %d median %d max %d'
              % (len(L), min(L), sorted(L)[len(L)//2], max(L)))
        print('a run length > 1 means the count AND the per-label type are')
        print('constant along a stretch of the line — i.e. the type is an')
        print('interval, not an isolated point.')


if __name__ == '__main__':
    main()
