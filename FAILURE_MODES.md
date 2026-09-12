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

### 11e. A monitoring command that fabricates the number it reports

`ps -o rss= -ax -p 54542,54543,54544,54545 | awk '{s+=$1}'` reported the four
393 workers holding **16.18 GB** on a 16 GB machine. They were holding 0.24 GB.

`-ax` overrides the `-p` filter, so the sum ran over EVERY process on the
machine. The number was not wrong by a little; it was a different quantity
wearing the right units, and it landed on a plausible value for the failure
already feared. Both facts made it convincing.

The near-miss: this was one sentence away from being reported as a second
out-of-memory event, which would have been the FOURTH wrong diagnosis of a
stoppage on this project (dispatch deadlock, external kill, chamber list, and
this) -- each named from a single reading.

**Two checks, both cheap.** Cross-measure with a different command shape before
believing an alarming aggregate: `for p in $pids; do ps -o rss= -p $p; done`
disagreed instantly. And sanity-check the total against its parts -- 16.18 GB
across four processes is 4 GB each, which no other reading supported.

**The general form.** A measurement that CONFIRMS the thing you are already
watching for deserves more scrutiny than one that contradicts it, not less. Same
family as [mode 2](#2-a-gate-that-cannot-fail): there a test could not fail; here
a monitor could not report calm.

**Second instance, 2026-08-22, opposite direction.** `pgrep -fl python3` and
`ps -ax | grep python3` both returned NOTHING while five processes were running,
including a 99.9%-CPU derivation. Cause: the Homebrew framework binary is named
**`Python`**, capital P -- `python3` is only a symlink used to launch it, and
never appears in the process table. Reading the empty result as "the jobs died", a
memory-pressure explanation was then constructed around swap usage that had
nothing to do with it, and reported to the user as fact. The user corrected it
with "5 python processes running".

So the same command lied in BOTH directions within two days: over-reporting 16 GB
when the true figure was 0.24 GB, and under-reporting five live processes as zero.

**Third instance, 2026-08-24, and the cheapest of the three to have avoided.**
`uniform_test.py` was launched on the remote box and reported to the user as
running, twice, across two separate turns. It had crashed **at startup**: the code
sync carried `*.py` and `*.md` but not `stream_727/`, so the input files it reads
were absent and it died on `paths[0]` with IndexError before printing anything past
its banner. The launch command had printed a PID, and that PID was taken as
evidence of work. A PID means a process STARTED, not that it is running or doing
anything.

The independent check that was supposed to arbitrate a disputed number therefore
contributed nothing for hours, while being cited as pending.

**Standing check.** A process monitor must be validated against a process you KNOW
is running before its silence is believed. And a launched job is not a running job:
read its OUTPUT once, a few seconds after launch, before telling anyone it is
under way. When work is moved to another machine, the inputs move too -- verify by
reading the first lines of output, not by observing that a command returned. `ps -ax -o command | grep -i` (case
insensitive, full command, no assumption about the executable's name) is the
version that works here. An empty result from a monitor is a claim like any other
and needs the same evidence as a non-empty one -- ABSENCE IS A MEASUREMENT.

Companion observation from the same minute: the run's log had not advanced in
90 seconds while CPU sat at 98%. That was print granularity -- progress prints
every 200 candidates and 192 remained. **Slow, hung, killed and out-of-memory all
present as silence.** Check RSS, %CPU, and whether the OUTPUT FILES are still
growing before naming a cause; `wc -l` on the checkpoints settled it in one
command.

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

### 16b. Addendum, 2026-08-24: "scale to integers" is denominator COMPOUNDING, not simplification

Evaluating region counts on 727's chambers found **47% unevaluable** — the engine
refusing witnesses produced by the LP. The tell was mode 16's exactly: evaluable
witnesses had median height 1.1e7, unevaluable ones 3.1e9, a 276x separation by
SIZE rather than by anything about the chamber.

A chamber is an open CONE, so any positive multiple of a witness is equally valid.
That looked like a free fix: clear denominators, divide by the gcd, get an integer
point. Measured, it made things **worse** — evaluable fell from 50% to 18%, and
median height ROSE from 1.4e8 to 3.0e10.

Clearing denominators multiplies by the LCM over 15 coordinates whose denominators
are unrelated, and those compound exactly as midpoints did in mode 16. A
Fraction's height is max(|num|,|den|); the integer obtained by clearing every
denominator at once is far larger than any single coordinate's height.

**The lesson is narrow and worth stating exactly:** "make it an integer" and "make
it simple" are different operations, and on a vector of unrelated rationals they
point in opposite directions. The documented remedy still stands — choose the
SIMPLEST rational in the admissible range per coordinate (`_simplest_between`),
verifying the sign conditions exactly — and it is real work, not a one-liner.

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

### 16c. Addendum, 2026-08-31: a refinement sweep whose refusals turned a plateau into a point

Asking whether the n=6 rung 1217 sits on a plateau or a single point, the first sweep
along its solved 13-pair curve stepped by 4/63 and found the count 1217 at **1 of 19
offsets** — the recorded one. That reads as an isolated maximum, and it was reported
as one.

The refinement built to check it stepped by 1/5000 and 1/50000 around the recorded
t. It returned **"1 offset within budget, count==1217 at 1"**. Those two numbers are
the whole failure: 60 of 61 offsets were never evaluated, because a t with a large
denominator canonicalises to a quaternion whose components exceed the narrow
engine's 512 cap. The sweep confirmed nothing and looked like confirmation, because
the surviving point was the one already known.

On the wide engine the same line reads:

    step 1/630     17 offsets   1217 holds at  9
    step 1/6300    13 offsets   1217 holds at 11
    step 1/63000    9 offsets   1217 holds at  9

**1217 is a continuum**, extending over t in [-59/315, -11/63] at minimum. The
original step of 4/63 is 40x the plateau's width, so it could not have landed inside
twice; the "isolated point" was the step size, not the geometry.

Three modes composing, all of them already in this file:

- [mode 16](#16-a-refusal-caused-by-the-representative-misread-as-a-limit-of-the-tool):
  the refusals were caused by the REPRESENTATIVE — offsets chosen with denominators
  5000 and 50000 rather than multiples of the recorded 1/63 — not by the object.
  The tell was mode 16's own: the split was perfectly clean by input height.
- "unevaluable is not a negative result" (investigation-principles): 60 unevaluable offsets were scored as agreement with the coarse sweep.
- [METHODS 1](METHODS.md#1-solve-the-line-do-not-sample-it) / solve don't sample: the curve
  was SOLVED and the extent was SAMPLED, and only the sampled half was wrong.

**The rule this adds.** A refinement sweep must report its evaluated count in the
same breath as its result, and a refinement that evaluates FEWER points than the
sweep it refines has failed, whatever it returns. Choose offsets in the recorded
point's own denominator (here 1/630, 1/6300 = multiples of 1/63), not in round
decimal denominators, which compound against every cap in the pipeline.

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

### 19a. Addendum, 2026-08-31: the RUN was not kept either

[Mode 19](#19-the-specification-is-the-one-artifact-not-kept) is about specifications.
The same gap swallowed a 3 216-second measurement.

The n=10 arrangement job — the one testing [P172](LEDGER.md#p172)'s linear wall law —
was launched from an inline heredoc. It wrote `n10_arr.log` and exited 0, leaving:

    n=10: walls 101  ambient 27  rank 22  DEFICIT 5   (3216s)
    P172 predicted: walls 123 ... PREDICTION: REFUTED

and **no file in the repository that could produce those numbers again**. Worse than
irreproducible: the log does not record its own INPUT, and at n=10 the input is
exactly the thing in question — `R[9]` ends in (56,56,55,56) while P181's n=10 is
built on (57,57,56,57), a different member of the same continuum. A reader cannot
tell from the log whether the law was refuted or never tested.

An hour of compute produced a headline ("PREDICTION: REFUTED") that could not be
checked, defended, or corrected. `arr_tower.py` now does the measurement from a saved
file, gated on reproducing P172's n=9 row, and computes the k=57 row that decides
which of the two readings is right.

**The rule.** A run long enough to be worth reporting is long enough to be worth
saving first, and its output must name its own input. "Deliverables go where they
survive" covers the script; this adds that the LOG must carry the configuration, not
just the result — otherwise the artifact that survives cannot be interpreted.

### 19b. Addendum, 2026-09-01: saying "this belongs in X" is not putting it in X

Twice within ten minutes, and both caught by the user rather than by me.

Writing OQ 18, I recorded two routes to a smaller ceiling bound under the heading
"Related, and NOT this question", with the sentence that they "belong with their
questions or in MAXIMISER_TAXONOMY §5". I did not put them there. `grep` on §5 returned
**zero** mentions of either. So they existed only as a pointer inside a question that
explicitly disclaims them — named, disowned, unrecorded.

Then, having filed them, I wrote that the convergence of both routes on CONCENTRICITY
was "worth noting on its own", and that I would "flag" having made the first mistake.
Neither was written anywhere. Both existed only in conversation until the user asked
"has the point worth noting been noted? has the flag been flagged?"

**This is [the record-propagation principle](../.claude/investigation-principles.md)
one level up.** That principle says writing a correction into the record feels like
completing the correction while the summary still carries the old claim. This is the
same substitution applied to filing: **naming the destination feels like delivering to
it.** The tell is a sentence of the form "this belongs in X" or "worth noting" or "I'll
flag that" — every one of which is a description of an action standing in for the
action, and every one of which reads as completed work in a transcript.

**The rule.** If a sentence names where something should go, put it there in the same
turn or do not write the sentence. "Worth noting" is not a note.

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


## 21. The point-to-object MAP was never gated, only the engine

`evaluate727.py` and `walk13.py` produced tens of thousands of region counts that
were all wrong, because a chamber witness `y` is a DISPLACEMENT from the record
point `pt`, and both scripts evaluated `count_at(y)` instead of `count_at(pt + y)`.
P163 is retracted in full.

**What was gated, and what was not.** The engine was gated properly: `--n 7 --seed
777` returns 973, the documented value, on both machines. The witness simplifier
was gated: evaluability 50% -> 100%. The arrangement was gated: 4 621 728 chambers
by two independent methods. **The map from a point of the arrangement to a cube
configuration was never gated at all** — and it is the one component that sits
between all the others.

**The check costs one line and would have caught it instantly:**

    count_at(point_of(record)) == 727      # the record, by definition
    count_at(origin)           == 13       # what the broken path was measuring

**How it hid.** The wrong counts were plausible: in range, mostly odd (matching a
real parity law), varying smoothly, with a maximum below the record — exactly what
correct output would look like. Two REAL findings were then built on them: "no
chamber approaches 727" and "99.65% of counts are odd". Both are artifacts.

**The tell that was visible and mis-read for an hour.** The count was not constant
within a face — three points of one face gave three different values, 0 of 24 faces
agreeing. That is impossible if the walls are the coincidence conditions, so it was
proof of an apparatus fault. It was first blamed on the gauge quaternion (a real
but secondary bug), then on the arrangement being a tangent cone (a plausible and
wrong theory). Only the origin check settled it.

**Standing rule.** Gate every ADAPTER, not just every engine. Wherever one
representation is converted to another — arrangement coordinates to configuration,
sign vector to witness, flat to subspace — there is a known value on both sides of
the conversion. Evaluate it. A pipeline of individually gated components is not a
gated pipeline.

## 22. A sampled termination test read as a decision

`climb.py` ended with "no crossing above the record; region is locally maximal OVER THE
DIRECTIONS WALKED". The hedge is accurate and was written deliberately — and it did not
help. The terminal counts were still used as terminal counts, a basin histogram was
built from them, and the sentence "6 of the first 8 random starts were already local
maxima" was reported to the user. Re-tested against exactly-solved lines, **3 of those 8
terminations were premature.**

The lesson is not "hedge harder". A search procedure and a decision procedure are
different objects, and a hedge in the log does not convert one into the other. If a
result will be USED as a decision, the test has to be a decision — here, walls solved
rather than rays sampled. The tell: a stopping condition whose statement contains the
name of the method ("over the directions walked", "within the sweep window", "up to the
budget"). That phrase marks a lower bound, and a lower bound must not be histogrammed.

Related: FAILURE_MODES 16c (refusals turning a plateau into a point) and the standing
rule that a sampled count is a lower bound and a solved one is not.

## 23. A statistic measured on my own recomputation, not on the statistic

The Möbius-weight predictor was declared unusable because it cost 3.8x a count. Then the
catalogue turned out to record exactly what it needs — `real_pts.append((s, len(on),
len(cubes_on)))`, the point, its multiplicity, and a face test already applied — so the
information was free and only my recomputation was expensive. That hope was also wrong:
reading it from the catalogue costs **14x a count**, worse still, because the catalogue
computes a bounded box search and all crossing lines besides. The negative survived, but
it was nearly overturned on a guess and then re-confirmed by measurement rather than by
the original reasoning.

Still open and flagged rather than smoothed: the two statistics **disagree, r = −0.049**,
while both order the count at 86–90 %. Two supposedly equivalent measures of one quantity
cannot be uncorrelated; one is not measuring what I think.

## 24. A gate that caught a fast, plausible, wrong engine

The first incremental counting engine compiled, ran **5.2x faster at n=10**, and was
wrong: it returned the base's own count for every candidate after the first. Cause —
`exact_count_config` calls `verts.clear()` on entry, so restoring the base by
`verts.resize(g_baseVerts)` refilled it with default-constructed vertices and every saved
cell indexed into zeros. The speedup was measuring skipped work.

The equivalence gate — 75 configurations at n=4, 7 and 10, counted both ways — caught it
immediately: 3 of 75 agreed. After saving the vertex DATA rather than its length, 75 of 75
agree and the honest speedup is 2.6x at n=10, half what the broken version advertised.

**The tell, and it is general: a performance win that exceeds its own prediction.** The
base-share measurement predicted at most 3.4x; the broken engine reported 5.2x. A speedup
larger than the work you believed you were skipping means you are skipping work you did
not intend to.

## 25. Two ratios conflated inside one sentence

[P223](LEDGER.md#p223) was written claiming the incremental engine was "the one lever with
70x-scale headroom". 70x is the SOLVE-versus-COUNT ratio and has nothing to do with
incremental counting, whose headroom is the base share — 2.4x at n=5 rising to 3.4x at
n=10. Both numbers were measured in the same session, minutes apart, and were joined by
nothing but proximity. Corrected before the claim was used anywhere.

## 26. An enumeration run without a gate, and a symmetry claimed without checking it

The n=5 record family (hub + one cube per body diagonal, [P225]) was swept over 66 045
angle tuples and returned **best 375, 0 bases at >=385**. The 393 is IN that family by
construction, so the negative was void before it was printed.

**The reduction was wrong.** I argued: the cube's rotation group acts as S4 on the four
body diagonals, and conjugation preserves a rotation's angle, so permuting which diagonal
carries which angle gives a congruent compound -- hence only sorted 4-tuples need
evaluating, 24x fewer. Both premises are true and the conclusion does not follow. The
action is not free on the SIGNED structure: a rotation permuting diagonals can reverse
orientations, sending t to -t on some of them, so permuting angles alone is not the group
action. Measured directly afterwards: the 24 assignments of (-5,-3,5,5) give **two**
counts, 341 and 393, and the sorted tuple gives **341**. Sorted-only discarded exactly the
arrangement that reaches the record.

**Two separate failures, and the second is the one that cost the hour.**

1. A symmetry argued from plausible premises and never tested. One command -- count all 24
   permutations of a known-good tuple -- would have refuted it in seconds, before the
   sweep. Testing a claimed symmetry is cheap precisely because a symmetry makes a
   prediction: the counts must agree.
2. **No gate.** The campaign had an obvious one available -- it must rediscover the 393 --
   and [P186] had already taught this project exactly that lesson on the arc sweeps, where
   the gate was the thing that made the negatives real. I wrote the sweep without one, got
   a negative, and only checked afterwards.

Compounding it: the FIRST gate I then wrote was also wrong. It found the first
(diagonal, t) pair expressing each cube and asked whether that particular t was in the
swept set -- but the C3 orbit of 1/4 is {1/4, 5, -3/7} and the sweep keeps 5, the same
cube. The gate reported failure for a family that did contain the target. A gate is code
and can be wrong; it needs its own sanity check, which here is "does it pass on a case
known to be good".

The rerun puts the gate FIRST -- it reproduces the 393 exactly, or exits -- and drops the
reduction, trimming the angle set instead. Trimming is honest (the negatives are then
about a stated set); an unchecked symmetry is not.

## 27. A statistic that was a function of the SPELLING, not the object

`concurrence.planes()` built each cube's six face normals from the ROWS of its rotation
matrix. In world coordinates the face normals are the COLUMNS; the rows are the normals of
the inverse rotation. Every plane-incidence signature this project computed — the whole
`signature.py` / `realsig.py` / `signed_sig.py` line, and the `sig` column of a 3 135 491-row
census — therefore described a real compound that was not the one being measured.

**The gate costs one loop, and it is forced by the objects themselves.** A cube is
invariant under the 24 rotations of the octahedral group, so `q` and `q·s` are two names
for the SAME cube. Any honest function of the compound must be constant along that orbit.

    for s in OCT:  assert signature(respell(cfg, s)) == signature(cfg)

Broken code: **6 of 6** respellings changed the signature. Corrected: **0 of 96**. The
gate is now permanent — it runs on every `python3 concurrence.py`.

**What it cost**, and the size is the point: the census's signature column (3.1M rows), a
Chao1 richness estimate built on it, the claim that the n=4 record carries a 9-fold plane
concurrence (it carries **6**, and the shared-axis 161 carries 8 — so the record is BELOW
the configuration the statistic was invented to rank above it), a 1 500-configuration
construction aimed at that phantom 9-fold, and [P222]'s best-ever count predictor, whose
correlation did not shrink but **changed sign**, from r = +0.562 to −0.147, with ordering
falling from 77.6 % to 50.6 % — chance. See [P227].

**Why it survived so long.** Every internal consistency check passed. The signature was
deterministic, exact (integer planes, exact rational intersection points, no tolerance
anywhere), reproducible, and correlated with the count well enough to look like a finding.
Two implementations would have agreed, because both would have read rows. Nothing inside
the method could see it: the anchor had to come from a symmetry of the INPUT, which is
outside the method by construction.

**Standing rule, and it generalises past this project.** When a statistic is computed from
a REPRESENTATION of an object — a quaternion for a rotation, a basis for a subspace, a
coset representative, a chart — gate it against the representation's own redundancy group
before believing one number it produces. The redundancy group is usually known for free and
usually small; here it was 24 elements and one loop. This is [FAILURE_MODES 21]'s rule
("gate every ADAPTER") pointed at the other end of the pipeline: 21 is about the map INTO
the object, this is about a map OUT of it, and both are invisible to a correct engine.

**Corollary about correlation as evidence.** r = 0.562 across half a million configurations
felt like strong evidence that the statistic meant something. It was strong evidence that
the statistic was not noise — and the inverse rotation of a compound is not noise. A
statistic can be highly structured, highly reproducible, and about the wrong object.

### 27a. The correction's own evidence was a single sample — and the second one contradicted it

Same day, inside the fix for 27. Reporting the damage, I wrote that per-ensemble signature
richness *"moves in BOTH directions (`chain` 34 → 102, `axis` 93 → 89), so no scale factor
repairs the table"*, and propagated that sentence into four documents.

It came from one 3 000-row resample computed inline, whose script was not kept. Writing
`resig.py` so the correction would be reproducible produced a second sample — and `axis`
moved the **other** way (74 → 77), as did `twoaxis` (129 → 120 becomes 115 → 126). Only
`chain` is resolved: it roughly triples in both. The predictor figures agreed across the two
runs (r = −0.184 / −0.147, ordering 52.3 % / 50.6 %), which is why the headline claim was
right; the per-ensemble directions did not, and I had quoted the directions as evidence.

**The conclusion was right and its stated evidence was noise.** "No scale factor repairs the
table" is true because the table has not been re-measured — not because a direction was
established. Those are different claims and only the second one needs data.

**Three things this says that 27 does not.**

1. **A correction is a result and gets a result's discipline.** The bug it corrects makes
   the correction feel like the careful part of the work. It is not; it is new measurement,
   made in a hurry, usually on a smaller sample than the thing being corrected.
2. **The script that produces a quoted number must exist before the number is quoted.**
   Run 1 was inline. Had it been a file, run 2 would have been a re-run with a different
   seed — five seconds of thought — instead of an accident of rewriting it for
   reproducibility. [METHODS 12](METHODS.md), and this project has now paid for it twice.
3. **Two samples that agree on the headline can disagree on the detail**, and quoting the
   detail as support for the headline reads as more evidence than there is. The honest form
   quotes both runs, which is what [P227](LEDGER.md#p227) now does.

## 28. A regenerator that reported success while dropping the newest entries

The ledger's index had stopped at Postscript 146 while the file had reached 229 — the table
of contents of the document every other file cross-references into, 83 entries behind. It is
generated by `index_ledger.py`, so I ran it.

**It made things worse, and said it had worked.** It printed
`indexed 232 postscript blocks; 232 distinct anchors` and wrote an index that (a) omitted
every postscript from 220 on and (b) replaced 146 working `#pN` links with GitHub heading
slugs. Two format drifts it predated:

* Headings acquired status tags — `## [VERIFIED] Postscript 229: …`. Its regex began at
  `Postscript`, so every tagged block failed to match and was skipped. By 2026 that was all
  the recent ones, i.e. exactly the entries the regeneration was for.
* The body acquired explicit `<a id="pN">` anchors, and every cross-reference in every other
  document points at those. A slug is a function of the heading TEXT, so re-tagging one
  heading `[PARTLY RETRACTED]` — which had happened that same day — silently breaks its
  link. The stable anchor was sitting one line above the heading, unread.

**The tell was in its own output and I did not read it.** 232 blocks for a file with 274
postscript headings. A generator that reports a count has already computed the number that
would have caught it; nothing was comparing it to anything.

**Fixed:** strip the tag, prefer the explicit anchor, fall back to a slug only where none
exists — and **gate it**: if the number of blocks indexed is less than the number of
postscript headings in the file, refuse to write. Now `indexed 274 of 274 … (225 explicit
<a id>, 49 slugs)`, and the index runs 1–229 with zero dangling explicit links.

**Standing rule.** A tool that regenerates a derived artifact wholesale must assert its
output covers its input, not merely report a count. Wholesale replacement is what makes
silent narrowing possible: an appender that missed a case leaves the old entries alone; a
regenerator deletes them. Same shape as [FAILURE_MODES 2](#2-a-gate-that-cannot-fail) — a
success message is not a check — and the reason this one bit is that the format the tool
parses had been evolved by the same process that keeps the document alive.

### 27b. I applied 27's own lesson to one of three statistics, and scored the other two as refuted

Written the same day as 27, about what happened four hours later.

[P227] voided three count predictors at once, because all three came from the broken face
normals. `resig.py` re-measured **one** — the Möbius weight — found it at chance, and I
wrote *"there is no predictor"* and *"this project has no cheap non-circular count
predictor"* into five documents.

Re-measured on the full census ([P231](LEDGER.md#p231)), **max plane-concurrence orders
61.1 % of pairs, ~78σ from chance**, and carries enough enrichment to make filtering pay at
1.81×. It is the statistic I never re-ran. The one I did re-run is the only one of the three
that is genuinely worthless.

**Two unevaluated entries were reported as negative results**, in a project with a standing
rule titled *unevaluable is not a negative result*, hours after I added the failure mode
about gating statistics before believing them. The rule was known, written down, and
restated by me that morning.

**Why it happened, since "be more careful" is not a mechanism.** The three statistics shared
a cause of death, so they felt like one item. Voiding them was a single act; re-measuring
them was three acts, and finishing one felt like finishing the class. The tell was visible in
my own postscript: its table had three rows and its conclusion had one.

**Standing rule.** When a single fault voids N results, the correction has N parts and is not
complete at part one. Write the count in the correction — *"three statistics are void; one
has been re-measured, two have not"* — because a table of three rows under a sentence about
one is not a discrepancy anyone notices, including its author.

## 29. Six scales agreeing, and all six measuring the direction set

The strongest-looking agreement this project has produced, and it was wrong.

Testing whether a signature survives perturbation, a finite-step sweep returned **~35 %
preserved at every scale from 2⁻⁴ to 2⁻²⁶** — six scales, eight seeds, 160 000
configurations, agreeing to within 0.3 %. Flatness across five orders of magnitude reads as
scale-independence, and I reported it as contradicting the claim it was testing.

**All six were the same measurement.** The sweep varied the step and held the DIRECTION set
fixed at ±1 on one quaternion component — eight axis-aligned directions per cube. Holding the
step at an infinitesimal instead and varying only the direction:

    +-1 on one component  16.2%      random in [-5,5]^4     2.5%
    random in [-1,1]^4    10.4%      random in [-50,50]^4   0.0%
                                     random in [-500,500]^4 0.0%

The entire effect was the height of the perturbing direction. At generic height the rate is
0 of 240. The claim under test had been right all along.

**Three lessons, and the second is the one I keep paying for.**

1. **A parameter held fixed is a parameter untested, and agreement across the varied one says
   nothing about it.** Six scales agreeing is [FAILURE_MODES 14](#14-agreement-between-samples-certifies-a-shared-cell-not-a-correct-one)
   at 160 000 configurations: convergence and co-location look identical from inside, and
   sample size does not separate them — only a different parameter does.
2. **Small-integer, axis-aligned directions are special, and this project has recorded that
   before.** [METHODS 16](METHODS.md) is about a routine choosing midpoints as
   representatives; the earlier instance was seven "representative" directions that were all
   small-integer and axis-aligned. I built the replacement measurement on ±1 jogs without
   noticing I was reproducing the documented failure inside the fix for a related one.
3. **The tell is a clean monotone split by the SIZE of the input.** 16.2 → 10.4 → 2.5 → 0.0 →
   0.0 against nothing about the geometry. When the failures and successes separate perfectly
   on height, degree, or denominator, the method chose badly and the question is still open.

**What actually broke it open** was removing a parameter rather than refining one. With a
finite step, scale and direction are confounded — every displacement has both. An
infinitesimal deletes the scale by construction, leaving direction as the only remaining
degree of freedom, and the artifact appeared in a five-row table. It cost 45× more per
evaluation and was worth it, which is the opposite of the trade I had assumed when I
(wrongly) claimed it would also be cheaper.

## 30. A nested chain counted as independent observations

[P225](LEDGER.md#p225) asserted two pair rules as exact laws on the strength of *"zero
violations across every record from n=4 to n=7 (6, 10, 15 and 21 pairs)"*. That reads as 52
confirmations across four records. The four records are the TOWER and are perfectly nested —
each is the previous one plus a cube — so every pair at level n reappears at level n+1:

    n      4    5    6    7    8    9
    pairs  6   10   15   21   28   36
    NEW    6    4    5    6    7    8

The real evidence was **21 distinct pairs from a single 7-cube configuration**. Tested on
4 000 independent pairs, one rule held perfectly (1 403 of 1 403) and **the other is false**
(150 of 199), with counterexamples the engine confirms in one call.

**Why it reads as strong evidence.** Summing per-level counts is the natural way to describe
a sweep, and it is correct when the levels are independent samples. Here the levels are a
CHAIN, and the phrase "across every record from n=4 to n=7" makes the dependence invisible —
it sounds like a range of cases rather than one object observed at six sizes. [P226] uses the
identical phrasing ("a hub persists at every level") on the identical chain.

**The rule.** Before quoting an evidence count, ask what the DISTINCT objects are. For nested
or derived families, report the new observations per level, not the cumulative total — the
`NEW` row above is the honest one and it was one subtraction away. And where a claim is about
a sub-object (here, a PAIR of cubes), it is usually testable on sub-objects drawn from
anywhere, which converts a handful of correlated instances into thousands of independent ones
for the cost of one script.


## 30a. A summary keyed on a string property that collides — 41 phantom violations

*2026-09-07, self-caught within one run.* `anchor_report.py` picked out the largest subset of
each cube's record with `max(per, key=lambda R: R.count(","))`, the keys being repr'd tuples.
At n = 4 that works: `"(1, 2)"` has one comma, `"(1, 2, 3)"` has two. At n = 3 it does not:
`"(1,)"` and `"(2, 3)"` BOTH have one comma, so the singleton was sometimes chosen as the
full set and the monotonicity test ran backwards. The roll-up reported **41 violations of
Lemma 3 and 8 of the per-cube theorem** on a proof that was correct.

**What caught it, and what did not.** Not the count being large — a real refutation would also
have been large. What caught it was that the GATE SCRIPT ITSELF had a separate counter for the
same condition, computed from the tuples rather than their printed form, and it read zero. Two
routes to one number, disagreeing, and the cheaper-looking one was the wrong one.

**The rule.** A property extracted from the PRINTED form of a key is a different property from
the one it looks like, and the difference appears at a size other than the one it was written
at. Where a roll-up recomputes something the producing script already knows, keep the
producer's own counter and compare them — the disagreement is the gate. Same family as
FAILURE_MODES 27 (a statistic that was a function of the spelling).

## 31. Counting integer-sampled instances to argue a condition has positive measure

*2026-09-08, caught by a user challenge ("so c_ℓ>1 is degenerate").* [P269] argued that
`c_ell = 2` is not a degeneracy from two numbers: 37 known instances share no face plane, and
0.42 % of random draws show it. Both are true and neither is evidence for the claim.

**Why.** The instances came from sampling INTEGER quaternions. Integer sampling hits rational
measure-zero loci with positive probability — that is what rational points on a variety ARE —
so a nonzero hit rate is consistent with the condition being exactly degenerate. And excluding
one named degeneracy (a shared face plane) excludes one, not the class; there is no finite list
to finish.

**What decides it.** Perturbation. A degeneracy is closed and measure-zero, so a generic
arbitrarily small move destroys it; an open condition survives. 108 of 108 perturbations at
1/100 and finer kept `c = 2`. That is definition-independent: it settles the question against
every notion of degeneracy as a closed condition without enumerating them.

**The rule.** To show a condition is NOT degenerate, perturb off it — never count instances,
and never argue from the absence of a listed coincidence. The conclusion here survived; the
argument for it did not, and the difference was invisible until someone pushed on it.

**Companion trap, hit in the same run.** The first perturbation sweep scored 26 draws as
failures when the C++ engine refused quaternions above its `|component| <= 512` budget. `c` is
computed in exact `Fraction` arithmetic in Python and has no size limit; only the identity
check needed the engine. Skipping that check at fine scales took the unevaluated count from 26
to 0. Reporting engine refusals as evidence about the object is FAILURE_MODES-grade on its own
(see "unevaluable is not a negative result").


### 31a. Addendum: the rule was written down, then broken in the same session

*2026-09-08.* FAILURE_MODES 31 was recorded after a user challenge, saying that integer
sampling hits rational coincidence loci with positive probability and that excluding ONE named
coincidence (a shared face plane) excludes one, not the class. Within the same session [P271]
sampled integer quaternions at heights 3, 9, 30, 120, filtered on `shares_plane` alone, and
reported "fails on 6.9 % of GENERIC configurations".

Re-tested with a real genericity condition — no vertex on four or more cube boundaries, every
3-body vertex of degree 3 — the rate splits 0.9 % (simple, 211) against 41.7 % (coincident,
36), and the headline figure was the pool.

**The transferable part is not the rule, it is where the rule failed to bind.** The filter
`shares_plane` was already in the code and reading `True/False`, so genericity FELT tested. A
named boolean that answers a narrower question than its name suggests is worse than no filter,
because it stops the question being asked. Check what the predicate actually excludes against
the coincidences the argument needs excluded — here, four boundaries through a point, which no
pair of parallel normals ever produces.

## 32. An assertion disabled by `or True` — the assumption documented, tested for, and never checked

`dimension.branch_numerator` cancelled a pair of denominators that only cancel when a
condition's two normals belong to the same cube. The code said so:

    assert sp.simplify(d1 - d2) == 0 or True     # same pair -> same denominator

The comment is correct, the assert is correct, and `or True` makes the whole line a no-op.
The result: for every condition whose two normals came from DIFFERENT cubes, `P` was a
different polynomial from the wall it claimed to be, and nothing said so. 6% of conditions at
n = 6, 16% at n = 7.

**Why the shape matters more than the algebra.** The consumer, `variety_incremental`, asks
"which directions make `P == 0` identically in `t`". A wrongly-nonzero `P` admits no
direction, so the over-constrained system returns **ISOLATED** — a plausible answer, of a kind
the project already publishes, in the same format as the right one. The bug had no failure
signature at all: no exception, no unevaluable, no implausible number. It could only ever cause
a false ISOLATED, never a false continuum, which is exactly the direction that reads as a
strong result.

**What found it** was not a consumer but an oracle: `P(record) == 0` must hold because a wall
contains its own point. That made the wrong values impossible rather than merely unexamined,
and the failures then sorted themselves perfectly by `|{j}| == 2` versus `|{j}| == 1` — the
clean split by a property of the INPUT that says the method chose badly, not that the objects
differ.

**The rule.** A disabled assertion is worse than a missing one, because the comment beside it
persuades every later reader that the case was handled. Grep for `or True`, `if False`, `pass
 # TODO`, and bare `except: pass` in any file that produces a number. And when an assumption is
worth writing an assert for, it is worth a gate that runs: this one was one line —
substitute the record point and demand zero.

## 32a. A cache path that follows the CODE instead of the DATA

`CACHE = HERE + '/dimension_cache'` and `DIR = os.path.join(HERE, 'catalogue_cache')`. Moving
the code into `src/` repointed both at empty directories. Nothing failed: `os.makedirs(...,
exist_ok=True)` created the new empty one and every expensive step was recomputed in silence.
587 condition sets (15 MB) and 219 catalogue entries went invisible for a day, and the six
entries recomputed in that time were all DUPLICATES of entries already sitting in the orphaned
cache — the recomputation produced no new information whatsoever, at a cost of hours.

This is failure mode 11's shape one level up: a probe that reads zero because it is pointed at
the wrong place, not because there is nothing there. A cache miss and an empty cache are
indistinguishable from inside the program, so the check has to be external — assert the
directory is non-empty at import, or print the resolved path and the entry count once per run.
The third file broken by that move, and the first where the breakage raised nothing.

## 33. A selective run that rebuilds the whole index — a deletion wearing a write's clothes

`wall_keys.py` accepts record labels on the command line and exports only those. Its `main`
built a fresh `out` dict, filled in the selected records, and dumped it — so `wall_keys.py 4`,
run as a one-record regression check, silently reduced a six-record index to one. No error, no
warning; the file was rewritten smaller and looked perfectly well-formed.

I did not notice at the time. It surfaced only because a LATER selective run was about to do it
again and I checked the file first — so the detection was luck, not a gate.

**The shape.** A write that produces a valid file is invisible to every check that asks whether
the file is valid. The only checks that would have caught it ask about CONTENT: does the file
still contain what it contained before, and did this run measure everything it is about to
write? Both are cheap and neither was there.

**The rule, now the file's stated invariant.** An export that is allowed to run on a subset must
MERGE into what exists, never replace it. Removing a record has to be a separate deliberate act,
not a side effect of measuring a different one. Same family as 32a: the failure is silent because
the mechanism cannot distinguish "nothing there" from "not asked for".

## 34. A PREMISE read as a theorem — the candidate space that could not contain the answer

Every count-plateau tangent search in this project builds its candidates from the wall
gradients: a tangent is assumed to lie in every wall, so the candidates are their null space.
The assumption is never stated as one, and it is **false**. At n = 7 a direction that crosses
**7 of the 51 walls** preserves the count, and of the wall crossings measured since, **4 of 6
change nothing**. A wall is a coincidence condition; crossing one need not create or destroy
a region.

**Why it survived so long.** The method never returns a wrong direction — everything it finds
does hold the count. It only fails to find, and a search that returns fewer answers than exist
looks like a rigorous search returning a small true answer. `tangents_full.py`, written to
remove a DIFFERENT restriction in the same code (the last-cube slice), inherited the premise
without noticing and reproduced the same blindness in a wider space.

**What caught it** was not a gate but a CONTRADICTION between two measurements made for
unrelated reasons: a full-ambient search found no base direction at n = 7, while a direction
measured days earlier — for a drawing — demonstrably held the count over five orders of
magnitude. Neither measurement was wrong; they could not both be about the same thing.

**The rule.** When a search defines its candidate space by a mathematical argument rather than
by enumeration, write the argument down as an assumption and test it on one known answer. Here
the test is one line: take a direction known to hold the count and check whether it is
orthogonal to every wall gradient. It is not.

## 35. Comparing keys across contexts where the same index names different objects

Condition keys here are `(frame, group, sig, c0)` and the group names cubes by INDEX. Comparing
keys between levels is therefore only meaningful when those indices denote the same cubes.

Met concretely: n = 8 and n = 9 each have a wall with frame 7 and group `((0,2,1),(5,2,1))` —
identical keys, at parameters differing by a factor of two. They are different walls, because
cube 7 is `(24,-24,24,-61)` at n = 8 and `(168,-168,168,-415)` at n = 9. Reading the match as
one shared wall would have produced exactly the inheritance story the data refutes.

**What made it safe elsewhere.** The inheritance count in the same postscript compares only
conditions on cubes 0..6, which ARE the same cubes at both levels, so that comparison stands.
The distinction is not "keys are unreliable" but "a key is a name in a context" — check that
the contexts agree before intersecting sets of them.

## 36. Sampling correctly, then interpolating wrongly

A 5x5 grid located a plateau boundary and every one of its brackets was right. The error came
after: two boundary points were joined with a straight line and the line was recorded as the
boundary. Solving the wall showed a curve of total degree 4 — successive differences 0.225,
0.240, 0.255, 0.272, not constant — and the straight fit was wrong by ~0.17 at mid-range, which
is 17% of the region's width.

The sampling was sound and the conclusion was not, because the step between "here are points
on the boundary" and "here is the boundary" is an interpolation, and an interpolation is a
model. Two points determine a line only if you already know it is a line. Where the boundary is
an algebraic curve, the honest options are to record the bracketed points as points, or to
solve the wall — which the wall-key machinery makes cheap, and which took one substitution.
