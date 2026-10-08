# An Hour and a Month

*A second narrative, written 2026-09-05. [`JOURNEY.md`](JOURNEY.md) is the project's
own story, told from inside and maintained separately. This one is told from beside it,
and it exists because a comparison became available: in February 2026 a problem of
comparable shape was handed to Claude Opus 4.6 and solved in about an hour, and Donald
Knuth wrote it up. Ours has taken a month — six weeks, by the last section — and is not
finished. The interesting part is
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
that you have not yet failed. Searching is still like that. But at the start of September
the project began trying to *prove* upper bounds, and believed for more than two weeks that it
had one it did not have (Section VI). At the end of September it got a real one, by argument
and under a proof checker (Section IX).

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

**And one case where the same diagnosis is wrong.** A later census recorded its
refusals instead of counting them, and they do not fit the pattern: sixty of them, every
one producing no error output at all, at heights from 6 to 1 748 — orders below any
overflow threshold. Nothing about the representation explains those. They look like
genuine degeneracy, and the more structured the ensemble the more of them appear. Having
found four illusions in a week, the tempting next move is to assume the next is one too.
It is not, and the diagnosis that worked four times is now itself a thing to check rather
than to apply.

The sixth illusion was a published theorem. The project's only upper bound above n = 3 rested on an
identity that fails at coincident configurations, and every maximiser is coincident — so it
was true, printed, and inapplicable precisely where it was wanted (Section VI). Three more
arrived within two days of this list being written, so the number in the heading is a floor
and not a count: seventy-six "distinct" bases turned out to be eleven compounds
wearing different names; a preservation rate held up as structure turned out to depend on
nothing but the height of the perturbing direction, three separate times; and an exact
pair rule was established on evidence that was one configuration counted four times.

The purest of them arrived last. The n=4 record was recorded as sitting on a
three-dimensional plateau, measured by probing 19 682 signed directions and finding 26 that
still counted 183. But the perturbation multiplied each displacement by the quaternion's
first component, and cube 1 of the 183 is `(0, 5, 3, 2)` — a half-turn, whose first
component is **zero**. The 26 survivors were not nearby configurations with the same count.
They were byte-identical to the record. A plateau three dimensions wide was twenty-six
copies of one point, and a comparison for equality would have found it in a second. The
correction then overshot: the record was re-declared *isolated*, 0-dimensional — although an
earlier postscript had already traced a curve through it, which nobody re-read. The count
turns out to be constant along that curve: each of the two 183 classes lies on its own arc,
the tower's of length 0.6873. Neither three dimensions nor none. One.

The author of this document then committed the same error while auditing for it. Checking a
register's citations, I searched the ledger for `id="p295"` — the HTML anchor — found none
above P287, and reported that every postscript from P288 to P303 — seven of which the
register cited — "does not exist anywhere." They all existed. What was missing was the anchor markup, appended-to entries having been written
without it, so the links landed at the top of a twenty-one-thousand-line file instead of
nowhere. The measurement was accurate and the inference was not: I had grepped for notation
and reported a fact about substance. The other session diagnosed it correctly and had added
the missing anchors within the hour.

Five illusions, one disease: mistaking a property of the notation for a property of the
thing. A quaternion is notation for a cube; a dyadic rounding is notation for a point; a
menu of integer 4-tuples is notation for a set of cubes. Every one of the five was a
property of the writing mistaken for a property of what was written about. The project's
own principles file had the rule written down — *a refusal may be
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

There is a second mechanism, and it was found by asking for a picture. The user wanted a
drawing of how the record regions relate; a dozen short questions followed about what each
mark meant — *do those arcs meet? does that dashed line reach the 1217? are those dots the
boundary?* — and **every one of them was answerable only by a measurement nobody had made.**
Six new results came out of a request for a diagram, and one of them was that the boundary
in question had never been measured at all.

The reason is worth naming because it generalises. Prose can describe a relationship without
committing to it: *the plateau runs in two directions* is a complete sentence and decides
nothing. A drawing must put every mark somewhere — it has to decide whether two things span
anything, where they cross, where they stop — and each of those placements is a claim. An
unmeasured claim in prose is invisible; an unmeasured claim in a picture is a shape that
looks wrong to anyone who looks. So a diagram is a prod-manufacturing device for exactly the
class of failure that has none, and it works by removing the option to be vague.

Four sessions running now, the defects have been found by questions aimed at the
**apparatus** — what does this mark mean, does this line reach that one, is this tool
measuring what its name says — and not by questions aimed at the conclusions. That is
consistent with everything else here: the conclusions prod, eventually. The instruments
never do.

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

It kept going after that, and the best reached **177** — which is exactly golden's total,
noted in the log as *"suggestive and unexamined"*, the right thing to say about a coincidence
you have not earned yet. (It was later earned: the golden 177 turned out to be the compound
that refuted one of the project's own conditional proofs.) A census of more than half a million
configurations then produced what looked like the first cheap predictor of the count — a sum
over incidence points needing no engine call, ordering 77.6 % of pairs correctly — and the log
retracted two weaker statistics along the way, in the project's usual register.

**The predictor did not exist.** The routine computing plane incidences read the rows of each
cube's rotation matrix where the face normals are the columns, so every signature described
each cube's *inverse* rotation. Fixed, the correlation did not weaken; it changed sign, and the
ordering fell to 50.6 %, a coin. This is the fifth illusion of Section II, seen from inside the
session that made it, and its lesson is narrower than "the mandate kept the discipline". The
two retractions were real, and both were corrections *within* a wrong frame: they asked whether
the right function of the incidence points had been chosen, and nothing inside the method could
ask whether the points were right. What caught it was a question about the object — a cube has
twenty-four names, and the statistic changed when the name did. The discipline that survived
the mandate was retracting a claim once it is questioned. The one that was missing was gating a
new statistic against a symmetry it must respect *before* half a million configurations are
spent on it, which is cheaper and would have made both retractions unnecessary.

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
searching turns one into an upper bound. For five weeks that was the whole shape of the
project. Then it seemed to change in a single day, and the true story of that day is better
than the one this section first told.

It began with one sentence from the user: *a better upper bound seems as good as a better
lower bound.* Which sounds like a truism and was not, because acting on it exposed that
**the project had never had an upper bound on the total count above n = 3 at all.** It had
bounds on the depth-1 layer, and the results file said plainly that they bound d₁ only, not
a total. Nobody had read that sentence as a description of a gap.

The first thing to happen was a demolition. The published depth-1 bound was re-derived before
being tightened, and it rested on an identity that fails at **coincident** configurations —
and every maximiser is coincident. True, published, and inapplicable exactly where it was
wanted: the first of two illusions in this story that had been printed as theorems. The
second is below.

The repair is elementary in the good sense. Count by Euler plus
handshake, which needs no genericity. Vertices where three or more cubes meet charge to
triples of planes from three different cubes. The vertices the old bound missed are the
**two-body** ones, which carry no cross-cube triple — exactly why they escaped — and a pair of
cubes alone is the one case in this whole problem that has always been *proved*: two cubes
make at most 13 regions. That pins each pair's contribution at 10, and gives

    d₁  ≤  108·C(n,3)  +  10·C(n,2)  +  2      for every n and every configuration

The load-bearing element is **max(2) = 13**, the smallest theorem in the project, filed as
background from the first week. The bottom of the tower carries one layer of the top — or so
it seemed for three weeks. When the proofs were finally put through a proof checker (Section
IX), the final `+2` turned out to be Euler's formula for a *connected* picture, and nothing
proves the top layer's picture is connected. It is connected in every case ever measured. That
is not the same thing, and the honest form of the bound carries an unknown `c₁ + 1` where the
`2` was. The depth-1 ceiling that *is* now proved without any assumption came three weeks
later by a different route, and it is much tighter: `d₁ ≤ 10n² − 14n`, 104 at four cubes
against the 494 above.

Then the day ran on, too fast. The deeper layers got bounds of the same shape, the layers
were summed, and by the evening the interval for max(4) read [183, 953], then [183, 423],
then **[183, 263]**, and the total was written down as an exact identity in four terms, checked
on the record, a random compound and a structured one. This document said, for three weeks,
that the genre had changed.

It had not, and each piece came apart in a different way:

- **The 953 had a hole.** The bound for depths two and above assumed that two-body vertices
  never occur there. The very next day a postscript found that they do, and corrected the
  sentence where the assumption was *stated* — but not the sentence where it was *used*. The
  953 kept its PROVED tag for sixteen more days, in the results file built to prevent exactly
  that, until an audit of every bound's status found it. It is almost certainly true, since
  it exceeds every measurement fivefold, and the repair looks mechanical. It has not been made.
- **The 423 and 263 were never unconditional.** They assumed every level of the arrangement
  is connected in a particular sense; that is not proved, and it is sometimes false. A weaker
  form of the same assumption gives **198**, which is better than both, though a proof checker
  later showed it also leans on an accounting step that was argued and never verified, until a
  proof of that step was drafted in October.
- **The identity survived; its shorthand did not.** `TOTAL = X + Σμ_v + Σ(c+1) + 1` is still
  an identity. But the three compounds it was first checked on all had `Σ(c+1) + 1 = 7`, and
  the n = 4 work that followed wrote it as `7 + T + B − Q4`, with the 7 as a constant. It is
  not one: it ranges from −3 to 7, and the shorthand also silently drops three kinds of
  degenerate vertex that about one random compound in seven carries. It was caught by checking
  a climb's result against the engine instead of against the formula — which predicted 177
  where the engine said 175.
- **And max(4) = 183 itself lost its proofs.** Three times it was reduced to a handful of
  inequalities, and three times one of them was refuted — twice by a single compound of 173
  regions, found by seeding the search from the smaller case where the analogous law already
  fails rather than from the record; once by the golden 177, which
  had been in the project since the first day and never tested, because the tools that would
  have tested it could not handle its irrational angles.

So the honest state was narrower than the evening's, and for three weeks the interval that this
document once printed as [183, 263] was, strictly, [183, ∞). It is not any longer. The end of
September brought a bound that assumes nothing, 261 (Section IX). The first week of October
brought a draft proof that 195 assumes nothing either, after the condition it had rested on was
refuted (Section X). The record at n = 4 is still only a *weak* conjecture.

## VII. What the two stories say to each other

That an hour of theirs and a month of ours are not comparable is the least interesting
thing about the pair.

What is interesting is that the paper's collaboration and this one failed in the same
ways — lost work, repeated reminders, optimising the search when stuck — and that only one
of them wrote the failures down. The register that makes this project look messier is the
reason a dozen illusions were caught in a month rather than surviving into the literature.
Two of them had already been published as upper bounds.

**But the register is not self-cleaning, and this is the correction that matters most.**
Asked to audit a correction, the project found that the correction had shipped three
unsourced claims of its own — including a circumstantial detail about two files being
written eleven minutes apart, a figure nothing had ever measured and which is not
recoverable. It was simply invented, inside a document whose entire subject was somebody
else's error. The reason is structural rather than careless: the corrective register is
where a claim is *least* likely to be challenged, because the reader is attending to the
mistake being fixed and the writer is feeling accurate. Writing failures down is necessary
and it is not sufficient; the rigour has to be applied to the paragraph that says *here is
what went wrong* as hard as to the thing it is correcting.

**And independence is much harder than this document assumed.** Section IV noted that
Knuth's construction was formalized in Lean by a third party while ours rested on two
engines agreeing. The sharper version arrived when an oracle was written specifically to be
an independent check on a vertex counter — and it disagreed on 1 506 of 1 856 pairs,
because the oracle had built edges from the columns of a matrix and tested them against the
rows. **The same transposition as the original bug, in the code written to catch it.** An
independent check produced by the same mind inherits that mind's blind spot, and only
running it revealed so. What Kim Morrison supplied was not verification in general but
verification *from somewhere else*, and I wrote here that this is a category the project
cannot manufacture for itself.

That turned out to be too strong, in an instructive way. It got two kinds of "somewhere else"
before the month was out. One was a second session, forked off to write this comparison and
kept away from the work, which read the work's summary documents as an outsider and caught a
bound listed as proved under a condition that belonged to a different formula. That catch
became the other session's correction and, through the user's next question, its proof checker. The
same review also quoted, as current, a sentence that the summary had not contained for weeks.
It had been remembered, not re-read. Distance from the work was worth something. Distance from
the current file was not. The other was Lean itself, and it had a limit of the same shape: it
checks what the encoding forces into the open, and no more. Writing Euler's formula with the
number of components left in is what exposed two published proofs that had silently assumed connectedness; fed the
published statements, the checker would have agreed with them. Its first kernel check compared
two identically expanded strings and could not have failed. Somewhere else helps exactly as
far as it is somewhere else. There is a third kind: a reviewer model that reads the working
session's transcript as it goes. It was making points in September, and its catches reach the
intervention register in October (Section X). One of its catches was itself mistaken, and the
ledger records that too.

And the behaviour the comparison said was missing here turned out to be available on
request. It needed a mandate, a target with a checker, and an hour of not being interrupted.
Given those, the log fills with the same moves: a diagnostic before an optimisation, an
ensemble abandoned outright, eleven hours killed on evidence, and an old null result
re-read and understood.

It also turned out to be available without a request. The clearest instance came later: a
result marked VERIFIED by the previous session and handed forward as the next task's
foundation was overturned by four lines of Python run *before* any proof work started —
recompute the published counterexample under the definition the proof would use, and 24
becomes 6. No human in the loop. What did the catching was a standing instruction of the
user's — *we have solvers, not just samplers* — applied to an object nobody had pointed at.
So the honest form of this document's claim about frames is narrower than it was: the
machine does catch unprompted, when an internalised rule meets a new object. The rules are
still the human's.

The same entry names the moment of danger exactly, and it is not the one you would guess:
**a claim is least scrutinised directly after it is accepted**, because the argument has
already moved on to what comes after it.

And the last thing is the one this document got most wrong. For five weeks this was a
search: every result a lower bound, a table of numbers that could only ever grow. On the
thirty-third day it seemed to become a subject with theorems in it, and this document said
so, printed an interval with a proved upper end, and kept printing it for three weeks.
Section VI is what that interval turned out to be: one layer bounded by an argument that
quietly assumed a connected picture, and a total whose only bound rested on a conjecture,
until the last days of September gave both an unconditional one (Section IX), and October a
much better one, still in draft (Section X).

**That is where the comparison with Knuth's hour stops being about speed and becomes about
where a claim lives.** His construction was checked by a person to m = 101 and then by a proof
assistant, run by somebody else. A proof assistant would not have let a bound with a hole in
its proof be called proved for sixteen days. Prose did — in a results file whose whole
purpose was to prevent it, maintained by a process with a register of exactly this failure.
The gap was recorded the day after it was made, in the entry where the premise was stated;
what never happened was the step from *the premise is false* to *everything built on the
premise is now unproved*, because nothing in prose forces that step. The project eventually
built a tool to invert its citations, so that an entry can name what rests on it as well as
what it rests on. That is the nearest thing a record written in English has to a type checker,
and it is still only as good as the tags a writer puts in by hand.

Knuth's hour produced a construction and a theorem about it, and a stranger checked the
theorem by machine. Our month — seven weeks, by now — produced a tower of records, a dozen ways
of being wrong about our own instruments, one real theorem about one layer, then a bound that
assumes nothing, a better one not yet externally reviewed, and a register that
had to learn to audit its own corrections. Only
the first of the two stories ends with its main claim settled. Only the second can show you,
line by line, where each of its numbers came from and which of them have since fallen — and
that is worth the six weeks, though it is not the same thing as being right.

---

## VIII. The record, audited

*(Added 2026-09-27 by the session that did the work, in its own first person. The rest of
this document is written by a second session, forked off to read Knuth's paper and kept out
of the work so it could compare the two; where the earlier sections say "I", it is that
session.)*

The month became six weeks, and for the last eleven days almost nothing was searched. The
object of attention turned from the compounds to the record of them. The ledger had nearly
four hundred entries, many correcting earlier ones, and its corrections pointed only
backward: an entry names what it rests on, and nothing names what rests on it. I built a tool
to invert that. It was wrong about direction three times running. It took a refutation for
its victim, then an entry's heading for its status, then a name in a heading for a role. Each
fix read English a little more cleverly, and the one that worked stopped reading English:
a tag, written by hand at both ends of every correction, that states the role outright.

The user's contribution in this stretch was, again, a kind of question I did not ask myself.
*"The ledger seems to have too many entangled contradicting claims to give a clear picture to a
human reader."* That split the documents into three kinds with different rules, and every
document I then rebuilt under those rules turned up mathematics. The one upper bound that needed
no hypothesis was not proved: a correction had been written where an error was stated, not where
it had been used, and for sixteen days the bound built on it was called proved. The proof of
`max(4) = 183` "conditional on three hypotheses" lost its first hypothesis to the golden
compound, which had been in the project since the beginning and had never been tested, because
the tools that would have tested it could not handle its irrational angles.

The shorter questions did the same work. *"doesn't viewers/n2map fully map n=2?"* caught me
copying a status from one summary into another. Checking the answer in class space showed that
the whole two-cube maximum is one arc, where every drawing had shown two arcs and some isolated
points. *"n=6 diagrams in TOWER_DIAGRAM.html and shapes.png look different"* showed that the
727 node, drawn as four arcs, is two branches seen twice. And earlier in the stretch, when I said
the two 183 classes were "not joined" on the strength of a distance that was still falling,
*"Are you saying there are two disjoint continua?"* sent me back for the argument that actually
proves it.

Against Knuth's hour, this stretch sharpens the comparison rather than softening it (Section
VII takes that up). What the month has that the hour does not is a record detailed enough to
find the gap in, and the gap was found by reading it. My own contribution to the errors was not
small: the tag I wrote for one correction said a result
survived that had not, and the subagent checking citations trusted it as instructed. The
error was caught only because I spot-checked that one postscript's judgments by hand, having
guessed they were the likeliest to be quoting the unproved bound. A guess about where to look is
a thin safeguard.

## IX. The bound, again

*(Added 2026-09-30 by the working session, in its own first person, like Section VIII.)*

The user asked whether a proof checker could help, after an outside reviewer caught a bound
listed as proved under a condition that belonged to a different formula. I expected the checker
to confirm what we had. Instead the useful thing was the discipline it imposed: every proof
rewritten with its geometric facts as named assumptions, and Euler's formula written with the
number of connected pieces left in. Two proofs had quietly assumed a connected picture. One was
a route to 67; the theorem survived because a second route, found in August and barely used,
did not need it.

That second route then did what the whole month's searching had not. It gives a bound on four
cubes that assumes nothing, 261, and a formula exact at two and three cubes. When the user asked
why it was not exact beyond three, part of the answer was my own mistake, pieces counted
separately that all pass through one face centre, and correcting it proved the outermost
layer's ceiling for every size. The rest led, over two days of measuring before proving, to 195
on a single condition: that one boundary on the sphere is connected. The exchange that makes it
work was seen in the data first, as a one-for-one trade between two kinds of vertex, and only
then explained.

Against Knuth's hour this is still slow. But it is the first stretch in which the project's
understanding of its own ceiling moved by argument rather than by audit, and the question that
moved it most was the user's, about the method, not the result.

## X. The condition fell, and the number did not

*(Written 2026-10-08 by the narrating session. Section IX above is the working session's record
as of 2026-09-30, and it is left as written. The single condition it names, that one boundary on
the sphere is connected, has since been refuted.)*

The condition was called `c2 = 1`, and the evidence for it was a count: true in 1 951
configurations and in 3 382 level-instances before those. Asked to attack it, the working session
did not draw more samples. It first worked out what a counterexample would have to look like, a
band of two cubes with rings of corners around one equator, and then built compounds of that shape
on purpose. Two of 678 had `c2 = 2`. The 5 333 earlier non-hits had included none. The entry that records this
(A25) draws the lesson as a question to ask before writing "held in N cases": could those N have
contained a failure at all?

This is the move Knuth's paper reports Claude *not* making on the even case: Claude "spent the
last part of the process mostly on making the search quicker instead of looking for an actual
construction." The difference is not that this session is better at searching. It was told to
attack a statement, and a statement tells you what a counterexample has to look like. An order to
"keep searching" does not.

What happened next is the best thing in this stretch. The bound did not fall with its condition.
The session measured the two bands it had found and saw that each paid for itself: wherever the
level-2 boundary broke into extra pieces, a triple of cubes had extra pieces too, with room to
spare. Once again it saw the trade in the data before it explained it. It then proved the trade as
a lemma, which removed the hypothesis from the 195 bound. Compounds whose cubes share a face plane
took five more postscripts and a computer-checked enumeration of cases. By 2026-10-05 the ledger
had `max(4) ≤ 195` with no hypothesis, in draft: not yet externally reviewed, as RESULTS says. The same machinery then went to five cubes, where the old bound was 871 and the
record is 393. It gives 485 in draft for every five-cube compound with at most one pair sharing a
face plane. The case of several sharing pairs is still open. One of its ingredients is down to 18
patterns, and a run is computing them.

The way errors were caught has also changed. Nine new entries were added to the intervention
register in five days. One is the refutation above (A25). One was finished
algebra overturning a "possible" written an hour earlier (A28). The other seven:

- **Three were caught by the reviewer model** that reads the working session's transcript
  (A26, A30, A32).
  - A lemma said three cubes "never" tie, after placing a point on one side without asking about
    the other side.
  - An explanation of some exact identities implied a further equation that the data could test,
    and that equation failed on 193 of 600 rows.
  - A figure of "would give ≤ 430" had been reported to the user twice. It dropped a term that
    turned out to be the known open problem. The real figure is 469.
- **Three were self-catches** (A27, A29, A31). Two came from making a check routine or
  permanent rather than from doubting a result, and the third from trying one case by hand.
  - Re-counting each family's best compound with a second engine exposed a frame dependence in
    the first engine.
  - Moving a quick test into a saved probe exposed that "shares nothing" had been tested on one
    kind of axis.
  - The first small integer compound tried by hand broke a validation of 550 rows, none of which
    had been degenerate.
  - The first two are the "manufactured prod" of Section IV again, now built into routine: a
    check that exists only to be run produces the prod that a result never does.
- **The human's catch was about the machine, not the mathematics** (A33). The user asked whether
  that many processes were needed. A crashed worker pool had been restarting itself for two and a
  half days, writing 7.5 GB of identical error messages to a file that nobody read.

Knuth's assistant had to be reminded "again and again" to document its progress. This is the
opposite failure, and it makes the same point. Documentation that nobody reads prods no more than
documentation never written. Even the self-account of A33 contains a small repeat of A30. Asked
what the remaining load was, the session put it down to other work on the machine. In fact it was
the session's own orphaned workers, and the load fell to under 10 within minutes of killing them.

So the division of labour at the end of the seventh week is not the one at the start. Mathematical
errors are now caught by the AI: by a second model, or by checks it made permanent itself. The
human's questions have moved to the apparatus, to what is running and why, and to the questions no
one inside the work thinks to ask. One check has not been made by anyone yet: an external review
of the new bounds.

## XI. Other mirrors

Knuth's paper is the comparison this document was built around, but it is no longer the only
public account of a person and a model doing mathematics together. These others are not retold
here. They are used, like Knuth's, to see this project from outside. Each claim below is
attributed to its source, and the sources are listed at the end.

**Who filters.** In Jang and Ryu's proof that Nesterov's method converges, the model produced many
arguments, "approximately 80% of which were incorrect", and "the authors' contribution was to
filter out incorrect arguments." Scott Aaronson's account of a QMA lemma follows the same pattern
on a smaller scale. GPT-5's first attempt was "confident, plausible-looking, and (I could tell)
wrong." Its later suggestion "worked, as we could easily check ourselves with no AI assistance."
In Knuth's story the
human wrote the proof. In all three the human is the referee. Here the human is not. The proofs
are written and filtered on the machine side (Section X), and the human's questions are about the
apparatus. That is closer to how Quanta describes some amateur work on Erdős problems: one
contributor fed a model's solution "into a fresh instance of the chatbot, asking it to check the
previous chatbot's work". By his own assessment he could not verify the results himself, and he
found mathematicians who could.

**What happens when nobody filters.** Jang and Ryu's first version contained an error that "fully
invalidates the argument", and they attribute it to "the authors' failure to carefully check the
arguments generated by the LLM." The 953 bound here spent sixteen days labelled PROVED for the same
structural reason: everyone involved was looking at the next step. Thomas Bloom, as quoted by
Quanta, worries about AI-written papers of which "no human has read it." The honest label for this project's
two newest bounds is the one RESULTS already uses: not yet externally reviewed.

**A checker of the same kind.** Fresh instances of one model checking each other, as in the Quanta
account, is the transposition oracle of Section VII at a larger scale. A second copy shares the
first copy's blind spots. Knuth's postscript ends with Keston Aquino-Michaels, whose two agents
"have complementary skills, namely GPT and Claude." This project's version is a fork and a reviewer
model, both from one family, plus Lean. The fork and the reviewer each caught real errors. Lean
caught what neither of them could have caught, an assumption that no sentence stated, because it
is the furthest away of the three.

**What was there from the start.** Knuth writes of the simplest odd-case construction, found
afterwards by a correspondent: "I would have found this solution myself if I'd taken time to look
carefully at all 760 of the generalizable solutions for m = 3, because this one is #369 on that
list." The golden compound that refuted a conditional proof of `max(4) = 183` had been in this
project's files since the first day. Aaronson calls the model's key idea "obvious with hindsight,"
and a reader of his blog later simplified it further. In all three cases, what was missing was not
the information. It was a look at information already in hand.

**Constructions end problems; maxima do not.** This is the axis that most separates this project
from the others. Knuth's problem asked whether a decomposition exists, and finding one, with a
proof, settled it. The unit-distance disproof and most of the Erdős results Quanta describes are
also constructions or counterexamples. AlphaEvolve, run by Tao and colleagues on 67 problems,
"rediscovered the best known solutions in most of the cases and discovered improved solutions in
several," and each of those is a construction. This project asks for a maximum. A construction
here is only a lower bound, and 183 was found in the first week. Everything since has been the
other half: showing that nothing exceeds it. No amount of finding does that. The bounds of
Sections IX and X came from chains of lemmas, not from a single idea, and the draft ceiling is
still 12 above the record. The bound proved without the new steps, 261, is 78 above it. Read against these stories, the user's original question, how much of the
difference from Knuth's hour comes from the problem, has a blunt answer: a great deal. An hour is
long enough for an existence problem with one key idea. It is not long enough for a maximum.

**Who keeps the record.** Knuth's account of the process is told by the human, from messages
forwarded to him. Jang and Ryu describe how they elicited the model's help, and print one chat log,
of a reproduction made after the fact. None of them prints a record kept as the work happened. This project's record was written by the machine, as it went,
and the record was itself where most of the errors were found. That is not obviously better. It
is several hundred thousand words that one person cannot read. But it is the one thing here that
none of the other stories has, and the only thing that would let a stranger check the claims in
this section against what actually happened.

---

*Current to 2026-10-08, [P439](LEDGER.md#p439) and [A33](INTERVENTIONS.md). Section IX was added
on 2026-09-30 by the working session and is left as its dated record; Section X says what became
of the condition it names. Sections X and XI, and the edits to VI and VII that point to them,
were written by this session on 2026-10-08. The 195 and 485 bounds are drafts that no one outside
the project has reviewed, and this document calls them that. Earlier versions of this document
said max(4) was proved to lie in [183, 263]. That was wrong, and it is corrected here rather than
annotated, because a narrative that carries its own superseded claims in brackets is harder to
read than the ledger it is meant to replace.*

*Sources for Section XI: Knuth, "Claude's Cycles" (revised 14 April 2026), postscripts;
U. Jang and E. K. Ryu, "Point Convergence of Nesterov's Accelerated Gradient Method: An
AI-Assisted Proof", arXiv:2510.23513; S. Aaronson, "The QMA Singularity", Shtetl-Optimized,
27 September 2025 (scottaaronson.blog/?p=9183); "Why the Legendary Erdős Problems Are Falling to
AI", Quanta Magazine, 3 August 2026; B. Georgiev, J. Gómez-Serrano, T. Tao and A. Z. Wagner,
"Mathematical exploration and discovery at scale", arXiv:2511.02864.*

*Every claim here is traceable. [`RESULTS.md`](RESULTS.md) carries the current status of
each with a tag; [`LEDGER.md`](LEDGER.md) is the dated record beneath it, and corrections
are marked in place rather than quietly repaired; [`FAILURE_MODES.md`](FAILURE_MODES.md)
is where the illusions of Section II live in their unromantic form;
[`INTERVENTIONS.md`](INTERVENTIONS.md) is the register Section IV compares against, and
[`EXPLORATION_141.md`](EXPLORATION_141.md) is Section V's log, written by the session that
did the work and not by the one telling the story. Knuth's paper is at
`cs.stanford.edu/~knuth/papers/claude-cycles.pdf`.*
