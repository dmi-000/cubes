# Exact rational LP to replace Fourier-Motzkin

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-19T17:52:20 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_01S5b9NJpioE7mgJWtTASnGS` |
| Files named | `arrangement.py`, `exactlp.py`, `isolation67.py` |
| Present in repo | `arrangement.py`, `exactlp.py`, `isolation67.py` |
| Cited in LEDGER/RESULTS | `arrangement.py`, `isolation67.py` |

## Prompt as sent

```text
Write `/Users/dmi/cube-compounds/exactlp.py`. Work in that directory. **Run the validation to completion in the foreground and report the numbers. Do not background the work and wait for a monitor.**

# THE PROBLEM

`isolation67.py`'s `_fm(rows, nv)` decides strict homogeneous feasibility exactly over ℚ: is there `y ∈ ℚ^nv` with `c·y > 0` for every row `c`? It returns a witness `y` or `None`. It is implemented by naive Fourier–Motzkin elimination.

**It is the dominant cost of a running multi-day campaign.** A live `py-spy` trace caught it seven levels deep in its own recursion after 9+ minutes on a SINGLE candidate; 51 of 12 888 candidates (0.4%) cost ≥3 s each. FM blows up multiplicatively in both row count and coefficient bit-length across elimination steps.

Replace it with an exact rational method without that worst case — a rational simplex phase-I, or exact Gaussian/pivoting feasibility. Same signature, same semantics, exact arithmetic only (`fractions.Fraction`), **no floating point anywhere**.

# REQUIRED INTERFACE

'''python
def feasible_strict(rows, nv):
    """Witness y with c·y > 0 for every row c (each row has length nv), or None."""
'''
It must be a drop-in replacement for `isolation67._fm`. Note `_fm` is homogeneous and STRICT: the all-zeros vector never counts, and the system `{c·y > 0}` is feasible iff the origin is not in the convex hull of the rows... derive the right formulation yourself, but the semantics must match `_fm` exactly.

# VALIDATION — THIS IS THE POINT OF THE TASK

**1. Agreement with `_fm` on random instances.** Generate thousands of random rational systems across a range of sizes (nv from 2 to 15, rows from 1 to 40, coefficients of varied magnitude, including many INFEASIBLE ones — a test set of only feasible systems proves nothing). For each, both must agree on feasible/infeasible. When your routine returns a witness, **verify it directly**: every `c·y` must be `> 0` exactly.

**2. Agreement on the REAL decided candidates — the important one.** A running campaign has checkpointed ~146 000 already-decided candidates at `/Users/dmi/cube-compounds/ckpt_727/worker_*.jsonl`, and ~12 900 more at `/Users/dmi/cube-compounds/arrangement_ckpt_183/worker_*.jsonl`. Read them, reconstruct the systems they represent (inspect the JSONL to learn the schema; `arrangement.py` wrote it — read `run_parallel` and the worker function to see exactly what a record contains), and confirm your routine reproduces **every recorded decision**. Report the number checked and the number of disagreements. **A single disagreement is a failure — report it with the offending system, do not average it away.**

If the checkpoint schema does not retain enough to reconstruct the system, say so plainly and fall back to validating on systems you regenerate from the same walls (`growth727.walls_of`), reporting what you could and could not check.

**3. Speed, measured not asserted.** Time both routines on the same instances. Report the median and the 99th-percentile ratio. The 99th percentile matters more than the median: the campaign is dominated by the 0.4% of hard candidates, so a routine that is 2× faster typically but equally bad on the tail buys nothing. **Explicitly report how your routine does on the hardest instances you can find** — construct some by taking the slowest candidates from the checkpoints if the schema allows.

# CONSTRAINTS

- Exact `Fraction` arithmetic only. No floats, no tolerances, no `limit_denominator`.
- Do not modify any existing file. Create only `exactlp.py` and its outputs.
- Do not touch `ckpt_727/` — a campaign is actively writing there. Read only.
- Include a `__main__` guard. (A script without one re-ran an entire campaign on import earlier in this project.)
- The module docstring must state why FM was replaced and what the measured tail behaviour is, so the next reader does not reintroduce it.

Report back: agreement counts on random and on real checkpointed instances, any disagreements in full, and median plus 99th-percentile speed ratios.
```
