#!/usr/bin/env python3
"""ANCHOR, strengthened form, checked on degenerate and generic compounds.  [P416]

ANCHOR (max2_report Theorem 1; soft step tightened in P416): every component of
S_C = {C strictly innermost} contains a face direction of C that lies IN S_C.  Consequence tested:
    #pi0(S_C)  <=  #{face directions n of C with M_i(n) < 1 for every other cube i}.
The face-direction count drops when C shares a face plane (P413's d3 <= 20 and d2(S) <= 14 rest on
exactly this), so the shared-plane compounds are the hard controls.  Compounds: tiebreak_scan's 48
shared-plane ones, the 183 record, the golden-free n = 2 13-pair at n = 2, and their triples.
Output: data/anchor_check.json.
"""
import os, sys, json, itertools, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
from sphere_count import Compound, dot

ROOT = os.path.dirname(os.path.dirname(HERE))


def check(qs):
    rows = []
    for sub in [tuple(range(len(qs)))] + list(itertools.combinations(range(len(qs)), 3)) if len(qs) == 4 else [tuple(range(len(qs)))]:
        C = Compound([tuple(qs[i]) for i in sub], 'Q')
        for c in range(C.n):
            others = [i for i in range(C.n) if i != c]
            comps = C.components(C.beat_pieces(others, [c]))
            anchors = sum(1 for n in C.fc[c]
                          if all(max(abs(dot(f, n)) for f in C.fc[i]) < 1 for i in others))
            # must-fail control: only the three POSITIVE normals counted as anchors
            half = sum(1 for n in C.fc[c][0::2]
                       if all(max(abs(dot(f, n)) for f in C.fc[i]) < 1 for i in others))
            rows.append({'sub': sub, 'cube': c, 'components': comps, 'anchors': anchors, 'control': half})
    return {'qs': qs, 'rows': rows, 'violations': sum(r['components'] > r['anchors'] for r in rows),
            'reduced': sum(r['anchors'] < 6 for r in rows)}


def main():
    cases = [r['qs'] for r in json.load(open(os.path.join(ROOT, 'data', 'tiebreak_scan.json')))]
    cases += [[(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)],
              [(1, 0, 0, 0), (3, 1, 1, 1)], [(1, 0, 0, 0), (3, 0, 0, 1)]]
    with mp.Pool(8) as p:
        out = p.map(check, cases)
    n = sum(len(o['rows']) for o in out)
    v = sum(o['violations'] for o in out)
    red = sum(o['reduced'] for o in out)
    tight = sum(1 for o in out for r in o['rows'] if r['components'] == r['anchors'])
    cv = sum(1 for o in out for r in o['rows'] if r['components'] > r['control'])
    print('control (positive normals only): %d violations, %s' % (cv, 'fails as it must' if cv else 'VACUOUS'))
    print('%d (sub-compound, cube) instances over %d compounds; %d with fewer than 6 anchors (shared planes); '
          '%d violations; %d tight' % (n, len(out), red, v, tight))
    json.dump(out, open(os.path.join(ROOT, 'data', 'anchor_check.json'), 'w'), indent=1, default=str)
    sys.exit(1 if v or not cv else 0)


if __name__ == '__main__':
    main()
