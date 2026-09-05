#!/usr/bin/env python3
"""Climb by whole LINES, not by adjacent chambers.

Attempt 2 in EXPLORATION_141.md. Every climber in this repo moves to a first crossing --
one wall, one chamber. Local maxima at n=4 sit ~3900 walls apart, so a search whose step
is one chamber is exploring a neighbourhood it cannot leave.

`solved_scan.scan_line` already computes EVERY chamber along a single-cube line exactly
(W4 quadratics and W3 quartics, one simplest rational strictly inside each cell). Using
it as the move generator makes the step size a whole line rather than one wall, for about
the cost of a single bisected ray. Nothing new is built here; the existing exact machinery
is pointed at a different question.

Reported per iteration: the best count found anywhere on the scanned lines, and how far
along the line it sat, because if the wins are always in the first cell then this buys
nothing over the old move and should be abandoned.
"""
import random, sys, time
from fractions import Fraction as F
sys.path.insert(0, '.')
import dimension as D
from solved_scan import scan_line, count
from haarsample import haar_config

def linehop(cfg, iters=20, ndir=4, reach=10, seed=0, verbose=True):
    rng = random.Random(seed)
    cur = count(cfg)
    best = (cur, list(cfg))
    seen = set()
    for it in range(1, iters + 1):
        cands = []
        for j in range(1, len(cfg)):
            for _ in range(ndir):
                dv = [F(rng.randint(-9, 9)) for _ in range(3)]
                if not any(dv):
                    continue
                for k, (s, c, q) in enumerate(scan_line(cfg, j, dv, reach)):
                    if c is None or c <= cur:
                        continue
                    c2 = list(cfg); c2[j] = q
                    if tuple(map(tuple, c2)) in seen:
                        continue
                    cands.append((c, k, j, c2))
        if not cands:
            if verbose:
                print('   iter %2d: no cell on any scanned line beats %d; stop' % (it, cur), flush=True)
            break
        cands.sort(key=lambda t: -t[0])
        c, k, j, cfg = cands[0][0], cands[0][1], cands[0][2], list(cands[0][3])
        seen.add(tuple(map(tuple, cfg)))
        cur = c
        if c > best[0]:
            best = (c, list(cfg))
        if verbose:
            print('   iter %2d: -> %d  (cube %d, cell %d along the line, %d candidates above)'
                  % (it, c, j, k, len(cands)), flush=True)
    return best

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 900)
    print('linehop n=%d, %d Haar starts   (climbing plateaus at 141; record 183)' % (n, K), flush=True)
    top = (0, None)
    for i in range(K):
        cfg = haar_config(rng, n, 128, chart=True)
        t0 = time.time()
        print('\nstart %d: total %d' % (i, count(cfg)), flush=True)
        b = linehop(cfg, seed=i)
        print('   best %d  (%.0fs)' % (b[0], time.time() - t0), flush=True)
        if b[0] > top[0]:
            top = b
    print('\nBEST OVER ALL STARTS: %d' % top[0], flush=True)
    if top[1]:
        print(';'.join(','.join(map(str, q)) for q in top[1]), flush=True)
