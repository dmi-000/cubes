#!/usr/bin/env python3
"""[OQ 39] The one branch `EE + B <= 164` does not cover: the PAW.

`TOTAL = 7 + EE + 2*SC2 + B - Q4`, so the candidate law `EE + B <= 164` gives
`TOTAL <= 171 + 2*SC2 - Q4`.  Every construction with `SC2 <= 6` is then capped at 183 -- the
record, which sits on the line with `SC2 = 6, Q4 = 0`, attains it exactly.

**The exception is the paw.**  It carries `SC2 = 8` with `Q4 = 0` ([P350], [P358]: its cube 2
keeps a free rotation, so the four-fold coincidence is codimension 1 and generically absent).
On the line it would give `171 + 16 = 187`.  Its measured `EE + B` is 152 -- twelve short --
but that was ONE value of its free parameter.

So this sweeps the paw's exact one-parameter family, `Rot((1,-1,1), psi)` with `psi` rational
in the `(w:k)` chart, and reports `EE + B` and `Q4` across it.  Exact arithmetic in
`Q(sqrt3, sqrt5)` throughout -- no sampling of the geometry, only of the parameter.

The question is sharp: does any member reach `EE + B > 152`, and does any keep `SC2 = 8` with
`Q4 = 0` while doing so?
"""
import sys, os, json, itertools, collections
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import paw_construction as PAW          # NOTE: prints and builds C0, C1 at import scope
import provenance as PROV

ROOT = os.path.dirname(os.path.dirname(HERE))


def main():
    rows = []
    best = (-1, None)
    refused = 0
    for w in range(0, 13):
        for k in range(1, 13):
            if gcd(w, k) != 1:
                continue
            try:
                C2 = PAW.qrot(w, k, -k, k)
                sig, _ = PAW.census([PAW.C0, PAW.C1, C2, PAW.C3])
            except Exception:
                refused += 1
                continue
            EE = sig.get((2, 2), 0); SC = sig.get((3, 3), 0)
            T3 = sig.get((1, 1, 1), 0); Qg = sig.get((1, 1, 1, 1), 0)
            Q4 = sum(v for kk, v in sig.items() if len(kk) == 4)
            B = T3 + 4 * Qg
            tot = 7 + EE + 2 * SC + B - Q4
            rows.append({'psi': '%d:%d' % (w, k), 'EE': EE, 'SC2': SC, 'B': B, 'Q4': Q4,
                         'EE_plus_B': EE + B, 'TOTAL': tot})
            if EE + B > best[0]:
                best = (EE + B, rows[-1])
    print('paw family members evaluated: %d   unevaluable: %d' % (len(rows), refused))
    print('   psi      EE    B   EE+B   SC2  Q4   TOTAL')
    seen = set()
    for r in sorted(rows, key=lambda r: -r['EE_plus_B'])[:14]:
        print('   %-7s %3d  %3d   %3d    %2d  %2d    %3d'
              % (r['psi'], r['EE'], r['B'], r['EE_plus_B'], r['SC2'], r['Q4'], r['TOTAL']))
    sp = collections.Counter(r['EE_plus_B'] for r in rows)
    print('   EE + B spectrum across the family: %s' % dict(sorted(sp.items(), reverse=True)))
    q4s = collections.Counter(r['Q4'] for r in rows)
    print('   Q4 spectrum: %s' % dict(sorted(q4s.items())))
    print('   MAX EE + B in the paw family: %d   (the line is 164; 164 would give TOTAL 187)'
          % best[0])
    print('   MAX TOTAL in the paw family: %d   (record 183)' % max(r['TOTAL'] for r in rows))

    out = {'what': 'EE + B across the paw one-parameter family', 'supports': 'OQ 39',
           'evaluated': len(rows), 'unevaluable': refused,
           'max_EE_plus_B': best[0], 'max_TOTAL': max(r['TOTAL'] for r in rows),
           'rows': rows}
    out['reproduce'] = PROV.stamp(parameters={'psi_chart': 'w:k, 0<=w<=12, 1<=k<=12, coprime'},
                                  note='exact Q(sqrt3,sqrt5) census; parameter sampled, '
                                       'geometry exact')
    json.dump(out, open(os.path.join(ROOT, 'data', 'paw_ee_plus_b.json'), 'w'), indent=1)
    print('wrote data/paw_ee_plus_b.json')


if __name__ == '__main__':
    main()
