# Update PROJECT/JOURNEY/README docs

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-16T17:08:35 |
| Agent type | default |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_014ge5TGUUgSGJHrLJU4txWh` |
| Files named | `dihedral_slider_report.md`, `handoff_report.md`, `nfamily_report.md`, `opaque_report.md`, `q3_count.py`, `q6_count.py`, `six_cube_search_results.md` |
| Present in repo | `dihedral_slider_report.md`, `handoff_report.md`, `nfamily_report.md`, `opaque_report.md`, `q3_count.py`, `q6_count.py` |
| Cited in LEDGER/RESULTS | `handoff_report.md`, `nfamily_report.md`, `q3_count.py`, `q6_count.py` |

## Prompt as sent

```text
Update the project documentation in /Users/dmi/carroll to cover everything since the last doc update. Sources (all READ-ONLY except the three docs you are updating): six_cube_search_results.md Postscripts 25 (+ 4 addenda) and 26 (+ addendum), C45_notes.md section 12 (four new theorems), nfamily_report.md, handoff_report.md, dihedral_slider_report.md, opaque_report.md, DIHEDRAL_FAMILY_NEXT.md. Files to update: PROJECT.md (formal, self-contained — all terms defined), JOURNEY.md (informal narrative, self-contained), README.md (index — new files and one-paragraph pointers).

New material to integrate:
1. The dihedral family saga (Postscript 25 + addenda): prompted by the user noticing coincident edges perpendicular to (1,1,1) in the viewer; the closed-form family (cube rotated ±120° about an in-face-plane axis (sinψ,cosψ,0)); both 67s are members (octahedral at arcsin(1/√3), golden at tanψ=φ² via φ²+φ⁻²=3); the old slide's ghost gaps explained as leaving the family; the new ℚ(√6) face-diagonal compound with certified count 49={30,18,1}; the core-18 persistence across the whole octahedral→golden drag with corner docking at t=±1/φ³ and ±1; the exact staircase of counts along the family (25/31/43/55 symmetric about 45°, spikes 67/49/67 — the face-diagonal point is a local MINIMUM, extra coincidences can merge regions); the 26-concurrence chain path and the handoff-chase verdict (18 stands end-to-end, obstruction identified at the ψ=45°/tetrahedral-angle wall).
2. Postscript 26: the records are built from family pairs (183: 6/6 pairs, 393: 10/10, 723: a family 5-clique + glued cube), but single-axis family sweeps top out at 175/335/615 — records are gluings of cliques on different axes; deep layers pinned at exactly the record values at every n, deficits all in shallow layers.
3. The four theorems (C45 §12): mirror ψ↔90−ψ, 90° periodicity, the coincidence identity (proved for all n and phases), and the rational-invariant obstruction with the conditional corollary that n=3 is the unique irrational level of the record tower.
4. New engines: q3_count.py (ℚ(√3)) and q6_count.py (ℚ(√6)) field clones; the Rel-gauge closed form making Pythagorean family members integer-quaternion (C++-countable).
5. Viewer additions (published artifact, same URL): opaque surfaces with depth/containment coloring, the dihedral-family slider replacing the old slide (named ticks incl. mirror-golden, core-aware "maintain concurrences" lock, corrected transition marks), split/merge surface highlighting, zoom, one-sided clipping.
6. Ongoing (mark as in-progress, do not overclaim): the two-clique gluing search, the n=4 resonance algebraic solve.

REQUIRED: JOURNEY.md must state clearly (in its introduction or the collaboration section) that the document itself — like the project's code, searches, and analysis — was written by AI (Claude), working under human direction, with the human contributors (the user, and correspondents like Chris Cole and Werner) supplying questions, corrections, and key observations (e.g. the perpendicular-edges observation that unlocked the dihedral family). Keep the existing tone: honest, concrete, no hype.

Style: match the existing documents' voice and structure; keep PROJECT.md formal and JOURNEY.md narrative; update the records/structure tables only where the new material touches them (records are UNCHANGED: 13/67/183/393/723/1207/1879). Do not edit six_cube_search_results.md, C45_notes.md, or any validated file. Report back: what you changed in each file, section by section, and anything you chose to leave out.
```
