# Build Q(sqrt d) C++ counting engine

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-31T17:18:11 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01QYLGoFqbUwHoCjF7q2ue37` |
| Files named | `cube_compound_exact.py`, `cube_regions.cpp`, `cube_regions_q2.cpp`, `q6_count.py`, `slide3_q2.py` |
| Present in repo | `cube_compound_exact.py`, `cube_regions.cpp`, `cube_regions_q2.cpp`, `q6_count.py`, `slide3_q2.py` |
| Cited in LEDGER/RESULTS | `cube_compound_exact.py`, `cube_regions.cpp`, `cube_regions_q2.cpp`, `q6_count.py`, `slide3_q2.py` |

## Prompt as sent

```text
Engineering task in /Users/dmi/carroll: build a C++ exact region counter for cube compounds whose rotations have coordinates in a real quadratic field Q(sqrt d), by generalising the existing integer engine's scalar type.

## Context you must read first

- `cube_regions.cpp` (774 lines) — the existing exact integer engine. Its geometry/topology is correct and validated; DO NOT MODIFY IT. You are writing a new file.
- `CPP_SPEC.md` — the design invariants it must preserve.
- `cube_compound_exact.py` — the Python Q(sqrt5) counter, including the `Q5` field class and the exact golden-compound rotations.
- `slide3_q2.py` — the Q(sqrt2) counterpart, with the exact octahedral configuration.
- `q6_count.py` — a Q(sqrt6) counter used for a dihedral-family point.

The single most important domain invariant, stated in CPP_SPEC.md and the ledger: a REGION is a connected component of constant cube-CONTAINMENT, separated by real finite FACES — not a cell of the infinite face-plane arrangement. The existing engine implements this ("phantom-facet merge"). Preserve that exactly; a counter that splits regions at a face's invisible extension produces inflated counts and has already caused one full retraction in this project's history.

## What to build

`cube_regions_q2.cpp`, a copy of the existing engine with its scalar type abstracted from `__int128` to elements of Z[sqrt d]:

    element = p + q*sqrt(d),  p,q integers,  d a squarefree positive integer given at runtime

Required operations: add, subtract, multiply, negate, compare-to-zero (sign), and equality. Sign is the delicate one: sign(p + q*sqrt d) when p and q have opposite signs requires comparing p^2 against q^2*d, which needs wider-than-128-bit intermediates. Implement that comparison exactly — either with a small 256-bit multiply/compare helper or by a carefully justified reduction — and document the approach in a comment.

Interface: extend the existing CLI. Add `--d D` (default 0, meaning the pure-integer path) and accept quaternion components as `p+q` pairs in a documented syntax of your choosing (e.g. `--quats 'p:q,p:q,p:q,p:q;...'`), keeping the existing integer syntax working unchanged when `--d 0`. Support a stdin streaming mode like the current `--quats-stdin`, because the eventual use is counting hundreds of thousands of configurations.

## Gates — the task is not done until all of these pass

These exact values are established in the project and are the correctness criteria. Extract the exact configurations from the Python sources named above; do not invent coordinates.

1. `--d 0` must reproduce the integer engine EXACTLY on several configurations. Verify against `./cube_regions_n` on at least: the n=6 record `4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;7,14,1,-5` (expect 727, by_depth {1:214,2:220,3:156,4:100,5:36,6:1}), the n=4 record `1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4` (expect 183), and the axial self-test the existing binary already runs.
2. Q(sqrt5), golden compounds (from `cube_compound_exact.py`): the golden triple must give **67** with by_depth {1:48, 2:18, 3:1}; the golden 4-compound **177**; the golden 5-compound **351**.
3. Q(sqrt2), octahedral triple (from `slide3_q2.py`): **67**, by_depth {1:48, 2:18, 3:1}.
4. Q(sqrt6), the psi=45-degree dihedral point (from `q6_count.py`): **49**, by_depth {1:30, 2:18, 3:1}.

Report each gate as pass/fail with the actual numbers. If a gate fails, say so plainly and diagnose it — do not adjust the expected value to match your output.

## Overflow analysis (required, not optional)

The existing engine documents an int128 budget with |quaternion component| <= 512. Products in Z[sqrt d] grow faster than in Z. Derive the corresponding bound for your implementation, state it in a comment at the top of the file, and add a runtime check that rejects inputs exceeding it rather than silently overflowing. Silent truncation is the specific failure mode CPP_SPEC.md warns about, and it produces plausible wrong answers.

## Benchmark

Report timing at n=6 for a Q(sqrt5) configuration against the Python `cube_compound_exact` path (which takes roughly 20 s at n=6, 2.7 s at n=4, 1.1 s at n=3). State the measured speedup.

## Build

`clang++ -O2 -std=c++17 -Wall -o cube_regions_q2 cube_regions_q2.cpp` must compile clean. Do not add dependencies — no GMP, no boost; the project's engines are dependency-free by design.

## Report back

The gate table with actual versus expected numbers, the overflow bound you derived and how, the benchmark, and anything you could not get working. Do not claim a gate passes without having run it.
```
