# In-flight state — 2026-09-01

*A handoff note so nothing in flight is lost across a context boundary. Everything
below is already recorded durably in LEDGER/RESULTS/TAXONOMY/OPEN_QUESTIONS; this is
just the pointer.*

## Running now

- **`arcs_extend.py`** (pid 66382, ~51 min) → `arcs_extend.log`. Extends 727's arcs
  A, B, C to n=7 — [OQ 17](OPEN_QUESTIONS.md), the two-parameter search never run
  (`which_member.py`, 0-byte log). Currently still on arc D's 62 chamber
  representatives (the GATE: arc D must rediscover 1217, and its menu provably
  contains the target since 1217's seventh cube has height 4).
  **Arcs A, B, C — the unexplored ones — come after.**

## Records as of now

    13, 67, 183, 393, 727, 1217, 1895, 2787, 3925          n = 2..10

n=9 = **2787** and n=10 = **3925**, both set 2026-08-31, both verified by two engines,
rotation-invariant, nesting intact. Superseded 2785 and 3913/3917/3921.

## The live threads

- **[OQ 18](OPEN_QUESTIONS.md)** — is d1 <= 3n^2 + O(n)? 91% of the ceiling gap is at
  depth 1; the ceiling's leading coefficient is 3x too large. The unexploited
  constraint is CONCENTRICITY. This is the only route to a maximality proof.
- **[OQ 17](OPEN_QUESTIONS.md)** — arcs A, B, C never used as extension bases.
- **[OQ 15](OPEN_QUESTIONS.md)** — answered ([P206](LEDGER.md#p206)); its follow-on
  (what sets an added cube's r) is open, and the "lower r wins" reading was refuted
  ([P207](LEDGER.md#p207)).
- **Unimplemented plans** (TAXONOMY §5): components at n>=4; component counts for
  other totals (orphaned, possibly overcounted); **Lemma B** (orphaned — g(13,13)=16,
  measured, unproved, two attack routes in the ledger, deserves converting to a
  stated question).

## Added after this note was first written

- **[OQ 18](OPEN_QUESTIONS.md)** now records that BOTH live routes to a smaller ceiling
  bound converge on CONCENTRICITY — neither the depth-1 ceiling nor the increment bound
  uses the fact that every cube shares a centre. They are not independent attacks.
- **[TAXONOMY §5](MAXIMISER_TAXONOMY.md)** gained the two plans that OQ 18 disclaims:
  the joint depth constraint and sharpening the recursion.
- **[FAILURE_MODES 19b](FAILURE_MODES.md#19b)** — saying "this belongs in X" is not
  putting it in X. Three instances in fifteen minutes, all caught by the user. Treat
  "worth noting" / "I'll flag that" as a predictor that nothing was written.
- **[P209](LEDGER.md#p209)** — both 67s VERIFIED 0-dimensional in ℚ(√2) and ℚ(√5); the
  TAXONOMY §5 plan that named this as blocked was never actually blocked.

## Standing cautions earned today

- A search that finds nothing has found nothing **within the set it searched** — a
  null-space-only pool gives a FALSE negative at 727 ([P204](LEDGER.md#p204)).
- Editing a file does not change a process already running ([P201](LEDGER.md#p201)).
- `grep python3` does not match the actual binary path; use `ps -p <pid>`.
- Of 17 open questions, only 5 state what would settle them; of 201 postscripts, only
  those from P182 carry status tags.
