#!/usr/bin/env python3
"""The top level as a coloured spherical Voronoi diagram, and a fast search against `d4 >= 2c4`.  [P431]

**Reformulation.** Cube x is innermost in direction u exactly when its M_x(u) = max_i |n_i·u| is
largest, that is, when u is angularly closest to one of x's six face centres ±n_i among all 6n
face centres. With no shared face plane, the 6n points are distinct.
- Γ_{n−1} (the top level) is the union of the Voronoi edges between cells of DIFFERENT cubes.
- Its faces (d_{n−1}) are the connected same-colour unions of cells.
- The Voronoi diagram is dual to the convex hull of the points (the spherical Delaunay
  triangulation). Cells are adjacent iff their points share a hull edge, and Voronoi vertices
  are hull facets.
So:
- `d4` = number of components of the colour-induced subgraphs of the hull's edge graph;
- `c4` = number of components of the graph on hull facets, joined across bichromatic hull edges,
  among facets with a bichromatic edge.

**Validation.** On compounds already counted, d4 and c4 must equal the exact engine's / c_level's.
That includes c4 = 2 rows.

**Search.** [P430] needs `d4 − 2c4 >= 0` for 457. Random and climbed configurations minimise it.
The hull is computed in floating point, which is fine for generic points. Every candidate with a
small value is re-checked exactly with c_level before it counts.

**`--degrees`**: the lemma that would prove `d4 >= 2c4`. If no component of Γ4 borders only two
faces, then every component has degree >= 3 in the face/component tree and `F − 2c4 >= 1`. This
mode reports, for every compound with `c4 >= 2` it can find (band rows on file, plus fresh climbs
maximising c4), the number of distinct faces each Γ4 component borders.
Output: data/top_voronoi_degrees.json.

**`--pairs`**: two cubes alone. Is the tie set of two cubes (the boundary between the union of
x's Voronoi cells and the union of y's) always connected? If so, a Γ4 component bordering only
two faces would be the whole two-cube tie set, which is antipodally symmetric, and that is
impossible. Output: data/top_voronoi_pairs.json.

**`--pair-degrees`**: two cubes alone, the reduced lemma. A Γ4 component bordering only cubes x and
y is a whole component of the x–y tie set, and each x–y region it borders contains a distinct
five-cube region. So it is enough that every component of two cubes' tie set borders >= 3 regions.
This mode measures that, with a climb minimising it. Output: data/top_voronoi_pair_degrees.json.

**Correction, 2026-10-06.** The first version joined cells across every hull edge. When four face
centres are cocircular, Qhull splits the quadrilateral facet with a diagonal, and that diagonal
invented an adjacency between two cells meeting at a point. An n = 3 integer compound gave
d2 = 14 against the engine's 16. The first validation (550 rows, all at n = 5) passed only because
none of its rows was degenerate. Edges between coplanar facets are now skipped, and the validation
includes small-coordinate integer compounds at n = 3, 4, 5, where degeneracy is common.
The merge tolerance was first 1e-9. That merged nearly coplanar facets of generic inputs: 1 random pair,
and 61 more reached by climbs, gave a false single component. It is now 1e-12, and the tolerance
sweep (`--pairs-audit`) shows the merge firing only on true degeneracies.

Output: data/top_voronoi.json.
"""
import os, sys, json, random, itertools, collections, multiprocessing as mp
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL

ROOT = os.path.dirname(os.path.dirname(HERE))


def rot(q):
    w, x, y, z = np.array(q, float) / np.linalg.norm(q)
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
                     [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
                     [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]])


TOL = 1e-12       # coplanarity tolerance for merging hull facets. 1e-9 was too loose: it merged
                  # nearly coplanar facets of generic pairs (2026-10-06 audit, --pairs-audit). Qhull's
                  # noise is ~1e-15, so true degeneracies (integer inputs) still merge at 1e-12.
MERGES = [0]      # number of facet pairs merged in the last call (diagnostic)


def _diagram(qs):
    """points, colours, true Voronoi adjacencies, and Voronoi vertices.

    DEGENERACY (found 2026-10-06 on an n = 3 integer compound): four or more cocircular points
    make a hull facet that Qhull triangulates, and the added diagonal invents an adjacency between
    two cells that meet only at a point. So a hull edge counts as a Voronoi edge only when its two
    facets are NOT coplanar, and coplanar facets are merged into one Voronoi vertex."""
    pts, col = [], []
    for k, q in enumerate(qs):
        R = rot(q)
        for i in range(3):
            for s_ in (1, -1):
                pts.append(s_ * R[:, i]); col.append(k)
    pts = np.array(pts)
    hull = ConvexHull(pts)
    eq = hull.equations
    edge_facets = collections.defaultdict(list)
    for f, simp in enumerate(hull.simplices):
        for a, b in itertools.combinations(sorted(simp), 2):
            edge_facets[(a, b)].append(f)
    vpar = list(range(len(hull.simplices)))
    def vf(x):
        while vpar[x] != x:
            vpar[x] = vpar[vpar[x]]; x = vpar[x]
        return x
    true_edges = {}
    MERGES[0] = 0
    for e, fs in edge_facets.items():
        if len(fs) == 2 and np.allclose(eq[fs[0]], eq[fs[1]], atol=TOL, rtol=0):
            MERGES[0] += 1
            vpar[vf(fs[0])] = vf(fs[1])          # same Voronoi vertex; not a Voronoi edge
        else:
            true_edges[e] = fs
    return pts, col, true_edges, vf


def top_counts(qs):
    pts, col, edges, vf = _diagram(qs)
    par = list(range(len(pts)))
    def fnd(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in edges:
        if col[a] == col[b]:
            par[fnd(a)] = fnd(b)
    d4 = len({fnd(i) for i in range(len(pts))})
    fp = {}
    def ff(x):
        while fp[x] != x:
            fp[x] = fp[fp[x]]; x = fp[x]
        return x
    for (a, b), fs in edges.items():
        if col[a] != col[b]:
            vs = [vf(f) for f in fs]
            for v in vs:
                fp.setdefault(v, v)
            if len(vs) == 2:
                fp[ff(vs[0])] = ff(vs[1])
    c4 = len({ff(v) for v in fp})
    return d4, c4


def validate():
    """against exact counts: the n = 5 evidence rows, plus integer compounds at n = 3, 4, 5 drawn
    with SMALL coordinates (so cocircular face centres, the degenerate case, occur), checked
    against the exact engine (d) and c_level (c)."""
    rows = []
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_n5.json')))['rows'][:150]:
        rows.append((r['qs'], r['bd']['4'], r['c']['4'], 'n5 rows'))
    for r in json.load(open(os.path.join(ROOT, 'data', 'band_hunt_n5.json')))['measured']:
        rows.append((r['qs'], r['bd']['4'], r['c']['4'], 'n5 bands'))
    rnd = random.Random(31)
    for n in (3, 4, 5):
        k = 0
        while k < 150:
            qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-4, 4) or 1 for _ in range(4)) for _ in range(n - 1)]
            if CL.shares_plane(qs) or len({tuple(q) for q in qs}) < n:
                continue
            e = CL.engine(qs)
            if 'by_depth' not in e:
                continue
            g = CL.level_graph(qs)
            rows.append((qs, e['by_depth'][str(n - 1)], g[n - 1]['c'], 'n%d small ints' % n))
            k += 1
    res = collections.defaultdict(lambda: [0, 0, 0])
    bad = []
    for q, d, c, kind in rows:
        res[kind][0] += 1
        _, _, edges, vf = _diagram(q)
        res[kind][2] += len({vf(f) for fs in edges.values() for f in fs}) < len({f for fs in edges.values() for f in fs})
        got = top_counts(q)
        if got == (d, c):
            res[kind][1] += 1
        else:
            bad.append((kind, q, (d, c), got))
    return dict(res), bad


def search(seed, iters=200000):
    rnd = random.Random(seed)
    best = None
    hist = collections.Counter()
    worst = []
    for _ in range(iters):
        qs = [(1, 0, 0, 0)] + [tuple(rnd.gauss(0, 1) for _ in range(4)) for _ in range(4)]
        d4, c4 = top_counts(qs)
        hist[c4] += 1
        v = d4 - 2 * c4
        if best is None or v < best[0]:
            best = (v, d4, c4, qs)
        if c4 >= 3:
            worst.append((v, d4, c4, qs))
    return {'seed': seed, 'hist': dict(hist), 'best': best, 'c4ge3': worst[:20]}


def climb(seed, steps=20000):
    """minimise d4 − 2c4 by perturbing cubes (Gaussian steps on quaternions)"""
    rnd = random.Random(seed)
    cur = [(1, 0, 0, 0)] + [tuple(rnd.gauss(0, 1) for _ in range(4)) for _ in range(4)]
    d4, c4 = top_counts(cur)
    val = d4 - 2 * c4
    best = (val, d4, c4, cur)
    for _ in range(steps):
        i = rnd.randrange(1, 5)
        sc = rnd.choice((0.3, 0.1, 0.03, 0.01))
        nxt = list(cur)
        nxt[i] = tuple(x + rnd.gauss(0, sc) for x in nxt[i])
        d, c = top_counts(nxt)
        if d - 2 * c <= val:
            cur, val = nxt, d - 2 * c
            if val < best[0]:
                best = (val, d, c, cur)
    return {'seed': seed, 'best': best}


def main():
    res, bad = validate()
    print('validation against exact counts (rows, agree, rows with a degenerate Voronoi vertex): %s' % res, flush=True)
    for b in bad[:10]:
        print('   MISMATCH', b)
    assert not bad, 'reformulation does not match the exact counts'
    n = sum(v[0] for v in res.values()); ok = sum(v[1] for v in res.values()); n2 = ok2 = None
    with mp.Pool(8) as p:
        rs = p.map(search, range(8))
        cs = p.map(climb, range(100, 116))
    hist = collections.Counter()
    for r in rs:
        hist.update(r['hist'])
    best = min((r['best'] for r in rs), key=lambda b: b[0])
    cbest = sorted((r['best'] for r in cs), key=lambda b: b[0])
    print('random: %d compounds, c4 histogram %s, min d4 - 2c4 = %d (d4 %d, c4 %d)'
          % (sum(hist.values()), sorted(hist.items()), best[0], best[1], best[2]))
    print('climbs minimising d4 - 2c4: %s' % [(b[0], b[1], b[2]) for b in cbest])
    # exact re-check of the climb bests (rationalised) with c_level
    exact = []
    for b in cbest[:6]:
        qs = [tuple(int(round(x * 1000)) or 1 for x in q) for q in b[3]]
        if CL.shares_plane(qs):
            continue
        g = CL.level_graph(qs)
        e = CL.engine(qs)
        exact.append({'float': b[:3], 'exact_d4': e['by_depth']['4'], 'exact_c4': g[4]['c'],
                      'float_on_rationalised': top_counts(qs), 'qs': qs})
    for x in exact:
        print('   exact recheck: float %s, rationalised float %s, exact d4 %d c4 %d'
              % (x['float'], x['float_on_rationalised'], x['exact_d4'], x['exact_c4']))
    json.dump({'validation': {'rows': n, 'agree': ok, 'c4_2_rows': n2, 'c4_2_agree': ok2},
               'random_hist': dict(hist), 'random_best': best[:3],
               'climb_best': [b[:3] for b in cbest], 'exact_recheck': exact},
              open(os.path.join(ROOT, 'data', 'top_voronoi.json'), 'w'), indent=1, default=str)


def component_degrees(qs):
    pts, col, edges, vf = _diagram(qs)
    par = list(range(len(pts)))
    def fnd(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for (a, b) in edges:
        if col[a] == col[b]:
            par[fnd(a)] = fnd(b)
    fp = {}
    def ff(x):
        while fp[x] != x:
            fp[x] = fp[fp[x]]; x = fp[x]
        return x
    for (a, b), fs in edges.items():
        if col[a] != col[b]:
            vs = [vf(f) for f in fs]
            for v in vs:
                fp.setdefault(v, v)
            if len(vs) == 2:
                fp[ff(vs[0])] = ff(vs[1])
    faces_of = collections.defaultdict(set)
    for (a, b), fs in edges.items():
        if col[a] != col[b]:
            faces_of[ff(vf(fs[0]))].update((fnd(a), fnd(b)))
    return sorted(len(v) for v in faces_of.values())


def climb_c4(seed, steps=20000):
    rnd = random.Random(seed)
    cur = [(1, 0, 0, 0)] + [tuple(rnd.gauss(0, 1) for _ in range(4)) for _ in range(4)]
    d4, c4 = top_counts(cur)
    key = (c4, -min(component_degrees(cur)))
    found = []
    for _ in range(steps):
        i = rnd.randrange(1, 5)
        nxt = list(cur)
        nxt[i] = tuple(x + rnd.gauss(0, rnd.choice((0.3, 0.1, 0.03))) for x in nxt[i])
        d, c = top_counts(nxt)
        k = (c, -min(component_degrees(nxt)))
        if c >= 2:
            found.append(component_degrees(nxt))
        if k >= key:
            cur, key = nxt, k
    return found


def main_degrees():
    rows = [r['qs'] for r in json.load(open(os.path.join(ROOT, 'data', 'band_hunt_n5.json')))['measured']]
    rows += [r['qs'] for r in json.load(open(os.path.join(ROOT, 'data', 'band_hunt_n5_min4.json')))['rows']]
    degs = collections.Counter()
    mins = collections.Counter()
    n2 = 0
    for q in rows:
        d4, c4 = top_counts(q)
        if c4 >= 2:
            n2 += 1
            cd = component_degrees(q)
            degs[tuple(cd)] += 1
            mins[min(cd)] += 1
    with mp.Pool(8) as p:
        fr = p.map(climb_c4, range(300, 316))
    for f in fr:
        for cd in f:
            n2 += 1
            degs[tuple(cd)] += 1
            mins[min(cd)] += 1
    print('compounds with c4 >= 2: %d; min component degree histogram %s' % (n2, sorted(mins.items())))
    print('degree patterns (most common): %s' % degs.most_common(8))
    json.dump({'c4ge2': n2, 'min_degree_hist': dict(mins), 'patterns': [[list(k), v] for k, v in degs.most_common(50)]},
              open(os.path.join(ROOT, 'data', 'top_voronoi_degrees.json'), 'w'), indent=1)


if __name__ == '__main__' and not any(a.startswith('--pair') for a in sys.argv):
    main_degrees() if '--degrees' in sys.argv else main()


def pair_components(seed, iters=200000):
    """two cubes: number of components of their tie set (the bichromatic Voronoi boundary of
    their 12 face centres). Random rotations plus a climb maximising it."""
    rnd = random.Random(seed)
    hist = collections.Counter()
    worst = None
    for _ in range(iters):
        qs = [(1, 0, 0, 0), tuple(rnd.gauss(0, 1) for _ in range(4))]
        d, c = top_counts(qs)
        hist[c] += 1
        if worst is None or c > worst[0]:
            worst = (c, d, qs)
    cur = worst[2]
    cc = worst[0]
    for _ in range(20000):
        nxt = [cur[0], tuple(x + rnd.gauss(0, rnd.choice((0.3, 0.05, 0.01))) for x in cur[1])]
        d, c = top_counts(nxt)
        hist[c] += 1
        if c >= cc:
            cur, cc = nxt, c
            if c > worst[0]:
                worst = (c, d, nxt)
    return {'hist': dict(hist), 'worst': worst}


def pairs_audit(seed, iters=220000):
    """the random phase of --pairs (same seeds), keeping every c = 1 case, whether a coplanar
    merge fired, and c at three tolerances"""
    global TOL
    rnd = random.Random(seed)
    out = []
    for _ in range(iters):
        qs = [(1, 0, 0, 0), tuple(rnd.gauss(0, 1) for _ in range(4))]
        TOL = 1e-9
        d, c = top_counts(qs)
        if c != 2 or MERGES[0]:
            row = {'qs': qs, 'c_1e-9': c, 'merges_1e-9': MERGES[0]}
            for t in (1e-12, 1e-7):
                TOL = t
                row['c_%g' % t] = top_counts(qs)[1]
                row['merges_%g' % t] = MERGES[0]
            out.append(row)
    TOL = 1e-9
    return out


if __name__ == '__main__' and '--pairs-audit' in sys.argv:
    with mp.Pool(8) as p:
        rs = p.map(pairs_audit, range(8))
    rows = [r for x in rs for r in x]
    print('pairs with c != 2 or a coplanar merge, in the random phase: %d' % len(rows))
    for r in rows[:15]:
        print('   ', {k: v for k, v in r.items() if k != 'qs'})
    json.dump(rows, open(os.path.join(ROOT, 'data', 'top_voronoi_pairs_audit.json'), 'w'), indent=1)
elif __name__ == '__main__' and '--pairs' in sys.argv:
    with mp.Pool(8) as p:
        rs = p.map(pair_components, range(8))
    h = collections.Counter()
    for r in rs:
        h.update(r['hist'])
    print('two cubes: tie-set component histogram %s; max %s' % (sorted(h.items()), max(r['worst'][0] for r in rs)))
    json.dump({'hist': dict(h), 'worst': [r['worst'] for r in rs]},
              open(os.path.join(ROOT, 'data', 'top_voronoi_pairs.json'), 'w'), indent=1, default=str)


def pair_degrees(seed, iters=100000):
    """two cubes: number of faces (d1 of the pair) and each tie-set component's face degree;
    random rotations, then a climb MINIMISING the smallest component degree"""
    rnd = random.Random(seed)
    hist = collections.Counter()
    fh = collections.Counter()
    best = None
    for _ in range(iters):
        qs = [(1, 0, 0, 0), tuple(rnd.gauss(0, 1) for _ in range(4))]
        cd = component_degrees(qs)
        d, c = top_counts(qs)
        hist[min(cd)] += 1
        fh[d] += 1
        if best is None or (min(cd), d) < best[:2]:
            best = (min(cd), d, qs)
    cur = best[2]
    for _ in range(20000):
        nxt = [cur[0], tuple(x + rnd.gauss(0, rnd.choice((0.3, 0.05, 0.01, 0.002))) for x in cur[1])]
        cd = component_degrees(nxt)
        d, c = top_counts(nxt)
        hist[min(cd)] += 1
        fh[d] += 1
        if (min(cd), d) <= best[:2]:
            cur = nxt
            best = (min(cd), d, nxt)
    return {'min_degree_hist': dict(hist), 'faces_hist': dict(fh), 'best': best}


if __name__ == '__main__' and '--pair-degrees' in sys.argv:
    with mp.Pool(8) as p:
        rs = p.map(pair_degrees, range(8))
    h, f = collections.Counter(), collections.Counter()
    for r in rs:
        h.update(r['min_degree_hist']); f.update(r['faces_hist'])
    print('two cubes: min component degree histogram %s' % sorted(h.items()))
    print('two cubes: faces (pair d1) histogram %s' % sorted(f.items()))
    print('climb bests (min degree, faces): %s' % sorted((r['best'][0], r['best'][1]) for r in rs))
    json.dump({'min_degree_hist': dict(h), 'faces_hist': dict(f), 'bests': [r['best'] for r in rs]},
              open(os.path.join(ROOT, 'data', 'top_voronoi_pair_degrees.json'), 'w'), indent=1, default=str)
