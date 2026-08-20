# `exactlp.py` — exact rational feasibility, replacing `isolation67._fm`

> **Status.** Written 2026-08-20, **after** the module was delivered. It is
> therefore a contract for FUTURE changes, not a certificate of the delivered
> version: nothing was diffed against this text at build time because this text
> did not exist then. The three prompts actually sent are recovered verbatim in
> `backfill/20260819-1752-*.md`, `backfill/20260819-1810-*.md` and
> `backfill/20260819-2255-*.md` — they differ (4 046 / 3 789 / 4 070 characters),
> and which one the surviving code was built to is not recorded anywhere. That
> gap is [FAILURE_MODES 19](../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept);
> this file is the practice resuming.

## Why this module exists

`isolation67._fm` decides strict feasibility by Fourier–Motzkin elimination.
FM is not merely slow here — it is the cause of all three observed failure
symptoms, which had been attributed to three different things before being
traced to one:

- **Schedule.** Campaigns sized in hours ran in days.
- **Stalls.** A single hard instance freezes an entire stage; `run393` sat at
  stage 14 with `tested` frozen and 9 173 candidates outstanding.
- **Memory.** Measured 2026-08-20: FM's tail peaked at **7 449 MB**, and four
  workers holding such instances exhausted the machine and froze the terminal.
  This corrected P144, which had attributed the memory growth to the chamber
  list.

## Interface

`feasible_strict(rows, nv) -> witness | None`

Returns a witness point strictly satisfying all rows, or `None` if none exists.
Exact rational arithmetic throughout. **RATIONAL COEFFICIENTS ONLY** — `Fraction(...)` conversion means this cannot accept ℚ(√d) elements, which Fourier–Motzkin handles unchanged; `isolation67._fm` dispatches on coefficient type and falls back. See [P147 Addendum 1](../LEDGER.md). The 237 668 validated instances are all rational, so no gate here covers the irrational records. **No floating point may decide anything** —
the project-wide rule, non-negotiable, and the reason a simplex implementation
was written rather than a library called.

## Gates

Each gate names a *pre-existing* value from an independent source. Values below
are what the delivered module achieved on 2026-08-20 and become the regression
baseline.

| Gate | Requirement | Achieved |
|---|---|---|
| `ckpt183` | Agree with `_fm` on every decided candidate of the known-answer case | 12 882 / 12 882, **0** disagreements |
| `ckpt393` | Agree on every decided candidate | 10 057 / 10 057, **0** |
| `ckpt727` | Agree on every decided candidate | 214 729 / 214 729, **0** |
| Witness validity | Every returned witness verified to satisfy all rows strictly, by substitution, in exact arithmetic | 0 bad witnesses |
| Memory | Peak RSS bounded well below FM's tail | ≤ 70 MB across all phases, vs FM 7 449 MB |

**237 668 real decided instances, zero disagreements.** These are the load-bearing
gates: they are the actual workload and require no sampling distribution.

## `phase_random` is not a workload model

It samples synthetic instances and is a broad agreement check only. Two
constraints on how its numbers may be used:

1. **The denominator is `n_compared`, never `n_trials`.** A timed-out `_fm` call
   returns no verdict, so that trial yields no comparison. On 2026-08-20, 978 of
   2 500 trials timed out at `fm_timeout=0.3 s`; the honest statement is *0
   mismatches in 1 522 comparisons*. The agent's own summary said "2500/2500",
   which credited 978 non-comparisons to agreement.
2. **No speed claim rests on it.** Its distribution is deliberately weighted
   toward instances `_fm` can finish, purely so a thousands-of-trials sweep is
   tractable. That excludes exactly the tail this module exists for. Speed
   claims come from `phase_hard` and the `ckpt*` phases.

Both the weighting and the timeout are run-time parameters (`SAMPLING_DEFAULT`,
`key=value` overrides) and are echoed into the report, so no report is silent
about the distribution that produced it.

## Requirements on any future change

- Output path stays a parameter; exploratory runs pass `out=`
  ([FAILURE_MODES 20](../FAILURE_MODES.md#20-a-test-run-writing-to-the-production-output-path)).
- The `_Timeout` race — alarm firing after `fn` returns but before the disarm —
  must remain caught such that it can only ever be scored as a timeout, never as
  a false SUCCESS.
- `ckpt_727/` and `ckpt_393/` are live campaign directories: **read only**.
- Re-run all five gates before the module is trusted on new data.

## Gate-vacuity check

Per [mode 2](../FAILURE_MODES.md#2-a-gate-that-cannot-fail), for each gate, the
input that makes it FAIL: return a witness violating any row (witness validity);
flip any single decision on any checkpointed candidate (the three `ckpt` gates);
allocate per-candidate state proportional to the elimination tree (memory). None
of these gates passes vacuously — each was checked against instances whose
answers were computed by a different method before this module existed.
