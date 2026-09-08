#!/usr/bin/env python3
"""Chamber enumeration that STREAMS to disk — removes the memory ceiling.

Postscript 144: the 727 campaign does not fail on time, it fails on MEMORY.
Incremental construction holds every sign vector in RAM as it grows, and measured
cost is 272 bytes per chamber at 27 walls:

    14M chambers ->  3.5 GB   (7.1 GB at a stage transition, both lists alive)
    36M chambers ->  9.1 GB  (18.2 GB at a stage transition)

against 16 GB on this machine. The run was doomed at launch and died twice around
stage 19-20. The Zaslavsky bound alone needs 18.05 GB, so it could never fit here.

FIX: never hold a whole stage. Read stage k from a file one line at a time, write
stage k+1 as it is produced, then swap. Peak memory becomes the read buffer plus
one output buffer -- a few megabytes regardless of chamber count. The cost is disk
I/O and the space for two stage files; at 36M chambers a stage file is about 1 GB
as text, which the disk has and the RAM does not.

RESTARTABLE the same way as `arrangement.run_parallel`: a completed stage file is
final, so a relaunch resumes at the first stage whose file is missing. Nothing is
recomputed.

NOT A REPLACEMENT for `arrangement.py` -- that stays the in-memory version, which
is faster when a problem fits (183: 1 712 chambers in 1.6 s). Use this when it does
not.
"""
import json, os, sys, time
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0, HERE)
from isolation67 import _fm


# ENCODING: a sign vector is a string of '+'/'-', one character per wall, and the
# EMPTY vector (the whole space, stage 0) is the sentinel '.'.  The first attempt
# wrote comma-separated integers and let the empty vector be an empty line -- which
# the reader then skipped as blank, so stage 0 yielded nothing and every stage
# after it was empty.  It returned 0 chambers for a case whose answer is 1 712.
# Caught by the known-answer check; it would have been invisible otherwise.
# The encoding is also 3x smaller: 28 bytes per chamber at 27 walls, not ~80.
EMPTY = '.'


def _sv_encode(sv):
    return EMPTY if not sv else ''.join('+' if x > 0 else '-' for x in sv)


def _sv_read(path):
    """yield sign vectors from a stage file, one at a time -- never a whole list"""
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue                      # a genuinely blank line is padding
            if line == EMPTY:
                yield ()
            else:
                yield tuple(1 if c == '+' else -1 for c in line)


def stream_chambers(walls, ncols, workdir, log=sys.stdout, time_budget=None):
    """Chamber count of the central arrangement, streaming stages through disk.

    Returns (count, stage_files). Memory stays flat in the chamber count.
    """
    os.makedirs(workdir, exist_ok=True)
    m = len(walls)
    t0 = time.time()

    stage0 = os.path.join(workdir, 'stage_00.txt')
    if not os.path.exists(stage0):
        with open(stage0, 'w') as fh:
            fh.write(EMPTY + '\n')             # the whole space: the empty sign vector
    prev, count = stage0, 1

    for i in range(m):
        cur = os.path.join(workdir, 'stage_%02d.txt' % (i + 1))
        if os.path.exists(cur):                # RESUME: a finished stage file is final
            count = sum(1 for _ in open(cur) if _.strip() or True) - 0
            with open(cur) as fh:
                count = sum(1 for _ in fh)
            print('   stage %2d/%d: already on disk, %s chambers -- skipped'
                  % (i + 1, m, '{:,}'.format(count)), file=log, flush=True)
            prev = cur
            continue
        w = walls[i]
        tmp = cur + '.partial'
        n_out = 0
        with open(tmp, 'w') as out:
            for sv in _sv_read(prev):
                rows = [[s * walls[j][t] for t in range(ncols)]
                        for j, s in enumerate(sv)]
                if _fm(rows + [[w[t] for t in range(ncols)]], ncols) is not None:
                    out.write(_sv_encode(sv + (1,)) + '\n'); n_out += 1
                if _fm(rows + [[-w[t] for t in range(ncols)]], ncols) is not None:
                    out.write(_sv_encode(sv + (-1,)) + '\n'); n_out += 1
        os.replace(tmp, cur)                   # atomic: a stage file appears only when complete
        count = n_out; prev = cur
        el = time.time() - t0
        print('   stage %2d/%d: %9s chambers  (%.0fs)'
              % (i + 1, m, '{:,}'.format(count), el), file=log, flush=True)
        if time_budget and el > time_budget:
            print('   TIME BUDGET reached after stage %d of %d' % (i + 1, m),
                  file=log, flush=True)
            return count, i + 1
    return count, m


if __name__ == '__main__':
    from growth727 import walls_of, BASE
    which = sys.argv[1] if len(sys.argv) > 1 else '393'
    cfg = BASE if which == '393' else BASE + [(7, 14, 1, -5)]
    W, nc = walls_of(cfg)
    print('%s: %d walls, ambient %d -- streaming' % (which, len(W), nc), flush=True)
    n, done = stream_chambers(W, nc, os.path.join(HERE, 'stream_' + which),
                              time_budget=float(sys.argv[2]) if len(sys.argv) > 2 else None)
    print('%s: %s chambers after %d stages' % (which, '{:,}'.format(n), done), flush=True)
