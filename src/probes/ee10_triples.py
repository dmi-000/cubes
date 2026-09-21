#!/usr/bin/env python3
"""[OQ 39] The 3-subset envelope at `E_S = 32`, by ENUMERATION rather than sampling.

[P359] reported the maximum `sum EE` over a triple at `E_S = 32` as **20**, from 1 400 random
3-compounds, and [P360] and [P366] both build on it (`EE <= 40`, and the 105-pattern kill
list).  A hard control refutes it: seeding face-diagonal members AGAINST EACH OTHER rather than
against random rotations reaches 26.

So the value is settled here by enumeration instead.  Every pair at the per-pair maximum
`EE = 10` comes from one finite family ([P330]: the coprime quaternions of height <= 6 with
`EE = 10`), and the interesting triples are those built from two of its members.  All of them
are enumerated, exactly, and the largest `sum EE` at `E_S = 32` is reported with its witness.

Scope, stated because it bounds the claim: this enumerates triples whose two non-identity cubes
BOTH lie in the height-<= 6 `EE = 10` family.  It is exhaustive over that family and is a lower
bound on the true envelope everywhere else ([METHODS 1]).
"""
import sys, os, json, itertools, collections
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_determinantal as D
import ee_bound_refute as EB
from c_level import shares_plane
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def family(h=6):
    out = []
    for q in itertools.product(range(-h, h + 1), repeat=4):
        if not any(q):
            continue
        g = 0
        for v in q:
            g = gcd(g, abs(v))
        if g != 1:
            continue
        for v in q:                       # keep one of each antipodal pair
            if v:
                if v < 0:
                    q = None
                break
        if q is None:
            continue
        if shares_plane([(1, 0, 0, 0), q]):
            continue
        if D.ee_exact(q) == 10:
            out.append(q)
    return out


def main():
    fam = family()
    print('per-pair EE = 10 family, coprime, entries -6..6: %d' % len(fam), flush=True)
    best = (0, None); rows = collections.Counter(); n = refused = 0
    for a, b in itertools.combinations(fam, 2):
        qs = [(1, 0, 0, 0), a, b]
        if shares_plane(qs):
            continue
        try:
            sig, _ = EB.vertices(qs)
        except Exception:
            refused += 1
            continue
        n += 1
        ES = sig.get((1, 1, 1), 0) + 4 * sig.get((1, 1, 1, 1), 0)
        ee = sig.get((2, 2), 0)
        rows[(ES, ee)] += 1
        if ES == 32 and ee > best[0]:
            best = (ee, qs)
    print('triples evaluated: %d   unevaluable: %d' % (n, refused), flush=True)
    print('MAX sum EE at E_S = 32: %d   ([P359] reported 20)' % best[0], flush=True)
    print('   witness: %s' % (';'.join(','.join(map(str, q)) for q in best[1])
                              if best[1] else None), flush=True)
    at32 = sorted(((k[1], v) for k, v in rows.items() if k[0] == 32), reverse=True)
    print('   EE spectrum at E_S = 32: %s' % at32[:8], flush=True)
    mx = max(rows) if rows else None
    print('   largest EE seen at ANY E_S in this family: %d'
          % max((k[1] for k in rows), default=0), flush=True)
    out = {'what': 'max sum-EE at E_S = 32, enumerated over the EE = 10 family',
           'supports': 'OQ 39; refutes P359 max of 20',
           'family_size': len(fam), 'triples': n, 'unevaluable': refused,
           'max_EE_at_ES32': best[0],
           'witness': [list(q) for q in best[1]] if best[1] else None,
           'EE_spectrum_at_ES32': at32,
           'dist': {'%d,%d' % k: v for k, v in sorted(rows.items())}}
    out['reproduce'] = PROV.stamp(parameters={'family_height': 6},
                                  note='exhaustive over the height<=6 EE=10 family; a LOWER '
                                       'bound on the envelope outside it')
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee10_triples.json'), 'w'), indent=1)
    print('wrote data/ee10_triples.json', flush=True)


if __name__ == '__main__':
    main()
