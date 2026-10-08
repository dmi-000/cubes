#!/usr/bin/env python3
"""H1 of [P425] as a local, per-vertex statement, reduced to three finite checks.  [P428]

**Setting.** n = 5, no two cubes share a face plane. Take a point P on two or more cube
boundaries. Then:
- T is the set of cubes whose boundary contains P (t = |T| >= 2);
- c is the number of other cubes strictly containing P;
- the rest do not contain P.

In the circle model ([P405]), the cubes of T are ranked in each direction θ around P by the angular
distance to their nearest active point. The cubes containing P rank above all of T in every
direction near P, and the others below.

For a subset S and a level ℓ, P is on S's level-ℓ graph exactly when `|T∩S| >= 2` and
`1 <= ℓ − |C∩S| <= |T∩S| − 1`. Its weight there is `e_S/2 − 1`, where e_S counts the directions θ in
which S's ℓ-th and (ℓ+1)-th reach tie. Off the graph the weight is 0, and so is every tie
indicator.

**H1 at P.** The vertex's share of `slack2 + slack3` is

    Σ_tri w_S(2) + Σ_4 w_S(3) − [w(2) + w(3) + 2 w(4)]  =  Σ_θ Δ(θ)/2 − K(t, c)

The two pieces:
- Δ(θ) counts, at direction θ, the subsets whose level-ℓ_S reach ties, minus the full compound's
  ties at levels 2, 3, 4 (level 4 counted twice);
- K counts the subset terms on which P lies, minus the full terms (level 4 twice). It depends only
  on (t, c).

**Three finite checks give `Σ_θ Δ(θ) >= 2K`.**
1. For every weak order of T at θ, `Δ(θ) >= Σ_{r : ranks r, r+1 of T tie} Δpair(c + r − 1)`. Here
   Δpair(u) is Δ for a single pair tie with u cubes above it.
2. For each r in 1..t−1, `e(T, r) >= 2`, by argument: going once round P, the top-r set of T must
   return to where it started, so it cannot change exactly once. It cannot change zero times
   either, since then P would be an isolated tie point, and [P412] excludes those (no shared
   plane).
3. Ray counts. Besides `e(T, r) >= 2`:
   - **bottom:** `e(T, t−1) >= t`. The bottom level's rays are the colour changes of the cyclic
     point sequence ([P405]), and t colours change at least t times.
   - **next to bottom:** if `e(T, t−1) = t`, then `e(T, t−2) >= t` (for t >= 3). Exactly t colour
     changes means each cube's points form one contiguous block. In any direction, the nearest
     point of another colour is then in an adjacent block, so the two innermost cubes are always
     a pair of neighbouring blocks. At the switch between blocks i and i+1 the pair is {i, i+1}.
     So the pair runs through all t adjacent pairs, which are distinct for t >= 3, and it changes
     at least t times.
   The check: the minimum of `Σ_r Δpair(c + r − 1) e(T, r)` over ray counts allowed by these
   bounds is >= 2K(t, c). At t = 2 it must be an EQUALITY, otherwise every regular point of an arc
   would carry slack. That is a consistency check on the bookkeeping.

Then `Σ_θ Δ(θ) >= Σ_r e(T, r) Δpair(c + r − 1) >= 2K`, using Δpair >= 0.

(Corrected the same day: the first version of check 3 used only `e >= 2`, which is too weak. A
three-cube tie point has 3 rays per level, and that is exactly what makes its slack 0.)

**Exhaustive.** Every t from 2 to 5, every c from 0 to 5 − t, and every weak order of T.
**Oracle.** The per-type slacks measured in [P427] (`data/vertex_types_n5_slack.json`) must be
consistent with the bound.

Output: data/h1_local.json.
"""
import os, sys, json, itertools, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = 5


def subsets():
    tri = list(itertools.combinations(range(N), 3))
    four = list(itertools.combinations(range(N), 4))
    return [(S, 2, 1) for S in tri] + [(S, 3, 1) for S in four]


FULL = [(tuple(range(N)), 2, 1), (tuple(range(N)), 3, 1), (tuple(range(N)), 4, 2)]


def layout(t, c):
    """cube labels: 0..c-1 contain P, c..c+t-1 are T, the rest are outside"""
    C = set(range(c))
    T = list(range(c, c + t))
    return C, T


def on(S, l, C, T):
    ts = [x for x in S if x in T]
    j = l - len([x for x in S if x in C])
    return len(ts) >= 2 and 1 <= j <= len(ts) - 1


def K(t, c):
    C, T = layout(t, c)
    return sum(w for S, l, w in subsets() if on(S, l, C, T)) - sum(w for S, l, w in FULL if on(S, l, C, T))


def tie_at(S, l, C, T, blocks):
    """blocks: T's weak order at θ, a list of tied blocks from most outer down.
    Does S's l-th and (l+1)-th reach tie?"""
    rank = []                                   # (block index) per member of S, C first
    for x in S:
        if x in C:
            rank.append(-1)
        elif x in T:
            rank.append(next(i for i, b in enumerate(blocks) if x in b))
        else:
            rank.append(10 ** 6)
    rank.sort()
    if l >= len(rank):
        return False
    a, b = rank[l - 1], rank[l]
    return a == b and 0 <= a < 10 ** 6


def delta(C, T, blocks):
    return (sum(w for S, l, w in subsets() if tie_at(S, l, C, T, blocks))
            - sum(w for S, l, w in FULL if tie_at(S, l, C, T, blocks)))


def weak_orders(items):
    """all ordered set partitions"""
    items = list(items)
    if not items:
        yield []
        return
    for k in range(1, len(items) + 1):
        for first in itertools.combinations(items, k):
            rest = [x for x in items if x not in first]
            for tail in weak_orders(rest):
                yield [set(first)] + tail


def dpair(u):
    """Δ for one pair tie with u cubes above it (u containing cubes, or T-cubes ranked above)"""
    # realise: t = 2 + (u - c) ... simplest: take c = u, t = 2
    C, T = layout(2, u)
    return delta(C, T, [set(T)])


def main():
    DP = {u: dpair(u) for u in range(0, N - 1)}
    print('Δpair(u) for u = 0..3: %s' % DP)
    assert all(v >= 0 for v in DP.values())
    fail1, n1, tight1 = [], 0, 0
    table = []
    for t in range(2, N + 1):
        for c in range(0, N - t + 1):
            C, T = layout(t, c)
            for blocks in weak_orders(T):
                n1 += 1
                bound = 0
                r = 0
                for b in blocks:
                    # ranks r+1 .. r+|b| tie: adjacent tied pairs at ranks r+1..r+|b|-1
                    for i in range(len(b) - 1):
                        bound += DP[c + r + i]
                    r += len(b)
                d = delta(C, T, blocks)
                if d < bound:
                    fail1.append((t, c, [sorted(b) for b in blocks], d, bound))
                tight1 += d == bound and bound > 0
            k = K(t, c)
            s = sum(DP[c + r - 1] for r in range(1, t))
            # minimum of Σ_r Δpair(c+r-1) e_r over ray counts allowed by the lemmas:
            # e_r >= 2 (P412); e_{t-1} >= t (colour changes); e_{t-1} = t  =>  e_{t-2} >= t (t >= 3)
            best = None
            for es in itertools.product(range(2, t + 3), repeat=t - 1):
                e = dict(zip(range(1, t), es))
                if e[t - 1] < t or (t >= 3 and e[t - 1] == t and e[t - 2] < t):
                    continue
                v = sum(DP[c + r - 1] * e[r] for r in range(1, t))
                best = v if best is None else min(best, v)
            table.append({'t': t, 'c': c, 'K': k, 'sum_dpair': s, 'min_weighted_rays': best,
                          'ok': best >= 2 * k})
    print('check 1 (Δ >= Σ Δpair over tied adjacent ranks): %d weak orders, %d failures, %d tight with bound > 0'
          % (n1, len(fail1), tight1))
    for f in fail1[:10]:
        print('   FAIL t=%d c=%d order %s  Δ=%d < %d' % f)
    print('check 3 (min over allowed ray counts of Σ_r Δpair(c+r-1) e_r >= 2K(t, c)):')
    for row in table:
        print('   t=%d c=%d  2K=%2d  min Σ Δpair·e=%2d  %s%s' % (row['t'], row['c'], 2 * row['K'],
                                                          row['min_weighted_rays'],
                                                          'ok' if row['ok'] else 'FAIL',
                                                          '  (t=2: must be equal)' if row['t'] == 2 else ''))
    t2 = all(r['min_weighted_rays'] == 2 * r['K'] for r in table if r['t'] == 2)
    print('consistency (t = 2 equality): %s' % t2)
    # oracle: P427's measured vertex types on real compounds. With r = ℓ − c and e_r the measured
    # degree on full level ℓ, the formula Σ_r Δpair(c+r-1) e_r / 2 − K(t, c) must EQUAL the
    # measured per-vertex slack (slack2 + slack3) / count; and the ray lemmas must hold.
    from fractions import Fraction as Fr
    ty = json.load(open(os.path.join(ROOT, 'data', 'vertex_types_n5_slack.json')))['types']
    orc = []
    for on_, inside, degs, cnt, s2, s3 in ty:
        t, c = len(on_), inside
        if t < 2 or t + c > N:
            continue
        e = {r: degs[c + r - 1] for r in range(1, t) if c + r - 1 < len(degs)}
        pred = Fr(sum(DP[c + r - 1] * e[r] for r in e), 2) - K(t, c)
        meas = (Fr(s2) + Fr(s3)) / cnt
        lem = (all(e[r] >= 2 for r in e) and e[t - 1] >= t
               and (t < 3 or e[t - 1] != t or e[t - 2] >= t))
        orc.append({'type': [on_, inside, degs], 'count': cnt, 'predicted': str(pred), 'measured': str(meas),
                    'equal': pred == meas, 'ray_lemmas': lem})
    print('oracle vs P427 types: %d types, formula equals measured on %d, ray lemmas hold on %d'
          % (len(orc), sum(o['equal'] for o in orc), sum(o['ray_lemmas'] for o in orc)))
    for o in orc:
        if not (o['equal'] and o['ray_lemmas']):
            print('   MISMATCH', o)
    assert all(o['equal'] and o['ray_lemmas'] for o in orc)
    path = os.path.join(ROOT, 'data', 'h1_local.json')
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update({'dpair': DP, 'check1': {'orders': n1, 'failures': fail1, 'tight': tight1},
                'check3': table, 't2_equality': t2, 'oracle_p427': orc})
    json.dump(old, open(path, 'w'), indent=1, default=str)


if __name__ == '__main__' and '--direct' not in sys.argv:
    main()


# ------------------------------------------------------------------ direct check in the circle model
def circle_direct(trials=20000, seed=7):
    """Σ_θ Δ(θ)/2 − K(t, c) computed directly from exact circle configurations.

    Each cube of T owns 1 point (face), 2 points theta apart with theta in (120, 180] (edge) or 3
    points 120 apart (corner). Angles are Fractions with small denominators, so that degenerate
    coincidences (three or more cubes tying in one direction) occur often. Points are distinct (no
    shared plane). Ties are evaluated at every critical direction (points, antipodes, bisectors
    and their antipodes); ties elsewhere are impossible, since distance functions are linear
    between critical directions and two different lines meet at most once.
    Also records e(T, r) per level, for the remaining lemma."""
    import random
    from fractions import Fraction as Fr
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from residue_exact import cd, critical
    rnd = random.Random(seed)
    worst = {}
    lem = collections.Counter()
    fails = []
    for it in range(trials):
        t = rnd.choice((3, 3, 4, 4, 5))
        c = rnd.randint(0, N - t)
        C, T = layout(t, c)
        den = rnd.choice((1, 2, 3, 4, 6, 12))
        pts = {}
        used = set()
        okc = True
        for x in T:
            kind = rnd.choice(('f', 'f', 'e', 'e', 'k'))
            o = Fr(rnd.randrange(360 * den), den)
            if kind == 'f':
                ps = [o]
            elif kind == 'e':
                th = Fr(rnd.randrange(120 * den + 1, 180 * den + 1), den)
                ps = [o, o + th]
            else:
                ps = [o, o + 120, o + 240]
            ps = [p % 360 for p in ps]
            if used & set(ps):
                okc = False
                break
            used |= set(ps)
            pts[x] = ps
        if not okc:
            continue
        crit = critical(sorted(used))
        def blocks_at(w):
            ds = {x: min(cd(w, p) for p in pts[x]) for x in T}
            vals = sorted(set(ds.values()), reverse=True)
            return [set(x for x in T if ds[x] == v) for v in vals]
        tot = 0
        e = collections.Counter()
        for w in crit:
            b = blocks_at(w)
            tot += delta(C, T, b)
            r = 0
            for blk in b:
                for i in range(len(blk) - 1):
                    e[r + i + 1] += 1
                r += len(blk)
        # isolated tie point: some level with no rays is excluded by [P412]; record and skip
        if any(e[r] == 0 for r in range(1, t)):
            lem['skipped: a level with no rays'] += 1
            continue
        s = tot - 2 * K(t, c)
        key = (t, c)
        worst[key] = min(worst.get(key, 10 ** 9), s)
        if s < 0:
            fails.append({'t': t, 'c': c, 'pts': {x: [str(p) for p in v] for x, v in pts.items()},
                          'twice_slack': s, 'e': dict(e)})
        if e[t - 1] == t:
            lem[(t, 'bottom minimal', 'next level rays', e[t - 2] if t >= 2 else None)] += 1
    return worst, fails, lem


if __name__ == '__main__' and '--direct' in sys.argv:
    worst, fails, lem = circle_direct()
    print('direct per-vertex check, minimum of 2 x slack by (t, c): %s' % dict(sorted(worst.items())))
    print('failures: %d' % len(fails))
    for f in fails[:5]:
        print('   ', f)
    print('lemma data: %s' % dict(lem))
    d = json.load(open(os.path.join(ROOT, 'data', 'h1_local.json')))
    d['direct'] = {'worst_twice_slack': {str(k): v for k, v in worst.items()}, 'failures': fails[:50],
                   'n_failures': len(fails), 'lemma': {str(k): v for k, v in lem.items()}}
    json.dump(d, open(os.path.join(ROOT, 'data', 'h1_local.json'), 'w'), indent=1, default=str)
