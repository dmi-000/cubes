# STRUCTURED_RULINGS_SPEC results

Run at 2026-08-12 05:00:47, wall-clock 48.0 minutes of the 40-minute budget.

## No ruling solved in this run holds its line's record value constant along its length.

## Spec issues found

- specs/STRUCTURED_RULINGS_SPEC.md sec 4 asks for m "at the known arc termini across all four lines", but only arc A has a documented terminus in LEDGER.md (Postscript 96, s=19/6). loop723, n7_1217 and n8_1895 are catalogue LINES through record configurations, not documented two-terminus arcs -- grepping LEDGER.md for their endpoints found none. Only arc A's terminus is tested below; this is a data gap, not something this script can resolve without re-deriving those lines' arc structure, which is out of scope.
- specs/STRUCTURED_RULINGS_SPEC.md sec 1 states "arc A's is s = 19/6, m = 3 by Postscript 96 -- it must come out that way". Under the spec's OWN operational definition of m(s) (validated here: this run reproduces the spec's own "3590 pairs over 360 distinct s, mean ~10" figures for arcA_727 exactly), m_aggregate(19/6) = 18, not 3. Postscript 96's "3" counts only the ONE triple point (-11/19,-31/19,-1/19)'s own 6 W4 conditions (3 of which are active there); the aggregate root_map additionally counts other triple points and crossing lines that happen to also vanish at the same s (including the C2-mirror triple point (11/19,31/19,1/19), another unrelated triple point pair, and 8 W3 conditions). These are two different, both legitimate, notions of "multiplicity at a point" that the spec conflates. Per the hard instruction not to adjust the expectation, this is reported as a spec inconsistency rather than silently resolved -- both readings (m_aggregate=18, m_own_point=3) are used below.

## 1. Regression: does the arc-A terminus reproduce 725 across 11 chambers?

**PASS**

| check | result |
|---|---|
| 863 W4 roots on the line | True |
| 3184 W3 roots on the line | True |
| 11 chambers | True |
| count 725 in all eleven chambers | True |
| target rational ruling (-2/5,3/5,1) found among active axes | True |
| m_own_point(19/6) == 3 (Postscript 96) | True |

Chamber counts: [725]

## 2. Multiplicity at the arc termini

arcA's terminus s=19/6 is the only documented arc terminus found in the project records (Postscript 96) -- searched LEDGER.md for loop723/n7_1217/n8_1895 termini and found none; see spec issues above.

- m_own_point(19/6) [restricted to triple point `(-11/19,-31/19,-1/19)`'s own 6 conditions, Postscript 96's reading] = **3**
- m_aggregate(19/6) [every W3/W4 condition on the WHOLE catalogue line, the operational definition validated by the "3590 pairs / 360 s / mean~10" figures in specs/STRUCTURED_RULINGS_SPEC.md sec 1] = **18**

## 3. Does constancy track m? (constancy-vs-multiplicity table)

Of **38** rulings solved total: **8 vacuous** (window crosses 0 or 1 walls -- excluded from the constant/non-constant tally per spec) and **30 non-vacuous**.

| point_kind | n (non-vacuous) | constant | not constant | unevaluable | constancy rate |
|---|---|---|---|---|---|
| low | 20 | 0 | 20 | 0 | 0% |
| high | 0 | 0 | 0 | 0 | n/a |
| terminus_aggregate | 4 | 0 | 4 | 0 | 0% |
| terminus_own_point | 6 | 0 | 6 | 0 | 0% |
| **all non-vacuous** | 30 | 0 | 30 | 0 | 0% |

Same table, by low-m selection vs high-m selection (the direct test of H):

| selection | n (non-vacuous) | constant | not constant | constancy rate |
|---|---|---|---|---|
| low-m (control) | 20 | 0 | 20 | 0% |
| high-m | 0 | 0 | 0 | n/a |

**Sample size caveat: this is 38 rulings (30 non-vacuous), a small sample -- the table above is not a law, only what this run measured.**

## 4. Do constant rulings reach higher counts than varying ones?

Max count among non-vacuous CONSTANT rulings: **None**. Max count among VARYING rulings: **1879**. Records per line: {'arcA_727': 727, 'loop723': 723, 'n7_1217': 1217, 'n8_1895': 1895}.

None of the constant rulings solved in this run reached a record value.

## 5. Crashes

**4 ruling(s) crashed** exact_chambers.decompose with the known IndexError (large decomposition), out of 42 attempted -- recorded and skipped, run continued.

| line | s0 | m | point_kind | direction |
|---|---|---|---|---|
| n8_1895 | -199793/1032 | 2 | low | [86, -8477, 8391] |
| n8_1895 | -199793/1032 | 2 | low | [86, -8477, 8391] |
| n7_1217 | -6247/92 | 2 | low | [1246885, 17894, 18423] |
| n7_1217 | -6247/92 | 2 | low | [1246885, 17894, 18423] |

## Coverage and per-line detail

| line | distinct s on line | (wall,point) pairs | min m | max m | mean m | points selected | rulings solved |
|---|---|---|---|---|---|---|---|
| arcA_727 | 360 | 3590 | 2 | 304 | 9.97 | 4 | 18 |
| loop723 | 167 | 7044 | 6 | 828 | 42.18 | 2 | 8 |
| n7_1217 | 740 | 8982 | 2 | 1134 | 12.14 | 2 | 6 |
| n8_1895 | 1022 | 12100 | 2 | 1508 | 11.84 | 2 | 6 |

## Full data

See `structured_rulings.json` for every solved ruling's base point, multiplicity, wall identity, direction, window, chamber count sequence, and `structured_rulings.log` for the run trace.

## Budget

48.0 minutes elapsed of a 40-minute budget.
