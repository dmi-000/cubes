#!/usr/bin/env python3
"""Re-sign the whole census with the CORRECTED face normals, in exact integers.

Closes the correction opened by [P227]: `concurrence.planes()` read matrix ROWS where a
cube's face normals are the COLUMNS, so every `sig` in the 3 135 491-row census described
each cube's inverse rotation. `cfg`, `count` and `depth` were never affected, so this is a
recomputation and not a re-search.

It emits FOUR statistics per row in ONE incidence pass, because all four were void and all
four come from the same points -- METHODS 2, cache the expensive step, and here the expensive
step is shared by every analysis that has ever wanted it:

    sig    the multiplicity histogram (the census's `sig` column)
    maxc   max plane-concurrence          -- [P222] row 1, VOID, never re-measured
    real   real (face-bounded) incidences -- [P222] row 2, VOID, never re-measured
    mob    Moebius weight of real points  -- [P222] row 3, re-measured on samples only

WHY THIS IS INTEGER-ONLY, and it is the whole reason the job is affordable. The reference
implementation carries intersection points as `Fraction` triples: 0.048 s/row, i.e. 41 core-
hours for the census. But every decision here is an exact SIGN TEST with a bounded multiply
chain, so the rationals are unnecessary. Cramer's rule already produces a common denominator
`det`, so a point is carried as (numerators, det) in integers and

    "p lies on cube k's face"   |M_i . num| <= n * |det|      (integer, exact)
    "two triples meet at one point"   compared after normalising by gcd and sign

are integer comparisons. Same answers, no Fraction objects. Measured below; the equivalence
is GATED against the Fraction implementation on real census rows rather than assumed --
a faster reimplementation that disagrees is a new bug, not an optimisation.

Usage:  resign_all.py --gate            check integer == Fraction on 300 real rows
        resign_all.py SHARD NSHARDS     re-sign one stripe, checkpointing per file
"""
import glob, itertools, json, os, sys, time
from collections import defaultdict, Counter
from math import gcd
sys.path.insert(0, '.')
from concurrence import planes

OUT = 'resign_results'


def mult(c):
    m = 3
    while m * (m - 1) * (m - 2) // 6 < c:
        m += 1
    return m


def cube_mats(cfg):
    out = []
    for (w, x, y, z) in cfg:
        n = w*w + x*x + y*y + z*z
        M = [[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
             [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
             [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]]
        out.append((M, n))
    return out


def solve3_int(p, q, r):
    """Cramer's rule without division: returns (num0, num1, num2, det) or None."""
    a, b, c = p[:3]; d, e, f = q[:3]; g, h, i = r[:3]
    A, B, C = p[3], q[3], r[3]
    det = a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)
    if det == 0:
        return None
    n0 = A*(e*i - f*h) - b*(B*i - f*C) + c*(B*h - e*C)
    n1 = a*(B*i - f*C) - A*(d*i - f*g) + c*(d*C - B*g)
    n2 = a*(e*C - B*h) - b*(d*C - B*g) + A*(d*h - e*g)
    if det < 0:
        n0, n1, n2, det = -n0, -n1, -n2, -det
    g4 = gcd(gcd(abs(n0), abs(n1)), gcd(abs(n2), det))
    if g4 > 1:
        n0 //= g4; n1 //= g4; n2 //= g4; det //= g4
    return (n0, n1, n2, det)          # canonical: det > 0, gcd 1 -> hashable identity


def stats(cfg):
    P = planes(cfg)
    cubes = cube_mats(cfg)
    owner = [i // 6 for i in range(len(P))]
    own = defaultdict(set); cnt = defaultdict(int)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3_int(P[i], P[j], P[k])
        if s is None:
            continue
        own[s].update((owner[i], owner[j], owner[k])); cnt[s] += 1
    sig = Counter(); maxc = 0; real = 0; mob = 0
    for p, c in cnt.items():
        m = mult(c)
        if m > maxc:
            maxc = m
        if m >= 4:
            sig[min(m, 12)] += 1
        n0, n1, n2, det = p
        ok = True
        for q in own[p]:
            M, nn = cubes[q]
            lim = nn * det                     # det > 0 by construction
            sat = False
            for row in M:
                v = row[0]*n0 + row[1]*n1 + row[2]*n2
                if v > lim or v < -lim:
                    ok = False; break
                if v == lim or v == -lim:
                    sat = True
            if not ok or not sat:
                ok = False; break
        if ok:
            real += 1; mob += (m - 1) * (m - 2) // 2
    return tuple(sorted(sig.items())), maxc, real, mob


def reference(cfg):
    """the Fraction implementation this replaces -- used only by the gate"""
    from concurrence import solve3
    from realsig import cube_data, on_face
    P = planes(cfg); cubes = cube_data(cfg)
    owner = [i // 6 for i in range(len(P))]
    own = defaultdict(set); cnt = defaultdict(int)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is None:
            continue
        own[s].update((owner[i], owner[j], owner[k])); cnt[s] += 1
    sig = Counter(); maxc = 0; real = 0; mob = 0
    for p, c in cnt.items():
        m = mult(c); maxc = max(maxc, m)
        if m >= 4:
            sig[min(m, 12)] += 1
        if all(on_face(p, cubes[q][0], cubes[q][1]) for q in own[p]):
            real += 1; mob += (m - 1) * (m - 2) // 2
    return tuple(sorted(sig.items())), maxc, real, mob


FILES = sorted(glob.glob('census_n4_*.jsonl'))


def rows_of(shard, nsh):
    i = 0
    for fn in FILES:
        with open(fn) as f:
            for line in f:
                if i % nsh == shard:
                    yield fn, line
                i += 1


if __name__ == '__main__':
    if sys.argv[1] == '--gate':
        # A faster reimplementation must agree with what it replaces, on REAL data --
        # not on a hand-picked case, and not merely "no crash". Both sides must also be
        # non-trivial: a gate whose two sides are both empty is [FAILURE_MODES 2].
        import random
        pool = []
        for fn in FILES:
            with open(fn) as f:
                for i, line in enumerate(f):
                    if i >= 60: break
                    pool.append(json.loads(line))
        rng = random.Random(3); rng.shuffle(pool)
        pool = [d for d in pool if d.get('count')][:300]
        bad = 0; nontrivial = 0
        t_int = t_ref = 0.0
        for d in pool:
            cfg = [tuple(q) for q in d['cfg']]
            t0 = time.time(); a = stats(cfg); t_int += time.time() - t0
            t0 = time.time(); b = reference(cfg); t_ref += time.time() - t0
            if a != b:
                bad += 1
                if bad <= 3:
                    print('  MISMATCH\n    int %s\n    ref %s' % (a, b))
            if a[0] or a[2]:
                nontrivial += 1
        print('gate: %d rows, %d mismatches, %d with a non-empty signature or real count'
              % (len(pool), bad, nontrivial))
        print('integer %.4f s/row   Fraction %.4f s/row   speedup %.1fx'
              % (t_int/len(pool), t_ref/len(pool), t_ref/max(t_int, 1e-9)))
        N = 3135491
        print('full census at the integer rate: %.0f core-hours (%.1f h on 4 shards)'
              % (N*t_int/len(pool)/3600, N*t_int/len(pool)/3600/4))
        sys.exit(0 if bad == 0 and nontrivial > len(pool)//2 else 1)

    shard, nsh = int(sys.argv[1]), int(sys.argv[2])
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'sig_s%d_of%d.jsonl' % (shard, nsh))
    done = 0
    if os.path.exists(path):
        with open(path) as f:
            done = sum(1 for _ in f)
    t0 = time.time(); i = 0
    with open(path, 'a') as out:
        for fn, line in rows_of(shard, nsh):
            i += 1
            if i <= done:                      # restartable: skip what is already written
                continue
            d = json.loads(line)
            if not d.get('count'):
                out.write('null\n'); continue
            sg, mx, rl, mb = stats([tuple(q) for q in d['cfg']])
            out.write(json.dumps({'ens': d['ens'], 'count': d['count'],
                                  'sig': [list(t) for t in sg],
                                  'maxc': mx, 'real': rl, 'mob': mb}) + '\n')
            if i % 20000 == 0:
                out.flush()
                print('shard %d: %d rows, %.1f h elapsed' % (shard, i, (time.time()-t0)/3600),
                      flush=True)
    print('shard %d done: %d rows' % (shard, i), flush=True)
