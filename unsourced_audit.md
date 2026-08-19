# Audit of seven uncited claim blocks in RESULTS.md

Read-only audit. No file other than this one was modified. Line numbers below
are current as of this pass (`RESULTS.md`, 403 lines; `LEDGER.md`, 9123 lines,
123 Postscripts).

---

## 1. "d_{n−1} ≤ 6n for every n" (RESULTS.md line 182, the l=1 ceiling law)

**Verdict: SUPPORTED** — Postscript 24 (anchor lemma / Theorem A) + Postscript 33
(unconditional proof).

- Postscript 24 (`LEDGER.md#p24`, "FIRST THEOREM — the anchor lemma is proven
  (all n)"): "**Theorem A (proven).** The radial envelope of any n-cube
  configuration has local minima only at the 6n face-center directions (value
  1 = the minimum)." At that point the exact upper bound `C(1,n) = 6n` was
  still open ("What remains for C(1,n) = 6n: only excluding 'parasite'
  cells").
- Postscript 33 (`LEDGER.md#p33`, "FIRST COMPLETE MAXIMUM THEOREM"): "**d_{n-1}
  <= 6n for all n unconditionally** — the l=1 ceiling law of Postscript
  [19](#p19), previously only empirical (~1M configs), now a theorem."

No later Postscript revises this — every other "6n" occurrence in the ledger
(lines 1362, 1398, 1469, 1553, 1583, 1592, 1805, 7956) either predates P33 or
restates the same theorem (e.g. line 7956, Postscript 123, still cites P24's
Theorem A approvingly).

---

## 2. "727 is isolated on the 393 base, and its coincidence pattern is unaugmentable" (RESULTS.md line 193)

**Verdict: SUPPORTED** — Postscript 47.

Postscript 47 (`LEDGER.md#p47`, "727 is PROVED isolated on the 393 base and
its coincidence pattern is unaugmentable..."), via `eliminate729.py`
(sympy, exact ℚ):

> "GATE 36 conditions vanish at the known 727 cube ... Q1 their Gröbner basis
> has 3 elements and IS ZERO-DIMENSIONAL ... Q1b exactly ONE real solution
> point — the 727 cube itself ... Q2 684 infeasible augmentations, 0
> feasible."
>
> "So on the 393 base: **727 is isolated** ... and **its coincidence pattern
> is unaugmentable** — no sixth cube realises those 36 conditions plus any
> 37th, each certified by a Gröbner basis of {1}."

The RESULTS.md caveat ("the Cayley chart used omits the 180° rotations") is
also verbatim from P47: "the Cayley chart omits the 180° rotations (w = 0),
which need a separate chart." No later Postscript contradicts this; Postscript
113 (line 8417) still cites it approvingly: "[Postscript 47] proved 727
isolated on the 393 base, while arc A lies on an arc" — treated as
established fact, not revised.

---

## 3. "The maximum at n=3 requires irrational coordinates" — rest of the block (RESULTS.md lines 202–212)

**Verdict: SUPPORTED (for the un-annotated part)**, existing annotation for
the "only two maximizers" clause stands.

RESULTS.md already carries a 2026-08-17 annotation citing Postscript 118 for
the "conditional on the two known maximizers being the only ones" clause. But
the block's own **factual core** — "The O-reduced invariant μ is rational for
any rational configuration, and equals ½+√2 and 3φ/2 at the two maximizers" —
was itself uncited. It traces to:

- Postscript 26 (`LEDGER.md#p26`, original statement): "**Theorem R (rational
  obstruction)**: rational configurations have rational O-reduced pair
  invariants; the 67s' invariants are 1/2+sqrt2 and 3phi/2 — so no rational
  config is congruent to either. **Corollary**: conditional on the two known
  67s being the only n=3 maximizers, the n=3 maximum REQUIRES irrational
  coordinates."
- Reaffirmed unchanged at Postscript 44 (`#p44`, μ = 1/2+√2 octahedral vs
  3φ/2 golden, citing `C45_notes §12`), Postscript 52 (`#p52`, "At n=3 it
  provably is — no rational configuration attains 67 (Theorem R)"), and
  Postscript 64 (`#p64`, restates the same two irrational values).

No Postscript revises Theorem R itself or the μ values. Only the *scope*
claim ("the only ones") was ever weakened, and RESULTS.md's own annotation
already covers that. Recommend RESULTS.md also cite Postscript 26 (origin of
Theorem R) for the μ sentence, since the current annotation cites only P118.

---

## 4. "The record tower nests at every level except n=3" (RESULTS.md line 225)

**Verdict: SUPPORTED**, and stronger than when first found — Postscript 44
then made exhaustive by Postscript 111 using the CURRENT record values.

- Postscript 44 (`#p44`, "the n=3 anomaly audit..."), part (b): "**NESTING —
  the record tower nests at every adjacent level except n=3.**" ... "13 ⊂
  183 ⊂ 393 ⊂ 723 ... The best triple anywhere in the tower is 63 — four
  short of 67. n=3 is the sole break." (Uses the then-current records 723/
  1207, since superseded by 727/1217/1895/2785.)
- Postscript 111 (`#p111`, "every subset of every record, counted"), the
  exhaustive re-check on the CURRENT records: "**NESTING FAILS AT k = 3, AND
  ONLY AT k = 3, UNIFORMLY.** For every record from n=4 to n=9 and every
  subset size k, the maximum k-subset equals the level-k record — 13, 183,
  393, 727, 1217, 1895 — with the single exception k = 3, where the best
  triple is 63 against max(3) = 67, in every one of the six records."

Not stale: P111 re-derives the same conclusion against the up-to-date record
tower (727 not 723, 1217 not 1207, 1895 not 1889), so the claim survives the
record updates that would otherwise have made P44's version stale.

---

## 5. "727 is usually reached without a maximal pair, but not always" (RESULTS.md line 228)

**Verdict: SUPPORTED** — Postscript 55 addendum.

Postscript 55 addendum (`LEDGER.md#p55`, "the ways of reaching 727 — the
discovered record is a 1-in-161 outlier, and one route carries a 13-pair"):

> "(9, 9, 4, 4, 4)   159 configurations
> (9, 9, 9, 4, 4)     1   <- the originally discovered record (7,14,1,-5)
> (13, 5, 4, 4, 4)    1   <- reaches 727 WITH a maximal pair"
>
> "159 of 161 reach 727 with only TWO 9-pairs, and one reaches it carrying a
> 13-pair — the rigid maximal pair the frustration story says optima avoid."

This matches RESULTS.md's numbers and its "atypical of its own plateau"
language exactly. No later Postscript revises this specific 159/1/1 split
(the pair-signature invariant discussed later, at Postscript 79/80, is a
different invariant — the full 15-pair multiset of the whole compound, not
the free-cube-vs-base signature — and does not touch this count).

Cross-reference for the reader: this 159/1/1 breakdown is computed over the
same 161-configuration census that claim 6 below relies on, and that census
is now known (Postscript 80) to cover only a finite sample of what is
actually an infinite/uncountable plateau. The breakdown itself is not
contradicted, but it should not be read as covering "the" full 727 plateau.

---

## 6. "727 is a plateau of at least 161 non-congruent compounds in 54 combinatorial types" (RESULTS.md line 235)

**Verdict: STALE** — Postscript 52 addendum 5/6 established the 161/54
figures; Postscripts 79 and 80 supersede the completeness implied by the rest
of the block (the eight-field list and the implicit finiteness of the
classification).

Source of the "161 configurations, 54 types" figure:

- Postscript 52 addendum 6 (`LEDGER.md#p52`, "a taxonomy of the 727 plateau"):
  "417 configurations, 109 types -> 161 configurations, 54 types" (after
  correcting for the base's own C₃ symmetry).

The RESULTS.md block also asserts "Eight of the fields reached are
irrational ... VERIFIED" — but this is contradicted by two later Postscripts:

- Postscript 79 (`LEDGER.md#p79`, "the wide-engine campaign is COMPLETE"):
  found the fifteenth field and seven new ones beyond the original eight:
  "What IS new is the field list. The completed sweep reaches 727 in
  **fifteen** fields, so **seven are new**: 3459 5305 12313 13461 13489
  25561 27349."
- Postscript 80 (`LEDGER.md#p80`, "the 727 classes are not indexed by field
  ... there are infinitely many of them"), which goes further and dissolves
  the entire finite-classification framing:

  > "**THERE ARE INFINITELY MANY CONGRUENCE CLASSES AT 727 — at least one for
  > every squarefree d.**" ... "the classes at 727 are **UNCOUNTABLE**."

  And explicitly, about the very same lower-bound language RESULTS.md still
  uses: "'At least 12', 'at least 19' and 'one class per field that reaches
  it' are all descriptions of the ENUMERATION, not of the problem."

  Also directly on the framing RESULTS.md uses ("a plateau of ... N
  compounds in M types"): "**What changes is the shape of the maximiser
  set.** It is not a finite list of special compounds to be classified; it
  is a positive-dimensional plateau whose rational and irrational points are
  equally unremarkable ... A classification programme aimed at listing the
  727s is aimed at the wrong object."

So: the "at least 161 ... 54 types" wording is not technically false (161 ≤
∞), but the surrounding sentence ("Eight of the fields reached are
irrational") is a stale, superseded count — it was already out of date by
Postscript 79 (fifteen fields known) before Postscript 80 proved the true
count is infinite. RESULTS.md presents this block as a settled census
("VERIFIED") when the ledger's own later verdict is that no finite census of
this plateau is the right object to report.

---

## 7. "The irrational classes are the first configurations this project found by SEARCH rather than by symmetry" (RESULTS.md line 259)

**Verdict: SUPPORTED** — Postscript 51.

Postscript 51 (`LEDGER.md#p51`, "a ℚ(√d) C++ engine, 82 458 irrational
configurations counted..."):

> "Two-engine verified ... So 727 has at least FIVE congruence classes, one
> of them irrational — and this is **the first irrational configuration this
> project has found by SEARCH; the two n=3 maximizers came from symmetry**."

This is a near-verbatim match to the RESULTS.md sentence, including the
octahedron/icosahedron framing elsewhere in the ledger for the two n=3
maximizers (Postscript 44/64: μ = 1/2+√2 "octahedral" vs 3φ/2 "golden"/
icosahedral; Postscript 84 area line 5988: "by provenance (octahedron vs
icosahedron)"). Not contradicted later — Postscript 80's finding of
infinitely many further irrational classes (also found by search, via the
line-interval construction) is consistent with, not contrary to, "the first
... found by search."

---

## Summary

| # | Claim | Verdict | Key Postscript(s) |
|---|-------|---------|--------------------|
| 1 | d_{n−1} ≤ 6n | SUPPORTED | P24 (anchor lemma), P33 (unconditional proof) |
| 2 | 727 isolated on 393 base, unaugmentable | SUPPORTED | P47 |
| 3 | n=3 requires irrational coords (rest of block) | SUPPORTED | P26 (Theorem R, origin — currently uncited), P44, P64 |
| 4 | Record tower nests except n=3 | SUPPORTED | P44 (original), P111 (exhaustive, current records) |
| 5 | 727 usually without maximal pair | SUPPORTED | P55 addendum |
| 6 | 727: ≥161 compounds, 54 types, eight fields | **STALE** | P52 addendum 5/6 (source) vs. P79 (15 fields), P80 (infinitely many/uncountable classes) |
| 7 | Irrational classes first found by search | SUPPORTED | P51 |

One STALE finding (claim 6): the "eight irrational fields" / implied-finite
"54 combinatorial types" framing is superseded by Postscript 79 (fifteen
fields) and, more fundamentally, Postscript 80's proof that the 727 plateau
carries an uncountable number of congruence classes across infinitely many
fields — the ledger's own verdict is that "a classification programme aimed
at listing the 727s is aimed at the wrong object." Claim 3's block, while
supportable, still omits a citation for its factual core (Theorem R / the μ
values) even after the 2026-08-17 annotation, which cites only Postscript 118
for the narrower "only two maximizers" question.
