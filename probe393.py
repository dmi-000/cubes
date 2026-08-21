#!/usr/bin/env python3
"""Is the ckpt_393 outstanding set actually hard for Fourier-Motzkin?

WHY THIS EXISTS.  On 2026-08-20 the LP `exactlp.feasible_strict` was swapped in
for `isolation67._fm` on the strength of a 7 449 MB FM memory peak.  Reading
`exactlp_report_hard.json` afterwards showed that peak came ENTIRELY from
`dense-random-nv15-rows40` synthetic instances.  The 8 REAL outstanding
stage-14 candidates sampled from the live campaign were solved by FM in
0.4-1.6 ms, while the LP took 5.7-9.2 ms -- FM roughly 10x FASTER on the actual
workload.

8 of 9 173 is a 0.09% sample, so it refutes "the outstanding set is uniformly
hard" and establishes nothing about whether a hard SUBSET exists.  A sampled
count is a lower bound.  This probe raises the sample enough to say which.

WHAT WOULD END IT.  Either (a) a measurable rate of FM instances exceeding the
budget, which justifies routing by size, or (b) no timeout in a few hundred
draws, which means the 393 stall was NOT FM's arithmetic and the real cause is
still unidentified -- and must not be recorded as though it were.

MEMORY CAP, deliberately.  Four workers of this campaign exhausted a 16 GB
machine and froze the terminal on 2026-08-19.  Each FM call therefore runs in a
FORKED CHILD under RLIMIT_AS.  A blowup kills one child and is scored as
`memory` rather than taking the session down with it.  Cost of not doing this,
measured: one forced restart.

Every threshold here is a run-time parameter with a documented default, per
FAILURE_MODES 20 and the sampling discipline in `exactlp.SAMPLING_DEFAULT`.
"""
import json, os, random, resource, signal, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))

DEFAULTS = {
    'n_samples': 400,      # draws from the outstanding set; 0 means all 9 173
    'fm_timeout': 20.0,    # seconds per FM call before it is scored a timeout
    'mem_cap_gb': 2.0,     # per-child address-space cap; a blowup dies alone
    'seed': 20260820,
    'lp_too': 1,           # also time the LP on each instance, for the ratio
}


def _outstanding():
    """Stage-14 candidates the live ckpt_393 run has not decided. READ ONLY."""
    sys.path.insert(0, HERE)
    from growth727 import walls_of, BASE
    from exactlp import _iter_ckpt, _deser_sigma_local
    walls, ncols = walls_of(BASE)
    by_len = {}
    for rec in _iter_ckpt(os.path.join(HERE, 'ckpt_393')):
        sigma = _deser_sigma_local(rec['sigma'])
        by_len.setdefault(len(sigma), {})[sigma] = rec['witness'] is not None
    frontier13 = [s for s, feas in by_len.get(13, {}).items() if feas]
    decided14 = set(by_len.get(14, {}).keys())
    out = [s + (sgn,) for s in frontier13 for sgn in (1, -1)
           if s + (sgn,) not in decided14]
    return walls, ncols, out


def _child_rss_mb(pid):
    """Resident size of one pid, MB, or None once it is gone."""
    import subprocess
    try:
        out = subprocess.run(['ps', '-o', 'rss=', '-p', str(pid)],
                             capture_output=True, text=True, timeout=5).stdout.strip()
        return int(out) / 1024 if out else None
    except Exception:
        return None


def _fm_in_child(rows, ncols, timeout, mem_cap_gb):
    """(status, seconds, peak_rss_mb). status in {'ok','timeout','memory','error'}.

    The call runs in a forked child so neither an unbounded allocation nor a
    runaway recursion can reach this process.

    THE CAP IS ENFORCED BY POLLING RSS, NOT BY RLIMIT_AS.  Setting
    RLIMIT_AS to 2 GB on this machine raises `ValueError: current limit exceeds
    maximum limit` even though the hard limit reads as unlimited: macOS refuses
    a cap below the address space the process has ALREADY mapped, and CPython on
    arm64 reserves far more than 2 GB virtually while resident size stays tiny.
    The first version of this probe used RLIMIT_AS and scored all 25 smoke
    samples as `error` -- an apparatus failure that, unexamined, would have read
    as "FM cannot solve these".  Note the shape: a tool reporting a uniform
    failure it invented itself (FAILURE_MODES 11, tooling that fails silently).

    RSS is also the RIGHT quantity: resident memory is what exhausted the 16 GB
    machine on 2026-08-19, not virtual reservations.
    """
    r, w = os.pipe()
    t0 = time.time()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        try:
            signal.alarm(int(timeout) + 1)
            sys.setrecursionlimit(20000)
            import isolation67 as iso
            t = time.time()
            iso._fm_fourier_motzkin(rows, ncols)
            os.write(w, b'ok %.6f' % (time.time() - t))
        except MemoryError:
            os.write(w, b'memory 0')
        except BaseException:
            os.write(w, b'error 0')
        finally:
            os._exit(0)
    os.close(w)
    cap_mb = mem_cap_gb * 1024
    deadline = t0 + timeout
    status, peak = None, 0.0
    next_poll = t0 + 0.05
    while True:
        done, _ = os.waitpid(pid, os.WNOHANG)
        if done:
            break
        now = time.time()
        if now >= next_poll:
            rss = _child_rss_mb(pid)
            if rss is not None:
                peak = max(peak, rss)
                if rss > cap_mb:
                    os.kill(pid, signal.SIGKILL)
                    os.waitpid(pid, 0)
                    status = 'memory'
                    break
            next_poll = now + 0.05
        if now > deadline:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
            status = 'timeout'
            break
        time.sleep(0.002)
    try:
        msg = os.read(r, 64).decode()
    except Exception:
        msg = ''
    os.close(r)
    if status in ('timeout', 'memory'):
        return status, time.time() - t0, peak
    if not msg:
        return 'error', time.time() - t0, peak
    part = msg.split()
    return part[0], (float(part[1]) if len(part) > 1 else time.time() - t0), peak


def _pct(vals, p):
    if not vals:
        return None
    v = sorted(vals)
    k = (len(v) - 1) * p
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return v[f] if f == c else v[f] + (v[c] - v[f]) * (k - f)


def main():
    cfg = dict(DEFAULTS)
    out_path = os.path.join(HERE, 'probe393_report.json')
    for a in sys.argv[1:]:
        if a.startswith('out='):
            out_path = a[4:]
            continue
        if '=' not in a or a.split('=')[0] not in cfg:
            raise SystemExit('usage: probe393.py [out=PATH] [%s]'
                             % ' '.join('%s=%s' % kv for kv in DEFAULTS.items()))
        k, v = a.split('=', 1)
        cfg[k] = type(DEFAULTS[k])(v)

    walls, ncols, outstanding = _outstanding()
    n_total = len(outstanding)
    random.Random(cfg['seed']).shuffle(outstanding)
    if cfg['n_samples']:
        outstanding = outstanding[:int(cfg['n_samples'])]
    print('outstanding total %d; probing %d (fm_timeout=%ss, cap=%sGB)'
          % (n_total, len(outstanding), cfg['fm_timeout'], cfg['mem_cap_gb']),
          flush=True)

    from exactlp import feasible_strict
    rows_of = lambda s: [walls[t] if s[t] == 1 else [-x for x in walls[t]]
                         for t in range(len(s))]
    recs, t_start = [], time.time()
    counts = {'ok': 0, 'timeout': 0, 'memory': 0, 'error': 0}
    for i, sigma in enumerate(outstanding):
        rows = rows_of(sigma)
        st, t_fm, rss = _fm_in_child(rows, ncols, cfg['fm_timeout'], cfg['mem_cap_gb'])
        counts[st] = counts.get(st, 0) + 1
        t_lp = None
        if cfg['lp_too']:
            t0 = time.time()
            feasible_strict(rows, ncols)
            t_lp = time.time() - t0
        recs.append({'sigma': list(sigma), 'fm_status': st, 't_fm_s': t_fm,
                     'fm_peak_rss_mb': rss, 't_lp_s': t_lp})
        if (i + 1) % 50 == 0:
            print('   %d/%d  %s  %.0fs' % (i + 1, len(outstanding), counts,
                                           time.time() - t_start), flush=True)

    ok = [r for r in recs if r['fm_status'] == 'ok']
    fm_t = [r['t_fm_s'] for r in ok]
    lp_t = [r['t_lp_s'] for r in recs if r['t_lp_s'] is not None]
    ratio = [r['t_lp_s'] / r['t_fm_s'] for r in ok
             if r['t_lp_s'] is not None and r['t_fm_s'] > 0]
    report = {
        'config': cfg, 'n_outstanding_total': n_total, 'n_probed': len(recs),
        'counts': counts,
        'fm_median_s': _pct(fm_t, 0.5), 'fm_p99_s': _pct(fm_t, 0.99),
        'fm_max_s': max(fm_t) if fm_t else None,
        'lp_median_s': _pct(lp_t, 0.5), 'lp_p99_s': _pct(lp_t, 0.99),
        'median_lp_over_fm': _pct(ratio, 0.5), 'p99_lp_over_fm': _pct(ratio, 0.99),
        'fm_peak_rss_mb_max': max((r['fm_peak_rss_mb'] or 0) for r in recs) if recs else None,
        'wall_s': time.time() - t_start,
        'records': recs,
    }
    json.dump(report, open(out_path, 'w'), indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
