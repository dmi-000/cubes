# Orientation — read this FIRST after any context loss

One screen. Not a summary of results (that is `RESULTS.md`; per level, `LEVELS.md`) and not
the record (`LEDGER.md`, which is for audits, not for reading straight through). This is the frame whose absence has caused real errors: three in the
session of 2026-09-18 alone, each because a named object was not recognised.

## Why this project exists

It began as a search for **max(6)**, because `max(n <= 5)` was believed solved by the
subsets of **UC09**, the classical compound of five cubes inscribed in a dodecahedron.
Counted exactly, UC09's subsets are:

    5-subset 351    4-subset 177    3-subset 67    2-subset 13

**The belief is correct at n = 2 and n = 3** — 13 and 67 are the proved maxima — **and
wrong at n = 4 and n = 5**: 177 < 183, and 351 < 393 ([P16], which is where the floor
moved). That is the whole origin, and it is why the search starts at six cubes.

## Named objects — recognise these, they recur under several names

| name | what it is | count |
|---|---|---|
| **UC09** / "the compound of five cubes" / "golden five" | 5 cubes in a dodecahedron; COMPLETE corner sharing, all 10 pairs | 351 |
| **golden 177** | UC09's 4-subset. Also reached from `A4` symmetry ([P342]) and from a 5-edge sharing graph forcing its 6th ([P351]) — three routes, one object | 177 |
| **golden 67** | UC09's 3-subset; one of the two proved `max(3)`, in `Q(sqrt5)` | 67 |
| **octahedral 67** | the OTHER proved `max(3)`, in `Q(sqrt2)`; a `C3` orbit | 67 |
| **the records** | 183, 393, 727, 1217, 1895, 2787, 3925 for n = 4..10 | |

**Every subset of the golden 177 is at its proved maximum** — because it IS a UC09
subset, not by coincidence — **and it still loses to 183.** That single fact is the
sharpest statement in the project: subset-optimality does not give the maximum.

## The framework (n = 4)

    TOTAL <= 7 + two-body + B - Q4         two-body = EE + 2*SC2
    B := T3 + 4*Q4generic <= 32*C(n,3)     beating 183 needs two-body + B - Q4 > 176
    the record sits at  48 + 128 - 0 = 176

**It is a BOUND, not an identity** ([P374]). The `7` is `1 + L + sum c_ell` and varies in
`{-3..7}`; it equals 7 on the record by structure. And `two-body + B - Q4` omits the excess of
`(1,1,2)`, `(1,2,2)`, `(2,2,2)` vertices, so for a compound carrying one the formula is not a
bound at all — about 15 % of random compounds. **Quote engine counts, or name the formula.**

More generally the count is EXACT inclusion-exclusion over subsets ([P340], [P341]),
and `max(3) = 67` applied per 3-subset drives most of the bounds ([P338]).

## A parity claim that was WRONG, kept as a warning ([P375])

**"Region counts are odd" is FALSE.** The argument — central symmetry pairs the regions, and a
fixed region must contain the origin — fails at its second step: a fixed SET need not contain a
fixed POINT (a shell is centrally symmetric and misses the origin). Even counts occur, e.g.
**100** at `1,0,0,0; -6,4,-6,-5; -3,6,-12,-7; 1,-5,11,9`.

What is true: `TOTAL == (number of self-antipodal regions) mod 2`. Every RECORD is odd
(`13, 67, 183, 393, 727, 1217, 1895, 2787, 3925`) and so is everything near them, which is
exactly why 35 counts from one region looked like a theorem. **Beating 183 does NOT require
185; 184 is not excluded.**

## The policy the records follow ([P364])

**One hub, saturated at degree 4; every other cube gets at most ONE shared axis.**
A cube with one shared axis keeps a free rotation and can dodge a forced coincidence
(codimension 1 in it); pinned cubes cannot ([P358]). No second hub, no cycles. Above
n = 5 the records add cubes with NO sharing at all.

## Status

* **Proved:** `max(2) = 13`, `max(3) = 67`.
* **`max(4) = 183` is UNPROVED, and three reductions have been refuted** — `T <= 48` by the golden
  177, whose level-1 two-body weight is 60 ([P389]), and the two below BY THE SAME KIND OF SEED. `EE <= 36` at `B = 128`
  ([P352], [P361]) and `EE + B <= 164` ([P368]) both died to
  `1,0,0,0; 0,2,-3,-2; 0,2,-3,2; -4,-2,-5,-6` — `EE 38, B 128`, 173 regions ([P373]) — and a
  climb from it reaches `EE = 42` at `B = 128`. Both refuted ceilings were maxima over searches
  seeded from the record and the face-diagonal family; the refuter is the n = 3 `EE + B`
  extreme extended. **What bounds `EE` at `B = 128` is open.**
* **Proved and still standing:** `E_i <= 10` ([P237]), `E_S <= 32` (PROOF_67), hence
  `EE + B <= 188 - 2*SC2`, and `TOTAL <= 195 - Q4` **only for compounds with no `(1,1,2)`,
  `(1,2,2)` or `(2,2,2)` vertices** (Scope note 2026-09-24: the framework paragraph above says
  so, and this line did not). The golden attains `EE + B = 164` at
  `SC2 = 12`, exactly its box bound — the one branch closed by proof.
* Complete corner-sharing is sub-maximal at both sizes where it exists (n = 4, n = 5).

## Before trusting any claim in a summary, run the dependency check

    python3 src/claim_deps.py --audit        FALLEN postscripts with unflagged dependents
    python3 src/claim_deps.py P352           everything that cites P352

**Measured 2026-09-23: about half of all citations to fallen postscripts carry no correction
marker** — 227 of 480, over 25 fallen postscripts, as of 2026-09-24. The SUSPECT tier is empty:
all nine were resolved by hand, seven as fallen and marked, two as not fallen and recorded in
`RESOLVED_NOT_FALLEN`. The exact figure drifts with every
edit, so `--audit` prints the live one and the number here is only a scale. Three successive
measurements ([P386] 73 %, [P387] 52 %, [P388] 48 %) all sat near half while the set being
measured changed twice underneath them — **the percentage was never the finding.**
<!-- reviewed 2026-09-24: cites P386/P387 as the history of the tool, not for their fallen figures -->

**READ THE TWO TIERS AS DIFFERENT THINGS.** `FALLEN` means the entry carries its own in-place
correction marker: not in doubt. `SUSPECT` means it is NAMED in a refutation-family heading and
the role is unverified — a heading title says who is mentioned, not who lost, and the winner and
the corrector get named in exactly the same sentence shape. Resolve a SUSPECT by hand; if it
really fell, write the marker into its own entry, which promotes it to FALLEN. Do not propagate
from the SUSPECT list. *This figure moves every time a document is written or
a postscript is marked — run `--audit` for the live one rather than quoting this.* Treating a
stale copy of a measurement as current is the failure this whole section is about. Citations point BACKWARD (claim names evidence);
refutation travels FORWARD (evidence invalidates claims). Nothing in the documents runs that
direction, so propagation was done from memory — and memory is what a compaction destroys.

> **CORRECTED 2026-09-23.** This section previously read *73 %, 207 of 284, measured
> 2026-09-21 ([P386])*. **That figure was wrong and so was the list under it.** The audit
> keyed on the ledger heading TAG — but the tag names the entry's ACTION, not its status:
> `[REFUTATION] Postscript 378` is P378 refuting [P136] and [P287], and P378 itself stands.
> So the audit was listing the CORRECTORS: 13 of its 18 rows were current results, and
> propagating from it would have stamped REFUTED markers on [P330], [P374], [P378], [P383].
> The selector now reads two structural signals instead — a `[Pnnn]` named in a
> refutation-family heading and an in-place `> **CORRECTED/REFUTED** ` blockquote inside an
> entry. **[P388] then demoted the first of those to SUSPECT** — it read names as roles and
> falsely reported [P16] and [P272] fallen — and fixed a heading regex that could see only 200
> of 383 entries, which had hidden eight genuinely fallen postscripts. Oracle for the fix: [P304] (59 dependents,
> `[VERIFIED**]`, skipped because its tag said neither word) and [P334] (42 dependents,
> refuted by [P370], not detected at all) must both appear. They do. So does [P375], the
> example this tool was built for, which the broken selector also missed.

## The traps — each cost a run, and the tell is always the same

1. **A vertex lies on the facets of its OWN cubes and may be outside every other.**
   Discarding points outside any cube killed `T3` four separate times.
2. **Face normals are the COLUMNS of `mat(q)`** — five occurrences in one session.
6. **A ceiling certified by a directed search is still a search.** Two have now been
   refuted, both by seeding from where the analogous law FAILS at a smaller n rather than
   from the record. Before quoting a maximum, ask what it was seeded from.
7. **A gate whose control lacks the feature cannot fail** ([FAILURE_MODES 45]). [P334]'s
   `T3 = 74` was `T3 + Q4generic`; its gate ran on the record, where `Q4generic = 0`.
3. **Engine refusals** (`{"error": ...}`) scored as 0 by `.get(...) or {}`.
4. **Grep for the OBJECT's name, not your own phrasing.** "Complete corner sharing"
   appears nowhere; the record says *UC09*, *five-cube compound*, *golden 351*.
5. **Before opening an OPEN QUESTION, grep `RESULTS.md` for its subject.**

**THE TELL for 1 and 2: a census returning zero for something the construction
guarantees.** That is a contradiction, not a result — stop and check the code.

## Where things live

`SESSION_STATE.md` current state · `RESULTS.md` beliefs by strength · `LEDGER.md`
append-only record (indexed) · `OPEN_QUESTIONS.md` · `METHODS.md` what to do ·
`FAILURE_MODES.md` what goes wrong, by symptom · `src/probes/` one script per finding,
each with provenance · `cb/six_cube_search_results.md` the early UC09 work.
