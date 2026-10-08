#!/usr/bin/env python3
"""The Mayer-Vietoris route to d2 <= 70 on shared-plane compounds, measured.  [P415]

[P110]/[P399]: for each pair P = {x, y} with the other two z, w,
    s_P <= a_P + b_P + m_P - 2,
where s_P = #pi0 D({x,y}) in the compound, a_P and b_P are the same set's counts in the triples
xyz and xyw, and m_P = #pi0 {x or y innermost of the four}.  Summing over the six pairs,
    d2 <= sum_S d2(S) + sum_P (m_P - 2).
On shared-plane compounds sum_S d2(S) <= 64 ([P413]), so d2 <= 70, which gives 195 there, follows
from sum_P m_P <= 18.  This measures both sums with sphere_count's exact counter on the shared-plane
compounds of tiebreak_scan, with the 183 record (generic) as a reference.
Output: data/shared_mv.json.
"""
import os, sys, json, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from sphere_count import Compound

ROOT = os.path.dirname(os.path.dirname(HERE))


def job(qs):
    C = Compound([tuple(q) for q in qs], 'Q')
    tot, dep = C.count()
    rows = [r for r in C.mv_checks() if r[0].startswith('D')]
    sumS = sum(r[2] + r[3] for r in rows)
    sumM = sum(r[4] for r in rows)
    return {'qs': qs, 'total': tot, 'd2': dep.get(2), 'sum_d2S': sumS, 'sum_m': sumM,
            'mv_bound': sumS + sumM - 12, 'm_by_pair': {r[0]: r[4] for r in rows},
            'mv_ok': all(r[1] <= r[2] + r[3] + r[4] - 2 for r in rows)}


def main():
    qs = [r['qs'] for r in json.load(open(os.path.join(ROOT, 'data', 'tiebreak_scan.json')))]
    qs.append([(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)])
    with mp.Pool(8) as p:
        out = p.map(job, qs)
    for r in out:
        print('total %3d d2 %2d | sum d2(S) %2d  sum m %2d  MV bound on d2 %2d  %s  m %s'
              % (r['total'], r['d2'], r['sum_d2S'], r['sum_m'], r['mv_bound'], 'MV ok' if r['mv_ok'] else 'MV VIOLATED',
                 sorted(r['m_by_pair'].values())))
    sh = out[:-1]
    print('\nshared-plane compounds: %d; max sum d2(S) %d (cap 64); max sum m %d (need <= 18); max MV bound %d (need <= 70)'
          % (len(sh), max(r['sum_d2S'] for r in sh), max(r['sum_m'] for r in sh), max(r['mv_bound'] for r in sh)))
    json.dump(out, open(os.path.join(ROOT, 'data', 'shared_mv.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
