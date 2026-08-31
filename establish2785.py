#!/usr/bin/env python3
"""Establish n = 9 = 2785 to the standard of Postscript 101 (n = 8).

WHY. `RESULTS.md` flags that 2785 has **no establishing entry in LEDGER.md** —
documented only in MAXIMISER_TAXONOMY.md and METHODS 9, outside the append-only
record — and declines to backfill one, because a dated record of what was known
when cannot honestly be reconstructed. This does not reconstruct 2026-08-07. It
does the work AGAIN, today, so the entry can be dated honestly.

THE STANDARD, from P101, which established n = 8:
  1. the record: exact command line and count
  2. by_depth profile
  3. both engines agree
  4. symmetry order by stabiliser computation
  5. subset check: the k-cube subsets give exactly the lower records
  6. search evidence: "beaten by nothing in N further exact evaluations"
  7. the plateau, solved

Items 5 and 7 are already done (subset scan; P178's two rays k >= 56 and k <= -69
with the puncture at the duplicate). This supplies 1-4 and 6.

GATE. The stabiliser computation must reproduce P101's stated 3/3/1/1/1 for
393/723/727/1217/1891 before any symmetry order for 2785 is believed.

WHAT THIS DOES AND DOES NOT CLAIM. Like P101, "beaten by nothing we tried" —
verified, not proved.
"""
import json, os, subprocess, sys, itertools, random, time
sys.path.insert(0, '.')
from growth727 import BASE

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'cube_regions_n')
ENGW = os.path.join(HERE, 'cube_regions_q2w')

C6 = BASE + [(7, 14, 1, -5)]
C7 = C6 + [(4, -3, -4, -4)]
C8 = C7 + [(24, -24, 24, -61)]
C9 = C8 + [(56, 56, 55, 56)]
RECORDS = {'393': BASE, '723': BASE + [(5, 2, 2, 2)], '727': C6,
           '1217': C7, '1891': C8}


def qmul(p, q):
    w, x, y, z = p; e, f, g, h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g,
            w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)


def canon(q):
    from math import gcd
    g = 0
    for v in q: g = gcd(g, abs(v))
    if g == 0: return None
    q = tuple(v // g for v in q)
    for v in q:
        if v > 0: break
        if v < 0: q = tuple(-x for x in q); break
    return q


SYMS = list(dict.fromkeys(
    canon(t) for t in
    [(w, x, y, z) for w in (-1, 0, 1) for x in (-1, 0, 1)
     for y in (-1, 0, 1) for z in (-1, 0, 1)
     if (w, x, y, z) != (0, 0, 0, 0) and w*w+x*x+y*y+z*z in (1, 2, 4)]))


def symkey(q):
    """A cube's orientation modulo its OWN 24 rotational self-symmetries."""
    return min(canon(qmul(tuple(q), h)) for h in SYMS)


def stabiliser(cfg):
    """|{g : the global rotation g maps the compound to itself}|

    A compound symmetry is a GLOBAL rotation applied on the left, which may
    permute the cubes; each cube is identified only up to its own 24 self-
    symmetries, so cubes are compared by symkey. My first version right-multiplied
    a single g into every cube and compared raw quaternions -- a different group
    action entirely. It returned 1/1/1/1/1 where P101 states 3/3/1/1/1, and the
    gate refused to proceed. That is the gate earning its place: a wrong symmetry
    order would have gone into the record as a fact.
    """
    base = sorted(symkey(q) for q in cfg)
    n = 0
    for g in SYMS:
        if sorted(symkey(qmul(g, tuple(q))) for q in cfg) == base:
            n += 1
    return n


def batch(cfgs, eng=ENG):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run([eng] + (['--d', '0'] if eng == ENGW else []) + ['--quats-stdin'],
                       input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l)['bounded'])
        except Exception: out.append(None)
    return out + [None] * (len(cfgs) - len(out))


def main():
    print('GATE: stabiliser orders (P101 states 3/3/1/1/1)', flush=True)
    got = {k: stabiliser(v) for k, v in RECORDS.items()}
    want = {'393': 3, '723': 3, '727': 1, '1217': 1, '1891': 1}
    print('   %s' % got, flush=True)
    if got != want:
        raise SystemExit('stabiliser gate FAILED: got %s want %s' % (got, want))
    print('   PASS\n', flush=True)

    print('THE RECORD', flush=True)
    a = batch([C9])[0]
    b = batch([C9], eng=ENGW)[0]
    print('   cube_regions_n  -> %s' % a, flush=True)
    print('   cube_regions_q2w-> %s' % b, flush=True)
    print('   both engines agree: %s' % (a == b == 2785), flush=True)
    print('   symmetry order of 2785: %d' % stabiliser(C9), flush=True)

    rnd = random.Random(20260830)
    tried, best, bestcfg = 0, 2785, None
    t0 = time.time()

    def run(cfgs, label):
        nonlocal tried, best, bestcfg
        for i in range(0, len(cfgs), 400):
            chunk = cfgs[i:i+400]
            for c, v in zip(chunk, batch(chunk)):
                tried += 1
                if v is not None and v > best:
                    best, bestcfg = v, c
        print('   %-34s cumulative %6d evaluations, best %d (%.0fs)'
              % (label, tried, best, time.time()-t0), flush=True)

    # 1. one- and two-component lattice perturbations of every cube
    pert = []
    for i in range(len(C9)):
        for j in range(4):
            for d in (-2, -1, 1, 2):
                c = [list(q) for q in C9]; c[i][j] += d
                pert.append([tuple(x) for x in c])
    for i in range(len(C9)):
        for j, k in itertools.combinations(range(4), 2):
            for dj in (-1, 1):
                for dk in (-1, 1):
                    c = [list(q) for q in C9]; c[i][j] += dj; c[i][k] += dk
                    pert.append([tuple(x) for x in c])
    run(pert, 'lattice perturbations')

    # 2. replacement ninth cube: exhaustive small, then log-uniform samples
    rep = [C8 + [q] for q in itertools.product(range(-4, 5), repeat=4)
           if canon(q) is not None]
    run(rep, 'replacement 9th, |component| <= 4')
    samp = []
    while len(samp) < 8000:
        q = tuple(rnd.choice([1, -1]) * int(round(2 ** rnd.uniform(0, 9))) for _ in range(4))
        if canon(q) is not None and max(map(abs, q)) <= 512:
            samp.append(C8 + [q])
    run(samp, 'replacement 9th, log-uniform')

    # 3. replacement eighth and seventh
    for idx, lbl in ((7, 'replacement 8th'), (6, 'replacement 7th')):
        s = []
        while len(s) < 3000:
            q = tuple(rnd.choice([1, -1]) * int(round(2 ** rnd.uniform(0, 9))) for _ in range(4))
            if canon(q) is None or max(map(abs, q)) > 512: continue
            c = list(C9); c[idx] = q
            s.append(c)
        run(s, lbl)

    print('\nRESULT: %d exact evaluations, best found %d' % (tried, best), flush=True)
    if bestcfg: print('   BEATEN BY: %s' % (bestcfg,), flush=True)
    json.dump({'evaluations': tried, 'best': best, 'beaten_by': bestcfg,
               'symmetry_order': stabiliser(C9), 'secs': time.time()-t0},
              open(os.path.join(HERE, 'establish2785.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
