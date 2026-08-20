# Update PROJECT JOURNEY README CPP_SPEC

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-01T17:19:58 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01Tk1xQW8uhiqav2qi5z44ky` |
| Files named | `balance_hunt.py`, `bigd_probe.py`, `clique_hunt.py`, `corner_probe.py`, `cube_regions.cpp`, `cube_regions_q2.cpp`, `dof_probe.py`, `eliminate729.py`, `incidence.py`, `index_ledger.py`, `irrational_probe.py`, `locus_enum.py`, `locus_linear.py`, `locus_probe.py`, `mixed_enum.py`, `mixed_q2.py`, `mixed_q2_full.py`, `opencount.py`, `record_hunt.py`, `recover_1889.py`, `six_cube_search_results.md` |
| Present in repo | `balance_hunt.py`, `bigd_probe.py`, `clique_hunt.py`, `corner_probe.py`, `cube_regions.cpp`, `cube_regions_q2.cpp`, `dof_probe.py`, `eliminate729.py`, `incidence.py`, `index_ledger.py`, `irrational_probe.py`, `locus_enum.py`, `locus_linear.py`, `locus_probe.py`, `mixed_enum.py`, `mixed_q2.py`, `mixed_q2_full.py`, `opencount.py`, `record_hunt.py`, `recover_1889.py` |
| Cited in LEDGER/RESULTS | `balance_hunt.py`, `bigd_probe.py`, `clique_hunt.py`, `corner_probe.py`, `cube_regions.cpp`, `cube_regions_q2.cpp`, `dof_probe.py`, `eliminate729.py`, `incidence.py`, `index_ledger.py`, `irrational_probe.py`, `locus_enum.py`, `locus_linear.py`, `locus_probe.py`, `opencount.py`, `record_hunt.py`, `recover_1889.py` |

## Prompt as sent

```text
Documentation update in /Users/dmi/carroll. Add the 2026-07-31/08-01 results to `PROJECT.md`, `JOURNEY.md`, `README.md` and `CPP_SPEC.md`. Do NOT re-derive or re-run anything — all facts are below.

HARD CONSTRAINTS: do not edit `six_cube_search_results.md` (the ledger — the main session maintains it) or `RESULTS.md` (already updated). Do not touch `/Users/dmi/carroll/cubes/` or `cb/` — the user syncs the mirror themselves now. Top-level files only. An earlier pass already covered results through Postscript 47; this pass adds what came after.

## Facts (source: ledger Postscripts 48-51 and their addenda)

F1. **The coincidence walls factor into pairs of rational PLANES.** Each edge-edge coplanarity condition on the 393 base, written in Cayley coordinates for the free sixth cube, is not an irreducible quadric but a product of two rational linear forms. So the 144 walls per fixed cube collapse to just 24 distinct planes, a three-wall system is 8 linear 3x3 solves (Bezout's 8 = the eight plane choices), and the entire three-wall family is 134,784 systems giving 2,733 distinct configurations — EXHAUSTED in four minutes, maximum 727. A Groebner enumeration of the same family had ground through 1.3 million systems covering only part of it; ~99% of that work was re-deriving identical plane triples.

F2. **The all-rational character of those strata is an ARTIFACT**, not a fact about the problem: three rational planes always meet in a rational point, so irrational configurations cannot appear there by construction.

F3. **Corner-on-face conditions are IRREDUCIBLE QUADRICS** — a different stratum type. Pure corner triples are sparse (245 solved systems gave only 55 real roots) and top out at 719. But MIXED strata — two planes and one quadric — restrict the quadric to a line, giving a quadratic in one parameter, hence solutions that are rational or degree-2 irrational, i.e. ℚ(√d). That family holds 1,377,612 degree-2 irrational solutions against 2,856 rational ones, a ratio of about 240:1. Its rational half maxes at 725.

F4. **A ℚ(√d) C++ engine now exists**: `cube_regions_q2.cpp` generalises the integer engine's scalar type to ℤ[√d] with d given at runtime, leaving geometry and topology untouched. It runs ~100× faster than the Python algebraic path (5.3/11.5/21.9 ms at n=3/4/5 against 0.48/1.10/2.20 s). Verified: `--d 0` reproduces `cube_regions.cpp` bit-for-bit including per_label; the ℚ(√5) golden triple gives 67 = {1:48,2:18,3:1}; scaling invariance holds (multiplying all components by k>0 is the same rotation and must give the same count). `cube_regions.cpp` itself is unmodified.

F5. **82,458 irrational configurations across 56 quadratic fields have been counted — nothing above 727.** Every previous campaign in the project sampled integer quaternions, so this stratum was structurally invisible to all of them.

F6. **727 is a plateau of at least FIVE non-congruent compounds, one of them IRRATIONAL.** Four rational classes with depth profiles {214,220,156,100,36,1}, {216,216,160,98,36,1}, {214,218,160,98,36,1}, {214,216,162,98,36,1}; the fifth shares the last profile but lies in ℚ(√13) with sixth cube (1, 1−√13, 16−4√13, 11−3√13), and is non-congruent to it (differing O-reduced pair invariants). Two-engine verified (cube_regions_q2 and opencount.py, separate codebases). Every class satisfies d1+d2+d3+d4 = 690 with d5=36, d6=1 fixed. **This is the first irrational configuration the project found by SEARCH** — the two n=3 maximizers came from symmetry (the octahedron and the icosahedron).

F7. **ℚ(√13) is the only field among the 56 whose strata reach 727.** It is the 393 base's own tilt field (the unique 4-clique axis (3,2,0), tan 2/3). The most populous field ℚ(√5), with 13,500 solutions, tops out at 721; ℚ(√2) at 713.

F8. **The engine's overflow guard was rectangular (d ≤ 100 and |p|,|q| ≤ 512) and is now a traced per-configuration bound.** Tracing |p| and |q| separately through the pipeline showed the invariant is NOT d·m²: the true boundary's m²·d value runs ~9.0e6 at d=1, ~2.53e7 at d=29, and plateaus near 2.9-3.0e7 for large d — so a flat d·m² rule would be over-permissive below d≈38 (at d=5 it admits m=2289 against a true limit of 1855, an exploitable overflow). The engine now evaluates the traced bound at runtime. Widening the guard makes ~343,000 previously-unreachable configurations countable.

F9. **A search-space note worth recording**: the Cayley chart q=(1,a,b,c) cannot represent 180° rotations, which looked like a coverage gap. It is not one — q·(0,1,0,0) is a cube self-symmetry, so the chart omits quaternion representatives, not compounds; an independent second chart returns an identical census.

## Edits

E1. `PROJECT.md` — it is the analytic synthesis. Add F1-F3 near the existing material on search methods and the algebraic-search section; F4-F7 as a new subsection on irrational strata (this is a genuinely new capability for the project, so give it room); F6's plateau to the record-tower section, replacing or extending whatever it currently says about 727's plateau; F8 and F9 where the document discusses method or tooling. Update any open-problem item that F5 bears on (the n=6 question is now closed over several more strata, though not proved).

E2. `JOURNEY.md` — narrative in acts, with an existing Act X on the turn from searching to proving. Add a further act covering this arc: the walls turning out to be planes (and the enumeration collapsing from 27 hours to 4 minutes), the discovery that the all-rational result was an artifact of the condition type, the decision to build a ℚ(√d) engine, and the irrational 727 in the base's own tilt field. The shape of the story is that a challenge to an assumption exposed a whole stratum the project had never been able to see. Keep existing acts intact.

E3. `README.md` — the code map needs the new tooling: `cube_regions_q2.cpp` / `cube_regions_q2` (ℚ(√d) engine), `locus_linear.py`, `locus_probe.py`, `locus_enum.py` (marked superseded in its own header), `mixed_enum.py` / `mixed_q2.py` / `mixed_q2_full.py`, `corner_probe.py`, `incidence.py` (exact coincidence signatures), `eliminate729.py`, `dof_probe.py`, `record_hunt.py` + waves, `balance_hunt.py`, `clique_hunt.py`, `bigd_probe.py`, `irrational_probe.py`, `index_ledger.py` (regenerates the ledger's postscript index), `recover_1889.py`. Read each file's docstring for a one-line description rather than guessing. Also note in the n=6 records row or nearby that 727 has five known congruence classes including an irrational one in ℚ(√13).

E4. `CPP_SPEC.md` — it specifies the integer engine's design and invariants. Add a section noting that a second engine, `cube_regions_q2.cpp`, extends the scalar type to ℤ[√d] with a runtime-evaluated overflow bound rather than a fixed rectangle, that its geometry and topology are unchanged, and that it reproduces the integer engine exactly at `--d 0`. State F8's finding that the naive d·m² invariant is wrong, since that is the kind of trap a future implementer would otherwise repeat.

Match each document's voice. Be precise with numbers. Do not invent results beyond F1-F9.

## Report back
Files changed with before/after per edit, and anything you chose not to change and why.
```
