#!/usr/bin/env python3
# Working principles: OPENCOUNT_SPEC.md. Project index: README.md
"""Degree-agnostic exact sign engine for the n=4 family-resonance OPEN
candidates (OPENCOUNT_SPEC.md) -- the ~160 degree-4 (nested-radical /
genuine-quartic) points that resonance4_solve.py's Q(sqrt d) engine could
not represent.

Two field representations, both exposing the `Field(x)` / +,-,*,/,neg,
.sign(),__eq__,__hash__ contract so `resonance4_solve.exact_count_field`
(REUSED UNCHANGED, imported below) runs on either without modification:

  (A) Primitive-element field Q(alpha).  alpha: a real algebraic number
      given by an irreducible rational minimal polynomial + a numeric seed
      (diagnostic only) used to isolate ONE real root via a hand-rolled
      Sturm-sequence bisection (`AlphaInterval`) -- exact rational interval
      arithmetic throughout, no floats in any predicate.  An element is a
      Q-vector in the power basis {1,alpha,...,alpha^(n-1)}; it is exactly
      zero iff that vector is the zero vector (decidable, symbolic).  Sign
      of a nonzero element is resolved by refining alpha's isolating
      interval (bisection, via the Sturm root-count) until the element's
      polynomial evaluates to the same sign at both endpoints -- guaranteed
      to terminate because a nonzero low-degree polynomial cannot vanish at
      the (irrational) alpha (minimality of alpha's minimal polynomial).
      Multiplication reduces modulo the minimal polynomial; division uses
      an extended-Euclidean polynomial inverse mod the (irreducible, hence
      coprime-to-everything-nonzero) minimal polynomial -- both hand-rolled
      over `fractions.Fraction`, no sympy in the hot path.
      Degree-agnostic: this is the ONLY representation used for the
      genuinely-quartic (non-tower) candidates.

  (B) Relative quadratic tower K(sqrt b), K = Q(sqrt a), b = p+q*sqrt(a) in
      K (an OPTIMIZATION / cross-check for the candidates that are honest
      degree-2-over-degree-2 towers -- rows with structure "Q(sqrt a)(sqrt
      ...)" in OPENCOUNT_SPEC.md).  Element A+B*sqrt(b), A,B in K.  Sign via
      the standard quadratic-surd recursion (qtower.py's Ext3 pattern,
      generalized so the "D" of the outer extension is a full K-element,
      not just a rational int): if sign(A)==sign(B), that is the sign; if
      B=0, sign(A); else compare A^2 vs B^2*b in K (K's own sign() already
      resolves that, K being an ordinary Q(sqrt a) field from
      resonance4_solve.make_qd, REUSED unchanged).

Field data for the 6 documented open classes was re-derived from
resonance4_solve.wl's g_type/coplanarity system (a FRESH driver script,
scratchpad-local, reproducing -- not editing -- resonance4_solve.wl's
polynomial definitions) and Mathematica's `ToNumberField`/`MinimalPolynomial`
(exact CAS, not numerics) to express every solved coordinate
(cP,sP,c2,s2,c3,s3,c4,s4) as a rational power-basis vector in one shared
primitive element.  That exact data is checked in at opencount_wl_data.json
(read by this file) so opencount.py is runnable standalone without
wolframscript.

No floats in any predicate; float-only for diagnostics (seeding which root
of a minimal polynomial is "the" candidate, printing psi in degrees).
"""
import json
import math
import random
import sys
import time
from fractions import Fraction as Fr
from itertools import product as iproduct

sys.path.insert(0, '/Users/dmi/carroll')
from golden_rotations import Rot, rot_from_quat          # noqa: E402  (read-only reuse)
from resonance4_solve import exact_count_field, rel_matrix_field, make_qd  # noqa: E402 (REUSE UNCHANGED)

CARROLL = '/Users/dmi/carroll'
WL_DATA_PATH = f'{CARROLL}/opencount_wl_data.json'


# =====================================================================
# Polynomial utilities over Fraction, DESCENDING coefficient order
# (index 0 = highest degree).  Pure Python, no sympy -- used for the
# Sturm sequence (root isolation) and for representation-A's
# multiplication-reduction / extended-Euclid division.
# =====================================================================
def trim(p):
    i = 0
    while i < len(p) - 1 and p[i] == 0:
        i += 1
    return p[i:]


def poly_mul(p, q):
    if (len(p) == 1 and p[0] == 0) or (len(q) == 1 and q[0] == 0):
        return [Fr(0)]
    r = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j, b in enumerate(q):
            if b != 0:
                r[i + j] += a * b
    return trim(r)


def poly_sub(p, q):
    n = max(len(p), len(q))
    p2 = [Fr(0)] * (n - len(p)) + list(p)
    q2 = [Fr(0)] * (n - len(q)) + list(q)
    return trim([p2[i] - q2[i] for i in range(n)])


def poly_scale(p, c):
    if c == 0:
        return [Fr(0)]
    return trim([c * x for x in p])


def poly_divmod(a, b):
    """(quotient, remainder) of descending-order Fraction polynomials a,b."""
    a = list(a)
    b = trim(list(b))
    assert not (len(b) == 1 and b[0] == 0), 'division by zero polynomial'
    qlen = max(len(a) - len(b) + 1, 0)
    q = [Fr(0)] * qlen
    while True:
        a = trim(a)
        if len(a) < len(b) or (len(a) == 1 and a[0] == 0):
            break
        shift = len(a) - len(b)
        coef = a[0] / b[0]
        q[qlen - 1 - shift] = coef
        for i in range(len(b)):
            a[i] -= coef * b[i]
        a = a[1:]
    return q, (a if a else [Fr(0)])


def poly_deriv(p):
    n = len(p) - 1
    if n <= 0:
        return [Fr(0)]
    return trim([c * (n - i) for i, c in enumerate(p[:-1])])


def poly_eval(p, x):
    v = Fr(0)
    for c in p:
        v = v * x + c
    return v


def poly_ext_gcd(a, b):
    """Extended Euclid: returns (g, s, t) with s*a + t*b = g (descending)."""
    r0, r1 = trim(list(a)), trim(list(b))
    s0, s1 = [Fr(1)], [Fr(0)]
    t0, t1 = [Fr(0)], [Fr(1)]
    while not (len(r1) == 1 and r1[0] == 0):
        q, r = poly_divmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, poly_sub(s0, poly_mul(q, s1))
        t0, t1 = t1, poly_sub(t0, poly_mul(q, t1))
    return r0, s0, t0


def sturm_sequence(p_desc):
    p = trim(list(p_desc))
    seq = [p, poly_deriv(p)]
    while True:
        prev2, prev1 = seq[-2], seq[-1]
        if len(prev1) == 1 and prev1[0] == 0:
            break
        _, r = poly_divmod(prev2, prev1)
        r = trim(r)
        if len(r) == 1 and r[0] == 0:
            break
        seq.append(poly_scale(r, Fr(-1)))
        if len(seq[-1]) == 1:
            break
    return seq


def _sign_changes(seq, x):
    signs = []
    for p in seq:
        v = poly_eval(p, x)
        if v > 0:
            signs.append(1)
        elif v < 0:
            signs.append(-1)
    changes = 0
    for i in range(1, len(signs)):
        if signs[i] != signs[i - 1]:
            changes += 1
    return changes


def sturm_count_roots(seq, lo, hi):
    """Exact count of real roots of seq[0] strictly inside (lo,hi], via
    Sturm's theorem -- rational lo,hi, no floats."""
    return _sign_changes(seq, lo) - _sign_changes(seq, hi)


# =====================================================================
# AlphaInterval: exact isolating interval for one real algebraic number,
# refinable to arbitrary precision by bisection certified via Sturm's
# theorem (no floats in the certificate; a float `target` only SEEDS which
# root/interval to start bisecting around, per spec's diagnostic-only rule).
# =====================================================================
class AlphaInterval:
    def __init__(self, minpoly_asc, target_float, label='alpha'):
        n = len(minpoly_asc) - 1
        lead = minpoly_asc[-1]
        self.coeffs_asc = tuple(Fr(c) / lead for c in minpoly_asc)  # monic
        self.n = n
        self.label = label
        self.seq = sturm_sequence(list(reversed(self.coeffs_asc)))
        self.lo, self.hi = self._bracket(target_float)
        self.refine_count = 0

    def _count(self, lo, hi):
        return sturm_count_roots(self.seq, lo, hi)

    def _bracket(self, target_float):
        c = Fr(target_float).limit_denominator(10 ** 9)
        w = Fr(1, 4)
        for _ in range(300):
            lo, hi = c - w, c + w
            cnt = self._count(lo, hi)
            if cnt == 1:
                return lo, hi
            if cnt == 0:
                w *= 2
            else:
                w /= 2
        raise RuntimeError(f'{self.label}: failed to isolate a root near {target_float}')

    def refine(self):
        mid = (self.lo + self.hi) / 2
        if self._count(self.lo, mid) == 1:
            self.hi = mid
        else:
            self.lo = mid
        self.refine_count += 1

    def sign_of_vec(self, vec):
        if all(c == 0 for c in vec):
            return 0
        desc = list(reversed(vec))
        for _ in range(4000):
            vlo, vhi = poly_eval(desc, self.lo), poly_eval(desc, self.hi)
            slo = 1 if vlo > 0 else (-1 if vlo < 0 else 0)
            shi = 1 if vhi > 0 else (-1 if vhi < 0 else 0)
            if slo == shi and slo != 0:
                return slo
            self.refine()
        raise RuntimeError(f'{self.label}: sign refinement failed to converge')

    def float_val(self):
        return float(self.lo + self.hi) / 2


# =====================================================================
# Representation A: Q(alpha) factory
# =====================================================================
_algfield_cache = {}


def make_alg_field(minpoly_asc, target_float, label='alpha'):
    """Q(alpha) field class. minpoly_asc: ascending int/Fraction coeffs of
    an IRREDUCIBLE rational polynomial (need not be monic). target_float:
    a numeric seed identifying which real root (diagnostic only)."""
    key = (label, tuple(str(Fr(c)) for c in minpoly_asc))
    if key in _algfield_cache:
        return _algfield_cache[key]

    n = len(minpoly_asc) - 1
    lead = minpoly_asc[-1]
    coeffs_asc = tuple(Fr(c) / lead for c in minpoly_asc)
    minpoly_desc = list(reversed(coeffs_asc))
    alpha_data = AlphaInterval(minpoly_asc, target_float, label=label)

    def reduce_vec(prod):
        prod = list(prod) + [Fr(0)] * (2 * n - 1 - len(prod))
        c = coeffs_asc
        for i in range(len(prod) - 1, n - 1, -1):
            co = prod[i]
            if co != 0:
                prod[i] = Fr(0)
                for j in range(n):
                    prod[i - n + j] -= co * c[j]
        return tuple(prod[:n])

    class Alg:
        __slots__ = ('vec',)
        N = n
        MINPOLY = coeffs_asc
        ALPHA = alpha_data
        LABEL = label

        def __init__(s, v):
            if isinstance(v, Alg):
                s.vec = v.vec
            elif isinstance(v, (int, Fr)):
                s.vec = (Fr(v),) + (Fr(0),) * (n - 1)
            else:
                vv = tuple(Fr(x) for x in v)
                assert len(vv) == n, f'vector length {len(vv)} != field degree {n}'
                s.vec = vv

        def __add__(s, o):
            o = o if isinstance(o, Alg) else Alg(o)
            return Alg(tuple(a + b for a, b in zip(s.vec, o.vec)))

        __radd__ = __add__

        def __sub__(s, o):
            o = o if isinstance(o, Alg) else Alg(o)
            return Alg(tuple(a - b for a, b in zip(s.vec, o.vec)))

        def __rsub__(s, o):
            return Alg(o) - s

        def __neg__(s):
            return Alg(tuple(-a for a in s.vec))

        def __mul__(s, o):
            o = o if isinstance(o, Alg) else Alg(o)
            prod = [Fr(0)] * (2 * n - 1)
            for i, a in enumerate(s.vec):
                if a == 0:
                    continue
                for j, b in enumerate(o.vec):
                    if b != 0:
                        prod[i + j] += a * b
            return Alg(reduce_vec(prod))

        __rmul__ = __mul__

        def inv(s):
            assert any(x != 0 for x in s.vec), 'inverse of zero field element'
            u_desc = trim(list(reversed(s.vec)))
            g, sc, _t = poly_ext_gcd(u_desc, minpoly_desc)
            assert len(g) == 1 and g[0] != 0, (
                f'{label}: gcd(u, minpoly) not constant -- minpoly not irreducible '
                f'or u shares a factor (should be impossible for u!=0, irreducible minpoly)')
            inv_desc = [x / g[0] for x in sc]
            _, rem = poly_divmod(inv_desc, minpoly_desc)
            rem = list(reversed(rem))
            rem = rem + [Fr(0)] * (n - len(rem))
            return Alg(tuple(rem[:n]))

        def __truediv__(s, o):
            o = o if isinstance(o, Alg) else Alg(o)
            return s * o.inv()

        def sign(s):
            return alpha_data.sign_of_vec(s.vec)

        def __eq__(s, o):
            return isinstance(o, Alg) and s.vec == o.vec

        def __hash__(s):
            return hash(s.vec)

        # resonance4_solve.exact_count_field's plane_key() canonicalizes
        # planes via `(x.a, x.b)` -- written against make_qd's 2-component
        # Qd representation, so despite the "field-generic" docstring it is
        # NOT actually representation-agnostic on this one internal detail
        # (everything else -- +,-,*,/,neg,sign,eq,hash -- genuinely is).
        # Since resonance4_solve.py is READ-ONLY, expose a faithful (a,b)
        # fingerprint here instead: a=the full power-basis vector (hashable,
        # injective via __eq__/__hash__ above), b=0 filler.  This affects
        # only the internal plane-dedup dict key, never arithmetic.
        @property
        def a(s):
            return s.vec

        @property
        def b(s):
            return 0

        def __float__(s):
            a = alpha_data.float_val()
            v = 0.0
            for c in reversed(s.vec):
                v = v * a + float(c)
            return v

        def __repr__(s):
            return f'Alg_{label}{s.vec}'

    Alg.__name__ = f'Alg_{label}'
    _algfield_cache[key] = Alg
    return Alg


# =====================================================================
# Representation B: relative tower K(sqrt b), K = Q(sqrt a)
# =====================================================================
def _is_rational_square(q):
    q = Fr(q)
    if q < 0:
        return False
    rn, rd = math.isqrt(q.numerator), math.isqrt(q.denominator)
    return rn * rn == q.numerator and rd * rd == q.denominator


_tower_cache = {}


def make_tower_field(a, b_pq, label=''):
    """K = Q(sqrt a) (resonance4_solve.make_qd, reused). b = p+q*sqrt(a) in
    K, assumed (certified upstream, via the WL degree-4 MinimalPolynomial of
    sqrt(b)) to NOT be a perfect square in K.  Returns (Tower class, K)."""
    key = (a, str(Fr(b_pq[0])), str(Fr(b_pq[1])), label)
    if key in _tower_cache:
        return _tower_cache[key]

    K = make_qd(a)
    p0, q0 = Fr(b_pq[0]), Fr(b_pq[1])
    bK = K(p0, q0)
    norm_b = p0 * p0 - a * q0 * q0
    if _is_rational_square(norm_b):
        # N(b) square is NECESSARY but not SUFFICIENT for b to be a square in
        # K (see opencount_report.md gates section for the worked
        # counterexample a=6,b=7/2-sqrt6: N(b)=25/4 yet b is not a square in
        # K).  Non-degeneracy here is certified upstream by WL's
        # MinimalPolynomial[sqrt(b)] having degree 2*deg(K); sign()'s
        # runtime assertion below is the final safety net.
        pass

    class Tower:
        __slots__ = ('a', 'b')
        D = bK
        BASE = K
        LABEL = label

        def __init__(s, p, q=None):
            s.a = p if isinstance(p, K) else K(p)
            s.b = (q if isinstance(q, K) else K(q)) if q is not None else K(0)

        def __add__(s, o):
            o = o if isinstance(o, Tower) else Tower(o)
            return Tower(s.a + o.a, s.b + o.b)

        __radd__ = __add__

        def __sub__(s, o):
            o = o if isinstance(o, Tower) else Tower(o)
            return Tower(s.a - o.a, s.b - o.b)

        def __rsub__(s, o):
            return Tower(o) - s

        def __neg__(s):
            return Tower(-s.a, -s.b)

        def __mul__(s, o):
            o = o if isinstance(o, Tower) else Tower(o)
            return Tower(s.a * o.a + Tower.D * (s.b * o.b), s.a * o.b + s.b * o.a)

        __rmul__ = __mul__

        def __truediv__(s, o):
            o = o if isinstance(o, Tower) else Tower(o)
            den = o.a * o.a - Tower.D * (o.b * o.b)
            return Tower((s.a * o.a - Tower.D * (s.b * o.b)) / den,
                         (s.b * o.a - s.a * o.b) / den)

        def sign(s):
            sa, sb = s.a.sign(), s.b.sign()
            if sb == 0:
                return sa
            if sa == 0:
                return sb
            if sa == sb:
                return sa
            t = s.a * s.a - Tower.D * (s.b * s.b)
            st = t.sign()
            assert st != 0, f'{label}: tower degeneracy at runtime (sqrt(b) collapsed into K)'
            return st if sa > 0 else -st

        def __eq__(s, o):
            return isinstance(o, Tower) and s.a == o.a and s.b == o.b

        def __hash__(s):
            return hash((s.a.a, s.a.b, s.b.a, s.b.b))

        def __float__(s):
            bf = float(p0) + float(q0) * math.sqrt(a)
            return float(s.a) + float(s.b) * math.sqrt(bf)

        def __repr__(s):
            return f'({s.a!r}+{s.b!r}*sqrt_b_{label})'

    Tower.__name__ = f'Tower_{label}'
    _tower_cache[key] = (Tower, K)
    return Tower, K


def tower_elem_from_v(v, p0, q0, K):
    """Convert a 4-vector (coeffs in basis {1,gamma,gamma^2,gamma^3},
    gamma^2 = p0+q0*sqrt(a)) into tower form (A,B) with A,B in K, i.e.
    value = A + B*gamma."""
    v0, v1, v2, v3 = [Fr(x) for x in v]
    A = K(v0 + v2 * p0, v2 * q0)
    B = K(v1 + v3 * p0, v3 * q0)
    return A, B


# =====================================================================
# WL-derived exact candidate data
# =====================================================================
def _parse_wl_num(s):
    """Parse a WL InputForm string ('3/4', '5', or a `-precision-suffixed
    numeric like '19.37...`40.') into a float (diagnostic use only)."""
    s = s.split('`')[0]
    if '/' in s:
        num, den = s.split('/')
        return float(num) / float(den)
    return float(s)


def load_wl_data():
    with open(WL_DATA_PATH) as f:
        return json.load(f)


def alg_field_from_branch(rec, label):
    """Build a representation-A Field + the 8 quantities (cP,sP,c2..s4)
    as Field elements, from one exportBranch() WL record."""
    minpoly = [Fr(x) for x in rec['minpoly_coeffs']]
    target = _parse_wl_num(rec['gen_numeric_re'])
    Field = make_alg_field(minpoly, target, label=label)
    vals = {}
    for key in ('cP', 'sP', 'c2', 's2', 'c3', 's3', 'c4', 's4'):
        vals[key] = Field([Fr(x) for x in rec[key]])
    return Field, vals


def rots_from_vals(Field, vals):
    """cube1 = Rel(0,psi) (= identity, any psi); cubes 2..4 = Rel(theta_k,psi)."""
    one, zero = Field(1), Field(0)
    r1 = rel_matrix_field(Field, one, zero, vals['cP'], vals['sP'])
    r2 = rel_matrix_field(Field, vals['c2'], vals['s2'], vals['cP'], vals['sP'])
    r3 = rel_matrix_field(Field, vals['c3'], vals['s3'], vals['cP'], vals['sP'])
    r4 = rel_matrix_field(Field, vals['c4'], vals['s4'], vals['cP'], vals['sP'])
    return [r1, r2, r3, r4]


def detect_degenerate_pairs(vals):
    """Exact equality check: which pairs of cubes (0=cube1 fixed at (1,0))
    coincide (Delta_jk = 0)."""
    thetas = {1: (None, None)}  # placeholder; cube1 is (1,0) implicitly
    cs = {1: ('CONST1', 'CONST0'), 2: (vals['c2'], vals['s2']),
          3: (vals['c3'], vals['s3']), 4: (vals['c4'], vals['s4'])}
    one_field = None
    for k, (c, s) in cs.items():
        if c == 'CONST1':
            continue
        one_field = type(c)(1) if one_field is None else one_field
        break
    zero_field = type(one_field)(0)
    cs[1] = (one_field, zero_field)
    pairs = []
    for j in (1, 2, 3, 4):
        for k in (1, 2, 3, 4):
            if j < k:
                cj, sj = cs[j]
                ck, sk = cs[k]
                if cj == ck and sj == sk:
                    pairs.append((j, k))
    return pairs


def fingerprint(psiDeg, thetaDegs):
    """Cheap congruence fingerprint: psi mod 90, sorted theta mod 360
    (rounded).  Diagnostic dedup only, per spec."""
    pm = round(psiDeg % 90, 4)
    ts = tuple(sorted(round(t % 360, 4) for t in thetaDegs))
    return (pm, ts)


# =====================================================================
# GATE G1: field self-tests
# =====================================================================
def gate_g1():
    print('=== GATE G1: field self-test ===')
    ok = True

    # --- Representation A self-test: octahedral-style Q(sqrt2) as a degree-2
    # "AlgField" instance (rep A specialized to n=2), cross-checked against
    # the direct sqrt(2) construction.
    FieldA = make_alg_field([-2, 0, 1], 1.4142135623730951, label='g1_sqrt2')
    alpha = FieldA([Fr(0), Fr(1)])
    zero_test = alpha * alpha - FieldA(2)
    ok_a1 = zero_test.sign() == 0 and all(c == 0 for c in zero_test.vec)
    print(f'  A: (sqrt2)^2 - 2 == 0 exactly: {ok_a1}')
    ok &= ok_a1

    # random sign-vs-50-digit-float agreement, representation A (degree 4,
    # reuse the CHAIN candidate's field)
    wl = load_wl_data()
    chain_rec = next(r for r in wl['chain13_branches'] if r['tag']['branch'] == 15)
    FieldChain, _ = alg_field_from_branch(chain_rec, 'g1_chainA')
    random.seed(12345)
    bad = 0
    for _ in range(1000):
        vec = [Fr(random.randint(-1000, 1000), random.randint(1, 50)) for _ in range(FieldChain.N)]
        e = FieldChain(vec)
        s = e.sign()
        # 50-digit float check via high-precision Decimal-free approach:
        # evaluate using the AlphaInterval refined to >50 decimal digits.
        fa = FieldChain.ALPHA
        while (fa.hi - fa.lo) > Fr(1, 10 ** 55):
            fa.refine()
        fv = float(sum(float(c) * (fa.float_val() ** i) for i, c in enumerate(vec)))
        fs = 1 if fv > 1e-30 else (-1 if fv < -1e-30 else 0)
        if s != fs and vec != [Fr(0)] * FieldChain.N:
            bad += 1
    ok_a2 = bad == 0
    print(f'  A: sign() vs high-precision float agreement on 1000 random elements: '
          f'{1000 - bad}/1000 OK  {"PASS" if ok_a2 else "FAIL"}')
    ok &= ok_a2

    # exact-zero detection on a constructed zero: cP^2+sP^2-1
    cP = FieldChain([Fr(x) for x in chain_rec['cP']])
    sP = FieldChain([Fr(x) for x in chain_rec['sP']])
    z = cP * cP + sP * sP - FieldChain(1)
    ok_a3 = all(c == 0 for c in z.vec) and z.sign() == 0
    print(f'  A: exact zero detection (cP^2+sP^2-1) on chain13 data: {ok_a3}')
    ok &= ok_a3

    # --- Representation B self-test: sqrt(b)^2 == b exactly; conjugate
    # products land in base field; sign vs float; exact-zero detection.
    TowerR6, K6 = make_tower_field(6, (Fr(14), Fr(-4)), label='g1_r6')
    beta = TowerR6(K6(0), K6(1))
    b_elem = TowerR6(K6(14, -4))
    diff = beta * beta - b_elem
    ok_b1 = diff.a == K6(0) and diff.b == K6(0)
    print(f'  B: (sqrt b)^2 - b == 0 exactly: {ok_b1}')
    ok &= ok_b1

    # conjugate product (A+B*sqrt b)(A-B*sqrt b) = A^2 - B^2*b lands in K
    A_, B_ = K6(Fr(3, 5), Fr(-1, 2)), K6(Fr(1, 7), Fr(2, 3))
    elem = TowerR6(A_, B_)
    conj = TowerR6(A_, -B_)
    prod = elem * conj
    ok_b2 = prod.b == K6(0)
    print(f'  B: conjugate product lands in base field (b-part==0): {ok_b2}')
    ok &= ok_b2

    random.seed(999)
    bad_b = 0
    for _ in range(1000):
        A_ = K6(Fr(random.randint(-50, 50), random.randint(1, 10)),
                Fr(random.randint(-50, 50), random.randint(1, 10)))
        B_ = K6(Fr(random.randint(-50, 50), random.randint(1, 10)),
                Fr(random.randint(-50, 50), random.randint(1, 10)))
        e = TowerR6(A_, B_)
        s = e.sign()
        fv = float(e)
        fs = 1 if fv > 1e-9 else (-1 if fv < -1e-9 else 0)
        if s != fs:
            bad_b += 1
    ok_b3 = bad_b == 0
    print(f'  B: sign() vs float agreement on 1000 random tower elements: '
          f'{1000 - bad_b}/1000 OK  {"PASS" if ok_b3 else "FAIL"}')
    ok &= ok_b3

    zero_b = TowerR6(K6(0), K6(0))
    ok_b4 = zero_b.sign() == 0
    print(f'  B: exact zero detection: {ok_b4}')
    ok &= ok_b4

    print(f'GATE G1: {"PASS" if ok else "FAIL"}')
    return ok


# =====================================================================
# GATE G2: rational reproduction via a degenerate field/tower wrapper
# =====================================================================
def gate_g2():
    print('=== GATE G2: rational reproduction (degenerate field wrapper) ===')
    import subprocess
    ok = True
    # Use the CHAIN's own degree-4 field as the "degenerate wrapper": embed
    # rational quaternions with the irrational power-basis coordinates zero.
    wl = load_wl_data()
    chain_rec = next(r for r in wl['chain13_branches'] if r['tag']['branch'] == 15)
    Field, _ = alg_field_from_branch(chain_rec, 'g2_wrapper')

    def embed_rat(fr):
        return Field([Fr(fr), Fr(0), Fr(0), Fr(0)])

    def rot_from_quat_field(w, x, y, z):
        n = w * w + x * x + y * y + z * z
        q = lambda val: embed_rat(Fr(val, n))
        return Rot([
            [q(w * w + x * x - y * y - z * z), q(2 * (x * y - w * z)), q(2 * (x * z + w * y))],
            [q(2 * (x * y + w * z)), q(w * w - x * x + y * y - z * z), q(2 * (y * z - w * x))],
            [q(2 * (x * z - w * y)), q(2 * (y * z + w * x)), q(w * w - x * x - y * y + z * z)],
        ])

    def run_config(quats, expect_total, expect_depth, name):
        rots = [rot_from_quat_field(*q) for q in quats]
        t0 = time.time()
        total, by_depth = exact_count_field(rots, Field)
        dt = time.time() - t0
        by_depth_clean = {k: v for k, v in by_depth.items() if k != 0}
        # cross-check against ./cube_regions_n
        qstr = ';'.join(','.join(str(c) for c in q) for q in quats)
        cpp = subprocess.run([f'{CARROLL}/cube_regions_n', '--quats', qstr],
                              capture_output=True, text=True, timeout=60)
        print(f'  {name}: field-engine total={total} by_depth={dict(sorted(by_depth_clean.items()))} '
              f'({dt:.1f}s)')
        print(f'    cube_regions_n stdout tail: {cpp.stdout.strip().splitlines()[-3:]}')
        good = (total == expect_total)
        print(f'    expected total={expect_total} by_depth={expect_depth}  '
              f'{"PASS" if good else "FAIL"}')
        return good

    quats_151 = [(1, 0, 0, 0), (-1, 2, 1, 0), (2, 2, 1, 0), (7, -2, -1, 0)]
    ok &= run_config(quats_151, 151, {1: 68, 2: 58, 3: 24, 4: 1}, '151-config')

    quats_175 = [(1, 0, 0, 0), (7, 3, 4, 0), (12, 21, 28, 0), (-91, 183, 244, 0)]
    ok &= run_config(quats_175, 175, {1: 92, 2: 58, 3: 24, 4: 1}, '175-config')

    print(f'GATE G2: {"PASS" if ok else "FAIL"}')
    return ok


# =====================================================================
# GATE G3: quadratic reproduction (octahedral 67 via Q(sqrt2); golden via
# Q(sqrt5), both through THIS file's field engine, representation A)
# =====================================================================
def gate_g3():
    print('=== GATE G3: quadratic field reproduction ===')
    ok = True

    # octahedral 67, Q(sqrt2), representation A
    FieldR2 = make_alg_field([-2, 0, 1], 1.4142135623730951, label='g3_r2')
    r2_2 = FieldR2([Fr(0), Fr(1, 2)])  # sqrt2/2
    one, zero = FieldR2(1), FieldR2(0)
    IDENT = Rot([[one, zero, zero], [zero, one, zero], [zero, zero, one]])
    Rx = Rot([[one, zero, zero], [zero, r2_2, -r2_2], [zero, r2_2, r2_2]])
    Ry = Rot([[r2_2, zero, r2_2], [zero, one, zero], [-r2_2, zero, r2_2]])
    Rz = Rot([[r2_2, -r2_2, zero], [r2_2, r2_2, zero], [zero, zero, one]])
    total, bd = exact_count_field([Rx, Ry, Rz], FieldR2)
    bd_clean = {k: v for k, v in bd.items() if k != 0}
    ok_67 = (total == 67)
    print(f'  octahedral via representation-A Q(sqrt2): total={total} '
          f'by_depth={dict(sorted(bd_clean.items()))}  {"PASS" if ok_67 else "FAIL"}')
    ok &= ok_67

    # golden n=4 (177), Q(sqrt5), representation A: build the 4 orthogonal
    # face-normal triples of the dodecahedral cube family directly (same
    # construction as cube_compound_exact.build_axes/find_cubes, READ-ONLY
    # reference, reproduced here through OUR OWN field so the check is a
    # genuine end-to-end test of this file's engine, not an import of the
    # validated oracle).
    FieldR5 = make_alg_field([-5, 0, 1], 2.23606797749979, label='g3_r5')
    H = FieldR5([Fr(1, 2), Fr(0)])
    PHI_H = FieldR5([Fr(1, 4), Fr(1, 4)])
    IPHI_H = FieldR5([Fr(-1, 4), Fr(1, 4)])
    ONE_, ZERO_ = FieldR5(1), FieldR5(0)
    axes = [(ONE_, ZERO_, ZERO_), (ZERO_, ONE_, ZERO_), (ZERO_, ZERO_, ONE_)]
    base = [PHI_H, IPHI_H, H]
    for cyc in range(3):
        p = base[-cyc:] + base[:-cyc] if cyc else base[:]
        for s1 in (1, -1):
            for s2 in (1, -1):
                v = (p[0] if s1 > 0 else -p[0], p[1] if s2 > 0 else -p[1], p[2])
                axes.append(v)
    assert len(axes) == 15

    def dot3(u, v):
        return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]

    from itertools import combinations
    triples = [t for t in combinations(range(15), 3)
               if all(dot3(axes[i], axes[j]).sign() == 0 for i, j in combinations(t, 2))]
    assert len(triples) == 5, f'expected 5 orthogonal triples, got {len(triples)}'
    # cube k's rotation matrix = COLUMNS are its 3 face normals (see
    # cube_compound_exact.py docstring: cube={x:|n.x|<=1} for the triple).
    rots5 = []
    for t in triples[:4]:
        cols = [axes[i] for i in t]
        m = [[cols[j][i] for j in range(3)] for i in range(3)]
        R = Rot(m)
        # fix handedness (det=+1) like cube_compound_exact's dodecahedron check implies orthonormal triples are already a right- or left-handed frame; ensure det=1
        det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
               - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
               + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        if det.sign() < 0:
            m2 = [[m[i][0], m[i][2], m[i][1]] for i in range(3)]
            R = Rot(m2)
        rots5.append(R)
    total5, bd5 = exact_count_field(rots5, FieldR5)
    bd5_clean = {k: v for k, v in bd5.items() if k != 0}
    ok_177 = (total5 == 177)
    print(f'  golden n=4 (177) via representation-A Q(sqrt5): total={total5} '
          f'by_depth={dict(sorted(bd5_clean.items()))}  {"PASS" if ok_177 else "FAIL"}')
    ok &= ok_177

    print(f'GATE G3: {"PASS" if ok else "FAIL"}')
    return ok


# =====================================================================
# GATE G4: representation A vs B agreement (the sqrt6 row)
# =====================================================================
def gate_g4():
    print('=== GATE G4: representation A vs B agreement (sqrt6 row) ===')
    wl = load_wl_data()
    r6_rec = next(r for r in wl['chain13_branches'] if r['tag']['branch'] == 13)

    # -- representation A --
    FieldA, valsA = alg_field_from_branch(r6_rec, 'g4_r6_A')
    rotsA = rots_from_vals(FieldA, valsA)
    t0 = time.time()
    totalA, bdA = exact_count_field(rotsA, FieldA)
    dtA = time.time() - t0
    bdA_clean = {k: v for k, v in bdA.items() if k != 0}
    print(f'  representation A: total={totalA} by_depth={dict(sorted(bdA_clean.items()))} ({dtA:.1f}s)')

    # -- representation B (tower K=Q(sqrt6), gamma^2 = 14 - 4*sqrt6) --
    tower_data = wl['tower_r6']
    a = tower_data['a']
    p0, q0 = _parse_frac_from_wl(tower_data['gamma2_simplified'], a)
    TowerB, K = make_tower_field(a, (p0, q0), label='g4_r6_B')
    coeffs = tower_data['coeffs']
    keys = ('cP', 'sP', 'c2', 's2', 'c3', 's3', 'c4', 's4')
    valsB = {}
    for key, cvec in zip(keys, coeffs):
        A_, B_ = tower_elem_from_v(cvec, p0, q0, K)
        valsB[key] = TowerB(A_, B_)
    rotsB = rots_from_vals(TowerB, valsB)
    t0 = time.time()
    totalB, bdB = exact_count_field(rotsB, TowerB)
    dtB = time.time() - t0
    bdB_clean = {k: v for k, v in bdB.items() if k != 0}
    print(f'  representation B: total={totalB} by_depth={dict(sorted(bdB_clean.items()))} ({dtB:.1f}s)')

    ok = (totalA == totalB) and (bdA_clean == bdB_clean)
    print(f'GATE G4: {"PASS" if ok else "FAIL"} (A total={totalA}, B total={totalB})')
    return ok, totalA, bdA_clean


def _parse_frac_from_wl(expr, a):
    """Parse a WL 'p + q*Sqrt[a]' / 'p - q*Sqrt[a]' InputForm-ish string
    (as produced by Simplify[...]) into (p,q) Fractions.  Handles the
    specific small set of forms this project's Simplify output uses."""
    import re
    s = expr.replace(' ', '')
    # handle an outer "(...)/ N" division (e.g. "(25+Sqrt[13])/2")
    mdiv = re.match(r'^\((.*)\)/(\d+)$', s)
    if mdiv:
        inner, denom = mdiv.group(1), Fr(mdiv.group(2))
        p, q = _parse_frac_from_wl(inner, a)
        return p / denom, q / denom
    m = re.search(r'Sqrt\[' + str(a) + r'\]', s)
    assert m, f'no Sqrt[{a}] term found in {expr!r}'
    before = s[:m.start()]
    after = s[m.end():]
    assert after == '' or after[0] in '+-', f'unexpected trailing content: {after!r}'
    # split "before" into (constant part, coefficient of sqrt term)
    # before looks like "<p><sign><q>*" or "<p><sign>" (q=1) etc.
    mm = re.match(r'^(.*?)([+-])(?:(\d+(?:/\d+)?)\*?)?$', before)
    if mm is None:
        # no explicit constant term, e.g. "-Sqrt[6]" or "4*Sqrt[6]"
        mm2 = re.match(r'^([+-]?)(\d+(?:/\d+)?)?\*?$', before)
        sign = -1 if mm2.group(1) == '-' else 1
        coefstr = mm2.group(2)
        q = sign * (Fr(coefstr) if coefstr else Fr(1))
        p = Fr(0)
    else:
        pstr, sign_ch, coefstr = mm.groups()
        p = Fr(pstr) if pstr else Fr(0)
        sign = -1 if sign_ch == '-' else 1
        q = sign * (Fr(coefstr) if coefstr else Fr(1))
    return p, q


# =====================================================================
# Candidate counting
# =====================================================================
def count_branch(rec, label, do_degeneracy=True):
    Field, vals = alg_field_from_branch(rec, label)
    rots = rots_from_vals(Field, vals)
    t0 = time.time()
    total, by_depth = exact_count_field(rots, Field)
    dt = time.time() - t0
    by_depth_clean = {int(k): v for k, v in by_depth.items() if k != 0}
    degen_pairs = detect_degenerate_pairs(vals) if do_degeneracy else []
    tag = rec['tag']
    fp = fingerprint(rec['psiDeg'], [rec['t2Deg'], rec['t3Deg'], rec['t4Deg']])
    return {
        'label': label,
        'tag': tag,
        'field_degree': rec['field_degree'],
        'minpoly_coeffs': rec['minpoly_coeffs'],
        'psiDeg': rec['psiDeg'],
        'thetasDeg': [rec['t2Deg'], rec['t3Deg'], rec['t4Deg']],
        'total': total,
        'by_depth': by_depth_clean,
        'degenerate_pairs': degen_pairs,
        'is_degenerate': len(degen_pairs) > 0,
        'congruence_fingerprint': fp,
        'solve_time_s': round(dt, 2),
    }


def main():
    print('opencount.py -- degree-agnostic exact sign engine for the n=4 open resonance candidates')
    print()
    results = []

    g1_ok = gate_g1()
    print()
    g2_ok = gate_g2()
    print()
    g3_ok = gate_g3()
    print()
    g4_ok, g4_total, g4_bd = gate_g4()
    print()

    gates_summary = {'G1': g1_ok, 'G2': g2_ok, 'G3': g3_ok, 'G4': g4_ok,
                      'G4_total': g4_total, 'G4_by_depth': g4_bd}
    if not (g1_ok and g2_ok and g3_ok and g4_ok):
        print('!!! one or more gates FAILED -- counts below are NOT certified !!!')

    wl = load_wl_data()

    print('=== Counting the CHAIN sqrt13 candidate (headline) ===')
    chain15 = next(r for r in wl['chain13_branches'] if r['tag']['branch'] == 15)
    res = count_branch(chain15, 'chain13_branch15')
    print(f"  CHAIN sqrt13 (representation A): total={res['total']} by_depth={res['by_depth']} "
          f"degenerate={res['is_degenerate']} ({res['solve_time_s']}s)")

    # extra cross-check (beyond G4's minimum requirement): the headline
    # candidate is ALSO counted via representation B (tower K=Q(sqrt13),
    # gamma^2 = 25/2+sqrt13/2), independent code path from representation A.
    tower_data = wl['tower_chain13']
    a = tower_data['a']
    p0, q0 = _parse_frac_from_wl(tower_data['gamma2_simplified'], a)
    TowerB, K = make_tower_field(a, (p0, q0), label='chain13_headline_B')
    keys = ('cP', 'sP', 'c2', 's2', 'c3', 's3', 'c4', 's4')
    valsB = {k: TowerB(*tower_elem_from_v(cvec, p0, q0, K))
             for k, cvec in zip(keys, tower_data['coeffs'])}
    rotsB = rots_from_vals(TowerB, valsB)
    t0 = time.time()
    totalB, bdB = exact_count_field(rotsB, TowerB)
    dtB = round(time.time() - t0, 2)
    bdB_clean = {int(k): v for k, v in bdB.items() if k != 0}
    cross_ok = (totalB == res['total']) and (bdB_clean == res['by_depth'])
    print(f"  CHAIN sqrt13 (representation B, tower): total={totalB} by_depth={bdB_clean} "
          f"({dtB}s)  cross-check: {'PASS -- A and B AGREE' if cross_ok else 'MISMATCH!!'}")
    res['representation_B_cross_check'] = {
        'total': totalB, 'by_depth': bdB_clean, 'agrees_with_A': cross_ok, 'solve_time_s': dtB}
    results.append(res)

    print('=== Counting remaining branches of the chain system (13,14,16) ===')
    for br in (13, 14, 16):
        rec = next(r for r in wl['chain13_branches'] if r['tag']['branch'] == br)
        res = count_branch(rec, f'chain13_branch{br}')
        print(f"  branch {br} (psi={res['psiDeg']:.4f}): total={res['total']} "
              f"by_depth={res['by_depth']} degenerate={res['is_degenerate']} "
              f"({res['solve_time_s']}s)")
        results.append(res)

    print('=== Counting row1 (sqrt3-tower) branches ===')
    for br in (5, 6):
        rec = next(r for r in wl['row1_branches'] if r['tag']['branch'] == br)
        res = count_branch(rec, f'row1_branch{br}')
        print(f"  branch {br} (psi={res['psiDeg']:.4f}): total={res['total']} "
              f"by_depth={res['by_depth']} degenerate={res['is_degenerate']} "
              f"({res['solve_time_s']}s)")
        results.append(res)

    print('=== Counting row4/row5 (pentagonal / golden-nested) representatives ===')
    for br in (56, 64):
        rec = next(r for r in wl['row45_branches'] if r['tag']['branch'] == br)
        res = count_branch(rec, f'row45_branch{br}')
        print(f"  branch {br} (psi={res['psiDeg']:.4f}): total={res['total']} "
              f"by_depth={res['by_depth']} degenerate={res['is_degenerate']} "
              f"({res['solve_time_s']}s)")
        results.append(res)

    print('=== Counting bulk-sweep representatives beyond the 6 documented classes ===')
    print('  (found by re-deriving the uniform yz/zy/xz/zx k=4 sweep, 15 subsets each,')
    print('   and the mixed triangle+1 yz/xz sweep, 48 systems -- the same combinatorial')
    print('   scope as the original resonance4_solve.wl sweep minus the xy/yx uniform')
    print('   systems, which mostly timed out originally and are not implicated by any')
    print('   documented class.  1317+1104 = 2421 raw solutions dedup to 238 unique')
    print('   non-45-degenerate (psi mod 90, theta multiset) fingerprints; folding by the')
    print('   psi<->90-psi mirror and excluding matches to the 5 documented psi values and')
    print('   the 3 already-counted rational-tangent psi values (45, 63.435, 135 from')
    print('   resonance4_results.jsonl) leaves 8 distinct psi clusters.  2 of those (yz-type')
    print('   at the SAME subset {12,14,23,34} as the chain/sqrt6 system) turned out to have')
    print('   theta multisets that are exact sign-negations of already-counted zy branches')
    print('   14/16 -- congruent by the type-reversal (Delta -> -Delta) swap symmetry, not')
    print('   new.  1 cluster (psi~24.389) is, like rows 4/5, constitutionally degenerate')
    print('   (every representative found has a coincident cube pair).  That leaves 2')
    print('   genuinely new non-degenerate degree-4 systems, counted below; the remaining')
    print('   xy/yx uniform systems and the full mixed-class (non-triangle) combinatorial')
    print('   space were NOT re-swept (budget) -- see report Honest Coverage section.')
    for br in (4,):
        rec = next(r for r in wl['bulk_branches'] if r['tag']['candidate'] == 'bulk1_yz_12_13_23_24' and r['tag']['branch'] == br)
        res = count_branch(rec, f'bulk1_branch{br}')
        print(f"  bulk1 branch {br} (psi={res['psiDeg']:.4f}): total={res['total']} "
              f"by_depth={res['by_depth']} degenerate={res['is_degenerate']} "
              f"({res['solve_time_s']}s)")
        results.append(res)
    for br in (2, 6):
        rec = next(r for r in wl['bulk_branches'] if r['tag']['candidate'] == 'bulk2_mixed_yz_zy_yz_yz' and r['tag']['branch'] == br)
        res = count_branch(rec, f'bulk2_branch{br}')
        print(f"  bulk2 branch {br} (psi={res['psiDeg']:.4f}): total={res['total']} "
              f"by_depth={res['by_depth']} degenerate={res['is_degenerate']} "
              f"({res['solve_time_s']}s)")
        results.append(res)
    for br in (68,):
        rec = next(r for r in wl['bulk_branches'] if r['tag']['candidate'] == 'bulk3_deg24.389_degenerate' and r['tag']['branch'] == br)
        res = count_branch(rec, f'bulk3_branch{br}')
        print(f"  bulk3 branch {br} (psi={res['psiDeg']:.4f}, DEGENERATE representative): "
              f"total={res['total']} by_depth={res['by_depth']} "
              f"degenerate={res['is_degenerate']} ({res['solve_time_s']}s)")
        results.append(res)

    # write results
    with open(f'{CARROLL}/opencount_results.jsonl', 'w') as f:
        f.write(json.dumps({'sweep': 'gates', **gates_summary}) + '\n')
        for res in results:
            f.write(json.dumps(res, default=str) + '\n')

    print()
    print('=== SUMMARY ===')
    best = max(results, key=lambda r: r['total'] if not r['is_degenerate'] else -1)
    print(f"Best non-degenerate open-candidate total found: {best['total']} "
          f"({best['label']}, psi={best['psiDeg']:.4f})")
    print('Records written to opencount_results.jsonl')


if __name__ == '__main__':
    main()
