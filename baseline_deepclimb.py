#!/usr/bin/env python3
"""BASELINE: the method that actually found 183, run from RANDOM starts.

`n4_search_report.md` records how the n=4 record was found -- greedy +-1/+-2 climbing,
radius-4 certification, then WIDE perturbations (1-6 simultaneous components, each +-1..4)
fired at the original start and re-climbed. The documented chain is
159 -> 171 -> 173 -> 175 -> 179 -> 183, every arrow an escape from a certified local
maximum that no single-component move could leave.

But phase D was seeded from S1_CHAMPION, a STRUCTURED octahedral-type configuration at
159. So the documented result is "structured seed + wide-escape climb". This baseline
separates the two: run the same method from Haar-random starts and see where it lands.

  if it reaches ~183   the METHOD was decisive and every climber built here since --
                       wall-crossing moves in Cayley coordinates, 3900 walls between
                       local maxima -- was using the wrong move set;
  if it stalls lower   the SEED was decisive, and structure is what the search needs,
                       which is what this session's ensemble work has been finding.

The historical log is not touched: `n4_search.py` opens n4_search.jsonl in append mode at
import, so the module's handle is redirected before anything runs. Never edit the run's
data files.
"""
import os, random, sys
sys.path.insert(0, '.')

import n4_search as N
N._LOGF.close()
N.LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'n4_baseline.jsonl')
N._LOGF = open(N.LOG_PATH, 'a')

from haarsample import haar_quat

if __name__ == '__main__':
    starts = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    rng = random.Random(2718)
    print('baseline: the documented deep-climb method, from %d Haar-random starts' % starts,
          flush=True)
    print('(documented chain from a STRUCTURED seed: 159 -> 171 -> 173 -> 175 -> 179 -> 183)',
          flush=True)
    for i in range(starts):
        q = [(1, 0, 0, 0)] + [haar_quat(rng, 6) for _ in range(3)]
        print('\n=== start %d: %s' % (i, ';'.join(','.join(map(str, c)) for c in q)), flush=True)
        try:
            N.phaseD_deepclimb([list(c) for c in q], n_restarts=restarts, seed=1000 + i)
        except Exception as e:
            print('   failed: %s' % str(e)[:120], flush=True)
    print('\ntotal rational evaluations: %d' % N.EV.evals, flush=True)
