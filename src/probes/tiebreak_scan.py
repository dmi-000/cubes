#!/usr/bin/env python3
"""Does breaking a shared pair's tie (one cube scaled by 1 +- eps) ever lose regions both ways?  [P414]

For each shared-plane compound (the 16 run-bests of P411's climb, and a sample of the 700 of
degenerate_counts), find the sharing pair (i, j), and count with cube j scaled by 1 - eps and by
1 + eps, eps = 1e-6 and 1e-12.  The hope: max(shrink, grow) >= the actual count, always.  A compound
where both tie-breaks lose refutes it.  eps is a sample, not an infinitesimal: the two values must
agree, and a disagreement is reported as unevaluated, not scored.
Output: data/tiebreak_scan.json.
"""
import os, sys, json, itertools, random, multiprocessing as mp
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import c_level as CL
from euler3 import rowsT, frames
from scaled_count import count

ROOT = os.path.dirname(os.path.dirname(HERE))


def sharing_pairs(qs):
    Ms = [rowsT(R) for R in frames(qs)]
    out = []
    for i, j in itertools.combinations(range(len(qs)), 2):
        # a shared face plane = a common face normal up to sign = a zero cross product
        if any(not any([u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]])
               for u in Ms[i] for v in Ms[j]):
            out.append((i, j))
    return out


def job(qs):
    qs = [tuple(q) for q in qs]
    pairs = sharing_pairs(qs)
    base = count(qs)[0]
    row = {'qs': qs, 'pairs': pairs, 'count': base, 'breaks': {}}
    if len(pairs) != 1:
        row['note'] = 'not exactly one sharing pair: skipped'
        return row
    i, j = pairs[0]
    for sign in (-1, 1):
        vals = []
        for eps in (F(1, 10**6), F(1, 10**12)):
            sc = [1] * len(qs); sc[j] = 1 + sign * eps
            vals.append(count(qs, sc)[0])
        row['breaks']['shrink' if sign < 0 else 'grow'] = vals
    return row


def main():
    starts = [r['at'] for r in json.load(open(os.path.join(ROOT, 'data', 'shared_plane_climb.json')))]
    deg = json.load(open(os.path.join(ROOT, 'data', 'degenerate_counts.json')))['rows']
    rnd = random.Random(414)
    starts += [r['qs'] for r in deg[:12]] + [r['qs'] for r in rnd.sample(deg[12:], 20)]
    with mp.Pool(8) as p:
        rows = p.map(job, starts)
    lose_both = unev = skipped = ok = 0
    for r in rows:
        if not r['breaks']:
            skipped += 1; continue
        s, g = r['breaks']['shrink'], r['breaks']['grow']
        if s[0] != s[1] or g[0] != g[1]:
            unev += 1; r['verdict'] = 'UNEVALUATED (eps-dependent)'
        elif max(s[0], g[0]) >= r['count']:
            ok += 1; r['verdict'] = 'a tie-break keeps or gains'
        else:
            lose_both += 1; r['verdict'] = 'BOTH TIE-BREAKS LOSE'
        print(r['count'], 'shrink', s, 'grow', g, r['verdict'], flush=True)
    print('\n%d compounds: %d a tie-break keeps or gains, %d both lose, %d unevaluated, %d skipped (not one pair)'
          % (len(rows), ok, lose_both, unev, skipped))
    json.dump(rows, open(os.path.join(ROOT, 'data', 'tiebreak_scan.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
