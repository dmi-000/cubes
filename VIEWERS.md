# The HTML viewers

Standalone pages in this directory. Each opens in a browser with no server and
no network — everything is inlined, because the Artifact CSP that these were
built under blocks external hosts.

---

## `n2map_standalone.html` — "The shape of two cubes"

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

The page presents the n = 2 map as of Postscript 70 and has **not** been
regenerated since. Three later results refine it:

* **Postscript 76** — the 13-locus is BIGGER than the page's summary card
  suggests. "Body diagonal → 13" is the headline, but 13 also occurs on mirror
  planes and edge arcs; the page's own data table already shows this ((1,2,0)
  reaches 13 once, (1,1,0) six times), so the table is right and the summary
  card is incomplete.
* **Postscript 83** — the 13-locus about a body diagonal is a punctured
  **circle**, not an arc: it wraps through the half-turn at t → ∞ and is
  punctured at the identity and the two 120° symmetries, where the count
  collapses to 1.
* **Postscript 86** — the n = 2 maximiser's symmetry group is **D₆**, not merely
  "order 12", which is why that circle's three punctures form one C₃ orbit and
  collapse to a single arc in class space.

Anyone regenerating this page should fix the summary card first.

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

## `arcmap.png` — the 727 arc network as a transit map

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
artifact, see Postscript 97.) Station spacing within a line is even rather than
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

---

## `shapes.png` — the maximiser set at every n, side by side

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

---

## Other pages here, not yet documented

* `depth_explorer.html` (61 KB) — the dihedral-family slider: ψ from 0° to 90°
  through a 3-cube compound with exact face-plane coincidences, with a
  maintain-concurrences lock and marks at the region-count transitions. See
  `DIHEDRAL_SLIDER_SPEC.md` and `dihedral_slider_report.md`.
* `seed119_viewer.html` (56 KB) — the seed explorer.

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
