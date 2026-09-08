#!/usr/bin/env python3
"""Constraint SIGNATURES, and which ones nobody has evaluated.

The user's program, and its sting in the tail: a filter tuned to look like the known
records can only rediscover what we already have. Demonstrated concretely -- the n=4
record has max plane-concurrence 6 and today's breakthrough (the shared-axis 161) has 8,
so a "concurrence >= the record's" filter would have discarded the most productive
configuration of the day. Fitness-shaped filters are circular here.

CORRECTED 2026-09-07: this paragraph first read "the record has 9, the shared-axis 161 has
8" -- both from `planes()` reading matrix ROWS, i.e. the inverse rotation. With the columns
the record has 6 and the 161 has 8, so the record is BELOW the shared-axis configuration on
this statistic and the filter would have been circular in the other direction. The lesson
is unchanged and the numbers are not; see [P227]. Every signature below is likewise a
different function from the one this file first computed.

The non-circular version is to catalogue the constraint structure itself and look for
combinations NOBODY HAS EVALUATED, rather than combinations that resemble the record. So
the signature recorded here is the full histogram of plane-concurrence multiplicities --
"one 9-fold, three 5-folds, ..." -- not a single fitness-like scalar. Two configurations
with the same signature have the same incidence combinatorics at this resolution; if their
counts differ, the signature underdetermines the count, and by how much is measurable
rather than arguable.

This is also the direct test of "does a given set of roots determine a set of possible
counts": group by signature and look at the spread inside each group.
"""
import itertools, json, random, subprocess, sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
from concurrence import planes, solve3
from sharedaxis import q_axis
from symmetrize import axes
from haarsample import haar_config

def signature(cfg, cap=12):
    """histogram of plane-concurrence multiplicities, as a hashable signature"""
    P = planes(cfg)
    pts = Counter()
    for i, j, k in itertools.combinations(range(len(P)), 3):
        s = solve3(P[i], P[j], P[k])
        if s is not None:
            pts[s] += 1
    mult = Counter()
    for _, c in pts.items():
        m = 3
        while m * (m - 1) * (m - 2) // 6 < c:
            m += 1
        if m >= 4:                       # 3-fold points are generic and everywhere
            mult[min(m, cap)] += 1
    return tuple(sorted(mult.items()))

def count(cfg):
    s = ';'.join(','.join(map(str, q)) for q in cfg)
    try:
        return json.loads(subprocess.run(['./cube_regions_n', '--quats', s],
                                         capture_output=True, text=True).stdout).get('bounded')
    except Exception:
        return None

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    KNOWN = {
        'n=4 record 183': [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)],
        'shared-axis 161': [(1,0,0,0),(1,-8,-8,0),(6,-5,-5,0),(5,-4,-4,0)],
    }
    print('KNOWN configurations and their constraint signatures:')
    known_sigs = {}
    for name, cfg in KNOWN.items():
        sg = signature(cfg)
        known_sigs[sg] = name
        print('  %-18s count %3d   signature %s' % (name, count(cfg), sg), flush=True)
    print()
    rng = random.Random(9); AX = axes(3)
    vals = [F(p, q) for q in (1,2,3,4,5,6) for p in range(-6,7) if p and gcd(abs(p), q) == 1]
    groups = defaultdict(list)
    for i in range(N):
        cfg = (haar_config(rng, 4, 64, chart=True) if i % 2 else
               [(1,0,0,0)] + [q_axis(rng.choice(AX), rng.choice(vals)) for _ in range(3)])
        c = count(cfg)
        if not c:
            continue
        groups[signature(cfg)].append(c)
    print('%d distinct signatures over %d configurations' % (len(groups), sum(len(v) for v in groups.values())))
    print()
    print('DOES A SIGNATURE DETERMINE THE COUNT?  (groups with >1 member)')
    multi = {s: v for s, v in groups.items() if len(v) > 1}
    for s, v in sorted(multi.items(), key=lambda kv: -len(kv[1]))[:8]:
        print('  n=%-3d counts %4d..%-4d spread %3d   sig %s'
              % (len(v), min(v), max(v), max(v) - min(v), s))
    det = sum(1 for v in multi.values() if min(v) == max(v))
    print('  -> %d of %d repeated signatures pin the count exactly' % (det, len(multi)))
    print()
    print('SIGNATURES SEEN, ranked by best count -- the top ones are where to look next')
    for s, v in sorted(groups.items(), key=lambda kv: -max(kv[1]))[:6]:
        tag = '   <-- ' + known_sigs[s] if s in known_sigs else ''
        print('  best %4d  (n=%2d)  %s%s' % (max(v), len(v), s, tag))
