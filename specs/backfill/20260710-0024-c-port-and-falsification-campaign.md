# C++ port and falsification campaign

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-10T00:24:54 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01K1x9gGWayMJyEmg4dZZikC` |
| Files named | `breakdown.py`, `certify_six.py`, `cube_regions.cpp`, `make_seed_viewer.py`, `mt_sim.py`, `run_campaign.py`, `six_cube_search_results.md` |
| Present in repo | `breakdown.py`, `certify_six.py`, `cube_regions.cpp`, `make_seed_viewer.py`, `mt_sim.py`, `run_campaign.py` |
| Cited in LEDGER/RESULTS | `breakdown.py`, `certify_six.py`, `cube_regions.cpp`, `run_campaign.py` |

## Prompt as sent

```text
Build a fast exact region counter in C++ and run a falsification campaign against the region-count ceiling conjectures. Work in /Users/dmi/carroll. All context you need is on disk; read these first, in this order:

1. /Users/dmi/carroll/CPP_SPEC.md — the complete spec for what you're building (number system, algorithm, validation gates, campaign phases, conjectures). Follow it exactly; the design decisions there (integer homogeneous coordinates via plane-triple Cramer, int128 with a small 256-bit helper for centroids, canonical gcd-reduced vertex keys) are deliberate and analyzed for overflow — do not substitute floating point or chained interpolation.
2. /Users/dmi/carroll/certify_six.py — the reference implementation your C++ must match: `exact_count_config` is the exact algorithm to port 1:1 including every assert (facet groups of exactly 2, phantom facets join equal labels, real facets flip exactly the owning cubes' bits, single outside region, coincident-plane owner classes). These asserts caught real bugs during development; they are the correctness net.
3. /Users/dmi/carroll/mt_sim.py — the validated seed chain (numpy MT19937 + legacy polar gaussian + scipy quaternion conventions + rationalization). Port bit-exactly.
4. /Users/dmi/carroll/breakdown.py and the tail of /Users/dmi/carroll/six_cube_search_results.md — background on what's being tested and the per-subset structure found so far.

Ground truth oracle: /Users/dmi/carroll/exact_search_results.jsonl (seeds 40+, counts and depth histograms from the validated Python pipeline; the user's background search may still be appending to it — read-only for you). Seeds 0-39 counts are the BATCH list inside /Users/dmi/carroll/make_seed_viewer.py.

HARD GATES, in order — do not start any campaign until all pass:
  G1: --selftest axial case returns exactly 121 with depth histogram {1:24,...,5:24,6:1} (see spec for the integer (p,0,0,r) quaternion construction).
  G2: seeds 0..199 match the oracle exactly (count AND depth histogram). Any mismatch: stop and debug; the Python pipeline is right and your port is wrong.
  G3: report single-config timing.
If you cannot pass the gates after serious effort, deliver the diagnosis of where the port diverges instead of a broken campaign — a failed-with-analysis report is a valid outcome, a campaign on an unvalidated counter is not.

Then, per the spec:
  Phase A: parallel mass search (8 worker processes on disjoint seed ranges, starting at seed 3000, going as far as the time budget allows — target at least 100k seeds). Every config's JSON line includes per_label. Watch for violations of: total<=623, depth-1<=112, depth-2<=208, depth-3<=164, depth-4<=102, depth-5==36, depth-6==1.
  Phase B: exact hill-climbing from the top-20 configurations found anywhere (integer quaternion component moves per spec, all configs logged as explicit quats for reproducibility). Also run variant climbs maximizing depth-1 alone and depth-2 alone — the per-cube analysis showed single cubes reach 22 exposed pieces while the sum caps at 112, so try to construct configs with many 22-cubes.
  Phase C: breakdown analysis (per-cube depth-1 and per-pair depth-2 distributions of the top configs; identify whether the depth-3=164 / depth-4=102 sums are ever exceeded or are conserved-at-max; summarize the evidence for/against each conjecture C1-C6).

Deliverables:
  /Users/dmi/carroll/cube_regions.cpp (single file, C++17, no external deps; build with clang++ -O2 -std=c++17)
  /Users/dmi/carroll/run_campaign.py (parallel driver + merge + violation watch)
  campaign shard outputs merged to /Users/dmi/carroll/campaign_results.jsonl (do NOT touch exact_search_results.jsonl)
  an appended section in /Users/dmi/carroll/six_cube_search_results.md with the campaign findings
Do not modify any existing validated Python file. Budget: a few hours of compute is fine; prioritize gate-passing correctness over campaign breadth.

Your final message must state: gate results (exact numbers), configs/second achieved, seeds covered, new records with their quats and breakdowns, whether ANY conjecture was violated (with the violating config's quats if so), and where every deliverable lives.
```
