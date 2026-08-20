# Establish census_variety lineage

> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**
> This is the prompt as it was sent, extracted from the session
> transcript by `extract_specs.py` on demand. It records what was
> ASKED. It does not certify that the delivered code satisfies it:
> no diff against this text was performed at the time, because this
> text was not on disk at the time. See
> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).

| | |
|---|---|
| Delegated | 2026-08-18T02:52:18 |
| Agent type | general-purpose |
| Model override | haiku |
| Session | `833a739b-86d7-4754-94e1-446688dfcac3` |
| Tool-use id | `toolu_014zDGB2naep5KDMm5d4XUMk` |
| Files named | `3.json`, `census_variety.py`, `census_variety_lineage.md`, `census_variety_redo.json`, `d.json` |
| Present in repo | `census_variety.py`, `census_variety_lineage.md`, `census_variety_redo.json` |
| Cited in LEDGER/RESULTS | `census_variety.py` |

## Prompt as sent

```text
Read-only data archaeology in `/Users/dmi/cube-compounds`. **Do not edit or delete any file.** Produce one new report file and nothing else.

# THE PROBLEM

There are five generations of one campaign's output:

    census_variety_0..3.json        (4 files)
    census_variety_redo.json        (1 file)
    census_variety2_0..3.json       (4 files)
    census_variety3_0..3.json       (4 files)
    census_variety4_0..3.json       (4 files)

`census_variety.py` today writes `census_variety4_%d.json`. **Nothing in the repository writes generations 1, 2 or 3** — the script was edited in place for each generation, so the producing code is gone. Which generation supersedes which has never been established, and `DATA_MANIFEST.md` records the lineage as UNAUDITED.

# TASK — establish what can be established, and say clearly what cannot

For each of the 17 files, gather:
1. **Modification time** (`ls -la --time-style=full-iso` or `stat -f '%Sm'`).
2. **Record count** and the JSON structure: top-level type, and the KEYS of one record (`python3 -c "import json;d=json.load(open(F));print(type(d),len(d));print(list(d[0].keys()) if isinstance(d,list) and d else '')"`).
3. Whether records carry identifying fields (n, k, count, idxs, status, lineality, or similar).

Then:
4. **Do later generations COVER earlier ones?** For each pair of generations, compute the set of record identities (whatever key uniquely names a class — e.g. `(n,k,tuple(idxs))` if present, else `(n,count)` or whatever exists) and report: how many identities in gen X also appear in gen Y, and how many are unique to X.
5. **Do they AGREE where they overlap?** For identities present in both, compare the substantive fields (status, lineality, dirs, confirmed...). Report the number that agree and the number that DISAGREE, and show up to 5 disagreements in full.
6. Check `census_variety*.log` files if present for clues about what each run did.
7. Check `LEDGER.md` for mentions of these files or of reruns — grep for "census_variety", "GeneratorsNeeded", "rerun", "redo". Postscript 117 is known to describe 23 classes that crashed with `GeneratorsNeeded` and were rerun; work out whether one of these generations IS that rerun.

# WHAT TO REPORT

Write `/Users/dmi/cube-compounds/census_variety_lineage.md` containing:
- A table: file, mtime, records, structure.
- A supersession verdict per generation: which is newest, which is covered by which, whether any generation contains records found nowhere else (those cannot be discarded).
- **Any DISAGREEMENT between generations on the same class — this is the most important output.** If two generations give different `status` or `lineality` for the same class, one of them is wrong, and that matters.
- An explicit list of what could NOT be determined and why.

# RULES

- Read-only. Create only `census_variety_lineage.md`.
- Exact comparisons; do not round or approximate.
- If a file is unparseable or empty, say so — do not skip it silently.
- Do not guess which generation is authoritative from filename numbering alone; state what the DATA shows. If the evidence is only "gen4 has the newest mtime", say exactly that and no more.

Report back: the supersession order if determinable, and the count of cross-generation disagreements.
```
