#!/usr/bin/env python3
"""An independent exact region counter from convex pieces on the sphere -- the anchor for [P399].

THE CLAIM IT TESTS.  The hypothesis-free bound max(4) <= 285 rests on two lemmas:
  DEPTH   the regions of depth |A| inside exactly the cubes of A biject with the components of
              D(A) = { u in S^2 : max_{a in A} M_a(u) < min_{b not in A} M_b(u) }
          (M_x(u) = max over x's six faces f of f.u, so the reach is r_x = 1/M_x);
  PIECES  fixing an active face t_b of every b not in A cuts D(A) into convex polyhedral cones
              P(t) = D(A) n  sector(b, t_b) for each b,
          each relatively closed in D(A), so #components(D(A)) = components of the graph whose
          vertices are the nonempty pieces and whose edges are pairs of pieces that meet.
If both hold, summing the component counts over every nonempty A must reproduce the engine's
bounded-region count EXACTLY.  This counter shares no code with the engine: it never builds the
arrangement in R^3, only solves small linear systems on the sphere.

EXACT.  Every piece is a system of homogeneous linear inequalities, strict and non-strict, in
u in R^3.  On a piece the chosen face t of the first b has t.u = M_b(u) > 0, so u is normalised to
the plane t.u = 1, parametrised by the cube's other two normals, and one Fourier-Motzkin step
leaves an interval test.  Arithmetic is Fraction, or kfield.K for Q(sqrt5) configurations.

ALSO MEASURED, for the Mayer-Vietoris step of the bound: for each cube i of a 4-compound,
    s = #pi0 T_i,  a = #pi0 {i beats the first two others}, b = #pi0 {i beats the third},
    m = #pi0 of the complement of their union,
and for each pair the same with K = {i,j beat k}, L = {i,j beat l}.  Every instance must satisfy
s <= a + b + m - 2, and the caps used by the bound: T_i <= 26, pair set <= 22, and the complement
m <= 6 |A| ([P401]: its pieces share face centres), i.e. 6 for a cube and 12 for a pair.

    python3 src/probes/sphere_count.py
"""
import sys, os, itertools, json, subprocess, random
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from kfield import K

ROOT = os.path.dirname(os.path.dirname(HERE))
ENGINE = os.path.join(ROOT, 'cube_regions_n')
ENGINE_Q2 = os.path.join(ROOT, 'src', 'cube_regions_q2w')


def sgn(x):
    return x.sign() if isinstance(x, K) else (x > 0) - (x < 0)


def normals(q, one):
    """the three face normals of the cube of quaternion q (rows), exact."""
    w, x, y, z = [one * c for c in q]
    N = w * w + x * x + y * y + z * z
    M = [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
         [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
         [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]
    return [[M[r][c] / N for r in range(3)] for c in range(3)]


def faces(nv):
    """six outward face normals: (+v0, -v0, +v1, -v1, +v2, -v2)"""
    out = []
    for v in nv:
        out.append(v)
        out.append([-c for c in v])
    return out


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def feasible(cons, frame):
    """cons: list of (c, strict) meaning c.u > 0 (strict) or c.u >= 0.  frame = (t, e1, e2):
    u = t + al e1 + be e2 (so t.u is fixed positive).  Exact Fourier-Motzkin."""
    t, e1, e2 = frame
    rows = []                                   # p*al + q*be + r  (>|>=) 0
    for c, st in cons:
        rows.append((dot(c, e1), dot(c, e2), dot(c, t), st))
    lo, hi, rest = [], [], []
    for p, q, r, st in rows:
        s = sgn(p)
        if s > 0:
            lo.append((p, q, r, st))            # al > -(q be + r)/p
        elif s < 0:
            hi.append((p, q, r, st))
        else:
            rest.append((q, r, st))
    for (p1, q1, r1, s1) in lo:
        for (p2, q2, r2, s2) in hi:
            # p1 al + q1 be + r1 >= 0,  p2 al + q2 be + r2 >= 0 with p2 < 0:
            # eliminate al: (-p2)(q1 be + r1) + p1 (q2 be + r2) (>|>=) 0
            rest.append(((-p2) * q1 + p1 * q2, (-p2) * r1 + p1 * r2, s1 or s2))
    blo, bhi, strictlo, stricthi = None, None, False, False
    for q, r, st in rest:
        s = sgn(q)
        if s == 0:
            sr = sgn(r)
            if sr < 0 or (sr == 0 and st):
                return False
            continue
        bound = -r / q                          # be > bound (q>0) or be < bound (q<0)
        if s > 0:
            if blo is None or sgn(bound - blo) > 0 or (sgn(bound - blo) == 0 and st):
                if blo is None or sgn(bound - blo) != 0:
                    strictlo = st
                else:
                    strictlo = strictlo or st
                blo = bound
        else:
            if bhi is None or sgn(bhi - bound) > 0 or (sgn(bhi - bound) == 0 and st):
                if bhi is None or sgn(bhi - bound) != 0:
                    stricthi = st
                else:
                    stricthi = stricthi or st
                bhi = bound
    if blo is None or bhi is None:
        return True
    d = sgn(bhi - blo)
    return d > 0 or (d == 0 and not strictlo and not stricthi)


class Compound:
    def __init__(self, quats, field='Q'):
        one = K(1) if field == 'K' else F(1)
        self.field = field
        self.nv = [normals(q, one) for q in quats]
        self.fc = [faces(v) for v in self.nv]
        self.n = len(quats)

    def frame(self, b, t):
        """plane t.u = 1 for face t of cube b, spanned by b's other two normals"""
        k = t // 2
        others = [self.nv[b][j] for j in range(3) if j != k]
        return (self.fc[b][t], others[0], others[1])

    # --- set type 1: "every cube of A beats every cube of B":  max_A M < min_B M --------------
    def beat_pieces(self, A, B):
        out = []
        for ts in itertools.product(range(6), repeat=len(B)):
            cons = []
            for b, t in zip(B, ts):
                tv = self.fc[b][t]
                cons += [(sub(tv, f), False) for f in self.fc[b]]            # t active for b
                for a in A:
                    cons += [(sub(tv, f), True) for f in self.fc[a]]        # M_a < t.u
            out.append((cons, self.frame(B[0], ts[0])))
        return out

    # --- set type 2: "x does not lose to any of Y":  M_x >= max_Y M ------------------------------
    def geq_pieces(self, x, Y):
        out = []
        for s in range(6):
            sv = self.fc[x][s]
            cons = [(sub(sv, f), False) for f in self.fc[x]]
            for y in Y:
                cons += [(sub(sv, g), False) for g in self.fc[y]]
            out.append((cons, self.frame(x, s)))
        return out

    def components(self, pieces):
        live = [(c, fr) for c, fr in pieces if feasible(c, fr)]
        par = list(range(len(live)))

        def find(i):
            while par[i] != i:
                par[i] = par[par[i]]
                i = par[i]
            return i
        for i, j in itertools.combinations(range(len(live)), 2):
            if find(i) != find(j) and feasible(live[i][0] + live[j][0], live[i][1]):
                par[find(i)] = find(j)
        return len({find(i) for i in range(len(live))})

    def count(self):
        """sum over nonempty A of #pi0 D(A), with the per-depth split"""
        idx = list(range(self.n))
        by_depth = {}
        for k in range(1, self.n + 1):
            for A in itertools.combinations(idx, k):
                B = [b for b in idx if b not in A]
                c = 1 if not B else self.components(self.beat_pieces(list(A), B))
                by_depth[k] = by_depth.get(k, 0) + c
        return sum(by_depth.values()), by_depth

    def mv_checks(self):
        """Mayer-Vietoris instances used by the bound, at n = 4"""
        assert self.n == 4
        rows = []
        for i in range(4):
            j, k, l = [x for x in range(4) if x != i]
            s = self.components(self.beat_pieces([i], [j, k, l]))
            a = self.components(self.beat_pieces([i], [j, k]))
            b = self.components(self.beat_pieces([i], [l]))
            m = self.components(self.geq_pieces(i, [j, l]) + self.geq_pieces(i, [k, l]))
            rows.append(('T%d' % i, s, a, b, m))
        for i, j in itertools.combinations(range(4), 2):
            k, l = [x for x in range(4) if x not in (i, j)]
            s = self.components(self.beat_pieces([i, j], [k, l]))
            a = self.components(self.beat_pieces([i, j], [k]))
            b = self.components(self.beat_pieces([i, j], [l]))
            m = self.components(self.geq_pieces(i, [k, l]) + self.geq_pieces(j, [k, l]))
            rows.append(('D%d%d' % (i, j), s, a, b, m))
        return rows


def engine(quats):
    spec = ';'.join(','.join(str(c) for c in q) for q in quats)
    r = subprocess.run([ENGINE, '--quats', spec], capture_output=True, text=True)
    try:
        return json.loads(r.stdout).get('bounded')
    except Exception:
        return None


def engine_q5(spec):
    r = subprocess.run([ENGINE_Q2, '--d', '5', '--quats', ';'.join(spec)], capture_output=True, text=True)
    try:
        return json.loads(r.stdout).get('bounded')
    except Exception:
        return None


def main():
    R5 = K(0, 0, 1, 0)
    cases = [
        ('n=2 13-pair (shared body diagonal)', [(1, 0, 0, 0), (3, 1, 1, 1)], 'Q'),
        ('n=2 SHARED FACE PLANE (rotation about z)', [(1, 0, 0, 0), (3, 0, 0, 1)], 'Q'),
        ('n=3 record subset', [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5)], 'Q'),
        ('n=3 two cubes share a face axis', [(1, 0, 0, 0), (2, 0, 0, 1), (3, 1, 2, 2)], 'Q'),
        ('n=4 RECORD 183', [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (1, 1, 1, 1)], 'Q'),
        ('n=4 refuter 173 (P373)', [(1, 0, 0, 0), (0, 2, -3, -2), (0, 2, -3, 2), (-4, -2, -5, -6)], 'Q'),
        ('n=4 near-coincident', [(1, 0, 0, 0), (100, 1, 0, 0), (1, 1, 1, 1), (3, 1, 2, 2)], 'Q'),
        ('n=4 with a shared face axis', [(1, 0, 0, 0), (3, 0, 0, 1), (4, 1, 1, -1), (5, -1, -5, -5)], 'Q'),
    ]
    rnd = random.Random(20260930)
    for r in range(8):
        qs = [tuple(rnd.randint(-6, 6) for _ in range(4)) for _ in range(4)]
        qs = [q if any(q) else (1, 0, 0, 0) for q in qs]
        cases.append(('n=4 random #%d' % r, qs, 'Q'))
    golden = [(R5, K(1), K(1), K(1)), (R5, K(1), K(-1), K(-1)), (R5, K(-1), K(1), K(-1)), (R5, K(-1), K(-1), K(1))]
    out, bad = [], 0
    for name, qs, fld in cases + [('n=4 GOLDEN 177, Q(sqrt5)', golden, 'K')]:
        C = Compound(qs, fld)
        tot, dep = C.count()
        eng = engine_q5(["0:1,1,1,1", "0:1,1,-1,-1", "0:1,-1,1,-1", "0:1,-1,-1,1"]) if fld == 'K' else engine(qs)
        ok = eng is not None and tot == eng
        bad += not ok
        line = '%-44s sphere %4d  engine %-5s %s  depths %s' % (name, tot, eng, 'AGREE' if ok else
                                                             ('UNEVALUATED' if eng is None else 'DISAGREE'), dep)
        print(line, flush=True)
        row = {'case': name, 'sphere': tot, 'engine': eng, 'depths': dep}
        if C.n == 4:
            mv = C.mv_checks()
            viol = [r for r in mv if r[1] > r[2] + r[3] + r[4] - 2]
            capT = max(r[1] for r in mv if r[0][0] == 'T')
            capD = max(r[1] for r in mv if r[0][0] == 'D')
            capmT = max(r[4] for r in mv if r[0][0] == 'T')
            capmD = max(r[4] for r in mv if r[0][0] == 'D')
            print('      MV violations %d | max T_i %d (cap 26) | max pair set %d (cap 22) | max m %d/%d (caps 6/12)'
                  % (len(viol), capT, capD, capmT, capmD), flush=True)
            bad += bool(viol) + (capT > 26) + (capD > 22) + (capmT > 6) + (capmD > 12)
            row['mv'] = mv
        out.append(row)
    # MUST-DISAGREE controls on the record: without the joining step (PIECES untested), and with
    # ties counted as wins (DEPTH's strictness untested).  Measured 2026-09-30: 195 and 95.
    global feasible
    rec = Compound([(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5), (1, 1, 1, 1)])
    joined = rec.components
    rec.components = lambda pieces: sum(1 for c, fr in pieces if feasible(c, fr))
    c1 = rec.count()[0]
    rec.components = joined
    strict_feasible = feasible
    feasible = lambda cons, fr: strict_feasible([(c, False) for c, st in cons], fr)
    c2 = rec.count()[0]
    feasible = strict_feasible
    for name, c in (('pieces not joined', c1), ('ties counted as wins', c2)):
        print('control %-22s %4d  %s' % (name, c, 'disagrees with 183, as it must' if c != 183 else 'AGREES: VACUOUS'))
        bad += c == 183
    json.dump(out, open(os.path.join(ROOT, 'data', 'sphere_count.json'), 'w'), indent=1, default=str)
    print('\n%s' % ('ALL AGREE, no MV violation, no cap exceeded' if not bad else '%d PROBLEMS' % bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
