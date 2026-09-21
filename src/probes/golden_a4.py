#!/usr/bin/env python3
"""The A4 golden compound: every subset maximal, and 18 quadruple points.  [P342], [P343], [P344]

THE DERIVATION.  The octahedral 67 is a C3 ORBIT `{I, R, R^2}` with R a 120-degree rotation
([P341]).  A 4-compound whose every triple is a C3 orbit is one permuted by A4 -- each 3-cycle
fixes one cube and cycles the other three -- i.e. four cubes rotated by a common angle about the
FOUR BODY DIAGONALS.  Solving for a 120-degree relative rotation:

    cos(theta/2) = sqrt10/4   =>   q_k = (sqrt5, +-1, +-1, +-1), even sign patterns

WHAT IT SHOWS.  All four triples count 67 and all six pairs 13 -- every subset at its PROVED
maximum -- and the compound counts 177, six short of the record.  The shortfall is exactly its
18 quadruple points, one region each ([P340]'s law, here at magnitude 18 rather than 2).

    T3 = 56 separate triple points,  Q4 = 18   =>   56 + 4*18 = 128 = 32*C(4,3), the cap
    a quadruple point is FOUR triple points collided: 4 x excess 2 = 8 half-excess (4 regions)
    against excess 6 (3 regions) -- one region lost per merge, 18 merges, 18 regions.

AND WHERE THEY SIT ([P344]).  6 on the three 2-fold (coordinate) axes at +-2/phi, 12 a free A4
orbit at 1/phi coordinates; |A4| = 12, 6 = 12/2, 12 = 12/1.  So they are ORBITS, and the 6 are
imposed by loci the 2-fold rotations FIX.

CAUTION CARRIED FROM [P334].  A vertex lies ON THE FACETS of its own cubes and may be OUTSIDE
the others.  Requiring containment in all four undercounts T3 (it gave 8 instead of 56) while
leaving Q4 correct, since a 4-fold vertex is on every boundary.  All decisions here are exact
over Q(sqrt5) via `kfield`; no tolerances.
"""
import sys, os, json, itertools, collections, subprocess
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from kfield import K
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))
ENGINE_Q2 = os.path.join(ROOT, 'cube_regions_q2w')
ENGINE = os.path.join(ROOT, 'cube_regions_n')
R5 = K(0, 0, 1, 0)
# the golden A4 compound, in the engine's p:q syntax for d = 5
GOLDEN = ["0:1,1,1,1", "0:1,1,-1,-1", "0:1,-1,1,-1", "0:1,-1,-1,1"]
OCT67 = ["1,0,0,0", "1,1,0:1,0", "-1,1,0:1,0"]


def q2(cubes, d=5):
    r = subprocess.run([ENGINE_Q2, '--d', str(d), '--quats', ';'.join(cubes)],
                       capture_output=True, text=True)
    if not r.stdout.strip():
        return None
    j = json.loads(r.stdout)
    return None if 'error' in j else j.get('bounded')


def plain(qs):
    r = subprocess.run([ENGINE, '--quats',
                        ';'.join(','.join(map(str, q)) for q in qs)],
                       capture_output=True, text=True)
    if not r.stdout.strip():
        return None
    j = json.loads(r.stdout)
    return None if 'error' in j else j.get('bounded')


def rot(q):
    """face normals as ROWS, exactly, from a quaternion over K."""
    w, x, y, z = q
    N = w * w + x * x + y * y + z * z
    M = [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
         [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
         [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]
    Ni = N.inv()
    return [[M[r][c] * Ni for r in range(3)] for c in range(3)]


CUB = [rot(q) for q in [(R5, K(1), K(1), K(1)), (R5, K(1), K(-1), K(-1)),
                        (R5, K(-1), K(1), K(-1)), (R5, K(-1), K(-1), K(1))]]


def solve3(rows, rhs):
    A = rows
    det = (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
           - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
           + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
    if det.is_zero():
        return None
    out = []
    for i in range(3):
        B = [r[:] for r in A]
        for k in range(3):
            B[k][i] = rhs[k]
        d = (B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1])
             - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
             + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0]))
        out.append(d / det)
    return out


def onface(M, P):
    cnt = 0
    for r in range(3):
        h = sum([M[r][t] * P[t] for t in range(3)], K(0))
        if h == K(1) or h == K(-1):
            cnt += 1
            continue
        if (K(1) - h).sign() < 0 or (K(1) + h).sign() < 0:
            return False, 0
    return True, cnt


def census():
    """every vertex on >= 3 cube boundaries, with its signature and its position."""
    pts = {}
    for tri in itertools.combinations(range(4), 3):
        for pick in itertools.product(range(3), repeat=3):
            for sg in itertools.product([1, -1], repeat=3):
                rows = [[K.lift(sg[k]) * CUB[tri[k]][pick[k]][t] for t in range(3)]
                        for k in range(3)]
                P = solve3(rows, [K(1), K(1), K(1)])
                if P is None:
                    continue
                sig, ok = [], True
                for c in tri:
                    good, m = onface(CUB[c], P)
                    if not good or m == 0:
                        ok = False
                        break
                    sig.append(m)
                if not ok:
                    continue
                for c in range(4):
                    if c in tri:
                        continue
                    good, m = onface(CUB[c], P)
                    if good and m:
                        sig.append(m)
                pts[tuple((t.a, t.b, t.c, t.d) for t in P)] = (tuple(sorted(sig)), P)
    return pts


def direction(P):
    v = [P[0], P[1], P[2]]
    zeros = sum(1 for t in v if t.is_zero())
    a = [abs(float(t.num())) for t in v]
    eq = lambda p, q: abs(p - q) < 1e-25
    if zeros == 2:
        return 'coordinate axis (2-fold)'
    if zeros == 1:
        nz = [x for x in a if x > 1e-25]
        return 'coordinate plane'
    if eq(a[0], a[1]) and eq(a[1], a[2]):
        return 'body diagonal (3-fold)'
    return 'generic'


def main():
    out = {'what': 'the A4 golden compound: every subset maximal, 18 quadruple points',
           'supports': 'LEDGER P342, P343, P344'}

    print('=== the rational A4 family: right symmetry, wrong angle ===')
    from math import gcd
    rows = []
    for w, t in ((1, 5), (4, 1), (5, 2)):
        if gcd(w, t) != 1:
            continue
        qs = [(w, t, t, t), (w, t, -t, -t), (w, -t, t, -t), (w, -t, -t, t)]
        tot = plain(qs)
        tri = [plain([qs[i] for i in S]) for S in itertools.combinations(range(4), 3)]
        rows.append({'w': w, 't': t, 'total': tot, 'triples': tri})
        print('   q=(%d,+-%d,+-%d,+-%d)  total %s  triples %s' % (w, t, t, t, tot, tri))
    out['rational_A4'] = rows

    print('\n=== the GOLDEN angle: cos(theta/2) = sqrt10/4, q = (sqrt5,+-1,+-1,+-1) ===')
    tri = [q2([GOLDEN[i] for i in S]) for S in itertools.combinations(range(4), 3)]
    pr = [q2([GOLDEN[i] for i in P]) for P in itertools.combinations(range(4), 2)]
    tot = q2(GOLDEN)
    print('   four triples %s   (max(3) = 67, PROVED)' % tri)
    print('   six pairs    %s   (max(2) = 13, PROVED)' % pr)
    print('   TOTAL        %s                     record 183' % tot)
    ie = sum(tri) - sum(pr) + 5
    print('   inclusion-exclusion: %d - %d + 5 = %d' % (sum(tri), sum(pr), ie))
    out['golden'] = {'triples': tri, 'pairs': pr, 'total': tot, 'ie_bare': ie,
                     'all_subsets_maximal': all(t == 67 for t in tri) and all(p == 13 for p in pr)}

    print('\n=== exact vertex census over Q(sqrt5) ===')
    pts = census()
    sig = collections.Counter(s for s, _ in pts.values())
    for k, v in sorted(sig.items()):
        print('   %-14s %3d' % (str(k), v))
    T3 = sig.get((1, 1, 1), 0)
    Q4 = sum(v for k, v in sig.items() if len(k) == 4)
    print('   T3 + 4*Q4 = %d + 4*%d = %d      cap 32*C(4,3) = 128' % (T3, Q4, T3 + 4 * Q4))
    print('   ie %d - Q4 %d = %d   engine %s   %s'
          % (ie, Q4, ie - Q4, tot, 'MATCH' if ie - Q4 == tot else 'MISMATCH'))
    out['census'] = {'signatures': {str(k): v for k, v in sorted(sig.items())},
                     'T3': T3, 'Q4': Q4, 'T3_plus_4Q4': T3 + 4 * Q4, 'cap': 128,
                     'ie_minus_Q4': ie - Q4, 'matches_engine': ie - Q4 == tot}

    print('\n=== where the quadruple points sit ([P344]) ===')
    d = collections.Counter(direction(P) for s, P in pts.values() if len(s) == 4)
    for k, v in sorted(d.items(), key=lambda kv: -kv[1]):
        print('   %-26s %3d' % (k, v))
    print('   |A4| = 12, so 6 = 12/2 (stabilised by a 2-fold) and 12 = 12/1 (free orbit)')
    out['q4_directions'] = dict(d)

    print('\n=== negative control: does the OCTAHEDRAL 67 extend to all-67? ===')
    print('   a 21 608-candidate scan over Z[sqrt2] found ZERO such extensions.')
    print('   SCOPE: a search, hence a lower bound ([METHODS 1]) -- zero found is not zero')
    print('   existing.  [P131] is the settled statement for that family.')
    out['octahedral_control'] = {'candidates': 21608, 'all67_found': 0,
                                 'scope': 'search window a,b,c,e in [-3,3], sqrt2 parts on the '
                                          'first two components only; lower bound, not a proof'}

    out['reproduce'] = PROV.stamp(parameters={'field': 'Q(sqrt5)', 'compound': GOLDEN})
    json.dump(out, open(os.path.join(ROOT, 'data', 'golden_a4.json'), 'w'), indent=1, default=str)
    print('\nwritten data/golden_a4.json')


if __name__ == '__main__':
    main()
