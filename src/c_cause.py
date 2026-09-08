#!/usr/bin/env python3
"""Do DEGENERACIES create c > 1?

The question separates into two, because [P268] showed c > 1 has two different
shapes under the antipodal decomposition c = (#self-antipodal) + 2*(#pairs):

  c = 2  is  0 self + 1 pair  -- the graph is CONNECTED in the quotient mod +-,
         but its antipodal double cover is TRIVIAL: every loop downstairs lifts
         to a loop, so the lift is two disjoint copies.  Nothing is broken; this
         is a Z/2 monodromy fact about a connected object.
  c >= 3 needs a component to DETACH on top of that -- genuine fragmentation.

So "degeneracy causes c > 1" could be true of one shape and false of the other,
and a single P(c>1 | degenerate) would hide that.  This measures them apart, and
tests validity by whether the per-level Euler identity HOLDS rather than by the
shared-plane locus alone ([P268]: on the degenerate cases the identity fails, so
its failure is the sharper validity test).

Other coincidences are tested too, because "non-degenerate" here means only "no
shared face plane" -- if the non-degenerate c=2 cases all carry some OTHER
coincidence, the answer would be yes with a different definition of degenerate.
"""
import collections, itertools, json, os, random, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euler3 import rowsT, frames
from c_level import level_graph, shares_plane, parse, engine
from c_antipodal import components_with_nodes, antipodal_structure


def _par(u, v):
    cr = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
    return not any(cr)


def coincidences(qs):
    """cheap exact coincidence flags, beyond the shared-face-plane one"""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    edges = []          # the 12 edge directions of each cube = its 3 face normals
    for M in Ms:
        edges.append([M[a] for a in range(3)])
    diags = []          # the 4 body-diagonal directions of each cube
    for M in Ms:
        ds = []
        for sx in (1, -1):
            for sy in (1, -1):
                ds.append([M[0][k]*1 + M[1][k]*sx + M[2][k]*sy for k in range(3)])
        diags.append(ds)
    flags = collections.Counter()
    for i, j in itertools.combinations(range(n), 2):
        for a in range(3):
            for b in range(3):
                if _par(Ms[i][a], Ms[j][b]):
                    flags["shared face plane"] += 1
                if sum(Ms[i][a][k]*Ms[j][b][k] for k in range(3)) == 0:
                    flags["face normal _|_ face normal"] += 1
        for u in edges[i]:
            for v in diags[j]:
                if _par(u, v):
                    flags["face normal || body diagonal"] += 1
        for u in diags[i]:
            for v in diags[j]:
                if _par(u, v):
                    flags["shared body diagonal"] += 1
    return flags


def study(qs):
    e = engine(qs)
    lv = level_graph(qs)
    deg = shares_plane(qs)
    rows = []
    for ell in sorted(lv):
        g = lv[ell]
        d = e["by_depth"].get(str(ell), 0)
        idc = g["E"] - g["V"] + g["c"] + 1
        sa = pr = un = None
        if g["c"] > 1:
            sa, pr, un = antipodal_structure(components_with_nodes(qs, ell))
        rows.append({"ell": ell, "c": g["c"], "identity_ok": idc == d,
                     "self": sa, "pairs": pr, "unmatched": un,
                     "sizes": g["sizes"][:6]})
    return {"deg": deg, "levels": rows, "coin": coincidences(qs), "total": e["bounded"]}


def main():
    print("=" * 78)
    print("1. THE KNOWN c>1 CONFIGURATIONS: is each one degenerate, and does the")
    print("   IDENTITY hold there?  (identity holding = the value is a measurement)")
    print("=" * 78)
    specs = [l.strip() for l in open("c2_configs.txt") if l.strip()]
    tally = collections.Counter()
    nondeg_c2 = []
    for spec in specs:
        qs = parse(spec)
        try:
            r = study(qs)
        except Exception as ex:
            print("  skip", spec, ex)
            continue
        for row in r["levels"]:
            if row["c"] > 1:
                tally[(r["deg"], row["c"], row["identity_ok"])] += 1
                if not r["deg"] and row["identity_ok"]:
                    nondeg_c2.append((spec, row, r["coin"]))
    print("  (shares face plane, c, identity holds) -> count")
    for k in sorted(tally):
        print(f"    deg={str(k[0]):5s} c={k[1]:<3} identity_ok={str(k[2]):5s} : {tally[k]}")
    print()
    print(f"  c>1 instances that are NON-degenerate AND identity-valid: {len(nondeg_c2)}")
    for spec, row, coin in nondeg_c2[:8]:
        print(f"    ell={row['ell']} c={row['c']} self={row['self']} pairs={row['pairs']} "
              f"sizes={row['sizes']}")
        print(f"      {spec}")
        print(f"      other coincidences: {dict(coin) if coin else 'NONE'}")

    print()
    print("=" * 78)
    print("2. RATES: P(c>1) with and without a shared face plane, by SHAPE")
    print("=" * 78)
    rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 250
    stat = collections.Counter()
    for t in range(N):
        n = rnd.choice((4, 4, 5))
        mode = t % 3
        if mode == 0:
            qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-3, 3) for _ in range(4)) for _ in range(n-1)]
        elif mode == 1:
            qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-9, 9) for _ in range(4)) for _ in range(n-1)]
        else:
            qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-40, 40) for _ in range(4)) for _ in range(n-1)]
        if any(not any(q) for q in qs):
            continue
        try:
            r = study(qs)
        except Exception:
            continue
        for row in r["levels"]:
            shape = ("c=1" if row["c"] == 1 else
                     "c=2 (0 self + 1 pair)" if row["c"] == 2 and row["self"] == 0 else
                     "c=2 (other shape)" if row["c"] == 2 else
                     "c>=3 (detachment)")
            stat[(r["deg"], shape, row["identity_ok"])] += 1
    tot_d = sum(v for k, v in stat.items() if k[0])
    tot_n = sum(v for k, v in stat.items() if not k[0])
    print(f"  level-instances: {tot_n} non-degenerate, {tot_d} plane-degenerate")
    for k in sorted(stat, key=lambda x: (x[0], x[1])):
        base = tot_d if k[0] else tot_n
        print(f"    deg={str(k[0]):5s} {k[1]:24s} identity_ok={str(k[2]):5s} : "
              f"{stat[k]:>5}  ({stat[k]/base:6.2%})")


if __name__ == "__main__":
    main()
