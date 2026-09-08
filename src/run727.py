#!/usr/bin/env python3
"""The 727 chamber run — launched knowing it may not finish, because a PARTIAL
enumeration is itself the deliverable.

Postscript 143 sized this honestly: 14M-36M chambers extrapolated, at a MEASURED
85.8 ms per count at n = 6, so 330-860 core-hours -- 3.5 to 9 days on 4 cores, not
a weekend. Restart is verified (Postscript 143), so a kill costs only the in-flight
item, and the deliverables do not require completion:

  * the chamber-count curve to a deeper wall count than 19
  * the region-count distribution over however many chambers get evaluated
  * the ratio behaviour, which decides whether continuing is worth it

CHAMBERS ONLY. `faces()` is NOT invoked: its lower-dimensional descent is unsound
(rate decayed 7 800/s -> 119/s, quadratic in output, Postscript 142) and would burn
the budget for nothing.

The known bottleneck is `_fm`'s Fourier-Motzkin blowup -- 0.4% of candidates cost
>= 3 s and one was caught at 9+ minutes. Replacing it with an exact rational
simplex is the right optimisation and has NOT been done; this run proceeds with the
slow LP, which is the main reason the estimate is days rather than hours.
"""
import json, os, sys, time
import os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from growth727 import walls_of, BASE
from arrangement import run_parallel, zaslavsky_bound

def main():
    W,ncols=walls_of(BASE+[(7,14,1,-5)])
    rank=None
    import dimension as D
    rank=ncols-len(D.nullspace(W,ncols))
    print('727: %d walls, rank %d of %d | Zaslavsky bound %s'
          %(len(W),rank,ncols,'{:,}'.format(zaslavsky_bound(len(W),rank))),flush=True)
    print('extrapolated actual 14M-36M chambers; this run may not finish, and that '
          'is expected -- partial output is the deliverable',flush=True)
    # BUDGET IS RE-READ FROM A FILE, so it can be raised or lowered WITHOUT
    # killing the run. Restart is cheap here (verified: a relaunch recomputes
    # nothing), but a live control file costs even the in-flight candidates
    # nothing, and it lets a run be extended by someone who is not watching the
    # clock. Write seconds into ckpt_727/BUDGET to change it; delete it to fall
    # back to the argv value.
    budget=float(sys.argv[1]) if len(sys.argv)>1 else 172800     # 48h default
    bf=os.path.join(HERE,'ckpt_727','BUDGET')
    os.makedirs(os.path.dirname(bf),exist_ok=True)
    if not os.path.exists(bf):
        open(bf,'w').write('%d\n'%int(budget))
    print('budget control file: %s (edit it to extend; re-read each stage)'%bf,flush=True)
    ck=os.path.join(HERE,'ckpt_727')
    t0=time.time()
    res=run_parallel(W,ncols,0,'727-chambers',ck,nworkers=4,
                     max_codim=0,            # CHAMBERS ONLY -- no face descent
                     time_budget=budget)
    print('elapsed %.0fs'%(time.time()-t0),flush=True)
    try: json.dump({'walls':len(W),'rank':rank,'result':str(res)[:2000]},
                   open(HERE+'/run727.json','w'),indent=1)
    except Exception as e: print('summary write failed: %s'%e,flush=True)

if __name__=='__main__':
    main()
