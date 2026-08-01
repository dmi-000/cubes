#!/usr/bin/env python3
# Working principles: certify_six.py (exact_count_config) + CPP_SPEC.md.
"""Region ADJACENCY graph for cube compounds, on top of certify_six's
exact counting engine.

certify_six.exact_count_config() already computes, for every pair of
touching arrangement fragments, whether the shared wall is PHANTOM
(same face plane, but outside the actual bounded face square of every
cube that owns the plane -> the two fragments are the same region) or
REAL (inside at least one owning cube's face square -> the two
fragments are genuinely different regions, separated by a real facet
of the compound). The phantom case drives a union-find merge; the real
case was previously just asserted-and-discarded. This module keeps the
real touches instead of discarding them: they are exactly the
adjacency edges between the regions exact_count_config already counts.

certify_six.py is NOT modified. Its algorithm is reproduced here
line-for-line up through the facet loop (see exact_count_config for the
canonical, validated version); this file adds bookkeeping around the
same loop rather than monkeypatching a closure-heavy function. Any
future fix to the validated engine's clip/label/merge logic must be
mirrored here by hand -- there is no code sharing at that level, only
shared imports of the exact-arithmetic primitives (CN, clip, dot, ...).

STRUCTURAL GATE (see report): crossing a real face changes the
containment set by exactly one cube, the cube that face belongs to.
So every adjacency edge must join two regions whose labels (bitmasks
of containing cubes) differ in exactly one bit. This is asserted for
EVERY edge as it is discovered -- not filtered after the fact -- so a
violation aborts the computation rather than silently producing a
plausible-looking but wrong graph.
"""
from itertools import product

from cube_compound_exact import Q5, ZERO, ONE
from cube_compound_interval import CN, clip, dot, vadd, vscale, STATS


def region_adjacency(rots, verbose=False):
    """Exact region graph for cubes R_k([-1,1]^3), R_k rational rotations.

    Returns a dict:
      total       -- bounded region count (excludes the outside region;
                      agrees with exact_count_config's `total`)
      by_depth    -- {depth: count}, INCLUDES the outside depth-0 entry
                      (count 1), same convention as exact_count_config's
                      raw by_depth (headline reports usually drop it)
      per_label   -- {bitmask: count}, includes label 0 (outside);
                      agrees with exact_count_config's per_label
      region_label-- {region_id: bitmask} for every merged region,
                      INCLUDING the outside region
      outside_rid -- the region_id of the outside (label 0) region
      edges       -- sorted list of (rid_u, rid_v), rid_u < rid_v; the
                      SIMPLE adjacency graph (one edge per adjacent
                      region pair, regardless of how many real-facet
                      fragments realize it)
      edge_facet_count -- {(rid_u, rid_v): n} how many real-facet
                      fragments were merged into that one edge (>1 is
                      normal: two regions can share several coplanar or
                      non-coplanar real facet pieces)
      adjacency   -- {region_id: sorted [neighbor region_id, ...]}
      profile     -- canonical comparable invariant, see build below
    """
    for k in STATS:
        STATS[k] = 0
    one = CN.leaf(ONE)
    cubes = []
    for R in rots:
        cols = [tuple(CN.leaf(R.m[i][j]) for i in range(3)) for j in range(3)]
        cubes.append(cols)
    nq = len(cubes)

    planes = [(k, j, c) for k in range(nq) for j in range(3) for c in (1, -1)]

    # See certify_six.exact_count_config's INVARIANT comment: coincident
    # planes carry the facets of ALL their owning cubes; reproduced
    # verbatim here.
    def plane_key(k, j, c):
        comps = [x.exact() for x in cubes[k][j]]
        s = 0
        for x in comps:
            s = x.sign()
            if s != 0:
                break
        if s < 0:
            comps = [-x for x in comps]
            c = -c
        return (tuple((x.a, x.b) for x in comps), c)

    classes = {}
    for k, j, c in planes:
        classes.setdefault(plane_key(k, j, c), []).append((k, j))
    owners_of = [classes[plane_key(k, j, c)] for (k, j, c) in planes]

    B, nB = CN.leaf(Q5(4)), CN.leaf(Q5(-4))
    corners = list(product((B, nB), repeat=3))

    def box_face(fix_axis, val):
        pts = [c for c in corners if c[fix_axis] is val]
        a, b = [i for i in range(3) if i != fix_axis]
        pts.sort(key=lambda p: (p[a].iv[0], p[b].iv[0]))
        p00, p01, p10, p11 = pts
        return [p00, p01, p11, p10]

    cells = [[(('box', i, s), box_face(i, v))
              for i in range(3) for s, v in ((1, B), (-1, nB))]]

    for pid, (k, j, c) in enumerate(planes):
        n = cubes[k][j]
        cq = one if c == 1 else -one
        f = lambda p, n=n, cq=cq: dot(n, p) - cq
        cache = {}
        nxt = []
        for cell in cells:
            neg, pos = clip(cell, f, cache)
            for half in (neg, pos):
                if half is not None:
                    nxt.append([(pid if q == 'cap' else q, loop)
                                for q, loop in half])
        cells = nxt
    if verbose:
        print(f'exact: arrangement cells = {len(cells)}')

    def centroid_pts(pts):
        from fractions import Fraction as Fr
        kk = CN.leaf(Q5(Fr(1, len(pts))))
        s = (CN.leaf(ZERO),) * 3
        for p in pts:
            s = vadd(s, p)
        return vscale(s, kk)

    def label(w):
        lab = 0
        for k in range(nq):
            if all((dot(cubes[k][j], w) - one).sign() < 0 and
                   (dot(cubes[k][j], w) + one).sign() > 0 for j in range(3)):
                lab |= 1 << k
        return lab

    labs = [label(centroid_pts(list({p for _, loop in c for p in loop})))
            for c in cells]

    groups = {}
    for ci, cell in enumerate(cells):
        for pid, loop in cell:
            if isinstance(pid, tuple):
                continue
            groups.setdefault((pid, frozenset(loop)), []).append(ci)

    parent = list(range(len(cells)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    real_facets = []  # (cell_a, cell_b) pairs joined by a REAL facet
    for (pid, verts), cs in groups.items():
        assert len(cs) == 2, f'facet shared by {len(cs)} cells'
        a, b = cs
        w = centroid_pts(list(verts))
        flip = 0
        for kk, jj in owners_of[pid]:
            others = [cubes[kk][t] for t in range(3) if t != jj]
            if all((dot(n, w) - one).sign() < 0 and
                   (dot(n, w) + one).sign() > 0 for n in others):
                flip |= 1 << kk
        if flip:
            assert labs[a] ^ labs[b] == flip, 'real facet flip mismatch'
            real_facets.append((a, b))
        else:
            assert labs[a] == labs[b], 'phantom facet with differing labels'
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

    # --- everything above is certify_six.exact_count_config, verbatim
    # up to the point where it discards the real-facet information.
    # From here: build the merged-region graph. -------------------------

    comps = set()
    for ci in range(len(cells)):
        comps.add((labs[ci], find(ci)))
    per_label = {}
    for lab, _r in comps:
        per_label[lab] = per_label.get(lab, 0) + 1
    assert per_label.get(0, 0) == 1, 'outside must be a single region'
    by_depth = {}
    for lab, cnt in per_label.items():
        d = bin(lab).count('1')
        by_depth[d] = by_depth.get(d, 0) + cnt
    total = sum(per_label.values()) - 1

    root_of_cell = [find(ci) for ci in range(len(cells))]
    roots = sorted(set(root_of_cell))
    region_id = {r: i for i, r in enumerate(roots)}
    region_label = {}
    for ci, r in enumerate(root_of_cell):
        rid = region_id[r]
        if rid in region_label:
            assert region_label[rid] == labs[ci], \
                'label mismatch within a merged (phantom-joined) region'
        else:
            region_label[rid] = labs[ci]
    assert len(region_label) == total + 1, \
        'region count mismatch between union-find and per_label'

    outside_candidates = [rid for rid, lab in region_label.items() if lab == 0]
    assert len(outside_candidates) == 1
    outside_rid = outside_candidates[0]

    edge_facet_count = {}
    for a, b in real_facets:
        ra, rb = region_id[root_of_cell[a]], region_id[root_of_cell[b]]
        assert ra != rb, \
            'real-facet endpoints ended up phantom-merged into one region'
        la, lb = region_label[ra], region_label[rb]
        diff_bits = bin(la ^ lb).count('1')
        # THE STRUCTURAL GATE. Do not filter violations out -- abort.
        assert diff_bits == 1, (
            f'adjacency gate violated: regions {ra} (label {la:#x}) and '
            f'{rb} (label {lb:#x}) share a real facet but differ in '
            f'{diff_bits} bits, not 1 -- phantom/real classification is '
            f'wrong')
        e = (ra, rb) if ra < rb else (rb, ra)
        edge_facet_count[e] = edge_facet_count.get(e, 0) + 1

    edges = sorted(edge_facet_count)
    adjacency = {}
    for ra, rb in edges:
        adjacency.setdefault(ra, set()).add(rb)
        adjacency.setdefault(rb, set()).add(ra)
    adjacency = {k: sorted(v) for k, v in adjacency.items()}

    edges_labeled = []
    for ra, rb in edges:
        la, lb = region_label[ra], region_label[rb]
        edges_labeled.append((la, lb) if la <= lb else (lb, la))
    edges_labeled.sort()

    profile = {
        'per_label': tuple(sorted(per_label.items())),
        'edges': tuple(edges_labeled),
    }

    return {
        'total': total,
        'by_depth': by_depth,
        'per_label': per_label,
        'region_label': region_label,
        'outside_rid': outside_rid,
        'edges': edges,
        'edge_facet_count': edge_facet_count,
        'adjacency': adjacency,
        'profile': profile,
    }


def profile_key(result):
    """Hashable canonical fingerprint for `result['profile']`."""
    return (result['profile']['per_label'], result['profile']['edges'])


if __name__ == '__main__':
    import sys
    import time
    from golden_rotations import rot_from_quat

    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__)
        raise SystemExit(0)

    print('=== n=2 gate: quaternions (1,0,0,0), (0,1,1,1) ===')
    rots = [rot_from_quat(1, 0, 0, 0), rot_from_quat(0, 1, 1, 1)]
    t0 = time.time()
    res = region_adjacency(rots, verbose=True)
    dt = time.time() - t0
    print(f'total={res["total"]}  by_depth={dict(sorted(res["by_depth"].items()))}'
          f'  ({dt:.2f}s)')
    print(f'per_label={res["per_label"]}')
    print(f'region_label={res["region_label"]}  outside_rid={res["outside_rid"]}')
    print(f'edges (rid pairs)={res["edges"]}')
    print(f'edge_facet_count={res["edge_facet_count"]}')
    deg_sum = sum(len(v) for v in res['adjacency'].values())
    print(f'sum(degree)={deg_sum}  2*|E|={2 * len(res["edges"])}  '
          f'match={deg_sum == 2 * len(res["edges"])}')
    for rid in sorted(res['region_label']):
        lab = res['region_label'][rid]
        nbrs = res['adjacency'].get(rid, [])
        nbr_labs = [res['region_label'][n] for n in nbrs]
        print(f'  region {rid} (label {lab:#04b}, depth {bin(lab).count("1")}): '
              f'neighbors {nbrs} (labels {[f"{x:#04b}" for x in nbr_labs]})')
