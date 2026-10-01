#!/usr/bin/env python3
"""The citation graph, INVERTED — what depends on a postscript, and what needs revisiting.

THE FAILURE THIS EXISTS TO CATCH, re-measured 2026-09-23 after the selector was fixed: of 361
citations to postscripts that have FALLEN, **175 (48 %) carry no correction marker anywhere near
them**, plus 9 SUSPECT postscripts with 84 more, uncounted. The figure moves as documents are
written; `--audit` prints the live one, in two tiers that mean different things.
[P375] is the founding example — its parity claim was refuted the same day it was made, the
entry was marked, and not one of the places relying on it was.

(The first version of this tool reported 207 of 284, 73 %. Both numbers were wrong, and in the
worse direction: the selector keyed on the heading TAG, which is an ACTION tag, so it counted
citations to the CORRECTORS. 13 of its 18 rows were current results — acting on that audit
would have stamped REFUTED markers on [P330], [P374], [P378] and [P383]. See REFUT_FAMILY.)

WHY IT HAPPENS, and it is structural rather than careless. A citation points BACKWARD: a claim
names the evidence under it. Refutation has to travel FORWARD: evidence invalidates the claims
above it. Nothing in the documents runs that direction, so propagation is done from memory by
whoever just wrote the refutation — and memory is exactly what a compaction destroys.

WHAT THIS DOES.  Builds the citation graph over the authored documents, inverts it, and answers
the only question that matters when something falls: **what did this hold up?**

    python3 src/claim_deps.py P352          # everything that cites P352, with its context
    python3 src/claim_deps.py --audit       # every FALLEN postscript with unflagged dependents
    python3 src/claim_deps.py --stats       # graph shape
    python3 src/claim_deps.py --fell        # uncited restatements of what fell (status-tag strings)
    python3 src/claim_deps.py --hyp         # conditional results stated as proved without their condition

Which documents count, and how, is read from DOCUMENTS.md's classification table.

A dependent is FLAGGED if a correction marker appears in its paragraph or either neighbour,
and a postscript citing itself inside its own ledger entry is not a dependent at all. Both
windows are heuristics and both directions of error are live: a long postscript has parts that
survive, so citing those needs no flag (over-report); and a neighbouring marker about something
else now counts (under-report). It is TUNED to over-report — a false alarm costs a glance, a
missed one costs a wrong claim standing in a summary — but see [P387] for what it cost to find
that a correctly-written in-place marker was scoring as absent.
"""
import os, re, sys, glob, fnmatch, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# verbatim records are exempt: they are what was said at the time
SKIP_DIRS = ('github', 'transcripts', 'bak', '.git')
SKIP_FILES = re.compile(r'(-this-session-|cycles\.txt|compactions\.txt)')
CITE = re.compile(r'\[P(\d+)\]|\(LEDGER\.md#p(\d+)\)|Postscript \[?(\d+)\]?')
# The tag is OPTIONAL and its contents are arbitrary.  `[A-Z ]+` matched 200 of 383 headings:
# every untagged early entry (`## Postscript 16:`) and every parenthesised or mixed-case tag
# (`## [OBSERVED (SUPERSEDED by P192)] Postscript 189:`) was invisible -- so P189's own
# SUPERSEDED marker was attributed to P188, the last heading the regex could see.
HEAD = re.compile(r'^##\s*(?:\[([^\]\n]+)\]\s*)?Postscript (\d+)(?:\s*\(([^)\n]*)\))?:([^\n]*)',
                  re.M)
# The one heading form that ENCODES ROLE, so it may assert rather than suspect:
#     ## Postscript 76 (CORRECTION to Postscript 70): ...
# Three entries use it (P61, P66, P76).  Before 2026-09-24 the regex required the colon straight
# after the number, so all three were invisible, their bodies were attributed to the entry before
# them, and P60, P63 and P70 were never known to have been corrected.
ROLE_PAREN = re.compile(r'CORRECTION to Postscript (\d+)', re.I)
MARK = re.compile(r'(CORRECTED|REFUTED|WITHDRAWN|RETRACTED|superseded|Scope note|'
                  r'DOES NOT EXIST|is FALSE|was wrong)', re.I)
# VOID is a term of art here, distinct from both of the above: REFUTED means a VALID measurement
# shows the claim false; CORRECTED means a replacement value exists; VOID means the claim was
# never validly measured -- broken instrument, so the number says nothing either way (35 uses in
# the documents, e.g. "r = 0.562 ... VOID -- broken normals").  CASE-SENSITIVE on purpose: the
# lowercase word is ordinary prose ("a restatement of mine was void"), and matching it would
# mark neighbouring citations as handled when nothing handled them.
VOIDMARK = re.compile(r'\b(VOID|WRONG|PROOF GAP)\b')
# PROOF GAP joined 2026-09-24: a claim stated as proved whose proof has a hole -- distinct from
# VOID (never validly measured) and REFUTED (shown false).  First case: [P249]'s 953.
# WRONG joined 2026-09-24: 47 uses, all verdicts ('"isolated in both senses"  WRONG -- ...').
# CLOSED was considered and NOT added: it mostly means an open QUESTION was answered, sometimes
# in agreement with the claim beside it, so it does not reliably mean 'this fell'.

# The heading TAG is an ACTION tag and its direction is NOT reliable: [REFUTED] Postscript 323
# means 323 refutes 304, while [CORRECTED] Postscript 329 means 329 WAS corrected.  Reading the
# tag as a status is what the first version of this tool did, and it inverted 13 of 18 rows --
# it would have stamped REFUTED markers on the dependents of current results ([P330], [P374],
# [P378], [P383]).  Two STRUCTURAL signals are used instead, neither of which depends on the
# tag's direction:
#
#   (B) MARKED   -- the entry's body carries a `> **CORRECTED/REFUTED/...` blockquote, the
#                   in-place marker required by "documents are living, their data is not".
#                   This one ASSERTS: the marker sits in the victim's own entry and says so.
#   (A) SUSPECT  -- a [Pnnn] named in the heading line of a refutation-family entry.  This one
#                   only SUSPECTS, because a heading title does not carry grammatical role:
#
#       [REFUTED]  Postscript 323: [P304]'s mechanism does not survive ...   P304 IS the victim
#       [CORRECTION] Postscript 363: ... it was the believed max(5), and [P16] beat it
#                                                                        P16 is the WINNER
#       [SUPERSEDED IN PART] Postscript 271: ... corrected to ... by [P272](#p272)
#                                                                        P272 is the CORRECTOR
#
# Same sentence shape, three different roles.  Asserting from (A) produced false FALLEN rows for
# [P16] and [P272], which is the THIRD time this tool has been wrong about direction: the prose
# loop was inverted by passive voice ("was refuted by [P330]" marked the refuter), the selector
# read the ACTION tag as a status, and now the victim rule reads a name as a role.  The lesson
# taken is not a fourth patch on the parse.  It is that only (B) is unambiguous, so (A) is
# reported SEPARATELY and as a question.  The durable fix for a genuine fall is to write the
# in-place marker into the victim's own entry, which moves it from SUSPECT to FALLEN.
REFUT_FAMILY = {'REFUTATION', 'CORRECTION', 'REFUTED', 'CORRECTED', 'PARTLY REFUTED',
                'REFUTED IN PART', 'PARTLY RETRACTED', 'SUPERSEDED IN PART', 'REVERSED',
                'EVIDENCE OVERSTATED', 'FAILED DERIVATION'}
# SUSPECTS RESOLVED BY HAND AS NOT FALLEN.  A verdict belongs in the record, or the next reader
# re-derives it -- and after a compaction the next reader is starting cold.  Each entry says what
# role the name actually plays in the heading that named it.
RESOLVED_NOT_FALLEN = {
    '16':  'P363 names it as the WINNER ("the believed max(5), and [P16] beat it")',
    '272': 'P271 names it as the CORRECTOR ("corrected ... by [P272]")',
}
# The structured status tag (DOCUMENTS.md, adopted 2026-09-24).  Role is STATED, not inferred:
#     <!-- status: corrected-by=P383; fell="n = 8 figure is 2"; stands="n = 6, 7 values" -->
#     <!-- status: corrects=P307 -->
STATUS = re.compile(r'^<!--\s*status:\s*(.*?)-->', re.S | re.M)
# ^ ON ITS OWN LINE ONLY.  [P388]'s prose quotes the convention inline, `<!-- status: ...;
# fell="..." -->`, and an unanchored pattern read that example as a real tag: every "..." in every
# document then "matched" (77 spurious --fell hits, found by the retrofit that first ran it).
FELLSTR = re.compile(r'fell\s*=\s*((?:"[^"]*"\s*\|?\s*)+)')
# HYPOTHESIS TAGS ([P395]).  A result proved only under a hypothesis carries
#     <!-- status: proved-if="trivial holes"|"c = 1"; claim="195 - Q4"|"195 − Q4" -->
# proved-if: phrases, any ONE of which shows a sentence has kept the condition;
# claim:     distinctive strings of the conclusion, searched for directly.
# The claim strings are the point.  The failure that motivated this, [P395], was a summary line
# stating P348's bound as proved under the wrong condition while citing P374 and P237 -- not P348.
# A citation graph cannot see a restatement that cites something else.
PROVIFSTR = re.compile(r'proved-if\s*=\s*((?:"[^"]*"\s*\|?\s*)+)')
CLAIMSTR = re.compile(r'claim\s*=\s*((?:"[^"]*"\s*\|?\s*)+)')
# "proved" as a claim of proof: not "unproved", not "PROVED IF"/"proved if" (which keeps a
# condition by construction), not "proved implication".
PROVED = re.compile(r'(?<![A-Za-z])(?<!un)(?<!UN)(proved|proven|theorem)\b(?!\s+(if|implication)\b)', re.I)
REVIEWED = re.compile(r'<!--\s*reviewed\b')
SELFMARK = re.compile(r'^>\s*\*\*(CORRECTED|REFUTED|RETRACTED|WITHDRAWN|SUPERSEDED|REVERSED|VOID)',
                      re.M)


def doc_kinds():
    """(pattern, kind) rows from DOCUMENTS.md's classification table -- the single source of
    truth for what each document PROMISES, which decides how the audit treats a citation in it:
    current  -> must be rewritten when a cited postscript falls (counted, listed first)
    record   -> gets a pointer only where a reader could act on the dead claim (counted)
    narrative-> written for people, never marked for a tool: passages are LISTED as a reading
                list and never counted (DOCUMENTS.md)
    verbatim -> never corrected, never scanned"""
    rows = []
    try:
        for l in open(os.path.join(ROOT, 'DOCUMENTS.md'), encoding='utf-8'):
            m = re.match(r'^\| `([^`]+)` \| (record|verbatim|current|narrative) \|', l)
            if m:
                rows.append((m.group(1), m.group(2)))
    except OSError:
        pass
    return rows


KINDS = None


def kind_of(fname):
    global KINDS
    if KINDS is None:
        KINDS = doc_kinds()
    for pat, k in KINDS:
        if fnmatch.fnmatch(fname, pat):
            return k
    return 'unclassified'


def docs():
    out = []
    for f in glob.glob(os.path.join(ROOT, '*.md')):
        if SKIP_FILES.search(os.path.basename(f)) or kind_of(os.path.basename(f)) == 'verbatim':
            continue
        out.append(f)
    return sorted(out)


FELL = {}          # postscript -> distinctive strings of what fell, from its status tag
HYP = {}           # postscript -> (condition phrases, claim strings), from its status tag
CLAIM_ONLY = set() # postscripts whose tag says trigger="claim": search the claim strings only


def status_of_postscripts():
    """postscript number -> (tag, fallen, why).  See REFUT_FAMILY above for why the tag alone
    is not the status."""
    s = open(os.path.join(ROOT, 'LEDGER.md'), encoding='utf-8', errors='ignore').read()
    FELL.clear()                                 # module-level; re-parsing must not accumulate
    HYP.clear()
    CLAIM_ONLY.clear()
    heads = list(HEAD.finditer(s))
    tag, fallen, suspect, span = {}, {}, {}, {}
    for i, m in enumerate(heads):
        n, t, paren, title = m.group(2), (m.group(1) or '').strip(), m.group(3) or '', m.group(4)
        rp = ROLE_PAREN.search(paren)
        if rp and rp.group(1) != n:
            fallen.setdefault(rp.group(1), []).append('corrected by P%s (heading states it)' % n)
        tag[n] = t
        nxt = heads[i + 1].start() if i + 1 < len(heads) else len(s)
        span[n] = (s.count('\n', 0, m.start()) + 1, s.count('\n', 0, nxt) + 1)
        # (A) victims named in a refutation-family heading
        if t in REFUT_FAMILY:
            for v in re.findall(r'\[P(\d+)\]', title):
                if v != n:
                    suspect.setdefault(v, []).append('named by P%s [%s]' % (n, t))
        # (B) an in-place marker at the top of this entry's own body
        end = heads[i + 1].start() if i + 1 < len(heads) else len(s)
        body = s[m.end():end]
        # the whole body, not just its head: a PARTIAL retraction belongs beside the
        # claim it retracts, and [P375]'s sat 37 lines in -- invisible to a head-only window.
        sm = SELFMARK.search(body)
        if sm:
            fallen.setdefault(n, []).append('in-place marker: %s' % sm.group(1))
        for st in STATUS.findall(body):          # NOT 'tag': that name is the dict above
            for v in re.findall(r'corrected-by\s*=\s*P(\d+)', st):
                fallen.setdefault(n, []).append('status tag: corrected-by P%s' % v)
            if re.search(r'corrected-by\s*=\s*self\b', st):     # refuted inside its own entry
                fallen.setdefault(n, []).append('status tag: corrected within itself')
            for v in re.findall(r'corrects\s*=\s*P(\d+)', st):
                if v != n:
                    fallen.setdefault(v, []).append('status tag on P%s: corrects it' % n)
            fm = FELLSTR.search(st)
            if fm:
                FELL.setdefault(n, []).extend(re.findall(r'"([^"]+)"', fm.group(1)))
            pm, cm = PROVIFSTR.search(st), CLAIMSTR.search(st)
            if pm:
                if re.search(r'trigger\s*=\s*"claim"', st):
                    CLAIM_ONLY.add(n)          # the entry's other results stand: citations are not restatements
                conds, claims = HYP.setdefault(n, ([], []))
                conds.extend(re.findall(r'"([^"]+)"', pm.group(1)))
                if cm:
                    claims.extend(re.findall(r'"([^"]+)"', cm.group(1)))
    return tag, fallen, suspect, span


# A CASUALTY TABLE is one paragraph giving a DIFFERENT verdict to each postscript in it:
#
#     VOID     [P304]'s "coincidence walls are steps ..."
#     SAFE     ... [P307]'s plateau dimensions ... stand
#
# Tested as a paragraph, the VOID in one row marked the SAFE row's [P307] as handled -- and P307
# had fallen, for an unrelated reason, the same week.  So each row is its own unit, and a row is
# flagged by ITS OWN verdict: VOID and SUSPECT warn the reader, SAFE and UNAFFECTED assert the
# opposite and count as flagged only if a marker was written into the row itself.
ROW = re.compile(r'^    (VOID|SUSPECT|SAFE|UNAFFECTED)\s')
WARN_VERDICTS = ('VOID', 'SUSPECT')


def units(para, line0, near):
    """split a paragraph into (first_line, text, flagged) units -- rows of a casualty table
    individually, everything else together under the paragraph-neighbour rule."""
    lines = para.split('\n')
    if not any(ROW.match(l) for l in lines):
        return [(line0, para, near)]
    rest, rows, cur = [], [], None
    for k, l in enumerate(lines):
        m = ROW.match(l)
        if m:
            cur = [line0 + k, [l], m.group(1)]
            rows.append(cur)
        elif cur is not None and l.startswith('     '):
            cur[1].append(l)                     # continuation of the current row
        else:
            cur = None
            rest.append((line0 + k, l))
    out = []
    if rest:
        out.append((rest[0][0], '\n'.join(l for _, l in rest), near))
    for ln, ls, verdict in rows:
        t = '\n'.join(ls)
        flagged = (verdict in WARN_VERDICTS or bool(MARK.search(t)) or bool(VOIDMARK.search(t))
                   or bool(REVIEWED.search(t)))
        out.append((ln, t, flagged))
    return out


def graph(entry_span=None):
    """citations: postscript -> [(file, line, paragraph, flagged)]

    TWO THINGS THE FIRST VERSION GOT WRONG, both found by the probe in [P387]: writing an
    in-place marker under [P304]'s heading did not clear [P304]'s own heading from the audit.

    (1) SELF-REFERENCE IS NOT DEPENDENCY.  A `[Pnnn]` inside Pnnn's OWN ledger entry is the
        entry talking about itself.  It cannot be a stale dependent, and counting it means the
        audit can never reach zero.  Dropped.
    (2) THE FLAG WINDOW IS THE PARAGRAPH PLUS ITS NEIGHBOURS.  An in-place marker is a separate
        blockquote paragraph directly under the heading it marks -- which is how the convention
        requires it to be written -- so a strictly paragraph-local test scores the thing it was
        built to reward as unflagged.
    """
    g = collections.defaultdict(list)
    for f in docs():
        text = open(f, encoding='utf-8', errors='ignore').read()
        paras = text.split('\n\n')
        marks = [bool(MARK.search(p) or VOIDMARK.search(p) or REVIEWED.search(p)) for p in paras]
        off = 0
        for i, para in enumerate(paras):
            line = text.count('\n', 0, off) + 1
            near = any(marks[max(0, i - 1):i + 2])
            for uline, utext, uflag in units(para, line, near):
                for m in CITE.finditer(utext):
                    n = m.group(1) or m.group(2) or m.group(3)
                    if entry_span and os.path.basename(f) == 'LEDGER.md':
                        lo, hi = entry_span.get(n, (0, 0))
                        if lo <= uline <= hi:
                            continue             # the entry citing itself
                    g[n].append((os.path.basename(f), uline, utext.strip()[:150], uflag))
            off += len(para) + 2
    return g


def hyp_paragraph(para, n, conds, claims):
    """why this paragraph states P<n>'s conditional result as proved without its condition, or
    None.  Triggered by a claim string OR a citation; needs a claim of proof; cleared by any one
    condition phrase or a reviewed comment.  Tuned to over-report, like the rest of this tool."""
    cite = None if n in CLAIM_ONLY else re.search(r'\[P%s\]|#p%s\)' % (n, n), para)
    hit = next((c for c in claims if c in para), None)
    # a claim of proof NOT preceded, within a few words, by a negation: "NOT yet a theorem",
    # "was never proved" and "not this theorem's to give" are the opposite claim, and were 5 of
    # the first run's 14 hits
    asserted = [m for m in PROVED.finditer(para)
                if not re.search(r'\b(not|never|nor|no longer)\b[^.;:]{0,20}$', para[max(0, m.start() - 30):m.start()], re.I)]
    if not (cite or hit) or not asserted or REVIEWED.search(para):
        return None
    low = para.lower()
    if any(c.lower() in low for c in conds):
        return None
    return ('states "%s"' % hit) if hit else 'cites it'


def hyp_hits(span, only=None):
    """(kind, file, line, n, why) for every paragraph that states a conditional result as proved
    and names none of its conditions.  `only` = [(name, text)] replaces the documents (gates)."""
    out = []
    sources = only or [(os.path.basename(f), open(f, encoding='utf-8', errors='ignore').read())
                       for f in docs()]
    for b, text in sources:
        k = kind_of(b)
        paras = text.split('\n\n')
        off = 0
        for para in paras:
            line = text.count('\n', 0, off) + 1
            off += len(para) + 2
            for n, (conds, claims) in HYP.items():
                if b == 'LEDGER.md' and n in span and span[n][0] <= line < span[n][1]:
                    continue                     # the entry's own statement of itself
                why = hyp_paragraph(para, n, conds, claims)
                if why:
                    out.append((k, b, line, n, why))
    return out


def main():
    a = sys.argv[1:]
    tag, fallen, suspect, span = status_of_postscripts()
    g = graph(span)
    if not a or a[0] in ('-h', '--help'):
        print(__doc__)
        return
    if a[0] == '--stats':
        tot = sum(len(v) for v in g.values())
        print('authored documents      %d' % len(docs()))
        print('postscripts cited       %d' % len(g))
        print('citation edges          %d' % tot)
        deg = sorted(((len(v), k) for k, v in g.items()), reverse=True)[:8]
        print('most-depended-upon:')
        for n, k in deg:
            print('   P%-5s %3d dependents   [%s]%s'
                  % (k, n, tag.get(k, 'no status'),
                     '   FALLEN' if k in fallen else '   SUSPECT' if k in suspect else ''))
        return
    if a[0] == '--audit':
        def rows_for(d):
            out = []
            for n, why in d.items():
                dep = [x for x in g.get(n, []) if kind_of(x[0]) != 'narrative']
                unf = [x for x in dep if not x[3]]
                if unf:
                    out.append((len(unf), int(n), n, why, dep, unf))
            out.sort(reverse=True)
            return out

        def show(rows, detail):
            tc = sum(len(r[4]) for r in rows)
            tu = sum(r[0] for r in rows)
            for cnt, _, n, why, dep, unf in rows:
                print('P%-5s [%s]  %d of %d citations unflagged   <- %s'
                      % (n, tag.get(n, '?'), cnt, len(dep), '; '.join(why)))
                if not detail:
                    continue
                seen = set()
                order = {'current': 0, 'unclassified': 1, 'record': 2}
                for f, ln, ctx, _ in sorted(unf, key=lambda x: (order.get(kind_of(x[0]), 3), x[0], x[1])):
                    if f in seen:
                        continue
                    seen.add(f)
                    print('      %-9s %-22s line %-6d %s' % (kind_of(f), f, ln,
                                                              ctx[:70].replace('\n', ' ')))
            return tu, tc

        fr = rows_for(fallen)
        sr = rows_for({k: v for k, v in suspect.items()
                       if k not in fallen and k not in RESOLVED_NOT_FALLEN})
        print('FALLEN -- the entry carries its own in-place correction marker, so the fall is')
        print('not in doubt.  These dependents need checking.\n')
        tu, tc = show(fr, True)
        print('\n%d fallen postscripts have unflagged dependents' % len(fr))
        print('%d of %d citations to them carry no correction marker (%.0f %%)'
              % (tu, tc, 100.0 * tu / max(tc, 1)))
        print('\n' + '-' * 78)
        print('SUSPECT -- named in the heading of a refutation-family entry, ROLE UNVERIFIED.')
        print('A heading title does not say whether the name is the victim, the corrector or')
        print('the winner, and all three occur.  Resolve BY HAND; if it really fell, write the')
        print('in-place marker into its own entry, which moves it to FALLEN above.\n')
        su, sc = show(sr, False)
        print('\n%d suspect postscripts, %d of %d citations unflagged  -- NOT counted above'
              % (len(sr), su, sc))
        print('%d more resolved by hand as NOT fallen (RESOLVED_NOT_FALLEN in this file)'
              % len(RESOLVED_NOT_FALLEN))
        nar = sorted({(x[0], x[1], n) for n in fallen for x in g.get(n, [])
                      if kind_of(x[0]) == 'narrative'})
        print('\nREADING LIST, not counted: narrative passages citing a fallen postscript. Narratives')
        print('carry no markers; read each to judge whether it names what replaced the old belief.')
        for (f, ln, n) in nar:
            print('      narrative %-22s line %-6d P%s' % (f, ln, n))
        unc = sorted({x[0] for n in fallen for x in g.get(n, []) if kind_of(x[0]) == 'unclassified'})
        if unc:
            print('UNCLASSIFIED documents (add a row to DOCUMENTS.md): %s' % ', '.join(unc))
        return

    if a[0] == '--fell':
        # restatements WITHOUT a citation are invisible to the graph; the strings a status tag
        # records as having fallen are searched for directly (DOCUMENTS.md, 'fell=')
        if not FELL:
            print('no status tag carries fell= strings yet')
            return
        hits = 0
        for f in docs():
            b = os.path.basename(f)
            k = kind_of(b)
            if b == 'LEDGER.md':
                continue
            text = open(f, encoding='utf-8', errors='ignore').read()
            paras = text.split('\n\n')
            marks = [bool(MARK.search(q) or VOIDMARK.search(q) or REVIEWED.search(q)) for q in paras]
            off = 0
            for i, para in enumerate(paras):
                line = text.count('\n', 0, off) + 1
                for n, strs in FELL.items():
                    for st in strs:
                        # OWN paragraph, or a correction BLOCKQUOTE directly after it (the
                        # in-place-note convention).  Not any neighbour: a correction about
                        # something else masked a planted restatement in the gating test.
                        nxt = paras[i + 1] if i + 1 < len(paras) else ''
                        note_after = nxt.lstrip().startswith('>') and bool(
                            MARK.search(nxt) or VOIDMARK.search(nxt))
                        if st in para and (k == 'narrative' or (not marks[i] and not note_after)):
                            hits += (k != 'narrative')
                            print('P%-5s %-9s %-22s line %-6d "%s"' % (n, k, b, line, st))
                off += len(para) + 2
        print('\n%d restatements of fallen claims, excluding narratives (%d postscripts carry fell= '
              'strings); narrative lines above are a reading list, never counted' % (hits, len(FELL)))
        return

    if a[0] == '--hyp':
        hits = 0
        for kind, f, line, n, why in hyp_hits(span):
            hits += (kind != 'narrative')
            print('P%-5s %-9s %-22s line %-6d %s' % (n, kind, f, line, why))
        print('\n%d statements of a conditional result as proved without its condition, excluding '
              'narratives (%d postscripts carry proved-if tags); narrative lines above are a reading '
              'list, never counted' % (hits, len(HYP)))
        return

    key = a[0].lstrip('Pp')
    dep = g.get(key, [])
    print('P%s  [%s]%s   %d citations\n'
          % (key, tag.get(key, 'no status'),
             '   FALLEN: ' + '; '.join(fallen[key]) if key in fallen
             else '   SUSPECT (role unverified): ' + '; '.join(suspect[key]) if key in suspect
             else '', len(dep)))
    for f, ln, ctx, fl in dep:
        print('   %-22s line %-6d %s  %s' % (f, ln, 'FLAGGED' if fl else '       ',
                                             ctx[:88].replace('\n', ' ')))


if __name__ == '__main__':
    main()
