#!/usr/bin/env python3
"""Does the `c = 2` shape match [P312]'s explanation?  A falsifiable prediction.

[P312]: a wall-graph face is a connected component of the depth-exactly-m set on ONE cube's
boundary `∂A_i` -- the arcs separate faces only where the cube index changes, and creases are
folds, not separators.  Euler on the sphere gives `c - 1 = sum_f (b(f) - 1)`, so `c = 2` means
exactly one face with two boundary circles, and the two graph components ARE those two circles.

THE PREDICTION, which can fail: both components consist entirely of arcs that involve one
COMMON cube `i` -- the cube whose boundary carries the annular face.  If some arc of one
component involves only cubes disjoint from the other component's, the explanation is wrong.

The antipodal half is already known ([P268]: `c = 2` is always an antipodal image pair) and is
re-checked here rather than assumed, since [P312] needs the annular face to be self-antipodal.
"""
import sys, os, json, itertools, collections, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import shares_plane, strictly_inside
import provenance as PROV


def labelled_level_graph(qs):
    """The wall graph, keeping each arc's cube PAIR and each node's coordinates."""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    per = collections.defaultdict(lambda: {'node': {}, 'arcs': []})
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j)
                        and strictly_inside(mid, Ms[k]))
                g = per[s + 1]
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    g['node'].setdefault(P, len(g['node']))
                    ends.append(g['node'][P])
                g['arcs'].append((tuple(ends), (i, j)))
    return per


def components(g):
    par = list(range(len(g['node'])))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for (a, b), _ in g['arcs']:
        par[f(a)] = f(b)
    comp = collections.defaultdict(lambda: {'nodes': set(), 'cubes': collections.Counter(),
                                            'every_arc': None})
    for (a, b), pr in g['arcs']:
        r = f(a)
        comp[r]['nodes'].update((a, b))
        comp[r]['cubes'].update(pr)
        # THE CUBES PRESENT IN *EVERY* ARC of the component.  Counting the cubes that appear
        # in SOME arc, which the first version of this file did, is vacuous: every component
        # meets every cube, so the intersection was always the full set and the test could
        # not fail -- FAILURE_MODES 2, self-inflicted.
        e = comp[r]['every_arc']
        comp[r]['every_arc'] = set(pr) if e is None else (e & set(pr))
    return comp, f


def main(trials=600, seed=11):
    rng = random.Random(seed)
    out = {'what': "[P312]'s explanation of c = 2, as a falsifiable prediction",
           'prediction': ('both components of a c = 2 level share a COMMON cube index in '
                          'every arc -- the cube whose boundary carries the annular face'),
           'instances': []}
    ok = fail = 0
    for _ in range(trials):
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-25, 25) for _ in range(4))
                               for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            per = labelled_level_graph(qs)
        except Exception:
            continue
        for ell, g in per.items():
            comp, f = components(g)
            if len(comp) != 2:
                continue
            (r1, c1), (r2, c2) = list(comp.items())
            common = (c1['every_arc'] or set()) & (c2['every_arc'] or set())
            inv = {tuple(-x for x in P) for P in g['node']}
            selfanti = len(inv & set(g['node'])) == len(g['node'])
            n1 = {P for P, k in g['node'].items() if f(k) == r1}
            n2 = {P for P, k in g['node'].items() if f(k) == r2}
            swap = {tuple(-x for x in P) for P in n1} == n2
            good = bool(common)
            ok += good; fail += (not good)
            out['instances'].append({
                'quats': [list(q) for q in qs], 'level': ell,
                'component_sizes': [len(c1['nodes']), len(c2['nodes'])],
                'cube_in_every_arc_comp1': sorted(c1['every_arc'] or []),
                'cube_in_every_arc_comp2': sorted(c2['every_arc'] or []),
                'common_cubes': sorted(common),
                'graph_is_centrally_symmetric': selfanti,
                'components_are_antipodal_images': swap,
                'prediction_holds': good})
            print('level %s sizes %s | in-every-arc %s / %s | COMMON %s | antipodal pair %s -> %s'
                  % (ell, [len(c1['nodes']), len(c2['nodes'])],
                     sorted(c1['every_arc'] or []), sorted(c2['every_arc'] or []),
                     sorted(common), swap,
                     'holds' if good else 'FAILS'), flush=True)
    out['n_holds'], out['n_fails'] = ok, fail
    out['reproduce'] = PROV.stamp(parameters={'trials': trials, 'seed': seed})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'c2_face_test.json'), 'w'),
              indent=1, default=str)
    print('prediction holds %d, fails %d' % (ok, fail))


if __name__ == '__main__':
    main()
