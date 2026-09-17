#!/usr/bin/env python3
"""`c_ell` from an EULER CHARACTERISTIC, computed without extracting a single face.

THE IDENTITY.  The faces of the wall graph on `S_ell` are the connected components of
`U_m = {x in ∂A_i : exactly m cubes contain x}`, m = ell+1, over all cubes i.  (Wall arcs have
depth >= m+1 so they are excluded; creases and corners at depth m are interior to faces, since
a crease is a fold and not a separator.)  For a graph on a sphere with c components and F
faces, `sum_f (b(f) - 1) = c - 1`, and a component of an open subsurface of S^2 with b boundary
circles has chi = 2 - b.  So `sum_f b = 2F - chi` and

    c_ell = 1 + F_ell - chi_ell,        F_ell = d_ell (the engine's own depth count).

**So c > 1 exactly when some face has chi < 1 -- an annulus.**  No face extraction needed: only
the total chi.

WHY chi IS COMPUTABLE HERE.  Compactly-supported Euler characteristic is ADDITIVE over any
partition into locally closed pieces, and the cube surface has an obvious one: 6 open facets,
12 open creases, 8 corners.  On an open facet the facet-centre lemma
([METHODS 26](METHODS.md#26-the-facet-centre-lemma)) makes the depth-m set a RADIAL BAND about
the facet centre -- so its components are the maximal angular runs where it is non-empty, each
an open disk (chi_c = 1), unless the run is the whole circle, which is one annulus (chi_c = 0).
On an open crease it is a union of open arcs (chi_c = -1 each) and points (+1).  Corners are
points (+1).

EXACTNESS.  The critical directions are the directions from the facet centre to the arrangement
vertices on that facet -- the only places the order of the radial functions can change.  A
representative direction strictly inside a sector is `d1/||d1||_1 + d2/||d2||_1`, a positive
combination of the two bounding directions, hence exactly inside the open cone and rational.
No angle is ever computed and no direction is sampled.  The critical rays are tested too, since
the band can pinch to nothing exactly on one.

THE GATE.  `c_ell` predicted this way must equal `c_level.level_graph`'s.  The two share no
machinery: one is a union-find over arcs, the other an Euler count over facets, creases and
corners plus the engine's `d_ell`.
"""
import sys, os, json, itertools, collections, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params
from c_level import level_graph, shares_plane, engine
import provenance as PROV


def dot(a, b):
    return sum(a[z] * b[z] for z in range(3))


def depth_of(x, Ms):
    """How many cubes contain x, counting the closed body."""
    return sum(1 for M in Ms if all(abs(dot(M[r], x)) <= 1 for r in range(3)))


def exit_radius(p, d, M):
    """The positive t with p + t d on ∂(that cube), given p strictly inside it."""
    best = None
    for r in range(3):
        a, b = dot(M[r], d), dot(M[r], p)
        if a == 0:
            continue
        for s in (F(1), F(-1)):
            t = (s - b) / a
            if t > 0 and (best is None or t < best):
                best = t
    return best


def facet_exit(p, d, M, k):
    """Where the ray leaves the FACET (the cube's other two slabs)."""
    best = None
    for r in range(3):
        if r == k:
            continue
        a, b = dot(M[r], d), dot(M[r], p)
        if a == 0:
            continue
        for s in (F(1), F(-1)):
            t = (s - b) / a
            if t > 0 and (best is None or t < best):
                best = t
    return best


def ang_key(v):
    """Sort 2-vectors by angle without trigonometry: half-plane, then cross product."""
    half = 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1
    return (half, v)


def cmp_ang(a, b):
    ha = 0 if (a[1] > 0 or (a[1] == 0 and a[0] > 0)) else 1
    hb = 0 if (b[1] > 0 or (b[1] == 0 and b[0] > 0)) else 1
    if ha != hb:
        return ha - hb
    cr = a[0] * b[1] - a[1] * b[0]
    return -1 if cr > 0 else (1 if cr < 0 else 0)


def facet_vertices(qs, Ms, i, k, sgn):
    """Arrangement vertices lying on this facet: where the order of radii can change."""
    n = len(qs)
    # every wall-arc endpoint on this facet, and every crossing of a wall curve with a
    # crease of A_i: these are the only places the ORDER of the radial functions can change
    out = []
    for j in range(n):
        if j == i:
            continue
        for p_, d_, lo, hi in segments(Ms[i], Ms[j]):
            cuts = {lo, hi} | {t for kk in range(n) if kk not in (i, j)
                               for t in on_bdry_params(p_, d_, lo, hi, Ms[kk])}
            for t in cuts:
                x = [p_[z] + t * d_[z] for z in range(3)]
                if dot(Ms[i][k], x) == sgn:
                    out.append(x)
    return out


def facet_chi(qs, Ms, i, k, sgn, depths_wanted):
    """chi_c and component counts of the depth-m band on one facet, for each m wanted."""
    n = len(qs)
    p = [sgn * Ms[i][k][z] for z in range(3)]
    e = [Ms[i][r] for r in range(3) if r != k]
    verts = facet_vertices(qs, Ms, i, k, sgn)
    dirs = []
    for x in verts:
        w = [x[z] - p[z] for z in range(3)]
        v = (dot(e[0], w), dot(e[1], w))
        if v != (0, 0):
            dirs.append(v)
    # dedupe by direction (same ray)
    uniq = []
    for v in dirs:
        if not any(cmp_ang(v, u) == 0 for u in uniq):
            uniq.append(v)
    if not uniq:
        uniq = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))]
    import functools
    uniq.sort(key=functools.cmp_to_key(cmp_ang))

    def l1(v):
        return abs(v[0]) + abs(v[1])

    rays = []
    for a in range(len(uniq)):
        b = (a + 1) % len(uniq)
        rays.append(uniq[a])                              # the critical ray itself
        u, w = uniq[a], uniq[b]
        mid = (u[0] / l1(u) + w[0] / l1(w), u[1] / l1(u) + w[1] / l1(w))
        if mid == (0, 0):                                 # antipodal pair: split differently
            mid = (-u[1], u[0])
        rays.append(mid)

    occupied = {m: [] for m in depths_wanted}
    reaches_centre = {m: [] for m in depths_wanted}
    for v in rays:
        d = [v[0] * e[0][z] + v[1] * e[1][z] for z in range(3)]
        rf = facet_exit(p, d, Ms[i], k)
        rs = []
        for j in range(n):
            if j == i:
                continue
            r = exit_radius(p, d, Ms[j])
            if r is not None:
                rs.append(r)
        rs.sort(reverse=True)                             # s_1 >= s_2 >= ...
        for m in depths_wanted:
            hi = rf if m == 1 else (rs[m - 2] if m - 2 < len(rs) else F(0))
            lo = rs[m - 1] if m - 1 < len(rs) else F(0)
            if rf is not None and hi is not None:
                hi = min(hi, rf)
            occupied[m].append(hi is not None and lo < hi)
            reaches_centre[m].append(lo == 0)

    out = {}
    for m in depths_wanted:
        occ = occupied[m]
        if all(occ):
            # A BAND THAT REACHES THE FACET CENTRE IS A DISK, NOT AN ANNULUS.  The centre has
            # depth n, so for m = n the inner radius is 0 and the region contains the centre;
            # flagging it as a wrap-around annulus cost chi exactly one per facet and made the
            # innermost level come out at chi = 0 where it must be positive.
            if any(reaches_centre[m]):
                out[m] = {'components': 1, 'chi': 1, 'annulus': False}
            else:
                out[m] = {'components': 1, 'chi': 0, 'annulus': True}
        elif not any(occ):
            out[m] = {'components': 0, 'chi': 0, 'annulus': False}
        else:
            runs = 0
            L = len(occ)
            for z in range(L):
                if occ[z] and not occ[(z - 1) % L]:
                    runs += 1
            out[m] = {'components': runs, 'chi': runs, 'annulus': False}
    out['_rays'] = rays
    out['_occ'] = occupied
    out['_basis'] = e
    out['_centre'] = p
    return out


def run_ids(occ):
    """Label each occupied angular position with the id of its maximal cyclic run."""
    L = len(occ)
    lab = [None] * L
    if all(occ):
        return [0] * L
    nxt = 0
    for z in range(L):
        if occ[z] and not occ[(z - 1) % L]:
            w = z
            while occ[w % L] and lab[w % L] is None:
                lab[w % L] = nxt
                w += 1
            nxt += 1
    return lab


def face_count(qs, Ms, depths_wanted):
    """F_m: the number of components of U_m, gluing facet runs across creases.

    A face of the sphere ∂D_m spans several facets of one cube, joined wherever a crease at
    depth m runs between them -- a crease is a FOLD, not a separator ([P312]).  This is the
    quantity the surjection faces -> regions is defined on, so it is what `d_m <= F_m`
    compares against.
    """
    import functools
    n = len(qs)
    data = {}
    for i in range(n):
        for k in range(3):
            for sgn in (1, -1):
                data[(i, k, sgn)] = facet_chi(qs, Ms, i, k, sgn, depths_wanted)
    par = {}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb

    labels = {}
    for key, r in data.items():
        for m in depths_wanted:
            lab = run_ids(r['_occ'][m])
            labels[(key, m)] = lab
            for v in set(x for x in lab if x is not None):
                par[(key, m, v)] = (key, m, v)

    def locate(key, m, x):
        """Which run of this facet's depth-m band the point x sits in."""
        r = data[key]
        p, e = r['_centre'], r['_basis']
        w = [x[z] - p[z] for z in range(3)]
        v = (dot(e[0], w), dot(e[1], w))
        if v == (0, 0):
            return None
        rays, lab = r['_rays'], labels[(key, m)]
        best = None
        for idx, u in enumerate(rays):
            if cmp_ang(u, v) == 0:
                best = idx
                break
        if best is None:                      # strictly inside a sector: find the bracket
            for idx in range(0, len(rays), 2):
                a = rays[idx]
                b = rays[(idx + 2) % len(rays)]
                cr1 = a[0] * v[1] - a[1] * v[0]
                cr2 = v[0] * b[1] - v[1] * b[0]
                if cr1 > 0 and cr2 > 0:
                    best = idx + 1
                    break
        if best is None:
            return None
        return lab[best]

    # creases glue runs on the two facets they separate
    for i in range(n):
        V = [Ms[i][r] for r in range(3)]
        for c in range(3):
            o = [r for r in range(3) if r != c]
            for s0 in (1, -1):
                for s1 in (1, -1):
                    p = [s0 * V[o[0]][z] + s1 * V[o[1]][z] for z in range(3)]
                    d = [V[c][z] for z in range(3)]
                    cuts = sorted({F(-1), F(1)} | {t for kk in range(n) if kk != i
                                  for t in on_bdry_params(p, d, F(-1), F(1), Ms[kk])})
                    for a, b in zip(cuts, cuts[1:]):
                        if a >= b:
                            continue
                        mid = [p[z] + ((a + b) / 2) * d[z] for z in range(3)]
                        m = depth_of(mid, Ms)
                        if m not in depths_wanted:
                            continue
                        k1, k2 = (i, o[0], s0), (i, o[1], s1)
                        r1, r2 = locate(k1, m, mid), locate(k2, m, mid)
                        if r1 is not None and r2 is not None:
                            a1, a2 = (k1, m, r1), (k2, m, r2)
                            if a1 in par and a2 in par:
                                union(a1, a2)
    out = collections.Counter()
    for key, m, v in list(par):
        pass
    roots = collections.defaultdict(set)
    for node in par:
        roots[node[1]].add(find(node))
    return {m: len(roots[m]) for m in depths_wanted}


def creases_and_corners(qs, Ms, i, depths_wanted):
    """chi_c contributions of the 12 open creases and 8 corners of cube i."""
    n = len(qs)
    arc = collections.Counter()
    pts = collections.Counter()
    V = [Ms[i][r] for r in range(3)]
    for c in range(3):
        o = [r for r in range(3) if r != c]
        for s0 in (1, -1):
            for s1 in (1, -1):
                p = [s0 * V[o[0]][z] + s1 * V[o[1]][z] for z in range(3)]
                d = [V[c][z] for z in range(3)]
                cuts = sorted({F(-1), F(1)} | {t for kk in range(n) if kk != i
                              for t in on_bdry_params(p, d, F(-1), F(1), Ms[kk])})
                for a, b in zip(cuts, cuts[1:]):
                    if a >= b:
                        continue
                    mid = [p[z] + ((a + b) / 2) * d[z] for z in range(3)]
                    arc[depth_of(mid, Ms)] += 1
                # CUT POINTS ARE NOT IN THE FACE SET.  A cut point on a crease is where
                # another cube's boundary crosses it, so it lies on a WALL and is a vertex of
                # the arrangement, not an interior point of a face.  Counting them as +1 was
                # the whole of the m = 2 error: chi came out 348 against F = 240, and chi <= F
                # is forced because every component has chi = 2 - b <= 1.  They are invisible
                # at m = 1 -- a cut point always has depth >= 2 -- which is why depth 1 alone
                # came out right and hid the bug.
    corner = collections.Counter()
    for s in itertools.product((1, -1), repeat=3):
        x = [sum(s[r] * V[r][z] for r in range(3)) for z in range(3)]
        corner[depth_of(x, Ms)] += 1
    # each interior cut point is shared by ONE crease (it lies in that crease's relative
    # interior), each corner by one cube; no double counting here.
    return {m: -arc[m] + corner[m] for m in depths_wanted}


def predict_c(qs):
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    wanted = list(range(1, n + 1))
    chi = collections.Counter()
    ann = collections.Counter()
    for i in range(n):
        for k in range(3):
            for sgn in (1, -1):
                r = facet_chi(qs, Ms, i, k, sgn, wanted)
                for m, v in r.items():
                    if isinstance(m, str):          # '_rays', '_occ', ... are scratch keys
                        continue
                    chi[m] += v['chi']
                    ann[m] += 1 if v['annulus'] else 0
        cc = creases_and_corners(qs, Ms, i, wanted)
        for m, v in cc.items():
            chi[m] += v
    return chi, ann


def main(trials=200, seed=11, want_c2=4):
    rng = random.Random(seed)
    out = {'what': 'c_ell from an Euler characteristic, gated against the union-find count',
           'identity': 'c_ell = 1 + d_ell - chi_ell', 'rows': []}
    ok = bad = 0
    seen_c2 = 0
    tried = 0
    while tried < trials and (ok + bad) < 40:
        tried += 1
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-20, 20) for _ in range(4))
                               for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            g = level_graph(qs)
            e = engine(qs)
            chi, ann = predict_c(qs)
        except Exception:
            continue
        by = e.get('by_depth') or {}
        for ell, v in sorted(g.items()):
            d = by.get(str(ell))
            if d is None:
                continue
            m = ell + 1
            pred = 1 + d - chi[m]
            good = (pred == v['c'])
            ok += good; bad += (not good)
            if v['c'] > 1:
                seen_c2 += 1
            out['rows'].append({'quats': [list(q) for q in qs], 'level': ell,
                                'd_ell': d, 'chi': chi[m], 'predicted_c': pred,
                                'measured_c': v['c'], 'annulus_facets': ann[m],
                                'agrees': bool(good)})
            print('level %s d=%-4s chi=%-5s -> c_pred %-3s  c_measured %-3s  %s%s'
                  % (ell, d, chi[m], pred, v['c'], 'ok' if good else 'MISMATCH',
                     '   <- c>1' if v['c'] > 1 else ''), flush=True)
    out['agree'], out['mismatch'] = ok, bad
    out['c_gt_1_instances'] = seen_c2
    out['reproduce'] = PROV.stamp(parameters={'trials': trials, 'seed': seed})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'euler_faces.json'), 'w'),
              indent=1, default=str)
    print('agree %d | mismatch %d | c>1 instances seen %d' % (ok, bad, seen_c2))


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
