# Build region adjacency invariant

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-01T23:37:37 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01DERycv4V2SvSfPDFwJDX4m` |
| Files named | `certify_six.py`, `cube_regions.cpp`, `region_adjacency.py` |
| Present in repo | `certify_six.py`, `cube_regions.cpp`, `region_adjacency.py` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_regions.cpp`, `region_adjacency.py` |

## Prompt as sent

```text
Engineering task in /Users/dmi/carroll: compute the REGION ADJACENCY GRAPH of a cube compound, so configurations can be classified topologically rather than merely by region counts.

## Background you must read

- `certify_six.py` — the Python exact counting engine, function `exact_count_config(rots, verbose=False, with_labels=True)`. This is the pipeline to extend. It cuts a box by all 6n face planes into convex fragments with exact rational arithmetic, then merges fragments that touch across "phantom" walls (a fragment boundary lying on a face's infinite plane but OUTSIDE the actual bounded face polygon), and labels each resulting region by which cubes contain it.
- `CPP_SPEC.md` — states the region definition and the phantom-merge invariant.
- `cube_regions.cpp` — the fast C++ engine, for cross-checking counts only. DO NOT MODIFY IT.

Do not modify `certify_six.py` either — write a new module that imports it or copies the needed parts, so the validated engine stays untouched.

## What to build

`region_adjacency.py`, exposing a function that takes a list of exact rotations (same input as `exact_count_config`) and returns:

1. the region count and per-label counts (must agree with `exact_count_config`);
2. the **adjacency graph**: vertices are regions, and two regions are adjacent when their closures share a 2-dimensional piece of a REAL face (not a phantom extension);
3. an **adjacency profile**: a canonical, comparable invariant — a sorted multiset over edges of the pair (label_u, label_v) of containment bitmasks joined by that edge, together with the per-label region counts.

The information is already present in the pipeline: the phantom-merge pass decides, for each pair of touching fragments, whether the shared wall is phantom (merge — same region) or real (do not merge). The real-wall touches are exactly the adjacency edges. Record them instead of discarding them.

## The structural gate — this is the important one

Crossing a real face changes the containment set by **exactly one cube**: the cube that face belongs to. Therefore **every adjacency edge must join two labels whose bitmasks differ in exactly one bit.** Assert this for every edge. If any edge violates it, the phantom/real classification is wrong and the whole computation is invalid — report that rather than filtering the offending edges out.

## Other gates (pre-existing values, do not adjust them to match your output)

- n=2, quaternions `1,0,0,0` and `0,1,1,1`: 13 regions, per-depth {1:12, 2:1}. Report the adjacency graph in full for this case — it is small enough to inspect by hand, and it should show the depth-2 core adjacent to depth-1 regions, each edge changing exactly one containment bit.
- n=6, the record 727: `4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;7,14,1,-5` → 727 regions, by_depth {1:214, 2:220, 3:156, 4:100, 5:36, 6:1}. Your region count and per-label counts must match `./cube_regions_n` exactly.
- Euler-style sanity: report sum of degrees = 2 × edge count.

## Then apply it

Compute adjacency profiles for the 727-counting configurations recorded in `mixed_q2_hits.jsonl` (field `d`, quaternion components as `[p,q]` pairs meaning p+q√d — for these you will need the field arithmetic; if extending the Python engine to ℤ[√d] is impractical, say so and instead apply it to the RATIONAL 727 configurations, which are integer quaternions: `(7,14,1,-5)`, `(15,-12,-2,-13)`, `(3,-51,-93,29)`, `(9,77,-27,-47)`, `(17,-25,-1,11)`, `(92,-19,-80,-85)` appended to the five fixed cubes above).

Report how many distinct adjacency profiles occur, compared with how many distinct depth profiles and per-label vectors occur over the same set. The point of the exercise is to learn whether adjacency separates configurations that per-label cannot.

## Report back

The gate results with actual numbers, the n=2 adjacency graph in full, the comparison of the three invariants on the 727 set, and any case where the one-bit assertion failed. Runtime per configuration too — if it is far slower than `exact_count_config`'s ~13 s at n=6, say so.
```
