#!/usr/bin/env python3
"""Re-measure TAXONOMY 12a: does signature space have local structure?

VOID and being replaced: the original reported median L1 histogram distance 66.0 / 66.0 /
71.0 at perturbations 2^-4 / 2^-8 / 2^-14, with the signature preserved 0% of the time at
every scale -- concluding there is no gradient to navigate, which is what killed navigation
as a search strategy and justified the ensemble-design program in METHODS 23a. Every one of
those numbers came from `concurrence.planes()` reading matrix ROWS instead of COLUMNS
([P227]). Unlike the rest of the correction this cannot be recomputed from the stored
census: it needs signatures of PERTURBED configurations, which were never stored.

THE CONTROL THE ORIGINAL DID NOT HAVE, and the reason this is worth rerunning rather than
patching. "0% unchanged at every scale" is exactly what a BROKEN COMPARISON also reports.
A measurement whose answer is "nothing ever matches" cannot distinguish a space with no
local structure from a comparison that never returns equal. So:

    GATE A (zero perturbation):  must give L1 = 0 and 100% unchanged.
    GATE B (non-degenerate):     the signatures compared must be non-empty, or the L1
                                 distance is between two empty histograms and means nothing.

Both must pass before any scale is believed. Exact throughout: a perturbation of 2^-k is
applied by scaling the integer quaternion by 2^k and adding an integer, so every
configuration stays rational and every incidence test stays an integer sign test.

Also widened, per "choose controls that are hard for the method": the original stopped at
2^-14. If the claim is that scale does not matter, the way to attack it is a scale far
outside the tested range, so 2^-20 and 2^-26 are included. If the L1 distance is still ~66
there, the claim is robust; if it collapses, the original range was the finding.

NO SOURCE SURVIVES FOR THE NUMBERS BEING REPLACED. There is no script in this repository
that produces 66.0 / 66.0 / 71.0, and no ledger postscript records the measurement -- so
12a's claim, the one that killed navigation as a search strategy and justified the whole
ensemble-design program in METHODS 23a, is unsourced as well as void. Its perturbation model
therefore cannot be inspected, which matters because the broken/corrected columns below show
the normals bug does NOT explain the disagreement: something about how it perturbed does,
and nobody can now say what. This file is the replacement and it is reproducible.

Usage:  local_structure.py [NCONF] [OUT.json] [SEED]
        run several seeds in parallel and merge; each is an independent sample.
"""
import itertools, json, random, sys
from collections import Counter, defaultdict
sys.path.insert(0, '.')
from resign_all import stats, solve3_int, mult
from haarsample import haar_config
from sharedaxis import q_axis
from symmetrize import axes, canon
from fractions import Fraction as F
from math import gcd

SCALES = [0, 4, 8, 14, 20, 26]          # 0 is the gate


def planes_broken(cfg):
    """the pre-[P227] version: ROWS of the rotation matrix, i.e. the inverse rotation"""
    out = []
    for (w, x, y, z) in cfg:
        n = w*w + x*x + y*y + z*z
        M = [[w*w+x*x-y*y-z*z, 2*(x*y-w*z), 2*(x*z+w*y)],
             [2*(x*y+w*z), w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
             [2*(x*z-w*y), 2*(y*z+w*x), w*w-x*x-y*y+z*z]]
        for r in range(3):
            out.append((M[r][0], M[r][1], M[r][2], n))
            out.append((M[r][0], M[r][1], M[r][2], -n))
    return out


def sig_broken(cfg):
    """signature under the broken normals -- kept ONLY so the two columns below differ in
    the one line under test. Without it a changed result cannot be attributed to the fix
    rather than to this script's perturbation differing from the original's."""
    P = planes_broken(cfg)
    cnt = defaultdict(int)
    for i, j, k in itertools.combinations(range(len(P)), 3):
        t = solve3_int(P[i], P[j], P[k])
        if t is not None:
            cnt[t] += 1
    h = Counter()
    for _, c in cnt.items():
        m = mult(c)
        if m >= 4:
            h[min(m, 12)] += 1
    return tuple(sorted(h.items()))


def perturb(cfg, k, rng):
    """exact perturbation of relative size ~2^-k: scale by 2^k, jog one component by 1"""
    if k == 0:
        return [tuple(q) for q in cfg]
    out = []
    for q in cfg[1:]:                    # cube 0 is the gauge and is never moved
        s = 1 << k
        t = [c * s for c in q]
        t[rng.randrange(4)] += rng.choice((-1, 1))
        out.append(canon(tuple(t)))
    return [tuple(cfg[0])] + out


def l1(a, b):
    A = Counter(dict(a)); B = Counter(dict(b))
    return sum(abs(A[m] - B[m]) for m in set(A) | set(B))


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    OUT = sys.argv[2] if len(sys.argv) > 2 else 'local_structure.json'
    SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 17
    rng = random.Random(SEED)
    AX = axes(3)
    vals = [F(p, q) for q in (1, 2, 3, 4, 5, 6) for p in range(-6, 7)
            if p and gcd(abs(p), q) == 1]

    bases = []
    for i in range(N):
        cfg = (haar_config(rng, 4, 64, chart=True) if i % 2 else
               [(1, 0, 0, 0)] + [q_axis(rng.choice(AX), rng.choice(vals)) for _ in range(3)])
        bases.append([tuple(q) for q in cfg])

    base_sigs = [stats(c)[0] for c in bases]
    nonempty = sum(1 for s in base_sigs if s)
    print('GATE B (non-degenerate): %d of %d base signatures are non-empty'
          % (nonempty, len(base_sigs)), flush=True)
    if nonempty < len(base_sigs) // 2:
        sys.exit('GATE B FAILED: comparing mostly-empty histograms measures nothing')

    bsigs = [sig_broken(c) for c in bases]
    res = {}
    print('\n  scale     CORRECTED normals        BROKEN normals (what 12a used)')
    print('            med L1   unchanged        med L1   unchanged')
    for k in SCALES:
        ds = []; same = 0; bd = []; bsame = 0
        for cfg, s0, b0 in zip(bases, base_sigs, bsigs):
            # THE SAME perturbed configuration is scored both ways, so the two columns
            # differ in exactly one line of code and nothing else.
            pc = perturb(cfg, k, rng)
            s1 = stats(pc)[0]; b1 = sig_broken(pc)
            ds.append(l1(s0, s1)); same += (s0 == s1)
            bd.append(l1(b0, b1)); bsame += (b0 == b1)
        ds.sort(); bd.sort()
        med = ds[len(ds) // 2]; bmed = bd[len(bd) // 2]
        pct = 100.0 * same / len(ds); bpct = 100.0 * bsame / len(bd)
        tag = '   <-- GATE A' if k == 0 else ''
        print('  2^-%-6s %6.1f  %7.1f%%        %6.1f  %7.1f%%%s'
              % (k if k else '0', med, pct, bmed, bpct, tag), flush=True)
        res[k] = {'median_l1': med, 'unchanged_pct': pct, 'n': len(ds),
                  'broken_median_l1': bmed, 'broken_unchanged_pct': bpct}
        if k == 0 and (med != 0 or pct != 100.0):
            sys.exit('GATE A FAILED: a ZERO perturbation changed the signature -- the '
                     'comparison is broken, and "0%% unchanged" at every scale would be '
                     'an artifact of it rather than a property of the space')
    res['_meta'] = {'n': N, 'seed': SEED, 'scales': SCALES}
    json.dump(res, open(OUT, 'w'), indent=1)
    print('\nwrote %s' % OUT)
    print('ORIGINAL (void, broken normals): 2^-4 66.0 / 2^-8 66.0 / 2^-14 71.0, 0%% unchanged')
