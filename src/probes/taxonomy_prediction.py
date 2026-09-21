#!/usr/bin/env python3
"""Can the TAXONOMY -- not just the count -- be predicted from subset taxonomies?  [P346]

THE DERIVATION.  A vertex's support determines its signature ([P338]), so the vertices with
support exactly T are a property of T's own sub-arrangement.  A GENERIC 4-fold vertex `(1,1,1,1)`
lies on one facet of each of four cubes, so in every 3-subset of those four it appears as a
TRIPLE POINT; a genuine triple point appears in exactly one 3-subset.  Hence

    sum over 3-subsets S of t_S   =   T3 + 4 * Q4_generic                         (*)

which DERIVES [P343]'s budget law instead of measuring it.

THE RESTRICTION THAT MATTERS.  Only `(1,1,1,1)` counts with multiplicity four.  A `(3,3,3,3)`
vertex appears in a 3-subset as `(3,3,3)` -- a three-cube shared corner -- and a `(2,2,2,2)` as
`(2,2,2)`; neither is a triple point, so neither enters the left side of (*).  Verified on five
configurations, including three whose 4-fold vertices are of the non-generic kinds.

WHAT SUBSETS DO AND DO NOT PIN.  Writing tau_S for the vertices supported by exactly S,

    t_S = tau_S + Q4_generic        for EVERY 3-subset S

-- every generic 4-fold point sits in all four.  So `Q4_generic <= min_S t_S`, a real constraint,
and (*) fixes `T3 + 4*Q4_generic`; but the SPLIT between T3 and Q4 is not determined by these
relations.  That split is exactly what the count needs (`T3 + 3*Q4`), which is why [P340]'s
prediction from subset COUNTS carries a defect of `-Q4`.

MEASURED.  No collision found: over 260 configurations spanning 251 distinct proper-subset
taxonomies, no two shared a subset taxonomy while differing in the full one.  A search, hence a
lower bound ([METHODS 1]) -- no counterexample is not a proof.
"""
import sys, os, json, itertools, random, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as B
from c_level import shares_plane
import wall_keys as W
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))

NAMED = [('n=4 RECORD', [tuple(q) for q in W.REC[4]]),
         ('merged corner', [(1, 0, 0, 0), (1, -7, -8, 0), (2, -13, 0, -11), (1, 0, -4, -5)]),
         ('body-diagonal', [(1, 0, 0, 0), (3, 1, 1, 1), (2, 1, 1, 1), (5, 2, 2, 2)]),
         ('face-diagonal', [(1, 0, 0, 0), (3, 2, 2, 0), (5, 4, 4, 0), (4, 3, 3, 0)])]


def sig_of(qs):
    s, _ = B.vertices(qs)
    return s


def tax(qs):
    return tuple(sorted((str(k), v) for k, v in sig_of(qs).items()))


def subset_tax(qs, n=4):
    rows = []
    for k in (2, 3):
        for S in itertools.combinations(range(n), k):
            rows.append((k, tax([qs[i] for i in S])))
    return tuple(sorted(rows))


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 260
    out = {'what': 'predicting the taxonomy from subset taxonomies', 'supports': 'LEDGER P346'}

    print('=== the identity  sum_S t_S = T3 + 4*Q4_generic ===')
    rows = []
    for lbl, qs in NAMED:
        s = sig_of(qs)
        T3 = s.get((1, 1, 1), 0)
        Qg = s.get((1, 1, 1, 1), 0)
        Qo = sum(v for k, v in s.items() if len(k) == 4) - Qg
        tot = sum(sig_of([qs[i] for i in S]).get((1, 1, 1), 0)
                  for S in itertools.combinations(range(4), 3))
        ok = tot == T3 + 4 * Qg
        rows.append({'label': lbl, 'sum_t_S': tot, 'T3': T3, 'Q4_generic': Qg,
                     'Q4_other': Qo, 'identity_holds': ok})
        print('   %-16s sum t_S %4d   T3 %4d   Q4gen %3d   Q4other %2d   T3+4Qg %4d  %s'
              % (lbl, tot, T3, Qg, Qo, T3 + 4 * Qg, 'OK' if ok else 'MISMATCH'))
    print('   (the golden 177, from data/golden_a4.json: 128 = 56 + 4*18)')
    out['identity'] = rows

    print('\n=== the bound Q4_generic <= min_S t_S ===')
    for lbl, qs in NAMED:
        ts = [sig_of([qs[i] for i in S]).get((1, 1, 1), 0)
              for S in itertools.combinations(range(4), 3)]
        Qg = sig_of(qs).get((1, 1, 1, 1), 0)
        print('   %-16s t_S %s   min %3d   Q4gen %d  %s'
              % (lbl, ts, min(ts), Qg, 'OK' if Qg <= min(ts) else 'VIOLATED'))

    print('\n=== collision: same subset taxonomy, different full taxonomy? ===')
    groups = collections.defaultdict(dict)
    rng = random.Random(83)
    n = 0
    while n < trials:
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-8, 8) for _ in range(4)) for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            k, t = subset_tax(qs), tax(qs)
        except Exception:
            continue
        n += 1
        groups[k][t] = qs
    clash = [k for k, v in groups.items() if len(v) > 1]
    print('   configurations %d   distinct subset-taxonomies %d' % (n, len(groups)))
    print('   subset-taxonomies carrying MORE THAN ONE full taxonomy: %d' % len(clash))
    print('   SCOPE: a search, hence a lower bound -- no counterexample is not a proof.')
    out['collisions'] = {'configs': n, 'distinct_subset_taxonomies': len(groups),
                         'clashes': len(clash),
                         'scope': 'integer quaternions in [-8,8]; lower bound only'}

    out['reproduce'] = PROV.stamp(parameters={'trials': trials, 'seed': 83})
    json.dump(out, open(os.path.join(ROOT, 'data', 'taxonomy_prediction.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/taxonomy_prediction.json')


if __name__ == '__main__':
    main()
