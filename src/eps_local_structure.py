#!/usr/bin/env python3
"""TAXONOMY 12a, asked exactly: along which DIRECTIONS does the signature survive?

12a reported "the signature is never preserved, at any scale" and concluded signature space
has no local structure -- which is why navigation was abandoned and ensemble construction
built instead (METHODS 23a). Those numbers are void (broken normals, [P227]) and unsourced
(no script, no postscript). A finite-step replacement gave ~35 % preserved, flat from 2^-4
to 2^-20 -- but four scales agreeing is exactly what CO-LOCATION looks like from inside, so
it settles nothing on its own.

This asks the question with the step size removed: perturb by an infinitesimal e and test
the signature exactly, in Z[e] ordered by the sign of the lowest nonzero coefficient.

TWO THINGS IT FIXES BEYOND EXACTNESS:

1. The answer is per-DIRECTION. "Is the signature preserved" has no scalar answer; there is
   a set of directions along which it survives, and a percentage was always a lossy summary
   of that set. Reported here as the per-configuration distribution -- all directions, none,
   or some -- because "35 % of (config, direction) pairs" cannot distinguish a third of
   configurations surviving everything from every configuration surviving a third of
   directions, and those are completely different geometries.

2. It CONDITIONS on the base being degenerate. A configuration whose signature is already
   empty has no coincidence to break, so preservation is trivial and says nothing about
   strata. 12a's claim is about degenerate strata specifically, and roughly a quarter of
   sampled configurations are not on one -- pooling them inflates any preservation rate.

Cost, stated because it is the argument's weak point: 0.37 s per (config, direction) against
0.0087 s for a finite step at 2^-26. The exact version is 45x MORE expensive, not less. It
is bought for correctness, not speed.
"""
import json, random, sys, time
from collections import Counter
sys.path.insert(0, '.')
from eps_signature import signature_e, perturb_generic, lift
from haarsample import haar_config
from sharedaxis import q_axis
from symmetrize import axes
from fractions import Fraction as F
from math import gcd

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    D = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 23
    OUT = sys.argv[4] if len(sys.argv) > 4 else 'eps_local_structure.json'
    rng = random.Random(SEED)
    AX = axes(3)
    vals = [F(p, q) for q in (1, 2, 3, 4, 5, 6) for p in range(-6, 7)
            if p and gcd(abs(p), q) == 1]

    triv = Counter(); nontriv = Counter()
    ntriv = nnon = 0
    t0 = time.time()
    for i in range(N):
        cfg = (haar_config(rng, 4, 64, chart=True) if i % 2 else
               [(1, 0, 0, 0)] + [q_axis(rng.choice(AX), rng.choice(vals)) for _ in range(3)])
        cfg = [tuple(q) for q in cfg]
        base, _ = signature_e([lift(q) for q in cfg])
        kept = 0
        for _ in range(D):
            s, _ = signature_e(perturb_generic(cfg, rng))
            kept += (s == base)
        if base:
            nnon += 1; nontriv[kept] += 1
        else:
            ntriv += 1; triv[kept] += 1
        if (i + 1) % 25 == 0:
            print('  %d/%d configs, %.1f min' % (i + 1, N, (time.time() - t0) / 60), flush=True)

    def show(name, c, n):
        if not n:
            print('%s: none' % name); return
        pairs = sum(k * v for k, v in c.items()); tot = n * D
        print('\n%s: %d configurations' % (name, n))
        print('   preserved in %d of %d (config, direction) pairs = %.1f%%'
              % (pairs, tot, 100.0 * pairs / tot))
        print('   directions preserved, per configuration:')
        for k in range(D + 1):
            if c[k]:
                print('      %d of %d : %5d configs (%5.1f%%)%s'
                      % (k, D, c[k], 100.0 * c[k] / n,
                         '   <-- all' if k == D else ('   <-- none' if k == 0 else '')))
    show('DEGENERATE bases (non-empty signature) -- what 12a is about', nontriv, nnon)
    show('GENERIC bases (empty signature) -- preservation here is trivial', triv, ntriv)
    json.dump({'n': N, 'dirs': D, 'seed': SEED,
               'nontrivial': dict(nontriv), 'trivial': dict(triv)}, open(OUT, 'w'), indent=1)
    print('\nwrote %s' % OUT)
