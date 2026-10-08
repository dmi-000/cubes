#!/usr/bin/env python3
"""The accounting step sum(E - V) <= T3 + two-body, measured at n = 4.  [P407]

[P326]'s tower bound uses SEV(compound) <= sum_S E_S + sum_P E_P, recorded by [P388] as argued and
not verified.  With E_P = SEV(pair) and E_S = SEV(S) - sum_{P in S} SEV(P) (the identity for a
sub-compound), the right side at n = 4 is  sum_S SEV(S) - sum_P SEV(P).  SEV of any compound is
sum over its levels of (E_l - V_l), from `c_level.level_graph` (gated against [P243]'s values).
Shared face planes excluded and counted; the claim's scope is no shared face plane ([P407]).
"""
import os, sys, itertools, random, collections, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import c_level as CL

ROOT = os.path.dirname(os.path.dirname(HERE))


def sev(qs):
    return sum(g['E'] - g['V'] for g in CL.level_graph(qs).values())


def main():
    if not CL.gate():
        sys.exit('GATE FAILED')
    named = [CL.parse('1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4'), CL.parse('1,0,0,0;0,2,-3,-2;0,2,-3,2;-4,-2,-5,-6')]
    rnd = random.Random(20261004)
    pop = list(named)
    for H in (2, 3, 7):
        pool = [q for q in itertools.product(range(-H, H + 1), repeat=4) if any(q) and q[0] >= 0]
        for _ in range(120):
            pop.append([(1, 0, 0, 0)] + rnd.sample(pool, 3))
    st, slack = collections.Counter(), []
    for qs in pop:
        if CL.shares_plane(qs):
            st['excluded'] += 1
            continue
        try:
            lhs = sev(qs)
            rhs = sum(sev([qs[k] for k in S]) for S in itertools.combinations(range(4), 3)) \
                - sum(sev([qs[k] for k in P]) for P in itertools.combinations(range(4), 2))
        except Exception as e:
            st['unevaluated'] += 1
            continue
        st['evaluated'] += 1
        st['violations'] += lhs > rhs
        slack.append(rhs - lhs)
    print('%s; slack (rhs - lhs): min %d, max %d, zero in %d' % (dict(st), min(slack), max(slack), slack.count(0)))
    json.dump({'stats': dict(st), 'slack': slack}, open(os.path.join(ROOT, 'data', 'accounting_step.json'), 'w'))
    sys.exit(1 if st['violations'] else 0)


if __name__ == '__main__':
    main()
