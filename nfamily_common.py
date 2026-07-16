#!/usr/bin/env python3
# Working principles: NFAMILY_SPEC.md. Project index: README.md
"""Exact rational arithmetic core for the n-cube BIG/DIHEDRAL FAMILY.

The family (NFAMILY_SPEC.md): n cubes, each with a face-axis u(theta_k)
perpendicular to a common axis s=(1,1,1)/sqrt3, common tilt psi, free
phases theta_k. Derivation here (verified symbolically with sympy,
2026-07-16): the RELATIVE rotation between family members j and k depends
ONLY on (Delta = theta_k - theta_j, psi), and is EXACTLY the Rodrigues
rotation by angle Delta about the FIXED axis n(psi) = (sin psi, cos psi, 0):

    Rel(Delta, psi) =
      [ cosD*cosP^2 + sinP^2,   cosP*sinP*(1-cosD),   cosP*sinD ]
      [ cosP*sinP*(1-cosD),     cosD*sinP^2 + cosP^2, -sinD*sinP]
      [ -cosP*sinD,             sinD*sinP,             cosD     ]

(This is the standard Rodrigues formula R = cosD*I + sinD*[n]_x +
(1-cosD)*n n^T for n=(sinP,cosP,0); confirmed to equal M_1(psi)^-1 M_2
(psi,theta) of bigfamily.py's cubeM by direct symbolic expansion using
sqrt2*sqrt3=sqrt6 -- the irrational face-axis frame vectors cancel
completely.)

Since a global rotation of the WHOLE compound does not change region
counts, WLOG set theta_1 = 0 (cube 1 = identity); then cube_k's matrix
in this gauge is exactly Rel(theta_k, psi) for k=2..n. When psi and every
theta_k are Pythagorean angles (sin,cos rational), every cube matrix is
RATIONAL -- integer quaternions after clearing denominators -- and the
whole n-cube family compound is countable by the fast C++ engine.

No floats anywhere in this module's exact path; only `fractions.Fraction`.
"""
import math
from fractions import Fraction as Fr
from itertools import product


class PyAngle:
    """A Pythagorean angle: cos, sin both exact Fractions with c^2+s^2=1."""
    __slots__ = ('c', 's')

    def __init__(self, c, s):
        self.c = Fr(c)
        self.s = Fr(s)
        assert self.c * self.c + self.s * self.s == 1, 'not on unit circle'

    @classmethod
    def from_pqr(cls, p, q, r, sign_p=1, sign_q=1):
        """sin = sign_p*p/r, cos = sign_q*q/r, p^2+q^2=r^2."""
        assert p * p + q * q == r * r, f'not Pythagorean: {p},{q},{r}'
        return cls(Fr(sign_q * q, r), Fr(sign_p * p, r))

    def __repr__(self):
        return f'PyAngle(c={self.c}, s={self.s})'

    def __mul__(self, other):
        """Angle addition (complex multiplication of unit points)."""
        if isinstance(other, PyAngle):
            return PyAngle(self.c * other.c - self.s * other.s,
                            self.s * other.c + self.c * other.s)
        return NotImplemented

    def inv(self):
        """Angle negation (complex conjugate)."""
        return PyAngle(self.c, -self.s)

    def pow(self, k):
        """Exact angle*k via fast exponentiation (k any integer)."""
        if k < 0:
            return self.inv().pow(-k)
        result = PyAngle(Fr(1), Fr(0))
        base = self
        while k:
            if k & 1:
                result = result * base
            base = base * base
            k >>= 1
        return result

    def deg(self):
        return math.degrees(math.atan2(float(self.s), float(self.c)))


IDENTITY_ANGLE = PyAngle(Fr(1), Fr(0))


def rel_matrix(delta, psi):
    """Exact Rel(Delta, psi) 3x3 Fraction matrix (see module docstring)."""
    cd, sd = delta.c, delta.s
    cp, sp = psi.c, psi.s
    return [
        [cd * cp * cp + sp * sp,       cp * sp * (1 - cd),   cp * sd],
        [cp * sp * (1 - cd),           cd * sp * sp + cp * cp, -sd * sp],
        [-cp * sd,                     sd * sp,               cd],
    ]


IDENTITY3 = [[Fr(1), Fr(0), Fr(0)], [Fr(0), Fr(1), Fr(0)], [Fr(0), Fr(0), Fr(1)]]


def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)]
            for i in range(3)]


def mat_transpose(A):
    return [[A[j][i] for j in range(3)] for i in range(3)]


def is_rotation_exact(M, tol_check=True):
    """Exact orthonormality + det=+1 check (Fraction arithmetic, no floats)."""
    Mt = mat_transpose(M)
    MtM = mat_mul(Mt, M)
    for i in range(3):
        for j in range(3):
            want = Fr(1) if i == j else Fr(0)
            if MtM[i][j] != want:
                return False
    det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
           - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
           + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
    return det == 1


def matrix_to_quat_exact(M):
    """Exact rational rotation matrix -> rational quaternion (w,x,y,z),
    entirely SQUARE-ROOT-FREE (unlike textbook Shepperd's method).

    Rationale (Cayley parametrization of SO(3,Q), no algebraic extension
    needed -- this is why G0 holds unconditionally for any rational
    rotation, not just "lucky" family members): the outer product q q^T
    has entries that are RATIONAL LINEAR combinations of M's entries (the
    familiar Shepperd relations 4w^2=1+tr(M), 4wx=M32-M23, etc, all
    degree-1 in M). Any row of q q^T equals q_i * q, so it is proportional
    to q itself -- take the row whose diagonal entry (q_i^2, guaranteed
    >=1 for the largest of the four since they sum to 4) is largest, and
    that ROW, verbatim, already IS q up to a positive rational scalar. No
    square root is ever needed. Returns Fractions (unnormalized scale);
    caller clears denominators."""
    a, b, c, d = M[0][0], M[1][1], M[2][2], None
    T = a + b + c
    cands = [1 + T, 1 + a - b - c, 1 - a + b - c, 1 - a - b + c]
    idx = max(range(4), key=lambda i: cands[i])
    rows = [
        (1 + T,          M[2][1] - M[1][2],  M[0][2] - M[2][0],  M[1][0] - M[0][1]),
        (M[2][1] - M[1][2], 1 + a - b - c,   M[0][1] + M[1][0],  M[0][2] + M[2][0]),
        (M[0][2] - M[2][0], M[0][1] + M[1][0], 1 - a + b - c,    M[1][2] + M[2][1]),
        (M[1][0] - M[0][1], M[0][2] + M[2][0], M[1][2] + M[2][1], 1 - a - b + c),
    ]
    assert cands[idx] > 0, 'degenerate: all four candidates <= 0 (impossible for a rotation)'
    return tuple(Fr(v) for v in rows[idx])


def quat_to_matrix_exact(w, x, y, z):
    """Exact rational quaternion (ints or Fractions) -> rotation matrix,
    same convention as golden_rotations.rot_from_quat (scalar-first)."""
    w, x, y, z = Fr(w), Fr(x), Fr(y), Fr(z)
    n = w * w + x * x + y * y + z * z
    def q(v):
        return v / n
    return [
        [q(w*w + x*x - y*y - z*z), q(2*(x*y - w*z)), q(2*(x*z + w*y))],
        [q(2*(x*y + w*z)), q(w*w - x*x + y*y - z*z), q(2*(y*z - w*x))],
        [q(2*(x*z - w*y)), q(2*(y*z + w*x)), q(w*w - x*x - y*y + z*z)],
    ]


def quat_to_int(w, x, y, z, cap=512):
    """Clear denominators of a rational quaternion, gcd-reduce, return
    integer tuple. Raises ValueError if any |component| > cap after
    reduction (the C++ engine's int128 budget, CPP_SPEC.md)."""
    fracs = [Fr(w), Fr(x), Fr(y), Fr(z)]
    lcd = 1
    for f in fracs:
        lcd = lcd * f.denominator // math.gcd(lcd, f.denominator)
    ints = [int(f * lcd) for f in fracs]
    g = math.gcd(*[abs(i) for i in ints]) if any(ints) else 1
    if g > 1:
        ints = [i // g for i in ints]
    if not any(ints):
        ints = [1, 0, 0, 0]
    mx = max(abs(i) for i in ints)
    if mx > cap:
        raise ValueError(f'quat {ints} exceeds cap {cap} (max |c|={mx})')
    return tuple(ints)


def matrix_to_int_quat(M, cap=512):
    """Full pipeline + exact round-trip verification (GATE G0 primitive).
    Returns integer quat tuple; raises AssertionError if round-trip fails."""
    w, x, y, z = matrix_to_quat_exact(M)
    ints = quat_to_int(w, x, y, z, cap=cap)
    back = quat_to_matrix_exact(*ints)
    for i in range(3):
        for j in range(3):
            assert back[i][j] == M[i][j], (
                f'round-trip FAILED at ({i},{j}): {back[i][j]} != {M[i][j]}')
    return ints


def build_family_quats(psi, thetas, cap=512):
    """thetas: list of PyAngle, theta[0] convention is 0 (cube 1 = I) but
    not enforced -- Delta is always taken against thetas[0].
    Returns list of n integer quat tuples (w,x,y,z), and the list of exact
    Fraction matrices (for downstream exact crossing counts)."""
    quats = []
    mats = []
    base = thetas[0]
    for th in thetas:
        delta = th * base.inv()
        M = rel_matrix(delta, psi)
        assert is_rotation_exact(M), 'family matrix failed orthonormality/det check'
        q = matrix_to_int_quat(M, cap=cap)
        quats.append(q)
        mats.append(M)
    return quats, mats


# ---- Pythagorean angle menus -------------------------------------------

# Same (p,q,r) triples as q3_count.py's driver (read-only reference file;
# reproduced here, not imported, to keep this module standalone). Spans
# (0,90) degrees at roughly-even spacing.
PQR_MENU = [(0,1,1),(13,84,85),(11,60,61),(9,40,41),(16,63,65),(7,24,25),(12,35,37),
            (5,12,13),(36,77,85),(39,80,89),(8,15,17),(33,56,65),(28,45,53),(3,4,5),
            (48,55,73),(65,72,97),(20,21,29),(21,20,29),(72,65,97),(55,48,73),(4,3,5),
            (45,28,53),(56,33,65),(15,8,17),(80,39,89),(77,36,85),(12,5,13),(35,12,37),
            (24,7,25),(63,16,65),(40,9,41),(60,11,61),(84,13,85),(1,0,1)]


def menu_angles():
    """PQR_MENU as sorted-by-degree PyAngle list covering [0,90]."""
    out = []
    for p, q, r in PQR_MENU:
        a = PyAngle.from_pqr(p, q, r)
        out.append(a)
    out.sort(key=lambda a: a.deg())
    return out


# Small extra triples (r<=65 primitive + a few composite) for building
# SMALL-DENOMINATOR phase angles independent of the psi menu (keeps quat
# components under the 512 cap for larger n without chain compounding).
SMALL_PQR = [(0,1,1),(3,4,5),(4,3,5),(5,12,13),(12,5,13),(8,15,17),(15,8,17),
             (7,24,25),(24,7,25),(20,21,29),(21,20,29),(9,40,41),(40,9,41),
             (12,35,37),(35,12,37),(11,60,61),(60,11,61),(28,45,53),(45,28,53),
             (33,56,65),(56,33,65),(16,63,65),(63,16,65),(48,55,73),(55,48,73),
             (13,84,85),(84,13,85),(36,77,85),(77,36,85),(39,80,89),(80,39,89),
             (65,72,97),(72,65,97),(1,0,1)]


def small_menu_angles():
    out = [PyAngle.from_pqr(p, q, r) for p, q, r in SMALL_PQR]
    out.sort(key=lambda a: a.deg())
    return out


# ---- exact edge-edge crossing counter (Q3) -------------------------------

def _cube_edges_fraction():
    """The 12 edges of [-1,1]^3 as (corner, direction) Fraction vectors,
    same convention as dihedral_scratch/edge_close4.py's EDGES: edge a
    (free axis a, corner fixed on the other two axes at +-1) runs from
    corner-direction to corner+direction, i.e. param corner + t*direction,
    t in [-1,1]."""
    edges = []
    for a in range(3):
        o = [i for i in range(3) if i != a]
        for s1, s2 in product((-1, 1), repeat=2):
            c = [Fr(0), Fr(0), Fr(0)]
            c[o[0]], c[o[1]] = Fr(s1), Fr(s2)
            d = [Fr(0), Fr(0), Fr(0)]
            d[a] = Fr(1)
            edges.append((tuple(c), tuple(d)))
    return edges


EDGES_FR = _cube_edges_fraction()


def _mat_vec(M, v):
    return tuple(sum(M[i][k] * v[k] for k in range(3)) for i in range(3))


def _cross(u, v):
    return (u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0])


def _dot(u, v):
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]


def _sub(u, v):
    return (u[0]-v[0], u[1]-v[1], u[2]-v[2])


def exact_pair_crossings(Mi, Mj, edges=EDGES_FR):
    """Exact count of INTERIOR edge-edge crossings between cubes i and j
    (Fraction 3x3 rotation matrices). No floats, no tolerances: coplanarity
    is an exact Fraction equality; interior means strictly -1 < t,s < 1
    (corner touches, |t| or |s| == 1, are excluded -- matches the
    bigfamily.py / pairmap.py float convention with tol->0 and
    |t|<0.999 exactness, made exact here).

    Method: transform each edge's (corner, direction) by the cube's exact
    rotation; two segments C1+t D1, C2+s D2 cross in their interior iff
    (a) coplanar: (C2-C1).(D1 x D2) == 0 exactly,
    (b) not parallel: D1 x D2 != 0,
    (c) solving C1+tD1 = C2+sD2 in the 2 coordinates with the larger
        |component| of n=D1xD2 (Cramer's rule, exact) gives -1<t<1, -1<s<1
        strictly, and the third coordinate equation also holds exactly
        (sanity check on the coplanar solve)."""
    edges_i = [(_mat_vec(Mi, c), _mat_vec(Mi, d)) for c, d in edges]
    edges_j = [(_mat_vec(Mj, c), _mat_vec(Mj, d)) for c, d in edges]
    n_cross = 0
    for C1, D1 in edges_i:
        for C2, D2 in edges_j:
            n = _cross(D1, D2)
            if n == (0, 0, 0):
                continue  # parallel, no isolated crossing
            w = _sub(C2, C1)
            if _dot(w, n) != 0:
                continue  # not coplanar
            # Solve t*D1 - s*D2 = C2-C1 using the 2 rows with largest |n| component
            idx = max(range(3), key=lambda k: abs(n[k]))
            rows = [k for k in range(3) if k != idx]
            r0, r1 = rows
            a11, a12 = D1[r0], -D2[r0]
            a21, a22 = D1[r1], -D2[r1]
            b1, b2 = w[r0], w[r1]
            det = a11 * a22 - a12 * a21
            if det == 0:
                continue  # degenerate 2x2 (shouldn't happen given idx choice)
            t = (b1 * a22 - a12 * b2) / det
            s = (a11 * b2 - b1 * a21) / det
            # sanity: third coordinate equation must also hold exactly
            k3 = idx
            if t * D1[k3] - s * D2[k3] != w[k3]:
                continue  # numerically shouldn't happen for exactly coplanar lines
            if -1 < t < 1 and -1 < s < 1:
                n_cross += 1
    return n_cross


def exact_config_crossings(mats):
    """All-pairs exact interior edge crossing counts for a compound.
    Returns dict {(i,j): count} for i<j."""
    out = {}
    for i in range(len(mats)):
        for j in range(i + 1, len(mats)):
            out[(i, j)] = exact_pair_crossings(mats[i], mats[j])
    return out


# ---- family-position axis test (Q3 confirmation) -------------------------

def _cube_rotation_group():
    """The 24 proper (det=+1) signed-permutation matrices -- the rotation
    group of the axis-aligned cube. Used to search over which of a cube's
    3 face axes (and sign/handedness) plays the role of 'u' in the family
    test below, since an arbitrary given pair doesn't come pre-labelled."""
    from itertools import permutations
    G = []
    for perm in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            M = [[Fr(0)] * 3 for _ in range(3)]
            for col, (p, s) in enumerate(zip(perm, signs)):
                M[p][col] = Fr(s)
            det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
                   - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                   + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
            if det == 1:
                G.append(M)
    return G


CUBE_ROT_GROUP = _cube_rotation_group()


def family_axis_test(Mi, Mj):
    """Exact confirmation test for Q3: does there exist a common axis s
    and equal tilt psi such that cube i and cube j are both family members
    (a face-axis of each perpendicular to s, common tilt)?

    Derivation (see module docstring): for a TRUE family pair, relative
    rotation R = Mi^T Mj equals Rel(Delta,psi) = Rodrigues(Delta, axis
    n(psi)=(sinP,cosP,0)) in the frame where cube i's own 3rd column is
    the z-axis -- i.e. R's antisymmetric part has a ZERO z-component:
    R[1][0] == R[0][1] exactly (since axis-of-R propto (R21-R12, R02-R20,
    R10-R01) and the third component vanishes identically for Rel).
    An arbitrary given pair isn't pre-labelled with which face is 'u', so
    search over the 24 elements Q of the cube's own rotation group
    (relabeling cube i's axes: R' = Q^T R) for one that satisfies the
    test exactly.

    Returns (is_family, Q) -- Q is a witnessing relabeling matrix, or
    (False, None)."""
    R = mat_mul(mat_transpose(Mi), Mj)
    for Q in CUBE_ROT_GROUP:
        Rp = mat_mul(mat_transpose(Q), R)
        if Rp[1][0] == Rp[0][1]:
            return True, Q
    return False, None


if __name__ == '__main__':
    # Self-test: G0-style sanity checks run standalone.
    print('nfamily_common self-test')
    a = PyAngle.from_pqr(3, 4, 5)       # 36.8699 deg
    psi = PyAngle.from_pqr(4, 3, 5)     # 53.1301 deg
    M = rel_matrix(a, psi)
    assert is_rotation_exact(M)
    q = matrix_to_int_quat(M)
    print(f'  a=36.87deg psi=53.13deg -> Rel matrix rational, quat={q}  OK')
    # chain a=36.87, k=0..2 (n=3), psi=53.13
    thetas = [IDENTITY_ANGLE, a, a.pow(2)]
    quats, mats = build_family_quats(psi, thetas)
    print(f'  n=3 chain quats: {quats}')
    print('self-test OK')
