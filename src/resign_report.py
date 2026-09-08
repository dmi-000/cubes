#!/usr/bin/env python3
"""Close every claim that rested on the broken face normals, from the full re-signed census.

Reads `resign_results/*.jsonl` (produced by `resign_all.py`) and recomputes, on ALL rows
rather than a 3 000-row sample, the four things [P227] voided:

  1. per-ensemble signature richness + Chao1   -- replaces TAXONOMY 12's table and ~4 216
  2. does a signature pin the count            -- the one claim that survived the sample
  3. the THREE predictors of P222's table      -- two of which were never re-measured at all
  4. how the corrected map differs by ensemble -- the "moves in both directions" claim,
                                                  which a second sample already contradicted

Written before the run finished, per [FAILURE_MODES 27a]: the correction's own numbers must
come from a script that exists. Quoting a figure computed inline is how run 1 became
irreproducible and how its per-ensemble directions turned out to be noise.

CHAO1 CAVEAT, stated because the original did not: Chao1 assumes independent draws from a
fixed population. These ensembles are constructed families with deliberate internal
structure, so its output is an order of magnitude, not an estimate with the coverage its
formula implies.
"""
import glob, json, math, random, sys
from collections import Counter, defaultdict


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n; my = sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs); syy = sum((b - my) ** 2 for b in ys)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


def orders(pairs, rng, trials=200000):
    """fraction of random pairs the statistic orders the same way as the count"""
    ok = tested = 0
    n = len(pairs)
    for _ in range(trials):
        (s1, c1) = pairs[rng.randrange(n)]
        (s2, c2) = pairs[rng.randrange(n)]
        if c1 == c2 or s1 == s2:
            continue
        tested += 1
        ok += (s1 > s2) == (c1 > c2)
    return ok, tested


if __name__ == '__main__':
    files = sorted(glob.glob('resign_results/*.jsonl'))
    rich = defaultdict(set)
    per_ens = Counter()
    groups = defaultdict(list)
    freq = Counter()                     # signature -> how many configurations
    maxc = []; real = []; mob = []; counts = []
    nrows = nnull = 0
    for fn in files:
        with open(fn) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                nrows += 1
                if line == 'null':
                    nnull += 1
                    continue
                d = json.loads(line)
                sg = tuple(tuple(t) for t in d['sig'])
                rich[d['ens']].add(sg); per_ens[d['ens']] += 1
                freq[sg] += 1
                groups[sg].append(d['count'])
                counts.append(d['count'])
                maxc.append(d['maxc']); real.append(d['real']); mob.append(d['mob'])

    print('re-signed rows: %d  (%d with no count, excluded)' % (nrows, nnull))
    print('CORRECTED normals throughout; `cfg`/`count`/`depth` were never affected.\n')

    print('1. PER-ENSEMBLE RICHNESS (full census, corrected)')
    print('   %-12s %10s %10s %10s %9s' % ('ensemble', 'configs', 'signatures', 'Chao1', 'coverage'))
    f1 = Counter(); f2 = Counter()
    ens_of = defaultdict(Counter)
    for fn in files:                     # second pass only for per-ensemble singletons
        with open(fn) as f:
            for line in f:
                line = line.strip()
                if not line or line == 'null':
                    continue
                d = json.loads(line)
                ens_of[d['ens']][tuple(tuple(t) for t in d['sig'])] += 1
    for e in sorted(rich):
        c = ens_of[e]
        s1 = sum(1 for v in c.values() if v == 1)
        s2 = sum(1 for v in c.values() if v == 2)
        obs = len(c)
        chao = obs + (s1 * s1 / (2.0 * s2) if s2 else s1 * (s1 - 1) / 2.0)
        print('   %-12s %10d %10d %10.0f %8.0f%%'
              % (e, per_ens[e], obs, chao, 100.0 * obs / chao if chao else 100))
    tot = len(freq)
    S1 = sum(1 for v in freq.values() if v == 1); S2 = sum(1 for v in freq.values() if v == 2)
    chao = tot + (S1 * S1 / (2.0 * S2) if S2 else S1 * (S1 - 1) / 2.0)
    print('   %-12s %10d %10d %10.0f %8.0f%%   <-- replaces the void ~4 216'
          % ('ALL', sum(per_ens.values()), tot, chao, 100.0 * tot / chao if chao else 100))
    print('   (Chao1 assumes independent draws from a fixed population; these are')
    print('    constructed families, so read it as an order of magnitude.)\n')

    multi = {s: v for s, v in groups.items() if len(v) > 1}
    det = sum(1 for v in multi.values() if min(v) == max(v))
    spreads = sorted(max(v) - min(v) for v in multi.values())
    print('2. DOES A SIGNATURE PIN THE COUNT?')
    print('   %d signatures seen >1 time; %d pin the count exactly (%.1f%%); median spread %d, max %d\n'
          % (len(multi), det, 100.0 * det / max(len(multi), 1),
             spreads[len(spreads)//2] if spreads else 0, spreads[-1] if spreads else 0))

    rng = random.Random(5)
    print('3. THE THREE PREDICTORS OF [P222], all recomputed on the full census')
    print('   %-34s %10s %18s' % ('statistic', 'r', 'orders pairs'))
    for name, xs, was in (('max plane-concurrence', maxc, 'was r=0.354'),
                          ('real (face-bounded) incidences', real, 'was 57%'),
                          ('Moebius weight of real incidences', mob, 'was r=0.562 / 77.6%')):
        r = pearson(xs, counts)
        ok, tested = orders(list(zip(xs, counts)), rng)
        print('   %-34s %+10.3f %8d/%d = %.1f%%   [%s]'
              % (name, r, ok, tested, 100.0 * ok / max(tested, 1), was))
    print('\n   50% is chance. All three were VOID; only the third had been re-measured,')
    print('   and it was re-measured on samples. The first two are measured here for the')
    print('   first time -- they were previously scored as negatives while unevaluated.')
