#!/usr/bin/env python3
"""Map the locus shape at each tower rung — is 727 / 1217 / 1895 a continuum?

WHY (OPEN_QUESTIONS 9). A plateau is one object by count and many by extension:
723's members reach four distinct n=7 maxima (spread 8), and 2785's reach 3905-3913
(spread 8), with the RECORDED member the worst tested. Every rung was built by
extending its predecessor's recorded representative, so if 727, 1217 and 1895 are
continua too, each rung may be the best extension of an arbitrary base.

Only 2785's shape is mapped (P178: two rays k >= 56 and k <= -69, punctured where
the ninth cube duplicates a base cube). Its family is the line
    (k, k, k-1, k)  =  k*(1,1,1,1) + (0,0,-1,0)
through the recorded ninth cube. This sweeps the analogous lines at the other
rungs: the last cube displaced along integer directions through its recorded value,
reporting where the record count holds.

Refusals are rescued by global rotation (P180 Addendum 5), never scored as absent.
"""
import json, os, subprocess, sys, time
from math import gcd
sys.path.insert(0, '.')
from growth727 import BASE

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'cube_regions_n')
C6 = BASE + [(7, 14, 1, -5)]
C7 = C6 + [(4, -3, -4, -4)]
C8 = C7 + [(24, -24, 24, -61)]
C9 = C8 + [(56, 56, 55, 56)]
RUNGS = [('727', C6, 727), ('1217', C7, 1217), ('1895', C8, 1895), ('2785', C9, 2785)]
DIRS = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),
        (1,1,1,1),(1,1,1,-1),(1,1,-1,1),(1,-1,1,1),(-1,1,1,1),
        (1,1,0,0),(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1)]
ROTS = [(2,1,0,0),(1,1,1,0),(3,0,1,2),(5,1,2,1)]


def qmul(p, q):
    w,x,y,z = p; e,f,g,h = q
    return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g, w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)


def canon(q):
    g = 0
    for v in q: g = gcd(g, abs(v))
    if g == 0: return None
    q = tuple(v//g for v in q)
    for v in q:
        if v > 0: break
        if v < 0: q = tuple(-x for x in q); break
    return q


def batch(cfgs):
    if not cfgs: return []
    inp = '\n'.join(';'.join(','.join(map(str,q)) for q in c) for c in cfgs) + '\n'
    p = subprocess.run([ENG, '--quats-stdin'], input=inp, capture_output=True, text=True)
    out = []
    for l in p.stdout.splitlines():
        try: out.append(json.loads(l).get('bounded'))
        except Exception: out.append(None)
    return out + [None]*(len(cfgs)-len(out))


def rescue(cfg):
    for g in ROTS:
        r = [canon(qmul(g, q)) for q in cfg]
        if any(x is None for x in r) or max(abs(v) for q in r for v in q) > 512: continue
        v = batch([r])[0]
        if v is not None: return v
    return None


def main():
    out = {}
    t0 = time.time()
    for name, cfg, rec in RUNGS:
        base, last = cfg[:-1], cfg[-1]
        print('\n%s  (last cube %s)' % (name, (last,)), flush=True)
        for d in DIRS:
            ts, cfgs = [], []
            for t in range(-60, 61):
                if t == 0: continue
                q = canon(tuple(last[i] + t*d[i] for i in range(4)))
                if q is None or max(map(abs,q)) > 512: continue
                ts.append(t); cfgs.append(base + [q])
            vals = []
            for i in range(0, len(cfgs), 400): vals += batch(cfgs[i:i+400])
            vals = [v if v is not None else rescue(c) for v, c in zip(vals, cfgs)]
            hold = [t for t, v in zip(ts, vals) if v == rec]
            better = [(t, v) for t, v in zip(ts, vals) if v is not None and v > rec]
            if hold or better:
                span = '%d..%d' % (min(hold), max(hold)) if hold else '-'
                print('   dir %-14s record holds at %3d of %3d offsets (t in %s)%s'
                      % (str(d), len(hold), len(ts), span,
                         '   *** BEATS: %s' % better[:3] if better else ''), flush=True)
            out.setdefault(name, {})[str(d)] = {'hold': hold, 'better': better, 'n': len(ts)}
    json.dump(out, open(os.path.join(HERE, 'shapes.json'), 'w'), indent=1)
    print('\n%.0fs' % (time.time()-t0), flush=True)


if __name__ == '__main__':
    main()
