#!/usr/bin/env python3
"""Task 3: radius-3/4 single-component + two-component hill-climb from the
699 plateau states. gcd-reduce (q1,p1),(q2,p2),R; cap 512."""
import sys, math, itertools
sys.path.insert(0, '/Users/dmi/carroll')
sys.path.insert(0, '/tmp')
from slide3_search import gcd_reduce
from sweep import run

MAXC = 512


def gcd2(q, p):
    g = math.gcd(abs(q), abs(p))
    if g > 1:
        q, p = q // g, p // g
    if q == 0 and p == 0:
        q = 1
    return q, p


def norm(state):
    s = list(state)
    s[0], s[1] = gcd2(s[0], s[1])
    s[2], s[3] = gcd2(s[2], s[3])
    s[4], s[5], s[6], s[7] = gcd_reduce(s[4:8])
    return tuple(s)


def state_params(s):
    return (s[0], s[1], s[2], s[3], (s[4], s[5], s[6], s[7]))


def neighbors(state, single_deltas=(-4, -3, -2, -1, 1, 2, 3, 4),
              pair_deltas=(-2, -1, 1, 2)):
    out = set()
    # single component, radius up to 4
    for idx in range(8):
        for d in single_deltas:
            s = list(state); s[idx] += d
            s = norm(s)
            if s != state and all(abs(c) <= MAXC for c in s):
                out.add(s)
    # two components at once
    for i, j in itertools.combinations(range(8), 2):
        for di in pair_deltas:
            for dj in pair_deltas:
                s = list(state); s[i] += di; s[j] += dj
                s = norm(s)
                if s != state and all(abs(c) <= MAXC for c in s):
                    out.add(s)
    return sorted(out)


def climb(start, phase, max_steps=15):
    cur = norm(start)
    best_total = None
    # eval start
    recs, over = run([(dict(state=list(cur)), state_params(cur))], phase, chunk_mult=1)
    cur_total = recs[0]['total'] if recs else None
    print(f'  start {cur} total={cur_total}')
    if cur_total is None:
        return cur, None
    for step in range(max_steps):
        nbrs = neighbors(cur)
        jobs = [(dict(state=list(s)), state_params(s)) for s in nbrs]
        recs, over = run(jobs, phase, chunk_mult=8)
        if over:
            print('  FOUND >699 during climb, stopping to verify')
            return cur, over
        # pick best strictly greater
        bstate = None; btotal = cur_total; bbd = None
        for r in recs:
            if r['total'] > btotal:
                btotal = r['total']; bstate = tuple(r['state']); bbd = r['by_depth']
        if bstate is None:
            print(f'  step {step}: LOCAL MAX at {cur} total={cur_total}')
            break
        cur = bstate; cur_total = btotal
        print(f'  step {step}: -> {cur} total={cur_total} bd={bbd}')
    return cur, None


if __name__ == '__main__':
    starts = [
        (3, 1, 9, 2, 5, 2, 2, 2),
        (9, 5, 12, 7, 3, 1, 1, 1),
        (11, 7, 2, 1, 5, 2, 2, 2),
    ]
    all_over = []
    for st in starts:
        print(f'=== climb from {st} ===')
        end, over = climb(st, 'climb_v2')
        if over:
            all_over.extend(over)
    print('DONE. >699 finds:', len(all_over))
    for o in all_over:
        print(o)
