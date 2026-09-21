#!/usr/bin/env python3
"""[OQ 39] The `+7` in `TOTAL = 7 + T + B - Q4` is NOT a constant.

Found by checking a climb result against the engine: at
`1,0,0,0; 0,2,-3,-2; 0,2,3,2; -4,0,-5,-6` the identity predicts 177 and the engine returns
**175**.  Its signature census is `{(1,1,1): 128, (1,2): 36, (2,2): 42}` -- no exotic signature,
so this is not [P328]'s omitted-signature gap.

The identity is `TOTAL = 1 + L + sum c_ell + (1/2) sum_v excess(v)`, and
`(1/2) sum excess = EE + 2*SC2 + T3 + 3*Q4gen = T + B - Q4`.  So the leading term is
`1 + L + sum c_ell` -- the LEVEL COMPONENT COUNT ([P312], [P319]) -- and calling it 7 assumes a
value for `sum c_ell` that the n = 4 record happens to have.

This measures the leading term directly, as `engine_count - (T + B - Q4)`, over a spread of
compounds.  What matters for every bound drawn from the identity is whether it can EXCEED 7:
if it cannot, upper bounds computed with 7 are safe and only some region counts were overstated;
if it can, [P367]'s grid and everything reading TOTAL off `(T, B, Q4)` is wrong in the unsafe
direction.
"""
import sys, os, json, random, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import ee_bound_refute as EB
from c_level import shares_plane, engine
import wall_keys as WK
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def parts(qs):
    sig, _ = EB.vertices(qs)
    EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
    T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
    Q4 = sum(v for k, v in sig.items() if len(k) >= 4)
    return EE, SC, T3, Qg, Q4, EE + 2 * SC + T3 + 4 * Qg - Q4


def main():
    rng = random.Random(7777)
    named = {
        'n=4 RECORD': [tuple(q) for q in WK.REC[4]],
        'refuter (P373)': [(1, 0, 0, 0), (0, 2, -3, -2), (0, 2, -3, 2), (-4, -2, -5, -6)],
        'EE=42 climb': [(1, 0, 0, 0), (0, 2, -3, -2), (0, 2, 3, 2), (-4, 0, -5, -6)],
        'TOTAL=179 climb': [(1, 0, 0, 0), (2, 2, -2, -4), (0, 2, -3, 5), (-4, 0, -10, -6)],
    }
    pool = list(named.items())
    n = 0
    while n < 220:
        qs = [(1, 0, 0, 0)] + [tuple(rng.randint(-8, 8) for _ in range(4)) for _ in range(3)]
        if any(not any(q) for q in qs) or shares_plane(qs):
            continue
        n += 1
        pool.append(('random %d' % n, qs))

    hist = collections.Counter(); refused = 0; rows = []
    over = []
    for name, qs in pool:
        try:
            EE, SC, T3, Qg, Q4, tb = parts(qs)
            r = engine(qs)
        except Exception:
            refused += 1
            continue
        if 'error' in r or not r.get('by_depth'):
            refused += 1                       # a refusal is NOT a zero ([FAILURE_MODES 43])
            continue
        tot = sum(v for k, v in r['by_depth'].items() if k != '0')
        lead = tot - tb
        hist[lead] += 1
        if lead > 7:
            over.append({'name': name, 'quats': [list(q) for q in qs], 'lead': lead,
                         'engine': tot})
        if name in named:
            rows.append({'name': name, 'lead': lead, 'engine': tot, 'T_plus_B_minus_Q4': tb})
            print('   %-16s  engine %3d   T+B-Q4 %3d   leading term %d'
                  % (name, tot, tb, lead))

    print('\n   compounds evaluated: %d   unevaluable (engine refusals): %d'
          % (sum(hist.values()), refused))
    print('   leading term  1 + L + sum c_ell  distribution: %s' % dict(sorted(hist.items())))
    print('   values ABOVE 7: %d   %s' % (len(over),
                                          'UPPER BOUNDS USING 7 ARE UNSAFE' if over
                                          else 'so TOTAL <= 7 + T + B - Q4 is SAFE as a bound'))
    for o in over[:4]:
        print('      ', o)

    out = {'what': 'the leading term of the n=4 identity is not the constant 7',
           'supports': 'OQ 39', 'named': rows,
           'evaluated': sum(hist.values()), 'unevaluable': refused,
           'distribution': {str(k): v for k, v in sorted(hist.items())},
           'above_7': over}
    out['reproduce'] = PROV.stamp(parameters={'seed': 7777, 'random': 220})
    json.dump(out, open(os.path.join(ROOT, 'data', 'identity_constant.json'), 'w'), indent=1)
    print('\nwrote data/identity_constant.json')


if __name__ == '__main__':
    main()
