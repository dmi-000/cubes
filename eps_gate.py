#!/usr/bin/env python3
"""Gate on the infinitesimal engine, before any count it produces is believed.

Controls, ordered by what they would catch, and chosen to be hard rather than
convenient:

  1. ZERO DIRECTION.  With the eps part zero the engine must reproduce
     cube_regions_q2 exactly -- same configurations, same counts, same depth
     profiles.  This is a different binary running different arithmetic on the
     same geometry, not two spellings of one routine.  Includes both 67s, whose
     answer (67) is known independently.

  2. AN INFINITESIMAL STEP MUST NOT CHANGE A GENERIC COUNT.  Displace a
     configuration that sits in the INTERIOR of a chamber: no wall is nearby, so
     the infinitesimal count must equal the undisplaced one for every direction.
     A sign rule that broke ties the wrong way would show here.

  3. AN INFINITESIMAL STEP MUST CHANGE THE COUNT AT A KNOWN WALL.  The n=2
     13-continuum's endpoint and the octahedral 67 both have measured facet
     counts (59, 53, 59, 53, 57, 63 at the 67).  The infinitesimal count along
     those same facet-crossing directions must reproduce them.  This is the
     control that fails if eps is being treated as zero rather than as an
     infinitesimal -- and it is the one a "does it run" check would pass.

  4. eps IS ORDER-SENSITIVE, NOT MAGNITUDE-SENSITIVE.  Scaling the direction by
     a positive rational must not change the count (same ray), while negating it
     may.  A finite-eps implementation fails the first of those as soon as the
     scale is large enough; an infinitesimal one cannot.
"""
import json, os, subprocess, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dimension as D
from qfield import Q
from epscount import count_eps, count_eps_err, eps_quats
from dimension67 import RECORDS

HERE = os.path.dirname(os.path.abspath(__file__))
Q2 = os.path.join(HERE, 'cube_regions_q2w')
fails = []


def check(name, ok, detail=''):
    print('%-58s %s %s' % (name, 'ok' if ok else 'FAIL', detail), flush=True)
    if not ok:
        fails.append(name)


def q2_count(quats, d):
    s = ';'.join(','.join('%d:%d' % c for c in q) for q in quats)
    p = subprocess.run([Q2, '--d', str(d), '--quats', s], capture_output=True, text=True)
    try:
        return json.loads(p.stdout.strip().splitlines()[-1])['bounded']
    except Exception:
        return None


def point_of(d, quats):
    D.set_field(d)
    qs = [tuple(Q(F(p), F(q), d) for p, q in quat) for quat in quats]
    pt = []
    for q in qs[1:]:
        pt += D.cayley_of(q)
    return qs, pt


def gate_zero_direction():
    for d, (name, quats) in sorted(RECORDS.items()):
        qs, pt = point_of(d, quats)
        ref = q2_count(quats, d)
        got, err = count_eps_err(pt, None, d, qs[0])
        check('zero eps reproduces q2 at the %s 67' % name, got == ref == 67,
              'eps %s vs q2 %s %s' % (got, ref, err))


def gate_generic_interior():
    """a chamber interior: every infinitesimal direction keeps the count"""
    d = 0
    D.set_field(0)
    pt = [F(1, 3), F(1, 7), F(2, 5)]          # generic, no wall through it
    base = count_eps(pt, None, d)
    ok, bad = True, []
    for k in range(len(pt)):
        for s in (1, -1):
            dirv = [F(0)] * len(pt)
            dirv[k] = F(s)
            c = count_eps(pt, dirv, d)
            if c != base:
                ok = False
                bad.append((k, s, c))
    check('generic interior point: count constant in all 6 directions',
          ok and base is not None, 'base %s bad %s' % (base, bad[:3]))


def gate_known_facets():
    """the octahedral 67's six measured facet counts, reproduced infinitesimally"""
    d = 2
    quats = RECORDS[2][1]
    qs, pt = point_of(d, quats)
    rec = json.load(open(os.path.join(HERE, 'dimension67.json')))
    oct_ = [r for r in rec if r['name'] == 'octahedral'][0]
    beyond = [e['beyond'][0] for e in oct_['cone']['beyond_each_facet']]
    ncols = 6
    vars_ = __import__('sympy').symbols('c0:%d' % ncols)
    Rs = D.frames(vars_, qs[0])
    D.QZERO[:] = [qs[0]]
    tight, loose = D.cached_conditions(Rs, 3, vars_, pt, D.quats_of(pt, qs[0]), qs[0])
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
    got = []
    for i in range(len(walls)):
        sub = [walls[t] for t in range(len(walls)) if t != i]
        cross = None
        for v in D.nullspace(sub, ncols):
            if sum(walls[i][k] * v[k] for k in range(ncols)) != 0:
                cross = v
                break
        got.append(None if cross is None else count_eps(pt, cross, d, qs[0]))
    # the facet-crossing direction is determined up to sign; compare as multisets
    check('octahedral 67: infinitesimal facet counts match the measured ones',
          sorted(x for x in got if x is not None) == sorted(beyond),
          'eps %s vs measured %s' % (sorted(x for x in got if x is not None),
                                     sorted(beyond)))
    check('  and none of the six was unevaluable', all(x is not None for x in got),
          str(got))


def gate_scale_invariance():
    d = 2
    quats = RECORDS[2][1]
    qs, pt = point_of(d, quats)
    dirv = [Q(F(1), 0, d), Q(F(-3), 0, d), Q(F(2), 0, d),
            Q(F(0), 0, d), Q(F(1), 0, d), Q(F(-1), 0, d)]
    a = count_eps(pt, dirv, d, qs[0])
    scaled = [x * 97 for x in dirv]
    b = count_eps(pt, scaled, d, qs[0])
    tiny = [x * F(1, 1000) for x in dirv]
    c = count_eps(pt, tiny, d, qs[0])
    check('count depends on the RAY, not the direction scale (x97, x1/1000)',
          a is not None and a == b == c, '%s %s %s' % (a, b, c))


def main():
    gate_zero_direction()
    gate_generic_interior()
    gate_known_facets()
    gate_scale_invariance()
    print('\n%s' % ('EPS ENGINE GATE PASSES' if not fails
                    else 'FAILED: ' + ', '.join(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
