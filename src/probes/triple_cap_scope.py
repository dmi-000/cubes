#!/usr/bin/env python3
"""The triple cap E_S <= 32 without transversality: the circle-lemma route, measured.  [P406]

E_S = (1/2) sum over the triple's triple points of (deg_top - 2) + (deg_bot - 2), the triple
points' share of the excess in the count identity.  Claim: for any cube triple with no shared
face plane, E_S <= 32, because deg_top <= deg_bot (circle lemma, [P405]) and
sum_{all bottom vertices}(deg_bot - 2) = 2(d2(S) - 1 - c) <= 32 (Euler, ANCHOR).
Checked on coincidence-rich small-height triples, shared face planes excluded and counted; reports
max E_S, and how often the triple points use the whole bottom budget.
"""
import os, sys, itertools, random, collections, json
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
from stepT_cubes import level0
from depth2_charging import level_s1, on_boundary
from euler3 import rowsT, frames

ROOT = os.path.dirname(os.path.dirname(HERE))


def main():
    out, stats = [], collections.Counter()
    for H in (2, 3):
        rnd = random.Random(500 + H)
        pool = [q for q in itertools.product(range(-H, H + 1), repeat=4) if any(q) and q[0] >= 0]
        for _ in range(3000):
            qs = [(1, 0, 0, 0)] + rnd.sample(pool, 2)
            if CL.shares_plane(qs):
                stats['excluded'] += 1
                continue
            Ms = [rowsT(R) for R in frames(qs)]
            top, _, _ = level0(Ms)
            bot, Eb, cb = level_s1(Ms, [0, 1, 2])
            tp = [P for P in set(top) | set(bot) if sum(1 for M in Ms if on_boundary(P, M)) == 3]
            ES = sum(F(top.get(P, 2) - 2 + bot.get(P, 2) - 2, 2) for P in tp)
            budget = Eb - len(bot)                     # = (1/2) sum (deg_bot - 2) over all vertices
            stats['evaluated'] += 1
            stats['ES>32'] += ES > 32
            stats['ES>budget'] += ES > 2 * budget     # E_S <= sum_tp (deg_bot-2) <= 2 * budget
            stats['ES==32'] += ES == 32
            out.append((str(ES), budget, len(tp)))
    mx = max(F(e) for e, _, _ in out)
    print('%s; max E_S = %s' % (dict(stats), mx))
    json.dump({'stats': dict(stats), 'max_ES': str(mx)},
              open(os.path.join(ROOT, 'data', 'triple_cap_scope.json'), 'w'), indent=1)
    sys.exit(1 if stats['ES>32'] or stats['ES>budget'] else 0)


if __name__ == '__main__':
    main()
