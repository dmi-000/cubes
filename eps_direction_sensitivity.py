#!/usr/bin/env python3
"""Does signature preservation depend on the DIRECTION SET, or on the space?

Two measurements of TAXONOMY 12a disagree, and they differ in two ways at once: step size
(finite vs infinitesimal) and direction set. The finite-step one jogs a single quaternion
component by +-1 -- eight axis-aligned directions per cube -- which is the "small-integer,
axis-aligned representative directions" failure this project has recorded before. So a
difference between them cannot be attributed to exactness until the direction set is
controlled.

This holds the step at an infinitesimal (exact, no scale) and varies ONLY the directions:

    axis      +-1 on one component      -- what the finite-step version used
    h=1       random v in [-1,1]^4
    h=5       random v in [-5,5]^4      -- what the eps version used
    h=50      random v in [-50,50]^4
    h=500     random v in [-500,500]^4

If the preservation rate is flat across these, it is a property of the space and both
measurements were sampling it fine. If it varies with the direction's HEIGHT, then both were
measuring their own direction sets -- and the tell is a clean split by height, which is the
signature of a badly chosen representative rather than of the object.

Restricted to DEGENERATE bases, since preservation is trivial when there is no coincidence
to break.
"""
import random, sys, time
from collections import Counter
sys.path.insert(0, '.')
from epsfield import trim
from eps_signature import signature_e, lift
from haarsample import haar_config
from sharedaxis import q_axis
from symmetrize import axes
from fractions import Fraction as F
from math import gcd


def perturb_dir(cfg, kind, rng):
    out = [lift(cfg[0])]
    for q in cfg[1:]:
        if kind == 'axis':
            v = [0, 0, 0, 0]
            v[rng.randrange(4)] = rng.choice((-1, 1))
        else:
            b = int(kind)
            v = [rng.randint(-b, b) for _ in range(4)]
            while not any(v):
                v = [rng.randint(-b, b) for _ in range(4)]
        out.append(tuple(trim((int(c), int(d))) for c, d in zip(q, v)))
    return out


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    KINDS = ['axis', '1', '5', '50', '500']
    rng = random.Random(31)
    AX = axes(3)
    vals = [F(p, q) for q in (1, 2, 3, 4, 5, 6) for p in range(-6, 7)
            if p and gcd(abs(p), q) == 1]

    bases = []
    while len(bases) < N:
        i = len(bases)
        cfg = (haar_config(rng, 4, 64, chart=True) if i % 2 else
               [(1, 0, 0, 0)] + [q_axis(rng.choice(AX), rng.choice(vals)) for _ in range(3)])
        cfg = [tuple(q) for q in cfg]
        sg, _ = signature_e([lift(q) for q in cfg])
        if sg:                                   # DEGENERATE bases only
            bases.append((cfg, sg))
    print('%d degenerate bases, %d directions each, exact (no step size)\n' % (N, D), flush=True)

    print('%-8s %12s %s' % ('direction', 'preserved', 'per-config: directions preserved'))
    t0 = time.time()
    for kind in KINDS:
        per = Counter(); kept = 0
        for cfg, sg in bases:
            k = 0
            for _ in range(D):
                s, _ = signature_e(perturb_dir(cfg, kind, rng))
                k += (s == sg)
            per[k] += 1; kept += k
        label = 'axis+-1' if kind == 'axis' else 'h=%s' % kind
        print('%-8s %11.1f%%  %s   (%.1f min)'
              % (label, 100.0 * kept / (N * D),
                 ' '.join('%d:%d' % (i, per[i]) for i in range(D + 1)),
                 (time.time() - t0) / 60), flush=True)
    print('\nFlat across rows -> a property of the space. Varying with height -> both')
    print('measurements were reporting their own direction sets.')
