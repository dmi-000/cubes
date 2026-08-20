# Viewer quats, search continuation, diagram census

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-10T10:11:53 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01DpuxDWo1wf3SF6WV6mnWjm` |
| Files named | `certify_six.py`, `cube_regions.cpp`, `exact_search.py`, `make_seed_viewer.py`, `mt_sim.py`, `run_campaign.py`, `six_cube_search_results.md` |
| Present in repo | `certify_six.py`, `cube_regions.cpp`, `exact_search.py`, `make_seed_viewer.py`, `mt_sim.py`, `run_campaign.py` |
| Cited in LEDGER/RESULTS | `certify_six.py`, `cube_regions.cpp`, `exact_search.py`, `run_campaign.py` |

## Prompt as sent

```text
Three independent workstreams on the cube-compound project in /Users/dmi/carroll. Context: read the tail of six_cube_search_results.md (Postscripts 3 and 4) and C45_notes.md first. The validated exact counter is ./cube_regions (C++ binary, cube_regions.cpp; JSON per config; --seed S, --seeds A B, --quats 'w,x,y,z;...' 6 groups, --selftest). Current record: 635 bounded regions at quats [[129,-171,-137,-28],[382,278,63,-186],[200,289,312,-203],[314,101,-391,1],[124,-61,26,-215],[276,269,33,335]]. Do not modify validated files (cube_regions.cpp only if a bug is proven; certify_six.py, exact_search.py, mt_sim.py never); do not touch exact_search_results.jsonl.

WORKSTREAM 1 — viewer quaternion input (do first, small):
The seed-viewer artifact template is /private/tmp/claude-502/-Users-dmi-carroll/c4196554-d37e-44f9-8da5-5d7210e1f156/scratchpad/seed_viewer_template.html and /Users/dmi/carroll/make_seed_viewer.py injects the counts snapshot into .../scratchpad/seed119_viewer.html. Add to the template: a quaternion input mode — a text field accepting 6 integer quaternions in the exact format 'w,x,y,z; w,x,y,z; ...' (whitespace tolerant), a Load button, validation (6 groups of 4 integers, |component| <= 512, nonzero), rendering via the existing quatToMat path, cube rows showing the entered quats, count area showing 'not certified from quats — run ./cube_regions --quats' unless the quats match a known config. Prefill the field's placeholder with the 635 record quats above and add a chip 'record 635 (climbed)' that loads them. Keep the existing seed mode fully working. Then run make_seed_viewer.py to regenerate seed119_viewer.html with a fresh counts snapshot. Do NOT attempt to publish (the main session publishes); just leave the file ready and say so.

WORKSTREAM 2 — search continuation toward >635 or local-maximality certification:
(a) Certify or refute local maximality of the 635 config: evaluate ALL single-component moves (each of 24 components, deltas ±1..±4, re-gcd, |c|<=512, skip degenerate zero quats) with ./cube_regions --quats. If any strictly exceeds 635, that's a new record — recurse on it greedily until a local max is reached. Report the final local max and the number of evaluations. This yields a certified statement: 'X is a local maximum under move radius 4' or a better record.
(b) Extended random campaign: continue seeds upward from where campaign_results.jsonl ends (188692) with 8 parallel workers via run_campaign.py, as far as your budget allows (aim 300k-500k more seeds). Watch: any total > 635, any depth-3 > 164, depth-4 > 102, depth-5 > 36 — these are now the live conjecture boundaries (the old C1/C2/C3 are dead; current observed ceilings: total 635, d1 118, d2 214).
(c) Deeper hill-climbing: 50+ greedy climbs with move radius up to ±4 from the top-50 configs across all logs (campaign_results.jsonl, hillclimb_log.jsonl, exact_search_results.jsonl read-only), logging every evaluation with quats to hillclimb_log.jsonl (append).

WORKSTREAM 3 — spherical diagram census (the mathematical payload; see C45_notes.md section 6 for the full spec):
For these configs — the 635 record, seeds 29390, 12, 2228, one sub-36-depth-5 seed (scan campaign_results.jsonl for by_depth['5']==34), and six6-family quats [(p,0,0,r) style: [[5,0,0,1],[5,0,0,-1],[5,1,0,0],[5,-1,0,0],[5,0,1,0],[5,0,-1,0]] as a structured case] — build the bottom-l diagrams B_1, B_2, B_3 on the direction sphere and count their cells, vertices, edges. Method guidance: the radial function of cube k at direction u is t_k(u) = 1/max_j |(column_j of R_k) . u| (columns from quatToMat over the integer quaternion, all rational). A robust approach: dense sampling + exact refinement is acceptable for CELL counts if you validate against ground truth — the cell counts of B_1/B_2/B_3 MUST equal the per_label-derived depth-5/4/3 counts from ./cube_regions (validation gate for your diagram code). Then the real deliverables: (i) V, E counts of the swap curves Sigma_1, Sigma_2, Sigma_3 (vertex types: rank-triple points where three t values tie as ranked neighbors, vs own-edge-arc crossings where a cube's active face changes) — test the T1 prediction E - V = 34, 100, 162 on generic configs; (ii) check for 'bottom-shoulder cells': any B_1 cell containing none of the 36 face-center directions (face centers of cube k = ± columns of R_k); any such cell is a major finding (it breaks the anchoring hypothesis); (iii) for the sub-36 config, identify WHICH face patches merged (which cube, which pair of faces, around which edge direction). Report the census tables.

Deliverables: updated template + regenerated seed119_viewer.html (ready to publish); local-maximality verdict for 635 (or new record with quats); extended campaign coverage + any conjecture boundary movement; diagram census tables + shoulder-cell verdict + T1 census verdict; append everything as 'Postscript 5' to six_cube_search_results.md. Final message: one-paragraph verdict per workstream with the key numbers. Honest negatives welcome; a diagram code that fails its validation gate must be reported as failed, not worked around.
```
