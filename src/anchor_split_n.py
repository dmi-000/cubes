#!/usr/bin/env python3
"""GATE for Theorem S at general n:  sum_T d_(n-2)(T) <= 6n(n-2) + d_(n-1)(S).

This is anchor_split.py generalised.  n = 4 is the case the project needs; the
theorem is stated for all n >= 3, and a general claim gated only at the one n it
was designed for is an untested generalisation, so this runs n = 3 and n = 5 too.

The proof reduces the inequality to two established project results --
FIB (fibration: d_{n-1} = sum_C #pi0(S_C)) and P33 Theorem 1 (every component
of S_C contains a face direction of C) -- plus two purely combinatorial steps.
This file exists because the proof's INTERMEDIATE objects, not just its
conclusion, have to be tested against a known answer: the engine's d2 and d3.

Everything here is computed independently of the C++ engine and of the
spherical picture, by a THIRD route: for K = intersection of the cubes in R,
K \ C is the union of the six open convex pieces K n {outside face f of C}, and
a union of convex sets has one component per component of its intersection
graph.  So #pi0 is 6 node-LPs + 15 edge-LPs, exact over Fraction.  If FIB and
the fibration bookkeeping are right, sum_C #pi0 must reproduce d2(T) and d3
exactly -- that is the gate.  It also tests Theorem 1 directly: #pi0 must equal
the number of BLOCKS of face directions, never more.

Invariant to maintain: comp/k/blocks are three different quantities and the
proof needs all three.  comp = components; k = |F n S_C| (face directions
surviving); blocks = grouping of those k by component.  Theorem 1 says
comp == blocks; k >= comp is then automatic and the DEFICIT splits as
6 - comp = (6 - k) + (k - comp) = m + s, which is what the proof adds up.
"""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from edgecross import rotF
from exactlp import feasible_strict

ENGINE = os.path.join(HERE, "cube_regions")


def cols(q):
    """the three face normals (unit, exact) of the cube R_q([-1,1]^3)"""
    R = rotF(q)
    return [[R[k][i] for k in range(3)] for i in range(3)]


def _rows_inside(Ms):
    """strict-interior rows for the cubes in Ms, homogenised with lambda (var 3)"""
    rows = []
    for M in Ms:
        for r in range(3):
            n = M[r]
            rows.append([-n[0], -n[1], -n[2], F(1)])   #  lambda - n.p > 0
            rows.append([n[0], n[1], n[2], F(1)])      #  lambda + n.p > 0
    return rows


def _row_outside(MC, f):
    """row for 'strictly outside face f=(r,s) of the cube with normals MC'"""
    r, s = f
    n = MC[r]
    return [s * n[0], s * n[1], s * n[2], F(-1)]       #  s*n.p - lambda > 0


FACES = [(r, s) for r in range(3) for s in (F(1), F(-1))]


def pi0(MC, Mothers):
    """#pi0 of (intersection of Mothers) \ (cube MC), and the component of each face.

    Exact.  Returns (ncomp, comp_of_face) with comp_of_face[f] = None if face f's
    piece is empty.
    """
    base = _rows_inside(Mothers) + [[F(0), F(0), F(0), F(1)]]   # lambda > 0
    active = []
    for f in FACES:
        if feasible_strict(base + [_row_outside(MC, f)], 4) is not None:
            active.append(f)
    parent = {f: f for f in active}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for f, g in itertools.combinations(active, 2):
        if find(f) == find(g):
            continue
        if feasible_strict(base + [_row_outside(MC, f), _row_outside(MC, g)], 4) is not None:
            parent[find(f)] = find(g)
    roots = {}
    comp_of = {f: None for f in FACES}
    for f in active:
        comp_of[f] = roots.setdefault(find(f), len(roots))
    return len(roots), comp_of


def anchors(MC, Mothers):
    """which face directions of MC lie in S_C, i.e. survive as anchors.

    u_f = s * MC[r] is a unit vector and |MC[r].u_f| = 1, so u_f is in S_C iff
    every other cube reaches strictly further out along u_f: max_a |M[a].u_f| < 1.
    """
    out = set()
    for (r, s) in FACES:
        u = [s * c for c in MC[r]]
        if all(max(abs(sum(M[a][k] * u[k] for k in range(3))) for a in range(3)) < 1
               for M in Mothers):
            out.add((r, s))
    return out


def engine(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    out = subprocess.run([ENGINE, "--quats", spec], capture_output=True, text=True).stdout
    return json.loads(out)


def analyse(qs):
    """all per-cube quantities the proof uses, plus the engine's answers"""
    n = len(qs)
    M = [cols(q) for q in qs]
    rec = {"per_cube": {}, "checks": []}
    d = {}
    for C in range(n):
        others = [i for i in range(n) if i != C]
        per = {}
        for size in (len(others) - 1, len(others)):
            for R in itertools.combinations(others, size):
                comp, comp_of = pi0(M[C], [M[i] for i in R])
                anc = anchors(M[C], [M[i] for i in R])
                blocks = len({comp_of[f] for f in anc})
                per[R] = {"comp": comp, "k": len(anc), "blocks": blocks,
                          "anchors": sorted(anc), "m": 6 - len(anc), "s": len(anc) - comp}
        rec["per_cube"][C] = per
    return rec


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--quats", action="append", default=[])
    ap.add_argument("--stdin", action="store_true")
    args = ap.parse_args()
    specs = list(args.quats)
    if args.stdin:
        specs += [l.strip() for l in sys.stdin if l.strip()]

    nviol = {"blocks": 0, "fib": 0, "s_mono": 0, "m_sub": 0, "perC": 0, "global": 0}
    ncfg = 0
    for spec in specs:
        qs = [tuple(int(v) for v in g.split(",")) for g in spec.split(";")]
        n = len(qs)
        assert n >= 3
        rec = analyse(qs)
        ncfg += 1
        full = engine(qs)
        d3 = full["by_depth"].get(str(n - 1), 0)

        # --- GATE A: FIB.  sum_C comp(S_C over all others) must equal the engine's d3
        fib3 = sum(rec["per_cube"][C][tuple(i for i in range(n) if i != C)]["comp"]
                   for C in range(n))
        okA = (fib3 == d3)
        if not okA:
            nviol["fib"] += 1

        # --- GATE A': same for each triple against the engine's d2(T)
        sumd2 = 0
        okA2 = True
        for m in range(n):
            T = [i for i in range(n) if i != m]
            e = engine([qs[i] for i in T])
            d2T = e["by_depth"].get(str(n - 2), 0)
            fib2 = sum(rec["per_cube"][C][tuple(i for i in T if i != C)]["comp"] for C in T)
            if fib2 != d2T:
                okA2 = False
            sumd2 += d2T
        if not okA2:
            nviol["fib"] += 1

        # --- GATE B: Theorem 1.  comp == blocks for every set considered
        for C in range(n):
            for R, v in rec["per_cube"][C].items():
                if v["comp"] != v["blocks"]:
                    nviol["blocks"] += 1

        # --- GATE C: the two combinatorial steps, per cube
        okC = True
        for C in range(n):
            others = [i for i in range(n) if i != C]
            t = rec["per_cube"][C][tuple(others)]
            pairs = [rec["per_cube"][C][tuple(i for i in others if i != mm)] for mm in others]
            if any(t["s"] > p["s"] for p in pairs):
                nviol["s_mono"] += 1
                okC = False
            if t["m"] > sum(p["m"] for p in pairs):
                nviol["m_sub"] += 1
                okC = False
            if sum(p["comp"] for p in pairs) > 6 * (n - 2) + t["comp"]:
                nviol["perC"] += 1
                okC = False
        if sumd2 > 6 * n * (n - 2) + d3:
            nviol["global"] += 1

        print(json.dumps({"spec": spec, "d3": d3, "sum_d2": sumd2,
                          "fib_d3": fib3, "fibA": okA, "fibA2": okA2, "combC": okC,
                          "per_cube": {str(C): {str(R): {kk: v[kk] for kk in
                                                         ("comp", "k", "blocks", "m", "s")}
                                                for R, v in rec["per_cube"][C].items()}
                                       for C in range(n)}}))
        sys.stdout.flush()
    print(json.dumps({"configs": ncfg, "violations": nviol}))


if __name__ == "__main__":
    main()
