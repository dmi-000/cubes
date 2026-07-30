# Repo triage: what moves into the git repo, what stays behind

Generated 2026-07-30 for the proposed consolidation (`~/carroll/cubes` -> `~/cubes`,
worked in directly; `~/carroll` keeps the AMA material).  Covers the 259 top-level
entries that are NOT currently in the repo.  Nothing here has been moved --
this is a proposal for approval.

## 1. Move into the repo (source and docs, small, currently untracked)

- `DIHEDRAL_FAMILY_NEXT.md` (8 KB)  <- referenced by the ledger/memory but never tracked
- `index_ledger.py` (4 KB)  <- regenerates the ledger's postscript index
- `record_hunt.py` (12 KB)  <- today's record-hunt tooling
- `record_hunt_wave2.py` (4 KB)  <- today's record-hunt tooling
- `record_hunt_wave3.py` (4 KB)  <- today's record-hunt tooling
- `recover_1889.py` (4 KB)  <- today's record-hunt tooling
- `scratch_diagram` (152 KB)  <- census tools + result_*.json cited in Postscript 5

The four scripts are the tooling behind 727 / 1217 / 1891; `record_hunt.py` is
reusable at every level.  `scratch_diagram/` holds the exact-arrangement census
code the proof program cites.

## 2. Cube-project data -- keep out of git, extend `.gitignore`

Current `.gitignore` is one line (`*.jsonl`).  These are project outputs, not
source, and total ~1.4 GB:

- `json` (410668 KB)
- `campaign_results.jsonl` (190104 KB)
- `glue_results.jsonl` (107584 KB)
- `campaign_n7.jsonl` (58748 KB)
- `campaign_n4.jsonl` (57944 KB)
- `campaign_n5.jsonl` (43364 KB)
- `shared_axis_search.jsonl` (41072 KB)
- `blueprint_search.jsonl` (37448 KB)
- `slide3_search.jsonl` (37120 KB)
- `algebraic_walls.m` (33800 KB)
- `n7_program.jsonl` (21172 KB)
- `rattan_results.jsonl` (20264 KB)
- `n4_search.jsonl` (19228 KB)
- `n5_search.jsonl` (14820 KB)

...and 131 more.  Proposed `.gitignore`:

    *.jsonl
    *.out
    *.log
    *.bak
    *.bakc
    *~
    \#*\#
    __pycache__/
    .DS_Store
    json/
    algebraic_walls.m
    cube_regions
    cube_regions_n

(The compiled engines are rebuilt from `cube_regions.cpp` in one command, so
they do not belong in the repo; the README already documents the build line.)

## 3. Leave in `~/carroll` -- not this project

- **AMA / Mindscape material**: 55 entries (~142 MB) -- the Patreon and Mindscape
  HTML, `Mindscape AMA - Q&A*.tsv/csv`, `ama_questions*.json`, `.webarchive`,
  `patreon_scrape.md`, the scrape output dirs (`page`, `export`, `posts`,
  `edit?pli=1`, `Ghost`).
- **Session transcripts**: 16 `2026-*.txt` exports (~3 MB).
- **Editor and shell debris**: `#common.*#`, `*~`, `.perldb_history`, `foo`,
  `sss`, `bak`, `common`, `2026-05-21`, and similar.

## 4. Your call

- `cb/` (1680 KB) -- a frozen snapshot of the project from ~10-11 July (record
  table tops out at 699, no `PROOF_67.md`).  Superseded in every respect by the
  repo's history.  **Recommend deleting**; git already holds that state.
- `census_data.json`, `nfamily_q3_records.json`, `glue_best.json`,
  `slide3_p*.json`, `opencount_wl_data.json` and friends (each < 150 KB) --
  small result files that reports cite by name.  **Recommend committing these
  specific ones** rather than blanket-ignoring `*.json`, so the cited numbers
  stay reproducible; the big `algebraic_walls.json` (72 KB) and
  `algebraic_walls.m` (34 MB) can stay out.
- `rosy-puzzling-hanrahan-agent-*.md` -- a leftover plan-mode artifact.
  Recommend deleting.
- `__pycache__/`, `.DS_Store` -- delete.

## 5. After the move

- `.claude/` settings live at `~/carroll/.claude`; the project ones should
  follow to `~/cubes` (or be recreated there).
- Path references to update: my memory file points at
  `~/carroll/six_cube_search_results.md` and `~/carroll/scratch_diagram/`;
  a few docs cite `~/carroll` paths.
- Future sessions should start in `~/cubes`.
- The running n=6 sweep writes `record_hunt_n6b.jsonl` / `.out` into
  `~/carroll`; move after it finishes, or those two files get left behind.
