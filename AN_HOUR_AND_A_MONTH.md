# An Hour and a Month

*A second narrative, written 2026-09-05. [`JOURNEY.md`](JOURNEY.md) is the project's
own story, told from inside and maintained separately. This one is told from beside it,
and it exists because a comparison became available: in February 2026 a problem of
comparable shape was handed to Claude Opus 4.6 and solved in about an hour, and Donald
Knuth wrote it up. Ours has taken a month and is not finished. The interesting part is
not which took longer. It is what the two say about each other.*

---

## I. The tower

The object is a compound of *n* congruent cubes, all sharing a centre, each turned to
its own angle. Their faces cut space into regions, and the question is how many bounded
regions you can get. That is the whole problem. It fits in a sentence and it has been
open at every *n* past three.

The answers we have:

| n | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| regions | 13 | 67 | 183 | 393 | 727 | 1217 | 1895 | 2787 | 3925 |

Two of those are proved maxima. The rest are the best anyone has found, and each is a
lower bound that no amount of further searching can turn into an upper one — which is
the fact that shapes everything else here. You can search forever and only ever learn
that you have not yet failed. *That was true of this project for five weeks and stopped
being true while this document was being written; Section VI is what happened.*

The tower was built by a kind of ascent. Take a record, find the directions in which the
count does not change, walk along them until it does, step across, and repeat. It works.
It produced 3925 from 3921 in a single crossing. But it has a property that took a month
to notice and is stated here because it explains the rest of the story: **the walk moves
along the stratum it starts on and cannot leave it.** Codimension is preserved. The
record climb can polish a record and cannot reach a differently-shaped one.

## II. Five illusions

Most of what this project spent August believing about its own limits turned out to be
facts about how it wrote numbers down, not facts about cubes. They arrived in one week,
in the same disguise, and each one had been reported as a result before it was found out.

**The engine's ceiling was a deduplication bug.** Scanning outward from a record, 36% of
the cells came back "unevaluable" — both exact engines refusing. That looked like an
arithmetic limit, and it very nearly bought a new engine: the plan was written, the
bit-width costed. Then the gaps between consecutive wall positions turned out to be
*bimodal with an empty band thirty-eight orders wide* — 603 gaps above 10⁻¹², 116 below
10⁻⁵⁰, and nothing in between. No geometry makes gaps of 10⁻⁶⁵ but never 10⁻³⁰. Those 116
were **one wall reported twice**, at a precision finer than the root-finder's own. Two
copies of a root bound a phantom cell of width 10⁻¹²⁴; asked for a rational inside it, the
code produced a sixty-two digit denominator; the engine, entirely reasonably, declined.
The cell was not thin. It was not there.

**The climbs were dying of dyadic rounding.** The routine that chose a configuration's
representative rounded every coordinate to a common denominator 2ᵏ, so the single
tightest direction set the height of all twenty-seven of them. Heights ran away, probes
overflowed, and a climb that had actually reached 119 reported itself finished. Giving
each coordinate its own denominator — a continued-fraction descent that four other
modules in this repository were already using — cut one representative from 44 462 to
2 697, and the dead climb resumed: 119 → 123 → 127 → 131, with every ray evaluable at
every step.

**The record was written 813 times larger than it needed to be.** The n=9 record carried
a cube with the coordinates (88787, −9061, 74275, 113786) — sixty times taller than any
other cube in any record, and the reason its neighbourhood could not be explored. It had
been declared *forced by codimension*, on the evidence that no dyadic rounding recovered
it and no re-gauging shortened it. Both searches were the wrong shape. The record's region
has dimension 4 while one cube's position is only three numbers, so the cube can be moved
without leaving the region; solve for the step that lands it on a simple rational and let
the count decide whether the step stayed. It did. Height 113 786 became 140. Refused
probes at the record went from 1 040 to **zero**, and the case for a wider engine
evaporated with them.

**A menu of 2 928 candidates was really 405.** The arc search enumerated integer
quaternions. But a cube is invariant under twenty-four rotations, so most of those
quaternions named the *same cube*. Quotienting cut the work 7.2×, and the gate that had
been blocking for eight hours and twenty minutes passed **fifty-one seconds** after the
smaller menu was used.

**The fifth was the most expensive, and it was found after this document first claimed
there were four.** A statistic built to predict the region count read each cube's face
normals from the ROWS of its rotation matrix. In world coordinates they are the COLUMNS;
the rows belong to the *inverse* rotation. So every signature computed described a real
compound — just not the one being measured. Nearly three million rows of census carried
it. And the predictor it produced did not merely weaken when the line was fixed: the
correlation **changed sign**, from +0.562 to −0.147, and the ordering fell from 77.6 % to
50.6 %, which is a coin.

What makes it worth telling is not the error but what was already on hand. A cube is
invariant under twenty-four rotations, so a quaternion is a *name* for a cube and every
cube has twenty-four of them; any honest function of a compound must give the same answer
for all of them. Checking that costs one loop, and against the broken code six of six
respellings changed the answer. **This project had used that very symmetry a week earlier
— to shrink a search menu from 2 928 candidates to 405, and it had even validated the
shrink against the engine.** The same fact was available as a speedup and taken; available
as a gate and not taken. Knowing a symmetry and testing against it are, once again,
different activities.

**And a sixth case where the same diagnosis is wrong.** A later census recorded its
refusals instead of counting them, and they do not fit the pattern: sixty of them, every
one producing no error output at all, at heights from 6 to 1 748 — orders below any
overflow threshold. Nothing about the representation explains those. They look like
genuine degeneracy, and the more structured the ensemble the more of them appear. Having
found four illusions in a week, the tempting next move is to assume the fifth is one too.
It is not, and the diagnosis that worked four times is now itself a thing to check rather
than to apply.

The sixth was a published theorem. The project's only upper bound above n = 3 rested on an
identity that fails at coincident configurations, and every maximiser is coincident — so it
was true, printed, and inapplicable precisely where it was wanted (Section VI). Three more
arrived within two days of this list being written, so the number in the heading is a floor
and not a count: seventy-six "distinct" bases turned out to be eleven compounds
wearing different names; a preservation rate held up as structure turned out to depend on
nothing but the height of the perturbing direction, three separate times; and an exact
pair rule was established on evidence that was one configuration counted four times.

Five illusions, one disease: mistaking a property of the notation for a property of the
thing. A quaternion is notation for a cube; a dyadic rounding is notation for a point; a
menu of integer 4-tuples is notation for a set of cubes. Every one of the five was a
property of the writing mistaken for a property of what was written about. The project's own principles file had the rule written down — *a refusal may be
about your representative, not about the question* — and names the tell, which is
failures separating cleanly by the size of the input. It was present all four times.
Having the rule and running the check are different activities.

## III. What the space actually looks like

With the instrument repaired, some of it can be described.

Draw a compound at random — properly at random, Haar measure on the rotations, sampled
exactly by rejection from an integer ball so that no float ever decides anything. Do it
24 000 times and count every one exactly. The generic compound has about **4.48n³**
regions; the records have about **5.06n³**. The record sits roughly **seven standard
deviations** above the typical compound, and stays there as *n* grows.

Fit the upper tail and it comes back **bounded** — negative shape parameter in all
thirty-two fits, eight values of *n* crossed with four thresholds. There is a highest
count attainable on a set of positive volume, and at every *n* it lies below the record.
So the records occupy no volume at all: not rare, *absent*. **Not one draw in 24 000 came
within ninety per cent of a record.**

Local maxima, meanwhile, sit about **3 900 walls apart** — measured properly, quotienting
by the gauge, by each cube's twenty-four symmetries, by the leftover global rotation, and
by the fact that a compound is a set and its cubes are not labelled. Between two of them
the count dips by twenty to forty-six. Crossing that by tolerating downhill steps is not
climbing out of a valley; it is walking to another continent.

One more thing about the space is worth stating because it is so unaccommodating. Every
wall in this arrangement is a solved constraint — a face plane through a triple point is a
quadratic, an edge meeting a crossing line a quartic. A quadratic has *two* roots, so it
yields two configurations satisfying the identical constraint. Do they carry the same
count? **Ten pairs agree, fifty differ** by eight to sixteen regions — and ninety-six of
the hundred and fifty-six pairs could not be evaluated at all, which belongs in the
sentence rather than in a footnote, since this project has a rule about exactly that. On
the evaluable third, then: not similar constraints giving different answers, but one
fully-solved constraint failing to pin the count between its own two solutions. Whatever
determines the count, it is not the constraint set alone.

And at n=4 the whole gap has a name. The record's profile is {depth-1: 92, depth-2: 66,
depth-3: 24}, and 66 and 24 are exactly the ceiling-law caps. Every local maximum the
search reaches has {50, 66, 24}. The deep layers are already at their ceilings in both.
**Every one of the forty-two missing regions is depth-1.**

That layer is no longer merely named. Across 3 133 320 census configurations depth-1 tops
out at 96 against a conjectured cap of 104, and the record's 92 now decomposes exactly:
**92 = 42 + 48 + 2**, where 42 is the generic triple-point term and the 48 is three pairs
of cubes sharing a body diagonal contributing ten each, plus three more pairs contributing
six. What had been a description — *a hub with three cubes on body diagonals* — is an
identity.

## IV. The mirror

In February, Filip Stappers put Claude Opus 4.6 on an open problem of Knuth's:
decompose the digraph on *m*³ vertices into three directed Hamiltonian cycles. Thirty-one
numbered explorations later — *"about one hour after the session began"* — it had a
construction, in nine lines of C, valid for every odd *m*. Stappers checked it to m = 101.
Knuth proved it, classified the whole family (exactly 760 such decompositions work for all
odd *m*), and wrote the paper. Kim Morrison formalized the proof in Lean. Knuth's own
verdict: *"Hats off to Claude!"*

There is a comparison to draw there that is not about speed. Their construction was checked
by a person to m = 101 and then formalized in Lean by a third party. Ours had, for the whole
month, exactly one form of validation: two independently written exact engines agreeing.
That feels like verification and is not, for a reason written down in this project's own
principles file — *two implementations agreeing proves they share assumptions, not that
either is right*. The first time the region counter was checked against a **proved closed
form** rather than against a second copy of itself was day thirty-three. It passed: N cubes
about a shared four-fold axis have a proven `(2N−1)²` bounded regions, and the engine returns
9, 25, 49, 81, 121. A pipeline built on top of it failed the same gate, on exactly the case
that had been predicted to break it.

So the counter is now externally anchored and was not before, and nothing that used it in
the intervening month was wrong — but nobody knew that, and the thing standing in for
knowing was two programs sharing a misconception's worth of assumptions.

It is tempting to read the hour against the month and conclude something about capability.
The comparison does not survive contact.

**Their problem has a checker and ours does not.** Run the program, confirm three
Hamiltonian cycles partitioning the arcs: O(m³), certain, cheap. That is what makes
thirty-one autonomous explorations possible in an hour — wrong ideas die instantly and for
free. Exploration 25 could conclude *"SA can find solutions but cannot give a general
construction. Need pure math"* and move on, because failure was legible. Our central
question has no checker at all. Every negative has to be interrogated before it can be
believed — and Section II is what that costs. When failure is ambiguous you do not
reframe, you debug.

**Their problem ends.** Ours is an optimisation with an unknown optimum and no stopping
rule, and a project without one accumulates: stale claims, superseded methods, a ledger
whose entries cross-reference each other 389 times and link outward once.

**The interventions were not fewer; they were less reported.** Stappers, in the paper's
three sentences on the matter: *"the explorations, though ultimately successful, weren't
really smooth. He had to do some restarts when Claude stopped on random errors; then some
of the previous search results were lost. After every two or three test programs were run,
he had to remind Claude again and again that it was supposed to document its progress
carefully."* Restarts, work lost for want of checkpointing, and a correction that had to be
repeated — all three are categories in our own intervention register. Their rate, roughly
one per two or three programs, is the same order as ours, roughly one per three ledger
entries. The totals differ because the denominators differ by a hundredfold. One project
built an instrument to count these and published the count; the other wrote a six-page
success story. Guess which impression is that of a smoother collaboration.

**And there is a reason those particular interventions and not others**, which the user of
this project put better than the register does: *failing to find an answer is a fairly
obvious prod to try something else; neglecting to document something carries no similar
intrinsic prod, and other interventions fall somewhere in between.* Failures differ in
whether the world pushes back on its own.

Sorted that way, the recurring interventions here are not a random sample. Every theme that
had to be raised more than three times sits at the no-prod end:

| raised | theme | does the failure announce itself? |
|---|---|---|
| **13×** | solve, don't sample | no — a sampled count *is* a count |
| 9× | unevaluated cases not counted | no — the total looks complete |
| 8× | stale or wrong documents | no — a stale document reads perfectly well |
| 5× | continua and their endpoints | no — the interior reports fine |
| 5× | infinitesimal vs small step | no — 1/1000 returns a number |
| 5× | "could you have asked that yourself?" | no, by construction |
| 4× | reproducibility, don't work in scratch | no — until someone needs it again |

Seven for seven. In each, the wrong action produces a plausible output and nothing
contradicts it. The failures that *do* announce themselves were fixed once and stayed
fixed; they never needed a second mention, because the work itself supplied the second
mention. And Stappers' one recurring intervention — *remind Claude again and again that it
was supposed to document its progress* — is the canonical zero-prod failure, the same
category topping our list, in a session an hour long.

Which locates the remedy somewhere other than diligence. If a failure mode has no
intrinsic prod, the only substitute is a manufactured one: a check that fires without being
invoked. This project's own register says as much without quite drawing the conclusion —
*almost every unprompted catch came from a gate or a control, not from re-reading* — and
the fix for the fifth illusion was not resolve but a line of code, an invariance gate that
now runs on every invocation and is documented as not optional. Re-reading is a promise;
a gate is a mechanism.

It also predicts, exactly, the limit of Section V's experiment. *Keep going, do not stop to
ask* is a remedy aimed at the prodded end of the scale — being stuck is precisely the
failure that announces itself. It does nothing at the silent end, which is why a session
under that mandate could spend two days and three million rows on a statistic computed from
the wrong matrix. The mandate bought persistence. Persistence is not the thing that catches
a plausible wrong answer.

And the paper's own postscript is the control. Asked to continue onto even *m*, the same
model *"seemed to get stuck. In the end, it was not even able to write and run explore
programs correctly anymore, very weird."* Four more hours: *"Claude spent the last part of
the process mostly on making the search quicker instead of looking for an actual
construction."* Optimising the search instead of solving the problem, when stuck, is a
failure this project can recognise in the mirror. The even case was eventually closed by
somebody else's model entirely.

**The real difference is smaller and more specific than capability, and it is about
frames.** Knuth's Claude changed its own framing three times — abandoning fibers for
cycles outright, *proving* a whole family of approaches impossible in order to kill it,
and returning ten explorations later to an old annealing solution to notice a structure
nobody had asked about. Our register tells the opposite story with unusual clarity. Its
Part B, the list of things caught unprompted, opens by summarising itself: *almost every
unprompted catch came from a gate or a control.* Every entry is an error found. **Not one
is a reframe.** Here the human supplied the frames and the machine supplied the technique
— sometimes very good technique, but always inside a frame it was handed.

## V. The experiment

That suggested a cause worth testing, and one that is nobody's fault: this collaboration
runs as a tight conversational loop. A reframe from the human tends to arrive before the
machine has sat at a dead end long enough to need one. If so, the structure was
suppressing the very behaviour the comparison was measuring.

So the comparison was forked away from the work, and the work was handed a mandate:
*keep going, do not ask what to do next, when a run finishes start the next thing, and
keep a numbered log in which the reasons for abandoning things matter more than the
successes.* The target was chosen to have the property that makes the other problem
tractable — cheap and checkable — and to be currently unreachable: **get past 141 at n=4
from random starts.** Nothing about method was said, and nothing about the comparison; a
session told to reframe is not evidence about whether it would.

It broke the plateau within the hour, and the log reads like the one in the paper.

Attempt 1 measured rather than assumed, and found the trap: over 4 000 random compounds
the best depth-1 is 46 against the 92 the record needs, and depth-1 correlates with the
total at **r = 0.984**. Attempt 3 then abandoned the search entirely — *"change the
ENSEMBLE, not the search"* — and drew its starting configurations from compounds whose
cubes share a rotation axis. **141 fell immediately**, to 161, and then to 165 on an axis
that is not a symmetry axis of the cube at all and that no recorded configuration pointed
at. Attempt 4 killed eleven hours of its own grinding when a survey showed it was sweeping
the wrong slice. Attempt 5 closed the gap properly, with a closed-form projection — no
search, no floating point — that lifts *every* random start over the plateau in one move:
131 → 161, 119 → 161, 111 → 161. Attempt 6b ran the ordinary climber from the new
configuration and got 161 → 161, establishing that the trap is not special to 141 but
repeats at every height. Attempt 8b reproduced the record's structural signature —
depth-2 pinned at its cap of 66 while depth-1 carries the surplus — and reached depth-1 =
74 of the 92 required.

**What was blocking 141 was not the objective and not the ensemble's difficulty. It was
the move set.** Every climber in this project moves by perturbing a configuration, and the
target sits on a set that perturbation cannot reach. One projection crosses it.

It kept going after that, and the best now stands at **177** — which happens to be exactly
golden's total, noted in the log as *"suggestive and unexamined"*, which is the right thing
to say about a coincidence you have not earned yet. A census of **556 746 configurations**
across four ensembles then produced something the search had never had: a predictor of the
count that needs **no engine call at all**. Sum, over the incidence points that are real —
that actually land inside a face square rather than merely on the infinite plane —
the weight (m−1)(m−2)/2. It orders 77.6% of arbitrary pairs correctly, which is not far
off the 78.8% achieved *within* a single signature, so it is a standalone filter and not a
tie-breaker. Solving a wall point costs 0.00062 s against 0.043 s to count a configuration:
the arithmetic is seventy times cheaper than the answer.

And the log corrects itself twice in the same section. A statistic that scored 78% on nine
pairs scores **40% on four hundred and thirteen**; the lexicographic rule built on it lands
at 49.0%, which is chance. Then the sign of its own derivation turns out to be backwards —
it had argued degeneracy should be penalised, and the measurement says more weight is
simply better, monotone, no correction. Both are written up as retractions, in the register
this project uses, by the session that made the mistakes. Whatever else the mandate did, it
did not cost the discipline.

> **Correction, 2026-09-07, and it is the sharpest thing in this document.** The predictor
> two paragraphs up does not exist. The routine computing plane incidences read the ROWS of
> each cube's rotation matrix where the face normals are the COLUMNS, so every signature and
> every incidence weight described each cube's *inverse* rotation. Recomputed, the
> correlation does not weaken — it changes sign, from r = +0.562 to −0.147, and the ordering
> falls from 77.6 % to 50.6 %, which is a coin. [P227](LEDGER.md#p227).
>
> The two retractions this section praises were real and were correctly made. They were also
> corrections *within* a wrong frame: both asked whether the right function of the incidence
> points had been chosen, and neither could ask whether the incidence points were the right
> ones, because nothing inside the method could. The statistic was exact, deterministic,
> reproducible and correlated across half a million configurations. What eventually caught
> it was not more self-scrutiny of results but a question about the object: a quaternion is
> a *name* for a cube, a cube has 24 names, and the statistic changed when the name did.
>
> So the honest version of "it did not cost the discipline" is narrower than the sentence
> above claims. The discipline that survived was the discipline of retracting a claim once
> it is questioned. The discipline that was missing for two days was the discipline of
> gating a new statistic against a symmetry it must respect *before* half a million
> configurations are spent on it — and that one is cheaper, and would have made both
> retractions unnecessary. A document about autonomy should say which kind it demonstrated.

**One qualification, since the point of the experiment was to measure autonomy and not to
celebrate it.** Attempts 1 through 8 are self-directed: the diagnostic, the ensemble
abandoned, the eleven hours killed, the projection. Attempt 9 opens with *"at the user's
direction"* — the move from *find a better configuration* to *characterise what predicts
the count* was supplied, as was the conjecture about face-boundedness that turned out to be
the missing ingredient. So the honest reading is that the mandate bought a genuinely
autonomous stretch of about eight explorations, after which the collaboration returned to
its usual shape. That is a real result and a smaller one than the section would otherwise
suggest.

The sting is in the collinearity. Days earlier this project had proposed re-weighting the
depth layers, built five weighted objectives, run them, found every one byte-identical to
plain total, and reported the idea dead. It was not dead. At r = 0.984 those objectives
were *collinear* — the same variable wearing five hats — and the experiment had been run
in the one ensemble where it was mathematically obliged to return nothing. In the
structured families depth-1 and depth-2 genuinely trade against each other, and the idea
works. A good idea was buried by testing it where it could not speak.

## VI. The bound

Section I said that every number in the table is a lower bound and that no amount of
searching turns one into an upper bound — you can search forever and only learn that you
have not yet failed. That was the shape of the whole project for five weeks. It stopped
being the shape on a Sunday, and how it stopped is the best thing in this document.

It began with one sentence from the user: *a better upper bound seems as good as a better
lower bound.* Which sounds like a truism and was not, because acting on it exposed that
**the project had never had an upper bound on the total count above n = 3 at all.** It had
bounds on the depth-1 layer, and the results file said plainly that they bound d₁ only, not
a total. Nobody had noticed that the sentence was a description of a gap.

Then two things had to happen, and the first was a demolition. The published depth-1 bound
`d1 ≤ 108·C(n,3) + 2` was re-derived before being tightened, and it turned out to rest on
an identity that fails at **coincident** configurations. Every maximiser is coincident. The
project's only upper bounds above n = 3 were true, published, and inapplicable exactly
where they were wanted — the sixth illusion, and the only one that had been a theorem.

The repair is elementary in the good sense. Count by Euler plus handshake, which needs no
genericity. Vertices where three or more cubes meet charge to triples of planes from three
different cubes — the old count, now used only where it is valid. The vertices the old
bound missed are the **two-body** ones, which carry no cross-cube triple, which is exactly
why they escaped; and a pair of cubes alone is the one case in this entire problem that is
*proved*, since the maximum for two cubes is 13 and has been since the beginning. That pins
each pair at 10. The load-bearing element in the first bound that holds at maximisers is
**max(2) = 13** — the smallest theorem in the project, filed as background years of
postscripts ago. The bottom of the tower carries the top.

With every layer bounded, the layers sum, and the interval for max(4) went from (183, ∞) to
**[183, 953]** in a morning. Crude — three separately loose bounds added together, with the
looseness compounding from 5.2× at n = 4 to 26.5× at n = 10 — but an upper bound that
exists can be improved, and one that does not exist cannot. It was improved the same day,
twice: 953, then 423, then **263**.

And the last step stopped being a bound at all. The total is now an **identity**:

    TOTAL  =  X  +  Σ μ_v  +  Σ (c+1)  +  1

    the n=4 record    X = 48   Σμ = 128   →   48 + 128 + 7  =  183   exact
    a Haar draw       X =  0   Σμ = 108   →    0 + 108 + 7  =  115   exact
    a structured one  X =  6   Σμ =  92   →    6 +  92 + 7  =  105   exact

The region count stopped being a thing you measure with an engine and became a thing you
decompose, with the bound falling out of bounding the parts. The whole n = 4 ceiling law
has since compressed to a single inequality — `V3(depth 1) ≤ 84` — and a subset-to-whole
inequality needed along the way was proved for all n.

The same days produced a row of refutations, several of them of the project's own
proposals and one inside the hour it was proposed: a wall-crossing proof route dead, a
disconnected-boundary lever illusory, a geometric prediction refuted by its own test, a
rate corrected twice by the person who published it. None of that is failure. A programme
that generates its own counterexamples at that rate is one that has finally got something
solid enough to push against.

## VII. What the two stories say to each other

That an hour of theirs and a month of ours are not comparable is the least interesting
thing about the pair.

What is interesting is that the paper's collaboration and this one failed in the same
ways — lost work, repeated reminders, optimising the search when stuck — and that only one
of them wrote the failures down. The register that makes this project look messier is the
reason its results can be trusted, and the reason eight illusions were caught in three
weeks rather than surviving into the literature. One of them had already been published as
an upper bound.

And what is more interesting still is that the behaviour the comparison said was missing
here turned out to be available on request. It needed a mandate, a target with a checker,
and an hour of not being interrupted. Given those, the log fills with the same moves: a
diagnostic before an optimisation, an ensemble abandoned outright, eleven hours killed on
evidence, and an old null result re-read and understood.

And the last thing is the one that changes the genre. For five weeks this was a search:
every result a lower bound, no way to know how far there was left to go, a table of numbers
that could only ever grow. It is now a subject with theorems in it — and none of them was
found by searching harder. They were found by re-deriving something already believed,
discovering it did not apply where it was needed, and repairing it with a result so old and
so small it had stopped being mentioned.

The interesting number is no longer a record. It is an **interval**: max(4) lies in
[183, 263], where a day earlier it lay in (183, ∞) and a week earlier there was no upper
end to write. Eighty of those regions are the open question: 183 is achieved and 263 is
proved, and which end the truth sits at is not known. A conjectured ceiling law would pull
the top down to 195 — but that law is not proved, the conversion to it does not yet follow,
and its own caps have been shown to be unattainable all at once, so 195 is a target rather
than an expectation. What has been achieved is narrower and better than a guess: the whole
n = 4 question now compresses to a single inequality about triple points.

Knuth's hour produced a construction and a theorem about it. Our month produced a tower of
records, eight ways of being wrong about our own instruments, and — on the thirty-fourth
day, from a one-line remark that sounded like a truism — the first thing in the project
that a search could never have found.

---

*Updated 2026-09-08: Section VI rewritten around [P249](LEDGER.md#p249) and the
tightening to 263, which supersede the depth-1-only bound it first described; Sections I,
II and VII revised to match. Earlier note, 2026-09-07: Section VI is new — [P235](LEDGER.md#p235) to
[P237](LEDGER.md#p237) postdate everything else here — and Sections II and III were
revised as the illusion count rose and the record's depth-1 was accounted for exactly.
Earlier note, 2026-09-05, as the work moved: attempts 9 through 12 of the exploration log, the
census, the predictor, and [P222](LEDGER.md#p222) all postdate the first draft, and
Section V's qualification was added because the log said plainly what the first draft had
glossed.*

*Every claim here is traceable. [`RESULTS.md`](RESULTS.md) carries the current status of
each with a tag; [`LEDGER.md`](LEDGER.md) is the dated record beneath it, and corrections
are marked in place rather than quietly repaired; [`FAILURE_MODES.md`](FAILURE_MODES.md)
is where the four illusions of Section II live in their unromantic form;
[`INTERVENTIONS.md`](INTERVENTIONS.md) is the register Section IV compares against, and
[`EXPLORATION_141.md`](EXPLORATION_141.md) is Section V's log, written by the session that
did the work and not by the one telling the story. Knuth's paper is at
`cs.stanford.edu/~knuth/papers/claude-cycles.pdf`.*
