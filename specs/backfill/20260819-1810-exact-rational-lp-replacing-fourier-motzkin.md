# Exact rational LP replacing Fourier-Motzkin

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-19T18:10:51 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_0157z2Y35rHyV6SBwXYswFhL` |
| Files named | `arrangement.py`, `exactlp.py`, `isolation67.py` |
| Present in repo | `arrangement.py`, `exactlp.py`, `isolation67.py` |
| Cited in LEDGER/RESULTS | `arrangement.py`, `isolation67.py` |

## Prompt as sent

```text
Write `/Users/dmi/cube-compounds/exactlp.py`. Work in that directory. **Run the validation to completion in the FOREGROUND and report the numbers in your reply. Do not background the work and wait for a monitor — a status sentence is not a deliverable.**

# THE PROBLEM

`isolation67.py`'s `_fm(rows, nv)` decides strict homogeneous feasibility exactly over ℚ: is there `y ∈ ℚ^nv` with `c·y > 0` for every row `c`? It returns a witness `y`, or `None` if infeasible. It is naive Fourier–Motzkin elimination.

**It governs the schedule of a multi-day campaign now running.** A live `py-spy` trace caught it seven levels deep in its own recursion after 9+ minutes on a SINGLE candidate; 51 of 12 888 candidates (0.4%) cost ≥3 s each. FM blows up multiplicatively in both row count and coefficient bit-length across elimination steps, so the tail dominates everything.

Replace it with an exact rational method without that worst case — rational simplex phase-I, or exact pivoting feasibility. Same signature, same semantics, `fractions.Fraction` throughout, **no floating point anywhere**.

# INTERFACE

'''python
def feasible_strict(rows, nv):
    """Witness y with c·y > 0 for every row c (each row length nv), or None."""
'''
A drop-in replacement for `isolation67._fm`. It is HOMOGENEOUS and STRICT — derive the correct LP formulation yourself, but the decisions must match `_fm` exactly.

# VALIDATION — the point of the task

**1. Agreement on random instances.** Thousands of random rational systems: nv from 2 to 15, rows from 1 to 40, coefficient magnitudes varied. **Include many INFEASIBLE systems** — a suite of only feasible ones proves nothing. Both routines must agree on feasible/infeasible. Whenever yours returns a witness, verify it directly: every `c·y` must be exactly `> 0`.

**2. Agreement on REAL decided candidates — the important one.** Two campaigns have checkpointed their decisions:
   - `/Users/dmi/cube-compounds/ckpt_727/worker_*.jsonl` — **214 000+ records and GROWING; a campaign is actively writing there, so READ ONLY, never write or truncate**
   - `/Users/dmi/cube-compounds/arrangement_ckpt_183/worker_*.jsonl` — ~12 900 records, static

Inspect the JSONL to learn the schema; `arrangement.py` wrote it (read `run_parallel` and the worker function). Reconstruct the systems and confirm your routine reproduces **every recorded decision**. Report how many were checked and how many disagreed. **One disagreement is a failure — report it with the offending system in full, do not average it away.**

If the schema does not retain enough to reconstruct the systems, say so plainly and fall back to regenerating them from the same walls (`growth727.walls_of`), reporting exactly what you could and could not check.

**3. Speed, measured — and the TAIL is what matters.** Time both routines on the same instances. Report median AND 99th-percentile ratios. The campaign is dominated by the slowest 0.4%, so a routine 2× faster at the median and equally bad on the tail buys nothing. Construct hard instances deliberately — take the slowest candidates you can identify — and report how yours does on those specifically.

# CONSTRAINTS

- Exact `Fraction` arithmetic only. No floats, no tolerances, no `limit_denominator`.
- Create only `exactlp.py` and its outputs. Do not modify any existing file.
- **`ckpt_727/` is being written by a live campaign: read only.**
- Include a `__main__` guard — a script without one re-ran an entire campaign on import earlier in this project.
- Module docstring must state why FM was replaced and what the measured tail behaviour is, so the next reader doesn't reintroduce it.

Report back: agreement counts on random and on real checkpointed instances, any disagreement in full, and median plus 99th-percentile speed ratios.
```
