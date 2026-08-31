#!/usr/bin/env python3
"""Does a record's tangent arrangement FACTOR? — the n=3 anomaly, generalised.

P169: both n=3 maximisers decompose completely (octahedral boolean, golden a
product of three rank-2 blocks) and both have deficit 0, while 727 has 8 coupling
walls and deficit 1. That suggests one arrangement-level fact behind all three of
n=3's anomalies. This tests where decomposability breaks.

TEST. An arrangement is a product iff its hyperplanes partition into blocks whose
SPANS ARE INDEPENDENT. Start with one block per hyperplane and merge any two whose
spans meet nontrivially; the arrangement factors iff the resulting block ranks sum
to the arrangement's rank. Merging is by span intersection, so the result is the
finest such partition and the test is exact, not a heuristic.
"""
import sys
sys.path.insert(0, '.')
from zaslavsky import Flats


def _rank(L, idxs):
    b = []
    for i in idxs:
        L._add(b, L.w[i])
    return len(b)


def blocks(walls):
    L = Flats(walls)
    m = len(walls)
    # MERGE RULE. Two distinct normals always span a 2-space, so "spans
    # intersect" never fires and the first version of this returned all
    # singletons -- including for the golden 67, whose three rank-2 blocks were
    # verified directly in P169. Elements are connected through a CIRCUIT, so the
    # rule is: merge blocks A and B when some normal OUTSIDE them lies in
    # span(A u B). Three coplanar hyperplanes then merge, independent ones do not.
    part = [[i] for i in range(m)]
    changed = True
    while changed:
        changed = False
        for a in range(len(part)):
            for b in range(a + 1, len(part)):
                un = part[a] + part[b]
                r = _rank(L, un)
                base = []
                for i in un:
                    L._add(base, L.w[i])
                pulled = any(not any(L._reduce(base, L.w[k]))
                             for k in range(m) if k not in un)
                if pulled or r < _rank(L, part[a]) + _rank(L, part[b]):
                    part[a] = un
                    part.pop(b)
                    changed = True
                    break
            if changed:
                break
    return L, part, _rank(L, range(m))


def report(name, walls, ncols, log=sys.stdout):
    seen, H = set(), []
    for w in walls:
        piv = next((x for x in w if x != 0), None)
        if piv is None:
            continue
        k = tuple(str(x / piv) for x in w)
        if k not in seen:
            seen.add(k)
            H.append([x / piv for x in w])
    L, part, r = blocks(H)
    ranks = [_rank(L, p) for p in part]
    factors = (sum(ranks) == r)
    print('%-12s hyperplanes %3d  ambient %2d  rank %2d  deficit %d  blocks %2d %s'
          % (name, len(H), ncols, r, ncols - r, len(part),
             'sizes ' + str(sorted(len(p) for p in part))), file=log, flush=True)
    print('              block ranks %s sum %d vs rank %d  ->  %s'
          % (sorted(ranks), sum(ranks), r,
             'FACTORS COMPLETELY' if factors and len(part) > 1 else
             ('irreducible (single block)' if len(part) == 1 else 'does not factor')),
          file=log, flush=True)
    return len(H), r, ncols - r, len(part), factors
