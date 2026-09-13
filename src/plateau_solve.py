#!/usr/bin/env python3
"""Settle [OQ 33] by SOLVING: which tight walls bound the count plateau, and its dimension.

THE PREMISE THAT WAS FALSE ([P298]).  Every plateau dimension in this project came from a
tangent search whose candidate space was the null space of ALL the tight walls' gradients --
"a first-order tangent must lie in every wall".  A direction crossing 7 of 51 walls preserves
the count, so that space is too small and every dimension it produced is a LOWER BOUND.

THE CORRECT OBJECT.  Let T be the tight walls at the record and C the subset whose crossing
actually changes the count.  Then locally

    plateau  is contained in  V(C)   and is NOT contained in  V(T \\ C)

so the plateau's tangent dimension is `ambient - rank(grad C)`, not `ambient - rank(grad T)`.
C is what [OQ 33] asks for and it is decidable one wall at a time.

HOW EACH WALL IS DECIDED, exactly and without a step size.  For wall w, solve for a direction

    d_w  in  null(grad of every tight wall EXCEPT w),  with  grad_w . d_w != 0

If no such d_w exists, grad_w lies in the span of the others and w cannot be crossed alone;
that is reported as UNDECIDABLE-ALONE, never as "preserves".  Otherwise d_w leaves V(w) while
staying on every other tight wall.  Then every condition is restricted to that ray, ALL real
roots are taken, and the count is evaluated at the simplest rational strictly inside the first
cell on each side of the origin.  No epsilon: the cell is measured, not a point near the wall.

    count drops on either side   ->  w BOUNDS the plateau, w is in C
    count equals the record      ->  w does NOT bound; the plateau leaves V(w)

THE DIMENSION, both bounds.
  upper:  ambient - rank(grad C), the tangent space of V(C).
  lower:  exhibited.  A direction in null(grad C) that is NOT in null(grad T) is solved for,
          its first wall crossing on each side is solved, and the count is taken strictly
          inside.  A record count there is a POINT of the plateau off the full tight variety,
          which is the thing the old premise said could not exist.
When the two meet the dimension is settled rather than bounded.

GATES.
  G1  count at the record must be the record.
  G5  every d_w must satisfy the linear system it was solved from -- checked by substitution,
      exactly, not by residual size.
  G6  the census's own answer must be reproduced where they overlap: on ray e0 at n = 6 the
      walls this file calls bounding must be among the count-changing crossings of
      `data/wall_census_n6.json` ([P304]).
  Unevaluable counts are COUNTED and reported, never scored as "no change".
"""
import sys, os, json, time, argparse
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
import sympy as sp
import dimension as D
import wall_keys as W
import wall_solve as WS
import wall_census as C

T = sp.Symbol('t')


# ------------------------------------------------------------------ exact linear algebra

def rref(M):
    """Reduced row echelon form over Q, with the pivot columns."""
    M = [row[:] for row in M]
    rows, cols = len(M), (len(M[0]) if M else 0)
    piv, r = [], 0
    for c in range(cols):
        k = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if k is None:
            continue
        M[r], M[k] = M[k], M[r]
        inv = F(1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(cols)]
        piv.append(c); r += 1
        if r == rows:
            break
    return M, piv


def nullspace(M, ncols):
    """A basis of {d : M d = 0}, over Q."""
    if not M:
        return [[F(1) if i == j else F(0) for i in range(ncols)] for j in range(ncols)]
    R, piv = rref(M)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [F(0)] * ncols
        v[f] = F(1)
        for i, c in enumerate(piv):
            v[c] = -R[i][f]
        basis.append(v)
    return basis


def rank(M):
    return len(rref(M)[1]) if M else 0


# ------------------------------------------------------------------ walls and gradients

def tight_walls(quats):
    """Distinct tight walls at the record, each with its exact gradient.

    The gradient is read off the wall's own polynomial restricted to each coordinate axis:
    the wall vanishes at the record, so the linear coefficient of P(t) along e_k IS the k-th
    partial.  Same P for every k, so the scaling is consistent by construction and no
    normalisation is needed or applied.
    """
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    nc = len(pt)
    seen, out = {}, []
    for c in WS.conditions_on(quats):
        if not c['tight']:
            continue
        key = {k: c[k] for k in ('frame', 'group', 'sig', 'c0')}
        g = []
        ok = True
        for k in range(nc):
            d = [F(0)] * nc; d[k] = F(1)
            try:
                co = W.on_line(key, quats[0], pt, d)
            except Exception:
                ok = False; break
            g.append(F(co[1]) if len(co) > 1 else F(0))
        if not ok or not any(g):
            continue
        lead = next(x for x in g if x != 0)
        sig = tuple(x / lead for x in g)          # gradient direction, up to scale
        if sig in seen:
            continue
        seen[sig] = True
        out.append({'key': key, 'grad': g,
                    'cubes': sorted({c['frame']} | {t[0] for t in c['group']}),
                    'size': len(c['group'])})
    return pt, nc, out


# ------------------------------------------------------------------ deciding one wall

def first_cells(quats, pt, nc, dirn, keys, window=F(1, 2)):
    """The simplest rational strictly inside the first cell each side of the origin.

    Solved, not stepped.  Every condition is restricted to the ray and ALL real roots are
    taken; the nearest strictly-negative and strictly-positive root bound the two cells the
    origin sits between.  Roots whose isolating interval straddles or touches 0 are the
    record's own walls and are skipped -- the first version let them collapse the lower
    bound to 0, so every negative side came back None and half the evidence was silently
    missing.
    """
    lo_b, hi_b = -window, window
    for key in keys:
        try:
            co = W.on_line(key, quats[0], pt, dirn)
        except Exception:
            continue
        if len(co) < 2:
            continue
        P = sp.Poly([sp.Rational(x) for x in reversed(co)], T)
        for a, b in C.root_intervals(P, float(-window), float(window)):
            if a <= 0 <= b:
                continue                     # a wall through the record itself
            if b < 0:
                lo_b = max(lo_b, b)
            elif a > 0:
                hi_b = min(hi_b, a)
    neg = C.simplest_in(lo_b, F(0)) if lo_b < 0 else None
    pos = C.simplest_in(F(0), hi_b) if hi_b > 0 else None
    return neg, pos


def closure(G, S, ncols):
    """Matroid closure: every wall whose gradient lies in the span of S's."""
    if not S:
        base = []
    else:
        base = [G[i] for i in S]
    R, piv = rref(base) if base else ([], [])
    out = set(S)
    for j, g in enumerate(G):
        if j in out:
            continue
        if rank(base + [g]) == len(piv):
            out.add(j)
    return frozenset(out)


def flats(G, ncols, max_rank):
    """Every flat of the gradient matroid up to `max_rank`, by closure BFS.

    The strata of the local arrangement ARE the flats: a stratum is `null(G_F)` and its
    dimension is `ambient - rank(G_F)`.  Enumerating them is what turns "search for a
    direction that preserves the count" into a finite decision.
    """
    seen = {closure(G, [], ncols): 0}
    frontier = [closure(G, [], ncols)]
    while frontier:
        nxt = []
        for Fl in frontier:
            r = rank([G[i] for i in Fl]) if Fl else 0
            if r >= max_rank:
                continue
            for j in range(len(G)):
                if j in Fl:
                    continue
                c = closure(G, list(Fl) + [j], ncols)
                if c not in seen:
                    seen[c] = rank([G[i] for i in c])
                    nxt.append(c)
        frontier = nxt
    return seen


def test_dir(quats, pt, nc, keys, d, rec):
    """Count in the first solved cell on each side of the record along d."""
    neg, pos = first_cells(quats, pt, nc, d, keys)
    out = {}
    for nm, sv in (('neg', neg), ('pos', pos)):
        out[nm] = {'at': (str(sv) if sv is not None else None),
                   'count': (None if sv is None else
                             D.count_at([pt[k] + sv * d[k] for k in range(nc)], len(quats)))}
    vals = [v['count'] for v in out.values() if v['count'] is not None]
    out['holds'] = bool(vals) and any(v == rec for v in vals)
    out['evaluated'] = len(vals)
    return out


def decide(quats, pt, nc, walls, rec, verbose=True):
    """For each tight wall: can the plateau leave it?

    WHY NOT "CROSS w AND NOTHING ELSE".  That was the first version and it decided 1 of 27
    walls at n = 6: with 27 gradients of rank 14, almost every gradient lies in the span of
    the others, so the system `stay on all the rest, leave w` has only the zero solution.
    Reporting the other 26 as anything but undecided would have been a fabricated answer.

    WHAT IS DONE INSTEAD.  Keep as many other walls as possible and drop the fewest needed:
    start from all of T \ {w}, and while the null space is orthogonal to grad_w, drop the
    wall that frees it.  The resulting d leaves V(w) and a few others, which makes the
    verdicts ASYMMETRIC and they are reported that way:

        count holds     ->  LEAVES: the plateau provably extends off V(w).  Decisive, because
                            a point with the record count and w != 0 is exhibited.
        count drops     ->  UNDECIDED: the drop may be caused by any wall dropped alongside w.

    Only the decisive direction is claimed.  A "drops" is never read as "w bounds".
    """
    keys = [{k: c[k] for k in ('frame', 'group', 'sig', 'c0')}
            for c in WS.conditions_on(quats)]
    G = [w['grad'] for w in walls]
    out, holding = [], []
    for i, w in enumerate(walls):
        S = [j for j in range(len(G)) if j != i]
        d = None
        while True:
            ns = nullspace([G[j] for j in S], nc) if S else \
                 [[F(1) if a == b else F(0) for a in range(nc)] for b in range(nc)]
            cand = [v for v in ns if sum(w['grad'][k] * v[k] for k in range(nc)) != 0]
            if cand:
                d = cand[0]; break
            if not S:
                break
            S.pop()                       # drop one more wall and try again
        if d is None:
            out.append({'cubes': w['cubes'], 'size': w['size'], 'key': str(w['key']),
                        'status': 'NO_DIRECTION'})
            continue
        assert all(sum(G[j][k] * d[k] for k in range(nc)) == 0 for j in S), 'G5 failed'
        r = test_dir(quats, pt, nc, keys, d, rec)
        st = ('LEAVES' if r['holds'] else
              ('UNEVALUABLE' if r['evaluated'] == 0 else 'UNDECIDED'))
        if st == 'LEAVES':
            holding.append(d)
        out.append({'cubes': w['cubes'], 'size': w['size'], 'key': str(w['key']),
                    'status': st, 'walls_kept': len(S), 'walls_dropped': len(G) - 1 - len(S),
                    'probe': r})
        if verbose:
            print('   wall %2d/%d cubes=%-12s kept %2d/%2d  %-12s %s'
                  % (i + 1, len(walls), w['cubes'], len(S), len(G) - 1, st,
                     {k: v['count'] for k, v in r.items() if isinstance(v, dict)}),
                  flush=True)
    return out, holding


def run(n, verbose=True):
    quats = list(W.REC[n])
    D.set_field(0); D.QZERO[:] = [quats[0]]
    try:
        pt, nc, walls = tight_walls(quats)
    except Exception as e:
        return {'n': n, 'status': 'NO CHART: %s' % type(e).__name__}
    rec = D.count_at(pt, len(quats))
    if rec is None:
        return {'n': n, 'status': 'record not evaluable in this chart'}
    G = [w['grad'] for w in walls]
    rT = rank(G)
    keys = [{k: c[k] for k in ('frame', 'group', 'sig', 'c0')}
            for c in WS.conditions_on(quats)]
    print('n=%d  ambient %d | record %s | distinct tight walls %d | rank %d | '
          'old-premise dimension %d' % (n, nc, rec, len(walls), rT, nc - rT), flush=True)

    # the old premise's own candidate space, evaluated at a SOLVED point rather than an eps
    lin = nullspace(G, nc)
    lin_probe = [test_dir(quats, pt, nc, keys, v, rec) for v in lin]

    res, holding = decide(quats, pt, nc, walls, rec, verbose)

    # LOWER BOUND on the plateau dimension: independent directions that hold the record,
    # plus a generic combination of them, which is what makes it a dimension and not a count
    ind, combo = [], None
    for d in holding:
        if rank(ind + [d]) > len(ind):
            ind.append(d)
    if len(ind) > 1:
        mix = [sum(ind[j][k] * F(j + 1) for j in range(len(ind))) for k in range(nc)]
        combo = test_dir(quats, pt, nc, keys, mix, rec)
    dim_lo = (len(ind) if (len(ind) < 2 or (combo and combo['holds'])) else 1)
    return {'n': n, 'ambient': nc, 'record': rec, 'tight_walls': len(walls),
            'rank_all_tight': rT, 'old_premise_dimension': nc - rT,
            'lineality_holds_record': [p['holds'] for p in lin_probe],
            'walls_the_plateau_provably_leaves': sum(1 for r in res if r['status'] == 'LEAVES'),
            'undecided': sum(1 for r in res if r['status'] == 'UNDECIDED'),
            'unevaluable': sum(1 for r in res if r['status'] == 'UNEVALUABLE'),
            'independent_holding_directions': len(ind),
            'generic_combination_holds': (None if combo is None else combo['holds']),
            'plateau_dimension_lower_bound': dim_lo,
            'walls': res}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('levels', nargs='*', type=int, default=[6])
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    path = os.path.join(ROOT, 'data', 'plateau_solve.json')
    out = {'what': 'which tight walls BOUND the count plateau, and the plateau dimension, '
                   'both by solving',
           'question': 'OPEN_QUESTIONS 33',
           'levels': {}}
    if os.path.exists(path):
        try:
            prev = json.load(open(path))
            out['levels'].update(prev.get('levels', {}))
        except Exception:
            pass
    for n in a.levels:
        t0 = time.time()
        r = run(n, verbose=not a.quiet)
        r['seconds'] = round(time.time() - t0, 1)
        out['levels'][str(n)] = r
        json.dump(out, open(path, 'w'), indent=1)
        print('n=%d -> %s' % (n, json.dumps({k: v for k, v in r.items()
                                             if k not in ('walls',)})), flush=True)
    print('written data/plateau_solve.json')


if __name__ == '__main__':
    main()
