#!/usr/bin/env python3
"""Replace hard-coded absolute paths with paths relative to the script's own
location.  Reversible, verified by the project's gates, and it does not move a
single byte of data.

WHY.  103 .py files hard-code /Users/dmi/cube-compounds, which ties the whole
repository to one machine: a clone elsewhere fails at import, and the engine
paths silently point at nothing.  The producer->output path is this project's
reproducibility record, so it must survive relocation to remain one.

WHAT IT DOES NOT DO.  It does not touch the DATA files or their names, and it
rewrites only string literals -- comments and prose in docstrings keep the
literal path, since those are documentation of where things lived, not code.

VERIFY AFTER RUNNING: dimension_gate.py, qfield_gate.py, eps_gate.py,
isolation_gate.py.  A path rewrite that breaks an engine call shows up there.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OLD = '/Users/dmi/cube-compounds'
SKIP_DIRS = {'bak', 'tmp', '__pycache__', 'github', 'scratchpad',
             'dimension_cache', 'runs', 'census_run1'}
# quoted string literal containing the absolute path
PAT = re.compile(r"(['\"])" + re.escape(OLD) + r"(/[^'\"]*)?\1")


def rewrite(text):
    def sub(m):
        tail = m.group(2)
        return "HERE" if not tail else "HERE + %s%s%s" % (m.group(1), tail, m.group(1))
    return PAT.subn(sub, text)


def ensure_here(text):
    if re.search(r'^HERE\s*=', text, re.M):
        return text, False
    lines = text.split('\n')
    # after the module docstring and the last top-level import
    ins = 0
    for i, l in enumerate(lines[:80]):
        if re.match(r'^(import |from )\S', l):
            ins = i + 1
    if not ins:                      # no imports: after any docstring
        ins = 1 if lines and lines[0].startswith('#!') else 0
    block = ['import os as _os',
             'HERE = _os.path.dirname(_os.path.abspath(__file__))']
    return '\n'.join(lines[:ins] + block + lines[ins:]), True


def main():
    dry = '--apply' not in sys.argv
    changed = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in sorted(files):
            if not f.endswith('.py') or f == os.path.basename(__file__):
                continue
            p = os.path.join(root, f)
            src = open(p).read()
            if OLD not in src:
                continue
            new, n = rewrite(src)
            if not n:
                continue                      # only in comments/prose
            new, added = ensure_here(new)
            try:
                compile(new, p, 'exec')
            except SyntaxError as e:
                print('SKIP (would not compile): %s -- %s' % (os.path.relpath(p, ROOT), e))
                continue
            changed.append((os.path.relpath(p, ROOT), n, added))
            if not dry:
                open(p, 'w').write(new)
    print('%s %d files, %d literal replacements'
          % ('WOULD REWRITE' if dry else 'REWROTE', len(changed),
             sum(c[1] for c in changed)))
    for name, n, added in changed[:12]:
        print('   %-34s %2d literals%s' % (name, n, ', HERE added' if added else ''))
    if len(changed) > 12:
        print('   ... and %d more' % (len(changed) - 12))
    return 0


if __name__ == '__main__':
    sys.exit(main())
