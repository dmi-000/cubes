#!/usr/bin/env python3
# Working principles: MULTIWALL_SPEC.md + multiwall_report.md. Project index: README.md
"""Extend M4: more random trials + deeper hillclimb from the top few starts."""
import json
from multiwall_m4 import (rand_quat, build_config, run_batch, log, gcd_reduce,
                           QD, qmul)
import random

def main():
    rng = random.Random(4242)
    batch = []
    for i in range(1500):
        while True:
            q1, q3, q5, q6 = (rand_quat(rng) for _ in range(4))
            quats = build_config(q1, q3, q5, q6)
            if quats is not None:
                break
        batch.append((f'r2_{i}', quats))
    results = run_batch(batch)
    scored = []
    for tag, quats, total, bd in results:
        log(dict(family='M4_doublewall', tag=tag, quats=quats, total=total,
                  by_depth=bd))
        scored.append((total, tag, quats, bd))
    scored.sort(reverse=True)
    print('top 5 fresh random:', [(s[0], s[1]) for s in scored[:5]])

    # hillclimb from top 3 distinct starts
    from multiwall_m4 import MAXC
    for rank, (total0, tag0, quats0, bd0) in enumerate(scored[:3]):
        q1, q2, q3, q4, q5, q6 = quats0
        cur = (q1, q3, q5, q6)
        cur_total = total0
        print(f'\nhillclimb #{rank} start total={cur_total}')
        for step in range(15):
            nbrs = []
            for idx in range(4):
                base = list(cur)
                q = list(base[idx])
                for comp in range(4):
                    for delta in (-2, -1, 1, 2):
                        qn = list(q)
                        qn[comp] += delta
                        qn = gcd_reduce(tuple(qn))
                        cand = list(base)
                        cand[idx] = qn
                        nbrs.append(tuple(cand))
            nbatch = []
            seen = set()
            for nb in nbrs:
                if nb in seen:
                    continue
                seen.add(nb)
                quats = build_config(*nb)
                if quats is not None:
                    nbatch.append((nb, quats))
            results = run_batch([(str(n), q) for n, q in nbatch])
            best_nb, best_total, best_bd = None, cur_total, None
            for (tag, quats, total, bd), (nb, _) in zip(results, nbatch):
                log(dict(family='M4_doublewall_climb', run=rank, step=step,
                          tag=tag, quats=quats, total=total, by_depth=bd))
                if total > best_total:
                    best_nb, best_total, best_bd = nb, total, bd
            if best_nb is None:
                print(f'  step {step}: LOCAL MAX total={cur_total}')
                break
            cur, cur_total = best_nb, best_total
            print(f'  step {step}: total={cur_total}', flush=True)
        print(f'hillclimb #{rank} final: {cur_total} at {cur}')

if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    main()
