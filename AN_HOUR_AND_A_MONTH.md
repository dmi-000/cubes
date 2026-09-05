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
that you have not yet failed.

The tower was built by a kind of ascent. Take a record, find the directions in which the
count does not change, walk along them until it does, step across, and repeat. It works.
It produced 3925 from 3921 in a single crossing. But it has a property that took a month
to notice and is stated here because it explains the rest of the story: **the walk moves
along the stratum it starts on and cannot leave it.** Codimension is preserved. The
record climb can polish a record and cannot reach a differently-shaped one.

## II. Four illusions

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

Four illusions, one disease: mistaking a property of the notation for a property of the
thing. The project's own principles file had the rule written down — *a refusal may be
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

And at n=4 the whole gap has a name. The record's profile is {depth-1: 92, depth-2: 66,
depth-3: 24}, and 66 and 24 are exactly the ceiling-law caps. Every local maximum the
search reaches has {50, 66, 24}. The deep layers are already at their ceilings in both.
**Every one of the forty-two missing regions is depth-1.**

## IV. The mirror

In February, Filip Stappers put Claude Opus 4.6 on an open problem of Knuth's:
decompose the digraph on *m*³ vertices into three directed Hamiltonian cycles. Thirty-one
numbered explorations later — *"about one hour after the session began"* — it had a
construction, in nine lines of C, valid for every odd *m*. Stappers checked it to m = 101.
Knuth proved it, classified the whole family (exactly 760 such decompositions work for all
odd *m*), and wrote the paper. Kim Morrison formalized the proof in Lean. Knuth's own
verdict: *"Hats off to Claude!"*

It is tempting to read that against a month of ours and conclude something about capability.
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

The sting is in the collinearity. Days earlier this project had proposed re-weighting the
depth layers, built five weighted objectives, run them, found every one byte-identical to
plain total, and reported the idea dead. It was not dead. At r = 0.984 those objectives
were *collinear* — the same variable wearing five hats — and the experiment had been run
in the one ensemble where it was mathematically obliged to return nothing. In the
structured families depth-1 and depth-2 genuinely trade against each other, and the idea
works. A good idea was buried by testing it where it could not speak.

## VI. What the two stories say to each other

That an hour of theirs and a month of ours are not comparable is the least interesting
thing about the pair.

What is interesting is that the paper's collaboration and this one failed in the same
ways — lost work, repeated reminders, optimising the search when stuck — and that only one
of them wrote the failures down. The register that makes this project look messier is the
reason its results can be trusted, and the reason four illusions were caught in a single
week rather than surviving into the literature.

And what is more interesting still is that the behaviour the comparison said was missing
here turned out to be available on request. It needed a mandate, a target with a checker,
and an hour of not being interrupted. Given those, the log fills with the same moves: a
diagnostic before an optimisation, an ensemble abandoned outright, eleven hours killed on
evidence, and an old null result re-read and understood.

The remaining gap to 183 is now sharp enough to state in one line: **depth-1 = 92 with
depth-2 held at 66.** Best so far, 74 and 66. Eighteen to go.

---

*Every claim here is traceable. [`RESULTS.md`](RESULTS.md) carries the current status of
each with a tag; [`LEDGER.md`](LEDGER.md) is the dated record beneath it, and corrections
are marked in place rather than quietly repaired; [`FAILURE_MODES.md`](FAILURE_MODES.md)
is where the four illusions of Section II live in their unromantic form;
[`INTERVENTIONS.md`](INTERVENTIONS.md) is the register Section IV compares against, and
[`EXPLORATION_141.md`](EXPLORATION_141.md) is Section V's log, written by the session that
did the work and not by the one telling the story. Knuth's paper is at
`cs.stanford.edu/~knuth/papers/claude-cycles.pdf`.*
