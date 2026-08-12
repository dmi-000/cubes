#!/usr/bin/env python3
"""Is ARC MEMBERSHIP what makes a ruling carry a long constant run?

Postscript 108 found the effect and killed the explanation: at arc A's terminus
rulings hold runs 10x longer than generic directions through the same point
(0.413 vs 0.043), but at a different point with the SAME own-point multiplicity
m_own = 3 there is no effect at all (0.016 vs 0.024).  So multiplicity is not the
variable.  The surviving candidate: the terminus lies ON a maximiser arc, while
the other point is an ordinary rational wall root.

This tests that across all four catalogue lines.  Termini are not documented for
loop723, n7 and n8 (the 2026-08-12 run looked and found none), so they are
RECOVERED here: decompose the line, take the run holding the line's record value,
and its endpoints are the arc's ends.  Then compare, at each point:

    rulings of the walls active there   vs   generic directions through it,

by longest constant run in wall-chambers -- the scale-free statistic of
Postscript 108, since a binary "constant over the window" verdict depends on the
window and mis-scored this twice.

    python3 arc_rulings.py [seconds]

Writes arc_rulings.json / .log incrementally.
"""
import json
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, '/Users/dmi/cube-compounds')
from exact_chambers import decompose
from solve_ends import catalogue, BASE
import wall_params as W
from rulings import build_w4_wall, rulings_of, normalize_dir

T0 = time.time()
LOG = open('/Users/dmi/cube-compounds/arc_rulings.log', 'w')
OUT = '/Users/dmi/cube-compounds/arc_rulings.json'

LINES = {
    'arcA_727': (BASE, [F(19, 3), F(-7), F(-11)], [F(1), F(-3), F(-6)],
                 F(3, 2), F(7, 2)),
    'loop723': (BASE, [F(0), F(0), F(0)], [F(1), F(1), F(1)], F(-5), F(-3)),
    'n7_1217': (BASE + [(7, 14, 1, -5)], [F(-3, 4), F(-1), F(-1)],
                [F(1), F(0), F(0)], F(-1, 8), F(1, 64)),
    'n8_1895': (BASE + [(7, 14, 1, -5), (4, -3, -4, -4)],
                [F(-1), F(1), F(-61, 24)], [F(0), F(0), F(1)], F(-1, 8), F(1, 8)),
}


def log(msg):
    line = '[%6.1fs] %s' % (time.time() - T0, msg)
    print(line, flush=True)
    LOG.write(line + '\n')
    LOG.flush()


def own_mult(a0, d, pts, s):
    """Largest number of ONE triple point's conditions vanishing at s."""
    M, N = W.line_polys(a0, d)
    best = (0, None, [])
    for p, npl, ncub in pts:
        active = []
        for i in range(3):
            col = W.padd(*[W.pscale(M[t][i], F(p[t])) for t in range(3)])
            for sign in (1, -1):
                poly = W.padd(col, W.pscale(N, -sign))
                if sum(c * s ** e for e, c in enumerate(poly)) == 0:
                    active.append((i, sign))
        if len(active) > best[0]:
            best = (len(active), p, active)
    return best


def longest_run(runs):
    tot = sum(r[3] for r in runs)
    best, val = 0, None
    for c, lo, hi, nch, profs, tc in runs:
        if c is not None and nch > best:
            best, val = nch, c
    return best, val, tot


def solve(base, d, p0, label):
    L = max(abs(x) for x in d) or F(1)
    try:
        runs, kind = decompose(base, [F(v) for v in p0], [F(v) for v in d],
                               F(-20) / L, F(20) / L, label)
    except Exception as e:
        log('   %s CRASH %s' % (label, type(e).__name__))
        return None
    best, val, tot = longest_run(runs)
    frac = float(best) / tot if tot else 0.0
    log('   %-30s chambers=%-5d longest=%-5d (%.3f) value=%s'
        % (label, tot, best, frac, val))
    return dict(chambers=tot, longest_run=best, fraction=frac, value=val,
                direction=[str(x) for x in d])


def main():
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 20000.0
    out = []
    rng = random.Random(19)
    for label, (base, a0, d, lo, hi) in LINES.items():
        if time.time() - T0 > budget:
            break
        pts, lns = catalogue(base)
        log('%s: catalogue %d triple points; locating the arc' % (label, len(pts)))
        try:
            runs, kind = decompose(base, a0, d, lo, hi, '%s (locate arc)' % label)
        except Exception as e:
            log('  %s: locate CRASH %s' % (label, type(e).__name__))
            continue
        vals = [r[0] for r in runs if r[0] is not None]
        if not vals:
            log('  %s: no evaluable run' % label)
            continue
        rec = max(vals)
        ends = []
        for c, l, h, nch, profs, tc in runs:
            if c == rec:
                ends += [l, h]
        log('  %s: record %d on this window; termini %s'
            % (label, rec, [str(e) for e in ends[:4]]))

        # candidate points: the arc's termini, plus ordinary roots for contrast
        roots = sorted({r for r in W.w4_params(a0, d, pts)
                        if r.denominator <= 10 ** 6 and lo <= r <= hi})
        ordinary = [r for r in roots if r not in ends]
        rng.shuffle(ordinary)
        cands = [('terminus', e) for e in ends[:2]] + \
                [('ordinary', r) for r in ordinary[:2]]

        for kind_name, s in cands:
            if time.time() - T0 > budget:
                break
            k, p, active = own_mult(a0, d, pts, s)
            if not k:
                log('  %s %s s=%s: no W4 wall active (W3-only root), skipped'
                    % (label, kind_name, s))
                continue
            p0 = [a0[t] + s * d[t] for t in range(3)]
            log('  %s %s s=%s  m_own=%d' % (label, kind_name, s, k))
            for i, sign in active[:2]:
                Q, expr = build_w4_wall(p, i, sign)
                rul = rulings_of(Q, [F(v) for v in p0])
                for tag, val in rul.get('dirs', []):
                    if not tag.startswith('rational'):
                        continue
                    r = solve(base, normalize_dir([F(v) for v in val]), p0,
                              'RULING %s' % kind_name)
                    if r:
                        r.update(line=label, kind=kind_name, s=str(s),
                                 m_own=k, is_ruling=True, record=rec)
                        out.append(r)
            for t in range(2):
                dd = [F(rng.randint(-6, 6)) for _ in range(3)]
                if not any(dd):
                    continue
                r = solve(base, normalize_dir(dd), p0, 'control %s' % kind_name)
                if r:
                    r.update(line=label, kind=kind_name, s=str(s), m_own=k,
                             is_ruling=False, record=rec)
                    out.append(r)
            json.dump(out, open(OUT, 'w'), indent=1)

    log('=== SUMMARY: mean longest-run fraction ===')
    for kind_name in ('terminus', 'ordinary'):
        for grp in (True, False):
            sub = [r for r in out if r['kind'] == kind_name and r['is_ruling'] == grp]
            if sub:
                log('  %-9s %-8s n=%-3d mean=%.3f max=%.3f'
                    % (kind_name, 'ruling' if grp else 'control', len(sub),
                       sum(r['fraction'] for r in sub) / len(sub),
                       max(r['fraction'] for r in sub)))
    json.dump(out, open(OUT, 'w'), indent=1)
    log('done, %d measurements' % len(out))


if __name__ == '__main__':
    main()
