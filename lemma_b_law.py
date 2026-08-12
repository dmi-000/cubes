#!/usr/bin/env python3
"""The singleton term is ADDITIVE in the two pair labels -- and that alone gives 67.

`step_b4.py` measures g(P,P') = max over rotation pairs with two-cube counts
P, P' of the singleton term s = comp(Ci \\ (Cj u Ck)).  Four independent shards
(seeds 11/22/33/44, 200 restarts x 5000 climb steps each) returned IDENTICAL
values on all ten combinations, with different witnesses.  Those ten values fit

    g(P, P') = v(P) + v(P'),      v(P) = 2 + 2*ceil((P-1)/4)
    v(13)=8   v(9)=6   v(5)=4   v(4)=4

exactly.  Substituting into Step B's decomposition T = 1 + sum_pairs + sum_i s_i,
with the pair terms bounded by 6 each unconditionally, each pair label appears at
two of the three cubes, so

    T  <=  19 + 2 * sum_over_pairs v(P)

and since max(2) = 13 is PROVED and v is monotone, T <= 19 + 2*24 = 67.

**The bound needs even less than the fit.** T <= 1 + 18 + 3*max(g), so
max(3) <= 67 follows from the single global statement s <= 16 -- no case analysis
over pair labels at all.  Lemma B's ten-value table is needed only for the
SHARPER claim that T <= 63 off the (13,13,13) cell, i.e. for uniqueness of the
maximising cell, not for the maximum itself.

STATUS.  The ten g values are hill-climbed maxima, so each is a LOWER bound on g;
four independent seeds agreeing at every one is strong evidence they are exact,
not a proof.  The additive law is a fit to those ten points.  Everything below is
verification of consequences that were NOT used in the fit.

Run: python3 lemma_b_law.py
"""
import itertools, json, math, random, subprocess

ENG = "/Users/dmi/cube-compounds/cube_regions_n"
MEASURED = {(13,13):16,(13,9):14,(13,5):12,(13,4):12,(9,9):12,
            (9,5):10,(9,4):10,(5,5):8,(5,4):8,(4,4):8}


def v(P):
    return 2 + 2*math.ceil((P-1)/4)


def bound(labels):
    return 19 + 2*sum(v(p) for p in labels)


def batch(cfgs):
    inp = "\n".join(";".join(",".join(map(str, q)) for q in c) for c in cfgs) + "\n"
    o = subprocess.run([ENG, "--quats-stdin"], input=inp, capture_output=True, text=True)
    out = {}
    for line in o.stdout.splitlines():
        try:
            j = json.loads(line)
        except Exception:
            continue
        out[tuple(tuple(q) for q in j["quats"])] = j["bounded"]
    return out


def check_fit():
    bad = [k for k in MEASURED if MEASURED[k] != v(k[0]) + v(k[1])]
    print("1. additive fit to the four-shard table: %s (%d combinations)"
          % ("EXACT" if not bad else "FAILS %s" % bad, len(MEASURED)))


def check_record_triples():
    """The n=4 record's four triples -- data NOT used in the fit."""
    Q = [(1,0,0,0),(0,5,3,2),(1,-4,-1,1),(1,1,-1,-4)]
    need = [[Q[i] for i in t] for t in itertools.combinations(range(4), 3)]
    need += [[Q[a],Q[b]] for a,b in itertools.combinations(range(4), 2)]
    res = batch(need)
    pair = {(a,b): res[(Q[a],Q[b])] for a,b in itertools.combinations(range(4),2)}
    print("2. the 183 record's triples (pair labels %s):"
          % sorted(pair.values(), reverse=True))
    for t in itertools.combinations(range(4), 3):
        labs = [pair[(a,b)] for a,b in itertools.combinations(t,2)]
        m = res[tuple(Q[i] for i in t)]
        b = bound(labs)
        print("     %s labels %-12s measured %3d   bound %3d   %s"
              % (str(t), sorted(labs, reverse=True), m, b,
                 "TIGHT" if m == b else ("ok" if m < b else "VIOLATION")))


def check_random(n=220, seed=7):
    rng = random.Random(seed)
    trips = []
    for _ in range(n):
        h = rng.choice([2,3,5,9,17])
        t = [tuple(rng.randint(-h,h) for _ in range(4)) for _ in range(3)]
        if all(any(q) for q in t):
            trips.append(t)
    need = []
    for t in trips:
        need.append(t)
        need += [[t[a],t[b]] for a,b in itertools.combinations(range(3),2)]
    res = batch(need)
    viol = tight = ok = 0
    for t in trips:
        kt = tuple(tuple(q) for q in t)
        labs = [res.get((tuple(t[a]),tuple(t[b]))) for a,b in itertools.combinations(range(3),2)]
        if kt not in res or any(l is None for l in labs):
            continue
        m, b = res[kt], bound(labs)
        viol += m > b
        tight += m == b
        ok += m < b
    print("3. %d random triples: %d violations, %d tight, %d slack"
          % (viol+tight+ok, viol, tight, ok))


if __name__ == '__main__':
    check_fit()
    check_record_triples()
    check_random()
    print("\n   max(2) = 13 (PROVED) => v <= 8 => T <= 19 + 2*24 = %d" % (19+2*24))
