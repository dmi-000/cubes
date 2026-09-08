#!/usr/bin/env python3
"""Parallel rank-synchronous lattice BFS, saving the high-rank flats.

WHY PARALLEL.  The serial version took 11.3 h for 727. Expanding a frontier is
embarrassingly parallel -- each flat's extensions are independent -- with the only
shared state, the dedup set, deferred to a merge at the end of each rank. Work is
concentrated where that helps: ranks 7-10 hold 921 785 of 1 192 678 flats (77%).

WHY IT SAVES FLATS.  The serial run recorded rank COUNTS and discarded the flats,
so we learned there are 2 044 rank-13 flats without learning which. The stratum
walk needs the objects. Emitting them per rank also means a kill costs one rank,
not the run.

NO SHARED CACHE, DELIBERATELY.  `zaslavsky.Flats` caches a basis per flat, but a
forked worker's cache additions never reach the parent, so a later rank would find
the cache empty for flats a worker discovered. Each worker instead rebuilds the
basis for a frontier flat ONCE and reuses it across that flat's 27 extensions --
the build is amortised and the code is stateless, hence fork-safe.

GATE: the 183 arrangement must reproduce 988 flats with per-rank counts
[12, 60, 163, 264, 264, 163, 60, 1]. A dedup bug in the merge would perturb those.
"""
import json, os, sys, time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)


def _reduce(basis, v):
    v = list(v)
    for p, row in basis:
        if v[p]:
            f = v[p]
            v = [a - f * b for a, b in zip(v, row)]
    return v


def _add(basis, v):
    r = _reduce(basis, v)
    for i, x in enumerate(r):
        if x:
            basis.append((i, [a / x for a in r]))
            return True
    return False


def _basis_of(W, mask, m):
    b = []
    for j in range(m):
        if mask >> j & 1:
            _add(b, W[j])
    return b


def _closure(W, basis, m):
    cl = 0
    for j in range(m):
        if not any(_reduce(basis, W[j])):
            cl |= 1 << j
    return cl


def expand_chunk(W, m, frontier, path):
    """Every closure reachable from these flats by adding one wall."""
    out = set()
    for Fm in frontier:
        base = _basis_of(W, Fm, m)
        for j in range(m):
            if Fm >> j & 1:
                continue
            b = [(p, list(r)) for p, r in base]
            _add(b, W[j])
            out.add(_closure(W, b, m))
    with open(path, 'w') as fh:
        fh.write('\n'.join(map(str, out)))


def bfs(W, ncols, nproc=4, save_rank=12, tag='727', log=sys.stdout):
    m = len(W)
    W = [[F(x) for x in w] for w in W]
    t0 = time.time()
    tmp = os.path.join(HERE, '.bfs_%s' % tag)
    os.makedirs(tmp, exist_ok=True)
    bot = _closure(W, [], m)
    seen = {bot}
    frontier = [bot]
    counts = {0: 1}
    saved = {}
    r = 0
    while frontier:
        r += 1
        chunks = [frontier[i::nproc] for i in range(nproc)]
        pids = []
        for w, ch in enumerate(chunks):
            if not ch:
                continue
            pid = os.fork()
            if pid == 0:
                try:
                    expand_chunk(W, m, ch, os.path.join(tmp, 'w%d' % w))
                    os._exit(0)
                except BaseException:
                    os._exit(1)
            pids.append(pid)
        bad = sum(1 for p in pids if os.waitpid(p, 0)[1] != 0)
        if bad:
            raise SystemExit('rank %d: %d workers failed' % (r, bad))
        nxt = []
        for w in range(nproc):
            p = os.path.join(tmp, 'w%d' % w)
            if not os.path.exists(p):
                continue
            for line in open(p):
                line = line.strip()
                if line:
                    g = int(line)
                    if g not in seen:
                        seen.add(g); nxt.append(g)
            os.remove(p)
        if not nxt:
            break
        counts[r] = len(nxt)
        if r >= save_rank:
            saved[r] = nxt
            with open(os.path.join(HERE, 'flats_%s_rank%02d.txt' % (tag, r)), 'w') as fh:
                fh.write('\n'.join(map(str, nxt)))
        frontier = nxt
        print('   rank %2d: %9d flats  (total %9d, %.0fs)%s'
              % (r, len(nxt), len(seen), time.time() - t0,
                 '  [saved]' if r >= save_rank else ''), file=log, flush=True)
        json.dump({'rank_counts': counts, 'total': len(seen), 'complete': False,
                   'secs': time.time() - t0},
                  open(os.path.join(HERE, 'flat_ranks_%s_par.json' % tag), 'w'), indent=1)
    json.dump({'rank_counts': counts, 'total': len(seen), 'complete': True,
               'secs': time.time() - t0},
              open(os.path.join(HERE, 'flat_ranks_%s_par.json' % tag), 'w'), indent=1)
    print('TOTAL %d flats, %.0fs' % (len(seen), time.time() - t0), file=log, flush=True)
    return counts, len(seen)


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'gate'
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    if which == 'gate':
        sys.argv = ['x']
        import arrangement as A
        W, nc = A._record183_walls(sys.stderr)
        c, tot = bfs(W, nc, nproc=nproc, save_rank=99, tag='183')
        want = {0: 1, 1: 12, 2: 60, 3: 163, 4: 264, 5: 264, 6: 163, 7: 60, 8: 1}
        ok = (tot == 988 and c == want)
        print('  183: total %d (want 988), counts match: %s -> %s'
              % (tot, c == want, 'PASS' if ok else 'FAIL'))
        sys.exit(0 if ok else 1)
    from growth727 import walls_of, BASE
    W, nc = walls_of(BASE + [(7, 14, 1, -5)])
    bfs(W, nc, nproc=nproc, save_rank=12, tag='727')
