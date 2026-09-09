#!/usr/bin/env python3
"""Keep resolved filesystem paths out of the records.

A run log or a report that quotes a resolved path carries the account layout of
whatever machine produced it, and the reader gains nothing: `data/x.json` locates
a file in the repository, an absolute path locates it on one host. Records are
the part of this project that travels, so they are the part that has to be clean.

DERIVED, NOT EMBEDDED. The strings to remove are computed from this file's own
location and from the user's home directory at runtime. Nothing to redact is
written down here, so this file is safe to read and safe to publish, and it keeps
working if either location changes.

SCOPE. Authored records: .md, .json, .log, .out, .err, .txt under the repository.

EXEMPT, and deliberately so:
  - verbatim records -- transcripts/, *.bak*, exported session files. They are
    what was actually said at the time and editing them would make them not that.
  - the publish tree. It is not mine to write to; this reports on it only.
  - caches and build outputs, which are regenerated rather than read.

DEFAULT IS A DRY RUN. Pass --apply to write. Every change is a shortening within
one line; no file is reordered, renamed, or moved.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
HOME = os.path.expanduser('~')

EXT = ('.md', '.json', '.log', '.out', '.err', '.txt')
SKIP_DIRS = {'github', 'transcripts', '__pycache__', 'dimension_cache',
             'catalogue_cache', 'scratchpad', 'bak', 'tmp', 'node_modules', '.git'}


def _verbatim(name):
    """A record of what was said, which must not be rewritten."""
    return ('.bak' in name or name.endswith('.orig')
            or 'this-session-is-being-continued' in name
            or name.startswith('20') and name.endswith('.txt') and '-' in name)


def targets(tree=None):
    """Walk the repository, or an explicitly named tree.

    The publish tree is never walked by default and is never written by this
    script on its own: pointing it there is a separate, deliberate act by whoever
    owns that tree (`--tree github --apply`).
    """
    base = tree or ROOT
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames
                       if (d not in SKIP_DIRS or (tree and d != '.git'))
                       and not d.startswith('.')]
        for fn in filenames:
            if (fn.endswith(EXT) or (tree and fn.endswith('.py'))) \
                    and not _verbatim(fn):
                yield os.path.join(dirpath, fn)


def scrub(text):
    """Repository paths become repo-relative; any other home path becomes ~."""
    out = text.replace(ROOT + '/', '').replace(ROOT, '.')
    if HOME != ROOT:
        out = out.replace(HOME + '/', '~/').replace(HOME, '~')
    return out


def main():
    apply = '--apply' in sys.argv
    tree = None
    if '--tree' in sys.argv:
        tree = os.path.abspath(sys.argv[sys.argv.index('--tree') + 1])
    changed, hits, skipped = [], 0, 0
    for f in targets(tree):
        try:
            t = open(f, encoding='utf-8', errors='surrogateescape').read()
        except (OSError, UnicodeError):
            skipped += 1
            continue
        s = scrub(t)
        if s != t:
            n = sum(1 for a, b in zip(t.split('\n'), s.split('\n')) if a != b)
            hits += n
            changed.append((os.path.relpath(f, tree or ROOT), n))
            if apply:
                with open(f, 'w', encoding='utf-8', errors='surrogateescape') as fh:
                    fh.write(s)
    changed.sort(key=lambda x: -x[1])
    print('%s: %d files, %d lines%s'
          % ('rewrote' if apply else 'would rewrite', len(changed), hits,
             '' if not skipped else '  (%d unreadable, skipped)' % skipped))
    for name, n in changed[:25]:
        print('   %5d  %s' % (n, name))
    if len(changed) > 25:
        print('   ... and %d more files' % (len(changed) - 25))
    # report on, never touch, the publish tree
    pub = os.path.join(ROOT, 'github')
    if os.path.isdir(pub) and not tree:
        c = 0
        for dp, dn, fns in os.walk(pub):
            dn[:] = [d for d in dn if d != '.git']
            for fn in fns:
                p = os.path.join(dp, fn)
                try:
                    if ROOT in open(p, encoding='utf-8', errors='ignore').read():
                        c += 1
                except (OSError, UnicodeError):
                    pass
        print('\npublish tree: %d files match. NOT modified -- that tree is not '
              'written by this script.' % c)
    if not apply:
        print('\ndry run. --apply to write.')


if __name__ == '__main__':
    main()
