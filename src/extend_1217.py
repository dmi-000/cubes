#!/usr/bin/env python3
"""Does an INTERIOR member of the 1217 continuum extend better than the recorded one?

[P182] found the n=7 rung 1217 to be a continuum along a solved 13-pair curve
q(t) = cube2 * (1, t*(1,1,-1)), holding on t in [-59/315, -11/63], and found the
RECORDED member to sit at an endpoint of that interval — as it does on both of
2785's curves.  [OQ 9] measured, at n=9 -> n=10, that the recorded (endpoint)
member was the WORST of nine tested, 8 below the best.

If endpoint members systematically extend worst, then extending an interior member
of the 1217 plateau should beat 1895, and n=7 is cheap enough to just ask.

VOID AS RUN — see [P186]. The search returned 1891 from the recorded base, which
provably reaches 1895, so its negatives do not count. The gate below now checks menu
membership of the known eighth cube before any comparison is read. A second defect
remains unfixed: base heights along this curve run 4 to 379 while the menu is
exhaustive only to 4, so one fixed menu is not equally dense around all bases.

Search shape copied from extend_n10.py so the comparison is like-for-like:
exhaustive cubes in [-4,4]^4 plus log-uniform samples to 512, per base.  Refusals
are rescued by rotation (P180 Addendum 5), never scored as "no result".

Interior members are chosen as the SIMPLEST rationals in the interval, not its
midpoints (METHODS 15 / FAILURE_MODES 16): -2/11 is interior and cheap, whereas a
midpoint of the endpoints has denominator 630 and drives the eighth cube's height
past the narrow engine's cap.
"""
import itertools, json, os, random, subprocess, sys, time
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, '.')
from growth727 import BASE

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'cube_regions_n')
C6 = BASE + [(7, 14, 1, -5)]                 # the n=6 rung, 727
CUBE2 = BASE[2]                              # base of the solved curve (P182)
AXIS = (1, 1, -1)
RECORDED = F(-11, 63)
# endpoints of the measured plateau, then the simplest interior rationals
TS = [F(-59, 315), F(-9, 50), F(-7, 39), F(-5, 28), F(-2, 11), F(-3, 17), RECORDED]
ROTS = [(2, 1, 0, 0), (1, 1, 1, 0), (3, 0, 1, 2), (5, 1, 2, 1), (1, 2, 0, 1)]


def qmul(p, q):
    w, x, y, z = p; e, f, g, h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)


def canon(q):
    den = 1
    for x in q:
        den = den * F(x).denominator // gcd(den, F(x).denominator)
    w = [int(F(x) * den) for x in q]
    g = 0
    for v in w:
        g = gcd(g, abs(v))
    if g == 0:
        return None
    w = [v // g for v in w]
    for v in w:
        if v > 0: break
        if v < 0: w = [-x for x in w]; break
    return tuple(w)


def batch(cfgs):
    if not cfgs: return []
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run([ENG, '--quats-stdin'], input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l).get('bounded'))
        except Exception: out.append(None)
    return out + [None] * (len(cfgs) - len(out))


def rescue(cfg):
    for g in ROTS:
        r = [canon(qmul(g, q)) for q in cfg]
        if any(x is None for x in r): continue
        if max(abs(v) for q in r for v in q) > 512: continue
        v = batch([r])[0]
        if v is not None: return v
    return None


KNOWN_EIGHTH = (24, -24, 24, -61)      # recorded base + this = 1895


def gate_search_can_find_1895(cand):
    """The oldest gate in the project: machinery must reproduce the known answer.

    Without this the campaign ran 8 046 s and returned 1891 from the base that
    provably reaches 1895, making every negative void ([P186]).  The menu is
    exhaustive on [-4,4]^4 plus ~4 000 log-uniform samples to height 512; the
    target has height 61, so it sits in the sampled part, and 4 000 samples in
    ~512^4 is not a search.  Checking MEMBERSHIP is instant and decisive.
    """
    if canon(KNOWN_EIGHTH) not in set(cand):
        raise SystemExit(
            'GATE FAILED: the candidate menu does not contain %s, the eighth cube '
            'that takes the recorded base to 1895. The search cannot reproduce the '
            'known answer, so its negatives would be void (P186). Widen the menu or '
            'add the known cube as a control before reading any comparison.'
            % (KNOWN_EIGHTH,))


def main():
    rnd = random.Random(20260831)
    t0 = time.time()
    best, bestcfg, tried, rescued, lost = 1895, None, 0, 0, 0
    per_base, skipped = {}, []
    for t in TS:
        seventh = canon(qmul(CUBE2, (1, t * AXIS[0], t * AXIS[1], t * AXIS[2])))
        base = C6 + [seventh]
        if max(map(abs, seventh)) > 512:
            skipped.append((str(t), 'height %d over cap' % max(map(abs, seventh))))
            print('   t=%-9s seventh cube %s exceeds cap — SKIPPED'
                  % (t, seventh), flush=True); continue
        if batch([base])[0] != 1217:
            skipped.append((str(t), 'base is not 1217'))
            print('   t=%-9s base is not 1217 — SKIPPED' % t, flush=True); continue
        cand = [canon(q) for q in itertools.product(range(-4, 5), repeat=4)]
        cand = [q for q in cand if q is not None]
        while len(cand) < 6561 + 4000:
            q = canon(tuple(rnd.choice([1, -1]) * int(round(2 ** rnd.uniform(0, 9)))
                            for _ in range(4)))
            if q and max(map(abs, q)) <= 512: cand.append(q)
        cand = list(dict.fromkeys(cand))
        if t == RECORDED:
            gate_search_can_find_1895(cand)
        bb, bq = 0, None
        for i in range(0, len(cand), 400):
            chunk = [base + [q] for q in cand[i:i+400]]
            for c, v in zip(chunk, batch(chunk)):
                tried += 1
                if v is None:
                    v = rescue(c)
                    if v is None: lost += 1; continue
                    rescued += 1
                if v > bb: bb, bq = v, c[-1]
                if v > best: best, bestcfg = v, c
        per_base[str(t)] = bb
        print('   t=%-9s %s seventh %-16s best n=8 = %-6d eighth %-16s (%d evals, %.0fs)'
              % (t, 'RECORDED' if t == RECORDED else 'interior',
                 str(seventh), bb, str(bq), tried, time.time() - t0), flush=True)
    print('\nBEST n=8 FOUND: %d   (recorded rung is 1895)' % best, flush=True)
    if bestcfg: print('   configuration: %s' % (bestcfg,), flush=True)
    print('   %d evaluations, %d rescued by rotation, %d unevaluable, %d bases skipped'
          % (tried, rescued, lost, len(skipped)), flush=True)
    print('   spread across continuum members: %s' % sorted(per_base.items()), flush=True)
    json.dump({'best': best, 'config': bestcfg, 'per_base': per_base,
               'skipped': skipped, 'evaluations': tried, 'rescued': rescued,
               'lost': lost, 'secs': time.time() - t0},
              open(os.path.join(HERE, 'extend_1217.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
