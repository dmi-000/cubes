# Spec: blueprint branch-and-prune search (n=6, exhaustive at the blueprint level)

For a Sonnet agent. Read first: six_cube_search_results.md Postscripts
17–19 (+ addenda: DOF hierarchy, ceiling law C(l,n), 63-vs-67 principle),
shared_axis_search.py (REUSE its cluster/spoke construction and knob
search — do not rewrite), PROJECT.md. Record to beat: n=6 723.

## The idea (from the user)

Search over WAYS TO COMBINE BUILDING BLOCKS and over FRUSTRATION
TRADE-OFFS, structured as branch-and-prune:

- A **blueprint** = the combinatorial skeleton of a 6-cube config: the
  partition of the 6 cubes into shared-axis clusters (each cluster's
  cubes are mutually 9-paired: they share one rotation axis), plus the
  relations between clusters / to hub cubes (generic-4, rigid-13, or
  wall-5), plus which cubes are free.
- **Branch**: enumerate blueprints (finite after symmetry).
- **Prune** (justified rules only):
  P1 realizability — 9-edges must form axis-sharing cliques; 13 is a
     rigid discrete relation (60° body-diagonal class); labelings that
     are geometrically inconsistent are pruned without counting.
  P2 frustration — any all-13 triangle forces the golden/octahedral
     wall, whose extensions provably lose (681 < 723): prune subtree.
  P3 dominance — blueprints whose parts cannot be deep-saturated
     (cannot reach their C(l,k) caps, e.g. a cluster too large to keep
     d-deep structure) are dominated; document each use.
- **Optimize per surviving blueprint**: the continuous knobs = spoke
  angles (rational tan-half grid + refine) and free-cube integer quats
  (hill-climb), exactly as shared_axis_search.py does. Budget per
  blueprint proportional to its knob count.

## Deliverable claim (why this matters)

The output statement is qualitatively stronger than any search so far:
"NO blueprint beats 723" (exhaustive at the skeleton level, given the
per-blueprint optimization), rather than "we didn't find one". State the
per-blueprint coverage honestly (grid resolution, restarts) so the claim
is auditable.

## Tasks

1. ENUMERATE blueprints for n=6 up to symmetry: cluster-size partitions
   of 6 (6; 5+1; 4+2; 4+1+1; 3+3; 3+2+1; 3+1+1+1; 2+2+2; 2+2+1+1;
   2+1+1+1+1; 1×6) × axis choices for each cluster ((1,1,1), (0,0,1),
   (1,1,0) classes; shared vs distinct axes between clusters) ×
   inter-cluster/hub relation labels. Apply P1–P3. Print the catalog
   with prune reasons — the catalog itself is a deliverable.
2. GATE: the blueprints of the known records must survive pruning and
   their optimization must reproduce 183 (as the n=4 sanity, optional)
   and 723 (required: the 3-spokes+3-on-axis blueprint → 723).
3. RUN the surviving blueprints' knob searches (≤4 cores, detached; do
   NOT park on monitors — launch a self-contained driver that writes
   the report at the end). Log every eval (blueprint id, quats, total,
   by_depth) to blueprint_search.jsonl.
4. REPORT blueprint_search_report.md: the catalog (total enumerated,
   pruned by which rule, survivors), best total per surviving blueprint
   vs 723, any config > 723 (flag IMMEDIATELY, verify with the Python
   oracle certify_six.exact_count_config before claiming), and the
   verdict sentence: does any blueprint beat 723, and is the blueprint
   level now exhausted at stated coverage?

## Rules

Exact arithmetic only (./cube_regions); do NOT modify validated files or
six_cube_search_results.md; exact_search_results.jsonl read-only;
≤4 cores; deliverables blueprint_enum.py + blueprint_search.py +
blueprint_search.jsonl + blueprint_search_report.md. Honest negatives
welcome — "no blueprint beats 723 at this coverage" is the expected and
valuable outcome.
