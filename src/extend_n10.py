#!/usr/bin/env python3
"""n = 10: extend the tower — across the 2785 continuum, not from one member.

WHY NOT ONE BASE. [P176] The n=9 record is a CONTINUUM, and [member723.log] showed
plateau members extend differently: eight members of the 723 continuum reached four
distinct n=7 maxima, spread 8, not monotone in the parameter. So "extend n=9" is a
family of operations. [P178] gives the family: the ninth cube runs along
(k,k,k-1,k), with 2785 on TWO rays, k >= 56 and k <= -69.

REFUSALS ARE HANDLED, NOT SKIPPED. [P180 Addendum 5] The counter can refuse a
configuration whose clipper emitted zero-volume cells at the box boundary. The
count cannot depend on orientation relative to that box, so a refused configuration
is re-evaluated under a global rotation — verified invariant on 393/727/1217, and
verified against the engine on 11 degenerate cases. Nothing is scored as "no
result" that a rotation can answer.

Search shape follows P101/P179: exhaustive small tenth cubes plus log-uniform
samples to 512, per base.
"""
import json, os, subprocess, sys, itertools, random, time
from math import gcd
sys.path.insert(0, '.')
from growth727 import BASE

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'cube_regions_n')
C8 = BASE + [(7, 14, 1, -5), (4, -3, -4, -4), (24, -24, 24, -61)]
ROTS = [(2, 1, 0, 0), (1, 1, 1, 0), (3, 0, 1, 2), (5, 1, 2, 1), (1, 2, 0, 1)]
KS = [56, 57, 60, 100, 1000, -69, -70, -100, -1000]      # members of both rays (P178)


def qmul(p, q):
    w, x, y, z = p; e, f, g, h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)


def canon(q):
    g = 0
    for v in q: g = gcd(g, abs(v))
    if g == 0: return None
    q = tuple(v // g for v in q)
    for v in q:
        if v > 0: break
        if v < 0: q = tuple(-x for x in q); break
    return q


def batch(cfgs):
    if not cfgs: return []
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run([ENG, '--quats-stdin'], input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try:
            d = json.loads(l); out.append(d.get('bounded'))
        except Exception:
            out.append(None)
    return out + [None] * (len(cfgs) - len(out))


def rescue(cfg):
    """A refusal is a box artifact; rotate and recount (P180 Addendum 5)."""
    for g in ROTS:
        r = [canon(qmul(g, q)) for q in cfg]
        if any(x is None for x in r): continue
        if max(abs(v) for q in r for v in q) > 512: continue
        v = batch([r])[0]
        if v is not None: return v
    return None


def main():
    rnd = random.Random(20260830)
    t0 = time.time()
    best, bestcfg, tried, rescued, lost = 2785, None, 0, 0, 0
    per_base = {}
    for k in KS:
        base = C8 + [(k, k, k - 1, k)]
        if batch([base])[0] != 2785:
            print('   k=%-6d base is not 2785 — skipped' % k, flush=True); continue
        cand = [canon(q) for q in itertools.product(range(-4, 5), repeat=4)]
        cand = [q for q in cand if q is not None]
        while len(cand) < 6561 + 4000:
            q = canon(tuple(rnd.choice([1, -1]) * int(round(2 ** rnd.uniform(0, 9))) for _ in range(4)))
            if q and max(map(abs, q)) <= 512: cand.append(q)
        cand = list(dict.fromkeys(cand))
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
        per_base[k] = bb
        print('   k=%-6d best n=10 = %-6d with tenth cube %-18s (%d evals, %.0fs)'
              % (k, bb, bq, tried, time.time() - t0), flush=True)
    print('\nBEST n=10 FOUND: %d' % best, flush=True)
    if bestcfg: print('   configuration: %s' % (bestcfg,), flush=True)
    print('   %d evaluations, %d rescued by rotation, %d unevaluable' % (tried, rescued, lost), flush=True)
    print('   spread across continuum members: %s' % sorted(per_base.items()), flush=True)
    json.dump({'best': best, 'config': bestcfg, 'per_base': per_base,
               'evaluations': tried, 'rescued': rescued, 'lost': lost,
               'secs': time.time() - t0},
              open(os.path.join(HERE, 'extend_n10.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
