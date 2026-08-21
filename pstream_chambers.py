#!/usr/bin/env python3
"""Parallel streaming chamber enumeration — flat memory, N cores, no queues.

WHY.  `stream_chambers.py` removed the memory ceiling (P146) but is
single-process, so on a 4-core machine three cores idle.  Measured on the live
727 run: stage 15 of 27 reached in 145 s with cost per stage rising ~2.4x, which
extrapolates to days.  The work is embarrassingly parallel — each chamber of
stage k is extended independently — so the only reason it was serial is that the
serial version was written first.

NO QUEUES, DELIBERATELY.  The 393 campaign deadlocked three times in
`multiprocessing.Queue` (P148, P149).  Here workers share nothing: worker w reads
the stage-k file(s) and handles only the lines with `index % N == w`, writing its
own output part.  The only thing crossing a process boundary is process exit
status; the counts are obtained by the parent counting lines afterwards.  A
design with no IPC cannot deadlock in IPC.

ATOMICITY AND RESUME.  Each part is written to `.partial` and renamed, so a part
file that exists is complete.  A stage is complete when its `.done` marker exists,
and the marker LISTS its part files — so the worker count may change between runs
(4 cores here, more on the 64 GB machine) without invalidating anything already
computed.  Single-file stages written by the serial `stream_chambers.py` are read
natively, so an in-flight serial run can be resumed by this program with no
recomputation.

THE KNOWN-ANSWER GATE IS NOT OPTIONAL.  This program exists for 727, where the
chamber count is unknown — which is exactly the situation in which a silent
undercount is accepted because nothing contradicts it.  `python3
pstream_chambers.py gate` must print 1 712 for the 183 record before any run is
believed.  The serial version's first release returned 0 for that case
(FAILURE_MODES 18).
"""
import os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from isolation67 import _fm
from stream_chambers import EMPTY, _sv_encode

DEFAULTS = {
    'nworkers': 4,        # processes per stage; set to the core count
    'time_budget': 0,     # seconds; 0 means no limit
}


def _sv_read_many(paths):
    """Sign vectors from one or more stage files, in order, one at a time."""
    for p in paths:
        with open(p) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                yield () if line == EMPTY else tuple(
                    1 if c == '+' else -1 for c in line)


def _stage_paths(workdir, k):
    """Paths holding a COMPLETE stage k, or None.

    Accepts both layouts: `stage_XX.txt` from the serial enumerator, and a
    `stage_XX.done` marker naming this program's part files."""
    single = os.path.join(workdir, 'stage_%02d.txt' % k)
    if os.path.exists(single):
        return [single]
    marker = os.path.join(workdir, 'stage_%02d.done' % k)
    if os.path.exists(marker):
        parts = [os.path.join(workdir, l.strip())
                 for l in open(marker) if l.strip()]
        if parts and all(os.path.exists(p) for p in parts):
            return parts
    return None


def _extend(wid, nworkers, in_paths, out_path, walls, ncols, i):
    """One worker's share of stage i -> i+1. Runs in a forked child."""
    w = walls[i]
    tmp = out_path + '.partial'
    with open(tmp, 'w') as out:
        for idx, sv in enumerate(_sv_read_many(in_paths)):
            if idx % nworkers != wid:
                continue
            rows = [[s * walls[j][t] for t in range(ncols)]
                    for j, s in enumerate(sv)]
            if _fm(rows + [[w[t] for t in range(ncols)]], ncols) is not None:
                out.write(_sv_encode(sv + (1,)) + '\n')
            if _fm(rows + [[-w[t] for t in range(ncols)]], ncols) is not None:
                out.write(_sv_encode(sv + (-1,)) + '\n')
    os.replace(tmp, out_path)


def pstream_chambers(walls, ncols, workdir, nworkers=4, log=sys.stdout,
                     time_budget=None):
    os.makedirs(workdir, exist_ok=True)
    m = len(walls)
    t0 = time.time()

    if _stage_paths(workdir, 0) is None:
        with open(os.path.join(workdir, 'stage_00.txt'), 'w') as fh:
            fh.write(EMPTY + '\n')
    count = 1

    for i in range(m):
        done = _stage_paths(workdir, i + 1)
        if done is not None:
            count = sum(1 for _ in _sv_read_many(done))
            print('   stage %2d/%d: on disk, %s chambers -- skipped'
                  % (i + 1, m, '{:,}'.format(count)), file=log, flush=True)
            continue
        prev = _stage_paths(workdir, i)
        if prev is None:
            raise SystemExit('stage %d is incomplete; cannot build stage %d' % (i, i + 1))

        names = ['stage_%02d.part%02d' % (i + 1, w) for w in range(nworkers)]
        pids = []
        for w in range(nworkers):
            pid = os.fork()
            if pid == 0:
                try:
                    _extend(w, nworkers, prev, os.path.join(workdir, names[w]),
                            walls, ncols, i)
                    os._exit(0)
                except BaseException:
                    os._exit(1)
            pids.append(pid)
        bad = 0
        for pid in pids:
            _, st = os.waitpid(pid, 0)
            if st != 0:
                bad += 1
        if bad:
            raise SystemExit('stage %d: %d of %d workers failed; refusing to '
                             'write a .done marker for an incomplete stage'
                             % (i + 1, bad, nworkers))
        # The marker is written LAST and only when every part is present, so a
        # stage is never seen as complete unless it is.
        with open(os.path.join(workdir, 'stage_%02d.done' % (i + 1)), 'w') as fh:
            fh.write('\n'.join(names) + '\n')
        count = sum(1 for _ in _sv_read_many(
            [os.path.join(workdir, n) for n in names]))
        el = time.time() - t0
        print('   stage %2d/%d: %9s chambers  (%.0fs, %d workers)'
              % (i + 1, m, '{:,}'.format(count), el, nworkers), file=log, flush=True)
        if time_budget and el > time_budget:
            print('   TIME BUDGET reached after stage %d of %d' % (i + 1, m),
                  file=log, flush=True)
            return count, i + 1
    return count, m


def _gate(nworkers):
    """1 712 chambers at the 183 record, or this program is not to be used."""
    import arrangement as A
    import tempfile, shutil
    W, nc = A._record183_walls(sys.stderr)
    d = tempfile.mkdtemp(prefix='pstream_gate_')
    try:
        n, done = pstream_chambers(W, nc, d, nworkers=nworkers)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    ok = (n == 1712 and done == len(W))
    print('GATE: %d chambers after %d/%d stages (expect 1712) -- %s'
          % (n, done, len(W), 'PASS' if ok else 'FAIL'))
    return 0 if ok else 1


def main():
    cfg = dict(DEFAULTS)
    args = [a for a in sys.argv[1:] if '=' not in a]
    for a in [a for a in sys.argv[1:] if '=' in a]:
        k, v = a.split('=', 1)
        if k not in cfg:
            raise SystemExit('unknown option %r (known: %s)'
                             % (k, ', '.join(sorted(cfg))))
        cfg[k] = type(DEFAULTS[k])(v)
    which = args[0] if args else '393'
    if which == 'gate':
        return _gate(int(cfg['nworkers']))
    from growth727 import walls_of, BASE
    cfgw = BASE if which == '393' else BASE + [(7, 14, 1, -5)]
    W, nc = walls_of(cfgw)
    print('%s: %d walls, ambient %d -- parallel streaming, %d workers'
          % (which, len(W), nc, cfg['nworkers']), flush=True)
    n, done = pstream_chambers(W, nc, os.path.join(HERE, 'stream_' + which),
                               nworkers=int(cfg['nworkers']),
                               time_budget=cfg['time_budget'] or None)
    print('%s: %s chambers after %d stages' % (which, '{:,}'.format(n), done),
          flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
