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
| Delegated | 2026-08-19T22:55:11 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_01LvHRp2Rjshoezr2nfKkzzU` |
| Files named | `arrangement.py`, `exactlp.py`, `isolation67.py` |
| Present in repo | `arrangement.py`, `exactlp.py`, `isolation67.py` |
| Cited in LEDGER/RESULTS | `arrangement.py`, `isolation67.py` |

## Prompt as sent

```text
Write `/Users/dmi/cube-compounds/exactlp.py`. Work in that directory. **Run the validation to completion in the FOREGROUND and report the numbers in your reply. Do not background the work and wait for a monitor — a status sentence is not a deliverable. Two previous attempts at this task were lost, so land the file and the numbers.**

# THE PROBLEM, and it is currently blocking two live campaigns

`isolation67.py`'s `_fm(rows, nv)` decides strict homogeneous feasibility exactly over ℚ: is there `y ∈ ℚ^nv` with `c·y > 0` for every row `c`? Returns a witness `y`, or `None` if infeasible. It is naive Fourier–Motzkin elimination.

It has a catastrophic tail. A live `py-spy` trace caught it seven levels deep in its own recursion after 9+ minutes on ONE candidate; 51 of 12 888 candidates (0.4%) cost ≥3 s each. FM blows up multiplicatively in both row count and coefficient bit-length across elimination steps. **Right now a running n=5 campaign is frozen at stage 14 with `tested` stuck at 10 057 and 9 173 candidates outstanding — one hard instance is holding up everything.**

Replace it with an exact rational method without that worst case: rational simplex phase-I, or exact pivoting feasibility (Bland's rule to guarantee termination). Same signature, same semantics, `fractions.Fraction` throughout, **no floating point anywhere**.

# INTERFACE

'''python
def feasible_strict(rows, nv):
    """Witness y with c·y > 0 for every row c (each row length nv), or None."""
'''
A drop-in replacement for `isolation67._fm`, HOMOGENEOUS and STRICT. Derive the right LP formulation yourself; decisions must match `_fm` exactly.

# VALIDATION — the point of the task

**1. Random instances, including many INFEASIBLE ones.** Thousands: nv 2..15, rows 1..40, varied coefficient magnitudes. A suite of only feasible systems cannot distinguish a correct routine from one that always finds something. Both routines must agree. Every witness yours returns must be verified directly: each `c·y > 0` exactly.

**2. The REAL decided candidates — the important test.** Live campaigns have checkpointed their decisions:
   - `/Users/dmi/cube-compounds/ckpt_727/worker_*.jsonl` — 214 729 records, static now
   - `/Users/dmi/cube-compounds/ckpt_393/worker_*.jsonl` — GROWING, a campaign is writing there
   - `/Users/dmi/cube-compounds/arrangement_ckpt_183/worker_*.jsonl` — ~12 900, static

**READ ONLY. Never write, truncate or delete in those directories.** Inspect the JSONL to learn the schema (`arrangement.py` wrote it — read `run_parallel` and the worker function). Reconstruct the systems and confirm your routine reproduces **every recorded decision**. Report how many checked, how many disagreed. **One disagreement is a failure — report it with the offending system in full.**

If the schema doesn't retain enough to reconstruct systems, say so plainly and fall back to regenerating from the same walls (`growth727.walls_of`), reporting exactly what you could and could not check.

**3. Speed — the TAIL is what matters.** Report median AND 99th-percentile ratios against `_fm`. The campaigns are governed by the slowest 0.4%; a routine 2× faster at the median and equally bad on the tail buys nothing. Deliberately construct hard instances and report your routine's behaviour on those specifically. If you can identify the instance currently blocking the n=5 run, time both routines on it and report.

# CONSTRAINTS

- Exact `Fraction` only. No floats, no tolerances, no `limit_denominator`.
- Create only `exactlp.py` and its outputs. Modify no existing file.
- Include a `__main__` guard — a script without one re-ran an entire campaign on import earlier in this project.
- This machine has 16 GB RAM and two campaigns are running. Keep your validation's memory modest and say what it peaked at.
- Module docstring must state why FM was replaced and the measured tail behaviour, so it isn't reintroduced.

Report back: agreement counts on random and on real checkpointed instances, any disagreement in full, median and 99th-percentile speed ratios, and peak memory.
```
