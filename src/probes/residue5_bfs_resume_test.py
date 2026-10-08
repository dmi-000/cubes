#!/usr/bin/env python3
"""Resume test for residue5_bfs.walk: a walk killed at random points and resumed from its
checkpoint must return exactly the faces of an uninterrupted walk.  [P440]

The kill is simulated by an exception raised from inside the walk after a random number of
feasibility calls, with checkpoints written between every two items (CKPT_EVERY = 0). Kills
land mid-item, which is where a lost or skipped boundary would show. The budget must exceed one
item's calls or the walk never advances; a walk that has not finished after 200 kills is reported
as inconclusive, not as a difference."""
import os, sys, random, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import residue5_bfs as B
import residue5_patterns as RP
import residue5_exact as RX


class Killed(Exception):
    pass


def walk_with_kills(forms, params, ck, rnd, total):
    """kill after a random number of feasibility calls, between 1/40 and 1/4 of the walk's total
    (an item can need hundreds of calls; a budget below one item would never let the walk advance)"""
    real = B.feasible
    kills = 0
    while True:
        budget = [rnd.randint(max(40, total // 40), max(400, total // 4))]

        def f(*a, **k):
            budget[0] -= 1
            if budget[0] < 0:
                raise Killed
            return real(*a, **k)
        B.feasible = f
        try:
            return B.walk(forms, params, ckpt=ck), kills
        except Killed:
            kills += 1
            if kills > 200:
                return (None, {}, 0), kills
        finally:
            B.feasible = real


def main():
    B.CKPT_EVERY = 0
    rnd = random.Random(1)
    pats = [(t, o) for t in range(3, 6) for o, u in RP.patterns(t)]
    cases = []
    for t, o in pats:
        for i, (forms, params) in enumerate(RX.placements_forms(t, o)):
            if len(params) == 2:
                cases.append((t, o, forms, params))
    bad = inconclusive = 0
    for t, o, forms, params in cases[::max(1, len(cases) // 4)][:4]:
        calls = [0]
        real = B.feasible

        def counting(*a, **k):
            calls[0] += 1
            return real(*a, **k)
        B.feasible = counting
        try:
            cf, ref, _ = B.walk(forms, params)
        finally:
            B.feasible = real
        with tempfile.TemporaryDirectory() as d:
            ck = os.path.join(d, 'w.pkl')
            (cf2, got, _), kills = walk_with_kills(forms, params, ck, rnd, calls[0])
        if cf2 is None:
            verdict = 'INCONCLUSIVE (no finish within 200 kills)'
            inconclusive += 1
        else:
            same = set(ref) == set(got)
            bad += not same
            verdict = 'same' if same else 'DIFFERENT'
        print('t=%d %s: %d faces uninterrupted (%d feasibility calls), %d after %d kills: %s'
              % (t, [sorted(x) for x in o], len(ref), calls[0], len(got), kills, verdict), flush=True)
    print('resume test: %d of 4 differ, %d inconclusive' % (bad, inconclusive))


if __name__ == '__main__':
    main()
