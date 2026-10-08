#!/usr/bin/env python3
"""The local charging inequality on the shared-plane locus, in the exact circle model.  [P418]

P404's charging is local.  With G' = Gamma minus the interior of its tie patches, and B'_S the same
for each triple, Euler's E - V = sum_v (deg(v)/2 - 1) turns

    E'_Gamma - V'_Gamma  <=  sum_S (E'_S - V'_S)  +  excess

into the pointwise statement, at every point v of G',

    (*)   deg_G'(v) - 2  <=  sum over triples S with v in G'_S of (deg_S(v) - 2),

with excess = the sum of the shortfalls, plus every B'_S having minimum degree >= 2, so that
uncharged vertices cost nothing.

**The circle model is exact near v ([P405], [P416]).** In the gnomonic chart, cube x's value is
`F + sigma_x(w)`, and sigma_x is governed by the points where x's active normals project onto ONE
circle.
- Every cube tying at v has a nonempty set of points.
- Cubes not tying at v are strictly outer or strictly inner, with a fixed rank nearby.
- In direction w, a tying cube's rank is set by the angular distance d_x(w) to its nearest point.
  The farther the nearest point, the larger the reach, so the cube is more OUTER.
- A shared face plane is two cubes owning the SAME point. That is the only new feature on the
  locus.

**Degree computation.** The tie set of a diagram, around v, is a closed subset of the circle of
directions.
- Each isolated tie direction is an edge of G' and counts 1.
- Each tie arc (a 2D patch sector) contributes its two boundary rays, 2.
- The whole circle means v is interior to a patch, so v is not on G'.

Exact arithmetic: the circle has N = 1440 units, points sit at multiples of 4, and every critical
direction is even. Sampling every unit therefore sees each open interval and each critical
direction.

**Configurations.**
- 'general': each tying cube gets 1-3 points anywhere.
- 'cube': realisable cubes only. All tying cubes share the value F, so a cube with two active faces
  has its two points theta(F) apart, cos theta = -F^2/(1-F^2), in [120, 180] degrees. Three points
  sit 120 degrees apart, and only when every two-point cube is also at 120.

**Shared points.**
- 'none' is the generic control and must reproduce P405: excess 0, min degree >= 2.
- 'pair': a and b share one point.
- 'two': a~b and c~d.
- 'hub': a~b and a~c, at different points of a.
- 'axis': a, b, c share one point.

**Must-fail control.** [P405]'s "blades": each tying cube's points sit on their own radius r_x,
so `sigma_x = r_x cos d_x`. That breaks the equal-radius property every argument here relies on,
and (*) must then fail.
- The control has no shared points, so it is computed in floating point, with each degree counted
  as the number of label changes around the circle.
- Two earlier controls were too weak and were replaced:
  - Γ at the wrong level fired 0-5 times in 300.
  - Per-cube distance offsets keep all slopes at +-1, which is what [P405]'s injection uses, and
    fired 0-16 times in 200.
**Identities asserted** (PROOF_SHARED §4). Both should hold whenever no three cubes tie in one
direction, which is guaranteed for zero or one shared point. The other patterns are reported, not
assumed.
- `k = 1`, `|T| = 3`: `deg top + deg bottom = sum over pairs of deg`.
- `k = 0`, `|T| = 4`: `sum_S deg B_S = deg middle + 2*C12`.

**Off-graph cases**, counted separately:
- `v` not on Γ;
- `v` interior to a patch;
- `v` an isolated point of Γ. This last must be 0, or the draft's no-isolated-points claim fails.

**Direction ties** (`--direction-ties`, data/patch_charging_local_dirties.json). These count the
directions where three or more cubes tie, in the one-shared-point rows. They document the
correction to PROOF_SHARED §4.

Output: data/patch_charging_local.json. The first run, sequential, without the identities or the split,
was stopped after 7 of 10 rows. Its log is kept as data/patch_charging_local_run1.log.
"""
import os, sys, json, random, itertools, math, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = 1440
CUBES = 'abcd'
TRIPLES = [''.join(t) for t in itertools.combinations(CUBES, 3)]
INF, NEG = 10 ** 6, -1


def cdist(x, y):
    d = abs(x - y) % N
    return min(d, N - d)


def tie_degree(tie):
    """(on_graph, degree): runs of True in the cyclic tie array; a run of length 1 is an isolated
    tie ray (1), a longer run a patch sector (2 boundary rays); all True = patch interior."""
    if all(tie):
        return False, 0
    if not any(tie):
        return False, 0
    start = tie.index(False)
    deg, run = 0, 0
    for i in range(1, N + 1):
        t = tie[(start + i) % N]
        if t:
            run += 1
        elif run:
            deg += 1 if run == 1 else 2
            run = 0
    return True, deg


def level_tie(dist, members, level, w):
    """In direction w, do the level-th and (level+1)-th most OUTER of `members` tie?"""
    ds = sorted((dist[x][w] for x in members), reverse=True)
    return ds[level - 1] == ds[level]


def analyse(pts, outer, gamma_level=2):
    """pts: {cube: set of positions} for tying cubes; outer: set of strictly outer cubes; the rest
    are strictly inner.  Returns None if v is not on G', else (deg_G, {S: deg_S for S with v on G'_S})."""
    dist = {}
    for x in CUBES:
        if x in pts:
            dist[x] = [min(cdist(w, p) for p in pts[x]) for w in range(N)]
        else:
            dist[x] = [INF if x in outer else NEG] * N
    def deg(members, level):
        tie = [level_tie(dist, members, level, w) for w in range(N)]
        return tie_degree(tie)
    onG, dG = deg(CUBES, gamma_level)
    if not onG:
        return None
    dS = {}
    for S in TRIPLES:
        on, d = deg(S, 2)
        if on:
            dS[S] = d
    return dG, dS


def blades_violation(rnd):
    """The must-fail control: random points, one radius per cube, no sharing; degrees by label
    changes (ties are measure-zero in floats, and there are no patches without shared points)."""
    T = set(rnd.sample(CUBES, rnd.choice([2, 3, 3, 4])))
    rest = [x for x in CUBES if x not in T]
    outer = {x for x in rest if rnd.random() < 0.5}
    pts = {x: [rnd.uniform(0, 2 * math.pi) for _ in range(rnd.randint(1, 3))] for x in T}
    rad = {x: rnd.uniform(0.3, 1.0) for x in T}
    def val(x, w):  # larger = more OUTER (smaller M)
        if x not in T:
            return 9.0 if x in outer else -9.0
        return -rad[x] * max(math.cos(w - p) for p in pts[x])
    def deg(members, j):
        lab = []
        for i in range(N):
            w = 2 * math.pi * i / N
            top = sorted(members, key=lambda x: -val(x, w))[:j]
            lab.append(frozenset(top))
        return sum(lab[i] != lab[i - 1] for i in range(N))
    dG = deg(CUBES, 2)
    if not dG:
        return False
    dS = [deg(S, 2) for S in TRIPLES]
    return dG - 2 > sum(d - 2 for d in dS if d)


def classify(pts, outer):
    """Why v is off G' (or 'on'), and the two identities where they apply.
    Returns (where, identity) with identity None (not applicable), True or False."""
    T = set(pts)
    dist = {}
    for x in CUBES:
        dist[x] = ([min(cdist(w, p) for p in pts[x]) for w in range(N)] if x in T
                   else [INF if x in outer else NEG] * N)
    def tieset(members, level):
        return [level_tie(dist, members, level, w) for w in range(N)]
    centre = sorted([INF if x in outer else (0 if x in T else NEG) for x in CUBES], reverse=True)
    on_gamma_at_v = centre[1] == centre[2]
    g = tieset(CUBES, 2)
    where = ('on' if any(g) and not all(g) else 'patch_interior' if all(g)
             else 'isolated' if on_gamma_at_v else 'off_gamma')
    k = len(outer)
    ident = None
    if k == 1 and len(T) == 3:
        Ts = sorted(T)
        top = tie_degree(tieset(Ts, 1))[1]
        bot = tie_degree(tieset(Ts, 2))[1]
        prs = sum(tie_degree(tieset(list(p), 1))[1] for p in itertools.combinations(Ts, 2))
        ident = top + bot == prs
    elif k == 0 and len(T) == 4:
        mid = tie_degree(tieset(CUBES, 2))[1]
        c12 = tie_degree(tieset(CUBES, 3))[1]
        bs = sum(tie_degree(tieset(S, 2))[1] for S in TRIPLES)
        ident = bs == mid + 2 * c12
    return where, ident


def direction_ties(pts, outer):
    """Directions where three or more tying cubes have equal distance.  Returns a Counter of
    types.
    - 'pair_same_side': two cubes tie on both sides of the direction (one shared point, nearest on
      both sides) and a third crosses them.  PROOF_SHARED §4 (corrected) says this is the ONLY
      type with one shared point, and that the fourth cube never joins it.
    - 'other': anything else."""
    T = sorted(pts)
    dist = {x: [min(cdist(w, p) for p in pts[x]) for w in range(N)] for x in T}
    out = collections.Counter()
    for w in range(0, N, 2):                      # critical directions are even
        vals = collections.defaultdict(list)
        for x in T:
            vals[dist[x][w]].append(x)
        for v, xs in vals.items():
            if len(xs) < 3:
                continue
            l, r = (w - 1) % N, (w + 1) % N
            both = [p for p in itertools.combinations(xs, 2)
                    if dist[p[0]][l] == dist[p[1]][l] and dist[p[0]][r] == dist[p[1]][r]]
            out['pair_same_side' if len(xs) == 3 and len(both) == 1 else 'other_%d' % len(xs)] += 1
    return out


def theta_units(F2):
    c = -F2 / (1 - F2)
    return int(round(math.degrees(math.acos(max(-1.0, min(1.0, c)))) * 4))


def config(rnd, kind, share):
    """Random tying set T, outer set, and points; the shared points imposed per `share`."""
    need = {'none': 2, 'pair': 2, 'two': 4, 'hub': 3, 'axis': 3}[share]
    forced = {'none': '', 'pair': 'ab', 'two': 'abcd', 'hub': 'abc', 'axis': 'abc'}[share]
    T = set(forced) | {x for x in CUBES if rnd.random() < 0.5}
    while len(T) < need:
        T.add(rnd.choice(CUBES))
    rest = [x for x in CUBES if x not in T]
    outer = {x for x in rest if rnd.random() < 0.5}
    used = set()
    def fresh():
        while True:
            p = 4 * rnd.randrange(N // 4)
            if p not in used:
                used.add(p); return p
    pts = {x: set() for x in T}
    shared = []
    if share in ('pair', 'two', 'hub', 'axis'):
        s = fresh(); shared.append(s); pts['a'].add(s); pts['b'].add(s)
        if share == 'axis':
            pts['c'].add(s)
    if share == 'two':
        s = fresh(); pts['c'].add(s); pts['d'].add(s)
    if share == 'hub':
        s = fresh(); pts['a'].add(s); pts['c'].add(s)
    if kind == 'general':
        for x in T:
            for _ in range(rnd.randint(0 if pts[x] else 1, 2)):
                pts[x].add(fresh())
    else:
        # one value F for every tying cube: two-point cubes have separation theta(F)
        corner = rnd.random() < 0.15
        th = 480 if corner else theta_units(rnd.uniform(1 / 3 + 1e-3, 1 / 2))
        th = 4 * round(th / 4)
        for x in T:
            k = rnd.choice([1, 1, 2, 3] if corner else [1, 1, 2])
            have = sorted(pts[x])
            if len(have) > k:
                return None
            if k == 1 and not have:
                pts[x].add(fresh())
            elif k >= 2:
                base = have[0] if have else fresh()
                pts[x].add(base)
                sign = rnd.choice([1, -1])
                cand = [(base + sign * th) % N] + ([(base - sign * th) % N] if k == 3 else [])
                if len(have) > 1 and not set(have[1:]) <= set(cand):
                    return None
                for c in cand:
                    if c in used and c not in pts[x]:
                        return None
                    used.add(c); pts[x].add(c)
    # a shared plane between two cubes is ONE shared point; two shared points = the same cube
    for x, y in itertools.combinations(T, 2):
        if len(pts[x] & pts[y]) > 1:
            return None
    return pts, outer


def row(args):
    kind, share, trials, seed = args
    rnd = random.Random(seed)
    stats = collections.Counter()
    worst = []
    n = 0
    while n < trials:
        c = config(rnd, kind, share)
        if c is None:
            continue
        pts, outer = c
        where, ident = classify(pts, outer)
        if ident is not None:
            stats['identity_%s' % ('ok' if ident else 'FAILS')] += 1
        r = analyse(pts, outer)
        n += 1
        if r is None:
            stats[where] += 1; continue
        dG, dS = r
        stats['on_G'] += 1
        if any(d < 2 for d in dS.values()):
            stats['B_min_degree_below_2'] += 1
        lhs, rhs = dG - 2, sum(d - 2 for d in dS.values())
        ex = max(0, lhs - rhs)
        stats['excess_%d' % ex] += 1
        if ex and len(worst) < 5:
            worst.append({'pts': {k: sorted(v) for k, v in pts.items()},
                          'outer': sorted(outer), 'deg_G': dG, 'deg_S': dS})
    # must-fail control: blades (one radius per cube)
    ctrl = sum(blades_violation(rnd) for _ in range(trials // 4))
    return '%s/%s' % (kind, share), {'stats': dict(stats), 'control_violations': ctrl,
                                     'control_trials': trials // 4, 'examples': worst}


def main_direction_ties(trials):
    """--direction-ties: count multi-cube direction ties in the one-shared-point rows, the
    correction to PROOF_SHARED §4 recorded in P418."""
    out = {}
    for i, kind in enumerate(('general', 'cube')):
        rnd = random.Random(4180 + i)
        tot, n = collections.Counter(), 0
        while n < trials:
            c = config(rnd, kind, 'pair')
            if c is None:
                continue
            n += 1
            d = direction_ties(*c)
            tot.update(d)
            tot['configs_with_any'] += bool(d)
        out[kind + '/pair'] = dict(tot)
        print('%-13s %s' % (kind + '/pair', dict(tot)), flush=True)
    json.dump(out, open(os.path.join(ROOT, 'data', 'patch_charging_local_dirties.json'), 'w'), indent=1)


def main():
    if '--direction-ties' in sys.argv:
        return main_direction_ties(int(sys.argv[-1]) if sys.argv[-1].isdigit() else 1000)
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    jobs = [(kind, share, trials, 418 + 10 * i + j)
            for i, kind in enumerate(('general', 'cube'))
            for j, share in enumerate(('none', 'pair', 'two', 'hub', 'axis'))]
    import multiprocessing as mp
    with mp.Pool(8) as p:
        res = p.map(row, jobs)
    out = dict(res)
    for k, v in res:
        print('%-13s %s   control violations %d of %d' % (k, dict(sorted(v['stats'].items())),
              v['control_violations'], v['control_trials']), flush=True)
    json.dump(out, open(os.path.join(ROOT, 'data', 'patch_charging_local.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
