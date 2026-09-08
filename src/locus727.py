#!/usr/bin/env python3
"""Is the n=6 rung 727 a continuum?  Exhaustive direction sweep in the last-cube slice.

[P182] found 1217, 1895 and 2785 all to be continua, each with the recorded member
at an ENDPOINT of its interval.  727 alone showed nothing — but only two families
had been tried there: 15 integer-offset directions (shapes.py) and the solved
13-pair curves (rungshapes.py).  Neither is a survey.

Here every direction in {-2..2}^4 up to sign and scale is swept at rational
resolution 1/12, the same resolution at which 1895's locus became visible where the
integer sweep had seen a single point.

SCOPE, stated because the negative depends on it: this moves only the LAST cube, a
3-dimensional slice of the 15-dimensional gauge-fixed configuration space.  A locus
that requires moving earlier cubes is invisible here.  That restriction is the same
one under which 1217, 1895 and 2785 DID show loci, so the comparison is like-for-
like — but "no locus in this slice" is not "no locus".
"""
import json, subprocess, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
from growth727 import BASE

C6 = BASE + [(7, 14, 1, -5)]
LAST = C6[-1]
STEP, REACH = 12, 4


def canon(q):
    den = 1
    for x in q:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    w = [int(F(x) * den) for x in q]
    g = 0
    for v in w:
        g = gcd(g, abs(v))
    if g == 0: return None
    w = [v // g for v in w]
    for v in w:
        if v > 0: break
        if v < 0: w = [-x for x in w]; break
    return tuple(w)


def batch(cfgs):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run(['./cube_regions_q2w', '--d', '0', '--quats-stdin'],
                       input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l).get('bounded'))
        except Exception: out.append(None)
    return out + [None] * (len(cfgs) - len(out))


dirs = []
seen = set()
for a in range(-2, 3):
    for b in range(-2, 3):
        for c in range(-2, 3):
            for d in range(-2, 3):
                v = canon((a, b, c, d))
                if v and v not in seen:
                    seen.add(v); dirs.append(v)
print('%d directions, step 1/%d, |t| <= %d  (%d evaluations)'
      % (len(dirs), STEP, REACH, len(dirs) * (2 * REACH * STEP + 1)), flush=True)

ts = [F(k, STEP) for k in range(-REACH * STEP, REACH * STEP + 1) if k]
hits, nun, ntot, best = [], 0, 0, 0
for d in dirs:
    cfgs = [C6[:-1] + [canon(tuple(x + t * y for x, y in zip(LAST, d)))] for t in ts]
    vals = batch(cfgs)
    ntot += len(vals); nun += sum(1 for v in vals if v is None)
    best = max([best] + [v for v in vals if v is not None])
    runs, cur = [], None
    for t, v in zip(ts, vals):
        if v == 727:
            cur = [t, t] if cur is None else [cur[0], t]
        elif cur:
            runs.append(tuple(cur)); cur = None
    if cur: runs.append(tuple(cur))
    for lo, hi in runs:
        hits.append((d, lo, hi))
        print('   dir %-14s 727 holds on [%s, %s] width %s (%d pts)'
              % (str(d), lo, hi, hi - lo, int((hi - lo) * STEP) + 1), flush=True)

print('\n%d evaluations, %d unevaluable, %d intervals found, max count seen %d'
      % (ntot, nun, len(hits), best), flush=True)
json.dump({'dirs': len(dirs), 'step': STEP, 'reach': REACH, 'evals': ntot,
           'unevaluable': nun, 'max_seen': best,
           'intervals': [[list(d), str(a), str(b)] for d, a, b in hits]},
          open('locus727.json', 'w'), indent=1)
