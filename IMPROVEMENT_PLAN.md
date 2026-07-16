# Improvement plan: carroll (Sean Carroll AMA corpus)

**Audience:** Sonnet/Haiku Claude Code session, executing autonomously. Haiku
is sufficient. Origin: Fable review 2026-07-06.

**Context:** NOT a git repo. A data workspace: ~40 scraped Patreon/AMA HTML
snapshots (dated filename suffixes are the versioning), n-gram frequency
tooling (`freq.perl` reads stdin — no hardcoded paths), derived tables
(`common.*`, `common.30.sort` etc.), and unrelated scratch (`norton.py` is a
physics script, `life.c`). Purpose: drafting AMA questions from phrase-
frequency analysis of past episodes.

**Ground rules:** this directory has no version control, so every mistake is
unrecoverable — MOVE, never delete; copy before any transform. Do not edit the
HTML snapshots, `common.*` tables, or any file you cannot identify. Do not run
the Perl one-liners in comments.

## Task 1 — README.md (the main deliverable)
Write a README documenting, based on reading the files (not guessing):
1. The pipeline: which inputs (`*.html`, `*.tsv`?) feed `freq.perl`, what the
   `common.*` outputs are (weighted n-gram tables — see the score/count/phrase
   format), and what the numbered variants mean (`common.30`, `common.3000`
   look like different corpus sizes or thresholds — read the first lines and
   say what is verifiable, mark the rest "unclear").
2. The HTML snapshot naming convention (`…2025-04.167.html` = date + snapshot
   sequence) and which pages they are.
3. A short "unrelated files" section: `norton.py` (physics), `life.c`,
   `1254344_1.pdf` — so future sessions don't puzzle over them.
Mark every uncertain statement with "(unverified)". No file moves in this task.

## Task 2 — raw/ for the HTML snapshots
1. `grep -l -F '.html' *.perl *.py c.s common.w foo page posts 2>/dev/null` —
   confirm no script references the HTML files by path (freq.perl reads
   stdin, so expect none; the only reference seen so far is a comment naming
   a `.tsv`).
2. If zero live references: `mkdir -p raw` and move `AMA*`, `*Patreon*`
   (`.html` and `.webarchive`) into it. Update the README.
3. If any reference is found, skip the move and record it in the README.

## Task 3 — Optional: git for the tooling only
`git init`; `.gitignore` containing `raw/`, `*.html`, `*.webarchive`, `*.pdf`,
`*.txt`, `#*#`, `*~`, `common.*` (derived data). Commit only: `README.md`,
`freq.perl`, `.gitignore`, and other small hand-written scripts you can
identify as tooling (`c.s`, `norton.py`, `life.c` if desired). Message:
`Initial commit: AMA n-gram tooling and README`. Never `git add -A` here —
the corpus stays untracked by design.

## Flagged — needs the user, do NOT do
- Deleting the 17 MB `.webarchive` (an HTML twin exists, but confirm with the
  user before removing anything from an unversioned directory).
- Any transformation/re-scrape of the corpus.
