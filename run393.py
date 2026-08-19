#!/usr/bin/env python3
"""The 393 neighbourhood, COMPLETE — the first for a rational record.

Postscript 122 recorded the rational records' neighbourhoods as uncharacterised:
the face enumeration is 3^27 at 727 and died, and single-wall crossings do not
exist (all walls entangled, Postscript 140). Postscript 143 then sized 727 at
14M-36M chambers -- days of compute and, on this 16 GB machine, 18 GB of memory
against 16 available, so it cannot finish here at any time budget (Postscript 144).

n = 5 fits comfortably: 18 walls, rank 11 of ambient 12, Zaslavsky bound 218 588
chambers -- 0.05 GB and about 3 core-hours. Completable on this hardware today.

CHAMBERS ONLY: faces() is unsound (rate decayed 7 800/s -> 119/s, Postscript 142)
and is not invoked. Counts come from the infinitesimal engine, so no step size.
"""
import json, os, sys, time
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from arrangement import run_parallel, zaslavsky_bound


def main():
    W, ncols = walls_of(BASE)                 # BASE is the 393 five-cube record
    import dimension as D
    rank = ncols - len(D.nullspace(W, ncols))
    print('393: %d walls, rank %d of %d | Zaslavsky bound %s'
          % (len(W), rank, ncols, '{:,}'.format(zaslavsky_bound(len(W), rank))), flush=True)
    ck = os.path.join(HERE, 'ckpt_393')
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 86400
    os.makedirs(ck, exist_ok=True)
    if not os.path.exists(os.path.join(ck, 'BUDGET')):
        open(os.path.join(ck, 'BUDGET'), 'w').write('%d\n' % int(budget))
    t0 = time.time()
    res = run_parallel(W, ncols, 0, '393-chambers', ck, nworkers=4,
                       max_codim=0, time_budget=budget)
    print('elapsed %.0fs' % (time.time() - t0), flush=True)
    try:
        json.dump({'walls': len(W), 'rank': rank, 'ambient': ncols,
                   'bound': zaslavsky_bound(len(W), rank), 'result': str(res)[:2000]},
                  open(HERE + '/run393.json', 'w'), indent=1)
    except Exception as e:
        print('summary write failed: %s' % e, flush=True)


if __name__ == '__main__':
    main()
