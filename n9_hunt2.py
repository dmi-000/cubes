#!/usr/bin/env python3
"""n = 9 hunt, v2: search NEAR CUBE SYMMETRIES, which is what v1 actually found.

v1 sampled random integer quaternions and screened them by the pair-type rule of
METHODS.md section 9 ("exactly two 13-pairs, no 9-pairs").  Two results after
~1M candidates:

  * the rule does NOT predict a better extension.  Counting all three
    neighbouring buckets rather than only the hypothesis:
        1x13/0x9  n=761   mean 2726.4  max 2771
        2x13/0x9  n=3380  mean ~2729   max 2781     <- the rule
        3x13/0x9  n=930   mean 2732.0  max 2777
    Means within 8 of each other, and the rule bucket is not the best of them.

  * what DOES predict it: 19 of the 20 best ninth cubes are k*S + P for S one of
    the 24 cube-symmetry quaternions and |P| = 1 -- a single unit step off a
    scaled symmetry.  The 20th is |P| = 4.

So this enumerates that family directly instead of waiting for random sampling to
land in it.  Near a symmetry the ninth cube nearly coincides with a copy already
present, which is the same mechanism that makes n = 2's 13 happen just off the
body diagonal -- many thin slabs rather than few fat ones.

    python3 n9_hunt2.py            # appends to n9_hunt2.{log,jsonl}
"""
import collections, itertools, json, math, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")
EIGHT = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]
CAP, KMAX, PMAX = 512, 400, 1
LOG = os.path.join(HERE, "n9_hunt2.log")
OUT = os.path.join(HERE, "n9_hunt2.jsonl")

SYM = []
for q in itertools.product((-1,0,1), repeat=4):
    if any(q) and sum(v*v for v in q) in (1,2,4): SYM.append(q)

def canon(q):
    g = 0
    for v in q: g = math.gcd(g, abs(v))
    if g == 0: return None
    q = tuple(v//g for v in q)
    for v in q:
        if v > 0: break
        if v < 0: q = tuple(-v for v in q); break
    return q if max(abs(v) for v in q) <= CAP else None

def run(cfgs):
    if not cfgs: return []
    inp = "\n".join(";".join(",".join(map(str, q)) for q in c) for c in cfgs)+"\n"
    p = subprocess.run([ENG, "--quats-stdin"], input=inp, capture_output=True, text=True)
    res = {}
    for line in p.stdout.splitlines():
        try: o = json.loads(line)
        except Exception: continue
        if "quats" in o and "bounded" in o:
            res[tuple(tuple(int(v) for v in q) for q in o["quats"])] = o["bounded"]
    return [res.get(tuple(tuple(q) for q in c)) for c in cfgs]

def candidates():
    seen = set()
    for k in range(1, KMAX+1):
        for S in SYM:
            for P in itertools.product(range(-PMAX, PMAX+1), repeat=4):
                if not any(P): continue
                q = canon(tuple(k*S[i]+P[i] for i in range(4)))
                if q and q not in seen:
                    seen.add(q); yield q, S, k, P

def main():
    base = run([EIGHT])[0]
    best, tried, counted = base, 0, 0
    bucket = collections.defaultdict(list)
    t0 = time.time()
    logf = open(LOG, "a"); outf = open(OUT, "a")
    print("n=9 v2: near-symmetry family, k<=%d |P|<=%d; the 1895 eight counts %s"
          % (KMAX, PMAX, base), file=logf, flush=True)
    gen = candidates(); done = False
    while not done:
        chunk = []
        for _ in range(400):
            try: chunk.append(next(gen))
            except StopIteration: done = True; break
        if not chunk: break
        pairs = [[b, q] for q, _, _, _ in chunk for b in EIGHT]
        lab = run(pairs)
        keep = []
        for i, (q, S, k, P) in enumerate(chunk):
            L = lab[8*i:8*i+8]
            if any(v is None for v in L): continue
            tried += 1
            keep.append((q, S, k, P, (L.count(13), L.count(9))))
        full = run([EIGHT+[q] for q, _, _, _, _ in keep])
        for (q, S, k, P, prof), c in zip(keep, full):
            if c is None: continue
            counted += 1
            bucket["%dx13/%dx9" % prof].append(c)
            print(json.dumps({"quat": list(q), "count": c, "sym": list(S),
                              "k": k, "P": list(P),
                              "profile": "%dx13/%dx9" % prof}), file=outf, flush=True)
            if c > best:
                best = c
                print("*** NEW BEST n=9: %d  ninth cube %s = %d*%s + %s  profile %dx13/%dx9"
                      % (c, q, k, S, P, prof[0], prof[1]), file=logf, flush=True)
        top = " | ".join("%s n=%d mean %.1f max %d" % (nm, len(v), sum(v)/len(v), max(v))
                         for nm, v in sorted(bucket.items(), key=lambda x: -len(x[1]))[:4] if v)
        print("[%6.0fs] enumerated %7d | counted %7d | best %s | %s"
              % (time.time()-t0, tried, counted, best, top), file=logf, flush=True)
    print("family exhausted: %d candidates, best %s" % (tried, best), file=logf, flush=True)

if __name__ == "__main__":
    main()
