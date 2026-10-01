#!/usr/bin/env python3
"""Hunt for X > 0, W4u > 0, c2 >= 2 at n = 4 among coincidence-rich configurations.  [P405]

[P404]'s route to max(4) <= 195 needs c2 = 1, X = 0 and W4u = 0.  In [P403]'s 210 generic-ish
configurations all three held.  Small-height rotations are dense in exactly the degeneracies that
could break them (multi-edge triple points, four-fold points), so this runs depth2_charging.check
on random 4-compounds of height <= H, shared face planes excluded and counted, and reports every
configuration where a hypothesis fails, with d2 and the gates.  Unevaluated rows are counted.
"""
import os, sys, random, json, itertools, collections, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import c_level as CL
import depth2_charging as DC

ROOT = os.path.dirname(os.path.dirname(HERE))


def main():
    H = int(sys.argv[1]); N = int(sys.argv[2])
    rnd = random.Random(1000 + H)
    pool = [q for q in itertools.product(range(-H, H + 1), repeat=4) if any(q) and q[0] >= 0]
    stats, hits, t0 = collections.Counter(), [], time.time()
    for _ in range(N):
        qs = [(1, 0, 0, 0)] + rnd.sample(pool, 3)
        if CL.shares_plane(qs):
            stats['excluded'] += 1
            continue
        try:
            c = DC.check(qs)
        except Exception as e:
            stats['unevaluated'] += 1
            print('UNEVALUATED', qs, type(e).__name__, str(e)[:120], flush=True)
            continue
        stats['evaluated'] += 1
        gates = c['g1_all'] and not c['g2_bad'] and c['g3'] and c['mindeg'] >= 2
        stats['gate_fail'] += not gates
        stats['W4>0'] += c['W4'] != 0
        stats['d2>66'] += c['d2'] > 66
        if c['X'] != 0 or c['W4_uncharged'] != 0 or c['c2'] >= 2 or not gates or c['d2'] > 66:
            hits.append({'qs': qs, 'd2': c['d2'], 'c2': c['c2'], 'X': str(c['X']),
                         'W4u': str(c['W4_uncharged']), 'gates': gates})
            print('HIT', hits[-1], flush=True)
    print('H=%d: %s, %.0fs; hypothesis failures: %d' % (H, dict(stats), time.time() - t0, len(hits)))
    json.dump({'H': H, 'N': N, 'stats': dict(stats), 'hits': hits},
              open(os.path.join(ROOT, 'data', 'depth2_hunt_H%d.json' % H), 'w'), indent=1)


if __name__ == '__main__':
    main()
