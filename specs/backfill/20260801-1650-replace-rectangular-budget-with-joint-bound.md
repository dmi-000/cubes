# Replace rectangular budget with joint bound

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-01T16:50:01 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01QE2AMC6pJnfP92NTLymbrD` |
| Files named | `cube_regions.cpp`, `cube_regions_q2.cpp` |
| Present in repo | `cube_regions.cpp`, `cube_regions_q2.cpp` |
| Cited in LEDGER/RESULTS | `cube_regions.cpp`, `cube_regions_q2.cpp` |

## Prompt as sent

```text
Focused change to /Users/dmi/carroll/cube_regions_q2.cpp (the Z[sqrt d] exact region counter you can read; it was built earlier and all its gates pass).

## The problem

Its input guard is a RECTANGLE: `d <= 100` AND `|p|,|q| <= 512` per quaternion component. But the real overflow constraint couples d and the component magnitude m. Growth through the pipeline is dominated by det3, whose entries are products of three rotation-matrix numerators, each of size ~m^2*(1+d); so the final predicate magnitude grows like (m^2 * d)^3, i.e. the invariant that matters is **m^2 * d**, not m and d separately.

This matters concretely. A measurement of the configurations we need to count found classes with large d but very small components — Q(sqrt115) with max component 3, Q(sqrt217) with 6, Q(sqrt145) with 7, Q(sqrt465) and Q(sqrt481) with 9, even Q(sqrt8761) with 36. The current guard rejects all of them despite their being arithmetically tiny. Under a joint budget at the same corner as the present rectangle (d * m^2 <= 100 * 512^2 = 26214400), about 343000 currently-unreachable configurations become admissible.

## What to do

1. **Re-derive the bound rigorously.** Trace the worst-case growth of |p| and |q| through the actual pipeline in this file — quaternion -> rotation-matrix numerator -> plane coefficient -> det3 minor -> vertex homogeneous coordinate -> side-of-plane predicate -> the squaring inside FieldElem::sign()'s mixed-sign branch. Determine the exact admissible region. If the true invariant is not exactly m^2*d, report what it is; do not force it to match my guess.

2. **Replace `validateBudget`** with the joint test, keeping the same safety margin the current rectangle has (the existing derivation left ~15 bits of headroom at its corner; preserve at least that). Keep the squarefree requirement on d. Reject with a clear error naming the actual constraint, as now.

3. **Verify empirically at the corners of the NEW region**, not just the old one. At minimum: (d=8761, m=36), (d=465, m=200), (d=115, m=400), (d=26214400/(512*512) rounded appropriately, m=512), and a case just outside the boundary to confirm it is rejected. For each, confirm the computed counts are correct by an independent route — the cleanest is to construct a configuration whose exact answer is already known, or to verify that the same configuration expressed in two different admissible ways agrees. Explain what you did; "it did not crash" is not verification.

4. **Re-run the existing gates** to confirm nothing regressed: `--d 0` must still reproduce `./cube_regions_n` bit-for-bit on `4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;7,14,1,-5` (727) and on `1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4` (183); the Q(sqrt5) golden triple must still give 67 = {1:48,2:18,3:1}; the Q(sqrt13) configuration `1:0,1:-1,16:-4,11:-3` appended to the five fixed cubes `4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1` (all with zero sqrt-parts) must still give 727 = {1:214,2:216,3:162,4:98,5:36,6:1}.

5. Update the file-header comment to state the new bound and its derivation.

Do not change the geometry, the topology, or the region-counting semantics — only the arithmetic budget and its guard. Do not modify `cube_regions.cpp`.

## Report back

The derivation (showing the growth exponents you found), the new guard expression, the corner verifications with what you actually checked, and the gate results. If the true admissible region is smaller than d*m^2 <= 26214400, say so plainly and give the correct one — an over-permissive guard silently produces wrong counts, which is the worst outcome here.
```
