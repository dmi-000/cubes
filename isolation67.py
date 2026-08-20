#!/usr/bin/env python3
"""Is each 67 an ISOLATED maximiser?  Decided by enumerating the faces of the
wall arrangement, not by probing directions.

WHY `dimension67.py` IS NOT ENOUGH.  It reports candidate dim 0 for both 67s,
which says only that no direction keeps EVERY wall satisfied.  Isolation is a
statement about the COUNT: a direction that crosses walls whose count changes
cancel would preserve 67 while lying outside null(J).  At the golden 67 that gap
is wide open -- all 9 walls came back `entangled`, meaning no direction crosses
one of them alone, so not a single delta was ever measured there.

WHAT MAKES THIS EXACT.  The count is constant on each face of the wall
arrangement, so "is there another 67 nearby" is a question about finitely many
faces, each of which needs ONE evaluation.  Enumerating them is a solve; picking
directions and stepping is a sample, and a sample yields a lower bound forever.

A face is a sign vector sigma in {-1,0,+1}^m: the relatively open cone
{d : sign(g_i . d) = sigma_i}.  Realizability is decided exactly by
Fourier-Motzkin over Q(sqrt d) -- with a WITNESS, which is what gets counted.
Prefix pruning keeps this far below the nominal 3^m.

VERDICT semantics, kept deliberately three-valued:
    isolated      every non-zero face counts < 67
    NOT isolated  some non-zero face counts 67 -> by Postscript 80a's dichotomy
                  (finite or uncountable, never countably infinite) there are
                  then uncountably many 67s
    unresolved    faces whose count disagreed across step sizes, or that the
                  engine's overflow budget rejected.  Counted and reported
                  separately; an unevaluated face is NOT scored as "< 67".
"""
import json, os, sys, time
import provenance
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dimension as D
from qfield import Q
from dimension67 import RECORDS
from epscount import count_eps

# --eps: infinitesimal displacement instead of adaptive halving (see epscount.py)
USE_EPS = '--eps' in sys.argv

EPS = (F(1, 64), F(1, 256), F(1, 1024))

# ADAPTIVE STEP.  A face's count is the count just outside the vertex, i.e. the
# limit as eps -> 0.  A fixed eps measures that only if the step stays inside the
# face, and it need not: the walls through the vertex are the 60-72 TIGHT
# conditions, but the loose conditions are walls too, sitting at a positive
# distance, and a coarse step crosses them.  The first golden run left 333 of
# 2196 faces disagreeing across three fixed steps, and in every one it was the
# LARGEST step that dissented while the two smaller ones agreed -- the signature
# of leaving the face, not of an ambiguous face.
#
# So shrink until two consecutive steps agree, and stop at the engine's overflow
# budget rather than pretending past it.  A face that never stabilises is
# reported unresolved with its whole sequence; it is NOT scored as "< 67".
EPS_CHAIN = tuple(F(1, 1 << k) for k in range(6, 22))


# ------------------------------------------------------- exact strict feasibility
def _simplest_between(lo, hi):
    """The rational of SMALLEST DENOMINATOR strictly inside (lo, hi).

    Fourier-Motzkin only needs SOME interior point of a cone, and the midpoint --
    the obvious choice -- is a bad one: midpoints of rationals with unrelated
    denominators compound through the recursion, and the witness direction that
    comes out then has huge integer coordinates.  Measured 2026-08-18 on the 727
    extension chambers: 10 of 24 witnesses had max |component| between 2 865 and
    13 528 and were REFUSED by the counting engine's overflow budget, while all 14
    that fit had max |component| <= 178.  The chambers were fine; the witnesses
    were not.  A cone is represented by any interior point, so choose the cheapest.

    Classic continued-fraction descent: if an integer lies strictly inside, it is
    simplest; otherwise both ends share a floor, and the simplest point is that
    floor plus the reciprocal of the simplest point of the reciprocal interval.
    """
    import math
    if lo > hi:
        lo, hi = hi, lo
    n = math.floor(lo) + 1
    if n < hi:
        return F(n)                      # an integer is inside: simplest possible
    fl = math.floor(lo)
    # No integer inside, so both ends share the floor.  Write x = fl + 1/y; the
    # y-interval is (1/(hi-fl), 1/(lo-fl)), and when lo is EXACTLY the floor that
    # upper bound is infinite -- the case that divided by zero on first write.
    a = F(1) / (hi - fl)
    if lo == fl:
        return fl + F(1) / F(math.floor(a) + 1)
    return fl + F(1) / _simplest_between(a, F(1) / (lo - fl))


def _pick(lo, hi):
    """an interior point of (lo, hi), preferring small height.

    Only the pure-rational case is optimised; over Q(sqrt d) "simplest
    denominator" is not defined and the midpoint is kept, so the two 67 runs are
    bit-for-bit unchanged.
    """
    rational = all(isinstance(v, (int, F)) or v is None for v in (lo, hi))
    if not rational:
        if lo is None and hi is None: return 0
        if lo is None: return hi - 1
        if hi is None: return lo + 1
        return (lo + hi) / 2
    if lo is None and hi is None:
        return F(0)
    import math
    if lo is None:
        return F(math.floor(hi) - 1)          # integer, strictly below hi
    if hi is None:
        return F(math.floor(lo) + 1)          # integer, strictly above lo
    return _simplest_between(F(lo), F(hi))


def _fm_fourier_motzkin(rows, nv):
    """Witness y with c.y > 0 for every row c (length nv), or None.

    THE ORIGINAL IMPLEMENTATION, KEPT DELIBERATELY.  `_fm` below now dispatches
    to the exact rational LP, which is faster and vastly lighter (P147). This
    function is retained, and MUST be retained, for two reasons:

      1. It is the independent second implementation that the LP is validated
         against. `exactlp.py` calls THIS NAME explicitly, never `_fm`. If it
         called `_fm` after the swap, the comparison would run the LP against
         itself and agree perfectly on everything forever -- a gate whose two
         sides are identical strings (FAILURE_MODES 2). The rename is what makes
         the gate keep meaning.
      2. Its recursion is the reference definition of the decision being made.

    Do not delete it because it is unused by the campaign; being unused by the
    campaign is the point.
    """

    # Homogeneous strict Fourier-Motzkin.  The combination rule is the usual one:
    # from c_p[k] y_k > -r_p.y' and c_n[k] y_k > -r_n.y' with c_p[k] > 0 > c_n[k],
    # a y_k exists iff  c_p[k]*r_n + |c_n[k]|*r_p  > 0.
    if nv == 0:
        return [] if not rows else None          # any surviving row reads 0 > 0
    k = nv - 1
    pos = [r for r in rows if r[k] > 0]
    neg = [r for r in rows if r[k] < 0]
    zer = [r for r in rows if r[k] == 0]
    nxt = [r[:k] for r in zer]
    for p in pos:
        for n in neg:
            nxt.append([p[k] * n[t] + (-n[k]) * p[t] for t in range(k)])
    sub = _fm_fourier_motzkin(nxt, k)
    if sub is None:
        return None
    # back-substitute: strictly between the induced bounds
    lo = hi = None
    for p in pos:
        v = -sum(p[t] * sub[t] for t in range(k)) / p[k]
        lo = v if lo is None or v > lo else lo
    for n in neg:
        v = -sum(n[t] * sub[t] for t in range(k)) / n[k]
        hi = v if hi is None or v < hi else hi
    y = _pick(lo, hi)
    return sub + [y]


# ---------------------------------------------------------------------------
# The decision procedure every caller uses.
#
# Swapped from Fourier-Motzkin to the exact rational LP on 2026-08-20, per
# Postscript 147 and `specs/EXACTLP_SPEC.md`. Both return an exact rational
# witness or None, so this is a pure substitution at every call site
# (`arrangement.py`, `growth727.py`, `isolation_gate.py`, `faces` below).
#
# WHY, in one line each, all measured rather than assumed:
#   correctness  237 668 real decided candidates, zero disagreements with FM
#                across ckpt183 / ckpt393 / ckpt727.
#   memory       FM's tail peaked at 7 449 MB and exhausted this machine; the
#                LP held <= 70 MB over the same instances. This, not speed, is
#                what made the 727 campaign impossible here.
#   stalls       one hard instance no longer freezes a whole stage.
#
# NO FLOATING POINT enters the decision on either path -- the project-wide
# invariant, and the reason a simplex was written rather than a library called.
#
# To fall back, set USE_EXACT_LP = False; the reference implementation above is
# retained permanently and must not be deleted (see its docstring).
USE_EXACT_LP = True


def _rows_are_rational(rows):
    """True when every coefficient is an ordinary rational.

    THE LP IS RATIONAL-ONLY.  `feasible_strict` converts each coefficient with
    `Fraction(...)`; Fourier-Motzkin never converts anything, using only the
    arithmetic and ordering the elements themselves provide. That is why FM
    works unchanged over Q(sqrt d) and the LP does not.

    Found on 2026-08-20 by `isolation_gate.py` immediately after the swap: the
    gate raised TypeError from `F(c[j])` on the golden (Q(sqrt 5)) case. The
    validation behind P147 -- 237 668 instances from ckpt_183 / ckpt_393 /
    ckpt_727 -- is entirely RATIONAL data, so it certified the LP only on the
    field it was tested on. The irrational records were never in that sample.
    """
    from numbers import Rational
    return all(isinstance(x, Rational) for r in rows for x in r)


def _fm(rows, nv):
    """Witness y with c.y > 0 for every row c (length nv), or None.

    Dispatches to the exact rational LP where it applies (P147) and to
    Fourier-Motzkin otherwise. The fallback is not a performance compromise: over
    Q(sqrt d) the LP is not merely slower, it is inapplicable.
    """
    if USE_EXACT_LP and _rows_are_rational(rows):
        from exactlp import feasible_strict
        return feasible_strict(rows, nv)
    return _fm_fourier_motzkin(rows, nv)


def faces(walls, ncols, zero, log):
    """every realizable non-zero face, as (sigma, witness direction)"""
    out = []
    m = len(walls)

    def rec(i, sigma, eqs, ineqs):
        if i == m:
            if all(s == 0 for s in sigma):
                return                                    # the vertex itself
            ns = D.nullspace(eqs, ncols) if eqs else None
            if eqs and not ns:
                return
            basis = ns if eqs else [[(zero + 1) if t == c else zero
                                     for t in range(ncols)] for c in range(ncols)]
            rows = [[sum(h[t] * b[t] for t in range(ncols)) for b in basis]
                    for h in ineqs]
            y = _fm(rows, len(basis))
            if y is None:
                return
            d = [sum(y[j] * basis[j][t] for j in range(len(basis)))
                 for t in range(ncols)]
            if all(x == 0 for x in d):
                return
            out.append((tuple(sigma), d))
            return
        # PRUNE on the prefix: an infeasible prefix cannot become feasible.
        for s in (0, 1, -1):
            e2 = eqs + [walls[i]] if s == 0 else eqs
            i2 = ineqs if s == 0 else ineqs + [
                walls[i] if s == 1 else [-x for x in walls[i]]]
            if s != 0 or True:
                ns = D.nullspace(e2, ncols) if e2 else None
                if e2 and not ns:
                    continue
                basis = ns if e2 else [[(zero + 1) if t == c else zero
                                        for t in range(ncols)] for c in range(ncols)]
                rows = [[sum(h[t] * b[t] for t in range(ncols)) for b in basis]
                        for h in i2]
                if rows and _fm(rows, len(basis)) is None:
                    continue
            rec(i + 1, sigma + [s], e2, i2)

    rec(0, [], [], [])
    print('   %d realizable non-zero faces of %d walls in R^%d'
          % (len(out), m, ncols), file=log, flush=True)
    return out


def run(d, name, quats, log):
    D.set_field(d)
    D.BUDGET[0] = 0
    zero = Q(0, 0, d)
    qs = [tuple(Q(F(p), F(q), d) for p, q in quat) for quat in quats]
    D.QZERO[:] = [qs[0]]
    pt = []
    for q in qs[1:]:
        pt += D.cayley_of(q)
    ncols = 3 * (len(qs) - 1)
    base = D.count_at(pt, len(qs))
    print('%s 67 over Q(sqrt%d): count_at -> %s' % (name, d, base), file=log, flush=True)
    if base != 67:
        return {'name': name, 'd': d, 'ABORT': 'count_at gave %s' % base}

    vars_ = __import__('sympy').symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, qs[0])
    tight, loose = D.cached_conditions(Rs, len(qs), vars_, pt,
                                       D.quats_of(pt, qs[0]), qs[0])
    good = [t for t in tight if not t['degenerate']]

    def _norm(g):
        piv = next((x for x in g if x != 0), None)
        return tuple(str(x / piv) for x in g) if piv is not None else None
    seen, walls = {}, []
    for t in good:
        k = _norm(t['grad'])
        if k is not None and k not in seen:
            seen[k] = True
            walls.append(t['grad'])
    print('   %d tight conditions -> %d distinct walls' % (len(good), len(walls)),
          file=log, flush=True)

    t0 = time.time()
    fs = faces(walls, ncols, zero, log)
    hits, unresolved, by_count = [], [], {}
    steps_used = {}
    per_face = []          # (codimension, count) for EVERY face
    for sigma, dvec in fs:
        dv = D.normalize_dir(dvec)
        if USE_EPS:
            # NO STEP SIZE AT ALL: eps is an infinitesimal, so this IS the
            # eps -> 0 limit.  There is nothing to stabilise and nothing that
            # can leave the face, so the only failure mode left is a refusal.
            c = count_eps(pt, dv, d, qs[0])
            if c is None:
                unresolved.append({'sigma': list(sigma), 'vals': [None],
                                   'eps': ['infinitesimal']})
                continue
            steps_used[1] = steps_used.get(1, 0) + 1
            by_count[c] = by_count.get(c, 0) + 1
            per_face.append({'codim': sum(1 for x in sigma if x == 0), 'count': c})
            if c >= base:
                hits.append({'sigma': list(sigma), 'count': c,
                             'dir': [str(x) for x in dv]})
            continue
        vals, c = [], None
        for e in EPS_CHAIN:
            v = D.count_at(pt, len(qs), dv, e)
            vals.append(v)
            if v is None:
                break                      # budget reached: stop, do not guess
            if len(vals) >= 2 and vals[-2] == v:
                c = v
                break
        if c is None:
            unresolved.append({'sigma': list(sigma), 'vals': vals,
                               'eps': [str(e) for e in EPS_CHAIN[:len(vals)]]})
            continue
        steps_used[len(vals)] = steps_used.get(len(vals), 0) + 1
        by_count[c] = by_count.get(c, 0) + 1
        if c >= base:
            hits.append({'sigma': list(sigma), 'count': c,
                         'dir': [str(x) for x in dv]})
    verdict = ('NOT ISOLATED' if hits else
               ('ISOLATED' if not unresolved else 'ISOLATED on evaluated faces'))
    print('   faces by count: %s' % dict(sorted(by_count.items(), reverse=True)),
          file=log, flush=True)
    print('   %s -- %d faces reaching %d, %d unresolved, %d budget rejects, %.0fs'
          % (verdict, len(hits), base, len(unresolved), D.BUDGET[0],
             time.time() - t0), file=log, flush=True)
    print('   steps to stabilise (eps halvings from 1/64): %s'
          % dict(sorted(steps_used.items())), file=log, flush=True)
    return {'name': name, 'd': d, 'count': base, 'walls': len(walls),
            'per_face': per_face,
            'faces': len(fs), 'verdict': verdict, 'hits': hits,
            'n_hits': len(hits), 'unresolved': len(unresolved),
            'steps_to_stabilise': {str(k): v for k, v in sorted(steps_used.items())},
            'unresolved_detail': unresolved, 'budget_rejects': D.BUDGET[0],
            'by_count': {str(k): v for k, v in sorted(by_count.items())},
            'secs': round(time.time() - t0, 1)}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    log = open(os.path.join(here, 'isolation67%s.log' % ('_eps' if USE_EPS else '')), 'a')
    print('\n===== %s' % time.strftime('%Y-%m-%d %H:%M:%S'), file=log, flush=True)
    out = []
    for d, (name, quats) in sorted(RECORDS.items()):
        out.append(run(d, name, quats, log))
        json.dump(out, open(os.path.join(here, 'isolation67%s.json' % ('_eps' if USE_EPS else '')), 'w'), indent=1)
    provenance.stamp(os.path.join(here, 'isolation67%s.json' % ('_eps' if USE_EPS else '')),
                     inputs=[os.path.join(here, 'cube_regions_eps' if USE_EPS
                                          else 'cube_regions_q2w')],
                     note='face enumeration of both 67s; --eps uses the '
                          'infinitesimal engine and has no step size')
    for r in out:
        print('%-12s %s' % (r['name'], r.get('verdict', r.get('ABORT'))),
              file=log, flush=True)


if __name__ == '__main__':
    main()
