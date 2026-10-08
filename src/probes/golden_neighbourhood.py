#!/usr/bin/env python3
"""The golden's neighbourhood, counted in Z[sqrt5]: is there any d1 from 97 to 103?  [plan item 4]

[P423] found no n = 4 compound with d1 from 97 to 103, but integer quaternions cannot come near the
golden (d1 = 104, in Q(sqrt5)). Here every member is in Z[sqrt5]^4, so `cube_regions_q2w --d 5`
counts it exactly (about 30 ms each).

**Modes.**
- `paw`: the paw through the golden. Rotate one cube A about the body diagonal it shares with one
  other cube B, by the quaternion (m, d) with m in Z[sqrt5] and d that shared diagonal
  (unnormalised, in Z[sqrt5]^3). A keeps its sharing with B and loses the two others, so the
  member is a paw (triangle of the other three plus the pendant A-B). Every (A, B) is run; under
  A4 they should agree, which is a check.
- `perturb`: the golden scaled by N, each component moved by a random small element of Z[sqrt5].
  Every stratum next to the golden is reached, not only the 1-dimensional paw and 4-cycle.
- `climb`: greedy climbs on d1 in Z[sqrt5]^4 from the golden's perturbations.

**Controls.**
- The golden itself must count (104, 48, 24, 1). (m = 0 is NOT the identity: (0, d) is the half
  turn about d. The identity is the limit of large |m|, since the angle is 2 atan(|d| / m) and
  |d| = 8 sqrt3 here; small angles need |m| much larger than 14.)
- Every paw member's sharing is read back exactly: precisely the pairs {A, B}, {B, C}, {B, D},
  {C, D}, with one shared diagonal each, except at isolated event values.
- Members the engine rejects (overflow budget) are counted as UNEVALUATED, never as results.
- `crosscheck`: two members are recounted per cube with sphere_count over kfield.

**Scope.** Samples at values of m give the generic value on each interval of the parameter.
Isolated event points, where d1 can jump up (the golden is one), are found only if a sampled m lands
on one exactly. Axis-sharing events along the paw are solved in closed form in `paw` mode: the
moving cube gains a shared axis with C or D only if the two axes make the same angle with d.

Output: data/golden_neighbourhood.json (modes merge into it).
"""
import os, sys, json, random, itertools, subprocess, collections
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))

ROOT = os.path.dirname(os.path.dirname(HERE))
ENGINE_Q2 = os.path.join(ROOT, 'src', 'cube_regions_q2w')
DATA = os.path.join(ROOT, 'data')


# ---- Z[sqrt5] as integer pairs (p, q) = p + q sqrt5 -------------------------------------------
def a(x, y): return (x[0] + y[0], x[1] + y[1])
def s(x, y): return (x[0] - y[0], x[1] - y[1])
def m(x, y): return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def neg(x): return (-x[0], -x[1])
Z = (0, 0)


def qmul(p, q):
    w1, x1, y1, z1 = p
    w2, x2, y2, z2 = q
    return (s(s(s(m(w1, w2), m(x1, x2)), m(y1, y2)), m(z1, z2)),
            s(a(a(m(w1, x2), m(x1, w2)), m(y1, z2)), m(z1, y2)),
            a(a(s(m(w1, y2), m(x1, z2)), m(y1, w2)), m(z1, x2)),
            a(s(a(m(w1, z2), m(x1, y2)), m(y1, x2)), m(z1, w2)))


def conj(q): return (q[0], neg(q[1]), neg(q[2]), neg(q[3]))


def rot(q, v):
    """q v q-bar, unnormalised (scaled by |q|^2)"""
    r = qmul(qmul(q, (Z,) + tuple(v)), conj(q))
    return r[1:]


def cross(u, v):
    return (s(m(u[1], v[2]), m(u[2], v[1])), s(m(u[2], v[0]), m(u[0], v[2])), s(m(u[0], v[1]), m(u[1], v[0])))


def dot(u, v): return a(a(m(u[0], v[0]), m(u[1], v[1])), m(u[2], v[2]))


def parallel(u, v): return all(c == Z for c in cross(u, v))


def tosqrt5(x):
    return x[0] + x[1] * 5 ** 0.5


DIAG = [((1, 0), (1, 0), (1, 0)), ((1, 0), (1, 0), (-1, 0)), ((1, 0), (-1, 0), (1, 0)), ((-1, 0), (1, 0), (1, 0))]
FACE = [((1, 0), Z, Z), (Z, (1, 0), Z), (Z, Z, (1, 0))]
TWO = [tuple(a(FACE[i][k], (FACE[j][k] if sg > 0 else neg(FACE[j][k]))) for k in range(3))
       for i, j in ((0, 1), (0, 2), (1, 2)) for sg in (1, -1)]


def axes(q):
    return {'body': [rot(q, d) for d in DIAG], 'face': [rot(q, f) for f in FACE], 'two': [rot(q, t) for t in TWO]}


def coincidences(qs):
    A = [axes(q) for q in qs]
    out = []
    for i, j in itertools.combinations(range(len(qs)), 2):
        for t1 in A[i]:
            for t2 in A[j]:
                k = sum(parallel(u, v) for u in A[i][t1] for v in A[j][t2])
                if k:
                    out.append((i, j, t1, t2, k))
    return out


GOLDEN = [((0, 1), (1, 0), (1, 0), (1, 0)), ((0, 1), (1, 0), (-1, 0), (-1, 0)),
          ((0, 1), (-1, 0), (1, 0), (-1, 0)), ((0, 1), (-1, 0), (-1, 0), (1, 0))]


def spec(qs):
    return ';'.join(','.join('%d:%d' % c for c in q) for q in qs)


def engine(qs):
    r = subprocess.run([ENGINE_Q2, '--d', '5', '--quats', spec(qs)], capture_output=True, text=True)
    try:
        e = json.loads(r.stdout)
    except ValueError:
        return {'unevaluated': (r.stdout + r.stderr).strip()[:200]}
    if 'by_depth' not in e:
        return {'unevaluated': str(e)[:200]}
    pc = [e['per_label'].get(str(1 << i), 0) for i in range(4)]
    assert sum(pc) == e['by_depth']['1']
    return {'bd': [e['by_depth'][str(k)] for k in range(1, 5)], 'pc': pc, 'total': e['bounded']}


def reduce(q):
    """divide a quaternion by the gcd of its integer coordinates (keeps Z[sqrt5])"""
    import math
    g = 0
    for c in q:
        g = math.gcd(g, math.gcd(abs(c[0]), abs(c[1])))
    return tuple((c[0] // g, c[1] // g) for c in q) if g > 1 else q


def shared_diag(i, j):
    for u in axes(GOLDEN[i])['body']:
        for v in axes(GOLDEN[j])['body']:
            if parallel(u, v):
                return u
    raise AssertionError('golden pair %d%d shares no diagonal' % (i, j))


def summarise(rows, label):
    ok = [r for r in rows if 'bd' in r]
    un = len(rows) - len(ok)
    d1 = collections.Counter(r['bd'][0] for r in ok)
    gap = [r for r in ok if 97 <= r['bd'][0] <= 103]
    print('%s: %d members, %d unevaluated; d1 values %s; d1 in 97..103: %d'
          % (label, len(rows), un, sorted(d1.items()), len(gap)), flush=True)
    return {'members': len(rows), 'unevaluated': un, 'd1': dict(d1), 'gap_hits': gap}


def paw():
    res = {}
    big = [20, 25, 30, 40, 50, 70, 100, 150, 200, 300, 500, 1000, 2000, 5000, 20000]
    vals = sorted({(p, q) for p in range(-12, 13) for q in range(-6, 7)}
                  | {(sg * b, q) for b in big for sg in (1, -1) for q in (0, 1)})
    g = engine(GOLDEN)
    assert g.get('bd') == [104, 48, 24, 1], ('control', g)
    for A, B in itertools.permutations(range(4), 2):
        d = shared_diag(A, B)
        rows = []
        for mm in vals:
            r = reduce(qmul((mm,) + tuple(d), GOLDEN[A]))
            qs = list(GOLDEN)
            qs[A] = r
            e = engine(qs)
            sh = sorted((i, j) for i, j, t1, t2, k in coincidences(qs) if t1 == t2 == 'body')
            rows.append({'m': mm, 'qs': spec(qs), **e, 'body_shared': sh,
                         'other': [c for c in coincidences(qs) if not (c[2] == c[3] == 'body')]})
        C, D = [x for x in range(4) if x not in (A, B)]
        expect = sorted([tuple(sorted(p)) for p in ((A, B), (B, C), (B, D), (C, D))])
        odd = [r for r in rows if r['body_shared'] != expect]
        res['%d%d' % (A, B)] = {**summarise(rows, 'paw A=%d B=%d' % (A, B)),
                                'sharing_not_paw': [(r['m'], r['body_shared'], r.get('bd')) for r in odd],
                                'events_other_coincidence': [(r['m'], r['other'], r.get('bd')) for r in rows if r['other']]}
        if odd:
            print('   members whose sharing is not exactly the paw: %s' % res['%d%d' % (A, B)]['sharing_not_paw'][:6])
    return res


def perturb(rnd, N, eps, count):
    rows = []
    for _ in range(count):
        qs = []
        for q in GOLDEN:
            qs.append(tuple((N * c[0] + rnd.randint(-eps, eps), N * c[1] + rnd.randint(-eps, eps)) for c in q))
        e = engine(qs)
        sh = coincidences(qs)
        rows.append({'qs': spec(qs), **e, 'coincidences': sh})
    return rows


def climb(rnd, N, steps):
    cur = [tuple((N * c[0], N * c[1]) for c in q) for q in GOLDEN]
    k = rnd.randrange(4)
    cur[k] = tuple((c[0] + rnd.choice((-1, 1)), c[1]) for c in cur[k])
    best = None
    ce = engine(cur)
    log = []
    for _ in range(steps):
        nxt = [list(q) for q in cur]
        i, j = rnd.randrange(4), rnd.randrange(4)
        c = nxt[i][j]
        nxt[i][j] = (c[0] + rnd.choice((-2, -1, 1, 2)), c[1]) if rnd.random() < 0.7 else (c[0], c[1] + rnd.choice((-1, 1)))
        nxt = [tuple(q) for q in nxt]
        ne = engine(nxt)
        if 'bd' not in ne:
            log.append({'qs': spec(nxt), **ne})
            continue
        log.append({'qs': spec(nxt), **ne})
        if 'bd' in ce and ne['bd'][0] == 104:
            continue                     # the golden itself (or a rescaling): not a step away
        if 'bd' not in ce or (ne['bd'][0], ne['total']) >= (ce['bd'][0], ce['total']):
            cur, ce = nxt, ne
            if best is None or (ce['bd'][0], ce['total']) > (best[1]['bd'][0], best[1]['total']):
                best = (spec(cur), ce)
    return log, best


def main():
    out = {}
    if 'paw' in sys.argv:
        out['paw'] = paw()
    if 'perturb' in sys.argv:
        rnd = random.Random(5)
        out['perturb'] = {}
        for N, eps in ((1, 1), (2, 1), (4, 1), (8, 1), (8, 3), (16, 2), (32, 3)):
            rows = perturb(rnd, N, eps, 150)
            out['perturb']['N%d_eps%d' % (N, eps)] = {**summarise(rows, 'perturb N=%d eps=%d' % (N, eps)),
                                                    'top': sorted((r for r in rows if 'bd' in r), key=lambda r: -r['bd'][0])[:5]}
    if 'climb' in sys.argv:
        out['climb'] = []
        for seed in range(6):
            rnd = random.Random(100 + seed)
            log, best = climb(rnd, (4, 8, 16)[seed % 3], 400)
            sm = summarise(log, 'climb seed %d' % seed)
            print('   best %s' % (best,), flush=True)
            out['climb'].append({**sm, 'best': best})
    old = {}
    p = os.path.join(DATA, 'golden_neighbourhood.json')
    if os.path.exists(p):
        old = json.load(open(p))
    old.update(out)
    json.dump(old, open(p, 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()


def crosscheck():
    """sphere_count over kfield on two members: a paw member next to the golden, and the climb's 88"""
    from sphere_count import Compound
    from kfield import K
    d = shared_diag(0, 1)
    paw20 = list(GOLDEN)
    paw20[0] = reduce(qmul(((20, 0),) + tuple(d), GOLDEN[0]))
    c88 = [tuple(tuple(map(int, c.split(':'))) for c in g.split(',')) for g in
           '0:16,16:0,16:0,16:0;1:16,17:0,-16:0,-16:0;0:16,-16:0,16:0,-16:0;0:16,-16:0,-16:0,16:0'.split(';')]
    rows = []
    for name, qs in (('paw m=20', paw20), ('climb 88', c88)):
        e = engine(qs)
        kq = [tuple(K(c[0], 0, c[1], 0) for c in q) for q in qs]
        C = Compound(kq, 'K')
        pc = [C.components(C.beat_pieces([i], [b for b in range(4) if b != i])) for i in range(4)]
        ok = pc == e['pc']
        print('%-9s engine per-cube %s  sphere_count %s  %s' % (name, e['pc'], pc, 'AGREE' if ok else 'DISAGREE'), flush=True)
        rows.append({'name': name, 'qs': spec(qs), 'engine_pc': e['pc'], 'sphere_pc': pc, 'agree': ok})
    p = os.path.join(DATA, 'golden_neighbourhood.json')
    old = json.load(open(p))
    old['crosscheck'] = rows
    json.dump(old, open(p, 'w'), indent=1, default=str)


if __name__ == '__main__' and 'crosscheck' in sys.argv:
    crosscheck()


def isqrt_z5(x):
    """square root in Z[sqrt5] of x = (p, q), or None. Tries r = (a, b) with r^2 = x."""
    import math
    p, q = x
    # (a + b r5)^2 = a^2 + 5 b^2 + 2ab r5 ; a^2 + 5b^2 = p, 2ab = q
    if p < 0:
        return None
    for b in range(0, int(math.isqrt(p // 5)) + 2):
        a2 = p - 5 * b * b
        if a2 < 0:
            break
        a_ = math.isqrt(a2)
        if a_ * a_ == a2:
            for sa in (a_, -a_):
                for sb in (b, -b):
                    if (sa * sa + 5 * sb * sb, 2 * sa * sb) == x:
                        return (sa, sb)
    return None


def events():
    """Axis-sharing events along each paw: A turned about d gains an axis shared with C or D.

    For an axis u of A and an axis w of C or D, the event needs (u.d)^2 / |u|^2 = (w.d)^2 / |w|^2.
    Then the turn carries u_perp onto +-w_perp (perpendicular parts to d) once both are scaled to
    the same length; the rotation is (|u_p||w_p| + u_p.w_p, u_p x w_p), which is in Z[sqrt5] when
    |u_p|^2 |w_p|^2 is a square there. Events needing sqrt outside Q(sqrt5) are UNEVALUATED.
    Only axis-sharing events are found; other degeneracies (four planes through a point, etc.)
    are not."""
    rows = []
    unev = 0
    for A, B in (((0, 1),)):
        d = shared_diag(A, B)
        C, D = [x for x in range(4) if x not in (A, B)]
        Aax = axes(GOLDEN[A])
        dd = dot(d, d)
        seen = set()
        for t1, us in Aax.items():
            for u in us:
                for X in (C, D):
                    for t2, ws in axes(GOLDEN[X]).items():
                        for w in ws:
                            for sg in (1, -1):
                                w2 = w if sg > 0 else tuple(neg(c) for c in w)
                                # equal angle with d: (u.d)^2 |w|^2 == (w.d)^2 |u|^2, and same sign side
                                ud, wd = dot(u, d), dot(w2, d)
                                if m(m(ud, ud), dot(w2, w2)) != m(m(wd, wd), dot(u, u)):
                                    continue
                                # perpendicular parts, scaled by |d|^2 (stay integral)
                                up = tuple(s(m(dd, u[k]), m(ud, d[k])) for k in range(3))
                                wp = tuple(s(m(dd, w2[k]), m(wd, d[k])) for k in range(3))
                                if all(c == Z for c in up):
                                    continue        # u is d itself
                                # need ud/|u| == wd/|w| (same side): compare signs numerically
                                if tosqrt5(ud) * tosqrt5(wd) < 0:
                                    continue
                                L = isqrt_z5(m(dot(up, up), dot(wp, wp)))
                                if L is None:
                                    unev += 1
                                    rows.append({'A': A, 'X': X, 'types': (t1, t2), 'unevaluated': 'sqrt not in Q(sqrt5)'})
                                    continue
                                # rotation taking up to wp direction: (|up||wp| + up.wp, up x wp); scale wp by |up|/|wp| implicit
                                r = (a(L, dot(up, wp)),) + cross(up, wp)
                                if all(c == Z for c in r):
                                    continue        # half turn: use (0, d)
                                if not parallel(r[1:], d) and any(c != Z for c in r[1:]):
                                    continue
                                qa = reduce(qmul(r, GOLDEN[A]))
                                qs = list(GOLDEN)
                                qs[A] = qa
                                key = spec(qs)
                                if key in seen:
                                    continue
                                seen.add(key)
                                e = engine(qs)
                                rows.append({'A': A, 'X': X, 'types': (t1, t2), 'qs': key, **e,
                                             'coincidences': [c for c in coincidences(qs)]})
    ok = [r for r in rows if 'bd' in r]
    print('paw events (A=0, B=1): %d evaluated, %d unevaluated (sqrt outside Q(sqrt5)), %d engine-rejected'
          % (len(ok), unev, sum(1 for r in rows if 'unevaluated' in r and 'qs' in r)))
    for r in sorted(ok, key=lambda r: -r['bd'][0]):
        print('   d1 %3d  bd %s  total %d  event %s with cube %d  sharings %s'
              % (r['bd'][0], r['bd'], r['total'], r['types'], r['X'],
                 sorted(set((c[0], c[1], c[2], c[3]) for c in r['coincidences']))))
    p = os.path.join(DATA, 'golden_neighbourhood.json')
    old = json.load(open(p))
    old['paw_events'] = {'rows': rows, 'unevaluated_sqrt': unev}
    json.dump(old, open(p, 'w'), indent=1, default=str)


if __name__ == '__main__' and 'events' in sys.argv:
    events()


def events_sqrt2():
    """The paw events that need sqrt2 (A's 2-fold axis meets a face axis of C or D), evaluated
    exactly with sphere_count over Q(sqrt2, sqrt5) (kfield with P = 2)."""
    from kfield import K
    K.setP(2)
    from sphere_count import Compound
    def k(x): return K(x[0], 0, x[1], 0)
    def kq(q): return tuple(k(c) for c in q)
    def kmul(p, q):
        w1, x1, y1, z1 = p
        w2, x2, y2, z2 = q
        return (w1*w2 - x1*x2 - y1*y2 - z1*z2, w1*x2 + x1*w2 + y1*z2 - z1*y2,
                w1*y2 - x1*z2 + y1*w2 + z1*x2, w1*z2 + x1*y2 - y1*x2 + z1*w2)
    A, B = 0, 1
    d = shared_diag(A, B)
    dd = dot(d, d)
    pts = {}
    for X in [x for x in range(4) if x not in (A, B)]:
        for u in axes(GOLDEN[A])['two']:
            for w0 in axes(GOLDEN[X])['face']:
                for sg in (1, -1):
                    w = w0 if sg > 0 else tuple(neg(c) for c in w0)
                    ud, wd = dot(u, d), dot(w, d)
                    if m(m(ud, ud), dot(w, w)) != m(m(wd, wd), dot(u, u)) or tosqrt5(ud) * tosqrt5(wd) < 0:
                        continue
                    up = tuple(s(m(dd, u[i]), m(ud, d[i])) for i in range(3))
                    wp = tuple(s(m(dd, w[i]), m(wd, d[i])) for i in range(3))
                    x = m(dot(up, up), dot(wp, wp))
                    r2 = isqrt_z5(m((2, 0), x))
                    assert r2 is not None
                    L = k(r2) * K(0, F(1, 2), 0, 0)              # sqrt(2x) / sqrt2
                    assert L * L == k(x)
                    r = (L + k(dot(up, wp)),) + tuple(k(c) for c in cross(up, wp))
                    qa = kmul(r, kq(GOLDEN[A]))
                    qs = [qa if i == A else kq(GOLDEN[i]) for i in range(4)]
                    num = tuple(round(float(c.num() / qa[0].num()), 9) for c in qa) if not qa[0].is_zero() else tuple(round(float(c.num()), 9) for c in qa)
                    pts.setdefault(num, (X, qs))
    print('distinct sqrt2 event points: %d' % len(pts), flush=True)
    import multiprocessing as mp
    jobs = [(num, X, [tuple((c.a, c.b, c.c, c.d) for c in q) for q in qs]) for num, (X, qs) in pts.items()]
    rows = []
    with mp.Pool(len(jobs)) as pool:
        for r in pool.imap_unordered(_count_p2, jobs):
            print('   event with cube %d: total %d  depths %s' % (r['X'], r['total'], r['bd']), flush=True)
            rows.append(r)
    p = os.path.join(DATA, 'golden_neighbourhood.json')
    old = json.load(open(p))
    old['paw_events_sqrt2'] = rows
    json.dump(old, open(p, 'w'), indent=1, default=str)


def _count_p2(job):
    from kfield import K
    K.setP(2)                      # each worker process sets the field itself
    from sphere_count import Compound
    num, X, raw = job
    qs = [tuple(K(*c) for c in q) for q in raw]
    tot, bd = Compound(qs, 'K').count()
    return {'X': X, 'approx_quat_A': num, 'total': tot, 'bd': bd}


if __name__ == '__main__' and 'events_sqrt2' in sys.argv:
    events_sqrt2()


def control_p2():
    """Control for kfield with P = 2: random Z[sqrt2] compounds counted by sphere_count over
    Q(sqrt2, sqrt5) must match `cube_regions_q2w --d 2`, which is an independent engine."""
    from kfield import K
    K.setP(2)
    from sphere_count import Compound
    rnd = random.Random(2)
    rows = []
    for t in range(3):
        qs = [((1, 0), Z, Z, Z)] + [tuple((rnd.randint(-3, 3), rnd.randint(-2, 2)) for _ in range(4)) for _ in range(2)]
        sp = ';'.join(','.join('%d:%d' % c for c in q) for q in qs)
        r = subprocess.run([ENGINE_Q2, '--d', '2', '--quats', sp], capture_output=True, text=True)
        e = json.loads(r.stdout)
        tot, bd = Compound([tuple(K(c[0], c[1], 0, 0) for c in q) for q in qs], 'K').count()
        ok = e.get('bounded') == tot and all(e['by_depth'][str(k)] == v for k, v in bd.items())
        print('control %s: engine %s %s  sphere_count %d %s  %s' % (sp, e.get('bounded'), e.get('by_depth'), tot, bd,
                                                                   'AGREE' if ok else 'DISAGREE'), flush=True)
        rows.append({'qs': sp, 'engine': e.get('by_depth'), 'sphere': bd, 'agree': ok})
    p = os.path.join(DATA, 'golden_neighbourhood.json')
    old = json.load(open(p))
    old['control_p2'] = rows
    json.dump(old, open(p, 'w'), indent=1, default=str)


if __name__ == '__main__' and 'control_p2' in sys.argv:
    control_p2()
