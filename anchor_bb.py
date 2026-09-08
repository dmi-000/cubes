#!/usr/bin/env python3
"""Is there an ADMISSIBLE, monotone bound for branch and bound in the anchor data?

Branch and bound needs a bound U(P) on every COMPLETION of a partial configuration
P, not an estimate of P.  The per-level Euler identity d_l = E_l - V_l + c_l + 1
([P243]) is an identity about the FINISHED arrangement: E, V and c_l all move
unboundedly when a cube is added, and c_l is exactly the term no prefix pins down
([OQ 30]).  So the Euler profile of a prefix bounds nothing above.

But ONE term of the deficit split in [P266] is monotone, and that is what this
measures.  Writing m_P(C) for the number of C's six face-centre directions already
killed by the cubes of P (Lemma 1: u in S_C(R) iff u in S_C({i}) for every i), a
killed anchor STAYS killed as more cubes arrive.  With ANCHOR ([P33] Theorem 1),

    d_(n-1)(S)  =  sum over C of #pi0(S_C)  <=  A(P) + 6(n-k),
    A(P) = sum over C in P of (6 - m_P(C)),   k = |P|,

for EVERY completion S of P.  Admissible, monotone non-increasing along a branch,
and free: alpha_i(C) depends only on the PAIR, so it is a 6-bit mask per ordered
pair and m_P(C) is a popcount of an OR.

What this file measures is whether it ever BINDS.  A bound that is admissible and
never below the trivial 6n prunes nothing, and that is an empirical question about
how often one cube reaches inside another's face centre -- not something to assert.
"""
import itertools, json, os, subprocess, sys, random, collections
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from edgecross import rotF

ENGINE = os.path.join(HERE, "cube_regions")
FACES = [(r, s) for r in range(3) for s in (F(1), F(-1))]


def cols(q):
    R = rotF(q)
    return [[R[k][i] for k in range(3)] for i in range(3)]


def pair_mask(MC, Mi):
    """6-bit mask: which of C's face-centre directions cube i kills on its own.

    u_f = s*MC[r] is a unit vector with |MC[r].u_f| = 1, so C fails to reach
    strictly least along u_f exactly when max_a |Mi[a].u_f| >= 1.
    """
    mask = 0
    for b, (r, s) in enumerate(FACES):
        u = [s * c for c in MC[r]]
        if max(abs(sum(Mi[a][k] * u[k] for k in range(3))) for a in range(3)) >= 1:
            mask |= 1 << b
    return mask


def profile(qs):
    """per-cube dead-anchor masks and the bound A(P), for the cubes present"""
    M = [cols(q) for q in qs]
    n = len(qs)
    dead = []
    for C in range(n):
        acc = 0
        for i in range(n):
            if i != C:
                acc |= pair_mask(M[C], M[i])
        dead.append(acc)
    A = sum(6 - bin(d).count("1") for d in dead)
    return dead, A


def engine(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENGINE, "--quats", spec], capture_output=True, text=True).stdout
    return json.loads(out)


def parse(spec):
    return [tuple(int(v) for v in g.split(",")) for g in spec.split(";")]


BASE = "4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1"
RECORDS = {
    # NOT the max(3) = 67 maximisers -- those are irrational (Q(sqrt2), Q(sqrt5))
    # and the integer engine cannot take them.  This is the 3-subset of the 183
    # record, a rational triple that attains d_2 = 18.  Labelled, not passed off.
    3: "1,0,0,0;0,5,3,2;1,-4,-1,1",
    4: "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4",
    5: BASE,
    6: BASE + ";7,14,1,-5",
    7: BASE + ";7,14,1,-5;4,-3,-4,-4",
    8: BASE + ";7,14,1,-5;4,-3,-4,-4;24,-24,24,-61",
}


def main():
    print("=" * 78)
    print("1. THE RECORDS: does the bound bind at the configurations that matter?")
    print("=" * 78)
    print(f"{'n':>2} {'total':>6} {'d_(n-1)':>8} {'6n':>4} {'A(S)':>5} {'dead anchors per cube':>26}")
    for n in sorted(RECORDS):
        qs = parse(RECORDS[n])
        e = engine(qs)
        d = e["by_depth"].get(str(n - 1), 0)
        dead, A = profile(qs)
        pc = [bin(x).count("1") for x in dead]
        print(f"{n:>2} {e['bounded']:>6} {d:>8} {6*n:>4} {A:>5}   {pc}")

    print()
    print("=" * 78)
    print("2. ALONG A BRANCH: the bound at each prefix of the n=8 record chain")
    print("   U(P) = A(P) + 6(n-k) must be >= the final d_(n-1) at every k (admissible)")
    print("   and non-increasing in k (monotone).  n = 8, target d_7.")
    print("=" * 78)
    qs8 = parse(RECORDS[8])
    final = engine(qs8)["by_depth"].get("7", 0)
    prev = None
    for k in range(2, 9):
        P = qs8[:k]
        dead, A = profile(P)
        U = A + 6 * (8 - k)
        flag = ""
        if prev is not None and U > prev:
            flag = "  <-- NOT MONOTONE"
        if U < final:
            flag += "  <-- INADMISSIBLE"
        print(f"  k={k}  A(P)={A:>3}  U(P)=A+6(8-k)={U:>3}   (final d_7 = {final}){flag}")
        prev = U

    print()
    print("=" * 78)
    print("3. DOES IT BIND AT ALL?  distribution of dead anchors per ORDERED PAIR")
    print("   (popcount of the 6-bit mask; 0 means that pair costs the bound nothing)")
    print("=" * 78)
    rnd = random.Random(7)
    for h in (1, 2, 3, 6, 12, 60):
        hist = collections.Counter()
        for _ in range(4000):
            qa = tuple(rnd.randint(-h, h) for _ in range(4))
            qb = tuple(rnd.randint(-h, h) for _ in range(4))
            if not any(qa) or not any(qb):
                continue
            hist[bin(pair_mask(cols(qa), cols(qb))).count("1")] += 1
        tot = sum(hist.values())
        zero = hist[0] / tot
        mean = sum(k * v for k, v in hist.items()) / tot
        print(f"  height {h:>3}: mean dead {mean:5.2f}   P(mask=0) = {zero:6.1%}   "
              f"{dict(sorted(hist.items()))}")

    print()
    print("=" * 78)
    print("5. THE OTHER ROUTE: the PROVED increment bound [P56], maximised over")
    print("   placements.  U(P) = TOTAL(P) + sum of Bmax(m) for the cubes still to")
    print("   come.  Bmax(m) = max cells that m other cubes' 6m face planes can cut")
    print("   on the new cube's surface.  CRUDE cap derived here, NOT from the")
    print("   project's own Lemma 1a -- two planes meet ∂C_new in <= 2 points, each")
    print("   plane curve has <= 6 vertices on the cube's 12 edges, degrees <= 4,")
    print("   components <= 6m+1.  Every step is generous; this is an upper bound on")
    print("   an upper bound and is quoted only to see whether the ROUTE could prune.")
    print("=" * 78)
    print(f"  {'m':>2} {'crude Bmax(m)':>14} {'actual increment':>17} {'ratio':>7}")
    tot = {}
    for n in sorted(RECORDS):
        tot[n] = engine(parse(RECORDS[n]))["bounded"]
    for n in sorted(RECORDS):
        if n - 1 not in tot:
            continue
        m = n - 1
        V = 6 * m * (6 * m - 1) + 36 * m + 8
        Bmax = V + 1 + (6 * m + 1)
        inc = tot[n] - tot[n - 1]
        print(f"  {m:>2} {Bmax:>14} {inc:>17} {Bmax/inc:>7.1f}x")
    print()
    print("  A bound 3-5x above the achieved increment, compounding over every")
    print("  remaining cube, cannot prune a branch whose completion is near the")
    print("  record.  The route is not refuted -- it needs a TIGHT Bmax, which is")
    print("  the open item, not the framework.")

    print()
    print("=" * 78)
    print("4. THE PAIRWISE NECESSARY CONDITION for d_(n-1) = 6n")
    print("   all masks zero is NECESSARY (not sufficient: m=0 still allows s>0).")
    print("   Checked on the records above -- see column A(S) vs 6n.")
    print("=" * 78)


if __name__ == "__main__":
    main()
