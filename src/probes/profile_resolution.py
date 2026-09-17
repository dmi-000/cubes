#!/usr/bin/env python3
"""Does (V, E, c) per level separate configurations that the DEPTH PROFILE conflates?

The depth profile `(d_1, ..., d_n)` is the project's standard structural fingerprint, and it is
known to fail at least once: the two n = 9 representatives agree on count and `by_depth` and
differ on everything else ([P285]).  Per level the arrangement also carries `V_ell`, `E_ell`,
`c_ell`, and

    d_ell = E_ell - V_ell + c_ell + 1,

so `d` is ONE linear combination of the three.  The enhanced profile is therefore strictly
richer as data; whether it is richer as a CLASSIFIER is an empirical question and this measures
it: over a sample, how many distinct depth profiles, and how many distinct enhanced profiles?

Reported as a resolution ratio and as the collisions actually broken, never as a claim that a
finer invariant is a better one -- a fingerprint that separates everything separates congruent
copies too, which is why the congruence control below matters.
"""
import sys, os, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from c_level import level_graph, shares_plane, engine
import provenance as PROV


def profiles(qs):
    g = level_graph(qs)
    by = engine(qs).get('by_depth') or {}
    n = len(qs)
    depth = tuple(by.get(str(m), 0) for m in range(1, n + 1))
    enh = tuple((g[l]['V'], g[l]['E'], g[l]['c']) for l in sorted(g))
    return depth, enh


def main(trials=260, seed=17):
    rng = random.Random(seed)
    rows, seen = [], 0
    d_map = collections.defaultdict(list)
    for _ in range(trials):
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-18, 18) for _ in range(4))
                               for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            d, e = profiles(qs)
        except Exception:
            continue
        seen += 1
        d_map[d].append((e, qs))
        rows.append({'quats': [list(q) for q in qs], 'depth': list(d),
                     'enhanced': [list(x) for x in e]})
    nd = len(d_map)
    ne = len({(d, e) for d, v in d_map.items() for e, _ in v})
    coll = {d: v for d, v in d_map.items() if len(v) > 1}
    broken = 0
    examples = []
    for d, v in coll.items():
        if len({e for e, _ in v}) > 1:
            broken += 1
            if len(examples) < 3:
                examples.append({'depth': list(d),
                                 'enhanced_variants': [list(map(list, e))
                                                       for e in {e for e, _ in v}][:3]})
    print('configurations %d | distinct depth profiles %d | distinct enhanced %d'
          % (seen, nd, ne), flush=True)
    print('depth-profile collisions %d | of those SPLIT by (V,E,c) %d'
          % (len(coll), broken), flush=True)

    # CONTROL: a relabelling of the same cubes must give identical profiles both ways.
    qs = [(1, 0, 0, 0), (3, 1, 4, 1), (5, 9, 2, 6), (5, 3, 5, 8)]
    a = profiles(qs)
    b = profiles([qs[0]] + [qs[3], qs[1], qs[2]])
    print('control (relabelled cubes): depth same %s | enhanced same %s'
          % (a[0] == b[0], a[1] == b[1]), flush=True)

    out = {'what': 'resolution of the depth profile vs (V,E,c) per level',
           'configurations': seen, 'distinct_depth_profiles': nd,
           'distinct_enhanced_profiles': ne,
           'depth_collisions': len(coll), 'collisions_split_by_enhanced': broken,
           'examples': examples,
           'control_relabelling': {'depth_invariant': a[0] == b[0],
                                   'enhanced_invariant': a[1] == b[1]},
           'rows': rows[:60]}
    out['reproduce'] = PROV.stamp(parameters={'trials': trials, 'seed': seed})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data',
                                     'profile_resolution.json'), 'w'), indent=1, default=str)
    print('written data/profile_resolution.json')


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 260)
