#!/usr/bin/env python3
"""Restart `run393.py` when it deadlocks, until the 393 neighbourhood is complete.

WHY THIS IS NEEDED, and what it is not.  `arrangement.run_parallel` deadlocks in
`multiprocessing.Queue`: sampled 2026-08-20 with `/usr/bin/sample`, the parent's
main thread, all four workers' main threads AND every `QueueFeederThread` sat in
`sem_wait` -- a feeder cannot flush into a full pipe while the process that would
drain it is itself blocked waiting to enqueue. Observed TWICE at chamber-stage
18/18, roughly 33 000 candidates apart, so it is recurrent rather than a one-off.

THIS IS A WORKAROUND, NOT A FIX.  The fix is to stop shipping witnesses through
the queue at all -- workers already append every decision to their own JSONL, so
the queue needs to carry an acknowledgement, not a payload. That change touches
`arrangement.py`, which is shared with the 727 campaign, and is not something to
make while a run is mid-flight. Recorded so the workaround is not mistaken for a
resolution.

WHY RESTARTING IS SAFE AND CHEAP.  Checkpoints are append-only per-worker JSONL
and the driver skips fully-decided stages outright. Measured across the first
restart: 32 771 new distinct stage-18 decisions, zero duplicates, zero
recomputation of earlier stages. Restartability is exactly what makes a campaign
survivable when its apparatus is faulty.

STALL DETECTION uses file growth, not CPU.  Slow, hung, killed and out-of-memory
all present as silence (FAILURE_MODES 11e); the checkpoint line count is the one
signal that distinguishes working from stuck.
"""
import json, glob, os, signal, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
CK = os.path.join(HERE, 'ckpt_393')

DEFAULTS = {
    'stall_s': 90,        # no checkpoint growth for this long => deadlocked
    'poll_s': 10,
    'max_restarts': 12,
    'budget_s': 7200,     # passed through to run393.py
    'target': 100992,     # distinct stage-18 candidates = 2 x feasible-at-17
}


def stage18_distinct():
    seen = set()
    for f in glob.glob(os.path.join(CK, 'worker_*.jsonl')):
        try:
            for line in open(f):
                try:
                    s = json.loads(line)['sigma']
                except Exception:
                    continue
                if s.count(',') == 17:
                    seen.add(s)
        except Exception:
            pass
    return len(seen)


def total_lines():
    n = 0
    for f in glob.glob(os.path.join(CK, 'worker_*.jsonl')):
        try:
            with open(f) as fh:
                for _ in fh:
                    n += 1
        except Exception:
            pass
    return n


def main():
    cfg = dict(DEFAULTS)
    for a in sys.argv[1:]:
        k, v = a.split('=', 1)
        cfg[k] = type(DEFAULTS[k])(v)
    log = open(os.path.join(HERE, 'supervise393.log'), 'a')

    def say(m):
        line = '%s  %s' % (time.strftime('%H:%M:%S'), m)
        print(line, flush=True)
        log.write(line + '\n')
        log.flush()

    for attempt in range(1, cfg['max_restarts'] + 1):
        done = stage18_distinct()
        if done >= cfg['target']:
            say('COMPLETE before launch: %d/%d' % (done, cfg['target']))
            return 0
        say('launch %d: stage-18 %d/%d' % (attempt, done, cfg['target']))
        p = subprocess.Popen([sys.executable, 'run393.py', str(cfg['budget_s'])],
                             cwd=HERE, stdout=subprocess.DEVNULL,
                             stderr=subprocess.STDOUT, start_new_session=True)
        last, last_change = total_lines(), time.time()
        while True:
            time.sleep(cfg['poll_s'])
            if p.poll() is not None:
                say('exited rc=%s; stage-18 %d/%d'
                    % (p.returncode, stage18_distinct(), cfg['target']))
                break
            cur = time.time()
            n = total_lines()
            if n != last:
                last, last_change = n, cur
            elif cur - last_change > cfg['stall_s']:
                say('STALL %ds at %d lines -- killing group'
                    % (int(cur - last_change), n))
                try:
                    os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                except Exception:
                    p.kill()
                p.wait()
                break
        done = stage18_distinct()
        if done >= cfg['target']:
            say('COMPLETE: stage-18 %d/%d' % (done, cfg['target']))
            return 0
    say('gave up after %d restarts at %d/%d'
        % (cfg['max_restarts'], stage18_distinct(), cfg['target']))
    return 1


if __name__ == '__main__':
    sys.exit(main())
