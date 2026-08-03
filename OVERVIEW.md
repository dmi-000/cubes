# Cubes through one point: the short version

*A ten-minute tour of the project: what the question is, what is known, and how
a human and a shifting cast of AI models actually produced it. Everything here
is stated plainly and without proof; each section says where to read the real
thing. [`JOURNEY.md`](JOURNEY.md) is the same story told at length and in
order, with the wrong turns left in. [`RESULTS.md`](RESULTS.md) is the current
state of belief, every claim tagged. Last updated 2026-08-02.*

*One disclosure up front, because it changes how to read everything else: the
code, the searches, the analysis, and this document were written by an AI
(Claude) working under human direction. What the human contributed was not
supervision but the noticing — see [How this was made](#how-this-was-made).*

---

## The question

Take some identical cubes. Push them all onto the same centre point, then spin
each one to its own angle — a die photographed mid-tumble, every frame kept.
Their faces slice space into pieces.

**How many pieces can *n* cubes make?**

One cube makes one piece. Two cubes make thirteen. Six cubes, arranged well,
make seven hundred and twenty-seven, and nobody knows whether that is the
best.

The question is easy to ask and easy to picture, which is most of its appeal.
It is also, as it turns out, hard in an interesting way rather than a tedious
one: the answers for small *n* are exact and slightly weird, the answers for
larger *n* seem to obey a law nobody has proved, and the structure that
appears in between is richer than the numbers suggest.

## The trap that set the house rules

The first serious version of this project counted the wrong thing, and got
beautiful wrong answers for weeks.

Here is the distinction. Each cube face lies in a plane. If you extend all
those planes to infinity and count the cells they cut space into, you get one
number. If you count *regions* — pieces you can walk around inside without the
set of cubes containing you ever changing — you get a smaller number.

Both halves of that matter. Two pieces can be contained by exactly the same
cubes and still be different regions, if you cannot get from one to the other
without leaving. With two cubes there are only three possible containment sets,
{A}, {B} and {A,B}, but thirteen regions: the shared core, plus six lobes of
each cube poking out of the other. The difference is
that a plane's infinite extension, out where its own cube isn't, doesn't
actually separate anything. Walk across it and nothing about your situation
changes.

Counting plane cells instead of containment regions inflated every total and
produced a string of records that weren't. Since then the rule has been: a
region is a connected component of constant cube-containment, you cross a
*real* face or nothing happened, and no floating-point number is ever allowed
to decide whether two things touch. Every count in the project is done in
exact rational or algebraic arithmetic, by two independently written engines
that must agree before anything is believed.

That sounds like fussiness. It is the reason the results are trustworthy, and
it caught at least four later errors that a tolerance would have hidden. It is
also the project's first house rule, and it came out of the failure rather than
out of foresight: an early voxel pipeline reported a "stable plateau" of about
1,340 regions for a configuration whose exact count is 567. Approximate methods
may suggest; only exact counts decide.

## Two sizes that are actually solved

**Two cubes: thirteen.** Proved. One core where they overlap, six lobes of
each cube sticking out — and the proof is a counting argument about convex
pieces, not a search.

The surprise is the maximisers. You would expect one best angle. There is a
whole continuum: *every* rotation about a shared body diagonal gives thirteen,
plus a closed arc about an edge axis. The optimum is a plateau, not a peak.
The project believed the opposite for weeks, because it tested rigidity by
perturbing randomly and asking whether the count survived — which reports
every measure-zero configuration as isolated and every plateau as a point.

**Three cubes: sixty-seven.** Also proved, and stranger. There are exactly two
best arrangements, and they are not congruent to each other: one comes from
the octahedron, one from the icosahedron. Their coordinates involve √2 and √5
respectively.

That second fact is the good one. **At three cubes the maximum cannot be
achieved with rational angles at all.** Irrationality is not decoration; it is
forced. And three is the only size where that is true so far — every later
record is rational, and every irrational near-record found since is *shadowed*
by a rational configuration with the same count.

Read [`PROOF_67.md`](PROOF_67.md) for the proof, or
[`PROOF_NARRATIVE.md`](PROOF_NARRATIVE.md) for the version with the false
lemma left in.

## Why it gets hard at four

Sort the regions by *depth* — how many cubes contain them. Depth 1 regions are
inside exactly one cube, depth *n* is the core where all of them overlap.

Each depth layer has its own ceiling, and for small *n* you can hit every
ceiling at once. From four cubes on, you can't. Maxing the shallow layers
costs you the deep ones. The layers have to be **traded**, and there is no
longer an arrangement that is simultaneously best at everything.

This is the project's name for the phenomenon — *frustration*, borrowed from
physics, where a system can't satisfy all its local constraints at once — and
it is the reason the problem changes character at *n* = 4. Below it, symmetry
finds the answer. Above it, you have to search.

It also explains the irrationality at three cubes: hitting every ceiling
simultaneously is a rigid demand, and rigid demands land on isolated,
irrational points. Trades, by contrast, live on open sets, and open sets
always contain rational points. That is why the record tower from four cubes
up is entirely rational.

## The tower

| cubes | best known | status |
|---|---|---|
| 2 | 13 | **proved maximum** |
| 3 | 67 | **proved maximum** |
| 4 | 183 | best found |
| 5 | 393 | best found |
| 6 | **727** | best found |
| 7 | 1217 | best found |
| 8 | 1891 | best found |

The records **nest**: the 393 is five of the six cubes of the 727, the 727 is
six of the seven of the 1217, and so on down. Adding a good cube to a good
arrangement beats searching the larger space from scratch — reliably enough
that it became the standard method.

The one break in the chain is three cubes, and it breaks for the reason above.
The best triple sitting inside any larger record is 63, four short of 67,
because every subset of a rational arrangement is rational and 67 needs
irrational angles.

There is also a formula. Each depth layer's ceiling appears to follow
C(l, n) = (12l − 6)n − 2(l² − 1), the shallowest case of which is proved and
the rest of which has never been exceeded in about a million configurations.
Add the ceilings up and subtract a "frustration deficit" of 6(n−3)(n−2) and
you get the observed maxima at *n* = 3, 4, 5 exactly, and a prediction of 729
at six cubes — two more than the best known. Whether those two are reachable
is the project's central open question.

## How a search actually works

Fix five cubes; the sixth has three degrees of freedom. Almost everywhere in
that three-dimensional space the region count is locally constant. It changes
only on **walls** — surfaces where some coincidence happens, a corner touching
a face, two edges crossing.

So the count is a piecewise-constant landscape of chambers, and the records
sit where several walls meet. Search the walls, not the space.

The full catalogue of wall types was only settled recently, and it is tidier
than expected. **Every wall is four face planes becoming concurrent at a
point.** They classify by how those four planes are distributed among cubes:

| planes per cube | what it looks like | enumerated? |
|---|---|---|
| 3 + 1 | a cube corner touching another cube's face | yes |
| 2 + 2 | an edge of one cube crossing an edge of another | yes |
| 2 + 1 + 1 | an edge crossing the line where two other cubes' faces meet | **no** |
| 1 + 1 + 1 + 1 | four planes from four different cubes | **no** |

The first two were the project's whole vocabulary for months. The last two had
never been enumerated — and one of them turns out to control the fine
structure of the record, which is the most recent finding in the project. Two
conditions that *sound* like they belong on the list, a corner meeting a
corner and an edge lying inside a face, are one dimension too special to be
walls at all.

## The record, close up

Seven hundred and twenty-seven is not a point. It is a **plateau**: at least
161 genuinely different arrangements reach it, falling into 54 distinct
combinatorial types. In configuration space they form a union of
one-dimensional segments — move along a segment and the count holds; step off
it in any other direction and the count drops to 715–721.

Within the plateau, the segments are cut into **chambers**. Crossing from one
chamber to the next, exactly two regions swap between labels at the same
depth — the smallest move the arrangement permits, and the quantum of 2 is
forced by the fact that every configuration is symmetric through its centre,
so regions come in antipodal pairs. Chamber boundaries were recently shown to
be exactly the wall crossings, and the walls doing that work are mostly the
never-enumerated kind.

Two things about this picture are worth saying plainly because both contradict
what the project believed earlier.

**The record is not where the most coincidences are.** The working heuristic
for a long time was that records concentrate at high-multiplicity
concurrences — many faces through one point. An early experiment had already
noticed a sweet spot (forcing four cubes through one corner collapses a
six-cube count into the 300s), but the heuristic kept driving the searches
anyway. Measured over 1200 unselected arrangements, the correlation runs the
other way: the ones counting 700 or
more average 1.6 hits on the base's coincidence walls, and the ones counting
below 650 average 92.6. Coincidence *merges* regions. The maximum lives at low
but nonzero coincidence. The old heuristic was an accurate description of 723,
which is the runner-up, and of nothing else.

**The record that was found first is atypical of its own plateau.** Of the 161
arrangements reaching 727, 159 share one structural signature; the originally
discovered one is a singleton, and another singleton reaches 727 while
carrying the very feature the project's theory said optima avoid. It was found
first because the search happened to land there, not because it is
representative — a good reminder that describing a set from its first member
is a mistake, and one this project made at least four times.

For the full classification, with generators that regenerate every family,
see [`TYPOLOGY.md`](TYPOLOGY.md).

## One theorem worth stating

If you have an arrangement and you delete one cube, the count drops by some
amount. How much?

Exactly this: build the graph whose nodes are the regions (plus the outside),
joining two regions when they share a wall belonging to the deleted cube.
Deleting the cube merges precisely the connected pieces of that graph, so the
drop equals the number of nodes minus the number of pieces. And that quantity
is bounded, in turn, by an Euler characteristic count on the deleted cube's
own surface: the other cubes' planes trace a pattern of closed curves on it,
and the number of faces in that pattern bounds the increment.

Measured against real arrangements, the bound overshoots by at most 11%, and
is exactly tight in several cases. It replaces a constant that had been
*measured* over a corpus with one that is *derived* from the geometry — which
is the difference between a search heuristic and a proof.

The first attempt at this failed and was written up as a failure, complete
with a counterexample. The counterexample was itself wrong: it came from a
configuration where the two cubes touch *tangentially*, and the code tested
for strict crossings, so it scored twelve real contacts as zero. Finding that
turned a documented dead end into the theorem above.

## What the project got wrong

The record of mistakes is kept deliberately, in one table at the end of
[`RESULTS.md`](RESULTS.md) and in dated detail in the ledger. The pattern is
worth more than any individual entry:

- **Counting plane cells instead of containment regions** — inflated
  everything, produced false records for weeks.
- **Measuring rigidity by perturbing randomly** — reports every plateau as a
  point, which is how a continuum of two-cube maximisers went unnoticed.
- **Describing a whole family from its first member** — done four separate
  times, each time producing a plausible generalisation that later collapsed.
- **Believing a documented failure without re-checking it** — the increment
  bound sat "refuted" for a while on the strength of a counterexample that
  didn't hold.
- **Confusing a search's reach with a fact about the problem** — several
  claimed structural laws turned out to be descriptions of whatever the
  enumerator could see.

Every one of these produced *plausible numbers*, not obvious failures.
[`FAILURE_MODES.md`](FAILURE_MODES.md) catalogues them by symptom — what you
notice first — so a later reader can triage rather than rediscover. That is
the argument for the exactness rule and for two independent engines: a wrong
answer that looks wrong costs an afternoon, and a wrong answer that looks right
costs a month.

Most were caught by the machinery. Several were caught by a human sentence.
"Are you sure the lack of irrational solutions isn't an artifact of some
unnecessary restriction?" reopened a closed question and turned out to be
right. "This machine has only 16GB" prompted a measurement that demolished a
confident diagnosis the AI had just given twice. And when a script was added to
regenerate stale numbers automatically, the response — *"generated positions is
good, but it doesn't update invalidated statements; discipline does that"* —
named the actual problem, which was that ten claims had gone false in summary
positions where nothing regenerates them.

## How this was made

The division of labour was not decorative; each layer did something the others
couldn't.

**The human noticed things.** Almost every pivot in the project came from a
short human remark rather than a computation: the edge-versus-corner
observation that separated the two three-cube maximisers, "are subsets of
records also records?", the frustration reframing, and — most dramatically —
looking at the 3-D viewer and saying that a scatter of near-miss edges seemed
to lie in a plane perpendicular to (1,1,1). That last sentence became a
closed-form family, four theorems, and a structural result about how records
are built. The pattern is worth naming: **the human watched the data for
meaning while the machines watched it for values.**

**A frontier model ran the main session** — designing the exact algorithms,
writing the specifications and their gates, spotting regularities (the ceiling
formula was found by staring at a table of maxima), and catching errors,
including its own. Three of the corrections in the ledger are the main session
refuting a claim it had made itself a few days earlier.

**Mid-tier models did the heavy building**: the C++ engines, the search
campaigns, the algebraic arithmetic, the incidence analysers. Two failure modes
showed up repeatedly, and both are manageable once named. *Coverage artifacts*
— a search implemented perfectly over an accidentally-too-small parameter space
— are fixed by a hard gate: your machinery must reproduce the current record
before your negative results count for anything. *Premature parking* — an agent
sets up a long computation and then stops to wait for it instead of running it
— is fixed by making every campaign a single detached self-sequencing script.
That second failure happened again on the day this document was written: an
agent built its engine correctly, then stalled twice waiting on its own monitor
job, and the main session finished the gating by hand.

**A small model audited**, and on one occasion overturned the frontier model's
stated belief about what the data showed. Cheap models audit well, partly
because they have no stake in the hypothesis. Specifications were written to
invite that: the instruction *"if the true invariant is not what I guessed,
report what it is; do not force it to match"* is in the delegation log, and the
two times an agent contradicted the main session, the agent was right.

**Non-LLM tools carried the actual mathematics**: twin C++/Python counting
engines that have never once disagreed across about a million counts, a
computer-algebra system for the Gröbner-basis work that found configurations no
numeric grid lands on, and a small browser visualiser — which is what the human
was looking at when the remark that opened Act VII got made.

**The filesystem was the long-term memory.** Sessions end, context windows
fill, models get swapped mid-project. What survives is the append-only ledger,
the specification files, and a log recording exactly what each delegated agent
was told and which pre-existing numbers it had to reproduce
([`DELEGATION_LOG.md`](DELEGATION_LOG.md)) — that last one exists because a
specification handed to a subagent is otherwise stored nowhere and vanishes
with the session, taking the gates with it.

## What is open

- **Is 729 reachable at six cubes?** The formula predicts it; exhaustive
  searches of three separate strata cap out at 727, 725 and 723.
- **Are 183, 393, 727, 1217, 1891 actually maximal?** None is proved. Only
  *n* = 2 and *n* = 3 have theorems.
- **The ceiling law and the frustration deficit** — both fit everything and
  neither is proved beyond the shallowest layer.
- **The two unenumerated wall types** — now catalogued, not yet swept.
- **A universal ceiling on the one-cube increment** — the per-arrangement
  bound is proved and tight; the universal version is still crude.

## Where to read next

| document | what it is |
|---|---|
| [`RESULTS.md`](RESULTS.md) | current beliefs, each tagged by strength of evidence; superseded claims in one table |
| [`JOURNEY.md`](JOURNEY.md) | the long narrative, in order, with the wrong turns left in |
| [`PROJECT.md`](PROJECT.md) | the formal write-up: methods, laws, record chain |
| [`six_cube_search_results.md`](six_cube_search_results.md) | the dated ledger — the primary record, append-only, indexed |
| [`TYPOLOGY.md`](TYPOLOGY.md) | the classification of the 727 plateau, with generators |
| [`PROOF_67.md`](PROOF_67.md) | the three-cube maximum, proved |
| [`README.md`](README.md) | map of the code |
| [`DELEGATION_LOG.md`](DELEGATION_LOG.md) | what was handed to which model, and what it had to prove |
| [`FAILURE_MODES.md`](FAILURE_MODES.md) | every error the project made, organised by symptom, with the check that catches it |
| [`GLOSSARY.md`](GLOSSARY.md) | the vocabulary, including terms that changed meaning and terms that are overloaded |

Reproducing any count takes one command and no special hardware; see the "how
to reproduce" section at the end of [`JOURNEY.md`](JOURNEY.md).
