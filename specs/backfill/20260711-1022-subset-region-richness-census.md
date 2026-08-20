# Subset region-richness census

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-11T10:22:58 |
| Agent type | general-purpose |
| Model override | haiku |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01P5BsgRkhzZsMbbxCFSFCqE` |
| Files named | `subset_richness.py`, `subset_richness_report.md` |
| Present in repo | `subset_richness.py`, `subset_richness_report.md` |
| Cited in LEDGER/RESULTS | `subset_richness_report.md` |

## Prompt as sent

```text
Working directory: /Users/dmi/carroll. This is a read-only DATA ANALYSIS task over an existing log. Do NOT modify any .py, .cpp, or the validated files; only READ campaign_results.jsonl and WRITE one new report file. No searching, no counting engine needed — pure JSON aggregation in Python.

INPUT: campaign_results.jsonl — one JSON object per line, ~278,000 lines. Each has:
  - "bounded": int (total bounded regions of a 6-cube config)
  - "by_depth": {"0":..,"1":..,...,"6":..}
  - "per_label": {"<mask>": count, ...} where <mask> is a string integer 0..63, a bitmask over the 6 cubes; per_label[mask] = number of bounded regions contained in EXACTLY the set of cubes whose bits are set in mask. (popcount(mask)=1 is a single-cube region, =2 a pair region, etc.)
Some lines may lack per_label — skip those (count how many).

DEFINITIONS (compute per config):
  - total = bounded
  - per-cube d1 vector: for k in 0..5, d1[k] = per_label.get(str(1<<k), 0)   (6 values)
  - per-pair d2 vector: for each of the 15 pairs (i<j), d2 = per_label.get(str((1<<i)|(1<<j)), 0)
  - max_d1 = max(d1 vector); spread_d1 = max(d1) - min(d1)  (a balance measure; small = balanced)
  - max_d2 = max(d2 vector); spread_d2 = max - min over the 15 pairs

ANSWER THESE, with numbers:
  (A) Correlation: does subset-richness predict a rich total? Report Pearson correlation of total vs max_d1, and total vs max_d2, over all configs. Also bucket configs by total (e.g. deciles or fixed bins) and report mean max_d1 and mean max_d2 per bucket — is it monotone, or does it peak in the middle?
  (B) Do the configs with the RICHEST single subset have high total? Find the configs achieving the global max of max_d1 (and separately max_d2); report their totals and where those totals fall in the overall total distribution (percentile). (Expected from prior work: the per-cube d1 max ~26 and per-pair d2 max ~34 occur at MID totals, not top — verify or refute.)
  (C) Balance vs total: among the top 1% of configs by total, report mean spread_d1 and spread_d2; compare to the median-total configs and bottom 1%. Are top-total configs more balanced (smaller spread) than typical? Quantify.
  (D) Are singleton-richness and pair-richness coupled? Report correlation of max_d1 vs max_d2 across configs.

OUTPUT: write /Users/dmi/carroll/subset_richness_report.md — a concise report (numbers first, one short interpreting sentence each for A/B/C/D), plus a 3-5 line "categorization" summarizing the distinct region-rich-subset signatures you actually observe in the data (e.g. "balanced-moderate high-total type" vs "one-spiky-subset mid-total type"). Keep the analysis script inline in the report (a fenced code block) OR save it as subset_richness.py with a module docstring and a "# Working principles: README.md" comment — your choice, but if you save a .py it must parse and run. State the skipped-line count. Do not overstate: this is one campaign's random-seed ensemble (generic stratum), so say so. Final message: the four headline numbers (A correlation signs, B the rich-subset totals' percentiles, C the balance comparison, D coupling correlation) in 4 lines.
```
