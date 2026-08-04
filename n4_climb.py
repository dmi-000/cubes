#!/usr/bin/env python3
"""Climb inside the leading n = 4 cells — is 183 beatable?

The phase-1 census (n4_program.py) ranks cells by the best total RANDOM
rational sampling reaches in them.  The record's own cell,
(9,9,9,13,13,13), reads 165 — eighteen short of the 183 we already know sits
there.  So the census under-reads a cell by however special its optimum is,
and four cells reading 171 are therefore candidates to contain something
ABOVE 183.

That is the whole hypothesis, and it is a hypothesis: the gap between
random-accessible and true ceiling need not be uniform across cells.  This
tests it the way 183 was originally found — greedy ascent with wide restarts,
seeded from each leading cell's best configuration.

The climb is deliberately NOT constrained to stay inside its seed cell.  A
constrained climb would measure the cell's ceiling; an unconstrained one finds
records.  The label of every peak is recorded, so we learn which cell the good
configurations actually live in rather than assuming it is the one we started
from.

CONTROL: the known record 183 is climbed too.  If the climber cannot hold 183
from its own configuration, nothing it reports about other cells means
anything.

Checkpointing: one file per seed, atomic rename, resumable — same discipline
as n4_program.py.
"""
import json
import os
import random
import sys
import time

import n4_program as N
from record_hunt import Engine, canon, climb, ok

OUT = os.path.join(N.OUT, 'climb')
RECORD_TOTAL = 183


def seeds(top):
    """Best configuration from each of the top cells, plus the record."""
    agg = N.cells_so_far()
    order = sorted(agg, key=lambda k: (-agg[k]['max'], k))
    out = []
    for key in order[:top]:
        out.append(('cell_' + key.replace(',', '_'), key, agg[key]['max'],
                    [list(q) for q in agg[key]['best']]))
    out.append(('control_183', 'the known record', RECORD_TOTAL,
                [list(q) for q in N.RECORD4]))
    return out


def main():
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    os.makedirs(OUT, exist_ok=True)
    eng = Engine(4, 1)
    rng = random.Random(20260803)
    best_overall = (0, None, None)
    for name, cell, seed_total, cfg in seeds(top):
        path = os.path.join(OUT, name + '.json')
        if os.path.exists(path):
            d = json.load(open(path))
            if d['peak'] > best_overall[0]:
                best_overall = (d['peak'], d['cell'], d['quats'])
            continue
        t0 = time.time()
        fh = open(os.path.join(OUT, name + '.log'), 'w')
        top_cfg, peak = climb(eng, cfg, fh, name, rng, restarts=restarts)
        fh.close()
        lab = N.labels_of([[tuple(q) for q in top_cfg]])[0][1]
        rec = {'name': name, 'seed_cell': cell, 'seed_total': seed_total,
               'peak': peak, 'peak_cell': ','.join(map(str, lab)) if lab else None,
               'quats': top_cfg, 'cell': cell, 'secs': round(time.time()-t0, 1),
               'evals': eng.evals}
        tmp = path + '.tmp'
        json.dump(rec, open(tmp, 'w'))
        os.replace(tmp, path)
        flag = ''
        if peak > RECORD_TOTAL:
            flag = '   *** ABOVE THE RECORD 183 ***'
        elif peak == RECORD_TOTAL:
            flag = '   (ties the record)'
        print('%-34s seed %3d -> peak %3d  in cell %-22s (%.0fs)%s'
              % (name[:34], seed_total, peak,
                 rec['peak_cell'], rec['secs'], flag), flush=True)
        if peak > best_overall[0]:
            best_overall = (peak, rec['peak_cell'], top_cfg)
    print('\nbest overall: %d in cell %s' % (best_overall[0], best_overall[1]))
    print('quaternions: %s' % (best_overall[2],))
    if best_overall[0] > RECORD_TOTAL:
        print('*** THIS BEATS THE PUBLISHED n=4 RECORD OF 183 ***')
        print('    verify independently before believing it:')
        print('    ./cube_regions_n --quats %s'
              % ';'.join(','.join(map(str, q)) for q in best_overall[2]))


if __name__ == '__main__':
    main()
