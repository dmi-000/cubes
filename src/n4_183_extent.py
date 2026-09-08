#!/usr/bin/env python3
"""Does the 183 set have extent, and do random-seeded climbs find it?

Two questions the n=4 census could not answer:
  1. Is 183 an isolated configuration, or does it lie on a positive-dimensional
     set?  Probed by the lattice-cardinality method: in the 9-dimensional n=4
     space a d-dimensional component contributes 3^d - 1 of the 3^9 - 1 = 19682
     radius-1 neighbours.
  2. Do climbs from RANDOM seeds reach 183, or only climbs seeded from the
     leading cells?  Postscript 74 measured the second; this measures the first.

Written to a FILE and run, not piped through a backgrounded heredoc -- that
construct has now silently truncated four separate runs in this project
(FAILURE_MODES.md section 11), including twice today.
"""
import collections, itertools, json, math, random, io, subprocess, sys
from record_hunt import Engine, climb

REC = [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]

def red(q):
    g = 0
    for x in q: g = math.gcd(g, abs(x))
    return tuple(x//g for x in q) if g > 1 else tuple(q)

def counts(cfgs):
    out = []
    for i in range(0, len(cfgs), 2000):
        ch = cfgs[i:i+2000]
        inp = '\n'.join(';'.join(','.join(map(str,q)) for q in c) for c in ch)+'\n'
        p = subprocess.run(['./cube_regions_n','--quats-stdin'], input=inp,
                           capture_output=True, text=True)
        r = [json.loads(l).get('bounded') for l in p.stdout.splitlines()
             if l.startswith('{')]
        if len(r) != len(ch):
            raise SystemExit('engine returned %d of %d' % (len(r), len(ch)))
        out += r
    return out

print('=== 1. extent of the 183 set at the record ===', flush=True)
for den in (32, 128, 512):
    cfgs = []
    for d in itertools.product((-1,0,1), repeat=9):
        if not any(d): continue
        c = [REC[0]]; ok = True
        for j in range(3):
            w,x,y,z = REC[j+1]
            num = (w*den, x*den+d[3*j]*w, y*den+d[3*j+1]*w, z*den+d[3*j+2]*w)
            if not any(num): ok = False; break
            c.append(red(num))
        if ok: cfgs.append(c)
    v = counts(cfgs)
    keep = sum(1 for t in v if t == 183)
    h = collections.Counter(v)
    print('  step 1/%-4d probed %5d  still 183: %4d   top neighbours %s'
          % (den, len(cfgs), keep,
             dict(sorted(h.items(), reverse=True)[:5])), flush=True)
print('  reference: 3^d-1 is 0, 2, 8, 26, 80 for d = 0,1,2,3,4', flush=True)

print('\n=== 2. do RANDOM-seeded climbs reach 183? ===', flush=True)
rng = random.Random(777)
def draw(h):
    while True:
        q = tuple(rng.randint(-h,h) for _ in range(4))
        if any(q): return list(red(q))
eng = Engine(4, 1)
peaks = []
for s in range(24):
    h = [4,8,16,40,100][s % 5]
    seed = [[1,0,0,0]] + [draw(h) for _ in range(3)]
    _, pk = climb(eng, seed, io.StringIO(), 's%d'%s, rng, restarts=4)
    peaks.append(pk)
    print('  seed %2d (height %3d) -> %d' % (s, h, pk), flush=True)
c = collections.Counter(peaks)
print('  reached 183: %d of 24   distribution %s'
      % (sum(1 for p in peaks if p >= 183),
         ' '.join('%d×%d' % (v,k) for k,v in sorted(c.items(), reverse=True))))
