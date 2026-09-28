# What each document is for, and how it is kept

Every document here makes one of three promises, and the promise decides how it is written, how it
is corrected, and how the audit treats it. A document that mixes promises is the usual source of
confusion: a record read as a statement of current belief, or a summary that quietly accumulated a
history.

This file is itself a **current-knowledge** document: the policies below are stated as they are
now, each with a pointer to where it was set. How they evolved is in the record ([P386](LEDGER.md#p386)–[P388](LEDGER.md#p388),
[`INTERVENTIONS.md`](INTERVENTIONS.md) A20), not here.

*Written 2026-09-24. The classification table below is read by `src/claim_deps.py`, so editing a
row changes how the audit treats that file.*

## The three kinds

### The record: auditable, history preserved

**Promise:** says what was done and what was believed, and when. **Never rewritten.**

**For:** AI and script audits, and as the source material for everything else. Not meant to be
read straight through by a person: its entries contradict each other by design, because each
records its own day's belief and the corrections are separate entries.

**Correcting it:** leave the original text; add a dated in-place note beside the claim, using the
vocabulary below, plus the structured status tag. Never delete.

**Verbatim records** are a sub-kind, never corrected at all: session transcripts and exports
(`*-this-session-*.txt`), `transcripts/`, the published copy under `github/`, and every file in
`data/`. They are what was actually said or computed; a correction to them would be a forgery.

### Current knowledge: strongest present beliefs

**Promise:** every statement is what is believed **now**, and each cites the ledger entry it rests
on now: the latest authority ([P383], not [P307]).
<!-- reviewed 2026-09-24: names P307 as the superseded example, P383 as current -->

**Not historical.** No strike-throughs, no "previously we thought". One exception: a belief that
**overturned** an earlier one may say so in a sentence when the overturn is itself informative ("the
records are continua, not the isolated points once believed"), because a reader who met the old
belief elsewhere needs to know it is dead.

**Correcting it:** rewrite in place to the current belief. The history of the change goes in the
record.

**Audit:** every citation is a live dependency. When a cited postscript falls, the audit lists the
sentence, and it must be rewritten.

### Narratives: history told for people

**Promise:** a readable account of what happened, grounded in what is true. Two strands, often in
one document: the story of the mathematics, and the story of the human-machine collaboration.

**Free to rewrite.** No result depends on a narrative, so changing one undermines nothing. A
narrative may highlight or summarise earlier beliefs, skip them to follow a different thread, or
order them chronologically or logically: whatever suits the telling.

**Every narrative is dated, and speaks only up to its date.** A narrative expresses the beliefs
held when it was written; it cannot be expected to know what came after, and it makes no claim
about anything after its date. The date must be honest: when a narrative is brought up to date,
its date moves with it.

**What makes a narrative wrong, as opposed to out of date:**
- **A false statement about what was believed, or when.** A story may leave a belief out; it may
  not misdate or misattribute it. A stale header date is such a statement.
- **A belief its own date had already superseded,** told without its successor. Writing on
  2026-09-16 that a record is isolated, when that fell on 2026-09-12, is an error; writing it on
  2026-08-02 was not.
- **A claim that something is PROVED, when it was not.** A proof claim is timeless, so a flawed
  one is a flaw at any date and needs correcting. Correct it visibly and with a date, in the
  narrative's own style (JOURNEY uses `[CORRECTED <date>: ...]`), so the rest of the text keeps its
  honest as-of date.

**Out of date is not wrong.** An outdated narrative is like an incomplete search: worth completing
eventually, and completing it is one goal among many competing for the same effort.

**Preserve what is still interesting.** Rewriting is free, but a passage that is worth reading
should survive in some form: kept, moved, or condensed, rather than deleted.

**Checked by reading, not by markers.** Narratives are written for people and are never shaped
for a tool: no correction vocabulary, no pointers, no comments. The audit and `--fell` may LIST
narrative passages that cite or restate a fallen claim. Most of that list is a completion
backlog; the items that matter now are proof claims, and beliefs already superseded at the
narrative's own date.

## Classification

The kinds are `record`, `verbatim`, `current`, `narrative`. `src/claim_deps.py` reads this table:
one row per file or pattern, first matching row wins.

| file | kind | note |
|---|---|---|
| `LEDGER.md` | record | the append-only project record; the audit's primary source |
| `INTERVENTIONS.md` | record | what human attention changed, entry by entry |
| `DELEGATION_LOG.md` | record | what subagents were asked, what came back, what was re-verified |
| `FAILURE_MODES.md` | record | incidents organised by symptom; each entry is a dated occurrence |
| `C45_notes.md` | record | working notes, 2026-07-10 |
| `EXPLORATION_141.md` | record | exploration log |
| `census_variety_lineage.md` | record | data archaeology |
| `unsourced_audit.md` | record | audit of RESULTS.md claim blocks, round 1 |
| `unsourced_audit2.md` | record | round 2 |
| `INVENTORY.md` | record | migration inventory, 2026-08-04 |
| `REPO_TRIAGE.md` | record | migration triage, 2026-07-30 |
| `DATA_INVENTORY.md` | record | generated by `data_inventory.py`; do not hand-edit |
| `DIHEDRAL_FAMILY_NEXT.md` | record | a handoff: instructions as given |
| `ALGEBRAIC_SEARCH.md` | record | a search and its outcome |
| `MAXIMISER_TAXONOMY.md` | record | the older per-level working record; its status claims predate the continuum results. Current status: `LEVELS.md` |
| `max2_report.md` | current | the certified proof of `max(2) = 13` (a report by name, a proof in content) |
| `*_SPEC*.md` | record | specifications as given to a subagent |
| `SYMMETRY_SEARCH_V*.md` | record | specifications as given to a subagent |
| `*_report*.md` | record | a run and its outcome, as reported at the time |
| `*-this-session-*` | verbatim | session exports |
| `LEVELS.md` | current | per level: record, proof status, plateau, classes, connections |
| `RESULTS.md` | current | everything, tagged by strength. *Known drift: to be rebuilt on `LEVELS.md`* |
| `ORIENTATION.md` | current | one screen: named objects, framework, traps |
| `SESSION_STATE.md` | current | the working state. *Must be PRUNED, not appended to: it accretes history* |
| `OPEN_QUESTIONS.md` | current | what is open, and what has been ruled out |
| `GLOSSARY.md` | current | vocabulary |
| `MAXIMISERS.md` | current | exact representatives, with commands |
| `CONTINUUM_MAP.md` | current | the plateaus mapped, and how they extend |
| `TYPOLOGY.md` | current | the 727 plateau classified; generated by `make_typology_note.py` |
| `N3_STRUCTURE.md` | current | the n = 3 structure graph |
| `METHODS.md` | current | what to do, each with the measurement that earned it |
| `DATA_MANIFEST.md` | current | which data files are current, superseded or wrong |
| `VIEWERS.md` | current | the figures, and which are stale |
| `README.md` | current | the map of the repository |
| `DOCUMENTS.md` | current | this file |
| `PROOF_67.md` | current | `max(3) = 67`, consolidated |
| `PROOF_FORMAL.md` | current | `max(3) = 67`, formalised |
| `PROOF_STEP_T.md` | current | step T of the n = 3 proof |
| `PROOF_SUBSET.md` | current | Theorem S, all n |
| `PROOF_L1b.md` | current | Theorem NP, a DRAFT proof |
| `JOURNEY.md` | narrative | the project's own story, told from inside: both strands |
| `AN_HOUR_AND_A_MONTH.md` | narrative | the collaboration, told from beside it |
| `PROOF_NARRATIVE.md` | narrative | how `max(3) = 67` got proved |
| `OVERVIEW.md` | narrative | the ten-minute tour; brought up to 2026-09-16 |
| `PROJECT.md` | narrative | the standalone write-up; brought up to 2026-09-16 |

`max2_report.md` sits above `*_report*.md` on purpose: first match wins.

## The order of an audit

Corrections flow the way citations run backward: **the record first, then current knowledge, then
narratives.** A narrative cites current-knowledge documents, which cite the ledger, so bringing a
narrative up to date before the documents it draws on either repeats the work or copies a claim
that is about to change. Within the record, settle upstream questions before the claims built on
them: an unevaluated doubt about a proof gets resolved before any summary of that proof is
rewritten. The one exception is a flawed PROOF claim in a narrative, which is corrected when found,
dated, whatever the order.

## How a claim is corrected

### The vocabulary

The words are not interchangeable, and the audit reads them.

| word | means |
|---|---|
| **REFUTED** | a valid measurement or proof shows the claim false |
| **CORRECTED** | the claim was wrong AND a replacement value exists (20 becomes 26) |
| **VOID** | the claim was never validly measured: a broken instrument, bad inputs. The number says nothing either way |
| **PROOF GAP** | the claim was stated as PROVED and its proof has a hole. It may well be true; it is not proved (953 at n = 4, [P249]) |
| **WRONG** | a plain verdict, used beside a quoted claim (`"isolated in both senses"  WRONG -- ...`) |
| **REINSTATED IN PART** | a claim once declared refuted was partly right after all |
| **Scope note** | the claim stands, but for less than it said |
| `... IN PART` | any of the above, applying to part of the entry; the note says which part stands |

Set in [P387](LEDGER.md#p387) and [P388](LEDGER.md#p388) (VOID added as its own term 2026-09-24, after
checking it was already used 35 times with this meaning; WRONG, in capitals, after checking its 47
uses were all verdicts). VOID and WRONG are recognised only in capitals, since the lowercase words
are ordinary prose. **CLOSED is deliberately not a correction word**: it mostly means an open
question was answered, sometimes in agreement with the claim beside it.

### In the record: an in-place note, a pointer, and a status tag

1. **In the fallen entry itself**, a dated blockquote near its heading saying what fell and what
   stands: `> **CORRECTED 2026-09-20 by [P383](#p383): the n = 8 figure is 3, not 2.** ...`
2. **At each dependent that a reader could act on** (a dead number stated as current, an argument
   built on it, a next step it made moot), a bare dated pointer in the same paragraph:
   `**VOID 2026-09-13 ([P322](#p322)).**` The target must cover the SPECIFIC claim: grep the target
   for it before writing. Citations of the part that stands, passing mentions, and the refuting
   entry's own discussion get no pointer.
3. **A structured status tag** at both ends, the corrector and the corrected, so that no tool has to
   infer role from prose:

       <!-- status: corrected-by=P383; fell="n = 8 figure is 2" | "1, 2, 2"; stands="n = 6, 7 values" -->
       <!-- status: corrects=P307 -->
       <!-- status: corrected-by=self; fell="..." -->     refuted inside its own entry

   **The tag must start its own line**, directly under the heading. A tag quoted inline as an
   example is ignored; before that rule, one quoted example turned every `...` in the repository
   into a match. Repeat a key for several correctors (`corrected-by=P323; corrected-by=P331`); a
   comma list is not read.

   `fell=` lists **distinctive** strings from the claim that fell. The audit searches every
   document for them, which is the only way to find a restatement that carries no citation. They
   must be distinctive: `1, 2, 2` alone also matches the vertex signature `(1,2,2)` and quaternions
   like `5,2,2,2`, so it is only usable alongside a longer string. `python3 src/claim_deps.py --fell`
   runs the search, over current-knowledge documents and the record outside the ledger; a hit
   counts as handled only if a correction word is in ITS OWN paragraph, or an in-place correction
   blockquote (`> **CORRECTED ...`) directly follows it.

**Adopted 2026-09-24.** All 30 postscripts known to have fallen carry a tag, with the 27 entries that
corrected them. For any entry without one, the audit falls back on the in-place blockquote and on
the heading forms listed in [P388](LEDGER.md#p388).

### In current knowledge: rewrite

No pointers, no notes: change the sentence to the current belief and cite the current authority.
The audit's job there is only to say which sentences need rewriting.

### Recording that a citation was checked and left alone

`<!-- reviewed 2026-09-24: cites the surviving part -->` next to a citation deliberately left
unmarked. Without it, "checked and fine" and "never checked" look the same, and every audit
after a compaction re-reviews both.

## Why the policies look like this

Each rule answers a failure that happened. The detail is in the record; the one-line versions:

- **Citations point backward, refutation travels forward**, so corrections were propagated from
  memory, and memory is what a compaction destroys. Hence a tool that inverts the graph ([P386](LEDGER.md#p386)).
- **A heading's tag names an action, not a status**, and a name in a title does not carry its
  role (victim, winner or corrector all appear the same way). Three successive versions of the
  tool inverted a relationship by reading English. Hence the status tag ([P387](LEDGER.md#p387),
  [P388](LEDGER.md#p388)).
- **The dangerous stale claims had no citation at all**: OQ 36's `T3 = 74`, the phantom `K4`
  branch in [P368] and in `SESSION_STATE.md`, "727 is isolated" in `CONTINUUM_MAP.md`. Only reading
  found them, or searching for their exact wording. Hence `fell=`.
- **Summaries built from summaries drift**: `LEVELS.md`'s first draft called n = 2 unmapped, copying
  `MAXIMISER_TAXONOMY.md` instead of [P69](LEDGER.md#p69) (INTERVENTIONS A20). Hence: current-knowledge
  documents cite ledger entries, never other summaries, as their authority.
- **The ledger's entangled corrections make it unreadable as a picture of the present**, which is
  why current knowledge lives in separate documents at all (user decision, 2026-09-24).
<!-- reviewed 2026-09-24: cites the fallen value as the example of an uncited restatement -->
