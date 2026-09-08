#!/usr/bin/env python3
"""Does the count buy its rarity with CONSTRAINTS? — dimension against count.

The hope, stated by the user: find an indicator of a count's rarity that varies with the
count, and see whether it runs out not far above the record. Search yields lower bounds
forever; an indicator that hits a wall would be an UPPER-bound argument, which is the
thing this project cannot get from searching.

The candidate indicator here is the one the geometry actually charges: the DIMENSION of
the set carrying the count. A generic configuration has no tight conditions and its
chamber is full-dimensional (9 at n=4). Every record so far sits on a stratum of high
codimension -- 183 is 0-dimensional ([P204]), 2787 has rank 4 in ambient 24. So the
count is bought with constraints, and the question is the exchange rate: d(c).

If d falls to 0 at some c*, then above c* a maximiser would need negative dimension --
the conditions are over-determined and no configuration can satisfy them. c* is then an
upper bound on the count, derived rather than searched. Whether d(c) is even a function
is part of what this measures: if configurations with the same count have different
dimensions, the indicator is not well defined and the argument does not start.

TWO MEASURES, because they are not the same and the project has been burned by
conflating them (FAILURE_MODES 13):
  nullity   dimension of the null space of the TIGHT wall gradients. Cheap, and an
            UPPER bound on the region's dimension -- it can report a direction that
            does not actually preserve the count.
  rank      the eps-verified preserving directions, count_eps in Q(sqrt d)(eps). The
            real tangent space, and the honest number. Costs 2 eps-counts per
            direction.
Both are reported. Where they differ, the nullity is the optimistic one.
"""
import json, glob, sys, collections
from fractions import Fraction as F
sys.path.insert(0, '.')
import sympy as sp
import climb as C
import dimension as D
from eps_null import walls_and_null
from qfield import Q
from epscount import count_eps
from lll import lll

def measure(cfg):
    """(count, #tight walls, nullity, eps-verified preserving rank, ambient)"""
    pt, walls, null, ncols = walls_and_null(cfg)
    rec = D.count_at(pt, len(cfg))
    if not null:
        return rec, len(walls), 0, 0, ncols
    B = [C.prim(b) for b in lll([list(C.prim(v)) for v in null])]
    good = []
    for b in B:
        ok = True
        for sgn in (1, -1):
            c = count_eps(pt, [Q(sgn * F(x), 0, 0) for x in b], 0, cfg[0])
            if c is None:
                c = count_eps(pt, [Q(sgn * F(x), 0, 0) for x in b], 0, cfg[0], wide=True)
            if c != rec:
                ok = False; break
        if ok:
            good.append(b)
    r = sp.Matrix([list(g) for g in good]).rank() if good else 0
    return rec, len(walls), len(null), r, ncols

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    # one configuration per distinct terminal count, from the basin campaign
    by = {}
    for f in glob.glob('basin_n*_d*_s*.jsonl'):
        for l in open(f):
            d = json.loads(l)
            if len(d['cfg0']) != n:
                continue
            c = d.get('end') if d.get('end') is not None else d.get('best_evaluable')
            if c is None:
                continue
            by.setdefault(c, []).append([tuple(q) for q in d['cfg1']])
    print('n=%d: %d distinct terminal counts from %d climbs'
          % (n, len(by), sum(len(v) for v in by.values())), flush=True)
    print('%8s %8s %9s %9s %8s   %s' % ('count', 'tight', 'nullity', 'rank', 'ambient', 'configs'))
    rows = []
    for c in sorted(by):
        for cfg in by[c][:2]:            # two per count: is the dimension even a function of it?
            try:
                rec, w, nl, r, nc = measure(cfg)
            except Exception as e:
                print('%8d   FAILED %s' % (c, str(e)[:50]), flush=True); continue
            print('%8d %8d %9d %9d %8d' % (rec, w, nl, r, nc), flush=True)
            rows.append((rec, w, nl, r, nc))
    json.dump(rows, open('rarity_n%d.json' % n, 'w'))
    print('\nwrote rarity_n%d.json' % n)
