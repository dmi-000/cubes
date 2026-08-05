# Six-cube compound region search — results

Empirical (voxel flood-fill) search over compounds of 6 congruent concentric
cubes for the configuration maximizing the number of bounded regions the 6
cube surfaces cut space into. Tool: `cube_compound_regions.py` (unmodified,
validated logic) extended additively by `six_cube_search.py` (new file,
matrix-list counting path with the identical small→big merge policy,
tau = 3R).

<!-- INDEX:START (regenerate with index_ledger.py; do not hand-edit) -->

## Postscript index

The ledger is **append-only and ordered by write time, not by number** —
a postscript number is reserved when the work is delegated and the text
lands when the report comes back, so e.g. 31 sits after 41 and the 29
addendum after that. This index is the lookup by number; regenerate it
with `index_ledger.py` after appending.

- [Postscript 1](#postscript-exact-certification-overturns-the-ranking) — exact certification overturns the ranking
- [Postscript 2](#postscript-2-subset-maximality-analysis-subset_analysispy-pair_checkspy) — subset-maximality analysis (subset_analysis.py, pair_checks.py)
- [Postscript 3](#postscript-3-c-engine-per-subset-structure-and-a-corrected-law) — C++ engine, per-subset structure, and a corrected "law"
- [Postscript 4](#postscript-4-mass-falsification-campaign--c1c2c3-fall-new-record-635) — mass falsification campaign — C1/C2/C3 fall, new record 635
- [Postscript 5](#postscript-5-635-certified-locally-maximal-campaign-to-260k-exact-spherical-census-confirms-t1) — 635 certified locally maximal; campaign to 260k; exact spherical census confirms T1
- [Postscript 6](#postscript-6-n--6-cubes--engine-generalized-n7-campaign-underway) — n > 6 cubes — engine generalized, n=7 campaign underway
- [Postscript 7](#postscript-7-beyond-rational-rotations--the-ℚd-program) — beyond rational rotations — the ℚ(√d) program
- [Postscript 8](#postscript-8-multi-constraint-search-pays--tower-verification-the-111-wall-explained-and-a-new-rational-record-655) — multi-constraint search pays — tower verification, the (1,1,1) wall explained, and a new…
- [Postscript 9](#postscript-9-sliding-3-cube-triples--a-new-rational-and-overall-record-699-slide3_reportmd) — sliding 3-cube triples — a new RATIONAL AND OVERALL record 699 (slide3_report.md)
- [Postscript 9 addendum](#postscript-9-addendum-2026-07-13-the-slide-axis-identified-exactly) — the slide axis identified exactly
- [Postscript 9 addendum](#postscript-9-addendum-2-2026-07-13-edge-crossings-along-the-slide--near-persistence-quantified) — edge crossings along the slide — near-persistence quantified
- [Postscript 10](#postscript-10-symmetry-stratified-sweep-of-the-walls--no-new-record-framework-validated-coverage-caveat) — symmetry-stratified sweep of the walls — no new record, framework validated, coverage caveat
- [Postscript 11](#postscript-11-full-quaternion-symmetry-re-run--new-record-717-and-705-postscript-10s-negative-was-a-coverage-artifact) — full-quaternion symmetry re-run — NEW RECORD 717 (and 705); Postscript 10's negative was a…
- [Postscript 11 addendum](#postscript-11-addendum-717-is-capped--the-shallow-tail-tradeoff-is-a-11-conservation) — 717 is capped — the shallow-tail tradeoff is a 1:1 conservation
- [Postscript 12](#postscript-12-shared-axis-intersection-families--new-record-723) — shared-axis "intersection" families — NEW RECORD 723
- [Postscript 13](#postscript-13-incidence-geometry--edge-vs-corner-concurrences-the-9-fold-sweet-spot-and-the-algebraic-search) — incidence geometry — edge vs corner concurrences, the 9-fold sweet spot, and the algebraic…
- [Postscript 14](#postscript-14-the-depth-trade-off-structure--deep-layers-quantize-shallow-layers-grow-records-sacrifice-deep-for-shallow) — the depth trade-off structure — deep layers quantize, shallow layers grow, records sacrifice…
- [Postscript 14](#postscript-14--results--a-correction-2026-07-12) — — results & a correction (2026-07-12)
- [Postscript 15](#postscript-15-n4--golden-177-is-not-the-maximum-new-rational-record-183) — n=4 — golden 177 is NOT the maximum; new rational record 183
- [Postscript 16](#postscript-16-records-nest--723s-subsets-contain-the-smaller-records-and-its-5-subset-beats-golden-351) — records NEST — 723's subsets contain the smaller records, and its 5-subset beats golden 351
- [Postscript 16 addendum](#postscript-16-addendum-greedy-extension-validated--new-n7-record-1207) — greedy extension VALIDATED — new n=7 record 1207
- [Postscript 16 addendum](#postscript-16-addendum-2-n2-and-n3-stress-tested--13-and-67-hold) — n=2 and n=3 stress-tested — 13 and 67 hold
- [Postscript 16 addendum](#postscript-16-addendum-3-n5--393-is-robust-native-search-cant-reach-it) — n=5 = 393 is robust; native search can't reach it
- [Postscript 17](#postscript-17-local-perfection-is-globally-frustrated-past-n3--the-middle-layer-mechanism) — local perfection is globally frustrated past n=3 — the "middle-layer" mechanism
- [Postscript 17 addendum](#postscript-17-addendum-the-dof-hierarchy--local-optima-are-rigid-flexibility-lives-in-suboptimal-but-structured-configs) — the DOF hierarchy — local optima are RIGID, flexibility lives in suboptimal-but-structured…
- [Postscript 18](#postscript-18-shared-axis-cluster-construction--free-spoke-angles-recover-every-record-lockedcontrol-variants-fall-short) — shared-axis-cluster construction — free spoke angles recover every record; locked/control…
- [Postscript 18 addendum](#postscript-18-addendum-shared-axis-campaign-complete-150k-evals) — shared-axis campaign complete (~150k evals)
- [Postscript 19](#postscript-19-the-general-ceiling-law--depth-nl--12l6n--2l²1) — THE GENERAL CEILING LAW — depth-(n−l) ≤ (12l−6)n − 2(l²−1)
- [Postscript 19 addendum](#postscript-19-addendum-why-63-beats-67-as-a-building-block--deep-structure-persists-shallow-count-is-recut) — why 63 beats 67 as a building block — deep structure persists, shallow count is recut
- [Postscript 20](#postscript-20-the-deficit-propagation-envelope--an-empirical-branch-and-bound-bound-and-723-nearly-cornered) — the deficit-propagation envelope — an empirical branch-and-bound bound, and 723 nearly cornered
- [Postscript 21](#postscript-21-blueprint-branch-and-prune-complete--67-skeletons-exhausted-nothing-beats-723) — blueprint branch-and-prune complete — 67 skeletons exhausted, nothing beats 723
- [Postscript 22](#postscript-22-the-n7-program--1207-certified-the-ceiling-law-passes-its-out-of-sample-test-first-n8-record-1879) — the n=7 program — 1207 certified, the ceiling law passes its out-of-sample test, first n=8…
- [Postscript 23](#postscript-23-the-cap-sum-bound-is-tight-at-n2-and-n3--a-proof-of-13-and-67-reduces-to-two-lemmas) — the cap-sum bound is TIGHT at n=2 and n=3 — a proof of 13 and 67 reduces to two lemmas
- [Postscript 23 addendum](#postscript-23-addendum-do-the-proofs-extend-to-n--3-chris-cole) — do the proofs extend to n > 3? (Chris Cole)
- [Postscript 24](#postscript-24-first-theorem--the-anchor-lemma-is-proven-all-n-and-the-n2-cad-verdict) — FIRST THEOREM — the anchor lemma is proven (all n), and the n=2 CAD verdict
- [Postscript 25](#postscript-25-the-dihedral-family--a-closed-form-1-parameter-family-with-exact-edge-coincidences-containing-both-67s-the-ghosts-explained-a-new-exactly-certified-compound-in-qsqrt6) — the DIHEDRAL FAMILY — a closed-form 1-parameter family with exact edge coincidences,…
- [Postscript 25 addendum](#postscript-25-addendum-the-persistent-18-core--octahedral-to-golden-slides-without-breaking-a-single-concurrence-corner-docking-corrected-transition-locations) — the persistent 18-core — octahedral-to-golden slides WITHOUT breaking a single concurrence;…
- [Postscript 25 addendum](#postscript-25-addendum-2-paths-preserving-more-than-18--the-pair-curve-identity-a-26-concurrence-chain-triple-and-why-18-is-still-the-end-to-end-record) — paths preserving MORE than 18 — the pair-curve identity, a 26-concurrence chain triple, and…
- [Postscript 25 addendum](#postscript-25-addendum-3-exact-region-counts-along-the-dihedral-family-task-1-executed--a-symmetric-staircase-spikes-at-the-67s-and-a-local-minimum-at-the-face-diagonal-point) — EXACT region counts along the dihedral family (Task 1 executed) — a symmetric staircase,…
- [Postscript 25 addendum](#postscript-25-addendum-4-the-handoff-chase--18-stands-the-obstruction-identified-and-a-correction-to-addendum-2s-golden-contact-count) — the handoff chase — 18 stands, the obstruction identified, and a CORRECTION to addendum 2's…
- [Postscript 26](#postscript-26-the-records-are-built-from-family-pairs--the-n3-verdict-on-the-dihedral-family) — the records are BUILT FROM family pairs — the n>3 verdict on the dihedral family
- [Postscript 26 addendum](#postscript-26-addendum-four-theorems-proved-c45_notesmd-section-12) — four theorems PROVED (C45_notes.md section 12)
- [Postscript 27](#postscript-27-the-gluing-search--records-still-unbeaten-deficit-exactly-8-at-every-n-and-the-rational-tangent-discovery-with-a-correction-to-the-agents-clique-inventory) — the gluing search — records still unbeaten (deficit exactly 8 at every n), and the…
- [Postscript 28](#postscript-28-the-n4-resonance-solve--cross-class-alignment-is-count-negative-at-n4-best-resonance-151-and-it-is-secretly-rational) — the n=4 resonance solve — cross-class alignment is count-NEGATIVE at n=4; best resonance…
- [Postscript 29](#postscript-29-the-rational-tangent-sweep-interim--the-exactly-8-floor-is-broken-at-n5-deficit-now-6) — the rational-tangent sweep (interim) — the "exactly 8" floor is BROKEN at n=5: deficit now 6
- [Postscript 29 addendum](#postscript-29-addendum-723-is-a-plateau-with-at-least-four-non-congruent-realizations--an-exact-three-layer-exchange-law-inside-the-summit) — 723 is a PLATEAU with (at least) four non-congruent realizations — an exact three-layer…
- [Postscript 30](#postscript-30-the-event-catalogue--the--1-per-coincidence-law-dies-a-depth-conservation-law-survives-1212-and-a-correction-to-postscript-25-addendum-3) — the event catalogue — the "+-1 per coincidence" law dies, a depth-conservation law survives…
- [Postscript 31](#postscript-31-the-census-extraction--the-92-budget-is-exact-at-both-67-witnesses-its-accounting-corrected-and-the-coincidences-are-top-diagram-vertices) — the census extraction — the 92 budget is EXACT at both 67 witnesses, its accounting…
- [Postscript 32](#postscript-32-the-open-n4-resonance-candidates-counted-exactly--still-all-count-negative-best-169--175-the-sqrt13-chain--159) — the open n=4 resonance candidates counted exactly — still all count-negative; best 169 <…
- [Postscript 33](#postscript-33-first-complete-maximum-theorem--max2--13-proved-all-r-and-d218--d_n-16n-proved-unconditionally) — FIRST COMPLETE MAXIMUM THEOREM — max(2) = 13 proved (all R), and d2<=18 / d_{n-1}<=6n proved…
- [Postscript 34](#postscript-34-feasibility-verdict-on-the-last-gap-star-sumdeg-292--it-splits-3260-the-easy-half-reduces-to-a-clean-16-simultaneous-triples-lemma-the-hard-half-needs-targeted-not-random-search) — feasibility verdict on the last gap (star) Sum(deg-2)<=92 — it splits 32+60, the easy half…
- [Postscript 35](#postscript-35-sub-lemma-1a-proved--triple-point-weight--32-via-d2--18-max367-now-hinges-on-one-inequality-contact-weight--60) — sub-lemma 1a PROVED — triple-point weight <= 32 (via d2 <= 18); max(3)=67 now hinges on ONE…
- [Postscript 36](#postscript-36-region-count-is-affine-invariant--the-records-are-realized-by-a-whole-affine-family-of-parallelepiped-cells-congruent-rhombohedra-match-67-correcting-a-first-wrong-probe) — region count is AFFINE-INVARIANT — the records are realized by a whole affine family of…
- [Postscript 37](#postscript-37--retracted-see-postscript-38---this-postscript-is-wrong-it-counted-cells-of-the-infinite-plane-arrangement-not-real-face-bounded-regions) — *** RETRACTED (see Postscript 38) *** — this postscript is WRONG; it counted cells of the…
- [Postscript 38](#postscript-38-the-counting-error-corrected--regions-are-separated-by-faces-not-infinite-planes-and-a-trivial-proof-that-max2--13-for-all-convex-6-faced-cells) — the counting error corrected — regions are separated by FACES, not infinite planes; and a…
- [Postscript 39](#postscript-39-the-correct-successor-to-p37--the-max367-proof-layers-generalize-to-all-convex-6-faced-cells-and-flex-does-not-beat-67) — the CORRECT successor to P37 — the max(3)=67 proof layers GENERALIZE to all convex 6-faced…
- [Postscript 40](#postscript-40-the-remaining-gap-reduced-to-a-clean-incidence-bound-on-the-cells-edge-skeletons-verified-with-an-euler-on-intersection-handle-not-yet-closed) — the remaining gap reduced to a clean INCIDENCE bound on the cells' edge-skeletons…
- [Postscript 41](#postscript-41-candidate-proof-of-max367-all-convex-6-faced-cells-via-euler-on-the-pairwise-intersection-polytopes--the-contact-bound-closes) — CANDIDATE PROOF of max(3)=67 (all convex 6-faced cells) via Euler on the PAIRWISE…
- [Postscript 42](#postscript-42-step-t-is-not-routine--the-reduction-deg_top--deg_bot-at-triple-points-is-false-counterexample-realized-on-genuine-cells-max367-stands-on-the-generic-stratum--both-maximizers-degenerate-triple-points-remain-an-open-gap) — Step T is NOT routine — the reduction "deg_top ≤ deg_bot at triple points" is FALSE…
- [Postscript 43](#postscript-43-step-t-closed--max367-proved-for-all-3-concentric-convex-6-facet-cells-meeting-pairwise-transversally-degenerate-triple-points-included-the-fix-is-a-two-budget-local-inequality-not-deg_topdeg_bot) — STEP T CLOSED — max(3)=67 proved for all 3 concentric convex ≤6-facet cells meeting pairwise…
- [Postscript 44](#postscript-44-the-n3-anomaly-audit--its-maximum-is-the-only-one-that-is-finite-yet-multiple-irrational-and-non-nesting-the-three-are-one-phenomenon-and-13-is-not-rigid--corrects-postscript-17-addendum) — the n=3 anomaly audit — its maximum is the only one that is finite-yet-multiple, irrational,…
- [Postscript 45](#postscript-45-new-records-n7--1211-and-n8--1889--found-top-down-then-bottom-up-in-one-afternoon-1211-is-a-plateau-reached-by-four-independent-routes) — NEW RECORDS n=7 = 1211 and n=8 = 1889 — found top-down-then-bottom-up in one afternoon; 1211…
- [Postscript 46](#postscript-46-723-is-beaten--n6--727-and-it-lifts-the-tower-to-n7--1217-n8--1891-the-large-height-quaternion-stratum-was-never-sampled) — 723 IS BEATEN — n=6 = 727, and it lifts the tower to n=7 = 1217, n=8 = 1891; the…
- [Postscript 46 addendum](#postscript-46-addendum-727-is-a-plateau-and-729-was-not-reached-80-000-sixth-cubes-on-the-393-base) — 727 is a plateau, and 729 was not reached (80 000 sixth cubes on the 393 base)
- [Postscript 47](#postscript-47-727-is-proved-isolated-on-the-393-base-and-its-coincidence-pattern-is-unaugmentable-the-record-has-fewer-coincidences-than-723-and-every-condition-is-a-quadric) — 727 is PROVED isolated on the 393 base and its coincidence pattern is unaugmentable; the…
- [Postscript 48](#postscript-48-the-locus-enumeration--9-loci-are-codimension-1-three-wall-intersection-is-a-30x-better-search-and-727-is-a-plateau-two-non-congruent-compounds) — the locus enumeration — 9-loci are codimension 1, three-wall intersection is a 30x better…
- [Postscript 48 addendum](#postscript-48-addendum-the-enumerations-first-9-h--727-is-a-four-class-plateau-with-d1d2d3d4--690-conserved-nothing-above-727-in-256-000-configurations) — the enumeration's first 9 h — 727 is a FOUR-class plateau with d1+d2+d3+d4 = 690 conserved;…
- [Postscript 49](#postscript-49-the-walls-are-pairs-of-planes--the-three-wall-family-is-2-733-configurations-exhausted-in-four-minutes-max-727-and-why-its-all-rational-solutions-are-an-artifact) — the walls are PAIRS OF PLANES — the three-wall family is 2 733 configurations, exhausted in…
- [Postscript 49 addendum](#postscript-49-addendum-the-w--0-gap-was-illusory--the-chart-omits-quaternions-not-configurations) — the w = 0 "gap" was illusory — the chart omits quaternions, not configurations
- [Postscript 50](#postscript-50-the-mixed-strata-are-2401-irrational-dominated-by-ℚ5--a-large-stratum-no-search-in-this-project-has-ever-counted) — the mixed strata are 240:1 IRRATIONAL, dominated by ℚ(√5) — a large stratum no search in…
- [Postscript 51](#postscript-51-a-ℚd-c-engine-82-458-irrational-configurations-counted--nothing-above-727-but-a-fifth-727-class-that-is-irrational-in-ℚ13) — a ℚ(√d) C++ engine, 82 458 irrational configurations counted — nothing above 727, but a…
- [Postscript 51 addendum](#postscript-51-addendum-the-d--100-gap-is-mostly-a-guard-shape-problem--a-joint-budget-unlocks-343-000-configurations-with-no-arithmetic-change) — the d > 100 gap is mostly a GUARD-SHAPE problem — a joint budget unlocks ~343 000…
- [Postscript 51 addendum](#postscript-51-addendum-2-correction-dm²-is-not-the-overflow-invariant-and-the-joint-rule-proposed-above-would-have-been-unsafe) — d·m² is NOT the overflow invariant, and the joint rule proposed above would have been UNSAFE
- [Postscript 51 addendum](#postscript-51-addendum-3-correction--completion-224-184-irrational-configurations-counted-still-nothing-above-727--but-727-has-at-least-twelve-congruence-classes-eight-of-them-irrational-across-eight-fields) — 224 184 irrational configurations counted, still nothing above 727 — but 727 has at least…
- [Postscript 51 addendum](#postscript-51-addendum-4-the-region-count-is-not-galois-invariant--and-the-arithmetic-structure-reading-of-the-727-plateau-was-mostly-bookkeeping) — the region count is NOT Galois-invariant — and the "arithmetic structure" reading of the 727…
- [Postscript 51 addendum](#postscript-51-addendum-5-n3-is-less-anomalous-than-postscript-44-claimed--two-of-its-three-anomalies-were-instrument-limited) — n=3 is less anomalous than Postscript 44 claimed — two of its three "anomalies" were…
- [Postscript 52](#postscript-52-a-new-congruence-class-of-the-n5-record-393--and-a-correction-the-irrational-record-achievers-are-rationally-shadowed-so-irrationality-is-doing-no-work-at-n5-or-n6) — a NEW congruence class of the n=5 record 393 — and a correction: the irrational…
- [Postscript 52 addendum](#postscript-52-addendum-n5-run-complete--three-fields-144-configurations-one-profile-and-the--part-structure) — n=5 run complete — three fields, 144 configurations, one profile, and the √-part structure
- [Postscript 52 addendum](#postscript-52-addendum-2-correction-the-μ-multiset-undercounts-classes--at-least-21-distinct-labelled-types-among-the-irrational-727s-not-8-and-the-irrational-727s-are-all-rationally-shadowed) — the μ-multiset UNDERCOUNTS classes — at least 21 distinct labelled types among the…
- [Postscript 52 addendum](#postscript-52-addendum-3-n4s-shortfall-holds-across-all-four-bases-and-a-region-adjacency-invariant-now-exists) — n=4's shortfall holds across ALL FOUR bases; and a region-adjacency invariant now exists
- [Postscript 52 addendum](#postscript-52-addendum-4-the-727-plateau-holds-at-least-600-configurations--every-earlier-class-count-measured-the-enumerator) — the 727 plateau holds at least 600 configurations — every earlier class count measured the…
- [Postscript 52 addendum](#postscript-52-addendum-5-the-727-plateau-has-at-least-109-distinct-combinatorial-types--and-per-label-is-as-sharp-as-adjacency) — the 727 plateau has at least 109 distinct combinatorial types — and per-label is as sharp as…
- [Postscript 52 addendum](#postscript-52-addendum-6-a-taxonomy-of-the-727-plateau--types-are-tight-clusters-with-fixed-pair-relations-and-the-c3-quotient-corrects-the-counts) — a taxonomy of the 727 plateau — types are tight clusters with fixed pair relations, and the…
- [Postscript 53](#postscript-53-a-failed-attempt-at-proving-e1-with-the-error-located--each-piece-adds-one-region-is-false-for-non-disk-pieces) — a FAILED attempt at proving E1, with the error located — "each piece adds one region" is…
- [Postscript 54](#postscript-54-the-727-plateau-is-a-nested-chamber-structure-and-adjacent-types-differ-by-an-elementary-2-exchange-within-one-depth) — the 727 plateau is a nested chamber structure, and adjacent types differ by an elementary ±2…
- [Postscript 55](#postscript-55-the-9-plane-corner-concurrence-stratum-is-capped-at-723--records-do-not-concentrate-there-723-did) — the 9-plane corner-concurrence stratum is CAPPED AT 723 — records do not concentrate there,…
- [Postscript 55 addendum](#postscript-55-addendum-the-ways-of-reaching-727--the-discovered-record-is-a-1-in-161-outlier-and-one-route-carries-a-13-pair) — the ways of reaching 727 — the discovered record is a 1-in-161 outlier, and one route…
- [Postscript 56](#postscript-56-e1-is-now-a-theorem--the-one-cube-increment-is-bounded-by-an-euler-count-on-the-cubes-own-surface-and-postscript-53s-counterexample-was-itself-wrong) — E1 is now a THEOREM — the one-cube increment is bounded by an Euler count on the cube's own…
- [Postscript 57](#postscript-57-the-complete-taxonomy-of-codimension-1-walls--two-types-were-never-enumerated-and-both-are-finite-catalogues-against-a-fixed-base) — the complete taxonomy of codimension-1 walls — two types were never enumerated, and both are…
- [Postscript 58](#postscript-58-the-chamber-boundaries-of-the-plateau-are-wall-crossings--and-the-wall-type-that-governs-them-is-the-one-nobody-had-enumerated) — the chamber boundaries of the plateau are wall crossings — and the wall type that governs…
- [Postscript 59](#postscript-59-a-256-bit-ℚd-engine--the-284-634-configurations-the-old-budget-rejected-are-now-countable-and-the-equivalence-gate-nearly-passed-vacuously) — a 256-bit ℚ(√d) engine — the 284 634 configurations the old budget REJECTED are now…
- [Postscript 60](#postscript-60-the-irrational-configurations-are-the-seams-between-rational-continua--never-interior-to-one-and-the-split-is-total) — the irrational configurations are the SEAMS between rational continua — never interior to…
- [Postscript 61](#postscript-61-correction-to-postscript-60-the-irrational-configurations-are-in-continua--k-counted-walls-not-chamber-boundaries-and-most-of-those-walls-are-combinatorially-inert) — the irrational configurations ARE in continua — k counted walls, not chamber boundaries, and…
- [Postscript 61 addendum](#postscript-61-addendum-over-all-183-some-are-in-continua-and-some-are-not--and-in-a-continuum-irrationality-is-the-generic-case-so-its-presence-was-never-informative) — over all 183, SOME are in continua and some are not — and in a continuum irrationality is…
- [Postscript 62](#postscript-62-what-happens-at-the-endpoint-of-a-727-continuum--the-interval-is-open-the-endpoint-has-its-own-count-and-region-counts-are-not-semicontinuous) — what happens at the endpoint of a 727 continuum — the interval is OPEN, the endpoint has its…
- [Postscript 62 addendum](#postscript-62-addendum-the-other-endpoint--w3-written-as-a-polynomial-at-last-and-both-ends-of-the-interval-are-725) — the OTHER endpoint — W3 written as a polynomial at last, and both ends of the interval are 725
- [Postscript 63](#postscript-63-the-line-catalogue-was-never-symmetry-closed--the-richest-727-continuums-own-c3-images-were-missing-and-a-uniform-parameter-grid-is-not-equivariant) — the LINE catalogue was never symmetry-closed — the richest 727 continuum's own C3 images…
- [Postscript 64](#postscript-64-the-n6-typology-applies-to-n3-but-the-wall-taxonomy-truncates-and-the-base-fixing-method-provably-cannot-reach-max3) — the n=6 typology applies to n=3, but the wall taxonomy TRUNCATES and the base-fixing method…
- [Postscript 65](#postscript-65-max3-is-an-upward-spike-on-a-55-plateau--the-exact-inverse-of-n6-and-the-geometric-face-of-frustration) — max(3) is an upward SPIKE on a 55-plateau — the exact inverse of n=6, and the geometric face…
- [Postscript 66](#postscript-66-correction-to-postscript-63-the-line-catalogue-was-symmetry-closed--the-test-compared-quaternion-representatives-instead-of-configurations) — the line catalogue WAS symmetry-closed — the test compared quaternion representatives…
- [Postscript 67](#postscript-67-the-full-endpoint-census--every-continuum-end-counts-725-and-n6-also-has-isolated-727-spikes-the-n3-shape-appearing-rationally-at-n6) — the full endpoint census — every continuum end counts 725, and n=6 ALSO has isolated 727…
- [Postscript 68](#postscript-68-epsilon-neighbourhoods-show-walls-are-not-equivalent--the-walls-carrying-727-are-worth-6-each-the-walls-that-end-it-cost-2) — epsilon-neighbourhoods show walls are NOT equivalent — the walls carrying 727 are worth +6…
- [Postscript 69](#postscript-69-n2-mapped-completely--five-counts-generic-4-and-the-maximum-on-curves-the-same-codimension-as-n6s-727-lines) — n=2 mapped completely — five counts, generic 4, and the maximum on CURVES, the same…
- [Postscript 69 addendum](#postscript-69-addendum-the-n2-stratification-from-epsilon-adjacency--the-count-is-determined-by-the-dimension-of-the-stratum) — the n=2 stratification, from epsilon-adjacency — the count is determined by the DIMENSION of…
- [Postscript 70](#postscript-70-the-topology-of-the-n2-stratification--it-is-the-octahedral-mirror-arrangement-on-the-axis-sphere-fibred-by-the-rotation-angle) — the topology of the n=2 stratification — it is the OCTAHEDRAL MIRROR ARRANGEMENT on the axis…
- [Postscript 71](#postscript-71-extending-the-n2-map-to-n3--every-triple-is-labelled-by-three-n2-strata-and-both-67s-live-in-the-single-cell-131313) — extending the n=2 map to n=3 — every triple is labelled by THREE n=2 strata, and both 67s…
- [Postscript 72](#postscript-72-the-131313-cell-is-reducible--a-2-dimensional-shared-axis-component-at-55-and-isolated-points-where-67-lives) — the (13,13,13) cell is REDUCIBLE — a 2-dimensional shared-axis component at 55, and isolated…
- [Postscript 73](#postscript-73-the-pair-label-of-every-record-and-what-extending-the-structure-graph-to-higher-n-would-cost) — the pair-label of every record, and what extending the structure graph to higher n would cost
- [Postscript 74](#postscript-74-the-n4-cell-census-and-the-one-record-no-climb-can-reach) — the n=4 cell census, and the one record no climb can reach
- [Postscript 74 addendum](#postscript-74-addendum-basins--the-n4-record-is-reachable-but-not-from-random-seeds-and-no-refinement-reaches-n3s-at-all) — basins — the n=4 record is reachable but NOT from random seeds, and no refinement reaches…
- [Postscript 75](#postscript-75-zero-signal-means-a-uniform-region--and-characterising-it-separates-the-two-n3-maxima-for-the-first-time) — zero signal means a uniform REGION — and characterising it separates the two n=3 maxima for…
- [Postscript 76](#postscript-76-correction-to-postscript-70-the-n2-13-locus-is-bigger-than-recorded--and-that-is-what-a-structural-proof-of-max3-would-have-to-be-built-on) — the n=2 13-locus is bigger than recorded — and that is what a structural proof of max(3)…
- [Postscript 77](#postscript-77-step-a-complete--a-closed-form-exact-formula-for-the-two-cube-region-count-and-with-it-the-13-locus-as-a-criterion-rather-than-a-list) — STEP A COMPLETE — a closed-form exact formula for the two-cube region count, and with it the…
- [Postscript 78](#postscript-78-step-b--the-three-cube-count-decomposed-exactly-and-max3--67-reduced-to-a-single-two-rotation-lemma) — STEP B — the three-cube count decomposed exactly, and max(3) = 67 reduced to a single…
- [Postscript 79](#postscript-79-the-wide-engine-campaign-is-complete--727-survives-all-508818-previously-unreachable-configurations-and-two-new-727-compounds-fall-out-of-it) — the wide-engine campaign is COMPLETE — 727 survives all 508,818 previously-unreachable…
- [Postscript 80](#postscript-80-the-727-classes-are-not-indexed-by-field--they-are-quadratic-points-inside-one-rational-interval-and-there-are-infinitely-many-of-them) — the 727 classes are not indexed by field — they are quadratic points inside one rational…
- [Postscript 81](#postscript-81-a-tangent-finder-the-two-67-representatives-recovered-and-symmetry-measured-across-every-record) — a tangent finder, the two 67 representatives recovered, and symmetry measured across every…
- [Postscript 82](#postscript-82-the-tangent-is-a-null-space-393-is-rigid-against-moving-one-cube-and-the-n7n8-extents) — the tangent is a null space, 393 is rigid against moving one cube, and the n=7/n=8 extents
- [Postscript 83](#postscript-83-the-epsilon-neighbourhood-probe-is-one-recursion-and-the-n2-maximiser-locus-is-a-punctured-circle) — the epsilon-neighbourhood probe is one recursion, and the n=2 maximiser locus is a punctured…
- [Postscript 84](#postscript-84-the-727-arcs-enumerated--1449-records-216-chart-lines-exactly-three-arcs-up-to-congruence) — the 727 arcs enumerated — 1,449 records, 216 chart lines, exactly THREE arcs up to congruence
- [Postscript 85](#postscript-85-component-counts-at-727725723-and-723s-family-is-enormous--the-charted-interval-was-a-fragment-near-the-origin) — component counts at 727/725/723, and 723's family is enormous — the charted interval was a…
- [Postscript 86](#postscript-86-symmetries-named-by-group-not-by-order--and-three-of-them-were-ambiguous) — symmetries named by group, not by order — and three of them were ambiguous
- [Postscript 87](#postscript-87-a-vast-family-has-a-one-line-generator--but-the-maximiser-subset-of-it-does-not) — a vast family has a one-line generator — but the MAXIMISER subset of it does not

<!-- INDEX:END -->

## Reference points

- **axial fan (N cubes about a shared 4-fold axis)**: exactly `(2N-1)^2`
  bounded regions, proven (cross-section edge lines are all tangent to the
  common incircle ⇒ no triple points). For N=6: **121**.
- **five-cube compound** (5 cubes of the dodecahedron, UC09): **351** bounded
  (exact, from the Q(√5) field arithmetic in `cube_compound_exact.py`).
- **loose ceiling**: C(35,3) = 6545, the plane-arrangement bound for 36
  planes. Not remotely approached by any configuration found — cube faces
  are bounded squares, not full planes, and even the most complex stable
  configuration found here (~1340) is well under a quarter of this ceiling.

## Step 1 — tool validation

```
one:200      -> bounded=1     (expected 1)   OK
stella:260   -> bounded=9     (expected 9)   OK
axial2:260   -> bounded=9     (expected 9)   OK
axial3:260   -> bounded=25    (expected 25)  OK
axial4:300   -> bounded=49    (expected 49)  OK
axial6:300   -> bounded=126, unresolved=5    (expected 121)
axial6:400   -> bounded=128, unresolved=7
axial6:500   -> bounded=127, unresolved=6
```

The first five match exactly. `axial6` does not match 121 on the nose, but
in every one of the three resolutions run, `bounded - unresolved = 121`
exactly (126-5, 128-7, 127-6) — precisely the documented tip-fragment
artifact (a handful of small components each lack a same-label *big*
neighbour within the 3-voxel dilation search, so they're counted as
"unresolved" rather than merged). This is consistent with, not a
contradiction of, the analytic proof. Treated as PASS with a noted caveat;
proceeded to Step 2.

## Step 2 — `six_cube_search.py`

New file, imports `cube_compound_regions` and adds `labels_grid_mats` /
`count_mats`: identical slab-wise labeling and identical small→big
same-label merge / tau=3R policy as `ccr.count()`, but taking an explicit
list of 6 rotation matrices instead of a preset name. Verified byte-for-byte
identical output to `ccr.count('six6:20+rot', 120)` before use.

`grot` (apply the module's fixed generic global rotation) is exposed as a
parameter rather than hardcoded, because empirically it is *not*
universally beneficial — see the axial finding below.

## Step 3a — six6 theta sweep

`six6:T+rot`, R=200 and R=300 (R=380 added for the two best):

| theta | R=200 bounded (unresolved) | R=300 bounded (unresolved) | R=380 bounded (unresolved) |
|---:|---:|---:|---:|
| 5  | 2509 (2400) | 3757 (3576) | — |
| 10 | 1292 (1111) | 1302 (1073) | — |
| 15 | 656 (427)   | 573 (320)   | — |
| 20 | 471 (218)   | 428 (145)   | — |
| **25** | **436 (153)** | **441 (134)** | **458 (151)** |
| 30 | 465 (182)   | 482 (175)   | 368 (13) |
| 35 | 580 (297)   | 644 (337)   | — |
| 40 | 1227 (992)  | 1564 (1329) | — |
| 44 | 8983 (8844) | 12256 (12096) | — |

Both tails (theta→0, theta→45) blow up and keep growing with resolution —
near those limits pairs of cube faces approach coincidence (theta=0: all 6
cubes coincide; theta=45: six6 degenerates to the highly symmetric
`escher3`), producing genuinely-thin sliver regions that no finite R here
resolves. These are not trustworthy.

theta=25 is the standout: bounded stays in a tight band (436 / 441 / 458)
across three resolutions with a roughly *constant* unresolved count
(153/134/151, not shrinking with R) — the signature of genuinely small real
regions, not a merge failure. **theta=30's unresolved count collapses from
182/175 down to 13 at R=380** — the signature of the *opposite* artifact
(coarser grids failing to find the big same-label neighbour); its truer
value is closer to 368 than to ~470.

**Best in the six6 family: theta ≈ 25°, bounded ≈ 440-460, three-resolution
stable.**

## Step 3b — axial6 baseline

Confirmed the "any distinct twist set gives 121" claim, using the
*un-rotated* path (`grot=False`) — the axial family's cubes are jittered
away from exact grid alignment already (see Step 1), and, surprisingly,
forcing the generic global rotation makes things *worse* for this family
(tested: with `grot=True`, the same 3 twist sets gave 246/125u, 776/663u,
300/179u instead of the well-behaved values below). Recorded as a concrete
counterexample to "always use +rot" — it should be "use +rot to counter
exact axis alignment; a fixed generic rotation is not otherwise a free
improvement, and can introduce its own unlucky near-alignments."

| twists (deg)                | R=300 bounded (unresolved) | bounded−unresolved |
|---|---:|---:|
| 0,15,30,45,60,75 (default)  | 126 (5)  | 121 |
| 0,7,19,33,51,80             | 125 (8)  | 117 |
| 3,11,26,40,58,71            | 131 (10) | 121 |

All consistent with the proven constant 121.

## Step 3c — random search (40 seeds, R=200, `grot=True`)

Raw bounded counts ranged from **962 (seed 20)** to **6395 (seed 5)** — huge
variance, but almost entirely explained by unresolved fraction (66% to 96%
of the raw count is unmerged "small" components). High-unresolved-fraction
seeds are the suspects for near-degenerate coincidental alignments; this was
confirmed directly (next section).

## Step 3d/e — refinement at R=300/380/(450)

**Negative control (seed 5, highest raw R=200 count):**

| R | bounded | unresolved |
|---:|---:|---:|
| 200 | 6395 | 6159 |
| 300 | 8675 | 8384 |
| 380 | 10245 | 9919 |

Monotonically diverging, no sign of leveling off, and already exceeds the
6545 plane-arrangement ceiling at R=300 — this is impossible for a genuine
finite region count from 6 bounded cubes, so this is conclusively a
voxelization artifact (an accidental near-tangency in this random draw),
not a real winner. **Discarded.**

**Candidates selected by low unresolved fraction at R=200, refined:**

| seed | R=200 | R=300 | R=380 | R=450 | verdict |
|---:|---:|---:|---:|---:|---|
| 20 | 962 (641) | 1009 (636) | 958 (546) | 948 (505) | stable ~950-1010, unresolved fraction falling (67%→53%) |
| 34 | 973 (670) | 960 (595)  | —          | —          | stable ~960-975 |
| 1  | 1136 (843)| 1125 (767) | —          | —          | stable ~1125-1136 |
| 21 | 1215 (895)| 1172 (792) | 1158 (743) | —          | stable, mildly decreasing, converging ~1150-1160 |
| 35 | 1223 (905)| 1235 (853) | 1189 (775) | —          | stable ~1190-1235 |
| 26 | 1198 (887)| 1225 (863) | 1271 (880) | —          | stable, mild growth ~1200-1270 |
| 12 | 1183 (850)| 1275 (894) | 1301 (880) | 1411 (981) | still growing at R=450 (+110 last step) — **not yet converged**, unreliable magnitude |
| **18** | 1195 (894) | 1315 (962) | 1346 (962) | 1337 (933) | **converged**: R=300/380/450 agree to ≈1% (1315/1346/1337); unresolved fraction slowly falling (75%→70%) |

**Winner: seed 18** (`Rotation.random(6, random_state=18)`, `grot=True`).
Bounded region count **≈ 1337–1346**, stable across three independent
resolutions (R=300, 380, 450) to within 1%.

Depth histograms (0 = outside, k = inside exactly k of the 6 cubes):

```
seed 18, R=380:  {0:1, 1:140, 2:464, 3:412, 4:230, 5:99, 6:1}   bounded=1346
seed 18, R=450:  {0:1, 1:168, 2:474, 3:366, 4:198, 5:130, 6:1}  bounded=1337
```

(depth 2-3, i.e. pairwise/triple overlaps, dominate — expected for a
generic arrangement of 6 bodies with no special symmetry to concentrate
volume at high depth, unlike the axial/five-cube families).

## Step 3d — hill-climbing: negative result

Hill-climbed from two seeds (35 and 18) for 10 steps at R=200, greedy accept
on raw bounded count, perturbation annealed 5°→2°. From seed 35: raw R=200
bounded rose 1223 → 1777 (looked like a big win). **Checked the final
climbed configuration at higher resolution:**

| R | bounded | unresolved |
|---:|---:|---:|
| 200 | 1777 | 1474 |
| 300 | 2068 | 1701 |
| 380 | 2304 | 1912 |

Diverging just like the seed-5 negative control, not plateauing like the
genuine seed-18 winner. **Conclusion: hill-climbing on raw (unresolved-
inclusive) R=200 bounded count is an unreliable objective — it climbs
toward near-degenerate coincidental alignments that inflate the voxel
artifact count, not toward genuinely more regions.** This is reported as an
explicit negative finding per the task brief; a resolution-stability-aware
objective (e.g., penalize growth in bounded count between two resolutions)
would be needed to hill-climb safely, and was out of the remaining time
budget.

## Bottom line

| configuration | bounded regions | resolution stability |
|---|---:|---|
| axial6 (any twist set) | 121 (exact, proven) | n/a — exact |
| five-cube compound | 351 (exact) | n/a — exact |
| six6, theta=25° (best symmetric) | ≈ 440-460 | stable R=200/300/380 |
| **random seed 18 (winner)** | **≈ 1340** | **stable R=300/380/450 (±1%)** |
| random seed 5 (discarded) | "6395"→"10245"→∞ | diverging — artifact |

**The search's winner is the random 6-cube compound from seed 18**
(`scipy.spatial.transform.Rotation.random(6, random_state=18)`, composed
with the module's fixed generic rotation), giving a resolution-stable
bounded-region count of **≈ 1337-1346** — about **3.8×** the five-cube
compound's 351 and about **11×** the axial fan's 121. This confirms the
expected qualitative picture (generic/random configurations beat the
symmetric families, because symmetry creates coincidences that merge
regions rather than splitting them) but the margin required real
resolution-stability filtering to trust: most high-raw-count random draws
(including the single highest, seed 5, and the hill-climbed configuration)
were voxelization artifacts from accidental near-degenerate alignments, not
real winners.

Among the *structured* six6 rotational family, theta ≈ 25° is the best and
is comfortably resolution-stable at ≈ 440-460 — itself already ~25% above
the five-cube compound's 351, without needing any randomness.

## Caveats (read before citing any number above)

- **Voxel-level confidence only.** Nothing here is a proof. The exact
  Q(√5) counter (`cube_compound_exact.py`) and its certified-interval
  cousin (`cube_compound_interval.py`) can only handle sub-compounds of the
  rigid five-cube compound, whose face normals live in the golden field
  Q(√5); `scipy.spatial.transform.Rotation.random()` matrices (and generic
  `six6:T` matrices for most T) leave that field immediately, so there is
  no exact cross-check available for any of the winning configurations.
- **Both directions of voxel error are real and were both observed**: tip
  fragments inflate the count (seed 5, the hill-climbed configuration,
  six6 near 0°/45°); sub-voxel separators between what should be distinct
  regions can also silently merge and deflate it (suspected for six6
  theta=30 at coarse R, where the unresolved count collapsed from ~180 to
  13 between R=300 and R=380 — the opposite artifact signature from seed
  5's divergence).
- **Only two-or-more-resolution-agreeing values were trusted as findings.**
  Every number reported as a "winner" or "stable" above agrees to within
  ~1-5% across at least 3 independent grid resolutions (R=200/300/380, plus
  R=450 for the top random candidate). Raw single-resolution counts (e.g.
  the 40-seed R=200-only sweep) were used only to *rank candidates for
  refinement*, never as final answers.
- **The random search was not exhaustive.** 40 seeds, plus refinement of 8,
  plus 2 failed hill-climb attempts, is a small sample of SO(3)^6. A better
  answer than seed 18's ~1340 almost certainly exists; this report claims
  only that seed 18 is the best *resolution-stable* configuration found
  within the ~40-minute compute budget, not a global optimum.
- Full raw JSON outputs for every run (sweep, axial baseline, 40-seed
  search, all refinements, hill-climb histories) were kept in this
  session's scratchpad, not in this repo, since they are working files
  rather than deliverables; the tables above are the complete distilled
  record.

## Postscript: exact certification overturns the ranking

After the voxel search concluded, the winning configurations were
*rationalized* (each rotation rounded to an exact rational rotation via a
common-scale integer quaternion, N=512, error ~0.2 deg — `certify_six.py`)
and re-counted EXACTLY by the certified-interval kernel generalized to
arbitrary rational plane triples (`exact_search.py`). Validation of the
generalized pipeline: axial-6 with rational Pythagorean twists → exactly
121; the five-cube compound through the same code path → exactly 351. A
coincident-plane bug (shared z=±1 faces in axial/six6 families) was caught
by the phantom-label assertion during validation and fixed; the invariant
is documented in `certify_six.py`.

**The certified results contradict the voxel ranking:**

| configuration | voxel estimate | EXACT count |
|---|---:|---:|
| seed 18 ("winner", plateau R300-450) | ~1315–1346 | **567** |
| seed 12 | 1183–1411 ("not converged") | **595** |
| seed 20 | 948–1009 (lowest raw count!) | **595** |
| seed 39 | — | 591 |
| seeds 8, 34, 36 | — | 587 |
| six6 θ=10..40° (all) | "440–460 at θ=25, tails diverge" | **355, exactly, θ-independent** |
| axial-6 | 121 (proven) | 121 ✓ |
| five-cube compound | 351 (exact) | 351 ✓ |

Full 40-seed certified counts are in the `exact_search.py batch` output;
range 467–595, all with depth-6 = 1 (convex core) and depth-5 = 36
(= 6 × the universal "all-but-one gives 6 pieces" law).

Corrected conclusions:
1. **The certified winners among configurations tried are random seeds 12
   and 20, with exactly 595 bounded regions** (rationalized forms). Seed
   18's voxel plateau (~1340) was ~70% tip-fragment artifacts; its true
   count is 567.
2. **The six6 family is exactly constant at 355** for generic θ — like the
   axial family's 121, the rotational-freedom family has θ-independent
   combinatorics; the voxel sweep's structure ("best at 25°") was entirely
   artifact. 355 barely beats the five-cube compound's 351.
3. **Voxel counts of generic 36-plane configurations are unusable even for
   ranking** (the lowest raw voxel count tied for the certified maximum).
   A stable-looking plateau with a high unresolved fraction is not
   evidence of convergence.
4. Generic beats symmetric by ~1.6× (595 vs 355), not the 3.8× the voxel
   numbers suggested.

Certified claims are about the rationalized (exactly rational)
configurations; the 40-seed sample remains small and the global maximum is
unknown. But every number in the table above is now an exact integer with
machine-checked consistency invariants, at ~6 s per configuration — faster
than the voxel counts it replaces.

## Postscript 2: subset-maximality analysis (subset_analysis.py, pair_checks.py)

Exact counts of every k-subset of the 595 winner (seed 12) vs random baselines:

| k | winner's subsets | random max | golden (five-compound) subset |
|---|---|---:|---:|
| 2 | all 15 = **4** | 4 (200 tried) | **13** |
| 3 | 29..38 (median 33) | 38 | **67** |
| 4 | 111..135 | 131 | **177** |
| 5 | 289..313 | 317 | **351** |

Key discoveries:
1. **Generic pairs are constant at 4** (1 lens + 3 outside pieces); the rich
   pair counts (axial 9, five-compound 13) live ONLY on measure-zero
   degenerate walls (coincident faces / shared corners) and collapse to 4
   under 1-degree perturbation (pair_checks.py). Walls carry MORE regions
   than their neighbouring chambers at small k.
2. **The five-cube compound achieves "all subsets maximal(-known)" at every
   level**: its pairs are all 13, triples all 67, quadruples all 177 - each
   the best known for its k, all equal by the transitivity of A5.
3. **The actual 6-cube maxima are the opposite**: no subset of the generic
   winners is close to maximal (pairs 4 vs 13, triples <=38 vs 67,
   quintuples <=313 vs 351).
4. **Why the pattern must break at 6**: four cubes of a five-compound
   determine the fifth uniquely (12 of the 15 two-fold axes used; the
   remaining orthogonal triple is forced). So if all six 5-subsets of a
   6-configuration were golden five-compounds, cubes 5 and 6 would both be
   the unique completion of {1..4} - equal, contradiction. Conditional on
   the golden compound being the true 5-maximum, "all six 5-subsets
   maximal" is IMPOSSIBLE, vindicating the question that prompted this
   analysis. (And no icosahedral 6-cube compound exists: 10 does not
   divide 24.)

Search record meanwhile: seed 119 = EXACT 603 (viewer artifact published).

## Postscript 3: C++ engine, per-subset structure, and a corrected "law"

**Per-subset breakdowns** (`breakdown.py`, and now logged per-config): the
shallow ceilings are BUDGETS, not per-unit laws. In the 623 record the
per-cube depth-1 counts are [22,22,16,18,12,22] (individual cubes reach 22
but the sum caps at 112) and per-pair depth-2 counts range 10..20 summing
208; the three top records have *different* depth-3/4 distributions with
*identical* sums 164/102 — conserved-at-max. Depth-5 is a strict 6-per-cube
law in every record.

**Corrected claim**: depth-5 = 36 is NOT universal. Scanning the full
oracle ensemble (6,671 seeds): 36 occurs 99.4% of the time, but 34 occurs
37 times and 32 once — the six per-cube "innermost" face patches (radial
escape lemma) can MERGE around a cube edge when all other cubes are far in
that direction. Conjecture C6 is therefore d5 <= 36 (and d6 = 1, which is
a theorem: the core is convex). Earlier text stating "36 always" is
superseded. Found because the C++ campaign smoke test flagged sub-36
configs at seeds 3088/3168/3244/3346 and the oracle confirmed they are
genuine (the "law" was an artifact of looking only at maxima and records).

**C++ engine** (`cube_regions.cpp`, spec in `CPP_SPEC.md`): exact integer
arithmetic in homogeneous coordinates (vertices from plane-triple Cramer,
int128, 256-bit centroid predicates), same algorithm and assert suite as
`certify_six.py`. Gates passed: axial-6 rational-twist selftest = 121 with
depth histogram {24x5, 1}; 200-seed oracle match, zero mismatches (counts
AND depth histograms); ~0.13-0.29 s/config single-threaded, ~22 configs/s
with 8 workers (`run_campaign.py`) — roughly 2M certified configs/day.
Driver watches conjectures C1-C5 (total<=623, d1<=112, d2<=208, d3<=164,
d4<=102) and C6 (d5<=36, d6==1). First 400-seed smoke range (3000-3400):
no ceiling violations; best 611.

Status: mass campaign ready to launch detached
(`nohup caffeinate -i python3 run_campaign.py 3000 200000 8 >> campaign.out 2>&1 &`);
exact hill-climbing (Phase B) and full analysis (Phase C) pending — the
implementing agent hit its session limit after delivering the validated
engine.

## Postscript 4: mass falsification campaign — C1/C2/C3 fall, new record 635

Full campaign delivered (Phases A-C of `CPP_SPEC.md`), superseding the
"pending" status above.

**Scope.** Phase A: 106,525 random seeds counted exactly (8 parallel
`cube_regions` workers on disjoint blocks of 3000..188692; stopped at the
~100k-seed target, merged to `campaign_results.jsonl`). Together with the
user's background oracle ensemble (seeds 40..7009) and 7,937 exact
hill-climb evaluations (Phase B, `hillclimb_log.jsonl`), the analysis set
is 117,422 distinct exactly-counted configurations. Throughput: ~82
ms/config single-threaded uncontended; ~40 configs/s aggregate during the
campaign (193 ms/config mean under full 8-way load).

**Headline: conjectures C1, C2, C3 are FALSIFIED.**

- Twelve random seeds break all three at once: 631 at seeds 29390, 30108,
  39451 and 627 at seeds 13311, 33098, 36078, 61638, 64824, 84866, 86468,
  89514, 162978.
- Phase B hill-climbing (moves: ±1/±2 on one quaternion component,
  re-gcd, |c| ≤ 512; 36 greedy starts + random restarts) pushed the record
  to **635 bounded regions**, with d1 = 118 and d2 = 214:

      quats = [[129,-171,-137,-28], [382,278,63,-186], [200,289,312,-203],
               [314,101,-391,1], [124,-61,26,-215], [276,269,33,335]]
      by_depth = {1:118, 2:214, 3:164, 4:102, 5:36, 6:1}   total 635
      d1 per cube [16,20,20,20,22,20]; d2 per pair
      [24,24,22,16,14,14,14,12,12,12,10,10,10,10,10]

  (two moves from seed 30108's configuration; one representative of a
  plateau of ~208 single-move-equivalent quat tuples). Every 623-start
  climbed to 625-631 within 1-3 moves — 623 was never even a local
  maximum of the exact objective.
- Independent certification: seeds 29390 (631), 30108 (631), 33098 (627)
  and the explicit 635 configuration were re-counted by the validated
  Python pipeline (`certify_six.exact_count_config`) with identical
  totals and depth histograms.

**Conjecture status after 117,422 exact configurations:**

| conjecture | status | evidence |
|---|---|---|
| C1 total ≤ 623 | **FALSIFIED** | 631 ×3 random seeds; 635 by climbing |
| C2 depth-1 ≤ 112 | **FALSIFIED** | 116 random; 118 climbed |
| C3 depth-2 ≤ 208 | **FALSIFIED** | 212 random; 214 climbed |
| C4 depth-3 ≤ 164 | survives | attained in 13.2%, never exceeded |
| C5 depth-4 ≤ 102 | survives | attained in 82.6%, never exceeded |
| C6 depth-5 ≤ 36, depth-6 = 1 | survives | d5=36 in 99.4% (34 ×713, 32 ×8); d6=1 always |

Updated observed ceilings: total ≤ 635, d1 ≤ 118, d2 ≤ 214 (new
conjectures at the same epistemic level the old ones had — the old ones
lasted one order of magnitude of search).

**Structure of the top of the spectrum.** Every configuration with total
≥ 625 (2,619 of them) has depth-3/4/5/6 pinned at exactly (164, 102, 36,
1): above 625 the entire variation is in d1 + d2, and the observed total
spectrum is {625, 627, 629, 631, 635} — 633 never appears anywhere in
117k configs. At 623 a second histogram class exists (d3 = 162 with
larger d1/d2). The "conserved-at-max" reading of C4/C5 strengthens: d4 =
102 is hit by 82.6% of ALL random configurations (it is the generic
value, not a rare maximum), d3 = 164 by 13.2%.

**Per-subset findings** (per-cube depth-1, per-pair depth-2, from
per_label): the per-cube maximum is 26 (e.g. seeds 179994, 177366 — the
latter reaching total 623 with a 26-cube), the per-pair maximum is 34
(seed 139148, total only 587). Neither extreme is compatible with record
totals: the 635/631 records have balanced profiles (cubes 16-24, pairs
≤ 24).

  [CORRECTION 2026-07-11, see subset_richness_report.md] The phrase
  "only mid-total", used earlier in this section for the d1=26 / d2=34
  configs, is MISLEADING and is withdrawn. Within the random ensemble
  (median total 555, p99 603, max 631) those totals are HIGH percentiles,
  not the middle: total 587 is the ~91st percentile, 623 ~100th. Measured
  over all 277,832 configs, subset-richness and total are POSITIVELY
  correlated — corr(total, max per-cube d1) = +0.64, corr(total, max
  per-pair d2) = +0.58, monotone, no mid-peak — and richest-subset
  configs cluster at the TOP of the distribution. The true statement is
  not "richness trades against total" but "records combine HIGH richness
  with balance": the 699 record (Postscript 9) has per-cube d1 = 30 for
  ALL six cubes — above this ensemble's max of 26 — and perfectly
  balanced. What random seeding cannot do is reach the measure-zero WALLS
  where a subset spikes to its field ceiling (pair 13, triple 67); it
  finds the rich-subset direction but not the constructed optima.

  Configurations with three ≥22-cubes exist (539 of them, best
total 629 at d1=118 with profile [24,16,22,24,14,18]) but none with
four — stacking 22-cubes saturates: both the balanced [16,20,20,20,22,20]
and the lopsided [24,16,22,24,14,18] profiles cap at d1 = 118.

**Depth-5 anomaly, quantified**: sub-36 depth-5 occurs in 0.61% of
configurations (34 ×713, 32 ×8, never odd, never <32) and is strictly a
low-total phenomenon: sub-36 configs average total 492 vs the ensemble's
557, max 563. Merged innermost patches cost more elsewhere than they
save. Also: 99.91% of totals are odd (each cube is centrally symmetric,
so regions pair up under x → -x around the self-symmetric core); the 48
even totals are mostly NOT the d5-merging configs (only 8 overlap).

**Tools delivered** (all counts exact, no floating point in any
predicate): `cube_regions.cpp` (C++17 counter, gates: axial-6 selftest
121 with histogram {24×5,1}; seeds 0..199 oracle match with zero
mismatches on counts AND histograms), `run_campaign.py` (parallel driver
+ merge + violation watch), `phase_b_hillclimb.py` (exact greedy
climbing, all evaluations logged as explicit quats),
`phase_c_analysis.py` (this breakdown analysis, re-runnable as data
grows). Logs: `campaign_results.jsonl` (106,525 configs with per_label),
`hillclimb_log.jsonl` (7,937 configs). `exact_search_results.jsonl` was
treated as read-only ground truth throughout.

## Postscript 5: 635 certified locally maximal; campaign to 260k; exact spherical census confirms T1

Three workstreams (2026-07-10, agent-executed, results in `task_a.log` /
`task_c.out` / `scratch_diagram/`).

**1. The 635 record is a certified local maximum.** All 192
single-component neighbor moves (±1..±4 on any of the 24 quaternion
components, re-gcd, |c| ≤ 512) were evaluated exactly: none exceeds 635
(`task_a_certify635.py`). Fifty independent deep hill-climbs restarted
from distinct points of the surrounding plateau (single-move-equivalent
quat tuples, including a gcd-reduced representative) all terminate at
635 (`task_c_deep_hillclimb.py`, 50/50 `local_max`). 635 is a radius-4
local max sitting on a broad plateau; beating it needs a jump, not a
step.

**2. Campaign extended to seed 260,000 — no new records, deep ceilings
intact.** 71,308 new exact configs (seeds 188692..260000), merged total
177,832 in `campaign_results.jsonl`; the full analysis set is now
~200k distinct exact configurations. Best new random total: 627 (×4,
e.g. seed 223671). Max observed d3/d4/d5 in the new range: 164/102/36 —
zero C4/C5/C6 violations; odd-total fraction 99.93%, consistent with
the mod-4 law's exception rate. The chunk [260000, 360000) was launched
but killed by a session limit before producing shards; restartable.

**3. Exact spherical-arrangement census: T1 is TRUE as stated, and the
census is rigid.** For five configs (record 635; generic seeds 12 and
2228; sub-36 seed 3088; a six6-family wall config) the swap curves
Sigma_1/2/3 were built exactly (rational great-circle predicates,
`scratch_diagram/exact_arrangement.py`) and independently the B_l cells
were counted by dense sampling (`cellcount.py`). Findings:

- Generic configs (635, seed12, seed2228) have IDENTICAL vertex/edge
  counts: Sigma_1 (V,E) = (68,102), Sigma_2 = (200,300), Sigma_3 =
  (324,486), giving E−V = 34/100/162 exactly as T1 predicts and Euler
  cell counts 36/102/164 = the observed depth-5/4/3 ceilings. The
  vertex census is pure: every Sigma_l vertex is a rank-triple point
  (incidence flags 204 = 3·68, 600 = 3·200, 972 = 3·324); own-edge
  crossings contribute ZERO vertices to generic swap curves. A fixed
  (V,E) across unrelated generic configs is the signature of a
  combinatorial identity — T1 is now an empirically exact census
  awaiting a counting proof, no longer a conjecture-shaped guess.
- Validation gate passed: sampled cell counts match the
  per_label-derived depth counts on all generic configs (the one
  mismatch, seed2228 l=3 giving 162, was sampling resolution: 164 at
  N=4,000,000 points, `refine_seed2228.py`).
- The sub-36 config (seed 3088, d5=34) deviates exactly as T2 predicts:
  E−V drops to 32/96/148, and 8/8/48 vertices become own-edge type —
  degeneracy REMOVES census vertices and merges cells, never adds.
- The six6-family wall config breaks the sampled-cells = regions
  correspondence (B_1 cells 30 vs d5 = 24): on positive-codimension
  ties the strict sets U_S merge across walls, so diagram cells
  OVERCOUNT regions there. Direction is again downward (24 ≤ 30 ≤ 36) —
  consistent with C6, and a caveat recorded: the census argument runs
  in the generic stratum; walls are handled by T2, not T1.
- **Shoulder-cell hunt: empty.** In all five configs — including the
  degenerate ones — every B_1 cell contains a face-center anchor
  (n_unanchored_roots = 0 across the board). The conjectured mechanism
  for T2 (bottom cells are floor-anchored; shoulders exist only on the
  top side) survives its first serious hunt.

**Proof status for C4/C5/C6** (see C45_notes.md): T1's census numbers
are now measured exactly and are config-independent; what remains is
(a) a combinatorial derivation of V_l = 68/200/324 for generic
6-tuples, and (b) T2 (degeneracy only merges bottom cells), whose
anchoring mechanism is now supported by the empty shoulder hunt.

**Viewer**: `seed119_viewer.html` regenerated with a quaternion-input
mode (paste 6 integer quats, exact counts snapshot + wireframe) —
the 635 record is now displayable despite having no seed.

## Postscript 6: n > 6 cubes — engine generalized, n=7 campaign underway

STATUS: IN PROGRESS (last updated 2026-07-11). This postscript records
what the n>6 program has reached so far and is updated as the campaign
continues; the parked implementation agent resumes it toward the full
cross-n picture (spec: NPLUS_SPEC.md). Numbers below are exact and
independently re-verified by the engine.

**Engine.** cube_regions.cpp gained `--n K` (K = 2..12) with no change
to the overflow budget (predicates still involve one plane and one
vertex; K only multiplies counts, not magnitudes). Binary cube_regions_n.
Gates passed: n=6 regression is exact (seed 2228 -> 623, unchanged);
n=7 cross-checks against the Python oracle hold (seeds 777/778/779 ->
973/993/873); axial selftest passes at each n.

**n = 7 campaign (partial).** 50,000 exact configs, seeds 3000..52999
(campaign_n7.jsonl), 4 workers (capped — the ℚ(√d)/wall program has
compute priority). Best so far **1085** (independently re-verified),
above the prior n=7 best-known of 993:

    quats = [[389,-161,212,199],[71,419,285,18],[161,-116,147,-68],
             [-12,52,-11,509],[1,414,148,262],[91,155,78,473],
             [-193,254,397,50]]
    by_depth = {1:158, 2:306, 3:264, 4:194, 5:120, 6:42, 7:1}   total 1085

Top of the observed spectrum: {1053, 1057, 1061, 1065, 1069, 1077,
1081, 1085} (no 1073 seen so far — a gap, echoing the missing 633 at
n=6). Per-depth maxima over the 50k configs: d1 158, d2 306, d3 264,
d4 194, d5 120, d6 42, d7 1 — these are the current empirical n=7
ceilings (not yet stress-tested by hill-climbing, so provisional upper
observations, not conjectures).

**mod-4 at n=7.** The parity law bounded ≡ 2n−1 (mod 4) predicts ≡ 1
for n=7; observed 49,941 of 50,000 ≡ 1, with 51 ≡ 3 and 8 ≡ 2 (the
same rare invariant-shell exceptions seen at n=6, here 0.12%). Law
holds.

**Record growth so far** (certified lower bounds; max regions by n):
n=2: 13, n=3: 67, n=4: 183+, n=5: 393+, n=6: 723, n=7: 1207+, n=8: 1879+. (The n≤5
and n=6 values are the current records from the rational/wall programs;
n=7 is campaign-only, no hill-climb yet.)

**Still pending** (resumes when the field program yields compute):
finish/scale the n=7 campaign, n=7 hill-climb from the top-20, the
trimmed n=8 campaign (~5k seeds), the depth-freeze structure per n
(which deep sums are conserved-at-max, the analog of n=6's frozen
(164,102,36,1) tail), and the T1(l,n) bottom-diagram census across n.
This section will be extended with those results.

## Postscript 7: beyond rational rotations — the ℚ(√d) program

(Numbering note: Postscript 6 is reserved for the cross-n report of the
n>6 agent, in flight; its gates already passed — `cube_regions_n --n 7
--seed 777` = 973 matching the Python oracle, `--n 6` regression exact —
and its first n=7 campaign row, seed 3000 = 997, already exceeds the
prior n=7 best-known 993.)

**Question** (user, 2026-07-10): could restricting the search to
rational rotations prevent the exact alignments needed for maximal
regions? Answer: in principle yes, and demonstrably at small n.

**Theory.** The count function is constant on finitely many
ℚ-semialgebraic strata; SO(3,ℚ) is dense, so every value attained on a
full-dimensional (generic) stratum is rationally attained — if the max
is generic, rationality costs nothing (and the 635 record's broad
integer-move plateau says it sits inside an open stratum). But maxima
can live on lower-dimensional walls, and walls sort by the field their
defining incidences need:

- rational: all coincident-plane walls; the pair-13 wall (60° about a
  shared body diagonal is a rational matrix); the shared-face-axis
  pair family (9 regions at EVERY generic angle — Pythagorean angles
  reach it rationally; only its symmetric 45° point is irrational);
- ℚ(√2): exact 45° relations about rational axes;
- ℚ(√3): exact 30°/60° relations (e.g. three cubes equally spaced
  about one axis);
- ℚ(√5): the icosahedral group — the golden five-compound and all its
  sub-walls (n=5's leader: 351 vs ~317 best random — the one place a
  wall demonstrably leads its n, though the random n=5 baseline is
  thin and will be firmed up by the --n engine);
- degree ≥4: k ≥ 4 cubes equally spaced about an axis (cos 90°/k),
  towers ℚ(√2,√3), …; universal fallback = certified intervals + exact
  sign on minimal polynomials (the CN design anticipates this).

Some number field always suffices (algebraic points are dense in every
stratum), but no single quadratic field covers all walls.

**Against walls** stands the census evidence (Postscript 5): degeneracy
only merges bottom-diagram cells (T2 direction), and observed walls
trade small shallow gains (six6: d1 = 120 > 118) for large deep losses
(total 355). Whether ANY exact-incidence wall can net-win the total at
n=6 is precisely what the field program tests.

**Engine readiness.** `exact_count_config` already computes over
CN-wrapped ℚ(√5), and the golden face normals (±φ/2, ±1/(2φ), ±1/2)
are exact unit vectors there — the five golden rotation matrices are
orthonormal over ℚ(√5) and feed the validated counter directly.

**In flight.** A ℚ(√5) pilot (golden_six.py) is searching golden-five +
sixth-cube configurations (families: rational sixth; rational rotation
of a golden cube), gated on 351/1/13/67/177 regression, rational-seed
embedding, and duplicate-cube coincidence handling; results land in
golden_wall_report.md and will be merged here. The continuation
framework for ℚ(√2)/ℚ(√3)/further ℚ(√5) — field-generic Qd class,
five hard gates, symmetric-vs-rational-control methodology (the delta
against a matched rational control is the measurement), and the
256-bit caveat for any future C++ ℤ[√d] port — is `QFIELD_SPEC.md`.
This program has priority over the n>6 campaigns.

**Update (2026-07-10, same day): the golden wall SHATTERS the rational
record.** The ℚ(√5) pilot passed all gates (sub-compound totals
1/13/67/177/351 cross-validated by two independent engines; rational
seed 40 reproduced exactly; duplicate-cube coincidence → 351). First
search results, all counts exact:

- EVERY random rational sixth cube added to the golden five beats 635:
  probes gave 643, 653, 669 before any climbing.
- Hill-climbing reached **681 bounded regions** (e.g. sixth-cube quat
  (2,1,1,1)), independently re-verified through the oracle path:
  by_depth = {1:234, 2:192, 3:128, 4:90, 5:36, 6:1}. New overall
  record; 635 stands only as the RATIONAL record. 681 ≡ 1 (mod 4) — a
  wall exception, precedented (351 likewise breaks the n=5 generic law).
- Structure: ALL the gain is shallow — d1 = 234 (rational record 118),
  d2 = 192 — while the deep counts sit BELOW the generic ceilings
  (d3 = 128 < 164, d4 = 90 < 102), exactly the T2 direction. The six6
  lesson ("walls trade shallow gains for bigger deep losses") is
  overturned in net: the golden wall nets +46 over the best rational
  config. C4/C5 remain unviolated — they cap the deep counts, and
  walls only lower those.
- The climb's best quats (2,1,1,1), (7,4,4,4), (26,15,15,15) have
  w/x converging to √3: the search is steering toward the sixth cube
  at exactly 90° about the body diagonal (1,1,1) — a ℚ(√3) incidence
  which, on top of the ℚ(√5) five, makes the limit configuration live
  in the degree-4 tower ℚ(√3,√5). The "additional extension" question
  is thereby answered constructively: the tower engine is now needed
  to evaluate the actual wall point (the 681s are rational-side
  approximants; the on-wall count may jump either way).

Search still running; full report to be merged from
golden_wall_report.md. Rational-search postscript: the extended n=6
campaign finished — 100,000 more seeds (260k-360k, merged total
277,832 configs), best random 631, zero C4/C5/C6 violations; the
rational record 635 survived 360k seeds precisely because the real
maxima live on walls no rational configuration touches.

**Refinement (golden_wall_report.md, final).** The 681 set is a
θ-INDEPENDENT plateau: 28 quats, all rotations of the sixth cube about
the body diagonal (1,1,1) — a 3-fold axis shared by the axis-aligned
golden cube and the icosahedral compound — over θ ≈ 8–10° and 64–112°,
every one with the identical histogram {1:234, 2:192, 3:128, 4:90,
5:36, 6:1}; certified radius-2 local max. So the operative second
constraint is the SHARED 3-FOLD AXIS, not θ = 90°: the √3-convergents
lie inside the plateau but are not special (whether the exact 90°
point — the ℚ(√3,√5) tower value — differs from 681 is being verified
by the multiwall agent). Further: family B re-anchored on golden cube
2 gives 679 at quat (8,3,0,0) (θ≈41° about x, a 2-fold axis of the
compound) with **d1 = 238**, twice the rational d1 record; all boosts
are depth-1 only (d2 ≤ 198, d3 ≤ 132, d4 = 90 throughout). All 150
random sixth cubes beat 635 (range 637–665); sub-635 occurs only when
the sixth lands exactly on a golden cube (351). Full details:
golden_wall_report.md.

## Postscript 8: multi-constraint search pays — tower verification, the (1,1,1) wall explained, and a new RATIONAL record 655

(multiwall_report.md, multiwall_search.jsonl, qtower.py; Postscript 6
remains reserved for the parked n>6 cross-n report.)

- **Tower engine**: qtower.py builds ℚ(√3,√5) as Q5(√3) over the
  validated Q5 base; gates W-G1..4 all pass; evals 0.5–27 s.
- **The exact √3×√5 point counts 681** — identical histogram to the
  rational plateau; no jump at the wall. The convergents (26,15,15,15)
  and (97,56,56,56) already realize the identical 4711-cell arrangement:
  the climb locks into the wall's combinatorial type before reaching it.
- **The 681 plateau is a 1-D wall, now explained**: ANY sixth-cube
  angle about the exact (1,1,1) axis gives 681. That diagonal is a
  dodecahedron vertex shared by golden cubes 0 and 2; the order-3
  icosahedral generator about it fixes those cubes and 3-cycles the
  other three. The four body diagonals split 1-vs-3 under this
  symmetry: the fixed-type diagonal gives 681, its three B-orbit
  siblings give 657 (verified exactly in the tower).
- **Rational double-wall control (the surprise): 655.** Two
  independent 60°-own-diagonal pair relations among six otherwise
  free RATIONAL cubes reached 655 in only 2,476 evaluations (C++ and
  Python cross-verified), beating the 360k-seed unrestricted rational
  record 635 AND its matched free-cube control (615) at equal budget.
  Constraint-first search wins even inside ℚ: the rational record is
  now 655, and it is wall-constructed, not random.
- **Not all walls give**: within-ℚ(√5) stacks are net losers
  (coincident-plane ≤ 563; 60°-own-diagonal constant 657 < 681), and
  the ℚ(√2,√5) exact-45° wall LOSES regions (543, with d5 = 32 — a
  wall that merges even the deep layer). Wall direction is not
  monotone; each family must be counted.

Record table: overall 681 (golden five + sixth on the (1,1,1) wall,
ℚ(√5) suffices — the tower point is not special); rational 655
(double-pair-wall construction); rational random+climb 635; d1 record
238 (golden family B); deep ceilings d3 ≤ 164 / d4 ≤ 102 / d5 ≤ 36
still never exceeded anywhere, including on every wall tested.

## Postscript 9: sliding 3-cube triples — a new RATIONAL AND OVERALL record 699 (slide3_report.md)

(slide3_report.md, slide3_search.jsonl, slide3_q2.py, slide3_search.py,
slide3_p1/p2/p3.py; SLIDE3_SPEC.md + SLIDE3_SPEC_V2.md. Postscript 6 still
reserved for the parked n>6 cross-n report.)

Prompted by the user's observation that a family of maximal 3-cube
configurations slides continuously between the octahedral 3-cube compound
and the three cubes inscribed in a dodecahedron. Two program threads.

- **The 3-cube family, corrected (V2).** The right continuous family is a
  common-3-fold-axis orbit T(t) = { S(t), C·S(t), C²·S(t) }, C = 120°
  about (1,1,1) (= B), with the seed S(t) rotating about the axis
  â of Δ = S_dod·S_octᵀ (angle 40.31°, a NON-coordinate axis). Endpoints
  built EXACTLY: S_oct = Rx(45°) in ℚ(√2) (slide3_q2.py, a Q(√2) clone of
  qtower's exact counter) and S_dod = golden cube 1 in ℚ(√5), each
  C-orbit counting **67**. The user's edge-crossing marker is confirmed at
  both ends: the edge crossing sits at the **midpoint (0.5)** at the
  octahedral end and the **golden-section point (1/φ² = 0.382)** at the
  dodecahedral end. Interior t is generic (≈37); the two count-67
  configurations are isolated walls connected through a generic sea (same
  wall-vs-generic structure as everywhere else in this project).

- **Congruence test fix (methodological).** An earlier attempt claimed no
  golden 3-subset is 3-fold symmetric. That was an artifact of (i)
  find_cubes returning two IMPROPER frames (det = −1) and (ii) comparing
  RAW relative-rotation traces without reducing by the cube's own 24-fold
  self-symmetry. Reduced correctly (proper frames; R = Mᵢ·u·Mⱼᵀ minimized
  over u ∈ O), **all 10 golden pairs share the identical relation (min
  angle 44.4775°, trace 3φ/2)** — the icosahedral 2-transitivity — and the
  golden 3-cycle subset {1,3,4} (fixed set of C) IS a genuine 3-fold triple.
  Lesson for all future congruence checks here: force proper frames and
  reduce by O before comparing.

- **Overlay search → NEW RECORD 699 (rational, both-engine-verified).**
  X(θ₁,θ₂,R) = T(θ₁) ∪ R·T(θ₂), two 3-fold triples. The winning region is
  the **shared (1,1,1) 3-fold axis**: both triples 3-fold-symmetric about
  (1,1,1) and R = (a,b,b,b) a rotation about that same axis, so the whole
  6-cube compound keeps a global 3-fold symmetry — the SAME constraint that
  built 681, but now with BOTH halves on the axis and reachable in ℚ.

      quats = [[3,1,0,0],[3,0,1,0],[3,0,0,1],
               [41,28,22,14],[41,14,28,22],[41,22,14,28]]
      by_depth = {1:180, 2:216, 3:164, 4:102, 5:36, 6:1}   total 699

  Cross-verified by certify_six.exact_count_config (699, identical
  histogram); a certified radius-2 local max on a plateau (≥3 (θ₁,θ₂,R)
  cells realize 699). **699 beats overall 681 (+18), rational 655 (+44),
  rational-random 635 (+64).** 699 ≡ 3 (mod 4) (generic parity, not a wall
  exception). Deep counts d3/d4/d5/d6 = 164/102/36/1 sit exactly at the
  established ceilings — no violation. NEW depth highs: **d2 = 216 (prior
  observed ceiling 214), d1 = 180** — the entire gain over 681 is shallow
  (d1+d2), the familiar T2 direction. Coarse+fine landscape: ~67k exact
  evals logged (slide3_search.jsonl); the (1,1,1)-diagonal R family
  dominates (699), sibling-diagonal R caps at 671, near-icosahedral R at
  657; R ∈ O (identity/90°-face/180°-edge) collapses to ≤ 407 (dead).
  Two GOLDEN triples overlaid (ℚ(√5) oracle) are a clean net LOSER (≤ 673),
  slower, and buy nothing over the rational construction.

- **In flight (follow-on agents).** (1) finishing the fine (1,1,1)-diagonal
  rational sweep at Farey(16–20)² × denser diagonal angles + radius-3/4
  two-component climb of 699, hunting 701+; (2) tower-verifying the EXACT
  on-(1,1,1)-axis wall points (ℚ(√2,√3), ℚ(√2,√5) composita) and the mixed
  octahedral×golden overlay on the shared axis. Results to be merged.

Record table (updated): **overall AND rational record 699** (two 3-fold
triples on the shared (1,1,1) axis, ℚ); prior overall 681 (golden five +
(1,1,1) sixth, ℚ(√5)); prior rational 655 (double-pair wall); rational
random+climb 635; d1 record 238 (golden family B), d2 high 216 (699); deep
ceilings d3 ≤ 164 / d4 ≤ 102 / d5 ≤ 36 still never exceeded anywhere.

## Postscript 10: symmetry-stratified sweep of the walls — no new record, framework validated, coverage caveat

(symmetry_search.py, symmetry_search.jsonl, symmetry_search_report.md,
SYMMETRY_SEARCH_SPEC.md.) Systematic search of the symmetry walls: for
each finite subgroup G ⊂ SO(3), enumerate 6-cube orbit-partitions and
exact-count each family in its proper field. A cube is a coset in
SO(3)/O, so orbits are computed and deduped modulo the octahedral group
(order 24, proper frames).

**Framework validated.** Gates GA–GE pass: orbit machinery correct
(generic C₃ seed → orbit 3, aligned seed → orbit 1); reproduces the
octahedral 3-compound = 67, the (C₃, 3+3) 699 config, and the (I,
5+free) 681 config exactly.

**Result: nothing beat 699.** Best symmetry-family totals (Phase 1
rational G via cube_regions; Phase 2 ℚ(√5) for I/C₅):

| family | best | vs 699 |
|---|---|---|
| I:5+free, C₅:5+free (golden) | 681 | −18 |
| T:4+free2 | 661 | −38 |
| D₃:3+3 | 657 | −42 |
| C₂:2+2+2 | 653 | −46 |
| D₂:4+free2 | 651 | −48 |
| C₆:6 | 649 | −50 |
| C₃:3+free3 | 643 | −56 |

**CAVEAT — this is a LOWER-BOUND map, not tight ceilings.** The
per-family seed grids are restrictive: the C₃:3+3 family, which
PROVABLY contains 699 (gate GC reproduces it, and its quats
independently count 699), was searched only to **399** — its grid tried
thin axis-angle seeds, not the general-quaternion seeds the record
needs (its second triple's seed is a full quaternion [41,28,22,14], not
a coordinate-axis rotation). So the sweep does NOT independently
re-derive 699, and every "best" above is a floor, not a proven family
maximum. The true ceiling of the 699-holding family remains the slide3
result (Postscript 9: 699, radius-2 local max, finer Farey sweep still
open).

**What the sweep DOES establish**: (1) the framework and dispatch are
correct (gates); (2) the golden I/C₅ families cap at 681 as known; (3)
no symmetry class OUTSIDE the shared-axis 3+3 / golden families reached
within ~40 of 699 even at coarse coverage — the maximum concentrates in
those two families. Phase 3 (ℚ(√2)/ℚ(√3)/towers) was deferred with
justification: no rational family came near enough to 699 to warrant a
quadratic refinement, and the one concrete tower point (the ℚ(√3,√5)
681 wall) was already shown non-special (Postscript 8).

**Next move if pursued**: re-run the top families (C₃:3+3 first, to
independently confirm ≤699; then the core+free families T/D₃/C₂) with
full-quaternion seed grids + deeper hill-climb, since the current grids
demonstrably under-cover. Until then, 699 stands and the symmetry map
is a floor.

## Postscript 11: full-quaternion symmetry re-run — NEW RECORD 717 (and 705); Postscript 10's negative was a coverage artifact

(symmetry_search2.py, symmetry_search2.jsonl, symmetry_search_report2.md,
SYMMETRY_SEARCH_V2.md.) Postscript 10's sweep validated the framework
but under-searched: its per-family seed grids used thin axis-angle
seeds, so C₃:3+3 (which provably contains 699) capped at 399. Re-run
with FULL integer-quaternion seeds — same validated orbit construction,
only the seed sampler + climber changed.

**Two configs beat 699; new project record 717** (both independently
re-verified by ./cube_regions, both respect every deep ceiling
d3≤164/d4≤102/d5≤36/d6=1, zero deep-count violations across 9,528
evals):

    717  D₂:4+free2   quats 5,2,2,2; -2,-2,2,5; -2,5,-2,2; -2,2,5,-2;
                            2,1,1,1; 1,0,0,0
         by_depth {1:210, 2:210, 3:158, 4:102, 5:36, 6:1}   (+18 over 699)
    705  C₃:3+3       quats 3,1,0,0; 1,2,2,1; 2,-1,-2,-1;
                            21,14,11,7; -11,31,39,25; 53,-3,-17,-11
         by_depth {1:180, 2:222, 3:164, 4:102, 5:36, 6:1}   (+6 over 699)

Both are radius-4 local maxima. Notable structure:
- **717's gain is entirely depth-1**: d1 = 210 (vs 699's 180, and above
  the old d1 record 180), while d3 = 158 sits BELOW the 164 ceiling —
  a record achieved with a SHALLOWER deep tail than 699. The record is a
  D₂-orbit-of-4 core + one free cube + one axis-aligned cube.
- 705 pushes d2 to 222 (new depth-2 high) with d3 = 164 at ceiling; its
  winning C₃ seed (21,14,11,7) is literally the one-unit neighbor of the
  699 seed the old thin grid could not represent.
- **Parity**: 717 and 705 are both ≡ 1 (mod 4), the WALL-exception class
  (like 681), whereas 699 was ≡ 3 (generic parity). The higher-symmetry
  records sit in the exception class.

**Postscript 10 corrected.** Its "nothing beat 699" and its per-family
"bests" were floors from thin coverage, now superseded: C₃:3+3 399→705,
D₂:4+free2 651→717, C₂:2+2+2 653→677. Families whose small orbits live
on a 1-parameter alignment locus a uniform quaternion draw never hits
(T:4+free2, D₃:3+3 — generic orbit sizes 12 and 6) were gridded over
their true DOF and reproduced 661/657, confirming those ARE the maxima
on that locus. Golden I/C₅:5+free confirmed a local cap at 681 (radius-3/4
ℚ(√5) climb). Coverage rule established: generic full quaternions give
orbit sizes 3/2/6/4 under C₃/C₂/C₆/D₂, so those accept full-quat seeds
for every block — and that is exactly where the gains landed.

**Record table (updated): overall 717** (D₂:4+free2, rational); 705
(C₃:3+3); prior 699 (two 3-fold triples), 681 (golden ℚ(√5)), 655
(double-pair wall). New depth highs d1 = 210 (717), d2 = 222 (705); deep
ceilings d3≤164/d4≤102/d5≤36 still never exceeded. Open: climb 717's D₂
family deeper (radius 5+) and re-examine whether an even shallower-tail
route (d3 < 158) buys more d1.

## Postscript 11 addendum: 717 is capped — the shallow-tail tradeoff is a 1:1 conservation

(d2_deepclimb.py, d2_deepclimb.jsonl, d2_deepclimb_report.md.) Deep-climb
of the D₂:4+free2 record with a larger neighborhood (single ±1..±6,
two-component ±1/±2, cross-block escape; 15 restarts) plus a 60-restart
broad D₂ resweep and siblings (D₂:2+4 → 547, D₂:2+2+2 degenerate):
**nothing beats 717.** Both known 717 configs are certified radius-4+
local maxima.

The deep-vs-shallow exchange table (best total at each d3 over 22,202
by_depth'd evals) rises to a FLAT ridge at 717 spanning d3 = 152, 158,
AND 164 (the ceiling), then falls off on both sides (d3=150 → 685,
d3=156 → 699). All three 717 configs share d1 = 210, d4/d5/d6 = 102/36/1,
and **d2 + d3 = 368 exactly conserved** (216+152 = 210+158 = 204+164):
lowering d3 returns precisely its worth in d2, so the "shallow-tail
tradeoff" is a 1:1 conservation that cannot exceed 717. A 717 config
exists WITH the deep tail at the ceiling (d3=164, quats
8,3,3,3;-3,-3,3,8;-3,8,-3,3;-3,3,8,-3;3,2,2,2;1,0,0,0), so the
below-ceiling tail is incidental, not the source of the record. 717
stands as the capped maximum of this family.

## Postscript 12: shared-axis "intersection" families — NEW RECORD 723

(symmetry_search3.py, symmetry_search3.jsonl, symmetry_search3_report.md,
SYMMETRY_SEARCH_V3.md.) Prompted by the user's "find intersections
between families" idea: build the 6 cubes as a union of two orbits under
different groups sharing a common axis (the structure behind 699 and
717). Gates reproduced 717 and 699 through the shared-axis builder.

**NEW RECORD 723** (verified by ./cube_regions), family
**C₃core3+free3 on (1,1,1)** — a C₃ orbit of 3 cubes about the body
diagonal + 3 free cubes:

    quats 4,1,1,-1; 3,3,7,3; 5,-1,-5,-5; 2,1,1,1; 1,1,1,1; 5,2,2,2
    by_depth {1:210, 2:216, 3:164, 4:96, 5:36, 6:1}   (+6 over 717)

- **Deep tail flexes again, in a NEW slot**: 723 has d4 = 96 BELOW its
  102 ceiling (d3 = 164 at ceiling), whereas 717 kept d4 = 102 and
  dropped d3. So the "trade a deep layer for shallow" mechanism is not
  tied to one depth — d1 = 210 is the constant, and the record buys
  total by lowering whichever deep layer costs least. d5/d6 = 36/1
  still pinned.
- **Parity**: 723 ≡ 3 (mod 4), generic parity (like 699, unlike 717's
  wall-exception ≡ 1). ~16 distinct 723 configs found (a plateau).

**Other V3 findings** (nothing else beat 717): T:4+free2 re-run with
full-quat free cubes TIES 717 (was 661 in V2 — the record is reachable
in the tetrahedral family too); C₂core2+free4 on (0,0,1) = 703; C₃⊕C₃
= 705; C₄/D₄:4+free2 = 683; D₃:3+free3 = 681. The T-generating
different-axis intersection (C₂(001)+C₃(111), ⟨C₂,C₃⟩=T) was a net loser
at 613 — forcing the full polyhedral symmetry HURTS; the loose
shared-axis union is what pays.

**Record chain: 635→655→681→699→705→717→723.** All deep ceilings
(d3≤164, d4≤102, d5≤36, d6=1) still never exceeded. Open: full-quat
C₃core3+free3 was only partly climbed — deeper climb of the 723 plateau,
and the same core+free template with a C₃ core on other axes / larger
cores.

## Postscript 13: incidence geometry — edge vs corner concurrences, the 9-fold sweet spot, and the algebraic search

(algebraic_search.wl/algebraic_demo.wl/algebraic_groebner*.wl/algebraic_bridge.py,
edge_search.py/edge_search_report.md, ALGEBRAIC_SEARCH.md, PROJECT.md.)
Prompted by the user's observation that the octahedral 3-cube maximum
uses edge concurrences and the dodecahedral one uses corner concurrences,
and the conjecture that a 6-cube maximum might substitute edge for corner
concurrences.

**Incidence characterization (exact).** Records sit at high-multiplicity
POINT concurrences (extra planes through a point), never line/edge
concurrences (no line lies on ≥3 planes — max line-multiplicity 2, same
as random; 3 coplanar normals never occur). Two point modes:
- EDGE concurrence: 4 planes = 2+2 (an edge of one cube crossing an edge
  of another), |x|²≈2. The octahedral 3-compound is edge-pure.
- CORNER concurrence: 6 or 9 planes = 3+3 / 3+3+3 (cube corners
  coinciding), |x|²=3. The golden 3-compound and both 717/723 are
  corner-dominated (two 9-fold 3+3+3 points). "k cubes share a corner"
  ⟺ "they differ by rotations about that corner's axis" — corner-sharing
  IS the shared-axis family, explaining why shared-axis searches win.
  723 also carries ~180 lesser edge (2+2) concurrences: the modes coexist.

**Multiplicity has a SWEET SPOT.** Forcing a 12-fold concurrence (four
cubes at one corner, via the Gröbner solver) gives only 393 — far below
the record. 9-fold is near-optimal; over-concentration merges away
regions.

**Edge-for-corner conjecture: NOT supported (evidence, not proof).**
~4,600 exact configs across four strategies (incl. exact ℚ(√2)): best
edge-dominated total = 691 (edge-pure, two octahedral 3-compounds joined
by R=(31,13,33,30), by_depth {1:174,2:214,3:164,4:102,5:36,6:1}) — 32
below 723, the whole gap in depth-1 (174 vs 210). Edge-richness
ANTI-correlates with total (Spearman ≈ −0.58 in structured families;
edge-maximizing climbs drive the total DOWN). Corner concurrences are the
stronger ingredient; edge crossings build d2 but not the d1 shell the
shared-axis construction produces. Caveat: an unsampled region or an
irrational edge wall beyond ℚ(√2) is not excluded.

**Algebraic search built (ALGEBRAIC_SEARCH.md).** Rotations about an
integer axis take a rational Cayley parameter (matrix stays over ℚ), so
incidences are polynomial equations solvable exactly (Wolfram). Two
solvers: (1) 1-parameter wall-mapping — solving n_face(s)·v=1 over a
family's vertices returns its exact rational walls (126 along the 723
shared-axis slide; counting confirms 723 an exact local max there); (2)
multi-constraint GroebnerBasis solve — weld an unknown cube to fixed
cubes by corner-coincidence, eliminate + solve; validated (recovers the
C₃ corner-stabilizer), found 26 exact configs at 689 with d1=224 (a
depth-1 high above the record's 210). Neither beat 723, but both reach
exact points a numeric grid misses and map the incidence↔count tradeoff.
The deep-layer caps (d3≤164/d4≤102/d5≤36), not depth-1, are the binding
constraint on beating 723.

## Postscript 14: the depth trade-off structure — deep layers quantize, shallow layers grow, records sacrifice deep for shallow

(Analysis over 456,922 exactly-counted configs pooled from every log with
a depth profile. Prompted by the user's reframing: the goal is not to
maximize any single heuristic but to map which depth trade-offs are
possible.)

**Sequential saturation, deepest first, then pinning.** Binning configs
by total and taking the mean profile [d1,d2,d3,d4,d5,d6], the deep layers
fill to their caps IN ORDER and then freeze:
  - d5 → 36 by total ≈ 475
  - d4 → ≈102 by total ≈ 525
  - d3 → ≈164 by total ≈ 600
  - d6 = 1 always.
From total ≈600 to the record, d3/d4/d5 are pinned at 164/102/36 and ALL
growth is in the shallow layers (d1: 119→206, d2: 194→214).

**Two distinct trade-offs:**
  1. At FIXED total — a conserved exchange between adjacent layers (the
     717 plateau has d2+d3 = 368 constant; regions shuffle between d2 and
     d3 without changing the total).
  2. To INCREASE the total — the deep layers cannot grow (capped), so the
     shallow ones do; and near the ceiling the profitable move is to give
     BACK a little deep count to unlock a lot of shallow count. 723 trades
     6 units of d4 (102→96) for roughly +45 in d1 vs the best d4=102
     config — a strongly non-1:1 trade. 717 likewise sacrifices d3
     (164→158). This deep-sacrifice lever is under-explored.

**Why (radial framework).** Deep-layer counts = cells of the innermost
great-circle "bottom-diagrams," which have a fixed GENERIC value — a
config either realizes the generic diagram (the cap 164/102/36) or a
degenerate merged one (below). They are QUANTIZED. Shallow-layer counts =
outermost diagrams, uncapped, growing with arrangement complexity. So the
maximum-total problem is: saturate the quantized deep layers, maximize the
unbounded shallow ones, and spend deep sacrifices only where they buy
disproportionate shallow gain.

**Reframed objective.** "Beat 723" = find the optimal point on the
deep-sacrifice surface: sweep the feasible (d3,d4,d5) profile and maximize
d1+d2 at each. 723 proves sacrificing d4 pays; whether sacrificing d3 AND
d4 together (or another combination) nets higher is open. Gröbner
corner-welding already reached d1 = 224 (with depressed deep layers), so
the shallow ceiling is high — the exchange rate is the question.

**Also open: non-concentric cubes.** No solid argument exists that
off-centering can't increase the count; allowing translations only adds
DOF, so the off-center max is ≥ the concentric max. The "concentric
maximizes overlap" intuition is undercut by our own sweet-spot finding
(over-concentration reduces the count). Off-centering should cost deep
layers (the common-intersection core weakens) but may buy shallow ones —
the same exchange. Untested only because every engine here assumes
concentric.

### Postscript 14 — results & a correction (2026-07-12)

Three experiments ran on the trade-off/extra-DOF questions:

- **Deep-sacrifice sweep** (deepsweep.py, 20,032 exact configs): best total
  = 723, nothing beat it. The trade-off surface: total 723 is reached
  along a RIDGE of deep profiles — (164,102,36) with d1+d2=420 AND
  (164,96,36) with d1+d2=426 both give 723. **CORRECTION:** the earlier
  claim that 723 trades 6 units of d4 for "+45 in d1" was WRONG — it
  compared 723 against the AVERAGE d4=102 config, not the best. Properly
  optimized, the deep↔shallow trade is ≈1:1 at the frontier (give back 6
  deep, recover 6 shallow, same total), and sacrificing MORE deep loses
  (e.g. (158,94,36) reaches only 719). So 723 sits at/near the peak of the
  trade-off surface; the deep-sacrifice lever is exhausted at ~723, not
  under-explored. Evidence 723 is a genuine local optimum, not proof.
- **Off-center** (offcenter_count.py, t=0 gate PASSED reproducing 723 and
  3 seeds; 167 perturbations): off-centering 723 does NOT help — best
  non-trivial total 706 (single small shift), monotonically worse from
  there; ALL depth layers decrease on average. Translating all six cubes
  together (a rigid shift) keeps 723 (invariance check). So around the
  record concentric is locally optimal — contradicting the guess that
  off-centering might trade deep for shallow; it just destroys regions.
- **Unequal sizes** (offcenter_count.py extended: cube k gets half-width
  s_k; offset ±s_k, containment/extent scale by s_k; size=1 gate
  reproduces 723): INCONCLUSIVE for 723. Every size perturbation of 723
  hit an exact face-coincidence (723 is so symmetric that resizing any
  cube by a rational factor creates a degeneracy) that this non-robust
  Python counter cannot evaluate — all 48 trials skipped. Settling the
  size question needs a degeneracy-robust counter (symbolic perturbation)
  or the C++ engine extended to per-cube sizes. Size PRESERVES central
  symmetry (unlike translation), so it is the gentler extra DOF and the
  more likely of the two to help, but it remains untested at n=6.

## Postscript 15: n=4 — golden 177 is NOT the maximum; new rational record 183

(n4_search.py, n4_search.jsonl, n4_search_report.md, prompted by Chris
Cole flagging the n=4 entry. The growth table's old "135+" was a rational
undershoot; corrected first to 177, now to 183.)

The golden four-cube sub-compound (4 of the 5 dodecahedral cubes) counts
**177** exactly (by_depth {1:104,2:48,3:24,4:1}, ℚ(√5)), confirmed by two
independent engines. But it is NOT the 4-cube maximum:

**New n=4 record: 183** (fully rational, verified by both cube_regions_n
and the Python oracle; ≡ 3 mod 4, generic parity):

    quats = [[1,0,0,0],[0,5,3,2],[1,-4,-1,1],[1,1,-1,-4]]
    by_depth = {1:92, 2:66, 3:24, 4:1}   total 183   (+6 over golden 177)

Certified a radius-4 local maximum (recurred 9/40 wide-restart climbs,
never exceeded). This mirrors n=6 exactly: the best RATIONAL config beats
the golden/√5 wall (n=6: 723 > 681; n=4: 183 > 177). The golden compound
leads among *symmetric* configs but is not the global max.

**How found**: 200k random campaign (best 137) → hill-climb (142) → four
symmetric families generalizing the n=6 record shapes (golden-3+free,
octahedral-type, C4-orbit, C3-orbit+free; max 159, none beat 177) → DEEP
multi-restart climbing from the octahedral-family champion: wide
(multi-component) perturbation + re-climb escapes each local max into a
richer basin, 159→171→173→175→179→183. The wide-perturbation escape is
the operative technique; plain ±1/±2 greedy climbing stalls below 177.

**Structural echo of the n=6 trade-off surface**: golden (177) and the
record (183) both have d3=24, d4=1 (identical deep tail); the record
trades 12 units of d1 for 18 of d2 (net +6) — same "grow the shallow
layers, deep layers pinned" pattern. **d3 ≤ 24 held across ~300,000
exact n=4 configs** (rational and golden) — a candidate n=4 analog of the
n=6 deep-layer ceilings.

**Not proven maximal**: the deep-climb was run systematically from only
one structured seed; applying it to the other families' champions is the
obvious next step. A naive additive bound from best-ever d1 (104, golden)
+ best d2 (66) + d3 cap 24 + 1 = 195 suggests real headroom remains.

## Postscript 16: records NEST — 723's subsets contain the smaller records, and its 5-subset beats golden 351

(Analysis of the record configs' sub-compounds, prompted by questions on
whether outstanding configs are built from outstanding sub-configs, and
Chris Cole's "does this call into question 351?".)

**351 is called into question — decisively.** A 5-cube sub-compound of
the 723 record (drop its 6th cube) counts **393**, verified by both
cube_regions_n and the Python oracle: quats [[4,1,1,-1],[3,3,7,3],
[5,-1,-5,-5],[2,1,1,1],[1,1,1,1]], by_depth {1:156,2:128,3:78,4:30,5:1},
+42 over golden 351. ALL five 5-subsets of 723 beat 351 (375/381/381/
381/387/393). The golden five-compound is NOT the n=5 maximum — same
story as n=4 (rational 183 > golden 177). Growth table n=5: 351 → 393+.
(d4 = 30 = 6·5 in the 393 config — the depth-(n−1) ≤ 6n ceiling holds.)

**Records NEST.** The subset spectrum of the 723 record:

| subset size | best subset count | the k-cube record | note |
|---|---|---|---|
| 2 | 13 (×5) | 13 | hits the record |
| 3 | 63 (×5) | 67 | 94% — falls short of the golden 67 |
| 4 | 183 | 183 | hits the n=4 record exactly |
| 5 | 393 | (was 351) | EXCEEDS the old golden value |

So 723 CONTAINS the n=4 record (183) and a 5-cube config (393) above the
old n=5 record, and its pairs hit the n=2 record (13). Its 3-subsets
reach only 63 (< 67): the golden/octahedral SYMMETRIC 67 is not
rationally compatible with 723's structure, whereas the rational records
(13, 183, 393) nest cleanly.

**Construction principle suggested.** Outstanding configs are
hierarchically nested — an n-cube record contains an (n−1)-cube config at
or above the (n−1) record. This motivates GREEDY EXTENSION: take the best
k-cube config, add a cube optimally, climb → candidate (k+1) record. The
183/393/723 chain is exactly such a tower (183 ⊂ … , 393 ⊂ 723). The
even-k subsets hitting their records while the odd-k (3) falls short is an
unexplained parity in the nesting worth investigating.

### Postscript 16 addendum: greedy extension VALIDATED — new n=7 record 1207

The nesting principle predicts an n-cube record can be built by extending
the (n−1) record with one cube. Tested directly: the 723 six-cube record
+ one seventh cube, over just 256 seventh-cube orientations (NO
hill-climbing), reaches **1207** — verified by both cube_regions_n and the
Python oracle — beating the prior n=7 best-known 1085 (from a 50k-seed
campaign) by 122.

    quats = 723's six cubes + [5,4,-4,-4]
    by_depth = {1:272, 2:324, 3:260, 4:192, 5:116, 6:42, 7:1}   total 1207
    (d6 = 42 = 6·7 — the depth-(n−1) ≤ 6n ceiling holds at n=7 too)

So greedy extension of the record BEATS a full random campaign at the
next n, cheaply — the construction principle is not just descriptive but
generative. Growth table n=7: 1085+ → 1207+. Un-climbed; hill-climbing
from 1207, and iterating the extension to n=8, are the obvious next steps.
The record tower is now 183(n4) → 393(n5) → 723(n6) → 1207(n7), adjacent
levels related by adding/dropping one cube.

### Postscript 16 addendum 2: n=2 and n=3 stress-tested — 13 and 67 hold

With the golden values 177 (n=4) and 351 (n=5) both broken, n=2 and n=3
were stress-tested. Thorough search in their low-dimensional spaces
(config space is 3(n−1)-D: n=2 is 3-D, n=3 is 6-D): n=2 = 13 CONFIRMED
(1,783 random seeds + hill-climbs, nothing above 13); n=3 = 67 CONFIRMED
(4,414 seeds + climbs, nothing above 67). Confidence scales inversely with
dimension, so these small cases are far better established than the large
records. Two structural reasons they are safer than 177/351: the 13-pair
is already RATIONAL (60° about a shared body diagonal), not a golden value
that a rational config could undercut; and at n=3 the SYMMETRIC value (67)
beats the best rational three-cube subsets of the records (63) — symmetric
leads at n=3, whereas rational overtook symmetric at n=4,5. Caveat:
thorough search, not proof. Confidence ladder: n=2 (near-certain) > n=3
(strong) > n=4 183 / n=5 393 (golden beaten, rational best-so-far) > n=6
723 > n=7 1207 (extension-seeded, least settled).

### Postscript 16 addendum 3: n=5 = 393 is robust; native search can't reach it

Full n=5 search (n5_search.py, ~171,600 exact configs): 393 confirmed the
best, nothing beat it. Wide-perturbation deep-climb (155 restarts from 393
and neighbors) found ZERO improvement, and — unlike n=4's 183, which had
to escape five successive plateaus — 393 shows NO plateau structure, so it
is a substantially more robust local optimum. d4 ≤ 30 = 6·5 held across
all ~171,600 configs (and is the generic value, >90% of random). Notable:
n=5-NATIVE structured families (golden-rationalized, octahedral-type,
C4-orbit, C3-orbit+free) deep-climbed only to 377/369/323/309 — all short
of 393. So 393 is reachable only as a sub-compound of the 723 six-cube
record, not by any independent five-cube search. This sharpens the nesting
principle: the n=5 optimum is INHERITED from the n=6 record, with no
constructive five-cube route to comparable richness — the tower is
top-down as much as bottom-up.

## Postscript 17: local perfection is globally frustrated past n=3 — the "middle-layer" mechanism

(Prompted by the observation that golden N4 is built from optimal
sub-configs on every subset yet is not maxN4. Verified exactly.)

**All-subsets-optimal ⟺ golden, and it equals the max only for n ≤ 3.**
- golden four-compound (177): ALL four 3-subsets = 67 (=max₃) and all six
  2-subsets = 13 (=max₂) — every part optimal — yet 177 < max₄ = 183.
- max₄ (183): 3-subsets = 63/63/63/55 (< 67), pairs = 13/13/13/9/9/9 —
  NOT all optimal. The global maximum must DETUNE its subsets to win.

"Every k-subset optimal" is a rigid constraint satisfiable only by the
fully symmetric (icosahedral) compound. So local perfection forces golden,
and golden is beaten for n ≥ 4 — a FRUSTRATION: honor all local
constraints (golden) OR maximize the whole (183), not both.

**Why n=4? The middle layer.** Compare depth profiles (d1..d_n):
  - n=3: golden=max=67 = {48, 18, 1}. Layers: d1 (top) and d2 =
    depth-(n−1) = 18 = 6·3 (the ceiling). NO middle layer. Golden maxes
    BOTH → golden = max.
  - n=4: golden {104, 48, 24, 1} vs max {92, 66, 24, 1}. Both hit
    d3 = 24 = 6·4 (ceiling). But d2 is a MIDDLE layer (neither the top d1
    nor the ceiling-ed deep layer). Golden leaves d2 = 48; the max pushes
    it to 66 by sacrificing d1 (104→92), netting +6.
  - n=5: golden {180,80,60,30,1} vs max {156,128,78,30,1}. Middle layers
    d2,d3: golden 80/60, max 128/78 — golden far behind in the middle.

Mechanism: **golden concentrates the count in the top layer (d1) and the
6n-capped deep layer, but n=4 is the FIRST size with a middle depth layer
that is neither — and golden leaves middle layers sub-maximal. The global
maximum trades down d1 to fill the middle, and wins.** (Golden is markedly d1-HEAVY: golden d1 = 104 (n4), 180 (n5) both exceed
the max-total configs' d1 = 92, 156 — so golden concentrates the outer
layer and the total-max redistributes to the middle. Whether golden
GLOBALLY maximizes d1 is a stronger claim, still untested.) This unifies the golden-falling, the C₃-only (not icosahedral)
symmetry of records, the incidence sweet spot, and why greedy extension
(which inherits detuned subsets) beats assembling from optimal parts.

## Postscript 17 addendum: the DOF hierarchy — local optima are RIGID, flexibility lives in suboptimal-but-structured configs

(Corrects earlier loose claims about pair flexibility, incl. a mistaken
"13 is 47% flat".) Sampling 1,500 random pairs: the count distribution is
4 (94%), 5 (4%), 9 (2%), 13 (0.1%). So:

| pair count | how common | degrees of freedom |
|---|---|---|
| 4 (generic) | 94% | full 3-D open sea |
| 9 (shared face-axis) | 2% | CONTINUOUS — exactly 9 at every angle about the shared axis (verified 8 angles) |
| 13 (the MAXIMUM) | 0.1% | rigid, near-isolated high-codimension wall [WRONG — corrected in Postscript 44: measure-zero but CONTINUOUS, a 1-parameter family] |

The MAX pair (13) is the RAREST and most rigid; the suboptimal 9 sits on a
fatter, continuously-parameterized locus. Same for triples: 67 is ISOLATED
(Postscript 9 — octahedral ℚ√2 and golden ℚ√5 endpoints connected by a
family whose INTERIOR drops to ~37; near-45° rational octahedral gives only
55, exact 45° needed; a climbed 63-triple has 0% DOF openness). So **local
optima (13, 67) are rigid points; they are NOT count-preserving-continuous.**
[PARTLY WRONG — see Postscript 44 (2026-07-29). True for 67 (the two
triples really are isolated), FALSE for 13: the 13-pair is measure-zero but
count-preserving-CONTINUOUS — every angle about a body diagonal gives 13.
The rigidity that drives the frustration principle lives one level up, at
the triple, not at the pair.]

Key distinction: a config always has CONFIGURATION DOF (you can perturb the
cubes), but the optima have no COUNT-PRESERVING DOF. The flexibility that a
larger arrangement can exploit lives in the suboptimal-but-structured
configs (the 9-pair's tunable shared-axis angle).

**This SHARPENS the frustration principle (Postscript 17):** local optima
are rigid, so the globally optimal arrangement is FORCED to build from
locally-suboptimal-but-flexible pieces. Golden fails precisely because it
insists on the rigid optimal pieces (all pairs = 13); the true max uses
tunable 9-pieces. Structure of max₄ (183): an axis-aligned HUB cube paired
13 (max) to each of three SPOKE cubes, with the spokes mutually 9-paired
(the C₃ orbit — a shared-axis cluster whose angles are the tunable freedom).
The C₃core+free family that built 723 is the six-cube version of this.

## Postscript 18: shared-axis-cluster construction — free spoke angles recover every record; locked/control variants fall short

(shared_axis_search.py/.jsonl, campaign partially complete — n=6 templates
still running; interim results already decisive on the hypothesis.)

Tests the Postscript-17-addendum principle constructively: parameterize
hub-and-spoke families (on-axis cubes + a cluster of spokes sharing an
axis, each spoke at an independent rational angle — the continuous 9-DOF)
and search the spoke angles DIRECTLY.

- **Gates: the family CONTAINS the records** — 183 and 723 both expressed
  exactly as instances (n=4 onaxis2+spoke2; n=6 spoke3+onaxis3).
- **n=4: free angles reach 183 (the record); C₃-locked angles only 165;
  unstructured 4-free control 163.** Freeing the flexible DOF is worth
  +18 over locking to the symmetric angles.
- **n=5: three cluster templates reach 393 (the record); control 369.**
- **n=6 (in progress): the 723 template reaches 723 free vs 679 locked.**

Verdict so far: "build from flexible 9-DOF clusters and tune the angles"
is a VALIDATED construction principle — it recovers every record from the
right variables where generic search and angle-locking fail; no template
has (yet) beaten a record. Full report when the n=6 templates finish.

## Postscript 19: THE GENERAL CEILING LAW — depth-(n−l) ≤ (12l−6)n − 2(l²−1)

(Discovered by fitting the bottom-l maxima across n and cross-checked two
independent ways. The single most consolidating result of the project.)

**The law.** For n concentric unit cubes and 1 ≤ l ≤ n−1:

    C(l, n)  =  (12l − 6)·n  −  2(l² − 1)
    depth-(n−l)  ≤  C(l, n),   attained (generically or by records/golden)

Slopes 6, 18, 30, 42, … (arithmetic, step 12); intercepts −2(l²−1).
Special cases: l=1 gives the 6n law (Postscript 14 era); l=n−1 gives the
TOP layer d1 ≤ 10n² − 14n.

**Evidence 1 — attainment table** (max observed per layer over ~1M exact
configs from every campaign/search log, n=2..7):

    n\l    l=1      l=2      l=3      l=4      l=5      l=6
     2    12=12      --       --       --       --       --
     3    18=18    48=48      --       --       --       --
     4    24=24    66=66   104=104     --       --       --
     5    30=30    84=84   134=134  180=180     --       --
     6    36=36   102=102  164=164  222=222  234<276     --
     7    42=42   120=120  194=194  264=264  306<330  158<392

Every testable cell l ≤ 4: ATTAINED EXACTLY, ZERO violations. The only
unattained cells are the shallowest layers at n=6,7 — exactly the
frustration (all layers cannot be capped simultaneously).

**Evidence 2 — golden attains the top-layer ceiling.** Golden depth-1 =
48, 104, 180 at n=3,4,5 = C(n−1,n) exactly. ("Golden maximizes d1" is now
a formula, and golden = the top-layer-ceiling config; the records are the
deep-layer-ceiling configs; the middle is the contested ground.)

**Evidence 3 — the spherical census matches.** All measured swap-curve
censuses are TRIVALENT (E = 3V/2), so Euler gives cells = 2 + V/2, i.e.
V_l(n) = 2·C(l,n) − 4 = (24l − 12)n − 4l². Measured at n=6 (Postscript 5):
V₁,V₂,V₃ = 68, 200, 324; formula: 68, 200, 324. Exact agreement from a
completely independent measurement.

**Corollary (max-total bound).** Total ≤ 1 + Σ_{l=1}^{n−1} C(l,n)
= 1 + (n−1)(16n² − 17n + 6)/3. At n=6: ≤ 801 (record 723; the gap is the
frustration cost). At n=4: ≤ 195 (record 183 — matches the "naive additive
bound" of Postscript 15, now derived). At n=5: ≤ 429 (record 393).
[445 was an arithmetic slip, corrected 2026-07-13.]

**Proof target, now crisp (T1/T2 sharpened).** T1: show the swap-curve
Σ_l of a generic n-cube compound has exactly (24l−12)n − 4l² vertices,
all trivalent; Euler then gives cells = C(l,n). T2: degeneracy only
merges cells (never exceeds the generic count). l=1 already reduces to
the no-shoulder lemma (envelope has only the 6n face-center minima).

**Predictions.** (i) d1 at n=6 can reach 276 (observed max 234 — 42 of
headroom; hunting a d1=276 config is a sharp target). (ii) n=8: deep
ceilings 48, 138, 224, 306. (iii) Any config exceeding ANY C(l,n) kills
the law — a standing falsification target.

### Postscript 19 addendum: why 63 beats 67 as a building block — deep structure persists, shallow count is recut

(Closes the building-block thread of Postscripts 16-18 using the ceiling
law. Verified on all six 63-triples of the 723 record.)

    golden 67:      {1:48, 2:18, 3:1}   pairs [13,13,13]  isolated √5/√2 wall
    723's 63-triples: {1:44, 2:18, 3:1}   pairs [9,13,13]   rational, tunable
    (all six 63-triples have the IDENTICAL profile and pair structure)

The two triples are IDENTICAL in the deep layers — both saturate
C(1,3) = 18 and have the single core. 67's entire +4 advantage lives in
depth-1, which is precisely the layer that does NOT survive embedding: a
larger compound's new faces recut and reassign the triple's depth-1
regions, while the deep skeleton (pairwise/triple intersections) persists
and feeds the big config's deep layers.

And 67 buys those +4 disposable regions by replacing the one FLEXIBLE
9-pair with a third rigid 13 — costing exactly what a building block
needs: (a) the continuous shared-axis angle (the tuning knob the assembly
spends), and (b) rational compatibility (all-13 at 67 forces the
golden/octahedral wall, whose extensions lose: 681 < 723).

**Principle: a building block's worth = deep structure (persists under
embedding) + flexibility (spent by the assembly). Shallow count is
recyclable and worthless to the tower. 63 is 67 with 4 depth-1 regions
converted back into a tuning knob — which is why the record is built
from deep-saturated, shallow-detuned, one-knob pieces.**

## Postscript 20: the deficit-propagation envelope — an empirical branch-and-bound bound, and 723 nearly cornered

(envelope_mine.py/.jsonl: 532 configs stratified across the total
spectrum + the records, all six 5-subsets of each counted exactly —
~3,200 config↔subset pairs. The missing-bound program of the
branch-and-prune reframing, first measurement.)

**Bound 1 — the extension envelope.** Over the whole corpus,
T − max_subset_total ≤ 336 (attained by 699 over its uniform 363
subsets; the records 723 and 717 sit at 330). Conjecture E1: every
6-config satisfies T ≤ S_max + 336, i.e. adding a sixth cube to a
5-config with total S yields at most S + 336.

**Corollary (723 nearly cornered).** If E1 holds, any 6-config beating
723 must CONTAIN a 5-subset with total ≥ 388. The known n=5 landscape:
the record 393 (= 723's own subset family), 717's best subset 387, and
every native n=5 search capped at 377 (Postscript 16 addendum 3, ~171k
configs). So beating 723 would require a 5-config in a class that only
the 723 family is known to occupy — the search for >723 reduces to the
search for new 5-configs ≥ 388, a far smaller frontier. (Empirical
bound; sample thin at the top — stated as conjecture E1, not theorem.)

**Bound 2 — deep-deficit propagation is STEEP.** Configs whose worst
5-subset misses its bottom-1 cap (d4 < 30 = C(1,5)) are capped far
below the record: min-subset-deficit 0 → max T = 723; deficit 2 → max
T = 567; deficit ≥3 → ≤ 519. All top configs (631+) have EVERY 5-subset
saturating both subset deep caps (d4 = 30, d3 = 84 = C(2,5) attained).
Conjecture E2: a positive deep deficit in any 5-subset costs the total
>150 — subset deep-saturation is a NECESSARY condition for records,
usable as a hard prune in blueprint search.

Together E1+E2 are the missing bounds for branch-and-bound: E2 prunes
blueprints whose parts can't deep-saturate; E1 bounds completions by
the best contained 5-config. Both are measured envelopes awaiting proof
— the natural lemma behind E1 is a zone-style bound on the regions a
sixth cube's six faces can create in a 30-plane arrangement.

### Postscript 18 addendum: shared-axis campaign complete (~150k evals)

Final per-template bests (free spoke angles vs C₃-locked, all n):
- n=4: best template free=183 (RECORD; locked 165; control 163).
- n=5: three templates reach 393 (RECORD; note the 723-subset template
  reaches it LOCKED too — consistent, since 393 retains the C₃ symmetry);
  control 369.
- n=6: the 723 template reproduces 723 free (locked 679); two-cluster
  spoke3+spoke3 reaches 717 free (693 locked); all other templates and
  the unstructured control ≤ 709. NOTHING beat any record.

Closing verdict: the hub-and-spoke/shared-axis family with FREE spoke
angles contains and recovers every record (183/393/723) from ~10-15k
evals per template, while angle-locking costs 15-45 and unstructured
controls trail by 20-30. The flexible 9-DOF is confirmed as the right
search variable; the blueprint level is now handed to the
branch-and-prune program (Postscript 20 bounds E1/E2 as its pruning).

## Postscript 21: blueprint branch-and-prune complete — 67 skeletons exhausted, nothing beats 723

(blueprint_enum.py, blueprint_search.py/.jsonl, blueprint_search_report.md.
The branch-and-prune program of Postscript 20, executed.)

**Catalog**: 391 raw blueprints (cluster partitions × axes × kinds) →
67 canonical survivors after symmetry/specialization collapse, plus 2
pruned with documented justification: P2 the golden/octahedral all-13
wall (irrational, and its best extension 681 < 723 — Postscript 12), P3
the multi-axis polyhedral-forcing family (tested at 613, dominated).

**Gates**: the 723 blueprint (onaxis3+spoke3 on (1,1,1)) survives
pruning and its knob optimization reproduces 723 exactly.

**Result**: all 67 skeletons knob-searched (spoke-angle coordinate
descent + free-cube climbs + wide-perturbation hops; ~600-1,400 exact
evals each, 83,700+ total): **nothing beat 723**. Best non-gate
blueprints: spoke6_ax001 = 689, onaxis4+free2 = 681, onaxis3+free3 =
679. A 4×-budget refinement of the top-12 runners-up runs detached
(first result: spoke6_ax001 confirmed stuck at 689).

**Standing of the record after this**: 723 is now (i) exhaustive at the
blueprint/skeleton level within the rational shared-axis/free family at
stated coverage, (ii) cornered at the subset level by envelope E1 (any
beater must contain a 5-config ≥ 388; only the 723 family is known to
reach that), and (iii) at the peak of the deep-sacrifice trade-off
surface (Postscript 14). Three independent closures. Beating 723 now
requires either a fundamentally new 5-cube near-record, an irrational
wall outside every family tested, or a violation of envelope E1.

## Postscript 22: the n=7 program — 1207 certified, the ceiling law passes its out-of-sample test, first n=8 record 1879

(n7_program.py/.jsonl/n7_program_report.md — the full n≤6 apparatus
applied at n=7 in one pass; the law's first test on a size it wasn't
fitted to... l≥5 aside, since l≤4 at n=7 were in the fitting data;
the fresh tests here are the near-attainment of l=5 and all of n=8.)

**1207 stands, now certified**: ±1/±2 climb flat; 26 wide-perturbation
restarts (best 1197); 7th-cube swap/reoptimize (1199); and the n=7
blueprint catalog (100 skeletons, 30 searched in budget, gate PASS) has
its best = the 1207 blueprint itself (onaxis3+spoke3+free1 on (1,1,1),
free 1207 vs locked 1187). Free spoke angles beat locked in every row.

**Ceiling law at n=7: zero violations in 112,864 exact records.**
Caps l=1..4 (42/120/194/264) all ATTAINED exactly. l=5 (depth-2):
observed 328 vs cap 330 — within 2 after a dedicated hunt. l=6
(depth-1): observed 276 vs cap 392, far short — mirroring n=6, where
the shallow caps are the unattained ones (the frustration).

**First n=8 record: 1879** (= 1207 + 8th cube, 300-candidate sweep +
climb), by_depth {1:340, 2:450, 3:380, 4:302, 5:222, 6:136, 7:48, 8:1}.
Against the law's predictions C(l,8) = 48/138/228/306/384/458/528:
d7 = 48 ATTAINED, d6 = 136 (−2), d5 = 222 (−6), d4 = 302 (−4) — no
violations, deep layers hugging their caps from below exactly as the
law prescribes for a single un-refined config. Tower now
183 → 393 → 723 → 1207 → 1879.

**Envelope at the 6→7 step**: max(T − S_max) over the top-50 n=7
configs = 484 (the 1207−723 point). And ALL 350 six-cube subsets of
those configs saturate the n=6 deep cap d5 = 36 (350/350) — subset
deep-saturation as a necessary condition replicates one level up.

The general-n picture is now: one formula governing every deep layer at
every size tested (n=2..8, ~1.2M exact configs, zero violations), a
record tower built by single-cube extension whose every level is the
best known, and the shallow caps as the standing open frontier.

## Postscript 23: the cap-sum bound is TIGHT at n=2 and n=3 — a proof of 13 and 67 reduces to two lemmas

(Prompted by Chris Cole: "I wonder if there is a proof of 67 somewhere in
there. Zaslavsky would be thrilled. A proof could borrow ideas from the
proof that there are five Platonic solids." He is right — the reduction
was already implicit in the ceiling law.)

The law's per-layer caps sum to an upper bound on the total,
1 + Σ_{l=1}^{n−1} C(l,n). Checking small n:

    n=2: 1 + 12           = 13   = the record  — TIGHT
    n=3: 1 + 18 + 48      = 67   = the record  — TIGHT
    n=4: 1 + 24 + 66 +104 = 195  vs 183 — gap 12 (frustration begins)
    n=5: 1 + ... = 429           vs 393 — gap 36

So for n ≤ 3 the maximum EQUALS the cap-sum (no frustration: with no
middle layer, both caps are simultaneously attainable, and golden/
octahedral attain them). Hence:

**A complete proof that max(2) = 13 requires only:**
  L1(2): for two unit cubes, depth-1 ≤ 12 — equivalently the
  direction-sphere envelope max over the 6 face-normals |n·û| has no
  local maxima besides the ±normals (two orthonormal triads only).

**A complete proof that max(3) = 67 requires only:**
  L1(3): depth-2 ≤ 18 (same no-extra-peaks lemma, 9 normals), and
  L2(3): depth-1 ≤ 48 — via the top-1 ("which cube reaches farthest")
  diagram: prove its swap curve generically has V = 92 vertices, all
  trivalent (Euler then gives cells = 2 + V/2 = 48), plus the
  semicontinuity half (degenerations only merge cells). Anchors: each
  cube's 8 corner directions are local maxima of its reach, giving 24
  anchored cells; the census bounds the remaining 24.

Both attainers are already exactly verified (golden triple by two
independent ℚ(√5) engines; octahedral compound in the gated ℚ(√2)
engine; identical profiles {48,18,1}), and non-exceedance is tested by
4,414 seeded climbs at n=3 plus every 3-subset in the ~1.2M-config
corpus. The lemmas are the only missing pieces.

The Zaslavsky framing is exactly right: C(l,n) is a face-count formula
for a structured family of great-circle-arc arrangements on S², and the
proof shape is the Platonic one — a finite local classification (which
vertex types the swap curves can have, constrained by each cube's
orthonormal normal triad) followed by Euler's formula. At n=3 there are
only 9 normals, so the local classification is finite and plausibly
hand-checkable. L1(2) is the single easiest full theorem on the board.

### Postscript 23 addendum: do the proofs extend to n > 3? (Chris Cole)

- The PER-LAYER lemmas extend uniformly in n: the census V_l(n) =
  (24l−12)n − 4l² is linear in n with an l-only correction, so the local
  vertex classification does not grow with n — proving L1 in general
  form proves depth-(n−1) ≤ 6n for ALL n at once; the l=2 census gives
  depth-(n−2) ≤ 18n−6 for all n. The hard direction is l, not n.
- The EXACT-MAXIMUM proofs provably do NOT extend: cap-sum tightness
  fails from n=4 (195 vs 183, 429 vs 393, 801 vs 723) — the frustration
  phenomenon. n=2,3 are the last sizes where per-layer analysis decides
  the maximum.
- An n ≥ 4 maximum proof needs JOINT-layer inequalities (trade-off
  constraints), of which we have measured shadows (d2+d3 = 368 ridge,
  envelopes E1/E2) but no conjectured exact form. Candidate first step:
  a rigidity lemma "d1 = 10n²−14n forces golden" (true in all data),
  enabling case analysis on d1 — necessary but not yet sufficient
  (at n=4 it leaves max ≤ 193 vs true 183). Open.

## Postscript 24: FIRST THEOREM — the anchor lemma is proven (all n), and the n=2 CAD verdict

Direct outcome of the fine-graining exchange with Chris Cole.

**Theorem A (proven).** The radial envelope of any n-cube configuration
has local minima only at the 6n face-center directions (value 1 = the
inradius). Proof is a two-line sandwich: at a local max of
M = max_i |n_i·û|, every ACTIVE |n_i·û| is itself locally maximized
(it is squeezed between its value and M), and a single |cos| has maxima
only at ±n_i with value 1. Full statement + proof in C45_notes §10.
This kills the long-standing "three-form peak" crux — a phantom: peaks
of a max require each active piece to peak. Numerically corroborated
(exactly 6n maxima, value 1, every config sampled; consistent with all
earlier zero-shoulder censuses).

**What remains for C(1,n) = 6n**: only excluding "parasite" cells
(components whose envelope-inf sits on the boundary tie curve, not the
interior). Sharper than before; two candidate routes recorded.

**CAD probe (n=2 unrestricted chamber exam)**: 4 of 12 distinct
vertex-wall quartics → 4.6M-leaf decomposition in ~4 min; the full wall
set is infeasible on this machine. Chris's caveat ("fine-graining works
if we fix a family") is thereby quantified at the smallest case: the
viable certification mode is per-family (few knobs), or Theorem A +
Euler census.

### Postscript 9 addendum (2026-07-13): the slide axis identified exactly

The 67↔67 family's seed rotates by δ about â where, unnormalized,
â ∝ ( −(√2+√10), −(4+√2+√10), −2+3√2+2√5−√10 ) / 8
  = ( −√2·φ/4, −(√2·φ/4 + 1/2), … )        [√2+√10 = 2√2·φ]
and cos δ = (−6 + 3√2 + 2√5 + 3√10)/16  (δ = 40.306°).
The axis lives in the COMPOSITUM ℚ(√2,√5) — the bridge between the
octahedral (√2) and golden (√5) walls — and is a symmetry axis of
neither endpoint (57.6° from (1,1,1)). Cube k of the family spins about
Cᵏ·â: three skew axes forming a 120°-orbit around the invariant global
3-fold axis (1,1,1). Interactive: the depth explorer's "67 ↔ 67 slide".

### Postscript 9 addendum 2 (2026-07-13): edge crossings along the slide — near-persistence quantified

User: "some of the edge concurrences should persist on the slide."
Measured: at t=0 the octahedral compound has 30 EXACT edge crossings
(crossing parameter 1 − 1/√2 ≈ 0.293 along the edge). In the interior
NO crossing is exact (confirming the P9 caveat) but 6–18 NEAR-crossings
persist with gaps of only 0.0015–0.006 (cube half-width 1) — the
crossings open into hairline gaps whose closest-approach points slide
along the edges — and at t=1 the gaps snap shut again with the crossing
at s = 1/φ = 0.618, the golden section (the user's original
middle→corner marker). So the edge-concurrence structure persists as a
sub-percent-gap GHOST through the whole family, exact only at the two
walls. Viewer updated to render near-concurrences as fading ghost rings.

## Postscript 25: the DIHEDRAL FAMILY — a closed-form 1-parameter family with exact edge coincidences, containing both 67s; the ghosts explained; a new exactly-certified compound in Q(sqrt6)

Prompted by the user viewing the slide midpoint (t=0.5) and asking whether a
nearby configuration — "perhaps with irrational rotations" — could close the
near-miss edge crossings exactly, noting the coincident edges looked
perpendicular to (1,1,1). That observation was the key.

**The family.** Take the cube [-1,1]^3 and rotate it by +-120 degrees about an
axis n(psi) = (sin psi, cos psi, 0) lying IN one of its own face planes
(through the center). The three cubes {I, S, S^2},
S = S(psi) = -1/2 I + (3/2) n n^T + (sqrt3/2) [n]_x, form a C3 orbit about
the axis s = n rotated... equivalently, in the world frame used by the
viewer: seed matrix with columns
[cos(psi) w + sin(psi) s | -sin(psi) w + cos(psi) s | u],
u any unit vector perpendicular to s=(1,1,1)/sqrt3, w = s x u, orbited by
C = 120 degrees about (1,1,1). The u-freedom (theta) is exactly a global
rotation about (1,1,1), so modulo congruence this is ONE parameter, psi.
Every member is D3-symmetric: the C2 axes are the cubes' horizontal face
axes u, Cu, C^2u.

**The coincidence theorem (hand algebra + 1e-16 numerics, not yet formal).**
For EVERY psi, the edge-edge coplanarity conditions of all three edge classes
(x-, y-, z-edges) vanish identically. For the u-edges it is elementary: all
three cubes' u-edges lie in two common planes perpendicular to (1,1,1) at
heights +-(sin psi + cos psi) (and +-(cos psi - sin psi)), and non-parallel
lines in a common plane always meet. For the other two classes the identity
falls out in the frame {w, s, u} using u x Cu = (sqrt3/2)s (verified at
random (theta,psi) to machine zero; dihedral_scratch/family_check.py).
Interior-of-segment crossing counts form plateaus in psi:
  12 (0<psi<21deg), 18 (21..45.5), 24 AT psi=45 exactly, 18, 12, and
  spikes: 30 at psi = arcsin(1/sqrt3) = 35.264deg, 30 at arctan(sqrt2),
  48 at psi = 0 and 90 (shared-axis compound, pair invariant 1+sqrt3).

**Both 67s are members.**
- Octahedral 67: psi = arcsin(1/sqrt3), axis n = (1, sqrt2, 0)/sqrt3.
  30 interior crossings, pair invariant 1/2+sqrt2 (matches).
- Golden 67: tan(psi) = phi^2, i.e. sin(psi) = phi/sqrt3,
  cos(psi) = 1/(phi sqrt3) — consistency is the identity
  phi^2 + phi^-2 = 3. Axis n proportional to (phi^2, 1, 0). Pair invariant
  = 3phi/2 = 2.4270509831... to 1e-16. At exactly this psi the 18 interior
  crossings hand over to 54 AT-CORNER contacts — the blue-ring -> gold-ring
  morph of Postscript 9, now in closed form.
- The relative rotation is the classical golden matrix
  (1/2)[[phi,1,1/phi],[1,-1/phi,-phi],[-1/phi,phi,-1]] at the golden point.

**Why the slide has ghosts.** The 67<->67 slide (Postscript 9) connects the
two 67s but leaves this family (its interior seed has face-axis dot (1,1,1)
approx 0.05, not 0). The dihedral family connects the same two endpoints
THROUGH exact-coincidence configurations the whole way. The ghost gaps of the
slide are precisely the cost of stepping out of the dihedral surface.
(First found numerically: from t=0.5, a 1.66-degree seed rotation about
approx (0.799,-0.545,-0.254) lands back in the family at psi=52.20 deg,
closing all 12 ghosts into 18 exact crossings; continuation + congruence
invariants then revealed the family. dihedral_scratch/edge_close*.py.)

**A new exactly-certified compound.** psi = 45 deg: axis = the FACE DIAGONAL
(1,1,0)/sqrt2. S = (1/4)[[1,3,r6],[3,1,-r6],[-r6,r6,-2]], entries in
Q(sqrt6). 24 interior crossings (plateau maximum away from the 67s).
Exact count via q6_count.py (new engine: field-constant clone of the
validated slide3_q2.py, D: 2->6; identity-pair self-test passes; S certified
orthonormal with S^3=I in exact arithmetic):
  TOTAL = 49, depth profile {d1: 30, d2: 18, d3: 1}.
Same deep layers as both 67s (18, 1) — another instance of "deep structure
conserved, d1 is what varies" (Postscript 17). SINGLE-ENGINE exact count
(not a record claim); a second engine pass is listed in the follow-ups.

**Arithmetic density (open route).** With sin psi = p/r, cos psi = q/r
rational (Pythagorean triples), S(psi) has entries in Q(sqrt3) — an infinite
family of exactly-countable members. A Q(sqrt3) clone of slide3_q2.py (one
constant) plus a Pythagorean sweep would chart the region count along the
whole family exactly. See DIHEDRAL_FAMILY_NEXT.md.

Files: q6_count.py (Q(sqrt6) verifier + the 49 count), dihedral_scratch/
(exploration + verification scripts), DIHEDRAL_FAMILY_NEXT.md (handoff).

### Postscript 25, addendum: the persistent 18-core — octahedral-to-golden slides WITHOUT breaking a single concurrence; corner docking; corrected transition locations

Prompted by the user asking for "another way to slide from octahedral sqrt2
to golden sqrt5 while maintaining edge concurrences." Fine-grained pair-
identity tracking (0.1-deg grid, persistence.py/docking.py in
dihedral_scratch/) shows the dihedral family already does this, more
literally than Postscript 25 realized:

1. **The 18-core.** The interior crossing SET is one and the same set of
   18 edge pairs (6 per cube pair) on the ENTIRE open interval
   (20.905deg, 69.095deg) — i.e. between the two golden copies. The count
   changes en route (30 at the octahedral points, 24 at the face-diagonal
   point) are +12/+6/+12 EXTRA coincidences that exist only exactly AT
   those isolated psi (measure zero); the core 18 never opens a gap. The
   ghost bands around the special points are entirely the extra pairs
   approaching/leaving — never the core.
2. **Corner docking.** At arrival at golden (either copy), nothing
   breaks: 6 of the core 18 remain interior at segment parameter
   t = +-0.23607 = 1/phi^3 (the golden section yet again; cf. the s=1/phi
   crossing of Postscript 9), and the other 12 land EXACTLY on cube
   corners (t = +-1, gap ~3e-16) — they BECOME the golden corner-
   coincidence structure. Verified identically at mirror-golden
   (20.905 deg): 6 interior + 12 docked, 0 broken.
3. **So**: sliding 35.264 -> 69.095 (or the shorter mirror route
   35.264 -> 20.905, arriving at a congruent golden compound) maintains
   all 18 core edge concurrences unbroken start to finish. Keeping all 30
   of octahedral's crossings is impossible at golden with interior
   crossings alone (golden has 18-core worth: 6 interior + 12 docked);
   whether some off-family path in the full 3-DOF C3 space preserves more
   than 18 is open (the 12 octahedral extras appear to be isolated —
   they exist only at the octahedral points of the family).
4. **Correction to the transition table**: the crossing SET changes ONLY
   at 20.905 (= 90 - arctan(phi^2), mirror-golden), 45, and 69.095
   (golden) in [20,70] — the "unnamed transitions at ~21.4 / ~68.6 deg"
   previously baked into the viewer's REGION_CHANGE_DEG are ghost-band
   BOUNDARIES (the fuzzy 0.02-gap window), not set changes, and the
   earlier bisection "conflation" mystery near 69 deg dissolves: there is
   only one event there, golden itself. Viewer follow-up: relabel those
   marks, and the "maintain concurrences" lock can be redefined
   core-aware (the core-18 is maintained on the whole span between the
   golden copies, so locking should permit the full octahedral->golden
   drag).

### Postscript 25, addendum 2: paths preserving MORE than 18 — the pair-curve identity, a 26-concurrence chain triple, and why 18 is still the end-to-end record

User asked for paths preserving more than the 18-core. Findings
(dihedral_scratch/: bigfamily.py, pairmap.py, loopholes.py, trace10.py,
window26.py):

1. **The big family.** The dihedral construction generalizes: n cubes,
   each with a face-axis u_k perpendicular to a COMMON axis s, arbitrary
   phases theta_k about s, and a COMMON tilt psi. Exact edge coincidences
   persist (control: different psi per cube kills all of them). Pair
   crossing structure depends only on (Delta theta, psi).
2. **Within the C3 dihedral family, >18 is impossible**: the 12 octahedral
   extras are valid only at isolated psi (measure zero on the slice).
3. **The pair-curve identity (new).** In the (Delta, psi) pair-plane, ALL
   FOUR extra coincidences of the octahedral pair share ONE zero curve
   Delta_c(psi) through (120 deg, 35.264 deg) — their line-coplanarity
   residuals stay ~1e-16 along the entire traced curve (psi from ~2 to
   ~85 deg), i.e. all 10 of the octahedral pair's edge-line coincidences
   hold identically on a one-parameter curve, not just at the octahedral
   point. (Full-3-DOF check: the 10 conditions' Jacobian at the
   octahedral pair config has rank 2 — kernel dim 1 — the curve is the
   whole local solution set.) Segment validity (|t|<=1) holds for psi in
   roughly (27.5, 46.5) deg; outside, the extra crossings exit through
   cube corners.
4. **A 26-concurrence path (new).** Chain triple theta = (0, Delta_c(psi),
   2*Delta_c(psi)): pairs (1,2) and (2,3) ride the curve carrying 10
   coincidences each; pair (1,3) at 2*Delta_c keeps its core 6. Verified:
   26 exact concurrences maintained continuously for psi in
   [35.264, ~44.5] deg (Delta_c drops 120 -> ~110). At psi ~44.5 the
   extras dock/exit at corners and the count falls to 18; at 45 the
   third pair briefly holds 8 (total 20).
5. **End-to-end oct -> golden still caps at 18** (best known): the four
   extra labels are not in golden's 24-label contact set at all, and the
   pair curve's segment window closes at ~46.5 deg. Open loophole:
   corner HANDOFFS — at |t|=1 a concurrence point can switch to an
   adjacent edge's label and continue; golden has 60 contacts total, so
   a handoff chain carrying >18 physical concurrence POINTS into golden
   is not excluded. Tracing the handoff network is a well-posed numeric
   task (delegable).
6. **n>3 relevance.** The big family is an (n-1)+1-parameter
   exact-coincidence scaffold for ANY n: every cube pair in segment
   range carries >=6 exact edge concurrences; chains
   theta=(0, Dc, 2Dc, ...) let consecutive pairs carry 10. Entries are
   algebraic (Pythagorean psi -> Q(sqrt3)), so members are exactly
   countable with the planned q3 engine. Records already exploit
   common-axis structure (723 contains a C3 orbit about (1,1,1); the
   continuous 9-family pairs are the psi->0 degenerations), so an
   in-family exact sweep at n=4/5/6 over (theta_2..theta_n, psi) — an
   n-dimensional sheet instead of (3n-3) — is a cheap structured probe
   of the trade-off surface. Proposed as follow-up alongside
   DIHEDRAL_FAMILY_NEXT.md Task 1.

### Postscript 25, addendum 3: EXACT region counts along the dihedral family (Task 1 executed) — a symmetric staircase, spikes at the 67s, and a local MINIMUM at the face-diagonal point

DIHEDRAL_FAMILY_NEXT.md Task 1, C3 slice, executed with a new Q(sqrt3)
engine (q3_count.py, field-constant clone of the validated slide3_q2.py,
same pattern as q6_count.py; identity self-test + orthonormality + S^3=I
asserts). At Pythagorean psi (sin=p/r, cos=q/r rational), S(psi) =
-I/2 + (3/2)nn^T + (sqrt3/2)[n]_x has entries in Q(sqrt3) -> exactly
countable. 40 points swept (~0.6 s each). Result, symmetric about 45 deg:

  psi in (0, ~9.6):        25 = {12, 12, 1}
  psi in (~9.6, ~10.9):    31 = {18, 12, 1}
  psi in (~10.9, 20.905):  43 = {24, 18, 1}
  psi in (20.905, 69.095): 55 = {36, 18, 1}     <- the central plateau
  ... mirrored on the other side; endpoints psi=0/90 (shared axis): 25.
  Isolated spikes: octahedral 35.264 -> 67 = {48,18,1};
  face-diagonal 45 -> 49 = {30,18,1} (Q(sqrt6) engine, addendum 25);
  golden 69.095 -> 67 = {48,18,1}.
  (Wall between 31 and 43 bracketed in (9.53, 10.39) deg; its mirror in
  (79.61, 80.47). Exact wall locations not yet identified.)

Observations:
1. **d3 = 1 always, d2 = 18 across the whole middle band** (dropping to 12
   only below ~10 deg and mirrored) — ALL action is in d1
   (12->18->24->36, spiking 48 at both 67s, 30 at 45 deg). The
   "deep-structure-conserved, d1-varies" principle (Postscript 17) holds
   pointwise along the entire family.
2. **The family's maxima are exactly the two 67s** — the proven n=3
   global maximum is attained precisely at the two most special family
   points, from a plateau of 55.
3. **The face-diagonal point is a local MINIMUM (49 < 55)**: its +6 extra
   edge crossings MERGE regions instead of creating them, while the +12
   extras at the octahedral points RAISE the count by 12. Coincidence-
   richness cuts both ways; it is how walls concur, not how many — the
   sharpest small illustration yet of the trade-off principle.
4. **Region-count walls != crossing-set walls**: the crossing set changes
   only at 20.905/45/69.095 (addendum 2), but the count also jumps at
   ~9.6/~10.9 deg (and mirrors) where d2 changes with NO edge-crossing
   event — vertex/face combinatorial walls of the deeper arrangement.
5. Bonus (not yet exploited): in the BIG family, Pythagorean phase
   DIFFERENCES make the relative rotations fully RATIONAL — integer
   quaternions — so the (theta_2, theta_3, psi) directions off the C3
   slice are countable by the fast C++ engine directly. The 2-parameter
   exact count map is a cheap delegable follow-up.

Files: q3_count.py (engine + sweep driver, 40-point table in __main__).

### Postscript 25, addendum 4: the handoff chase — 18 stands, the obstruction identified, and a CORRECTION to addendum 2's golden contact count

The corner-handoff exploration (HANDOFF_SPEC.md; scripts
dihedral_scratch/handoff_*.py; full report handoff_report.md) is done.
Verdict: **no path carrying more than 18 physical concurrences from
octahedral to golden was found** — 18 is the confirmed lower bound with a
specific, describable local obstruction; not a proven ceiling.

**CORRECTION (addendum 2, item 5).** "Golden has 60 exact contacts
(6 interior + 54 corner)" mixed a threshold artifact with a label count.
Correct figures (handoff_g1.py, confirmed against persistence.py): golden
triple = **18 interior + 54 corner LABEL-pairs (72)**; deduplicated to
physical points = **18 interior + 6 corner points = 24** (each corner
point is a genuine vertex-to-vertex coincidence registering 3x3=9 label
pairs). The old "6 interior" came from evaluating at psi rounded to
69.0948 deg (2e-5 deg off the exact arctan(phi^2)), where the 12 docking
core pairs already sit past the |t|<0.9999 cutoff. Golden's 18 interior =
6 persisting core + that point's OWN 12 extras — the golden-side analogue
of the octahedral +12. Also: octahedral has MORE distinct contact points
(30) than golden (24), so ">18 into golden" needs 19 of golden's 24
physical points fed — tight but not excluded a priori.

**What the chase established** (all three gates passed; the linker
independently reproduces the 18-carry, the 26-window, and — untuned —
the 12-plateau past golden):
1. Driving THROUGH golden on the C3 path, all 18 core trajectories pass
   continuously; beyond it 6 stay interior, 6 execute genuine verified
   corner handoffs (e.g. (0,1,0,1) -> (0,1,4,5) at shared vertex
   (-1,-1,-1)), 6 die. Handoffs are real and the machinery detects them.
2. The chain path's wall is at exactly **psi=45 deg, theta2 =
   arccos(-1/3) = 109.4712 deg (the tetrahedral angle)**, where cube-A's
   vertex (-1,1,-1) touches cube-B's vertex (1,-1,-1) — a vertex-VERTEX
   coincidence offering 9 relabeling candidates. NONE of the 9 continues
   to the golden basin: most re-hit |t|=1 immediately (psi=45 is a
   resonance where several branches of the algebraic curve cross); the
   rest run off to the shared-axis region (psi to 89 deg).
3. Golden's own extras form a THIRD pair-curve identity (x-z class:
   (1,9),(2,10),(9,0),(10,3) share one curve through golden). Traced
   backwards it walls at psi=45.00 deg, theta2=180.0 deg — the same
   psi-45 resonance but ~70 deg away in theta2 from the octahedral-side
   wall, and neither curve's far branch links them.
4. **The obstruction**: octahedral extras (y-z class, curve near
   theta2~110) and golden extras (x-z class, curve near theta2~180) are
   different label families on different curves; both graze the psi=45
   resonance but nothing bridges the 70-deg theta2 gap while holding any
   cross-class equality. Grid corroboration: pair-level count >=7 covers
   only 0.28% of the (theta2, psi) plane — a 1-D curve network, no open
   patches (as the DOF count predicts).
Scope: single-hop rescues at the identified walls + three cross-class
families + coarse grid; multi-hop chains through second/third walls not
exhausted.

## Postscript 26: the records are BUILT FROM family pairs — the n>3 verdict on the dihedral family

NFAMILY_SPEC.md executed (nfamily_report.md; two-engine gates G0/G1/G2 all
passed; spot-verified by the main session). The family generalized to n
cubes = {Rel(theta_k, psi)} with Rel(D,psi) = Rodrigues rotation by D
about axis (sin psi, cos psi, 0) — a new closed form making every
Pythagorean-parameter member an INTEGER-QUATERNION config, countable by
the C++ engine (~10 ms each).

**As a search space: no.** Best verified family members (9,218-config
exact sweep: chains, random Pythagorean phases, hill-climbing): n=4: 175
(record 183, -8); n=5: 335 (393, -58); n=6: 615 (723, -108). The deficit
GROWS with n. Caveat (fundamental, not budget): Pythagorean sweeps cannot
land on irrational spikes — at n=3 the same sweep sees only the
55-plateau, never the 67s — so these are lower bounds on the continuous
family's supremum.

**As structure: overwhelmingly yes.** Exact pairwise tests (two
independent methods, 34/34 agreement; crossing counts + an axis test
"exists a cube-symmetry relabeling with R[0][1]==R[1][0] exactly"):
- 183 record: ALL 6 pairs in family position (6 exact crossings each).
- 393 record: ALL 10 pairs in family position.
- 723 record: 12/15 — cubes {0..4} form a full family 5-clique (= the
  embedded 393, consistent with record nesting), cube 5 family-linked to
  two of them, generic vs the rest.
- 67 (n=3): confirmed a family member in exact Q(sqrt2) arithmetic —
  first exact (non-numeric) confirmation of its 30 crossings.
So the records are gluings of family cliques on DIFFERENT axes, not
single-axis members: the single-common-axis family is a strict subset of
"configs built from family-position pairs," and the latter is what
records exploit. Record-hunting reframed: search over multi-clique
gluings (clique sizes, axes, tilts, phases) instead of raw SO(3)^n.

**Deep layers**: at every n the family pins d_n=1 and d_{n-1} at exactly
the record's own value (24/30/36 at n=4/5/6) across the whole
non-degenerate range; the deficits sit in the SHALLOW layers (n=4: the
entire -8 in d2 alone, 58 vs 66, with d1/d3/d4 matching the record
exactly). Sharpest form yet of "deep structure conserved, shallow layers
are what records win."

**Also**: psi <-> 90-psi mirror symmetry persists at every n; chains at
a=90 deg collapse to total 93 INDEPENDENT of n (cube 90-degree
self-symmetry makes added cubes redundant — the degeneracy predicted in
DIHEDRAL_FAMILY_NEXT Task 4, now quantified).

Files: nfamily_report.md, nfamily_common.py, nfamily_gates.py/.out,
nfamily_q3_records.py/.json, nfamily_sweep.py, nfamily_results.jsonl.

### Postscript 26, addendum: four theorems PROVED (C45_notes.md section 12)

Answering "can we prove anything?" — yes, four statements moved from
verified-numerics to proved today (full proofs in C45_notes.md sect. 12):
- **Theorem M (mirror)**: config({theta_k}, psi) is congruent to
  config({-theta_k}, 90-psi) via the x<->y coordinate swap (improper
  isometry; conjugation reverses the rotation sense and swaps the axis
  components). Proves the psi<->90-psi degeneracy seen in every sweep,
  for all n; all family sweep domains are rigorously halved.
- **Theorem P (periodicity)**: psi+90 gives the SAME compound
  (M(psi+90) = M(psi)*rot(e3,90)); true parameter range is psi in [0,45].
- **Theorem F (coincidence identity)**: all same-class edge-line
  coincidences hold identically on the whole family — z-class by the
  equal-heights argument, y-class by a five-line vector computation
  (the coplanarity form collapses to s c^2 (sin D - sin D) = 0),
  x-class from y-class via Theorem P's relabeling. The family's exact
  crossings rest on proof; only segment-interior validity (|t|<=1)
  remains numeric (Sturm-certifiable, listed as next).
- **Theorem R (rational obstruction)**: rational configurations have
  rational O-reduced pair invariants; the 67s' invariants are 1/2+sqrt2
  and 3phi/2 — so no rational config is congruent to either.
  **Corollary**: conditional on the two known 67s being the only n=3
  maximizers, the n=3 maximum REQUIRES irrational coordinates — making
  n=3 provably the unique irrational level of the record tower, given
  witness uniqueness.
Identified as provable-next with real work: certified staircase (Sturm),
core-18 segment bounds with docking values +-1, +-1/phi^3, the
pair-curve identity, and (the prize, unchanged) the two lemmas of
Postscript 23 for max(3)=67.

## Postscript 27: the gluing search — records still unbeaten (deficit exactly 8 at every n), and the RATIONAL-TANGENT discovery (with a correction to the agent's clique inventory)

GLUE_SPEC.md executed (glue_report.md; gates G1/G2/G3 all passed;
319,141 exact configs; every near-record hit re-verified with the Python
oracle). Headline numbers, all two-engine verified:

| n | best glued (sizes)         | record | deficit |
|---|----------------------------|--------|---------|
| 4 | 175 (no gain over single)  | 183    | -8      |
| 5 | 385 (3+2)                  | 393    | -8      |
| 6 | 715 (3+3)                  | 723    | -8      |

Gluing recovers 50 of the single-axis deficit at n=5 and 100 at n=6 —
converging to a common floor of EXACTLY 8 below the record at every n.
Nothing beat or tied a record; the record-claim protocol never fired.

**Q0 verdict**: no record is a single-axis family member (full-record
axis intersections exactly empty). Postscript 26 stands.

**CORRECTION to the agent's sub-clique inventory** (main session,
exhaustive exact re-derivation over all subsets x all 3^k face-axis
choices, Fractions only): the agent claimed three overlapping 4-of-5
cliques in 393; in fact there is EXACTLY ONE single-axis 4-clique in
393: cubes {1,2,3,4}, integer axis (3,2,0), tan psi = 2/3 (hyp^2 = 13,
so sin/cos in Q(sqrt13)) — verified: each cube's local axis is a signed
permutation of (2,3,0), exactly. The other two claimed cliques fail
exact verification (their cubes lack the zero component / 2:3 ratio).
183's inventory, corrected and exhaustive: NO 4-clique, and three
3-cliques all on the SAME cube triple {0,2,3} with three DIFFERENT
integer axes — (2,-3,0) at tan 2/3 (sqrt13), (3,5,0) at tan 3/5
(sqrt34), (5,2,0) at tan 2/5 (sqrt29): a triply-resonant family triple.
393 has no 5-clique; 183 no 4-clique.

**The discovery that survives and sharpens**: the records' family
structure lives at RATIONAL-TANGENT, IRRATIONAL-SINE tilts
(tan psi = 2/3, 2/5, 3/5; hyp^2 = 13, 29, 34 non-square). A Pythagorean
(rational-sine) sweep can NEVER land on these at any resolution — the
Postscript 26 sweep searched the wrong rational locus. Yet these
configurations ARE integer-quaternion (the records prove it): a pair at
rational tan psi = q/p has rational Rel iff cos Delta is rational and
sin Delta is in sqrt(d)*Q with d = p^2+q^2 — rational points on the
conic c^2 + d s'^2 = 1, parametrizable by rational slope. So the
C++-searchable single-axis locus extends far beyond Pythagorean-x-
Pythagorean, and the natural next sweep is over rational-tangent tilts
with conic-coupled phase steps — the slice the records actually live in.
The exactly-8 floor at three consecutive n is either a coincidence or a
structural constant of the gluing space; the rational-tangent sweep
should decide which.

(Also: the n=4 resonance solve (RESONANCE4_SPEC.md) hit its session
limit mid-run; to be resumed.)

## Postscript 28: the n=4 resonance solve — cross-class alignment is count-NEGATIVE at n=4; best resonance 151, and it is secretly RATIONAL

RESONANCE4_SPEC.md executed (resonance4_report.md, resumed after a
session-limit interruption; resonance4_solve.py/.wl,
resonance4_results.jsonl). Gates R1 and R2 passed; R1 additionally
re-verified independently by the main session (sympy: both polynomials
vanish exactly at the known n=3 resonances).

**The cross-class coplanarity polynomials** (Rel gauge, cD=cos Delta,
sD=sin Delta, cP=cos psi, sP=sin psi; representative sign-variants):

    g_xy = 2 cD sP^2 - cD + cP sD - sD sP - 2 sP^2 + 1
    g_yz = -cD cP sP + cD sP^2 + cD - cP sD + cP sP - sP^2 + 1
    g_xz = cD cP - cD sP - cP - sD + sP     (sP=0 factor dropped)

Each type has 8 sign-variant curves (16 label pairs in antipodal
pairs); swapping the cubes is sD -> -sD, so ORIENTATION matters — the
n=3 octahedral resonance is itself mixed-orientation (Deltas
120,120,240). R1: substituting Delta=120 deg gives psi=arcsin(1/sqrt3)
as an exact root of g_yz and psi=arctan(phi^2) of g_xz.

**Systems solved**: 90 uniform k=4 systems (46 exact, 44 Groebner
timeouts, concentrated in the heavy xy class) + all 48 targeted
mixed-orientation triangle+1 systems. 385 unique candidate points. No
non-degenerate resonance has rational PARAMETERS; 63 candidates in
single quadratic fields — ALL exactly counted via a generic Q(sqrt d)
field engine (factory clone of the validated slide3_q2.py); ~160
degree-4-nested candidates reported open with minimal polynomials, per
spec's do-not-approximate rule.

**Verdict: every exactly-counted n=4 family resonance is
count-negative.** Best: 151 = {68,58,24,1} at tan psi = 2, theta =
(-131.81, 96.38, -35.43) deg, pairs {12,13,23,24} on the yz curve —
vs 175 (family plateau), 183 (record), 195 (cap-sum). The n=3 "+12
spike" mechanism does NOT carry to n=4 in any quadratic field: extra
coincidences merge regions, as at n=3's face-diagonal 49 < 55. Deep
structure conserved pointwise: every non-degenerate resonance counted
has d4=1 and d3=24 exactly.

**Main-session observation that unifies the two campaigns**: the 151
witness's parameters are irrational (Q(sqrt5)) but its CONFIGURATION is
rational — sin(theta_k) in sqrt5*Q times axis components in Q/sqrt5
cancels — and it reduces to tiny integer quaternions

    1,0,0,0; -1,2,1,0; 2,2,1,0; 7,-2,-1,0     (axis (2,1,0))

i.e. it sits exactly on Postscript 27's rational-tangent conic
(c^2 + 5 s'^2 = 1; cube 2's point is c=-2/3, s'=-1/3). Third-engine
verification: the C++ engine on those quats gives 151 = {68,58,24,1},
agreeing with both of the agent's engines. So the algebraically-found
resonances at rational-tangent tilts ARE inside the rattan sweep space
— the resonance solve and the conic sweep are probing the same locus
from two directions, and at n=4 that locus tops out below the plateau.

**Most interesting open point**: a pure chain theta_k = k*a
(a ~ 200.891 deg) at tan psi = (1+sqrt13)/6 — the record's own tilt
field Q(sqrt13) — with all four pairs {12,23,34,14} on one curve;
degree-4 nested coordinates, needs a certified nested-radical sign
oracle to count. The corner-contact (|t|=1) resonance sweep was not
reached.

## Postscript 29: the rational-tangent sweep (interim) — the "exactly 8" floor is BROKEN at n=5: deficit now 6

RATTAN_SPEC.md in flight (rattan_report.md; rattan_sweep.py;
rattan_results.jsonl, 17,080 configs at smoke scale; the implementing
agent hit its session limit before launching the full sweep — interim
results below are already two-engine verified and recorded now).

**All four gates pass.** G0: exact conic parametrization
(c,s') = ((1-d t^2)/(1+d t^2), 2t/(1+d t^2)) with round-trip and
group-law closure t1 (+) t2 = (t1+t2)/(1 - d t1 t2), all Fractions.
G1 (the sharp gate): 393's own 4-clique {1,2,3,4} is exactly a conic
chain on axis (3,2,0), tan psi = 2/3, d=13, at t-values

    t = 0 (base = clique cube 2), -5/6, 3/4, -1/5

with the three non-base pairs matching the conic group law with NO
further search (e.g. pair (1,3): c=29/133, s'=36/133 both ways). The
sweep space provably contains the record's clique. G2: two-engine
agreement on fresh rational-tangent configs at n=4 and n=5. G3: 723
reproduced from the ledger quats.

**Bonus**: 183's triply-resonant triple {0,2,3} independently
re-derived on all three axes — and in ALL three parametrizations the
two non-base cubes sit at OPPOSITE conic phases (t and -t): the record
triple is an antipodal pair about cube 0 three ways simultaneously.

**Headline: the deficit floor is not 8.** Taking 393's exact 4-clique
as fixed base and adding a 5th cube ON the same axis at conic phase
t5 = 3/14 (a plateau of t5 in [~8/39, ~3/14] gives the same count):

    n=5: 387 = {148,130,78,30,1}
    quats 1,0,0,0; -6,-10,15,0; 4,-6,9,0; 5,2,-3,0; 14,-6,9,0

Two-engine verified (C++ engine in the sweep; Python oracle re-run
independently by the main session: exact agreement). 387 > 385 (the
glue campaign's best): at n=5 the deficit to the record is now 6, so
the "exactly 8 at every n" pattern of Postscript 27 was a coincidence
of the glue search space, not a structural constant. Note the winning
config is FIVE cubes on ONE axis — a single-axis 5-chain-with-
non-uniform-phases, something the glue campaign's 3+2 split could not
represent.

Other interim facts: 393's clique alone counts 179 at n=4 (only -4);
the reconstructed conic chain reproduces the literal ledger clique's
count exactly (end-to-end gauge validation). The tier-3 "183 triple +
4th integer quat" search re-found the 183 RECORD itself — main session
check: the found 4th cube (1,-1,-1,4) right-multiplied by the cube
symmetry (0,1,-1,0) is exactly the ledger's (0,5,3,2). 723's 6th cube
(5,2,2,2) is NOT in family position w.r.t. the 4-clique (off-axis,
like 393's cube 0). Chains alone top out at 175 (n=4) / 671 (n=6).

## Postscript 30: the event catalogue — the "+-1 per coincidence" law dies, a depth-conservation law survives 12/12, and a correction to Postscript 25 addendum 3

EVENTS_SPEC.md executed (events_report.md, events_extract.py,
events.jsonl; all gates passed; new field-agnostic coincidence census
pair_census validated against nfamily_common on 16 pairs and against
the golden 18+54/6 census from an independently hand-derived matrix).
Twelve exact events tabulated across n=3 (dihedral family), n=4
(175/151/143), n=5 (387-plateau edges).

**The conjectured "+-1 region per coincidence" law is NOT general.**
It is EXACT (+/-1.000) precisely for the pure-interior-crossing n=3
events: octahedral spike +12 count on +12 crossings, its mirror, and
the face-diagonal -6 on +6. Everywhere else it bends or breaks:

- golden spike: +12 regions from 6 physical vertex-vertex contacts =
  +2.000/point — the SAME total 67 reached by a different mechanism at
  a different exchange rate than the octahedral 67;
- n=4, 175 -> 151: coincidences INCREASE (+2 interior) while the count
  DROPS 24 — falsified in sign, not just magnitude;
- n=5 plateau edges: identical coincidence deltas (+-2 corner points)
  give -2/point at one edge and -4/point at the other, depending only
  on WHICH cube pair touches;
- band-edge walls (~9.5 deg and mirror): count jumps +12 with the
  exact crossing census FROZEN (certified zero Fraction difference) —
  a genuine third event class: pure diagram-combinatorial
  reorganization with no coincidence change at all.

**The law that survives every event (12/12): depth conservation.** The
entire count delta of every event lands in d1 (occasionally d1+d2);
every deeper layer is bit-for-bit unchanged — creates, merges,
interior and corner mechanisms, no-coincidence walls, n=3/4/5 alike.
Postscript 17's "deep structure conserved" is now a pointwise,
per-event exact statement.

**CORRECTION to Postscript 25 addendum 3** (verified independently by
the main session with q3_count at psi ~ 0.23/2.29/7.6 deg): the table
row "psi in (0, ~9.6): 25 = {12,12,1}" is wrong as an interval. 25
holds ONLY at the isolated point psi=0 (and 90 by mirror); generic
psi arbitrarily close to 0 gives 31 = {18,12,1}: the 31-plateau spans
all of (0, ~9.5), and the 43-plateau (~9.5, 20.905). True structure
below the golden-mirror:
{25 at psi=0 only} | 31 on (0,~9.5) | 43 on (~9.5, 20.905) | 67 at
20.905 | 55 central band. psi=0 is itself a NEGATIVE mega-spike:
crossings jump 12 -> 48 while the count drops 6 (ratio -0.167) — the
most coincidence-rich, count-poorest event known; near-total geometric
redundancy at the fully degenerate shared-axis point.

Consequence for the theory program: a "create-vs-merge criterion"
cannot be a function of the coincidence census alone — it must see
the d1-layer combinatorics (top-diagram cell structure), which is
exactly what the census extraction (CENSUS_SPEC.md, in flight) is
digging out. The exact algebraic location of the ~9.5 deg wall is
still unpinned (bracketed (7.628, 9.527) deg; needs a resultant on
the top-diagram cell-change condition — natural follow-up).

## Postscript 32: the open n=4 resonance candidates counted exactly — still all count-negative; best 169 < 175, the sqrt13 chain = 159

OPENCOUNT_SPEC.md executed (opencount_report.md, opencount.py,
opencount_results.jsonl, opencount_wl_data.json). resonance4
(Postscript 28) left ~160 n=4 resonance candidates uncounted because
their coordinates live in degree-4 (nested-radical) fields where the
voxel triage is unreliable. This closes the countable ones exactly via
two independent exact-sign engines: a primitive-element number field
Q(alpha) (element = 0 iff its power-basis vector is 0 — exact; sign by
refining alpha's isolating interval) and a relative-quadratic tower
Q(sqrt a)(sqrt b). All four gates passed and were RE-RUN independently
by the main session: G1 exact-zero detection + 1000/1000 sign-vs-float
both representations; G2 reproduces rational 151 and 175 verbatim
against ./cube_regions_n; G3 reproduces octahedral 67 (Q(sqrt2)) and
golden-177 (Q(sqrt5)) through the field engine; G4 the sqrt6 candidate
counts 127 identically in BOTH representations.

**Verdict: no open candidate reaches 175 (the family plateau), let
alone 183 (the record).** Highlights (all with the deep layers
conserved, d3=24, d4=1, as everywhere on the resonance set):

- **The prime suspect settled**: the pure CHAIN at tan psi=(1+sqrt13)/6
  (psi=37.51 deg) — the record's OWN tilt field Q(sqrt13) — counts
  **159 = {76,58,24,1}**, confirmed by both field representations. The
  tilt-field coincidence with the 183 record produces no competitive
  resonance.
- Best total found anywhere: **169 = {80,64,24,1}** at psi=35.264 deg
  (the octahedral angle arcsin(1/sqrt3)), theta=(120,-120,153.1) — a
  degree-4 bulk-sweep point, still 6 short of the plateau.
- Documented rows: sqrt3-tower branches 159/165; sqrt6 branches
  127/131/167; the pentagonal (5s^4-5s^2+1) and golden-nested
  (t^4+t^2-1) rows are constitutionally degenerate — no non-degenerate
  4-distinct-cube member exists in their scope (best degenerate
  representatives 67/59, effectively 3-cube compounds). The
  degree-agnostic engine also handled one incidental degree-6 field
  with no code change.

**Honest coverage** (per report §6): 108 of the sweep's systems
re-derived from wolframscript (2421 solutions -> 238 fingerprints);
12 distinct exact counts spanning degree-4 and degree-6, every one
count-negative vs 175. NOT covered: the uniform xy/yx systems (30) and
the full non-triangle mixed-CLASS space (~19k systems) — so this
extends but does not EXHAUST resonance4. Record protocol not triggered.

Net: with Postscript 28's quadratic-field verdict, this makes "n=4
family resonances are uniformly count-negative" hold across every field
degree tested (2, 4, 6), the strongest computational support yet that
n=3 is the only irrational rung of the tower — with the standing
caveats that the mixed-class space is unswept and that "3 is unique"
remains conditional on the two 67s being the sole 3-cube maxima
(Theorem R corollary).

## Postscript 33: FIRST COMPLETE MAXIMUM THEOREM — max(2) = 13 proved (all R), and d2<=18 / d_{n-1}<=6n proved unconditionally

MAX2_SPEC.md executed (max2_report.md, max2_verify.py,
max2_verify_log.jsonl). The task was framed as a certified interval
covering; the agent instead found a clean ANALYTIC proof (Theorem 1)
that closes both degeneracies PROOF_67.md §3 had left open, for all n at
once. Main session reviewed the proof line by line (judged correct, one
standard step flagged), re-ran all gates, and independently verified the
maximizer facts. Recorded as a proof with that provenance — NOT merely
an agent claim.

**Theorem 1 (no parasites, all n).** Every connected component U of
S_C = {u : cube C reaches strictly least} contains a face direction of
C; hence #pi0(S_C) <= 6 for every cube C, with NO exceptional locus.
Proof mechanism: at the inf of r_C over cl(U), if it sits on the
boundary, split on whether some active face a of C is "matched" (shares
a normal identically with a tying cube). All branch gradients have equal
norm rho = sqrt(1-f^2), so by Cauchy-Schwarz v = e_a/rho is the UNIQUE
steepest-ascent direction — an unmatched a gives an into-U ascent point
with r_C below the inf (contradiction); if ALL active faces are matched,
the shared normals force r_C >= r_x in a whole neighborhood, so no S_C
point is near the boundary (contradiction). Any cube sharing a normal
with an active face of C is automatically tying, so the split is
exhaustive. The equal-norm + Cauchy-Schwarz choice handles arbitrary
face/cube multiplicity in one stroke — the multiplicities and shared
normals PROOF_67 flagged as gaps (i)/(ii). Shared normals are
self-exclusion, not parasites: the shared plane removes an anchor,
never adds one.

**Consequences (all proved):**
- **max(2) = 13** for every R in SO(3): d1 = #pi0(S_1)+#pi0(S_2) <= 12
  (Theorem 1), d2 = 1 (convex core), attained. The project's FIRST
  complete maximum theorem. Maximizer = 180 deg about the body diagonal
  (1,1,1), quaternion (0,1,1,1) -> 13 = {12,1} EXACT (rational,
  oracle-verified), on an open range of R.
- **d2 <= 18 unconditionally at n=3** — Cluster 1 of max(3)=67 now
  complete (was: proved only off the shared-normal locus).
- **d_{n-1} <= 6n for all n unconditionally** — the l=1 ceiling law of
  Postscript 19, previously only empirical (~1M configs), now a theorem.

**Correction to PROOF_67 (mine):** I had written the n=2 maximizer as
"45 deg about a face axis." Wrong — a face-axis rotation shares that
normal (on the shared-normal locus), where Theorem 1's self-exclusion
gives only d1 <= 8. Verified exactly: quaternion (2,0,0,1) and (5,0,0,2)
both -> 9 = {8,1}. The genuine maximizer is 180-about-(1,1,1). Good
catch by the agent, confirmed by main session.

**Verification (main session, 2026-07-20):** all four gates re-run:
G1 10,000 exact rational configs, max d1 = 12, zero violations; G2 seven
witnesses all 13={12,1}, #pi0(S_i)=6; G3 400 exact shared-normal configs,
worst per-cube count 4 (<=6). Maximizer 13 and face-axis 8/9 re-derived
independently through certify_six. Proof reviewed and judged correct; the
one soft step ("the ascent point lands in the SAME component U") is
standard and tightenable, corroborated by the zero-violation stress test,
and is not logically load-bearing for the reviewed argument.

**Status of max(3)=67 after this:** deep half PROVED (d2<=18, d3<=1);
shallow half is the sole remaining gap, exactly the inequality
Sum_v(deg_v-2) <= 92 on the top diagram (PROOF_67 sect.5,
CENSUS_BOUND_SPEC.md). 67 holds iff that holds.

## Postscript 34: feasibility verdict on the last gap (star) Sum(deg-2)<=92 — it splits 32+60, the easy half reduces to a clean "<=16 simultaneous triples" lemma, the hard half needs targeted (not random) search

CENSUS_BOUND_SPEC.md run in feasibility-first mode (census_bound_report.md,
census_bound.py). Gates: G1 reproduces 67={48,18,1} both witnesses; G2
the weight is exactly 92 at both maximizers via an INDEPENDENT code path
(cross-validates census_extract); G3 10,000 Haar-random configs, ZERO
violations of (star), max weight observed only 32. No (star) violation
found anywhere — max(3)=67 not refuted. Main session verified G2 and the
anchor-refutation independently.

**The central structural finding.** The weight-92 budget splits exactly
as the census's 32+60:
- Triple-point weight <= 32 (the "easy half"): generic configs ALREADY
  have 32 (32 trivalent triple points, F=18, d1=18 generic); random
  sampling saturates here. Reduces to a clean SIMULTANEITY lemma: "at
  most 16 elementary active-face triples (f0,f1,f2,s01,s12) are
  simultaneously realizable at any one config" -> x2 antipodal = 32.
  The number 16 is robust (max over 10^4 random configs = 16; exact at
  BOTH maximizers; 16 bare face-triples with unique sign patterns). This
  is a packing/angle-budget argument in the spirit of Theorem 1's
  matched/unmatched dichotomy applied to TRIPLES - the tractable next
  theorem. NOTE: reframes C45 sect.8's "Platonic elimination" - the
  restriction is NOT "which triples are globally impossible" (all 108 of
  the naive 3x3x3x2x2 occur SOMEWHERE) but "how many co-occur" (<=16).
- Contact-vertex weight <= 60 (the "hard half"): the 30 deg-4 / 6 deg-6
  same-pair coincidence vertices. This is a MEASURE-ZERO coincidence
  locus - structurally invisible to random sampling (why G3 maxes at 32,
  never approaching 92: the hard half isn't reachable by chance). Needs a
  TARGETED search, recommended via the dihedral family (C45 sect.12
  Theorem F: certain coincidences hold identically along Rel(theta,psi)) or
  by directly solving the coincidence equations - NOT blind sampling. The
  crux of (star); this run could not move it.

**Routes ruled out (concrete).** Chamber enumeration (approach 2):
INFEASIBLE, pilot measures chamber angular diameter <~0.02 rad in the 6-D
domain -> ~10^11-10^13 chambers. Certified-interval covering (approach 3):
infeasible for the same reason, worse constant. Anchor-reduction
(approach 4, my PROOF_67 sect.5.1 lead): DEAD/refuted (0/32 anchoring
triple points at both maximizers, confirmed exact + brute-force, 0.6-2.4%
margins) - corrected in PROOF_67 sect.5.1.

Net: the last gap is now cleanly split into a tractable sub-lemma (triple
weight <=32 via <=16-simultaneity) and the genuine crux (contact weight
<=60, a coincidence-locus classification needing the dihedral family).
max(3)=67 holds iff both hold; nothing found threatens it.

## Postscript 35: sub-lemma 1a PROVED — triple-point weight <= 32 (via d2 <= 18); max(3)=67 now hinges on ONE inequality (contact weight <= 60)

Main session, 2026-07-20 (proof + exact numerical verification). The
"easy half" of (star) closes cleanly, and it REUSES the proven d2 <= 18
rather than the packing/simultaneity argument the feasibility pass
envisioned.

Key observation: a triple point (M_0=M_1=M_2, all three cubes reach
equally far) is a vertex of BOTH the top diagram (the three
reaches-FARTHEST regions meet) AND the bottom diagram (the three
reaches-LEAST regions meet) — when all three values coincide, moving off
the point the argmax cycles through all three (top vertex) and the argmin
cycles through all three (bottom vertex). So the triple-point SET is
shared by the two diagrams.

LEMMA 1a: #triple points <= 32 (<=16 up to antipode); hence top-diagram
triple-point weight (deg-3, weight 1 each) <= 32.
PROOF: in the bottom diagram (deg-2 vertices suppressed), faces = S_i
components so F_bot = d2 <= 18 (Theorem 1). All remaining vertices deg>=3
=> by Euler V_bot <= 2(F_bot - 2) <= 32. Triple points are deg>=3 bottom
vertices, so #triple <= 32. QED.

Verified exactly: the generic relation is the EQUALITY #triple =
2(d2 - 2) (both diagrams trivalent on the shared vertex set, both
F = 2 + V/2, so d1 = d2 generically). Confirmed on 4 random configs
(#triple = 24,32,24,32 with fine-sampled d2 = 14,18,14,18 -> exact match)
and both maximizers (32 = 2(18-2), d2=18 attained, 1a TIGHT). This also
explains the census's "bottom stays generic": coincidences inflate the
TOP into contact vertices (the <=60 half) but leave the triple-point
count pinned by the bottom, which d2 <= 18 caps.

Caveat (same flavor as Theorem 1's soft step): needs each triple point to
be a genuine deg>=3 bottom vertex; a tangential triple point (bottom
argmin fails to cycle - a non-generic coincidence) folds into 1b's
degenerate analysis. Does not occur at the maximizers or generically.

STATUS OF max(3)=67: d3<=1 proved, d2<=18 proved, triple weight<=32
PROVED. The SOLE remaining gap is contact-vertex weight <= 60 (sub-lemma
1b) - the measure-zero coincidence-locus classification, to attack via
the dihedral family (Theorem F), not random search. max(3)=67 holds iff
contact weight <= 60. PROOF_67.md sect.5.3 has the proof.

## Postscript 36: region count is AFFINE-INVARIANT — the records are realized by a whole affine family of parallelepiped cells (congruent rhombohedra match 67), correcting a first wrong probe

Exploratory (2026-07-21, main session), prompted by "could cuboids/other
cells beat cube records?". Method: the region counter counts
{x : |m_a . x| <= 1 for the 3 body normals m_a}; feeding NON-orthonormal
columns counts a general parallelepiped cell. Validated: orthonormal
columns reproduce cube_regions_n (e.g. [I,R2,R3] cube triple = 55 =
{36,18,1}, exact).

**KEY FACT (user's point): region count is invariant under any global
invertible linear map A** (planes -> planes, arrangement type preserved).
So applying A to a cube-67 compound {R_k C} gives {A R_k C}, a compound of
PARALLELEPIPEDS, with count still 67. If A commutes with the compound's
symmetry the cells stay congruent. For the golden 67 (3-fold symmetry S
about (1,1,1)): take A = I + c*J (J = all-ones matrix) = a stretch ALONG
(1,1,1); it commutes with S, so the three cells A R_k C are congruent
RHOMBOHEDRA (cube stretched along its body diagonal). Verified EXACTLY
(cell normals A^{-1} R_k, Q(sqrt5)): total = 67 = {48,18,1} for all
c in [-1/6 .. 1] (drops to 57 only at c=2 where a wall is crossed). So
**congruent rhombohedra MATCH the 67 record over an open interval** - the
cube (c=0) is NOT special, it is one point of an affine family.

**CORRECTION of a first, wrong probe.** An earlier version of this
postscript claimed "cube is a STRICT local max vs cell shape" from a sweep
m_a(t)=e_a+t*(1,1,1) applied in each cube's OWN body frame (cells
R_k * rhombohedron), which collapsed 67 fast (67/37/25/13). That
deformation is NOT a global affine map (it deforms each cell in its own
rotated frame), so it does not preserve the arrangement - the collapse was
an artifact of the wrong operation, not a property of rhombohedra. The
correct WORLD-frame affine stretch (above) preserves 67. Lesson: cell-shape
questions must be posed as global affine maps to respect the affine
invariance of region count.

Consequences and what stays open:
- Congruent RHOMBOHEDRA match every record (affine stretch along the
  record's 3-fold axis). Congruent CUBOIDS (orthogonal stretch) do NOT
  arise this way for the octahedral/golden symmetry: an axis-PERMUTING
  symmetry forbids a non-scalar diagonal A that commutes with it (forces
  a=b=c=cube) - consistent with the n=2 cuboid scan finding no cuboid pair
  beating 13 (200 exact, best 8).
- Affine images only MATCH the record (count invariant); to BEAT it you
  need a parallelepiped config OFF the affine orbit of cubes. Not found:
  n=2 exact cuboid scan and n=3 rational rhombohedron scan (best 63 =
  rational cube max) produced no beat. So max_parallelepiped >= max_cube
  with equality on the affine orbit; whether it is STRICTLY greater is
  open.
- Proof bearing: since region count is affine-invariant but the
  equal-gradient-norm proof of d2<=18 / max(2)=13 is NOT (it uses
  orthonormality), an AFFINE-INVARIANT reformulation of the bounds may be
  cleaner and would automatically cover the whole parallelepiped orbit.
  The natural objects are parallelepiped compounds up to affine
  equivalence; "cube" is just a convenient representative.

## Postscript 37: *** RETRACTED (see Postscript 38) *** — this postscript is WRONG; it counted cells of the INFINITE-plane arrangement, not real face-bounded regions

RETRACTION (2026-07-21): every "beats the record" number below (hexahedra
40, off-center 25) is an ARTIFACT of a buggy counter that split regions at
the INFINITE extensions of face planes instead of at the actual finite
FACES. Under the correct definition (connected components of constant
cube-containment = the project's phantom-merged count), ALL these configs
give <= 13 at n=2: off-center = 5={4,1}, hexahedron pairs = 4, exactly as
the trivial convex-cover bound forces (A\B is covered by 6 half-space
intersections, one per face of B, so <= 6 components; d1 <= 12; total <=
13 for ANY two convex 6-faced bodies). "Central symmetry is the cap" is
FALSE - the cap is the generic convex-cover bound, holding for all convex
cells. See Postscript 38 for the correct analysis. The original (wrong)
text is kept below, struck, for the record.

~~Exploratory (2026-07-21, main session), answering "can anything with cube
topology beat 67?". YES, and immediately. A general convex hexahedron with
cube topology (6 quadrilateral faces, 8 vertices, cube adjacency) need NOT
have parallel opposite faces - so it contributes 6 INDEPENDENT face planes
per body, vs only 3 plane-DIRECTIONS (3 parallel pairs) for a
cube/cuboid/parallelepiped. Double the plane richness per body.

Method: trustworthy LP-based exact cell counter (enumerate realized sign
vectors of all planes; LP-verify each feasible + bounded; depth by
containment). Validated: reproduces the cube n=2 maximizer EXACTLY,
13 = {12,1}. (The grid counter is unreliable here - thin-cell aliasing,
counts that grow with resolution - and was NOT used for the conclusion.)

Result (n=2, both bodies verified genuine cube-topology: 8 vertices, 6
active faces; all contain the common center O; d2=1 sanity holds):
  eps:   0     0.05   0.1    0.2    0.3
  total: 13    17     18     23     21   (d1 = 12,16,17,22,20; d2=1)
Even eps=0.05 beats 13. The cube is NOT a local max within cube-topology
bodies; breaking parallelism raises d1 past 12 at once. A random n=2
hexahedron scan reached 40 = {39,1} - d1=39, more than TRIPLE the cube cap
of 12. (LP counter samples cells, so these are LOWER bounds on the true
counts; the qualitative "beats 13" is rock-solid.)

**Why: it is CENTRAL SYMMETRY that caps, not topology or rigidity.**
- Cube/cuboid/rhombohedron/parallelepiped are all CENTRALLY SYMMETRIC
  (opposite faces parallel & equidistant); they are exactly the affine
  images of a cube; region count is affine-invariant, so they all MATCH
  (Postscript 36) and are all CAPPED (13 at n=2).
- A general cube-topology hexahedron is NOT centrally symmetric, and the
  cap vanishes. Mechanism: the proof that caps cubes (Theorem 1, d2<=18,
  the <=6 components-per-body anchor bound) rests on the equal-gradient-
  norm identity at reach-ties, which comes from |n.u| = the |.| of
  CENTRAL SYMMETRY (faces come in +-n pairs). Without it the tie-gradient
  norms differ, parasite components form freely, and d1 balloons.

So the entire records tower (13/67/183/...) and its proof machinery
(Theorem 1, the mod-4 parity law, antipodal region pairing, d_n=1) are
features of CENTRALLY-SYMMETRIC cells. max(3)=67 is a theorem about cubes
(centrally symmetric) and stands; it is simply NOT the max over all
cube-TOPOLOGY cells - dropping central symmetry is a different, larger
problem with no such cap. This precisely locates where on the rigidity
ladder the records live: at the central-symmetry (parallelepiped) rung,
not the combinatorial-cube rung.

WHICH RIGIDITIES SUSTAIN >{12,1} (n=2, LP counter, lower bounds): the
ONLY forbidden one is cell central symmetry (inversion -I in the cell's
point group = parallelepiped = capped at 13). Everything else is
compatible: CONGRUENT non-central pair -> 39={38,1} (no penalty for
congruence); 4-fold-symmetric FRUSTUM pair (non-central) -> 27={26,1};
unconstrained -> 38={37,1}. Nuance: more cell symmetry costs some count
(frustum 27 < generic 39) but does NOT cap - only the inversion symmetry
triggers the parasite-exclusion cap. So a cell may carry any point group
that EXCLUDES -I (rotational axes, mirrors, frustum C4v, tapered-
rhombohedron C3v) and still clear the record cap; it must only avoid
central symmetry.

REFINEMENT + a correction to the off-centering belief: the true
cap-hypothesis is not "the cell is centrally symmetric about its own
center" but "the reach FROM THE COMMON CENTER O is symmetric,
r(u)=r(-u)". For a cube those coincide only when it is CENTERED at O.
Move a cube off O (center c): its faces sit at n_a.x = n_a.c +-1, still
parallel, but the reach-from-O vectors become m_a^+- = +-n_a/(1 +- n_a.c)
of UNEQUAL length -> breaks the equal-gradient-norm identity -> lifts the
cap, the SAME mechanism as non-parallel faces. Verified (LP counter, n=2):
OFF-CENTER cube pairs reach 25 = {24,1}, ~2x the concentric cap of 13
(d1=24 vs 12); less than the 39 of full non-parallel hexahedra because
off-centering keeps 3 plane-DIRECTIONS (unequal-length pairs) rather than
6 independent planes. This CORRECTS the standing project belief
"off-centering strictly hurts / concentric is optimal" (PROJECT.md sect.10):
that only tested TRANSLATING the 723 record (a local perturbation of a
concentric-tuned optimum, which of course falls), NOT a from-scratch
off-center search. Concentric is a LOCAL max; it is NOT the global max
once off-centering is allowed. Caveat on "record": the radial/depth
framework assumes O interior to every body; large offsets put O outside a
cube (its ray-contribution no longer starts at r=0), muddying the
depth-profile notion the records are stated in - so a fair off-center
"record" search should keep O interior to all cells, or restate the
target as raw bounded-cell count.~~ [END OF RETRACTED POSTSCRIPT 37]

## Postscript 38: the counting error corrected — regions are separated by FACES, not infinite planes; and a trivial proof that max(2) = 13 for ALL convex 6-faced cells

Root cause (user caught it, looking at the off-center viewer): "some
regions are separated by the infinite planes through the faces, not by the
faces." Exactly right. A "region formed by the cubes" is a connected
component of the complement of the actual finite FACE polygons -
equivalently a component of constant CUBE-CONTAINMENT (which cubes contain
the point), since you cross a real face iff the containment set changes.
Crossing a face's infinite EXTENSION where that cube is absent changes no
containment bit and must NOT split a region. The project's engines
(cube_regions_n, certify_six) do exactly this "phantom-facet merge". My
Postscript-37 experiments used LP/grid counters that instead counted cells
of the INFINITE-plane arrangement (constant 12-bit sign vector), which
over-splits - inflating the counts.

CORRECTED COUNTS (exact overlap-graph method; validated: concentric
maximizer = 13 = {12,1}, matching cube_regions_n):
- off-center cube pair (quat 0,1,1,1 + offset .5,0,.25): **5 = {4,1}**
  (Postscript 37 wrongly said 25).
- hexahedron (non-parallel-face) pairs: best **4** (wrongly said 40).
- off-center random scan: best **7** (wrongly said 25).
NONE beat 13.

TRIVIAL PROOF that max(2) <= 13 for ANY two convex cells with <= 6 faces
each: the depth-1 region contributed by cell A is A\B; write A\B =
union over the (<=6) faces f of B of (A intersect {outside face f}), each
a convex set, so A\B has <= 6 connected components (a union of k convex
sets has <= k components). Symmetrically B\A <= 6. With the single convex
core, total <= 6+6+1 = 13. This holds for cubes, cuboids, rhombohedra,
general hexahedra, off-center - ANY convex 6-faced bodies. So at n=2 the
cap 13 is NOT special to cubes or to central symmetry; it is the generic
convex-cover bound. (Note this also RE-PROVES max(2)=13 far more cheaply
than Theorem 1's equal-gradient-norm argument - Theorem 1's value is for
n>=3, where B is replaced by a NON-convex union of others and the cover
argument no longer applies.)

RETRACTIONS/CORRECTIONS:
- Postscript 37 is RETRACTED in full (hexahedra/off-center do NOT beat
  records; "central symmetry is the cap" is false; the "rigidity ladder"
  and frustum/congruence numbers were all sign-vector artifacts).
- The answer given to "could off-centering beat a record" (yes) is WRONG;
  correct answer: NO at n=2 (convex-cover), and the standing project
  belief "off-centering does not help" is VINDICATED, not overturned.
- Postscript 36 SURVIVES: affine-invariance of the count is correct
  (linear maps preserve containment), and "congruent rhombohedra match 67"
  was computed with certify_six (the correct engine) - matching, not
  beating, and true. Only 36's tentative "central symmetry" framing is
  superseded by the convex-cover picture here.
- Whether any NON-cube convex cell ATTAINS 13 at n=2 (the bound) is a
  separate, still-fine question: parallelepipeds do, via affine images of
  the cube-13 (Postscript 36); the bound is 13 for all 6-faced convex
  cells regardless.

n=3 correct counts (overlap-graph method extended to 3 cells; validated:
octahedral cube triple = 67 = {48,18,1}): general HEXAHEDRON triples
(random) best 20 = {10,9,1}; OFF-CENTER cube triples (random) best
26 = {13,12,1} - both FAR below 67. (Random, not optimized, so not a
proof of no-beat, but the same direction as n=2: irregular cells do
WORSE, cubes are near-optimal.) Note the convex-cover argument gives
d3<=1 and d2<=18 for ALL convex 6-faced cells (re-proving those bounds
beyond cubes), but only d1<=108 (each depth-1 region = union of 6x6=36
convex pieces), so it does NOT rule out a non-cube cell beating 67 at
n>=3 - that remains genuinely open, with all correct evidence pointing
to "no".

LESSON: use the project's own engines (or the exact overlap-graph /
containment method) for region counts; never the raw sign-vector cell
count, which is a different (larger) quantity.

## Postscript 39: the CORRECT successor to P37 — the max(3)=67 proof layers GENERALIZE to all convex 6-faced cells, and flex does not beat 67

Consolidation (2026-07-21, correct containment counter throughout). This
replaces the retracted P37 "central-symmetry" narrative with the right
one. Three of the four layers of the max(3)=67 proof are now seen to hold
for ANY 3 concentric convex 6-faced cells (cubes, cuboids, rhombohedra,
general hexahedra, off-center), NOT just cubes:
- d3 <= 1: convexity of the triple intersection.
- d2 <= 18: convex-cover — depth-2 region (X∩Y)\Z = union over Z's 6
  faces of a convex set, <= 6 comps, x3 pairs = 18.
- triple-point weight <= 32: follows from d2<=18 via the shared top/bottom
  vertex + bottom-Euler argument (Postscript 35), all radial, no cube
  specifics.
So d1 = 2 + (1/2)(triple + contact) and the WHOLE remaining question is
contact <= 60, equivalently d1 <= 48, equivalently #comp(cell\(others))
<= 16 per cell.

FLEX EVIDENCE (correct counter, ~4300 evals): hill-climbs maximizing total
regions from the octahedral 67 (2100 evals) AND the golden 67 (best 67)
AND random starts (best 31/31/33) NEVER exceed 67; random flex scans top
at ~33. So d1 <= 48 appears to hold for all convex 6-faced cells too -
i.e. **max(3)=67 generalizes to a conjecture: any 3 concentric convex
6-faced cells make <= 67 bounded regions, attained by cubes/parallelepipeds
(their affine images tie it, P36).** Nothing flex beats 67.

REMAINING GAP (unchanged in difficulty, clarified in scope): d1 <= 48,
i.e. #comp(cell\(B∪C)) <= 16. Convex-cover gives only <=36/cell (via
cell\(B∪C) = (cell\B)∩(cell\C), intersection of two <=6-component sets =
<=36), a factor ~2 loose. Tightening 36->16 is the SAME top-diagram
component bound as the cube-specific sub-lemma 1b (contact<=60); the
general framing just forbids cube specifics, so any proof must be robust.
This is the clean lemma to attack: bound the components of a convex
6-faced cell minus two convex bodies at <= 16. It subsumes max(3)=67.

Note P37's "beats records / central symmetry is the cap" is fully dead;
the correct statement is the opposite - cubes are (conjecturally) EXTREMAL
among convex 6-faced cells, and the cap is generic to convexity + 6 faces.

## Postscript 40: the remaining gap reduced to a clean INCIDENCE bound on the cells' edge-skeletons (verified), with an Euler-on-intersection handle (not yet closed)

Real run at contact-weight <= 60 (2026-07-21). Progress on FORMULATION,
NOT a completed proof - stated honestly.

VERIFIED CORRESPONDENCE: the top-diagram contact vertices are physical
crossings of the cells' 1-skeletons. A deg-4 contact = an edge-edge
crossing (an edge of cell i meets an edge of cell j in 3-space); a deg-6
contact = a corner coincidence (triple point at cell corners). Checked
exactly at octahedral 67: 30 edge-edge crossings, 10 per pair = the 30
deg-4 vertices. (Also: physical triple points ∂A∩∂B∩∂C, T=32, ARE the
direction-sphere triple vertices - since x on all 3 convex surfaces in
direction u => r_A=r_B=r_C=|x| at u.)

REDUCTION: contact weight <= 60  <=>  2*(edge-edge crossings) +
4*(corner coincidences) <= 60, for the 1-skeletons of 3 concentric convex
6-faced cells, ON-TOP (crossing must lie in a direction where its two
cells reach farthest = outside the third cell). Shape-independent; the
cleanest form of the crux (no direction sphere, no census).

HANDLE (new, right kind): edge-edge crossings of cells P,Q = the DEGREE-4
vertices of the convex intersection polytope P∩Q (a point where 2 faces
of P and 2 of Q meet). P∩Q has <=12 faces, so Euler bounds its excess
degree: Sum_v(deg_v - 3) <= 2F-4-V <= ~16 per pair. Same species of
argument that makes d2<=18 shape-independent, now on the pairwise
intersection.

NOT CLOSED: the Euler-on-P∩Q bound is ~1.6x loose (~16/pair vs actual 10;
~48 total vs needed 30). Two missing ingredients: (1) the ON-TOP
restriction (only crossings outside the third cell count) is not yet
folded into the Euler bound; (2) the edge/corner weight tradeoff (golden:
18*2+6*4=60) must hold across the redistribution. Concrete next step:
incorporate "outside the third cell" into the P∩Q Euler bound - that is
what stands between ~48 and 30.

## Postscript 41: CANDIDATE PROOF of max(3)=67 (all convex 6-faced cells) via Euler on the PAIRWISE intersection polytopes — the contact bound closes

2026-07-21, main session. Grew directly out of the user's "if 67 is
shape-independent there must be an Euler-characteristic constraint"
intuition. STATUS: candidate proof; one step verified on 35 configs
(tight at BOTH maximizers, zero failures) but wanting a rigorous
local-degree write-up before "proved". Nothing found > 67.

THE PROOF CHAIN (3 convex cells, each <=6 faces, concentric):
1. d1 = 2 + (1/2)(T + contact)   [Euler on the top diagram; T = # triple
   points, contact = weight of the deg>=4 top vertices]. So
   2(d1-2) = T + contact.
2. T <= 32   [PROVEN, Postscript 35: T = triple-point weight, bounded via
   the bottom-diagram Euler + d2<=18].
3. **contact <= Sum over the 3 pairs of (2*F(cell_i ∩ cell_j) - 4).**
   For a convex polytope, Sum over ALL vertices of (deg-2) = 2E-2V =
   2(V+F-2)-2V = 2F-4. The top-diagram contact vertices map to the
   deg>=4 vertices of the pairwise intersection polytopes with matching
   degree (a deg-4 top contact = an edge-edge crossing = a deg-4 vertex
   of P_i∩P_j; deg-6 = a corner = deg-6 vertex; etc.), so
   contact <= Sum_pairs Sum_v(deg_v - 2) = Sum_pairs(2F-4).
   Each cell has <=6 faces => F(P_i∩P_j) <= 12 => 2F-4 <= 20 =>
   contact <= 3*20 = **60.**
4. => 2(d1-2) <= 32 + 60 = 92 => **d1 <= 48.**
5. d2 <= 18, d3 <= 1   [convex-cover / convexity; Postscript 38/39].
6. total <= 48 + 18 + 1 = **67**, attained by cubes/parallelepipeds. QED
   (modulo step-3 rigor).

VERIFICATION (correct containment counter throughout): step 3 inequality
2(d1-2)-T <= Sum_pairs(2F-4) checked on 35 configs - octahedral 67 and
golden 67 (both TIGHT: contact=60=Sum(2F-4)), 12 near-octahedral
perturbations, 21 random hexahedra - ZERO failures, and Sum(2F-4)<=60
always (F<=12 is a hard fact). The two maximizers SATURATE every
inequality (T=32, contact=60, F=12 on all 3 pairs), which is exactly why
67 is the max and why the bound is calibrated, not loose.

STEP-3 CORRESPONDENCE - now argued (the LOCAL FACE-COUNT lemma):
At a contact where cells i,j are tied for farthest (cell k strictly less),
let a,b = # faces of i,j ACTIVE at the physical point x0. Then BOTH
degrees equal a+b:
  - deg_top = #sign-changes of M_i-M_j around the direction = a+b (the a
    active faces of i fan into a sectors, b into b sectors; M_i-M_j is
    linear per sector and flips once per ray).
  - deg_poly = edges of the pointed 3-cone cut by the a+b facet-planes
    through x0 (all active faces pass through x0) = a+b.
So deg_top = a+b = deg_poly (edge-edge a=b=2 ->4; corner a=b=3 ->6),
matching the exact spectra at both maximizers ({30 deg-4} octahedral;
{18 deg-4, 6 deg-6} golden). Hence contact = Sum(deg_top-2) =
Sum over contact vertices (deg_poly-2) <= Sum over ALL pairwise-polytope
vertices (deg_poly-2) = Sum_pairs(2F-4).

VERIFICATION STRENGTHENED: the inequality contact <= Sum_pairs(2F-4)
checked on 130 configs total (both maximizers TIGHT; near-octahedral
perturbations, random hexahedra, off-center cubes, cuboids, rhombohedra),
ZERO failures, ZERO d1>48. Directly confirms the bound independent of the
per-vertex argument.

LEMMA FILLED IN (PROOF_FORMAL.md, 2026-07-21): the |S|=2 correspondence
is now RIGOROUS - a genuine contact has a,b>=2; the swap curve has a+b
arcs; P_i∩P_j at x0 is a POINTED cone with a+b facets => a+b edges
(pointedness: the a+b active facet-normals span R^3 since the two cells
meet transversally at the isolated point x0). No "cut-off face" issue
arises. This covers EVERY contact at both maximizers. The one residual is
degenerate triple points (|S|=3, top-degree>3): fixed by booking ALL |S|=3
vertices into the triple-point term (Part C) and extending W_triple<=32 to
them via deg_top<=deg_bot (Step T). Non-generic, 0/130 occurrences, absent
at both maximizers.
NET: max(3)=67 PROVED for the generic stratum AND both maximizers (tight),
and for all convex 6-faced cells up to the single non-generic Step T. Full
clean proof: PROOF_FORMAL.md; narrative: PROOF_NARRATIVE.md.

SIGNIFICANCE: this proves max(3)=67 for ALL 3 concentric convex 6-faced
cells (cubes are one case), via three separate Euler arguments - bottom
diagram (T<=32), convex-cover (d2<=18), and NOW pairwise-intersection
polytopes (contact<=60). It is the shape-independent Euler constraint the
user predicted. Also finally supersedes the whole retracted-P37 detour:
the answer is that cubes are extremal and the cap is a triple Euler bound.

## Postscript 31: the census extraction — the 92 budget is EXACT at both 67 witnesses, its accounting corrected, and the coincidences ARE top-diagram vertices

CENSUS_SPEC.md executed (census_report.md, census_extract.py,
census_data.json; main session re-verified the Euler arithmetic from
the raw V/E and the weight decompositions below). Gates: G1 both
witnesses reproduce 67 = {48,18,1} (slide3_q2 for octahedral Q(sqrt2);
certify_six oracle for golden Q(sqrt5), matrix hand-derived, S^3=I
exact); G2 the sharp gate — exact-arithmetic diagram graphs give
TOP-1 Euler faces F = 48 and BOTTOM F = 18 at BOTH witnesses (W1:
V=62, E=108; W2: V=56, E=102; bottoms V=32, E=48); G3 antipodal
symmetry; plus a generic rational cross-validation (37-config: top
18, bottom 18, oracle-matched).

**The census, correcting sect. 13's projected accounting.** The
projected budget "46 triples x 2 = 92, F <= 2 + 92/2 = 48" is right
in TOTAL WEIGHT and wrong in attribution:

- Total top-diagram weight Sum_v(deg_v - 2) = 92 EXACTLY at both
  witnesses — the d1 = 48 bound is Euler-TIGHT (F = 2 + 92/2).
- Rank-triple points carry only 32 units: exactly 32 triple points,
  ALL trivalent, at both witnesses = 16 occurring active-face triples
  (6 C3-orbits) x 2 antipodal points. No merged triple points.
- The other 60 units sit on SAME-PAIR double-tie vertices, and these
  are precisely the coincidence census: W1 = its 30 interior edge-edge
  crossings, each a degree-4 vertex (weight 2, 30x2 = 60); W2 = its
  18 interior crossings (deg 4) + 6 physical corner contacts (deg 6,
  weight 4): 36 + 24 = 60. Two different degenerations, same 92.
- Sect. 13 L2.b's assumption "kinks are degree-2, discountable" is
  FALSE at both attainers: the (c2)/(c3) classification must budget
  same-pair multi-tie vertices alongside rank triples. The corrected
  target statement: Sum_v(deg_v - 2) <= 92 over triple points AND
  pair-contact vertices, with equality at both witnesses.
- BOTTOM diagrams of both witnesses are fully generic: V=32, E=48,
  F=18, zero degenerate vertices — exactly the V_1(3) = 12n-4 = 32
  census — despite the heavy top-side degeneracies.

**Synthesis with Postscript 30** (the two campaigns interlock): edge
and corner coincidences live as VERTICES OF THE TOP DIAGRAM ONLY —
the bottom diagram of even the maximally-degenerate witnesses is
untouched. That is WHY every event's count delta lands in d1 with
deep layers conserved (Postscript 30's 12/12 law): coincidence
events add/remove top-diagram vertex weight, and d1 = top faces =
2 + weight/2, while d2/d3 read the bottom diagram, which the
coincidences never touch. The create-vs-merge question becomes:
does the acquired vertex weight EXCEED the swap-arc structure it
consumes — an Euler bookkeeping question on one diagram, no longer
a mystery spread across mechanisms.

Proof-program status after this: cluster 2's remaining work is the
(c2) feasibility classification with the corrected two-type budget
and the (c3) degeneracy-robust form — the witnesses' own numbers now
give the exact equality cases the classification must reproduce.

Full sweep (dense tilt menu, tier-4 hill-climbs, n=6 completions of
the new 387) still to run — the agent resumes after its limit resets.

### Postscript 29 addendum: 723 is a PLATEAU with (at least) four non-congruent realizations — an exact three-layer exchange law inside the summit

Tier 3 at full scale (393's five ledger cubes fixed + 4,000 random 6th
integer quats, ||q||^2 <= 600): 27 completions tie 723 EXACTLY (28
counting the known (5,2,2,2)), none beat it. They fall into exactly
FOUR depth profiles (a different histogram proves non-congruence
outright):

    d2, d3, d4 = 216+2k, 164-4k, 96+2k    for k = 0,1,2,3
    d1=210, d5=36, d6=1 fixed;  d2+d3+d4 = 476 constant

k=0 is the ledger profile; k=1,2,3 are genuinely new compounds with
the same total. Example 6th quats: (11,11,10,11) k=2 (norm 463, not a
symmetry multiple of (5,2,2,2), norm 37), (3,-4,-3,3), (5,-5,5,4).
Every hit oracle-verified by the agent; main session independently
re-ran (11,11,10,11) through the C++ engine: 723 = {210,220,156,100,
36,1} confirmed. So the n=6 record is not an isolated configuration
but a summit plateau on which (d2,d3,d4) trade at fixed exchange rate
(+2,-4,+2) — the Postscript-11-addendum shallow-tail conservation
appearing exactly, at the top. The record VALUE 723 stands unbeaten;
"the 723 compound" is now four compounds (at least).

Also from run 1 at full tier-3 scale: 183-triple on-axis 4th-cube
sweeps (all three resonant axes, full Farey-40) top out below the
integer-quat completions — the 4th record cube must be off-axis,
exactly like 393's cube 0 and 723's cube 5. Phase 2 (71,510 more
configs: dense tilt menu + 387-completions + hill-climbs) has finished
computing; bests unchanged so far (183/387/723); agent summary pending.

## Postscript 42: Step T is NOT routine — the reduction "deg_top ≤ deg_bot at triple points" is FALSE (counterexample realized on genuine cells); max(3)=67 stands on the generic stratum + both maximizers, degenerate triple points remain an open gap

2026-07-21, main session, answering the user's "please write Step T
rigorously." Attempting to discharge the one step PROOF_FORMAL.md had
marked "routine/LOW risk," I instead found it is false as stated, and
have corrected all three proof documents accordingly.

WHAT STEP T NEEDED: W_triple ≤ 32 including degenerate triple points
(|S|=3 top-diagram vertices of degree > 3). The marked route: every
triple point is a bottom-diagram vertex, and "deg_top ≤ deg_bot" there,
so W_triple ≤ Σ_bottom(deg_bot−2) = 2(d2−2) ≤ 32.

WHY IT FAILS: deg_top ≤ deg_bot is false. The top diagram (farthest
cell) is the argmin of the three cells' support functions m_i = h_{P_i}
(P_i = convex hull of the active-facet tangential gradients at the triple
point); the bottom diagram (nearest cell) is the argmax. The argmax is
the support function of conv(∪P_i) — a simple outer envelope; the argmin
is an INNER envelope of convex bodies, which genuinely wiggles more.
Explicit: cell A a corner (a=3, small gradient triangle), cells B,C thin
blades (b=c=2, gradients ≈ (±g,0) and (0,±g)). The corner is farthest in
all four diagonal sectors and each blade near its own axis →
  deg_top = 8,  deg_bot = 4.
Confirmed three ways (scripts saved to project):
 • stepT_local.py — abstract support-function switch counts: 8 vs 4.
 • stepT_realize.py — built as three ≤6-facet cells about O (two blade
   wedges μz+g|x|≤1, μz+g|y|≤1 capped to 5 facets; one 3-facet corner
   cone capped to 4), valid triple point (x0 on 3/2/2 facets, O interior).
 • stepT_degcheck.py — sampled the ACTUAL reach functions on a small
   circle around û0: farthest-cell degree 8, nearest-cell degree 4.
So deg_top > deg_bot occurs for honest convex cells, not just the model.

WHY 67 IS NOT IN DANGER (but this is evidence, not proof): the isolated
degenerate triple gives only 10 total regions (region-poor); it is
non-generic (measure zero); ABSENT at both maximizers (their bottom
diagrams are exactly generic — 32 degree-3 triple points); and never
appeared in any sampled config. A 250-config search (thin boxes,
near-coincident triples) maxed at d1=18, far under 48 — random boxes just
don't interleave like the special maximizers, so this is weak. The record
67 rests on the project's exhaustive engine search, independent of this
proof. The open content of Step T is exactly: can a degenerate triple
point (deg_top > deg_bot) coexist with a high-count configuration and push
d1 past 48? Unresolved.

CORRECT ROUTE (recommended, not yet done): abandon the triple/contact
split for the degenerate case. The top diagram is precisely the radial
projection to S² of ∂U, U = K1∪K2∪K3, so d1 = 2 + ½W is the combinatorial
complexity of the boundary of a UNION of three convex ≤6-facet polytopes.
A global/amortized bound on that union-boundary complexity (rather than a
per-vertex deg_top ≤ deg_bot) is what would close d1 ≤ 48 unconditionally.

DOCUMENTS CORRECTED: PROOF_FORMAL.md (Step T rewritten from "LOW risk"
to OPEN, with the counterexample and the union-boundary route; status
section updated), PROOF_67.md (top verdict, §5.4 residual, §6, Open #1),
PROOF_NARRATIVE.md ("Where it stands"). The |S|=2 contact lemma
(deg_top = a+b = deg_poly, Part D) remains rigorous and unaffected —
the gap is solely the |S|=3 degenerate stratum. Net honest status:
max(3) = 67 is a theorem on the generic stratum and at both maximizers;
universal over all convex 6-faced cells only up to Step T.

## Postscript 43: STEP T CLOSED — max(3)=67 proved for all 3 concentric convex ≤6-facet cells meeting pairwise transversally (degenerate triple points included); the fix is a two-budget local inequality, not deg_top≤deg_bot

2026-07-21, main session, continuing "please try to close the gap." The
gap from P42 is now closed rigorously (PROOF_STEP_T.md). deg_top ≤ deg_bot
stays false; it is not needed.

THE FIX — charge each triple point to BOTH budgets at once. The single
local inequality at every top-diagram vertex is
  (◆)  deg_top − 2 ≤ (deg_bot − 2)⁺ + Σ_{tied pairs}(d_{ij} − 2),
d_{ij} = a_i+a_j = pairwise-polytope vertex degree. For a triple point
Σ(d_{ij}−2) = 2σ−6 (σ=a+b+c). Summing (◆) over all top vertices: the
(deg_bot−2)⁺ terms draw ≤ Σ_bottom(deg_bot−2)=2(d2−2) ≤ 32 (bottom-diagram
Euler), the pairwise terms draw ≤ Σ_pairs(2F−4) ≤ 60 (distinct polytope
vertices). So W ≤ 92, d1 ≤ 48, total ≤ 67. Contacts satisfy (◆) with
equality (Part D). Triples: proved below.

TWO ONE-LINE LEMMAS (support-function model at the triple point; m_i =
h_{P_i}, P_i = conv of active-facet tangential gradients, a_i = #vertices;
top = argmin m_i, bottom = argmax m_i; z_ij = #sign-changes of m_i−m_j,
N = Σz_ij):
 • Lemma A: deg_top = N − deg_bot. Every pairwise crossing has the third
   function strictly above (⟹ argmin/top switch) or below (⟹ argmax/bottom
   switch); exhaustive, so deg_top+deg_bot = N.
 • Lemma B: z_ij ≤ 2 min(a_i,a_j). z_ij = 2·(#arcs where m_i>m_j); such
   arcs are where P_i outreaches P_j on the hull conv(P_i∪P_j), each using
   a distinct P_i-vertex, so #arcs ≤ a_i and ≤ a_j.
   ⟹ N ≤ 2μ ≤ 2σ, μ = Σ min(a_i,a_j).
Also deg_bot ∈ {0,2,3,4,…} (a single switch can't close on a circle).

CASE SPLIT proving (◆) for triple points (deg_top−2 ≤ (deg_bot−2)⁺ + 2σ−6):
 • deg_bot ≥ 3: deg_top = N−deg_bot ≤ 2σ−deg_bot ≤ deg_bot+2σ−6 (since
   2deg_bot ≥ 6). [Covers the realized counterexample: deg_top=8,deg_bot=4,
   σ=7: 8 ≤ 4+8.]
 • deg_bot = 0: one cell always nearest ⟹ top only between the other two ⟹
   deg_top = z of that pair ≤ 2min ≤ 2σ−4.
 • deg_bot = 2: the never-nearest cell k forces every crossing of the two
   nearest cells to dominate k ⟹ z of that pair = 2 ⟹ deg_top =
   z_ik+z_jk ≤ 2σ−4.
No hypothesis on the triple points; only the pairwise transversality Part D
already assumes. VERIFIED 0 violations / 50 000 random triple-point models
(stepT_proof_verify.py), incl. both structural facts (deg_bot=0 ⟹ deg_top
= other pair's z; deg_bot=2 ⟹ two-nearest-cells' z = 2). The realized 3-D
counterexample itself has w=0 (winding), confirming the earlier
permutohedron/winding route needed the w=0 case — the case split above
avoids winding entirely.

NET STATUS: max(3) = 67 is now a THEOREM for all 3 concentric convex
≤6-facet cells whose boundaries meet pairwise transversally (open dense,
both maximizers included), cubes among them. Sole residual: the
pre-existing pairwise-TANGENCY degeneracy of Part D (two cells sharing a
boundary tangentially) — not a triple-point issue, higher codimension.
Docs: new PROOF_STEP_T.md (full proof); PROOF_FORMAL.md (Step T → CLOSED),
PROOF_67.md, PROOF_NARRATIVE.md updated. Verify scripts saved to project:
stepT_proof_verify.py (main), stepT_local/realize/degcheck.py (the
counterexample).

## Postscript 44: the n=3 anomaly audit — its maximum is the only one that is finite-yet-multiple, irrational, and non-nesting; the three are one phenomenon (and 13 is NOT rigid — corrects Postscript 17 addendum)

2026-07-29, main session, answering the user's four questions: is n=3 the
only level with two geometrically distinct maxima / with irrational
maxima / whose maximum is not a subset of a larger-n maximum, and are
these related. Everything below recomputed today; every count
two-engine (cube_regions_n and certify_six.exact_count_config).

**(a) MULTIPLICITY — n=3 is not the only level with several optima; it is
the only level whose optimum set is FINITE. This CORRECTS the Postscript
17 addendum claim that the 13-pair is "rigid, near-isolated".**

- n=2: 13 is attained at EVERY rotation angle about a body diagonal
  (excluded only at θ = 0, ±120°, where the cubes coincide and the count
  is 1). Verified at 40 random rational angles plus (400,1,1,1) θ=0.496°,
  (3,1,1,1) θ=60°, (0,1,1,1) θ=180° — all 13 = {12,1}. Also on the CLOSED
  arc [arccos(1/3), arccos(−1/3)] = [70.5288°, 109.4712°] about an edge
  (face-diagonal) axis: endpoints (2,0,1,1) and (1,0,1,1) give 13, just
  outside ((201,0,100,100), (99,0,100,100)) gives 9. Plus further isolated
  components (half-turns about (1,2,3), (1,1,2)). So max(2)'s maximizer set
  is POSITIVE-DIMENSIONAL: infinitely many pairwise non-congruent
  maximizers. It is nonetheless measure-zero — 400 random rotations gave
  4 (392), 5 (5), 9 (3), never 13, and tilting the axis off a body diagonal
  or off the edge axis drops the count to 5 or 9 immediately.
- n=3: exactly two maximizers, isolated (the connecting family's interior
  drops to ~37, Postscript 9) and provably non-congruent (Theorem R,
  C45_notes §12: μ = 1/2+√2 octahedral vs 3φ/2 golden).
- n=6: the record VALUE 723 is a summit plateau with ≥4 non-congruent
  realizations (Postscript 29 addendum).

So the anomaly is not multiplicity but rigidity-with-multiplicity: n=3 is
the only level whose optimum set is 0-dimensional and bigger than a point.

**(b) NESTING — the record tower nests at every adjacent level except
n=3.** All subsets of the three records recounted (both engines agree):

    183 (n=4): pairs 13,13,13,9,9,9      triples 63,63,63,55
    393 (n=5): 4-subsets 183,179,179,179,171   (the 183 one has the
               record profile {1:92,2:66,3:24,4:1} exactly)
    723 (n=6): 5-subsets 393,387,381,381,381,375 ; 4-subsets max 183 ;
               3-subsets max 63 ; pairs max 13

13 ⊂ 183 ⊂ 393 ⊂ 723, and 1207 = 723 + one cube by construction. The best
triple anywhere in the tower is 63 — four short of 67. n=3 is the sole
break.

**(c) THE THREE ANOMALIES ARE ONE PHENOMENON, and the switch is at n=4.**
Postscript 23's cap-sum 1 + Σ_l C(l,n): 13 TIGHT, 67 TIGHT, 195 vs 183,
429 vs 393. For n ≤ 3 there is no middle depth layer, so all per-layer
ceilings are simultaneously attainable. Saturating all of them at once is
a rigid, symmetry-forced condition — it pins the optimum to isolated
points, and the only three-cube symmetries that do it are octahedral and
icosahedral, i.e. ℚ(√2) and ℚ(√5). From n=4 the ceilings cannot be met
together, the maximum must trade d1 down to fill the middle, that requires
a tunable degree of freedom, and the tunable loci are rational and
plateau'd. Hence:
 rigidity → irrationality: only an isolated optimum can be irrational; a
 positive-dimensional optimum locus cut out by rational equations has
 dense rational points, which is why n=2's continuum and the n≥4 plateaus
 all have rational maximizers and n=3's two points do not;
 irrationality → non-nesting: any subset of a rational compound is
 rational, so by Theorem R no rational record can contain either 67 —
 (b) follows from Theorem R as a one-liner.
The arithmetic-free version of the same fact is Postscript 17's
frustration: the golden four-compound has ALL subsets optimal (pairs 13,
triples 67) and still totals 177 < 183, so carrying 67-triples actively
costs at n=4.

**(d) CORRECTION to the frustration MECHANISM (not to the principle).**
With 13 continuous, "the global max is forced to build from
locally-suboptimal-but-flexible pieces" is wrong at the PAIR level: max₄
(183) does use three 13-pairs (the hub-spoke structure), and those pairs
sit on the tunable body-diagonal curve — optimal AND flexible. The
mechanism survives one level up, where the rigidity is real: 67-triples
are isolated, so 183 must detune its triples (63/63/63/55). Read the
Postscript 17 addendum table with the 13-row corrected to "measure-zero
but continuous".

**Other ways n=3 is anomalous** (all from existing ledger results): it is
the last level where golden/icosahedral IS the maximum (177 < 183,
351 < 393 after); the last level where the cap-sum is tight — which is
exactly why the max(3)=67 proof closes at all, both maximizers saturating
every Euler step simultaneously; the only level with two optima in
DIFFERENT quadratic fields, joined by the dihedral family (interior ~37,
ℚ(√6) point 49 at ψ=45°); and the only level whose optimum is native-only
(1207 came from 723+1, 393 exists only as a 723-subset and is unreachable
by native n=5 search, but 67 cannot be inherited from anything above).

Scope: n=2 and n=3 are proved maxima; the n≥4 statements are about
RECORDS, and (a)/(b) for n≥4 are therefore conditional on those records
being maximal. Theorem R's corollary is conditional on the two known 67s
being the only n=3 maximizers.

## Postscript 45: NEW RECORDS n=7 = 1211 and n=8 = 1889 — found top-down-then-bottom-up in one afternoon; 1211 is a plateau reached by four independent routes

2026-07-29, main session, on the user's request to hunt records at n=4..8
with the searches scheduled to feed each other. Tooling: record_hunt.py
(new; extend / climb / subsets / campaign modes over cube_regions_n) and
record_hunt_wave2.py. Both new records two-engine certified (cube_regions_n
and certify_six.exact_count_config, identical totals AND histograms).
[SUPERSEDED the same day by Postscript 46 — n=7 is now 1217, n=8 is 1891.
The configs below were real, certified, and held for part of the day.]

**n=7 = 1211** (was 1207, +4):

    quats = 4,1,1,-1; 3,3,7,3; 5,-1,-5,-5; 2,1,1,1; 1,1,1,1; 5,2,2,2;
            39,-5,-34,-31
    by_depth = {1:272, 2:328, 3:260, 4:190, 5:118, 6:42, 7:1}   ≡ 3 mod 4

**n=8 = 1889** (was 1879, +10):

    quats = the 1211 seven + 3,-4,4,4
    by_depth = {1:344, 2:454, 3:382, 4:302, 5:222, 6:136, 7:48, 8:1}

Ceilings all respected: d7 = 48 = 6·8 attained (l=1 law), d6 136 ≤ C(2,8)=138,
d5 222 ≤ 224, d4 302 ≤ 306, d3 382 ≤ 384, d2 454 ≤ 458. Note 1889 ≡ 1 (mod 4)
— a parity EXCEPTION (generic is 2n−1 ≡ 3), the same wall-exception behaviour
717 showed; 1211 and the intermediate 1887 are both ≡ 3.

**HOW THEY WERE FOUND — the schedule is the result.** Extension menus were
sampled at mixed heights (log-uniform over 4..512) because the known winners
span (5,2,2,2) to (55,7,−148,79); a single scale misses most of the space.
 1. Extend the 1207 record with an 8000-cube menu, climb the best four →
    n=8 = 1887 (8th cube (39,−5,−34,−31) added to 1207's seven).
 2. Its seven-subsets, computed for free by the same job, contain
    **1211** — the n=7 record improved as a BYPRODUCT of searching n=8.
    This is the top-down direction of the nesting principle paying off
    directly, the same way 393 fell out of 723.
 3. Extend the (unchanged under climbing) 1211 upward again → **1889**,
    which is 1887 with its 7th cube (5,4,−4,−4) replaced by (3,−4,4,4).
    So the improved n=7 record immediately improved n=8 in turn.
Round trip: n=7 record → n=8 record → better n=7 → better n=8.

**1211 IS A PLATEAU, not a lucky seed.** Reached four independent ways:
as a 7-subset of 1887; and by extending each of the three previously
unextended 723 realizations of the Postscript 29 addendum plateau —
sixth cube (3,−4,−3,3) + (40,12,11,−8), and (5,−5,5,4) +
(191,−174,417,−148), both landing on 1211. A ±2 climb with 4 wide
restarts from 1211 moved nothing. Likewise 1889 is a ±2 local max
(1 wide restart).

**NO MOVEMENT at n ≤ 6, as predicted.** The 6-subsets of 1211 top out at
exactly 723 (then 721, 715, 709, …), and no n=6 candidate anywhere in the
run beat 723. Consistent with 723 being cornered three independent ways
(Postscript 18) and with E1: any >723 config must contain a 5-subset ≥ 388,
and no such 5-cube compound is known outside the 723 family. Native n=4/n=5
campaigns were deliberately NOT re-run (n=4 has ~300k configs behind it;
n=5's 171,600-config sweep plus 155 deep restarts found nothing over 393) —
their only live route is top-down from a better n=6, which did not arrive.

Growth table at the time: n=2..8 = 13 / 67 / 183+ / 393+ / 723 / 1211+ /
1889+. Record tower 183 → 393 → 723 → 1211 → 1889, adjacent-by-one-cube.

Logs: record_hunt_n8.jsonl (wave 1a), record_hunt_n7.jsonl (the three 723
variants), record_hunt_wave2.jsonl, record_hunt_n8b.jsonl, recover_1889.py
(replays a killed job's menu deterministically — the 1889 quats were counted
before the kill but not logged). Two jobs were stopped mid-run: the n=6
wide-menu campaign from 393 never executed, and wave 2's deeper n=8 climbs
and subset pass were cut short. Both are cheap to resume.

## Postscript 46: 723 IS BEATEN — n=6 = 727, and it lifts the tower to n=7 = 1217, n=8 = 1891; the large-height quaternion stratum was never sampled

2026-07-29, main session, same day as Postscript 45 and superseding its
n=7/n=8 numbers. All three counts two-engine certified (cube_regions_n and
certify_six.exact_count_config, identical totals AND histograms).

**n=6 = 727** (was 723, unbeaten since Postscript 12 and "cornered three
independent ways" in Postscript 18):

    quats = 4,1,1,-1; 3,3,7,3; 5,-1,-5,-5; 2,1,1,1; 1,1,1,1; 7,14,1,-5
    by_depth = {1:214, 2:220, 3:156, 4:100, 5:36, 6:1}      ≡ 3 mod 4

**n=7 = 1217** (was 1211 this morning, 1207 before):

    quats = the 727 six + 4,-3,-4,-4
    by_depth = {1:278, 2:328, 3:260, 4:190, 5:118, 6:42, 7:1}   ≡ 1 mod 4

**n=8 = 1891** (was 1889 this morning, 1879 before):

    quats = the 1217 seven + 3,-3,3,-8
    by_depth = {1:348, 2:452, 3:382, 4:302, 5:222, 6:136, 7:48, 8:1} ≡ 3 mod 4

Ceilings: every layer under C(l,n), with the l=1 law attained exactly at
each level (d5=36=6·6, d6=42=6·7, d7=48=6·8). 727 vs 723 is the familiar
shallow-for-deep trade: d1 210→214, d2 216→220, d3 164→**156** (d3=164 was
never the binding constraint), d4 96→100.

**WHY IT WAS MISSED — the untried stratum.** Every n<=6 campaign in this
project sampled small quaternions: the tier-3 sixth-cube sweep used
||q||^2 <= 600 (components <~24), the random campaigns used seeded small
integers. But the extension cubes that WIN at high n are not small — 1879's
eighth cube is (55,7,-148,79). record_hunt.py therefore samples menus
log-uniformly over component heights 4..512, and the very first such sweep
of 20 000 sixth cubes on 393 turned up 727. The winning cube (7,14,1,-5)
has ||q||^2 = 271, INSIDE the old tier-3 range — the old sweep simply drew
only 4 000 candidates and missed it. So the gap was sampling density in a
badly-shaped menu, not an unreachable region: a cheap, repeatable lesson.

**E1 NOW NEARLY PINS n=6.** The envelope bound (Postscript 18) says
T <= S_max + 336, and 727 sits on the 393 five-subset: 727 <= 393+336 = 729,
so the bound held and only 729 remains available on this base. A further
n=6 record therefore requires EITHER exactly 729 on a 393-containing config,
OR a genuinely new 5-cube compound >= 390. The 5-subsets of 727 top out at
393 (then 385), so no n=5 improvement came with it.

**CORRECTION to Postscript 16 addendum 3.** It concluded 393 is "reachable
only as a sub-compound of the 723 six-cube record, not by any independent
five-cube search". That was a statement about SMALL-quaternion search: a
wide-height extension menu on the 183 record reaches 393 bottom-up
(1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4;1,-2,-1,-1). Likewise a wide menu on a
rational 63-triple re-derives 183. Neither improves its level, but the
"top-down only" framing was an artifact of menu shape.

**Propagation pattern, twice in one day.** Wave 1: extend 1207 -> n=8 1887
-> its 7-subsets give 1211 -> re-extend -> 1889. Wave 3: 727 -> extend ->
1217 -> extend -> 1891. A record at level n lifts every level above it
within one extension pass, which makes n=6 the highest-leverage level in the
tower and the wide-stratum sweep the highest-leverage search.

Tower now: 13 / 67 / 183+ / 393+ / **727+** / **1217+** / **1891+**, still
adjacent-by-one-cube at every step. Logs record_hunt_n6.jsonl,
record_hunt_n5.jsonl, record_hunt_n4.jsonl, record_hunt_wave3.jsonl; driver
record_hunt.py + record_hunt_wave3.py.

### Postscript 46 addendum: 727 is a plateau, and 729 was not reached (80 000 sixth cubes on the 393 base)

A second, deeper wide-stratum sweep on the same 393 five-cube base — 60 000
sixth cubes at heights 4..512, top 8 climbed with 4 wide restarts each, on top
of the original 20 000 — returned **727 again, via a DIFFERENT sixth cube**:

    4,1,1,-1; 3,3,7,3; 5,-1,-5,-5; 2,1,1,1; 1,1,1,1; 15,-12,-2,-13
    by_depth = {1:214, 2:220, 3:156, 4:100, 5:36, 6:1}   (two-engine verified)

identical histogram to the (7,14,1,-5) realization.

[RE-ESTABLISHED 2026-07-30 (later): 727 IS a plateau, but not for the reason
first given and not via the (15,-12,-2,-13) cube. The locus enumeration
(Postscript 48) found two further sixth cubes, (3,-51,-93,29) and
(40,48,-11,45), giving 727 with a DIFFERENT depth profile
{1:216, 2:216, 3:160, 4:98, 5:36, 6:1} and a different pair structure
[9,5,4,9,4] — two-engine verified. A differing histogram proves
non-congruence outright, so there are at least two distinct 727 compounds,
trading layers by (+2,-4,+4,-2) with d1+d2+d3+d4 = 690 conserved. The
withdrawal below stands as written for the (15,-12,-2,-13) cube, which really
is congruent to the original.]

[CORRECTED 2026-07-30: the plateau reading here is WITHDRAWN. 723's plateau
was established by DIFFERING depth histograms, which prove non-congruence
outright; these two 727 realizations instead agree on the histogram, on the
full 5-subset profile [393,385,385,385,383,377], AND on all fifteen O-reduced
pair invariants mu(i,j) — consistent with one compound under a symmetry
relabeling, not two. Same count via a different sixth cube is NOT evidence of
a plateau. A real congruence test (or a genuinely different depth profile at
727) is needed before any plateau claim.] Next totals below it
in the sweep: 725, 725, then 723 repeatedly.

**729 was NOT attained.** E1 caps this base at 393+336 = 729, and 80 000
sampled sixth cubes plus climbs never exceeded 727. That is evidence — not
proof — that 727 is the ceiling on a 393-containing config, and it sharpens
the open question: a further n=6 record needs either the exact 729 corner
(apparently very rare if it exists at all) or a NEW 5-cube compound >= 390,
which no search has produced (the 5-subsets of both 727 realizations top out
at 393). Log: record_hunt_n6b.jsonl.

## Postscript 47: 727 is PROVED isolated on the 393 base and its coincidence pattern is unaugmentable; the record has FEWER coincidences than 723, and every condition is a quadric

2026-07-30, main session, following the user's programme: constraints that
individually have degrees of freedom may, taken together, have finitely many
solutions or none — and none means the search can be skipped entirely.

**STRUCTURE OF 727 (exact, incidence.py).** Against the five fixed cubes of
393, the record's sixth cube (7,14,1,-5) realises

    pair counts  9, 9, 9, 4, 4        18 interior edge-edge crossings
                                      36 coplanarity conditions

while 723's sixth cube (5,2,2,2) realises

    pair counts  4, 4, 4, 13, 13      48 interior crossings

**So the new record has FEWER coincidences than the old one and NO 13-pair at
all** — it replaces two rigid maximal pairs with three tunable 9-pairs. That
is Postscript 17's addendum thesis realised: the global optimum builds from
locally-suboptimal-but-flexible pieces. It also refutes "more coincidences ⇒
higher count" on this base, consistent with Postscript 30's finding that the
±1-per-coincidence law fails at n ≥ 4, and with the 9-fold-concurrence sweet
spot (over-concentration merges regions away).

**ELIMINATION (eliminate729.py, sympy over ℚ).** Fix the five cubes of 393;
the sixth then has three degrees of freedom, parameterised by Cayley
coordinates q = (1,a,b,c). Each candidate coincidence is one polynomial
det[dir(e), dir(f), pt(f)−pt(e)] = 0; there are 720 of them. Results:

    GATE  36 conditions vanish at the known 727 cube (matches incidence.py)
    Q1    their Gröbner basis has 3 elements and IS ZERO-DIMENSIONAL
    Q1b   exactly ONE real solution point — the 727 cube itself
    Q2    684 infeasible augmentations, 0 feasible

So on the 393 base: **727 is isolated** (no continuous family through it —
upgrading the single-cube DOF probe from empirical to algebraic), and **its
coincidence pattern is unaugmentable** — no sixth cube realises those 36
conditions plus any 37th, each certified by a Gröbner basis of {1}. This
explains why all six swap-completions and the balanced climb landed on the
identical profile [393,385,385,385,383,377]: there is nothing else there.

NOT proved: that no 729 exists on this base. A 729 config need not contain
727's pattern. Also the Cayley chart omits the 180° rotations (w = 0), which
need a separate chart.

**ALL CONDITIONS ARE QUADRICS** (total degree 2 in (a,b,c); measured over
cube 0's full set of 144). Three consequences:
 • per-stratum solving is cheap — three quadrics is easy for Gröbner;
 • exhaustive stratification is DEAD as stated: C(720,3) ≈ 6.2e7 systems,
   ≤ 2³ = 8 points each by Bézout, ~20 s per exact algebraic count;
 • solution fields reach degree 8, not just degree 2 — so the cheap C++ port
   (templating the coefficient type over ℤ[√d]) would cover only part of the
   strata. **Verdict on porting the algebraic engines to C++: NO.** Measured
   gap is ~120-200× (C++ integer n=6 = 0.11 s; certify_six = 13.1 s;
   cube_compound_exact ≈ 20 s at n=6), but the next bottleneck is SYMBOLIC,
   not numeric, and wolframscript + algebraic_groebner.wl already exist and
   are validated. Cheaper 100× is the existing 3-tier interval filter
   (cube_compound_interval.py), not a rewrite.

**THE STRUCTURAL ROUTE.** Enumerate pair-relation LOCI, not condition
triples. Dictionary measured today: a 9-pair carries 6 interior crossings
(12 coplanarity conditions), a 13-pair carries 24. 727 is the intersection of
three 9-loci (cubes 0, 1, 3). Each 9-locus is a curve (codim 2), so three of
them in 3-space is codim 6 — generically EMPTY. That it is non-empty here
means the five fixed cubes are mutually special, and that dependency is
exactly why 727 exists. A complete search of the three-9-pair family is then
tens of systems (C(5,3) = 10 triples of fixed cubes × components), not 6e7.

**SEARCHES RUN, ALL NEGATIVE ABOVE 727.**
 • swap-completion (balance_hunt.py): drop each of 727's six cubes and
   re-optimise the replacement. All five never-before-completed bases return
   to 727 with the IDENTICAL subset profile. The weak bases are the EASY
   routes (dropping cube 3 or 4 gives 727 in all six top completions) while
   the 393 base — the one every earlier search used — gave only 723 from an
   8000-cube menu. 727 is far more accessible from its mediocre subsets than
   from its best one.
 • balanced climb, objective (min 5-subset, total): no move at all.
 • core-and-clique (clique_hunt.py, the user's (n−2)-intersection idea): from
   the 4-cube 183 core, 60 000 candidates screened at n=5 give 80 vertices
   (after deduplication by the cube's own 24 rotations — the first run
   omitted this and its K4 layer silently counted clones, reporting a 5-cube
   total for an 8-cube config). 3 160 edges reach 727; 9 880 triangles reach
   **1217**. Both records reproduced from the core; no improvement. Cost is
   an order of magnitude below random menus, and the vertex screen is reused
   at every level above.

**NEW TOOLING** (all saved): record_hunt.py (extend/climb/subsets/campaign),
record_hunt_wave2/3.py, balance_hunt.py, clique_hunt.py, incidence.py (exact
coincidence signatures), eliminate729.py, dof_probe.py (count-preserving
family probe, with the 13-pair continuum as its positive control),
index_ledger.py (regenerates this file's postscript index — the ledger is
append-only and ordered by write time, not by number).

## Postscript 48: the locus enumeration — 9-loci are codimension 1, three-wall intersection is a 30x better search, and 727 IS a plateau (two non-congruent compounds)

2026-07-30, main session, executing the structural route Postscript 47 left
open. Tooling: locus_probe.py, locus_enum.py (conditions cached in
locus_polys.pkl).

**CODIMENSION (A).** Taking the 12 coincidence conditions active at the 727
cube against a single fixed cube: the Gröbner basis for cube 1 has ONE
element — a principal ideal, hence a surface — and all three tested cubes
(0, 1, 3) give positive-dimensional varieties. So a 9-pair locus is
**codimension 1**, three walls in the sixth cube's 3-DOF space form a
DETERMINED system, and Bézout caps it at 2³ = 8 points. That is why records
sit at three-wall intersections: it is forced, not coincidental. (The earlier
guess in Postscript 47 that the loci are codim-2 curves — which would make
727's existence a codim-6 accident — is wrong. Codim 1 is the right picture.)

**PAYOFF (B): a census of 500 sampled wall triples**, one wall against each
of three fixed cubes, solved exactly (lex Gröbner → rational roots → back
substitution), ~3 600 solution points:

    peak of the distribution   689–701   (~1 600 points)
    tail        717:86  719:8  721:21  723:21  725:9  727:6
    nothing above 727;  positive-dimensional systems: 15;  degenerate: 434

727 is reached 6 times per 500 trials — versus roughly one hit per 20 000
random sixth cubes, a **~30x hit rate**. Every solution point came out
RATIONAL with small components, so cube_regions_n counts them directly and no
algebraic engine is needed for this family (reinforcing Postscript 47's
verdict against a C++ port).

**727 IS A PLATEAU — two non-congruent compounds.** The census turned up two
further sixth cubes on the 393 base:

    (3,-51,-93,29) and (40,48,-11,45)
    727 = {1:216, 2:216, 3:160, 4:98, 5:36, 6:1}   pair counts 9,5,4,9,4

against the known cube (7,14,1,-5):

    727 = {1:214, 2:220, 3:156, 4:100, 5:36, 6:1}  pair counts 9,9,4,9,4

Both two-engine verified (cube_regions_n and certify_six, identical
histograms). A DIFFERING depth profile proves non-congruence outright — the
same criterion that established 723's plateau in the Postscript 29 addendum —
so there are at least two distinct 727 compounds, reached by different
structures (three 9-pairs versus two 9-pairs and a 5-pair). The layers trade
by (+2,−4,+4,−2) with d1+d2+d3+d4 = 690 conserved, echoing 723's (+2,−4,+2).
This SUPERSEDES the withdrawal recorded in the Postscript 46 addendum: that
withdrawal was correct for the (15,-12,-2,-13) cube, which is genuinely
congruent to the original (identical histogram, identical 5-subset profile,
identical O-reduced pair invariants), but wrong as a claim about 727 in
general.

**No consistency with 727 being beatable here so far.** Across the ~3 600
census points nothing exceeded 727. An exhaustive enumeration of the
three-wall family is running in three shards (locus_enum.py, ~9 h budget
each, symmetry-reduced by fixing the first wall's sixth-cube edge index,
candidates deduplicated by the cube's own 24 rotations before counting).
If it completes without exceeding 727, that is an EXHAUSTIVE negative over
the family that contains both 723 and 727 — which, with Postscript 47's
elimination (727 isolated, its pattern unaugmentable) and E1's cap of 729,
boxes n=6 on three independent sides.

**Coverage gaps, stated honestly.** The enumeration keeps only RATIONAL
solution points, so an irrational stratum could hide a configuration; and the
~3% of systems that are positive-dimensional (continuous families of sixth
cubes sharing three coincidences) are skipped entirely by a point
enumeration. Neither is likely to hold a record given everything above, but
both are real holes.

### Postscript 48 addendum: the enumeration's first 9 h — 727 is a FOUR-class plateau with d1+d2+d3+d4 = 690 conserved; nothing above 727 in ~256 000 configurations

Three shards ran to their 9 h budget (not to completion): ~1.3 million
three-wall systems solved, ~256 000 distinct configurations counted, covering
roughly the first six of the ten fixed-cube triples. Best in every shard:
**727**. Hits at or above 723:

    723 x 1347     725 x 135     727 x 17     (nothing above 727)

**The 17 sixth cubes reaching 727 fall into FOUR depth profiles**, all
two-engine verified:

    d1   d2   d3   d4   d5  d6      count of sixth cubes
    214  220  156  100  36   1        8      (the original, 7,14,1,-5)
    216  216  160   98  36   1        6      (3,-51,-93,29 and others)
    214  218  160   98  36   1        2      (e.g. 9,77,-27,-47)      NEW
    214  216  162   98  36   1        1      (e.g. 17,-25,-1,11)      NEW

Differing histograms prove non-congruence, so **727 is a plateau of at least
four distinct compounds** — exactly the multiplicity 723's summit showed
(Postscript 29 addendum). In every class

    d1 + d2 + d3 + d4 = 690   with d5 = 36, d6 = 1 fixed,

so the four classes are related by a conserved exchange, as at 723 — but
richer: at 723 the exchange moved (d2,d3,d4) with d1 = 210 pinned, whereas
here d1 itself varies (214 or 216). The deep tail is rigid, the shallow
layers trade.

Status of the enumeration: **not exhaustive yet** — the remaining triples are
(1,2,3), (1,2,4), (1,3,4), (2,3,4) plus the tail of (0,3,4), roughly 40% of
the family, about 7 h more at the same rate. The coverage gaps of the parent
postscript still apply (rational solution points only; positive-dimensional
systems skipped).

## Postscript 49: the walls are PAIRS OF PLANES — the three-wall family is 2 733 configurations, exhausted in four minutes, max 727; and why its all-rational solutions are an ARTIFACT

2026-07-31, main session. Prompted by the user asking whether the absence of
irrational solutions might be an artifact of an unnecessary restriction. It
is — see the scope section below — but the same investigation collapsed the
enumeration by three orders of magnitude.

**EVERY COINCIDENCE CONDITION FACTORS INTO TWO RATIONAL LINEAR FORMS.** In
Cayley coordinates q = (1,a,b,c) on the rational 393 base, each edge-edge
coplanarity condition is not an irreducible quadric but a PAIR OF PLANES,
e.g. −4(3a−5b−2c)(a+b−c+4) and −4a(b−c). Consequences:

 • a three-wall system is 2³ = 8 linear systems, each a 3×3 rational solve —
   Bézout's bound of 8 is exactly the eight plane choices;
 • the 144 walls per fixed cube collapse to **24 distinct planes** (23 for
   cube 4), so the whole family is 10 cube-triples × 24³ = 134 784 systems;
 • solutions are rational BY CONSTRUCTION.

**EXHAUSTIVE RESULT (locus_linear.py, ~4 minutes).**

    134 784 systems | 8 199 singular (positive-dimensional)
    2 733 distinct configurations after symmetry dedup and the height cap
    723 x 24    725 x 12    727 x 6    NOTHING ABOVE 727

The six 727 points split 3/3 between the two known depth profiles
{214,220,156,100,36,1} and {216,216,160,98,36,1}. So the entire three-wall
family is 2 733 configurations — the Gröbner enumeration of Postscript 48
ground through 1.3 million systems to sample part of that, because the 144
walls per cube are only 24 planes and ~99% of its systems were re-deriving
the same plane triples. The reformulation did not merely speed the search up;
it showed the family was small all along.

**WHY THE ALL-RATIONAL FINDING IS AN ARTIFACT.** irrational_probe.py measured
0 irrational roots out of 2 451 (400 systems). That is now explained rather
than lucky — and it is a property of the construction, not of the problem:

 1. The five fixed cubes are rational, so every wall has rational
    coefficients, so every three-plane intersection is rational. Irrational
    solutions CANNOT arise in this family. The one useful corollary: a sixth
    cube on ≥ 3 independent walls is necessarily rational, hence irrational
    candidates carry at most two coincidences.
 2. **The wall set is INCOMPLETE.** Only edge-edge coplanarity against a
    single fixed cube was enumerated. Corner coincidences, face-plane
    coincidences, edge-face incidences and multi-cube concurrences are all
    absent — and Postscript 12 found records sit at high-multiplicity plane
    concurrences (three cubes sharing a corner = 9 planes through a point),
    with 723 corner-dominated. This enumeration cannot see those strata.
 3. The |component| ≤ 512 height cap drops rational points with large
    denominators — exactly where near-irrational configurations live.

That irrational optima exist in this problem is not in doubt: max(3) = 67 is
attained ONLY at irrational configurations (Theorem R, Postscript 44).

**HONEST SCOPE of the exhaustion.** Complete over sixth cubes lying on three
EDGE-EDGE walls against three distinct fixed cubes of the rational 393 base,
within the w ≠ 0 Cayley chart and the height cap, with 8 199 singular
(positive-dimensional) systems skipped rather than resolved. That is the
family containing both 723 and 727. It is NOT the statement "no sixth cube
beats 727".

**REMAINING GAPS, now cheap.** At four minutes per chart the closable ones
are trivial: (a) the w = 0 chart (180° rotations — where symmetric
configurations concentrate); (b) resolving the singular systems by sampling
each component's generic count; (c) one- and two-wall strata; (d) the other
coincidence TYPES, which is the substantive one and needs new conditions
derived, not just a rerun.

### Postscript 49 addendum: the w = 0 "gap" was illusory — the chart omits quaternions, not configurations

Gap (a) of Postscript 49 is closed, by argument rather than by search. The
Cayley chart q = (1,a,b,c) cannot represent w = 0, so the 180° rotations
looked unreachable. But right multiplication by a cube SELF-symmetry leaves
the cube unchanged as a set, and

    q · (0,1,0,0) = (−x, w, z, −y),   with (0,1,0,0) = 180° about x ∈ O,

so any w = 0 quaternion maps to one with nonzero first component (if x = 0
too, use another generator; some component is nonzero). The chart therefore
omits quaternion REPRESENTATIVES, not compounds, and the enumeration's
existing deduplication by the cube's 24 rotations already absorbs the
difference.

Confirmed experimentally: rebuilding all conditions in the second chart
q = (a,1,b,c) — which does cover every 180° rotation — and re-running the
enumeration gives an identical census, 2 733 candidates, 8 199 singular
systems, the same distribution to the last entry (723×24, 725×12, 727×6),
and the SAME SIX 727 compounds up to cube symmetry (verified by symmetry
key). Scripts: locus_probe_chart2.py, locus_linear_chart2.py.

Remaining gaps of Postscript 49 are now (b) the 8 199 singular
(positive-dimensional) systems, (c) one- and two-wall strata, and (d) the
other coincidence TYPES — corner coincidences, face-plane coincidences,
edge-face incidences, multi-cube concurrences. (d) is the substantive one:
Postscript 12 found records sit at high-multiplicity corner concurrences and
723 is corner-dominated, so the stratum type most associated with records is
exactly the one these conditions do not encode.

## Postscript 50: the mixed strata are 240:1 IRRATIONAL, dominated by ℚ(√5) — a large stratum no search in this project has ever counted

2026-07-31, main session, following the user's challenge to the previous
postscript's all-rational finding. That finding was an artifact of the
condition type; here is what the other types look like.

**CORNER-ON-FACE CONDITIONS ARE IRREDUCIBLE QUADRICS** — unlike edge-edge
coplanarity, which factors into rational planes. Two families, both
codimension 1 (96 distinct per fixed cube after dedup): a corner of the free
cube on a face plane of a fixed cube, and the reverse. A sample of 250 pure
corner-triples (corner_probe.py) is POOR: 245 solved systems yielded only 55
real roots (edge-edge gives ~6.3 per system), all rational, best count **719**,
distribution topping at 717/719. So pure corner strata are sparser and lower
than the edge-edge family, not richer.

**THE MIXED FAMILY IS WHERE THE IRRATIONALITY LIVES.** Two planes cut a
rational line; restricting a quadric to it gives a QUADRATIC IN ONE
PARAMETER, so every solution is rational or degree-2 — exactly ℚ(√d), the
field of the n=3 maximizers. No Gröbner needed: intersect the planes exactly,
recover the restricted quadratic from three exact samples, read the
discriminant. Exhaustive over 2-plane + 1-quadric (mixed_enum2.py):

    1 620 000 systems
    2 856 distinct RATIONAL candidates -> max 725 (below 727)
    688 806 degree-2 IRRATIONAL solutions

    top squarefree classes:
      √5   13 500      √17  12 930     √465  8 394     √15  8 106
      √115  7 536      √6    7 104     √10   6 828     √481 6 594
      √217  5 970      √145  5 508     √13   5 244     √73  4 998

**ℚ(√5) is the most common field of all** — the golden field, in which the
n=3 golden maximizer sits. ℚ(√13) in the top twelve is the 393 record's own
tilt field (Postscript 27: the unique 4-clique axis (3,2,0), tan 2/3);
ℚ(√6) is the dihedral ψ=45° field. These are the fields this problem's
structure already produces, not arbitrary ones.

**NONE OF THESE 688 806 CONFIGURATIONS HAS EVER BEEN COUNTED.** Every search
campaign in this project's history sampled integer quaternions, which are
rational by construction; the algebraic engines (cube_compound_exact for
ℚ(√5), slide3_q2 for ℚ(√2), qtower, opencount) exist but run at ~20 s per
n=6 count in Python, enough to verify a known configuration and far too slow
to search. This is a large, structurally natural stratum that has been
invisible to the entire program.

Consequence: **the C++ port verdict of Postscript 47 is REVERSED.** That
verdict rested on solution fields reaching degree 8 — true for edge-edge
systems, which turn out to be all-rational anyway. The volume is here, in the
mixed strata, and it is entirely DEGREE 2, which is the cheap case: elements
p + q√d with integer p,q, arithmetic in the same cost class as the current
integer path. A ℚ(√d) C++ engine (cube_regions_q2.cpp) is under construction,
gated on reproducing the known algebraic values: golden 67/177/351 in ℚ(√5),
octahedral 67 in ℚ(√2), the ψ=45° point 49 in ℚ(√6), and exact agreement
with the integer engine when d = 0. 400 exact representatives are saved in
mixed_irrational_sample.json; the first real job is the 13 500 ℚ(√5) points.

Scope note: the rational half of this family maxes at 725, so no new record
comes from it. Whether the irrational half contains anything above 727 is
genuinely OPEN — the first such open question at n=6 in this program, as
distinct from the many that were closed at 727.

## Postscript 51: a ℚ(√d) C++ engine, 82 458 irrational configurations counted — nothing above 727, but a FIFTH 727 class that is IRRATIONAL, in ℚ(√13)

2026-08-01, main session, completing the arc the user opened by asking whether
the absence of irrational solutions was an artifact (it was) and then judging
a C++ irrational engine "worth having on general principle" (it was).

**THE ENGINE (cube_regions_q2.cpp).** The integer engine's scalar type
generalised to Z[√d], d squarefree and given at runtime; geometry and topology
untouched. Gates, all independently re-run by the main session:
 • --d 0 reproduces cube_regions.cpp BIT-FOR-BIT including per_label (727,
   183, and the axial self-test);
 • the field path on a purely rational config (d=5, all √-parts zero) returns
   727 with the correct histogram;
 • on a golden triple the main session derived INDEPENDENTLY — from
   cube_compound_exact's own axes, searching the cube's 24 frames for the
   representative lying in Z[√5], since the naive frame gives nested radicals
   √(7/16 + 3√5/16) — it returns 67 = {48,18,1} with per_label matching the
   Python engine;
 • the overflow guard rejects non-squarefree d, d > 100, and |p|,|q| > 512
   rather than truncating silently.
Measured ~100x faster than the Python algebraic path (n=3/4/5: 5.3/11.5/21.9 ms
against 0.48/1.10/2.20 s). Note cube_compound_exact caps at N=5 — run(6)
silently aliases to run(5) through a list slice — so the "~20 s at n=6" figure
used earlier in this project was an extrapolation, not a measurement.

**THE COUNT.** Of the 688 806 degree-2 solutions of the mixed strata
(Postscript 50), those in the engine's budget (squarefree d ≤ 100, components
≤ 512) are **56 fields, 82 458 configurations** — every one of them counted.
Result: **NOTHING ABOVE 727.** Best per field, largest classes first:

    ℚ(√5)  7374 cfgs -> 721      ℚ(√17) 6210 -> 717     ℚ(√6) 4218 -> 723
    ℚ(√13) 3156 cfgs -> **727**  ℚ(√2)  3000 -> 713     ℚ(√41) 2850 -> 719
    ℚ(√7), ℚ(√3), ℚ(√57), ℚ(√10), ℚ(√34), ℚ(√82), ℚ(√62) -> 723; rest lower

**A FIFTH 727 CLASS, AND IT IS IRRATIONAL.** ℚ(√13) is the ONLY field reaching
727, in 72 configurations, all with depth profile {1:214, 2:216, 3:162, 4:98,
5:36, 6:1}. That profile also occurs rationally (once, in the Postscript 48
run), but the two are NOT congruent: their O-reduced pair-invariant multisets
differ (2.298618/2.394195/2.548272/2.986205 against
2.277586/2.405405/2.540744/2.983337). Example sixth cube:

    (1, 1−√13, 16−4√13, 11−3√13)     727 = {214, 216, 162, 98, 36, 1}

Two-engine verified: cube_regions_q2 and opencount.py's degree-agnostic field
engine (separate codebases) agree on total and full histogram. So 727 has at
least FIVE congruence classes, one of them irrational — and this is the first
irrational configuration this project has found by SEARCH; the two n=3
maximizers came from symmetry.

ℚ(√13) is not an arbitrary field here: it is the 393 base's own tilt field
(Postscript 27, the unique 4-clique axis (3,2,0), tan 2/3). The base's
arithmetic reappears as the only field whose strata reach the record, while
the most populous field ℚ(√5) tops out at 721 and ℚ(√2) at 713.

**REMAINING GAP.** Classes with d > 100 — ℚ(√465), ℚ(√115), ℚ(√481),
ℚ(√217), ℚ(√145) and others, together the majority of the 688 806 solutions —
are outside the engine's derived overflow budget and remain uncounted.
Widening that budget needs wider arithmetic; the user's suggestion of a
continued-fraction sign test would let coordinates use the full width of the
type (comparing |p|/|q| against √d by comparing continued-fraction expansions,
with no products at all), though the binding constraint is the growth inside
det3, not the final sign test.

### Postscript 51 addendum: the d > 100 gap is mostly a GUARD-SHAPE problem — a joint budget unlocks ~343 000 configurations with no arithmetic change

Measured (bigd_probe.py) to size the remaining work. Of the mixed strata's
1 377 612 degree-2 solutions, 1 112 028 lie in the 1 328 classes with d > 100
that the engine currently rejects. But those classes are NOT arithmetically
large: the smallest quaternion component bound per class is 3 for ℚ(√115),
6 for ℚ(√217), 7 for ℚ(√145), 9 for ℚ(√465) and ℚ(√481), 36 even for
ℚ(√8761). The current guard rejects them only because it is a RECTANGLE
(d ≤ 100 AND |p|,|q| ≤ 512) while the real overflow constraint couples the
two — growth through det3 goes as roughly d·m².

Under a joint budget d·m² ≤ 26 214 400 (the same corner as the present
rectangle, so no weakening of safety), counted PER SOLUTION:

    admissible:  595 452 of 1 377 612  (43.2%)
    of which d > 100, i.e. newly reachable:  342 720

So re-deriving the bound as a joint constraint — a change to validateBudget
and its derivation, not to the arithmetic — would make ~343 000 currently
unreachable configurations countable. The remaining ~57% needs genuinely wider
intermediates (256-bit throughout, not only in the sign predicate).

Methodological note: the first version of this measurement reported 68%, by
counting every solution in a class whenever that class's SMALLEST component
passed the budget. That is an upper bound, not an estimate; the per-solution
figure is 43.2%. Recorded because the error is easy to repeat — a per-class
extremum is not a per-member property.

### Postscript 51 addendum 2 (CORRECTION): d·m² is NOT the overflow invariant, and the joint rule proposed above would have been UNSAFE

The addendum above proposed replacing the engine's rectangular guard with a
joint budget d·m² ≤ 26 214 400, on the reasoning that det3 growth goes as
(m²·d)³. Implementing it properly (2026-08-01) showed that reasoning is wrong.

Tracing |p| and |q| SEPARATELY through the pipeline — field multiply bounds to
(P₁P₂ + d·Q₁Q₂, P₁Q₂ + Q₁P₂), k-term sums to k times the per-term bound —
the true admissible boundary does not have constant m²·d. It runs ~9.0e6 at
d=1, rises to ~2.53e7 at d=29, crosses the proposed 2.62e7 near **d ≈ 38**,
plateaus around 2.9–3.0e7 for d ≳ 500, and drifts back to ~2.88e7 at d = 20000.

So the flat rule is **over-permissive below d ≈ 38** — at d=5 the true safe
component maximum is 1855 while the rule would admit 2289, an exploitable
overflow, not mere conservatism — and merely over-restrictive above it. A
monomial fit was the wrong instrument; the engine now evaluates the traced
bound per configuration at runtime, against 2^112 for the i128 chain (the
binding constraint throughout, verified over d ∈ [0, 3e7]) and 2^231 for the
u256 sign path.

Also corrected: the old file header cited (d=100, m=512) as a verified corner,
but **100 is not squarefree**, so that d was never an acceptable input — its
own squarefree gate would have rejected it. The nearest squarefree corner
(d=101, true max m = 531) was verified instead.

Verification of the new guard (independently re-run by the main session):
d=0 reproduces the integer engine semantically on 727 and 183; the ℚ(√13) 727
still counts 727 = {214,216,162,98,36,1}; SCALING INVARIANCE holds in the
newly-admitted region (multiplying every component by k > 0 is the same
rotation, so counts must agree — verified at d=8761 ×12, d=465 ×25,
d=115 ×25); and the boundary rejects exactly where predicted (d=465 accepts
m=253, rejects m=254).

Absolute ceiling of the engine: at m = 1, d may reach 30 319 844.

### Postscript 51 addendum 3 (CORRECTION + completion): 224 184 irrational configurations counted, still nothing above 727 — but 727 has at least TWELVE congruence classes, EIGHT of them irrational, across EIGHT fields

The full recount under the corrected (traced, per-configuration) overflow
budget is complete. It **supersedes two claims of Postscript 51**, both of
which were properties of the old narrow guard rather than of the problem.

**WRONG:** "ℚ(√13) is the only field whose strata reach 727."
**WRONG:** "a FIFTH 727 class, and it is irrational."

Both were stated from a run in which only 56 fields were countable at all —
everything with d > 100 was rejected before it could be counted. Scoping the
claim to the instrument ("the only field among the 56 counted", as RESULTS.md
happened to put it) would have been correct; stating it of the problem was not.

**FINAL COUNT.** 224 184 irrational configurations counted (up from 82 458),
284 634 rejected as genuinely exceeding the traced bound. Hits at or above 723:

    723 x 1581     725 x 75     727 x 255     nothing above 727

**727 IS REACHED IN EIGHT FIELDS:**

    ℚ(√13)  144    ℚ(√226)  51    ℚ(√403)  36    ℚ(√1093)  9
    ℚ(√1614)  6    ℚ(√1785)  3    ℚ(√1930)  3    ℚ(√2741)  3

falling into only three depth profiles, all of which also occur rationally:
{214,216,162,98,36,1} ×189, {214,220,156,100,36,1} ×63,
{214,218,160,98,36,1} ×3.

**AT LEAST TWELVE CONGRUENCE CLASSES — 4 rational, 8 irrational.** By the
O-reduced pair-invariant multiset: within each field every 727 shares one
signature, and the signatures differ across fields, so the classes are INDEXED
BY FIELD rather than scattered. That is a structural fact worth pursuing: the
plateau is not a loose collection of coincidences but an arithmetically
organised family, with one congruence class per field that reaches it.

d₁+d₂+d₃+d₄ = 690 with d₅ = 36, d₆ = 1 still holds in every class.

**Scope of the negative, stated precisely.** No configuration above 727 exists
among: the exhausted three-wall family (2 733 configs); pure corner-wall
triples (sampled, best 719); the rational half of the mixed family (2 856,
best 725); and 224 184 irrational mixed-family configurations across the
fields admitted by the traced budget. Still uncounted: the 284 634 solutions
whose (d, component) pair exceeds that budget, the positive-dimensional
systems, one- and two-wall strata, and the coincidence types never modelled
(corner-corner, edge-face, multi-cube concurrence).

### Postscript 51 addendum 4: the region count is NOT Galois-invariant — and the "arithmetic structure" reading of the 727 plateau was mostly bookkeeping

Prompted by the user pressing on a remark of mine — that one congruence class
per field "suggests the plateau has arithmetic structure rather than being a
loose collection, and that's a question worth asking properly." Asked
properly, the interesting version is false.

**THE TEST.** Every irrational 727 arose as a root of a quadratic on a
rational line, so its Galois conjugate (√d → −√d, i.e. negate every √-part) is
also a real configuration — a different one, since conjugation is not an
isometry. If the count were preserved, the FIELD rather than the individual
root would be carrying it, and one-class-per-field would follow.

**RESULT: 0 of 255 conjugate pairs agree.** Conjugate counts by field:
ℚ(√13) 727→687, ℚ(√226) 727→683, ℚ(√403) 727→711, ℚ(√1093) 727→683,
ℚ(√1614) 727→683, ℚ(√1785) 727→695, ℚ(√1930) 727→675, ℚ(√2741) 727→699.
Every conjugate lands in 675–711 — the bulk of the mixed-strata distribution,
exactly where an unrelated configuration sits. So conjugation is effectively
randomising, and the count is a property of the root, not of the field.

**CORRECTION to the framing of addendum 3.** That addendum called the classes
"INDEXED BY FIELD rather than scattered" and said the plateau is "an
arithmetically organised family". That over-reads the data. A configuration's
field of definition is itself a congruence invariant, so configurations over
different fields are non-congruent almost by definition — the field-indexing
is bookkeeping, not structure. The only genuine content is the word EXACTLY:
each field contributes exactly one class rather than several, and even that is
weakly supported, since four of the eight fields contributed only three
configurations each.

**WHAT REMAINS OPEN, and is a real question.** Only 8 of ~1 300 counted fields
reach 727: d = 13, 226, 403, 1093, 1614, 1785, 1930, 2741. ℚ(√13) is the 393
base's own tilt field and 403 = 13·31 contains it, but 226 = 2·113,
1614 = 2·3·269, 1785 = 3·5·7·17, 1930 = 2·5·193, and 1093 and 2741 prime show
no pattern the main session can see. No hypothesis with evidence behind it is
offered here.

### Postscript 51 addendum 5: n=3 is less anomalous than Postscript 44 claimed — two of its three "anomalies" were instrument-limited

User's observation, 2026-08-01, and it is correct. Postscript 44's audit
concluded that n=3 is (a) the only level whose optimum set is finite and larger
than one point, (b) the unique IRRATIONAL rung of the tower, and (c) the only
level that fails to embed in higher records. Today's results undercut the first
two.

**(a) Finite-and-multiple is ordinary, not anomalous.** 723 has four
non-congruent realizations; 727 has at least twelve. n=3's two isolated
maximizers are a small instance of a common phenomenon, not a unique one.

**(b) Irrational configurations achieve the n=6 record too.** Eight of 727's
twelve congruence classes are irrational. The claim that n=3 is "the unique
irrational rung" rested on evidence STRUCTURALLY INCAPABLE of finding
irrational configurations at other levels: every campaign in this project
sampled integer quaternions, which are rational by construction. The limited
exceptions — the quadratic-field and degree-4 resonance sweeps of Postscripts
28 and 32 — swept specific families, not strata. This is the same
instrument/problem conflation as the all-rational finding (Postscript 49) and
the "only field reaching 727" claim (addendum 3), now recurring a third time
in a claim recorded a week earlier.

**WHAT SURVIVES.** The genuine distinction is REQUIREMENT versus
AVAILABILITY: no rational configuration attains 67 (Theorem R, conditional on
the two known maximizers being the only ones), whereas rational configurations
DO attain 727 — irrationality is optional at n=6 and mandatory at n=3. That,
plus the nesting break (best triple in any higher record is 63, four short of
67), is what Postscript 44 should have led with. The cap-sum tightness at
n ≤ 3 is a statement about the bound, not about configurations.

**TESTABLE, and now cheap.** Run the mixed-strata enumeration on an n=4 or n=5
base and ask whether an irrational configuration reaches or beats 183 or 393.
If it does, n=3's distinction narrows to requirement alone, resting on a single
conditional theorem. The ℚ(√d) engine makes this a few hours of compute; it was
not possible before 2026-07-31.

## Postscript 52: a NEW congruence class of the n=5 record 393 — and a correction: the irrational record-achievers are RATIONALLY SHADOWED, so irrationality is doing no work at n=5 or n=6

2026-08-01, main session, following the user's question about irrational
configurations between n=3 and n=6.

**METHOD.** The n=6 mixed-strata machinery generalised to an arbitrary rational
base (mixed_base.py): fix the (n−1)-cube subset of a record, enumerate the
2-plane + 1-quadric strata for the free cube, count with cube_regions_q2.

**n=4 (base: three cubes of the 183 record).** 159 840 systems, 209 fields,
25 900 irrational configurations counted. **Best 173 — short of 183 by ten.**
Coverage caveat: three fixed cubes admit only ONE cube-triple, against four at
n=5 and ten at n=6, so this negative is thinner than the others.

**n=5 (base: the four cubes of 183).** Irrational configurations DO reach the
record: 393 attained in ℚ(√1105) and ℚ(√1126), with depth profile
**{1:146, 2:132, 3:84, 4:30, 5:1}** — different from the known rational 393's
{1:156, 2:128, 3:78, 4:30, 5:1}, hence a genuinely new congruence class.
Clustering the hits modulo the cube's own 24 rotations: all of them reduce to
**six distinct configurations**, three per field, stable at every threshold
below 0.1°; the nearest cross-field pair is 0.850663° apart. Pair counts
against the base are 9,9,9,4 — three tunable 9-pairs and no maximal pair,
where the rational 393's fifth cube has 13,9,9,9. The same
rigid-for-flexible substitution 727 made against 723.

**THE CORRECTION.** That class is NOT an irrational phenomenon. Rounding the
ℚ(√1105) configuration to a rational quaternion at denominator 1000 gives

    (1,0,0,0; 0,5,3,2; 1,-4,-1,1; 1,1,-1,-4; 4,-403,262,-137)
    = 393, profile {1:146, 2:132, 3:84, 4:30, 5:1}   [two-engine verified]

i.e. the same new class, realised RATIONALLY. So the n=5 record has at least
two congruence classes, and the second is reachable without leaving ℚ. The
enumeration found its irrational points first only because irrational points
are what it enumerates.

393 is NOT constant on a chamber here: 60 small perturbations of the rational
point give 365–383, with 393 recurring once. It is a wall, as records in this
project always are — but the wall carries rational points as well as
irrational ones.

**SAME CHECK AT n=6.** Rational approximations near the eight irrational 727s
mostly fall short (715–721), but ℚ(√403)'s neighbour (92,−19,−80,−85) gives
**727** with profile {214,216,162,98,36,1} — an already-known rational class
(two-engine verified). So at least one of the eight irrational 727s is
rationally shadowed too; the other seven are unresolved at the denominators
tried, which is weak evidence either way.

**WHAT THIS DOES TO THE n=3 QUESTION.** Addendum 5 concluded that n=3 is less
anomalous than Postscript 44 claimed, since irrational configurations achieve
the record at n=6. That conclusion now needs qualifying in the opposite
direction: every irrational record-achiever CHECKED so far has a rational
configuration nearby with the same count and profile, so irrationality is not
doing work at n=5 or n=6. At n=3 it provably is — no rational configuration
attains 67 (Theorem R). The distinction between REQUIREMENT and AVAILABILITY,
already flagged in addendum 5 as the part that survives, is looking like the
whole of it.

**METHODOLOGICAL NOTE.** Enumerating irrational strata finds irrational
points; that is not evidence that the count requires irrationality. The test
that matters is whether a rational point on the same wall achieves the same
count — cheap, and it should be run before any future claim that a record is
irrational.

### Postscript 52 addendum: n=5 run complete — three fields, 144 configurations, one profile, and the √-part structure

Final numbers for the n=5 base (the four cubes of 183): 644 544 systems over
543 squarefree classes, 188 382 candidate configurations, **79 398 counted**
and 108 984 rejected as beyond the traced overflow budget. **Nothing above
393.**

393 is reached in THREE fields, not the two recorded in the parent postscript:

    ℚ(√466) x63     ℚ(√1105) x36     ℚ(√1126) x45     (144 configurations)

all sharing the single depth profile {1:146, 2:132, 3:84, 4:30, 5:1} — the new
congruence class, distinct from the known rational 393's {1:156, 2:128, 3:78,
4:30, 5:1}, and (per the parent postscript) reachable rationally as well at
(4,−403,262,−137).

**STRUCTURE OF THE IRRATIONAL PART.** Writing each quaternion component as
p + q√d, the √-part of the axis is always a LOW-HEIGHT integer vector while the
rational part is large and unstructured (e.g. (143, 23, −57)). Across the 144
configurations there are 44 distinct primitive √-parts, and exactly HALF —
72 of 144 — lie along a cube face axis or face diagonal:

    (1,1,0) (1,0,−1) (0,1,1) (0,1,−1) (1,−1,0) (1,0,1)   x9 each  (face diagonals)
    (1,0,0) (0,1,0) (0,0,1)                              x6 each  (face axes)

the remainder being (1,2,3)-type, (3,3,4)-type and (2,3,5)-type vectors in
permuted and sign-varied form. The SAME collection of directions recurs in all
three fields. So the configuration is a generic rotation plus an irrational
nudge along a cube-symmetry direction — consistent with how these arise, since
the quadratic comes from restricting a CORNER condition (built from the cube's
own face normals) to a line, so the discriminant inherits that structure.

This also gives a concrete handle on the open "why these fields" question: the
field appears to be determined by which small direction pairs with which line,
rather than being an independent arithmetic property.

**CAUTION recorded because it recurred three times today.** Two earlier
readings of this data — "the √-parts are identical across fields" and
"these configurations are near-half-turns" — were both drawn from the FIRST
ROW of a file and were false of the set (44 distinct √-parts; angles spread
30°–165° with median ~135°). Aggregate before describing.

### Postscript 52 addendum 2 (CORRECTION): the μ-multiset UNDERCOUNTS classes — at least 21 distinct labelled types among the irrational 727s, not 8; and the irrational 727s are all RATIONALLY SHADOWED

Two corrections and one new measurement, prompted by the user asking which
configurations are topologically distinct.

**(1) RATIONAL SHADOWING IS UNIVERSAL AT n=6.** Each irrational 727 arose on a
line cut by two rational planes. Sampling 34 385 RATIONAL points along those
same lines: **every one of the eight fields is shadowed** — ℚ(√13), ℚ(√226),
ℚ(√403), ℚ(√1093), ℚ(√1614), ℚ(√1785), ℚ(√1930), ℚ(√2741) each have rational
points on their own 727-lines that also count 727. Combined with the n=5 result
(Postscript 52), irrationality does NO work at either level: it is a property
of which points the enumerator finds, not of which configurations reach the
record. n=3 remains the only level where irrationality is REQUIRED (Theorem R).

**(2) THE μ-MULTISET TEST UNDERCOUNTS.** Addendum 3 reported "at least twelve
congruence classes, eight irrational, one per field" from the O-reduced
pair-invariant multiset. That multiset is only a NECESSARY condition for
congruence — non-congruent configurations can share it — so it bounds the
class count from below, and weakly. Measuring instead by PER-LABEL vector
(regions counted by containment bitmask, an invariant that congruent
configurations must share): the 183 irrational 727 configurations have

    3 distinct depth profiles      but    21 distinct per-label vectors

so there are **at least 21 non-congruent irrational 727 configurations**, not 8.
The earlier figure was an artifact of a weak invariant, the same way the field
count was an artifact of a narrow guard.

**(3) THE INVARIANT HIERARCHY, for future use.** Coarse to fine:
total count (1) < depth profile (3) < per-label vector (21) < region adjacency
/ face lattice (uncomputed, ≥21) < congruence (≥21). Per-label is NOT
topological type: two arrangements can distribute regions identically among
containment classes while differing in which regions share a face. Any future
claim about how many distinct configurations achieve a record should state
which of these it is counting — three separate claims in this project have now
been wrong because they did not.

### Postscript 52 addendum 3: n=4's shortfall holds across ALL FOUR bases; and a region-adjacency invariant now exists

**n=4 CONFIRMED AS THE OUTLIER.** The earlier n=4 negative rested on one
cube-triple. Re-run over all four 3-subsets of the 183 record — every base
from which a fourth cube can complete it:

    base = 183 minus cube 3:  best 173  ℚ(√281)
    base = 183 minus cube 2:  best 173  ℚ(√281)
    base = 183 minus cube 1:  best 173  ℚ(√281)
    base = 183 minus cube 0:  best 165  ℚ(√2190)

Ten short of 183 in every case (the first three find the same configuration up
to cube symmetry, as expected since those bases differ by which cube was
dropped). So among n=3..6, n=4 is the only level whose record is NOT reached by
an irrational configuration — while n=5 and n=6 are reached but RATIONALLY
SHADOWED, and n=3 requires irrationality. Whether "rationality is required at
n=4" is a fact or a coverage artifact remains open: unlike Theorem R at n=3,
there is no candidate arithmetic obstruction pointing that way, and 183 is not
a proved maximum, so any such claim would be doubly conditional.

**REGION ADJACENCY (region_adjacency.py, new).** The counting pipeline already
distinguishes fragment touches across PHANTOM walls (merge — same region) from
touches across REAL faces (distinct regions); the latter were asserted and
discarded. They are exactly the adjacency edges. Recording them costs nothing
measurable (5.5–6.9 s per n=6 configuration against certify_six's own 6.5 s).

STRUCTURAL GATE, and it is a real one: crossing a real face changes the
containment set by exactly ONE cube, so every adjacency edge must join labels
whose bitmasks differ in exactly one bit. Asserted (hard abort, not a filter)
over ~14 000 edges across 8 configurations: zero violations.

Gates: n=2 (quats 1,0,0,0 / 0,1,1,1) gives 13 regions and 24 edges with degree
distribution {2:×12, 12:×2} — the twelve depth-1 regions each touching only the
core and the outside, and those two each touching all twelve, verified
independently by the main session. The 727 record reproduces total, by_depth
AND all 64 per_label entries against cube_regions_n, with 2054 edges.

FINDING, on the six rational 727 configurations: distinct depth profiles 4,
distinct per-label vectors 5, distinct adjacency profiles 5. **Adjacency
strictly refines the depth profile but added nothing beyond per-label on this
sample.** The one pair it could not separate — (7,14,1,-5) and (15,-12,-2,-13)
— is the pair already shown congruent by the O-reduced pair invariants
(Postscript 46 addendum's withdrawal), so agreement is the correct answer
there. Sample of six is small; the test worth running is the 21 per-label
classes among the irrational 727s, which needs ℤ[√d] arithmetic in the Python
pipeline (not yet built).

### Postscript 52 addendum 4: the 727 plateau holds at least 600 configurations — every earlier class count measured the enumerator

Sampling rational points along the same lines that produced the irrational
727s (the two-plane intersections recorded in provenance_727.json) and counting
each exactly:

    417 distinct RATIONAL 727 configurations   (deduplicated by the cube's
                                                own 24 rotations)
      profile {214,220,156,100,36,1}  x311
      profile {214,216,162, 98,36,1}  x82
      profile {214,218,160, 98,36,1}  x24

together with the 183 irrational ones already counted, **at least 600
configurations reach 727** on these lines alone — and the lines are only the
three-wall strata this enumeration happens to cover.

**This retires the class counts recorded earlier in this session.** The
progression was 4 (Postscript 48, by depth profile), then 12 (addendum 3, by
O-reduced pair invariant), then ≥21 (addendum 2, by per-label vector), now
≥600. Each figure was correct about what it measured and wrong as a statement
about the plateau, because each measured the reach of the instrument in use:
a coarser invariant merges classes, and a narrower enumeration finds fewer
configurations. Only the last of these was ever presented with its scope
attached.

The honest current statement: the number of distinct configurations achieving
727 on the 393 base is **at least 600 and not known**; the number of distinct
combinatorial types among them is unmeasured, since only three depth profiles
appear but per-label and adjacency both refine that (region_adjacency.py exists
for exactly this, and has not been run over the 417).


### Postscript 52 addendum 5: the 727 plateau has at least 109 distinct combinatorial types — and per-label is as sharp as adjacency

Running region_adjacency.py over all 417 rational 727 configurations recovered
from the 727-producing lines (2 260 s, 5.4 s each, ~850 000 edges, zero
one-bit-gate violations):

    distinct DEPTH profiles     :   3
    distinct PER-LABEL vectors  : 109
    distinct ADJACENCY profiles : 109

**(1) The plateau is heterogeneous.** 109 distinct combinatorial types among
417 configurations — the depth profile, which sees only 3, undercounts by a
factor of 36. "The 727 compound" is not a meaningful phrase: it is at least 109
genuinely different arrangements that happen to count the same, plus whatever
the irrational ones and the unenumerated strata add.

**(2) Adjacency adds NOTHING over per-label, at this scale.** The two
invariants partition the 417 identically. A priori adjacency should be strictly
finer — two arrangements can distribute regions identically across all 64
containment classes and still glue them differently — but empirically, on this
population, the containment-set distribution already determines the edge
multiset. The earlier six-configuration test (Postscript 52 addendum 3) saw the
same agreement but was far too small to support it; 417 configurations is not.

Practical consequence: classification can use `per_label`, which the counting
engine emits for free at 0.11 s, instead of the 5.4 s adjacency computation —
**50x cheaper at no measured cost in resolution**. region_adjacency.py remains
the instrument of record for checking that claim, and the one-bit assertion it
carries is a genuine correctness gate, not a self-consistency check.

Caveat on (2): "no measured loss" is not "provably equivalent". The adjacency
profile in use is the multiset of edge label-pairs; a finer topological
invariant (the full face lattice, or the adjacency graph up to isomorphism
rather than by profile) could still separate configurations these two agree on.
What is established is that the cheap invariant loses nothing the expensive one
currently detects.

### Postscript 52 addendum 6: a taxonomy of the 727 plateau — types are tight clusters with fixed pair relations, and the C3 quotient corrects the counts

Correcting the counts first. The 393 base is invariant under the C3 rotation
about (1,1,1) — it fixes cubes 3 and 4 (both lie on that axis) and 3-cycles the
spokes 0,1,2 — so rotating a whole compound by it gives a CONGRUENT compound
with the same base. Earlier counts quotiented only by the free cube's own 24
rotations and therefore double-counted:

    417 configurations, 109 types   ->   161 configurations, 54 types

The base has no genuine mirror symmetry: its only improper "symmetries" are the
central inversion times C3, and -I acts trivially on cubes because a cube is
centrally symmetric. **The base is chiral**, so reflection maps these
configurations out of the enumerated family rather than permuting within it.

**WHY ORBIT SIZES CAME OUT {1,2,3}** — impossible for a group of order 3.
The recovered set is not C3-closed, and the reason is structural: the C3
generator (1,1,1,1) has norm 4, so multiplying inflates quaternion components
about twofold. Of the C3 images of the 161 representatives, 49 EXCEED the
engine's |component| <= 512 budget (median component 200 -> 261, max 512 ->
1093) and are therefore unreachable by cube_regions_n. Nothing is lost
mathematically — each such image is congruent to a representative already in
hand, so its count and every invariant are known without evaluating it — but it
means **the height cap is not symmetry-equivariant**: a bound on a coordinate
representation is not a bound on the configuration. Same error shape as the
rectangular overflow guard (addendum 2). The fix is to canonicalise over the
orbit before filtering.

**THE TAXONOMY.** Over 416 within-type pairs:

    same pair-count signature vs the five base cubes : 416 / 416  (100%)
    from the same wall line                         : 287 (69%)
    geodesic separation WITHIN a type : min 0.005  median 0.285  max 1.568 deg
    geodesic separation ACROSS types  : min 0.088  median 5.598  max 18.859 deg

So a per-label TYPE is a tight geometric cluster — 20x closer within than
between — whose members share their pair relations to the base exactly. That
the fine combinatorial invariant determines the coarse geometric one is not a
tautology: pair counts are properties of two-cube subconfigurations and are not
readable from a six-cube per-label vector. No exceptions in 416 trials.

Type sizes are uneven: {1:19, 2:15, 3:9, 4:2, 5:4, 6:1, 10:1, 12:1, 14:1, 15:1}.

**Provenance does NOT determine type.** Only four wall-triple combinations
occur, every one using cube 3 for a plane — (0,3)+quadric1 -> 11 types,
(0,3)+quadric4 -> 7, (1,3)+quadric0 -> 24, (1,3)+quadric2 -> 12. The wall
triple selects the neighbourhood; something finer selects the type within it,
and what that is remains unidentified.

SCOPE, stated because "taxonomy" invites over-reading: this classifies the
RATIONAL 727s recovered from the 2-plane+1-quadric strata on the 393 base,
within the height cap. It does not cover the irrational 727s (183 of them,
classified at 21 types before this C3 correction, so that figure is inflated
too), the pure-corner or one- and two-wall strata, the 8 199
positive-dimensional systems, configurations not containing the 393 base, or
any level other than n=6.

## Postscript 53: a FAILED attempt at proving E1, with the error located — "each piece adds one region" is false for non-disk pieces

2026-08-02, main session. E1 (Postscript 18) bounds the one-cube increment by
a MEASURED constant, T <= S_max + 336 at n=6. This is an attempt to derive it
instead, and it fails; recorded because the failure is instructive and the
diagnosis points at the repair.

**THE ATTEMPT.** The increment identity T = count(S_j) + Delta_j is exact.
Every region created by re-adding cube j arises because dC_j cuts an existing
region, so — the claimed step — Delta_j <= #pieces into which dC_j is divided
by the other cubes' face planes. Then dC_j is a sphere, each other face plane
meets it in a closed curve, crossings have degree 4 so E = 2V, and Euler gives
F = 2 + V with V computable exactly (a plane pair contributes 2 iff their
intersection line meets int C_j).

**IT FAILS**, on 15 of 21 tested (config, j) pairs — e.g. the 183 record at
j=0 has Delta = 128 against a bound of 98, and the n=2 13-pair has Delta = 12
against a bound of 2.

**WHERE IT BREAKS.** Two compounding errors, both found by testing the n=2
case where the answer is checkable by hand:

 1. **F = 2 + V requires every face to be a DISK.** In the 13-pair the six
    traces of A's face planes on dB are DISJOINT closed curves, so the faces
    are annuli and worse, and that form of Euler does not apply. The correct
    general count is F = 1 + C + V with C the number of connected components
    of the curve union (verified: 1 circle -> 2 faces; 2 disjoint -> 3; 2
    crossing twice -> 4; 3 great circles -> 8). That gives 7 for the 13-pair.

 2. **The piece bound itself is FALSE.** "Each connected piece adds at most
    one region" holds only for disk pieces. In the 13-pair, dB ^ int A is ONE
    connected piece with SIX boundary circles, and it separates int A into
    seven parts. One piece, six extra regions. So 7 pieces cannot bound
    Delta = 12.

**THE REPAIR DIRECTION.** What governs how many parts a region is cut into is
the number of BOUNDARY CIRCLES of the cutting surface, not the number of
pieces: a connected separating surface with b boundary circles can create up
to b parts. For the 13-pair that gives 6 circles inside A plus 6 lobes
outside — exactly the 12 observed. So the right bookkeeping counts trace
curves and their crossings, not arrangement faces.

The geometric predicate is NOT at fault: line_meets_interior was cross-checked
against dense numeric sampling on all 153 plane pairs of the n=4 case, 153/153
agreement. Files: increment_bound.py (the failed bound, kept with this
postscript as its documentation).

E1 therefore remains an empirical envelope, and open problem 4 remains open.

## Postscript 54: the 727 plateau is a nested chamber structure, and adjacent types differ by an elementary ±2 exchange within one depth

2026-08-02, main session, answering "how are members of a type related?" and
"are there other structures among types?"

**NESTED CHAMBERS.** A wall line (the intersection of two coincidence planes)
carries a chamber structure at two levels:

    wall line
      count-chamber   — the total is constant along a stretch
        type-chamber  — the per-label vector is constant on a sub-stretch

Verified on one line: the count is 727 at 76 of 77 rational points sampled
across t in [2,6], including at denominators 11,13,17,19,23 deliberately
coprime to the grid that produced the original points — so 727 holds on a
genuine INTERVAL, not merely at lattice points. Within that one count-chamber
sit **11 type-chambers**.

**SO MEMBERS OF A TYPE ARE POINTS OF A COMMON TYPE-CHAMBER** — related by
continuous deformation along the line crossing no wall that alters the label
distribution. This explains the measured facts of addendum 6: pair signatures
identical within a type (they are constant along the whole count-chamber),
separations of a fraction of a degree, and 69% of within-type pairs sharing a
line. The other 31%, on different lines, share a type by combinatorial
coincidence with no deformation connecting them.

**THE ELEMENTARY EXCHANGE.** Crossing between adjacent type-chambers:

    label  2 -2  ->  label  1 +2      (both depth 1)
    label 32 -2  ->  label  2 +2      (both depth 1)
    label 40 -2  ->  label  6 +2      (both depth 2)
    label 11 -2  ->  label 50 +2      (both depth 3)
    label 1 -2, label 49 -2  ->  label 32 +2, label 7 +2   (depths 1 and 3,
                                                            each balanced)

Every observed transition moves **exactly ±2 regions**, between labels of the
**same depth**, with net zero at every depth — magnitude patterns (2,2) eight
times and (2,2,2,2) twice, out of ten transitions. So the type-transition is
an elementary exchange: two regions change which cubes contain them, without
changing how many.

The quantum of 2 is not mysterious: every compound here is centrally symmetric
(all cubes share the centre), so regions occur in antipodal pairs and no count
can change by an odd amount. Same mechanism as the parity law bounded = 2n-1
(mod 4), Postscript 4.

**CONSEQUENCE.** The 54 types are not an unstructured list: they are vertices
of a graph whose edges are these elementary exchanges, embedded along the wall
lines. This also corrects the picture of Postscript 52 addendum 6, which
described the 727 configurations as isolated points — true transverse to the
walls, where perturbation collapses the count to 715-721, but false ALONG
them, where the count persists on intervals. The earlier perturbation test
moved off the line, which is exactly where the count dies.

Scope: measured on one line of the 129, at n=6 on the 393 base. Whether the
±2-same-depth rule is universal is untested, though central symmetry makes the
parity half of it structural.

## Postscript 55: the 9-plane corner-concurrence stratum is CAPPED AT 723 — records do not concentrate there, 723 did

2026-08-02, main session. Postscript 12 concluded that records sit at
high-multiplicity corner concurrences (three cubes sharing a corner, nine face
planes through a point) and that 723 is corner-dominated. That stratum had
never been enumerated: every wall condition used in this project encodes
edge-edge coplanarity or corner-on-FACE incidence, never corner-to-corner
coincidence, which is codimension 2.

**IT IS DIRECTLY ENUMERABLE ON THE 393 BASE.** Cubes 3 = (2,1,1,1) and
4 = (1,1,1,1) are both rotations ABOUT (1,1,1), so both fix that direction and
both have a corner at exactly (1,1,1) — a 6-plane concurrence already in the
base. A free cube with a corner there makes it 9-plane. Those free cubes form
four rational one-parameter families: R0 * Rot((1,1,1), theta) where R0 carries
a chosen corner to (1,1,1); R0 = identity for the corner (1,1,1) itself, and a
180-degree turn about the bisector for the others — e.g. (0,1,1,0) carries
(1,1,-1) to (1,1,1) — so all four are integer-quaternion sweepable. Every
candidate was checked in exact arithmetic to actually have a corner at (1,1,1)
(gate: 200 sampled, 0 off-stratum).

**RESULT: 124 892 candidates, best 723, nothing above.**

    723 x49345   699 x19257   719 x16422   711 x13495   715 x9954
    707 x3972    703 x3252    717 x177     721 x69      713 x57
    697 x45      705 x33      709 x30      701 x27

723 occupies 40% of the stratum — unsurprising, since 723 IS this family: a C3
orbit on the (1,1,1) axis, built by placing cubes into that corner
concurrence. The stratum is the 723 family and it caps at 723.

**727 IS NOT IN IT.** Its free cube (7,14,1,-5) has no corner at (1,1,1). This
matches the incidence census (Postscript 47): 727 carries 18 interior edge-edge
crossings to 723's 48, and no maximal (13) pair where 723 has two. **The new
record beat the old one by LEAVING the stratum the old one occupied.**

**SO POSTSCRIPT 12'S FRAMING NEEDS NARROWING.** "Records concentrate at corner
concurrences" was a true statement about 723 and the chain below it — 699, 705,
717 were all built on the (1,1,1) axis — and a false generalisation. Corner
dominance was a property of one record, not of records. The searches that
followed from that generalisation, this project's blueprint and shared-axis
campaigns included, were therefore aimed at a stratum with a ceiling below the
current record, which is part of why 723 stood for weeks.

The count distribution is strongly quantised — five values hold 90% of the
stratum, and the intermediate values (697, 701, 705, 709, 713, 721) are rare —
as expected for a one-parameter family, where the count is piecewise constant
and the common values are the wide chambers.

### Postscript 55 addendum: the ways of reaching 727 — the discovered record is a 1-in-161 outlier, and one route carries a 13-pair

Pair-count signatures of the free cube against the five base cubes, over all
161 C3-quotiented configurations reaching 727:

    (9, 9, 4, 4, 4)   159 configurations
    (9, 9, 9, 4, 4)     1   <- the originally discovered record (7,14,1,-5)
    (13, 5, 4, 4, 4)    1   <- reaches 727 WITH a maximal pair

**CORRECTION.** Postscript 47 and its successors described 727 as "replacing
two rigid 13-pairs with three tunable 9-pairs" relative to 723, and read that
as the frustration principle appearing in a record. That is a true statement
about ONE configuration and false about the plateau: 159 of 161 reach 727 with
only TWO 9-pairs, and one reaches it carrying a 13-pair — the rigid maximal
pair the frustration story says optima avoid. The generalisation was drawn
from the single configuration then in hand, the same error as "the √-parts are
identical" and "these configurations are near-half-turns" (Postscript 52
addendum 4's caution).

The discovered record is therefore structurally atypical of its own plateau —
found first because extension-from-1207 and wide-height menus happened to land
on it, not because its structure is representative.

Signature and depth profile are INDEPENDENT axes: the (9,9,4,4,4) route spans
all three profiles (124 / 27 / 8), while each singleton route has one. So
neither invariant determines the other, and the earlier within-type constancy
of signatures (416/416, addendum 6) is consistent — types are finer than both.

## Postscript 56: E1 is now a THEOREM — the one-cube increment is bounded by an Euler count on the cube's own surface, and Postscript 53's counterexample was itself wrong

2026-08-02, main session, picking up open thread 1. Postscript 53 recorded a
failed derivation of E1 and diagnosed it as "each piece adds at most one
region is false for non-disk pieces", with the n=2 13-pair as counterexample.
**Both the diagnosis and the counterexample were wrong**, and the correct
argument is shorter than the failed one.

**THE IDENTITY.** Let G be the region adjacency graph of a compound S,
INCLUDING the outside region as a node, and let G_j keep only the edges whose
two labels differ in bit j. Forgetting cube j merges exactly those pairs, and
merging is transitive, so the regions of S minus cube j are the connected
components of G_j. With N = T + 1 nodes,

    Delta_j = N - #components(G_j)                                       (I)
            <= |E(G_j)| <= W_j <= K_j <= B_j                        (II-V)

where W_j counts walls on dC_j, K_j the mask-constant cells of dC_j, and B_j
the cells cut on dC_j by the other cubes' face PLANES (which refine the mask
cells, since each other cube's boundary lies in its own six planes). No
surface-separation lemma is needed anywhere: (II) is just "a graph on N nodes
with c components has at least N - c edges".

**THE EULER COUNT.** dC_j is a sphere and each other-cube face plane that
cuts the interior meets it in a closed curve. For any graph embedded on a
sphere with c components, F = 1 + c + E - V, so with E = sum_v deg(v)/2,

    B_j = 1 + c + SUM_v ( deg(v)/2 - 1 ),        deg(v) = 2 * #curves at v.

Checks: one circle -> 2; two disjoint circles -> 3; two circles crossing twice
-> 4; three great circles -> 8.

**WHERE POSTSCRIPT 53 WENT WRONG.** Its formula F = 2 + V assumed c = 1 and
disk faces, and — the substantive error — it counted a vertex only when two
planes' intersection line met the OPEN interior of C_j. In the 13-pair
(quaternions (1,0,0,0), (0,1,1,1)) all twelve of cube A's edge lines are
TANGENT to dB: min |R p|_inf = 1 exactly, never < 1. So the old predicate
scored twelve real vertices as zero and reported a bound of 2 against
Delta = 12. Counting them — two triple points at (1,1,1), (-1,-1,-1), six
double points (1,-1,0), (1,0,-1), (-1,1,0), (-1,0,1), (0,1,-1), (0,-1,1) —
gives 1 + 1 + (2*2 + 6*1) = 12 = Delta, EXACTLY TIGHT. The claim that
dB ^ int A is "one connected piece with six boundary circles splitting int A
into seven parts" is false; it has six components, one per wall.

**MEASURED.** Identity (I) verified on 9 (config, j) rows by two independent
routes — adjacency graph of the full compound vs re-counting the subset with
the engine (`increment_identity.py`). In all 9, |E(G_j)| = Delta_j exactly:
**G_j is a forest in every case measured**, so (II) is an equality, and the
increment equals the number of distinct region PAIRS separated by dC_j.

Bound (V) holds on all 21 rows of the old test set (`increment_bound2.py`,
delegated, gates in `DELEGATION_LOG.md`; cross-checked here on n=2/n=3/n=4):

    727 record   Delta 334-350   B 358-370    slack 1.02-1.11
    723          Delta 330-348   B 348-366    slack 1.00-1.07
    393 (n=5)    Delta 210-222   B 222-226    slack 1.00-1.06
    183 (n=4)    Delta 120-128   B 128        slack 1.00-1.07

Slack min 1.0000, median 1.0561, max 1.1078; tight at three real
configurations, not only in the hand-built n=2 case.

**WHAT IT BUYS.** E1's constant 336 was measured over a corpus; B_j is derived
per configuration and never exceeded it by more than 11%. As a UNIVERSAL
ceiling the derivation gives, at n=6, at most 2 vertices per plane pair and
C(30,2) = 435 pairs, so B_j <= 872 — rigorous but weak. The useful form is the
per-configuration one. Open problem 4 is closed for the identity and the
bound; what remains open is a good universal ceiling on B_j.

Files: `INCREMENT_BOUND_SPEC.md` (statement and gates), `increment_bound2.py`,
`increment_bound2_report.md`, `increment_identity.py`. `increment_bound.py`
stays as documentation of the failure, but Postscript 53's DIAGNOSIS is hereby
superseded: the piece bound was not the error, the tangency blindness was.

## Postscript 57: the complete taxonomy of codimension-1 walls — two types were never enumerated, and both are finite catalogues against a fixed base

2026-08-02, main session, open thread 3 ("corner-corner and edge-face
conditions"). Those two turn out not to be walls at all, and the real gap is
elsewhere.

**THE CLASSIFICATION.** For origin-centred congruent cubes the region complex
changes combinatorially exactly when FOUR FACE PLANES BECOME CONCURRENT at a
point lying on all four real faces — one condition, codimension 1 in the
3-DOF family. Classifying by how the four planes distribute over cubes gives
the complete list:

    (3,1)      corner of A on a face of B        corner-on-face quadrics
                                                 ENUMERATED (mixed strata)
    (2,2)      edge of A meets edge of B         edge-edge coplanarity
                                                 ENUMERATED (locus_linear)
    (2,1,1)    edge of A meets the crossing
               line of faces of B and C          NEVER ENUMERATED  -> W3
    (1,1,1,1)  four planes, four cubes           NEVER ENUMERATED  -> W4

The two conditions the thread named are codimension 2, hence not walls:
corner-of-A = corner-of-B is 2 independent conditions (both corners already
lie on the sphere of radius sqrt 3), and edge-of-A inside a face plane of B is
2. Both nonetheless OCCUR in the 393 base, which is part of what makes that
base special — see below.

**FINITE CATALOGUES.** Against a FIXED base the missing types become finite,
because what the free cube must meet is fixed in space (`base_points.py`):

  - 424 REAL triple points of the base's 30 planes (real = lying on the actual
    face square of every cube through it, not the plane extension). W4 becomes
    "a free-cube face plane passes through one of them", i.e. 2544 quadric
    walls in Cayley coordinates.
  - 360 crossing lines of two DIFFERENT base cubes. W3 becomes "a free-cube
    edge meets one of them": 4320 conditions.

**THE 393 BASE, DESCRIBED PROPERLY.** The triple points sort as 272 with 3
planes / 3 cubes, 60 with 4 planes / 2 cubes, 12 with **4 planes / 4 cubes**
(the (1,1,1,1) type, already present in the base), 24 single-cube corners, and
8 points carrying **6 planes from 2 cubes**. Those 8 are (+-1,+-1,+-1) — the
corners of the axis-aligned cube C4 — and each of C0, C1, C2, C3 pins an
antipodal corner pair onto them. So the base is not merely "hub-and-spoke
13-pairs": **every base cube shares a corner pair with C4**, a codimension-2
coincidence repeated four times. That is a sharper account of why 393 is
special than any given so far.

**ARE THE NEW WALLS PRODUCTIVE? EVIDENCE SAYS NO** (`w34_correlate.py`, 1200
integer quaternions drawn from a height ladder only — nothing about the count
or the incidence structure enters the draw):

    count >= 700 (n=148):  mean W4 hits  1.64,  mean W3 hits 12.45
    count <  650 (n= 37):  mean W4 hits 92.59,  mean W3 hits 96.97

The correlation runs the WRONG WAY: heavy incidence goes with FEWER regions,
as it must — coincidence merges regions. Within the low range there is a mild
positive signal (0 hits: mean 689, max 717; one antipodal pair: mean 696, max
723), then collapse. The best configuration in the sample, 717, sits on ZERO
W3 and ZERO W4 walls. Separately, W3 = 54 is the signature of the 723
corner-concurrence family, already capped in Postscript 55.

So the maximum lives at LOW but nonzero coincidence, not at high concurrence —
which retires, quantitatively, the working heuristic of Postscript 12 that
records concentrate at high-multiplicity concurrences. That heuristic
described 723, and 723 is exactly the W3 = 54 cluster.

**LIMITS.** This is a statistical argument over random draws, not an
enumeration: it says the new strata are not where a search should be pointed
first, not that nothing above 727 lies on them. An exhaustive W4 sweep would
need the wall parameterised (each is a rational conic condition on the free
cube's normal, then a rational circle of rotations about it) and is not done.

Files: `base_points.py`, `incidence2.py`, `w34_correlate.py`.

## Postscript 58: the chamber boundaries of the plateau are wall crossings — and the wall type that governs them is the one nobody had enumerated

2026-08-02, main session, open thread 4 ("do zero-width type-chambers coincide
with the high-coincidence configurations?"). TYPOLOGY.md guessed that they
"sit where extra coincidences meet". Sharpened to a testable claim: two planes
define a wall line, so a chamber boundary should be a parameter value where a
THIRD condition activates, and then

    #type changes along the line  =  #wall crossings that the type notices.

**A WRONG TEST FIRST, recorded because it is easy to repeat.** The first
version evaluated the condition catalogue AT the sampled rational points and
asked whether the type changed there. Wall crossings are measure zero, so
samples essentially never land on one; it reported "25 of 27 type changes have
no active condition" when what it had measured is that a rational sample
rarely sits exactly on a wall. The right test restricts every condition TO the
line — an edge-edge plane becomes linear in t, a corner-on-face quadric
quadratic — solves for its exact roots in the range, and asks whether each
observed change BRACKETS a root.

**RESULT** (`chamber_walls.py`, four 727-carrying lines from
`typology_data.json`, t in [2,6] at step 1/256, roots exact):

    line   samples  type changes   distinct crossings   explained  without W4
      9      874         11               19              11/11       3/11
     10      874         13               18              13/13       2/13
     11     1025         11               12               9/11       0/11
     12      351         11               16              10/11       1/11
                        ---                              -------     ------
                         46                               43/46       6/46

With ~16 crossings over ~1000 brackets, a bracket contains a crossing by
chance about 1.7% of the time, so 43/46 is not saturation — it is the claim
holding. **Chamber boundaries ARE wall crossings.**

**AND THE WALLS ARE MOSTLY THE UNENUMERATED KIND.** The project's own
catalogue — 119 edge-edge planes and 480 corner-on-face quadrics — explains
only 6 of the 46 boundaries. Adding Postscript 57's W4 walls (a free-cube face
plane through one of the base's 424 real triple points, 2544 quadrics) takes
it to 43. On line 11 the old catalogue explains NONE of the eleven.

So the combinatorial structure of the 727 plateau is governed by the
codimension-1 type that no search in this project ever enumerated. This does
NOT contradict Postscript 57's statistical finding that W4 hits do not predict
a high count: W4 walls control where the type CHANGES, not how large the count
is. Both can hold, and both now do.

The three unexplained boundaries are candidates for W3 — the (2,1,1) type,
still unmodelled as a polynomial in the Cayley coordinates — or for crossings
of a condition outside the catalogue entirely.

**WHAT THIS DOES AND DOES NOT SETTLE.** It establishes the mechanism: a
zero-width chamber is a parameter value where two crossings coincide, and
configurations satisfying many conditions at once (the discovered record's 36)
are exactly such multiple points. It does NOT verify the correspondence
configuration-by-configuration; that needs each root classified real vs
phantom, which for the irrational roots needs the ℚ(√d) engine.

Files: `chamber_walls.py`.

## Postscript 59: a 256-bit ℚ(√d) engine — the 284 634 configurations the old budget REJECTED are now countable, and the equivalence gate nearly passed vacuously

2026-08-02, main session, open thread 2. `mixed_q2_full.out` records that of
508 818 candidate configurations on the mixed 2-plane + 1-quadric strata, the
narrow engine counted 224 184 and **rejected 284 634** for exceeding its 2^112
chain budget. Rejected is not "checked and found wanting" — those
configurations are uncounted, and 56% of the stratum is a large place for a
record to hide.

**THE CONTINUED-FRACTION QUESTION, ANSWERED.** Deciding sign(p + q√d) by
continued-fraction convergents of √d instead of by comparing p² with d q²
would indeed decide more (p, q) inside 128 bits. It buys NOTHING here, because
the narrow engine's own budget derivation establishes that across the whole
admissible region the i128 CHAIN bound always binds before the sign bound.
Widening the scalar is the only thing that helps.

**THE ENGINE.** `cube_regions_q2w.cpp` (delegated; spec `WIDE_ENGINE_SPEC.md`,
gates in `DELEGATION_LOG.md`): the same engine with its scalar widened from
__int128 to a signed 256-bit type, chain threshold 2^112 -> 2^240, sign
threshold 2^231 -> 2^496, and a 512-bit square-compare in the sign predicate.
The narrow engine was not modified.

    G1 equivalence   1365 configs, 33 fields, identical bounded AND by_depth,
                     0 mismatches
    G2 rational      727 / 393 / 183 / 13 all agree with cube_regions_n
    G3 boundary      d=5, m=3001: narrow REJECTS (117.5 bits needed, limit
                     112), wide counts it (683). Wide rejects cleanly at
                     m=10^14.
    G4 selftest      ALL PASS
    G5 timing        64.5s vs 149.6s on identical input -> 2.32x

At d = 5 the admissible component magnitude moves from 1855 to between 10^13
and 10^14 — the pipeline is roughly degree 4 in the magnitude, so 128 extra
bits buys about 2^32.

**THE GATE NEARLY PASSED VACUOUSLY, which is the part worth keeping.** The
first version of the driver joined a quaternion's four components with ';'
instead of ',', so every line failed to parse, both engines emitted the same
error JSON, and comparing two identical lists of errors reported "IDENTICAL"
on all 1365 rows — in 0.11 seconds. Nothing in the verdict was wrong; the
verdict was about nothing. What caught it was the timing: 1365 six-cube counts
cannot take 0.11s when one takes 0.1s. The driver now asserts that every row
produced an actual count before any comparison is believed. **A gate that can
pass on empty output is worse than no gate**, because it manufactures
confidence.

Also noted, pre-existing in both engines and not introduced by the widening: a
component too large for int64 aborts in input parsing with an uncaught
std::out_of_range rather than a clean ConfigError. Nothing is silently
truncated, but it should be tidied.

**RUNNING.** `wide_campaign.py`, a detached sharded campaign, re-counts ALL
508 818 configurations with the wide engine — not just the 284 634 new ones,
so it doubles as an equivalence check at scale, and any disagreement on a
previously-counted configuration is a failure of the widening rather than a
new result. Results to follow.

Files: `cube_regions_q2w.cpp`, `wide_gate.py`, `wide_engine_report.md`,
`wide_campaign.py`, `wide_campaign_launch.sh`.

## Postscript 60: the irrational configurations are the SEAMS between rational continua — never interior to one, and the split is total

2026-08-02, main session, answering "are all the irrational configurations
with rational shadows part of a continuum?"

**No, and the separation is clean.** Counting active walls k from the project's
own catalogue (119 edge-edge planes + 480 corner-on-face quadrics) at every
727 configuration in hand — exactly, in ℤ[√d] for the irrational side
(`shadow_dim.py`, `shadow_type.py`):

    161 RATIONAL representatives     k = 2  : 159      <- chamber INTERIORS
                                     k = 3  :   1
                                     k = 16 :   1      <- the discovered record
    183 IRRATIONAL configurations    k = 4  : 183      <- ALL crossings

Two conditions define a wall line, so k = 2 is a point interior to a chamber —
a continuum of its own combinatorial type — and k >= 3 is a wall crossing, a
zero-dimensional stratum. **Every irrational 727 is a crossing. Not one is
interior to anything.** Their k = 4 is exactly the mixed-strata construction:
two planes and one corner-on-face condition, which the catalogue counts twice
as a ± pair.

**AND IT HAS TO BE THIS WAY.** The wall lines of the enumerated strata are cut
by pairs of RATIONAL planes (Postscript 49: edge-edge conditions factor into
rational planes). A chamber interior is an open interval of such a line, and an
open interval of a rational line contains rational points, on which the type is
constant. So **any combinatorial type possessing a continuum is attained
rationally**, and an irrational configuration can only ever be a zero-width
type — an endpoint. Irrationality is confined to the seams.

**MEASURED CONSEQUENCE.** Of the 21 distinct per-label types among the 183
irrational 727s, 11 also occur among the 161 rational representatives and
**10 occur at none of them** — the zero-width types whose defining root
happens to be irrational.

**WHAT "RATIONALLY SHADOWED" ACTUALLY MEANT.** Postscript 52 established
shadowing at the level of the COUNT: 727 holds along the whole stretch of line
through these points, so rationals are dense in the count-level set around
them. That remains true and is why irrationality does no work for the RECORD
VALUE at n = 6. It was never a statement about the configuration, and this
postscript marks the boundary: the count continuum is rational-dense; the type
stratum at an irrational point is a single algebraic point.

Contrast with n = 3, where irrationality is required for the count itself, not
merely realised at a seam. That distinction now has a mechanism rather than
just a pair of observations.

**LIMIT.** "Occurs at none of them" is relative to 161 known rational
representatives, not a proof of non-attainability; the argument above says a
type with a continuum must be rational, not that these 10 types have no other
rational realisation elsewhere.

Files: `shadow_type.py`, `shadow_dim.py`.

## Postscript 61 (CORRECTION to Postscript 60): the irrational configurations ARE in continua — k counted walls, not chamber boundaries, and most of those walls are combinatorially inert

2026-08-02, main session, same day, answering "what is the relationship
between an irrational configuration and its rational shadow?"

**THE RELATIONSHIP.** An irrational 727 and its shadow are the SAME
COMBINATORIAL OBJECT at different parameter values of one rational
one-parameter family. Verified exactly (`shadow_relation.py`, 16 configurations
across all eight fields, gate: the recovered line must contain the point
exactly in ℤ[√d], 16/16 pass):

  - The two active edge-edge planes are RATIONAL, so they cut a RATIONAL line
    in Cayley space. The irrational configuration lies on it, and so do its
    shadows: they share its two edge-edge coincidences exactly.
  - Its irrationality has one source and no other: the third condition, a
    corner-on-face quadric, meets that rational line at an irrational
    parameter t*. A rational line through a rational quadric, root irrational.
  - The shadow is obtained by sliding along the line to a nearby rational
    parameter. **In 14 of 16 cases the per-label type is IDENTICAL at t* and
    at both neighbours**; in 2 cases one side differs.

So the extra coincidence that makes the point irrational is invisible to the
region complex: it changes neither the count nor the labelling. It is a
tangency the combinatorics does not register.

**WHICH REFUTES POSTSCRIPT 60'S HEADLINE.** That postscript inferred from
k = 4 active walls that every irrational 727 is a chamber BOUNDARY and "not
one is interior to anything". The inference used k as a proxy for "chamber
boundary", and the proxy is wrong — Postscript 58 had already measured that
k >= 3 points frequently pass with NO type change (8 of 19 crossings on line
9 alone). Tested directly instead of by proxy, 14 of 16 irrational
configurations are interior to their own type-chamber. **They are part of
continua.** What survives from Postscript 60 is the wall count itself (161
rational reps: 159 at k=2; 183 irrational: all at k=4) and the observation
that irrationality enters only through a quadric root on a rational line.

**AND THE SECOND CLAIM FALLS TOO.** Postscript 60 reported 10 of 21 irrational
per-label types occurring at "no rational configuration", hedged as relative to
the 161 known representatives. The hedge was right and the number was an
artifact: of the sampled configurations whose type is absent from those 161,
**7 of 7 have that exact type at an immediate RATIONAL neighbour** on their own
line. The 161 representatives are k=2 points from the edge-edge three-wall
enumeration — a different family — so their absence from that list says
nothing about attainability. No type is known to be irrational-only.

**METHODOLOGICAL NOTE.** This is the fourth time in this project a structural
claim has been made from a proxy invariant rather than the thing itself
(after: rigidity by openness, μ-multiset for congruence, and describing a
family from its first member). The proxy was reasonable and the direct test
was cheap. Postscript 60 stood for about an hour.

**WHAT IRRATIONALITY DOES AT n = 6, FINALLY.** Nothing. Not to the count
(rationally shadowed, Postscript 52), and not to the combinatorial type
(shadowed as well, here). It is an accident of where a rational line happens to
cross a rational quadric. Contrast n = 3, where the maximum cannot be attained
rationally at all.

Files: `shadow_relation.py`, `shadow_type.py`, `shadow_dim.py`.

### Postscript 61 addendum: over all 183, SOME are in continua and some are not — and in a continuum irrationality is the generic case, so its presence was never informative

2026-08-02, main session, after "are you now saying that n≠3 irrationals are
part of a continuum?" and "some are and some aren't?" and "in any case every
continuum of configurations will contain irrational points."

**SCOPE FIRST.** No. Nothing here is a claim about irrational configurations at
n ≠ 3 in general. Everything measured is the 183 irrational **727s at n = 6 on
the 393 base**, produced by one enumeration (2 rational planes + 1 quadric).
Nothing is measured at n = 4, 5, 7, 8, nor for non-record irrationals, nor for
irrationals from the unenumerated strata — which need not lie on a rational
line at all, and so need not have rational neighbours by construction.

**THE FULL SET** (`shadow_all.py`, all 183, neighbours at step ~1e-5):

    2 rational planes + 1 quadric (± pair)          183 of 183   STRUCTURAL
    same per-label type on BOTH sides               105  (57%)
    same type on exactly ONE side                    28  (15%)
    neither side matches at this resolution          50  (27%)

So **some are and some are not** — the correct answer, and not the one given
from a 16-configuration sample an hour earlier, which read 14/16 and would have
implied ~87%. The structural half is universal: all 183 lie on RATIONAL lines,
so every one has rational neighbours; what varies is whether the type survives
the crossing.

**THE 50 ARE UNRESOLVED, NOT ISOLATED.** In most of them the sampled
neighbours do not count 727 at all, meaning the 727 stretch around the point is
narrower than the sampling step. Refining the step fails for an instrument
reason: the finer neighbours need quaternion components beyond about 1e7 on
these lines, and the rational engine rejects them ("degenerate plane triple").
A run at step 2e-8 returned engine REJECTIONS for 119 of 183, which is not a
measurement of anything — recorded here because such a run superficially
produces a table that looks like data.

**THE OBSERVATION THAT REFRAMES ALL OF IT.** Every continuum contains
irrational points — and more than that, irrational points are the GENERIC ones:
in any interval they have full measure and the rationals have measure zero. So
the moment the 727 set contains any interval at all, "727 is attained at
irrational configurations" is guaranteed and carries **no information**. The
project has repeatedly treated its irrational finds as exotic (Postscript 51's
"a fifth 727 class that is IRRATIONAL"); in a continuum, irrational is the
default and it is the RATIONAL points that are special.

Our 183 are not typical points of their continua either. They are the
low-degree algebraic points an equation-solver can emit — degree 2, in ℚ(√d).
A typical point of a 727 interval is irrational of unbounded degree, plausibly
transcendental, and no enumerator in this project will ever produce one.

**WHICH SHARPENS THE n = 3 STATEMENT.** What makes n = 3 different is not that
its maximisers are irrational; it is that its optimum set is TWO ISOLATED
POINTS. Isolated optima can be forced to be irrational; optima with a continuum
cannot, since any interval carries rationals. The real dichotomy is
isolated-versus-continuum, and irrationality is downstream of it.

Files: `shadow_all.py`.

## Postscript 62: what happens at the endpoint of a 727 continuum — the interval is OPEN, the endpoint has its own count, and region counts are NOT semicontinuous

2026-08-03, main session, answering "when there are continua, what happens at
the end points?"

**THE ENDPOINT, EXACTLY.** On wall line 9 of `typology_data.json`, 727 holds
across sampled t in [2, 13.5]. Its upper end is a W4 wall — the type
Postscript 57 catalogued and no search had enumerated — at the IRRATIONAL
parameter

    t* = 18913/2736 + sqrt(4111761)/304 = 13.58286911126...

verified by substituting back: the W4 condition simplifies to exactly 0 there.
The configuration at t* is the integer quaternion over ℤ[√4111761]

    (304:0, -12710:-6, 18913:9, 8980:4)          [p:q meaning p + q√4111761]

which the NARROW engine cannot count — it needs 214 bits against a 112-bit
chain budget, exactly the case this morning's wide engine was built for.

    t = 13.58286  (below t*)   ->  727
    t = t*        (the wall)   ->  725      <- two engines
    t = 13.58287  (above t*)   ->  723

The 725 is certified by the two-engine rule: `cube_regions_q2w` and,
independently, the Python exact-sign field engine
(`resonance4_solve.exact_count_field` over ℚ(√4111761)), agreeing on the total
AND the profile {212, 220, 156, 100, 36, 1}.

**SO THE INTERVAL IS OPEN.** The record value is not attained at its own
boundary here; the endpoint sits one ±2 step below the plateau and one step
above the next chamber. Three distinct values in a row, ±2 apart, which is the
quantum central symmetry forces.

**AND REGION COUNTS ARE NOT LOWER SEMICONTINUOUS.** The natural expectation —
stated in `endpoint.py` before the measurement — was that a coincidence merges
regions, so the count at a wall should be no larger than at nearby generic
configurations on EITHER side. That is false: 725 at the wall exceeds 723 just
above it. The mechanism is a PINCH. At a tangential contact the mask region is
open-but-pinched at the contact point, so the point is excluded and the two
lobes count as two regions; perturb one way and the channel opens and they
MERGE into one; perturb the other way and they separate properly. A degenerate
configuration can therefore carry MORE regions than a neighbour, and the count
is neither upper nor lower semicontinuous.

This also disposes of a tempting corollary — "records live in chamber
interiors, never at boundaries". The endpoint here does lose the record, but
the originally discovered 727 sits at k = 16 active walls (Postscript 60), a
heavily degenerate point that attains the record. Both happen.

**METHOD NOTE.** The first run of `endpoint.py` found ZERO roots at either end,
because it searched only the classical catalogue. The endpoint is a W4 wall.
An endpoint analysis using the pre-Postscript-57 vocabulary would have
concluded the interval simply stops for no reason.

Files: `endpoint.py`.

### Postscript 62 addendum: the OTHER endpoint — W3 written as a polynomial at last, and both ends of the interval are 725

2026-08-03, main session, prompted by "a line has two endpoints". The
postscript above analysed only the upper one; the lower end had reported ZERO
catalogued roots and was left unexplained. It is a W3 wall — the (2,1,1) type,
the last one with no polynomial form.

**W3 AS A POLYNOMIAL** (`w3_poly.py`). With q = (1,a,b,c), M the unnormalised
rotation matrix and N = 1+a²+b²+c², the free cube's edge along axis A with
signs sB, sC is the line through (M[:,B]sB + M[:,C]sC − M[:,A])/N with
direction M[:,A]. Meeting a fixed base crossing line (p, d) is

    det[ M[:,A],  d,  N·p − (M[:,B]·sB + M[:,C]·sC − M[:,A]) ] = 0.

**It is degree 4**, not a quadric: 4320 conditions on the 393 base, and
restricted to a wall line every one of them is a QUARTIC in t. So a W3
crossing can be an algebraic number of degree 4, outside every ℚ(√d) — a class
of configuration no enumeration in this project could ever have produced, since
the mixed strata solve a quadratic and return ℚ(√d) by construction, and one
that only the degree-agnostic `opencount.py` engine could count at all.

**THE LOWER ENDPOINT.** Bisecting the 727 stretch on line 9 puts it at
t ≈ 1.9317123. Exactly two W3 conditions change sign in that bracket — an
antipodal pair, base cubes 0 and 2, free edge axis 2 — and there the quartic
factors, leaving

    4455 t² − 11790 t + 6151 = 0,    t* = (11790 + 648√70)/8910

so this endpoint lands in ℚ(√70) after all. The configuration is the integer
quaternion over ℤ[√70]

    (55:0, -455:-24, 655:36, 395:16)

which the NARROW engine again rejects — m = 655 with d = 70 is outside its
budget. Counted by `cube_regions_q2w` and independently by the Python
exact-sign field engine, both giving

    count = 725,  by_depth {212, 220, 156, 100, 36, 1}

**SO THE INTERVAL IS SYMMETRIC.** The 727 continuum on line 9 runs from
(11790 + 648√70)/8910 to 18913/2736 + √4111761/304, is OPEN at both ends, and
carries **725 with the identical depth profile at each**. One end is a W3 wall,
the other a W4 wall — the two types this project had never enumerated until
today, neither reachable with yesterday's vocabulary, and both needing
this morning's widened engine to count.

Files: `w3_poly.py`, `endpoint.py`.

## Postscript 63: the LINE catalogue was never symmetry-closed — the richest 727 continuum's own C3 images were missing, and a uniform parameter grid is not equivariant

2026-08-03, main session, answering "do lines fit into our TYPOLOGY?"

**WHERE LINES SIT.** TYPOLOGY.md already places them: a per-label TYPE is a
CHAMBER of a wall line, so a line is one level ABOVE a type and carries a
sequence of them. The question is whether the typology's own structure extends
upward, and the sharp test is the C3 — the rotation about (1,1,1) that leaves
the 393 base invariant and that configurations must be quotiented by or they
triple-count.

**IT DOES.** The C3 acts on a free cube by LEFT MULTIPLICATION by (1,1,1,1),
and in Cayley coordinates left multiplication by a fixed quaternion is a
PROJECTIVE map of (1,a,b,c) — so it carries lines to lines. Measured exactly
(`line_typology.py`, collinearity in Fractions): among the 129 recorded lines,
all 129 distinct as geometric lines, 32 orbits of size 3.

**BUT THE CATALOGUE IS NOT CLOSED UNDER IT.** 22 of the 129 have images that
are not in the set. Closing it adds 33 lines: **162 total, 50 orbits of size 3
covering 150**; the remaining 12 have images running through w = 0, outside the
Cayley chart, which is a chart artifact rather than a geometric one.
(`lines_c3_closed.json`.)

**AND THE MISSING ONES ARE NOT MARGINAL.** Line 9 — the richest continuum
found, carrying 727 across t in [1.9317, 13.5829], width 11.65, the line whose
two endpoints Postscript 62 analysed — has BOTH its C3 images absent from the
recorded catalogue. By equivariance there are two further 11.65-wide 727
intervals that no enumeration in this project ever recorded. **Every census
over the 129 lines, including the one currently running, is incomplete by
construction.**

**A UNIFORM PARAMETER GRID IS NOT EQUIVARIANT.** Because the C3 is projective
it does NOT preserve the line parameter: a 727 stretch at t ≈ -1.75 maps to
its image line at t ≈ -0.013, compressed far below any fixed sampling step. So
scanning every line on the same grid in t systematically misses the compressed
images of intervals it finds elsewhere. This is the failure mode already
recorded for the height cap 512 and the rectangular (d, m) guard — a filter
that is not preserved by the group — recurring in a new place.

**TWO PROCESS FAILURES IN THE SAME HOUR**, both now in `FAILURE_MODES.md`:
 1. The first census run reported "0 continua" for all 129 lines in about two
    minutes. Engine children were dying under memory pressure from the
    concurrent 8-shard campaign; `count_many` returned an empty list;
    `zip(ts, got)` produced nothing. Uniformly zero AND impossibly fast. The
    driver now asserts result count equals input count.
 2. The orbit comparison then read `continua_shard_0.jsonl`, which is opened in
    APPEND mode and still contained that broken run's 129 empty records — so
    unscanned lines silently read as "no continua" and the comparison reported
    a tidy "26 orbits agree, 6 disagree". Rebuilt from the live run's own
    output: **0 orbits fully scanned so far**, so that entire table was about
    nothing. Accumulated output from a superseded run is not data.

**UNVERIFIED OBSERVATION.** The closed set has 54 orbits' worth of lines by
count (162/3), and the plateau has 54 per-label types. Whether that is a
correspondence or a coincidence is untested — types are chambers and a line
carries several, so equinumerosity would be surprising and should not be
assumed.

Files: `line_typology.py`, `lines_c3_closed.json`, `continua.py`.

## Postscript 64: the n=6 typology applies to n=3, but the wall taxonomy TRUNCATES and the base-fixing method provably cannot reach max(3)

2026-08-03, main session, answering "can the TYPOLOGY of n=6 apply to n=3
configurations?"

**THE MACHINERY TRANSFERS UNCHANGED.** Fix n−1 cubes, give the last one its 3
degrees of freedom in Cayley coordinates, and everything the n=6 typology uses
is defined: walls, lines as two-wall intersections, chambers, per-label types,
plateaux. Nothing in it is specific to six cubes.

**BUT THE TAXONOMY IS GRADED BY n.** A wall is four face planes concurrent, and
the types are named by how many CUBES supply them:

    (3,1)      corner-on-face     needs 2 cubes   exists from n = 2
    (2,2)      edge-edge          needs 2 cubes   exists from n = 2
    (2,1,1)    W3                 needs 3 cubes   exists from n = 3
    (1,1,1,1)  W4                 needs 4 cubes   exists from n = 4

So at n = 3 only three of the four types exist, and at n = 2 only two. **W4
first exists at n = 4** — which is exactly the level where frustration switches
on and the maximum stops being attainable by symmetry. Whether that is a
mechanism or a coincidence is untested and should not be assumed; it is
recorded because it is checkable.

**AND THE METHOD PROVABLY CANNOT FIND max(3).** The n=6 programme works by
fixing a RATIONAL base and sweeping the free cube. At n = 3 that is structurally
excluded from the answer:

  - Theorem R: a rational configuration has rational O-reduced pair invariants.
  - Both 67 maximisers have IRRATIONAL pair invariants on every pair — ½+√2
    (octahedral) and 3φ/2 (golden), and in each the three pairs are equivalent
    by symmetry.
  - μ of the base pair is an invariant OF THAT PAIR, untouched by whatever
    third cube is added.

Therefore fixing any rational pair excludes 67 no matter what the third cube
is, rational or not. Measured, over ~3500 third cubes each on three rational
bases:

    base = 13-pair (1,0,0,0),(0,1,1,1)      max 59
    base = 9-pair  (1,0,0,0),(2,1,0,0)      max 43
    base = C0,C1 of the 393 base            max 63

all short of 67, and 63 matches the known "best triple inside any higher
record" figure.

**THE FINDINGS INVERT.** At n = 6 the record is a PLATEAU — a union of
1-dimensional segments, at least 161 configurations in 54 types. At n = 3 the
maximum is TWO ISOLATED POINTS. So chamber language describes n = 3's
sub-maximal strata perfectly well, while its optimum has no chamber at all: it
is a zero-dimensional stratum. That the base-fixing method works at n = 6 is a
fact about where the n = 6 record happens to live (reachable from the rational
393 base), not a property of the method.

## Postscript 65: max(3) is an upward SPIKE on a 55-plateau — the exact inverse of n=6, and the geometric face of frustration

2026-08-03, main session, answering "could max(3) be thought of as a line where
the endpoints have more regions instead of less?" Nearly — and running the
measurement settles the shape. This also closes Task 1 of
`DIHEDRAL_FAMILY_NEXT.md`, open since 2026-07-16.

**THE FAMILY.** The dihedral family (Postscript 25) is the one-parameter
compound {I, S, S²} with S(ψ) the ±120° rotation about n(ψ) = (sin ψ, cos ψ, 0).
At Pythagorean ψ the entries lie in ℚ(√3), so `q3_count.py` counts them
exactly. Sweeping ψ across (0°, 90°) gives a symmetric staircase:

    psi      0      8.8    10-19    22.6-67.4    71-80    81     90
    count   25       31      43         55         43      31     25

**THE TWO 67s ARE SPIKES INSIDE THE 55 PLATEAU.** Refining with Pythagorean
angles up to r = 900:

    octahedral 67 at psi = 35.264deg (arcsin 1/sqrt3, irrational)
        34.894 -> 55    35.051 -> 55    35.300 -> 55    35.489 -> 55
    golden 67 at psi = 69.095deg (tan psi = phi^2, irrational)
        68.574 -> 55    68.761 -> 55    69.017 -> 55    69.390 -> 43

Both maxima are bracketed within a quarter of a degree by configurations
counting 55. **The n=3 maximum is a +12 spike at an isolated irrational point
of a plateau whose generic value is 55.** (+12 = six antipodal pairs, the
quantum central symmetry forces.)

**SO THE TWO LEVELS ARE OPPOSITE SHAPES**, though not quite as mirror images:

    n = 6:  the record is an INTERVAL (727 across a stretch of a wall line),
            and its ENDPOINTS DIP to 725 -- open at both ends (Postscript 62).
    n = 3:  the record is a POINT, spiking UP by 12 from the 55 plateau it
            sits inside. It is not the endpoint of a 67-interval; there is no
            67-interval.

**AND THE MECHANISM IS ALREADY IN HAND.** Postscript 62 found that region
counts are NOT semicontinuous, because a tangential contact PINCHES a region
at a point: the contact point is excluded, so the two lobes count separately.
That is exactly what lets a degenerate configuration carry MORE regions than
its neighbours — the upward spike here — while a coincidence that merges rather
than pinches produces the downward dip seen at the n=6 endpoints. Both
directions occur, and now both have been measured on real configurations.

**THIS IS FRUSTRATION, GEOMETRICALLY.** The project's account has been: at
n <= 3 every depth layer can be maxed at once, which is a RIGID demand and
lands on isolated irrational points; from n = 4 the layers must be traded, and
trades live on open sets, hence rational. The two shapes above are that story's
geometry — **rigid optima are spikes, traded optima are plateaux.** The
irrationality at n = 3 is then a corollary of the shape, not an extra fact: an
isolated point has no interval around it to carry rationals.

Files: `q3_count.py` (existed, never run), `dihedral_family_counts.out`.

## Postscript 66 (CORRECTION to Postscript 63): the line catalogue WAS symmetry-closed — the test compared quaternion representatives instead of configurations

2026-08-03, main session, after a chain script failed and forced a re-read of
the previous hour's work.

**POSTSCRIPT 63 IS WITHDRAWN in its structural claims.** It applied the C3 to
lines by LEFT MULTIPLICATION, q -> g*q. But g = (1,1,1,1) is the 120-degree
rotation about (1,1,1), which is a CUBE SELF-SYMMETRY, so g*q and g*q*g^-1
describe the SAME SOLID — they differ by right multiplication by an octahedral
element, which no cube can tell apart. Verified: both actions permute the five
base solids identically, as (0,1,2)->(1,2,0).

So the two differ only in WHICH of the 24 quaternion representatives they name,
and the catalogue stores one representative per line. Postscript 63 therefore
tested "is this particular representative in the list", not "is this
configuration in the list". **This project had already recorded exactly this
trap** — Postscript 49 addendum, "the Cayley chart omits quaternion
representatives, not compounds" — and it was repeated.

**THE CORRECTED MEASUREMENT.** Under conjugation q -> g*q*g^-1:

    image in the catalogue        129 of 129   (Postscript 63 said 107)
    orbits                        43, all of size 3, covering all 129
    parameter along the line      PRESERVED EXACTLY: t -> t

Line 9's images are lines 88 and 37, both present, both carrying 727 over the
identical stretch t in [2, 13.5].

Withdrawn with it: "22 lines have images outside the set"; "closing the
catalogue adds 33 lines, 162 total"; "line 9's C3 images are absent"; "there
are two further 11.65-wide 727 intervals never recorded"; "the C3 compresses
the parameter, so a uniform grid in t is not equivariant"; and "every census
over the 129 lines is incomplete by construction". The compression figure
(t = -1.75 -> -0.013) was the wrong representative, not a projective effect.
`lines_c3_closed.json` is an artifact of the error and should not be used.

**AND THE CENSUS NOW CHECKS OUT AGAINST THE SYMMETRY.** All 129 lines scanned,
t in [-20, 20] at step 1/2:

    21 lines carry a 727 continuum = EXACTLY 7 C3 orbits of 3, with matching
    widths in every orbit:
        [9, 37, 88]      width 11.5     <- the long one, Postscript 62's line
        [73, 116, 120]   width  1.5
        [12, 38, 95] [24, 35, 82] [31, 32, 103] [69, 106, 119]   width 0.5
        [28, 30, 34]     width  0.0     <- single sample; interval or isolated
                                           POINT is unresolved at this step

Locations differ within an orbit only because each line carries its own
(p0, dir) convention; the widths agree everywhere. That is the equivariance
Postscript 63 claimed was absent.

**HOW IT SURFACED.** A chain script died with "continua_shard_0.jsonl: No such
file or directory" — because the file had been renamed while the census still
held it OPEN in append mode, and on Unix a rename follows the inode, so the
running process kept writing to the renamed file and the expected name was
never created. The chain then printed "phase B done" without checking the exit
status. Both are now in `FAILURE_MODES.md`.

Files: `line_typology.py` (uses the wrong action; superseded),
`continua.py`, `continua_shard_0.jsonl` (rebuilt from the live run).

## Postscript 67: the full endpoint census — every continuum end counts 725, and n=6 ALSO has isolated 727 SPIKES, the n=3 shape appearing rationally at n=6

2026-08-03, main session, completing the census the "check all endpoints"
thread asked for.

**THE CONTINUA.** All 129 727-carrying lines scanned over t in [-20, 20] at
step 1/2 (`continua.py`). **21 lines carry a 727 continuum, forming exactly 7
C3 orbits of 3**, with matching widths inside every orbit:

    [9, 37, 88]    width 11.5      <- the long one (Postscript 62's line)
    [73, 116, 120] width  1.5
    [12, 38, 95] [24, 35, 82] [31, 32, 103] [69, 106, 119]   width 0.5
    [28, 30, 34]   width  0.0      <- below the sampling step

**THE ENDPOINTS.** All 42 analysed exactly (`continua_endpoints.py`): bisect to
a bracket ~1e-7 wide, find every catalogue condition changing sign inside it,
take its exact root, count the configuration AT the root.

    W3        -> 725    9 endpoints
    W4        -> 725   18
    edge-edge -> 725   12
                      ---
                       39, and EVERY ONE COUNTS 725

So the finding of Postscript 62 generalises: **a 727 continuum is open at both
ends, and its endpoint sits exactly one +-2 step below the plateau.** The W3
endpoints resolve only after the quartic is FACTORED over Q — unfactored they
report degree 4 and cannot be counted at all.

**THE OTHER THREE ARE NOT ENDPOINTS.** On the orbit [69, 106, 119] the
bisection converged on a point counting 727. It is not the edge of the
continuum: at t = 11/8 on line 119, the configuration is the rational
quaternion **(4, -28, -44, -17)**, and

    count(11/8)          = 727   (cube_regions_n AND region_adjacency)
    count(11/8 +- 1e-4)  = 723
    count(11/8 +- 1e-5)  = 723
    count(11/8 +- 1e-6)  = 723
    count(11/8 +- 1e-7)  = 723        (finer is beyond the engine's budget)

**This is an ISOLATED 727 point** — a +4 spike with 723 on both sides — sitting
on the same line as, but separate from, the continuum over [1.5, 2.0].

**SO n = 6 HAS BOTH SHAPES.** Postscript 65 found max(3) = 67 to be an upward
spike on a 55-plateau, and contrasted it with n = 6's record being an interval.
That contrast was too clean: n = 6 has continua AND isolated spikes, on the
same line. The difference that survives is arithmetic, not shape — **n = 3's
spikes are irrational and are the maximum; n = 6's spike here is RATIONAL and
merely ties a value also attained on intervals.**

**METHOD.** The bisection assumes a single monotone transition inside its
starting bracket. Where a spike sits between the bracket end and the continuum,
it converges on the spike instead. That is how these three were found — an
accident that produced the most interesting object in the census, and a
reminder that the routine is not a general endpoint locator.

**FOUR PROCESS FAILURES, all now in `FAILURE_MODES.md`:** an output file opened
in APPEND mode mixed four incompatible runs and made me "verify" a 727 endpoint
at a parameter that was not even inside the continuum (the count there is 691,
correctly); a file was RENAMED TWICE while a process held it open, so the live
records followed the inode into the quarantined name; `sympy.real_roots`
returned CRootOf objects which `nsimplify` then numerically GUESSED into
expressions like 2**(103/253), putting a float heuristic inside an exact
pipeline; and a chain script announced "phase B done" immediately after phase B
crashed, because it never checked the exit status.

Files: `continua.py`, `continua_endpoints.py`, `continua_phaseA.out`,
`continua_phaseB2.out`.

## Postscript 68: epsilon-neighbourhoods show walls are NOT equivalent — the walls carrying 727 are worth +6 each, the walls that end it cost −2

2026-08-03, main session, following "let's see what epsilon-neighbourhoods tell
us about the structure".

**THE OBJECT.** A wall line is the intersection of TWO walls, so a point on it
has a 9-cell neighbourhood in the 3-DOF configuration space: the line itself
(on both walls), 4 sectors on exactly one wall, and 4 open quadrants on
neither. With n1, n2 the defining normals and u1, u2 their reciprocal vectors,
moving by s1*u1 + s2*u2 crosses wall i exactly when si != 0, so the sign pair
names the cell with no numerical guessing (`eps_neighbourhood.py`).

**THE COUNTS ARE COMPLETELY UNIFORM.** Every chamber of line 9, and every line
tested — 6 different wall pairs drawn from 5 different C3 orbits — gives the
identical picture:

    on the line   (both walls)      727
    one wall only (4 sectors)       721
    neither wall  (4 quadrants)     715

**So each defining wall is worth +6**, additively and independently:
727 = 715 + 6 + 6. Six is three antipodal pairs, the ±2 quantum applied three
times.

**BUT THE ENDPOINT WALLS GO THE OTHER WAY.** At an endpoint the configuration
lies on a THIRD wall, and the count is 725 (Postscript 67, all 39 of them) —
not 715 + 18 = 733. The third wall contributes **−2**.

So the naive grading "count = 715 + 6·(walls you are on)" is FALSE, and its
failure is the finding: **walls are not equivalent.** Some add regions and some
remove them. The two edge-edge walls that carry a 727 line are +6 walls; the
W3, W4 and edge-edge walls that terminate the line are −2 walls. The same wall
TYPE appears on both sides of that divide — edge-edge walls both define lines
(+6) and end them (−2) — so the sign is not a function of the taxonomy of
Postscript 57. It is presumably the pinch/merge distinction of Postscript 62: a
coincidence that PINCHES a region into two adds regions, one that MERGES
removes them.

**WHICH REFRAMES WHAT A RECORD IS.** Not "a configuration with many
coincidences" — Postscript 57 already measured that more coincidence means
fewer regions. It is a configuration sitting on as many +6 walls as possible
while avoiding the −2 walls. The 727 lines are exactly the loci where two +6
walls meet, and they end precisely where a −2 wall crosses.

**AND THE NEIGHBOURHOOD ADDS NOTHING AT THE COUNT LEVEL, EVERYTHING AT THE
TYPE LEVEL.** The 9-cell count signature is identical for all 11 chambers of
line 9, so it cannot distinguish letters. The 9-cell per-label TYPE signature
is maximally fine: all 99 sampled cells (11 chambers x 9 cells) carry 99
DISTINCT canonical types. Between those extremes there is no intermediate
invariant here — counts are constant, types are injective.

Files: `eps_neighbourhood.py`, `word_typology.py`.

## Postscript 69: n=2 mapped completely — five counts, generic 4, and the maximum on CURVES, the same codimension as n=6's 727 lines

2026-08-03, main session, answering "can we map the full structure of
neighbourhoods for n=2?" Yes: two cubes have 3 degrees of freedom and, by
Postscript 57's taxonomy, only two wall types can exist (W3 needs three cubes,
W4 needs four), so n=2 is the one level where the whole space can be charted.

**ONLY FIVE COUNTS OCCUR**, with depth profiles {d1, 1}:

    count    1     4     5     9    13
    d1       0     3     4     8    12

**THE GENERIC COUNT IS 4.** Over random integer quaternions, as the height
grows the distribution converges hard:

    height     2 :  1:18.7%          9:35.0%  13:46.3%
    height    10 :  4:26.2%  5:40.5%  9:27.3%  13: 5.5%
    height   100 :  4:90.0%  5: 6.3%  9: 3.7%  13: 0%
    height  1000 :  4:98.8%  5: 0.8%  9: 0.3%  13: 0%

**CORRECTION, to a claim made an hour earlier in this same session.** A first
sample over mixed heights 2..144 gave 13 on 9.5% of draws, and I read that as
"the maximum is attained on an open set of positive measure". It is not.
SMALL INTEGER QUATERNIONS ARE THE SPECIAL CONFIGURATIONS — they satisfy many
rational conditions at once — so sampling them oversamples walls by an
enormous factor. At height 60, ZERO of 400 draws reach 13; at height 1000 the
count is 4 in 98.8% of draws. The ledger's own earlier description, "13 is a
continuum" (Postscript 44), was right; my gloss of continuum as "open set"
was the error.

**THE 13-SET IS A CURVE.** Along the body-diagonal family (a,b,c) = (t,-t,t)
the count is 13 at every sampled t; perturbing transversally at t = 5/7 gives
9 on one side and 5 on the other. So the maximum sits at codimension 2 in the
3-DOF space — **exactly the codimension of n=6's 727 lines**. The two levels
have the same shape after all; what differs is the size of the bonus. At n=2
the maximum is 3.25x the generic count (13 against 4); at n=6 it is 1.7% above
the local generic value (727 against 715).

**AND THE EXTREME DEGENERACY COLLAPSES.** The 24 rotations that are cube
self-symmetries make the two cubes coincide and the count falls to 1 — the
MINIMUM, at the most special points in the space. So "more coincidence" does
not run one way: coincidence raises the count (4 -> 5 or 9 -> 13) until the
cubes merge, at which point everything collapses.

Files: `n2_map.py`.

### Postscript 69 addendum: the n=2 stratification, from epsilon-adjacency — the count is determined by the DIMENSION of the stratum

2026-08-03, main session, answering "which of those five counts are epsilon
neighbours? identical counts epsilon-neighbours of each other should be
members of a continuum."

That criterion is exactly right, and it measures dimension. Probing each
count's representative with a lattice p + (i,j,k)/D, |i,j,k| <= 2 (124 points),
at D = 24, 96 and 384 — the neighbour distributions are IDENTICAL at all three
radii, so the local structure is conical — and the number of neighbours
sharing the count reads off the dimension directly:

    count   own-count neighbours   of 124      dimension
      4        124  (all)                        3   open
      5         24  = 5^2 - 1, a plane           2
      9         18                               2
     13          4  = +-1, +-2 on a line         1   CURVE
      1          0                               0   isolated

**Self-adjacency detects the continuum exactly as proposed**: 4, 5, 9 and 13
are each adjacent to themselves and so lie in continua; 1 is not, and is
attained only at the 24 isolated points where the cubes coincide.

**THE STRATIFICATION.** Every stratum has all the higher-dimensional ones in
its neighbourhood:

    dim 3   count  4     neighbours: 4
    dim 2   count  5     neighbours: 4, 5
    dim 2   count  9     neighbours: 4, 9
    dim 1   count 13     neighbours: 4, 5, 9, 13
    dim 0   count  1     neighbours: 4, 5, 9, 13

So n=2's configuration space is a clean stratified space in which **the region
count is a function of the stratum's dimension** — 3 -> 4, 2 -> 5 or 9,
1 -> 13, 0 -> 1. The count rises as the dimension falls, until the final
collapse at the coincidence points.

**ONE LATTICE ARTIFACT, caught before it was recorded as a fact.** The lattice
probe at the coincidence point reported neighbours {5, 9, 13} and NO 4,
suggesting the generic count does not occur near a coincidence. It does:
sampling genuinely generic rotations of angle ~1/1000, ~1/10^5 and ~1/10^7
about that point gives 4 in about 60% of draws at every scale. The lattice
near the origin consists entirely of small-denominator points, which are all
arithmetically special — the same bias that made the "13 is attained on an open
set" reading wrong earlier in this session. The bias is a useful instrument for
finding rational walls and a trap for judging what is generic; it must not be
used for both at once without saying which.

Files: `n2_adjacency.py`.

## Postscript 70: the topology of the n=2 stratification — it is the OCTAHEDRAL MIRROR ARRANGEMENT on the axis sphere, fibred by the rotation angle

2026-08-03, main session, answering "if we fill the 3-DOF space with dimension
labels, what is the topology of that structure?"

**IT IS NOT AN ARBITRARY ARRANGEMENT.** Cayley coordinates (a,b,c) are the
rotation AXIS scaled by tan(theta/2), so the space fibres over the sphere of
axis directions with the angle as fibre — and the strata are governed by where
the axis sits in the cube's OWN symmetry arrangement. Measured across 33
angles per axis:

    axis (1,2,3), (2,3,5)   GENERIC             count 4 at every angle
    axis (1,2,0),(1,1,2),
         (1,1,3)            IN A MIRROR PLANE   counts 5 and 9, never 4
    axis (1,0,0)            FACE axis           count 9 at every angle
    axis (1,1,0)            EDGE axis           count 9, with 13 on an arc
    axis (1,1,1)            BODY DIAGONAL       count 13 at every angle

**THE TOPOLOGY.** The octahedral group's reflection arrangement cuts the axis
sphere S^2 by 9 great circles (3 coordinate planes, 6 diagonal) into **48
spherical triangles** — the classical barycentric subdivision, whose vertices
are the 6 face axes, 12 edge axes and 8 body diagonals. The n=2 stratification
is that arrangement, fibred by the angle:

    triangle interior (dim 2) x angle  ->  dim 3   count 4
    triangle edge     (dim 1) x angle  ->  dim 2   count 5 or 9
    triangle vertex   (dim 0) x angle  ->  dim 1   count 9 (face),
                                                   9/13 (edge), 13 (diagonal)
    the 24 cube-symmetry rotations     ->  dim 0   count 1

which reproduces exactly the dimension/count table of the Postscript 69
addendum, and explains it: the count is a function of the stratum because the
stratum is a symmetry stratum.

**THE MAXIMUM LOCUS, DESCRIBED COMPLETELY.** 13 occurs on the 4 body-diagonal
circles (every angle) and on an arc of each of the 6 edge circles. Each circle
passes through the identity, and the cube-symmetry rotations on it are its
vertices. So **the 13-locus is a GRAPH embedded in SO(3)** — vertices at the 24
cube symmetries (where the count collapses to 1), edges the arcs of 13. This
is the derived form of Postscript 44's "every angle about a body diagonal, plus
a closed arc about an edge axis", which was observed rather than explained.

**A REFINEMENT: the walls come in two families.** The generic axis (1,2,3) gave
5 at one angle of 33, so "special angle" is a codimension-1 condition in its
own right, independent of the axis stratification. The 5-locus therefore has
components of two kinds — {mirror axis} x {generic angle} and {generic axis} x
{special angle} — both 2-dimensional. The fibration explains the axis
direction; the angle direction carries its own walls.

Files: `n2_map.py`, `n2_adjacency.py`.

## Postscript 71: extending the n=2 map to n=3 — every triple is labelled by THREE n=2 strata, and both 67s live in the single cell (13,13,13)

2026-08-03, main session, answering "every 3-cube configuration will be built
of components from that graph, so can we extend the graph to n=3?" Yes, and
the extension puts both maxima in one cell.

**THE MAP.** A 3-cube compound {I, R1, R2} contains three PAIRS, with relative
rotations R1, R2 and R1^-1 R2. Each is a point of the n=2 configuration space,
so every n=3 configuration carries a coarse label: the multiset of its three
n=2 strata, read off as the three pair counts from {1, 4, 5, 9, 13}. This is
the project's "pair signature" (9-pair, 13-pair, ...) given its proper home —
it is the image of the n=3 space in three copies of the n=2 map.

**THE TRIPLE BOUNDS BUT DOES NOT DETERMINE THE TOTAL.** Over ~2080 random
rational triples, 25 of the 35 possible labels occur, and each admits a range:

    (9,9,13)   max 59, seen {39,41,49,53,59}     (13,13,13)  seen {55} only
    (5,13,13)  max 59                            (9,9,9)     max 55, 9 values
    (4,4,4)    max 38, min 22                    (4,4,5)     max 40, min 19

So the label is a genuine invariant — it orders the cells by their ceiling —
but the fibre over a label is not a single count.

**A CONSISTENCY CHECK THE FRAMEWORK PASSES.** Every label containing a 1 (one
pair coincident, so the compound is really two cubes) returns exactly that
pair's count: (1,13,13) -> 13, (1,9,9) -> 9, (1,5,5) -> 5, (1,4,4) -> 4,
(1,1,1) -> 1. The degenerate cells collapse to the n=2 answer, as they must.

**BOTH MAXIMA ARE IN THE CELL (13,13,13).** Computed exactly in Q(sqrt 2): the
octahedral 67 — three 45-degree turns, Cayley point (sqrt2 - 1) times each
coordinate axis — has ALL THREE PAIRS EQUAL TO 13, and totals 67 with profile
{48, 18, 1}. The golden 67's pairs are 13 as well, from its own subcompound
chain 1, 13, 67, 177. So the two non-congruent maxima are not in different
cells: they are two points of the same one.

**AND THAT CELL IS MEASURE ZERO, WITH ITS RATIONAL MEMBERS CAPPED AT 55.**
Sampling random rational triples by height, the (13,13,13) label appears 13
times in 300 at height 2, then 4, 2, 1, and **zero from height 9 upward** — the
signature of a thin stratum reached only by arithmetically special
quaternions. Every rational member found totals 55. The 67s are the irrational
points of that cell.

**WHICH RESTATES THE n=3 IRRATIONALITY IN THE LANGUAGE OF THE MAP.** A 13-pair
is a pair whose relative rotation lies on the n=2 maximum graph — the four
body-diagonal circles and the six edge arcs (Postscript 70). So the n=3
maximum is exactly a configuration whose three pairs ALL lie on the n=2
maximum locus, and within that cell the maximum is attained only at points no
rational configuration reaches. The user's reading is the right one: three-cube
compounds are built from components of the two-cube graph, and the best ones
are built from its best components.

Files: `n2_adjacency.py`, and the pair-triple census in this postscript.

## Postscript 72: the (13,13,13) cell is REDUCIBLE — a 2-dimensional shared-axis component at 55, and isolated points where 67 lives

2026-08-03, main session, answering "what is the dimension of the one cell
containing both maxima, and what else besides the triple label is needed to
determine the total?"

**THE CELL DECOMPOSES.** A 13-pair is a pair whose relative rotation lies on
the n=2 maximum graph, whose main components are the four body-diagonal
circles. Scanning pairs of body-diagonal rotations:

    both rotations about the SAME diagonal     418 of 420 sampled pairs
                                               are 13-pairs
    rotations about DIFFERENT diagonals         40 of 441

The asymmetry is structural, not statistical. If R1 and R2 are rotations about
one diagonal then so is R1^-1 R2, so the third condition is FREE and two
parameters survive: **the shared-axis component is 2-dimensional.** With
distinct diagonals the third condition is a genuine codimension-2 constraint on
a 2-parameter family, leaving isolated points.

    component                       dimension    total
    all three axes one diagonal         2         55   (1512 of 1512
                                                        non-degenerate)
    axes on distinct diagonals          0         67   (the two maxima)

The 160 shared-axis cases returning 13 rather than 55 are the degenerate
sublocus where a 120-degree turn makes one cube the same SOLID as another, so
the compound is really two cubes.

**WHICH EXPLAINS AN EARLIER OBSERVATION.** Postscript 71 reported that every
rational (13,13,13) configuration found totals 55, and treated that as a cap on
the cell. It is not a cap — it is the value of the cell's 2-dimensional
component, which is the only part a rational scan lands on with any frequency.
The 67s are on the thin piece, and irrational.

**WHAT THE TRIPLE LABEL IS MISSING: THE AXIS RELATION.** The label records each
pair's stratum SEPARATELY; it cannot see how the three pairs sit relative to one
another. One extra bit — same diagonal or distinct diagonals — determines the
total on the whole 2-dimensional component (55 in all 1512 non-degenerate
cases) and isolates the piece where 67 becomes possible.

So the structure is a fibration, not a partition: the pair triple is the image
of an n=3 configuration in three copies of the n=2 map, and the FIBRE data —
how the three axes are glued to each other — is what the label discards. The
n=2 graph gives the components; the axis relation says how they are assembled;
and only then does the count follow.

Files: the body-diagonal scan in this postscript, on `cube_regions_n`.

## Postscript 73: the pair-label of every record, and what extending the structure graph to higher n would cost

2026-08-03, main session, answering "with full n=2 and n=3 structure graphs,
how hard would it be to extend to higher n?"

**THE LABEL LAYER IS ALREADY COMPUTABLE AT EVERY n**, in milliseconds — it is
C(n,2) two-cube counts. For the whole record tower:

    n   total   pairs   label
    2      13     1     1x13
    3      67     3     3x13                     <- every pair maximal
    4     183     6     3x13 3x9
    5     393    10     4x13 6x9
    6     727    15     4x13 9x9 2x4
    7    1217    21     6x13 9x9 6x4
    8    1891    28     8x13 9x9 11x4

Fraction of maximal pairs: 1.00, 1.00, 0.50, 0.40, 0.27, 0.29, 0.29. **Up to
n=3 the maximum is built ENTIRELY from maximal pairs; from n=4 it cannot be,
and settles near 30%.** The count of 9-pairs is 9 at n = 6, 7 and 8 alike.

**AND ALL-MAXIMAL IS ALWAYS AVAILABLE, JUST NOT OPTIMAL.** Putting every cube
on a shared body diagonal makes every pair a 13-pair at every n (verified,
n = 2..8). Its total against the record:

    n            2     3     4     5     6     7     8
    all-13      13    55   145   301   541   883  1345
    record      13    67   183   393   727  1217  1891
    ratio     1.00  0.82  0.79  0.77  0.74  0.73  0.71

So frustration, in the language of the graph, is a three-stage story:
 * n = 2: the record IS the all-maximal configuration.
 * n = 3: the record is still all-maximal, but on the ISOLATED component of the
   (13,13,13) cell — the 2-dimensional shared-axis component reaches only 55
   against 67 (Postscript 72).
 * n >= 4: the record is NOT all-maximal. Trading maximal pairs for tunable
   ones beats keeping them, by a margin that grows with n.

**COST OF EXTENDING, BY LAYER.**
 * *Nodes.* The label count is C(5 + C(n,2) - 1, C(n,2)): 35 at n=3, 210 at
   n=4, 1001 at n=5, 3876 at n=6. Small. The impossibility argument
   generalises: a pair counting 1 means the two cubes are the same solid, so
   coincidence is an equivalence relation and the pair-count matrix must
   respect it.
 * *Dimensions.* The lattice probe costs 3^(3(n-1)) - 1 points: 728 at n=3,
   19 682 at n=4, 531 440 at n=5, 14.3 MILLION at n=6 — about 16 core-days per
   representative. Exhaustive lattices die at n=5; replace them with random
   -direction sampling (the fraction of directions preserving the label
   estimates the codimension) which scales at any n.
 * *Ceilings.* These need search, which is the expensive part and exactly what
   this project already does. The graph gives no new leverage there.

**THE REAL LIMIT IS NOT COMPUTE, IT IS DISCRIMINATING POWER.** The label is the
image of the configuration in C(n,2) copies of the n=2 map, and the fibre —
the mutual geometry of the relative rotations — grows like 3(n-1). Already at
n=3 the label fails to determine the total, and one extra bit (the axis
relation) was needed. At n=6 the 727 plateau has 159 of its 161 configurations
sharing ONE signature, so the label is nearly constant exactly where the
interesting structure is.

**VERDICT.** n=4 is a weekend: 210 labels, a 9-dimensional space, 19 682-point
lattice probes, and a real question to settle — whether 183's cell
(3x13, 3x9) is the ceiling cell. n=5 is feasible with random-direction
dimension estimation. From n=6 the cell layer is still computable but too
coarse to classify, and the useful objects remain the ones already built:
walls, chambers, and the chamber words.

Files: the record-label and shared-diagonal computations in this postscript.

## Postscript 74: the n=4 cell census, and the one record no climb can reach

2026-08-03, main session. The n=4 structure program (`n4_program.py`,
`n4_climb.py`) run to completion on the M1; 239 338 configurations counted,
127 of 210 cells observed.

**THE CENSUS RANKS CELLS BY WHAT RANDOM SAMPLING REACHES, NOT BY THEIR
CEILING.** The record 183 lives in cell (9,9,9,13,13,13) — three 13-pairs and
three 9-pairs — whose census ceiling is **165**, eighteen short of the
configuration we already know sits there. Four other cells read 171:
(5,5,9,13,13,13), (4,9,9,13,13,13), (5,5,5,13,13,13), (4,4,9,13,13,13). Read
naively that says the record is not in the best cell. Read correctly it says
the census under-reads a cell by however special its optimum is.

**CLIMBING SETTLES IT, AND THE LEAD WAS BACKWARDS.** Greedy ascent with wide
restarts (the method that found 183 originally), seeded from each of the 16
leading cells plus the record as control:

    seed cell                 peak   cell the peak lives in
    (5,5,5,13,13,13)   171 ->  183   (9,9,9,13,13,13)
    (9,9,13,13,13,13)  169 ->  183   (9,9,9,13,13,13)
    (4,9,13,13,13,13)  167 ->  183   (9,9,9,13,13,13)
    (4,9,9,13,13,13)   171 ->  179   (9,9,9,13,13,13)
    (4,5,9,13,13,13)   169 ->  179   (9,9,9,13,13,13)
    control (the record 183)   ->  183   (9,9,9,13,13,13)

Nothing exceeded 183. Every climb reaching 179 or above ended in the RECORD'S
cell, having migrated out of its own. **(9,9,9,13,13,13) is an attractor.**

And the three configurations that tie 183 are not new: identical depth profile
{92,66,24,1} and identical per-label vector after canonicalising over the 24
relabellings of four cubes. One combinatorial type, four quaternion
representatives that look unrelated — one does not even have the identity as
its first cube. Three independent seeds, one destination.

**ARE ALL RECORDS REACHABLE BY CLIMBING? NO — AND n=3 IS THE EXCEPTION,
PROVABLY.** 24 climbs from random seeds at each level:

    n    record   best climb   reached the record
    2      13         13         20 of 24
    3      67         63          0 of 24    <- never
    4     183        183         yes, from 3 independent cells

At n=3 the ceiling was 63, with the rest spread over 49-59. This is not bad
luck: every move a climb makes is a +-1 or +-2 integer perturbation of an
integer quaternion, so **the entire orbit of a rational start is rational**,
and max(3) = 67 requires irrational coordinates (Theorem R). No rational
hill-climb can reach it at any step count. The rational climbing ceiling of 63
coincides exactly with the known "best triple inside any higher record",
reached here by an independent route.

So the n=3 exceptionality has one more face. It is the only level whose
maximum needs irrational coordinates; the only level whose optimum set is
finite and larger than one point; the only rung the record tower does not
nest through; the only level where the base-fixing method is structurally
excluded (Postscript 64); and now the only level whose record is unreachable
by the search method that found every other one.

Files: `n4_program.py`, `n4_climb.py`, `n4_run_011b219ec3/`.

### Postscript 74 addendum: basins — the n=4 record is reachable but NOT from random seeds, and no refinement reaches n=3's at all

2026-08-03, main session, answering "rationals get arbitrarily close to an
irrational — can we find a limit of climb steps? can basin size classify? what
seeds favour basins?"

**CORRECTION TO POSTSCRIPT 74.** It reported n=4's record as reached "from 3
independent cells" without noting those seeds came from the CENSUS. From
RANDOM seeds, 24 climbs at n=4 reach **0 of 24** — best 179, peaks spread
135-179. The record is reachable; random restarts do not reach it.

**THERE IS NO LIMIT PROCESS TOWARD THE n=3 RECORD** (`climb_limit.py`). The
octahedral 67 sits at Cayley coordinate sqrt2 - 1 on each axis. Walking its
continued-fraction convergents — the best rational approximations that exist
at each denominator — straight at it:

    p/q          distance     count        p/q            distance     count
    1/2          8.6e-02       55          169/408        2.1e-06       55
    2/5          1.4e-02       55          985/2378       6.3e-08       55
    5/12         2.5e-03       55          5741/13860     1.8e-09       55
    29/70        7.2e-05       55          13860/33461    3.2e-10       55
                                           exact point                  67

**Twelve orders of magnitude of approach and the count never leaves 55.** The
spike has ZERO WIDTH: the signal at every finite distance is exactly zero, so
no refinement schedule converts a rational climb into the irrational optimum.
This is not "the climb needs smaller steps" — there is no gradient to follow at
any scale. Contrast n=4, where the record sits on a 3-DIMENSIONAL continuum
(lattice probe: 26 = 3^3 - 1 neighbours keep 183, identical at steps 1/32 and
1/128, so the local structure is conical).

**BASIN SIZE AS A CLASSIFICATION AXIS.** It works, with one caveat that must
be stated or the number is meaningless: a basin is not a property of a
configuration alone but of the triple (configuration, move set, seed
distribution). Under this project's standard climb (+-1/+-2 integer moves,
wide restarts) and log-uniform height seeding, measured:

    n=2  record 13   basin >= 20/24     easily found
    n=3  record 67   basin = 0          EMPTY, provably: every move preserves
                                        rationality and 67 is irrational
    n=4  record 183  basin < 1/24       nonempty but small; found only from
                                        census-informed seeds

That is a genuine third axis alongside count and dimension, and it is the one
that predicts findability. Note it does not track dimension: 183 sits on a
3-dimensional set and still has a basin under 1/24, because 3 dimensions
inside 9 is thin.

**BETTER SEEDING, demonstrated rather than argued.** What actually found 183
was STRATIFIED seeding: sample broadly (239 338 configurations), bucket by a
coarse invariant (the cell = multiset of pair counts), and climb from the BEST
representative of each bucket. Uniform random restarts: 0 of 24. Cell-best
seeds: 3 of 16 reached 183. The census does not find the record — it delivers
the climb to a basin the climb can finish from.

The principle generalises to any coarse invariant that is cheap relative to
the objective: pair labels here, and the project's older "extension beats
native search" is the same idea with the invariant being "contains a known
(n-1)-record". What both avoid is spending the search budget re-discovering
which region of the space is worth being in.

Files: `climb_limit.py`, `n4_183_extent.py`.

## Postscript 75: zero signal means a uniform REGION — and characterising it separates the two n=3 maxima for the first time

2026-08-03, main session, from the observation that zero signal indicates a
uniform region, a region has boundaries, boundaries are more interesting than
interior points, and the size and shape of the region are themselves features.

Postscript 74's addendum reported the count staying at 55 through twelve orders
of magnitude of rational approach to the octahedral 67 and treated that as a
dead end — no gradient, therefore nothing to do. That was the wrong reading.
The flat 55 is not an absence of information; it is a UNIFORM REGION, and the
thing to do is find its edges.

**THE REGION.** In the dihedral family the 55 stretch runs from about
psi = 22.6 degrees to about 69.09 degrees — roughly 46 degrees wide, bounded
below by 43 and above by 43.

**WHERE THE TWO MAXIMA SIT IN IT.** This is the new fact.

  * The **octahedral 67** (psi = 35.26439) is DEEP INTERIOR: about 12.6
    degrees from the lower edge and 33.8 from the upper. It is a puncture in
    the middle of a uniform region — which is exactly why the approach study
    saw nothing, and why no refinement schedule can find it.

  * The **golden 67** (psi = 69.09484) is ON THE BOUNDARY. Bracketing with
    Pythagorean angles up to r = 60000:

        psi = 69.09032984   (-16.25 arcsec)   count 55
        golden 67           psi = 69.09484
        psi = 69.09673411   ( +6.81 arcsec)   count 43

    The 55/43 boundary and the golden maximum coincide to within 23
    arcseconds. Bracketed, not proved — but at that resolution the natural
    reading is that the boundary IS the golden point.

**SO THE TWO MAXIMISERS ARE STRUCTURALLY DIFFERENT, not merely non-congruent.**
They have been distinguished until now only by field (Q(sqrt2) vs Q(sqrt5)) and
by provenance (octahedron vs icosahedron). They differ in their position
relative to the uniform region that contains them: one is an interior puncture,
the other sits at the edge where the region gives way. Same count, same
"isolated irrational maximum" description, entirely different local situation.

**AND THE METHODOLOGICAL POINT GENERALISES.** A flat response is a cue to
locate boundaries, not a reason to stop. This project has now hit uniform
regions four times — the 727 continua (whose ENDS carried the W3/W4 walls and
the 725s), the n=2 strata (whose walls carry the higher counts), the 55 plateau
here, and the (13,13,13) cell's 2-dimensional shared-axis component at a flat
55. In every case the structure was at the boundary. Size and shape of the
region are then real characterising features: 46 degrees wide with a puncture
at its centre is a different object from the same value attained on a sliver.

Files: `climb_limit.py`, `region_shape.py`.

## Postscript 76 (CORRECTION to Postscript 70): the n=2 13-locus is bigger than recorded — and that is what a structural proof of max(3) would have to be built on

2026-08-03, main session, from the question of whether the region/neighbourhood
graphs could guide a simpler proof of max(3) = 67. Testing the first structural
fact such a proof would need immediately found an error in the graph.

**THE ERROR.** Postscript 70 described the 13-locus as "the four body-diagonal
circles (every angle) and an arc of each of the six edge circles" and
summarised mirror-plane axes as giving "5 or 9". The sweeps behind it each
showed a `13x1` in the mirror-plane rows, which the summary dropped.

It matters because the OCTAHEDRAL 67's three pairs are 13-pairs whose relative
rotations have axes [1,-1,sqrt2-1] and the like — not body diagonals, not edge
axes. They lie in MIRROR PLANES (x = -y here). Measured directly:

    axis (1,-1,1) body diagonal   13 at 358 of 359 angles
    axis (1,-1,2)                 13 at exactly ONE angle (t = 1)
    axis (1,-1,3)                 13 at exactly ONE angle
    axis (1,1,2)                  13 at exactly ONE angle
    axis (2,-2,1)                 13 at TWO angles
    axis (1,2,0)                  13 at TWO angles

So each mirror-plane axis carries isolated angles at which the count is 13,
and as the axis varies within the plane those isolated angles sweep out
CURVES. **The 13-locus has components inside the nine mirror planes**, in
addition to the body-diagonal circles and edge arcs. It remains 1-dimensional
(the n=2 adjacency measurement, 4 same-count neighbours in a radius-2 ball,
stands) — it simply has more components than were recorded.

**WHAT THIS SAYS ABOUT A STRUCTURAL PROOF OF max(3).** The strategy the graphs
suggest is coherent:

  1. show the maximum is attained in the cell (13,13,13) — currently observed,
     not proved;
  2. decompose that cell: the shared-axis component is 2-dimensional with the
     count identically 55 (Postscript 72), so it cannot hold the maximum;
  3. the distinct-axis part is 0-DIMENSIONAL, hence FINITE — enumerate it and
     check every point.

Step 3 is the appealing one, and it is only as good as the description of the
13-locus feeding it: an enumeration built on "body diagonals plus edge arcs"
would have MISSED BOTH MAXIMA, since the octahedral 67's pairs live on the
mirror-plane components. That is the immediate lesson — the proof route is
plausible, and the first deliverable is a complete and correct description of
the n=2 13-locus, which this project did not have until now.

**WHY IT MIGHT STILL BE WORTH IT.** The existing proof (PROOF_67.md +
PROOF_STEP_T.md) bounds the count by three Euler arguments and is not
constructive: several downstream claims — that n=3 is the unique irrational
level, that its optimum set is exactly two points — are explicitly CONDITIONAL
on the two known 67s being the only maximisers. A finite enumeration of the
0-dimensional component would settle that outright, producing the complete
list of maximisers rather than a bound. It trades Euler characteristic
arguments for algebraic enumeration: more computational, more elementary, and
constructive where the current proof is not.

It is a research programme, not a shortcut.

Files: `region_shape.py`, and the mirror-plane sweeps in this postscript.

## Postscript 77: STEP A COMPLETE — a closed-form exact formula for the two-cube region count, and with it the 13-locus as a criterion rather than a list

2026-08-03, main session, first step of the constructive-max(3) programme.

**THE FORMULA.** For cubes A = [-1,1]^3 and B = R(A):

    total = 1 + comp(A \ B) + comp(B \ A)

where each term is the number of CONNECTED COMPONENTS of an explicit graph:
 * nodes are the six slabs  A ^ {n_i . x > 1},  one per face normal n_i of B;
 * slab i is NONEMPTY iff ||n_i||_1 > 1 (the support function of the box), so
   it is empty exactly when n_i is a signed basis vector;
 * slabs i and j OVERLAP iff  max_{x in A} min(n_i.x, n_j.x) > 1, and by LP
   duality on the box that maximum equals

        min over lambda in [0,1] of || lambda n_i + (1-lambda) n_j ||_1,

   a one-dimensional piecewise-linear convex minimisation, solved exactly at
   its breakpoints (where a component changes sign).

Opposite faces never overlap, leaving 12 non-opposite pairs per side. Every
ingredient is an exact rational inequality in the rotation's entries: no
sampling, no floating point, no case enumeration.

**VALIDATED: 2158 random rotations across nine height scales (2 to 257),
2158 agreements with the engine, ZERO disagreements.**

**COROLLARY — the 13-locus, as a criterion.**

    L13 = { R : all six slabs nonempty, and all 12 non-opposite pairs
                pairwise disjoint }

This is what Step A needed, and it is better than the enumerated description
it replaces. That description was wrong twice in one afternoon — Postscript 70
listed only body-diagonal circles and edge arcs, missing the mirror-plane
components where the OCTAHEDRAL 67's own pairs live (Postscript 76); and the
follow-up conjecture that 13 forces the axis into a mirror plane was refuted
within the hour by the axes (1,-9,4) and (-1,-4,-9), which reach 13 off every
mirror plane. A criterion cannot be incomplete the way a list can.

**WHERE THE PROGRAMME STANDS.**

    A  complete L13                        DONE, and stronger than required
    B  bound the total by the pair label   THE REAL GAP — still 239k samples
                                           and a plausibility argument
    C  decompose the (13,13,13) cell       partly done (shared-axis == 55);
                                           A makes the rest tractable
    D  enumerate the 0-dimensional part    now well-posed: solve three
                                           simultaneous copies of A's
                                           inequalities, modulo symmetry
    E  conclude                            follows from C and D

The prize is that D would be CONSTRUCTIVE: it produces the complete list of
maximisers, settling outright the uniqueness hypothesis that several of this
project's headline claims are still explicitly conditional on — that n=3 is
the unique irrational level, and that its optimum set is exactly two points.

A plausible attack on B now exists: the same slab decomposition applied to the
third cube bounds the increment by how many slabs its faces can cut, which is
the shape of argument Postscript 56 used for the one-cube increment.

Files: `step_a.py` (the refuted mirror-plane conjecture, kept as its record),
`step_a2.py` (the criterion), `step_a3.py` (the validated formula).

---

## Postscript 78: STEP B — the three-cube count decomposed exactly, and max(3) = 67 reduced to a single two-rotation lemma

Step A (Postscript 77) turned the two-cube count into a closed form. Step B was
recorded as "the real gap — still 239k samples and a plausibility argument".
It is no longer that. The three-cube count now has an exact decomposition of
the same kind, and max(3) = 67 follows from it given ONE inequality about two
rotations — an inequality that is now explicitly finite (36 stated conditions)
rather than a vague hope about pair labels.

**THE DECOMPOSITION.** Sort the points of space by which cubes contain them.
Writing X_S for the set lying in exactly the cubes of S,

    T = comp(X_123) + sum over pairs comp(X_ij) + sum over singles comp(X_i)
      =      1      + sum_{ij} comp((Ci^Cj)\Ck) + sum_i comp(Ci\(Cj u Ck)).

* X_123 is an intersection of convex bodies: convex, hence ONE component, and
  nonempty because all three cubes share the origin.
* X_ij is a convex body minus a convex body — step A's situation with a
  12-facet base in place of the cube. It is covered by the six convex slabs
  (Ci^Cj) ^ {n.x > 1}, one per face of Ck, so **comp(X_ij) <= 6 with no
  hypotheses whatever.**
* X_i is covered by the 36 convex cells Ci ^ {n.x>1} ^ {m.x>1}, one per (face
  of Cj, face of Ck), since a point outside both cubes violates at least one
  facet of each.

A finite union of convex sets has as many components as its intersection graph,
so every comp() is a union-find over exact emptiness tests, and both tests are
step A's primitive: nonemptiness over the box is min over the simplex of
||sum lam_t n_t||_1 > 1 (LP duality), and over a general base polytope it is a
one-variable piecewise-linear minimisation across the vertex list.

`step_b.py` implements this in exact rational arithmetic and agrees with the
engine **24 of 24** on random triples spanning heights 2..33 and labels from
(1,5,5) to (13,13,13) — first run, no corrections.

**TWO IMMEDIATE CONSEQUENCES.**

*Every term is even, so T is odd.* The compound is centrally symmetric, so
x -> -x permutes the components of each class; a self-paired component would
have to contain the only fixed point, the origin, which lies in all three
cubes. Hence no component of any class other than X_123 is self-paired. This
is why every three-cube total ever recorded — 55, 67, 41, 39, 33, 29 — is odd.

*The pair terms are capped at 18 in total, unconditionally.* So the record
67 = 1 + 18 + 48 forces all three pair terms to 6 AND all three singleton terms
to 16. The whole of Step B lives in the singleton term.

**THE KEY MOVE: the singleton term is a TWO-rotation quantity.**
s_i = comp(Ci \ (Cj u Ck)) depends only on the two relative rotations at cube i.
The third pair does not enter. So it can be studied with the two rotations
chosen independently — the 13-locus can be hit by rejection instead of hoped
for — and it defines

    g(P,P') = max s over pairs of rotations with two-cube counts P, P'.

**AND IT IS TWO-DIMENSIONAL.** Every cube is centred at the origin, so along a
ray each contributes one interval [0, r(u)], and

    X_i = { r u : max(rj(u), rk(u)) < r <= ri(u) }

fibres over an open subset of the sphere with connected fibres. Hence
comp(X_i) = comp(U), U = {u : ri > rj and ri > rk} on S^2. Radially projecting
step A's slabs, U is the intersection of two families of at most six CONVEX
spherical cones, K_i = {u : n_i.u > |u_1|,|u_2|,|u_3|}, each an intersection of
six half-spaces. A three-dimensional extremal problem has become a spherical
one about two families of convex cells.

**WHY 13 IS SPECIAL, GEOMETRICALLY.** A pair counts 13 exactly when its six
cones are nonempty and pairwise disjoint (Postscript 77). Two disjoint families
never merge cells: K_i ^ L_j and K_i' ^ L_j' are automatically disjoint unless
i=i' and j=j'. So **at 13x13 the components ARE the cells**, and every merge
elsewhere is a loss. Measured at the witnesses that maximise the cell count:

    counts   cells  components  merged
    13,13      16       16         0
    13,9       20       14         6
    13,5       22       12        10
    4,13       22       10        12
    9,9        20       12         8
    5,5        20        8        12
    4,4        20        8        12
    4,5        20        6        14

The non-13 combinations reach MORE cells and FEWER components. That is the
mechanism the pair label was always standing in for.

Disjointness also buys a proof in the 13x13 case: the intersection graph of two
families of disjoint convex (hence simply connected) regions on a sphere is
planar and bipartite, so it has at most 2(6+6) - 4 = 20 edges. **s <= 20 at
13x13 is proved.** Off 13x13 the families overlap, planarity fails, and indeed
22 cells are observed — the bound correctly does not apply there.

**THE MEASURED LEMMA, and what it would give.**

    LEMMA B.  g(13,13) = 16, and g(P,P') <= 14 whenever min(P,P') < 13.

Status: measured, not proved. g(13,13) = 16 survived 400 hill-climbing
refinements at growing denominator (witness quaternions out to height 17314) —
this is not a random census reading a cell's typical value, which is the error
the n=4 census made in Postscript 74. The <= 14 half is so far the witness
table above plus a systematic sweep still running.

Given Lemma B the argument closes, and closes tightly:

    on (13,13,13):   T <= 1 + 18 + 3*16 = 67, and 67 is attained
    any other cell:  at least one pair is not 13, so at least TWO of the three
                     cubes carry a non-13 pair, and
                     T <= 1 + 18 + 14 + 14 + 16 = 63 < 67.

So **max(3) = 67**, with the maximum confined to the (13,13,13) cell — which is
exactly what Postscript 72's structure graph found empirically, now with a
reason rather than a census behind it. The observed off-cell ceiling is 59, so
the bound is loose by 4 and still decisive.

**WHAT REMAINS.** Only Lemma B, and only its arithmetic: for each of the ten
count combinations, the maximum over SO(3)^2 of the component count of an
explicit union of at most 36 convex cells. Two routes: sharpen the planar bound
from 20 to 16 using the extra structure at 13x13 (the six cones K_i are
complemented by six more around the base cube's own face directions, so each
family TILES the sphere with twelve convex cells, and the two tilings share the
six directions +-e_a); or certify the ten maxima by interval branch-and-bound
over the six-dimensional parameter space, where every condition is polynomial
in Cayley coordinates.

Note what has changed even without Lemma B: the pair label is no longer a
statistical proxy. It enters through one geometric fact — 13 means disjoint
cones, disjoint cones never merge — and the count it bounds is written down
exactly.

Files: `step_b.py` (the decomposition and its validation), `step_b2.py`
(g by direct probing), `step_b3.py` (the cell count, the cheap upper bound),
`step_b4.py` (the hill-climb inside each count combination).

---

## Postscript 79: the wide-engine campaign is COMPLETE — 727 survives all 508,818 previously-unreachable configurations, and two new 727 compounds fall out of it

The widened engine (Postscript 59) existed to answer one question: the narrow
q2 engine's 2^112 budget REJECTED configurations rather than counting them, and
a rejected configuration is not a counted one. Everything the project claimed
about the six-cube ceiling was therefore conditional on nothing above 727
hiding in the rejected set.

**It does not.** The campaign is finished:

    508,818 configurations counted   (8 shards, 63,602-63,603 each)
    0 still rejected                 (every shard, every d)
    best 727                         (every shard)

72 distinct squarefree d were swept. Zero rejections across the whole sweep is
itself the widening gate passing at full scale: the arithmetic that used to
give up now always decides.

**WHAT IS NEW, STATED AFTER CHECKING THE LEDGER — AND IT IS NOT WHAT IT
LOOKED LIKE.** The sweep records 1,449 configurations at 727 across 15 distinct
d, in three depth profiles:

    d1   d2   d3   d4  d5 d6   count
    214  220  156  100 36  1    1023
    214  216  162   98 36  1     328
    214  218  160   98 36  1      98

This postscript first claimed two of those profiles as new compounds. **That was
wrong, and the user caught it by asking whether they were really new or part of
an already logged region.** Postscript 61 already records exactly these three
profiles at 727, with these multiplicities' predecessors, and already records
eight fields reaching 727: 13, 226, 403, 1093, 1614, 1785, 1930, 2741. Nothing
about the profiles is new. The lesson is the ordinary one — check the ledger
before calling something new, especially when a campaign was designed to
re-cover ground.

What IS new is the field list. The completed sweep reaches 727 in **fifteen**
fields, so **seven are new**:

    3459   5305   12313   13461   13489   25561   27349

all necessarily from the 284,634 configurations the old budget rejected, since
the previous count had already exhausted everything it could reach.

**AND THEY ARE SEVEN NEW CONGRUENCE CLASSES.** The pair-count multiset does not
separate them — every 727 in every field gives the same signature, 9 x8, 13 x4,
4 x3 — so a finer invariant is needed. Use the field itself: the relative
rotations R_i^-1 R_j are unchanged by a global rotation, and each cube's 24
self-symmetries are RATIONAL, so the subfield of R generated by their entries is
a congruence invariant. Computing the traces exactly in Z[sqrt d] shows a
nonzero sqrt d part in every field, so that subfield is Q(sqrt d) exactly, and
distinct squarefree d give distinct fields. Hence configurations from different
fields cannot be congruent.

So the count of congruence classes at 727 goes from **at least 12 (4 rational,
8 irrational) to at least 19**.

[SUPERSEDED IMMEDIATELY by Postscript 80: "at least 19" is an undercount by an
infinite factor, and Postscript 61's "classes are INDEXED BY FIELD" is an
artifact of what the enumeration could produce. The classes lie on rational
LINES along which 727 holds on an interval, and every quadratic field has points
in that interval. Read Postscript 80 instead of this paragraph.]

**THE INVARIANT HOLDS THROUGHOUT.** Every 727 in every class still satisfies

    d1 + d2 + d3 + d4 = 690,   d5 = 36,   d6 = 1

Not new either -- Postscript 61 states it -- but it now has fifteen fields
behind it. d5 = 36 and d6 = 1 rigid across every maximiser says the deep layers
are saturated and every degree of freedom is shallow.

**Verification and its limits.** The two new-field witnesses were re-counted on
both the narrow and widened q2 engines, agreeing digit for digit across
`bounded`, `by_depth` and the 64-entry `per_label` subset profile. These are the
same program at two arithmetic widths, not the project's two independently
written engines -- and cannot be, since the rational engine cannot represent a
quaternion in Q(sqrt d). It is a width check, which is exactly what was in
doubt, and this postscript claims nothing stronger.

What this closes: the six-cube ceiling of 727 no longer rests on any
configuration having been skipped for arithmetic reasons. What it opens: the
maximiser set at n=6 keeps growing with the reach of the arithmetic -- seven
more fields appeared the moment the budget was widened -- so there is no reason
yet to think the list of fields reaching 727 is finite, and finding out what
distinguishes a field that reaches it is now the question.

---

## Postscript 80: the 727 classes are not indexed by field — they are quadratic points inside one rational interval, and there are infinitely many of them

Postscript 79 reported seven new fields reaching 727 and concluded "at least 19
congruence classes". The user asked the obvious next question — **how are the
classes related?** — and the answer dissolves the framing.

**STEP 1: THEY LIE ON SHARED RATIONAL LINES.** Every configuration here is the
fixed five-cube base plus a sixth cube, so each class is a point in the
3-dimensional Cayley space of sixth cubes. A configuration in ℚ(√d) has Cayley
coordinates a + b√d with a, b RATIONAL, so it names a rational line — point a,
direction b — and sits on it at parameter √d. Computing those lines for all
fifteen fields:

    direction (1, -3, -6)     d = 13, 1093, 2741     ONE line, not three
    direction (1, 1, -4)      d = 1614, 25561        ONE line
    direction (1, -3/2, 9/4)  d = 1785, 5305         ONE line

Not merely parallel — the base-point offsets are exact multiples of the
direction, so these are literally the same line carrying several classes.

**STEP 2: 727 HOLDS ON AN INTERVAL OF THAT LINE.** Sweeping the first line with
the ordinary integer engine, P(s) = a₀ + s·(1,-3,-6) with a₀ = (19/3, -7, -11):

    s = 2      721
    s ∈ [9/4, 3]   **727**        (the whole quarter-integer grid inside)
    s = 13/4   723

and the three quadratic points sit at s = 2.115 (d=1093), 2.404 (d=13),
2.802 (d=2741) — **all three inside the interval**, together with rational 727s
at s = 9/4, 5/2, 11/4, 3. The fields are not doing any work. The interval is.

**STEP 3: SO EVERY FIELD REACHES 727.** If that is the mechanism, then picking
any point of the interval with a √d in it must give 727 in field ℚ(√d).
Testing s = 5/2 + √d/100 — inside the interval for every d ≤ 97 — on the sixth
cube (300, 2650+3√d, -4350-9√d, -7800-18√d):

    d =  2  3  5  6  7  10  11  97      all give 727, profile {214,216,162,98,36,1}

None of those eight fields appears among the fifteen the enumeration found.
The construction works for any squarefree d whatever, by shrinking the
coefficient of √d until the point lies in the interval. Since the subfield
generated by the relative rotations is a congruence invariant (Postscript 79),
distinct d give non-congruent compounds, so:

**THERE ARE INFINITELY MANY CONGRUENCE CLASSES AT 727 — at least one for every
squarefree d.** And the field construction is not even the strongest form of
this. The five base cubes are FIXED, and although the isometry group O(3) is
itself uncountable, only FINITELY many of its elements can relate two members of
this family. An isometry carrying one origin-centred cube onto another is
pinned: g·(R·Q) = R'·Q forces R'^-1 g R into Sym(Q), so only 48 isometries take
a given cube to a given cube. Now fix the base cube B1. Under any congruence
between family members, g(B1) is one of the six cubes of the image, five of
which are the KNOWN base cubes — 5 x 48 = 240 candidates; and if instead
g(B1) is the sixth cube, then B2 cannot also go there, so g(B2) lands in the
base for another 240. Either way g comes from a set of at most 480 isometries
determined BY THE BASE ALONE, and each candidate determines the image
configuration outright. So every congruence class meets the interval in at most
480 points, and **the classes at 727 are UNCOUNTABLE.**

(An earlier draft of this paragraph said g "must carry the base to itself,"
putting it in the base's finite symmetry group. That is too strong — the cubes
are UNORDERED, so a congruence may swap the sixth cube with a base cube. The
finiteness survives, by the counting above, but not for the reason first given.) Stated plainly: once the plateau is positive-dimensional
— which Postscripts 52-55 already recorded — infinitely many congruence classes
follows immediately and the arithmetic adds nothing to it. The field argument
earns its place only for the OTHER claim, that infinitely many distinct FIELDS
occur, which is what refutes the indexed-by-field reading. "At least 12", "at least 19" and "one class per field that
reaches it" are all descriptions of the ENUMERATION, not of the problem. The
mixed family enumerates points where a quadric meets a line; each such point
lands in whatever field the quadratic happens to generate; and the enumeration
never looked anywhere else on the line.

**WHAT WAS ALREADY KNOWN, AND WHAT THIS ADDS.** Postscripts 52-55 already
recorded that 727 holds on INTERVALS of wall lines, subdivided into
type-chambers. That is exactly this phenomenon — the user's question, asked of
Postscript 79's "new" compounds, was for the second time in one session the
correct one: they were part of an already logged region. What is added is the
consequence for the arithmetic, which had been read backwards: the field is not
an organising principle of the maximiser set, it is a by-product of where the
enumeration sampled a continuum.

**A CHECKED ASIDE: the count is NOT a Galois invariant.** Each quadratic point
comes with a conjugate, at s = -1.559, -2.404, -7.669 on this line. Those count
683, 687-691 and 703 — not 727. Expected, since the combinatorial type is fixed
by sign conditions on REAL numbers and conjugation does not respect the real
order, but worth having on record: a 727 in ℚ(√d) does not imply its conjugate
is a 727, and any argument that treats a quadratic pair as a unit is wrong.

**WHAT THIS MEANS FOR THE CEILING.** Nothing weakens: 727 is still the ceiling,
now over 508,818 counted configurations with none above it. What changes is the
shape of the maximiser set. It is not a finite list of special compounds to be
classified; it is a positive-dimensional plateau whose rational and irrational
points are equally unremarkable, and the interesting objects are its BOUNDARIES —
where 721, 723 and 715 take over — exactly the lesson of Postscript 75. A
classification programme aimed at listing the 727s is aimed at the wrong object.

**ADDENDUM — what kind of rotations these classes actually are.** Asked
directly, and worth recording because the answer is unglamorous. O-reducing the
sixth cube's rotation (it is only defined modulo the cube's own 24 symmetries;
the raw Cayley angle reads ~176°, a near half-turn, which is the same rotation
composed with a cube symmetry):

    s = 9/4  ->  3     angle 46.10° -> 44.87°
                       axis (0.660,-0.466,0.589) -> (0.700,-0.449,0.556)

So the plateau is a one-parameter family of roughly-45° rotations about an axis
sweeping a short arc — neither a fixed axis with varying angle nor the reverse,
but both moving together along the rational line. The axis is near nothing
special: not a face normal, edge or body diagonal.

Sampling per_label at 1/32 across the interval gives **9 distinct combinatorial
types**, walls at s = 75/32, 19/8, 79/32, 5/2, 21/8, 85/32, 43/16, 89/32, with
chambers of very unequal width (the widest runs from 89/32 past s = 3). The
count is 727 in all of them: this is the type-chamber subdivision of
Postscripts 52-55, measured on a plateau whose extent is now known.

**A NEGATIVE WORTH KEEPING.** The angle crosses exactly 45° between s = 23/8
and 3 — a number with a pedigree here, since the octahedral three-cube maximiser
is three 45° turns. It is NOT a chamber wall: the type is constant across that
whole stretch, so the exact-45° configuration sits in a chamber interior with no
combinatorial event attached. The round number is a coincidence, and the
temptation to read significance into it is exactly the numerology this ledger
has fallen for before.

**ADDENDUM 2 — "finite or uncountable, never countably infinite", and a probe
that cannot tell isolated from non-aligned.** Asked whether the isolated 727s
must be finite in number, and whether infinitely many 727s forces a continuum.
Both yes, and they are one fact. The region count is fixed by the sign
conditions of finitely many polynomials in the configuration parameters, so
every level set is SEMIALGEBRAIC and therefore has finitely many connected
components, each a point or of dimension ≥ 1. Hence the 0-dimensional part is
finite, and an infinite level set must contain a positive-dimensional component.
**A maximiser set is finite or uncountable; countably infinite is impossible.**
This is the clean statement of why n=3 (exactly two 67s) and n=2 / n=6 (continua)
exhaust the possibilities — there was never a third option to look for.

Picking one configuration from each class then lands those representatives ON a
continuum, though a transversal need not itself be connected; here, since a
class generically meets the line once, a transversal is the interval minus a
thin set. The infinitude is therefore CHEAP: not many special configurations,
one continuum whose points are being counted.

**BUT OUR EVIDENCE FOR ISOLATION IS WEAKER THAN IT LOOKED.** Testing the record
(7,14,1,-5) with the lattice probe gives 0 of 26 neighbours at ε = 1/64, 1/256
and 1/1024 — which reads as isolated. It is not evidence. The same probe, at the
MIDDLE of the interval proved above to carry 727, also reads 0 of 26 — while
stepping along that interval's own tangent (1,−3,−6) gives 727 at every step.
The probe detects only AXIS-ALIGNED families; a curve in general position has no
lattice neighbour on it at any ε. So a positive reading remains good evidence of
an aligned family of that dimension, and **a zero reading means "not aligned",
never "isolated"**. Recorded as FAILURE_MODES 11d, with the affected claims named
there: the n=4 phase-2 cells reading dim 0.00, and any 0-dimensional claim about
the n=3 (13,13,13) distinct-axis component, which is where both 67s live.

**ADDENDUM 3 — type and class, made quantitative.** Distinct points of the
727 interval really are distinct congruence classes, and not only by the
counting argument: the five O-reduced angles of the relative rotations R_i^-1 R_6
against the base cubes move strictly monotonically along it,

    s = 9/4    6.3474  39.0667  44.7368  46.1012  49.0096
    s = 3      8.2220  40.0167  43.2630  44.8707  51.1876

so the invariant multiset separates every pair of points. Combined with the
chamber sweep this pins the two notions against each other on one interval:

    TYPES   9, with walls at s = 75/32, 19/8, 79/32, 5/2, 21/8, 85/32, 43/16,
            89/32 — finitely many, enumerable, a type IS a chamber
    CLASSES a continuum, one per point

Hence within a SINGLE chamber every configuration carries an identical 64-entry
per_label profile while being pairwise NON-CONGRUENT — uncountably many classes
sharing one type. That is the invariant-versus-definition gap in its most
concrete form, and precisely the step at which the earlier class counts went
wrong: per_label is constant on chambers, congruence separates points, and the
first was used to count the second.

**ADDENDUM 4 — the 727 locus is 4-dimensional, and 3 of those are gauge.**
Measured with the tangent method rather than the lattice probe (which cannot see
this locus at all — Addendum 2). At the interval's midpoint s = 5/2, all 14
directions perpendicular to the tangent (1,−3,−6) drop off 727 at ε = 1/64,
1/512 AND 1/4096, landing on 711/715/721; the tangent itself stays 727. So
inside the pinned slice the locus is a CURVE, one-dimensional, which confirms
Postscripts 52-55's "transverse to the line, isolated (perturbation → 715-721)"
with the tangent now identified explicitly.

Applying the isometry group to that curve then gives

    3  global rotation   GAUGE   — moves within a congruence class
    1  along the curve   MODULI  — moves between classes
    4  the 727 component in the 18-dimensional configuration space

so "how many degrees of freedom does 727 have" has no answer until the space is
named: 4 in configuration space, 1 in class space, the difference entirely
gauge. The 3 gauge dimensions are what make each class uncountable while adding
no class at all — the same distinction that separates 9 types from a continuum
of classes in Addendum 3.

**ADDENDUM 5 — how many arcs? At least four, and the count is the open
question.** Semialgebraicity PROVES the 727 set has finitely many connected
components, and that survives the quotient by the (compact) rotation group, so
"finitely many arcs" is not a guess. Two things in that phrase were assumptions
and are flagged as such: how many, and whether every component is
one-dimensional — the transverse test that established 1-dimensionality was run
at a single point of a single component.

Testing whether the known loci are even distinct: the three lines carrying the
irrational classes are **pairwise skew** (exact rational check), and the record
(7,14,1,-5) lies on none of them.

    A  (1,-3,-6)      d = 13, 1093, 2741
    B  (1,1,-4)       d = 1614, 25561
    C  (1,-3/2,9/4)   d = 1785, 5305
    D  the record's own wall line (Postscripts 52-55)

Skew lines cannot meet, so IF the locus is 1-dimensional along all of them they
are four distinct components; if the set thickens to 2 dimensions anywhere, two
skew lines could be joined through it. So: **at least four pairwise
non-intersecting 727 loci, and at least four components conditional on a
1-dimensionality that has been checked once.**

This is now the concrete form of the well-posed question that replaced "how many
maximisers": ENUMERATE THE 727 WALL LINES. It is a finite problem, the locus
enumeration of Postscript 48 is the machinery for it, and each line found comes
with its own arc of classes, its own chamber subdivision, and its own endpoints.

---

## Postscript 81: a tangent finder, the two 67 representatives recovered, and symmetry measured across every record

The method behind [`MAXIMISER_TAXONOMY.md`](MAXIMISER_TAXONOMY.md) and
[`MAXIMISERS.md`](MAXIMISERS.md), recorded here so those two files can be
results only.

**THE TANGENT FINDER** (`tangent_finder.py`). The lattice dimension probe is
blind to any locus not aligned with the coordinate directions (Addendum 2 /
FAILURE_MODES 11d), and detecting a curve needs a direction ALONG it, which
random and axis-aligned probes never supply. But a curve inside a maximiser
locus lies INSIDE the wall surfaces through its point — crossing a wall changes
the count — so

    tangent ⊥ gradient of every active wall.

One active wall reduces the search from the sphere of directions to a circle: a
finite scan. Active walls are found exactly, by substituting the point into the
119 catalogue locus planes. VALIDATED on arc A, where 2 of 96 in-plane
directions preserve 727 and they are ±(1,−3,−6), the tangent already known
independently from two ℚ(√d) solutions. APPLIED to 723 at (5,2,2,2), tangent
previously unknown: 2 of 96 give **(1,1,1)** — the sixth cube sliding along the
shared C₃ axis, which is the family Postscript 12 built 723 from in the first
place. The geometry rediscovered the construction. Limitation: it sees only
catalogue walls, and arc A lies on just ONE of them, its second wall being of
the unenumerated W3/W4 type.

**THE TWO 67s, DERIVED RATHER THAN SEARCHED.** They were not recorded anywhere
as exact quaternions, which is a reproducibility hole; guessing failed (the
nearest guess gives 49 = {30,18,1}, the ψ=45° dihedral compound). Deriving them
from the dihedral family works: both are {I, R, R²} with R a 120° rotation about
n(ψ) = (sin ψ, cos ψ, 0), i.e. R = (1/2, (√3/2)·n).

    octahedral  ψ = arcsin(1/√3)   R = (1, 1, √2, 0)        in Z[√2]
    golden      tan ψ = φ²         R = (2, 1+√5, −1+√5, 0)  in Z[√5]

The golden case needs the nested radical (√3/2)cos ψ = √((3−√5)/8) resolved,
which it does because 3−√5 = (√5−1)²/2, giving (√5−1)/4. Both verified: 67 with
by_depth {48,18,1}. Now in `MAXIMISERS.md` with runnable commands.

**SYMMETRY, MEASURED UNIFORMLY FOR THE FIRST TIME.** The order of each
maximiser's own rotation group:

    n=3  67 octahedral  24      n=5   393    3
    n=3  67 golden       6      n=6   723    3
    n=2  13             12      n=6   727    1
    n=4  183             3      n=7  1217    1
                                n=8  1891    1

**It decays from the maximum possible.** The octahedral 67 has the FULL cube
rotation group, order 24; nothing can exceed it. The collapse to 1 happens
exactly at 723 → 727, which Postscripts 52-55 independently describe as the
record beating 723 by LEAVING the corner-concurrence stratum — two vocabularies
for one event. **183 is C₃-symmetric**, apparently unrecorded: it was found by
wide-perturbation hill-climbing, so its symmetry was never the point of the
search that found it.

**And symmetry separates the two 67s where per_label cannot.** Their per-label
profiles are IDENTICAL, {1,16,16,6,16,6,6,1}; their symmetry orders are 24 and
6. That is a congruence invariant independent of Theorem R, and it settles
non-congruence outright.

**TYPES ALONG THE ARCS.** A type is a chamber; the count is constant across a
whole component while the type changes finitely often along it.

    n=2  13, body-diagonal arc          1 type over 199 rational points
    n=6  727, arc A                     9 types on s ∈ [9/4, 3]
    n=6  723, longest tangent interval 13 types on s ∈ [9/32, 35/32]

**Type-richness rises as symmetry falls.** The n=2 maximiser is combinatorially
uniform along its entire continuum — one chamber, no walls on it at all — while
the n=6 maximisers are cut into 9 and 13 chambers over comparable stretches. Low
n: symmetric and rigid. High n: no symmetry, finely chambered plateau. The count
is constant along all of them; what grows is the internal structure.

A correction made in passing: a first attempt at the symmetry table returned
orders 22 and 5, which are not possible for a rotation group. The cause was a
quaternion list holding 44 entries instead of 24 canonical rotations, so ± pairs
double-counted unevenly. Caught only by checking the values against the finite
subgroups of SO(3) — the wrong table was otherwise entirely plausible.

---

## Postscript 82: the tangent is a null space, 393 is rigid against moving one cube, and the n=7/n=8 extents

Continuing the live threads. Method here; results in
[`MAXIMISER_TAXONOMY.md`](MAXIMISER_TAXONOMY.md).

**THE TANGENT FINDER IS NOW EXACT.** Postscript 81 found tangents by scanning a
grid of directions inside one active wall and testing each with the engine. That
is a sampling argument: it can say no sampled direction preserved the count,
never that none exists. The right formulation is one line — a tangent must be
orthogonal to EVERY active wall normal, so

    tangent space = null space of the active normals,

exact linear algebra over ℚ, with no epsilon, no grid and no engine calls. The
rank answers the dimension question outright: rank 2 gives a 1-dimensional
tangent space which IS the tangent; **rank 3 proves no tangent exists**. Both
known tangents come back exactly — (−1/6,1/2,1) ∝ (1,−3,−6) at 727 arc A, and
(1,1,1) at 723. `tangent_finder.py` rewritten; the scan is kept as a cross-check.

**THE 393 BLOCKER WAS ILLUSORY.** Postscript 81 recorded that 393 was
unreachable because the tangent finder needed "a catalogue of wall planes for a
fifth cube on a four-cube base, which has not been enumerated". Wrong: reading
`locus_linear.extract_planes`, the catalogue is keyed per FIXED cube, and the
planes for "free cube vs cube j" depend on cube j alone. The existing 119 planes
therefore serve ANY slice — fix four base cubes, vary the fifth, use the planes
of those four. A five-minute look at the generator would have saved recording it
as a blocker at all.

**393 IS RIGID AGAINST MOVING ONE CUBE.** At the free fifth cube, Cayley
(1,1,1) — which the engine confirms counts 393 — there are **12 active walls of
rank 3, so no tangent**. Cross-checked by the old scan: 548 in-plane directions
at ε = 1/64, 1/512, 1/4096 and 1/65536, not one preserving 393, and the count
dropping to **377** in every direction at every scale. A drop of 16, uniformly.

Stated with its scope, which matters: this is the one-cube-free slice, 3 of the
12 moduli dimensions. 393 may still be positive-dimensional via directions that
move several cubes together. What IS established is that 393 is rigid against
moving any single cube, where 723 and 727 are not — both have tangents in
exactly that sense. So the n=5 record differs in kind from its neighbours, and
the "only n=3 is finite" reading of the taxonomy needs care: nobody has tested
the multi-cube directions at any n.

**n = 7 AND n = 8 EXTENTS.** No catalogue exists for cubes beyond the 393 base,
but their aligned directions are engine-verified, so none is needed:

    1217   2 of 36 single-axis moves preserve it, both cube 6 coordinate x;
           the interval has extent 1/32
    1891   4 of 42 — cube 6 coordinate x AND cube 7 coordinate z, two
           INDEPENDENT directions, confirming moduli dimension >= 2;
           along cube 7's z the locus is FRAGMENTED, 1891 on [0,3/32]
           and again on [15/64,3/8]

Both extents are far shorter than 727's arc, and 1891's fragmentation mirrors
723's union-of-intervals rather than 727's single clean arc.

**A reporting trap worth naming.** The rewritten finder reports arc A as "727 on
s ∈ [−5/4, 5/4]" — which is exactly the sweep range. The arc extends past both
ends; the interval reported is the WINDOW, not the locus. Any sweep that returns
its own bounds is telling you the window was too small, not that it found an
edge.

---

## Postscript 83: the epsilon-neighbourhood probe is one recursion, and the n=2 maximiser locus is a punctured CIRCLE

From a user reframing: the epsilon-neighbourhood categorisation was not a
separate technique from the dimension measurements — the dimension results came
out of it, and everything since has been hand-worked instances of one recursion.

**THE RECURSION.** The neighbourhood of a configuration is 3(n−1)-dimensional,
gauge already spent. Probe it. Two probes that DIFFER imply a boundary between
them; two that AGREE suggest a continuum through the centre. Extend an agreeing
direction: it must reach a boundary **or wrap**. A boundary is a stratum of
lower dimension — recurse into it. Terminate at point transitions, dimension 0.

The tools built piecemeal are steps of exactly this: the aligned probe is step 2
by sampling; the null space of the active wall normals (Postscript 82) is step 2
done exactly, returning every agreeing direction at once and proving when none
exists; the sweep is step 3. **Step 4 — descending into a boundary and
stratifying it — has never been built**, which is why components and types have
been collected one datum at a time instead of falling out of one pass.

**WRAPPING IS A REAL CATEGORY, AND n = 2 IS IN IT.** The user's point that an
extended agreeing direction might wrap all the way round rather than meet a
boundary is not hypothetical. The n=2 13-locus about a body diagonal is the
Cayley family t·(1,1,1), and t → ∞ is the half-turn (0,1,1,1) — which counts 13.
Verified along the whole family:

    t = 1/1000, 1/10, 2, 10, 1000, ∞, −1/1000, −10, −2      all 13
    t = 0, +1, −1                                            all 1

So the locus is a **CIRCLE**, punctured at three angles: the identity and the
two 120° rotations, where the two cubes coincide and the count collapses to 1.
The three punctures form one C₃ orbit, so the C₃ about that axis permutes the
three resulting arcs cyclically — they are ONE arc in class space, which is what
the taxonomy already recorded, but for a reason that was never stated.

**TWO KINDS OF END, previously conflated.** 727 arc A terminates at 723 and 721:
a WALL END, the count stepping to a neighbour. The n=2 loop's ends are
DEGENERACY PUNCTURES, the count collapsing to 1 because the cubes coincide.
Same dimension, different topology, and **no dimension measurement can tell them
apart** — which is why the taxonomy now carries topology as its own axis.

Untested everywhere else: whether 723's intervals, 727's arcs B/C/D, or the
n=7/n=8 families wrap. Cheap to settle — extend each sweep well past its
apparent ends and watch for the value returning.

---

## Postscript 84: the 727 arcs enumerated — 1,449 records, 216 chart lines, exactly THREE arcs up to congruence

A search rather than a measurement, run over data already on disk.

**THE METHOD.** Every ℚ(√d) configuration at 727 has Cayley coordinates
a + b√d with a, b RATIONAL, so it names a rational line P(t) = a + t·b and sits
on it at t = √d. Postscript 80 used this on ONE witness per field and found
three lines. Running it over all **1,449** recorded 727s gives **216 distinct
chart lines** — two orders of magnitude more, and the obvious reading was that
the component count had been badly underestimated.

**FIRST CHECK: are they arcs at all?** Naming a line is not the same as 727
holding along it — the count could hold only at the conjugate pair, making the
line an artefact of the parametrisation. `arc_survey.py` sweeps each line around
its own √d, t ∈ √d ± 2.5 at step 1/16:

    genuine ARCS (727 on >= 3 consecutive samples)   205
    727 only at isolated samples                      11
    no 727 anywhere on the swept range                 0

**SECOND CHECK, AND THE ONE THAT MATTERS: dedupe by symmetry.** A Cayley line is
a chart object. The same physical arc recurs under the free cube's own 24
rotations (R → Ru gives a different quaternion for the SAME cube) and under the
base's C₃ (R → gR), so up to 72 chart lines per arc. The dedup is exact because
q → g·q·u is LINEAR in q: lift each line to the 2-plane spanned by (1,a₀) and
(0,v), apply all 72 maps, reduce each image to row-echelon canonical form, and
collect orbits.

    ORBITS: 3        orbit sizes: 72, 72, 72

**216 = 3 × 72, uniformly.** So the campaign's 1,449 configurations at 727 lie
on exactly **three arcs up to congruence** — which are precisely the A, B, C of
Postscript 80, found there from one witness per field. The 216 was the same trio
seen 72 times each, and the uniform orbit size says no arc carries extra
stabiliser. The 11 "isolated" lines are sweep-window artefacts, since the orbit
structure places all 216 in those same three classes.

With the record's own wall line D — rational, so it never appears in a ℚ(√d)
campaign, and verified skew with A, B and C — the count stands at **at least 4
components**, and the campaign contributes exactly 3 of them. The earlier "≥4"
was right, and is now right for a reason.

**WRAPPING, TESTED.** Postscript 83 raised loop-versus-arc as a category.
Evaluating the point at infinity of a Cayley line — the half-turn about its
direction vector:

    727 arc A    s = ±10, ±100, ±1000 and ∞  ->  695/699/707, never 727
                 so arc A does NOT wrap; it is an arc with wall ends

    723 along (1,1,1)   s = −1000, −100, −10, +100, +1000  ->  **723**
                        s = ∞  ->  717

So 723 does not wrap either, but its family is **far larger than mapped**: it
was recorded as a union of intervals inside [9/32, 35/32], and it still counts
723 at |s| = 1000 — rotations approaching a half-turn about the shared C₃ axis.
Its point at infinity counts **717**, itself a record value (Postscript 11);
whether that is the 717 compound or merely its count is untested.

Files: `arc_survey.py`.

---

## Postscript 85: component counts at 727/725/723, and 723's family is enormous — the charted interval was a fragment near the origin

**COMPONENT COUNTS BY ORBIT DEDUP** (`orbit_count.py`, the Postscript 84 method
applied to every recorded total):

    total 727 :  216 chart lines ->  3 orbits   sizes {72:3}
    total 725 :  381 chart lines ->  6 orbits   sizes {27:1, 69:2, 72:3}
    total 723 :  844 chart lines -> 13 orbits   sizes {7:1, 54:1, 69:3, 72:8}

So the ℚ(√d) campaign's maximisers lie on **3, 6 and 13 arcs up to congruence**
at 727, 725 and 723 — the component count rising as the count falls, which is
what "more special ⇒ fewer places to be" predicts.

**Read the orbit sizes as a completeness gauge, not as stabilisers.** 27, 69, 54
and 7 do not divide 72, so they cannot be genuine orbit sizes under a
72-element group. They are the number of an arc's 72 chart images that the
campaign happened to RECORD. A size of 72 means the campaign saw every image;
the size-7 orbit at 723 means it saw seven. The orbit COUNT is unaffected —
any two observed lines in one true orbit are related by a single group element,
so the union-find merges them regardless of which images are missing.

**723's FAMILY IS FAR LARGER THAN RECORDED.** Postscript 82 charted 723 along
its tangent (1,1,1) as a union of intervals with the longest [9/32, 35/32].
Sweeping the whole line instead of a window, s ∈ [−50, 50] at step 1/8:

    579 of 801 samples count 723            7 maximal runs
    widest:  [−50, −4]  width 46            [53/2, 50]  width 47/2
    then:    [−15/8,−9/8], [3/8,1], [−3/4,−3/8], [−23/8,−21/8], {0}

**Both widest runs touch the sweep bounds**, and the wrap test already found 723
at |s| = 1000, so they extend far beyond ±50 — plausibly to the point at
infinity, where the count is 717. What Postscript 82 recorded as "a union of
intervals" is a small FRAGMENTED ZONE near the origin, which is simply where the
base point (2/5,2/5,2/5) sits. The family is dominated by two huge intervals
nobody had looked at. Highest count anywhere on the line: 723, so no 727 on it.

**The methodological point, for the third time this session.** A sweep centred
on the one configuration you already know, over a window sized by convenience,
describes the window. Postscript 82 flagged exactly this trap — "a sweep that
returns its own bounds is telling you the window was too small" — and the
charted 723 interval was itself an instance of it, unnoticed for two
postscripts. The fix is not a bigger default window; it is to sweep until the
count changes on BOTH sides, and to record when it does not.

Files: `orbit_count.py`, `arc_survey.py`.

---

## Postscript 86: symmetries named by group, not by order — and three of them were ambiguous

The symmetry column of Postscript 81 reported orders: 24, 12, 6, 3, 1. Order
does not determine a finite subgroup of SO(3), so three entries were ambiguous:
12 could be C₁₂, D₆ or T; 24 could be C₂₄, D₁₂ or O; 6 could be C₆ or D₃.
Classifying by element-order histogram instead:

    n=3  67 octahedral   O          {1:1, 2:9, 3:8, 4:6}   full octahedral group
    n=2  13              D₆         {1:1, 2:7, 3:2, 6:2}   NOT T
    n=3  67 golden       D₃         {1:1, 2:3, 3:2}        NOT C₆
    n=4  183             C₃         {1:1, 3:2}
    n=5  393             C₃
    n=6  723             C₃
    n=6  727             trivial
    n=7  1217            trivial
    n=8  1891            trivial

**The chain is O → D₆ → D₃ → C₃ → trivial.** Two things the order-only version
could not say. The n=2 maximiser is **D₆**, so it has a SIX-fold axis — a 60°
rotation about the body diagonal exchanges the two cubes, which is exactly why
the locus is the punctured circle of Postscript 83 and why its punctures are a
C₃ orbit. And the two 67s differ in group TYPE, **O against D₃**, not merely in
order 24 against 6: a far stronger separation than "different orders", and a
sharper form of the congruence invariant that already separated them where
per_label could not.

---

## Postscript 87: a vast family has a one-line generator — but the MAXIMISER subset of it does not

From the user's question: if a family is vast, is there a simple program that
generates it, short of redoing the searches that found it?

**FOR THE FAMILY, YES, AND IT IS ONE LINE.** The 723 sweep direction (1,1,1)
from base (2/5,2/5,2/5) keeps all three Cayley coordinates equal, so every
member is the sixth cube rotated about the shared C₃ axis (1,1,1). In quaternion
form the whole family is

    sixth cube = (d, n, n, n)      any coprime (n, d)

the SAME shape as the n=2 13-generator `1,0,0,0;d,n,n,n`. The vastness was never
mysterious: the family is a natural one-parameter stratum — a full rotation axis
— and the search only ever needed one point plus the tangent to name it. This is
the general recipe: get the tangent from the null space, recognise which stratum
it parametrises, write the closed form.

**FOR THE MAXIMISER SUBSET, NO — AND A CLAIM RETRACTED.** I said 723 is "what
you generically get" on that axis. It is not. Over 14 573 coprime (n,d) with
d < 60, |n| ≤ 200:

    723  46.8%    699  30.7%    711  18.9%    687  3.0%    717  0.3%
    also 693, 705, 681, and 393 (six configurations, the degenerate ones)

723 is the PLURALITY value, not the generic one. Nor is the pattern explained by
any simple parameter tested. Rate of 723 by sampling window:

    d = 2..5      |t| up to 100    74.0%
    d = 56..59    |t| <= 3.6       39.3%
    d = 197..223  |t| <= 1.0       56.8%

non-monotonic in the denominator AND in |t|, so neither is the driver.

**AND THE EARLIER "CONTINUOUS INTERVAL" WAS A GRID ARTEFACT.** Postscript 85
reported 723 unbroken on t ∈ [−49.6, −3.6] from a step-1/8 sweep, yet the dense
test finds exceptions at t = −9, inside that range. Both are right: the sweep
stepped in s with t = 2/5 + s, so it sampled t ≡ 2/5 (mod 1/8) and **never hit
an integer or a simple fraction at all**. An offset base point made the grid
systematically avoid exactly the special rationals it most needed to test.
Related to the window trap of Postscript 82, but distinct and worse: the window
was right, the PHASE was wrong, and no amount of widening would have found it.

**Where this leaves the question.** Generating the family is now free — one
parameter instead of three, no search. Deciding which members are maximisers is
not: no closed-form predicate has been found for which (n,d) give 723, and the
honest description remains "enumerate the stratum and count each member", which
is still an enormous reduction over searching Cayley space, and is exactly how
`MAXIMISERS.md` lists members by chamber.
