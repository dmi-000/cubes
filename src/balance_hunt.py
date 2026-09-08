#!/usr/bin/env python3
# Working principles: record_hunt.py (engines, menus, neighbourhoods).
"""Subset-balanced search at n=6, aimed at the predicted 729.

Motivation.  T = count(S_j) + delta_j for every cube j (dropping a cube only
merges regions), so a record at level n needs EVERY (n-1)-subset above
T - max_j delta_j -- not just the best one, which is all E1 constrains.  The
727 record's 5-subsets are 393, 385, 385, 385, 383, 377: one strong subset
and a tail 16 below it.  Two searches follow from that, neither of which a
total-only +-2 climb can reach:

  A. SWAP-COMPLETION.  Drop each cube of 727 in turn and re-optimise the
     replacement over a wide-height menu.  Five of the six resulting
     five-cube bases (385, 385, 385, 383, 377) have never been completed --
     only the 393 one has, twice.
  B. BALANCED CLIMB.  Climb 727 on a lexicographic (min 5-subset, total)
     objective, so moves that lift the weak tail are taken even when they do
     not immediately raise the total.  A total-only climb rejects exactly
     those moves, which is why the plateau looks flat to it.

INVARIANT: the objective may be the balanced one, but a RECORD is still a
total; every config with total > 727 is logged separately regardless of how
it scored, and nothing is claimed until certify_six agrees.
"""
import itertools
import random
import sys

import record_hunt as R

W = 2
BEST_KNOWN = 727
OUT = open('balance_hunt.jsonl', 'a')
rng = random.Random(729729)

REC = [[4, 1, 1, -1], [3, 3, 7, 3], [5, -1, -5, -5], [2, 1, 1, 1],
       [1, 1, 1, 1], [7, 14, 1, -5]]                    # 727

e6 = R.Engine(6, W)
e5 = R.Engine(5, W)
hits = []


def profile(cfg):
    """(total, sorted 5-subset counts) -- the whole constraint, not just max."""
    tot = e6.count([cfg])[0][0]
    subs = [[q for i, q in enumerate(cfg) if i != j] for j in range(len(cfg))]
    counts = sorted((r[0] for r in e5.count(subs)), reverse=True)
    return tot, counts


def note(tag, cfg, tot, counts):
    R.log(OUT, stage=tag, total=tot, subsets=counts, quats=cfg)
    if tot > BEST_KNOWN:
        hits.append((tot, cfg, counts))
        print('*** TOTAL %d  subsets %s  %s' % (tot, counts, R.fmt(cfg)),
              flush=True)


# ---------------------------------------------------------------- A: swaps
print('=== A: swap-completion, one dropped cube at a time', flush=True)
for j in range(6):
    base = [q for i, q in enumerate(REC) if i != j]
    base_ct = e5.count([base])[0][0]
    cands = [base + [q] for q in R.menu(8000, rng)]
    res = e6.count(cands)
    order = sorted(range(len(cands)), key=lambda k: -res[k][0])
    print('drop cube %d (5-subset %d) -> best %s'
          % (j, base_ct, [res[k][0] for k in order[:6]]), flush=True)
    for k in order[:3]:
        cfg, tot = R.climb(e6, cands[k], OUT, 'swap%d_%d' % (j, k), rng,
                           restarts=2)
        t, c = profile(cfg)
        note('swap_climbed', cfg, t, c)
        print('   climbed %d  subsets %s' % (t, c), flush=True)

# ------------------------------------------------------------ B: balanced
print('=== B: balanced climb, objective (min 5-subset, total)', flush=True)


def score(cfg):
    tot, counts = profile(cfg)
    note('scored', cfg, tot, counts)
    return (counts[-1], tot), tot, counts


cur = [list(q) for q in REC]
best_sc, tot, counts = score(cur)
print('start 727 subsets %s' % counts, flush=True)
for sweep in range(60):
    cands = R.neighbors(cur, rng)
    improved = False
    for c in cands:
        sc, t, cc = score(c)
        if sc > best_sc:
            cur, best_sc, improved = c, sc, True
            print('balanced step -> min-subset %d, total %d  %s'
                  % (sc[0], sc[1], R.fmt(c)), flush=True)
    if not improved:
        break
    R.log(OUT, stage='balanced_step', total=best_sc[1], minsub=best_sc[0],
          quats=cur)

print('BALANCED BEST: min-subset %d, total %d\n%s'
      % (best_sc[0], best_sc[1], R.fmt(cur)), flush=True)
R.log(OUT, stage='balanced_best', total=best_sc[1], minsub=best_sc[0],
      quats=cur)
print('configs above %d: %s' % (BEST_KNOWN, sorted(h[0] for h in hits)),
      flush=True)
R.log(OUT, stage='done', evals6=e6.evals, evals5=e5.evals,
      hits=[h[0] for h in hits])
