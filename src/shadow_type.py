#!/usr/bin/env python3
"""Are the irrational 727s part of a continuum, or isolated points on it?

"Rationally shadowed" (Postscript 52) was established at the level of the
COUNT: rational points sampled along the same wall lines also reach 727.  That
leaves the sharper question open.  A configuration can be interior to a
continuum of the same COUNT while being an isolated point of its own
combinatorial TYPE — and the two answers differ in what they say about
whether irrationality is doing any work.

The distinction is decidable with the per-label vector, which Postscript 52
addendum 5 showed is exactly as sharp as the full adjacency profile:

  - if an irrational 727's per-label type ALSO occurs rationally, the
    irrational point is combinatorially indistinguishable from rational
    neighbours -- consistent with sitting inside a chamber, i.e. a continuum;
  - if its type occurs at NO rational configuration, the point is a stratum of
    its own, and the shadow covers the count but not the configuration.

There is a structural reason to expect the second.  The mixed strata solve TWO
planes and ONE quadric: three conditions, so every solution they produce --
rational or not -- is a point where three walls MEET, which Postscript 58
identifies as a chamber BOUNDARY, not a chamber interior.

INVARIANT: the two type sets are computed by the same engine convention
(per_label including label 0), and the irrational side is deduplicated under
the base's C3 symmetry first -- without that the 255 hits triple-count and any
"how many distinct types" number measures the enumerator, not the plateau.
"""
import collections
import json
import subprocess

FIVE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
FIXED_Q2 = ';'.join(','.join('%d:0' % x for x in q) for q in FIVE)
FIXED_N = ';'.join(','.join(map(str, q)) for q in FIVE)


def types_rational(quats):
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


def types_algebraic(d, quats):
    lines = [FIXED_Q2 + ';' + ','.join('%d:%d' % tuple(c) for c in q)
             for q in quats]
    out = subprocess.run(['./cube_regions_q2', '--d', str(d), '--quats-stdin'],
                         input='\n'.join(lines) + '\n',
                         capture_output=True, text=True).stdout
    res = []
    for l in out.splitlines():
        if l.startswith('{'):
            j = json.loads(l)
            res.append((j.get('bounded'),
                        tuple(sorted((int(k), v) for k, v in
                                     j.get('per_label', {}).items()))))
    return res


def main():
    reps = [tuple(q) for q in json.load(open('c727_reps.json'))]
    rat = types_rational(reps)
    rat_types = {t for tot, t in rat if tot == 727}
    print('rational 727 representatives: %d, distinct per-label types: %d'
          % (len(reps), len(rat_types)), flush=True)

    hits = [r for r in (json.loads(l) for l in open('mixed_q2_hits.jsonl'))
            if r['total'] == 727]
    byd = collections.defaultdict(list)
    for r in hits:
        byd[r['d']].append(tuple(tuple(c) for c in r['quat']))

    shared = collections.Counter()
    unique = collections.Counter()
    alltypes = {}
    for d in sorted(byd):
        qs = sorted(set(byd[d]))
        res = types_algebraic(d, qs)
        for q, (tot, t) in zip(qs, res):
            if tot != 727:
                continue
            alltypes.setdefault(t, []).append((d, q))
            if t in rat_types:
                shared[d] += 1
            else:
                unique[d] += 1

    print('\n%-8s %10s %12s' % ('field', 'shared', 'unique'))
    for d in sorted(set(shared) | set(unique)):
        print('Q(sqrt%-4d) %8d %12d' % (d, shared[d], unique[d]))
    print('\ntotals: %d irrational 727 configurations, %d distinct types'
          % (sum(shared.values()) + sum(unique.values()), len(alltypes)))
    print('   types also seen rationally: %d'
          % len({t for t in alltypes if t in rat_types}))
    print('   types seen ONLY irrationally: %d'
          % len({t for t in alltypes if t not in rat_types}))


if __name__ == '__main__':
    main()
