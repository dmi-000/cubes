#!/usr/bin/env python3
"""SOLVE the ends of every continuum line still carrying sampled bounds.

[P183]/[OQ 13] audited the project's continua and found endpoints solved only for
727. That audit was incomplete: `n78_ends.py` (2026-08-08) had already solved both
ends of 1217 and the upper end of 1895 — on their CAYLEY-AXIS lines. What remains
unsolved is everything else, and this closes what is reachable:

    n=9  2785  k-family line              both ends        NEVER SOLVED
    n=7  1217  13-pair curve ([P182])     both ends        sampled only
    n=9  2785  13-pair curve, base 1      both ends        sampled only

METHOD, and why it is a solve. A W4 wall meets the line where a free-cube face plane
passes through a base triple point; on a line that condition is a QUADRATIC in the
line parameter, so its roots live in Q(sqrt d) and are exact. Enumerate every such
quadratic and every root: that is a FINITE EXACT list of every place the count can
possibly change, with no step size anywhere.

The endpoint is NOT the nearest root. A first version assumed it was and the gate
caught it: the nearest root below 1217's record sits at -0.0105 and the count AT it
is still 1217. [METHODS 7](METHODS.md) says exactly this — every boundary is a
coincidence boundary, but MOST COINCIDENCES ARE NOT BOUNDARIES. So the roots only
bracket; the count decides. Walking outward from the record, the count is probed at
one rational point strictly inside each successive inter-root interval, and the end
is the root separating the last interval holding the target from the first that does
not. The interior probe is the SIMPLEST rational in the interval, not its midpoint
([METHODS 15](METHODS.md)) — midpoints of roots with unrelated denominators compound
straight past the engine's height budget.

Then the endpoint itself is built exactly in Z[sqrt d] and counted with
`cube_regions_q2w --d`, which decides open vs closed.

WHY NOT `solve_ends.py` for the evaluation: it locates roots correctly but evaluates
via `q_of`, which needs a rational s, so every IRRATIONAL root silently returns None
— and None reads as "no result" beside real counts. Rational roots evaluate, so its
output looks partially fine. Endpoint counts here go through the exact Z[sqrt d]
path instead.

W3 ends (quartics) stay out of reach unless the quartic factors; they are reported
as unreached rather than omitted.
"""
import os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catcache import catalogue
from simplest import simplest_between, _selftest_simplest
from n78_ends import w4_polys, squarefree, qstr, run
import wall_params as W

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C6 = BASE + [(7,14,1,-5)]
C7 = C6 + [(4,-3,-4,-4)]
C8 = C7 + [(24,-24,24,-61)]
MAXWALK = 60          # roots to walk outward before declaring the end unreached


def exact_roots(p):
    """both roots of c + b*s + a*s^2 as (rp, rq, d): value = rp + rq*sqrt(d)"""
    c, b, a = p
    if a == 0:
        return []
    disc = b*b - 4*a*c
    if disc < 0:
        return []
    num, den = disc.numerator, disc.denominator
    m, d = squarefree(num * den)            # sqrt(disc) = m*sqrt(d)/den
    out = []
    for sgn in (1, -1):
        out.append((F(-b, 2*a), F(sgn*m, den)/(2*a), d))
    return out


def val(r):
    rp, rq, d = r
    return float(rp) + float(rq) * (d ** 0.5)


def exact_of(item):
    """Recover the exact (rp, rq, d) for ONE root, matching its value."""
    from n78_ends import squarefree
    v, p = item
    c, b, a = p
    disc = b*b - 4*a*c
    m, d = squarefree(disc.numerator * disc.denominator)
    den = disc.denominator
    for sgn in (1, -1):
        rp, rq = F(-b, 2*a), F(sgn*m, den)/(2*a)
        if abs(float(rp) + float(rq)*(d**0.5) - float(v)) < 1e-9:
            return rp, rq, d
    raise ValueError('no exact form matched root value %s' % v)


def count_at(base, a0, dv, r):
    """exact count at a0 + r*dv, with r = rp + rq*sqrt(d), in Z[sqrt d]"""
    rp, rq, d = r
    cay = [(F(a0[i]) + rp*F(dv[i]), rq*F(dv[i])) for i in range(3)]
    qs, mag = qstr([(F(1), F(0))] + cay)
    base_s = ";".join(",".join("%d:0" % v for v in q) for q in base)
    return run(base_s + ";" + qs, d), mag


def root_values(p, prec=60):
    """Both root VALUES of c+bx+ax^2 as Fractions accurate to ~10^-prec.

    PERFORMANCE, and it is not a micro-optimisation. `exact_roots` calls
    `n78_ends.squarefree`, which trial-divides to sqrt(disc). At n=9 discriminants
    were small; at n=10 (a0 denominator 19, dv up to 220) they reach ~1e18, so each
    call is ~1e9 iterations and the walk over ~38 000 roots never finishes — an
    n=10 endpoint run burned 37 minutes without emitting a line while the whole
    catalogue it depends on takes 11 seconds.

    The walk only needs root values, to ORDER the roots and to pick a rational
    between consecutive ones. The exact Z[sqrt d] form is needed for exactly one
    root — the endpoint — so it is deferred to there.
    """
    import math
    c, b, a = p
    if a == 0:
        return []
    disc = b*b - 4*a*c
    if disc < 0:
        return []
    scale = 10 ** prec
    n, d = disc.numerator, disc.denominator
    sq = F(math.isqrt(n * scale * scale // d), scale)      # sqrt(disc), ~1e-prec
    return [(-b + sq) / (2*a), (-b - sq) / (2*a)]


def approx(r, prec=60):
    """r = rp + rq*sqrt(d) as a Fraction, accurate to ~10^-prec"""
    rp, rq, d = r
    import math
    scale = 10 ** prec
    root = F(math.isqrt(d * scale * scale), scale)
    return rp + rq * root


def q_of_rat(a0, dv, s):
    from math import gcd
    c = [F(a0[i]) + s*F(dv[i]) for i in range(3)]
    L = 1
    for v in c:
        L = L*v.denominator//gcd(L, v.denominator)
    iq = [L] + [int(v*L) for v in c]
    g = 0
    for v in iq:
        g = gcd(g, abs(v))
    return tuple(v//g for v in iq)


def count_rat(base, a0, dv, s):
    import json, subprocess
    cfg = list(base) + [q_of_rat(a0, dv, s)]
    st = ";".join(",".join(map(str, q)) for q in cfg)
    m = max(abs(v) for q in cfg for v in q)
    cmd = (["./cube_regions_n", "--quats", st] if m <= 512
           else ["./cube_regions_q2w", "--d", "0", "--quats", st])
    try:
        return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)["bounded"]
    except Exception:
        return None


def ends_of(base, a0, dv, target, label, expect=None):
    pts, lines = catalogue(base)
    polys = w4_polys(a0, dv, pts)
    # Values only here — the exact Q(sqrt d) form is recovered for the endpoint alone
    # (see root_values: squarefree() is O(sqrt(disc)) and unusable at n=10 scale).
    #
    # BOTH wall types. Enumerating only W4 caused a real error: the 1217 level set is
    # PUNCTURED, and a walk that steps over the puncture reports the outer edge of a
    # further component as if it were the record's own endpoint. A component bounded
    # by a W3 (edge-edge) wall would be missed the same way, so W3 roots are included
    # as values. Their exact form needs the quartic factored (see `n8_lower.py`), so a
    # W3 endpoint is reported as a 1e-12 rational and flagged.
    vals = {}
    for p in polys:
        for v in root_values(p):
            vals.setdefault(v, ('W4', p))      # dedup by VALUE, not symbolic triple
    for v in W.w3_params(a0, dv, lines):
        vals.setdefault(F(v), ('W3', None))
    roots = sorted(vals.items(), key=lambda kv: kv[0])
    lo = [r for r in roots if r[0] < 0]
    hi = [r for r in roots if r[0] > 0]
    print('\n%s: %d triple points, %d W4 quadratics, %d distinct roots (%d below, %d above)'
          % (label, len(pts), len(polys), len(roots), len(lo), len(hi)), flush=True)
    if not lo or not hi:
        print('   record not bracketed by W4 roots on this line'); return

    def bisect_transition(seq, probe):
        """Index of a transition in `seq` by bisection, or None if the far end still holds.

        User's suggestion, and it is a genuine SOLVE rather than sampling: the roots
        are a finite exact list, so this bisects an INDEX, not a continuum. It costs
        O(log n) probes where the walk costs O(n) — the difference between 11 probes
        and 1 866 on the n=9 upper side.

        CAVEAT, and why it does not replace the walk: bisection assumes the predicate
        "count is still the target" is monotone along the ray, and it is NOT. The n=9
        k-line is one interval PUNCTURED at s=1/56, where the ninth cube duplicates a
        base cube; a bisection straddling that puncture can land on the wrong side of
        it. So this is used only to find SOME transition cheaply and bracket it; the
        first transition is then confirmed by walking inside that bracket.
        """
        if not seq:
            return None
        if probe(len(seq) - 1) == target:
            return None                      # target still holds at the far end
        lo_i, hi_i = 0, len(seq) - 1         # invariant: probe(lo_i)==target < hi_i
        if probe(0) != target:
            return 0
        while hi_i - lo_i > 1:
            mid = (lo_i + hi_i) // 2
            if probe(mid) == target:
                lo_i = mid
            else:
                hi_i = mid
        return hi_i

    def walk(side):
        """the outermost root still bounding a `target` interval — the END.

        OFF-BY-ONE, caught by the gate: the probe sits in the interval (prev_root,
        this_root), so a BAD probe means the count changed at PREV_ROOT, not at the
        root bounding the interval above. Returning the latter overshot 1217's upper
        end from 0.00255 to 0.0227 — one whole chamber out.
        """
        seq = list(reversed(lo)) if side == 'lower' else hi
        prev, prev_root = F(0), None
        probes = 0
        skipped = []
        for r in seq[:MAXWALK]:
            a = r[0]
            if a == prev:          # distinct (p,q,d) triples can denote the same value
                continue
            s_in = simplest_between(a, prev) if side == 'lower' else simplest_between(prev, a)
            c = count_rat(base, a0, dv, s_in)
            probes += 1
            if c is None:
                # An unevaluable probe is NOT a stop and NOT a change. Between two very
                # close roots the simplest rational necessarily has a large denominator,
                # so the configuration outruns even the wide engine — a property of the
                # interval, not of the count. Skip it, keep counting, and report how many
                # were skipped so the answer is qualified rather than silently truncated.
                skipped.append(s_in)
                prev, prev_root = a, r
                continue
            if c != target:
                if prev_root is None:
                    print('   %s: count already differs inside the FIRST interval'
                          % side, flush=True)
                if skipped:
                    print('   %s: %d interval(s) UNEVALUATED and skipped en route'
                          % (side, len(skipped)), flush=True)
                return prev_root, probes
            prev, prev_root = a, r
        if skipped:
            print('   %s: %d interval(s) UNEVALUATED and skipped' % (side, len(skipped)),
                  flush=True)
        return None, probes

    out = {}
    for name in ('lower', 'upper'):
        r, probes = walk(name)
        if r is None:
            print('   %-6s NOT FOUND within %d roots (%d probes) — unreached, not absent'
                  % (name, MAXWALK, probes), flush=True)
            continue
        kind = r[1][0]
        if kind == 'W3':
            print('   %-6s s = %.12f  (W3 quartic root; exact form needs the quartic '
                  'factored — see n8_lower.py)' % (name, float(r[0])), flush=True)
            print('          %d distinct walls crossed without the count changing'
                  % (probes - 1), flush=True)
            out[name] = (float(r[0]), None)
            continue
        rp, rq, d = exact_of((r[0], r[1][1]))
        c, mag = count_at(base, a0, dv, (rp, rq, d))
        print('   %-6s s = (%s) + (%s)sqrt(%d) = %.12f  height %d  count AT end: %s'
              % (name, rp, rq, d, float(r[0]), mag, c), flush=True)
        print('          %d distinct walls crossed between the record and this end '
              'WITHOUT the count changing (METHODS 7)' % (probes - 1), flush=True)
        out[name] = (float(r[0]), c)
    mid = F(0)
    inside = count_rat(base, a0, dv, mid)
    found = [k for k in ('lower', 'upper') if k in out]
    if not found:
        verdict = 'no end located — open/closed UNDETERMINED'
    else:
        ev = [k for k in found if isinstance(out[k][1], int)]
        opens = [k for k in ev if out[k][1] != target]
        # An end whose count could not be evaluated is UNDETERMINED, never "not open".
        verdict = ('%d of %d located end(s) OPEN; %d end(s) located but the count AT '
                   'them is UNEVALUABLE (engine height limit) — open/closed UNDETERMINED '
                   'there%s' % (len(opens), len(found), len(found) - len(ev),
                                '' if len(found) == 2 else '; the other end was NOT located'))
    print('   inside (s=0, the record): %s   %s' % (inside, verdict), flush=True)
    if expect:
        ok = all(abs(out[k][0] - v) < 1e-9 for k, v in expect.items())
        print('   GATE vs n78_ends: %s' % ('OK' if ok else 'MISMATCH %s' % out), flush=True)
        if not ok:
            sys.exit('gate failed')


if __name__ == '__main__':
    _selftest_simplest()
    # GATE: the known 1217 Cayley-axis ends must come back with their known values
    ends_of(C6, [F(-3,4), F(-1), F(-1)], [F(1), F(0), F(0)], 1217,
            'GATE n=7 1217, Cayley-axis line (1,0,0)',
            expect={'lower': -0.045258752093, 'upper': 0.002550224044})

    # n=9 2785, the k-family line: ninth cube (k,k,k-1,k) -> Cayley (1, 1-1/k, 1)
    ends_of(C8, [F(1), F(55,56), F(1)], [F(0), F(1), F(0)], 2785,
            'n=9 2785, k-family line (0,1,0)')

    # n=7 1217 on P182's 13-pair curve: tangent of t -> cube2*(1, t*(1,1,-1))
    def curve_dir(b, axis, t0):
        def qmul(p, q):
            w,x,y,z = p; e,f,g,h = q
            return (w*e-x*f-y*g-z*h, w*f+x*e+y*h-z*g,
                    w*g-x*h+y*e+z*f, w*h+x*g-y*f+z*e)
        h = F(1, 10**6)
        A = qmul(b, (1, t0*axis[0], t0*axis[1], t0*axis[2]))
        B = qmul(b, (1, (t0+h)*axis[0], (t0+h)*axis[1], (t0+h)*axis[2]))
        ca = [F(A[i+1], 1)/A[0] for i in range(3)]
        cb = [F(B[i+1], 1)/B[0] for i in range(3)]
        return [(cb[i]-ca[i])/h for i in range(3)]      # exact: the map is linear-fractional

    d7 = curve_dir((5,-1,-5,-5), (1,1,-1), F(-11,63))
    ends_of(C6, [F(-3,4), F(-1), F(-1)], d7, 1217,
            'n=7 1217, 13-pair curve (P182)')
