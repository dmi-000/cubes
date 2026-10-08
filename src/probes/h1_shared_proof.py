#!/usr/bin/env python3
"""H1 at a shared point: the finite checks of a proof.  [P435]

Setting as in `h1_shared_local.py` ([P434]): n = 5, cubes a and b of T own a common point s on the
circle around P. Three cases:
- (i) a and b own only s. They have the same distance function, and some graphs tie on the whole
  circle.
- (ii) exactly one of a, b owns more than s.
- (iii) both do.

In (ii) and (iii) no graph ties on the whole circle: two cubes have the same distance function only
if they own the same points. Then P is on a graph exactly when the graph's ranks tie at P, as in
[P428]. So `K(t, c)` is [P428]'s, and

    2·slack  =  Σ_θ Δ′(θ) − 2K(t, c),      Δ′(θ) = Σ_g m_g e_g(θ),

with `e_g(θ) = 1` when θ is an END of g's tie set: g ties at θ, but not on both sides.

**Check 1′** (`--check1`). At a direction θ, the local picture is a triple (L, W, R):
- W is T's weak order at θ;
- L and R are the orders just to the left and right, both refinements of W by continuity;
- only {a, b} may tie on a side (a sector), since every other tie is isolated ([P418] §3).

The claim is that for every such triple

    Δ′(θ)  >=  Σ_r e_{T,r}(θ) · Δpair(c + r − 1),

where `e_{T,r}(θ)` is the end indicator of T's own level-r tie set and Δpair is [P428]'s
(0, 0, 2, 4). Summing over θ gives `Σ_θ Δ′ >= Σ_r e(T, r) Δpair(c + r − 1)`, with `e(T, r)` now
counting ENDS. The enumeration covers a superset of the triples that occur: it does not impose the
crossing condition on other pairs.

**Step 4 table** (`--table`). If the ray lemmas R1–R3 of [P428] hold with ends in place of tie
directions, [P428]'s table applies unchanged. This also records which rows need R3, by
minimising with R1 and R2 only.

Output: data/h1_shared_proof.json.
"""
import os, sys, json, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import h1_local as H

ROOT = os.path.dirname(os.path.dirname(HERE))
N = 5


def _tie(order, S, l, C):
    """order: weak order of T (list of sets, most outer first); C: cubes containing P.
    Do S's l-th and (l+1)-th reaches tie?"""
    rank = []
    for x in S:
        if x in C:
            rank.append(-1)
        else:
            idx = next((i for i, b in enumerate(order) if x in b), None)
            rank.append(10 ** 6 if idx is None else idx)
    rank.sort()
    if l >= len(rank):
        return False
    u, v = rank[l - 1], rank[l]
    return u == v and 0 <= u < 10 ** 6


def refinements(order, allowed):
    """weak orders refining `order` (each block split into an ordered partition) in which a block
    of size > 1 must equal `allowed`"""
    parts = []
    for blk in order:
        opts = []
        for wo in H.weak_orders(sorted(blk)):
            if all(len(x) == 1 or allowed == 'any' or (allowed is None and len(x) == 2) or x == allowed for x in wo):
                opts.append(wo)
        parts.append(opts)
    for combo in itertools.product(*parts):
        yield [b for wo in combo for b in wo]


GRAPHS = H.subsets() + [(S, l, -w) for S, l, w in H.FULL]


def _block_at(order, r):
    """the block of the weak order containing T-rank r (1 = most outer)"""
    k = 0
    for b in order:
        if k < r <= k + len(b):
            return frozenset(b)
        k += len(b)
    return None


def switch(W, L, R, T, r):
    """σ_{T,r}(θ): T's level r ties at θ and on both sides, but the tied blocks on the two sides
    are not nested (the tie runs through θ while its pair switches). A pair growing into a larger
    tied block is not a switch (first definition, 2026-10-07, counted it and failed spuriously)."""
    if not (_tie(W, T, r, set()) and _tie(L, T, r, set()) and _tie(R, T, r, set())):
        return False
    bl, br = _block_at(L, r), _block_at(R, r)
    if PAIRS_ONLY and (len(bl) != 2 or len(br) != 2):
        return False
    return not (bl <= br or br <= bl)          # genuinely different pairs, not one tie growing


PAIRS_ONLY = '--pairs-only' in sys.argv


def check1s(t, c):
    """Check 1′ with switches: Δ′(θ) >= Σ_r (e_{T,r}(θ) + σ_{T,r}(θ))·Δpair(c + r − 1), any side ties"""
    C, T = H.layout(t, c)
    worst, n, fails = None, 0, []
    for W in H.weak_orders(T):
        Ls = list(refinements(W, 'any'))
        for L in Ls:
            for R in Ls:
                d = sum(m for S, l, m in GRAPHS if _tie(W, S, l, C) and not (_tie(L, S, l, C) and _tie(R, S, l, C)))
                rhs = 0
                for r in range(1, t):
                    endr = _tie(W, T, r, set()) and not (_tie(L, T, r, set()) and _tie(R, T, r, set()))
                    if endr or switch(W, L, R, T, r):
                        rhs += H.dpair(c + r - 1)
                n += 1
                if worst is None or d - rhs < worst:
                    worst = d - rhs
                if d < rhs and len(fails) < 10:
                    fails.append({'W': [sorted(x) for x in W], 'L': [sorted(x) for x in L], 'R': [sorted(x) for x in R],
                                  'delta': d, 'rhs': rhs})
    return {'t': t, 'c': c, 'triples': n, 'min': worst, 'fails': fails}


def top_set(order, r):
    """the top-r set of a weak order, or None when ranks r, r+1 tie (no label)"""
    if _tie(order, tuple(x for b in order for x in b), r, set()):
        return None
    out, k = set(), 0
    for b in order:
        if k >= r:
            break
        out |= set(b); k += len(b)
    return frozenset(out)


def touching(W, L, R):
    """a pair tied at θ, strict on both sides, in the SAME order: impossible. The distance
    difference would turn round at θ, which needs both cubes' distance 0 there, i.e. a common
    point at θ, and then they tie on both sides."""
    def pos(O):
        return {x: j for j, b in enumerate(O) for x in b}
    pw, pl, pr = pos(W), pos(L), pos(R)
    xs = list(pw)
    for x, y in itertools.combinations(xs, 2):
        if pw[x] == pw[y] and pl[x] != pl[y] and pr[x] != pr[y]:
            if (pl[x] < pl[y]) == (pr[x] < pr[y]):
                return True
    return False


def isolated_label_check(t):
    """For every (L, W, R) with any side ties: if T's level r ties at θ (W) but on NEITHER side,
    the top-r labels of L and R differ. This is the local fact R1 needs: an isolated tie changes
    the label."""
    T = list(range(t))
    bad, n = [], 0
    for W in H.weak_orders(T):
        Ls = list(refinements(W, 'any'))
        for L in Ls:
            for R in Ls:
                if touching(W, L, R):
                    continue
                for r in range(1, t):
                    if _tie(W, T, r, set()) and not _tie(L, T, r, set()) and not _tie(R, T, r, set()):
                        n += 1
                        if top_set(L, r) == top_set(R, r):
                            if len(bad) < 10:
                                bad.append({'W': [sorted(x) for x in W], 'L': [sorted(x) for x in L],
                                            'R': [sorted(x) for x in R], 'r': r})
    return n, bad


def check1(t, c, anypair=False, anyblock=False):
    C, T = H.layout(t, c)
    a, b = T[0], T[1]
    ab = 'any' if anyblock else (None if anypair else {a, b})
    worst, n, tight = None, 0, 0
    fails = []
    for W in H.weak_orders(T):
        Ls = list(refinements(W, ab))
        for L in Ls:
            for R in Ls:
                d = 0
                for S, l, m in GRAPHS:
                    if _tie(W, S, l, C) and not (_tie(L, S, l, C) and _tie(R, S, l, C)):
                        d += m
                rhs = 0
                for r in range(1, t):
                    if _tie(W, T, r, set()) and not (_tie(L, T, r, set()) and _tie(R, T, r, set())):
                        rhs += H.dpair(c + r - 1)
                n += 1
                s = d - rhs
                if worst is None or s < worst:
                    worst = s
                if s == 0 and rhs > 0:
                    tight += 1
                if s < 0 and len(fails) < 20:
                    fails.append({'W': [sorted(x) for x in W], 'L': [sorted(x) for x in L],
                                  'R': [sorted(x) for x in R], 'delta': d, 'rhs': rhs})
    return {'t': t, 'c': c, 'triples': n, 'min': worst, 'tight_positive': tight, 'fails': fails}


def table():
    """[P428]'s Step 4 minimisation, with R1 and R2 only, and with R3 as well"""
    rows = []
    for t in range(2, N + 1):
        for c in range(0, N - t + 1):
            dp = [H.dpair(c + r - 1) for r in range(1, t)]
            best12 = sum(d * 2 for d in dp[:-1]) + dp[-1] * t
            # with R3: if bottom = t, next >= t
            alt = [sum(d * 2 for d in dp[:-1]) + dp[-1] * (t + 1)]
            if t >= 3:
                alt.append(sum(d * 2 for d in dp[:-2]) + dp[-2] * t + dp[-1] * t)
            else:
                alt.append(best12)
            rows.append({'t': t, 'c': c, '2K': 2 * H.K(t, c), 'min_R1R2': best12, 'min_R1R2R3': min(alt)})
            print('t=%d c=%d: 2K = %d, min with R1,R2 = %d, with R3 = %d' % (t, c, 2 * H.K(t, c), best12, min(alt)))
    return rows


def K_case_i(t, c):
    """K for case (i): a, b own only s. A graph (S, l) is whole-circle exactly when S ∩ T = {a, b}
    and l − |S ∩ C| = 1: every other cube of T is above a = b somewhere (at s) and below somewhere
    (at its own point). Whole graphs carry no weight and no ends."""
    C, T = H.layout(t, c)
    ab = {T[0], T[1]}
    k = 0
    for S, l, m in GRAPHS:
        if not H.on(S, l, C, T):
            continue
        if set(S) & set(T) == ab and l - len(set(S) & C) == 1:
            continue
        k += m
    return k


def table_case_i():
    """case (i): Check 1′ applies unchanged (a = b on every side is among its triples). R1 holds;
    the bottom level gives only e(T, t−1) >= t − 1 (s is one point carrying both colours)."""
    rows = []
    for t in range(3, N + 1):
        for c in range(0, N - t + 1):
            dp = [H.dpair(c + r - 1) for r in range(1, t)]
            m = sum(d * 2 for d in dp[:-1]) + dp[-1] * max(2, t - 1)
            rows.append({'t': t, 'c': c, '2K_i': 2 * K_case_i(t, c), 'min_R1R2i': m})
            print('case (i) t=%d c=%d: 2K_i = %d, min with R1 and e(T,t-1) >= t-1: %d' % (t, c, 2 * K_case_i(t, c), m))
    return rows


def table_final():
    """the Step 4 minimisation with exactly the lemmas proved in PROOF_N5 Part 4:
    cases (ii)/(iii): R1 e(T,r) >= 2; R2 e(T,t−1) >= t; R3″ if e(T,t−1) = t and t >= 3 then
      e(T,t−2) >= 3.  Compared with 2K(t, c).
    case (i): R1; R2_i e(T,t−1) >= t − 1; R3_i if t >= 4 then e(T,t−2) >= 4.  Compared with 2K_i."""
    rows, ok = [], True
    for t in range(3, N + 1):
        for c in range(0, N - t + 1):
            dp = [H.dpair(c + r - 1) for r in range(1, t)]
            def val(lo):
                return sum(d * e for d, e in zip(dp, lo))
            base = [2] * (t - 1)
            # (ii)/(iii)
            a1 = base[:]; a1[-1] = t
            if t >= 3:
                a1[-2] = max(a1[-2], 3)
            a2 = base[:]; a2[-1] = t + 1
            m23 = min(val(a1), val(a2))
            # (i)
            b1 = base[:]; b1[-1] = max(2, t - 1)
            if t >= 4:
                b1[-2] = 4
            mi = val(b1)
            r = {'t': t, 'c': c, '2K': 2 * H.K(t, c), 'min_ii_iii': m23, '2K_i': 2 * K_case_i(t, c), 'min_i': mi}
            ok &= m23 >= r['2K'] and mi >= r['2K_i']
            rows.append(r)
            print('t=%d c=%d: cases (ii)/(iii) min %d vs 2K %d; case (i) min %d vs 2K_i %d' % (t, c, m23, r['2K'], mi, r['2K_i']))
    print('all rows hold: %s' % ok)
    return rows, ok


def defect_control():
    """injected defect: Δpair shifted by one rank (c + r instead of c + r − 1). The gate must fail."""
    orig = H.dpair
    H.dpair = lambda u: orig(min(u + 1, 3))
    try:
        fails = 0
        for t in range(3, N + 1):
            for c in range(0, N - t + 1):
                fails += len(check1(t, c)['fails'])
    finally:
        H.dpair = orig
    print('injected-defect control (Δpair shifted one rank): %d failing triples (must be > 0)' % fails)
    return fails


def main():
    if '--isolated' in sys.argv:
        out = {}
        for t in range(2, N + 1):
            n, bad = isolated_label_check(t)
            out[t] = {'isolated_ties': n, 'label_unchanged': bad}
            print('t=%d: %d isolated level ties over all (L, W, R); label unchanged in %d' % (t, n, len(bad)), flush=True)
            for b in bad[:4]:
                print('   ', b, flush=True)
        d = json.load(open(os.path.join(ROOT, 'data', 'h1_shared_proof.json')))
        d['isolated_label'] = {str(k): v for k, v in out.items()}
        json.dump(d, open(os.path.join(ROOT, 'data', 'h1_shared_proof.json'), 'w'), indent=1)
        return
    if '--switch' in sys.argv:
        out = []
        for t in range(2, N + 1):
            for c in range(0, N - t + 1):
                r = check1s(t, c)
                out.append(r)
                print('Check 1′ with switches, any side ties, t=%d c=%d: %d triples, min %s, failures %d'
                      % (t, c, r['triples'], r['min'], len(r['fails'])), flush=True)
                for f in r['fails'][:3]:
                    print('   ', f, flush=True)
        d = json.load(open(os.path.join(ROOT, 'data', 'h1_shared_proof.json')))
        d['check1_switch' + ('_pairs_only' if PAIRS_ONLY else '')] = out
        json.dump(d, open(os.path.join(ROOT, 'data', 'h1_shared_proof.json'), 'w'), indent=1)
        return
    if '--anyblock' in sys.argv:
        out = []
        for t in range(2, N + 1):
            for c in range(0, N - t + 1):
                r = check1(t, c, anyblock=True)
                out.append({k: v for k, v in r.items() if k != 'fails'} | {'fails': r['fails'][:3]})
                print('Check 1′, ANY side ties (every sharing pattern) t=%d c=%d: %d triples, min %s, failures %d'
                      % (t, c, r['triples'], r['min'], len(r['fails'])), flush=True)
        d = json.load(open(os.path.join(ROOT, 'data', 'h1_shared_proof.json')))
        d['check1_anyblock'] = out
        json.dump(d, open(os.path.join(ROOT, 'data', 'h1_shared_proof.json'), 'w'), indent=1)
        return
    if '--final' in sys.argv:
        rows, ok = table_final()
        d = json.load(open(os.path.join(ROOT, 'data', 'h1_shared_proof.json')))
        d['table_final'] = rows
        d['table_final_ok'] = ok
        json.dump(d, open(os.path.join(ROOT, 'data', 'h1_shared_proof.json'), 'w'), indent=1)
        return
    if '--case-i' in sys.argv:
        rows = table_case_i()
        f = defect_control()
        d = json.load(open(os.path.join(ROOT, 'data', 'h1_shared_proof.json')))
        d['table_case_i'] = rows
        d['defect_control_failures'] = f
        json.dump(d, open(os.path.join(ROOT, 'data', 'h1_shared_proof.json'), 'w'), indent=1)
        return
    if '--table' in sys.argv:
        rows = table()
        d = json.load(open(os.path.join(ROOT, 'data', 'h1_shared_proof.json')))
        d['table'] = rows
        json.dump(d, open(os.path.join(ROOT, 'data', 'h1_shared_proof.json'), 'w'), indent=1)
        return
    if '--control' in sys.argv:
        out = []
        for t in range(3, N + 1):
            for c in range(0, N - t + 1):
                r = check1(t, c, anypair=True)
                out.append({k: v for k, v in r.items() if k != 'fails'} | {'fails': r['fails'][:3]})
                print('MUST-FAIL control (every pair may tie on a sector) t=%d c=%d: min %s, failures %d'
                      % (t, c, r['min'], len(r['fails'])), flush=True)
        d = json.load(open(os.path.join(ROOT, 'data', 'h1_shared_proof.json')))
        d['control_any_pair_sector'] = out
        json.dump(d, open(os.path.join(ROOT, 'data', 'h1_shared_proof.json'), 'w'), indent=1)
        return
    out = []
    for t in range(2, N + 1):
        for c in range(0, N - t + 1):
            r = check1(t, c)
            out.append(r)
            print('t=%d c=%d: %d (L, W, R) triples, min Δ′ − rhs = %s, tight with rhs > 0: %d, failures %d'
                  % (t, c, r['triples'], r['min'], r['tight_positive'], len(r['fails'])), flush=True)
            for f in r['fails'][:3]:
                print('   ', f)
    path = os.path.join(ROOT, 'data', 'h1_shared_proof.json')
    d = json.load(open(path)) if os.path.exists(path) else {}
    d['check1'] = out                       # merge: other modes' keys are kept
    json.dump(d, open(path, 'w'), indent=1)


if __name__ == '__main__':
    main()
