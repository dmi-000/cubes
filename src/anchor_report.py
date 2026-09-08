#!/usr/bin/env python3
"""Roll up the anchor_split gates.  Reports, separately: violations of each gate,
and how often each gate was actually EXERCISED -- a pass on a pool that never
exercised a step is not evidence about that step (FAILURE_MODES 29)."""
import glob, json, sys, collections

files = sys.argv[1:] or glob.glob("anchor_gate_*.jsonl")
viol = collections.Counter()
exer = collections.Counter()
bind = collections.Counter()
n_cfg = 0
tight = 0
slack = collections.Counter()
d3hist = collections.Counter()
for f in files:
    for line in open(f):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if "configs" in d:
            continue
        n_cfg += 1
        n = len(d["spec"].split(";"))
        if not d["fibA"]:
            viol["FIB d_(n-1)"] += 1
        if not d["fibA2"]:
            viol["FIB d_(n-2)(T)"] += 1
        if d["sum_d2"] > 6 * n * (n - 2) + d["d3"]:
            viol["Theorem S"] += 1
        if d["sum_d2"] == 6 * n * (n - 2) + d["d3"]:
            tight += 1
        slack[6 * n * (n - 2) + d["d3"] - d["sum_d2"]] += 1
        d3hist[d["d3"]] += 1
        for C, per in d["per_cube"].items():
            # key strings are repr'd tuples; "(1,)" and "(2, 3)" both have ONE comma,
            # so size must come from parsing, not from counting commas (this bit
            # reported 41 phantom Lemma-3 violations at n=3 before it was fixed).
            import ast
            full = max(per, key=lambda R: len(ast.literal_eval(R)))
            t = per[full]
            subs = [v for R, v in per.items() if R != full]
            if t["comp"] != t["blocks"] or any(v["comp"] != v["blocks"] for v in subs):
                viol["ANCHOR (comp==blocks)"] += 1
            # Lemma 3 is only EXERCISED when some s > 0
            if any(v["s"] > 0 for v in subs) or t["s"] > 0:
                exer["Lemma 3 (s monotone)"] += 1
                if any(t["s"] > v["s"] for v in subs):
                    viol["Lemma 3 (s monotone)"] += 1
            # Lemma 2 only exercised when some anchor is lost
            if t["m"] > 0:
                exer["Lemma 2 (m subadditive)"] += 1
                if t["m"] > sum(v["m"] for v in subs):
                    viol["Lemma 2 (m subadditive)"] += 1
            if t["comp"] < 6 or any(v["comp"] < 6 for v in subs):
                exer["non-maximal c (deficit nonzero)"] += 1
            if sum(v["comp"] for v in subs) > 6 * (n - 2) + t["comp"]:
                viol["per-cube theorem"] += 1
            if sum(v["comp"] for v in subs) == 6 * (n - 2) + t["comp"]:
                exer["per-cube tight"] += 1
                bind["tight WITH nonzero deficit" if t["m"] + t["s"] > 0
                     else "tight with zero deficit (lemmas vacuous)"] += 1
            if t["s"] > 0 and t["s"] == min(v["s"] for v in subs):
                bind["Lemma 3 binding (s(t) = min over subsets)"] += 1
            if t["m"] > 0:
                ms = sorted((v["m"] for v in subs), reverse=True)
                if len(ms) >= 2 and t["m"] == ms[0] + ms[1]:
                    bind["Lemma 2 binding (m(t) = its two-term bound)"] += 1

print(f"configurations: {n_cfg}")
print(f"Theorem S tight (equality): {tight}")
print("\nVIOLATIONS")
for k in ("FIB d_(n-1)", "FIB d_(n-2)(T)", "ANCHOR (comp==blocks)",
          "Lemma 2 (m subadditive)", "Lemma 3 (s monotone)",
          "per-cube theorem", "Theorem S"):
    print(f"  {k:28s} {viol[k]}")
print("\nEXERCISED (cube-instances; a zero here means the pool never tested it)")
for k, v in sorted(exer.items()):
    print(f"  {k:34s} {v}")
print("\nslack of Theorem S (bound - actual):")
for s in sorted(slack):
    print(f"  {s:4d} : {slack[s]}")
print("\nd_(n-1) values seen:", dict(sorted(d3hist.items())))
print("\nBINDING (does the proof's slack accounting get tested at the boundary,")
print("or only where every deficit is zero and the lemmas are vacuous?)")
for k, v in sorted(bind.items()):
    print(f"  {k:44s} {v}")
