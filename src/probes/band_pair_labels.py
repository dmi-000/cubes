#!/usr/bin/env python3
"""NULL RESULT, superseded by band_faces.py: a side-label test cannot identify the band pair.  [P410]

In all 8 bands every one of the six labels borders both components of Γ, so the intersection
below is all six pairs and "agree" is False for lack of identification, not from a disagreement.
Kept as the record of why the face trace was needed.  The original intent follows.

Identify each band's pair from Γ's own side labels, independently of the triples.

An arc of Γ lies on dA_i n dA_j with exactly one cube k strictly containing it, so the regions on
its two sides are labelled {k,i} and {k,j}.  A band region borders both components of Γ (c2 = 2),
so its label appears beside arcs of both.  PROOF_BAND G1 + G4 predict that the triples that gain a
component are the two containing the band pair.  Here the band pair is read from Γ and compared
with the triples' c_S.  Output: data/band_pair_labels.json.
"""
import os, sys, json, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from depth2_charging import level_s1

ROOT = os.path.dirname(os.path.dirname(HERE))


def gamma_labelled(Ms):
    """arcs of Γ with their two side labels; components by union-find on endpoints."""
    node, arcs = {}, []
    idx = range(4)
    for i, j in itertools.combinations(idx, 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in idx if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                ins = [k for k in idx if k not in (i, j) and CL.strictly_inside(mid, Ms[k])]
                if len(ins) != 1:
                    continue
                k = ins[0]
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    node.setdefault(P, len(node)); ends.append(node[P])
                arcs.append((ends, frozenset((k, i)), frozenset((k, j))))
    par = list(range(len(node)))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for (u, v), _, _ in arcs:
        par[f(u)] = f(v)
    comp = collections.defaultdict(set)
    for (u, v), l1, l2 in arcs:
        comp[f(u)] |= {l1, l2}
    return list(comp.values())


def main():
    rows = json.load(open(os.path.join(ROOT, 'data', 'band_components.json')))
    out, agree = [], 0
    for r in rows:
        Ms = [rowsT(R) for R in frames([tuple(q) for q in r['qs']])]
        comps = gamma_labelled(Ms)
        common = set.intersection(*comps) if len(comps) >= 2 else set()
        disc = [tuple(S) for S in r['disconnected_triples']]
        shared = set.intersection(*[set(S) for S in disc]) if disc else set()
        cand = [tuple(sorted(P)) for P in common]
        ok = len(cand) == 1 and set(cand[0]) == shared
        agree += ok
        print('c2 %d  labels bordering every component: %s   pair shared by disconnected triples: %s  %s'
              % (len(comps), sorted(cand), tuple(sorted(shared)), 'AGREE' if ok else 'DIFFER'))
        out.append({'qs': r['qs'], 'components': len(comps), 'common_labels': sorted(cand),
                    'triple_pair': sorted(shared), 'agree': ok})
    print('%d of %d agree' % (agree, len(rows)))
    json.dump(out, open(os.path.join(ROOT, 'data', 'band_pair_labels.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
