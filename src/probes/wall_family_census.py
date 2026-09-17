#!/usr/bin/env python3
"""How many walls pass through each record -- BOTH families, genuine ones separated.

[OQ 4] asks why the tower gains 24 walls per added cube. That count is the COINCIDENCE
family alone, which [P304] showed is not the wall family of the count. This counts both, and
splits the concurrency family into quadruples that actually have a common point
(rank(normals) = rank(augmented) = 3) and those whose determinant vanishes for rank reasons --
a parallel pair, or an inconsistent system -- which are not walls at all.
"""
import sys, os, json
from fractions import Fraction as F
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import dimension as D, wall_keys as W, wall_solve as WS
import concurrency_walls as CW, plateau_solve as PS, provenance as PROV

out = {'what': 'walls through each record, both families, genuine concurrences separated',
       'question': 'OPEN_QUESTIONS 4, re-asked with the family P304 found',
       'levels': {}}
for n in (4, 5, 6, 7, 8):
    quats = list(W.REC[n]); q0 = quats[0]
    D.set_field(0); D.QZERO[:] = [q0]
    pt = D.point_of(quats); nc = len(pt)
    _, _, walls = PS.tight_walls(quats)
    tight = sum(1 for c in WS.conditions_on(quats) if c['tight'])
    z = [F(0)] * nc
    P0 = CW.planes_at(pt, z, q0, F(0)); rows0 = [x[1] for x in P0]
    thru = gen = 0
    for c in combinations(range(len(P0)), 4):
        rows = [rows0[i] for i in c]
        if CW.concur_det(*rows) != 0:
            continue
        thru += 1
        if PS.rank([x[:3] for x in rows]) == PS.rank(rows) == 3:
            gen += 1
    out['levels'][str(n)] = {'ambient': nc, 'record': D.count_at(pt, len(quats)),
                             'tight_conditions': tight,
                             'coincidence_walls': len(walls),
                             'concurrency_quadruples_through_record': thru,
                             'genuine_concurrency_walls': gen,
                             'rank_degenerate': thru - gen}
    print('n=%d | coincidence walls %3d | concurrency through record %4d | genuine %4d | '
          'rank-degenerate %4d' % (n, len(walls), thru, gen, thru - gen), flush=True)
out['reproduce'] = PROV.stamp(parameters={'levels': [4, 5, 6, 7, 8]})
json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'wall_family_census.json'), 'w'),
          indent=1, default=str)
print('written data/wall_family_census.json')
