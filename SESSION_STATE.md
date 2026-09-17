# Session state — 2026-09-16

**Read [RESULTS.md](RESULTS.md) §4's scope correction first, then this. Several claims made
EARLIER IN THIS SAME SESSION were later refuted; the corrections are propagated, but read the
refutation column below before quoting anything from P304–P321.**

## The single most important thing

**A cube's boundary is six SQUARES, not six planes.** `concurrency_walls.py` originally tested
only that four face planes meet, never that the meeting point is on the cubes. Most such points
are far outside the compound and are not walls of anything. This invalidated the mechanism of
[P304](LEDGER.md#p304) and several results built on it ([P322](LEDGER.md#p322),
[P323](LEDGER.md#p323)). **Fixed** — the family now carries `common_point_inside_cubes` per
root, and running the fix showed that even P304's own founding example, the `t = −2/9` wall,
is outside.

## What stands

| | |
|---|---|
| [P307](LEDGER.md#p307) | plateau dimensions **1, 2, 2** at n = 6, 7, 8 — equalities |
| [P308](LEDGER.md#p308) | boundary attributions audited and cleared; [P296], [P301]–[P303] stand |
| [P311](LEDGER.md#p311) | **the facet-centre lemma** — proved; depth is radially monotone on every facet ([METHODS 26](METHODS.md#26-the-facet-centre-lemma)) |
| [P312](LEDGER.md#p312) | `c_ell` is the WALL graph's, 43/43 against the engine |
| [P315](LEDGER.md#p315) | vertex taxonomy; **12 quadruple points in every record above n = 4**, forced by a shared body-diagonal axis |
| [P319](LEDGER.md#p319) | `c > 1` occurs **only at level 1** — 0 in 3382 deeper instances |
| [P321](LEDGER.md#p321) | a `c`-transition is a **pure reconnection**: `dV = dE = 0`, 8 of 8 |
| [P326](LEDGER.md#p326) | `holes <= 1` completes the bound for every n but barely tightens it |
| [P327](LEDGER.md#p327) | the frustration mechanism: every region is paid for by degree excess, and **every triple point is spent twice** |
| [P328](LEDGER.md#p328) | taxonomy completed; records buy **13–28 % of their regions with degeneracy** |
| [P330](LEDGER.md#p330) | `EE <= 6` per pair FALSE (max 10, at a FACE diagonal) — and **`sum EE <= 6*C(n,2)` is FALSE too**, at every n from 2 to 6 |

## What was refuted, by me, in this session

    P304's mechanism        four-plane concurrency does NOT explain the count drops   [P323]
    P309's +258 / 282       counted without containment                               [P323]
    P318's cost split       (b-1)(b-2) does not apply to CORNER concurrences           [P324]
    P321's concurrency      every concurrency wall at a c-transition is spurious       [P321 add.]
    EE <= 6 per pair        TRUE at q = (0,1,1,1); 18 of P329's 24 were corner incidences [P330]
    sum EE <= 6*C(n,2)      exceeded at every n from 2 to 6, and at a PROVED n = 2 maximiser [P330]
    P328's excess table     generic values, not invariants of the signature             [P330]

**The pattern, and it is long-standing, not mine alone ([METHODS 27](METHODS.md#27-a-cause-claim-needs-its-own-gate)):**
every CAUSE claim made this session fell; every MEASUREMENT stood. Across the whole ledger,
~40 of ~303 titles carry refutation language and about two thirds of those refute a cause, law
or mechanism. A sentence with *because* in it needs its own gate, and the gate must not share
the claim's model.

## Where to go next

**[OQ 37](OPEN_QUESTIONS.md#37) — prove `T3 + two-body <= 176` at n = 4, and `max(4) = 183`
follows.** [OQ 35]'s premise was retired by [P333](LEDGER.md#p333) and [OQ 36] was SOLVED by
[P334](LEDGER.md#p334), in that order, today.

**The chain.** [OQ 35] asked what bounds the degenerate terms, "which nothing bounds". They are
bounded: `EE + 2*SC2` **is** the two-body term and `two-body <= 10*C(n,2)` is proved ([P237]) —
gated by [P258]'s identity closing on the record as `128 + 48 + 6 + 1 = 183`. So the question
was never a missing bound; it is whether two proved caps can hold at once.

**They cannot, and both endpoints are now known exactly:**

    configuration        T3         two-body     T3 + two-body    count
    n = 4 RECORD      128 / 128     48 / 60          176           183
    K4 compound        74 / 128     60 / 60          134       138 + holes
    body-diagonal      72 / 128     36 / 60          108           145
    assumed by bound  128 / 128     60 / 60          188           198

[P334] built the middle row by SOLVING rather than searching: two cubes share a corner iff they
share a body diagonal, a cube's four diagonals are a regular tetrahedron, so K4 corner-sharing
is an axis-labelling problem. It has a solution in `Q(sqrt3, sqrt5)` with
`p, q = (sqrt3 +- sqrt15)/6`. **It attains the two-body cap for the first time at n = 4, and
pays 42 triple points for it.**

**The target.** `1 + 176 + L + holes = 1 + 176 + 3 + 3 = 183`, so proving `T3 + two-body <= 176`
proves `max(4) = 183` — the first proved maximum above n = 3. One coupling inequality instead of
two caps known not to be simultaneously tight. Both terms are vertex counts in the SAME identity
([P327]), so this is a statement about how vertices distribute between signatures, not a relation
between unrelated quantities.

**Method note, carried at the top because it nearly cost the result.** The first `T3` for the K4
compound was **8**, from a 50-digit float enumeration whose oracle — the same code on the record,
where 128 is known — returned 38, then 90, and never 128. `Matrix.inv()` on `Float` entries loses
far more than the `1e-30` equality tolerance assumed: **the tolerance sat below the noise floor
of its own arithmetic.** Redone over an exact biquadratic field (`src/kfield.py`, where zero-test
is a tuple comparison), the oracle returns 128 and the compound returns 74. Three wrong values
went to the oracle; none reached a document.
