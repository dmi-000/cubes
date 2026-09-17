#!/usr/bin/env python3
"""Is c_ell >= 3 reachable next to a RECORD?  [OQ 30]'s last ingredient, looked for where
nobody has looked.

[OQ 30] reduces a proved cap max(4) <= 198 to the claim c_ell <= 2, i.e. the quotient level
graph mod the antipodal map is connected. Every instance behind that claim -- 418
non-degenerate level-instances, 0 with c >= 3 -- came from sampling random INTEGER quaternions.

A record is the opposite of a random draw: [P309] counts 282 walls through each one in the
n = 6..8 window, so it is the most degenerate point available. If a third component can detach
at all, the neighbourhood of a record is where the structure to do it exists. The cells are
entered EXACTLY -- the simplest rational strictly inside the first solved cell on each side of
a ray, both wall families bounding it -- so the configurations are as close to the record as
the arrangement allows, and are low-height by construction.
"""
import sys, os, json, collections
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import dimension as D, wall_keys as W, wall_solve as WS
import wall_census as C, plateau_order as PO, provenance as PROV
from c_level import level_graph


def c_profile(qs):
    g = level_graph([tuple(q) for q in qs])
    return {str(l): {'V': v['V'], 'c': v['c'], 'sizes': v['sizes']} for l, v in g.items()}


def main(n=6, nrays=15):
    quats = list(W.REC[n]); q0 = quats[0]
    D.set_field(0); D.QZERO[:] = [q0]
    pt = D.point_of(quats); nc = len(pt)
    keys = [{k: c[k] for k in ('frame', 'group', 'sig', 'c0')}
            for c in WS.conditions_on(quats)]
    out = {'n': n, 'record': D.count_at(pt, len(quats)),
           'at_record': c_profile(D.quats_of(pt, q0)), 'cells': []}
    mx = max(v['c'] for v in out['at_record'].values())
    print('n=%d AT the record: max c_ell = %d over %d levels'
          % (n, mx, len(out['at_record'])), flush=True)
    best = mx
    for k in range(min(nrays, nc)):
        d = [F(0)] * nc; d[k] = F(1)
        lo, hi = PO.gated_cell(quats, pt, nc, q0, d, keys)
        for nm, a, b in (('neg', lo, F(0)), ('pos', F(0), hi)):
            s = C.simplest_in(a, b) if a < b else None
            if s is None:
                continue
            qs = D.quats_of([pt[i] + s * d[i] for i in range(nc)], q0)
            prof = c_profile(qs)
            m = max(v['c'] for v in prof.values())
            best = max(best, m)
            out['cells'].append({'ray': 'e%d' % k, 'side': nm, 'at': str(s),
                                 'max_c': m, 'profile': prof})
            if m >= 2:
                print('   e%d %s at %s: max c_ell = %d  sizes %s'
                      % (k, nm, s, m,
                         [v['sizes'] for v in prof.values() if v['c'] > 1]), flush=True)
        print('   e%d done (best so far %d)' % (k, best), flush=True)
    out['max_c_found'] = best
    out['reproduce'] = PROV.stamp(parameters={'n': n, 'nrays': nrays})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data',
                                     'c_ell_near_record_n%d.json' % n), 'w'),
              indent=1, default=str)
    print('max c_ell found anywhere in this neighbourhood: %d' % best)


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
