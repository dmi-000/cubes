#!/usr/bin/env python3
"""Hunt for a depth-2 BAND (c2 >= 2) at n = 4, targeted at the shape that would make one.  [P408]

[P404]/[P405]: max(4) <= 195 iff (beyond the scope) c2 = 1, i.e. no depth-2 cell is an annulus.
A symmetric band needs one pair innermost all round an equator and another pair innermost at the
poles.  Level-1 bands (c1 = 2) DO occur ([P269]) and are the POSITIVE CONTROL: the tool must find
them.  Targeted families: i, j with a body diagonal near the pole axis (their corner rings reach
far round the equator), k near the identity and l a small tilt of it, all perturbed at random; plus
random compounds.  c at every level from `c_level.level_graph` (gated), shared face planes excluded.
"""
import os, sys, itertools, random, collections, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import qmul

ROOT = os.path.dirname(os.path.dirname(HERE))
DIAG = (11, 4, -4, 0)          # maps the body diagonal (1,1,1) close to the z axis


def family(rnd):
    rz = lambda: (rnd.randint(3, 12), 0, 0, rnd.randint(-6, 6))
    jit = lambda s: tuple(x + rnd.randint(-s, s) for x in (0, 0, 0, 0))
    i = qmul(rz(), DIAG); j = qmul(rz(), DIAG)
    i = tuple(a + b for a, b in zip(i, jit(2))); j = tuple(a + b for a, b in zip(j, jit(2)))
    l = (rnd.randint(6, 20), rnd.randint(-2, 2), rnd.randint(-2, 2), rnd.randint(-2, 2))
    return [(1, 0, 0, 0), l, i, j]


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    rnd = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 20261004)
    st = collections.Counter(); hits = []
    for it in range(N):
        if it % 2:
            qs = family(rnd)
            kind = 'targeted'
        else:
            qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-7, 7) for _ in range(4)) for _ in range(3)]
            kind = 'random'
        if any(not any(q) for q in qs) or CL.shares_plane(qs):
            st['excluded'] += 1
            continue
        try:
            lv = CL.level_graph(qs)
        except Exception:
            st['unevaluated'] += 1
            continue
        st[kind] += 1
        for ell, g in lv.items():
            st['c%d=%d' % (ell, g['c'])] += 1
        if lv.get(2, {}).get('c', 1) >= 2:
            hits.append({'qs': qs, 'kind': kind, 'levels': {k: v['c'] for k, v in lv.items()}})
            print('LEVEL-2 BAND', hits[-1], flush=True)
    print(dict(sorted(st.items())))
    print('level-1 c >= 2 (positive control): %d   level-2 c >= 2: %d'
          % (sum(v for k, v in st.items() if k.startswith('c1=') and k != 'c1=1'), len(hits)))
    json.dump({'stats': dict(st), 'hits': hits}, open(os.path.join(ROOT, 'data', 'band_hunt%s.json' % ('' if len(sys.argv) < 3 else '_' + sys.argv[2])), 'w'), indent=1)


if __name__ == '__main__':
    if not CL.gate():
        sys.exit('GATE FAILED')
    main()
