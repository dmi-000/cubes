#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (mod-4 law). Project index: README.md
"""Test of the mod-4 conjecture for generic cube compounds.

Observation (2026-07-09): every certified generic count satisfies
  bounded == 2k - 1 (mod 4)          [k = number of cubes]
    k=4: all == 3 (55 samples)   k=5: all == 1 (36)   k=6: all == 3 (120+)
while k=2 (==0) and k=3 (mixed 1/2) break it, and wall/degenerate
configurations (axial 121, five-compound subsets 13/67/177/351) deviate.

Mechanism hypothesis: every configuration is centrally symmetric (each
concentric cube is), so the antipodal map pairs regions; the count is
(#invariant regions) mod 2.  At k <= 3 wrap-around shell regions can be
invariant (parity varies); at k >= 4 the shells are cut and only the core
survives, forcing odd counts; the finer mod-4 law is conjecturally the
Euler relation V - E + F = C on S^3 read mod 4 with the free antipodal
action on the skeleton (quotient RP^3) and the per-cube sphere relations
Sum chi(dC_k) = 2k.

This script tests the PREDICTION at k = 7: bounded == 13 == 1 (mod 4).
"""
import sys
import time

from scipy.spatial.transform import Rotation

from certify_six import rationalize, exact_count_config


def main(ks=(7,), nseeds=3):
    for k in ks:
        for s in range(nseeds):
            mats = [m for m in Rotation.random(k, random_state=777 + s)
                    .as_matrix()]
            rats = rationalize(mats, 512)
            t0 = time.time()
            total, bd = exact_count_config(rats, verbose=False)
            print(f'k={k} seed={777 + s}: EXACT {total}  '
                  f'mod4={total % 4} (predicted {(2 * k - 1) % 4})  '
                  f'({time.time() - t0:.0f}s)', flush=True)


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    ks = tuple(int(a) for a in sys.argv[1:]) or (7,)
    main(ks)
