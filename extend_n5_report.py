#!/usr/bin/env python3
"""Report the n=5 -> n=6 extension sweep: one row per congruence class of base.

Written BEFORE the run finished, so the numbers in the write-up come from a script that
exists rather than from an inline computation -- [FAILURE_MODES 27a], which this project
paid for twice on 2026-09-07 alone.

For each base it reports the count distribution over the whole 43 707-cube menu and, for the
cubes attaining the maximum, how many CONGRUENCE CLASSES of n=6 compound they represent. The
last part matters: a base with C3 symmetry has its winners in orbits of 3, so "6 cubes reach
727" is 2 compounds, not 6 ([P228], [P229]).
"""
import collections, glob, json, os, sys
sys.path.insert(0, '.')
from congruent import classes, cube_key, OCT, qmul, qconj
from symmetrize import canon


def symmetry(A):
    """the compound's OWN group: global rotations g with {g*a_i} == {a_i} as cubes.

    Same 24n-candidate trick as congruent(): g must send a_0 to some a_j, so
    g = a_j * s^-1 * a_0^-1 exhausts the possibilities.
    """
    ta = sorted(cube_key(a) for a in A)
    a0i = qconj(A[0]); out = set()
    for a in A:
        for s in OCT:
            g = qmul(qmul(a, qconj(s)), a0i)
            if not any(g):
                continue
            g = canon(g)
            if g in out:
                continue
            if sorted(cube_key(qmul(g, x)) for x in A) == ta:
                out.add(g)
    return out

RES = 'extend_n5_results'
NSH = 4


def load(b):
    fs = [os.path.join(RES, 'b%d_s%d.json' % (b, s)) for s in range(NSH)]
    if not all(os.path.exists(f) for f in fs):
        return None
    rows = []
    for f in fs:
        rows += [(v, tuple(c)) for v, c in json.load(open(f))]
    return rows


if __name__ == '__main__':
    bases = json.load(open('n5family_classes.json'))
    MENU = 43707
    print('%-4s %-5s %-8s %-6s %-6s %-6s %-7s %-6s %-6s %-5s %-5s %s'
          % ('base', 'n=5', 'evaluated', 'max', 'cubes', 'classes', 'median',
             'bulk', 'esc', 'sym', 'orb', 'dup-gate'))
    done = 0
    rows_all = []
    for b, (c5, cf) in enumerate(bases):
        rows = load(b)
        if rows is None:
            print('%-4d %-5d %s' % (b, c5, '-- shards incomplete --'))
            continue
        done += 1
        vals = [v for v, _ in rows]
        mx = max(vals)
        wins = [w for v, w in rows if v == mx]
        base = [tuple(q) for q in cf]
        # classes() is O(k^2) congruence tests and each test is ~10^4 quaternion products,
        # so it is run only where the answer is interesting: a handful of winners, which is
        # the case whenever the maximum is genuinely isolated. A wide tie at a lower count
        # is reported as a count and left unclassified rather than being allowed to dominate
        # the runtime -- and it is reported AS unclassified, never as 1.
        # ORBITS under the base's own symmetry group are cheap and are an upper bound on
        # congruence classes (two cubes in different G-orbits can still give congruent
        # compounds, via a rotation that does not preserve the base). Reported always;
        # the exact class count only where it is affordable.
        G = symmetry(base)
        seen = set(); norb = 0
        for w in wins:
            if cube_key(w) in seen:
                continue
            seen |= {cube_key(qmul(g, w)) for g in G}
            norb += 1
        ncls = len(classes([base + [w] for w in wins])) if len(wins) <= 24 else None
        # A GATE THAT FIRES ON EVERY BASE, free, and stronger than the single 727 check
        # because it does not depend on knowing an answer in advance: the menu is the full
        # octahedral quotient, so it CONTAINS this base's own five cubes, and adding a cube
        # already present leaves the arrangement -- hence the count -- unchanged. So the
        # sweep's MINIMUM must equal the base's own n=5 count, attained by exactly the 5
        # duplicates and nothing else. If it does not, the --base path is not reusing what
        # it claims to reuse.
        lo = min(vals)
        dups = [w for v, w in rows if v == lo]
        keys = {cube_key(tuple(q)) for q in cf}
        gate = (lo == c5 and len(dups) == len(cf)
                and all(cube_key(w) in keys for w in dups))
        if not gate:
            print('     GATE FAILED base %d: min %d (base counts %d), %d cubes at min, '
                  'all duplicates: %s' % (b, lo, c5, len(dups),
                                          all(cube_key(w) in keys for w in dups)))
        # how far the maximum escapes the BULK of the distribution, defined before looking:
        # the highest count reached by at least 100 of the 43 707 menu cubes.
        bulk = max(v for v, n in collections.Counter(vals).items() if n >= 100)
        med = sorted(vals)[len(vals) // 2]
        print('%-4d %-5d %-8d %-6d %-6d %-6s %-7d %-6d %-6d %-5d %-5d %s'
              % (b, c5, len(vals), mx, len(wins),
                 ncls if ncls is not None else '(>24)', med, bulk, mx - bulk,
                 len(G), norb, 'pass' if gate else 'FAIL'))
        rows_all.append((b, c5, mx, len(wins), ncls, med, bulk, gate, vals))
        if len(vals) != MENU:
            print('     NOTE: %d of %d menu cubes evaluated -- %d REFUSED'
                  % (len(vals), MENU, MENU - len(vals)))
    print('\n%d of %d bases complete' % (done, len(bases)))
    if len(rows_all) > 1:
        mxs = [r[2] for r in rows_all]
        print('n=6 maxima across completed bases: %d..%d, spread %d'
              % (min(mxs), max(mxs), max(mxs) - min(mxs)))
        if all(r[7] for r in rows_all):
            print('duplicate-cube gate: PASSES on all %d completed bases '
                  '(min == base count, attained by exactly its own 5 cubes)' % len(rows_all))
        tier = [r for r in rows_all if r[1] == 387]
        if len(tier) > 1:
            t = [r[2] for r in tier]
            print('among the %d bases that all count 387 at n=5: n=6 max ranges %d..%d'
                  % (len(tier), min(t), max(t)))
            print('  -> the n=5 count does NOT determine how well a base extends'
                  if max(t) != min(t) else
                  '  -> every 387 base extends to the same maximum')
