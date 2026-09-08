#!/usr/bin/env python3
"""Where does the climb GET TO from a random compound, and how much volume leads there?

For each region count c: the Haar volume of the set of configurations from which the
climb terminates at c.  Each start is an i.i.d. exactly-Haar draw (haarsample.py), so
the histogram of terminal counts IS that volume distribution, with binomial errors.

THE CLIMBER IS climb.py's, not a new one.  A basin belongs to a climber, so measuring
the basin of a second climber would answer about the second climber.  The only thing
changed is the DIRECTION MENU, and only because climb.py's own menu is undefined at a
random start: its directions come from the null space of the TIGHT walls, and a
Haar-random configuration has none (measured at n=4: 0 tight walls, nullity 9 of 9),
so that path degenerates to the coordinate basis with coefficients in [-2,2] --
axis-aligned and small-integer, the two biases that voided earlier direction choices
here.  So `menu` supplies isotropic directions instead: integer vectors drawn
uniformly from a ball, exact and primitive, no axis preferred.  Everything below the
menu is climb.py unchanged -- the ray walk, the bisection to the FIRST crossing, the
low-height re-representation, and the two-engine + three-rotation gate on every
accepted move.

MENU SIZE IS A METHOD PARAMETER.  A larger menu can only find more crossings, so every
terminal count here is a LOWER bound on what climbing can reach and every basin volume
for a given c is an estimate for THIS menu.  NDIR is recorded in each output line and
`--sat` re-runs the same starts at several NDIR to show whether it has saturated.

START HEIGHT.  Probe points cost Q^2 * M in coordinate height and both engines
refuse above ~1e8 (measured, and the same ceiling at n=4 and n=10), so the basin
starts are drawn at Q=128.  That is a coarser lattice than Phase 1's Q=30000, so
the two start-count distributions are compared directly rather than assumed
equal -- haarsample.py at both Q is the control.

Usage:  basin.py N K [Q] [shard] [NDIR]
"""
import json, os, random, sys, time
from math import gcd
sys.path.insert(0, '.')
import climb as C
import dimension as D
from haarsample import haar_config, count
from solved_scan import best_on_lines

RBALL = 1000
SCAN_NDIR = 6      # single-cube lines per cube in the solved termination test

def rand_dir(rng, m):
    """integer vector uniform in the m-ball: isotropic, exact, primitive"""
    R2 = RBALL * RBALL
    while True:
        v = [rng.randint(-RBALL, RBALL) for _ in range(m)]
        s = sum(x * x for x in v)
        if 0 < s <= R2:
            g = 0
            for x in v:
                g = gcd(g, abs(x))
            return tuple(x // g for x in v)

if __name__ == '__main__':
    n = int(sys.argv[1]); K = int(sys.argv[2])
    Q = int(sys.argv[3]) if len(sys.argv) > 3 else 30000
    shard = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    NDIR = int(sys.argv[5]) if len(sys.argv) > 5 else 12
    C.NDIR = NDIR
    out = 'basin_n%d_d%d_s%d.jsonl' % (n, NDIR, shard)
    done = sum(1 for _ in open(out)) if os.path.exists(out) else 0
    # two independent streams: the STARTS must not depend on NDIR, or the saturation
    # check would compare different starts and measure the sampler instead of the menu
    rng = random.Random(770001 + 131 * n + 7919 * shard)
    rngd = random.Random(31337 + 131 * n + 7919 * shard)
    for _ in range(done):                     # replay the start stream so restarts continue it
        haar_config(rng, n, Q, chart=True)
    menu = lambda ncols, it: [rand_dir(rngd, ncols) for _ in range(NDIR)]
    with open(out, 'a') as f:
        for i in range(done, K):
            cfg = haar_config(rng, n, Q, chart=True)
            c0 = count(cfg)
            if c0 is None:                    # unevaluable is not a negative result
                f.write(json.dumps({'i': i, 'start': None, 'end': None,
                                    'unevaluated': True}) + '\n'); f.flush()
                print('#%d UNEVALUATED start' % i, flush=True); continue
            t0 = time.time()
            # The ray walk is the cheap SEARCH; it must not be the termination TEST.
            # Measured on the first 8 climbs: 3 of 8 of its "locally maximal" verdicts
            # were premature -- the exactly-scanned single-cube lines reached 129 from a
            # configuration it stopped at 121, and 99 from one it stopped at 95. So each
            # time the walk gives up, every wall on n-1 families of single-cube lines is
            # SOLVED and the chambers along them counted exactly; only when that also
            # finds nothing higher does the climb terminate.
            cubes = list(cfg); rec = c0; scan_tot = scan_unev = 0; rounds = 0
            C.REFUSED.clear()
            while rounds < 12:
                rounds += 1
                cubes, rec2 = C.climb(cubes, 'basin n=%d s%d #%d r%d' % (n, shard, i, rounds),
                                      menu=menu, iters=40)
                if rec2 is None:
                    rec = None; break
                rec = rec2
                (b, cfg2), tot, unev = best_on_lines(cubes, ndir=SCAN_NDIR, reach=6,
                                                     seed=rounds, verbose=True)
                scan_tot += tot; scan_unev += unev
                if b > rec:
                    cubes = cfg2; rec = b
                    continue
                break
            # rec is None when climb.py could not DECIDE (every probe refused by both
            # engines). That is not a terminal count and must never be histogrammed as
            # one; it is recorded and counted separately.
            f.write(json.dumps({'i': i, 'start': c0, 'end': rec,
                                'undetermined': rec is None,
                                'secs': round(time.time() - t0, 1),
                                'cfg0': [list(q) for q in cfg],
                                'cfg1': [list(q) for q in cubes],
                                # An UNDETERMINED climb is not a lost sample: it reached
                                # a real count before the engines gave out, and those
                                # counts are the HIGHEST in the run (n=4 climbs reached
                                # 137 and 141, above the 4000-draw Haar maximum of 135).
                                # Dropping them biases the distribution down at exactly
                                # the end that matters, so the best evaluable count and
                                # the width that would have been needed are both kept.
                                'best_evaluable': count(cubes),
                                'refused_probes': len(C.REFUSED),
                                'refused_max_height': max(C.REFUSED) if C.REFUSED else 0,
                                'bits_needed_max': round(C.required_bits(max(C.REFUSED)), 1)
                                                   if C.REFUSED else 0,
                                'rounds': rounds, 'scan_chambers': scan_tot,
                                'scan_unevaluated': scan_unev,
                                'params': {'NDIR': NDIR, 'RBALL': RBALL, 'Q': Q,
                                           'M': C.M, 'iters': 40,
                                           'SCAN_NDIR': SCAN_NDIR}}) + '\n'); f.flush()
            print('=== n=%d s%d #%d  %d -> %s  %.0fs' % (n, shard, i, c0,
                  'UNDETERMINED' if rec is None else rec, time.time() - t0), flush=True)
