#!/usr/bin/env python3
"""Where a depth-2 band's cost sits: per-triple components and depth-2 counts.  [P410]

margin = 64 - sum_S budget_S - (c2 - 1), with budget_S = E_S - V_S = d2(S) - 1 - c_S, splits as
    margin = sum_S (18 - d2(S))  +  [ sum_S (c_S - 1) - (c2 - 1) ]
             (ANCHOR slack, >= 0)     (COMPONENT slack: the band lemma says >= 0)
This prints both terms for every known band, checks the identity against the direct margin, and
names the triples whose bottom diagram is disconnected (c_S >= 2).  c from `level_s1` (exact level
graphs); d2(S) from the engine.  Output: data/band_components.json.
"""
import os, sys, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from depth2_charging import level_s1, engine_d2
from euler3 import rowsT, frames

ROOT = os.path.dirname(os.path.dirname(HERE))


def split(qs):
    qs = [tuple(q) for q in qs]
    Ms = [rowsT(R) for R in frames(qs)]
    G, EG, c2 = level_s1(Ms, [0, 1, 2, 3])
    tri = []
    for S in itertools.combinations(range(4), 3):
        dS, ES, cS = level_s1(Ms, list(S))
        tri.append({'S': S, 'd2': engine_d2([qs[k] for k in S]), 'c': cS, 'budget': ES - len(dS)})
    budget = sum(t['budget'] for t in tri)
    anchor = sum(18 - t['d2'] for t in tri)
    comp = sum(t['c'] - 1 for t in tri) - (c2 - 1)
    margin = 64 - budget - (c2 - 1)
    # identity check: budget_S = d2(S) - 1 - c_S on every triple, so margin = anchor + comp
    ok = all(t['budget'] == t['d2'] - 1 - t['c'] for t in tri) and margin == anchor + comp
    return {'qs': qs, 'c2': c2, 'd2': EG - len(G) + c2 + 1, 'margin': margin, 'anchor_slack': anchor,
            'component_slack': comp, 'identity': ok, 'triples': tri,
            'disconnected_triples': [t['S'] for t in tri if t['c'] >= 2]}


def main():
    bands = []
    for f in ('band_hunt.json', 'band_hunt_7.json'):
        bands += [h['qs'] for h in json.load(open(os.path.join(ROOT, 'data', f)))['hits']]
    bands.append([[1, 0, 0, 0], [16, 0, 1, -1], [43, 33, 3, 52], [81, 27, -32, -10]])  # P409
    out = [split(qs) for qs in bands]
    for r in out:
        print('c2 %d d2 %2d margin %2d = anchor %2d + component %d  identity %s  disconnected %s'
              % (r['c2'], r['d2'], r['margin'], r['anchor_slack'], r['component_slack'],
                 r['identity'], r['disconnected_triples']))
    json.dump(out, open(os.path.join(ROOT, 'data', 'band_components.json'), 'w'), indent=1)
    sys.exit(0 if all(r['identity'] for r in out) else 1)


if __name__ == '__main__':
    main()
