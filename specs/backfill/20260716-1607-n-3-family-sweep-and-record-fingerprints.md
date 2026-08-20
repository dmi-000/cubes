# n>3 family sweep and record fingerprints

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-16T16:07:28 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01UE5XshwVE4sZLYAVW1wp1H` |
| Files named | `bigfamily.py`, `nfamily_report.md`, `nfamily_sweep.py`, `six_cube_search_results.md` |
| Present in repo | `nfamily_report.md`, `nfamily_sweep.py` |
| Cited in LEDGER/RESULTS | `nfamily_report.md`, `nfamily_sweep.py` |

## Prompt as sent

```text
Execute the task specified in /Users/dmi/carroll/NFAMILY_SPEC.md: determine whether the dihedral/big family (n cubes with face-axes perpendicular to a common (1,1,1) axis, common tilt ψ, free phases θ_k) helps at n>3. Read the spec fully first. It defines the family, the key arithmetic fact (Pythagorean ψ and phase differences make relative rotations rational → integer quaternions → countable by the fast C++ engine ./cube_regions_n in /Users/dmi/carroll), three hard gates (G0 exact rational round-trip, G1 two-engine agreement on n=3 and n=4 family configs, G2 reproduce the 723 record from ledger quats before sweep negatives count), four questions (Q1 how high do family counts go at n=4/5/6 vs records 183/393/723; Q2 which deep layers stay stable along the family; Q3 do the existing record configs already contain family-type pairs — count exact edge crossings per pair in the records with exact rational arithmetic; Q4 chain-path spikes), and the sweep design with budget. Background scripts: /Users/dmi/carroll/dihedral_scratch/bigfamily.py and neighbors; ledger six_cube_search_results.md Postscript 25 + addenda for context (READ-ONLY). Write nfamily_report.md, nfamily_sweep.py, nfamily_results.jsonl to /Users/dmi/carroll. ≤4 cores, run the sweep detached, don't park on monitors — write interim results to the report as you go. Verify any claimed best-of-n with the Python oracle certify_six.exact_count_config before reporting. Report back: gate results, Q1–Q4 answers with numbers, honest coverage statement.
```
