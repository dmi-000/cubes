# The viewers and figures

Standalone pages and static figures in this directory. Every page opens in a
browser with no server and no network — everything is inlined, because the
Artifact CSP that these were built under blocks external hosts. Every figure is
self-contained too: literal colours in the SVG, no external stylesheet, no
webfont.

## Inventory

| file | kind | subject | documented in |
|---|---|---|---|
| `n2map_source.html` | page fragment | the complete n = 2 map | §1 |
| `n2map_standalone.html` | page | the same, wrapped to render offline | §1 |
| `arcmap.svg` / `.png` / `@2x.png` | figure | the 727 arc network as a transit map | §2 |
| `arcmap.html` | page fragment | the map plus its prose | §2 |
| `arcmap_standalone.html` | page | the same, offline | §2 |
| `shapes.svg` / `.png` / `@2x.png` | figure | the maximiser set at every n, side by side | §3 |
| `depth_explorer.html` | page, interactive 3-D | one compound's region walls, by depth | §4 |
| `seed119_viewer.html` | page, interactive 3-D | the exact-search seed explorer | §5 |

`shapes` was **redrawn on 2026-08-06** and now matches `MAXIMISER_TAXONOMY.md`;
§3 records what changed. `n2map` is still as published and is the one file here
that is stale — §1 lists the four results that have overtaken it.

**Static or interactive is the first thing to know about each.** `arcmap` and
`shapes` are figures: they carry their argument at a glance and take no input.
`n2map`, `depth_explorer` and `seed119_viewer` are instruments: they render
almost nothing useful until dragged, so a screenshot of one is not a summary of
it.

---

## 1. `n2map_standalone.html` — "The shape of two cubes"

**What it is.** An interactive presentation of the complete n = 2 map: the claim
that the two-cube region count is decided entirely by where the rotation axis
sits in the cube's own mirror arrangement. It is the visual form of Postscripts
69–70.

**Opening it.** Double-click, or `open n2map_standalone.html`. The one
interactive element is a canvas (`id="c"`) showing the axis sphere — **drag to
rotate it**. Nine great circles are drawn (three coordinate planes, six
diagonal), with the 6 face axes marked as squares, 12 edge axes as diamonds, and
8 body diagonals as triangles.

**What it argues.** A rotation is an axis plus an angle, so configuration space
fibres over the sphere of axes with the angle as fibre. The octahedral group's
nine mirror planes cut that sphere into 48 triangles, and the count depends only
on which stratum the axis lands in:

| stratum | dimension | count |
|---|---|---|
| triangle interior | 3 | 4 — generic, 98.8% of rotations |
| triangle edge (axis in a mirror plane) | 2 | 5 or 9 |
| face or edge vertex (4-fold, 2-fold axis) | 1 | 9 |
| body diagonal (3-fold axis) | 1 | 13 |
| the 24 symmetries | 0 | 1 — cubes coincide |

**The data it embeds.** Exact integer-arithmetic counts, each row a sweep of 33
angles about a fixed axis — (2,3,5) and (1,2,3) in triangle interiors, (1,2,0)
and (1,1,2) in mirror planes, (1,0,0), (1,1,0) and (1,1,1) on symmetry axes —
plus height-sampled frequencies (at height 10: 4 is 26.2%; at height 1000:
98.8%) showing the special strata thinning as measure-zero sets must.

**It carries its own methodological warning**, which is worth reading even apart
from the mathematics: small integer quaternions are the arithmetically special
ones, so they land on walls far more often than chance. That bias is a good
instrument for finding rational walls and a trap for judging what is generic —
an earlier reading of this same data, taken at small heights, is what produced
the retracted claim that 13 holds on an open set.

### What has changed since it was published

The page presents the n = 2 map as of Postscript [70](LEDGER.md#p70) and has **not** been
regenerated since. Three later results refine it:

* **Postscript [76](LEDGER.md#p76)** — the 13-locus is BIGGER than the page's summary card
  suggests. "Body diagonal → 13" is the headline, but 13 also occurs on mirror
  planes and edge arcs; the page's own data table already shows this ((1,2,0)
  reaches 13 once, (1,1,0) six times), so the table is right and the summary
  card is incomplete.
* **Postscript [83](LEDGER.md#p83)** — the 13-locus about a body diagonal is a punctured
  **circle**, not an arc: it wraps through the half-turn at t → ∞ and is
  punctured at the identity and the two 120° symmetries, where the count
  collapses to 1.
* **Postscript [86](LEDGER.md#p86)** — the n = 2 maximiser's symmetry group is **D₆**, not merely
  "order 12", which is why that circle's three punctures form one C₃ orbit and
  collapse to a single arc in class space.
* **2026-08-05** — the edge arc, which the page's data table hints at and its
  summary card omits, is now exact: 13 on the CLOSED interval t ∈ [1/2, 1] of
  `1,0,0,0;d,n,n,0`, that is rotation angle θ ∈ [arccos(1/3), arccos(−1/3)], with
  9 immediately outside both ends. It does not wrap. And both n = 2 arcs carry
  the SAME per-label profile (1, 6, 6, 1), so the type invariant does not
  separate them — a point the page's stratum table could make directly.

Anyone regenerating this page should fix the summary card first: the row
"body diagonal (3-fold axis) → 13" is the one that reads as exhaustive and is
not.

### Provenance

* Published as an Artifact at
  `https://claude.ai/code/artifact/20ce90bc-4aa1-4011-9ba9-c7c5a0cc2022`.
* `n2map_source.html` is the exact fragment that was published — no doctype or
  body tags, since the Artifact runtime supplies those. Edit and re-publish THIS
  file; the standalone is generated from it.
* `n2map_standalone.html` is that fragment wrapped in doctype/head/body with a
  minimal reset, so it renders offline. Regenerate it by re-wrapping the source.
* The source survived only in a session scratchpad under `/private/tmp`, which
  is volatile; it was copied into the project on 2026-08-04. **Artifact sources
  live nowhere durable unless copied.**

---

## 2. `arcmap.png` — the 727 arc network as a transit map

**What it is.** A static diagram of every known six-cube configuration reaching
727, drawn in the transit-map idiom: **distances distorted, topology preserved,
relative positions locally approximate**. Informative on its own, before any
interaction — it is meant to carry the 727 categorisation in one picture.

**Files.** `arcmap.svg` is the self-contained source (all colours literal, no
external CSS), `arcmap.png` is 1800px wide and `arcmap@2x.png` is 3600px.
`arcmap_standalone.html` is the same map with the full prose around it, and
`arcmap.html` is the publishable fragment.

**How to read it.** Each coloured line is one congruence class of 727 arc.
Stations are the ℚ(√d) classes lying on that arc, labelled by d and drawn in
their true ORDER along it. Ringed termini carry the arc's exact bound, and every
terminus is annotated with the count beyond it — always 723, except arc A's
lower end at 721. The ringed interchange on line D is the n = 6 record, where
two arcs genuinely cross. A dashed grey curve is the single W4 wall crossed by
all three of A, B and C.

**What is to scale and what is not.** Line lengths ARE to scale, at 60 px per
degree of rotation — the arcs' true extents are 3.99°, 7.04°, 8.43°, 5.91° and
7.31°, a spread of only 2.1×. (An earlier version printed Cayley-chart lengths
spanning 520× and claimed a faithful map was impossible; that was a chart
artifact, see Postscript [97](LEDGER.md#p97).) Station spacing within a line is even rather than
proportional to parameter, and that is the remaining distortion. The D1/D2 crossing angle is really 4.51° and is drawn wide
to make the interchange legible. Each arc has 72 chart copies under the free
cube's rotations and the base's C₃; one representative is shown.

**The vertical axis carries nothing.** Row order and spacing are legibility
choices: the gaps encode neither distance between arcs, nor any ordering, nor
discovery order. This is stated on the map itself. It is not merely unused — the
arcs are pairwise SKEW lines in a 3-dimensional space, so their separations do
not embed in one dimension and any vertical placement would impose an order the
geometry does not have.

**Vertical alignment is now meaningful, but only for the wall.** Station
positions are per-line, so a column shared by two lines would be coincidence —
and in a transit map a column reads as correspondence, the way a timetable does.
Rather than leave that hazard, each line's station spacing is chosen so that the
W4 wall crosses all three at the same x, making it a straight vertical boundary:
A between 403 and 2741, C between 1785 and 1930, B between 1614 and its
terminus. That one vertical carries meaning — which side of the wall a class
sits on. No other vertical alignment does, and the caption says so.

**The one feature worth pointing at.** C and D1's carriers meet exactly, but at
s = −6.84 on C and t = 0.391 on D1 — outside both 727 ranges, at a point
counting 725. The map draws that as a crossing WITHOUT an interchange, the
transit convention for lines sharing no station, because it is precisely why the
component count stays at four.

### What has changed since it was drawn

Less than for `shapes` — every number printed on `arcmap` still holds. The
2026-08-05 work confirms rather than contradicts it: both of the record's
tangents were re-verified exactly, so the line-D interchange is real, and the
point-at-infinity test now proves what the map assumed, that **none of the four
arcs wraps** (the half-turns about their directions count 699, 693, 689, and 693
and 691 for D's two tangents).

One thing the map cannot show has become worth saying beside it. The 723
stratum, which every terminus on this map steps down to, is itself a
one-parameter family — and it **wraps**, spanning 21.19° of rotation against
3.99–8.43° for the arcs drawn here. So the grey "723" annotations around the
edge of this map are not background: they are a loop 2.5× longer than the
longest line on the map, and the 727 network sits inside a much larger structure
that the frame excludes. A redraw might show 723 as the enclosing ring it is.

---

## 3. `shapes.png` — the maximiser set at every n, side by side

**What it is.** One figure comparing the shape of the maximiser set for n = 2
through 8, drawn in a single frame so the levels can be read against each other.
`shapes.svg` is the source; `shapes.png` is 1800px, `shapes@2x.png` 3600px.

**The mark carries the dimension**, which is the whole point of putting them in
one frame:

| mark | meaning | where |
|---|---|---|
| filled dot | 0-dimensional — finitely many maximisers | n = 3 (two), n = 5 (one, vs single-cube moves) |
| line | a 1-dimensional continuum | n = 2 (a punctured circle), n = 6 (arcs + interchange), n = 7 |
| dashed patch | 2 or more dimensions | n = 4 (≥3), n = 8 (≥2) |

Dimension is measured in CLASS space throughout — the three gauge dimensions of
rotating a whole compound are quotiented out and never counted.

**What it shows that the table does not.** That **n = 3 is the only finite
case**, sitting between continua on both sides. Every level set here is
semialgebraic, so it has finitely many components and each is either a point or
a continuum — a maximiser set is finite or uncountable, never countably
infinite. Only n = 3 takes the finite option, with exactly two classes, both
irrational, in ℚ(√2) and ℚ(√5). Reading left to right the symmetry also decays
from the full octahedral group at n = 3 down to trivial from n = 6 on.

**Caveats printed on the figure.** The n = 4 and n = 8 dimensions are LOWER
bounds from the axis-aligned probe, which cannot see a locus in general
position; n = 5's zero holds only against moving a single cube, since
multi-cube directions have never been tested at any n.

### Redrawn 2026-08-06 — what changed and why

`shapes.svg`, `shapes.png` and `shapes@2x.png` were regenerated on 2026-08-06 and
now match `MAXIMISER_TAXONOMY.md`. The mirror in `github/` was updated with them.
The figure gained a fourth and fifth mark, a drawn legend, and a taller canvas
(720px, was 660). What was wrong before, kept because the corrections are the
point:

| the figure says | now |
|---|---|
| `n = 8` · `1891` | **1895** — a new record; the whole n = 8 column is superseded |
| `n = 4` · `≥3-dim`, dashed patch | **0 by every probe** — the "≥3, 6 of 18 aligned moves" figure is withdrawn as unsourced and unreproducible; 0 of 20 aligned at three ε, 0 of 870 integer directions at three scales |
| `n = 5` · `components —` | ≥1 |
| `n = 7` · `components —` | ≥1 |
| `n = 8` · `components —` | ≥1 |

n = 4's dashed patch became a HOLLOW dot, and n = 5's filled dot became hollow
with it: a hollow mark now means the zero is only a reading, not an argument.
n = 8 keeps its dashed patch — 1895 still carries two independent aligned
directions, 2 of 42 — and only the value beside it changed.

**The headline was what the redraw had to solve.** "n = 3 is the only finite
case" is still the best-supported reading, but the figure would have stopped
carrying it: turning n = 4's patch into a dot puts dots in three of seven
columns, and a legend reading "a filled dot is 0-dimensional — finitely many
maximisers" would then contradict the headline printed below it. So the mark no
longer means the dimension alone. It distinguishes a zero with an argument
behind it (n = 3, filled) from a zero that only means no direction has been
found (n = 4 and n = 5, hollow), and the subtitle and both caption blocks say
so. That is the whole reason the figure still works with three dots on it.

**The n = 6 column does not change.** It is 727, and 727's arcs terminate —
re-confirmed by the point-at-infinity test. The family that wraps at n = 6 is
723, which is not on this figure because it is not the maximiser. And the loop
vocabulary already exists here: the n = 2 panel is drawn as a punctured circle,
three arcs with three open circles at the punctures. The legend text simply
never mentions it, listing only dot / line / dashed patch. A redraw should add
the loop to the legend rather than invent it.

**Caveats the figure prints are themselves now understated.** It says the n = 4
and n = 8 dimensions are lower bounds from the axis-aligned probe. Since then
`tight_set.py`, the method that would have upgraded them, has been shown to fail
its control at the n = 6 record, so there is currently NO method whose zeros are
trustworthy at any n — including the n = 3 zero this figure's headline rests on.
That headline is still the best-supported reading, but it is evidence rather
than proof and the figure does not say so.

---

## 4. `depth_explorer.html` — the compound, its walls, and the dihedral slider

**What it is.** The only page here that draws the actual GEOMETRY rather than a
summary of it: a 3-D view of a compound's cubes, the wall arrangement they cut,
and a cross-section through it, with the walls coloured by DEPTH — how many
cubes a region lies inside. 67 KB, self-contained, no network.

**Opening it.** `open depth_explorer.html`, then drag to orbit. It starts on a
preset; the four preset buttons are **723 record**, **octahedral √2**,
**golden √5** and **dihedral family**, and the text box takes any compound as
quaternions or as matrices (radio `quaternions` / `matrices`, then **Load**).
The 723 preset is the five-cube base plus `5,2,2,2`, so it is the 723 stratum's
own generator seen as a solid.

**The controls, and which are analysis rather than decoration.**

| control | what it does |
|---|---|
| depth / containment filters | show only regions at a chosen depth, or only walls bounding them |
| slice: normal ∥ x, y, z, (1,1,1) | the cross-section plane; the count of slice regions is displayed live |
| wireframe / walls by depth / opaque / clip / flip | render modes; `opaque` and `clip` are what make an interior depth legible at all |
| concurrences | rings where **4 or more face planes meet**, sized by multiplicity and coloured by kind — **gold = corner coincidence, blue = edge crossing** |
| spin, axis | slow rotation for reading a shape without dragging |

**The dihedral slider is the part with a result in it.** Selecting the family
preset gives ψ ∈ [0°, 90°] through the 3-cube dihedral family, with:

One cube rotates ±120° about an axis in its own face plane, and ψ tilts that
axis. Then:

* **`🔒 maintain concurrences`** — clamps dragging to the current core interval.
  Between the two golden copies, **ψ ∈ [20.905°, 69.095°]** — that is
  90° − arctan(φ²) and arctan(φ²) — a fixed core of **18 edge concurrences**
  stays exact and unbroken across the whole drag; outside that interval the core
  is **12**. The lock is what makes the sweep a path along a stratum rather than
  a drift off it, and the 18-to-12 step is the page's central claim.
* **ticks at the region-count transitions**, at ψ = 20.905°, **45°** and
  69.095°, plus **ghost-free zones** marking where nothing changes.
* the two octahedral values, **ψ = arcsin(1/√3) ≈ 35.264°** and
  **ψ = arctan(√2) ≈ 54.736°**, shown as **momentary spikes** in their own mark
  colour. The page's own comment records what they are: +12 extra coincidences
  existing only exactly AT those isolated ψ, with the set reverting on either
  side and the core untouched. That is the **wall dip** of
  `MAXIMISER_TAXONOMY.md` §1, drawn well before it was named there — a
  coincidence that exists only on the wall and changes nothing on either side of
  it. If you want to see why a sweep must not report the value it finds at a
  nice-looking parameter, drag the slider onto one of those two spikes.
* the arithmetic is why the two named angles matter: √2 resolves at the
  octahedral point and φ = (1+√5)/2, hence √5, at the golden point — the same
  two quadratic fields the two 67s live in.

**Specs and report.** `specs/DIHEDRAL_SLIDER_SPEC.md`, `dihedral_slider_report.md`,
and `specs/SLIDE3_SPEC.md` / `SLIDE3_SPEC_V2.md` for the underlying slide-3 work.

**Older copies exist and differ.** `bak/depth_explorer.html` and
`bak/depth_explorer.07-15.html` are earlier versions — `bak/depth_explorer.html`
is NOT identical to the live one. `github/scratchpad/` holds two more, including
`depth_explorer.pre-highlight-zoom-clip.html`, whose name records the feature
added after it. Treat the top-level file as the only current one.

---

## 5. `seed119_viewer.html` — the exact-search seed explorer

**What it is.** A browser for the six-cube exact search: type a seed, see that
seed's compound in 3-D, its exact region count, its by-depth histogram, and its
six integer quaternions. 56 KB, self-contained.

**The filename is stale and the file is not.** It was named at seed 119 and has
been regenerated repeatedly since: the embedded snapshot now covers **seeds 0
through 1176**, counts ranging 463 to 619. Do not infer the contents from the
name.

**Opening it.** `open seed119_viewer.html`; drag to orbit, scroll to zoom. The
seed box (with −/+ buttons) is the only real input; `face opacity` and
`slow spin` are view settings. It opens on seed 403.

**What the embedded data is.** One entry per seed: the exact bounded-region
count, and for seeds 40 upward the full by-depth vector. Seeds 0–39 were
certified in a batch that recorded counts only, so their histograms are absent
and the bar chart is empty for them — that is missing data, not a zero.

**The one number to read it for.** The best seed in the snapshot is **1026, at
619**, with by-depth `110, 206, 164, 102, 36, 1`. Set against the conjectured
per-depth ceiling `112, 208, 164, 102, 36, 1` — total 623 — it is 2 short at
depth 1 and 2 short at depth 2 and exactly at the ceiling in every deeper slot.
That is the page's actual argument: random seeds saturate the deep structure and
lose only at the shallow end.

**It self-checks.** A hidden banner (`id="warn"`) appears if the page's RNG
reimplementation disagrees with the search's, because the geometry is
regenerated in the browser from the seed rather than shipped: if the RNG does
not match, the shapes are not the certified ones. If that banner is visible,
the counts are still right and the picture is not.

**Regenerating it.** `make_seed_viewer.py` rebuilds the HTML from
`exact_search_results.jsonl` plus the hardcoded seeds 0–39 batch. Note the
script's paths point at a scratchpad under `/private/tmp` and a log under
`~/carroll/`, neither of which is in this repo — it will need its two path
constants repointed before it runs. `cb/seed119_viewer.html` is a byte-identical
older copy.

---

## Where the duplicates are

Three trees hold copies, and only the top level is current:

* **`github/`** — a full mirror, byte-identical for **all twelve** figure and
  page files (verified with `cmp` on 2026-08-05). It is a publication staging
  copy, not a fork.
* **`bak/`** — older `depth_explorer.html`, which DIFFERS from the live file.
* **`cb/`** — an older working directory; its `seed119_viewer.html` is identical
  to the live one.

If a figure is regenerated, `github/` needs the same file or the mirror silently
goes stale.

---

## Removed

**Deleted 2026-08-04:** `The shape of two cubes.html`. Despite the name it was
the browser-saved OUTER page of the published artifact — 12 KB carrying
`data-frame-uuid="20ce90bc-…"`, three loader scripts, and no map content at all
(no canvas, no great circles, no body diagonal; its entire visible text was
"Claude Artifact" and a CSS variable block). It loaded its content over the
network and rendered nothing offline. `n2map_standalone.html` replaces it.
Recorded here because the filename was more authoritative-looking than the file:
a browser "Save Page As" on an Artifact captures the shell, not the artifact.
