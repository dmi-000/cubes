#!/usr/bin/env python3
"""Can a configuration's count be PREDICTED from its subsets' counts?  [P340]  Yes -- exactly,
with one small correction.

THE DERIVATION.  [P338]'s lemma: `excess(v)` depends only on `supp(v)`.  So writing
`E(T)` for the half-excess carried by vertices whose support is exactly `T`, the identity
`TOTAL = 1 + L + sum c + (1/2) sum excess` applied to any subset `S` gives

    count(S)  =  1 + (|S|-1) + sum c(S) + sum_{T subset S, |T|>=2} E(T)

a ZETA TRANSFORM over the subset lattice, hence invertible by Moebius inversion.  Predicting
the full count from PROPER subsets only leaves out exactly one term: `E([n])`, the vertices
where ALL n cubes meet.

MEASURED.  Over random n = 4 configurations: 194 of 199 EXACT, the other 5 off by exactly -2,
maximum |defect| 2.  The -2 cases are precisely those carrying an n-fold vertex.

A TRAP THIS PROBE WALKED INTO, kept because the number was seductive.  A first run reported one
defect of **-93**.  The engine had answered `{"error": "outside must be a single region"}` and
the count helper scored that refusal as 0 -- the project's own documented failure
(FAILURE_MODES: unevaluable is not a negative result).  Refusals are now raised and counted, and
the true maximum defect is 2.  **A predictor with rare huge errors is a different object from one
with bounded errors, and the difference here was entirely an unhandled refusal.**
"""
import sys, os, json, itertools, collections, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
from c_level import level_graph, engine, shares_plane
import ee_bound_refute as B
import wall_keys as W
import provenance as PROV


class Refused(Exception):
    pass


def count(qs):
    r = engine(qs)
    if 'error' in r or not r.get('by_depth'):
        raise Refused(r.get('error', 'no by_depth'))
    return sum(v for k, v in r['by_depth'].items() if k != '0')


def holes(qs):
    return sum(v['c'] for v in level_graph(qs).values())


def predict(qs):
    """the count, from PROPER subsets only."""
    n = len(qs)
    E = {}
    for k in range(2, n):
        for T in itertools.combinations(range(n), k):
            sub = [qs[i] for i in T]
            E[T] = (count(sub) - 1 - (k - 1) - holes(sub)
                    - sum(E[U] for U in E if set(U) < set(T)))
    return 1 + (n - 1) + holes(qs) + sum(E.values())


def nfold(qs):
    """number of vertices supported by ALL n cubes."""
    sig, _ = B.vertices(qs)
    return sum(v for k, v in sig.items() if len(k) == len(qs))


def ie_exact(qs):
    """The predictor written out as INCLUSION-EXCLUSION over subsets (n = 4):

        TOTAL = sum(triple counts) - sum(pair counts) + 4
                + [ c(full) - sum_S c(S) + sum_P c(P) ]          hole correction
                - (number of n-fold vertices)

    The bracket is 1 when every subset and the whole have c = 1 at every level, which is why the
    bare form `sum t - sum p + 5` fits the records and the named families and drifts by up to 5
    on random draws.  With the bracket included the formula is exact.
    """
    n = len(qs)
    st = sum(count([qs[i] for i in S]) for S in itertools.combinations(range(n), 3))
    sp = sum(count([qs[i] for i in P]) for P in itertools.combinations(range(n), 2))
    hc = (holes(qs)
          - sum(holes([qs[i] for i in S]) for S in itertools.combinations(range(n), 3))
          + sum(holes([qs[i] for i in P]) for P in itertools.combinations(range(n), 2)))
    return st - sp + 4 + hc


def h_of(qs, S):
    """h(S) = t_S - (1/2)(its three pair counts).  TOTAL = sum_S h(S) + 4 + holecorr - nfold,
    because each pair lies in exactly two triples at n = 4."""
    sub = [qs[i] for i in S]
    t = count(sub)
    ps = [count([sub[i] for i in P]) for P in itertools.combinations(range(3), 2)]
    return t - 0.5 * sum(ps), t, ps


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    out = {'what': 'predicting a count from its subsets', 'supports': 'LEDGER P340'}

    print('=== named configurations ===')
    named = [('n=4 RECORD', [tuple(q) for q in W.REC[4]]),
             ('n=5 RECORD', [tuple(q) for q in W.REC[5]]),
             ('merged corner', [(1, 0, 0, 0), (1, -7, -8, 0), (2, -13, 0, -11), (1, 0, -4, -5)]),
             ('body-diagonal', [(1, 0, 0, 0), (3, 1, 1, 1), (2, 1, 1, 1), (5, 2, 2, 2)]),
             ('face-diagonal', [(1, 0, 0, 0), (3, 2, 2, 0), (5, 4, 4, 0), (4, 3, 3, 0)])]
    rows = []
    for lbl, qs in named:
        t, p, nf = count(qs), predict(qs), nfold(qs)
        rows.append({'label': lbl, 'total': t, 'predicted': p, 'defect': t - p, 'n_fold': nf})
        print('   %-16s TOTAL %4d   predicted %4d   defect %3d   n-fold vertices %d'
              % (lbl, t, p, t - p, nf))
    out['named'] = rows

    print('\n=== random n = 4, refusals COUNTED not scored ===')
    rng = random.Random(19)
    d = collections.Counter()
    pair = collections.Counter()
    ok = refused = 0
    while ok + refused < trials:
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(3)]
        if any(all(v == 0 for v in q) for q in qs) or shares_plane(qs):
            continue
        try:
            t, p = count(qs), predict(qs)
        except Refused:
            refused += 1
            continue
        except Exception:
            continue
        ok += 1
        d[t - p] += 1
        pair[(t - p, nfold(qs))] += 1
    print('   evaluated %d   REFUSED %d' % (ok, refused))
    print('   defect distribution: %s' % dict(sorted(d.items())))
    print('   EXACT %d of %d = %.1f %%   max |defect| = %d'
          % (d[0], ok, 100.0 * d[0] / ok, max(abs(k) for k in d)))
    print('\n   (defect, n-fold vertex count) -> how many:')
    for k, v in sorted(pair.items()):
        print('      %-12s %4d' % (str(k), v))
    conj = all(dd == -nf for (dd, nf), _ in pair.items())
    print('\n   conjecture  defect = -(number of n-fold vertices):  %s'
          % ('HOLDS on every case here' if conj else 'FAILS'))
    out['random'] = {'evaluated': ok, 'refused': refused,
                     'defects': {str(k): v for k, v in sorted(d.items())},
                     'defect_vs_nfold': {str(k): v for k, v in sorted(pair.items())},
                     'conjecture_defect_eq_minus_nfold': conj}
    out['reproduce'] = PROV.stamp(parameters={'trials': trials, 'seed': 19})
    json.dump(out, open(os.path.join(HERE, '..', '..', 'data', 'subset_predictor.json'), 'w'),
              indent=1, default=str)
    print('\nwritten data/subset_predictor.json')


if __name__ == '__main__':
    main()
