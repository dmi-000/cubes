#!/usr/bin/env python3
"""(L) at low-end vertices, checked exactly: every owner pattern, every cell.  [P420]

[P419] reduced the multi-pair local inequality (L) to a residue: vertices where nearly every
active point is shared. At such a vertex every point has two or more owners, except possibly the
points of ONE cube `x`. This script settles that residue by exhaustion instead of sampling.

1. **Exact circle model.** Angles are Fractions, in degrees. Each distance function is linear
   between consecutive critical directions: points, antipodes, and the bisectors of any two points
   (and their antipodes). So the tie status at each critical direction and at each interval
   midpoint gives every degree exactly. It is validated against `patch_charging_local.analyse` on
   integer configurations before use.

2. **Owner patterns.** Each tying cube owns 1 or 2 points, or 3 at a corner.
   - Two cubes co-own at most one point.
   - Every point has two or more owners, except points owned by `x` alone.
   - The implied sharing classes form one of the eight realisable structures
     (`lowend_check.realisable`).
   - Vertex kinds: four-fold (all four tie, none outer), or triple (three tie, the fourth outer).
     All other kinds are equalities.
   - Patterns are taken up to relabelling of the cubes.

3. **Positions.** A two-point cube's points are theta apart, with theta in (120, 180]; corners have
   three at 120.
   - Points linked through cubes form components, each with a free offset. One offset is fixed by
     rotation.
   - The degrees change only where two critical directions coincide, a linear condition in
     (theta, offsets).
   - Every cell of that arrangement is sampled: each critical value and each open interval between
     consecutive critical values. With two parameters, every vertex, every edge midpoint, and a
     point just off each edge on both sides are sampled.
   - Parameter values where two distinct points coincide are skipped: that is a different
     pattern, enumerated separately if realisable.

**Sharpness.** The slack of (L) is tabulated. Tight cases (slack 0 at vertices of degree >= 3)
must occur among the samples, or the check never touched the boundary of (L). This is the
control: a checker that only saw slack would pass a false inequality one unit stronger.

**Sampler cross-check.** Compares cyclic ORDER TYPES of the critical directions, not degree
signatures. A placement has only 1-3 degree signatures, so a missed cell would almost never show
up as a new one; the first version's check (2026-10-04) was too weak for that reason. Every
order type reached by 3 000 random rational parameter values must also appear among the cell
samples.

**Isolated vertices.** A diagram through `v` whose tie set around `v` is empty would make `v` a
degree-0 vertex, costing −2. These are flagged (`ISOLATED_*`), never dropped.

**Merged points.** A sample where two distinct points coincide is a configuration of the merged
pattern. Each such sample is asserted to be unrealisable, not low-end, or among the enumerated
patterns (`MISSING` otherwise).

**Completeness of the patterns.** With two cubes owning unshared points, the innermost diagram has
>= 3 ends. A block of single points between shared ones has 2 ends plus its colour changes; with
no shared points, all >= 3 colours change. So "all shared but one cube's" IS the residue.
Corner patterns are empty: a non-x cube's three points would all be shared, which is three
distinct planes and a forbidden triangle.

Output: data/residue_exact.json. Any excess is a counterexample to (L) and is printed.
"""
import os, sys, json, itertools, collections
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ROOT = os.path.dirname(os.path.dirname(HERE))
CUBES = 'abcd'
TRIPLES = [''.join(t) for t in itertools.combinations(CUBES, 3)]
INF, NEG = Fr(10 ** 6), Fr(-1)


# ---------------------------------------------------------------- exact circle model

def cd(a, b):
    d = (a - b) % 360
    return min(d, 360 - d)


def critical(allpts):
    c = set()
    for p in allpts:
        c.add(p % 360); c.add((p + 180) % 360)
    for p, q in itertools.combinations(allpts, 2):
        m = (p + q) / 2
        c.add(m % 360); c.add((m + 180) % 360)
    return sorted(c)


def exact_degrees(pts, outer):
    """pts: {cube: [Fraction degrees]} for tying cubes.  Returns (dG, {S: dS}) as analyse does,
    or None if v is not on G'."""
    allpts = sorted({p % 360 for ps in pts.values() for p in ps})
    crit = critical(allpts)
    n = len(crit)
    mids = [((crit[i] + (crit[(i + 1) % n] if i + 1 < n else crit[0] + 360)) / 2) % 360 for i in range(n)]
    def dist(x, w):
        if x in pts:
            return min(cd(w, p) for p in pts[x])
        return INF if x in outer else NEG
    def deg(members, level):
        def tie(w):
            ds = sorted((dist(x, w) for x in members), reverse=True)
            return ds[level - 1] == ds[level]
        tc = [tie(c) for c in crit]
        tm = [tie(m) for m in mids]
        if all(tc) and all(tm):
            return False, 0
        if not any(tc) and not any(tm):
            return False, 0
        ends = 0
        for i in range(n):
            left, right = tm[i - 1], tm[i]
            if tc[i] and not (left and right):
                ends += 1
        return True, ends
    onG, dG = deg(CUBES, 2)
    if not onG:
        return None
    dS = {}
    for S in TRIPLES:
        on, d = deg(S, 2)
        if on:
            dS[S] = d
    return dG, dS


def isolated(pts, outer):
    """diagrams through v whose tie set around v is EMPTY (v an isolated point: degree 0, which
    would cost -2).  v is in a diagram if the level's two values tie AT v: there every tying cube
    has the common value, the others are strictly outer or inner."""
    allpts = sorted({p % 360 for ps in pts.values() for p in ps})
    crit = critical(allpts)
    n = len(crit)
    mids = [((crit[i] + (crit[(i + 1) % n] if i + 1 < n else crit[0] + 360)) / 2) % 360 for i in range(n)]
    def dist(x, w):
        if x in pts:
            return min(cd(w, p) for p in pts[x])
        return INF if x in outer else NEG
    def at_v(x):
        return Fr(0) if x in pts else (INF if x in outer else NEG)
    out = []
    for name, members in [('Gamma', CUBES)] + [(S, S) for S in TRIPLES]:
        vs = sorted((at_v(x) for x in members), reverse=True)
        if vs[1] != vs[2]:
            continue                                  # v not on this diagram
        def tie(w):
            ds = sorted((dist(x, w) for x in members), reverse=True)
            return ds[1] == ds[2]
        if not any(tie(c) for c in crit) and not any(tie(m) for m in mids):
            out.append(name)
    return out


def validate(trials=300):
    """the exact model against patch_charging_local.analyse on integer (quarter-degree) configs"""
    import random
    from patch_charging_local import analyse, config
    rnd = random.Random(420)
    bad = n = 0
    for share in ('none', 'pair', 'two', 'hub', 'axis'):
        k = 0
        while k < trials // 5:
            c = config(rnd, 'general', share)
            if c is None:
                continue
            k += 1
            pts, outer = c
            a = analyse(pts, outer)
            b = exact_degrees({x: [Fr(p, 4) for p in ps] for x, ps in pts.items()}, outer)
            n += 1
            if a != b:
                bad += 1
    return n, bad


# ---------------------------------------------------------------- patterns

def patterns(corner):
    """yield (T, outer, owners) where owners maps point label -> frozenset of cubes, and each
    cube's labels are listed; up to relabelling."""
    from lowend_check import realisable
    seen = set()
    for kind in ('four', 'triple'):
        T = list(CUBES) if kind == 'four' else list('abc')
        outer = set() if kind == 'four' else {'d'}
        counts_opts = [[3] * len(T)] if corner else list(itertools.product([1, 2], repeat=len(T)))
        for counts in counts_opts:
            slots = [(x, i) for x, k in zip(T, counts) for i in range(k)]
            # set partitions of the slots into point labels
            for part in set_partitions(slots):
                ok = True
                owners = []
                for block in part:
                    cubes = [x for x, _ in block]
                    if len(set(cubes)) != len(cubes):
                        ok = False; break          # a cube's two slots are distinct points
                    owners.append(frozenset(cubes))
                if not ok:
                    continue
                if any(len(a & b) > 1 for a, b in itertools.combinations(owners, 2)):
                    continue                        # two cubes co-own <= 1 point
                singles = {next(iter(o)) for o in owners if len(o) == 1}
                if len(singles) > 1:
                    continue                        # low-end: only one cube owns unshared points
                classes = sorted({''.join(sorted(o)) for o in owners if len(o) >= 2})
                if not classes or not realisable(classes):
                    continue
                key = canon(T, outer, owners)
                if key in seen:
                    continue
                seen.add(key)
                yield T, outer, owners, [(x, k) for x, k in zip(T, counts)]


def set_partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in set_partitions(rest):
        yield [[first]] + p
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]


def canon(T, outer, owners):
    best = None
    for perm in itertools.permutations(T):
        m = dict(zip(T, perm))
        k = tuple(sorted(tuple(sorted(m[x] for x in o)) for o in owners))
        if best is None or k < best:
            best = k
    return (len(T), best)


# ---------------------------------------------------------------- positions

def placements(T, owners, corner):
    """Position each point label as an affine form in (theta, o1, o2, ...): a dict var -> coeff,
    with '1' the constant.  Cubes with two (three) points link them by +-theta (and -+theta).
    Yields (forms, nparams_free, has_theta) for every sign choice."""
    labels = list(range(len(owners)))
    cube_pts = {x: [i for i in labels if x in owners[i]] for x in T}
    # union-find over labels via cube links
    par = list(labels)
    def find(i):
        while par[i] != i:
            par[i] = par[par[i]]; i = par[i]
        return i
    for x, ps in cube_pts.items():
        for p in ps[1:]:
            par[find(p)] = find(ps[0])
    comps = sorted({find(i) for i in labels})
    multi = [x for x in T if len(cube_pts[x]) >= 2]
    sign_opts = list(itertools.product([1, -1], repeat=len(multi))) if not corner else [tuple([1] * len(multi))]
    for signs in sign_opts:
        sgn = dict(zip(multi, signs))
        # BFS assigning forms
        forms = {}
        for ci, c in enumerate(comps):
            base = {'1': Fr(0)} if ci == 0 else {'o%d' % ci: Fr(1)}
            forms[c] = base
            stack = [c]
            while stack:
                i = stack.pop()
                for x in T:
                    ps = cube_pts[x]
                    if i not in ps:
                        continue
                    k = ps.index(i)
                    for j, q in enumerate(ps):
                        # cube x's points sit at base_x + m*theta: m = 0, +s, -s (corner: 0, 1, -1)
                        mi = [0, 1, -1][k] * (sgn.get(x, 1))
                        mj = [0, 1, -1][j] * (sgn.get(x, 1))
                        f = dict(forms[i])
                        f['t'] = f.get('t', Fr(0)) + (mj - mi)
                        if q in forms:
                            if norm(forms[q]) != norm(f):
                                break               # inconsistent cycle: handled by the check below
                        else:
                            forms[q] = f
                            stack.append(q)
        if len(forms) != len(labels):
            continue
        # consistency: every cube's points must be exactly theta apart as assigned
        consistent = True
        for x in T:
            ps = cube_pts[x]
            if len(ps) >= 2:
                d = sub(forms[ps[1]], forms[ps[0]])
                if norm(d) not in (norm({'t': Fr(1)}), norm({'t': Fr(-1)})):
                    consistent = False
        if consistent:
            yield forms, [v for v in sorted({k for f in forms.values() for k in f}) if k_is_param(v)]


def k_is_param(v):
    return v != '1'


def norm(f):
    return tuple(sorted((k, v) for k, v in f.items() if v != 0))


def sub(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Fr(0)) - v
    return out


def evalf(f, vals):
    return sum(v * (vals[k] if k != '1' else 1) for k, v in f.items())


# ---------------------------------------------------------------- cells

DOM = {'t': (Fr(120), Fr(180))}          # theta in (120, 180]; offsets in [0, 360]


def dom(v):
    return DOM.get(v, (Fr(0), Fr(360)))


def crit_forms(forms):
    labs = list(forms)
    out = []
    def add(f, c=0):
        g = dict(f); g['1'] = g.get('1', Fr(0)) + c; out.append(norm(g))
    for i in labs:
        add(forms[i]); add(forms[i], 180)
    for i, j in itertools.combinations(labs, 2):
        m = {k: (forms[i].get(k, Fr(0)) + forms[j].get(k, Fr(0))) / 2 for k in set(forms[i]) | set(forms[j])}
        add(m); add(m, 180)
    return sorted(set(out))


def lines(forms, params):
    """all conditions 'two critical directions coincide mod 360': (coeffs over params, value)"""
    cf = crit_forms(forms)
    out = set()
    for a, b in itertools.combinations(cf, 2):
        g = sub(dict(a), dict(b))
        coef = tuple(g.get(v, Fr(0)) for v in params)
        if not any(coef):
            continue
        c0 = g.get('1', Fr(0))
        # range of the linear part over the box
        lo = hi = Fr(0)
        for cv, v in zip(coef, params):
            a0, a1 = dom(v)
            lo += min(cv * a0, cv * a1); hi += max(cv * a0, cv * a1)
        import math
        for k in range(math.floor((lo + c0) / 360) - 1, math.ceil((hi + c0) / 360) + 2):
            out.add((coef, 360 * k - c0))       # coef . x = value
    return sorted(out)


def samples(forms, params):
    if not params:
        yield {}
        return
    L = lines(forms, params)
    if len(params) == 1:
        v = params[0]
        lo, hi = dom(v)
        xs = {lo, hi}
        for coef, val in L:
            x = val / coef[0]
            if lo <= x <= hi:
                xs.add(x)
        xs = sorted(xs)
        pts = set(xs) | {(a + b) / 2 for a, b in zip(xs, xs[1:])}
        for x in pts:
            yield {v: x}
        return
    assert len(params) == 2
    (lx, hx), (ly, hy) = dom(params[0]), dom(params[1])
    box = [((Fr(1), Fr(0)), lx), ((Fr(1), Fr(0)), hx), ((Fr(0), Fr(1)), ly), ((Fr(0), Fr(1)), hy)]
    allL = sorted(set(L) | set(box))
    inside = lambda p: lx <= p[0] <= hx and ly <= p[1] <= hy
    out = set()
    for i, (c1, v1) in enumerate(allL):
        on = []
        for j, (c2, v2) in enumerate(allL):
            if i == j:
                continue
            det = c1[0] * c2[1] - c1[1] * c2[0]
            if det == 0:
                continue
            p = ((v1 * c2[1] - v2 * c1[1]) / det, (c1[0] * v2 - c2[0] * v1) / det)
            if inside(p):
                on.append(p)
        on = sorted(set(on))
        out.update(on)
        for p, q in zip(on, on[1:]):
            m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
            out.add(m)
            # step off the edge on both sides, less than the distance to any other line
            nrm = c1
            eps = None
            for c2, v2 in allL:
                if (c2, v2) == (c1, v1):
                    continue
                g = c2[0] * m[0] + c2[1] * m[1] - v2
                rate = c2[0] * nrm[0] + c2[1] * nrm[1]
                if g != 0 and rate != 0:
                    e = abs(g / rate) / 2
                    eps = e if eps is None else min(eps, e)
            if eps is None:
                eps = Fr(1)
            for sgn in (1, -1):
                r = (m[0] + sgn * eps * nrm[0], m[1] + sgn * eps * nrm[1])
                if inside(r):
                    out.add(r)
    for p in out:
        yield dict(zip(params, p))


SEEN = set()


def merged_status(T, outer, owners, pos):
    """A sample where distinct points coincide is a configuration of a MERGED pattern.  It must be
    either unrealisable or one of the enumerated patterns."""
    from lowend_check import realisable
    groups = collections.defaultdict(set)
    for i, p in pos.items():
        groups[p] |= owners[i]
    merged = list(groups.values())
    cube_pts = {x: sum(x in o for o in merged) for x in T}
    if any(cube_pts[x] < sum(x in o for o in owners) for x in T):
        return 'unrealisable(cube_points_merge)'
    if any(len(a & b) > 1 for a, b in itertools.combinations(merged, 2)):
        return 'unrealisable(two_shared)'
    classes = sorted({''.join(sorted(o)) for o in merged if len(o) >= 2})
    if not realisable(classes):
        return 'unrealisable(structure)'
    singles = {next(iter(o)) for o in merged if len(o) == 1}
    if len(singles) > 1:
        return 'not_low_end'
    return 'enumerated' if canon(T, outer, [frozenset(o) for o in merged]) in SEEN else 'MISSING'


def evaluate(T, outer, owners, forms, vals):
    if 't' in vals and not (Fr(120) < vals['t'] <= Fr(180)):
        return 'out_of_domain'
    pos = {i: evalf(f, vals) % 360 for i, f in forms.items()}
    if len(set(pos.values())) < len(pos):
        return 'points_coincide:' + merged_status(T, outer, owners, pos)
    pts = {x: [pos[i] for i in pos if x in owners[i]] for x in T}
    iso = isolated(pts, outer)
    if iso:
        return 'ISOLATED_' + '_'.join(iso)
    r = exact_degrees(pts, outer)
    if r is None:
        return 'off_G'
    dG, dS = r
    if any(d < 2 for d in dS.values()):
        return 'B_degree_below_2'
    ex = (dG - 2) - sum(d - 2 for d in dS.values())
    if ex > 0:
        return 'excess_%d' % ex
    # sharpness: how close to failing (slack 0 = tight); the vertices of degree >= 3 are the ones
    # where (L) has content
    return 'deg%s_slack_%d' % ('>=3' if dG >= 3 else '<=2', -ex)


def order_type(forms, vals):
    """the cyclic order, with ties, of the critical directions at a parameter point"""
    cf = crit_forms(forms)
    v = [evalf(dict(f), vals) % 360 for f in cf]
    ranks = sorted(set(v))
    return tuple(ranks.index(x) for x in v)


def crosscheck(n=3000):
    """every order type random parameter values reach must be among the cell samples' types"""
    import random
    rnd = random.Random(7)
    miss = tot = 0
    detail = []
    for T, outer, owners, counts in patterns(False):
        for forms, params in placements(T, owners, False):
            if not params:
                continue
            def ok(v):
                return not ('t' in v and not (Fr(120) < v['t'] <= 180))
            cell = {order_type(forms, v) for v in samples(forms, params) if ok(v)}
            rand = set()
            for _ in range(n):
                v = {}
                for p in params:
                    v[p] = (Fr(120 * 89 + rnd.randrange(1, 60 * 89 + 1), 89) if p == 't'
                            else Fr(rnd.randrange(0, 360 * 97), 97))
                rand.add(order_type(forms, v))
            tot += 1
            extra = rand - cell
            detail.append((len(cell), len(rand), len(extra)))
            if extra:
                miss += 1
    return tot, miss, detail


# ---------------------------------------------------------------- main

def main():
    n, bad = validate()
    print('exact model vs grid model: %d configurations, %d disagree' % (n, bad), flush=True)
    assert bad == 0
    stats = collections.Counter()
    dims = collections.Counter()
    per = []
    fails = []
    allpat = [(c, p) for c in (False, True) for p in patterns(c)]
    for c, (T, outer, owners, counts) in allpat:
        SEEN.add(canon(T, outer, owners))
    for corner, (T, outer, owners, counts) in allpat:
        if True:
            for forms, params in placements(T, owners, corner):
                dims[(corner, len(params))] += 1
                st = collections.Counter()
                for vals in samples(forms, params):
                    r = evaluate(T, outer, owners, forms, vals)
                    st[r] += 1
                    if r.startswith('excess') or r == 'B_degree_below_2' or 'ISOLATED' in r or 'MISSING' in r:
                        fails.append({'owners': [sorted(o) for o in owners], 'outer': sorted(outer),
                                      'vals': {k: str(v) for k, v in vals.items()}, 'result': r})
                stats.update(st)
                per.append({'kind': 'four' if len(T) == 4 else 'triple',
                            'owners': [''.join(sorted(o)) for o in owners], 'params': params,
                            'samples': dict(st)})
    print('placements by (corner, number of parameters):', dict(sorted(dims.items())))
    print('cell samples:', dict(sorted(stats.items())))
    tot, miss, detail = crosscheck()
    print('order-type cross-check: %d placements, %d with a random order type the cells missed; '
          '(cell types, random types) per placement: %s' % (tot, miss, [(a, b) for a, b, _ in detail]))
    print('failures: %d' % len(fails))
    for f in fails[:10]:
        print('  ', f)
    json.dump({'placements': per, 'stats': dict(stats), 'failures': fails,
               'validation': {'n': n, 'disagree': bad},
               'order_type_crosscheck': {'placements': tot, 'missed': miss, 'detail': detail}},
              open(os.path.join(ROOT, 'data', 'residue_exact.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
