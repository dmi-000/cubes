#!/usr/bin/env python3
"""[OQ 39] What it would take to DERIVE `EE <= 36` at `B = 128` -- the last measured link.

[P359] pushed the question to 3-subsets and got `EE <= 40`; [P360] showed the residual 4 is not
recoverable by any counting argument over the subset lattice (40 IS the combinatorial optimum);
[P361] attacked the ceiling from both sides and it held.  All three left it MEASURED.

This probe does not close it.  It establishes the four things a derivation would need, and
measures which of them are already true, so the remaining work is a statement rather than a
search.

  A.  AN INDEPENDENT EXACT ORACLE for EE.  Every number in this thread comes from
      `ee_bound_refute.vertices`, which reads EE off the arrangement's (2,2) signature.  Two
      implementations agreeing proves they share assumptions ([METHODS]); so EE is recomputed
      here from scratch -- 12 edges per cube as exact rational segments, pairwise exact
      intersection -- and the two are compared.

  B.  EE > 0 IS CODIMENSION 1.  Every EE census in this project draws SMALL quaternions, where
      coincidences are common; that is a property of the representative, not of the object.  At
      height 1e6 the count collapses, which is what makes the level sets varieties rather than
      clouds -- and therefore solvable.

  C.  THE LEVEL SETS ARE CUT OUT BY 144 QUARTICS.  Edge `e` of cube 1 meets edge `f` of cube 2
      iff a 3x3 determinant vanishes and the crossing lies in range.  Cleared of denominators
      that determinant is a homogeneous DEGREE-4 form in the quaternion, and none of the 144 is
      identically zero.  So `EE(q) = #{forms vanishing, in range}`, and `EE >= 10` is five
      simultaneous quartic conditions (antipodal symmetry halves the 144 to 72 and pairs them)
      on a 3-dimensional space -- an overdetermined system, i.e. a Groebner computation and not
      a search.

  D.  THE KILL LIST IS FINITE AND SHORT.  Every pair-EE pattern with total >= 37 subject to
      [P360]'s per-triple cap of 20 is enumerated exactly.  These, and only these, are what a
      derivation has to rule out.

  E.  THE LEMMA THAT WOULD CLOSE IT, and a first test of it.  [P359] observed that a 3-subset
      can hold `E_S = 32` together with an `EE = 10` pair -- which is exactly why the per-subset
      route fails.  At n = 4 each pair lies in TWO triples, so the surviving form of the
      observation is:

          if a pair has EE >= 8, at least one of its two containing 3-subsets has E_S < 32

      which would force every pair to EE <= 6 at `B = 128`, hence `EE <= 36`.  This is a
      statement about a 4-subset that no 3-subset fact implies -- the pair-to-subset incidence
      the summing argument discards.  It is tested here, not proved.
"""
import sys, os, json, random, itertools, collections
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from euler3 import rowsT, frames
from c_level import shares_plane
import ee_bound_refute as B
import wall_keys as W
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


# ---------------------------------------------------------------- A. the independent oracle

def corners(M):
    """the 8 corners of {x : |<M[r],x>| <= 1}, exactly.  M's ROWS are the face normals --
    the rows/columns confusion has cost this project five separate measurements."""
    out = {}
    for s in itertools.product((-1, 1), repeat=3):
        a = [[F(M[r][c]) for c in range(3)] + [F(s[r])] for r in range(3)]
        for c in range(3):
            p = next(r for r in range(c, 3) if a[r][c] != 0)
            a[c], a[p] = a[p], a[c]
            pv = a[c][c]; a[c] = [v / pv for v in a[c]]
            for r in range(3):
                if r != c and a[r][c] != 0:
                    f = a[r][c]; a[r] = [a[r][k] - f * a[c][k] for k in range(4)]
        out[s] = tuple(a[r][3] for r in range(3))
    return out


def edges(M):
    C = corners(M)
    E = []
    for s in C:
        for k in range(3):
            t = list(s); t[k] = -t[k]; t = tuple(t)
            if s < t:
                E.append((C[s], C[t]))
    return E


def _cross(a, b): return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def _dot(a, b):   return sum(a[i]*b[i] for i in range(3))


def seg_int(A, Bp, C, D):
    """exact intersection point of CLOSED segments AB, CD -- or None.  No tolerance anywhere."""
    u = [Bp[i]-A[i] for i in range(3)]; v = [D[i]-C[i] for i in range(3)]
    w = [C[i]-A[i] for i in range(3)]
    n = _cross(u, v)
    if all(x == 0 for x in n):       # parallel: no isolated crossing
        return None
    if _dot(w, n) != 0:              # skew
        return None
    nn = _dot(n, n)
    s = F(_dot(_cross(w, v), n)) / nn
    t = F(_dot(_cross(w, u), n)) / nn
    if 0 <= s <= 1 and 0 <= t <= 1:
        return tuple(A[i] + s*u[i] for i in range(3))
    return None


def nfacets(M, p):
    """how many facets of {x : |<M[r],x>| <= 1} pass through p.  3 means p is a CORNER."""
    return sum(1 for r in range(3) if abs(sum(F(M[r][c]) * p[c] for c in range(3))) == 1)


def ee_exact(q):
    """EE for the PAIR (identity, q), from the edges up.  Independent of the arrangement code.

    A crossing at a CORNER of either cube is NOT an edge-edge vertex: it has signature (3,2)
    or (3,3), not (2,2).  This is the distinction that cost [P329] its witness -- at a shared
    corner three edges meet three edges, which is nine incidences and ONE vertex of a different
    type.  Dropping the filter makes every self-coincident rotation -- (1,1,0,0), (1,1,1,1) --
    report 8, one per corner of a cube that has been mapped to itself."""
    Ms = [rowsT(R) for R in frames([(1, 0, 0, 0), q])]
    E0, E1 = edges(Ms[0]), edges(Ms[1])
    hits = set()
    for a in E0:
        for b in E1:
            p = seg_int(a[0], a[1], b[0], b[1])
            if p is None:
                continue
            if nfacets(Ms[0], p) != 2 or nfacets(Ms[1], p) != 2:
                continue
            hits.add(p)
    return len(hits)


def ee_arrangement(q):
    s, _ = B.vertices([(1, 0, 0, 0), q])
    return s.get((2, 2), 0)


# ---------------------------------------------------------------- D. the kill list

def kill_list(values=(0, 4, 6, 8, 10), lo=37):
    """every assignment of EE to the six pairs of a 4-compound with total >= lo and every
    3-subset summing to at most 20 ([P360]).  Exhaustive over the observed per-pair values."""
    pairs = list(itertools.combinations(range(4), 2))
    tri = [[i for i, p in enumerate(pairs) if set(p) <= set(S)]
           for S in itertools.combinations(range(4), 3)]
    out = []
    for a in itertools.product(values, repeat=6):
        if sum(a) < lo:
            continue
        if any(sum(a[i] for i in T) > 20 for T in tri):
            continue
        out.append(a)
    return pairs, out


# ---------------------------------------------------------------- E. the candidate lemma

def anat(qs):
    s, _ = B.vertices(qs)
    return {'EE': s.get((2, 2), 0), 'T3': s.get((1, 1, 1), 0), 'Qg': s.get((1, 1, 1, 1), 0)}


def es(qs):
    a = anat(qs)
    return a['T3'] + 4 * a['Qg']


def main():
    out = {'what': 'what a derivation of EE <= 36 at B = 128 would need', 'supports': 'OQ 39'}

    print('A. INDEPENDENT EXACT ORACLE vs the arrangement count')
    rng = random.Random(4801)
    probe = [(3, 2, 2, 0), (0, 1, 1, 1), (1, 1, 0, 0), (1, 1, 1, 1), (2, 1, 1, 0), (5, 8, 5, 0)]
    probe += [tuple(rng.randint(-8, 8) for _ in range(4)) for _ in range(30)]
    agree = dis = 0; bad = []
    for q in probe:
        if all(v == 0 for v in q):
            continue
        x, y = ee_exact(q), ee_arrangement(q)
        if x == y:
            agree += 1
        else:
            dis += 1; bad.append([list(q), x, y])
    print('   quaternions compared: %d   agree %d   DISAGREE %d' % (agree + dis, agree, dis))
    for b in bad[:6]:
        print('      %s   edges %d   arrangement %d' % (b[0], b[1], b[2]))
    out['oracle'] = {'compared': agree + dis, 'agree': agree, 'disagree': dis, 'cases': bad}

    print('\nB. IS EE > 0 CODIMENSION 1?  the same census at three heights')
    out['by_height'] = {}
    for h, N in ((6, 120), (400, 120), (10**6, 120)):
        r = random.Random(9 + h % 97); c = collections.Counter()
        n = deg = 0
        while n < N:
            q = tuple(r.randint(-h, h) for _ in range(4))
            if all(v == 0 for v in q):
                continue
            # a pair sharing a face PLANE is degenerate and excluded project-wide; such pairs
            # reach EE = 16, above the admissible per-pair maximum of 10 ([P330]).  Both
            # oracles agree on them -- they are excluded, not miscounted.
            if shares_plane([(1, 0, 0, 0), q]):
                deg += 1
                continue
            n += 1; c[ee_exact(q)] += 1
        nz = sum(v for k, v in c.items() if k)
        print('   height %-8d  nonzero EE: %3d / %d    %s   (degenerate skipped: %d)'
              % (h, nz, N, dict(sorted(c.items())), deg))
        out['by_height'][str(h)] = {'n': N, 'nonzero': nz, 'degenerate_skipped': deg,
                                    'dist': {str(k): v for k, v in c.items()}}

    print('\nC. THE 144 QUARTICS')
    try:
        import sympy as sp
        w, x, y, z = sp.symbols('w x y z')
        N = w*w + x*x + y*y + z*z
        R = sp.Matrix([[w*w+x*x-y*y-z*z, 2*(x*y-w*z),     2*(x*z+w*y)],
                       [2*(x*y+w*z),     w*w-x*x+y*y-z*z, 2*(y*z-w*x)],
                       [2*(x*z-w*y),     2*(y*z+w*x),     w*w-x*x-y*y+z*z]])
        degs = collections.Counter()
        for a in range(3):
            for b in range(3):
                for s, t, u, v in itertools.product((-1, 1), repeat=4):
                    d1 = sp.Matrix([1 if i == a else 0 for i in range(3)])
                    p1 = sp.Matrix([0, 0, 0]); p1[(a+1) % 3] = s; p1[(a+2) % 3] = t
                    d2 = R * sp.Matrix([1 if i == b else 0 for i in range(3)])
                    q2 = sp.Matrix([0, 0, 0]); q2[(b+1) % 3] = u; q2[(b+2) % 3] = v
                    D = sp.expand(sp.Matrix.hstack(d1, d2, R*q2 - N*p1).det())
                    degs['zero' if D == 0 else sp.Poly(D, w, x, y, z).total_degree()] += 1
        print('   coplanarity determinants over all 12x12 edge pairs:', dict(degs))
        out['quartics'] = {str(k): v for k, v in degs.items()}
    except ImportError:
        print('   sympy unavailable -- skipped'); out['quartics'] = None

    print('\nD. THE KILL LIST -- every pattern a derivation must rule out')
    pairs, KL = kill_list()
    byt = collections.Counter(sum(a) for a in KL)
    print('   patterns with total >= 37 and every triple <= 20: %d   totals %s'
          % (len(KL), dict(sorted(byt.items()))))
    for a in KL[:8]:
        print('      ' + '  '.join('%s%d%s=%d' % ('(', p[0], ')' if False else str(p[1]) + ')', v)
                                   for p, v in zip(pairs, a)))
    out['kill_list'] = {'patterns': [list(a) for a in KL], 'pairs': [list(p) for p in pairs],
                        'by_total': {str(k): v for k, v in byt.items()}}

    print('\nE. THE CANDIDATE LEMMA:  EE(pair) >= 8  =>  one of its two triples has E_S < 32')
    rng = random.Random(5150)
    rec = [tuple(q) for q in W.REC[4]]
    pool = []
    seeds = [(3, 2, 2, 0), (5, 8, 5, 0), (4, 5, -9, -9), (0, 4, -6, 7), (-2, -8, 3, -3)]
    n = 0
    while n < 260:
        if rng.random() < 0.5:
            qs = [(1, 0, 0, 0)] + [rng.choice(seeds) if rng.random() < 0.5 else
                                   tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(3)]
        else:
            qs = [list(q) for q in rec]
            for _ in range(rng.choice([1, 2, 3])):
                i, j = rng.randrange(1, 4), rng.randrange(4)
                qs[i][j] += rng.choice([-2, -1, 1, 2])
            qs = [tuple(q) for q in qs]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        n += 1
        pool.append(qs)

    tested = viol = hi = refused = 0
    worst = []
    for qs in pool:
        try:
            ES = {S: es([qs[i] for i in S]) for S in itertools.combinations(range(4), 3)}
        except Exception:
            refused += 1
            continue
        tested += 1
        for i, j in itertools.combinations(range(4), 2):
            e = ee_exact(B.qmul(B.qconj(qs[i]), qs[j])) if hasattr(B, 'qmul') else None
            if e is None:
                e = anat([qs[i], qs[j]])['EE']
            if e < 8:
                continue
            hi += 1
            both = [ES[S] for S in ES if {i, j} <= set(S)]
            if min(both) >= 32:
                viol += 1
                a4 = anat(qs)
                worst.append({'quats': [list(q) for q in qs], 'pair': [i, j], 'EE_pair': e,
                              'E_S_pair': both, 'E_S_all': sorted(ES.values()),
                              'B': a4['T3'] + 4 * a4['Qg'], 'EE_total': a4['EE']})
    print('   4-compounds evaluated: %d   (unevaluable: %d)' % (tested, refused))
    print('   pairs with EE >= 8 found: %d' % hi)
    print('   of those, BOTH containing triples at E_S >= 32: %d   %s'
          % (viol, 'LEMMA REFUTED' if viol else 'lemma survives this pool'))
    at128 = [c for c in worst if c['B'] == 128]
    print('   of THOSE, compounds actually at B = 128: %d   %s'
          % (len(at128), 'THE CEILING IS BROKEN' if any(c['EE_total'] > 36 for c in at128)
             else 'none breaks EE <= 36'))
    for c in worst[:4]:
        print('      pair %s  EE %2d   its two E_S %s   all four %s   B %3d   EE_total %d'
              % (c['pair'], c['EE_pair'], c['E_S_pair'], c['E_S_all'], c['B'], c['EE_total']))
    out['lemma'] = {'statement': 'EE(pair) >= 8 => min over its two 3-subsets of E_S < 32',
                    'compounds_tested': tested, 'unevaluable': refused,
                    'high_EE_pairs': hi, 'violations': viol,
                    'violations_at_B_128': len(at128),
                    'max_EE_total_at_B_128': max([c['EE_total'] for c in at128], default=None),
                    'witnesses': worst[:8],
                    'witnesses_at_B_128': at128[:8]}

    out['reproduce'] = PROV.stamp(
        parameters={'seeds': [4801, 5150], 'heights': [6, 400, 10**6],
                    'pool': 260, 'kill_list_values': [0, 4, 6, 8, 10], 'kill_list_min': 37},
        note='EE recomputed from exact rational edge intersections, independent of '
             'ee_bound_refute.vertices')
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee_determinantal.json'), 'w'), indent=1)
    print('\nwrote data/ee_determinantal.json')


if __name__ == '__main__':
    main()
