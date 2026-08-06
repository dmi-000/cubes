#!/usr/bin/env python3
"""Which single Cayley axis moves preserve 1217 / 1891? Full 36- and 42-move probe."""
import sys
from fractions import Fraction as F
sys.path.insert(0, "/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad")
from n78 import BASE, C6, C7, C8, cay, q_of, run

def probe(cubes, label, epss=(F(1,64), F(1,256))):
    base, _ = run(list(cubes))
    print('%s  base %s' % (label, base))
    surv = []
    for ci in range(1, len(cubes)):
        c0 = cay(cubes[ci])
        for ax in range(3):
            for sg in (1, -1):
                res = []
                for e in epss:
                    c = list(c0); c[ax] += sg*e
                    cfg = [cubes[k] if k != ci else q_of(c) for k in range(len(cubes))]
                    res.append(run(cfg)[0])
                if all(r == base for r in res):
                    surv.append((ci, 'xyz'[ax], '+-'[sg < 0]))
                    print('   HOLDS cube %d (quat %s) axis %s%s' % (ci, cubes[ci], 'xyz'[ax], '+-'[sg < 0]))
    print('   %d of %d single-axis moves preserve the count' % (len(surv), 6*(len(cubes)-1)))
    return surv

if __name__ == '__main__':
    probe(BASE+[C6, C7], 'n=7 1217')
    probe(BASE+[C6, C7, C8], 'n=8 1891')
