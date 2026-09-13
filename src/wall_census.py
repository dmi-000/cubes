#!/usr/bin/env python3
"""Which walls actually BOUND the count plateau -- a census, exact at every crossing.

THE QUESTION ([OPEN_QUESTIONS 33], opened by [P298]).  Every count-plateau tangent
number in this project was built from the premise that a first-order tangent must
lie in EVERY wall, so the candidate space is the null space of the wall gradients.
That premise is false: at n = 7 a direction crossing 7 of 51 walls preserves the
count, and of six wall crossings solved since, four left the count unchanged.  A
wall is a COINCIDENCE condition; crossing one changes the coincidence structure and
need not create or destroy a region.  So the plateau is bounded by a SUBSET of the
walls, and no method here had identified that subset.

WHAT THIS DOES.  Along each ray of a stated direction family: restrict every
condition to the ray, take ALL its real roots exactly, sort them into distinct
crossing points, and count the regions in each open interval between consecutive
crossings.  A crossing where exactly one WALL is active is attributable, and the
counts on its two sides are a verdict on that wall.

THE BRANCH CLOSURE, which the first version of this did not have.  A condition's
polynomial depends on which piece of a piecewise formula is active, the (sig, c0)
branch.  Freezing every branch at the base point is the worst available choice at
a record, because the record is the degenerate point: moving 1/1000 along e0 already
changes the active branch of 72 of 2338 keys.  So the key set is closed under
sampling -- solve, sample one point per interval, recompute the active keys there,
add what is new, repeat until a pass adds nothing.  On e0 the base's 2338 keys close
to 2700 and the crossing count rises from 15 to 23 in a window of 0.15.  Roots of a
branch that is not active anywhere near them are SPURIOUS and are dropped, not
counted; leaving them in would pad the census with walls that are not there.

WHY THE SAMPLE POINTS ARE EXACT AND NOT SMALL.  No step size appears anywhere.
Between two consecutive roots the count is constant, so any rational strictly inside
the interval carries the whole interval's value.  Isolating intervals are disjoint
by construction, and the simplest rational between two of them is as good as a
limit: the cell gets measured, not a point near a wall.  This is METHODS 14 obtained
for free by solving, and METHODS 15 in the choice of representative -- the first
version used a non-simplest rational and the engine refused four of its points.

SIGN, NOT MULTIPLICITY.  Whether a wall is genuinely crossed or merely touched is
decided by an exact rational sign test at the two flanking sample points.  Equal
signs mean even multiplicity: the condition becomes tight without the configuration
passing through the wall, and such a non-event cannot bound anything.

GATES.
  G1  count at t = 0 must equal the record.  An anchor outside every measurement
      here; if the base point is not the record the rest is about some other point.
  G2  CONSTANCY: in every interval, count at a point in its first third and one in
      its last third as well as at the primary point.  All must agree.  A
      disagreement means a wall is missing from the enumeration -- which no amount
      of agreement between root-finders could ever reveal.  G2 is what caught the
      frozen-branch defect: nine failures on the first full ray.
  G2N NEGATIVE CONTROL for G2 (`--control`): hide half the keys and G2 must FAIL.
      Its first form did not -- zero failures with 1339 of 2592 keys hidden -- which
      is why the check now probes the two ends of each interval rather than two
      neighbouring points.  A gate that cannot fail is [FAILURE_MODES 2].
  G3  every interval must be evaluable, or the refusal is COUNTED.  An unevaluable
      interval is reported as unevaluated, never as "no change".

SCOPE, STATED IN THE NUMBER'S OWN LABEL.  Each verdict is exact, but the POPULATION
is whatever these rays meet: a rate here is "k of m solved crossings on this
direction family", not a probability and not a statement about all walls.
"""
import sys, os, json, time, argparse, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE
import sympy as sp
import dimension as D
import wall_keys as W
import wall_solve as WS
import map_arcs as M

T = sp.Symbol('t')


# ---------------------------------------------------------------- roots on a ray

EPS = sp.Rational(1, 10**24)   # isolating-interval width demanded of the solver


def root_intervals(P, lo, hi):
    """Isolating intervals with RATIONAL endpoints for the real roots in [lo, hi].

    `Poly.intervals` is used rather than root objects because sympy returns a real
    root as whatever expression is smallest -- a Rational, a CRootOf, or a Rational
    times a CRootOf -- and only the interval form is uniform.  The endpoints are
    exact rationals, which is what the sample points between roots are built from.
    """
    try:
        ivs = P.sqf_part().intervals(sqf=True, eps=EPS,
                                     inf=sp.Rational(lo), sup=sp.Rational(hi))
    except Exception:
        return []
    out = []
    for iv in ivs:
        a, b = iv[0] if isinstance(iv[0], tuple) else iv
        out.append([F(int(a.p), int(a.q)), F(int(b.p), int(b.q))])
    return out


def cluster(roots):
    """Group (bounds, cond_index) pairs into distinct crossing points.

    DISJOINT INTERVALS PROVE DISTINCTNESS.  Two roots whose isolating intervals
    still overlap at width 1e-24 are treated as ONE crossing -- the conservative
    direction, since the only consequence is that the crossing becomes
    unattributable rather than attributed to the wrong wall.  The smallest feature
    ever measured in these arrangements is ~1e-3 ([P292]), twenty-one orders above
    the resolution used here.
    """
    items = sorted(({'b': b, 'c': ci} for b, ci in roots),
                   key=lambda it: (it['b'][0], it['b'][1]))
    out = []
    for it in items:
        if out and it['b'][0] <= out[-1]['bounds'][1]:
            out[-1]['bounds'][1] = max(out[-1]['bounds'][1], it['b'][1])
            out[-1]['members'].append(it['c'])
        else:
            out.append({'bounds': list(it['b']), 'members': [it['c']]})
    return out


def simplest_in(a, b):
    """The rational with the SMALLEST DENOMINATOR strictly inside (a, b).

    Written here rather than reused from `map_arcs.simplest_between`, which
    returns a valid but not simplest rational on these inputs -- on the first
    interval of ray e0 it returned -2090843335179/13955710574720 for an interval
    of width 3.6e-4, and the engine refused the resulting quaternion.  That is
    METHODS 15 exactly: the refusal was a property of the REPRESENTATIVE, not of
    the cell.  Classic continued-fraction descent, gated below against known
    answers.
    """
    if a > b:
        a, b = b, a
    fa = a.numerator // a.denominator
    if a < fa + 1 < b:
        return F(fa + 1)
    if a == fa:                      # left endpoint integral: fa + 1/k
        k = (1 / (b - fa)).numerator // (1 / (b - fa)).denominator + 1
        return fa + F(1, k)
    return fa + 1 / simplest_in(1 / (b - fa), 1 / (a - fa))


def wall_id(P):
    """Canonical identity of the WALL a condition cuts on this ray.

    One geometric coincidence appears as several conditions: the sign-flipped
    normal is the same wall, and the pair (i, j) is enumerated from both cubes'
    frames.  On ray e0 every simple crossing carried exactly two conditions for
    that reason.  Two conditions cut the same wall on the ray iff their
    polynomials have the same roots, so the monic squarefree part is the identity.
    """
    Q = P.sqf_part().monic()
    return tuple(str(c) for c in Q.all_coeffs())


def concurrency_for(n, label, lo, hi):
    """The four-plane concurrency walls on one ray, from `concurrency_walls.py`.

    A SECOND WALL FAMILY, and one the project had never enumerated ([P304]).  It is
    read from the data file rather than recomputed: the enumeration is ~2 minutes a
    ray and is keyed by ray label, so the census can be rerun freely.  Isolating
    intervals are rebuilt here from the stored polynomial -- the polynomial is the
    deliverable, the roots are read off it.
    """
    path = os.path.join(ROOT, 'data', 'concurrency_walls_n%d.json' % n)
    if not os.path.exists(path):
        return []
    doc = json.load(open(path))
    ray = doc.get('rays', {}).get(label)
    if not ray:
        return []
    out = []
    for w in ray['walls']:
        P = sp.Poly([sp.Rational(c) for c in w['polynomial']], T)
        for b in root_intervals(P, lo, hi):
            out.append((b, ('concur', tuple(tuple(x) for x in w['planes'])), P))
    return out


def ckeys_at(quats):
    """The branch keys ACTIVE at one configuration: {key: tight?}.

    A key is (frame, group, sig, c0) -- the complete argument list of
    `dimension.branch_numerator`, which is to say the polynomial itself ([P288]).
    """
    out = {}
    for c in WS.conditions_on(quats):
        out[(c['frame'], tuple(c['group']), tuple(c['sig']), c['c0'])] = bool(c['tight'])
    return out


def build_poly(key, q0, pt, dirn):
    """The key's polynomial restricted to the ray, or None if it is constant."""
    k = {'frame': key[0], 'group': key[1], 'sig': list(key[2]), 'c0': key[3]}
    try:
        co = W.on_line(k, q0, pt, dirn)
    except Exception:
        return False                      # unbuildable, distinct from constant
    if len(co) < 2:
        return None
    return sp.Poly([sp.Rational(x) for x in reversed(co)], T)


# ---------------------------------------------------------------- the census

def census_ray(quats, dirn, label, lo, hi, verbose=True, drop=None, max_passes=6,
               concurrency=None):
    """One ray: every wall crossing on it, and what the count does at each.

    THE BRANCH PROBLEM, AND WHY THIS ITERATES.  A condition's polynomial depends
    on which piece of a piecewise formula is active -- the (sig, c0) branch -- and
    the first version of this census froze every branch at the base point.  At the
    record that is the worst possible choice: the record is the degenerate point,
    and moving off it by 1/1000 along e0 already changes the active branch of 72 of
    2338 keys.  The consequence is missing walls, and G2 duly caught it: nine
    constancy failures on the first full ray, which is the gate doing its job
    before any number was believed.

    THE FIX is a fixed point, not a smaller window.  Take the keys active at the
    base, solve, sample one point per interval, recompute the active keys THERE,
    and add whatever is new; repeat until a pass adds nothing.  The key set then
    contains every branch active anywhere on the ray, so no wall of the ray is
    missing from it.

    AND SPURIOUS ROOTS ARE DROPPED, NOT COUNTED.  A key's polynomial has roots
    where that branch is not the active one; those are not wall crossings and would
    otherwise pad the census with fake count-preserving walls.  A crossing counts
    only if at least one of its keys is active on one of the two sides, which is
    read off the same recomputation.
    """
    n = len(quats)
    t0 = time.time()
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    q0 = quats[0]

    def quats_at(s):
        return D.quats_of([pt[k] + s * dirn[k] for k in range(len(pt))], q0)

    def count_at(s):
        return D.count_at([pt[k] + s * dirn[k] for k in range(len(pt))], n)

    base_keys = ckeys_at(quats)
    if drop is not None:
        base_keys = {k: v for i, (k, v) in enumerate(sorted(base_keys.items(), key=str))
                     if i not in drop}
    keys = dict(base_keys)
    polys, unbuildable = {}, 0
    active_cache = {}
    passes = 0
    while True:
        passes += 1
        for k in keys:
            if k not in polys:
                P = build_poly(k, q0, pt, dirn)
                if P is False:
                    unbuildable += 1
                    P = None
                polys[k] = P
        roots = []
        for k, P in polys.items():
            if P is None:
                continue
            for b in root_intervals(P, lo, hi):
                roots.append((b, k))
        for b, k, P in (concurrency or []):      # the second wall family
            polys.setdefault(k, P)
            roots.append((b, k))
        cl = cluster(roots)
        edges = [F(str(lo))] + [b for c in cl for b in (c['bounds'][0], c['bounds'][1])] \
                + [F(str(hi))]
        pts = []
        for i in range(0, len(edges) - 1, 2):
            a, b = edges[i], edges[i + 1]
            pts.append(simplest_in(a, b) if a < b else None)

        # G2 IN ITS STRONG FORM, run every pass because it is also what STEERS the
        # next one.  The first version put its second sample between the interval's
        # lower edge and the primary point, and the negative control killed it: with
        # half the keys hidden it raised ZERO failures, because two nearby points sit
        # on the same side of a hidden wall.  It now takes a point from the FIRST
        # THIRD and one from the LAST THIRD of every interval, so a missed wall has to
        # hide in a third of a cell to survive.
        counts, second, budget = [], {}, 0
        for i, s in enumerate(pts):
            if s is None:
                counts.append(None)
                continue
            c = count_at(s)
            if c is None:
                budget += 1
            counts.append(c)
            a, b = edges[2 * i], edges[2 * i + 1]
            w = (b - a) / 3
            probes, seen = [], []
            for lo_, hi_ in ((a, a + w), (b - w, b)):
                if lo_ < hi_:
                    s2 = simplest_in(lo_, hi_)
                    if s2 != s:
                        probes.append(s2)
                        c2 = count_at(s2)
                        if c2 is not None:
                            seen.append((str(s2), c2))
            if seen:
                second[i] = {'primary': [str(s), c], 'probes': seen,
                             'agree': all(c2 == c for _, c2 in seen) and c is not None,
                             'probe_points': probes}

        # THE CLOSURE, and its REPAIR.  Ordinary closure recomputes the active keys
        # at one point per cell.  That is a fixed point of its own sampling and not a
        # certificate: at window 1.0 it converged in three passes and G2 still found
        # five cells with a wall inside.  So a cell that FAILS G2 also contributes its
        # two probe points to the closure -- the gate steers the search that the gate
        # then re-checks, and the loop ends only when it has nothing left to report.
        added = 0
        if drop is None and passes < max_passes:
            look = [s for s in pts if s is not None]
            for i, v in second.items():
                if not v['agree']:
                    look += v['probe_points']
            for s in look:
                if s in active_cache:
                    continue
                active_cache[s] = ckeys_at(quats_at(s))
                for k in active_cache[s]:
                    if k not in keys:
                        keys[k] = active_cache[s][k]
                        added += 1
        fails = sum(1 for v in second.values() if not v['agree'])
        if verbose:
            print('%-10s pass %d | %d keys | %d roots | %d crossings | %d new keys | '
                  'G2 fail %d  (%.0fs)'
                  % (label, passes, len(keys), len(roots), len(cl), added, fails,
                     time.time() - t0), flush=True)
        if (added == 0 and fails == 0) or passes >= max_passes:
            break

    for s in pts:                      # activity is needed at every sample point
        if s is not None and s not in active_cache:
            active_cache[s] = ckeys_at(quats_at(s))

    rows = []
    for j, c in enumerate(cl):
        before = counts[j] if j < len(counts) else None
        after = counts[j + 1] if j + 1 < len(counts) else None
        sbef = pts[j] if j < len(pts) else None
        saft = pts[j + 1] if j + 1 < len(pts) else None
        mem = sorted(set(c['members']), key=str)
        act_b = active_cache.get(sbef, {}) if sbef is not None else {}
        act_a = active_cache.get(saft, {}) if saft is not None else {}
        info = []
        for k in mem:
            P = polys.get(k)
            sign_change = None
            if P is not None and sbef is not None and saft is not None:
                v1 = P.eval(sp.Rational(sbef.numerator, sbef.denominator))
                v2 = P.eval(sp.Rational(saft.numerator, saft.denominator))
                sign_change = bool(sp.sign(v1) * sp.sign(v2) < 0)
            if k[0] == 'concur':
                info.append({'family': 'concurrency', 'planes': [list(x) for x in k[1]],
                             'cubes': sorted({x[0] for x in k[1]}),
                             'degree': P.degree() if P is not None else None,
                             'sign_change': sign_change,
                             'active_before': True, 'active_after': True})
            else:
                info.append({'family': 'coincidence',
                             'frame': k[0], 'group': [list(g) for g in k[1]],
                             'size': len(k[1]), 'sig': list(k[2]), 'c0': k[3],
                             'cubes': sorted({k[0]} | {g[0] for g in k[1]}),
                             'tight_at_base': base_keys.get(k),
                             'degree': P.degree() if P is not None else None,
                             'sign_change': sign_change,
                             'active_before': k in act_b, 'active_after': k in act_a})
        live = [w_ for w_, k in zip(info, mem)
                if w_['active_before'] or w_['active_after']]
        wids = {wall_id(polys[k]) for w_, k in zip(info, mem)
                if (w_['active_before'] or w_['active_after']) and polys.get(k) is not None}
        rows.append({
            'n_walls': len(wids),
            'spurious': not live,
            'bounds': [str(c['bounds'][0]), str(c['bounds'][1])],
            'decimal': float((c['bounds'][0] + c['bounds'][1]) / 2),
            'rational': (str(c['bounds'][0])
                         if c['bounds'][0] == c['bounds'][1] else None),
            'n_conditions': len(mem), 'n_active': len(live),
            'conditions': live or info,
            'count_before': before, 'count_after': after,
            'changes': (None if before is None or after is None
                        else bool(before != after)),
            'delta': (None if before is None or after is None else after - before),
        })
    return {'label': label, 'direction': [str(x) for x in dirn],
            'window': [str(lo), str(hi)], 'passes': passes,
            'n_keys': len(keys), 'n_keys_at_base': len(base_keys),
            'n_crossings': len(cl), 'unbuildable': unbuildable,
            'unevaluable_intervals': budget,
            'constancy_checks': {str(k): {kk: vv for kk, vv in v.items()
                                          if kk != 'probe_points'}
                                 for k, v in second.items()},
            'constancy_failures': sum(1 for v in second.values() if not v['agree']),
            'counts': counts, 'sample_points': [str(s) if s else None for s in pts],
            'crossings': rows, 'seconds': round(time.time() - t0, 1)}


def negative_control(quats, dirn, lo, hi, frac=0.5, seed=7):
    """G2 MUST FAIL when walls are hidden from it.

    A constancy check that cannot fail is not a check ([FAILURE_MODES 2]).  Here
    half the conditions are deleted before the roots are taken, so intervals get
    merged across walls that are really there.  If the two sample points inside a
    merged interval still always agree, the check is blind and every "0 failures"
    above is worthless.  Reported as the number of failures it raises: zero is the
    failure of this control, not its success.
    """
    conds = ckeys_at(quats)
    rng = random.Random(seed)
    drop = {i for i in range(len(conds)) if rng.random() < frac}
    r = census_ray(quats, dirn, 'CONTROL', lo, hi, verbose=False, drop=drop)
    return {'dropped': len(drop), 'of': len(conds),
            'crossings_seen': r['n_crossings'],
            'G2_checks': len(r['constancy_checks']),
            'G2_failures': r['constancy_failures'],
            'PASSES': bool(r['constancy_failures'] > 0)}


# ---------------------------------------------------------------- configurations

def record_quats(n):
    """The tower record at level n -- from `wall_keys.REC`, the project's one table.

    Deliberately not re-typed here.  A second copy of the records is a second
    thing to get wrong, and FAILURE_MODES 35 is precisely a comparison across two
    spellings of what was meant to be the same object.
    """
    if n not in W.REC:
        raise SystemExit('no record wired for n=%d in wall_keys.REC' % n)
    return list(W.REC[n])


def directions(nc, family, count, seed=1):
    """The stated direction family.  Named in the output, never left implicit.

    'axis'  every coordinate axis -- complete, and the only family for which
            "all of them" is a finite statement.
    'mixed' random entries in {-1,0,1}: deliberately NOT axis-aligned, because
            axis-aligned probes are one of the scope errors P298 catalogues.
    """
    out = []
    if family in ('axis', 'both'):
        for k in range(nc):
            d = [F(0)] * nc; d[k] = F(1)
            out.append(('e%d' % k, d))
    if family in ('mixed', 'both'):
        rng = random.Random(seed)
        for i in range(count):
            while True:
                d = [F(rng.choice((-1, 0, 0, 1))) for _ in range(nc)]
                if any(d):
                    break
            out.append(('m%d' % i, d))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', type=int, default=6)
    ap.add_argument('--family', default='both', choices=('axis', 'mixed', 'both'))
    ap.add_argument('--mixed', type=int, default=6)
    ap.add_argument('--window', type=float, default=1.0)
    ap.add_argument('--only', default=None, help='comma-separated ray labels')
    ap.add_argument('--out', default=None)
    ap.add_argument('--concurrency', action='store_true',
                    help='include the four-plane concurrency wall family')
    ap.add_argument('--control', action='store_true',
                    help='run the G2 negative control on e0 and stop')
    a = ap.parse_args()

    quats = record_quats(a.n)
    D.set_field(0); D.QZERO[:] = [quats[0]]
    pt = D.point_of(quats)
    rec = D.count_at(pt, len(quats))
    print('n=%d  base count %s' % (a.n, rec), flush=True)
    expect = {6: 727, 7: 1217, 8: 1895}[a.n]
    assert rec == expect, 'G1 FAILED: base is not the record (%s != %d)' % (rec, expect)
    print('G1 ok: base point is the %d record' % expect, flush=True)

    if a.control:
        d = [F(0)] * len(pt); d[0] = F(1)
        c = negative_control(quats, d, -a.window, a.window)
        print('NEGATIVE CONTROL', json.dumps(c))
        if not c['PASSES']:
            raise SystemExit('CONTROL FAILED: G2 raised nothing with %d of %d '
                             'conditions hidden -- the constancy check is blind'
                             % (c['dropped'], c['of']))
        print('control ok: G2 raises %d failure(s) when walls are hidden'
              % c['G2_failures'])
        return

    rays = directions(len(pt), a.family, a.mixed)
    if a.only:
        want = set(a.only.split(','))
        rays = [r for r in rays if r[0] in want]

    path = a.out or os.path.join(ROOT, 'data', 'wall_census_n%d.json' % a.n)
    out = {'what': 'does crossing a wall change the region count -- one verdict per '
                   'attributable crossing, exact on both sides',
           'question': 'OPEN_QUESTIONS 33, opened by P298',
           'n': a.n, 'record': expect,
           'quats': [list(q) for q in quats],
           'direction_family': a.family,
           'scope': ('a census over the STATED direction family below, not over all '
                     'directions. Each verdict is exact; the POPULATION of crossings '
                     'is whatever these rays meet.'),
           'rays': {}}
    if os.path.exists(path):                  # merge, never replace
        try:
            prev = json.load(open(path))
            if isinstance(prev.get('rays'), dict):
                out['rays'].update(prev['rays'])
        except Exception:
            pass

    for label, d in rays:
        cw = (concurrency_for(a.n, label, -a.window, a.window)
              if a.concurrency else None)
        if a.concurrency:
            print('   %s: %d concurrency roots in window' % (label, len(cw or [])),
                  flush=True)
        r = census_ray(quats, d, label, -a.window, a.window, concurrency=cw)
        out['rays'][label] = r
        json.dump(out, open(path, 'w'), indent=1)
        att = [c for c in r['crossings'] if c['n_walls'] == 1]
        ch = sum(1 for c in att if c['changes'] is True)
        pr = sum(1 for c in att if c['changes'] is False)
        un = sum(1 for c in att if c['changes'] is None)
        print('   %-8s attributable %3d | changes %3d | preserves %3d | '
              'unevaluated %d | G2 failures %d'
              % (label, len(att), ch, pr, un, r['constancy_failures']), flush=True)
    print('written %s' % os.path.relpath(path, ROOT))


if __name__ == '__main__':
    main()
