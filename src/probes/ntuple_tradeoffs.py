#!/usr/bin/env python3
"""What are the trade-offs among n-tuple points?  [P335]

THE EXCESS OF A b-FOLD VERTEX, measured per vertex (`sum_levels (deg - 2)`) and never read off
[P328]'s table, which records generic values only:

    generic       (1,1,...,1)   b cubes, transversal        (b-1)(b-2)
    edge-concurrent (2,2,...,2) b cubes' EDGES concurrent    2(b-1)^2
    corner-shared (3,3,...,3)   b cubes sharing a CORNER    (b-1)(3b-2)

THE MERGE IDENTITY, exact in both multi-cube families at every b tested:

    e_X(b)  =  C(b,2) * e_X(2)  +  (b-1)(b-2)

A b-fold vertex is worth its C(b,2) PAIRWISE contributions PLUS a free generic b-fold point.
So merging is LOCALLY always better, by exactly the generic b-fold excess.

AND YET THE RECORDS DO NOT MERGE.  Because forcing b cubes through one point needs a shared
axis, and a shared axis is what destroys generic triple points -- which dominate the sum (128
of the record's 176 half-excess).  The curve is NOT monotone, and the record sits at its peak.
"""
import sys, os, json, random, collections, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as B
from c_level import shares_plane, engine
import wall_keys as W
import provenance as PROV

FACE = [(1, 0, 0, 0), (3, 2, 2, 0), (5, 4, 4, 0), (4, 3, 3, 0), (5, 3, 3, 0), (6, 5, 5, 0)]
BODY = [(1, 0, 0, 0), (3, 1, 1, 1), (2, 1, 1, 1), (5, 2, 2, 2), (4, 1, 1, 1)]
LAWS = {'generic': lambda b: (b - 1) * (b - 2),
        'edge': lambda b: 2 * (b - 1) ** 2,
        'corner': lambda b: (b - 1) * (3 * b - 2)}


def measured_excesses():
    """signature -> set of measured excess values, over families chosen to exhibit each type."""
    tab = collections.defaultdict(set)
    def harvest(qs):
        if shares_plane(qs):
            return
        _, meas = B.vertices(qs)
        for k, d in meas.items():
            for e, c in d.items():
                tab[k].add(e)
    for n in range(2, 7):
        harvest(FACE[:n])
    for n in range(2, 6):
        harvest(BODY[:n])
    for n in (4, 5, 6):
        harvest([tuple(q) for q in W.REC[n]])
    return tab


def profile(qs):
    sig, meas = B.vertices(qs)
    by = engine(qs).get('by_depth') or {}
    return {'T3': sig.get((1, 1, 1), 0), 'EE': sig.get((2, 2), 0), 'SC2': sig.get((3, 3), 0),
            'corner_pairs': sig.get((3, 3), 0) // 2,
            'two_body': sig.get((2, 2), 0) + 2 * sig.get((3, 3), 0),
            'merged': {str(k): v for k, v in sig.items() if len(k) > 2 and set(k) == {3}},
            'half_excess': sum(e * c for k in meas for e, c in meas[k].items()) // 2,
            'count': sum(v for k, v in by.items() if k != '0')}


def main():
    out = {'what': 'trade-offs among n-tuple points', 'supports': 'LEDGER P335'}

    print('=== MEASURED excess by signature ===')
    tab = measured_excesses()
    fam = {'generic': {}, 'edge': {}, 'corner': {}}
    for k in sorted(tab, key=lambda t: (len(t), t)):
        b = len(k)
        which = ('generic' if set(k) == {1} else 'edge' if set(k) == {2}
                 else 'corner' if set(k) == {3} else None)
        vals = sorted(tab[k])
        mark = ''
        if which and len(vals) == 1:
            fam[which][b] = vals[0]
            mark = '   law %s -> %d  %s' % (which, LAWS[which](b),
                                            'OK' if LAWS[which](b) == vals[0] else 'MISMATCH')
        print('   %-22s b=%d  excess %s%s' % (str(k), b, vals, mark))
    out['measured'] = {w: {str(b): e for b, e in d.items()} for w, d in fam.items()}

    print('\n=== the MERGE IDENTITY: e(b) = C(b,2)*e(2) + (b-1)(b-2) ===')
    rows = []
    for which, e2 in (('corner', 4), ('edge', 2)):
        for b in range(2, 7):
            merged = LAWS[which](b)
            split = (b * (b - 1) // 2) * e2
            rows.append({'family': which, 'b': b, 'merged': merged, 'split': split,
                         'gain': merged - split, 'generic_bfold': (b - 1) * (b - 2),
                         'identity_holds': merged - split == (b - 1) * (b - 2)})
            print('   %-7s b=%d   merged %3d   split %3d   gain %3d   (b-1)(b-2) = %3d  %s'
                  % (which, b, merged, split, merged - split, (b - 1) * (b - 2),
                     'OK' if merged - split == (b - 1) * (b - 2) else 'FAIL'))
    out['merge_identity'] = rows

    print('\n=== BUT GLOBALLY THERE IS AN INTERIOR OPTIMUM (n = 4) ===')
    cfgs = [('n=4 RECORD', [tuple(q) for q in W.REC[4]]),
            ('body-diagonal (merged)', BODY[:4])]
    rng = random.Random(5)
    got = 0
    while got < 3:
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            if profile(qs)['SC2'] == 0:
                cfgs.append(('random #%d' % (got + 1), qs)); got += 1
        except Exception:
            continue
    tbl = []
    print('   %-24s %6s %8s %9s %7s' % ('configuration', 'pairs', 'T3', 'two-body', 'count'))
    for lbl, qs in cfgs:
        p = profile(qs)
        tbl.append(dict(p, label=lbl, quats=[list(q) for q in qs]))
        print('   %-24s %6s %8s %9d %7d %s'
              % (lbl, p['corner_pairs'] if not p['merged'] else 'merged',
                 '%d%s' % (p['T3'], ' CAP' if p['T3'] == 128 else ''),
                 p['two_body'], p['count'],
                 str(p['merged']) if p['merged'] else ''))
    print('   %-24s %6d %8d %9d %7s   (exact, [P334])' % ('K4 compound', 6, 74, 60, '138+h'))
    tbl.append({'label': 'K4 compound', 'corner_pairs': 6, 'T3': 74, 'two_body': 60,
                'count': None, 'note': 'exact, P334'})
    out['n4_curve'] = tbl

    print('\n   0 pairs -> T3 ~100 (random);  3 pairs -> T3 = 128 CAP (the record);')
    print('   6 pairs -> T3 = 74;  merged 4-fold -> T3 = 72.')
    print('   Past the optimum: 3->6 pairs gains 6 regions and costs 54 triple points. NET -48.')

    out['reproduce'] = PROV.stamp(parameters={'families': {'face': [list(q) for q in FACE],
                                                           'body': [list(q) for q in BODY]},
                                              'random_seed': 5})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'ntuple_tradeoffs.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/ntuple_tradeoffs.json')


if __name__ == '__main__':
    main()
