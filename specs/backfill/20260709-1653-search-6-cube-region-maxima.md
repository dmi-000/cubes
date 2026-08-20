# Search 6-cube region maxima

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-07-09T16:53:49 |
| Agent type | general-purpose |
| Model override | sonnet |
| Session | `c4196554-d37e-44f9-8da5-5d7210e1f156` |
| Tool-use id | `toolu_01A6GMvoSGJg72krzRMTX9Hp` |
| Files named | `cube_compound_regions.py`, `six_cube_search.py`, `six_cube_search_results.md` |
| Present in repo | `cube_compound_regions.py`, `six_cube_search.py` |
| Cited in LEDGER/RESULTS | `cube_compound_regions.py`, `six_cube_search.py` |

## Prompt as sent

```text
Empirical search: among compounds of 6 congruent, concentric cubes (each cube an arbitrary rotation of [-1,1]^3 about the shared center), which configurations maximize the number of BOUNDED regions that the 6 cube surfaces cut space into? Work in /Users/dmi/carroll.

EXISTING TOOL (do not modify its validated logic; extend additively):
/Users/dmi/carroll/cube_compound_regions.py — a voxel region counter. Read its docstring first. Key API:
- compound(name) -> list of 3x3 rotation matrices (one per cube). Supports 'six6:THETA' (6 cubes: +-THETA degrees about x, y, z), 'axialN' (N cubes fanned about z, default twists k*90/N deg; also 'axialN:t0,t1,...' with explicit twists in degrees), 'escher3', 'bakos4', 'fiveN'.
- labels_grid(name, R) -> per-voxel n-bit inside/outside labels on an R^3 grid over [-1.8, 1.8]^3. A '+rot' suffix on the name applies a fixed generic global rotation (use it for any configuration with axis-aligned cubes — axis alignment with the grid causes systematic false merges).
- count(name, R, tau) -> prints and returns the bounded-region count. It merges "small" components (< tau ~ 3R voxels) into adjacent same-label big components (tip fragments of thin corners), NEVER merges big with big (distinct regions can touch at points), and counts unmergeable smalls as unresolved. Read the docstring's artifact taxonomy: counts can err BOTH ways (unresolved fragments overcount; sub-voxel separators undercount), so trust only values that agree across two resolutions.

STEP 1 — validate the tool (fast, mandatory): run
  python3 cube_compound_regions.py count one:200 stella:260 axial2:260 axial3:260 axial4:300 axial6:300
Expected bounded counts: 1, 9, 9, 25, 49, 121. The axial family obeys exactly (2N-1)^2 (proven: the cross-section squares' edge lines are all tangent to the common incircle, so no triple points). If these fail, stop and report.

STEP 2 — write a NEW file /Users/dmi/carroll/six_cube_search.py that imports from cube_compound_regions and adds a way to count arbitrary configurations (list of 6 rotation matrices, e.g. via scipy Rotation.random with fixed seeds or your own Rodrigues code — there is a rodrigues() in the module). Simplest approach: monkeypatch/extend compound() lookup or write a labels/count variant taking matrices directly (copy the ~20-line counting wrapper if easier; keep the small->big merge policy and tau=3R exactly as in count()).

STEP 3 — search, with this budget discipline (total compute ~40 min; each count at R=200 with 6 cubes takes tens of seconds; 64 labels max fits uint8):
  a. theta-sweep of the six6 family: 'six6:T+rot' for T in {5,10,15,20,25,30,35,40,44}, R=200.
  b. axial baseline: axial6 with a few random distinct twist lists (expect 121 every time — the family is provably constant; confirm once or twice).
  c. ~40 random configurations: 6 uniform-random rotations each, fixed seeds 0..39, R=200.
  d. take the top 3-5 configurations found anywhere; hill-climb each a little (perturb each cube by small random rotations ~2-5 degrees, keep improvements, ~10 steps), R=200.
  e. refinement: re-run the best ~5 configurations at R=300 AND R=380. Report two-resolution agreement and the unresolved-smalls counts. Only two-resolution-stable values count as findings.

STEP 4 — deliverable: write /Users/dmi/carroll/six_cube_search_results.md containing: the validation results; a table of all configurations tried (name/seed/params, bounded count at each resolution run); the winner and runner-ups with their depth histograms (the count() printout includes them); and honest caveats (voxel-level confidence only — the exact Q(sqrt5) counter in this directory cannot check random configurations since their matrices leave the golden field; artifact modes as per the docstring). Also state the reference points: the axial fan gives exactly 121; the five-cube compound (5 cubes) gives exactly 351; the loose ceiling from the 36-plane arrangement bound C(35,3) = 6545 is not remotely approached because cube faces are bounded squares.

Context you should know: random/generic configurations plausibly beat symmetric ones (more transversal face-face intersections; symmetric compounds have coincidences that merge regions), so do not be surprised if random seeds beat the six6 family. Report whatever you find, including negative results. Your final message should summarize: winner configuration, its stable bounded count, how it compares to 121/351, and where the results file is.
```
