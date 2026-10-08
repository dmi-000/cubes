#!/usr/bin/env python3
"""Can a depth-2 band coexist with full triple budgets?  [P409]

[P408]: max(4) <= 195 follows from  margin = 64 - sum_S budget_S - (c2 - 1) >= 0,  with
budget_S = E_S - V_S of the triple's bottom diagram (= d2(S) - 1 - c_S).  The two known bands have
margins 13 and 23.  This climbs to MINIMISE the margin while keeping c2 >= 2: a step perturbs one
cube's integer quaternion, and is accepted if the band survives (c2 >= 2, no shared face plane)
and the margin does not grow.  A margin < 0 would put 195 in doubt (then checked with the engine).
Every evaluation is exact (level graphs, Fractions).  Rejected steps are counted, never scored.
"""
import os, sys, itertools, random, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from depth2_charging import level_s1
from euler3 import rowsT, frames

ROOT = os.path.dirname(os.path.dirname(HERE))


def measure(qs):
    if any(not any(q) for q in qs) or CL.shares_plane(qs):
        return None
    Ms = [rowsT(R) for R in frames(qs)]
    G, EG, c2 = level_s1(Ms, [0, 1, 2, 3])
    budget = 0
    for S in itertools.combinations(range(4), 3):
        dS, ES, _ = level_s1(Ms, list(S))
        budget += ES - len(dS)
    return {'c2': c2, 'budget': budget, 'margin': 64 - budget - (c2 - 1), 'd2': EG - len(G) + c2 + 1}


def climb(start, steps, rnd, log):
    cur = [tuple(q) for q in start]
    m = measure(cur)
    best = (m['margin'], cur, m)
    rej = 0
    for t in range(steps):
        k = rnd.randrange(1, 4)
        q = list(cur[k])
        for z in range(4):
            q[z] += rnd.choice([-2, -1, 0, 0, 1, 2])
        cand = cur[:k] + [tuple(q)] + cur[k + 1:]
        try:
            mc = measure(cand)
        except Exception:
            rej += 1
            continue
        if mc is None or mc['c2'] < 2 or mc['margin'] > m['margin']:
            rej += 1
            continue
        cur, m = cand, mc
        if m['margin'] < best[0]:
            best = (m['margin'], cur, m)
            print('   step %4d  margin %3d  budget %3d  c2 %d  d2 %d  %s' % (t, m['margin'], m['budget'], m['c2'], m['d2'], cur), flush=True)
    log.append({'start': start, 'best_margin': best[0], 'best': best[1], 'measure': best[2], 'rejected': rej})
    return best


def main():
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    starts = [[(1, 0, 0, 0), (10, 1, 2, 0), (112, 42, -40, -2), (110, 42, -39, -1)],
              [(1, 0, 0, 0), (18, 2, -2, 0), (45, 34, 6, 54), (78, 23, -32, -9)]]
    log, overall = [], []
    for s, start in enumerate(starts):
        for rep in range(2):
            rnd = random.Random(100 * s + rep)
            print('start %d, run %d: initial %s' % (s, rep, measure(start)), flush=True)
            overall.append(climb(start, steps, rnd, log))
    best = min(overall, key=lambda b: b[0])
    print('\nLOWEST MARGIN %d at %s (%s)' % (best[0], best[1], best[2]))
    if best[0] < 0:
        e = CL.engine(best[1])
        print('engine total %s, by_depth %s' % (e.get('bounded'), e.get('by_depth')))
    json.dump(log, open(os.path.join(ROOT, 'data', 'band_climb.json'), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
