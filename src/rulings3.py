#!/usr/bin/env python3
"""Rulings, measured with a SCALE-FREE statistic and against a control.

Two prior passes asked "is the count constant over the window", and the window is
arbitrary: Postscript 103's campaign fixed s in (-4,4) against primitive integer
directions, so it swept 4*|d| Cayley units and varied by ~200x between rulings;
the corrected pass fixed the extent instead, but kept the binary verdict, and a
ruling that holds its value across 99 chambers and then ENDS reads as "not
constant" exactly like one that changes at every wall.  Both verdicts are
artefacts of the criterion (Postscripts 103, and the 2026-08-12 re-check that
found 725 holding on 99 of 160 chambers at the arc-A terminus).

What is scale-free is the LONGEST CONSTANT RUN, measured in wall-chambers, which
`exact_chambers.decompose` already returns per run.  A maximiser arc is precisely
a long run terminating at a wall; "constant" and "varying" are the degenerate
ends of that statistic.

And the missing control: the earlier passes compared rulings at different POINTS
instead of comparing, at the SAME point, a ruling against a generic direction.
Only the second comparison isolates what being a ruling contributes -- the first
confounds it with whatever makes the point special.

    python3 rulings3.py [budget_seconds]
"""
import json
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, HERE)
from exact_chambers import decompose
from solve_ends import catalogue, BASE
import wall_params as W
from rulings import build_w4_wall, rulings_of, normalize_dir
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))

A0 = [F(19, 3), F(-7), F(-11)]
D = [F(1), F(-3), F(-6)]
TERMINUS = F(19, 6)
LOG = open(HERE + '/rulings3.log', 'w')
T0 = time.time()


def log(msg):
    line = '[%6.1fs] %s' % (time.time() - T0, msg)
    print(line, flush=True)
    LOG.write(line + '\n')
    LOG.flush()


def own_multiplicity(pts, s):
    """For each base triple point, how many of its OWN conditions vanish at s.
    This is Postscript 96's reading (3 at the terminus), not the aggregate."""
    M, N = W.line_polys(A0, D)
    best = {}
    for idx, (p, npl, ncub) in enumerate(pts):
        k = 0
        active = []
        for i in range(3):
            col = W.padd(*[W.pscale(M[t][i], F(p[t])) for t in range(3)])
            for sign in (1, -1):
                poly = W.padd(col, W.pscale(N, -sign))
                if sum(c * s ** e for e, c in enumerate(poly)) == 0:
                    k += 1
                    active.append((i, sign))
        if k:
            best[idx] = (k, p, active)
    if not best:
        return 0, None, []
    idx = max(best, key=lambda i: best[i][0])
    return best[idx]


def longest_run(runs):
    """(chambers in the longest constant run, its value, total chambers)."""
    tot = sum(r[3] for r in runs)
    best, val = 0, None
    for c, lo, hi, nch, profs, tc in runs:
        if c is not None and nch > best:
            best, val = nch, c
    return best, val, tot


def solve(d, p0, label):
    L = max(abs(x) for x in d) or F(1)
    lo, hi = F(-20) / L, F(20) / L
    try:
        runs, kind = decompose(BASE, [F(v) for v in p0], [F(v) for v in d],
                               lo, hi, label)
    except Exception as e:
        log('   %s: CRASH %r' % (label, type(e).__name__))
        return None
    best, val, tot = longest_run(runs)
    frac = float(best) / tot if tot else 0.0
    log('   %-34s chambers=%-5d longest_run=%-5d (%.2f) value=%s'
        % (label, tot, best, frac, val))
    return dict(direction=[str(x) for x in d], chambers=tot, longest_run=best,
                fraction=frac, value=val)


def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 2400.0
    pts, lns = catalogue(BASE)
    log('catalogue: %d triple points' % len(pts))

    roots = sorted(set(W.w4_params(A0, D, pts)))
    roots = [r for r in roots if r.denominator <= 10 ** 6]
    scored = []
    for s in roots:
        k, p, active = own_multiplicity(pts, s)
        if k:
            scored.append((k, s, p, active))
    scored.sort(key=lambda x: -x[0])
    log('%d rational W4 roots; own-multiplicity max %d, min %d'
        % (len(scored), scored[0][0], scored[-1][0]))

    chosen = []
    term = [x for x in scored if x[1] == TERMINUS]
    if term:
        chosen.append(('terminus', term[0]))
    for x in scored[:3]:
        if x[1] != TERMINUS:
            chosen.append(('high_m', x))
    lows = [x for x in scored if x[0] == 1]
    random.Random(3).shuffle(lows)
    for x in lows[:3]:
        chosen.append(('low_m', x))
    log('selected: %s' % [(k, str(x[1]), 'm_own=%d' % x[0]) for k, x in chosen])

    out = []
    rng = random.Random(11)
    for kind, (k, s, p, active) in chosen:
        if time.time() - T0 > budget:
            log('budget reached'); break
        p0 = [A0[t] + s * D[t] for t in range(3)]
        log('%s point s=%s  m_own=%d  triple point %s' % (kind, s, k, p))
        # the rulings of each active wall at this point
        for i, sign in active[:2]:
            Q, expr = build_w4_wall(p, i, sign)
            rul = rulings_of(Q, [F(v) for v in p0])
            for tag, val in rul.get('dirs', []):
                if not tag.startswith('rational'):
                    continue
                d = normalize_dir([F(v) for v in val])
                r = solve(d, p0, 'RULING i=%d sign=%+d' % (i, sign))
                if r:
                    r.update(kind=kind, s=str(s), m_own=k, is_ruling=True)
                    out.append(r)
        # CONTROL: generic directions through the same point
        for t in range(3):
            d = [F(rng.randint(-6, 6)) for _ in range(3)]
            if not any(d):
                continue
            r = solve(normalize_dir(d), p0, 'control #%d' % t)
            if r:
                r.update(kind=kind, s=str(s), m_own=k, is_ruling=False)
                out.append(r)
        json.dump(out, open(HERE + '/rulings3.json', 'w'), indent=1)

    log('=== SUMMARY: longest constant run as a fraction of chambers ===')
    for grp in (True, False):
        sub = [r for r in out if r['is_ruling'] == grp]
        if not sub:
            continue
        mean = sum(r['fraction'] for r in sub) / len(sub)
        log('  %-9s n=%-3d mean fraction=%.3f  max=%.3f'
            % ('RULINGS' if grp else 'controls', len(sub), mean,
               max(r['fraction'] for r in sub)))
    for kind in ('terminus', 'high_m', 'low_m'):
        for grp in (True, False):
            sub = [r for r in out if r['kind'] == kind and r['is_ruling'] == grp]
            if sub:
                log('    %-9s %-9s n=%-3d mean=%.3f'
                    % (kind, 'ruling' if grp else 'control', len(sub),
                       sum(r['fraction'] for r in sub) / len(sub)))
    json.dump(out, open(HERE + '/rulings3.json', 'w'), indent=1)
    log('done, %d measurements' % len(out))


if __name__ == '__main__':
    main()
