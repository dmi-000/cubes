#!/usr/bin/env python3
"""Are the records' plane concurrences ON the compound?  [P331].

THE QUESTION THIS ANSWERS.  [P322]/[P323] found `concurrency_walls.py` counting four-plane
meeting points with no containment predicate -- a cube is bounded by six SQUARES, and most
four-plane meeting points are nowhere near the solid.  The follow-up asked by the user is
whether any OTHER live claim rests on the same defect.  `concurrence.py` has no containment
test either, and [RESULTS §7] still cites it for "723 does carry two 9-folds, so
ALGEBRAIC_SEARCH.md's premise stands".

THE ANSWER: not one top-multiplicity point in 183, 723 or 727 lies on the compound.  723's
9-fold is three cubes SHARING A CORNER -- real, structural, and sticking out 63 % past the
other three cubes, so it is not an arrangement vertex and buys no regions.

This probe does NOT import `concurrence` at module scope by accident: that module is safe
(it guards its work under __main__), but several probes in this tree are not, and importing
one of those rewrites its data file -- see [INTERVENTIONS A15].
"""
import sys, os, json, itertools, collections
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from concurrence import planes, solve3
import provenance as PROV

CFG = {'183': [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)],
       '723': [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1),
               (5, 2, 2, 2)],
       '727': [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1),
               (7, 14, 1, -5)]}


def frames(cfg):
    """(face normals as ROWS, offset) per cube -- the normals are the COLUMNS of the rotation
    matrix, which is [P227]'s correction and is preserved here deliberately."""
    out = []
    for (w, x, y, z) in cfg:
        n = w * w + x * x + y * y + z * z
        M = [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
             [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
             [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]
        out.append(([[M[r][c] for r in range(3)] for c in range(3)], n))
    return out


def multiplicities(cfg):
    P = planes(cfg)
    pts = collections.Counter()
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is not None:
            pts[s] += 1
    mult = {}
    for s, c in pts.items():
        m = 3
        while m * (m - 1) * (m - 2) // 6 < c:
            m += 1
        mult[s] = m
    return mult


def classify(cfg, P):
    """per cube: how many of its face planes the point lies on, and whether it is outside."""
    rows = []
    for idx, (C, n) in enumerate(frames(cfg)):
        h = [F(abs(sum(C[c][k] * P[k] for k in range(3))), n) for c in range(3)]
        rows.append({'cube': idx, 'ratios': [str(v) for v in h],
                     'on_planes': sum(1 for v in h if v == 1),
                     'outside': max(h) > 1})
    return rows


def main():
    out = {'what': 'do the records\' maximal plane concurrences lie ON the compound?',
           'supports': 'LEDGER P331', 'configs': {}}
    for lbl, cfg in CFG.items():
        mult = multiplicities(cfg)
        mx = max(mult.values())
        tops = [s for s, m in mult.items() if m == mx]
        inside = 0
        detail = []
        for s in tops:
            rows = classify(cfg, s)
            ok = not any(r['outside'] for r in rows)
            inside += 1 if ok else 0
            worst = max(max(F(x) for x in r['ratios']) for r in rows)
            detail.append({'point': [str(v) for v in s], 'on_compound': ok,
                           'worst_ratio': str(worst), 'per_cube': rows})
        out['configs'][lbl] = {'max_concurrence': mx, 'points': len(tops),
                               'on_compound': inside, 'detail': detail}
        print('%-5s max plane-concurrence %d at %2d point(s);  ON THE COMPOUND: %d   worst ratio %s'
              % (lbl, mx, len(tops), inside,
                 max(d['worst_ratio'] for d in detail)))
        if lbl == '723':
            print('   the 9-fold at (1,1,1), cube by cube:')
            for r in detail[0]['per_cube']:
                print('      cube %d  ratios %-26s on %d planes%s'
                      % (r['cube'], ','.join(r['ratios']), r['on_planes'],
                         '   OUTSIDE' if r['outside'] else '   <- shares this CORNER'))
    out['reproduce'] = PROV.stamp(parameters={'configs': sorted(CFG)})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data',
                                     'concurrence_containment.json'), 'w'), indent=1, default=str)
    print('\nwritten data/concurrence_containment.json')


if __name__ == '__main__':
    main()
