#!/usr/bin/env python3
"""H1 at a shared point: the n = 5 charging inequality with tie patches, per vertex.  [P434]

**The statement.** For five cubes in which cubes 0 and 1 share a face plane (and no other pair
does), let `X′ = E′ − V′` for each level graph with the patch interiors removed ([P418]'s `G′`).
The one-pair chain ([P433] corrected) needs

    Σ_tri X′_S(2)  +  Σ_4 X′_S(3)   >=   X′2 + X′3 + 2 X′4,

which, as in [P428], follows if it holds at every point P, with P's weight in a graph being
`deg/2 − 1` when P is on it and 0 otherwise.

**With patches, the weight is computed from the circle, not from (t, c).** Near P, each graph's
tie set is a closed subset A of the circle of directions:
- P is on the closed tie set exactly when the level's two ranks tie AT P (all of T tie at P);
- if A is the whole circle, P is interior to a patch and NOT on `G′` (weight 0);
- otherwise P is on `G′`, with degree `Σ_θ e_A(θ)`, where `e_A(θ) = 1` if θ ∈ A and A does not
  contain both sides of θ ([P418]'s count of ends: an isolated ray and an arc end count alike).

**The circle model** ([P405], [P418]). Cubes in T own points on a circle; in direction θ a cube's
reach rank among T is set by the angular distance to its nearest point (farther = reaches
farther). Cubes containing P rank above T; cubes not containing P rank below. Cubes 0 and 1 are in
T and own a common point s (the projection of the shared face normal); no other point is shared.
- 'general': each cube owns 1 point, 2 points θ apart with θ in [120, 180], or 3 points 120 apart,
  with θ chosen independently per cube. This is a superset of what cubes can do.
- 'realisable': every cube of T has the same value F at P, so every two-point cube has the SAME
  separation θ(F); a corner forces θ = 120.
Angles are Fractions with small denominators, so multi-cube ties are frequent. Each tie set is read
off exactly at the critical directions (points, antipodes, bisectors and their antipodes) and at
the midpoints between consecutive ones; distance functions are linear between critical
directions.

**Controls.**
- Regression: with no shared point, the weights computed here must reproduce [P428]'s
  `Σ_θ Δ(θ) − 2K(t, c)` from `h1_local.py` on the same configuration, exactly. The two are
  different implementations (ends of tie sets here; tie indicators and a (t, c) table there).
- Patch interior: T = {0, 1} owning only s must weigh 0 in every graph.
- `--compare4`: the shared-point paths (sectors, whole circle), which the regression never reaches,
  compared per graph at n = 4 with patch_charging_local's independent implementation
  (data/h1_shared_local_compare4.json).
- Anomalies are counted, not skipped: P not on a graph whose circle tie set is nonempty, and P on a
  graph with degree 0 or 1 (an isolated or dangling point).

Output: data/h1_shared_local.json.
"""
import os, sys, json, random, itertools, collections, multiprocessing as mp
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from residue_exact import cd, critical
import h1_local as H

ROOT = os.path.dirname(os.path.dirname(HERE))
N = 5
GRAPHS = ([(S, 2, 1) for S in itertools.combinations(range(N), 3)] +
          [(S, 3, 1) for S in itertools.combinations(range(N), 4)] +
          [(tuple(range(N)), 2, -1), (tuple(range(N)), 3, -1), (tuple(range(N)), 4, -2)])
INF = 10 ** 9


def values(w, pts, C, n=N):
    """reach value per cube in direction w (None = the point P itself)"""
    v = {}
    for x in range(n):
        if x in C:
            v[x] = INF
        elif x in pts:
            v[x] = 0 if w is None else min(cd(w, p) for p in pts[x])
        else:
            v[x] = -INF
    return v


def ties(v, S, l):
    r = sorted((v[x] for x in S), reverse=True)
    return l < len(r) and r[l - 1] == r[l] and abs(r[l]) < INF


def weights(pts, C, graphs=GRAPHS, n=N):
    """per-graph (on, whole, deg) at P, and the anomaly flags"""
    allpts = sorted({p for ps in pts.values() for p in ps})
    crit = critical(allpts)
    mids = [(crit[i] + (crit[i + 1] if i + 1 < len(crit) else crit[0] + 360)) / 2 % 360
            for i in range(len(crit))]
    vc = [values(w, pts, C, n) for w in crit]
    vm = [values(w, pts, C, n) for w in mids]
    v0 = values(None, pts, C, n)
    out = []
    for S, l, m in graphs:
        tc = [ties(v, S, l) for v in vc]
        tm = [ties(v, S, l) for v in vm]       # tm[i]: open interval after crit[i]
        on = ties(v0, S, l)
        whole = all(tm)
        deg = sum(1 for i in range(len(crit)) if tc[i] and not (tm[i] and tm[i - 1]))
        out.append((S, l, m, on, whole, deg, any(tc)))
    return out


def slack2(pts, C):
    """twice P's share of the slack, and anomalies"""
    tot, anom = 0, collections.Counter()
    for S, l, m, on, whole, deg, anytie in weights(pts, C):
        if not on:
            if anytie:
                anom['tie near P but not at P'] += 1
            continue
        if whole:
            continue
        if deg < 2:
            anom['on G′ with degree %d' % deg] += 1
        tot += m * (deg - 2)
    return tot, anom


def config(rnd, kind, shared=True):
    den = rnd.choice((1, 2, 3, 4, 6, 12))
    role = {0: 'T', 1: 'T'}
    for x in range(2, N):
        role[x] = rnd.choice(('T', 'T', 'C', 'O'))
    T = [x for x in range(N) if role[x] == 'T']
    C = {x for x in range(N) if role[x] == 'C'}
    corner = rnd.random() < 0.2
    th = Fr(120) if corner else Fr(rnd.randrange(120 * den, 180 * den + 1), den)
    used = set()

    def fresh():
        while True:
            p = Fr(rnd.randrange(360 * den), den)
            if p not in used:
                used.add(p)
                return p
    pts = {}
    s = fresh() if shared else None
    for x in T:
        k = rnd.choice((1, 1, 2, 2, 3) if corner else (1, 1, 2, 2))
        if kind == 'general' and k == 2:
            sep = Fr(rnd.randrange(120 * den, 180 * den + 1), den)
        else:
            sep = th
        base = s if (shared and x in (0, 1)) else fresh()
        sign = rnd.choice((1, -1))
        ps = [base]
        if k >= 2:
            ps.append((base + sign * sep) % 360)
        if k == 3:
            ps.append((base - sign * sep) % 360)
        for p in ps[1:]:
            if p in used:
                return None
            used.add(p)
        pts[x] = ps
    return pts, C


def run(args):
    seed, trials, kind, shared = args
    rnd = random.Random(seed)
    worst = {}
    hist = collections.Counter()
    anom = collections.Counter()
    fails, regress = [], [0, 0]
    for _ in range(trials):
        cf = config(rnd, kind, shared)
        if cf is None:
            continue
        pts, C = cf
        s, a = slack2(pts, C)
        anom.update(a)
        T = sorted(pts)
        key = (len(T), len(C), tuple(len(pts[x]) for x in (0, 1)))
        worst[key] = min(worst.get(key, INF), s)
        hist[s] += 1
        if s < 0 and len(fails) < 30:
            fails.append({'pts': {x: [str(p) for p in v] for x, v in pts.items()}, 'C': sorted(C),
                          'twice_slack': s})
        if not shared:
            # regression against [P428]'s implementation; relabel C first, then T
            t, c = len(T), len(C)
            order = sorted(C) + T
            Cl, Tl = H.layout(t, c)
            ptl = {order.index(x): pts[x] for x in T}
            crit = critical(sorted({p for ps in pts.values() for p in ps}))
            tot = 0
            for w in crit:
                ds = {order.index(x): min(cd(w, p) for p in pts[x]) for x in T}
                vals = sorted(set(ds.values()), reverse=True)
                tot += H.delta(Cl, Tl, [set(y for y in ds if ds[y] == v) for v in vals])
            ref = tot - 2 * H.K(t, c)
            regress[0] += 1
            regress[1] += (ref != s)
    return {'worst': worst, 'hist': hist, 'anom': anom, 'fails': fails, 'regress': regress}


def compare4(trials=4000, seed=4):
    """Intermediate-object control for the SHARED-point code paths (sectors, whole circle), which
    the regression never reaches: at n = 4, per graph (the four triples at level 2 and the
    compound's level 2), compare (on G′, degree) with patch_charging_local's independent
    implementation ([P418]: a 1440-unit grid, runs of tie directions, all-true = patch interior).
    Integer-degree points, so every critical direction is a grid point."""
    import patch_charging_local as PC
    rnd = random.Random(seed)
    graphs = [(S, 2, 1) for S in itertools.combinations(range(4), 3)] + [(tuple(range(4)), 2, -1)]
    done, differ, kinds = 0, [], collections.Counter()
    for _ in range(trials):
        role = {0: 'T', 1: 'T', 2: rnd.choice('TTCO'), 3: rnd.choice('TTCO')}
        C = {x for x in role if role[x] == 'C'}
        T = [x for x in role if role[x] == 'T']
        corner = rnd.random() < 0.2
        th = 120 if corner else rnd.randint(120, 180)
        used, pts, ok = set(), {}, True
        s0 = rnd.randrange(360); used.add(s0)
        for x in T:
            k = rnd.choice((1, 1, 2, 2, 3) if corner else (1, 1, 2, 2))
            if x in (0, 1):
                base = s0
            else:
                base = rnd.randrange(360)
                if base in used:
                    ok = False; break
                used.add(base)
            sg = rnd.choice((1, -1))
            ps = [base] + ([(base + sg * th) % 360] if k >= 2 else []) + ([(base - sg * th) % 360] if k == 3 else [])
            for q in ps[1:]:
                if q in used:
                    ok = False
                used.add(q)
            pts[x] = ps
        if not ok:
            continue
        mine = weights({x: [Fr(q) for q in v] for x, v in pts.items()}, C, graphs, 4)
        dist = {}
        for x in range(4):
            if x in pts:
                dist[x] = [min(PC.cdist(w, 4 * q) for q in pts[x]) for w in range(PC.N)]
            else:
                dist[x] = [PC.INF if x in C else PC.NEG] * PC.N
        done += 1
        for S, l, m, on, whole, deg, anytie in mine:
            ton, tdeg = PC.tie_degree([PC.level_tie(dist, S, l, w) for w in range(PC.N)])
            a = (on and not whole, deg if (on and not whole) else 0)
            b = (ton, tdeg)
            kinds['whole' if whole else ('on' if a[0] else 'off')] += 1
            if a != b:
                differ.append({'pts': pts, 'C': sorted(C), 'S': S, 'mine': a, 'theirs': b})
    return done, differ, kinds


def config_multi(rnd, kind):
    """Any sharing pattern at P: each cube of T (2–5 cubes) builds its 1–3 points from a base that
    is, with probability 1/2, a point some other cube already owns. Constraints: two cubes share at
    most one point (two shared planes = the same cube). Triangles of three distinct shared points
    are rejected ([P419]: they force an identical pair); longer cycles are allowed, a superset.
    Small denominators make further coincidences frequent; they are kept if they respect the
    constraints."""
    den = rnd.choice((1, 2, 3, 4, 6))
    role = {x: rnd.choice(('T', 'T', 'T', 'C', 'O')) for x in range(N)}
    T = [x for x in range(N) if role[x] == 'T']
    if len(T) < 2:
        return None
    C = {x for x in range(N) if role[x] == 'C'}
    corner = rnd.random() < 0.2
    th = Fr(120) if corner else Fr(rnd.randrange(120 * den, 180 * den + 1), den)
    pts = {}
    for x in T:
        k = rnd.choice((1, 1, 2, 2, 3) if corner else (1, 1, 2, 2))
        sep = th if (kind == 'realisable' or k != 2) else Fr(rnd.randrange(120 * den, 180 * den + 1), den)
        owned = sorted({p for v in pts.values() for p in v})
        if owned and rnd.random() < 0.5:
            base = rnd.choice(owned)
        else:
            base = Fr(rnd.randrange(360 * den), den)
        sign = rnd.choice((1, -1))
        ps = [base]
        if k >= 2:
            ps.append((base + sign * sep) % 360)
        if k == 3:
            ps.append((base - sign * sep) % 360)
        if len(set(ps)) < len(ps):
            return None
        pts[x] = ps
    share = {}
    for x, y in itertools.combinations(T, 2):
        com = set(pts[x]) & set(pts[y])
        if len(com) > 1:
            return None
        if com:
            share[(x, y)] = next(iter(com))
    for x, y, z in itertools.combinations(T, 3):
        ps = [share.get((x, y)), share.get((x, z)), share.get((y, z))]
        if all(p is not None for p in ps) and len(set(ps)) == 3:
            return None
    return pts, C, share


def multi_sig(pts, share):
    """sharing pattern at P: multiplicities of shared points, and how many sharing cubes own more"""
    mult = collections.Counter()
    for x, ps in pts.items():
        for p in ps:
            mult[p] += 1
    sh = sorted((m for m in mult.values() if m >= 2), reverse=True)
    sharers = {x for e in share for x in e}
    extra = sum(1 for x in sharers if len(pts[x]) > 1)
    return '%s, sharers owning more: %d/%d' % (sh, extra, len(sharers))


def multi_run(args):
    seed, trials, kind = args
    rnd = random.Random(seed)
    worst, anom, fails, n = {}, collections.Counter(), [], 0
    for _ in range(trials):
        cf = config_multi(rnd, kind)
        if cf is None:
            continue
        pts, C, share = cf
        if len([1 for _ in share]) < 2 and not any(
                sum(p in v for v in pts.values()) >= 3 for p in {q for v in pts.values() for q in v}):
            continue                                  # at most one shared pair: done in [P435]
        s2, a = slack2(pts, C)
        anom.update(a)
        n += 1
        key = (len(pts), len(C), multi_sig(pts, share))
        worst[key] = min(worst.get(key, INF), s2)
        if s2 < 0 and len(fails) < 40:
            fails.append({'pts': {x: [str(p) for p in v] for x, v in pts.items()}, 'C': sorted(C), 'twice_slack': s2,
                          'sig': key})
    return n, worst, anom, fails


def reduced_run(args):
    """After Check 1′ (which holds for any sharing pattern), H1′ at P follows from
        R(P) = Σ_r e(T, r)·Δpair(c + r − 1) − 2K*  >=  0,
    with e(T, r) the ends of T's own level-r tie set and K* the weighted number of graphs that
    tie at P and are not whole. Measured here, per sharing pattern, together with the full slack."""
    seed, trials, kind = args
    rnd = random.Random(seed)
    worst, fails, n = {}, [], 0
    for _ in range(trials):
        cf = config_multi(rnd, kind)
        if cf is None:
            continue
        pts, C, share = cf
        T = tuple(sorted(pts))
        t, c = len(T), len(C)
        e = {}
        for S, l, m, on, whole, deg, anytie in weights(pts, set(), [(T, r, 1) for r in range(1, t)]):
            e[l] = 0 if whole else deg
        # K* with the full levels' weights: subsets +1, full levels −1, −1, −2
        ks = sum(m for S, l, m, on, whole, deg, anytie in weights(pts, C) if on and not whole)
        R = sum(e[r] * H.dpair(c + r - 1) for r in e) - 2 * ks
        n += 1
        key = (t, c, multi_sig(pts, share))
        worst[key] = min(worst.get(key, INF), R)
        if R < 0 and len(fails) < 40:
            fails.append({'pts': {x: [str(p) for p in v] for x, v in pts.items()}, 'C': sorted(C), 'R': R, 'e': e,
                          'Kstar': ks, 'sig': key})
    return n, worst, fails


def both_run(args):
    """Full per-vertex slack AND the reduced inequality R on the SAME configurations (all sharing
    patterns), and, where R < 0, the per-direction excess Δ′(θ) − rhs(θ) tabulated by the
    direction's (L, W, R) type, written relative to T's tied blocks."""
    import h1_shared_proof as HP
    seed, trials, kind = args
    rnd = random.Random(seed)
    full, red, n = {}, {}, 0
    excess = collections.Counter()
    fails = []
    for _ in range(trials):
        cf = config_multi(rnd, kind)
        if cf is None:
            continue
        pts, C, share = cf
        T = tuple(sorted(pts))
        t, c = len(T), len(C)
        s2, _ = slack2(pts, C)
        e = {l: (0 if whole else deg) for S, l, m, on, whole, deg, anytie in
             weights(pts, set(), [(T, r, 1) for r in range(1, t)])}
        ks = sum(m for S, l, m, on, whole, deg, anytie in weights(pts, C) if on and not whole)
        R = sum(e[r] * H.dpair(c + r - 1) for r in e) - 2 * ks
        n += 1
        key = (t, c, multi_sig(pts, share))
        full[key] = min(full.get(key, INF), s2)
        red[key] = min(red.get(key, INF), R)
        if s2 < 0 and len(fails) < 40:
            fails.append({'pts': {x: [str(p) for p in v] for x, v in pts.items()}, 'C': sorted(C), 'twice_slack': s2})
        if R < 0:
            allpts = sorted({p for ps in pts.values() for p in ps})
            crit = critical(allpts)
            mids = [(crit[i] + (crit[i + 1] if i + 1 < len(crit) else crit[0] + 360)) / 2 % 360
                    for i in range(len(crit))]
            def order(w):
                ds = {x: min(cd(w, p) for p in pts[x]) for x in T}
                vals = sorted(set(ds.values()), reverse=True)
                return [frozenset(x for x in T if ds[x] == v) for v in vals]
            Wm = [order(w) for w in mids]
            for i, w in enumerate(crit):
                W, L, Rr = order(w), Wm[i - 1], Wm[i]
                d = sum(m for S, l, m in HP.GRAPHS
                        if HP._tie(W, S, l, C) and not (HP._tie(L, S, l, C) and HP._tie(Rr, S, l, C)))
                rhs = sum(H.dpair(c + r - 1) for r in range(1, t)
                          if HP._tie(W, T, r, set()) and not (HP._tie(L, T, r, set()) and HP._tie(Rr, T, r, set())))
                if d - rhs > 0:
                    # type: block sizes of W, and for each tied block whether a side tie persists / switches
                    tied = [b for b in W if len(b) > 1]
                    def sides(b):
                        lt = [x for x in L if len(x) > 1 and x <= b]
                        rt = [x for x in Rr if len(x) > 1 and x <= b]
                        if lt and rt and set(lt) != set(rt):
                            return 'switch'
                        if lt and rt:
                            return 'both'
                        if lt or rt:
                            return 'one side'
                        return 'cross'
                    typ = (c, tuple(len(b) for b in W), tuple(sides(b) for b in tied))
                    excess[(typ, d - rhs)] += 1
    return n, full, red, excess, fails


def reduced2_run(args):
    """R′(P) = Σ_r (e(T, r) + σ(T, r))·Δpair(c + r − 1) − 2K*, where σ counts pair SWITCHES of T's
    level r (tie on both sides, by two different pairs). Check 1′ with pair-only switches holds
    exhaustively (h1_shared_proof.py --switch --pairs-only), so R′ >= 0 implies H1′ at P."""
    import h1_shared_proof as HP
    HP.PAIRS_ONLY = True
    seed, trials, kind = args
    rnd = random.Random(seed)
    worst, fails, n = {}, [], 0
    for _ in range(trials):
        cf = config_multi(rnd, kind)
        if cf is None:
            continue
        pts, C, share = cf
        T = tuple(sorted(pts))
        t, c = len(T), len(C)
        allpts = sorted({p for ps in pts.values() for p in ps})
        crit = critical(allpts)
        mids = [(crit[i] + (crit[i + 1] if i + 1 < len(crit) else crit[0] + 360)) / 2 % 360
                for i in range(len(crit))]
        def order(w):
            ds = {x: min(cd(w, p) for p in pts[x]) for x in T}
            vals = sorted(set(ds.values()), reverse=True)
            return [frozenset(x for x in T if ds[x] == v) for v in vals]
        Wm = [order(w) for w in mids]
        es = collections.Counter()
        for i, w in enumerate(crit):
            W, L, Rr = order(w), Wm[i - 1], Wm[i]
            for r in range(1, t):
                endr = HP._tie(W, T, r, set()) and not (HP._tie(L, T, r, set()) and HP._tie(Rr, T, r, set()))
                if endr or HP.switch(W, L, Rr, T, r):
                    es[r] += 1
        ks = sum(m for S, l, m, on, whole, deg, anytie in weights(pts, C) if on and not whole)
        R = sum(es[r] * H.dpair(c + r - 1) for r in range(1, t)) - 2 * ks
        n += 1
        key = (t, c, multi_sig(pts, share))
        worst[key] = min(worst.get(key, INF), R)
        if R < 0 and len(fails) < 40:
            fails.append({'pts': {x: [str(p) for p in v] for x, v in pts.items()}, 'C': sorted(C), 'R': R,
                          'e_plus_sigma': dict(es), 'Kstar': ks, 'sig': key})
    return n, worst, fails


def residue_profile(pts, C):
    """discrete features of a configuration: realisable-model dimension (sharing components of T
    minus 1, plus the common edge angle unless fixed by a corner or unused), the number of points
    with a single owner, and the cubes owning them"""
    T = sorted(pts)
    par = {x: x for x in T}
    def f(x):
        while par[x] != x:
            x = par[x]
        return x
    for x, y in itertools.combinations(T, 2):
        if set(pts[x]) & set(pts[y]):
            par[f(x)] = f(y)
    comps = len({f(x) for x in T})
    multi = [x for x in T if len(pts[x]) > 1]
    corner = any(len(pts[x]) == 3 for x in T)
    theta = 1 if (multi and not corner) else 0
    owners = collections.Counter(p for x in T for p in pts[x])
    single = [p for p, k in owners.items() if k == 1]
    single_cubes = sorted({x for x in T for p in pts[x] if owners[p] == 1})
    return {'dim': comps - 1 + theta, 'single_points': len(single), 'single_owner_cubes': len(single_cubes),
            'points': len(owners)}


def profile_run(args):
    """profile of every configuration with R′ < 0 (realisable kind only: common edge angle)"""
    import h1_shared_proof as HP
    HP.PAIRS_ONLY = True
    seed, trials = args
    rnd = random.Random(seed)
    prof = collections.Counter()
    allprof = collections.Counter()
    n = 0
    for _ in range(trials):
        cf = config_multi(rnd, 'realisable')
        if cf is None:
            continue
        pts, C, share = cf
        T = tuple(sorted(pts))
        t, c = len(T), len(C)
        allpts = sorted({p for ps in pts.values() for p in ps})
        crit = critical(allpts)
        mids = [(crit[i] + (crit[i + 1] if i + 1 < len(crit) else crit[0] + 360)) / 2 % 360
                for i in range(len(crit))]
        def order(w):
            ds = {x: min(cd(w, p) for p in pts[x]) for x in T}
            vals = sorted(set(ds.values()), reverse=True)
            return [frozenset(x for x in T if ds[x] == v) for v in vals]
        Wm = [order(w) for w in mids]
        es = collections.Counter()
        for i, w in enumerate(crit):
            W, L, Rr = order(w), Wm[i - 1], Wm[i]
            for r in range(1, t):
                endr = HP._tie(W, T, r, set()) and not (HP._tie(L, T, r, set()) and HP._tie(Rr, T, r, set()))
                if endr or HP.switch(W, L, Rr, T, r):
                    es[r] += 1
        ks = sum(m for S, l, m, on, whole, deg, anytie in weights(pts, C) if on and not whole)
        R = sum(es[r] * H.dpair(c + r - 1) for r in range(1, t)) - 2 * ks
        pr = residue_profile(pts, C)
        k = (pr['dim'], pr['single_owner_cubes'])
        allprof[k] += 1
        n += 1
        if R < 0:
            prof[k] += 1
    return n, prof, allprof


def u3_run(args):
    """configurations where >= 3 cubes own an unshared point: the bottom level's ends + pair
    switches against u + 1 (u = such cubes; + 1 when a shared point exists), and, when the bottom
    is minimal, the next level's ends + switches. Also R′ itself."""
    import h1_shared_proof as HP
    HP.PAIRS_ONLY = True
    seed, trials = args
    rnd = random.Random(seed)
    viol = collections.Counter()
    nextmin = {}
    n = 0
    ex = []
    for _ in range(trials):
        cf = config_multi(rnd, 'realisable' if seed % 2 else 'general')
        if cf is None:
            continue
        pts, C, share = cf
        T = tuple(sorted(pts))
        t, c = len(T), len(C)
        owners = collections.Counter(p for x in T for p in pts[x])
        u = len({x for x in T for p in pts[x] if owners[p] == 1})
        shared = any(k >= 2 for k in owners.values())
        if u < 3 or not shared:
            continue
        n += 1
        allpts = sorted(owners)
        crit = critical(allpts)
        mids = [(crit[i] + (crit[i + 1] if i + 1 < len(crit) else crit[0] + 360)) / 2 % 360
                for i in range(len(crit))]
        def order(w):
            ds = {x: min(cd(w, p) for p in pts[x]) for x in T}
            vals = sorted(set(ds.values()), reverse=True)
            return [frozenset(x for x in T if ds[x] == v) for v in vals]
        Wm = [order(w) for w in mids]
        es = collections.Counter()
        for i, w in enumerate(crit):
            W, L, Rr = order(w), Wm[i - 1], Wm[i]
            for r in range(1, t):
                endr = HP._tie(W, T, r, set()) and not (HP._tie(L, T, r, set()) and HP._tie(Rr, T, r, set()))
                if endr or HP.switch(W, L, Rr, T, r):
                    es[r] += 1
        if es[t - 1] < u + 1:
            viol['bottom < u + 1'] += 1
        for S, l, m, on, whole, deg, anytie in weights(pts, set(), [(T, r, 1) for r in range(1, t)]):
            if whole and 2 <= c + l <= 4:
                viol['a full level 2–4 is whole (K* > K)'] += 1
        ksr = sum(m for S, l, m, on, whole, deg, anytie in weights(pts, C) if on and not whole)
        if ksr > H.K(t, c):
            viol['K* > K(t, c)'] += 1
        if t >= 3 and es[t - 1] == u + 1:
            k = (t, c, u)
            nextmin[k] = min(nextmin.get(k, INF), es[t - 2])
        if any(es[r] < 2 for r in range(1, t)):
            viol['some level has < 2 (all hits so far are WHOLE levels, which have no ends; not a violation)'] += 1
            wh = {l: whole for S, l, m, on, whole, deg, anytie in weights(pts, set(), [(T, r, 1) for r in range(1, t)])}
            ex.append({'pts': {x: [str(p) for p in v] for x, v in pts.items()}, 'C': sorted(C),
                       'ends_plus_switches': dict(es), 'whole': wh})
    return n, viol, nextmin, ex


def whole_run(args):
    """which of T's own levels are ever whole (tie on the whole circle), for any sharing pattern,
    and what the cubes at the tied ranks own"""
    seed, trials = args
    rnd = random.Random(seed)
    seen = collections.Counter()
    ex = []
    n = 0
    for _ in range(trials):
        cf = config_multi(rnd, 'realisable' if seed % 2 else 'general')
        if cf is None:
            continue
        pts, C, share = cf
        T = tuple(sorted(pts))
        t = len(T)
        n += 1
        owners = collections.Counter(p for x in T for p in pts[x])
        u = len({x for x in T for p in pts[x] if owners[p] == 1})
        common = set.intersection(*[set(pts[x]) for x in T])
        only = sum(1 for x in T if len(pts[x]) == 1 and pts[x][0] in common)
        for S, l, m, on, whole, deg, anytie in weights(pts, set(), [(T, r, 1) for r in range(1, t)]):
            if whole:
                k = (t, l, u, 'common point' if common else 'no common point', only)
                seen[k] += 1
                if len(ex) < 5 and l >= 2:
                    ex.append({'pts': {x: [str(p) for p in v] for x, v in pts.items()}, 'level': l})
    return n, seen, ex


def lemma_run(args):
    """ray lemmas of PROOF_N5 Part 4 measured on random configurations: e(T, r) = ends of T's own
    level-r tie set, by case (i) a, b own only s; (ii) one of them owns more; (iii) both do."""
    seed, trials, kind = args
    rnd = random.Random(seed)
    viol, seen = collections.Counter(), collections.Counter()
    for _ in range(trials):
        cf = config(rnd, kind, True)
        if cf is None:
            continue
        pts, C = cf
        T = tuple(sorted(pts))
        t = len(T)
        if t < 3:
            continue
        ext = (len(pts[0]) > 1) + (len(pts[1]) > 1)
        case = ('i', 'ii', 'iii')[ext]
        e = {}
        for S, l, m, on, whole, deg, anytie in weights(pts, set(), [(T, r, 1) for r in range(1, t)]):
            e[l] = deg if not whole else None
        seen[case] += 1
        if any(e[r] is None for r in e):
            viol[(case, 'T level whole')] += 1
            continue
        if any(e[r] < 2 for r in e):
            viol[(case, 'R1')] += 1
        if case == 'i':
            if e[t - 1] < t - 1:
                viol[(case, 'R2_i')] += 1
            if t >= 4 and e[t - 2] < 4:
                viol[(case, 'R3_i')] += 1
        else:
            if e[t - 1] < t:
                viol[(case, 'R2')] += 1
            if e[t - 1] == t and e[t - 2] < 3:
                viol[(case, 'R3pp')] += 1
            if case == 'iii' and e[t - 1] < t + 1:
                viol[(case, 'R2 iii: bottom >= t+1')] += 1
    return seen, viol


def decomp_run(args):
    """PROOF_N5 Part 4.2's Step 1′ identity and Check 1′'s coverage, on real circle configurations.
    At each critical direction the triple (L, W, R) is read from the adjacent midpoints. Asserts:
    (a) 2·slack = Σ_θ Δ′(θ) − 2K*, with K* = K(t, c) in cases (ii)/(iii) and K_i(t, c) in (i)
        (the RULE, not a measured count);
    (b) L and R refine W, and only {0, 1} tie on a side;
    (c) Σ_θ Δ′ >= Σ_r e(T, r) Δpair(c + r − 1).
    Also the minimum of 2·slack per (t, c, case)."""
    import h1_shared_proof as HP
    seed, trials, kind = args
    rnd = random.Random(seed)
    bad = collections.Counter()
    mins = {}
    n = 0
    for _ in range(trials):
        cf = config(rnd, kind, True)
        if cf is None:
            continue
        pts, C = cf
        T = sorted(pts)
        t, c = len(T), len(C)
        case = ('i', 'ii', 'iii')[(len(pts[0]) > 1) + (len(pts[1]) > 1)]
        s2, _ = slack2(pts, C)
        allpts = sorted({p for ps in pts.values() for p in ps})
        crit = critical(allpts)
        mids = [(crit[i] + (crit[i + 1] if i + 1 < len(crit) else crit[0] + 360)) / 2 % 360
                for i in range(len(crit))]
        def order(w):
            ds = {x: min(cd(w, p) for p in pts[x]) for x in T}
            vals = sorted(set(ds.values()), reverse=True)
            return [set(x for x in T if ds[x] == v) for v in vals]
        Wm = [order(w) for w in mids]
        dsum, rsum = 0, 0
        for i, w in enumerate(crit):
            W, L, R = order(w), Wm[i - 1], Wm[i]
            # (b)
            pos = lambda O: {x: j for j, blk in enumerate(O) for x in blk}
            pw = pos(W)
            for O in (L, R):
                po = pos(O)
                if any(len(blk) > 1 and blk != {0, 1} for blk in O):
                    bad['side tie other than {a, b}'] += 1
                for x in T:
                    for y in T:
                        if pw[x] < pw[y] and not po[x] < po[y]:
                            bad['side order does not refine W'] += 1
            for S, l, m in HP.GRAPHS:
                if HP._tie(W, S, l, C) and not (HP._tie(L, S, l, C) and HP._tie(R, S, l, C)):
                    dsum += m
            for r in range(1, t):
                if HP._tie(W, tuple(T), r, set()) and not (HP._tie(L, tuple(T), r, set()) and HP._tie(R, tuple(T), r, set())):
                    rsum += H.dpair(c + r - 1)
        Kr = HP.K_case_i(t, c) if case == 'i' else H.K(t, c)
        if s2 != dsum - 2 * Kr:
            bad[('identity (a) fails', case, t, c)] += 1
        if dsum < rsum:
            bad['(c) fails'] += 1
        key = (t, c, case)
        mins[key] = min(mins.get(key, INF), s2)
        n += 1
    return n, bad, mins


def main():
    if '--whole' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(whole_run, [(sd, 8000) for sd in range(1100, 1116)])
        n, seen, ex = 0, collections.Counter(), []
        for a, b, e in rs:
            n += a; seen.update(b); ex += e
        print('%d configurations; whole T-levels by (t, level r, u, common point of all T, cubes owning only it):' % n, flush=True)
        for k, v in sorted(seen.items()):
            print('   ', k, v, flush=True)
        for e in ex[:5]:
            print('   example level >= 2:', e, flush=True)
        json.dump({'n': n, 'whole': {str(k): v for k, v in seen.items()}, 'examples': ex},
                  open(os.path.join(ROOT, 'data', 'h1_multi_whole.json'), 'w'), indent=1)
        return
    if '--u3' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(u3_run, [(sd, 8000) for sd in range(1000, 1016)])
        n, viol, nm, ex = 0, collections.Counter(), {}, []
        for a, b, c_, e_ in rs:
            n += a; viol.update(b); ex += e_
            for k, v in c_.items():
                nm[k] = min(nm.get(k, INF), v)
        print('configurations with >= 3 cubes owning an unshared point and a shared point: %d; violations %s'
              % (n, dict(viol)), flush=True)
        print('when the bottom is exactly u + 1: minimum next-level ends + switches by (t, c, u): %s' % sorted(nm.items()), flush=True)
        for e in ex[:8]:
            print('   level < 2:', e, flush=True)
        json.dump({'n': n, 'violations': dict(viol), 'next_min': {str(k): v for k, v in nm.items()}, 'examples': ex},
                  open(os.path.join(ROOT, 'data', 'h1_multi_u3.json'), 'w'), indent=1)
        return
    if '--profile' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(profile_run, [(sd, 6000) for sd in range(900, 916)])
        n, prof, allp = 0, collections.Counter(), collections.Counter()
        for a, b, c_ in rs:
            n += a; prof.update(b); allp.update(c_)
        print('realisable configurations: %d; R′ < 0 in %d' % (n, sum(prof.values())), flush=True)
        print('(dimension, cubes owning an unshared point): R′<0 count / all', flush=True)
        for k in sorted(allp):
            print('   ', k, prof.get(k, 0), '/', allp[k], flush=True)
        json.dump({'n': n, 'fail_profile': {str(k): v for k, v in prof.items()}, 'all_profile': {str(k): v for k, v in allp.items()}},
                  open(os.path.join(ROOT, 'data', 'h1_multi_profile.json'), 'w'), indent=1)
        return
    if '--reduced2' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(reduced2_run, [(sd, 6000, k) for sd, k in zip(range(800, 816), ['general', 'realisable'] * 8)])
        n, worst, fails = 0, {}, []
        for a, w, f in rs:
            n += a; fails += f
            for k, v in w.items():
                worst[k] = min(worst.get(k, INF), v)
        neg = {k: v for k, v in worst.items() if v < 0}
        print('R′ (ends + pair switches) on %d configurations, %d classes: negative in %d classes'
              % (n, len(worst), len(neg)), flush=True)
        for k, v in sorted(neg.items(), key=lambda kv: kv[1])[:40]:
            print('   ', k, v, flush=True)
        for f in fails[:6]:
            print('   example', f, flush=True)
        json.dump({'n': n, 'worst': {str(k): v for k, v in worst.items()}, 'fails': fails},
                  open(os.path.join(ROOT, 'data', 'h1_multi_reduced2.json'), 'w'), indent=1, default=str)
        return
    if '--both' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(both_run, [(sd, 25000, k) for sd, k in zip(range(700, 716), ['general', 'realisable'] * 8)])
        n, full, red, excess, fails = 0, {}, {}, collections.Counter(), []
        for a, f, r, ex, fl in rs:
            n += a; excess.update(ex); fails += fl
            for k, v in f.items():
                full[k] = min(full.get(k, INF), v)
            for k, v in r.items():
                red[k] = min(red.get(k, INF), v)
        negf = {k: v for k, v in full.items() if v < 0}
        negr = {k: v for k, v in red.items() if v < 0}
        print('%d configurations, %d classes: full slack negative in %d classes; reduced R negative in %d'
              % (n, len(full), len(negf), len(negr)), flush=True)
        for k, v in sorted(negf.items(), key=lambda kv: kv[1])[:20]:
            print('   FULL NEGATIVE', k, v, flush=True)
        print('on the R < 0 configurations, the excess Δ′ − rhs > 0 sits at these direction types (c, W block sizes, tied-block side behaviour), excess: count', flush=True)
        for (typ, x), v in excess.most_common(40):
            print('   ', typ, x, v, flush=True)
        json.dump({'n': n, 'full_min': {str(k): v for k, v in full.items()}, 'reduced_min': {str(k): v for k, v in red.items()},
                   'excess_types': [[str(k), v] for k, v in excess.most_common()], 'full_fails': fails},
                  open(os.path.join(ROOT, 'data', 'h1_multi_both.json'), 'w'), indent=1, default=str)
        return
    if '--reduced' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(reduced_run, [(sd, 8000, k) for sd, k in zip(range(600, 616), ['general', 'realisable'] * 8)])
        n, worst, fails = 0, {}, []
        for a, w, f in rs:
            n += a; fails += f
            for k, v in w.items():
                worst[k] = min(worst.get(k, INF), v)
        neg = {k: v for k, v in worst.items() if v < 0}
        print('reduced inequality R(P) >= 0 on %d configurations (all sharing patterns), %d classes; negative in %d'
              % (n, len(worst), len(neg)), flush=True)
        for k, v in sorted(neg.items(), key=lambda kv: kv[1])[:40]:
            print('   ', k, v, flush=True)
        for f in fails[:6]:
            print('   example', f, flush=True)
        json.dump({'n': n, 'worst': {str(k): v for k, v in worst.items()}, 'fails': fails},
                  open(os.path.join(ROOT, 'data', 'h1_multi_reduced.json'), 'w'), indent=1, default=str)
        return
    if '--multi' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(multi_run, [(sd, 8000, k) for sd, k in zip(range(500, 516), ['general', 'realisable'] * 8)])
        n, worst, anom, fails = 0, {}, collections.Counter(), []
        for a, w, an, f in rs:
            n += a; anom.update(an); fails += f
            for k, v in w.items():
                worst[k] = min(worst.get(k, INF), v)
        neg = {k: v for k, v in worst.items() if v < 0}
        print('two or more shared points at P: %d configurations, %d (t, c, pattern) classes; anomalies %s'
              % (n, len(worst), dict(anom)), flush=True)
        print('classes with negative 2·slack: %d' % len(neg), flush=True)
        for k, v in sorted(neg.items(), key=lambda kv: kv[1])[:30]:
            print('   ', k, v, flush=True)
        for f in fails[:5]:
            print('   example', f, flush=True)
        json.dump({'n': n, 'worst': {str(k): v for k, v in worst.items()}, 'anomalies': dict(anom), 'fails': fails},
                  open(os.path.join(ROOT, 'data', 'h1_multi_local.json'), 'w'), indent=1, default=str)
        return
    if '--decomp' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(decomp_run, [(sd, 4000, k) for sd, k in zip(range(400, 416), ['general', 'realisable'] * 8)])
        n, bad, mins = 0, collections.Counter(), {}
        for a, b, m in rs:
            n += a; bad.update(b)
            for k, v in m.items():
                mins[k] = min(mins.get(k, INF), v)
        print('Step 1′ identity and Check 1′ coverage on %d shared-point configurations: problems %s' % (n, dict(bad)), flush=True)
        print('minimum 2·slack by (t, c, case): %s' % sorted(mins.items()), flush=True)
        json.dump({'n': n, 'problems': {str(k): v for k, v in bad.items()}, 'min_twice_slack': {str(k): v for k, v in mins.items()}},
                  open(os.path.join(ROOT, 'data', 'h1_shared_local_decomp.json'), 'w'), indent=1)
        return
    if '--lemmas' in sys.argv:
        with mp.Pool(8) as p:
            rs = p.map(lemma_run, [(sd, 5000, k) for sd, k in zip(range(300, 316), ['general', 'realisable'] * 8)])
        seen, viol = collections.Counter(), collections.Counter()
        for a, b in rs:
            seen.update(a); viol.update(b)
        print('ray lemmas on random shared-point configurations (t >= 3): by case %s; violations %s'
              % (dict(seen), dict(viol)), flush=True)
        json.dump({'seen': dict(seen), 'violations': {str(k): v for k, v in viol.items()}},
                  open(os.path.join(ROOT, 'data', 'h1_shared_local_lemmas.json'), 'w'), indent=1)
        return
    if '--compare4' in sys.argv:
        done, differ, kinds = compare4()
        print('n = 4 per-graph comparison with patch_charging_local: %d configurations, graph kinds %s, %d graphs differ'
              % (done, dict(kinds), len(differ)), flush=True)
        for d in differ[:5]:
            print('   ', d)
        json.dump({'configurations': done, 'kinds': dict(kinds), 'differ': differ[:50], 'n_differ': len(differ)},
                  open(os.path.join(ROOT, 'data', 'h1_shared_local_compare4.json'), 'w'), indent=1, default=str)
        return
    patch = slack2({0: [Fr(10)], 1: [Fr(10)]}, set())
    print('patch interior control (T = {0,1}, only s): twice slack %d, anomalies %s' % patch, flush=True)
    res = {}
    for kind, shared, seeds in (('general', False, range(0, 8)), ('general', True, range(100, 116)),
                                ('realisable', True, range(200, 216))):
        with mp.Pool(8) as p:
            rs = p.map(run, [(sd, 6000, kind, shared) for sd in seeds])
        worst, hist, anom, fails, reg = {}, collections.Counter(), collections.Counter(), [], [0, 0]
        for r in rs:
            for k, v in r['worst'].items():
                worst[k] = min(worst.get(k, INF), v)
            hist.update(r['hist']); anom.update(r['anom']); fails += r['fails']
            reg[0] += r['regress'][0]; reg[1] += r['regress'][1]
        name = '%s, %s' % (kind, 'shared point' if shared else 'no shared point')
        print('%s: %d configurations; twice-slack histogram %s' % (name, sum(hist.values()), sorted(hist.items())), flush=True)
        print('   minimum by (t, c, points of cubes 0 and 1): %s' % sorted(worst.items()), flush=True)
        print('   failures %d; anomalies %s' % (sum(v for k, v in hist.items() if k < 0), dict(anom)), flush=True)
        if not shared:
            print('   regression against h1_local: %d compared, %d differ' % tuple(reg), flush=True)
        res[name] = {'hist': dict(hist), 'worst': {str(k): v for k, v in worst.items()},
                     'anomalies': dict(anom), 'fails': fails[:30], 'regression': reg}
    res['patch_interior_control'] = list(patch[:1]) + [dict(patch[1])]
    json.dump(res, open(os.path.join(ROOT, 'data', 'h1_shared_local.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
