#!/usr/bin/env python3
"""Geometric test of P155's factorisation: is EVERY 393 chamber cut into exactly 62?

WHY.  P155 found chi_727 = chi_393 . (t-1)(t^2-8t+22) despite 8 of 27 walls
coupling the old and new coordinate blocks (P154), so there is no product
structure to explain it.  Stanley's modular factorisation theorem does: if the
flat X = intersection of the 18 old walls is MODULAR in L(A_727), then
chi_{A_X} | chi_A, and A_X is exactly 393's arrangement.

THE GEOMETRIC CONTENT, and what makes it falsifiable.  The quotient expands as
g(t) = t^3 - 9t^2 + 30t - 22 with |coefficients| summing to 1+9+30+22 = 62.
Modularity forces the subdivision to be UNIFORM: every chamber of the 393
arrangement (inflated to R^15) must be cut into exactly 62 chambers by the 9 new
walls.  Not 62 on average -- 62 every time.  A single chamber cut into any other
number refutes the modular explanation while leaving the polynomial identity
intact, which is precisely the kind of test worth running: it can fail without
contradicting anything already established.

METHOD.  For a sampled 393 chamber, fix its sign vector on the 18 old walls and
enumerate feasible sign extensions over the 9 new walls by incremental
construction with the exact LP.  No floating point decides anything.
"""
import json, os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from exactlp import feasible_strict

DEFAULTS = {'n': 25, 'seed': 20260822}


def main():
    cfg = dict(DEFAULTS)
    for a in sys.argv[1:]:
        k, v = a.split('=', 1); cfg[k] = type(DEFAULTS[k])(v)
    W7, nc = walls_of(BASE + [(7, 14, 1, -5)])
    W3, n3 = walls_of(BASE)
    old = [i for i, w in enumerate(W7) if all(x == 0 for x in w[n3:])]
    new = [i for i in range(len(W7)) if i not in old]
    print('727: %d walls | old(=393) %d | new %d | ambient %d'
          % (len(W7), len(old), len(new), nc), flush=True)
    assert len(old) == 18 and len(new) == 9

    # 393 chambers, as sign vectors on the OLD walls, from the completed campaign.
    import glob
    sigs = []
    for f in glob.glob(os.path.join(HERE, 'ckpt_393', 'worker_*.jsonl')):
        for line in open(f):
            try:
                r = json.loads(line)
            except Exception:
                continue
            s = r['sigma']
            if s.count(',') == 17 and r['witness'] is not None:
                sigs.append(tuple(int(x) for x in s.split(',')))
    print('%d complete 393 chambers on disk; sampling %d' % (len(sigs), cfg['n']), flush=True)
    rnd = random.Random(cfg['seed'])
    sample = rnd.sample(sigs, min(int(cfg['n']), len(sigs)))

    counts, t0 = [], time.time()
    for idx, sig in enumerate(sample):
        base = [[s * W7[old[j]][t] for t in range(nc)] for j, s in enumerate(sig)]
        frontier = [[]]
        for k in new:
            nxt = []
            for ext in frontier:
                rows = base + [[e * W7[m][t] for t in range(nc)]
                               for e, m in zip(ext, new[:len(ext)])]
                for s in (1, -1):
                    if feasible_strict(rows + [[s * W7[k][t] for t in range(nc)]], nc) is not None:
                        nxt.append(ext + [s])
            frontier = nxt
        counts.append(len(frontier))
        print('   chamber %2d/%d -> %d sub-chambers%s  (%.0fs)'
              % (idx + 1, len(sample), len(frontier),
                 '' if len(frontier) == 62 else '   <<< NOT 62',
                 time.time() - t0), flush=True)

    uniform = all(c == 62 for c in counts)
    print('\n%d chambers tested; distinct subdivision counts: %s'
          % (len(counts), sorted(set(counts))))
    print('UNIFORM 62: %s' % ('CONFIRMED' if uniform else 'REFUTED'))
    json.dump({'n_tested': len(counts), 'counts': counts, 'uniform_62': uniform,
               'secs': time.time() - t0},
              open(os.path.join(HERE, 'modular62_report.json'), 'w'), indent=1)
    return 0 if uniform else 1


if __name__ == '__main__':
    sys.exit(main())
