# Off-center (translation) counter prototype

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-12T14:50:34 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_0169fBKsFBtyZiYcEP9VFuuP` |
| Files named | `certify_six.py`, `cube_compound_exact.py`, `cube_compound_regions.py`, `cube_regions.cpp`, `offcenter_count.py`, `offcenter_report.md`, `six_cube_search_results.md` |
| Present in repo | `certify_six.py`, `cube_compound_exact.py`, `cube_compound_regions.py`, `cube_regions.cpp`, `offcenter_count.py`, `offcenter_report.md` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_compound_exact.py`, `cube_compound_regions.py`, `cube_regions.cpp`, `offcenter_count.py` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. Exact cube-compound region-counting project. Read first: PROJECT.md (self-contained overview), certify_six.py (the Python exact counter `exact_count_config` — study how it builds planes and counts, but do NOT modify it), README.md.

GOAL: prototype a NON-CONCENTRIC (translation-capable) exact region counter and use it to test whether moving cubes off-center can increase the region count of the record 723.

THE MATH: currently cube k = R_k·([-1,1]³) centred at origin; its 6 face planes are n·x = ±1 where n runs over the columns of R_k. For a cube TRANSLATED by vector t_k, the cube is R_k([-1,1]³) + t_k, so its face planes become n·x = ±1 + n·t_k (n = R_k column). The face SQUARE also shifts: a point on the plane is a real face (not phantom) iff it lies within the translated square face, i.e. its offset from the cube CENTRE t_k projects within [-1,1] on the other two axes. Everything stays rational when R_k (integer quaternion) and t_k are rational. So the ONLY changes vs the concentric counter are: (a) plane offsets ±1 → ±1 + n·t_k, and (b) the inside-face-square test is relative to the cube's centre t_k, and (c) the depth/containment test (a point is inside cube k iff |n·(x−t_k)| < 1 for all three columns n).

BUILD offcenter_count.py: a fresh exact counter (rational arithmetic, Fraction; you may adapt the plane-arrangement + phantom-facet-merge + depth-label logic from certify_six.py / cube_compound_regions.py into the new file, but keep the file self-contained and do NOT edit the originals). Input: list of (integer quaternion, rational translation vector) per cube.

HARD GATE (do first, do not skip): with all t_k = 0 it MUST reproduce the concentric counts exactly. Verify against ./cube_regions on several configs INCLUDING the 723 record (quats 4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;5,2,2,2 must give 723 with by_depth {1:210,2:216,3:164,4:96,5:36,6:1}) and 2-3 random seeds. If t=0 does not reproduce cube_regions exactly, the counter is wrong — debug, do not proceed to the experiment.

THEN THE EXPERIMENT: perturb 723 off-center. Translate cubes by small rational vectors (e.g. components in {-1/2,-1/4,-1/8,0,1/8,1/4,1/2}): try (i) translating one cube at a time along each axis, (ii) a few random small translation sets, (iii) translating along the shared (1,1,1) axis (the record's symmetry axis). For each, count exactly and record total + by_depth. Report: does off-centering 723 ever INCREASE the total above 723? What happens to the depth profile — do the deep layers (d3,d4,d5) drop as predicted (the common-intersection core weakens) while shallow layers change? Give the best off-center total found and its translations.

HARD RULES: exact arithmetic only in predicates; do NOT modify validated files (certify_six.py, cube_compound_regions.py, cube_compound_exact.py, cube_regions.cpp, etc.) or six_cube_search_results.md; exact_search_results.jsonl read-only; run detached, write the report at the end. Deliverables: offcenter_count.py, offcenter_report.md. Final message: did the t=0 gate pass; does off-centering 723 increase the total (yes/no + best off-center total); and what the depth profile does under translation.
```
