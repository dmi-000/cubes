# Certified proof of max(2)=13

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-21T00:39:20 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01NhTABKhSvPkqwFYMn3g7Ks` |
| Files named | `certify_six.py`, `cube_compound_interval.py`, `max2_report.md`, `max2_verify.py`, `opencount.py`, `six_cube_search_results.md` |
| Present in repo | `certify_six.py`, `cube_compound_interval.py`, `max2_report.md`, `max2_verify.py`, `opencount.py` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_compound_interval.py`, `max2_report.md`, `max2_verify.py`, `opencount.py` |

## Prompt as sent

```text
Execute /Users/dmi/carroll/MAX2_SPEC.md — the certified computer-assisted proof that two concentric unit cubes make at most 13 bounded regions (the project's first complete maximum theorem). Working directory /Users/dmi/carroll. Read the spec first, and READ PROOF_67.md §3 — the analytic argument you are completing. This is proof-grade: correctness and honest error bars dominate speed; a partial covering with a precisely-named uncertified region is a valid honest outcome, a false "proved" is not.

Orientation:
- The generic bound (d1 ≤ 12, hence ≤ 13) is ALREADY proved analytically off two codimension-≥1 degenerate loci: multi-face boundary kinks, and the shared-face-normal locus Σ = {R : some n_{1,a} = ±R·n_{2,b}}. Your job is ONLY to certify the bound on/near those loci, closing the theorem. Do not re-prove the generic case; certify the degeneracies.
- Config space is R ∈ SO(3) mod O_h×O_h — a compact 3-manifold; take an explicit fundamental domain. Prefer Strategy B (parametrize Σ as lower-dimensional families and certify #π₀(S_i) ≤ 6 on them + a rigorous neighborhood-inheritance/semicontinuity step) if you can make the inheritance airtight; else Strategy A (certified-interval box covering of the whole domain).
- REUSE machinery: cube_compound_interval.py's certified-numeric (CN) interval core for all box/gradient evaluations (outward rounding, no bare floats in any decision); certify_six.py per-label logic for exact spot counts; opencount.py (just built) for exact-sign arithmetic on algebraic-coordinate configs that arise on Σ. Exact zeros on Σ handled symbolically (rational/low-degree configs → exact), never by interval refinement alone.

Gates G1–G4 must pass: G1 interval #π₀(S_i) matches exact count on ~10^4 generic R (zero disagreements); G2 certify d1=12 at the maximizer (45° about a face axis) — the bound is attained, method must be tight there; G3 certify the shared-axis (common face-normal) config gives #π₀(S_i) ≤ 6; G4 the full fundamental domain covered with ZERO uncertified boxes (report box count, max subdivision depth near Σ, wall-clock). The theorem is proved only when G4 is clean.

≤4 cores, detached for the covering run, don't idle on monitors (background tasks + end turn; you'll be re-invoked on completion). Never edit six_cube_search_results.md or any validated/read-only file. Deliverables: max2_report.md (the certificate with the explicit statement of what was proved and the domain covered), max2_verify.py, and a machine-checkable covering log for independent re-run. Report honestly: if any box resists certification, name it precisely rather than declaring success.
```
