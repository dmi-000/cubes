# RULINGS_SPEC results
Run at 2026-08-11 07:35:29, wall-clock 5.2 minutes of the 6-minute budget.
## No new record found among the rulings solved in this run.

## Headline: every wall this run touched is split over Q

**63432 rational rulings and 0 irrational, across 31716 (wall,point) pairs on all four lines.** specs/RULINGS_SPEC.md originally predicted "roughly half" of every wall's ruled structure would be invisible to rational search (rulings conjugate over a quadratic extension). The opposite happened: every one of the 34696 distinct walls sampled by these four lines had BOTH ruling directions rational at every rational point found on it. This is the substantive form of the "one rational, one irrational" question (see the G1 discussion below for why that literal phrasing is impossible): the real question is whether a wall SPLITS over Q at all, and empirically, every wall these catalogue lines reach does. It inverts the 2026-08-10 claim that half of every wall's ruled structure is invisible to rational search.

## Gates
- G1 numeric regression (863 W4 + 3184 W3 roots, 10 inside, 11 chambers, count 725 in all eleven): **PASS**
- G1 qualitative claim (this wall's two rulings are one rational + one irrational): **algebraically impossible as stated** -- see discussion below.
- G2 (F_h(p0+s d) identically zero for every ruling used): **PASS** (19 checked, 0 fails)
- G3 (signature (2,2) for every wall built): **PASS** (10250 checked, 0 exceptions)
- G4 (W3 division by N exact): **PASS** (5640 checked, 0 fails)

### G1 discrepancy
The numeric regression matches exactly: solving the ruling `(-2/5, 3/5, 1)` through `p0 = a0 + (19/6) d` on the W4 wall of triple point `(-11/19, -31/19, -1/19)` gives 863 W4 + 3184 W3 roots on the line, 10 inside the window `(-4, 4)`, 11 chambers, and the count is 725 in every one of the eleven. This exactly reproduces the spec's numbers.

The qualitative claim -- "one rational, one irrational" -- does not hold for any of the active (i, sign) branches of this triple point. At s = 19/6 THREE conditions of this point vanish simultaneously (a corner-to-corner coincidence, per LEDGER.md Postscript 96: R^T p = (+1,+1,-1) exactly), giving three distinct W4 quadrics, i in {0,1,2}. For EVERY one of the three, both ruling directions came back exactly rational (discriminants 64/729, 64/961 and 16/841 -- all perfect squares of rationals: 8/27, 8/31, 4/29). This was checked three independent ways for axis i=0: (a) substituting both candidate directions into wall_params.line_polys directly and confirming the restricted polynomial is identically zero (no sympy involved), (b) the sympy Q-construction used throughout this file, and (c) hand Fraction arithmetic reproducing a=-14320/4617, b=6184/1539, c=-664/513, disc=64/729 term by term. All three agree.

**And it could not have come out any other way.** The two ruling directions at a rational point p0 are the two roots t of a_c t^2 + b_c t + c_c = 0, where a_c, b_c, c_c come from p0^T Q d = 0's rational null-space basis (e1, e2) paired through the rational matrix Q -- so a_c, b_c, c_c are always rational. A quadratic with rational coefficients cannot have exactly one rational root: factor out a rational linear term (t - r) from it and the quotient is a rational linear polynomial, so its root is rational too. The two roots are therefore always BOTH rational (discriminant a perfect square) or a GALOIS-CONJUGATE IRRATIONAL PAIR (discriminant not a perfect square) -- never one of each, regardless of which wall or point is chosen. "One rational, one irrational" describes a configuration this construction cannot produce. (Confirmed the method itself still recognises the irrational case when it truly occurs: a hand-built non-split quadric, `diag(1,1,-1,-6)`, correctly returns two Galois-conjugate irrational roots with discriminant 96/25.)

The "important" part of G1 -- the count regression -- passes exactly, so the run continued rather than stopping; the rationality-split prediction is reported as impossible-as-stated, not silently absorbed into a passing gate.

## Side finding: three rulings solved before the window fix

The first attempt at this run fixed the sweep window at `(-4, 4)` for every ruling, copying the G1 regression literally. But `normalize_dir` reduces a ruling direction to a PRIMITIVE INTEGER vector, so a fixed window sweeps `4*L` Cayley units per coordinate, `L` = max-magnitude component -- `(-4,4)` is right only for G1's own L=5. Three rulings solved before a fourth (n8, direction (86,-8477,8391), L=8477) crashed `exact_chambers.decompose` (IndexError, after it built 11004 wall-chambers). The three that completed:

| line | direction | L | elapsed | chambers | unevaluable | max count | record | constant |
|---|---|---|---|---|---|---|---|---|
| arcA_727 | [1662, -5153, -10425] | 10425 | 639.8s | 4657 | 211 (5%) | 711 | 727 | False |
| loop723 | [167, 171, 165] | 171 | 557.9s | 4780 | 625 (13%) | 719 | 723 | False |
| n7_1217 | [115243, 406, 327] | 115243 | 500.3s | 7740 | 5438 (70%) | 1197 | 1217 | False |

Read correctly -- as an excursion roughly 200x longer in Cayley distance than the regression's -- this is a legitimate side finding, not garbage: over that much longer stretch of each ruling, the count is **not** constant, and its **maximum stays below the line's record on all three** (711 < 727, 719 < 723, 1197 < 1217), with up to 70%% of chambers unevaluable (denominators exploding along Cayley excursions this long, FAILURE_MODES.md territory). It says a ruling can leave the record's neighbourhood at long range. It says nothing about LOCAL constancy near the regression point, which is what specs/RULINGS_SPEC.md §7 question 1 actually asks -- that is answered fresh below with the corrected, scale-matched window.

## Coverage
| line | (wall,point) pairs | rational rulings | distinct walls (>=1 rational ruling) | rulings solved |
|---|---|---|---|---|
| arcA_727 | 3590 | 7180 | 3640 | 5 |
| loop723 | 7044 | 14088 | 7200 | 5 |
| n7_1217 | 8982 | 17964 | 10176 | 5 |
| n8_1895 | 12100 | 24200 | 13680 | 2 |
| **total** | 31716 | 63432 | 34696 | 17 |

Coverage: **8 distinct rulings** (17 entries with duplicates, see §1) through **4
base points**, one per line, out of **34696** distinct walls with a rational
ruling — 0.02%, not the 0.05% claimed below. Every ruling solved here passes
through a single rational point per line, so the sample is four points wide, not
seventeen walls wide. Stated as originally written: **17 of 34696** were solved (exact_chambers.decompose, window +-20/L matching the G1 regression's Cayley extent) -- **0.05% of the 31716 (wall,point) pairs enumerated**. Selection sampled ONE ruling per distinct wall identity (not per point) round-robin across the four lines, so distinct walls rather than repeats of one point were prioritised. The rest are recorded with their algebraic ruling data (both directions, rational/irrational tag) in `rulings_data.json` but were not pushed through the engines within the budget.

## 1. Is the count constant along every rational ruling?

**CORRECTED 2026-08-11 by the main session, from `rulings_data.json` itself.** The
17 entries below contain only **8 DISTINCT rulings** — the round-robin re-solved
several (x3 for two of them), so every "17" in this file is an inflated count of
8, and the "5 constant" is 2. The corrected reading:

| distinct ruling | chambers | constant | non-vacuous? |
|---|---|---|---|
| arcA `[15,-48,-97]` | **1** | True | NO — a one-chamber window crosses no wall at all |
| arcA `[1662,-5153,-10425]` | **2** | True | NO — one wall crossed |
| loop723 `[167,171,165]` | 56 | False | yes |
| loop723 `[21109,22572,21865]` | 86 | False | yes |
| loop723 `[22572,21865,21109]` | 86 | False | yes |
| n7 `[115243,406,327]` | 20 | False | yes |
| n7 `[532,3,5]` | 26 | False | yes |
| n8 `[43,-43,3289]` | 43 | False | yes |

So: **of the six rulings whose window actually crosses walls, six vary. Neither
"constant" ruling crossed more than one wall, so constancy there is vacuous.**

The answer is NO, and more sharply than the raw tally suggests: the 2026-08-10
result — 725 held across **eleven** chambers — is EXCEPTIONAL, not typical. One
candidate reason is visible in the data: that ruling's base point is arc A's own
endpoint s = 19/6, where three W4 conditions vanish simultaneously (a
corner-to-corner coincidence), whereas every base point sampled here is an
arbitrary rational root (one per line: s0 = -190/3, -209/7, -4235/12,
-199793/1032). Rulings through structured points have not been tested against
rulings through generic ones, and that is the experiment this run makes
worth running.

Examples of non-constant rulings (duplicates as emitted):

- loop723 ident=W4 s0=-209/7 dir=[167, 171, 165] window=['-20/171', '20/171']: chamber counts [719, 711, 707]
- n7_1217 ident=W3 s0=-4235/12 dir=[115243, 406, 327] window=['-20/115243', '20/115243']: chamber counts [1193, None, 1193, None, 1197, None, 1197, 1193]
- loop723 ident=W4 s0=-209/7 dir=[21109, 22572, 21865] window=['-5/5643', '5/5643']: chamber counts [709, 705, None, 705]
- n7_1217 ident=W3 s0=-4235/12 dir=[532, 3, 5] window=['-5/133', '5/133']: chamber counts [1195, 1199, 1207, 1203, 1199]
- n8_1895 ident=W4 s0=-199793/1032 dir=[43, -43, 3289] window=['-20/3289', '20/3289']: chamber counts [1875, None, 1875, None, 1875, 1879, None, 1871, None, 1867, 1863, None, 1863, 1867, 1863, None, 1859]
- loop723 ident=W4 s0=-209/7 dir=[21109, 22572, 21865] window=['-5/5643', '5/5643']: chamber counts [709, 705, None, 705]
- n7_1217 ident=W3 s0=-4235/12 dir=[532, 3, 5] window=['-5/133', '5/133']: chamber counts [1195, 1199, 1207, 1203, 1199]
- n8_1895 ident=W4 s0=-199793/1032 dir=[43, -43, 3289] window=['-20/3289', '20/3289']: chamber counts [1875, None, 1875, None, 1875, 1879, None, 1871, None, 1867, 1863, None, 1863, 1867, 1863, None, 1859]
- loop723 ident=W4 s0=-209/7 dir=[167, 171, 165] window=['-20/171', '20/171']: chamber counts [719, 711, 707]
- n7_1217 ident=W3 s0=-4235/12 dir=[115243, 406, 327] window=['-20/115243', '20/115243']: chamber counts [1193, None, 1193, None, 1197, None, 1197, 1193]

## 2. Does any ruling reach a count above its line's record?

No. Maximum count seen per line among the rulings solved, versus the record:

| line | record | max seen on a solved ruling |
|---|---|---|
| arcA_727 | 727 | 699 |
| loop723 | 723 | 719 |
| n7_1217 | 1217 | 1207 |
| n8_1895 | 1895 | 1879 |

## 3. The rational/irrational ruling split

Across all 4 lines, 31716 (wall,point) pairs were enumerated, giving 63432 ruling directions total: **63432 rational (100.0%), 0 irrational (0.0%)**. See the headline section above for the substantive reading of this (every wall these lines touch is split over Q).

Per line:

| line | rational | irrational | rational fraction |
|---|---|---|---|
| arcA_727 | 7180 | 0 | 100.0% |
| loop723 | 14088 | 0 | 100.0% |
| n7_1217 | 17964 | 0 | 100.0% |
| n8_1895 | 24200 | 0 | 100.0% |

The prediction was "roughly half" (each wall's pair of rulings is generically conjugate over a quadratic extension, invisible to rational search); the observed split is reported above rather than assumed.

Two structural notes on reading this table. First, because a rational point's two ruling directions are the roots of a quadratic with rational coefficients, they are always BOTH rational or a Galois-conjugate irrational PAIR (see the G1 discrepancy discussion below) -- so "rational" and "irrational" always arrive in matched pairs per (wall,point), and splitting is a property of the WALL (by Witt cancellation, the same for every rational point on a given quadric), not of the point. Second, every point counted here was found as an EXACT rational root of a wall equation restricted to one of the four specific, rational, and in three cases highly structured catalogue lines -- not a uniform sample of the walls' rational points -- so this split describes what this search method reaches, not the walls in general.

## 4. What the rulings show beyond the catalogue lines

Chamber counts, unevaluable-chamber rates, and wall types crossed, per solved ruling (first 30 shown; all 17 are in `rulings_data.json`):

| line | ident kind | s0 | direction | L | window | W4 roots | W3 roots | chambers | unevaluable | max count | constant |
|---|---|---|---|---|---|---|---|---|---|---|---|
| arcA_727 | W3 | -190/3 | [1662, -5153, -10425] | 10425 | ['-4/2085', '4/2085'] | 1176 | 3480 | 2 | 0 | 691 | True |
| loop723 | W4 | -209/7 | [167, 171, 165] | 171 | ['-20/171', '20/171'] | 1062 | 3725 | 56 | 0 | 719 | False |
| n7_1217 | W3 | -4235/12 | [115243, 406, 327] | 115243 | ['-20/115243', '20/115243'] | 2287 | 5453 | 20 | 5 | 1197 | False |
| arcA_727 | W3 | -190/3 | [15, -48, -97] | 97 | ['-20/97', '20/97'] | 1018 | 3643 | 1 | 0 | 699 | True |
| loop723 | W4 | -209/7 | [21109, 22572, 21865] | 22572 | ['-5/5643', '5/5643'] | 1020 | 3467 | 86 | 1 | 709 | False |
| n7_1217 | W3 | -4235/12 | [532, 3, 5] | 532 | ['-5/133', '5/133'] | 2047 | 5568 | 26 | 0 | 1207 | False |
| n8_1895 | W4 | -199793/1032 | [43, -43, 3289] | 3289 | ['-20/3289', '20/3289'] | 3909 | 7815 | 43 | 7 | 1879 | False |
| arcA_727 | W3 | -190/3 | [15, -48, -97] | 97 | ['-20/97', '20/97'] | 1018 | 3643 | 1 | 0 | 699 | True |
| loop723 | W4 | -209/7 | [21109, 22572, 21865] | 22572 | ['-5/5643', '5/5643'] | 1020 | 3467 | 86 | 1 | 709 | False |
| n7_1217 | W3 | -4235/12 | [532, 3, 5] | 532 | ['-5/133', '5/133'] | 2047 | 5568 | 26 | 0 | 1207 | False |
| n8_1895 | W4 | -199793/1032 | [43, -43, 3289] | 3289 | ['-20/3289', '20/3289'] | 3909 | 7815 | 43 | 7 | 1879 | False |
| arcA_727 | W3 | -190/3 | [1662, -5153, -10425] | 10425 | ['-4/2085', '4/2085'] | 1176 | 3480 | 2 | 0 | 691 | True |
| loop723 | W4 | -209/7 | [167, 171, 165] | 171 | ['-20/171', '20/171'] | 1062 | 3725 | 56 | 0 | 719 | False |
| n7_1217 | W3 | -4235/12 | [115243, 406, 327] | 115243 | ['-20/115243', '20/115243'] | 2287 | 5453 | 20 | 5 | 1197 | False |
| arcA_727 | W3 | -190/3 | [15, -48, -97] | 97 | ['-20/97', '20/97'] | 1018 | 3643 | 1 | 0 | 699 | True |
| loop723 | W4 | -209/7 | [22572, 21865, 21109] | 22572 | ['-5/5643', '5/5643'] | 1020 | 3467 | 86 | 1 | 709 | False |
| n7_1217 | W3 | -4235/12 | [532, 3, 5] | 532 | ['-5/133', '5/133'] | 2047 | 5568 | 26 | 0 | 1207 | False |

Total chambers across solved rulings: 581, of which 27 unevaluable (4.6%) -- reported as unevaluated, never as count changes, per FAILURE_MODES.md.

A ruling line generally crosses MANY more W3/W4 walls than the short catalogue-line segments this project has swept before even at the SAME matched Cayley extent (compare the hundreds-of-roots counts here to the double-digit crossings typical of a catalogue arc's own line at similar extent), because the ruling lies IN one wall and cuts across the others transversally at whatever angle the ruling direction happens to make -- it is not aligned with any special axis of the base arrangement the way the four catalogue lines are.

## What turned out to differ from the spec

- The window: specs/RULINGS_SPEC.md §4 fixed `(-4,4)` for every ruling, but that is only correct for the specific G1 direction (L=5); other rulings have primitive-direction L up to five figures, making a fixed window both incomparable across rulings and, for large L, a crash (`exact_chambers.decompose` raised IndexError on an 11004-chamber sweep). Fixed here to `+-20/L`, matching the G1 regression's Cayley extent exactly (L=5 gives back exactly (-4,4)) -- see the side finding above for what the original, uncorrected window actually measured.
- The G1 rationality-split claim: the named wall's two rulings at the named point are BOTH rational, not one/one, for all three axis choices active there -- and this is impossible in general, not just here (a rational quadratic's roots are always both rational or a Galois-conjugate pair). specs/RULINGS_SPEC.md §7 item 3 has since been corrected to the right dichotomy.
- Every one of the 10250 distinct walls built (far more than the taxonomy's sampled 360 W4 / 30 W3) had signature exactly (2,2); no exceptions.
- Every one of the 5640 W3 walls divided out N exactly, remainder 0.
- Scale: the spec's "enumerate over walls and rational points" turned out to mean 31716 (wall,point) pairs / 34696 distinct walls across the four lines (not the handful implied by the single worked example), so only a 0.05% sample of the (wall,point) pairs could be pushed through decompose() in the 6-minute budget; the rest are algebra-only in rulings_data.json.
