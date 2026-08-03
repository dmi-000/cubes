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
lists of errors. (Postscript 59.)

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
  directly, most of them *are* interior. (Postscripts 60 → 61; the wrong
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
  tight on that very example. It had stood for weeks. (Postscripts 53 → 56.)
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
semicontinuous. (Postscript 62.)

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
[`six_cube_search_results.md`](six_cube_search_results.md) for the dated record
in which every failure above is written down at the point it happened.
