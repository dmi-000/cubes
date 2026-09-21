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
| [P198](LEDGER.md#p198) | **"let's find the boundaries of the record regions, then start testing hypotheses"** | **TWO NEW RECORDS**: n=9 = 2787 and n=10 = 3921. Mapping a region's boundary walked out of it into higher counts |
| [P199](LEDGER.md#p199) | **"would it suffice to look around the vertices of the bounding polygon?"** | replaced direction-sampling with FACET enumeration — the finite object — plus vertex probes that reach cells no first crossing can. The facet census saturated at 4 |
| [P199](LEDGER.md#p199) | "after climbing facets, we should have the boundaries at hand and not need a separate record_boundaries run" | removed a duplicated expensive computation: the climb was already walking to every boundary and discarding it. `record_boundaries.py` superseded |

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
| [P188](LEDGER.md#p188) | **"I don't see anything updating. pid 97154 is still running."** | a 2.5-hour job burning CPU on a direction whose cheapest representative is (1,0,0) — and, once diagnosed, that P182's headline finding ("recorded members sit at plateau ENDPOINTS") is false in all three cases, each a different sweep artifact | **a process that had printed nothing** |
| [FM 19b](FAILURE_MODES.md#19b) | **"Has the point worth noting been noted? Has the flag been flagged?"** | caught that I had written "worth noting on its own" and "I'd flag that" and recorded NEITHER — one turn after writing "this belongs in TAXONOMY §5" and not putting it there. Naming a destination substituting for delivering to it | **my own words** "worth noting" and "I'd flag" |
| [P197](LEDGER.md#p197) | "what are the real open questions that we can expect to resolve?" | exposed that I had been reading the ceiling law's index as DEPTH when it is CO-DEPTH — read correctly the bound is tight (ratio 1.100-1.104) and **91% of the gap is at depth 1** | a triage question I had not asked |
| — | **"a hypothesis sounds like an OPEN QUESTION"** | killed my proposal for a new register between RESULTS and METHODS. `CONJECTURE` already existed and had been used twice, once being its own definition. The gap was a missing FIELD, not a missing file | — |
| — | **"Are discoveries distinct from results or methods?"** | produced the OBSERVED tag, and the measurement behind it: **4 of 17 entries written that day were retracted or superseded the same day, and all four were pattern claims while every survivor was a measurement** | — |
| — | "would we want similar tags to characterize METHODS?" | tagging by KIND revealed **4 of 22 METHODS entries are FACTs, not methods** — including §7, which I had cited as authority all day and whose n=9 evidence I had corrected that morning | — |
| — | **"would you now say P194's OBSERVATION rather than discovery?"** | forced the method/observation split: the technique is a METHOD, the conclusion drawn with it is OBSERVED. Produced METHODS 22 with its directionality caveat — sound as essential=>unchanged, HEURISTIC in the converse actually used | my own loose word "discovery" |
| — | **"Is that a case for solve not sample?"** | yes — 18 directions in a 4-dimensional subspace. Led to finding that all 76 tight walls vanish identically on the null space, so the cheap chamber solve does not apply, and to EXHAUSTION over a stated family as the honest rung | "18 directions" in my own report |
| [P184](LEDGER.md#p184) | **"I think we implemented epsilon as a step size"** | the ENGINE is a true infinitesimal; **P175** used steps 1/1000, 1/100, 1 — and two of them agreed, certifying a shared cell. P175's universal is false for n ≥ 7 | **"1/1000: 685  1/100: 685"** printed in the entry |

**The shift.** Early interventions were generative — a human seeing meaning in a
picture. Recent ones are corrective — a human auditing method. Both matter, but the
second kind is the one that scales badly: it requires the human to read closely
enough to spot a leaked parameter, on work that is by then several documents deep.

### A3. Recurring interventions — the same correction, over and over

*Added 2026-08-31 after mining all five session transcripts (`mine_interventions.py`).
These are counts of DISTINCT human turns, not impressions.*

| theme | times raised | first | last |
|---|---|---|---|
| **"solve, don't sample"** | **13** | 2026-07-15 | 2026-08-31 |
| unevaluated cases / gaps not counted | 9 | 2026-07-21 | 2026-08-30 |
| stale or wrong documents | 8 | 2026-07-30 | 2026-08-18 |
| continua and their ENDPOINTS | 5 | 2026-08-03 | 2026-08-31 |
| epsilon / infinitesimal vs step | 5 | 2026-08-03 | 2026-08-31 |
| "could you have asked that yourself?" | 5 | 2026-08-02 | 2026-08-19 |
| reproducibility / don't work in scratch | 4 | 2026-08-04 | 2026-08-31 |

**Thirteen times.** "can we solve instead of search?" (08-05), "why did we sweep
instead of solve?" (08-10), "you said sweep the rulings systematically — did you
mean solve?" (08-10), "is subset_topology.log sampling directions?" (08-13), "are
the 15 directions chosen by sampling or solving?" (08-31). METHODS 1 is the FIRST
principle in the global principles file, and it is there because this question kept
having to be asked. Writing it down did not stop it being needed.

Three of these threads close a loop that is worth stating exactly, because each is a
case where the human supplied the remedy and the remedy was later ignored:

- **The ε engine was the user's idea.** 2026-08-03: "Which of those five counts are
  epsilon neighbors?" Then 2026-08-16: *"can arithmetic fields handle epsilon? or can
  1/2^n be solved rather than sampled?"* and "infinitesimal-arithmetic engine seems a
  useful tool." `cube_regions_eps` was built that afternoon. Two weeks later
  [P175](LEDGER.md#p175) answered an infinitesimal question with 1/1000 and 1/100 —
  and it took the user saying "I think we implemented epsilon as a step size" on
  08-31 to find it ([P184](LEDGER.md#p184)).
- **Endpoints were asked for on 2026-08-03**: "Are there other continua? we should
  check all endpoints." On 2026-08-31 the audit found them still undocumented for
  every rung except 727 ([P183](LEDGER.md#p183), [OQ 13](OPEN_QUESTIONS.md)). Four
  weeks, unclosed, never resurfaced by me.
- **The reproducibility rule is the user's**: 2026-08-04, "if exact ℚ(√2)/ℚ(√5)
  representatives aren't in a findable file, they should be. **Everything we do
  should be reproducible**"; 2026-08-11, "some early .pys were written to temporary
  scratch and may not have gotten archived... we should strengthen our policy." On
  2026-08-31 a 3 216-second n=10 measurement turned out to have been launched from an
  unsaved heredoc ([FAILURE_MODES 19a](FAILURE_MODES.md#19a)).

### A4. Interventions recovered from transcripts that no ledger entry records

Mined 2026-08-31. None of these carry a "Prompted by" marker.

| date | what the human said | what it did |
|---|---|---|
| 2026-07-09 | "Is there a way to count analytically without having to approximate irrationals?" | **founded the project's exact-arithmetic rule** — the constraint every engine since has been built to satisfy |
| 2026-07-09 | "why are all the region counts == 3%4?" | the mod-4 structure |
| 2026-07-11 | "I think slide3_report.md failed to find the way the 3 cube configurations continuously slide into each other. the 3 cubes all need to rotate together" | corrected a delegated agent's report on the geometry it was hired to find |
| 2026-07-12, 07-21 | "it seems counter intuitive that moving the center of any of the cubes could increase the number of regions, but do we have any solid arguments against it?" | exposed a **counting bug** — sign-vector cells of infinite face planes instead of containment regions ([P38](LEDGER.md#p38)) |
| 2026-07-13 | "I think postscript 9 described the 67 flexibility" | the human remembered the ledger's contents better than I did |
| 2026-07-14 | "I think some of the edge concurrences should persist on the slide" | corrected a claimed loss of coincidences |
| 2026-07-30 | "why is Postscript 31 after Postscript 41?" | record integrity — ordering corruption in the ledger |
| 2026-08-02 | "generated positions is good, but **it doesn't update invalidated statements. discipline does that.**" | the doctrine behind the superseded-claims table |
| 2026-08-05 | "Are you sure the continuum is one dimensional?" | a dimension claim challenged directly |
| 2026-08-16 | "did we record any claim with falsified numbers?" → "was the method that produced falsified numbers used as the basis of any other claim?" → "how did a wrong answer slip through?" → **"Could you have asked those questions yourself?"** | the audit sequence, and the question that became the standing rule to run it unprompted |

### A5. What the "Prompted by" marker does and does not capture

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
| The contradiction that exposed [P195](LEDGER.md#p195): it claimed dimension 4 at 2785, whose null space is 4-dimensional, so every null direction would have to preserve — but P184 had measured one changing. `map_geometry.py` was reporting `len(list)` as a dimension and never checked linear independence | noticing that two of my own entries could not both be true |
| A misattribution in **this file**: the "another way to slide" quote was cited to P26 when it is inside P25 | verifying every anchor against the ledger before publishing the register |
| Third instance in one session of claiming something undone that the repo had already done (727's arcs, then `n78_ends.py`'s solved 1217/1895 endpoints) — all three surfaced by the user asking, none by me checking | not caught by me; recorded here because the ratio is the measurement |
| Reported a "climbing trend" in `extend_1217` (1885 → 1887 → 1889) that does not exist — I read EXECUTION order as PARAMETER order, and the `TS` list is not sorted by t | sorting the results by t before describing them; the real sequence is 1885, 1883, 1887, 1889, 1885, 1883 — non-monotone, like the 723 spread |
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

---

## Part D — How this file gets updated (the token question)

The obvious objection to mining transcripts is cost: 5 files, **84.4 MB**, 32 186
JSONL lines. Reading them is impossible. Reading the *human* is easy, because the
human is a rounding error in the corpus:

    all JSONL lines                    32 186      84.4 MB
    genuine human turns                 1 554     476.6 KB     0.58%
    challenge-like turns                  589     321.5 KB
    long pastes truncated to 400 ch       589      79.6 KB    ~20k tokens   0.09%

`mine_interventions.py` does this. "Genuine" drops `tool_result` blocks (which carry
`role=user`), system reminders, task notifications and slash-command envelopes;
"challenge-like" keeps turns with a question mark or corrective vocabulary and drops
bare acknowledgements; truncation is safe because a long paste only needs its opening
to be classified. Re-run it after new sessions.

**The recovery rate is the point.** Part A4 lists ten interventions that no ledger
entry records, including the one that founded the project's exact-arithmetic rule.
The ledger's own "Prompted by" marker found 15; mining found the rest. Attribution
by memory undercounts, and it undercounts in a specific direction — the earliest and
most foundational contributions are the ones least likely to still be cited.

## A5. 2026-09-01 — three challenges, three defects, one campaign

All three arrived as short questions about method, not about results, and each one
turned out to sit on top of a defect that was producing numbers at the time.

| user's words | what it found | would it have been caught? |
|---|---|---|
| "Don't we already have a climber?" | A second climber was being written alongside `climb.py`. Checking rather than assuming produced the measurement that mattered anyway — at a Haar-random point there are **0 tight walls, nullity 9 of 9** — so the right move was to give `climb.py` a direction menu, not to fork it. `simplest_between` was also extracted to one module instead of two. | Probably not. The duplicate had a plausible justification and was already written. |
| "[the second machine]" / "if this is a long run" | The campaign was queued on a laptop already running `arcs_extend` and eight samplers. The second machine has 12 cores and was idle at load 1.5. | No — the machine was simply not in mind. |
| "Is it not selecting tangents guaranteed to find walls?" | **No, and it was not.** `conditions()` emits gradients only for already-TIGHT conditions; at a generic point `loose` is a bare counter. Re-testing the first 8 climbs against solved lines found **3 of 8 terminations premature**. The hedge "locally maximal OVER THE DIRECTIONS WALKED" was in the log the whole time and did not stop the numbers being used as terminal counts. | No. The hedge had been written deliberately, which is exactly why it stopped being read. |
| "could a rational engine use factorizations instead of large products?" + "volume of engine failure space might help judge the value" | The 36 % refusal rate at records — reported one message earlier as the measured case for building a modular-arithmetic engine — was **four fifths a duplicate-root bug in the caller** ([P212](LEDGER.md#p212)). Asking for the volume is what exposed it: 0 refusals in 30 000 Haar draws against 36 % at records is a contradiction, and one side had to give. | No. The build was about to be specced. |

**What the four have in common.** None asked whether a result was right. Each asked what
the METHOD was — which climber, which machine, which directions, which arithmetic — and
in every case the method had a defect the results were quietly carrying. The producer
checks results against expectations; the reader asks what produced them.

**Self-caught in the same session, for the ledger's balance:** the unevaluable-vs-
disagreement conflation in `gate()`; the height runaway that made a climb declare
maximality on refused probes; the `basin.py` RNG stream that would have made the NDIR
saturation check compare different starts; the `facet_walk` budget bug and then its
refusal-rate bug, each found by running the control rather than the method. The last two
are also the session's worst pattern: the same claim was published and withdrawn twice
before the control was clean.


## A6. 2026-09-06/07 — the signature bug, and the shape of the gate that found it

**The defect.** `concurrence.planes()` built each cube's six face normals from the ROWS of
its rotation matrix; in world coordinates they are the COLUMNS. Every plane-incidence
signature this project ever computed therefore described each cube's INVERSE rotation.

**How it was caught, and this one is a self-catch worth recording precisely** — not because
it reflects well, but because the shape is reusable. It did not come from doubting a result.
Every result looked fine: the statistic was exact, deterministic, reproducible, and
correlated with the count at r = 0.562 over half a million configurations. It came from
asking what the statistic was a function OF. A quaternion is a *representation* of a cube,
and a cube is invariant under 24 rotations, so `q` and `q·s` are two names for one object
and any honest function must be constant along that orbit. Broken: **6 of 6** respellings
changed the signature. Corrected: **0 of 96**.

| what it cost | |
|---|---|
| census `sig` column | 3 135 491 rows void (counts and configs valid) |
| Chao1 richness ≈ 4 216 | void, no replacement |
| the count predictor | r **+0.562 → −0.147**, ordering **77.6 % → 50.6 %** |
| "the n=4 record has a 9-fold" | wrong; it has 6 |
| a corner-triple construction | 1 500 configurations, aimed at a phantom |

**The four turns from the user that this sits under**, and they are the same pattern as A5
— all about the method, none about a result:

| user's words | what it led to |
|---|---|
| "When identical signatures give different counts, what distinguishes the configurations?" | The face-boundedness mechanism, and the whole real-incidence line. The QUESTION survives the bug: re-measured under the corrected map, 6 of 161 repeated signatures pin the count. |
| "Can we normalize the signature?" | Directly upstream of the fix. Asking whether the signature *needed* normalising is asking what it is invariant under, which is the gate. |
| "Can the signature outputs be corrected?" | Forced the distinction between the void column (`sig`) and the valid ones (`cfg`, `count`, `depth`) — i.e. that the correction costs a recomputation and not a re-search. |
| "Also consider whether there are other kinds of signatures not yet characterized. If identical signatures can give the same count, then the signatures are incomplete in some way." | The incompleteness claim was the one thing in this line that did not depend on the normals, and it is the one thing that survived. |

**Self-caught in the same stretch, for balance, and each one is a gate failing correctly:**
the `--base` incremental engine silently returning the base's count for every candidate
(caught by a 75/75 agreement gate, after a broken version had already been reported as
5.2× — the honest figure is 2.6×); an S₄ "reduction" argued from true premises to a false
conclusion and refuted by counting 24 permutations of a known-good tuple; the FIRST gate
written against that, which was also wrong; and a THIRD gate failure that read as
"CUBE NOT IN MENU" when the menu was fine — it tested membership of an octahedral QUOTIENT
with `in`, and the target class was present under a different one of its four equal-height
spellings.

**The pattern in all four.** A gate is code and can be wrong; it needs its own known-good
case. Two of the four failures above were the gate rather than the thing gated, and both
would have been caught by running the gate once on a case known to pass — which costs
seconds and was skipped because the gate felt like the check rather than a thing to check.

**And the omission that made the bug survivable for two days**: there was never a positive
control. Three cubes sharing a corner axis MUST show a 9-fold concurrence, four MUST show a
12-fold — it is three lines, it is forced by geometry rather than by the code, and it fails
loudly on the broken map. It was written after the fix, like the probe in
[METHODS 4](METHODS.md)'s own cautionary note about being built seventh.

## A7. 2026-09-07 — one question about the TOOL overturned three of my conclusions

**The turn**, in full: *"for something as small as 2^-20, would calculus be a more
appropriate tool than arithmetic?"*

It arrived while I was reporting a finished measurement as a finding. It named no result,
disputed no number, and pointed at the instrument.

**What it found.** I was re-measuring [TAXONOMY 12a](MAXIMISER_TAXONOMY.md) with finite
displacements at 2⁻⁴ … 2⁻²⁶ and had just reported ~35 % of signatures preserved, flat at
every scale across 160 000 configurations and 8 seeds, agreeing to 0.3 %. I read the flatness
as scale-independence and had already written into two documents that 12a might be backwards
and that the ensemble-design program of [METHODS 23a](METHODS.md) rested on a claim that
might reverse.

Working through the question produced three successive corrections, all of them mine:

| | what changed | result |
|---|---|---|
| 1 | the tool: an infinitesimal instead of a small number | exposed that "preserved" pooled 24 % of bases whose signature was EMPTY — nothing to break |
| 2 | conditioning on degenerate bases | 35 % → 1.8 % |
| 3 | varying DIRECTION height, step removed | 1.8 % → **0.0 %** at h ≥ 50 |

**12a was right.** Its numbers stay void and unsourced; its conclusion is now supported by an
exact, two-sidedly gated, direction-resolved measurement it never had. My flag on METHODS 23a
is withdrawn.

**Why the question worked, and it is the same mechanism as [A5](#a5-2026-09-01--three-challenges-three-defects-one-campaign) and [A6](#a6-2026-09-0607--the-signature-bug-and-the-shape-of-the-gate-that-found-it).**
The user's own principles file already contained the answer — *"an infinitesimal is exact; a
small number is a sample"* — and I had read it that morning and quoted its neighbours in two
postscripts. It did not fire, because the finite-step measurement did not feel like sampling:
it was exact integer arithmetic, deterministic, gated, and flat over five orders of
magnitude. **The rule was known, written down, and inapplicable-looking.** A question about
the instrument is what made it applicable.

And the deeper thing the question bought was not exactness at all. With a finite step, scale
and direction are confounded — every displacement has both. Removing the scale by
construction left direction as the only free parameter, which is how a five-row table found
what 160 000 configurations had hidden. **The value of the better tool was that it had one
fewer knob**, not that it was more precise.

**Cost of the version I would have shipped:** two documents asserting that a sound method
premise was about to reverse, on the strength of six agreeing scales that were six
measurements of the same axis-aligned direction set ([FAILURE_MODES 29](FAILURE_MODES.md)).

**Also this session, same shape, no defect found:** *"While that runs on this machine, do you
want to start something on the other machine?"* — the [A5](#a5-2026-09-01--three-challenges-three-defects-one-campaign)
pattern of a resource simply not being in mind. It is what caused the 12a re-measurement to
be attempted at all.

**Self-caught the same day, for balance:** the two-statistic debt in
[FAILURE_MODES 27b](FAILURE_MODES.md) (I re-measured 1 of 3 void statistics and wrote "there
is no predictor" into five documents); the per-ensemble richness directions that a second
seed contradicted (27a); a stale index generator that silently dropped every recent entry
while printing success (28); and the six n=5 bases that were six names for one compound
([P228](LEDGER.md#p228)).

**The counting that matters.** Four user turns this session, three of them one sentence.
Every one was about method — which tool, which machine, which parameter — and none was about
a number. The producer checks results against expectations; the reader asks what produced
them. That is now three consecutive entries in this file saying the same thing, which
suggests it is not an observation about particular sessions.

<a id="a8-2026-09-07--the-user-quoted-my-own-next-step-back-and-the-method-i-named-was-wrong"></a>
## A8 (2026-09-07) — the user quoted my own next step back, and the method I named was wrong

**The intervention.** Not a question. The user quoted the closing paragraph of [P265] back —
*"So a proof needs exactly one thing: that merging in the subsets is at least as fast as the
loss in d₃… That's where I'd pick up."* — and nothing else. The whole content was: do the
thing you just said was next.

**Yield: Theorem S ([P266]), the first subset-to-whole inequality in the project, proved for
all n**, closing [OQ 31].

**The part that is against me.** The route I had NAMED in that same paragraph — "which walls
disappear when a cube is removed, which is the one direction of this problem the incremental
engine already models exactly" — is not the route that worked, and would not have worked. It
is a REGION-counting route, and [P265] had already shown on its own page that region counts
lose a factor of three through an intersection. The proof came instead from the fibration plus
[P33]'s anchor theorem, i.e. from the two oldest theorems in the project, because a fixed
six-point witness set survives intersection where a region count does not. I had the
disproof of my own proposed method printed above my proposal.

**What the pattern is.** [A5] and [A7] were the user naming a resource or a parameter that was
not in mind. This is the complement: the user named nothing, and the defect was in the
direction I had supplied myself. A stated next step is not evidence about the next step; it is
a record of what was in mind when the previous result was written down, which is exactly the
moment [P265]'s own audit question ("what else used this method") went unasked.

**Cost if the instruction had been followed literally:** an incremental-engine campaign
measuring wall disappearance, which is the same region count that had already failed, on
machinery that would have taken hours to build.

<a id="a9-2026-09-08--three-challenges-on-c_ell-no-defect-found-and-one-claim-strengthened"></a>
## A9 (2026-09-08) — three challenges on `c_ell`, no defect found, one claim strengthened

*"when is c_ℓ == 3?"* → [P268]. *"Do degeneracies create c>1?"* → [P269]. *"isn't every cube
antipodal to itself?"* → the [P269] addendum.

**No defect found in any of the three** — which is worth recording, because the previous eight
entries in this file are all defects and that is not a representative sample of what user
questions do.

**What they produced instead.** The first forced a rebuild: the script behind `c_check.log`,
`c_recheck.log` and `bylevel.log` had never been saved, only the logs, so the numbers being
quoted had no reproducible source. Rebuilding it and gating it against those logs' recorded
`V` and `E` — not just `c` — is the only reason the follow-ups could be trusted. The second
separated two mechanisms a single statistic had been averaging. The third asked for the step
from the whole to the parts to be exhibited, and the exhibition turned up an ALL-OR-NOTHING
structure (150/0, 0/176, 0/130 — never mixed) that had not been noticed and that is a
prediction of the double-cover framing rather than a further observation.

**The pattern.** A challenge to a step you believe is correct still pays, because the
demonstration is not the same object as the belief. Two of the three were answerable only
because the first one forced the measuring code back into existence.

## A10 (2026-09-08) — "record enough to reconstruct them" turned up a formula that had been answering ISOLATED

**What the user asked.** "If we don't have wall polynomials recorded, we want to at least
record enough to easily reconstruct them." A request for BOOKKEEPING, not for mathematics, and
the second time in two turns the user had pressed on whether the polynomials were recorded.

**What I would have done unprompted.** Written the keys out and stopped. The keys are small,
the export is twenty lines, and `data/record_walls.json` already existed with a docstring
politely explaining that gradients are not polynomials — which reads as the gap being known and
therefore handled.

**What the request forced.** "Enough to reconstruct" is only meaningful if the reconstruction is
demonstrated, so the export needed a gate, and the only honest gate is one whose anchor sits
outside the code being gated: a wall contains its own point, so `P(record) == 0`. That check —
one substitution — failed on 6 of 27 walls at n = 6, 24 of 51 at n = 7, 42 of 75 at n = 8, and
found a cancellation in `dimension.branch_numerator` valid only when a condition's two normals
come from the same cube, guarded by an assert that `or True` had disabled. See FAILURE_MODES 32.

**The cost of not having asked.** The wrong polynomial over-constrains, so its consumer returns
ISOLATED — the shape of answer the project publishes. n = 4 and n = 5 have zero cross-cube
conditions and are exactly unaffected (P287 stands, re-confirmed under the fix); n = 6 and n = 7
had their ISOLATED verdicts withdrawn.

**The pattern, which is now three for three.** A10, like A7 and A8, came from a user question
aimed at the APPARATUS rather than the result — is it recorded, does the tool do what its name
says, is that really the next step. My own audit questions arrive pointed at conclusions. The
producer checks the answer; the reader checks the instrument, and the instrument is where the
defects have been.

**Second catch, same turn.** Locating the keys meant opening `dimension_cache` — which the
repo reorganisation had orphaned a day earlier, along with `catalogue_cache`, silently
(FAILURE_MODES 32a). I had checked HERE-relative paths for the ENGINES and for the DOCUMENTS
after that move and twice reported the sweep complete. I had not checked them for the CACHES.

## A11 (2026-09-09 to 09-12) — a drawing asked questions the prose never had to

**What the user asked for.** A picture of the relationships between the record regions.
Then, across a dozen short questions, what each mark in it meant.

**What that produced.** Every one of those questions was answerable only by a measurement
that had not been made, because prose can describe a relationship without committing to it
while a drawing cannot:

| question | what it forced |
|---|---|
| "is there a relationship between the arcs and the circles?" | the arcs were drawn concurrent; they are not, and cannot be — they contain congruent copies, not a shared point |
| "does the dashed line extend to the 1217?" | the congruence tie LIFTS — verified, not assumed |
| "does it project down to 393?" | all four arcs share the 393 base; the middle layer IS one fibre over it |
| "are those dots the boundaries?" | the plateau's boundary had never been measured at all |
| "what does a yellow line along a blue line mean?" | the blue line was doing two incompatible jobs — a fibre and a cube-addition |
| "is the region a linear combination?" | it is not: a THIRD wall cuts a corner ([P301](LEDGER.md#p301)) |
| "does that wall project down or up?" | created by the 7th cube, inherited unchanged by the 8th ([P302](LEDGER.md#p302)) |

**Six postscripts came out of a request for a picture** — P295, P299, P301, P302, P303, and
the gap register P297 that P298 then overturned.

**The mechanism, worth naming.** A diagram must place every mark somewhere. Prose can say
"the plateau runs in two directions" and stop; a drawing must decide whether they span
anything, where they cross, and where they end. Each of those decisions is a claim, and a
claim that has not been measured is visible to a reader as a shape that looks wrong. The
producer sees a picture of what they already believe; the reader sees the geometry.

**And it repeated the A7/A8/A10 pattern.** The questions were aimed at the APPARATUS — what
does this mark mean, does this line reach that one — not at the conclusions. That is now
four sessions running in which the defects were found by questions about the instrument.

## A12 (2026-09-12) — an audit finding that was wrong in its claim and right in its signal

**What was reported.** "INTERVENTIONS.md A11 cites eight postscripts that do not exist."

**What was true.** A11 cites seven postscripts, and all seven exist. What did not exist were
the `<a id>` anchors for P288–P303, so every link into that range — A11's two included —
resolved to the top of the ledger rather than to the entry. The finding's *reading* was the
correct one to have: a citation that cannot be reached is indistinguishable from a citation to
nothing, and the burden of distinguishing them is not the reader's.

**What it turned up beyond itself.** Checking the class instead of the instance found 23 dead
links, not 2 — nine of them into METHODS and FAILURE_MODES, dead for longer, because they
addressed sections by heading slug and those headings carry a `[PRACTICE]`/`[FACT]` prefix.
Recorded as [FAILURE_MODES 37](FAILURE_MODES.md#37), and `doc_audit.py` now checks whether a
citation RESOLVES, having only ever checked what a claim CITES.

**The pattern, fifth session running.** The defect was found by a question aimed at the
APPARATUS — can this reference be followed — and not at any conclusion. Nothing in the
mathematics changed.

## A13 (2026-09-16) — "are we sure we caught any prior propagation?" — no, and the miss was the documented one

**What the user asked.** After [P323] voided [P304]'s mechanism and listed the casualties:
*are we sure we caught any prior propagation?*

**The honest answer was no.** The casualty list went into the LEDGER and never reached the
documents that get read:

    OPEN_QUESTIONS.md  OQ 4   "+258 on the SAME window, true increment 282"  -- as MEASURED
    OPEN_QUESTIONS.md  OQ 30  "282 walls through each record"
    SESSION_STATE.md          the P309 row, and P304's "concurrency walls are PUNCTURES"

Every one of those is void, and every one was still standing an hour after [P323] was written.

**This is the project's own documented failure mode, verbatim.** *Corrections propagate inside a
record and not out of it* — measured once at 118 ledger entries, 389 internal cross-references,
**1 link outward** — and the memory note `results-md-can-be-stale` records it recurring. Writing
the correction into the ledger FEELS like completing the correction. It is not, while the
document people read still carries the old claim.

**And `doc_audit.py` cannot catch this class.** It checks that citations RESOLVE and flags
claims revisited by a later postscript; it does not know that a number inside a paragraph is
now wrong. The stale text here cited [P309] correctly — the link worked, the postscript exists,
and the sentence was false.

**What the fix surfaced, which is worth more than the fix.** Adding the containment predicate to
`concurrency_walls.py` and re-running its own gate: **G4's anchor — the `t = -2/9` wall that
[P304] was built on — returns `common_point_inside_cubes: false`.** The founding example of the
family is not an arrangement wall. [P323] is confirmed from the gate's own reference point.

**The rule this leaves.** After voiding a claim, grep the READ documents for its NUMBERS, not
its postscript number — `258`, `282`, `663` found the stale text; searching for `P309` would
have found correct citations and missed all of it.

## A14 (2026-09-16) — a self-catch, on the previous session's own result, found by re-deriving before proving

**No human catch here, and that is the point worth recording**: [P329] was written in the session
immediately before, marked [VERIFIED], and handed forward as the lead. The instruction that
caught it was the user's standing one — "we have solvers not just samplers" — applied to the
first step of the proof attempt rather than to the proof.

**What the catch cost.** Four lines of Python, run before any proof work began: recompute the
published counterexample under the definition the identity uses. `24` became `6`.

**What it found, in order of severity.**

1. The counterexample refuting `EE <= 6` per pair was not a counterexample — it agrees with the
   bound. (The bound is still false; the true witness is 10, elsewhere.)
2. The replacement conjecture `sum EE <= 6*C(n,2)`, offered as the thing to prove, is false at
   every n from 2 to 6.
3. [P328]'s per-signature excess constants are generic values, not invariants.

**The propagation check, run because [A13] is two entries up.** The numbers to grep were `24`,
`(0,1,1,1)` and `6*C(n,2)`, not "P329". They appeared in [OQ 35] and in [P328]'s closing lead;
both are corrected in place and dated. `data/ee_per_pair.json` and `data/ee_total.json` are
untouched — they are what was measured, and [P330] says what they measured.

**The lesson that generalises past this project.** A result marked VERIFIED and handed forward as
the next task's foundation gets less scrutiny than a result being argued about, because the
argument has moved on to what comes AFTER it. The moment of maximum danger for a claim is
directly after it is accepted. [METHODS 28] is the procedure.

## A15 (2026-09-16) — "check corrections and false claims" — the correction itself carried three errors

Asked directly, one turn after [A14], to audit the correction. It did not survive the audit
intact, which is the entry's whole point: **[P330] was written in the register of a careful
correction and shipped three unsourced claims of its own.**

| what [P330] said | what checking it showed |
|---|---|
| [P329]'s search "never looked where the `(2,2)` vertices are", its seeds coming from the wrong counter | **Wrong.** The violating family was IN its 255-element pool — best 4-subset scores 40 against the bound's 36. 400 random triples, 0.012 expected hits. A sampling failure, not a coverage one. |
| the two EE functions were "written eleven minutes apart" | **Invented.** Both files carry one mtime, the moment they were rescued from scratch. The interval is not recoverable, and nothing ever measured it. |
| `(2,2,...,2)` has excess `2(b-1)^2` | Fitted to five points in one family and stated as if derived. [P324] is the record of exactly such a fit breaking at `b = 5`. Now marked as a pattern. |

**And one more, found by building the check rather than by reasoning.** The independent oracle
written to validate the vertex counter disagreed with it on 1506 of 1856 pairs — because the
ORACLE built edges from the columns of `mat(q)` and tested signatures against the rows.
[FAILURE_MODES 38] for the third time. Corrected, the two paths agree on all 1856, 0
disagreements, so the counter is now gated against a genuinely independent path. **The check was
wrong in the same way the original code had been wrong, and only running it revealed that.**

**The self-inflicted one.** The audit script IMPORTED `ee_per_pair`, whose census runs at module
level — so the import re-ran it and overwrote `data/ee_per_pair.json`, destroying the `reproduce`
block backfilled hours earlier. Restored by hand with a note. **An audit that imports the code it
is auditing can modify the evidence**, and a probe whose work happens at module level is a
landmine for exactly the reader most likely to import it.

**The lesson, and it is not "be more careful".** Every one of these went into a document whose
subject was someone else's error. The corrective register is where an unsourced claim is least
likely to be challenged, because the reader is attending to the error being fixed, and the writer
is feeling accurate. **Gate the claims IN a correction the way the correction demands of the
thing it corrects** — [METHODS 27] applies to the postscript that cites [METHODS 27].

## A16 (2026-09-16) — "are all sources on which current claims stand free of such bugs?" — no

The third audit question in a row, and the one that paid best. [A15] fixed the correction; this
asked whether the same defects sit under claims nobody had questioned. **They do.**

**What was actually done, because "we checked" is not an answer.** Each known bug class was
turned into a mechanical search over `src/`:

| bug class, and where it was first found | swept how | result |
|---|---|---|
| rows vs columns as face normals ([P227], [P304], and the A15 oracle) | every module calling `mat()`, flagging row inner products with no transpose | 7 hits, **all 7 benign** — 4 are `in_cube(pt, Minv)` helpers whose callers pass an explicit transpose, 3 are ordinary matrix multiplies |
| no containment predicate ([P322]/[P323]) | modules that solve plane intersections, checked for an inside test | **`concurrence.py` — a live claim, now [P331]** |
| incidences counted as objects ([P330]) | the two EE counters, gated against an independent enumerator | 0 disagreements on 1856 pairs |
| import-time file writes ([A15]) | `ast` walk of every top level | 68 writers, 4 imported, 3 nondeterministic — [FAILURE_MODES 42] |

**The find.** `concurrence.py` counts plane concurrences with no containment test. Not one
top-multiplicity point in 183, 723 or 727 lies on the compound — they sit 63–68 % past the
nearest face. 723's celebrated 9-fold is three cubes sharing a corner that **sticks out beyond
the other three cubes**, so it is not an arrangement vertex and buys no regions. The claim had
been re-verified once already, for the ROWS bug, and the containment question was never asked of
it because [P304] came three weeks later and nobody went back.

**And it closed an older loose end.** [P55]/[P57] measured the "high concurrence" heuristic as
NEGATIVELY correlated with the count and recorded the reversal with no cause. The cause is this:
the statistic ranks configurations by points that are not part of the object being counted.
**A refutation without a mechanism is an open question wearing a closed question's label** — it
sat for five weeks looking settled.

**The generalisable procedure.** When a bug is found, do not only fix it and propagate it.
**Turn its SIGNATURE into a search and run it over everything**, including code that predates
the bug's discovery and claims that were verified against a different defect. A claim that
survived one audit is not thereby audited; it was audited for one thing. Every class above took
minutes to sweep, and one of the four returned a live wrong claim.

## A17 (2026-09-17) — I opened as OPEN a question the ledger had closed a month earlier

The user, in one sentence: *all triples of a 4-compound can be 67, but it falls short of the
record.* Both halves correct, and both already in `RESULTS.md` §4, from
[P131](LEDGER.md#p131), 2026-08-18: *"The 'two 67 triples' family at n = 4 is EXHAUSTED and caps
at 177 ... 960 candidates, zero engine refusals, best 177, six short of 183."*

**What I did.** [P341] asserted the all-67 ceiling was "certainly not attainable, since it
requires all four triples to be 67s and the 67's pairs are rigid", and [OQ 38] then posed *can
two triples both be 67s?* as **the decisive open sub-question**. It was neither open nor
decisive. The answer was four, not two, and it had been obtained by exactly the method I was
recommending — solving rather than searching.

**Why it happened, and it is not ignorance of the file.** I had read `RESULTS.md` this same
session — I edited §3d into it, and wrote new rows into its superseded-claims table. The failure
was not in reading but in DIRECTION: when a new formalism (the subset decomposition) produced a
question, I asked whether the question was interesting, not whether it was answered. **A
reformulation feels like new territory even when it is a change of coordinates on old ground.**

**The check that would have caught it, in one command.** The question was about 67s inside
4-compounds. `grep -n "67" RESULTS.md` returns the exhausted-family bullet directly. Cost: three
seconds, against a postscript and an open question that had to be corrected.

**The rule.** Before opening an OPEN QUESTION, grep the record for its SUBJECT — not for the
postscript number, not for the formalism, but for the object it is about. [A13] established that
rule for propagating corrections; it applies identically to posing questions. **The record is as
easy to duplicate as it is to contradict, and duplication is harder to notice** because nothing
in the new entry looks wrong.

**What survives.** The measurement in [P342] is new and stands: every subset of the golden 177 is
simultaneously maximal, and its 6-region shortfall is exactly its 18 quadruple points, confirming
[P340]'s law at magnitude 18 rather than 2. The error was in the framing around it, not the
arithmetic inside it.

## A18 (2026-09-17) — "are scratchpad sources that support or refute claims recorded?" — no, for the five most recent postscripts

Asked mid-turn. The answer was no, and the question was worth more than the analysis it
interrupted.

**What was fine.** Ten scratch scripts had been rescued into the repository under new names —
`fld.py` to `src/kfield.py`, `coupling.py` to `src/probes/subset_coupling.py`,
`predict*.py` and `outlier.py` folded into `src/probes/subset_predictor.py`, and so on. My first
check compared FILENAMES and reported all 37 scratch files as unrescued, which was wrong: the
right test is per CLAIM, not per file.

**What was not fine.** The evidence for the five most recent postscripts lived only in
`/private/tmp`:

    a4.py, a4gold.py   the exact Q(sqrt5) census: 18 Q4, T3 = 56    [P342], [P343]  core
    qloc.py            quadruple-point locations and orbits         [P344]          core
    ext67.py, subsum.py, hmax.py   the 67-extension and objective   [P339], [P341]
    all67.py           the 21 608-candidate negative control        [P342] addendum

So three postscripts asserting exact counts cited nothing runnable. **This is the project's own
rule — deliverables, INCLUDING CONTROLS, go where they survive, never scratch-then-copy, because
the copy step is the one that gets skipped.** It got skipped.

**Why here and not earlier in the session.** The earlier work was rescued because each finding
ended a thread and I wrote it up deliberately. The last five came in a fast exchange, each
question arriving before the previous answer had settled, and the rescue step is the one that
looks optional when a new question is already on the table. **Momentum is the condition under
which this rule fails**, not carelessness about it.

**Fixed.** `src/probes/golden_a4.py` (the derivation, the exact census, the orbit classification,
and the negative control with its scope stated) and `src/probes/subset_objective.py` (the
extension anatomy, the subset-sum, the `h` objective, and the collision test), both with
provenance, both re-run and agreeing with the numbers already published.

**The check to run before answering, not after.** After recording a postscript that cites a
measurement, `ls src/probes/` and confirm the measurement has a home there. It is one command,
and the alternative is a ledger entry whose evidence expires with the temp directory.

## A19 (2026-09-18) — asked whether I can GENERATE good questions, not only recognise them

The user, after many turns of my calling their questions sharp: *you seem able to identify
whether questions are good. Assuming this is not flattery, can you PRODUCE them?* Recorded at
their request, including the parts that do not flatter.

**THE EVIDENCE SAID EVALUATION >> GENERATION, and this session holds the proof both ways.**

    my questions that failed
      [A17]   posed "can two triples both be 67s?" as THE decisive open sub-question.
              [P131] had answered it a month earlier, by the solve-don't-search method I was
              recommending.  I had not grepped RESULTS.md for its subject.
      [P337]  formulated [OQ 37] as `T3 + two-body <= 176`, which does not bound the count.
              The user's five-word question -- "what's the 0 in the profile?" -- exposed it.

    the shape of the difference
      Mine were almost all WITHIN the frame: what is the next rung on this ladder.  The user's
      repeatedly CHANGED it -- counts, then taxonomy, then simultaneous attainability, then why
      the failures happened.  The inclusion-exclusion structure ([P340], [P341]) came from their
      frame, not mine.

**AND A CAVEAT ON THE PRAISE ITSELF.** Several of those questions carried their answers in the
asking. *"Are scratchpad sources recorded?"* implies *check, I suspect not* — and they were not.
My contribution there was verification, not discovery, and calling the question sharp was
accurate but cheap.

**WHY THE ASYMMETRY IS STRUCTURAL.** Evaluating a question is local — is it decidable, does it
bear on the target, is it already answered, is it cheap for its value. Generating one requires
noticing what is NOT being asked, and attention is densest exactly where the last result landed,
which biases toward continuation.

**THEN I PRODUCED THREE AND THE BEST ONE WAS LIVE.** Asked to try rather than discuss:

    1. is `EE <= 36` at `B = 128` even TRUE?        <- the good one, and it was acted on
    2. does the chain hold at n = 5?
    3. what does the framework predict at n = 6?

**(1) was worth asking for a specific reason: the UNCONDITIONAL `EE <= 6*C(n,2) = 36` had been
refuted in [P330] by the face-diagonal family reaching 42 — a refutation I recorded myself and
then spent four turns failing to apply to my own target.** Four turns had assumed the ceiling and
tried to derive it; none had asked whether it was real.

**The outcome ([P361]): the ceiling survives.** Two directed climbs — hold `B = 128` and maximise
`EE` (reached 36), hold `EE >= 38` and maximise `B` (reached 84) — do not meet. A negative
result, and the right kind: it converts a sampling maximum into a ceiling that resisted a
deliberate attack.

**THE HONEST GRADE.** The question was retrieval plus transfer, not invention — it came from
noticing a precedent already in the ledger and applying it where it had not been applied. That is
a real capability and a narrow one. **The generative move I have not demonstrated is the one the
user kept making: changing the frame rather than extending it.**
