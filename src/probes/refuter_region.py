#!/usr/bin/env python3
"""[OQ 39] Searching the region [P373]'s refuter opened — on ENGINE COUNTS, not the formula.

Every n = 4 search in this thread was seeded from the record or the face-diagonal family, and
both of the ceilings they produced turned out to be false ([P373]).  The refuter came from a
third place: the n = 3 `EE + B` extreme — two members of the `EE = 10` family placed against
each other — extended by a fourth cube.  **That region has never been searched for region
count.**  A first climb in it already reached 179.

TWO CORRECTIONS OF METHOD, both from this session:

  * **The objective is the ENGINE, not `7 + T + B - Q4`.**  [P374] showed that formula is a
    bound with a scope and not an identity, and it overstated one climb result by 2.  The
    engine costs 18 ms against the census's 66 ms, so there was never a reason to use the
    formula as an objective at all.
  * **A refusal is not a zero** ([FAILURE_MODES 43]): refusals are counted and reported.

What would END this search: reaching 184.  What it can otherwise produce is a lower bound
([METHODS 1]) — and the honest report of one is its seed and its budget.
"""
import sys, os, json, random, itertools, collections
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as EB
import ee_determinantal as D
from c_level import shares_plane, engine
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def count(qs):
    r = engine(qs)
    if 'error' in r or not r.get('by_depth'):
        return None
    return sum(v for k, v in r['by_depth'].items() if k != '0')


def family(h=5):
    out = []
    for q in itertools.product(range(-h, h + 1), repeat=4):
        if not any(q):
            continue
        g = 0
        for v in q:
            g = gcd(g, abs(v))
        if g != 1:
            continue
        neg = False
        for v in q:
            if v:
                neg = v < 0
                break
        if neg or shares_plane([(1, 0, 0, 0), q]):
            continue
        if D.ee_exact(q) == 10:
            out.append(q)
    return out


def main():
    rng = random.Random(183184)
    stats = collections.Counter()
    fam = family()
    print('EE = 10 family (height <= 5): %d' % len(fam), flush=True)

    # the n = 3 extremes: E_S = 32 with sum EE = 26
    extremes = []
    for a, b in itertools.combinations(fam, 2):
        qs = [(1, 0, 0, 0), a, b]
        if shares_plane(qs):
            continue
        sig, _ = EB.vertices(qs)
        if sig.get((1, 1, 1), 0) + 4 * sig.get((1, 1, 1, 1), 0) == 32 and sig.get((2, 2), 0) == 26:
            extremes.append(qs)
        if len(extremes) >= 16:
            break
    print('n = 3 extremes (E_S 32, EE 26): %d' % len(extremes), flush=True)

    best = (0, None)
    hist = collections.Counter()

    def step(qs):
        c = [list(q) for q in qs]
        for _ in range(rng.choice([1, 1, 1, 2, 3])):
            i = rng.randrange(1, 4); j = rng.randrange(4)
            c[i][j] += rng.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        return [tuple(q) for q in c]

    def evaluate(qs):
        if any(not any(q) for q in qs) or shares_plane(qs):
            return None
        stats['tried'] += 1
        v = count(qs)
        if v is None:
            stats['refused'] += 1
            return None
        hist[v] += 1
        return v

    # phase 1: broad seeding
    print('\nphase 1 -- seeding', flush=True)
    seeds = []
    for base in extremes:
        for q in rng.sample(fam, min(25, len(fam))) + \
                 [tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(25)]:
            qs = base + [q]
            v = evaluate(qs)
            if v is None:
                continue
            seeds.append((v, qs))
            if v > best[0]:
                best = (v, qs)
    seeds.sort(reverse=True, key=lambda t: t[0])
    print('   evaluated %d   refusals %d   best %d'
          % (stats['tried'] - stats['refused'], stats['refused'], best[0]), flush=True)

    # phase 2: climb from the top seeds
    print('phase 2 -- climbing from the top 20 seeds', flush=True)
    for v0, qs0 in seeds[:20]:
        cur, cv = qs0, v0
        for _ in range(260):
            cand = step(cur)
            v = evaluate(cand)
            if v is None:
                continue
            if v > best[0]:
                best = (v, cand)
                print('      new best: %d  at %s'
                      % (v, ';'.join(','.join(map(str, q)) for q in cand)), flush=True)
            if v >= cv - 1:
                cur, cv = cand, v
    print('   evaluated %d total   refusals %d' % (stats['tried'] - stats['refused'],
                                                   stats['refused']), flush=True)

    print('\nBEST region count found: %d   (record 183)   %s'
          % (best[0], 'EXCEEDS THE RECORD' if best[0] > 183 else 'does not reach it'), flush=True)
    if best[1]:
        print('   %s' % ';'.join(','.join(map(str, q)) for q in best[1]), flush=True)
        sig, _ = EB.vertices(best[1])
        EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
        T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
        Q4 = sum(v for k, v in sig.items() if len(k) >= 4)
        print('   census %s' % dict(sorted(sig.items())), flush=True)
        print('   EE %d  SC2 %d  B %d  Q4 %d   formula would say %d, ENGINE says %d'
              % (EE, SC, T3 + 4 * Qg, Q4, 7 + EE + 2 * SC + T3 + 4 * Qg - Q4, best[0]),
              flush=True)
    print('   count distribution, top: %s' % sorted(hist.items(), reverse=True)[:8], flush=True)

    out = {'what': 'region-count search in the region P373 opened', 'supports': 'OQ 39',
           'evaluated': stats['tried'] - stats['refused'], 'unevaluable': stats['refused'],
           'n3_extremes': len(extremes), 'best': best[0],
           'best_quats': [list(q) for q in best[1]] if best[1] else None,
           'distribution': {str(k): v for k, v in sorted(hist.items())}}
    out['reproduce'] = PROV.stamp(
        parameters={'seed': 183184, 'family_height': 5, 'climb_steps': 260, 'restarts': 20},
        note='objective is the ENGINE region count, not the identity ([P374])')
    json.dump(out, open(os.path.join(ROOT, 'data', 'refuter_region.json'), 'w'), indent=1)
    print('\nwrote data/refuter_region.json', flush=True)


if __name__ == '__main__':
    main()
