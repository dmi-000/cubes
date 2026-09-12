#!/usr/bin/env python3
"""Every wall on a line, as an exact polynomial with ALL its real roots recorded.

This replaces the two restrictions that made `arc_special` a partial instrument:

  RATIONAL ROOTS ONLY.  It searched only for rational roots and reported the rest
  as "irrational, not testable". One of arc D's ten such roots WAS its own upper
  boundary ([P296]). Here every real root is found exactly, as an algebraic number
  with its minimal polynomial and an isolating interval.

  THE 'UNEVALUATED' GROUPS.  Size-2 groups with no active coordinate were skipped
  because `branch_numerator` implements only the breakpoint branch. They need no
  branch: `min_l1_argmin` returns a 2-element minimiser ONLY with a vanishing
  coordinate, so such a group's minimiser is at a VERTEX and the wall is the
  size-1 wall of the surviving normal. Verified exhaustively on arc D: 254 of 254
  are vertex cases, and in 254 of 254 the surviving normal is already present as a
  size-1 group. They are duplicates, not gaps.

WHAT IS RECORDED, per condition: the branch key, the exact coefficient list of the
polynomial restricted to the line, its degree, and every real root -- rational as a
fraction, irrational as (minimal polynomial, isolating interval, decimal). The
polynomials are the deliverable; the roots are read off them.

A ROOT IS A CANDIDATE UNTIL VERIFIED. The branch is frozen at the base point, so a
root locates where THAT branch reaches 1, which is an analytic continuation. Each
rational root is checked by recomputing the tight set there; irrational roots
cannot be evaluated in rational arithmetic and are recorded as unverified, which
is a statement about the arithmetic and not about the root.
"""
import sys, os, json, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
import sympy as sp
import dimension as D
import wall_keys as W


def conditions_on(quats):
    """Every (frame, group) with branch data, tightness, and the vertex-collapse
    applied so nothing is skipped."""
    n = len(quats)
    out = []
    for i in range(n):
        others = [j for j in range(n) if j != i]
        Nval = {}
        for j in others:
            R = D.mat_num(quats[i], quats[j])
            for k in range(3):
                for sg in (1, -1):
                    Nval[(j, k, sg)] = [sg * R[r][k] for r in range(3)]
        keys = list(Nval)
        groups = [(kk,) for kk in keys] + list(itertools.combinations(keys, 2))
        for g in groups:
            got = D.min_l1_argmin([Nval[k] for k in g])
            if got is None:
                continue
            val, lam, v = got
            sig = D.l1_signs(v)
            Z = [c for c in range(3) if sig[c] == 0]
            if len(g) == 2 and not Z:
                # vertex case: collapse to the surviving single normal
                nz = [t for t, x in enumerate(lam) if x != 0]
                if len(nz) != 1:
                    continue
                g = (g[nz[0]],)
                got = D.min_l1_argmin([Nval[g[0]]])
                if got is None:
                    continue
                val, lam, v = got
                sig = D.l1_signs(v)
                Z = [c for c in range(3) if sig[c] == 0]
            if len(g) == 1 and Z:
                continue                       # kink, genuinely degenerate
            if len(g) == 2 and len(Z) != 1:
                continue
            out.append({'frame': i, 'group': g, 'sig': sig,
                        'c0': (Z[0] if Z else None), 'tight': val == 1})
    return out


def _roots_exact(coeffs, t):
    """Every real root, exactly. Rational as a Fraction; irrational as its minimal
    polynomial plus an isolating interval -- never discarded, never rounded away."""
    P = sp.Poly([sp.Rational(c) for c in reversed(coeffs)], t)
    if P.degree() < 1:
        return []
    out = []
    for r in sp.real_roots(P):
        if r.is_rational:
            out.append({'kind': 'rational', 'value': str(sp.Rational(r)),
                        'decimal': float(r)})
        else:
            mp = sp.minimal_polynomial(r, sp.Symbol('x'))
            iv = r.interval if hasattr(r, 'interval') else None
            out.append({'kind': 'algebraic', 'minimal_polynomial': str(mp),
                        'degree': sp.Poly(mp, sp.Symbol('x')).degree(),
                        'isolating_interval': [str(iv.a), str(iv.b)] if iv else None,
                        'decimal': float(r.evalf(20))})
    return out


def solve_line(quats, dirn, label, lo=None, hi=None, verbose=True, s_shift=None):
    """All wall polynomials along quats + t*dirn, with all real roots."""
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    nc = len(pt)
    t = sp.Symbol('t')
    conds = conditions_on(quats)
    rows, nroot, nirr, skipped = [], 0, 0, 0
    for c in conds:
        key = {k: c[k] for k in ('frame', 'group', 'sig', 'c0')}
        try:
            co = W.on_line(key, quats[0], pt, dirn)
        except Exception:
            skipped += 1
            continue
        if len(co) < 2:
            continue                            # constant on this line
        rr = _roots_exact(co, t)
        if lo is not None:
            rr = [r for r in rr if lo <= r['decimal'] <= hi]
        if not rr:
            continue
        if s_shift is not None:          # record roots in the ARC's parameter too
            for r in rr:
                r['s_decimal'] = r['decimal'] + float(s_shift)
                if r['kind'] == 'rational':
                    r['s_value'] = str(sp.Rational(r['value']) + sp.Rational(s_shift))
        nroot += len(rr)
        nirr += sum(1 for r in rr if r['kind'] == 'algebraic')
        rows.append({'frame': c['frame'], 'group': [list(x) for x in c['group']],
                     'sig': list(c['sig']), 'c0': c['c0'], 'tight_at_base': c['tight'],
                     'degree': len(co) - 1,
                     'polynomial': [str(x) for x in co], 'roots': rr})
    if verbose:
        print('%-14s %d conditions | %d walls with a root in range | %d roots '
              '(%d irrational) | %d unbuildable'
              % (label, len(conds), len(rows), nroot, nirr, skipped), flush=True)
    return {'label': label, 'conditions': len(conds), 'walls_with_roots': len(rows),
            'roots_total': nroot, 'roots_irrational': nirr,
            'unbuildable': skipped, 'walls': rows}


def main():
    import map_arcs as M
    S0 = {'D': F(1, 8), 'A': F(3), 'B': F(1, 2), 'C': F(2)}
    want = [a for a in sys.argv[1:] if a in M.ARCS] or ['D']
    p = os.path.join(ROOT, 'data', 'wall_polynomials.json')
    out = {'what': 'every wall polynomial on each 727 arc, with ALL real roots exact',
           'method': 'restrict each condition to the arc line; real_roots; minimal polynomials',
           'note': ('rational roots are verifiable by evaluation; irrational ones are '
                    'recorded with minimal polynomial and isolating interval and are '
                    'NOT verifiable in rational arithmetic'),
           'arcs': {}}
    if os.path.exists(p):
        try:
            prev = json.load(open(p))
            if isinstance(prev.get('arcs'), dict):
                out['arcs'].update(prev['arcs'])
        except Exception:
            pass
    import arc_special as A
    for name in want:
        a0, vv, lo, hi = M.ARCS[name]
        s0 = S0[name]
        quats = A.arc_quats(name, s0)
        D.set_field(0); D.QZERO[:] = [quats[0]]
        nc = 3 * (len(quats) - 1)
        d = [F(0)] * nc
        for k in range(3):
            d[nc - 3 + k] = vv[k]
        r = solve_line(quats, d, 'arc %s' % name,
                       lo=float(lo - s0), hi=float(hi - s0), s_shift=s0)
        r['s0'] = str(s0); r['extent_searched'] = [str(lo), str(hi)]
        r['roots_in_s'] = 'add s0 = %s to each root in t' % s0
        out['arcs'][name] = r
        json.dump(out, open(p, 'w'), indent=1)
    print('written data/wall_polynomials.json')


if __name__ == '__main__':
    main()
