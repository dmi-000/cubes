#!/usr/bin/env python3
"""n = 9 record hunt, driven by the pair-type rule of METHODS.md section 9.

Both extensions at the top of the tower added exactly TWO 13-pairs and ZERO
9-pairs:

    727    4x13   9x9    2x4        (15 pairs)
    1217   6x13   9x9    6x4        (21)
    1895   8x13   9x9   11x4        (28)

If that holds once more, a ninth cube must form exactly two 13-pairs and no
9-pairs with the 1895 eight, giving 10x13 9x9 17x4 over 36 pairs.  That is a
cheap PRESCREEN: eight two-cube counts per candidate, batched through the engine
at n = 2 at ~500/s, against one n = 9 arrangement count at ~seconds.  So the run
spends its time on candidates the rule likes and prices the rule at the same
time -- the histogram of (13, 9, 4) profiles is logged whether or not anything
wins, which is what turns a failed hunt into a measurement.

Writes JSONL to n9_hunt.jsonl and a running summary to n9_hunt.log; both are
appended to, so it is safe to stop and restart.  Check progress with
`tail -5 n9_hunt.log`.
"""
import collections, json, math, os, random, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, "cube_regions_n")
EIGHT = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1),
         (7,14,1,-5),(4,-3,-4,-4),(24,-24,24,-61)]
CAP = 512
HEIGHTS = [4, 8, 16, 40, 100, 250, 512]
BATCH = 3000                      # candidates per engine call group
LOG = os.path.join(HERE, "n9_hunt.log")
OUT = os.path.join(HERE, "n9_hunt.jsonl")

def gcd4(q):
    g = 0
    for v in q: g = math.gcd(g, abs(v))
    return g

def canon(q):
    g = gcd4(q)
    if g == 0: return None
    q = tuple(v//g for v in q)
    for v in q:                                    # fix the sign convention
        if v > 0: break
        if v < 0: q = tuple(-v for v in q); break
    return q if max(abs(v) for v in q) <= CAP else None

def run(cfgs):
    """batched exact counts; cfgs is a list of lists of integer quaternions"""
    if not cfgs: return []
    inp = "\n".join(";".join(",".join(map(str, q)) for q in c) for c in cfgs)+"\n"
    p = subprocess.run([ENG, "--quats-stdin"], input=inp, capture_output=True, text=True)
    res = {}
    for line in p.stdout.splitlines():
        try: o = json.loads(line)
        except Exception: continue
        if "quats" not in o or "bounded" not in o: continue
        res[tuple(tuple(int(v) for v in q) for q in o["quats"])] = o["bounded"]
    return [res.get(tuple(tuple(q) for q in c)) for c in cfgs]

def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 20260806)
    base = run([EIGHT])[0]
    prof = collections.Counter()
    bucket = collections.defaultdict(list)
    seen = set()
    best = base
    tried = screened = 0
    t0 = time.time()
    logf = open(LOG, "a"); outf = open(OUT, "a")
    print("n=9 hunt: the 1895 eight counts %s; looking for a ninth cube with "
          "exactly two 13-pairs and no 9-pairs" % base, file=logf, flush=True)
    while True:
        cands = []
        while len(cands) < BATCH:
            h = HEIGHTS[rng.randrange(len(HEIGHTS))]
            q = canon(tuple(rng.randint(-h, h) for _ in range(4)))
            if q and q not in seen:
                seen.add(q); cands.append(q)
        pairs = [[b, q] for q in cands for b in EIGHT]
        counts = run(pairs)
        keep = []
        for i, q in enumerate(cands):
            lab = counts[8*i:8*i+8]
            if any(v is None for v in lab): continue
            k = (lab.count(13), lab.count(9))
            prof[k] += 1
            tried += 1
            # count the RULE bucket and its two neighbours, so the rule can be
            # compared against alternatives rather than only confirmed
            if k in ((2, 0), (1, 0), (3, 0)):
                keep.append((q, k))
        screened += sum(1 for _, k in keep if k == (2, 0))
        if keep:
            full = run([EIGHT+[q] for q, _ in keep])
            for (q, k), c in zip(keep, full):
                if c is None: continue
                bucket["%dx13/%dx9" % k].append(c)
                print(json.dumps({"quat": list(q), "count": c,
                                  "profile": "%dx13/%dx9" % k}), file=outf, flush=True)
                if c > best:
                    best = c
                    print("*** NEW BEST n=9: %d  ninth cube %s  profile %dx13/%dx9"
                          % (c, q, k[0], k[1]), file=logf, flush=True)
        top = " | ".join("%s n=%d mean %.1f max %d" % (nm, len(v), sum(v)/len(v), max(v))
                         for nm, v in sorted(bucket.items()) if v)
        print("[%6.0fs] tried %7d | rule-passing %5d (%.3f%%) | best n=9 so far %s | "
              "buckets %s" % (time.time()-t0, tried, screened,
                              100*screened/max(tried, 1), best, top),
              file=logf, flush=True)

if __name__ == "__main__":
    main()
