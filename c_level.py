#!/usr/bin/env python3
"""When is c_ell = 3?  The by-level curve-arrangement component count, rebuilt.

c_ell is the number of connected components of the arc graph on the depth-ell
boundary, the term carried by the per-level Euler identity ([P243])

    d_ell = E_ell - V_ell + c_ell + 1.

An arc on the curve dA_i n dA_j has depth s+2 just inside and s just outside, so
it lies on the depth-ell boundary exactly when s = ell-1 other cubes strictly
contain it.  ell = 1 is v3_outer.outer_curve_components (s = 0); this is that
routine with the s = 0 test replaced by s = ell-1, which is the whole difference.

REBUILT because the script that produced c_check.log / c_recheck.log / bylevel.log
was never saved -- only the logs were.  So the first thing here is a GATE against
those logs' recorded numbers, which are a known answer for the intermediates
(V_ell and E_ell separately, not just c_ell): [P243]'s table for the n=4 record is
ell=1 V=150 E=240, ell=2 V=128 E=192, ell=3 V=44 E=66, all with c=1.

DEGENERACY.  Two cubes sharing a face plane make this pipeline invalid ([P246]):
the pairwise "curve" degenerates and the arc bookkeeping is meaningless.  Every
c_ell >= 3 ever recorded came from that locus, so the degeneracy test is not a
detail here -- it is the question.  `shares_plane` is checked and reported
separately, never silently filtered.
"""
import itertools, json, os, subprocess, sys, collections
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euler3 import rowsT, frames, segments
from cellcomplex import on_bdry_params

ENGINE = os.path.join(HERE, "cube_regions")


def strictly_inside(P, M):
    for r in range(3):
        v = sum(M[r][k] * P[k] for k in range(3))
        if v >= 1 or v <= -1:
            return False
    return True


def shares_plane(qs):
    """does any pair of cubes share a face plane (a common face normal, up to sign)?"""
    Ms = [rowsT(R) for R in frames(qs)]
    for i, j in itertools.combinations(range(len(qs)), 2):
        for a in range(3):
            for b in range(3):
                u, v = Ms[i][a], Ms[j][b]
                cr = [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
                if not any(cr):
                    return True
    return False


def level_graph(qs):
    """V_ell, E_ell, c_ell and the component sizes, for every level ell >= 1"""
    Ms = [rowsT(R) for R in frames(qs)]
    n = len(qs)
    per = collections.defaultdict(lambda: {"node": {}, "arcs": []})
    for i, j in itertools.combinations(range(n), 2):
        for p, d, lo, hi in segments(Ms[i], Ms[j]):
            cuts = sorted({lo, hi} | {t for k in range(n) if k not in (i, j)
                                      for t in on_bdry_params(p, d, lo, hi, Ms[k])})
            for a, b in zip(cuts, cuts[1:]):
                if a >= b:
                    continue
                mid = tuple(p[z] + ((a + b) / 2) * d[z] for z in range(3))
                s = sum(1 for k in range(n) if k not in (i, j) and strictly_inside(mid, Ms[k]))
                g = per[s + 1]
                ends = []
                for t in (a, b):
                    P = tuple(p[z] + t * d[z] for z in range(3))
                    g["node"].setdefault(P, len(g["node"]))
                    ends.append(g["node"][P])
                g["arcs"].append(tuple(ends))
    out = {}
    for ell, g in per.items():
        par = list(range(len(g["node"])))

        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x

        for a, b in g["arcs"]:
            par[f(a)] = f(b)
        comp = collections.Counter(f(x) for x in range(len(par)))
        out[ell] = {"V": len(g["node"]), "E": len(g["arcs"]),
                    "c": len(comp), "sizes": sorted(comp.values(), reverse=True)}
    return out


def engine(qs):
    spec = ";".join(",".join(str(v) for v in q) for q in qs)
    return json.loads(subprocess.run([ENGINE, "--quats", spec],
                                     capture_output=True, text=True).stdout)


def parse(spec):
    return [tuple(int(v) for v in g.split(",")) for g in spec.split(";")]


GATE = [("n=4 record 183", "1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4",
         {1: (150, 240, 1), 2: (128, 192, 1), 3: (44, 66, 1)})]


def gate():
    print("GATE against [P243]/bylevel.log recorded V, E and c -- intermediates, not just c")
    ok = True
    for name, spec, want in GATE:
        qs = parse(spec)
        got = level_graph(qs)
        e = engine(qs)
        for ell, (V, E, c) in want.items():
            g = got.get(ell, {"V": -1, "E": -1, "c": -1})
            d = e["by_depth"].get(str(ell), 0)
            idc = g["E"] - g["V"] + g["c"] + 1
            good = (g["V"], g["E"], g["c"]) == (V, E, c) and idc == d
            ok &= good
            print(f"  {name} ell={ell}: V={g['V']} (want {V})  E={g['E']} (want {E})  "
                  f"c={g['c']} (want {c})  E-V+c+1={idc} vs engine d={d}  "
                  f"{'OK' if good else '*** MISMATCH ***'}")
    return ok


def report(qs, label=""):
    e = engine(qs)
    lv = level_graph(qs)
    deg = shares_plane(qs)
    rows = []
    for ell in sorted(lv):
        g = lv[ell]
        d = e["by_depth"].get(str(ell), 0)
        rows.append((ell, g["V"], g["E"], g["c"], g["E"] - g["V"] + g["c"] + 1, d, g["sizes"]))
    return {"spec": ";".join(",".join(str(v) for v in q) for q in qs),
            "total": e["bounded"], "degenerate": deg, "levels": rows, "label": label}


def show(r):
    print(f"  {r['label']}  total={r['total']}  shares a face plane: {r['degenerate']}")
    print(f"    {r['spec']}")
    for ell, V, E, c, idc, d, sizes in r["levels"]:
        mark = "" if idc == d else "   <-- IDENTITY FAILS"
        print(f"      ell={ell}  V={V:>4} E={E:>4} c={c:>3}  E-V+c+1={idc:>4}  "
              f"engine d={d:>4}{mark}   component sizes {sizes[:8]}")


def main():
    import random
    if not gate():
        print("GATE FAILED -- nothing below is trustworthy")
        return
    print()
    print("=" * 78)
    print("THE RECORDED c=3 CASE (c_check.log): is it degenerate, and is c still 3?")
    print("=" * 78)
    show(report(parse("1,0,0,0;1,4,-4,12;3,-1,1,-3;5,-1,1,-3"), "c_check's ell=2 c=3"))

    print()
    print("=" * 78)
    print("SEARCH: c_ell >= 3, split by whether the pipeline is VALID there")
    print("=" * 78)
    rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 5)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    seen = collections.Counter()
    hits_valid, hits_deg = [], []
    for t in range(N):
        # deliberately weighted TOWARD the locus where c > 1 has ever been seen:
        # small integer quaternions, shared axes, and exact plane sharing.
        mode = t % 4
        n = rnd.choice((4, 4, 5))
        if mode == 0:
            qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-3, 3) for _ in range(4)) for _ in range(n - 1)]
        elif mode == 1:
            ax = tuple(rnd.randint(-3, 3) for _ in range(3))
            qs = [(1, 0, 0, 0)] + [(rnd.randint(1, 6),) + ax for _ in range(n - 1)]
        elif mode == 2:
            qs = [(1, 0, 0, 0)]
            for _ in range(n - 1):
                a = rnd.randrange(3)
                q = [rnd.randint(1, 6), 0, 0, 0]
                q[1 + a] = rnd.randint(-6, 6)
                qs.append(tuple(q))
        else:
            qs = [(1, 0, 0, 0)] + [tuple(rnd.randint(-9, 9) for _ in range(4)) for _ in range(n - 1)]
        if any(not any(q) for q in qs):
            continue
        try:
            r = report(qs)
        except Exception:
            continue
        deg = r["degenerate"]
        for ell, V, E, c, idc, d, sizes in r["levels"]:
            seen[(deg, c)] += 1
            if c >= 3:
                (hits_deg if deg else hits_valid).append((ell, c, sizes, r))
    print("level-instances by (shares a face plane, c):")
    for k in sorted(seen):
        print(f"   degenerate={str(k[0]):5s} c={k[1]:<3} : {seen[k]}")
    print()
    print(f"c >= 3 on NON-degenerate configurations : {len(hits_valid)}")
    for ell, c, sizes, r in hits_valid[:6]:
        print(f"   ell={ell} c={c} sizes={sizes[:8]}")
        show(r)
    print(f"c >= 3 on plane-degenerate configurations : {len(hits_deg)}")
    for ell, c, sizes, r in hits_deg[:3]:
        print(f"   ell={ell} c={c} sizes={sizes[:8]}   {r['spec']}")


if __name__ == "__main__":
    main()
