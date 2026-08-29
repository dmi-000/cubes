#!/usr/bin/env python3
"""Exact region count on EVERY chamber of the 727 neighbourhood.

The chambers are cells on which the region count is constant, so evaluating one
point per chamber gives the EXACT MAXIMUM over the neighbourhood -- a local
maximality certificate, not a sample. 4 621 728 chambers, confirmed by two
independent methods (P152/P153 derivation; P146/P149 enumeration, both machines).

THREE THINGS THIS GETS RIGHT BECAUSE THEY WERE GOT WRONG FIRST:

1. SIMPLEST WITNESSES.  The LP's witness has median height 1.4e8 and the engine
   refuses 47% of them -- FAILURE_MODES 16, a refusal about the representative.
   `witness.simplify` drops median height to 189 and evaluability to 100%.
   Scaling to integers instead makes it WORSE (16b); do not "optimise" that away.

2. UNEVALUABLE IS COUNTED, NEVER SCORED.  Any chamber the engine cannot decide is
   written with count null and tallied separately. A maximum computed over an
   unknown fraction of the space is not a maximum.

3. SHARDED AND RESUMABLE AT FINE GRAIN.  cube64 rebooted mid-run on 2026-08-25 and
   destroyed a 25-hour stage that had no intra-stage checkpoint. Shards here are
   sized in minutes; a finished shard is renamed atomically and never recomputed.

Batching: the engine is invoked through `--quats-stdin`, many configurations per
process, because per-call process spawn dominates otherwise.
"""
import json, os, subprocess, sys, time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from exactlp import feasible_strict
from witness import simplify
from dimension import q_of

NSHARDS = int(os.environ.get('EVAL_SHARDS', '960'))
BATCH = int(os.environ.get('EVAL_BATCH', '250'))
OUT = os.path.join(HERE, 'eval727')
ENG = os.path.join(HERE, 'cube_regions_n')
ENGW = os.path.join(HERE, 'cube_regions_q2w')


def _sv_read(paths):
    for p in paths:
        with open(p) as fh:
            for line in fh:
                line = line.strip()
                if line and line != '.':
                    yield line


def _line(y):
    """(line, needs_wide). The narrow engine caps components at 512; exceeding
    that is NOT unevaluable, it is a budget of the wrong instrument -- the wide
    engine takes it. Dropping this fallback (the first version of this file did)
    scored 16.7% of a pilot shard as unevaluable when `dimension.count_at` would
    have answered every one. FAILURE_MODES 16, reproduced by omission."""
    quats = [(1, 0, 0, 0)]
    for k in range(0, len(y), 3):
        quats.append(q_of(y[k:k + 3]))
    line = ';'.join(','.join(map(str, q)) for q in quats)
    return line, max(abs(v) for q in quats for v in q) > 512


def run_shard(k, paths, W, nc):
    out = os.path.join(OUT, 'shard%04d.jsonl' % k)
    if os.path.exists(out):
        return
    tmp = out + '.partial'
    recs, pend, pend_sv, wide, wide_sv = [], [], [], [], []

    def _run(cmd, lines, svs):
        p = subprocess.run(cmd, input='\n'.join(lines) + '\n',
                           capture_output=True, text=True)
        outs = [l for l in p.stdout.splitlines() if l.startswith('{')]
        for sv, ln in zip(svs, outs + [None] * (len(svs) - len(outs))):
            c = None
            if ln:
                try:
                    c = json.loads(ln)['bounded']
                except Exception:
                    c = None
            recs.append({'sigma': sv, 'count': c})

    def flush():
        if pend:
            _run([ENG, '--quats-stdin'], pend, pend_sv)
            pend.clear(); pend_sv.clear()
        if wide:
            # ENGW ALSO takes --quats-stdin. The first version spawned one process
            # per overflow config; with ~1 in 6 configs overflowing that is a
            # process launch every few chambers, and the measured ETA came out
            # 187 h against an estimated 39 h. Batching it costs one line.
            _run([ENGW, '--d', '0', '--quats-stdin'], wide, wide_sv)
            wide.clear(); wide_sv.clear()

    for idx, sv in enumerate(_sv_read(paths)):
        if idx % NSHARDS != k:
            continue
        sig = [1 if ch == '+' else -1 for ch in sv]
        rows = [[s * W[j][t] for t in range(nc)] for j, s in enumerate(sig)]
        y = feasible_strict(rows, nc)
        if y is None:
            recs.append({'sigma': sv, 'count': None, 'why': 'no witness'})
            continue
        z = simplify(rows, list(y), nc)
        ln, needs_wide = _line([F(v) for v in z])
        if needs_wide:
            wide.append(ln); wide_sv.append(sv)
        else:
            pend.append(ln); pend_sv.append(sv)
        if len(pend) >= BATCH or len(wide) >= BATCH:
            flush()
    flush()
    with open(tmp, 'w') as fh:
        for r in recs:
            fh.write(json.dumps(r) + '\n')
    os.replace(tmp, out)


def main():
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    os.makedirs(OUT, exist_ok=True)
    W, nc = walls_of(BASE + [(7, 14, 1, -5)])
    d = os.path.join(HERE, 'stream_727')
    marker = os.path.join(d, 'stage_27.done')
    paths = [os.path.join(d, l.strip()) for l in open(marker) if l.strip()]
    todo = [k for k in range(NSHARDS)
            if not os.path.exists(os.path.join(OUT, 'shard%04d.jsonl' % k))]
    print('%d shards, %d remaining, %d processes' % (NSHARDS, len(todo), nproc), flush=True)
    t0 = time.time()
    for base in range(0, len(todo), nproc):
        pids = []
        for k in todo[base:base + nproc]:
            pid = os.fork()
            if pid == 0:
                try:
                    run_shard(k, paths, W, nc); os._exit(0)
                except BaseException:
                    os._exit(1)
            pids.append(pid)
        for pid in pids:
            os.waitpid(pid, 0)
        done = min(base + nproc, len(todo))
        el = time.time() - t0
        print('   %d/%d shards (%.0fs elapsed, ETA %.1f h)'
              % (done, len(todo), el, el / done * (len(todo) - done) / 3600), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
