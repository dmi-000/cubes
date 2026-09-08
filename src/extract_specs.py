#!/usr/bin/env python3
"""Recover delegation specifications from session transcripts into `specs/backfill/`.

WHY.  65 agents were delegated to on this project and 8 were written up in
`DELEGATION_LOG.md`.  The specifications for the rest existed only as tool
parameters in session transcripts -- see FAILURE_MODES 19.  They are recoverable,
contrary to what DELEGATION_LOG.md claimed until 2026-08-20, because each agent's
own transcript carries the full prompt as its first user message and the parent
session carries it as the `Agent` tool-use input.

RETROACTIVE, AND SAID SO IN EVERY FILE.  A spec written BEFORE the work is a
contract: the code can be diffed against it.  A spec recovered AFTER is only a
record of what was asked -- it cannot certify that the delivered code satisfies
it, because nobody checked at the time.  This is the same distinction
`provenance.py` draws with `retroactive=True`, and for the same reason: a stamp
taken after the fact manufactures assurance it does not have.  Every file this
writes carries the marker in its header, and they go in `specs/backfill/` rather
than `specs/` so the two kinds can never be confused by a reader who sees only a
path.

WHAT IS SELECTED.  Not all 65.  The criterion is the one the project already
applies to agent reports: a spec is worth keeping when its output is CITED.  A
delegation is selected if any file it names both exists in the repository and is
mentioned in LEDGER.md or RESULTS.md.  Everything else is listed in the manifest
with the reason it was skipped, so "not recovered" never reads as "did not exist".

IDEMPOTENT.  Re-running overwrites the same paths with the same content; the
slug is derived from the timestamp and the tool-use id, both immutable.
"""
import json, os, re, sys, glob, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SESSIONS = os.path.expanduser('~/.claude/projects/-Users-dmi-cube-compounds')
OUT = os.path.join(HERE, 'specs', 'backfill')


def spawns():
    """Every Agent delegation found in every session transcript, oldest first."""
    out = []
    for path in sorted(glob.glob(os.path.join(SESSIONS, '*.jsonl'))):
        session = os.path.basename(path)[:-6]
        for line in open(path):
            try:
                rec = json.loads(line)
            except Exception:
                continue
            msg = rec.get('message') or {}
            content = msg.get('content')
            if not isinstance(content, list):
                continue
            for blk in content:
                if not (isinstance(blk, dict) and blk.get('type') == 'tool_use'
                        and blk.get('name') == 'Agent'):
                    continue
                inp = blk.get('input') or {}
                out.append({
                    'session': session,
                    'id': blk.get('id') or '',
                    'ts': (rec.get('timestamp') or '')[:19],
                    'description': inp.get('description') or '(no description)',
                    'subagent_type': inp.get('subagent_type') or '',
                    'model': inp.get('model') or '',
                    'prompt': inp.get('prompt') or '',
                })
    out.sort(key=lambda r: (r['ts'], r['id']))
    return out


def named_files(prompt):
    """Repository files the prompt names.  Deliberately narrow: bare basenames
    with a source or document extension.  A prompt that names no file produced
    nothing citable and is not a candidate."""
    return sorted(set(re.findall(r'\b([a-z_0-9]+\.(?:py|md|cpp|json))\b', prompt)))


def slug(rec):
    base = re.sub(r'[^a-z0-9]+', '-', rec['description'].lower()).strip('-')[:52]
    stamp = rec['ts'].replace(':', '').replace('-', '').replace('T', '-')[:13]
    return '%s-%s' % (stamp or 'undated', base or 'delegation')


def main():
    cited_text = ''
    for doc in ('LEDGER.md', 'RESULTS.md'):
        p = os.path.join(HERE, doc)
        if os.path.exists(p):
            cited_text += open(p).read()
    present = set(os.listdir(HERE))

    recs = spawns()
    selected, skipped = [], []
    for r in recs:
        files = named_files(r['prompt'])
        r['files'] = files
        r['exists'] = [f for f in files if f in present]
        r['cited'] = [f for f in r['exists'] if f in cited_text]
        if r['cited']:
            selected.append(r)
        else:
            skipped.append(r)

    os.makedirs(OUT, exist_ok=True)
    for r in selected:
        name = slug(r) + '.md'
        body = [
            '# %s' % r['description'],
            '',
            '> **RETROACTIVE SPECIFICATION — recovered, not contemporaneous.**',
            '> This is the prompt as it was sent, extracted from the session',
            '> transcript by `extract_specs.py` on demand. It records what was',
            '> ASKED. It does not certify that the delivered code satisfies it:',
            '> no diff against this text was performed at the time, because this',
            '> text was not on disk at the time. See',
            '> [FAILURE_MODES 19](../../FAILURE_MODES.md#19-the-specification-is-the-one-artifact-not-kept).',
            '',
            '| | |',
            '|---|---|',
            '| Delegated | %s |' % (r['ts'] or 'unknown'),
            '| Agent type | %s |' % (r['subagent_type'] or 'default'),
            '| Model override | %s |' % (r['model'] or 'inherited'),
            '| Session | `%s` |' % r['session'],
            '| Tool-use id | `%s` |' % r['id'],
            '| Files named | %s |' % (', '.join('`%s`' % f for f in r['files']) or 'none'),
            '| Present in repo | %s |' % (', '.join('`%s`' % f for f in r['exists']) or 'none'),
            '| Cited in LEDGER/RESULTS | %s |' % ', '.join('`%s`' % f for f in r['cited']),
            '',
            '## Prompt as sent',
            '',
            '```text',
            r['prompt'].replace('```', "'''"),
            '```',
            '',
        ]
        with open(os.path.join(OUT, name), 'w') as fh:
            fh.write('\n'.join(body))

    man = [
        '# Backfilled delegation specifications — manifest',
        '',
        'Generated by `extract_specs.py`. **Every file in this directory is',
        'RETROACTIVE**: recovered from a transcript after the work was done, so it',
        'records what was asked and certifies nothing about what was delivered.',
        'Specs written before the work live in `specs/`, one level up.',
        '',
        '**%d delegations found across all sessions. %d recovered here, %d not.**' % (
            len(recs), len(selected), len(skipped)),
        '',
        'Selection criterion, the same one already applied to agent reports: a spec',
        'is kept when a file it names both exists in the repository and is cited in',
        '`LEDGER.md` or `RESULTS.md`. The rest are listed below with the reason, so',
        'that "not recovered" is never read as "did not exist" —',
        '[unevaluable is not a negative result].',
        '',
        '## Recovered (%d)' % len(selected),
        '',
        '| Date | Delegation | Cited output |',
        '|---|---|---|',
    ]
    for r in selected:
        man.append('| %s | [%s](%s.md) | %s |' % (
            r['ts'][:10], r['description'], slug(r),
            ', '.join('`%s`' % f for f in r['cited'][:3])))
    man += ['', '## Not recovered (%d)' % len(skipped), '',
            '| Date | Delegation | Reason |', '|---|---|---|']
    for r in skipped:
        if not r['files']:
            why = 'names no repository file'
        elif not r['exists']:
            why = 'named files absent: %s' % ', '.join('`%s`' % f for f in r['files'][:3])
        else:
            why = 'output present but uncited: %s' % ', '.join('`%s`' % f for f in r['exists'][:3])
        man.append('| %s | %s | %s |' % (r['ts'][:10], r['description'], why))
    man.append('')
    with open(os.path.join(OUT, 'MANIFEST.md'), 'w') as fh:
        fh.write('\n'.join(man))

    print('%d delegations; %d recovered to %s; %d skipped' % (
        len(recs), len(selected), os.path.relpath(OUT, HERE), len(skipped)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
