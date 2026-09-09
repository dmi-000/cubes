#!/usr/bin/env python3
"""Map the 727 arcs A, B, C -- the three of the four-arc node never mapped.

CONTINUUM_MAP mapped arc D (the recorded 727) and left A, B, C as "not yet
mapped".  They are lines a0 + s*v in the sixth cube's Cayley coordinates, with
extents already SOLVED in arcs_extend.py (wall roots, not sampled endpoints), so
nothing here has to search: pick a representative strictly inside the extent and
run the same three measurements arc D got.

REPRESENTATIVE CHOICE.  Simplest rational strictly inside the extent, not the
midpoint -- METHODS 15, and the reason arcs_extend gives in its own docstring:
midpoints of rationals with unrelated denominators compound past the engine's
budget, and s = 1/128 on arc D produces a height-3598 cube.  The cost of the
representative is a free choice, not a property of the arc.

GATE.  Each representative must count 727.  That is the arc's defining property
and an anchor outside every measurement below: an arc whose representative does
not count 727 has been mis-parameterised and its dimensions mean nothing.
"""
import json, sys, os
from fractions import Fraction as F
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE

def relpath(p):
    """Report paths relative to the repository, never as resolved absolutes.

    Logs and run records are quoted in documents that get published, and a
    resolved path carries the account layout of whatever machine produced it.
    The value is also just less useful to a reader: `data/x.json` locates the
    file in the repo, an absolute path locates it on one host.
    """
    try:
        return os.path.relpath(p, ROOT)
    except ValueError:
        return os.path.basename(p)

import sympy as sp
import dimension as D
import wall_keys as W

BASE = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (2, 1, 1, 1), (1, 1, 1, 1)]
ARCS = {
 'D': ([F(2), F(1, 7), F(-5, 7)], [F(-1), F(-1, 7), F(3, 14)], F(-1, 8), F(1, 4)),
 'A': ([F(19, 3), F(-7), F(-11)], [F(1), F(-3), F(-6)], F(20639, 10000), F(19, 6)),
 'B': ([F(4, 35), F(2, 5), F(-41, 35)], [F(1), F(1), F(-4)], F(43, 105), F(5794, 10000)),
 'C': ([F(245, 29), F(-295, 29), F(428, 29)], [F(1), F(-3, 2), F(9, 4)],
       F(11675, 10000), F(477720, 10000)),
}


def simplest_between(lo, hi):
    """simplest rational strictly in (lo, hi), by Stern-Brocot descent.

    Handles an INTEGER endpoint, which the first version of this in solve_wall.py
    did not: it divided by the fractional part and so reported nothing inside
    (4, 5), where 9/2 sits.
    """
    if lo > hi:
        lo, hi = hi, lo
    a, b = lo, hi
    p0, q0, p1, q1 = 0, 1, 1, 0
    while True:
        fl = a.numerator // a.denominator
        if fl + 1 <= b.numerator / b.denominator and fl + 1 > a:
            n, d = p0 + (fl + 1) * p1, q0 + (fl + 1) * q1
            c = F(n, d) if d else None
            if c is not None and lo < c < hi:
                return c
        if fl < a and fl > lo:
            pass
        # integer strictly inside?
        for k in range(int(lo) - 1, int(hi) + 3):
            if lo < k < hi:
                return F(k)
        break
    # no integer inside: descend
    lo_, hi_ = lo, hi
    p0, q0, p1, q1 = 0, 1, 1, 0
    while True:
        fl = lo_.numerator // lo_.denominator
        p0, q0, p1, q1 = p1, q1, fl * p1 + p0, fl * q1 + q0
        lo_ = lo_ - fl
        hi_ = hi_ - fl
        if lo_ == 0:
            lo_ = None
        if hi_ <= 0 or lo_ is None:
            break
        lo_, hi_ = 1 / hi_, (1 / lo_ if lo_ else None)
        if hi_ is None:
            break
        fl2 = lo_.numerator // lo_.denominator
        cand = F(p1 * (fl2 + 1) + p0, q1 * (fl2 + 1) + q0)
        if lo < cand < hi:
            return cand
        p0, q0, p1, q1 = p1, q1, fl2 * p1 + p0, fl2 * q1 + q0
        lo_ -= fl2
        hi_ -= fl2
        if lo_ == 0:
            break
        lo_, hi_ = 1 / hi_ if hi_ else None, 1 / lo_
        if lo_ is None:
            break
    return (lo + hi) / 2                      # fallback, reported as such


def q_of(c):
    L = 1
    for v in c:
        L = L * v.denominator // gcd(L, v.denominator)
    iq = [L] + [int(v * L) for v in c]
    g = 0
    for v in iq:
        g = gcd(g, abs(v))
    return tuple(v // (g or 1) for v in iq)


def measure(label, quats):
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    n = len(quats); nc = 3 * (n - 1)
    cnt = D.count_at(pt, n)
    v = sp.symbols('c0:%d' % nc); Rs = D.frames(v, quats[0])
    tight, loose = D.cached_conditions(Rs, n, v, pt, D.quats_of(pt, quats[0]), quats[0])
    good = [t for t in tight if not t['degenerate']]
    ns = D.nullspace([t['grad'] for t in good], nc)
    st, dirs = D.variety_incremental(good, list(range(len(good))), pt, n, ns,
                                     quats[0], progress=False)
    _, walls = W.walls_of(quats)
    return {'count': str(cnt), 'tight': len(tight), 'nondegenerate': len(good),
            'lineality': len(ns), 'variety': st, 'variety_dirs': len(dirs),
            'distinct_walls': len(walls)}, walls, pt, dirs


OUT = os.path.join(ROOT, 'data', 'arc_node_map.json')


def main():
    out = {'what': 'the 727 four-arc node: A, B, C mapped, D for comparison',
           'gate': 'every representative must count 727',
           'representative_rule': ('simplest rational strictly inside the SOLVED '
                                   'extent, not the midpoint (METHODS 15)'),
           'arcs': {}}
    # MERGE, never replace -- FAILURE_MODES 33.  This file is written per arc, so
    # a run restricted to one arc would otherwise delete the arcs it did not
    # measure.  The same defect was found in wall_keys.py the same day; recording
    # it there did not fix it here, which is the point of the failure mode.
    if os.path.exists(OUT):
        try:
            prev = json.load(open(OUT))
            if isinstance(prev.get('arcs'), dict):
                out['arcs'].update(prev['arcs'])
        except Exception:
            pass
    want = [a for a in sys.argv[1:] if a in ARCS] or ['D', 'A', 'B', 'C']
    for name in want:
        a0, vv, lo, hi = ARCS[name]
        s = F(0) if name == 'D' else simplest_between(lo, hi)
        c = [a0[i] + s * vv[i] for i in range(3)]
        q6 = q_of(c)
        quats = BASE + [q6]
        try:
            m, walls, pt, dirs = measure(name, quats)
        except Exception as e:
            out['arcs'][name] = {'error': type(e).__name__ + ': ' + str(e)[:90]}
            print('%s FAILED %s' % (name, type(e).__name__), flush=True)
            continue
        m.update({'s': str(s), 'extent': [str(lo), str(hi)],
                  'sixth_cube': list(q6), 'height': max(abs(x) for x in q6),
                  'GATE_727': m['count'] == '727'})
        m['keys'] = [{'frame': w['frame'], 'group': [list(x) for x in w['group']],
                      'sig': list(w['sig']), 'c0': w['c0'],
                      'grad': [str(x) for x in w['grad']]} for w in walls]
        m['point'] = [str(x) for x in pt]
        m['quats'] = [list(q) for q in quats]
        out['arcs'][name] = m
        print('%s  s=%-10s cube %-22s h=%-6d count %-5s %s | %d walls | '
              'lineality %d | variety %s %d'
              % (name, s, str(q6), m['height'], m['count'],
                 'GATE OK' if m['GATE_727'] else 'GATE **FAIL**',
                 m['distinct_walls'], m['lineality'], m['variety'],
                 m['variety_dirs']), flush=True)
        json.dump(out, open(OUT, 'w'), indent=1)
    print('written data/arc_node_map.json')


if __name__ == '__main__':
    main()
