# Audit of RESULTS.md claim blocks, round 2

Read-only audit. No file other than this one was modified. Line numbers below
are current as of this pass (`RESULTS.md`, 419 lines; `LEDGER.md`, 9179 lines,
124 Postscripts). This round covers the ten items listed in the task (nine
claim blocks plus the Records table), continuing from `unsourced_audit.md`
(seven claims, one STALE).

---

## STALE findings (highest value, listed first)

## 8. "Irrational configurations are now countable at scale ... 224,184 irrational configurations have been counted: nothing above 727" (RESULTS.md lines 371–375)

**Verdict: STALE** — the 224,184 figure is Postscript 51 addendum 3's number;
Postscripts 59 and 79 complete the count to 508,818 (all of it), with zero
rejections, before RESULTS.md was last touched on this line.

- Source of 224,184: Postscript 51 addendum 3 (`LEDGER.md#p51`, "224 184
  irrational configurations counted, still nothing above 727"): "**FINAL
  COUNT.** 224 184 irrational configurations counted (up from 82 458), 284 634
  rejected as genuinely exceeding the traced bound." At that point 284,634
  configurations were still unreached, explicitly flagged as a gap: "Still
  uncounted: the 284 634 solutions whose (d, component) pair exceeds that
  budget."
- Postscript 59 (`LEDGER.md#p59`, "a 256-bit ℚ(√d) engine"): built
  `cube_regions_q2w.cpp` specifically to count "the 284 634 configurations the
  old budget REJECTED", widening the scalar from `__int128` to 256-bit.
- Postscript 79 (`LEDGER.md#p79`, "the wide-engine campaign is COMPLETE"):
  > "**It does not.** The campaign is finished: 508,818 configurations
  > counted (8 shards, 63,602–63,603 each), 0 still rejected (every shard,
  > every d), best 727 (every shard)."

  224,184 + 284,634 = 508,818 — the wide-engine campaign is exactly the
  completion of the count RESULTS.md still reports as partial. The
  conclusion ("nothing above 727") still holds and is in fact *stronger* now
  (EXHAUSTIVE over the whole mixed-degree-2 stratum admitted by the traced
  budget, not a 44%-covered sample) — but citing "224,184 ... counted" as the
  current state, with no mention that the campaign was later completed to
  508,818 with zero rejections, understates what is now known and reproduces
  exactly the round-1 pattern: a partial-search count stood in for a
  completed one.

## 9. "Nothing above 727 has been found at n = 6 by: ... 224,184 irrational configurations across the fields the overflow budget admits" (RESULTS.md lines 376–381)

**Verdict: STALE**, for the identical reason as claim 8 — same figure, same
fix (Postscripts 59, 79).

The rest of the list in this block is individually sourced and none of it is
contradicted:
- "random menus (100k sixth cubes)" — Postscript 46 (20,000-cube sweep) +
  Postscript 46 addendum (60,000 more, "on top of the original 20 000" = 80,000);
  20,000 + 80,000 = 100,000.
- "swap-completion from all six five-cube bases", "a balanced climb on the
  worst-subset objective", "core-and-clique construction from the 183 core" —
  all three, verbatim as methods, from Postscript 47 (`balance_hunt.py`,
  "balanced climb, objective (min 5-subset, total): no move at all",
  `clique_hunt.py`).
- "the exhausted three-wall family (2 733 configurations)" — Postscript 49:
  "2 733 distinct configurations after symmetry dedup and the height cap ...
  NOTHING ABOVE 727."
- "pure corner-wall triples (best 719)" — Postscript 50: "245 solved systems
  yielded only 55 real roots ... best count **719**."
- "the rational half of the mixed family (best 725)" — Postscript 50: "2 856
  distinct RATIONAL candidates -> max 725 (below 727)."

But the phrase "the fields the overflow budget admits" is itself the tell:
after Postscript 79 the budget admits *everything* (0 rejections at full
scale), so the qualifier and the 224,184 figure both describe an
intermediate state of the search, not its current, completed one. A 30-hour
independent search (Postscript 105, `hunt_v3`, 720,500 candidates) also found
nothing above 727 and is not in this list at all — consistent with, but not
cited in support of, the claim; worth adding since the list format
("nothing above X found by: ...") invites exactly this kind of staleness as
soon as a method not on the list is tried.

---

## NO EVIDENCE FOUND

## 4. "The frustration deficit is 6(n−3)(n−2) ... predicts max(6) = 729, max(7) = 1223, max(8) = 1907" (RESULTS.md lines 346–350)

**Verdict: NO EVIDENCE FOUND.**

Searched `LEDGER.md` for "frustration deficit", "6(n-3)(n-2)" (and the
"−" variant), "1223", "1907", and "three-point fit" / "3-point fit". None of
these appear as an established result:
- "frustration deficit" as a phrase: zero hits (the word "deficit" is used
  throughout the ledger for unrelated quantities — Postscript 20's
  "deficit-propagation envelope", Postscript 27/29's "gluing deficit",
  Postscript 106's parity "deficit" — never for "cap-sum minus true maximum").
- "6(n-3)(n-2)" or any equivalent product form: zero hits.
- "1907": zero hits anywhere in the ledger.
- "1223": one hit (line 314), in a table of *voxel-count* seed data from an
  early, later-retracted search method — unrelated to this claim; not a
  match.

The three anchor numbers RESULTS.md cites as "exact" (gaps 0, 12, 36 at
n=3,4,5) ARE independently traceable — Postscript 19/22/23 give the cap-sum
1+ΣC(l,n) and the gaps against the *then-current* records: "n=4:
1+24+66+104 = 195 vs 183 — gap 12 (frustration begins)" and "n=5: ... = 429
vs 393 — gap 36" (`LEDGER.md` line 1766-1767, Postscript 23). The formula
6(n−3)(n−2) does reproduce those two gaps and, applied to the *current*
n=6/7/8 cap-sums (801, 1343, 2087 from Postscript 19's closed form), gives
exactly 729/1223/1907. So the arithmetic is self-consistent with data that IS
in the ledger — but the formula itself, its name, and its n=6/7/8
predictions are not written down anywhere in `LEDGER.md`. This is either a
derivation original to RESULTS.md (in which case it should say so, not cite
nothing) or it exists in a file outside the ledger that was not checked here.
Note also that at the time gap-36-at-n=5 was recorded (Postscript 23), the
n=6 record was 723, giving an observed gap of 78, not 72 — the formula only
matches today's records (727/1217/1895, gaps 74/120/192... actually 801−727=74,
1343−1217=126, 2087−1895=192) *not exactly either*, so even granting the
formula as a genuine conjecture, RESULTS.md's own framing ("predicts
max(6)=729") is an upper conjecture that the actual record (727) falls two
short of — consistent with a conjectured ceiling, but worth flagging since
the block asserts the fit is "exact" only at n=3,4,5 and silently drops the
question of how well it does anywhere it's supposed to predict something not
already known.

---

## SUPPORTED

## 1. "Coincidence conditions are quadrics in the Cayley coordinates of the free cube, and a 9-pair locus is codimension 1 ... three walls meet in at most 8 points by Bézout" (RESULTS.md lines 278–280)

**Verdict: SUPPORTED** — Postscript 47 (quadrics) + Postscript 48 (codimension
1, Bézout).

- Postscript 47 (`LEDGER.md#p47`): "**ALL CONDITIONS ARE QUADRICS** (total
  degree 2 in (a,b,c); measured over cube 0's full set of 144)."
- Postscript 48 (`LEDGER.md#p48`, "the locus enumeration"): "So a 9-pair locus
  is **codimension 1**, three walls in the sixth cube's 3-DOF space form a
  DETERMINED system, and Bézout caps it at 2³ = 8 points. That is why records
  sit at three-wall intersections: it is forced, not coincidental."

Not contradicted later — Postscript 49's finding that edge-edge conditions
factor into two rational planes does not contradict "quadric" (a product of
two linear forms is still a degree-2 polynomial); it refines *which*
conditions factor, which is claim 2 below.

## 2. "Edge-edge conditions factor into PAIRS OF RATIONAL PLANES; corner-on-face conditions are IRREDUCIBLE QUADRICS ... 1 377 612 degree-2 solutions against 2 856 rational ones" (RESULTS.md lines 297–302)

**Verdict: SUPPORTED** — Postscript 49 (edge-edge) + Postscript 50
(corner-on-face + the 2,856 figure) + Postscript 51 addendum (the 1,377,612
figure).

- Postscript 49 (`LEDGER.md#p49`): "**EVERY COINCIDENCE CONDITION FACTORS
  INTO TWO RATIONAL LINEAR FORMS.** ... each edge-edge coplanarity condition
  is not an irreducible quadric but a PAIR OF PLANES."
- Postscript 50 (`LEDGER.md#p50`): "**CORNER-ON-FACE CONDITIONS ARE
  IRREDUCIBLE QUADRICS** — unlike edge-edge coplanarity, which factors into
  rational planes." Same postscript: "1 620 000 systems / **2 856** distinct
  RATIONAL candidates -> max 725 (below 727) / 688 806 degree-2 IRRATIONAL
  solutions."
- Postscript 51 addendum (`LEDGER.md#p51`): "Of the mixed strata's
  **1 377 612** degree-2 solutions, 1 112 028 lie in the 1 328 classes with
  d > 100."

Caveat, not a staleness finding: the 1,377,612 figure is from a later,
apparently widened recount than the 688,806-irrational figure first given in
Postscript 50 (roughly 2×); the ledger does not explain the discrepancy
directly, but both numbers are literally attested at the point RESULTS.md
uses them and neither is contradicted, so this is reported as a sourcing
note rather than a stale claim.

## 3. "d₃ ≤ 164, d₄ ≤ 102, d₅ ≤ 36 and the general ceiling law C(l,n) = (12l−6)n − 2(l²−1) for l ≥ 2. Never exceeded in ~1M configurations; proved only for l = 1" (RESULTS.md lines 334–336)

**Verdict: SUPPORTED** — Postscript 19 (the law and the n=6 attainment
table), reaffirmed at Postscript 22 with an out-of-sample test, never
proved beyond l=1 (Postscript 24/33) and never violated anywhere in the
ledger.

- Postscript 19 (`LEDGER.md#p19`, "THE GENERAL CEILING LAW"): gives
  `C(l,n) = (12l−6)·n − 2(l²−1)` and the n=6 attainment row `36=36 102=102
  164=164 222=222 234<276` — i.e. d₅≤C(1,6)=36, d₄≤C(2,6)=102, d₃≤C(3,6)=164,
  exactly RESULTS.md's numbers, "Never exceeded" matching "Every testable
  cell l ≤ 4: ATTAINED EXACTLY, ZERO violations."
- Postscript 22 (`LEDGER.md#p22`): "**Ceiling law at n=7: zero violations in
  112,864 exact records.**" — the out-of-sample test.
- "proved only for l=1": matches Postscript 24 (anchor lemma) / Postscript 33
  ("d_{n-1} <= 6n for all n unconditionally"); no later postscript proves
  l ≥ 2 or reports a violation anywhere (`grep -i "ceiling law\|C(l,n)"`
  across the whole ledger turns up only restatements and the one
  out-of-sample confirmation).

## 5. "Extension beats native search ... improvements propagate both directions ... searching n=8 has twice improved n=7 as a byproduct" (RESULTS.md lines 354–358)

**Verdict: SUPPORTED**, with one unverified detail flagged.

- Postscript 45 (`LEDGER.md#p45`): "Its seven-subsets, computed for free by
  the same job, contain **1211** — the n=7 record improved as a BYPRODUCT of
  searching n=8 ... Round trip: n=7 record → n=8 record → better n=7 → better
  n=8."
- Postscript 46 (`LEDGER.md#p46`): "A record at level n lifts every level
  above it within one extension pass, which makes n=6 the highest-leverage
  level in the tower."

Flagged detail: `grep -i "byproduct"` over the whole ledger returns exactly
**one** hit (Postscript 45, above). The "twice" in RESULTS.md most plausibly
traces to Postscript 46's own "**Propagation pattern, twice in one day**"
(two waves that day: Wave 1 = the byproduct case above; Wave 3 = 727 →
extend → 1217 → extend → 1891, which is direct extension, not a subset
byproduct). So the general claim is well supported, but "n=8 has *twice*
improved n=7 as a byproduct" specifically is not literally attested — the
ledger records one byproduct instance, not two.

## 6. "Menu shape matters more than menu size. 723 stood for weeks because every campaign sampled small quaternions; 727's sixth cube was found immediately by sampling component heights log-uniformly to 512" (RESULTS.md lines 359–362)

**Verdict: SUPPORTED** — Postscript 46.

> "**WHY IT WAS MISSED — the untried stratum.** Every n<=6 campaign in this
> project sampled small quaternions ... record_hunt.py therefore samples
> menus log-uniformly over component heights 4..512, and the very first such
> sweep of 20 000 sixth cubes on 393 turned up 727. The winning cube
> (7,14,1,-5) has ||q||^2 = 271, INSIDE the old tier-3 range ... So the gap
> was sampling density in a badly-shaped menu, not an unreachable region."

Not contradicted; Postscript 55 later gives an *additional*, non-conflicting
reason 723 stood ("723 stood for weeks" appears verbatim at `LEDGER.md` line
4565): the searches that followed Postscript 12's "records concentrate at
corner concurrences" heuristic were aimed at a stratum whose ceiling is 723,
not that 727 was unreachable. Both are true and both are in the ledger; they
are complementary causes, not a revision.

## 7. "Three-wall intersection is the best search method found ... ~30× the hit rate ... 134 784 linear systems giving 2 733 distinct configurations — EXHAUSTED in four minutes ... 1.3 million systems ... ~99% ... re-deriving identical plane triples" (RESULTS.md lines 363–370)

**Verdict: SUPPORTED (core)**, with one unsourced clause flagged.

- Postscript 48: "727 is reached 6 times per 500 trials — versus roughly one
  hit per 20 000 random sixth cubes, a **~30x hit rate**."
- Postscript 49: "the 144 walls per fixed cube collapse to 24 distinct
  planes ... the whole family is 10 cube-triples × 24³ = **134 784**
  systems ... `locus_linear.py`, ~4 minutes ... **2 733** distinct
  configurations after symmetry dedup ... NOTHING ABOVE 727 ... the Gröbner
  enumeration of Postscript 48 ground through **1.3 million** systems to
  sample part of that ... ~99% of its systems were re-deriving the same
  plane triples."

Flagged: the clause "found 727 compounds that eight prior campaigns missed"
does not appear anywhere in the ledger. `grep -i "eight"` across the whole
file turns up no match paired with "campaigns" or "prior"; the only "eight"
figures near this material are unrelated (Bézout's "eight plane choices",
"eight fields" from the irrational census). This looks like it may be a
miscount drawn from RESULTS.md's own adjacent list of eight search methods
(claim 9) rather than a ledger-sourced fact — recommend treating it as
uncited until traced.

---

## 10. Records table (RESULTS.md lines 40–49, n = 2..9: 13/67/183/393/727/1217/1895/2785) — cites nothing

Per-row findings:

| n | value | establishing Postscript | notes |
|---|---|---|---|
| 2 | 13 | pre-dates the ledger's Postscript numbering; **maximality** proved at Postscript 33 (`d_{n-1}<=6n` unconditional) | Not "found" by a search postscript — 13 is a baseline value already in play when Postscript 1 (unnumbered) opens. RESULTS.md's own theorem section (§3) already cites this correctly for the *proof*, not the value's origin. |
| 3 | 67 | pre-dates the ledger; **maximality** proved at Postscript 43 ("STEP T CLOSED — max(3)=67 proved") | Same situation as n=2. |
| 4 | 183 | Postscript 15 (`LEDGER.md#p15`, "n=4 — golden 177 is NOT the maximum; new rational record 183") | Not superseded. |
| 5 | 393 | Postscript 16 (`LEDGER.md#p16`, "records NEST"; the 723 record's 5-subset "counts **393**, verified by both") | Not superseded. |
| 6 | 727 | Postscript 46 (`LEDGER.md#p46`, "723 IS BEATEN — n=6 = 727") | Not superseded — still the current record throughout the rest of the ledger. |
| 7 | 1217 | Postscript 46 (same postscript, same day: "it lifts the tower to n=7 = 1217") | Not superseded (1211 and 1207 are its own predecessors, both explicitly noted as superseded in that same postscript: "was 1211 this morning, 1207 before"). |
| 8 | 1895 | Postscript 101 (`LEDGER.md#p101`, "n = 8 = 1895 — the record was inside a window an earlier sweep had already covered") | **Supersedes 1891** (Postscript 46), which superseded 1889 (Postscript 45), which superseded 1879 (Postscript 22). RESULTS.md's own prose immediately below the table already carries this citation ("1895 replaced 1891 on 2026-08-05 (Postscript 101)") — but the table row itself, like the rest of the table, carries no inline citation. This is the exact case the task asked to hunt for, and it is already caught in the surrounding text, just not in the table cell. |
| 9 | 2785 | **not found in `LEDGER.md` at all** | Exhaustive search for "2785", "335 600", "21 290", "ninth cube", "q(k)" and "k ≥ 55" (the specific figures RESULTS.md gives for how 2785 was found) returns **zero hits** for all of them except "2785" itself, which appears only in *later*, downstream usages (Postscripts 115/117/120/122 citing it as an already-established record) — never in an establishing search postscript. RESULTS.md's own text points to `MAXIMISER_TAXONOMY.md` and `METHODS.md §9` for this record, and both files do contain the relevant material (`MAXIMISER_TAXONOMY.md` line 254: "n = 9 — 2785, and it is a continuum running into a degeneracy"). So the record is not uncited in the strict sense — RESULTS.md names its source — but that source is outside the append-only ledger the rest of this table is implicitly checked against, which means the n=9 row cannot be given a Postscript citation the way n=4 through n=8 can. |

---

## Summary

| # | Claim | Verdict | Key Postscript(s) |
|---|-------|---------|--------------------|
| 8 | 224,184 irrational configs, nothing above 727 | **STALE** | P51 addendum 3 (source, partial) vs. P59 (256-bit engine built to finish it), P79 (508,818 counted, 0 rejected, complete) |
| 9 | "Nothing above 727 by: ... 224,184 irrational ... the budget admits" | **STALE** | same as #8 |
| 4 | Frustration deficit = 6(n−3)(n−2), predicts 729/1223/1907 | **NO EVIDENCE FOUND** | searched "frustration deficit", the formula, "1223", "1907" — no hits; anchor gaps (0/12/36) ARE in P19/P22/P23 but the formula and its n=6-8 predictions are not |
| 1 | Coincidence conditions are quadrics, 9-pair locus codim 1, Bézout ≤ 8 | SUPPORTED | P47 (quadrics), P48 (codim 1, Bézout) |
| 2 | Edge-edge = plane pairs, corner-on-face = irreducible quadrics, 1,377,612 / 2,856 | SUPPORTED | P49, P50, P51 addendum |
| 3 | d₃≤164, d₄≤102, d₅≤36, C(l,n) law, proved only l=1 | SUPPORTED | P19, P22 (out-of-sample), P24/P33 (l=1 proof) |
| 5 | Extension beats native search, propagates both ways, "twice" byproduct | SUPPORTED (core); "twice" not literally attested — only one byproduct instance in the ledger | P45, P46 |
| 6 | Menu shape > menu size; 723 stood for weeks; log-uniform heights found 727 | SUPPORTED | P46 (P55 adds a second, compatible reason) |
| 7 | Three-wall intersection best method; 30×; 134,784/2,733/4 min; Gröbner 1.3M/99% | SUPPORTED (core); "eight prior campaigns missed" clause unsourced | P48, P49 |
| 10 | Records table n=2..9 | see per-row table above | n=8 supersession already caught in RESULTS prose (not the table); **n=9 (2785) has no establishing Postscript in LEDGER.md at all** — sourced only outside the ledger, in MAXIMISER_TAXONOMY.md / METHODS.md §9 |

Two STALE findings (claims 8 and 9, same underlying cause): a partial-search
count (224,184, with 284,634 explicitly flagged as still-uncounted at the
time) was left standing in RESULTS.md after the ledger's own later
postscripts (59, 79) completed that exact search to 508,818 with zero
rejections — the same shape as round 1's finding, a count of an in-progress
search recorded as if final. One NO EVIDENCE FOUND (claim 4): a specific
formula and three specific numerical predictions with no trace anywhere in
`LEDGER.md`, despite being internally consistent with data that IS in the
ledger. And one structural gap in the Records table: the n=9 record (2785)
has no establishing Postscript in the ledger at all, unlike every other row,
though RESULTS.md does name an external source for it.
