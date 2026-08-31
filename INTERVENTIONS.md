# Interventions: what human attention changed, and what it did not have to

*Started 2026-08-31, at the user's request, after three corrections in one session
all traced to the same trigger.*

`JOURNEY.md`'s [collaboration section](JOURNEY.md#the-collaboration-honestly-described)
describes the division of labour as narrative. This is the register behind it: a
running, appendable list of **specific** moments where a human sentence changed the
result, and — kept beside it, because the ratio is the point — moments where the
error was caught without one.

It exists because of an observation the register itself should not be allowed to
soften. The user, 2026-08-31:

> I only suspected you had forgotten things when you mentioned things like 15
> directions or 1/1000 1/100, so there may be other things you've forgotten that I
> didn't notice.

That is the finding, not the anecdote. **Detection depended on a method-revealing
number happening to surface in prose.** Both catches came from a parameter leaking
into a report, not from the claim being checked. Claims that never leaked one were
not audited by anybody — and there is no way, from inside, to enumerate them.

---

## Part A — Interventions that changed the outcome

Two kinds, and the mix has shifted over the project's life.

### A1. Generative: a human noticing something, which opened work that did not exist

These are the ones `JOURNEY.md` already celebrates. Listed here with their ledger
anchors so the register is complete rather than only self-critical.

| # | The human contribution | What it produced |
|---|---|---|
| [P9](LEDGER.md#p9) | noticed a family of maximal 3-cube configurations slides continuously between the octahedral compound and the dodecahedral one | rational + overall record 699 |
| [P12](LEDGER.md#p12) | "find intersections between families" | **new record 723** |
| [P13](LEDGER.md#p13) | noticed octahedral max uses EDGE concurrences, dodecahedral uses CORNER | the incidence-geometry programme |
| [P14](LEDGER.md#p14) | reframed the goal: not maximise a heuristic, map which depth trade-offs are possible | the depth trade-off structure |
| [P17](LEDGER.md#p17) | noticed golden N4 is optimal on every subset yet not maxN4 | frustration; the middle-layer mechanism |
| [P25](LEDGER.md#p25) | looking at the viewer, asked whether a nearby configuration "perhaps with irrational rotations" could close the near-miss edges exactly; and separately, for "another way to slide from octahedral √2 to golden √5 maintaining edge concurrences" | the **dihedral family** — closed form, four theorems, both 67s; and pair-identity tracking across the slide |
| [P49](LEDGER.md#p49) | asked whether the absence of irrational solutions was an artifact of an unnecessary restriction | it was; walls are pairs of planes |

### A2. Corrective: a human question that invalidated something already reported

These are the ones that motivate this file. In each, a claim had been stated
confidently, and the question — always about METHOD, never about the result — took
it apart.

| # | What the human said | What it overturned | **The tell** |
|---|---|---|---|
| [P115](LEDGER.md#p115) | "was that correlation a RESULT at all?" | no: `lineality = ambient − rank`, so the "finding" restated a definition | a claim that could not have come out otherwise |
| [P170](LEDGER.md#p170) | "could exploring higher n reveal anything about lower n?" | "183 does not embed in 393" — false; I had assumed the 4-subset was contiguous cubes | — (came out of new work, not a tell) |
| [P175](LEDGER.md#p175) | "do all points on a plateau generate the same tower?" | required first showing deficit directions ARE plateaus; they are not | — |
| [P182](LEDGER.md#p182) | **"are the 15 directions chosen by sampling or solving?"** | `shapes.py` was sampling. METHODS 1's *named* failure — "seven representative directions, all small-integer and axis-aligned" | **"15 directions"** in my own report |
| [P183](LEDGER.md#p183) | "are all continua paths and endpoints documented?" | they are not; and I had claimed 727 showed no locus while `RESULTS.md` had said for weeks it is a plateau on four arcs | an audit question I had not asked |
| [P184](LEDGER.md#p184) | **"I think we implemented epsilon as a step size"** | the ENGINE is a true infinitesimal; **P175** used steps 1/1000, 1/100, 1 — and two of them agreed, certifying a shared cell. P175's universal is false for n ≥ 7 | **"1/1000: 685  1/100: 685"** printed in the entry |

**The shift.** Early interventions were generative — a human seeing meaning in a
picture. Recent ones are corrective — a human auditing method. Both matter, but the
second kind is the one that scales badly: it requires the human to read closely
enough to spot a leaked parameter, on work that is by then several documents deep.

### A3. What the "Prompted by" marker does and does not capture

The ledger marks user-initiated entries with the phrase "Prompted by" — 15 of them.
That count is an **undercount and should not be quoted as a measurement**:
[P182](LEDGER.md#p182), one of the largest corrections in the project, carries no
such marker even though it exists entirely because of the sampling question. The
marker records what I remembered to attribute.

---

## Part B — Caught without prompting

Kept beside Part A so the register is not a confession. The pattern in it is sharper
than the list: **almost every unprompted catch came from a GATE or a control, not
from re-reading.**

| What was caught | How |
|---|---|
| A misattribution in **this file**: the "another way to slide" quote was cited to P26 when it is inside P25 | verifying every anchor against the ledger before publishing the register |
| Wrong n=9 representative in `rungshapes.py` — (57,57,56,57) is the member P181 extended, not the recorded k=56 | the gate demanding METHODS 12's known curve **failed**, on the right grounds |
| `cube_regions_fix`'s "correct count = 145" was wrong (true 143) | the user's rotation idea supplied ground truth — *shared credit*: the idea was theirs, the test mine |
| [P147](LEDGER.md#p147)'s two performance claims | my own follow-up probe falsified both; recorded as Addendum 3 |
| [P158](LEDGER.md#p158)'s n=7 count | retracted; modularity refuted four independent ways |
| [P163](LEDGER.md#p163) retracted in full | I had hardcoded the gauge AND evaluated `count_at(y)` instead of `count_at(pt+y)` |
| `None` scored as "changes both sides" in `eps_null.py` | noticed on reading my own output — *after* writing FAILURE_MODES 16c about exactly that |
| `size_reduce` made n=7's direction unevaluable where it had evaluated | comparing runs; reported as a self-inflicted regression, not a new negative |
| `RESULTS.md` still said n=9 had no establishing Postscript; no n=10 row | the P183 audit — but the audit was user-prompted |
| P172's "four confirmations" at n=10 were two | ambient is by construction, deficit = ambient − rank is derived |
| The n=10 arrangement run was irreproducible and its log omitted its own input | asking what file would regenerate the number |
| `METHODS 6` cited for a rule that lives only in the global principles file | checking the reference before relying on it |

---

## Part C — What the tells have in common, and the practice that follows

Both 2026-08-31 catches have the same shape: **a number that encodes a methodological
choice appeared in output, unlabelled as a choice.** "15 directions" does not say
*sampled*. "1/1000, 1/100" does not say *step size*. A reader who knows the project's
principles recognises them instantly; the producer, already looking at the next task,
does not.

Three consequences, in increasing order of discomfort:

1. **The method-revealing parameter belongs in the claim, not the appendix.** A
   result should carry its step size, direction count, sample size, engine, and
   window — in the sentence that states it. "1217 holds along its curve" is not
   auditable; "1217 holds at 9 of 17 offsets at step 1/630 on the wide engine" is.
2. **A sampled quantity must say so in the same breath.** METHODS 1's corollary
   already requires this ("a sampled count is a lower bound, a solved one is not — say
   which you have"). Both catches were violations of a rule already written down.
   Writing a principle does not install it.
3. **The audited set is exactly the set that leaked a parameter.** This is the part
   with no fix from inside. The three corrections this session were not found by
   review; they were found because a number happened to be visible. The honest
   statement of coverage is therefore: *unknown, and not estimable by me.*

**Maintenance.** Append to Part A whenever a human sentence changes a result, with
the tell recorded — the tell is the reusable part. Append to Part B whenever
something is caught without one, with *how*. Neither list is allowed to be pruned for
looking bad; the ratio between them is the measurement, and a register that only
keeps its successes measures nothing.
