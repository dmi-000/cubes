#!/usr/bin/env python3
"""[P400] the general-n bound's per-set caps, anchored at n = 5 with sphere_count's exact counter.

Every set D(A, B) = {max_A M < min_B M} has at most  f(a, k) = 4k + 2 + 3 a k (k - 1)  components
(a = |A|, k = |B|), by Mayer-Vietoris splitting off one cube of B at a time ([P399]'s argument,
generalised).  Summed: max(n) <= 1 + sum_l C(n,l) f(l, n-l).  Here every D(A, B) of each
configuration is counted exactly and checked against f, and the total against the engine.
"""
import os, sys, itertools, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sphere_count as S

f = lambda a, k: 4 * k + 2 + 6 * a * (k - 1)      # [P401]; [P400]'s was 4k + 2 + 3ak(k-1)


def main():
    rnd = random.Random(20260930)
    cases = [('n=5 RECORD 393', [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]),
             ('n=5 with a shared face plane', [(1, 0, 0, 0), (3, 0, 0, 1), (4, 1, 1, -1), (5, -1, -5, -5), (2, 1, 1, 1)])]
    for r in range(2):
        cases.append(('n=5 random #%d' % r, [tuple(rnd.randint(-6, 6) for _ in range(4)) for _ in range(5)]))
    out, bad = [], 0
    for name, qs in cases:
        C = S.Compound(qs)
        idx = list(range(5))
        tot, worst = 0, {}
        for k in range(1, 6):
            for A in itertools.combinations(idx, k):
                B = [b for b in idx if b not in A]
                c = 1 if not B else C.components(C.beat_pieces(list(A), B))
                tot += c
                if B:
                    key = (len(A), len(B))
                    worst[key] = max(worst.get(key, 0), c)
                    if c > f(*key):
                        print('   CAP VIOLATED', A, B, c, f(*key)); bad += 1
        eng = S.engine(qs)
        ok = tot == eng
        bad += not ok
        print('%-32s sphere %4d engine %-5s %s | worst per (|A|,|B|) vs cap: %s' % (
            name, tot, eng, 'AGREE' if ok else 'DISAGREE',
            ', '.join('%s:%d/%d' % (k, v, f(*k)) for k, v in sorted(worst.items()))), flush=True)
        out.append({'case': name, 'sphere': tot, 'engine': eng, 'worst': {str(k): v for k, v in worst.items()}})
    json.dump(out, open(os.path.join(S.ROOT, 'data', 'sphere_count_n5.json'), 'w'), indent=1)
    print('\n%s' % ('ALL AGREE, no cap violated' if not bad else '%d PROBLEMS' % bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
