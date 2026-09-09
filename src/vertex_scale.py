#!/usr/bin/env python3
"""Smallest length scale in the arrangement: how close do two vertices get?

A curiosity about SCALE, answered exactly.  `c_level.level_graph` already builds
every arrangement vertex on the pairwise intersection curves and keys them by
exact rational coordinates -- it just throws the coordinates away and keeps V, E,
c.  This keeps them.

TWO DIFFERENT QUESTIONS, and they must not be conflated:

  SHORTEST EDGE   the two endpoints of one arc.  An arc borders a region, so its
                  endpoints are both vertices OF THAT REGION.  This is a genuine
                  answer to "closest two vertices of a region", and an UPPER
                  BOUND on it.

  CLOSEST PAIR    the two nearest distinct vertices anywhere on the level.  They
                  need not share a region, so this is a LOWER BOUND on the
                  same quantity.  When the two agree, the answer is pinned.

Distances are reported as EXACT SQUARED distances (rational) plus a float, because
the distance itself is a square root and the exact object is the square.  A float
here is a display convenience, never the comparison: all mins are taken on the
rationals.

Scope: this walks the level graph, whose vertices are the 0-cells lying on
two-cube intersection curves.  Arrangement vertices NOT on any such curve -- a
cube's own corner sitting free inside another cube -- are not enumerated here.
Stated so the number is not read as covering more than it does.
"""
import sys, os, json, itertools, collections
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE

def relpath(p):
    """Report paths relative to the repository, never as resolved absolutes.

    Logs and run records are quoted in documents that get published, and a
    resolved path carries the account layout of whatever machine produced it.
    The value is also just less useful to a reader: `data/x.json` locates the
    file in the repo, an absolute path locates it on one host.
    """
    try:
        return os.path.relpath(p, ROOT)
    except ValueError:
        return os.path.basename(p)

from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import strictly_inside, shares_plane

B5 = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
REC = {4: [B5[i] for i in (0,1,2,4)], 5: B5, 6: B5+[(7,14,1,-5)],
       7: B5+[(7,14,1,-5),(4,-3,-4,-4)],
       8: B5+[(7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)],
       9: B5+[(7,14,1,-5),(4,-3,-4,-4),(168,-168,168,-415),(109,-11,91,140)]}


def d2(P, Q):
    return sum((P[i]-Q[i])**2 for i in range(3))


def graph_with_coords(qs):
    """c_level.level_graph, but the node COORDINATES are kept."""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    per = collections.defaultdict(lambda: {"node": {}, "arcs": []})
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a+b)/2)*d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j)
                        and strictly_inside(mid, Ms[k]))
                g = per[s+1]
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t*d[z] for z in range(3))
                    g["node"].setdefault(P, len(g["node"]))
                    ends.append(g["node"][P])
                g["arcs"].append(tuple(ends))
    return per


def scan(qs, label):
    per = graph_with_coords(qs)
    rows = []
    for ell in sorted(per):
        g = per[ell]
        pts = list(g["node"])
        idx = {v: k for k, v in g["node"].items()}
        best_edge = best_pair = None
        for a, b in g["arcs"]:
            if a == b:
                continue
            v = d2(idx[a], idx[b])
            if v > 0 and (best_edge is None or v < best_edge[0]):
                best_edge = (v, idx[a], idx[b])
        for A, B in itertools.combinations(pts, 2):
            v = d2(A, B)
            if v > 0 and (best_pair is None or v < best_pair[0]):
                best_pair = (v, A, B)
        rows.append({'level': ell, 'V': len(pts), 'E': len(g["arcs"]),
                     'shortest_edge_sq': str(best_edge[0]) if best_edge else None,
                     'shortest_edge': float(best_edge[0])**.5 if best_edge else None,
                     'closest_pair_sq': str(best_pair[0]) if best_pair else None,
                     'closest_pair': float(best_pair[0])**.5 if best_pair else None,
                     'pinned': bool(best_edge and best_pair
                                    and best_edge[0] == best_pair[0])})
        r = rows[-1]
        print('  %-6s ell=%d  V=%-5d E=%-5d  shortest EDGE %.3e   closest PAIR %.3e%s'
              % (label, ell, r['V'], r['E'],
                 r['shortest_edge'] if r['shortest_edge'] else float('nan'),
                 r['closest_pair'] if r['closest_pair'] else float('nan'),
                 '   [pinned]' if r['pinned'] else ''), flush=True)
    return rows


def main():
    want = [int(a) for a in sys.argv[1:] if a.isdigit()] or sorted(REC)
    out = {'what': 'smallest vertex-to-vertex scale in the arrangement',
           'edge_vs_pair': ('shortest EDGE = two endpoints of one arc, so both are '
                            'vertices of the regions that arc borders -- an UPPER '
                            'bound on the closest two vertices of a region. '
                            'closest PAIR = nearest two vertices anywhere, which '
                            'need not share a region -- a LOWER bound. Equal means '
                            'pinned.'),
           'scope': ('level-graph vertices only: 0-cells on two-cube intersection '
                     'curves. A cube corner free inside another cube is not '
                     'enumerated.'),
           'exact': 'squared distances are exact rationals; floats are display only',
           'records': {}}
    p = os.path.join(ROOT, 'data', 'vertex_scale.json')
    if os.path.exists(p):                     # MERGE, never replace (FAILURE_MODES 33)
        try:
            prev = json.load(open(p))
            if isinstance(prev.get('records'), dict):
                out['records'].update(prev['records'])
        except Exception:
            pass
    for n in want:
        qs = REC[n]
        deg = shares_plane(qs)
        print('n=%d (shares_plane=%s)' % (n, deg), flush=True)
        out['records'][str(n)] = {'quats': [list(q) for q in qs],
                                  'shares_plane': bool(deg),
                                  'levels': scan(qs, 'n=%d' % n)}
        json.dump(out, open(p, 'w'), indent=1)
    print('written', relpath(p))


if __name__ == '__main__':
    main()
