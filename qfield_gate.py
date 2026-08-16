#!/usr/bin/env python3
"""Gate on the Q(sqrt d) scalar layer, run BEFORE anything downstream trusts it.

The dimension machinery accumulated seven apparatus faults, and the probe that
would have caught four of them -- evaluate the machinery's own intermediates at
a KNOWN answer -- was built seventh.  This is that probe for the field layer,
built first: every scalar operation the port depends on is checked against a
value known independently, and the two 67s are counted through the field engine
before any of their derived quantities are believed.

Checks, in order of what they would catch:
  1. sign()      -- against 400-digit mpmath, on adversarial elements where
                    a^2 and b^2 d are close, which is where a naive sign fails.
  2. to_sp/from_sp round trip -- the port's only lossy-looking step.
  3. from_sp on EXPRESSIONS (products, quotients, radsimp'd denominators),
     not just on literals: literals round-trip through code paths that the
     gradients never take.
  4. clear_denoms -> engine syntax -> the engine returns 67 for both 67s.
  5. d = 0 must reproduce the Fraction path bit-for-bit, since the whole
     port rests on the rational case being unchanged.
"""
import json, os, random, subprocess, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from qfield import Q, to_sp, from_sp, clear_denoms

HERE = os.path.dirname(os.path.abspath(__file__))
ENGW = os.path.join(HERE, 'cube_regions_q2w')

# The two n = 3 maximisers, as quaternions over Z[sqrt d]; component (p, q)
# means p + q*sqrt(d).  Cube 0 is the identity in both.
RECORDS = {
    2: [((1, 0), (0, 0), (0, 0), (0, 0)),
        ((1, 0), (1, 0), (0, 1), (0, 0)),
        ((-1, 0), (1, 0), (0, 1), (0, 0))],
    5: [((1, 0), (0, 0), (0, 0), (0, 0)),
        ((2, 0), (1, 1), (-1, 1), (0, 0)),
        ((-2, 0), (1, 1), (-1, 1), (0, 0))],
}

fails = []


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'ok' if ok else 'FAIL', detail), flush=True)
    if not ok:
        fails.append(name)


def rand_q(rng, d, hard=False):
    if hard:
        # a^2 within a hair of b^2 d: the case where sign() must not guess.
        b = F(rng.randint(1, 50), rng.randint(1, 12))
        a = F(int((b * b * d) ** 0.5 * 10 ** 6), 10 ** 6) + F(rng.randint(-1, 1), 10 ** 7)
        return Q(a * rng.choice([1, -1]), b * rng.choice([1, -1]), d)
    return Q(F(rng.randint(-99, 99), rng.randint(1, 30)),
             F(rng.randint(-99, 99), rng.randint(1, 30)), d)


def gate_sign(rng):
    try:
        import mpmath
    except ImportError:
        print('mpmath absent -- sign checked against sympy instead')
        mpmath = None
    bad = 0
    for d in (2, 5, 3, 7):
        for hard in (False, True):
            for _ in range(400):
                q = rand_q(rng, d, hard)
                if mpmath is not None:
                    mpmath.mp.dps = 400
                    v = mpmath.mpf(q.a.numerator) / q.a.denominator + (
                        mpmath.mpf(q.b.numerator) / q.b.denominator) * mpmath.sqrt(d)
                    ref = 0 if v == 0 else (1 if v > 0 else -1)
                else:
                    ref = int(sp.sign(to_sp(q)))
                if q.sign() != ref:
                    bad += 1
    check('exact sign vs 400-digit reference (3200 elements)', bad == 0,
          '%d disagreements' % bad)


def gate_roundtrip(rng):
    bad = 0
    for d in (2, 5, 3):
        for _ in range(300):
            q = rand_q(rng, d)
            if from_sp(to_sp(q), d) != q:
                bad += 1
    check('to_sp / from_sp round trip (900 elements)', bad == 0, '%d lost' % bad)


def gate_expressions(rng):
    """from_sp on expressions, which is how the gradients actually arrive."""
    bad, examples = 0, []
    for d in (2, 5):
        for _ in range(200):
            x, y, z = (rand_q(rng, d) for _ in range(3))
            if y.is_zero():
                continue
            truth = (x * z + y) / y - z * z          # exercises division
            expr = (to_sp(x) * to_sp(z) + to_sp(y)) / to_sp(y) - to_sp(z) ** 2
            got = from_sp(expr, d)
            if got != truth:
                bad += 1
                if len(examples) < 2:
                    examples.append((str(truth), str(got)))
    check('from_sp on rational EXPRESSIONS (400 cases)', bad == 0,
          '%d wrong %s' % (bad, examples))


def gate_diff(rng):
    """the exact path conditions() takes: symbolic diff, then substitute a field
    point, then read the value back.  This is the step that had to be generalised."""
    d = 5
    x, y = sp.symbols('x y')
    expr = (x * x * y - 3 * y + sp.Rational(1, 2) * x) / (1 + y * y)
    px, py = rand_q(rng, d), rand_q(rng, d)
    g = sp.diff(expr, x).subs({x: to_sp(px), y: to_sp(py)})
    got = from_sp(g, d)
    truth = (2 * px * py + F(1, 2)) / (1 + py * py)     # d/dx by hand
    check('symbolic diff -> field substitution -> from_sp', got == truth,
          '%s vs %s' % (got, truth))


def gate_engine():
    """the known answer: both records must count 67 through the field engine."""
    for d, quats in RECORDS.items():
        s = ';'.join(','.join('%d:%d' % c for c in q) for q in quats)
        p = subprocess.run([ENGW, '--d', str(d), '--quats', s],
                           capture_output=True, text=True)
        try:
            got = json.loads(p.stdout.strip().splitlines()[-1])['bounded']
        except Exception:
            got = 'unparseable: ' + p.stdout[:80] + p.stderr[:80]
        check('engine counts the Q(sqrt %d) record' % d, got == 67, 'got %s' % got)


def gate_clear_denoms(rng):
    """clear_denoms must reproduce the record's own quaternions from its Cayley
    coordinates -- the round trip the port needs to call the engine at all."""
    for d, quats in RECORDS.items():
        for q in quats[1:]:
            w = Q(F(q[0][0]), F(q[0][1]), d)
            cay = [Q(F(c[0]), F(c[1]), d) / w for c in q[1:]]
            L, ints = clear_denoms([Q(1, 0, d)] + cay)
            back = [Q(F(a), F(b), d) for a, b in ints]
            ok = all((back[0] * cay[k - 1]) == back[k] for k in (1, 2, 3))
            # and the reconstructed quaternion must be the original up to scale
            scale = back[0] / w
            same = all(back[k] == Q(F(q[k][0]), F(q[k][1]), d) * scale
                       for k in range(4))
            check('clear_denoms round trip, d=%d cube %s' % (d, q[0]), ok and same,
                  'L=%d ints=%s' % (L, ints))


def gate_d0(rng):
    """d = 0 must be the Fraction path unchanged."""
    bad = 0
    for _ in range(200):
        a = F(rng.randint(-99, 99), rng.randint(1, 30))
        if from_sp(to_sp(a), 0) != a:
            bad += 1
    check('d = 0 is the Fraction path (200 elements)', bad == 0, '%d lost' % bad)


def main():
    rng = random.Random(20260817)
    gate_sign(rng)
    gate_roundtrip(rng)
    gate_expressions(rng)
    gate_diff(rng)
    gate_clear_denoms(rng)
    gate_d0(rng)
    gate_engine()
    print('\n%s' % ('ALL GATES PASS' if not fails else 'FAILED: ' + ', '.join(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
