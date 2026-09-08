#!/usr/bin/env python3
"""Extend every good n=5 base by one cube, with the incremental engine. Target: 727.

`n5family.py` keeps every base reaching >=385 (76 of them, the 393 among them). Those 76 are
only ELEVEN compounds -- see `congruent.py` -- and one representative of each is extended
against the octahedral quotient of [-14,14]^4, 43 707 cubes, using `cube_regions_inc --base`,
which reuses the base arrangement and clips only the six new planes.

THREE THINGS THIS FILE GETS RIGHT THAT EARLIER VERSIONS DID NOT, each one a measured cost:

1. THE GATE IS CHEAP AND RUNS FIRST. It counts ONE candidate, not the whole menu: the 393
   base plus the menu's spelling of (7,14,1,-5) must give 727. The previous version put the
   gate behind a full 43 707-cube pass, so a failure cost two hours to observe. It costs a
   second now.

2. THE GATE GOES THROUGH key(), NOT `in`. The menu is the octahedral QUOTIENT, so each class
   appears under ONE spelling chosen by an arbitrary tie-break among equal-height members.
   (7,14,1,-5) has FOUR members at height 14, so the class is in the menu while that literal
   tuple is not -- which is exactly how the second gate failure read as "CUBE NOT IN MENU"
   when the menu was fine. Never test menu membership with `in`.

3. IT SHARDS AND CHECKPOINTS. Measured: 0.168 s per candidate at n=6, so 6 bases x 43 707
   is ~12 h of CPU. Each (base, shard) writes its own result file and is skipped if present,
   so a kill or a correction costs only what has not been done -- METHODS 2, and the reason
   it is safe to fix the method mid-run.

Usage:  extend_n5.py SHARD NSHARDS      (one process per shard; results merge on read)
        extend_n5.py --report           (merge whatever exists and print the best)
"""
import itertools, json, os, subprocess, sys, time
sys.path.insert(0, '.')
from symmetrize import canon

OUT = 'extend_n5_results'
B393 = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
KNOWN = (7,14,1,-5)          # takes the 393 to 727 -- the anchor outside this sweep


def qmul(p, r):
    w,x,y,z = p; e,f,g,h = r
    return canon((w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e))

OCT = sorted({canon(t) for t in itertools.product((-1,0,1), repeat=4)
              if any(t) and sum(v*v for v in t) in (1,2,4)})

def key(q):
    """the octahedral class of a cube: q and q*s are two names for the SAME cube"""
    return min(canon(qmul(q, s)) for s in OCT)


def build_menu():
    raw = {canon(t) for t in itertools.product(range(-14,15), repeat=4) if any(t)}
    kl = {}
    for q in raw:
        k = key(q); h = max(map(abs, q))
        if k not in kl or (h, q) < kl[k][:2]:
            kl[k] = (h, q)
    return sorted(v[1] for v in kl.values()), {k: v[1] for k, v in kl.items()}


def extend(base, cands):
    """count base+c for each candidate c, one engine process, base arrangement reused"""
    bs = ';'.join(','.join(map(str,q)) for q in base)
    inp = '\n'.join(','.join(map(str,c)) for c in cands) + '\n'
    p = subprocess.run(['./cube_regions_inc','--base',bs,'--candidates-stdin'],
                       input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l).get('bounded'))
        except Exception: out.append(None)
    if len(out) != len(cands):
        # one line per candidate, in order. If that ever stops holding the zip below
        # silently mislabels every count, so it is checked rather than assumed.
        raise SystemExit('engine returned %d lines for %d candidates' % (len(out), len(cands)))
    return list(zip(out, cands))


def bases():
    """one representative per CONGRUENCE CLASS, best n=5 count first.

    `n5family_keep.json` holds 76 bases and they are 11 compounds: the six highest-counting
    entries are six spellings of ONE, and extending all six would have spent 6x the CPU on
    one answer. `congruent.py` partitions them constructively -- it exhibits the rotation --
    and writes `n5family_classes.json`. Exactly one class reaches 393 (and it is congruent
    to the tower's 393); the other ten reach 387.
    """
    b = json.load(open('n5family_classes.json'))
    return [(c5, [tuple(q) for q in cf]) for c5, cf in b]


def report():
    best = (0, None, None); done = miss = 0
    for i, (c5, cf) in enumerate(bases()):
        for fn in sorted(os.listdir(OUT)) if os.path.isdir(OUT) else []:
            pass
        for sh in range(64):  # shard files are named by index, not enumerated
            path = os.path.join(OUT, 'b%d_s%d.json' % (i, sh))
            if not os.path.exists(path):
                continue
            done += 1
            for v, c in json.load(open(path)):
                if v and v > best[0]:
                    best = (v, cf, tuple(c))
    print('shard files present: %d' % done)
    print('best n=6 reached from the family: %s  (727 is the record)' % best[0])
    if best[1]:
        print(';'.join(','.join(map(str,q)) for q in best[1]) + ';' + ','.join(map(str,best[2])))
    return best


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--report':
        MENU, BY_KEY = [], {}
        report(); sys.exit()

    shard = int(sys.argv[1]); nsh = int(sys.argv[2])
    MENU, BY_KEY = build_menu()
    TARGET = BY_KEY[key(canon(KNOWN))]

    if shard == 0:
        # ONE candidate. The whole point of a gate is that it fails before the run, not after.
        got = extend(B393, [TARGET])[0][0]
        print('GATE: 393 + %s (menu spelling of %s) -> %s   [727 required]'
              % (str(TARGET), str(KNOWN), got), flush=True)
        if got != 727:
            sys.exit('gate failed; every negative from this menu would be void')
        with open('extend_n5.gate', 'w') as f:
            f.write('727\n')
    else:
        for _ in range(600):
            if os.path.exists('extend_n5.gate'):
                break
            time.sleep(1)
        else:
            sys.exit('shard %d: no gate file after 10 min; refusing to run ungated' % shard)

    os.makedirs(OUT, exist_ok=True)
    sub = MENU[shard::nsh]
    print('shard %d/%d: %d of %d menu cubes' % (shard, nsh, len(sub), len(MENU)), flush=True)
    for i, (c5, cf) in enumerate(bases()):
        path = os.path.join(OUT, 'b%d_s%d.json' % (i, shard))
        if os.path.exists(path):
            print('  base %d shard %d: already done' % (i, shard), flush=True)
            continue
        t0 = time.time()
        res = extend(cf, sub)
        tmp = path + '.%d.tmp' % os.getpid()          # pid in the temp name: siblings race
        with open(tmp, 'w') as f:
            json.dump([[v, list(c)] for v, c in res if v], f)
        os.replace(tmp, path)
        mx = max((v for v, _ in res if v), default=0)
        print('  base %d (n=5 %d) shard %d: best %d  (%.0fs)'
              % (i, c5, shard, mx, time.time()-t0), flush=True)
    print('shard %d done' % shard, flush=True)
