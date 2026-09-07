# Session state — 2026-09-07

## Where the work stands

**The n=4 record is now a CONSTRUCTION, not just a configuration** ([P224], [P225]):
- 183 = hub cube + three cubes at t = ±1/4 about three of the four body diagonals.
  Eight such configurations, each with C3 symmetry about the UNUSED diagonal, pairwise
  26.35° / 43.00° apart — not one orbit.
- A NINTH 183 exists (the tower's n=4 layer, = the 393 minus its cube 3): asymmetric,
  symmetry group order 1, two cubes on no diagonal. Both routes extend to 393.

**Two exact pair rules, zero violations n=4..7:**
- 13-pair ⟺ relative rotation axis is a BODY DIAGONAL
- 9-pair ⟺ that axis lies in a COORDINATE PLANE

**393 = hub + one cube on each of the four body diagonals** — saturating, since a cube has
only four. Hence 727 must break the pattern, and does (first generic 4-pairs at n=6).

**Frustration curve** (P225): 9-pairs stay ~constant (6,9,9,9,10,10) while total pairs go
10→45; structured share falls 100%→50% by n=9. The supply of maximal pairs is bounded by
the CUBE's geometry, not by n.

## Corrections made (do not re-derive from the old claims)

- `concurrence.planes()` used matrix ROWS where face normals are COLUMNS — the inverse
  rotation. Every signature computed before 2026-09-06 was a property of the quaternion
  SPELLING. Fixed; `python3 concurrence.py` runs a permanent invariance gate (0 of 96).
- INVALIDATED by that: the signature census counts, Chao1 estimates, "the n=4 record has a
  9-fold concurrence" (it has 6), the corner-triple construction, and the Möbius-weight
  predictor (r = 0.562 → **−0.147**, orders 77.6% → **50.6%** of 3 320 pairs, i.e. chance).
- **PROPAGATED 2026-09-07 — the correction is now written OUT of the record, not only into
  it.** [P227] is the correction postscript; [FAILURE_MODES 27] is the transferable lesson;
  and the following were corrected IN PLACE, dated, with the void numbers struck rather
  than deleted: LEDGER P222 (now [PARTLY RETRACTED]) and P223, OPEN_QUESTIONS 21 (now
  CLOSED — void, not answered), MAXIMISER_TAXONOMY §12/§12a, METHODS §23/§23a,
  PROJECT.md, README.md, ALGEBRAIC_SEARCH.md, and the `signature.py` / `concurrence.py`
  docstrings. FAILURE_MODES had two entries numbered 20 and two numbered 21; the newer set
  is renumbered 22–26.
- SURVIVED the fix: that the signature underdetermines the count (8 of 166 pin it in one
  resample, 6 of 161 in a second; median spread 22 in both).
- **NOT survived, and I said it did:** "per-ensemble richness moves in both directions" was
  read off ONE resample. A second one moves `axis` and `twoaxis` the OTHER way. Only `chain`
  is resolved (roughly triples). Corrected in [P227] with both runs shown.
- The July baseline (`n4_search.py` phase D: ±1/±2 integer-component climb, radius-4
  certification, WIDE 1–6-component escapes) reaches **183 from Haar-random starts in
  30 899 evaluations**. The census spent 2.58M and never passed 177. Two days of climb
  machinery used an inferior move set that a July report had already outperformed.

## Added during the autonomous stretch (2026-09-06)

- [P226]: the tower is a five-cube CORE plus cubes hung off a hub. A hub of 13-degree
  4-6 persists at every n; the 9-degree sequence FREEZES at [4,4,4,3,3,0,...] from n=6,
  so exactly five cubes ever carry 9-pairs and later additions carry none.
- Census STOPPED at 3.13M configurations. Counts valid and kept; `sig` fields invalid
  until recomputed from the stored `cfg` (~2.5 h across shards, only if wanted).
- Four sweep designs were costed and three killed before running: 181M configs
  (five free angles), 62 h (no quotient), 18.6 h (C3 only). The live one applies BOTH
  exact reductions -- the diagonal's own C3 on the Cayley parameter
  t -> (t+1)/(1-3t), and S4 on the four body diagonals -- giving 66 045 tuples.

## Added 2026-09-07

- **AUDIT of the planes() bug — what else used this method.** `ALGEBRAIC_SEARCH.md`'s
  founding premise (723 has two 9-fold plane concurrences, and they are corner-sharing
  triples) was re-measured with the corrected normals and **SURVIVES**: 723's corrected
  signature is `((4,216),(6,6),(9,2))`. The derivation was geometric, not code-derived.
- **But 727 — the BETTER n=6 record — has max concurrence 6 and no 9-fold at all**
  (`((4,208),(6,10))`), as does the n=4 record 183 (`((4,90),(6,6))`) and the n=5 record 393
  (`((4,174),(6,8))`). The "9-fold sweet spot" is a property of 723 alone. PROJECT.md had
  silently transferred it to 727 when 727 superseded 723; corrected.
- **Positive control added** (the thing the whole signature line lacked): three cubes on a
  corner axis must show a 9-fold and four must show a 12-fold. Corrected code returns
  `((4,60),(9,2))` and `((4,114),(12,2))`. Three lines; it would have failed loudly on the
  broken map.
- `resig.py` written: the correction is now REPRODUCIBLE. It re-signs a seeded sample of
  the stored census under both maps on the same rows, so the two columns differ only in the
  line under test. The original numbers came from an inline run whose script was not kept.

- **[P228] — the n=5 record is UNIQUE in the four-diagonal family.** The 76 kept bases are
  **11 compounds**: exactly one reaches 393 (congruent to the tower's, verified
  constructively) and ten reach 387. `congruent.py` does it in 24n quaternion products, not
  n!·24^n, and its gate checks a self-match, a respelling AND two negatives.
- Caught before the run: the six "top" bases the extension sweep was about to process were
  six NAMES for one object. Extending them would have spent ~10 h of CPU answering one
  question once. The sweep now runs on the 11 class representatives.

## Latest (2026-09-06, late)

- n=5 family sweep, GATED (reproduces 393 or exits): best **393** at t=(-5,3,5,-5);
  **76 bases at >=385** in `n5family_keep.json`. An earlier ungated run said 375/none --
  VOID: my S4 "reduction" was wrong (the action is not free on the SIGNED structure;
  the 24 assignments of (-5,-3,5,5) give 341 AND 393). See FAILURE_MODES 26.
- Extension gate then fired correctly: a [-4,4]^4 menu cannot express (7,14,1,-5), which
  takes 393 -> 727. Menu widened to [-14,14]^4, which is **43 707** octahedral classes (not
  the ~29k first estimated).
- A THIRD gate failure followed, and it was the gate's fault: it tested menu membership
  with `in`. The menu is the octahedral QUOTIENT, so each class appears under one spelling
  chosen by a tie-break, and (7,14,1,-5) has four members at height 14 — the class was in
  the menu, the literal tuple was not. Membership now goes through `key()`.
- Measured 0.168 s per candidate at n=6, so 6 bases x 43 707 is ~12 h of CPU, not 2 h.
  `extend_n5.py` rewritten: gate counts ONE candidate and runs first (it was behind a
  two-hour pass), work is sharded 4 ways, and each (base, shard) checkpoints to
  `extend_n5_results/` so a kill costs only what is unfinished.
- **GATE PASSED 2026-09-07:** `393 + (1,-5,-7,-14)` (the menu's spelling of (7,14,1,-5))
  `-> 727`. That confirms the engine, the `--base` path, and that the octahedral respelling
  is the same physical cube, in one call.
- RUNNING: four shards, `extend_n5_s{0..3}.log`. Merge with `extend_n5.py --report`.

## Running / next

**Running now (2026-09-07):**
- `extend_n5.py` shards 0–3 → `extend_n5_s{0..3}.log`, checkpointing to
  `extend_n5_results/`. ~3 h wall. Merge any time with `python3 extend_n5.py --report`;
  partial merges are meaningful because every shard is a uniform stride through the menu.
- `resig.py 3000` → `resig_rerun.log`. Re-signs a seeded census sample under both maps.

**Next, in the order I would take them:**
1. The census's `sig` column is still void for 3 132 491 of 3 135 491 rows. `resig.py` does
   the work; it just needs to be pointed at all of them instead of a sample (~2.5 h across
   shards). Only worth it if any signature claim is going to be reused — the corrected
   3 000-row resample already says what happened to the ones that were.
2. Re-ask OPEN_QUESTIONS 21's replacement: is there ANY engine-free statistic that orders
   the count better than chance? All three tried were measured through the broken map, so
   all three are UNMEASURED, not refuted.
3. The 4-pair growth sequence (0, 2, 6, 11, 18) from [P225] — whether it is forced, and
   what it bounds.

**Standing:** do NOT write into `github/` — the publish tree is the user's alone.
