#!/usr/bin/env python3
"""[OQ 39] EXPLORING THE BAND [P367] opened: B = 118..126, where no EE ceiling has been measured.

[P367] enumerated every way a 4-compound could beat 183 and found the project's chain covers
only the `B = 128` column of a twelve-column grid.  The user: *if there's unexplored, we may
want to explore there.*  This is that exploration.

THREE PARTS, in increasing cost, and the cheap one carries the most.

  A.  THE 3-SUBSET ENVELOPE.  [P359] measured ONE point of it -- at `E_S = 32` the largest
      `sum EE` over a triple's three pairs is 20.  The band needs the whole curve: for each
      `E_S`, the largest `sum EE`.  This is 3-cube work, ~60x cheaper per evaluation than
      4-cube work, and it is what couples `B` to `EE` across the entire grid rather than at one
      column.

  B.  THE GRID, RECOMPUTED under that envelope.  Exact enumeration over pair profiles, with
      each triple's EE capped by the measured envelope at its own `E_S`.  This says which
      cells of [P367]'s grid survive.

  C.  A DIRECTED CLIMB IN THE BAND.  [P367]'s first scan perturbed the record, which walks
      DOWNHILL in `B`; the band deserves a climb that holds `B` in [117, 128] and maximises the
      objective, seeded from both regimes that bracket it -- the record (EE 36, B 128) and the
      face-diagonal family (EE 42, B 84).

THE ENVELOPE IS SAMPLED, SO IT IS A LOWER BOUND ON ITSELF.  A measured `max` over draws is not
a cap ([METHODS 1]); using it AS a cap would repeat exactly the error [P361] was written to
avoid.  Part B is therefore a map of where to look, never a proof that the rest is empty, and
it is labelled that way in the output.

Restartable: every 3- and 4-cube evaluation is cached on disk by normalised quaternion tuple,
so a corrected rerun costs the correction only ([METHODS 2]).
"""
import sys, os, json, random, itertools, collections
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as EB
from c_level import shares_plane
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, 'data', 'band_cache.jsonl')
PAIRS = list(itertools.combinations(range(4), 2))
TRIPLES = list(itertools.combinations(range(4), 3))
INTRI = [[k for k, p in enumerate(PAIRS) if set(p) <= set(S)] for S in TRIPLES]

_mem = {}


def norm(q):
    g = 0
    for v in q:
        g = gcd(g, abs(v))
    if g == 0:
        return None
    q = tuple(v // g for v in q)
    for v in q:                       # sign-normalise: q and -q are the same rotation
        if v:
            return q if v > 0 else tuple(-x for x in q)
    return None


def key(qs):
    n = [norm(q) for q in qs]
    if any(x is None for x in n):
        return None
    return json.dumps(sorted(map(list, n)))


def load_cache():
    if _mem or not os.path.exists(CACHE):
        return
    for line in open(CACHE):
        try:
            r = json.loads(line)
        except ValueError:
            continue                  # a truncated last line from a killed run is not an error
        _mem[r['k']] = r['v']


def anat(qs):
    """(EE, SC2, B, Q4, objective) for a 2-, 3- or 4-compound.  Cached on disk."""
    k = key(qs)
    if k in _mem:
        return _mem[k]
    sig, _ = EB.vertices(qs)
    EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
    T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
    Q4 = sum(v for kk, v in sig.items() if len(kk) == 4)
    v = {'EE': EE, 'SC2': SC, 'ES': T3 + 4 * Qg, 'Q4': Q4,
         'obj': EE + 2 * SC + T3 + 4 * Qg - Q4}
    _mem[k] = v
    with open(CACHE, 'a') as f:
        f.write(json.dumps({'k': k, 'v': v}) + '\n')
    return v


def rq(rng, h):
    while True:
        q = tuple(rng.randint(-h, h) for _ in range(4))
        if any(q):
            return q


# face-diagonal family: the EE = 42 regime of [P330], rotations about a common face diagonal
FACEDIAG = [(3, 2, 2, 0), (5, 3, 3, 0), (7, 2, 2, 0), (4, 3, 3, 0), (5, 2, 2, 0),
            (7, 4, 4, 0), (2, 1, 1, 0), (9, 4, 4, 0), (5, 4, 4, 0), (8, 3, 3, 0)]


def part_a(budget, rng):
    """the 3-subset envelope: largest sum-EE at each E_S."""
    env = collections.defaultdict(int)
    wit = {}
    hist = collections.Counter()
    rec = [tuple(q) for q in WK.REC[4]]
    seeds = [list(t) for t in itertools.combinations(rec, 3)]
    n = refused = 0
    while n < budget:
        r = rng.random()
        if r < 0.25:
            qs = list(rng.choice(seeds))
            i = rng.randrange(3)
            q = list(qs[i]); q[rng.randrange(4)] += rng.choice([-2, -1, 1, 2]); qs[i] = tuple(q)
        elif r < 0.45:
            qs = [(1, 0, 0, 0), rng.choice(FACEDIAG), rng.choice(FACEDIAG)]
        elif r < 0.6:
            qs = [(1, 0, 0, 0), rng.choice(FACEDIAG), rq(rng, rng.choice([4, 9]))]
        else:
            qs = [(1, 0, 0, 0)] + [rq(rng, rng.choice([3, 6, 9, 14])) for _ in range(2)]
        if shares_plane(qs) or key(qs) is None or len(set(map(norm, qs))) < 3:
            continue
        n += 1
        try:
            a = anat(qs)
            ee = sum(anat([qs[i], qs[j]])['EE'] for i, j in itertools.combinations(range(3), 2))
        except Exception:
            refused += 1
            continue
        hist[a['ES']] += 1
        if ee > env[a['ES']]:
            env[a['ES']] = ee
            wit[a['ES']] = [list(q) for q in qs]
    return env, wit, hist, n, refused


def part_b(env):
    """[P367]'s grid, with each triple's EE capped by the measured envelope at its own E_S."""
    def cap(es):
        # monotone closure: the envelope at E_S is at least what was seen at any E_S' >= it is
        # NOT assumed; use the measured value at this E_S, and 30 (the box) where unmeasured.
        return env.get(es, 30)
    types = [(e, 0) for e in (0, 4, 6, 8, 10)] + [(e, 2) for e in (0, 4, 6)]
    bestB = collections.defaultdict(lambda: (-1, None))
    for a in itertools.product(types, repeat=6):
        EE = [t[0] for t in a]; SC = [t[1] for t in a]
        E = [EE[k] + 2 * SC[k] for k in range(6)]
        s = sum(1 for c in SC if c)
        if s == 5:
            continue                                   # [P351]
        T = sum(E)
        # choose each E_S as large as its own envelope permits
        B = 0
        ok = True
        for T3 in INTRI:
            eeS = sum(EE[k] for k in T3)
            best = -1
            for es in range(0, 33):
                if eeS <= cap(es) and es <= 62 - sum(E[k] for k in T3):
                    best = max(best, es)
            if best < 0:
                ok = False
                break
            B += best
        if not ok:
            continue
        if T + B > bestB[B][0]:
            bestB[B] = (T + B, {'s': s, 'EE': sum(EE), 'T': T})
    return bestB


def part_c(budget, rng):
    """a climb that HOLDS B in the band and maximises the objective."""
    rec = [tuple(q) for q in WK.REC[4]]
    starts = [rec,
              [(1, 0, 0, 0)] + [rng.choice(FACEDIAG) for _ in range(3)],
              [rec[0], rec[1], rec[2], rng.choice(FACEDIAG)],
              [rec[0], rec[1], rng.choice(FACEDIAG), rec[3]]]
    perB = collections.defaultdict(lambda: (-1, None))
    n = refused = 0
    for st in starts:
        cur = [tuple(q) for q in st]
        try:
            ca = anat(cur)
        except Exception:
            continue
        for _ in range(budget // len(starts)):
            cand = [list(q) for q in cur]
            for _ in range(rng.choice([1, 1, 2])):
                i = rng.randrange(1, 4); j = rng.randrange(4)
                cand[i][j] += rng.choice([-3, -2, -1, 1, 2, 3])
            cand = [tuple(q) for q in cand]
            if any(not any(q) for q in cand) or shares_plane(cand) or key(cand) is None:
                continue
            n += 1
            try:
                a = anat(cand)
            except Exception:
                refused += 1
                continue
            if 112 <= a['ES'] <= 128 and a['obj'] > perB[a['ES']][0]:
                perB[a['ES']] = (a['obj'], {'quats': [list(q) for q in cand],
                                            'EE': a['EE'], 'SC2': a['SC2'], 'Q4': a['Q4']})
            # accept if it does not lose objective, with a floor on B to stay in the band
            if a['obj'] >= ca['obj'] and a['ES'] >= 112:
                cur, ca = cand, a
    return perB, n, refused


def main():
    load_cache()
    rng = random.Random(20260918)
    out = {'what': 'exploring the B = 118..126 band opened by P367', 'supports': 'OQ 39'}
    print('cache entries loaded: %d' % len(_mem))

    print('\nA. THE 3-SUBSET ENVELOPE -- largest sum-EE at each E_S  ([P359] had E_S = 32 only)')
    env, wit, hist, n, refused = part_a(3000, rng)
    print('   3-compounds evaluated: %d   unevaluable: %d' % (n - refused, refused))
    print('   E_S :  ' + ' '.join('%3d' % e for e in sorted(env, reverse=True)[:12]))
    print('   maxEE: ' + ' '.join('%3d' % env[e] for e in sorted(env, reverse=True)[:12]))
    print('   n    : ' + ' '.join('%3d' % hist[e] for e in sorted(env, reverse=True)[:12]))
    out['envelope'] = {'evaluated': n - refused, 'unevaluable': refused,
                       'max_EE_by_ES': {str(k): v for k, v in sorted(env.items())},
                       'n_by_ES': {str(k): v for k, v in sorted(hist.items())},
                       'witness_at_32': wit.get(32)}
    print('   SAMPLED, so this is a LOWER bound on the envelope, never a cap ([METHODS 1]).')

    print('\nB. THE GRID under that envelope -- best reachable TOTAL per B column')
    bb = part_b(env)
    print('      B    best T+B   TOTAL   at (s, EE, T)')
    live = []
    for B in sorted(bb, reverse=True):
        if B < 112:
            continue
        v, d = bb[B]
        tot = 7 + v
        mark = '  <-- beats 183' if tot > 183 else ''
        print('    %4d    %6d   %5d   s=%d EE=%d T=%d%s' % (B, v, tot, d['s'], d['EE'], d['T'], mark))
        if tot > 183:
            live.append({'B': B, 'TOTAL': tot, **d})
    out['grid_under_envelope'] = {str(B): {'obj': bb[B][0], 'TOTAL': 7 + bb[B][0], **bb[B][1]}
                                  for B in sorted(bb) if B >= 112}
    out['live_cells'] = live

    print('\nC. A DIRECTED CLIMB HELD IN THE BAND')
    perB, n, refused = part_c(2400, rng)
    print('   4-compounds evaluated: %d   unevaluable: %d' % (n - refused, refused))
    print('      B     best obj   TOTAL   EE  SC2  Q4')
    band = {}
    for B in sorted(perB, reverse=True):
        v, d = perB[B]
        print('    %4d    %7d   %5d   %2d   %2d  %2d' % (B, v, 7 + v, d['EE'], d['SC2'], d['Q4']))
        band[str(B)] = {'obj': v, 'TOTAL': 7 + v, 'EE': d['EE'], 'SC2': d['SC2'],
                        'Q4': d['Q4'], 'quats': d['quats']}
    out['climb'] = {'evaluated': n - refused, 'unevaluable': refused, 'by_B': band}

    out['reproduce'] = PROV.stamp(
        parameters={'seed': 20260918, 'part_a_budget': 3000, 'part_c_budget': 2400,
                    'band': [112, 128]},
        inputs=['data/band_cache.jsonl'],
        note='envelope is SAMPLED: a lower bound on itself, not a cap')
    json.dump(out, open(os.path.join(ROOT, 'data', 'band_frontier.json'), 'w'), indent=1)
    print('\nwrote data/band_frontier.json   (cache now %d entries)' % len(_mem))


if __name__ == '__main__':
    main()
