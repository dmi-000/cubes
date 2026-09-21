#!/usr/bin/env python3
"""Is there room to beat the records -- by new COMPONENTS, or new COMBINATIONS?  [P347]

PART 1, THE COMPONENT SPACE, and it is now CHARACTERISED.

  THEOREM (one line, same shape as [P311]).  A cube is `{x : |<x,v_k>| <= 1}` with `v_k`
  orthonormal, so `|x|^2 = sum_k <x,v_k>^2 <= 3` with equality IFF every term is 1 -- i.e. only
  at a CORNER.  So the only boundary points at distance sqrt3 are corners.  A corner of cube j
  IS at distance sqrt3, so if a vertex is a corner of j it must be a corner of EVERY cube whose
  boundary contains it.

      => a signature is ALL 3s, or contains NO 3.   (1,3), (2,3), (1,1,3), ... are IMPOSSIBLE.

  And a signature is a VERTEX (0-dimensional) only if its facet conditions sum to >= 3, which
  kills `(1,1)` -- two surfaces meeting transversally give a CURVE.

PART 2, THE COMBINATIONS.  At n = 4 with trivial holes, `TOTAL = sum_S h(S) + 5 - Q4` where
`h(S) = count(S) - (1/2)(its pair counts)`.  Beating 183 needs `sum_h - Q4 > 178`.
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
P328 = {(1, 2), (2, 2), (1, 1, 1), (3, 3), (1, 1, 1, 1), (2, 2, 2), (3, 3, 3)}
NAMED = [('n=4 RECORD', [tuple(q) for q in W.REC[4]]),
         ('merged corner', [(1, 0, 0, 0), (1, -7, -8, 0), (2, -13, 0, -11), (1, 0, -4, -5)]),
         ('body-diagonal', [(1, 0, 0, 0), (3, 1, 1, 1), (2, 1, 1, 1), (5, 2, 2, 2)])]


def stats(qs):
    hs = []
    for S in itertools.combinations(range(4), 3):
        sub = [qs[i] for i in S]
        t = count(sub)
        ps = [count([sub[i] for i in P]) for P in itertools.combinations(range(3), 2)]
        hs.append(t - 0.5 * sum(ps))
    s, _ = B.vertices(qs)
    Q4 = sum(v for k, v in s.items() if len(k) == 4)
    return sum(hs), Q4, count(qs)


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 160
    out = {'what': 'room to beat records: components and combinations', 'supports': 'LEDGER P347'}

    print('=== PART 1: which signatures OCCUR, and which are permitted ===')
    seen, exc = collections.Counter(), collections.defaultdict(set)
    rng = random.Random(101)
    n = 0
    while n < 120:
        m = rng.choice([3, 4, 4, 5])
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(m - 1)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            s, meas = B.vertices(qs)
        except Exception:
            continue
        n += 1
        for k, v in s.items():
            seen[k] += v
        for k, d in meas.items():
            for e in d:
                exc[k].add(e)
    mixed = [k for k in seen if 3 in k and set(k) != {3}]
    print('   configurations %d;  signatures MIXING 3 with 1 or 2: %d  %s'
          % (n, len(mixed), mixed if mixed else '(none -- the theorem)'))
    for k in sorted(seen, key=lambda t: (len(t), t)):
        print('      %-14s count %6d  excess %-10s %s'
              % (str(k), seen[k], sorted(exc[k]), '' if k in P328 else '** NOT in P328 **'))
    permitted = set()
    for b in range(2, 6):
        for c in itertools.combinations_with_replacement((1, 2), b):
            if sum(c) >= 3:
                permitted.add(tuple(sorted(c)))
        permitted.add(tuple([3] * b))
    unobs = sorted(permitted - set(seen), key=lambda t: (len(t), t))
    print('   PERMITTED but unobserved here: %s' % [str(k) for k in unobs][:10])
    out['components'] = {'observed': {str(k): seen[k] for k in sorted(seen, key=str)},
                         'mixed_three': len(mixed),
                         'not_in_P328': [str(k) for k in seen if k not in P328],
                         'permitted_unobserved': [str(k) for k in unobs]}

    print('\n=== PART 2: the feasible region, TOTAL = sum_h + 5 - Q4 ===')
    rows = [{'label': 'golden 177', 'sum_h': 190.0, 'Q4': 18, 'total': 177},
            {'label': '67-extension', 'sum_h': 168.0, 'Q4': 0, 'total': 175}]
    for lbl, qs in NAMED:
        sh, q, t = stats(qs)
        rows.append({'label': lbl, 'sum_h': sh, 'Q4': q, 'total': t})
    print('   %-18s %8s %5s %11s %7s' % ('configuration', 'sum h', 'Q4', 'sum h - Q4', 'TOTAL'))
    for r in sorted(rows, key=lambda r: -r['total']):
        print('   %-18s %8.1f %5d %11.1f %7d'
              % (r['label'], r['sum_h'], r['Q4'], r['sum_h'] - r['Q4'], r['total']))
    env = collections.defaultdict(float)
    rng = random.Random(113)
    n = 0
    while n < trials:
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            sh, q, t = stats(qs)
        except Refused:
            continue
        except Exception:
            continue
        n += 1
        env[q] = max(env[q], sh)
    print('   random %d configs, upper envelope of sum_h by Q4: %s'
          % (n, {k: round(v, 1) for k, v in sorted(env.items())}))
    print('\n   sum_h <= 190 (= 4 x 47.5, the 67 maximum), so TOTAL <= 195.')
    print('   The record sits at (178, 0); the golden at (190, 18).')
    print('   Room to beat 183 is exactly the region 178 < sum_h - Q4, and it lies in the')
    print('   UNMAPPED middle of the frontier.  The two known endpoints give slope 18/12 = 1.5;')
    print('   if the frontier slope is >= 1 throughout, there is NO room and 183 is optimal.')
    out['region'] = {'points': rows, 'envelope': {str(k): v for k, v in sorted(env.items())},
                     'sum_h_max': 190.0, 'total_ceiling': 195,
                     'endpoint_slope': 1.5,
                     'conjecture': 'Q4 >= 1.5*(sum_h - 178) would give max(4) = 183'}

    out['reproduce'] = PROV.stamp(parameters={'trials': trials})
    json.dump(out, open(os.path.join(ROOT, 'data', 'component_space.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/component_space.json')


if __name__ == '__main__':
    main()
