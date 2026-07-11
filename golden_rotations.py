#!/usr/bin/env python3
# Working principles: six_cube_search_results.md (rot_from_quat rational-rotation basis). Project index: README.md
"""Exact arithmetic in the dense rotation group <cube, dodecahedron>.

The rotation group O of the (axis-aligned) cube and the rotation group I of
the standard dodecahedron together generate a countable DENSE subgroup of
SO(3) (no closed subgroup lies strictly between a maximal finite group and
SO(3) itself).  Every element of <O, I> is a 3x3 orthogonal matrix with
entries in the golden field Q(sqrt5):

  - O: signed permutation matrices (entries 0, +-1),
  - I: the classic golden matrices, e.g. (1/2)[[1,-phi,1/phi],
       [phi,1/phi,-1],[1/phi,1,phi]] - a 72-degree turn about (1,0,phi).

Representation
--------------
A rotation is stored as its exact matrix (9 entries, each a pair of
rationals a + b*sqrt5).  This is a CANONICAL finite string: two generator
words denote the same rotation iff their matrices are equal entry-by-entry,
so the word problem for <O, I> is decided by comparing strings.  Words in
the generators are supported as human-friendly input/output; the matrix is
the normal form.

Generators (word alphabet; uppercase = inverse):
  a : 90-degree rotation about z            (cube;  a^4 = 1)
  b : cyclic rotation about (1,1,1)         (shared 3-fold: in O AND I; b^3=1)
  d : 72-degree rotation about (1, 0, phi)  (dodecahedron; d^5 = 1)

O = <a, b> (order 24),  I = <d, b> (order 60),  O intersect I = T (order 12)
- the tetrahedral amalgam this whole geometry runs on; verified at import.

Why exact matrices and not quaternions
--------------------------------------
"Matrix vs quaternion" is a representation choice; "exact field vs floating
point" is an arithmetic choice.  Most classic pro-quaternion arguments are
really arguments against FLOATING-POINT matrices and die under exactness:
  - drift/renormalisation: moot - these matrices are exactly orthogonal
    forever (is_rotation is a check, not maintenance);
  - compactness: a wash (see field sizes below: 16 vs 18 rationals);
  - slerp: inapplicable - interpolation leaves the countable group and
    needs transcendentals, which have no exact form; targets are
    approximated by word search, not slerp.

The twist: quaternion components are HALF-angle data (cos(theta/2) etc.),
and the cube's 90-degree generator lifts to (1+k)/sqrt2, so the double
cover of <O, I> needs the degree-4 field Q(sqrt2, sqrt5).  The icosahedral
half alone lifts beautifully (binary icosahedral group = unit icosians,
entries in Q(sqrt5)), but binary octahedral drags in sqrt2.  The SO(3)
matrices see only whole angles and stay in the degree-2 golden field.
Cost: matrix product = 27 Q(sqrt5) mults (~108 rational mults); quaternion
product = 16 degree-4-field mults (~256 rational mults) - about 2x.  The
matrix is also canonical as-is (no q ~ -q sign convention) and acts on
Q(sqrt5) points with one product instead of the sandwich q v q~.

What quaternions genuinely keep:
  1. the double cover itself: a 2*pi word evaluates to -1 there (the
     fermionic sign on spin-1/2); the SO(3) matrix is blind to it;
  2. the 4D vista: icosians -> 600-cell, H4, and the icosian construction
     of E8, where quaternions are the native language;
  3. floating-point applications (graphics/robotics), where cheaper
     composition and trivial renormalisation still favour them.
Build the Q(sqrt2, sqrt5) quaternion lift the day the spin or the 4D
structure of these rotations matters; for exact group arithmetic and the
word problem in SO(3), the golden matrices win.

Rounding to bounded rationals
-----------------------------
Word length k costs precision: the generator D has quarter-integer entries,
so a word with m d-letters has entry denominators up to 4^m.  Two sound
rounding operations keep the notation small; naive per-entry rounding is
NOT one of them (it breaks orthogonality, and exact re-orthogonalisation
needs square roots that leave the field):

  round_rot(R, max_denom)  - round via the quaternion parametrisation:
      every integer quaternion (a,b,c,d) yields an EXACTLY orthogonal
      matrix with denominator n = a^2+b^2+c^2+d^2 (rational points are
      dense in SO(3)).  A float quaternion guides the rounding at a COMMON
      scale N = isqrt(max_denom), so the matrix denominator is <= max_denom
      by construction and the error angle scales ~ 2/sqrt(max_denom).  The
      error is CERTIFIED afterwards in exact arithmetic (cos of the
      relative angle, an element of Q(sqrt5)), so float sloppiness in the
      guide cannot corrupt the guarantee.  The result generally leaves the
      word-group <O, I> but stays in SO(3, Q) - exact, bounded height.
      Multiply-exactly-then-round gives floating-point-style arithmetic on
      SO(3) with exact carriers and per-operation certified error.

  word_round(R, radius)    - in-group rounding: nearest element of the
      word ball of given radius (exact comparison of relative-angle
      cosines).  Stays in <O, I>; coarse at small radius.  Scaling this to
      fine precision with words of length polylog(1/eps) is exactly the
      Solovay-Kitaev algorithm, which this library's exact metric would
      support.

API
---
  Rot            exact rotation; * (compose), .inv(), ==, hash, .apply(v)
  Rot.to_str() / Rot.from_str(s)    canonical finite-string form
  word(s)                           generator word -> Rot
  closure(gens)                     finite closure by BFS (finite subgroups)
  ball(radius)                      distinct rotations of word length <= r

Run as a script for self-tests and a small tour (group orders, the A4
intersection, exponential ball growth = density in action, a word-problem
collision, and the smallest rotation angle reached at each radius).
"""
import math
import sys
from fractions import Fraction as Fr
from itertools import product

from cube_compound_exact import Q5, ZERO, ONE

H = Q5(Fr(1, 2))
PH2 = Q5(Fr(1, 4), Fr(1, 4))     # phi/2
IPH2 = Q5(Fr(-1, 4), Fr(1, 4))   # 1/(2*phi)
NEG = lambda x: -x


class Rot:
    __slots__ = ('m',)

    def __init__(self, rows):
        self.m = tuple(tuple(rows[i][j] for j in range(3)) for i in range(3))

    def __mul__(a, b):
        m, n = a.m, b.m
        return Rot([[m[i][0] * n[0][j] + m[i][1] * n[1][j] + m[i][2] * n[2][j]
                     for j in range(3)] for i in range(3)])

    def inv(self):
        return Rot([[self.m[j][i] for j in range(3)] for i in range(3)])

    def __eq__(s, o):
        return isinstance(o, Rot) and s.m == o.m

    def __hash__(s):
        return hash(s.m)

    def apply(self, v):
        return tuple(self.m[i][0] * v[0] + self.m[i][1] * v[1]
                     + self.m[i][2] * v[2] for i in range(3))

    def det(self):
        m = self.m
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    def is_rotation(self):
        m = self.m
        for i in range(3):
            for j in range(3):
                d = sum((m[k][i] * m[k][j] for k in range(3)),
                        Q5(0)) - (ONE if i == j else Q5(0))
                if d.sign() != 0:
                    return False
        return (self.det() - ONE).sign() == 0

    def cos_angle(self):
        """Exact cos(theta) = (trace - 1)/2, an element of Q(sqrt5)."""
        tr = self.m[0][0] + self.m[1][1] + self.m[2][2]
        return (tr - ONE) * H

    def axis(self):
        """Unnormalised rotation axis (exact); zero vector for identity/pi."""
        m = self.m
        return (m[2][1] - m[1][2], m[0][2] - m[2][0], m[1][0] - m[0][1])

    def to_str(self):
        return ';'.join(f'{e.a},{e.b}' for row in self.m for e in row)

    @staticmethod
    def from_str(s):
        parts = s.split(';')
        assert len(parts) == 9
        es = [Q5(Fr(p.split(',')[0]), Fr(p.split(',')[1])) for p in parts]
        r = Rot([es[0:3], es[3:6], es[6:9]])
        assert r.is_rotation(), 'string does not encode a rotation'
        return r

    def __repr__(self):
        return 'Rot[' + self.to_str() + ']'


IDENT = Rot([[ONE, ZERO, ZERO], [ZERO, ONE, ZERO], [ZERO, ZERO, ONE]])

# generators
A = Rot([[ZERO, -ONE, ZERO], [ONE, ZERO, ZERO], [ZERO, ZERO, ONE]])   # z, 90
B = Rot([[ZERO, ZERO, ONE], [ONE, ZERO, ZERO], [ZERO, ONE, ZERO]])    # (1,1,1)
D = Rot([[H, -PH2, IPH2], [PH2, IPH2, -H], [IPH2, H, PH2]])           # 72 deg

GEN = {'a': A, 'b': B, 'd': D, 'A': A.inv(), 'B': B.inv(), 'D': D.inv()}


def word(s):
    r = IDENT
    for ch in s:
        r = r * GEN[ch]
    return r


def closure(gens, cap=1000):
    gens = list(gens) + [g.inv() for g in gens]
    seen = {IDENT}
    frontier = [IDENT]
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                y = x * g
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
                    if len(seen) > cap:
                        raise RuntimeError('closure exceeded cap (infinite?)')
        frontier = nxt
    return seen


def ball(radius, alphabet='aAbBdD'):
    """Distinct rotations of word length <= radius; also returns one
    word-problem collision (two different shortest words, same rotation)."""
    seen = {IDENT: ''}
    frontier = [(IDENT, '')]
    collision = None
    sizes = []
    for _ in range(radius):
        nxt = []
        for x, w in frontier:
            for ch in alphabet:
                y = x * GEN[ch]
                if y not in seen:
                    seen[y] = w + ch
                    nxt.append((y, w + ch))
                elif collision is None and len(seen[y]) == len(w) + 1 \
                        and seen[y] != w + ch:
                    collision = (seen[y], w + ch)
        frontier = nxt
        sizes.append(len(seen))
    return seen, sizes, collision


def max_denominator(R):
    return max(max(e.a.denominator, e.b.denominator)
               for row in R.m for e in row)


def _quat_from_float(M):
    """Float quaternion (w,x,y,z) from a float 3x3 rotation (guide only)."""
    m00, m01, m02 = M[0]
    m10, m11, m12 = M[1]
    m20, m21, m22 = M[2]
    t = m00 + m11 + m22
    if t > 0:
        s = math.sqrt(t + 1.0) * 2
        return (s / 4, (m21 - m12) / s, (m02 - m20) / s, (m10 - m01) / s)
    if m00 >= m11 and m00 >= m22:
        s = math.sqrt(1.0 + m00 - m11 - m22) * 2
        return ((m21 - m12) / s, s / 4, (m01 + m10) / s, (m02 + m20) / s)
    if m11 >= m22:
        s = math.sqrt(1.0 + m11 - m00 - m22) * 2
        return ((m02 - m20) / s, (m01 + m10) / s, s / 4, (m12 + m21) / s)
    s = math.sqrt(1.0 + m22 - m00 - m11) * 2
    return ((m10 - m01) / s, (m02 + m20) / s, (m12 + m21) / s, s / 4)


def rot_from_quat(a, b, c, d):
    """Exact rotation from an integer (or rational) quaternion."""
    n = a * a + b * b + c * c + d * d
    q = lambda x: Q5(Fr(x, n))
    r = Rot([[q(a * a + b * b - c * c - d * d), q(2 * (b * c - a * d)),
              q(2 * (b * d + a * c))],
             [q(2 * (b * c + a * d)), q(a * a - b * b + c * c - d * d),
              q(2 * (c * d - a * b))],
             [q(2 * (b * d - a * c)), q(2 * (c * d + a * b)),
              q(a * a - b * b - c * c + d * d)]])
    assert r.is_rotation()
    return r


def round_rot(R, max_denom=10 ** 6):
    """Round to a nearby exact RATIONAL rotation of bounded height.

    The matrix entries of the result have denominator <= max_denom (a
    common quaternion scale N = isqrt(max_denom) is used, so the matrix
    denominator is a^2+b^2+c^2+d^2 ~ N^2).  Error angle scales roughly as
    2/sqrt(max_denom); simultaneous Diophantine approximation (LLL) could
    do better at the same height.  Returns (rounded Rot, exact cos of the
    error angle in Q(sqrt5)) - the certificate is exact regardless of the
    float guide."""
    qf = _quat_from_float([[float(e) for e in row] for row in R.m])
    # INVARIANT: all four components are rounded at ONE common scale N.
    # Rounding each component to its own best fraction (limit_denominator)
    # and clearing the four denominators certifies smaller errors but makes
    # the common denominator ~ the product of the four, so the matrix
    # height explodes (a max_denom=100 request produced heights ~4e9).
    # The bounded-height guarantee (denominator <= max_denom) lives or dies
    # on the common scale; improve accuracy at fixed height only by better
    # SIMULTANEOUS approximation (e.g. LLL), never per-component.
    N = max(1, math.isqrt(max_denom))
    ints = [round(c * N) for c in qf]
    if not any(ints):
        ints = [1, 0, 0, 0]
    g = math.gcd(*ints)
    if g > 1:
        ints = [i // g for i in ints]
    Q = rot_from_quat(*ints)
    return Q, (R.inv() * Q).cos_angle()


def word_round(R, radius=4):
    """Nearest element of the word ball (in-group rounding).

    Returns (word, rounded Rot, exact cos of the error angle)."""
    seen, _, _ = ball(radius)
    best = None
    for elem, w in seen.items():
        c = (R.inv() * elem).cos_angle()
        if best is None or (c - best[0]).sign() > 0:
            best = (c, w, elem)
    c, w, elem = best
    return w, elem, c


def _angle_deg(cosq):
    return math.degrees(math.acos(max(-1.0, min(1.0, float(cosq)))))


def _selftest():
    assert A.is_rotation() and B.is_rotation() and D.is_rotation()
    assert word('aaaa') == IDENT and word('bbb') == IDENT \
        and word('ddddd') == IDENT
    assert word('aA') == IDENT and word('dD') == IDENT
    # exact round trip
    r = word('adBDa')
    assert Rot.from_str(r.to_str()) == r

    octa = closure([A, B])
    icosa = closure([D, B])
    inter = octa & icosa
    assert len(octa) == 24, len(octa)
    assert len(icosa) == 60, len(icosa)
    assert len(inter) == 12, len(inter)   # the tetrahedral amalgam A4

    # D permutes the dodecahedron vertices
    PHI, IPHI = Q5(Fr(1, 2), Fr(1, 2)), Q5(Fr(-1, 2), Fr(1, 2))
    dod = set()
    for s in product((1, -1), repeat=3):
        dod.add(tuple(ONE if c > 0 else -ONE for c in s))
    for cyc in range(3):
        p = [ZERO, IPHI, PHI][-cyc:] + [ZERO, IPHI, PHI][:-cyc]
        nz = [i for i in range(3) if p[i] != ZERO]
        for s1, s2 in product((1, -1), repeat=2):
            q = list(p)
            q[nz[0]] = q[nz[0]] if s1 > 0 else -q[nz[0]]
            q[nz[1]] = q[nz[1]] if s2 > 0 else -q[nz[1]]
            dod.add(tuple(q))
    assert len(dod) == 20
    assert {D.apply(v) for v in dod} == dod
    print('self-tests OK: |O|=24, |I|=60, |O∩I|=12 (=A4), D^5=1, '
          'dodecahedron preserved, canonical strings round-trip')


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] in ('-h', '--help'):
        print(__doc__ or __file__); raise SystemExit(0)
    _selftest()
    radius = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    seen, sizes, collision = ball(radius)
    print(f'ball sizes (word length 1..{radius}): {sizes}')
    if collision:
        w1, w2 = collision
        print(f'word problem demo: "{w1}" and "{w2}" are the SAME rotation '
              f'(canonical strings equal)')
    # smallest nontrivial rotation angle reached: cos closest to 1
    best = None
    for r in seen:
        if r == IDENT:
            continue
        c = r.cos_angle()
        if best is None or (c - best[0]).sign() > 0:
            best = (c, seen[r])
    c, w = best
    print(f'smallest angle in ball: {math.degrees(math.acos(max(-1.0, min(1.0, float(c))))):.3f} deg '
          f'from word "{w}" (cos = {c!r}, exact)')
    # sample product with exact axis/angle data
    r = word('ad')
    print(f'sample: word "ad" -> canonical string {r.to_str()}')
    print(f'        exact cos(angle) = {r.cos_angle()!r}  '
          f'axis ~ {tuple(float(x) for x in r.axis())}')

    # rounding demo: long word -> huge denominators -> bounded rationals
    long_word = 'adbD' * 10
    r = word(long_word)
    print(f'rounding demo: word "{long_word}" (length {len(long_word)}): '
          f'max entry denominator = {max_denominator(r)}')
    for md in (10 ** 4, 10 ** 8):
        q, cerr = round_rot(r, max_denom=md)
        print(f'  round_rot(max_denom={md}): rational rotation, '
              f'max denominator = {max_denominator(q)}, certified error = '
              f'{_angle_deg(cerr):.4f} deg')
    w, elem, cerr = word_round(r, radius=4)
    print(f'  word_round(radius=4): word "{w}", in-group, certified error = '
          f'{_angle_deg(cerr):.2f} deg')
