#!/usr/bin/env python3
"""First tranche: the LOCUS of each subset class of the n=6 and n=7 records.

`subset_census.py` ([Postscript 111](LEDGER.md#p111)) collapsed the hundreds of subsets of each record
into a few dozen (count, depth-profile) classes.  Nothing is known about their
LOCI: the five invariants that make up "topology" here -- dimension, components,
arc-or-loop, boundary wall type, and the count across the boundary -- have been
measured for a handful of records and for no subset at all.

DIMENSION is handled separately by `dimension.py`, which passes its controls as
of 2026-08-13 ([Postscript 113](LEDGER.md#p113)); this file measures the other four invariants.
Per (class, moved cube, direction):

    own_count    the configuration's OWN count, evaluated directly -- NOT read off
                 a run, because a maximiser sits ON a wall, s = 0 is a root, and
                 `decompose` evaluates strictly BETWEEN roots
    on_wall      whether s = 0 is a root, and of which wall type
    left/right   the counts of the chambers either side of it
    extends      whether either neighbouring chamber carries the same count, i.e.
                 whether the locus is a point or extends in this direction
    wrap         the count at the point at infinity, the half-turn (0, d):
                 the one-call arc-or-loop test of METHODS section 3
    max_on_line  whether the count is the maximum along the line -- locus vs saddle

Windows are +-20/L with L the direction's max component -- the scale-matched
window of [Postscript 103](LEDGER.md#p103); a fixed window measures a different question per
direction.  A cube whose quaternion has w = 0 is a half-turn, at infinity in the
Cayley chart, and is skipped with that stated rather than silently.

    python3 subset_topology.py [seconds]
"""
import itertools
import json
import subprocess
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, '/Users/dmi/cube-compounds')
from exact_chambers import decompose
from solve_ends import q_of

ENG = '/Users/dmi/cube-compounds/cube_regions_n'
BASE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
RECORDS = {6: BASE + [(7, 14, 1, -5)],
           7: BASE + [(7, 14, 1, -5), (4, -3, -4, -4)]}
DIRS = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (1, -3, -6), (1, 1, -4), (1, 1, 0)]

T0 = time.time()
LOG = open('/Users/dmi/cube-compounds/subset_topology.log', 'w')
OUT = '/Users/dmi/cube-compounds/subset_topology.json'


def log(m):
    line = '[%6.1fs] %s' % (time.time() - T0, m)
    print(line, flush=True)
    LOG.write(line + '\n')
    LOG.flush()


def count(cfg):
    s = ';'.join(','.join(map(str, q)) for q in cfg)
    if max(abs(v) for q in cfg for v in q) > 512:
        return None
    p = subprocess.run([ENG, '--quats', s], capture_output=True, text=True)
    try:
        o = json.loads(p.stdout.strip().splitlines()[-1])
        return o['bounded'], tuple(o['by_depth'][str(i)] for i in range(1, len(cfg) + 1))
    except Exception:
        return None


def classes(Q, n):
    """one representative per (count, depth profile) class, for k = 3..n-1"""
    out = []
    for k in range(3, n):
        seen = {}
        for idxs in itertools.combinations(range(n), k):
            cfg = [Q[i] for i in idxs]
            got = count(cfg)
            if got is None:
                continue
            if got not in seen:
                seen[got] = idxs
        for (c, prof), idxs in sorted(seen.items(), reverse=True):
            out.append({'k': k, 'count': c, 'profile': prof, 'idxs': idxs,
                        'cfg': [Q[i] for i in idxs]})
    return out


def cayley(q):
    w, x, y, z = q
    if w == 0:
        return None
    return [F(x, w), F(y, w), F(z, w)]


def study(cfg, t, d, label):
    """move cube t of cfg along direction d; describe the run containing it"""
    a0 = cayley(cfg[t])
    if a0 is None:
        return {'skipped': 'cube %d is a half-turn (w=0): at Cayley infinity' % t}
    base = [q for i, q in enumerate(cfg) if i != t]
    L = max(abs(x) for x in d)
    try:
        runs, kind = decompose(base, a0, [F(x) for x in d],
                               F(-20, L), F(20, L), label)
    except Exception as e:
        return {'crash': type(e).__name__}
    # THE CONFIGURATION SITS ON A WALL, so s = 0 is itself a ROOT and
    # `decompose` -- which evaluates strictly BETWEEN roots -- never reports its
    # count.  Taking "the run containing 0" gave the NEIGHBOURING chamber in 71%
    # of the first tranche's 728 measurements, so every boundary type, wrap and
    # max_on_line statistic there described the wrong object.  Evaluate the
    # configuration itself and locate the runs on either side of 0.
    own = count(cfg)
    own_count = own[0] if own else None
    left = right = None
    inside = None
    for c, lo, hi, nch, profs, tc in runs:
        if hi == 0:
            left = (c, nch)
        if lo == 0:
            right = (c, nch)
        if lo < 0 < hi:
            inside = (c, lo, hi, nch)
    on_wall = inside is None
    vals = [r[0] for r in runs if r[0] is not None]
    extends = None
    if on_wall:
        extends = [left[0] == own_count if left else None,
                   right[0] == own_count if right else None]
    return {'own_count': own_count, 'on_wall': on_wall,
            'left': list(left) if left else None,
            'right': list(right) if right else None,
            'inside': list(inside[:1]) + [str(inside[1]), str(inside[2]), inside[3]]
                      if inside else None,
            'extends_into_chamber': extends,
            'max_on_line': (own_count == max(vals + [own_count])) if vals else None,
            'wrap_count': (lambda w: w[0] if w else None)(
                count(base + [tuple([0] + list(d))])),
            'wall_kind_at_zero': kind.get(F(0), 'not-a-root')}


def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 30000.0
    out = []
    for n, Q in sorted(RECORDS.items()):
        cls = classes(Q, n)
        log('n=%d: %d (count, profile) classes over k=3..%d' % (n, len(cls), n - 1))
        for rep in cls:
            if time.time() - T0 > budget:
                log('budget reached')
                json.dump(out, open(OUT, 'w'), indent=1)
                return
            log('  n=%d k=%d count=%d idxs=%s' % (n, rep['k'], rep['count'], rep['idxs']))
            for t in range(rep['k']):
                for d in DIRS:
                    r = study(rep['cfg'], t, d, 'n%d k%d c%d cube%d %s'
                              % (n, rep['k'], rep['count'], t, d))
                    r.update(n=n, k=rep['k'], count=rep['count'],
                             profile=list(rep['profile']), idxs=list(rep['idxs']),
                             moved=t, direction=list(d))
                    out.append(r)
                    if 'own_count' in r:
                        log('     cube %d dir %-11s count %s  on_wall=%s (%s)  '
                            'left/right %s/%s  extends %s  max_on_line=%s'
                            % (t, str(d), r['own_count'], r['on_wall'],
                               r['wall_kind_at_zero'],
                               r['left'][0] if r['left'] else None,
                               r['right'][0] if r['right'] else None,
                               r['extends_into_chamber'], r['max_on_line']))
                json.dump(out, open(OUT, 'w'), indent=1)
    json.dump(out, open(OUT, 'w'), indent=1)
    log('done: %d measurements' % len(out))


if __name__ == '__main__':
    main()
