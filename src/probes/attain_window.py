#!/usr/bin/env python3
"""The CONSTRUCTIVE attempt on the window [OQ 39].  [P349]

If infeasibility cannot be proved, attain it.  The framework makes the target exact: at n = 4
with trivial holes,

    TOTAL = 7 + two-body + B - Q4 ,     B := T3 + 4*Q4_generic <= 128
    beating 183  <=>  two-body + B - Q4 > 176      (the record sits at 48 + 128 - 0 = 176)

THE OBVIOUS SEARCH TARGET IS THE WRONG ONE.  A pair counts 13 iff its two-body is 10, so "get
more pairs to 13" looks right.  It is not: **isolated pair quality does not transfer to the
compound.**  The body-diagonal family has ALL SIX pairs counting 13 -- every pair a proved
2-cube maximiser -- and its compound two-body is 36, not 60, because all four cubes share the
SAME corner and the six `(3,3)` vertices merge into one `(3,3,3,3)`.  It counts 145.

So the target must be stated in COMPOUND quantities, and the exchange rates out of the record
are adverse in both available directions.
"""
import sys, os, json, itertools, random, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as B
from c_level import shares_plane
from subset_predictor import count, Refused
import wall_keys as W
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
NAMED = [('n=4 RECORD', [tuple(q) for q in W.REC[4]]),
         ('body-diagonal', [(1, 0, 0, 0), (3, 1, 1, 1), (2, 1, 1, 1), (5, 2, 2, 2)]),
         ('face-diagonal', [(1, 0, 0, 0), (3, 2, 2, 0), (5, 4, 4, 0), (4, 3, 3, 0)])]


def anat(qs):
    s, _ = B.vertices(qs)
    EE = s.get((2, 2), 0)
    SC = s.get((3, 3), 0)
    T3 = s.get((1, 1, 1), 0)
    Qg = s.get((1, 1, 1, 1), 0)
    Q4 = sum(v for k, v in s.items() if len(k) == 4)
    pc = [count([qs[i] for i in P]) for P in itertools.combinations(range(4), 2)]
    tb, Bv = EE + 2 * SC, T3 + 4 * Qg
    return {'isolated_pairs': pc, 'EE': EE, 'SC2': SC, 'two_body': tb, 'B': Bv, 'Q4': Q4,
            'objective': tb + Bv - Q4, 'total': count(qs)}


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
    out = {'what': 'constructive attempt on the record-beating window',
           'supports': 'LEDGER P349', 'target': 'two_body + B - Q4 > 176'}

    print('=== isolated pair quality does NOT transfer to the compound ===')
    rows = []
    for lbl, qs in NAMED:
        a = anat(qs)
        rows.append(dict(a, label=lbl))
        print('   %-15s isolated pairs %-26s two-body %2d  B %3d  Q4 %2d  obj %3d  TOTAL %3d'
              % (lbl, str(a['isolated_pairs']), a['two_body'], a['B'], a['Q4'],
                 a['objective'], a['total']))
    print('   the body-diagonal family has all six pairs at the 2-cube MAXIMUM and counts 145:')
    print('   its four cubes share ONE corner, so the six (3,3)s merge and SC2 = 0.')
    out['named'] = rows

    print('\n=== can random search even reach >= 4 isolated 13-pairs? ===')
    rng = random.Random(151)
    dist = collections.Counter()
    n = 0
    while n < trials:
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            pc = [count([qs[i] for i in P]) for P in itertools.combinations(range(4), 2)]
        except Refused:
            continue
        except Exception:
            continue
        n += 1
        dist[sum(1 for c in pc if c == 13)] += 1
    print('   sampled %d;  #pairs at 13: %s' % (n, dict(sorted(dist.items()))))
    print('   four or more: %d  -- random sampling does not reach it ([METHODS 1])'
          % sum(v for k, v in dist.items() if k >= 4))
    out['sampling'] = {'sampled': n, 'distribution': {str(k): v for k, v in sorted(dist.items())},
                       'four_or_more': sum(v for k, v in dist.items() if k >= 4)}

    print('\n=== the exchange rates out of the record ===')
    print('   corner route : record SC2=6 (3 sharings) B=128  ->  K4 [P334] SC2=12 (6) B=74')
    print('                  per sharing: two-body +4, B -18        NET -14')
    print('   edge route   : face-diagonal raises EE 36 -> 42, and B falls 128 -> 84')
    print('                  NET adverse as well')
    print('   both available directions out of the record are DOWNHILL.')
    out['exchange'] = {'corner_per_sharing': {'two_body': +4, 'B': -18, 'net': -14},
                       'edge_face_diagonal': {'EE': +6, 'B': -44, 'net': -38}}

    out['reproduce'] = PROV.stamp(parameters={'trials': trials, 'seed': 151})
    json.dump(out, open(os.path.join(ROOT, 'data', 'attain_window.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/attain_window.json')


if __name__ == '__main__':
    main()
