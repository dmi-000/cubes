# Failure modes

Every entry below actually happened in this project, most of them more than
once. They are organised by **symptom** — what you notice first — because when
something goes wrong you have the symptom, not the cause.

The pattern worth internalising before the list: **almost every error here
produced a plausible number rather than an obvious failure.** A wrong answer
that looks wrong costs an afternoon. A wrong answer that looks right costs a
month, and three of the entries below survived for weeks inside the ledger as
established results.

---

## Triage: something looks off

Run down this list before investigating anything specific.

1. **Time it against one item.** If a single count takes 0.1 s, then 1365
   counts cannot take 0.11 s. Impossible throughput is the single most
   reliable signal that a batch produced nothing.
2. **Compare output length to input length.** `zip()` truncates silently.
   Assert equality; do not filter and hope.
3. **Ask whether the check could have failed.** If the code were wrong, would
   this gate have noticed? A gate comparing two empty lists, or two lists of
   identical error messages, passes beautifully and means nothing.
4. **Ask whether you tested the property or a proxy for it.** Proxies are
   where the confident wrong answers live (§4).
5. **Ask what the sample is a sample of.** "14 of 16" and "105 of 183" were
   the same claim measured twice; only one was right.
6. **Re-derive any recorded failure before building on it.** Two of this
   project's documented dead ends were themselves wrong (§9).

---

## 1. Impossible speed → the batch produced nothing

**Symptom.** A run finishes far faster than the per-item cost allows, and
every row agrees.

**Seen.** The widened-engine equivalence gate reported "IDENTICAL" on all 1365
configurations in 0.11 seconds. The driver had joined a quaternion's four
components with `;` instead of `,`, so every line failed to parse, both
engines emitted the same error JSON, and the comparison compared two identical
lists of errors. (Postscript [59](LEDGER.md#p59).)

**Seen again, same day.** The continua census reported "0 continua" for all
129 lines in about two minutes. The engine children were being killed under
memory pressure from a concurrent 8-shard campaign; `count_many` returned an
empty list; `zip(ts, got)` produced nothing; zero runs were found. Uniformly
zero *and* fast.

**Check.** Assert `len(results) == len(inputs)`. Assert that a positive number
of rows carry a real value. Treat an empty answer as an error, never as a
finding.

## 2. A gate that cannot fail

**Symptom.** A verification passes on the first try, over a large set, with no
near-misses.

**Check.** Deliberately break the thing being tested and confirm the gate goes
red. A gate that has never failed has not been shown to work — it has only
been shown to run. Prefer gates whose expected value came from somewhere else
entirely: a hand computation, an earlier engine, a published number.

## 3. Approximate methods deciding instead of suggesting

**Seen.** A voxel pipeline reported a "stable plateau" of ~1340 regions across
three grid resolutions for a configuration whose exact count is 567. About 70%
of the "regions" were slivers thinner than any affordable grid, while other
real regions were being merged — both failure directions live at once, and
resolution convergence proved nothing.

**Rule.** Approximate methods may *suggest*; only exact arithmetic *decides*.
No floating-point number may settle whether two things touch.

## 4. A proxy invariant standing in for the thing itself

The most productive error in this project, in the sense that it produced the
most confident wrong statements.

- **Rigidity by openness.** Perturbing randomly and asking whether the count
  survives reports every measure-zero configuration as isolated. That is how a
  *continuum* of two-cube maximisers went unnoticed for weeks.
- **Congruence by μ-multiset.** The O-reduced pair invariant is necessary, not
  sufficient. It reported 8 classes where the per-label vector finds ≥ 21.
- **Chamber boundary by active-wall count.** k ≥ 3 was used to conclude that
  no irrational 727 is interior to a continuum. But a wall crossing usually
  leaves the combinatorial type unchanged, so k is not that property. Tested
  directly, most of them *are* interior. (Postscripts [60](LEDGER.md#p60) → 61; the wrong
  version stood for one hour.)

**Check.** When the direct test is cheap — and here it always was, minutes at
most — run the direct test. Use a proxy only when you have shown it is
equivalent, not merely correlated.

## 5. Describing a set from its first member

**Seen four times.** "These configurations are near-half-turns" (the median
was 135°). "The √-parts are identical" (44 distinct ones). "ℚ(√13) is the only
field reaching 727" (eight, once the guard widened). "727 swaps rigid 13-pairs
for tunable 9-pairs" (true of 1 of 161 configurations; 159 have a different
signature entirely).

**Check.** Before writing "these are…", compute the distribution. If you have
one example, say "this one is…".

## 6. Coverage artifacts — a perfect search of the wrong space

**Symptom.** A well-implemented, well-tested search returns a clean negative.

**Seen.** An early symmetry sweep was silently under-parameterised: its seed
grid could not even represent the then-current record, and it "found" the
family capped at 399. Later, a height cap of 512 was not preserved by the
base's C₃ symmetry, so 49 orbit images fell outside the search while their
partners fell inside.

**Rule.** A search must reproduce the current record from its own machinery
before its negative results are believed. And a filter must be checked against
the symmetry group: apply the group to the *filter*, not just to the data.

## 7. Reporting before persisting

**Seen.** A three-minute enumeration completed and was then thrown away by a
stale variable name in the reporting code — the accumulator had been renamed
and one reference missed.

**Rule.** Persist results before formatting them. Pickle first, print second.

## 8. Stale summary statements

**Symptom.** Generated tables are current; prose is not.

**Seen.** Ten claims went false in *summary* positions — openings,
open-question lists, footers, table-of-contents descriptions — including
"max(3) = 67 is still open" weeks after it was proved. A script that
regenerates positions and counts does not touch a sentence that has become
false.

**Rule, in the user's words:** *"Generated positions is good, but it doesn't
update invalidated statements. Discipline does that."* Keep superseded claims
in one explicit table rather than editing history, so a reader can see what
changed and why.

## 9. A recorded failure that was itself wrong

**Symptom.** A documented dead end blocks a line of work.

**Seen twice.**
- The increment-bound derivation was recorded as failed, with a
  counterexample. The diagnosis was wrong (the piece-bound it blamed was never
  needed) *and* the counterexample was geometrically false. The real error was
  that the code tested whether a line met the **open** interior of a cube, so
  twelve *tangential* contacts scored as zero. Corrected, the bound is exactly
  tight on that very example. It had stood for weeks. (Postscripts [53](LEDGER.md#p53) → 56.)
- "Irrational 727s are never interior to a continuum" — see §4. Stood for an
  hour.

**Rule.** Before treating a recorded failure as settled, re-derive it. Failures
deserve the same scepticism as successes, and get less of it.

## 10. Theory contradicting measurement

**Symptom.** A clean structural argument disagrees with an exact computation.

**Seen.** Regions are open sets, so they should survive small perturbations,
so the count at a wall should not exceed its neighbours'. Measured: 725 at the
wall against 723 just beyond it. The measurement was right and the argument
was wrong — at a tangential contact the region is *pinched* at a point, the
point is excluded, and the two lobes count separately; perturbing one way opens
the channel and merges them. Region counts are neither upper nor lower
semicontinuous. (Postscript [62](LEDGER.md#p62).)

**Check.** Confirm the measurement with a second, independently written engine
*and* re-examine the argument. Do not assume the code is at fault because the
theory is pretty.

## 11. Tooling that fails silently

- **Backgrounded heredocs.** `nohup python3 - <<'EOF' &` produced no process
  and no output, at least four times. Write the script to a file and run the
  file.
- **String-surgery patches.** `s.replace(old, new)` with `old` copied from the
  wrong source file silently changes nothing; a provenance script recorded 0
  records for that reason. `assert old in s` before every replacement.
- **Truncated heredocs.** A script that lost its `if __name__ == '__main__':`
  defined `main()` and exited 0, doing nothing. This was then misdiagnosed as
  an out-of-memory kill *twice*, with confident-sounding supporting evidence,
  before anyone measured the actual memory use (55 MB).
- **Memory blowups.** Accumulating hundreds of thousands of exact `Fraction`
  records to report on them at the end. Stream instead.

## 11b. Renaming a file a running process holds open

**Symptom.** A downstream step dies with "No such file or directory" for a file
you can see was being written.

**Seen.** A census was quarantined mid-run with
`mv continua_shard_0.jsonl continua_shard_0.CONTAMINATED.jsonl`. On Unix a
rename follows the **inode**, so the still-running process kept appending to
the renamed file and the original name was never recreated. The chained Phase B
then crashed on the missing name.

**Check.** Quarantine by copying, or stop the writer first. And when a script
announces a stage is finished, have it check the exit status — the chain here
printed "phase B done" immediately after Phase B crashed, because it never
looked. A success message that cannot report failure is the shell equivalent of
a gate that cannot fail (§2).

## 11c. Comparing representatives instead of objects

**Symptom.** A symmetry that should close a set appears not to.

**Seen.** The C3 was applied to wall lines by left multiplication q -> g*q, and
22 of 129 images appeared to fall outside the catalogue — supporting a whole
postscript about the catalogue being incomplete. But g is a cube
self-symmetry, so g*q and g*q*g^-1 are the SAME SOLID in different quaternion
representatives, and the catalogue stores one representative per line. The test
asked "is this representative listed", not "is this configuration listed".
Under conjugation: 129 of 129, 43 orbits of 3, parameter preserved exactly.

**Check.** Canonicalise before comparing, or compare invariants of the object
rather than of the encoding. This project had already recorded the identical
trap once — "the chart omits quaternion representatives, not compounds" — and
repeated it a month later, which is the argument for this file existing.

## 12. Delegation-specific: premature parking

**Symptom.** A subagent burns a large budget and returns having built the
thing but not run it.

**Seen.** Twice in one day, at ~205 000 tokens: an agent built the widened
engine correctly, then stopped to wait on its own monitor job instead of
running the gates. The main session finished the gating by hand in minutes.

**Rule.** A long computation must be a single **detached, self-sequencing
script** — it waits for its own prerequisite, checks the prerequisite is real,
fans out, and exits. An agent should collect results afterwards, never watch a
job.

**Also for delegation.** State your hypothesis in the spec and explicitly
license the agent to refute it: *"if the true invariant is not what I guessed,
report what it is; do not force it to match."* Both times an agent contradicted
the main session, the agent was right.

---

## The standing rules these produced

1. Exact arithmetic decides; approximations only suggest.
2. Two independently written engines must agree before a number is believed.
3. A search must reproduce the current record before its negatives count.
4. Gates use pre-existing values from an independent source, never
   self-consistency.
5. Persist before reporting.
6. Superseded claims go in one table; the body is never quietly edited.
7. Long computations are detached and self-sequencing.
8. Test the property, not a proxy for it, whenever the direct test is
   affordable.

See [`DELEGATION_LOG.md`](DELEGATION_LOG.md) for what each delegated agent was
told and which gates it had to pass, and
[`LEDGER.md`](LEDGER.md) for the dated record
in which every failure above is written down at the point it happened.

## 11d. The lattice dimension probe is blind to loci that are not axis-aligned

**Symptom.** A configuration you have other reasons to believe sits on a curve
or surface reads "0 of 26" (or 0 of 728) on the lattice-cardinality probe, and
gets written down as an ISOLATED POINT.

**What the probe actually measures.** Perturb each coordinate by 0, ±ε and count
how many of the 3^k − 1 neighbours keep the property; a d-dimensional family is
supposed to show 3^d − 1. That inference assumes the locus is locally a
COORDINATE SUBSPACE. A curve in general position contains no lattice neighbour
at all, at any ε, so it reads exactly 0 — indistinguishable from a genuine
isolated point.

**Demonstration (2026-08-04).** On the 393 base, the sixth cube at Cayley point
a₀ + (5/2)·(1,−3,−6), a₀ = (19/3,−7,−11), is the middle of an interval on which
727 holds — verified by stepping along the tangent, which gives 727 at ±1/64 and
±1/32. The lattice probe at that same point reads **0 of 26**, at ε = 1/64 and
1/256 alike. Known 1-dimensional, measured 0-dimensional.

**How to read past results.** A POSITIVE reading is still good evidence: it
exhibits an aligned family of that dimension. A ZERO reading is uninformative —
it means "no axis-aligned family", never "isolated". Claims resting on a zero
reading need re-testing along candidate tangents before the word "isolated" is
used. Affected and to be re-checked: the n=4 phase-2 cells reporting dim 0.00,
and any 0-dimensional claim about the n=3 (13,13,13) distinct-axis component.

**Triage.** To test for a curve you must move ALONG it; random and axis-aligned
directions both leave a curve immediately, so a negative from either is not
evidence. Get a tangent from the structure (a wall line, a symmetry, a family
parameter) and step along that.

## 13. A dimension method's zeros mean nothing until it passes a control

**The rule.** Any method that reports the dimension of a maximiser locus must
first be run on a configuration whose tangent is ALREADY KNOWN. If it cannot
recover that tangent, its zeros elsewhere are measurements of its own
conservatism and carry no information about the geometry. Report them as void,
not as evidence of isolation.

**Why this keeps being needed.** Every dimension method tried in this project
fails in the same direction — it under-reports:

* the LATTICE PROBE reads 0 for any locus not aligned with the coordinate axes
  (§11d), and read 0 at the middle of an interval proved to carry 727;
* the WALL-NORMAL null space treats every active catalogue wall as binding,
  though most concurrences do not change the count, so it reported the n=6
  record 0-dimensional when it demonstrably carries two tangents (Postscript [88](LEDGER.md#p88));
* `multicube2.py` did the same over all 3(n−1) coordinates, exactly and
  overnight, and returned 0 for all nine maximisers INCLUDING the record and
  n=8 where tangents were already verified (Postscript [100](LEDGER.md#p100));
* a hand-picked direction scan missed the tangent (1,1,0) at n=2 because it
  sampled x, y, z and (1,−1,0) — and the miss was read as isolation, twice in
  one session.

**The controls that exist.** Use them.

    n=2 mirror-plane 13 at Cayley (−12,−11,0)   tangent (1,−3,−6)? no: (1,1,0)
    n=6 727 arc A midpoint                       tangent (1,−3,−6)
    n=6 723 at Cayley (2/5,2/5,2/5)              tangent (1,1,1)
    n=6 record (7,14,1,−5)                       TWO tangents
    n=8 1891                                     two aligned directions

`tight_set.py` passes the first FOUR of these and **fails the fifth**: at the
n = 6 record it returns null dimension 1 where two independent tangents are
verified, and neither lies in the space (projections 0.6018, 0.6194). So its
zeros at the two 67s are evidence, not proof, and Postscript [100](LEDGER.md#p100)'s closure of
the n = 3 multi-cube gap is reopened.

`edgecross.py` solves an unrelated condition set — preservation of the real
edge-edge crossings, a purely geometric incidence — and produces the IDENTICAL
null space at all nine configurations (principal angles 0°, despite 90 crossings
against 108 tight quantities at n = 4). Step-A tightness and edge-crossing
preservation are the same linear condition. It therefore fails at the record for
the same reason, and the failure is a fact about the record rather than a bug in
either formulation: there the count-preserving directions destroy crossings and
the crossing-preserving direction does not hold the count. Everywhere else
tested, the crossing null space CONTAINS the true tangent — so crossing
preservation is necessary for the count on every maximiser except the one that
sits at a node.

**The asymmetry to remember.** A POSITIVE result — a direction that verifies —
is self-certifying. A zero never is.

## 13a. A control chosen because it is convenient tests nothing

**The rule.** Passing a control only licenses the zeros if the control was HARD
for the method. Pick the control that stresses the assumption you are least sure
of; a control that every plausible version of the method would pass is a
formality, not a check.

**Demonstration (2026-08-06), three attempts at one direction scan.** The
question was whether any single-cube direction preserves 183 at n = 4. Attempt 1
scanned 290 primitive integer triples |uᵢ| ≤ 3 in the body chart q → q·(1,εu) and
read 0 of 870. Attempt 2 rescanned the world chart (1,εu)·q and read 0 of 870.
Both were void, for two INDEPENDENT reasons:

* **chart** — a direction that is an integer triple in one chart is not one in
  another, and every tangent this project has verified is integral in the CAYLEY
  chart and no other;
* **range** — |uᵢ| ≤ 3 does not contain 727 arc A's tangent (1,−3,−6) or arc B's
  (1,1,−4), so two of the four known tangents were never candidates at all.

**Neither defect was detectable from the controls used**, which were n = 2's
(1,1,0) and (1,1,1) and 723's (1,1,1). Those three are axis-parallel, so every
chart agrees on them and the chart defect is invisible; and they are the smallest
integer triples in existence, so they lie inside any search set and the range
defect is invisible. The controls passed both times while the method was broken
both times.

**The repair.** Cayley chart, |uᵢ| ≤ 6, control 727 arc A — whose tangent
(1,−3,−6) is in general position and outside the old range. It returns exactly
±(1,−3,−6), **2 of 1 730 directions**, and nothing else. Only then do the zeros
mean anything: n = 4 reads 0 of 3 460 and n = 5 reads 0 of 6 920.

**How to pick one.** Rank the available controls by how much they differ from
the easy case along the axis the method could plausibly be wrong about — chart
dependence, search range, tolerance, symmetry — and use the extreme one. In this
project that ordering is:

    (1,1,1) at n=2 or 723   trivial: axis-parallel AND minimal
    (1,1,0) at n=2 mirror   axis-parallel
    (1,1,-4) on 727 arc B   general position, range 4
    (1,-3,-6) on 727 arc A  general position, range 6
    the n=6 record          two tangents at a node, neither in any null space yet

A method that only passes the first line has been tested against nothing.

## 14. Agreement between samples certifies a SHARED CELL, not a correct one

A face's count is the count just outside the vertex. Measured by stepping, the
rule "shrink the step until two consecutive values agree, then take that value"
looks like convergence and is not: **both steps can land outside the intended
cell, in the SAME wrong cell**, and their agreement then certifies only that
they share a cell.

Cost of learning it: 2026-08-17, the golden 67. The rule misassigned **36 of
2 196 faces** and reported counts 33, 34 and 35 that do not occur anywhere in
the true face set. It was caught only by rebuilding the measurement with an
infinitesimal step (`cube_regions_eps`, [Postscript 119](LEDGER.md#p119)), which
has no step size to be wrong about.

Same family as [mode 2](#2-a-gate-that-cannot-fail): two things agreeing is
evidence they share assumptions, not evidence either is right. The tell is that
the agreeing quantities are both OUTPUTS of the same possibly-wrong procedure,
with nothing external anchoring either.

Note which case exposed it. The octahedral 67 — 6 independent walls, a simplicial
arrangement, wide faces — agreed perfectly under both methods. Only the golden
67 — 9 dependent walls of rank 6, narrow faces — disagreed. **The convenient
control passed and carried no information; only the awkward one did.**
See [METHODS §4](METHODS.md).

## 15. A caveat field you designed, and then did not read

`isolation67.py` was deliberately built with a three-valued verdict — isolated /
not isolated / **isolated on evaluated faces** — precisely so unevaluated faces
could not be silently scored as "< 67". It printed `ISOLATED on evaluated faces`.
The run summary then reported "both 67s isolated", and the 333 unevaluated faces
of 2 196 reached the user only because they read the log line and asked.

The mechanism worked. It was not consulted. Building the caveat is the easy half;
the failure is in reading your own output charitably instead of adversarially.

**Standing rule.** An unevaluated count belongs in the HEADLINE of a result, not
in its detail. If a field was designed to carry a caveat, read that field first,
before the verdict — and quote it verbatim rather than summarising it, since
summarising is exactly where "on evaluated faces" was lost.

## 16. A refusal caused by the REPRESENTATIVE, misread as a limit of the tool

When a computation is refused — overflow budget, precision limit, timeout — the
reflex is to reach for a bigger instrument. Ask first whether the INPUT had to be
that expensive.

Cost of learning it, 2026-08-18. Enumerating the 24 local chambers around the
727 record's sixth cube, **10 of 24 came back unevaluable**: the engine rejected
them for exceeding its joint overflow budget (component magnitude up to 13 528
against a limit near 512). The obvious reading was that the neighbourhood needed
a wider engine, and the result was written up as 42% unmeasurable.

The split by witness height gave it away — no overlap at all:

    evaluated   (14)   max |component|  1 … 178
    UNEVALUABLE (10)   max |component|  2 865 … 13 528

A chamber is a CONE, represented by ANY interior point. Fourier–Motzkin's
back-substitution took the midpoint of each bound pair, and midpoints of
rationals with unrelated denominators compound through the recursion. Replacing
the midpoint with the SIMPLEST RATIONAL in the interval (continued-fraction
descent) dropped the maximum height to 178 and **all 24 chambers evaluated, 0
unevaluable**. The counts confirmed the partial result rather than revising it —
{715: 4, 711: 10} became {715: 8, 711: 16}, each value exactly doubled as the
antipodal partners filled in.

The geometry was never the obstacle; the representative was. Same family as
[mode 14](#14-agreement-between-samples-certifies-a-shared-cell-not-a-correct-one)
and the ε-step problem: in both, an arbitrary choice inside the method was
mistaken for a property of the object.

**Standing check.** Whenever an object is defined only up to an equivalence — a
cone's interior point, a direction's scale, a class representative, a basis — the
cost of the representative is a FREE CHOICE. A refusal traceable to that cost
bounds the choice, not the question. Before widening a tool, measure the input's
height and ask whether a cheaper representative exists.

### 16a. Addendum, same day: mode 2 reproduced within hours of writing mode 16

Testing whether the octahedral 67's face counts respect its order-24 symmetry, the
check written was "is every count multiplicity a SUM OF DIVISORS of 24?" It passed
on both 67s, at every codimension, on every count — **because 1 divides 24, so
every positive integer qualifies.** A 100% pass rate on a predicate with no
discriminating power.

The opposite check is no better: not one multiplicity is divisible by 24, which
looks damning until 728 = 3^6 - 1 = 24*30 + 8 is noticed. A group of order 24
acting on 728 objects MUST have small orbits, so non-divisibility is forced by
arithmetic and carries no information either.

**Both directions of the cheap test are worthless, and the expensive one is
required**: compute how each symmetry permutes the walls, decompose the faces into
genuine orbits, and check whether the count is constant on each.

The lesson is not new — it is [mode 2](#2-a-gate-that-cannot-fail), written up in
this same file. Writing a failure mode down does not immunise against it. Before
believing a pass, ask what input would have produced a FAIL; if none exists, the
test is decoration.

## 17. A delegated agent that parks on its own background job

Three agents launched the same afternoon (2026-08-18) each returned, as their
FINAL ANSWER, a sentence of the form "waiting for the calibration run to complete
before proceeding". None reported a number. Each had written a correct, gated
script and then backgrounded it, set up a monitor, and stopped.

The specs said "budget roughly 40 minutes", which was read as permission to set up
long-running infrastructure rather than as an instruction to finish. One agent ran
its own campaign for 90 seconds against a specified 40 and called that a
calibration.

This is [mode 12](#12-delegation-specific-premature-parking) with a new trigger:
not stopping early on difficulty, but stopping early on ITS OWN asynchrony. The
agent's work was fine; the handoff was empty.

**Fix, in the spec:** *run it to completion in the FOREGROUND and report the
numbers. Do not background the work and wait for it.* Say what the deliverable is
in the reply -- "report back the histogram and the best count" -- so a status
sentence cannot satisfy it.

**Recovery, when it happens:** the scripts are usually correct and already
gate-passed. Running them yourself is cheaper than resuming the agent, which
re-derives context to reach the same place.

## 18. A wrong answer that raises nothing, in a tool built for a case with no known answer

`stream_chambers.py` was written to remove a memory ceiling, and validated against
the one case with a known answer: 183, which has exactly 1 712 chambers. It
returned **0**.

The cause was in the first line of the first stage. The whole space is the EMPTY
sign vector; it was serialised as an empty line; and the reader skipped empty lines
as blank padding. So stage 0 yielded nothing, every subsequent stage was empty, and
the function returned a number without raising anything.

**The point is where this tool was headed.** It exists for 727, where the chamber
count is unknown — that is the entire reason to build it. A silent 0, or worse a
plausible non-zero undercount from the same class of bug, would have been accepted
there because nothing existed to contradict it. The known-answer case is the ONLY
place the bug was visible, and it was visible instantly.

**Standing rule.** A tool built for a case with no known answer must be validated on
a case with one, BEFORE it is pointed at the unknown. If no such case exists,
construct one small enough to check by hand. "It ran and produced a number" is not
a result; it is the failure mode.

Related: [mode 2](#2-a-gate-that-cannot-fail) — there the test could not fail; here
the tool could not report failing.

## 19. The specification is the one artifact not kept

**Symptom.** A delegated program is in the repository, its report is in the
repository, its numbers are cited in the ledger — and what the agent was actually
asked to do exists only in a session transcript.

**The measurement, 2026-08-20.** Across all sessions of this project: 65
delegations. `DELEGATION_LOG.md` describes 8 of them (12%). `specs/` holds 27
specification files, the newest dated 2026-08-13 — while 13 agents were spawned on
08-18 and 08-19 with no spec written for any. 08-18 was the heaviest delegation day
of the project at 9 spawns. **The rate of delegating went up as the recording of it
went to zero.**

The asymmetry is the tell. Agent *output* was already being made durable and it
worked: 30 `*_report.md` files are in the repository and 24 of them are cited in
`LEDGER.md` or `RESULTS.md`. Only the input side lapsed. Nobody decided to stop —
which is why nothing announced it.

**Why the defect hides.** A spec can be wrong in ways the delivered code cannot
reveal, so the spec is the only place the defect is visible, and it is the one
thing not kept:

- **The gate was vacuous.** Three times here, most sharply in
  [16a](#16a-addendum-same-day-mode-2-reproduced-within-hours-of-writing-mode-16):
  the specified check was "is every multiplicity a sum of divisors of 24?", which
  every positive integer passes. The agent complied exactly. The delivered code was
  correct. The *specification* was the error, and reading the code will never say so.
- **A budget read as permission.** "Budget roughly 40 minutes" produced three agents
  that built infrastructure and reported status instead of numbers
  ([mode 17](#17-a-delegated-agent-that-parks-on-its-own-background-job)). That is a
  wording defect, diagnosable only against the wording.
- **A requirement silently dropped.** `growth727.py` was specified with a `__main__`
  guard and delivered without one, so importing it re-ran the campaign. Against a
  spec on disk: a one-line diff. Against a prompt: a transcript search nobody runs.
- **The spec drifted between attempts.** `exactlp.py` was commissioned three times in
  one day with prompts of 4 046, 3 789 and 4 070 characters. Nothing on disk records
  which version the surviving code was built to.

**The compounding error.** `DELEGATION_LOG.md` — the file created to fix exactly
this — asserted in its own opening paragraph that specs are recoverable from
neither the exports nor the per-agent transcripts. Half of that was false: every
agent transcript carries the full prompt as its first user message. A document
whose purpose was to preserve specifications contained the sentence that made
preserving them look impossible. Same shape as the superseded claim that survived
longest inside the SUPERSEDED-CLAIMS TABLE: **the mechanism built to prevent a
failure is where that failure lives longest**, because nobody audits the auditor.

**Standing rule.** Write `specs/X_SPEC.md` before spawning and spawn with "build to
`specs/X_SPEC.md`". The spec is then a repository file both sides cite, so the
instruction and the record cannot drift apart, and the spec can be reviewed as an
experimental design *before* an agent spends an hour satisfying it. Apply
[mode 2](#2-a-gate-that-cannot-fail) to the spec itself while writing it: name the
input that would make each gate FAIL. If no such input exists, the gate is
decoration and the delegation will confirm nothing, however well it is executed.

**Recovery.** Prompts are recoverable from
`~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl` (first user
message) and from the main session's `.jsonl` as the `Agent` tool-use input. They
are NOT in `/export` output. Backfill by the criterion already used for reports: a
spec is worth saving when its output is cited.

## 20. A test run writing to the production output path

**What happened, 2026-08-20.** `exactlp.py` had just been changed to take its
sampling distribution as run-time parameters. A 120-trial smoke test confirming
the new `key=value` overrides worked wrote its report to
`exactlp_report_random.json` — **the path holding the completed 2 500-trial
validation**, which had no other copy. The smoke test passed. The data it landed
on was gone.

**The defect was not carelessness, it was an unparameterised path.** The output
location was computed as `exactlp_report_%s.json % phase` with no way to
redirect it, so *every* invocation of the program — a real campaign, a
three-trial syntax check, a demonstration in a reply — aimed at the same file.
Under that design a test run cannot be made safe by intending it to be safe.
Note the irony precisely: the edit being tested was the promotion of magic
numbers to parameters, and the magic value that did the damage was the one not
promoted.

**Why the usual guard did not apply.** `provenance.py` protects against this
where it runs — `reproduce()` copies the cited output aside and restores it in a
`finally` — but that guard lives in the reproducing harness, not in the
producing program. Any program that writes a result is one careless argument away
from this unless the destination is an argument too.

**Standing rule.** A program that writes a result takes its output path as a
parameter, and any exploratory, smoke, calibration or demonstration run passes an
explicit throwaway destination. Never let the convenient invocation be the
destructive one. Corollary for this project's own habit: *documents are living,
data is immutable* is a rule about intent, and intent does not defend a file — an
argument does.

**Recovery, and why it existed.** The run was reproducible because the seed was
fixed (`seed=20260820`) and the edits had not touched the RNG call sequence or the
sampled defaults, so re-running regenerated the same trials. That is the whole
value of a recorded seed, and it is the second time on this project that a fixed
seed converted a loss into an inconvenience. Timing fields (`wall_s`, the ratio
and duration percentiles) do not reproduce exactly and are honestly different
numbers from a different machine state.

Related: [mode 7](#7-reporting-before-persisting) — there the result never reached
disk; here it reached disk and was then overwritten by a test of the writer.
