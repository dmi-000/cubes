#!/usr/bin/env python3
"""The n=5 record family: hub + ONE cube per body diagonal. Four angles, not five.

[P225]: 393 is a hub cube plus four cubes, one on each of the four body diagonals, every
remaining pair axis-in-plane. That is a FOUR-parameter family, and a cube has only four
diagonals, so it saturates at n=5.

A first attempt swept five angles for n=6 directly: 181 million configurations, ~100 days.
The right shape is to enumerate the n=5 family here and extend each good base by ONE cube
using the incremental engine (405-cube menu, ~20 s per base) -- which is exactly the
one-base-many-candidates workload `cube_regions_inc` was built for.

Angles stay at small denominators because every optimum found so far is a coincidence
point at a simple rational: the n=4 record is exactly +-1/4, and 1/48 off it costs 12
regions.
"""
import itertools, json, subprocess, sys, time
from fractions import Fraction as F
from math import gcd

DIAG = [(1,1,1), (1,1,-1), (1,-1,1), (1,-1,-1)]

def q_axis(ax, t):
    p, d = t.numerator, t.denominator
    q = (d, p*ax[0], p*ax[1], p*ax[2]); g = 0
    for v in q: g = gcd(g, abs(v))
    return tuple(v // (g or 1) for v in q)

def batch(cfgs):
    inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run(['./cube_regions_n', '--quats-stdin'], input=inp,
                       capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l).get('bounded'))
        except Exception: out.append(None)
    return out + [None] * (len(cfgs) - len(out))

if __name__ == '__main__':
    # QUOTIENT BY THE DIAGONAL'S OWN C3. The octahedral stabiliser of a body diagonal is
    # the 120-degree rotation about it, which acts on the Cayley parameter as
    # t -> (t+1)/(1-3t)  (|axis|^2 = 3). So t, that image, and its image again all denote
    # the SAME cube -- which is why the 393 shows t = 5 for what is t = 1/4:
    # (1/4+1)/(1-3/4) = 5. Keeping one representative per orbit cuts the sweep ~3x, the
    # same unlabelled-object reduction that cut the arc menu 7.2x in [P219].
    raw = sorted({F(p,q) for q in (1,2,3,4,5,6) for p in range(-6,7) if p and gcd(abs(p),q)==1})
    def orbit(t):
        o = {t}
        for _ in range(2):
            t = (t + 1) / (1 - 3*t) if (1 - 3*t) != 0 else F(10**9)
            o.add(t)
        return o
    seen, VALS = set(), []
    for t in raw:
        if t in seen: continue
        ob = orbit(t); seen |= ob
        VALS.append(min(ob, key=lambda x: (abs(x.denominator), abs(x.numerator))))
    # SMALL CANONICAL ANGLES ONLY. Without the (incorrect) S4 reduction the full product is
    # 18.6 h, so the set is trimmed rather than the symmetry over-claimed. Both known
    # records live here: the 393 needs {5,5,-5,-3}, and the n=4 record's t = 1/4
    # canonicalises to 5. The gate below fails loudly if the trim ever excludes the target.
    VALS = sorted(t for t in VALS if abs(t) <= 6 and t.denominator <= 2)
    # GATE FIRST: the sweep must be able to express the known 393.
    TRUE = {(1,-1,1): F(5), (1,1,-1): F(5), (1,-1,-1): F(-5), (1,1,1): F(-3)}
    if not all(t in VALS for t in TRUE.values()):
        sys.exit('GATE FAILED: the angle set cannot express the 393; negatives would be void')
    gcfg = [(1,0,0,0)] + [q_axis(a, TRUE[a]) for a in DIAG]
    if batch([gcfg])[0] != 393:
        sys.exit('GATE FAILED: the reconstruction does not count 393')
    print('gate: the family reproduces the 393 exactly', flush=True)
    print('n=5 family: hub + one cube per diagonal, %d angles -> %d configurations'
          % (len(VALS), len(VALS)**4), flush=True)
    keep = []
    best = (0, None); n = 0; t0 = time.time()
    buf, meta = [], []
    def flush():
        global best, n
        for c, cf, m in zip(batch(buf), buf, meta):
            if not c: continue
            n += 1
            if c >= 385: keep.append((c, cf, m))
            if c > best[0]:
                best = (c, cf)
                print('   %4d  t %s  (%d evaluated, %.0fs)'
                      % (c, [str(x) for x in m], n, time.time()-t0), flush=True)
    # THE S4 REDUCTION WAS WRONG AND IS REMOVED. The cube's rotation group does act as S4
    # on the four body diagonals, and conjugation does preserve the angle -- but the action
    # is not free on the SIGNED structure: a rotation permuting diagonals can reverse
    # orientations, sending t to -t on some of them. Permuting angles alone is therefore
    # not the group action. Measured: the 24 assignments of (-5,-3,5,5) give TWO counts,
    # 341 and 393, and the sorted tuple gives 341 -- so sorted-only dropped the 393 and
    # voided an hour-long sweep. The gate that would have caught it before the run was
    # missing; it is now first.
    for ts in itertools.product(VALS, repeat=4):
        buf.append([(1,0,0,0)] + [q_axis(a,t) for a,t in zip(DIAG,ts)])
        meta.append(ts)
        if len(buf) >= 4000:
            flush(); buf, meta = [], []
    flush()
    print('\nevaluated %d ; best %d ; %d bases at >=385' % (n, best[0], len(keep)), flush=True)
    with open('n5family_keep.json','w') as f:
        json.dump([[c,[list(q) for q in cf]] for c,cf,_ in keep], f)
    print('kept bases written to n5family_keep.json', flush=True)
