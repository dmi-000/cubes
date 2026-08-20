# STRUCTURED_RULINGS_SPEC — does ruling constancy track the base point's multiplicity?

Postscript [103](../LEDGER.md#p103) refuted "rulings are constant-count lines": of eight distinct
rulings solved at matched Cayley extent, all six whose window crosses a wall
vary. But the one ruling that DID hold its count — 725 across eleven chambers,
2026-08-10 — sits at arc A's terminus `s = 19/6`, where **three** W4 conditions
vanish simultaneously (the corner-to-corner contact of Postscript [96](../LEDGER.md#p96)). Every
point sampled in the campaign was an arbitrary rational root, one per line.

So there is exactly one hypothesis left standing, and it is cheap to test:

> **H.** Constancy along a ruling is a property of the BASE POINT's multiplicity —
> the number of wall conditions vanishing there — not of rulings in general.

If H holds, rulings through coincidence-rich points are a generator of
constant-count one-parameter families, which is what maximiser arcs are. If it
fails, the ruling idea is finished and should be recorded as such.

Postscript [104](../LEDGER.md#p104) removes the only arithmetic obstacle: **det(Q) is a perfect square
identically** — `(|p|²−1)²` for W4, `16(|m×q|²−2|m|²)²` for W3 — so every wall is
split over ℚ and BOTH rulings through any rational point are rational. Nothing is
out of reach for the integer engines. Do not re-derive this; `detq_check.py`
proves it.

Deliverables: `structured_rulings.py`, `structured_rulings.json`,
`structured_rulings_report.md`, `structured_rulings.log`. **Add files only.**

## 1. Multiplicity, and the points to use

`rulings.py` already enumerates, per catalogue line, every exactly-rational root
`s` of every W3/W4 condition, and identifies which conditions vanish there. Reuse
that machinery — do not rewrite it.

Define **m(s) = the number of distinct wall conditions vanishing exactly at s**.
The campaign's own numbers say this varies a lot: arc A gave 3 590 (wall, point)
pairs over 360 distinct `s`, so the mean is ~10 and the tail is what matters.

For each of the four lines (arcA_727, loop723, n7_1217, n8_1895 — parameters as
in `specs/RULINGS_SPEC.md` §3), select:

* the **five highest-m** rational points on the line;
* the **five lowest-m** points (m ≥ 1), as the control;
* and, where it is a rational root of the line, **the arc's own terminus**
  (arc A's is `s = 19/6`, m = 3 by Postscript [96](../LEDGER.md#p96) — it must come out that way, and
  if it does not, stop and report, because the enumeration disagrees with a
  logged result).

Both rulings at each selected point, so ~120 solves. They are seconds each.

## 2. Solving

`exact_chambers.decompose`, window **±20/L** with `L` the direction's max
component — the scale-matched window of Postscript [103](../LEDGER.md#p103), NOT the spec-2026-08-11
fixed `(−4, 4)`, which measured a different question per ruling.

Guard: `decompose` raises IndexError on large decompositions (11 004 chambers, and
again at n = 8). Catch it, record the ruling as `crashed`, continue — and report
how many crashed, since a systematically crashing subset would bias the answer.

Per ruling record: base point `s`, its multiplicity `m`, wall identity, direction,
`L`, window, roots on the line, chambers, unevaluable chambers, the chamber count
sequence, max count, and constant yes/no. **A window yielding 0 or 1 wall
crossings is VACUOUSLY constant — count it separately and never in the "constant"
tally.** That error is what inflated the first campaign's report.

## 3. The question, answered with numbers

1. **Does constancy track m?** Report constancy rate against m as a table, high-m
   against low-m. State the sample size; ~120 rulings is small and the report must
   say so rather than implying a law.
2. **Does the arc-A terminus ruling reproduce?** It must give 725 across 11
   chambers (863 W4 + 3184 W3 roots, 10 inside) — this is the regression, and a
   failure means the selection or the window is wrong, not that the old result was.
3. **Do constant rulings reach higher counts than varying ones?** The campaign's
   maxima all sat below the record (699/719/1207/1879). If a ruling through a
   high-m point holds the RECORD value along its length, that is a maximiser arc
   found by construction rather than by search — verify any such claim on both
   engines and flag it at the top.
4. **What is m at the known arc termini** across all four lines? Postscript [96](../LEDGER.md#p96)
   says a terminus is a corner-to-corner contact, doubled; if termini are
   systematically high-m, that connects the arc structure to the wall structure
   directly.

Report the negative honestly if H fails. "Rulings are not a generator" closes a
path, which is worth as much as opening one — Postscript [105](../LEDGER.md#p105)'s exchange-rate note
is the standing lesson.
