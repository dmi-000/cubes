# Delegation log

What was handed to subagents, what they were required to prove, what came back,
and what the main session re-verified independently.

**Why this file exists.** The specifications given to subagents are not stored
anywhere by default — not in the conversation exports (they are tool
parameters, not messages), not in the per-agent transcript files (metadata
only). They vanish with the session. But they contain the *gates*: the
pre-existing known values each agent had to reproduce. Those gates are the
whole reason a delegated result can be trusted, so they belong in the record
alongside the result.

**Standing rules applied to every delegation.** Agents never edit the ledger
`LEDGER.md` — the main session does. Agents do not modify
`cube_regions.cpp`. Gates must be *pre-existing* values from independent
sources, never self-consistency checks. An agent that cannot pass a gate must
say so rather than adjust the expected value. Every substantive claim is
re-verified by the main session before it enters the ledger.

---

## 2026-08-01 — Replace the engine's rectangular overflow guard

**Model:** Sonnet. **Target:** `cube_regions_q2.cpp`.

**Task.** The guard was a rectangle (d ≤ 100 AND |p|,|q| ≤ 512), but overflow
couples d and component magnitude. Re-derive the real admissible region,
implement it, verify at the corners of the NEW region, re-run all existing
gates.

**Key instruction, and the reason it mattered:** *"If the true invariant is not
exactly m²·d, report what it is; do not force it to match my guess."* The main
session's hypothesis was d·m² ≤ 26214400.

**Gates required:** `--d 0` bit-for-bit against `cube_regions_n` on 727 and
183; ℚ(√5) golden triple = 67 {1:48,2:18,3:1}; the ℚ(√13) configuration = 727
{214,216,162,98,36,1}; `--selftest`; plus corner verification by an
independent route, with *"it did not crash is not verification"* stated
explicitly.

**Outcome — the hypothesis was wrong and the agent said so.** Tracing |p| and
|q| separately, the boundary's m²·d is not constant: ~9.0e6 at d=1, ~2.53e7 at
d=29, plateauing near 2.9–3.0e7 for large d. The flat rule would have been
**over-permissive below d ≈ 38** (at d=5 admitting m=2289 against a true limit
of 1855 — an exploitable overflow). It implemented the traced bound at runtime
instead. It also caught that d=100, cited as a verified corner in the old
header, is not squarefree and was never an acceptable input.

**Main session re-verified:** semantic `--d 0` agreement on 727 and 183;
ℚ(√13) still 727; scaling invariance in the newly-admitted region (same
rotation at 12×, 25×, 25× components for d=8761, 465, 115 — counts identical);
boundary rejects at d=465 m=254, accepts m=253.

---

## 2026-07-31 — Build a ℚ(√d) C++ counting engine

**Model:** Sonnet. **Produced:** `cube_regions_q2.cpp`.

**Task.** Generalise the integer engine's scalar type to ℤ[√d] with d given at
runtime, leaving geometry and topology untouched.

**Gates required (all pre-existing project values):** `--d 0` reproducing
`cube_regions.cpp` exactly on 727, 183, and the axial self-test; ℚ(√5) golden
triple 67, 4-compound 177, 5-compound 351; ℚ(√2) octahedral triple 67; ℚ(√6)
ψ=45° dihedral point 49. Overflow analysis required, not optional, with the
note that *silent truncation is the specific failure mode `CPP_SPEC.md` warns
about, and it produces plausible wrong answers.*

**Outcome.** All gates passed; ~100× faster than the Python algebraic path. The
agent had to reconstruct ℤ[√d] quaternions itself, since the Python sources
parameterise by matrices — the naive frame gives nested radicals
√(7/16 + 3√5/16), so it searched the cube's 24 relabelings for a
representative lying in the field. It also corrected a figure the main session
had asserted: `cube_compound_exact` caps at N=5, so the quoted "~20 s at n=6"
was an extrapolation, not a measurement.

**Main session re-verified:** `--d 0` bit-for-bit including `per_label`; the
field path on a purely rational config returning 727; and the golden triple on
quaternions the main session derived **independently** from
`cube_compound_exact`'s own axes.

---

## 2026-07-30 and 07-31 — Documentation propagation (four delegations)

**Model:** Sonnet each. **Targets:** `README.md`, `PROJECT.md`, `JOURNEY.md`,
`PROOF_67.md`, `n7_program_report.md`, `BLUEPRINT_SPEC.md`, `CPP_SPEC.md`.

**Tasks, in order:** (1) propagate the max(2)=13 continuum correction and the
n=3 non-congruence wording; (2) propagate records n=7 = 1211, n=8 = 1889;
(3) supersede those with 727 / 1217 / 1891 the same day; (4) add Postscript 47
(727's structure and the elimination), and later Postscripts 48–51.

**Standing instruction across all four:** update live "current record" claims,
but *annotate rather than rewrite* dated or historical passages — a report of a
completed run stays as-run, with a forward pointer. This keeps the documents
readable as history while preventing a reader from picking up a stale claim.

**Notable agent catches.** The third delegation flagged that a ledger
cross-reference pointed at "Postscript 48" before that postscript existed — a
dangling forward reference the main session had created and had to resolve by
writing it. The first determined that `cubes/` was a live mirror while `cb/`
was a frozen July-10 snapshot, and correctly left the latter alone.

**Main session re-verified:** spot-checked each edit, and corrected one scope
call — an agent left `JOURNEY.md`'s open-question list reading "Beat 723" after
723 had fallen, on the grounds that updating it was out of scope. It was a
defensible reading of the instruction, but a stale open-questions list is
exactly what misleads a later reader, so the main session fixed it.

---

## 2026-08-02 — The repaired increment bound

**Model:** Sonnet. **Target:** new `increment_bound2.py`. **Spec:**
`INCREMENT_BOUND_SPEC.md` (written by the main session, in the repo).

**Task.** Implement the bound B_j = 1 + c + SUM_v (deg(v)/2 - 1) on the cell
count of the plane arrangement cut on dC_j, which links (V) of the chain
Delta_j = N - #comps(G_j) <= |E(G_j)| <= W_j <= K_j <= B_j.

**Key instruction, and why it mattered:** G1 is a hand-computed case — the n=2
13-pair, where the main session derived B = 12 = Delta by hand from eight
named tangency points. *"If your code does not reproduce it, do not adjust the
gate or the expected value to match your code."* The earlier failed attempt
(Postscript 53) went wrong precisely there, by testing whether a line met the
OPEN interior of the cube and so scoring twelve tangential vertices as zero.

**Gates required:** G1 the hand-computed n=2 case (B = 12, c = 1, two degree-6
and six degree-4 vertices at named points); G2 all 21 (config, j) rows of the
old `increment_bound.py` with B_j >= Delta_j required and refutation explicitly
welcomed; G3 reduction to the old 2+V formula on generic inputs; G4 an exact
self-check on every emitted vertex.

**Main session did independently:** derived the theorem and the failure
diagnosis; verified identity (I) in `increment_identity.py` against the
counting engine on 9 (config, j) rows by a genuinely different route (adjacency
graph of the full compound vs re-counting the subset).

---

## 2026-08-02 — A 256-bit ℤ[√d] engine

**Model:** Sonnet. **Target:** new `cube_regions_q2w.cpp`. **Spec:**
`WIDE_ENGINE_SPEC.md`.

**Task.** Widen the validated ℚ(√d) engine's scalar from __int128 to a signed
256-bit type so the 284 634 mixed-strata configurations rejected by the
2^112 chain budget can be counted; retrace the budget to 2^240 / 2^496 with
the same headroom style; 512-bit sign predicate.

**Recorded in the spec, not left implicit:** a continued-fraction sign test
would NOT widen the admissible region, because the engine's own header
establishes that the i128 chain bound always binds before the sign bound.
Widening the scalar is the only thing that helps.

**Gates required:** G1 equivalence — 3000+ in-budget configs across six or
more d, identical `bounded` and `by_depth` from both engines, one mismatch
being a refutation to report rather than tune around; G2 rational
specialisation against `cube_regions_n` on 727 / 393 / 183 / 13; G3 a config
rejected by the narrow engine and counted by the wide one; G4 randomised
arithmetic selftest against __int128; G5 timing ratio.

---

## Outcomes of the 2026-08-02 delegations

**Increment bound (Sonnet).** Clean pass, first try, ~1.4 s runtime. G1
reproduced the hand-computed n=2 case exactly, including the eight named
vertices by set equality rather than by count. G2 came back with all 21 rows
satisfying the bound. The agent also tightened G3's definition on its own —
"generic" had to exclude line-tangency and disconnected traces, and in both
cases the discrepancy was the new code being right and the old formula wrong,
which it reported rather than smoothing over. Main session re-verified on
n=2 / n=3 / n=4 by the independent adjacency route.

**Wide engine (Sonnet).** The C++ was correct — 1365-configuration
equivalence, 0 mismatches — but the agent hit the project's known *premature
parking* failure mode twice: it built the engine, then stopped to wait on its
own monitor job instead of running the gates, twice in a row, at a cost of
about 205 000 tokens. The main session took the gating over and finished G1,
G2, G3, G5 by hand in a few minutes.

The fix is the one already in the standing rules and was simply not applied
here: **a long computation must be a single detached self-sequencing script,
with the agent collecting results afterwards** — never an agent watching a
job. The campaign that followed (`wide_campaign_launch.sh`) is written that
way: it waits for the enumeration, checks the pickle is real, fans out eight
shards, and exits.

And a main-session error worth logging next to the agent's: the first
equivalence gate the main session wrote passed VACUOUSLY on all 1365 rows,
because a separator bug made every input fail to parse and the two engines
returned identical error lines. Delegation is not the only place a gate can be
about nothing.

---

## What delegation was and was not used for

**Delegated:** mechanical propagation across many documents; a well-specified
C++ implementation with externally-checkable gates; a bounded numerical
derivation with a stated hypothesis the agent was explicitly licensed to
refute.

**Not delegated:** anything entering the ledger; the mathematical judgment
about which strata to enumerate; verification of any headline number. The two
occasions an agent contradicted the main session's stated expectation — the
d·m² invariant, and the Python timing figure — both turned out in the agent's
favour, which is an argument for stating hypotheses explicitly in the spec and
inviting refutation rather than asking for confirmation.
