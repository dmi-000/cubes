#!/usr/bin/env python3
"""Find the SPECIAL POINTS of the 727 arcs by solving, not by walking.

[P293](LEDGER.md#p293) showed the four arcs of the 727 node are structurally
identical -- 20 walls, lineality 2, two surviving directions at a generic point --
and that the record is a special POINT (27 walls, lineality 1, isolated) that
happens to lie on arc D.  That predicts arcs A, B and C hold special points of
their own, and nothing has looked.

WHY THIS IS A SOLVE.  A special point is where extra conditions go TIGHT.  Each
arc is an affine line in the ambient Cayley coordinates (verified: the arc moves
only the sixth cube, whose three coordinates are ambient 12,13,14), and a
condition restricted to a line is an exact univariate polynomial.  So the
parameters where a condition goes tight are that polynomial's ROOTS.  Walking `s`
would measure the walk; `wall_keys.on_line` returns the polynomial.

THE FROZEN BRANCH, AND WHY EVERY ROOT IS ONLY A CANDIDATE.  A condition's sign
pattern and active coordinate are frozen at the generic point, so `P(t) = 0`
locates where THAT BRANCH reaches 1, which is the analytic continuation and not
the condition itself -- the same distinction that cost a wrong claim in
[P288](LEDGER.md#p288).  Every root is therefore verified by recomputing
`min_l1_argmin` at that parameter and asking whether the group is genuinely
tight.  Verification is numeric-exact and cheap; only the polynomial build is not.

CONTROL, and it is the point of the exercise.  Arc D's special point is known:
`s = 0`, the 727 record, where the tight count rises to 216 and the walls to 27.
A method that cannot rediscover `s = 0` from the polynomials is not working, and
its answers for A, B and C would mean nothing.
"""
import sys, os, json, itertools, collections
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
import sympy as sp
import dimension as D
import wall_keys as W
import map_arcs as M


def groups_at(quats):
    """Every (frame, group) with its branch data and whether it is TIGHT.

    Numeric only -- no symbolic normals and no gradients.  `dimension.conditions`
    builds symbolic normals in order to differentiate, which is what makes it
    minutes per configuration; nothing here needs a derivative, so this is the
    same enumeration at a fraction of the cost.
    """
    n = len(quats)
    out = []
    for i in range(n):
        others = [j for j in range(n) if j != i]
        Nval = {}
        for j in others:
            Rij = D.mat_num(quats[i], quats[j])
            for k in range(3):
                col = [Rij[r][k] for r in range(3)]
                for sgn in (1, -1):
                    Nval[(j, k, sgn)] = [sgn * c for c in col]
        keys = list(Nval)
        groups = [(kk,) for kk in keys] + list(itertools.combinations(keys, 2))
        for g in groups:
            got = D.min_l1_argmin([Nval[k] for k in g])
            if got is None:
                continue
            val, lam, v = got
            sig = D.l1_signs(v)
            Z = [c for c in range(3) if sig[c] == 0]
            if len(g) == 1 and Z:
                continue                      # kink: degenerate, excluded
            if len(g) == 2 and len(Z) > 1:
                continue
            c0 = Z[0] if Z else None
            out.append({'frame': i, 'group': g, 'sig': sig, 'c0': c0,
                        'tight': val == 1})
    return out


def tight_count(quats):
    return sum(1 for g in groups_at(quats) if g['tight'])


def arc_quats(name, s):
    a0, vv, lo, hi = M.ARCS[name]
    return M.BASE + [M.q_of([a0[i] + s*vv[i] for i in range(3)])]


def solve_arc(name, s0, verbose=True):
    """Candidate special parameters on one arc, by roots then verification."""
    a0, vv, lo, hi = M.ARCS[name]
    quats = arc_quats(name, s0)
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    ncols = len(pt)
    d = [F(0)]*ncols
    for k in range(3):
        d[ncols-3+k] = vv[k]                  # the sixth cube's three coordinates
    gs = groups_at(quats)
    loose = [g for g in gs if not g['tight']]
    base_tight = len(gs) - len(loose)
    mov = len(quats) - 1
    # Only groups involving the MOVING cube can change along the arc; the rest
    # are constant in t, which the polynomial confirms by coming out degree 0.
    loose = [g for g in loose
             if g['frame'] == mov or any(x[0] == mov for x in g['group'])]
    # A size-2 group whose minimiser is INTERIOR has no active coordinate (c0 is
    # None) and branch_numerator does not cover it: that formula is the
    # breakpoint branch.  Such a group can still go tight -- and when it does the
    # minimiser moves TO a breakpoint, so the branch to continue is not the one
    # frozen here.  Counted and reported, never silently dropped.
    unevaluated = [g for g in loose if len(g['group']) == 2 and g['c0'] is None]
    loose = [g for g in loose if not (len(g['group']) == 2 and g['c0'] is None)]
    if verbose:
        print('%s  s0=%-8s  groups %d | tight %d | loose-on-moving-cube %d | '
              'UNEVALUATED %d (interior minimiser, no branch)'
              % (name, s0, len(gs), base_tight, len(loose), len(unevaluated)),
              flush=True)
    cand = collections.Counter()
    polys = inrange = irrational = 0
    tvar = sp.Symbol('t')
    for g in loose:
        key = {'frame': g['frame'], 'group': g['group'],
               'sig': g['sig'], 'c0': g['c0']}
        try:
            co = W.on_line(key, quats[0], pt, d)
        except Exception:
            continue
        polys += 1
        if len(co) < 2:
            continue
        # PRUNE BEFORE FACTORING.  _rational_roots enumerates divisors of the
        # constant term, which is the expensive step and is wasted on every
        # polynomial with no root inside the arc's extent -- the overwhelming
        # majority.  Sturm's count_roots answers "any real root in [a,b]?" without
        # factoring anything, so ask that first.  Measured: the unpruned version
        # spent an hour of CPU and did not finish; the cost was in the method's
        # choice of work order, not in the problem.
        try:
            P = sp.Poly([sp.Rational(c) for c in reversed(co)], tvar)
            if P.degree() < 1:
                continue
            nr = P.count_roots(sp.Rational(lo - s0), sp.Rational(hi - s0))
        except Exception:
            nr = 1                            # cannot prune -> do the full work
        if nr == 0:
            continue
        inrange += 1
        roots = D._rational_roots([sp.Rational(c) for c in co])
        rat = 0
        for r in roots:
            v = s0 + F(str(r))
            if lo <= v <= hi:
                cand[v] += 1
                rat += 1
        if rat < nr:
            irrational += int(nr) - rat       # int(): count_roots returns sympy Integer
    if verbose:
        print('   %d polynomials | %d with a real root inside the extent | '
              '%d distinct rational candidates | %d roots IRRATIONAL '
              '(algebraic, not testable by rational evaluation)'
              % (polys, inrange, len(cand), irrational), flush=True)
    # VERIFY: a candidate is real only if the tight count actually rises there
    rows = []
    for s in sorted(cand):
        if not (lo <= s <= hi):
            continue
        try:
            t = tight_count(arc_quats(name, s))
        except Exception:
            continue
        cnt = None
        try:
            cnt = str(D.count_at(D.point_of(arc_quats(name, s)), len(quats)))
        except Exception:
            pass
        rows.append({'s': str(s), 'predicted_by': int(cand[s]), 'tight': int(t),
                     'baseline': int(base_tight), 'rises': bool(t > base_tight),
                     'region_count': cnt})
        if verbose and t > base_tight:
            print('   s=%-10s tight %d (baseline %d)  <== SPECIAL'
                  % (s, t, base_tight), flush=True)
    # SAMPLED CROSS-CHECK -- and measurement says it is NEARLY POWERLESS, which
    # is recorded here rather than quietly relied on.
    #
    # Special points are MEASURE ZERO in the parameter.  A 41-point rational
    # sweep can only find one by landing exactly on it, which happens essentially
    # never except at the endpoints it samples by construction.  Measured: on arc
    # D the sweep found 0 of the 3 special points the solve found; on arc A it
    # found 1 of 2, and that one is the extent's upper endpoint.
    #
    # So "0 rises not proposed by the solve" is close to uninformative and MUST
    # NOT be read as evidence that nothing was missed.  What would actually
    # detect a miss is covering the unevaluated groups; nothing here does that.
    # Kept because a hit would be real information, and because writing down that
    # a check is weak is cheaper than rediscovering it later.
    swept, K = [], 40
    for i in range(K + 1):
        s = lo + (hi - lo) * F(i, K)
        try:
            t = tight_count(arc_quats(name, s))
        except Exception:
            continue
        if t > base_tight:
            swept.append({'s': str(s), 'tight': int(t)})
    proposed = {r['s'] for r in rows}
    missed = [x for x in swept if x['s'] not in proposed]
    if verbose and missed:
        print('   sweep found %d rise(s) the solve did NOT propose: %s'
              % (len(missed), [x['s'] for x in missed]), flush=True)
    return {'arc': name, 's0': str(s0), 'extent': [str(lo), str(hi)],
            'baseline_tight': base_tight, 'n_loose_evaluated': len(loose),
            'n_unevaluated': len(unevaluated),
            'n_irrational_roots_in_extent': int(irrational),
            'irrational_note': ('a special point at an irrational parameter cannot '
                                'be verified by evaluating there with rational '
                                'arithmetic. Counted, not ignored.'),
            'unevaluated_note': ('size-2 groups with an interior minimiser; '
                                 'branch_numerator covers only the breakpoint '
                                 'branch. These could hide a special point.'),
            'candidates_in_extent': rows,
            'special': [r['s'] for r in rows if r['rises']],
            'sampled_crosscheck': {'points': K + 1, 'rises_found': swept,
                                   'not_proposed_by_solve': missed,
                                   'IS_NOT_THE_METHOD': 'a sample can find a miss, never rule one out',
                                   'POWER_IS_NEAR_ZERO': ('special points are measure zero; this sweep '
                                       'found 0 of 3 on arc D and 1 of 2 on arc A (that one an endpoint). '
                                       '"0 not proposed" is NOT evidence that nothing was missed.')}}


def main():
    which = [a for a in sys.argv[1:] if a in M.ARCS] or ['D']
    out = {'what': 'special points of the 727 arcs, by solving the wall polynomials',
           'control': 'arc D must return s = 0, the 727 record',
           'method': ('roots of each loose condition restricted to the arc line, '
                      'then VERIFIED by recomputing min_l1_argmin -- a frozen '
                      'branch locates candidates, not answers'),
           'arcs': {}}
    p = os.path.join(ROOT, 'data', 'arc_special.json')
    if os.path.exists(p):                     # merge, never replace
        try:
            prev = json.load(open(p))
            if isinstance(prev.get('arcs'), dict):
                out['arcs'].update(prev['arcs'])
        except Exception:
            pass
    S0 = {'D': F(1, 8), 'A': F(3), 'B': F(1, 2), 'C': F(2)}
    for name in which:
        out['arcs'][name] = solve_arc(name, S0[name])
        json.dump(out, open(p, 'w'), indent=1)
    print('written data/arc_special.json')


if __name__ == '__main__':
    main()
