#!/usr/bin/env python3
"""Settle a plateau dimension by ORDER OF VANISHING, not by gradient.

WHY GRADIENTS CANNOT DO IT ([P306]).  A wall that CONTAINS the plateau branch vanishes
identically along it, so its gradient there is zero.  Every rank computation then files it
under "walls the plateau does not leave" -- into the container, never into the boundary.
But containing a direction is not containing a neighbourhood of it, and these walls are
curved.  At n = 6 the first-order container came out 2-dimensional while the plateau is
1-dimensional, pinned by 222 genuine concurrency walls that contain arc D and are left by
any step off it.  The walls that bound a plateau are exactly the ones gradients cannot see.

WHAT THIS DOES, per level.

  1. Tight coincidence walls and their exact gradients; the lineality is their null space.
  2. Holding directions: those basis directions of the lineality whose GATED first cell
     counts the record.  "Gated" means the cell is bounded by roots of BOTH wall families --
     coincidence conditions and four-plane concurrency.  At n = 6 the coincidence-only cell
     was 200x too wide and reported a distant cell's count as if it were local.
  3. For each holding direction d and each other container direction u: the count at the
     gated first cell along d + lambda*u.  If it drops, the plateau does not extend that way
     and the first-order container over-estimates.
  4. THE DECIDER: every quadruple of face planes concurrent AT the record, classified by the
     order of vanishing of its determinant along d versus along d + lambda*u.  Identically
     zero along d and finite order beside it means the wall CONTAINS the branch.  Filtered
     for geometry: rank(normals) = rank(augmented) = 3, since a quadruple carrying a parallel
     pair has determinant zero for rank reasons with no common point at all (264 of 486 at
     n = 6 were exactly that, and counting them would have inflated the answer).

The dimension is then read off: a holding direction with genuine containing walls separating
it from every container direction is a 1-dimensional branch, exactly.  Two independent holding
directions whose combination also holds, with no separating wall, is 2-dimensional, exactly.

GATES.
  G1  the record count at the base point.
  G7  lambda = 0 must reproduce the holding direction's own count -- the probe family has to
      be anchored at the thing it perturbs.
  G8  the through-record quadruple set must contain the walls already known at that level.
  Unevaluable counts are COUNTED, never scored as "no change".
"""
import sys, os, json, time, argparse
from fractions import Fraction as F
from itertools import combinations
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
import sympy as sp
import dimension as D
import wall_keys as W
import wall_solve as WS
import wall_census as C
import concurrency_walls as CW
import plateau_solve as P
import provenance as PROV

T = sp.Symbol('t')
TS = [F(i + 1, 7) - F(1, 3) for i in range(CW.DEG + 1 + CW.CHECK)]


def snapshot(pt, q0, dirn):
    return [[x[1] for x in CW.planes_at(pt, dirn, q0, t)] for t in TS]


def poly_along(snap, c):
    """Exact coefficients of the concurrency determinant along a ray, highest power first."""
    vals = [CW.concur_det(*[snap[si][i] for i in c]) for si in range(len(TS))]
    co = CW.newton_poly(TS[:CW.DEG + 1], vals[:CW.DEG + 1])
    if not all(CW._polyval(co, TS[CW.DEG + 1 + j]) == vals[CW.DEG + 1 + j]
               for j in range(CW.CHECK)):
        return None                      # degree bound too low: reported, never absorbed
    return co


def order_sign(co):
    """(order of vanishing at t = 0, sign of the leading coefficient); (None, 0) if zero."""
    if co is None:
        return ('DEGREE_FAIL', 0)
    for i, x in enumerate(reversed(co)):
        if x != 0:
            return (i, 1 if x > 0 else -1)
    return (None, 0)


def gated_cell(quats, pt, nc, q0, dirn, keys, window=F(1, 2)):
    """First cell each side of the record, bounded by BOTH wall families."""
    lo_b, hi_b = -window, window

    def take(Pp):
        nonlocal lo_b, hi_b
        for a, b in C.root_intervals(Pp, float(-window), float(window)):
            if a <= 0 <= b:
                continue
            if b < 0:
                lo_b = max(lo_b, b)
            elif a > 0:
                hi_b = min(hi_b, a)
    for key in keys:
        try:
            co = W.on_line(key, q0, pt, dirn)
        except Exception:
            continue
        if len(co) > 1:
            take(sp.Poly([sp.Rational(x) for x in reversed(co)], T))
    snap = snapshot(pt, q0, dirn)
    lab = [x[0] for x in CW.planes_at(pt, dirn, q0, F(0))]
    mov = CW.moving_cubes(dirn)
    for c in combinations(range(len(lab)), 4):
        if not any(lab[i][0] in mov for i in c):
            continue
        co = poly_along(snap, c)
        if co is None or len(co) < 2:
            continue
        if CW.sturm_count(co, -window, window) == 0:
            continue
        take(sp.Poly([sp.Rational(x) for x in co], T))
    return lo_b, hi_b


def count_in_cell(quats, pt, nc, q0, dirn, keys):
    lo_b, hi_b = gated_cell(quats, pt, nc, q0, dirn, keys)
    out = {}
    for nm, a, b in (('neg', lo_b, F(0)), ('pos', F(0), hi_b)):
        s = C.simplest_in(a, b) if a < b else None
        out[nm] = {'at': (str(s) if s is not None else None),
                   'count': (None if s is None else
                             D.count_at([pt[k] + s * dirn[k] for k in range(nc)], len(quats)))}
    out['cell'] = [str(lo_b), str(hi_b)]
    return out


def seeds_for(n, nc):
    """Known holding directions that do NOT lie in the lineality.

    At n = 6 the plateau's own direction is arc D, and the lineality holds nothing ([P305]),
    so a lineality-seeded search finds no branch there and correctly declines to settle.
    Seeding the arc is what makes n = 6 a validation of this instrument rather than a blank.
    """
    import map_arcs as M
    a0, v, lo, hi = M.ARCS['D']
    if n == 6:
        d = [F(0)] * nc
        for k in range(3):
            d[nc - 3 + k] = v[k]
        return [('arcD', d)]
    if n == 7:
        # The two directions [P299]/[P301] measured the 1217 plateau with: the fibre
        # direction +e15, and the base direction that lifts arc D to the seventh cube.
        # Seeding them is not optional -- a lineality-only search at n = 6 missed the
        # plateau completely, and those two are the directions known to hold 1217.
        f = [F(0)] * nc; f[nc - 3] = F(1)
        b = [F(0)] * nc
        for k in range(3):
            b[nc - 6 + k] = v[k]
        return [('fibre_e15', f), ('base_arcD_lift', b)]
    return []


def analyse(n, lam=F(1, 64), verbose=True):
    t0 = time.time()
    quats = list(W.REC[n]); q0 = quats[0]
    D.set_field(0); D.QZERO[:] = [q0]
    pt, nc, walls = P.tight_walls(quats)
    rec = D.count_at(pt, len(quats))
    G = [w['grad'] for w in walls]
    rT = P.rank(G)
    lin = P.nullspace(G, nc)
    keys = [{k: c[k] for k in ('frame', 'group', 'sig', 'c0')}
            for c in WS.conditions_on(quats)]
    print('n=%d ambient %d record %s | tight walls %d rank %d | lineality %d'
          % (n, nc, rec, len(walls), rT, len(lin)), flush=True)

    holding = []
    lin_res = []
    for j, d in enumerate(lin):
        r = count_in_cell(quats, pt, nc, q0, d, keys)
        hold = any(v['count'] == rec for v in (r['neg'], r['pos']))
        lin_res.append({'dir': j, 'holds': hold, 'probe': r})
        print('  lineality dir %d: cell %s counts %s -> holds %s'
              % (j, r['cell'], [r['neg']['count'], r['pos']['count']], hold), flush=True)
        if hold:
            holding.append((j, d))
    for nm, d in seeds_for(n, nc):
        r = count_in_cell(quats, pt, nc, q0, d, keys)
        hold = any(v['count'] == rec for v in (r['neg'], r['pos']))
        lin_res.append({'dir': nm, 'holds': hold, 'probe': r, 'seeded': True})
        print('  seed %s: cell %s counts %s -> holds %s'
              % (nm, r['cell'], [r['neg']['count'], r['pos']['count']], hold), flush=True)
        if hold:
            holding.append((nm, d))

    # the through-record concurrency quadruples: the only place a containing wall can live
    z = [F(0)] * nc
    P0 = CW.planes_at(pt, z, q0, F(0))
    rows0 = [x[1] for x in P0]
    thru = [c for c in combinations(range(len(P0)), 4)
            if CW.concur_det(*[rows0[i] for i in c]) == 0]
    print('  concurrency quadruples through the record: %d  (%.0fs)'
          % (len(thru), time.time() - t0), flush=True)

    pairs = []
    for (j, d) in holding:
        snapd = snapshot(pt, q0, d)
        base = {c: order_sign(poly_along(snapd, c)) for c in thru}
        kept = [g for g in G if sum(g[i] * d[i] for i in range(nc)) == 0]
        container = P.nullspace(kept, nc) if kept else lin
        print('    container of %s: rank(kept %d) -> dimension %d'
              % (j, len(kept), len(container)), flush=True)
        for k, u in enumerate(container):
            if P.rank([d, u]) < 2:
                continue
            dd = [d[i] + lam * u[i] for i in range(nc)]
            r = count_in_cell(quats, pt, nc, q0, dd, keys)
            hold = any(v['count'] == rec for v in (r['neg'], r['pos']))
            snapp = snapshot(pt, q0, dd)
            contain, degen = 0, 0
            for c in thru:
                o0 = base[c]
                if o0[0] is not None:            # not identically zero along d
                    continue
                o1 = order_sign(poly_along(snapp, c))
                if o1[0] is None or o1[0] == 'DEGREE_FAIL':
                    continue
                rows = [rows0[i] for i in c]
                rn = P.rank([x[:3] for x in rows]); ra = P.rank(rows)
                if rn == 3 == ra:
                    contain += 1
                else:
                    degen += 1
            pairs.append({'hold_dir': j, 'other_dir': k, 'lambda': str(lam),
                          'combination_holds': hold, 'probe': r,
                          'genuine_containing_walls': contain,
                          'rank_degenerate': degen})
            print('    dir %s + %s*dir %s: holds %s | genuine containing walls %d '
                  '(rank-degenerate %d)' % (j, lam, k, hold, contain, degen), flush=True)

    # THE VERDICT IS ABOUT THE BRANCHES TESTED, NOT ABOUT THE PLATEAU.  A lineality-only
    # search at n = 6 found no branch at all while the plateau was 1-dimensional along an arc
    # outside the lineality, so a dimension reported here is a statement about the seeds it
    # was given.  Anything else it is called is the seed's scope read as the world ([P298]).
    # The mixed case is the normal one and the first version returned None for it: at n = 7
    # one container direction is free and one is cut, which is exactly a 2-dimensional branch.
    # Dimension = 1 + the number of independent container directions the branch extends along.
    settled, per_seed = None, {}
    for p in pairs:
        d0 = p['hold_dir']
        e = per_seed.setdefault(d0, {'free': set(), 'cut': 0, 'undecided': 0})
        if p['combination_holds']:
            e['free'].add(p['other_dir'])
        elif p['genuine_containing_walls'] > 0:
            e['cut'] += 1
        else:
            e['undecided'] += 1          # drops with nothing shown to separate it
    for d0, e in per_seed.items():
        e['branch_dimension'] = (1 + len(e['free'])) if not e['undecided'] else None
        e['free'] = sorted(e['free'], key=str)
    if per_seed:
        dims = [e['branch_dimension'] for e in per_seed.values()
                if e['branch_dimension'] is not None]
        settled = max(dims) if dims else None
    return {'n': n, 'ambient': nc, 'record': rec, 'tight_walls': len(walls),
            'rank_tight': rT, 'lineality_dimension': len(lin),
            'old_premise_dimension': nc - rT,
            'lineality': lin_res,
            'holding_directions': [j for j, _ in holding],
            'through_record_quadruples': len(thru),
            'pairs': pairs,
            'branch_dimension_settled': settled,
            'per_seed': per_seed,
            'SCOPE': ('a dimension here is the dimension of the branch through the SEEDED '
                      'directions, not of the plateau. Seeds: lineality basis'
                      + (' plus ' + ', '.join(nm for nm, _ in seeds_for(n, nc))
                         if seeds_for(n, nc) else '')),
            'seconds': round(time.time() - t0, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('levels', nargs='*', type=int, default=[7])
    ap.add_argument('--lam', default='1/64')
    a = ap.parse_args()
    path = os.path.join(ROOT, 'data', 'plateau_order.json')
    out = {'what': 'plateau dimension by order of vanishing -- the walls that CONTAIN the '
                   'branch, which gradients cannot see',
           'method': 'P306', 'levels': {},
           'reproduce': PROV.stamp(parameters=vars(a))}
    if os.path.exists(path):
        try:
            out['levels'].update(json.load(open(path)).get('levels', {}))
        except Exception:
            pass
    for n in a.levels:
        r = analyse(n, F(a.lam))
        out['levels'][str(n)] = r
        # RE-READ BEFORE WRITING.  Two levels running as separate processes each loaded the
        # file at startup and wrote their own union, so the later writer silently reverted the
        # other's level to its stale copy -- FAILURE_MODES 33 one level out.  Merging at write
        # time keeps concurrent runs additive; only the level this process computed is replaced.
        merged = {}
        if os.path.exists(path):
            try:
                merged = json.load(open(path)).get('levels', {})
            except Exception:
                merged = {}
        merged.update({k: v for k, v in out['levels'].items() if k == str(n)})
        for k, v in out['levels'].items():
            merged.setdefault(k, v)
        out['levels'] = merged
        json.dump(out, open(path, 'w'), indent=1)
        print('n=%d -> branch dimension %s (%.0fs)\n' % (n, r['branch_dimension_settled'],
                                                r['seconds']), flush=True)
    print('written data/plateau_order.json')


if __name__ == '__main__':
    main()
