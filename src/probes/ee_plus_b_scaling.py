#!/usr/bin/env python3
"""[OQ 39] Can `EE + B <= 164` be established, and what is the analogue at other n?

The second question is the sharper one, because it names a way to REFUTE the first.  At n = 3
the enumerated maximum of `EE + B` is **58**, and `58 > 6*C(3,2) + 32*C(3,3) = 50` -- so the
obvious general form of the n = 4 law is already false one size down.  If the n = 3 extremes
extend, `EE + B = 164` is a sampling plateau and not a law.

  A. THE REFUTATION ATTEMPT.  Take the n = 3 compounds that MAXIMISE `EE + B` (58, from the
     exhaustive family enumeration of [P369]) and extend each by a fourth cube, drawn from the
     `EE = 10` family and from random rotations.  Every previous n = 4 search was seeded from
     the record or the face-diagonal family; none started from the `EE + B` extreme.

  B. THE LADDER.  `max(EE + B)` measured at n = 2, 3, 4, 5, against the two candidate closed
     forms `6*C(n,2) + 32*C(n,3)` and `10*C(n,2) + 32*C(n,3)`.

  C. WHAT A PROOF WOULD NEED, stated from [P372]'s merge law rather than guessed:

         EE + B  =  sum_pairs EE_i  +  sum_S E_S  -  (merges)

     with `EE_i <= 10` and `E_S <= 32` PROVED, giving `EE + B <= 10*C(n,2) + 32*C(n,3)` = 188 at
     n = 4.  The law asks for 164, so a proof must find **24 units of merge or shortfall** that
     no configuration can avoid.  That is the whole gap, and it is stated in the quantities
     [P372] showed are the right ones.
"""
import sys, os, json, random, itertools, collections
from math import comb, gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as EB
import ee_determinantal as D
from c_level import shares_plane
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def anat(qs):
    sig, _ = EB.vertices(qs)
    EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
    T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
    Q4 = sum(v for k, v in sig.items() if len(k) >= 4)
    B = T3 + 4 * Qg
    return {'EE': EE, 'SC2': SC, 'B': B, 'Q4': Q4, 'sum': EE + B,
            'TOTAL': 7 + EE + 2 * SC + B - Q4}


def family(h=5):
    out = []
    for q in itertools.product(range(-h, h + 1), repeat=4):
        if not any(q):
            continue
        g = 0
        for v in q:
            g = gcd(g, abs(v))
        if g != 1:
            continue
        neg = False
        for v in q:
            if v:
                neg = v < 0
                break
        if neg or shares_plane([(1, 0, 0, 0), q]):
            continue
        if D.ee_exact(q) == 10:
            out.append(q)
    return out


def main():
    rng = random.Random(164)
    out = {'what': 'can EE + B <= 164 be established; the analogue at other n',
           'supports': 'OQ 39'}

    print('A. THE REFUTATION ATTEMPT -- extending the n = 3  EE + B = 58  extremes')
    fam = family()
    print('   EE = 10 family (height <= 5): %d' % len(fam), flush=True)

    # rebuild the n = 3 extremes exactly: pairs from the family whose triple has E_S = 32, EE = 26
    tri58 = []
    for a, b in itertools.combinations(fam, 2):
        qs = [(1, 0, 0, 0), a, b]
        if shares_plane(qs):
            continue
        try:
            r = anat(qs)
        except Exception:
            continue
        if r['B'] == 32 and r['EE'] == 26:
            tri58.append(qs)
        if len(tri58) >= 12:
            break
    print('   n = 3 extremes rebuilt (E_S 32, EE 26, EE+B 58): %d' % len(tri58), flush=True)

    cands = list(fam) + [tuple(rng.randint(-9, 9) for _ in range(4)) for _ in range(400)]
    best = (0, None); n = refused = 0; hist = collections.Counter()
    for base in tri58:
        for q in cands:
            qs = base + [q]
            if not any(q) or shares_plane(qs):
                continue
            n += 1
            try:
                r = anat(qs)
            except Exception:
                refused += 1
                continue
            hist[r['sum']] += 1
            if r['sum'] > best[0]:
                best = (r['sum'], (qs, r))
    print('   n = 4 extensions evaluated: %d   unevaluable: %d' % (n - refused, refused),
          flush=True)
    print('   MAX EE + B reached: %d   %s'
          % (best[0], 'EXCEEDS 164 -- THE LAW IS REFUTED' if best[0] > 164
             else 'does not exceed 164'), flush=True)
    if best[1]:
        qs, r = best[1]
        print('      at %s' % ';'.join(','.join(map(str, q)) for q in qs), flush=True)
        print('      EE %d  SC2 %d  B %d  Q4 %d  TOTAL %d'
              % (r['EE'], r['SC2'], r['B'], r['Q4'], r['TOTAL']), flush=True)
    print('   top of the EE + B distribution: %s'
          % sorted(hist.items(), reverse=True)[:6], flush=True)
    out['extension'] = {'n3_extremes': len(tri58), 'evaluated': n - refused,
                        'unevaluable': refused, 'max_EE_plus_B': best[0],
                        'witness': [list(q) for q in best[1][0]] if best[1] else None,
                        'witness_anat': best[1][1] if best[1] else None,
                        'distribution': {str(k): v for k, v in sorted(hist.items())}}

    print('\nB. THE LADDER -- max(EE + B) by n, against two candidate closed forms')
    known = {2: 10, 3: 58}
    rec4 = anat([tuple(q) for q in WK.REC[4]])
    rec5 = anat([tuple(q) for q in WK.REC[5]])
    known[4] = max(164, best[0]); known[5] = rec5['sum']
    print('    n   max EE+B seen   6*C(n,2)+32*C(n,3)   10*C(n,2)+32*C(n,3)   source')
    src = {2: 'per-pair EE max 10, B = 0 ([P330])',
           3: 'exhaustive over the EE=10 family ([P369])',
           4: 'this session, 3730 compounds + these extensions',
           5: 'the n = 5 RECORD (not a search)'}
    for k in (2, 3, 4, 5):
        print('    %d   %10d   %14d   %17d   %s'
              % (k, known[k], 6 * comb(k, 2) + 32 * comb(k, 3),
                 10 * comb(k, 2) + 32 * comb(k, 3), src[k]))
    out['ladder'] = {str(k): {'max_seen': known[k],
                              'six_form': 6 * comb(k, 2) + 32 * comb(k, 3),
                              'ten_form': 10 * comb(k, 2) + 32 * comb(k, 3),
                              'source': src[k]} for k in (2, 3, 4, 5)}
    print('   n = 4 record EE+B %d   n = 5 record EE+B %d' % (rec4['sum'], rec5['sum']))

    out['reproduce'] = PROV.stamp(parameters={'seed': 164, 'family_height': 5, 'random': 400})
    json.dump(out, open(os.path.join(ROOT, 'data', 'ee_plus_b_scaling.json'), 'w'), indent=1)
    print('\nwrote data/ee_plus_b_scaling.json')


if __name__ == '__main__':
    main()
