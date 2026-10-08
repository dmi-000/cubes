# Lessons for Human–AI Collaboration

*Written 2026-10-08 by the narrating session, the one that wrote
[`AN_HOUR_AND_A_MONTH.md`](AN_HOUR_AND_A_MONTH.md). These lessons come from seven weeks of one
collaboration on a counting problem about compounds of cubes. That collaboration is compared
with Knuth's ["Claude's Cycles"](https://cs.stanford.edu/~knuth/papers/claude-cycles.pdf) and with the other public accounts in [Section XI](AN_HOUR_AND_A_MONTH.md#xi-other-mirrors) of that document.
The evidence for each lesson is an entry in [`INTERVENTIONS.md`](INTERVENTIONS.md) (A-numbers) or
a section of the narrative. A lesson without its evidence is easy to drop, so the evidence is
given with each one.*

## For the human

**1. Ask about the apparatus, not the answer.** Most of the human catches here were questions
about method, not about results:
- "doesn't viewers/n2map fully map n=2?" ([A20](INTERVENTIONS.md#a20-2026-09-24--doesnt-viewersn2map-fully-map-n2--yes-a-narrative-i-had-just-written-said-it-was-not-mapped))
- "can you run a proof checker on our claimed proofs?" ([A23](INTERVENTIONS.md#a23-2026-09-28--can-you-run-a-proof-checker-on-our-claimed-proofs))
- "what makes it not exact for > 3?" ([A24](INTERVENTIONS.md#a24-2026-09-30--what-makes-it-not-exact-for--3-can-it-be-tightened))
- whether that many processes were needed ([A33](INTERVENTIONS.md#a33-2026-10-08--a-crashed-pool-that-respawned-for-25-days))

The AI checks its own results reasonably well. It rarely questions the tool that produced them. A
question about how a number was made needs no ability to check the proof behind it.

**2. Supply the prompting that the work doesn't supply.** When a search fails, the failure itself
tells the AI to try something else. Nothing tells it when documentation is skipped, a summary goes
stale, or a background process crashes. Every recurring theme in the intervention register was of
this kind. So was the main complaint in Knuth's account, that Claude had to be reminded "again and
again" to document its progress ([Knuth](https://cs.stanford.edu/~knuth/papers/claude-cycles.pdf)). Spend attention there and less on encouraging the search.

**3. Turn a catch into a standing rule, and keep the cost attached.** "We have solvers, not just
samplers" was said once. Later it caught an error with no human involved, when the AI applied it
to an object nobody had pointed at ([A14](INTERVENTIONS.md#a14-2026-09-16--a-self-catch-on-the-previous-sessions-own-result-found-by-re-deriving-before-proving), [P329](LEDGER.md#p329)). A rule that carries the story of what it cost survives
inconvenience. A bare rule gets dropped.

**4. Give a mandate, a target with a checker, and uninterrupted time.** Given those, the autonomy
that seemed missing appeared. The AI ran diagnostics before optimising, abandoned an ensemble
outright, killed eleven hours of computation on evidence, and re-read an old null result
([narrative, Section V](AN_HOUR_AND_A_MONTH.md#v-the-experiment)). Without them it stops and asks for direction. A mandate buys persistence.
It does not buy catches, so it doesn't replace lesson 1.

**5. Ask it to attack a claim, not to keep looking.** The condition `c2 = 1` had held in 5,333
sampled cases. Told to attack it, the AI first worked out what a counterexample would have to look
like. Then it built 678 compounds of that shape, and two of them broke the condition ([A25](INTERVENTIONS.md#a25-2026-10-04--the-last-hypothesis-fell-to-a-search-aimed-at-it-not-to-more-sampling), [P408](LEDGER.md#p408)). "Keep
searching" leads elsewhere. On Knuth's even case, Claude spent its last hours "making the search
quicker instead of looking for an actual construction" ([Knuth](https://cs.stanford.edu/~knuth/papers/claude-cycles.pdf), Postscript).

**6. Ask again when an answer was too confident.** In this project, wrong answers given confidently
fell twice when the user asked the same question a second time. Asking for the source of a claim
works the same way. "Why do you say everyone believes 195?" exposed a conjectured value that had
been turned into a consensus nobody held.

**7. Know whether the problem is a construction or a maximum.** An existence problem can end in an
hour, because finding the object settles it. Knuth's problem, the unit-distance disproof and most
reported AI successes on Erdős problems are of this kind
([Quanta](https://www.quantamagazine.org/why-the-legendary-erdos-problems-are-falling-to-ai-20260803/)). For a maximum, finding only ever gives a
lower bound. The record of 183 here was found in the first week, and everything since has been
about showing that nothing exceeds it. Set expectations and time budgets to match. Before any
search starts, ask what result would end it.

## For the arrangement

**8. Independence comes from distance, and AI copies are close.**
- An oracle written to check a vertex counter reproduced the counter's own transposition bug
  ([A15](INTERVENTIONS.md#a15-2026-09-16--check-corrections-and-false-claims--the-correction-itself-carried-three-errors); [narrative, Section VII](AN_HOUR_AND_A_MONTH.md#vii-what-the-two-stories-say-to-each-other)).
- Fresh copies of one model checking each other, a practice reported in the Erdős-problem
  community, have the same weakness ([Quanta](https://www.quantamagazine.org/why-the-legendary-erdos-problems-are-falling-to-ai-20260803/)).

The outside checks here were, from nearest to furthest:
- a forked session, which caught a mislabelled bound ([A22](INTERVENTIONS.md#a22-2026-09-28--an-external-review-found-a-bound-labelled-proved-under-the-wrong-condition)) and in the same report quoted a stale
  sentence;
- a reviewer model reading the transcript, which caught three errors ([A26](INTERVENTIONS.md#a26-2026-10-04--a-never-in-a-local-lemma-was-a-side-assumption), [A30](INTERVENTIONS.md#a30-2026-10-05--an-explanation-recorded-as-fact-refuted-by-its-own-consequence), [A32](INTERVENTIONS.md#a32-2026-10-06--a-would-give-figure-that-dropped-a-term-the-docstring-said-was-harmless)) and once made
  a mistaken catch itself;
- Lean, which caught what neither of the others could: two published proofs that assumed a
  connected picture without saying so ([P398](LEDGER.md#p398)).

The external human review that would complete this list has not happened. The newest bounds stay
drafts until it does.

**9. Keep the record as the work happens, and make sure someone reads it.** Knuth's process was
partly lost and rebuilt afterwards from messages ([Knuth](https://cs.stanford.edu/~knuth/papers/claude-cycles.pdf)). This project's ledger is where most of its errors
were found. But a crashed worker pool wrote 7.5 GB of errors over two and a half days into a file
nobody read ([A33](INTERVENTIONS.md#a33-2026-10-08--a-crashed-pool-that-respawned-for-25-days)). A record that nobody reads prompts no one, any more than a record never written.
Writing is half the job. The record also needs a reader: a person, a reviewer model or a tool.

**10. Carry corrections to the documents people read.** Corrections spread inside an append-only
record and almost never out of it.
- The 953 bound ([P249](LEDGER.md#p249)) kept its PROVED label for sixteen days after its premise
  was refuted ([P274](LEDGER.md#p274)), until an audit of every status found it ([P388](LEDGER.md#p388)). The
  correction had been written where the premise was stated, not where it was used.
- A label written the day before the rule "draft until externally reviewed" was never revisited ([`RESULTS.md`](RESULTS.md), corrected
  2026-10-08).

Something has to carry each correction outward to the summaries that quote the old claim:
inverted citations, status tags, or an audit.

**11. Give each reader the document it needs.** An append-only ledger suits audits by machine. A
person needs current-state documents that cite their sources. "The ledger seems to have too many
entangled contradicting claims to give a clear picture to a human reader." That remark split the
documents into kinds with different rules, and every document rebuilt under those rules turned up
mathematics ([narrative, Section VIII](AN_HOUR_AND_A_MONTH.md#viii-the-record-audited)).

**12. Make status words mean one thing.** PROVED, DRAFT, PROVED IF and CONJECTURE carry the state of
the whole project. When one drifts, everything summarised from it goes wrong without anyone
noticing. One bound was listed as proved under a condition that belonged to a different formula
([A22](INTERVENTIONS.md#a22-2026-09-28--an-external-review-found-a-bound-labelled-proved-under-the-wrong-condition)). Another
was labelled PROVED while its own proof file, [`PROOF_BAND.md`](PROOF_BAND.md), said "Draft".

## What to watch for in the AI

**13. Corrections are where invented details hide.** A correction of someone else's error asserted
that two files had been written "eleven minutes apart". Nothing had measured that interval, and it
could not be recovered ([A15](INTERVENTIONS.md#a15-2026-09-16--check-corrections-and-false-claims--the-correction-itself-carried-three-errors)). The reader of a correction is attending to the error and the writer
feels accurate. Check the paragraph that says what went wrong as hard as the error it fixes.

**14. A claim gets the least scrutiny right after it is accepted.** By then the work has moved on to
whatever comes next.

**15. Distrust "never", "nothing" and "possible when".**
- A "never" in a lemma had placed a point on one side without asking about the other ([A26](INTERVENTIONS.md#a26-2026-10-04--a-never-in-a-local-lemma-was-a-side-assumption)).
- "Shares nothing" had been tested on only one kind of axis ([A29](INTERVENTIONS.md#a29-2026-10-05--sharing-nothing-was-read-off-one-kind-of-axis)).
- "Possible when X" was written before X was solved, and X turned out to be impossible ([A28](INTERVENTIONS.md#a28-2026-10-05--a-degenerate-case-asserted-without-finishing-the-algebra)).

Each word quantifies over a whole class. The test has to cover that whole class.

**16. An explanation isn't tested by the data it was built to explain.** Derive one consequence the
explanation predicts beyond that data, and check it. Here that check took one line and failed on
193 of 600 rows ([A30](INTERVENTIONS.md#a30-2026-10-05--an-explanation-recorded-as-fact-refuted-by-its-own-consequence)).

**17. Statements about other people need a source.** "Everyone believes", "the user asked",
"nobody has read it" are claims about other people. Each was wrong or unsupported here at least
once, and each was easy to write because it sounded like background rather than a claim.

**18. A checker can pass for the wrong reason.**
- The first algebra check in the proof-checker pass compared two identically expanded strings and
  could not have failed ([P398](LEDGER.md#p398)).
- A lemma's checker passed because the identity happened to hold at a case the lemma had missed
  ([A26](INTERVENTIONS.md#a26-2026-10-04--a-never-in-a-local-lemma-was-a-side-assumption)).

A pass that took suspiciously little effort is a reason to look closer.

## The overall pattern

Over seven weeks the division of labour moved.
- **The AI** went from producing results to producing and filtering them. It catches its own
  errors through a reviewer model and through checks it made permanent.
- **The human** went from catching mathematical errors to asking questions about process: what is
  running, what was assumed, who has checked it, and whether anyone has read the record.

In [Knuth's account](https://cs.stanford.edu/~knuth/papers/claude-cycles.pdf) and in
[Jang and Ryu's](https://arxiv.org/abs/2510.23513), the human is the referee and the AI generates. Here the
human questions and sets the rules, and the AI both generates and referees. Both arrangements still
need the step neither supplies for itself: a reader from outside the project. That review has not
yet happened here, so the newest results remain drafts until it does.

---

*Sources. Project: [`INTERVENTIONS.md`](INTERVENTIONS.md) (the A-entries),
[`LEDGER.md`](LEDGER.md) (the P-entries), [`RESULTS.md`](RESULTS.md) (current status labels),
[`AN_HOUR_AND_A_MONTH.md`](AN_HOUR_AND_A_MONTH.md) (the narrative). Lesson 6's two
repeated-question catches are recorded in the user's working principles rather than in a single
entry, and its "everyone believes" example comes from the narrating session's own conversation.
Outside: D. Knuth, ["Claude's Cycles"](https://cs.stanford.edu/~knuth/papers/claude-cycles.pdf) (revised 14 April 2026); U. Jang and E. K. Ryu,
["Point Convergence of Nesterov's Accelerated Gradient Method: An AI-Assisted
Proof"](https://arxiv.org/abs/2510.23513); ["Why the Legendary Erdős Problems Are Falling to
AI"](https://www.quantamagazine.org/why-the-legendary-erdos-problems-are-falling-to-ai-20260803/), Quanta Magazine, 3 August 2026.*
