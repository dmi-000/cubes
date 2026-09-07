#!/usr/bin/env python3
"""Re-measure the signature findings with the CORRECTED planes(), and say what moved.

`concurrence.planes()` built each cube's face normals from the ROWS of its rotation matrix.
In world coordinates they are the COLUMNS; the rows belong to the inverse rotation. So every
signature computed before that fix described a different compound, and the octahedral
invariance gate says so: a cube is unchanged by its own 24 rotations, so `q` and `q*s` must
give the same signature -- broken, 6 of 6 respellings changed it; corrected, 0 of 96.

This script is the reproducible form of that correction. It re-signs a SAMPLE of the stored
census -- the `cfg` column is valid, only `sig` was void, so nothing needs re-searching --
and reports the three claims that rested on the broken map:

  1. per-ensemble signature richness (input to the Chao1 estimate)
  2. does a signature pin the count
  3. the Moebius-weight predictor, [P222]'s r = 0.562 / 77.6 %

It deliberately computes BOTH maps on the SAME rows, so the two columns differ only in the
one line under test. The sample is seeded, so the numbers are reproducible; it is a sample
and not the census, and the row counts are printed for that reason.
"""
import glob, itertools, json, math, random, sys
from collections import Counter, defaultdict
from fractions import Fraction as F
sys.path.insert(0, '.')
import concurrence
from concurrence import solve3
from realsig import cube_data, on_face

SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
SEED = 11


def planes_broken(cfg):
    """the pre-fix version, kept ONLY so the two columns are computed on the same rows"""
    out = []
    for (w, x, y, z) in cfg:
        n = w*w + x*x + y*y + z*z
        M = [[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
             [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
             [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]]
        for r in range(3):                      # ROWS -- the bug
            v = (M[r][0], M[r][1], M[r][2])
            for s in (1, -1):
                out.append((v[0], v[1], v[2], s * n))
    return out


def incidences(P):
    """{point: (set of owning cubes, number of triples through it)}"""
    owner = [i // 6 for i in range(len(P))]
    own = defaultdict(set); cnt = defaultdict(int)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is None:
            continue
        own[s].update((owner[i], owner[j], owner[k])); cnt[s] += 1
    return own, cnt


def mult(c):
    m = 3
    while m * (m - 1) * (m - 2) // 6 < c:
        m += 1
    return m


def signature(P, cap=12):
    _, cnt = incidences(P)
    h = Counter()
    for s, c in cnt.items():
        m = mult(c)
        if m >= 4:                              # 3-fold points are generic and everywhere
            h[min(m, cap)] += 1
    return tuple(sorted(h.items()))


def mobius_weight(cfg, P):
    """sum of |mu| = (m-1)(m-2)/2 over the REAL (face-bounded) incidence points"""
    cubes = cube_data(cfg)
    own, cnt = incidences(P)
    w = 0
    for p, owners in own.items():
        if not all(on_face(p, cubes[o][0], cubes[o][1]) for o in owners):
            continue
        m = mult(cnt[p])
        w += (m - 1) * (m - 2) // 2
    return w


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n; my = sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs); syy = sum((b - my) ** 2 for b in ys)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


if __name__ == '__main__':
    files = sorted(glob.glob('census_n4_*.jsonl'))
    rows = []
    for fn in files:
        with open(fn) as f:
            for line in f:
                rows.append(line)
    print('census: %d rows in %d files; re-signing a seeded sample of %d'
          % (len(rows), len(files), SAMPLE), flush=True)
    print('(the `cfg` column was never void -- only `sig` -- so no search is repeated)\n',
          flush=True)

    rng = random.Random(SEED)
    pick = rng.sample(rows, min(SAMPLE, len(rows)))
    recs = []
    for line in pick:
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get('count'):
            recs.append((d['ens'], [tuple(q) for q in d['cfg']], d['count']))

    rich_b = defaultdict(set); rich_c = defaultdict(set)
    groups = defaultdict(list)
    pts = []
    for ens, cfg, c in recs:
        Pb = planes_broken(cfg); Pc = concurrence.planes(cfg)
        rich_b[ens].add(signature(Pb))
        sc = signature(Pc)
        rich_c[ens].add(sc)
        groups[sc].append(c)
        pts.append((mobius_weight(cfg, Pc), c))

    print('1. PER-ENSEMBLE RICHNESS  (distinct signatures in this sample)')
    print('   %-12s %8s %9s' % ('ensemble', 'broken', 'corrected'))
    for ens in sorted(set(rich_b) | set(rich_c)):
        print('   %-12s %8d %9d' % (ens, len(rich_b[ens]), len(rich_c[ens])))
    print()

    multi = {s: v for s, v in groups.items() if len(v) > 1}
    det = sum(1 for v in multi.values() if min(v) == max(v))
    spreads = sorted(max(v) - min(v) for v in multi.values())
    med = spreads[len(spreads) // 2] if spreads else 0
    print('2. DOES THE CORRECTED SIGNATURE PIN THE COUNT?')
    print('   %d signatures seen >1 time; %d pin the count exactly; median spread %d\n'
          % (len(multi), det, med), flush=True)

    r = pearson([a for a, _ in pts], [b for _, b in pts])
    prng = random.Random(SEED + 1)
    ok = tested = 0
    for _ in range(4000):
        (w1, c1), (w2, c2) = prng.sample(pts, 2)
        if c1 == c2 or w1 == w2:
            continue
        tested += 1
        ok += (w1 > w2) == (c1 > c2)
    print('3. THE MOEBIUS-WEIGHT PREDICTOR  (was r=0.562, ordered 77.6%% -- both from broken planes)')
    print('   corrected: r = %+.3f, orders %d/%d = %.1f%%  on %d configurations'
          % (r, ok, tested, 100.0 * ok / max(tested, 1), len(pts)), flush=True)
