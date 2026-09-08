#!/usr/bin/env python3
"""GENERATED inventory of run data. Writes DATA_INVENTORY.md -- do not hand-edit.

DIVISION OF LABOUR, and why it is this way.  `DATA_MANIFEST.md` is hand-written
and holds JUDGMENT: which files are wrong, superseded, current.  That cannot be
computed.  This holds INVENTORY: what exists, what wrote it, how many records,
whether anything points at it.  That must not be hand-written, because a
hand-maintained list of 84 files is a second document that drifts -- the exact
failure measured on 2026-08-17, where LEDGER.md carried 389 internal
cross-references and 1 link back out to RESULTS.md, and two claims went stale for
two weeks.  Mechanical checks over remembered discipline.

The two halves CHECK EACH OTHER: every file DATA_MANIFEST calls current must
exist and be non-empty, and any file this finds unreferenced is a candidate the
manifest has not judged.

REFERENCE MATCHING IS A HEURISTIC AND SAYS SO.  Many outputs are named by a
format string (`members_%d.json`), so a literal filename search reports them as
orphans when their producer is obvious.  A literal match, then a digit-stripped stem
required to occur inside something ending in `.json`, are tried, and which one hit is recorded, so a
"referenced" verdict can be checked rather than trusted.  A file reported
UNREFERENCED is one that neither test found -- evidence, not proof, of an orphan.
"""
import json, os, re, subprocess, sys, time
import provenance
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
# ERE tail requiring the stem to sit inside a token ending in .json
PATH_TAIL = "[^'\"[:space:]]*[.]json"
OUT = os.path.join(HERE, 'DATA_INVENTORY.md')
# '.claude' is editor/tool configuration, not run data; 'json/' and 'cb/' hold
# older campaign output and are kept, since unlike the skipped dirs they are
# results someone may still need to judge.
SKIP_DIRS = {'__pycache__', 'bak', 'tmp', 'scratchpad', 'dimension_cache',
             'scratch_diagram', '.git', '.claude'}


def data_files():
    out = []
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            # .prov.json files are METADATA about data, not data; counting
            # them would inflate the inventory with its own bookkeeping.
            if f.endswith('.json') and not f.endswith('.prov.json'):
                p = os.path.join(root, f)
                out.append((os.path.relpath(p, HERE), f))
    return sorted(out)


def records(path):
    try:
        d = json.load(open(path))
    except Exception as e:
        return 'unparseable(%s)' % type(e).__name__
    if isinstance(d, list):
        return len(d)
    if isinstance(d, dict):
        return len(d)
    return 1


def grep_files(needle, exts, as_path=False):
    """files of the given extensions containing the needle.

    as_path=True requires the needle to appear INSIDE SOMETHING ENDING IN .json,
    which is what makes a stem match mean anything.  Without it, the stem "p2"
    matched 127 files -- it is a variable name, not a filename reference -- and
    the orphan count fell from 45 to 2 because the check had stopped being able
    to fail, not because the files had become reachable (FAILURE_MODES 2).
    """
    try:
        if as_path:
            args = ['grep', '-rlE', re.escape(needle) + PATH_TAIL,
                    '--include=*' + exts[0]]
        else:
            args = ['grep', '-rlF', needle, '--include=*' + exts[0]]
        for e in exts[1:]:
            args.append('--include=*' + e)
        args.append(HERE)
        r = subprocess.run(args, capture_output=True, text=True, timeout=120)
        # THIS FILE'S OWN COMMENTS MENTION EXAMPLE FILENAMES.  Excluding self here
        # rather than after the fallback decision: filtering later let a self-hit
        # suppress the prefix search and then vanish, so `members_3.json` was
        # reported an orphan while census_members.py plainly writes it.
        return [os.path.relpath(x, HERE) for x in r.stdout.split('\n')
                if x.strip() and not x.endswith(('data_inventory.py',
                                                 'DATA_INVENTORY.md'))]
    except Exception:
        return []


# Directories that are ONE CAMPAIGN'S SHARDS, not distinct datasets.  204 of the
# 334 data files are per-cell results from a single n=4 climb, ~251 bytes each;
# listing them individually buries the ~90 root files that actually carry
# distinct results.  They are summarised as a group and reference-checked as a
# group -- the campaign is the unit of provenance, not the shard.
GROUP_DIRS = ('n4_run_011b219ec3', 'multicube_out', 'multicube2_out',
              'scratch_diagram', 'github')


def summarise_group(d, rows):
    tot = sum(1 for r in rows if r[0].startswith(d + '/'))
    recs = sum(r[1] for r in rows if r[0].startswith(d + '/') and isinstance(r[1], int))
    return tot, recs


def main():
    files = data_files()
    rows, unref = [], []
    for rel, base in files:
        # Outputs are usually named by a FORMAT STRING (members_%s%d.json), so a
        # literal search finds nothing and the producer is still obvious.  Try
        # progressively weaker stems and RECORD WHICH ONE HIT, so a "referenced"
        # verdict can be checked rather than trusted: a first-token match is much
        # weaker evidence than a literal one.
        stems = [re.sub(r'[_-]?\d+\.json$', '', base),        # members_3.json -> members
                 re.sub(r'[_-]?[a-z]?\d+\.json$', '', base)]  # members_t3.json -> members
        py, md, how = grep_files(base, ['.py']), grep_files(base, ['.md']), 'none'
        if py:
            how = 'literal'
        else:
            seen = set()
            for st in stems:
                if not st or st in seen or len(st) < 4:
                    continue          # a stem under 4 chars is a token, not a name
                seen.add(st)
                py = grep_files(st, ['.py'], as_path=True)
                if py:
                    how = 'stem "%s" in a .json path' % st
                    break
        # A PROVENANCE STAMP BEATS THE GREP HEURISTIC and is preferred whenever
        # present: it is the data describing itself, not the source being
        # interrogated about the data.  The grep tiers remain for files that
        # predate stamping.
        prov = provenance.read(os.path.join(HERE, rel))
        if prov:
            ok, _msg = provenance.verify(os.path.join(HERE, rel))
            how = 'STAMPED%s' % ('' if ok else
                                 (' (retroactive)' if prov.get('retroactive')
                                  else ' (script changed)'))
            py = [prov.get('rerun') or prov.get('script') or '?']
        n = records(os.path.join(HERE, rel))
        mtime = time.strftime('%Y-%m-%d', time.localtime(
            os.path.getmtime(os.path.join(HERE, rel))))
        rows.append((rel, n, mtime, py[:2], md[:2], how))
        if not py and not md:
            unref.append(rel)

    man = ''
    mp = os.path.join(HERE, 'DATA_MANIFEST.md')
    if os.path.exists(mp):
        man = open(mp).read()
    named = set(re.findall(r'`([A-Za-z0-9_/*]+\.json)`', man))
    missing = [f for f in named if '*' not in f
               and not os.path.exists(os.path.join(HERE, f))]
    unjudged = [r[0] for r in rows if os.path.basename(r[0]) not in
                {os.path.basename(x) for x in named}]

    L = []
    L.append('# Data inventory (GENERATED by `data_inventory.py` — do not hand-edit)')
    L.append('')
    L.append('Generated %s. Judgment about which files are wrong, superseded or '
             'current lives in [DATA_MANIFEST.md](DATA_MANIFEST.md); this file '
             'only records what exists and what points at it.' % time.strftime('%Y-%m-%d %H:%M'))
    L.append('')
    L.append('- **%d data files** across the tree (scratch and cache dirs excluded)'
             % len(rows))
    stamped = sum(1 for r in rows if str(r[5]).startswith('STAMPED'))
    L.append('- **%d carry a provenance stamp** (`<file>.prov.json`, written by '
             '`provenance.py`) — these say how to rerun themselves' % stamped)
    L.append('- **%d referenced by no .py and no .md** — orphan candidates, listed below'
             % len(unref))
    L.append('- **%d named in DATA_MANIFEST.md**, of which %d are missing from disk'
             % (len(named), len(missing)))
    L.append('- **%d not judged by DATA_MANIFEST.md** — unaudited, which is not the '
             'same as correct' % len(unjudged))
    L.append('')
    if missing:
        L.append('## MANIFEST ERROR: named but absent from disk')
        L.append('')
        for f in sorted(missing):
            L.append('- `%s`' % f)
        L.append('')
    L.append('## Unreferenced (no .py and no .md points at them)')
    L.append('')
    L.append('Neither a literal filename search nor a digit-stripped prefix search '
             'found a reference. Evidence of an orphan, not proof.')
    L.append('')
    shown = [f for f in sorted(unref)
             if not any(f.startswith(g + '/') for g in GROUP_DIRS)]
    hidden = len(unref) - len(shown)
    for f in shown:
        L.append('- `%s`' % f)
    if hidden:
        L.append('- *(%d further unreferenced files inside grouped campaign '
                 'directories, summarised above)*' % hidden)
    L.append('')
    L.append('## Campaign directories (grouped — one campaign, many shards)')
    L.append('')
    L.append('Shards of a single run are summarised rather than listed: the '
             'campaign is the unit of provenance, not the shard.')
    L.append('')
    L.append('| directory | files | total records |')
    L.append('|---|---|---|')
    for gd in GROUP_DIRS:
        t, rc = summarise_group(gd, [(r[0], r[1]) for r in rows])
        if t:
            L.append('| `%s/` | %d | %d |' % (gd, t, rc))
    L.append('')
    L.append('## All other data files')
    L.append('')
    L.append('| file | records | modified | referenced by | match |')
    L.append('|---|---|---|---|---|')
    for rel, n, mtime, py, md, how in rows:
        if any(rel.startswith(g + '/') for g in GROUP_DIRS):
            continue                      # summarised in the group table above
        refs = ', '.join('`%s`' % x for x in (py + md)[:2]) or '—'
        L.append('| `%s` | %s | %s | %s | %s |' % (rel, n, mtime, refs, how))
    open(OUT, 'w').write('\n'.join(L) + '\n')
    print('wrote DATA_INVENTORY.md: %d files, %d unreferenced, %d unjudged, '
          '%d manifest errors' % (len(rows), len(unref), len(unjudged), len(missing)))
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
