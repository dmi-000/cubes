# Output-sensitive face enumerator

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-19T15:08:40 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_0122Dork8MKzVL1jxWjo2Y19` |
| Files named | `arrangement.py`, `isolation67.py`, `onewall183.py` |
| Present in repo | `arrangement.py`, `isolation67.py`, `onewall183.py` |
| Cited in LEDGER/RESULTS | `arrangement.py`, `isolation67.py` |

## Prompt as sent

```text
Write `/Users/dmi/cube-compounds/arrangement.py`. Work in that directory. **Run it to completion in the foreground on the validation case and report the numbers. Do not background the work and wait for a monitor.**

# WHAT IS WRONG WITH THE CURRENT CODE

`isolation67.py`'s `faces()` enumerates faces of a central hyperplane arrangement by walking the 3^m sign-vector tree with prefix pruning. That is exponential in the NUMBER OF WALLS regardless of how many faces exist. On the 183 record (12 walls, rank 8, ambient 9) it ran **3 hours without finishing**, when the arrangement provably has **at most 3 632 chambers** (Zaslavsky/Buck bound: 2·Σ_{k<r} C(m−1,k)).

Replace it with an **output-sensitive** enumerator: cost polynomial in the number of faces actually produced, not in 3^m.

# THE ALGORITHM: INCREMENTAL CONSTRUCTION

Maintain a list of chambers as sign vectors. Start with the empty arrangement (one chamber). Add hyperplanes one at a time; for each existing chamber C and new hyperplane h, decide by exact LP whether C ∩ {h>0} and C ∩ {h<0} are both non-empty:
- both non-empty → C splits into two
- only one → C survives with that sign

Feasibility must be **exact over ℚ** — use the strict Fourier–Motzkin routine `_fm` already in `isolation67.py` (import it; do not rewrite), or exact rational Gaussian elimination. **No floating point anywhere.**

Also expose lower-dimensional faces: a face is a sign vector in {−1,0,+1}^m: for each chamber, its subfaces come from setting subsets of signs to 0 and testing feasibility. Provide `chambers(walls, ncols)` and `faces(walls, ncols, max_codim=None)`; `max_codim` bounds the work when only near-full-dimensional faces are wanted.

# ARCHITECTURE — THIS IS THE PART THAT MATTERS

**1. Common work queue, NOT static assignment.** A previous campaign pre-assigned configurations to 4 shards; two finished in 30 minutes and two ran 10+ hours, with completed workers idle while work sat blocked behind a slow shard. Workers must PULL from a shared queue so a slow item never blocks others.

Implement with `multiprocessing` using a **fork** context (`mp.get_context('fork')`) — spawn re-imports `__main__` and recursively re-runs any caller lacking a `__main__` guard; that bug already cost this project a run. Workers pull work items and push results.

**2. Checkpointing such that nothing runs hours without output.** Requirements:
   - each worker appends its results to its OWN `.jsonl` (one JSON object per line, flushed immediately) — no shared-file write contention, and a kill loses at most the in-flight item
   - a progress line to the log at least every 30 seconds AND every N items, stating: items done, items remaining, elapsed, current rate
   - **restartable**: on start, read all existing `.jsonl` files and skip work already done. A relaunch after a kill must not recompute anything.
   - a heartbeat even when an individual item is slow, so a long item is distinguishable from a hang

**3. Bounded reporting.** Print the Zaslavsky/Buck upper bound at the start so progress can be read as a fraction of a known ceiling.

# VALIDATION — mandatory, run these and report before anything else

1. **Known closed forms.** The coordinate arrangement e_1..e_n in R^n has exactly 2^n chambers and 3^n−1 non-zero faces. Verify for n = 2..6.
2. **m lines through the origin in R^2** → exactly 2m chambers and 4m faces. Verify m = 2..6.
3. **Agreement with the old enumerator** on a case the old one can finish: the octahedral 67's 6 walls in ambient 6 must give **728** non-zero faces (`isolation67.faces` produces this; use `wall_sharing.labels`-style extraction or read the walls from `isolation67.py`'s own path). Both must agree exactly.
4. **The case that broke the old code**: the 183 record — 12 walls, rank 8, ambient 9. Report the chamber count and face count and the wall-clock time. The old code did not finish in 3 hours; this must.

Get the 183 walls exactly as `onewall183.py` does (read it): degauge the configuration, `dimension.cached_conditions`, drop degenerates, dedupe gradients up to scale.

# CONSTRAINTS

- Exact rational arithmetic only. No floats, no tolerances.
- Do not modify any existing file. Create only `arrangement.py` and its outputs.
- If the 183 case does not finish within ~10 minutes, STOP and report the chamber count reached and where the time went — do not let it run indefinitely.
- Module docstring must state why the old enumerator failed (exponential in m, not in output size) so the next reader does not reintroduce it.

Report back: the four validation results, the 183 chamber and face counts with timing, and whether the queue/checkpoint machinery demonstrably restarts without recomputation.
```
