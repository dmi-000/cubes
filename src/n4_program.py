#!/usr/bin/env python3
"""The n = 4 structure program: cells, ceilings, dimensions.

Extends the n=2 map (Postscript 70) and n=3 structure graph (N3_STRUCTURE.md)
to four cubes.  A 4-cube compound has C(4,2) = 6 pairs, each a point of the
n=2 configuration space, so its label is the multiset of its six pair counts
drawn from {1,4,5,9,13}.  There are 210 such multisets; the realisable ones are
fewer (a label containing 1 must respect the fact that coincidence is an
equivalence relation).  The live question: the record 183 has label
(3x13, 3x9) -- is that the ceiling cell, or does some other mixture beat it?

PHASE 1  census: random configurations -> label, total.  Per-cell ceiling.
PHASE 2  dimension: probe a lattice around the best configuration of each
         cell and count how many neighbours keep the label.  In the
         9-dimensional n=4 space a d-dimensional component contributes
         3^d - 1 of the 3^9 - 1 = 19682 points, so the cardinality reads off
         the dimension (the method that gave 728 -> 3-dim and 8 -> 2-dim at
         n=2 and n=3).

CHECKPOINTING, and why it is shaped this way.  Work is split into UNITS, each
writing ONE file, written to .tmp and renamed atomically.  A unit is complete
iff its file exists.  Resuming skips those.  There is no append-mode
accumulation and no manifest to fall out of sync -- both of which corrupted
results earlier in this project (see FAILURE_MODES.md 1 and 11b).  The work
definition is hashed into the directory name, so a resume against a changed
definition lands in a fresh directory instead of blending incompatible runs.

USAGE
    python3 n4_program.py gate                 # engine must reproduce knowns
    python3 n4_program.py phase1 --shard i --of k
    python3 n4_program.py phase2 --shard i --of k
    python3 n4_program.py report
"""
import argparse
import collections
import hashlib
import itertools
import json
import math
import os
import random
import subprocess
import sys
import time

ENGINE = './cube_regions_n'
BATCH = 2000

# ---- work definition; its hash names the output directory -------------------
WORKDEF = {
    'version': 1,
    'phase1_units': 60,
    'phase1_per_unit': 4000,
    'heights': [3, 5, 8, 13, 21, 34, 55, 89],
    'seed': 20260803,
    'probe_full_top': 12,      # cells given the full 19682-point lattice
    'probe_sampled': 3000,     # random directions for the rest
    'probe_eps_den': 64,
}
TAG = hashlib.sha256(json.dumps(WORKDEF, sort_keys=True).encode()).hexdigest()[:10]
OUT = 'n4_run_%s' % TAG
PARTS = os.path.join(OUT, 'parts')

KNOWN = {
    '1,0,0,0;0,1,1,1': 13,
    '1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4': 183,
    '4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1': 393,
    '4,1,1,-1;3,3,7,3;5,-1,-5,-5;2,1,1,1;1,1,1,1;7,14,1,-5': 727,
}
RECORD4 = [(1, 0, 0, 0), (0, 5, 3, 2), (1, -4, -1, 1), (1, 1, -1, -4)]


def red(q):
    g = 0
    for x in q:
        g = math.gcd(g, abs(x))
    return tuple(x // g for x in q) if g > 1 else tuple(q)


def counts(cfgs):
    """Exact bounded-region counts for a list of configurations."""
    out = []
    for i in range(0, len(cfgs), BATCH):
        chunk = cfgs[i:i+BATCH]
        inp = '\n'.join(';'.join(','.join(map(str, q)) for q in c)
                        for c in chunk) + '\n'
        p = subprocess.run([ENGINE, '--quats-stdin'], input=inp,
                           capture_output=True, text=True)
        rows = [json.loads(l).get('bounded') for l in p.stdout.splitlines()
                if l.startswith('{')]
        if len(rows) != len(chunk):
            raise SystemExit('engine returned %d results for %d configs -- '
                             'refusing to continue on truncated output'
                             % (len(rows), len(chunk)))
        out += rows
    return out


def labels_of(cfgs):
    """(total, label) for each configuration; label = sorted 6 pair counts."""
    tot = counts(cfgs)
    pairs = [(c[i], c[j]) for c in cfgs
             for i, j in itertools.combinations(range(4), 2)]
    pc = counts(pairs)
    out = []
    for k, c in enumerate(cfgs):
        six = pc[6*k:6*k+6]
        out.append((tot[k], tuple(sorted(x for x in six if x is not None))
                    if None not in six else None))
    return out


def gate():
    print('gate: engine must reproduce known values')
    ok = True
    for q, want in KNOWN.items():
        p = subprocess.run([ENGINE, '--quats', q], capture_output=True, text=True)
        got = json.loads(p.stdout).get('bounded') if p.stdout.startswith('{') else None
        print('   %-58s -> %-6s expected %-6s %s'
              % (q[:58], got, want, 'OK' if got == want else 'FAIL'))
        ok &= (got == want)
    if not ok:
        raise SystemExit('GATE FAILED -- the rebuilt engine does not reproduce '
                         'known counts; no results from this build are valid')
    print('gate PASSED')


def unit_path(name):
    return os.path.join(PARTS, name + '.json')


def unit_params():
    """The parameters a unit was actually computed with."""
    return {k: WORKDEF[k] for k in ('phase1_per_unit', 'heights', 'seed')}


def complete(name):
    """A unit counts as done only if it exists AND was computed with the
    current parameters.  The directory is named by a hash of WORKDEF, but that
    hash is fixed at import time -- mutating WORKDEF afterwards (as a smoke
    test easily does) would otherwise leave a short unit masquerading as a
    finished one.  Checked, not assumed."""
    fn = unit_path(name)
    if not os.path.exists(fn):
        return False
    try:
        d = json.load(open(fn))
    except Exception:
        return False
    if 'params' in d and d['params'] != unit_params():
        print('  %s was computed with different parameters -- redoing' % name,
              flush=True)
        return False
    return True


def write_unit(name, obj):
    os.makedirs(PARTS, exist_ok=True)
    tmp = unit_path(name) + '.tmp'
    with open(tmp, 'w') as fh:
        json.dump(obj, fh)
    os.replace(tmp, unit_path(name))          # atomic


def phase1(shard, of):
    for u in range(WORKDEF['phase1_units']):
        if u % of != shard:
            continue
        name = 'p1_%03d' % u
        if complete(name):
            continue
        t0 = time.time()
        rng = random.Random(WORKDEF['seed'] * 1000 + u)
        h = WORKDEF['heights'][u % len(WORKDEF['heights'])]
        cfgs = []
        while len(cfgs) < WORKDEF['phase1_per_unit']:
            c = [(1, 0, 0, 0)] + [red(tuple(rng.randint(-h, h) for _ in range(4)))
                                  for _ in range(3)]
            if all(any(x) for x in c):
                cfgs.append(c)
        agg = {}
        for cfg, (tot, lab) in zip(cfgs, labels_of(cfgs)):
            if tot is None or lab is None:
                continue
            k = ','.join(map(str, lab))
            e = agg.setdefault(k, {'n': 0, 'max': -1, 'min': 10**9, 'best': None})
            e['n'] += 1
            e['min'] = min(e['min'], tot)
            if tot > e['max']:
                e['max'] = tot
                e['best'] = [list(q) for q in cfg]
        write_unit(name, {'unit': u, 'height': h, 'cells': agg,
                          'params': unit_params(),
                          'secs': round(time.time()-t0, 1)})
        print('  %s: %d cells, %.0fs' % (name, len(agg), time.time()-t0),
              flush=True)


def cells_so_far():
    agg = {}
    for fn in sorted(os.listdir(PARTS)) if os.path.isdir(PARTS) else []:
        if not fn.startswith('p1_') or not fn.endswith('.json'):
            continue
        d = json.load(open(os.path.join(PARTS, fn)))
        for k, e in d['cells'].items():
            a = agg.setdefault(k, {'n': 0, 'max': -1, 'min': 10**9, 'best': None})
            a['n'] += e['n']
            a['min'] = min(a['min'], e['min'])
            if e['max'] > a['max']:
                a['max'] = e['max']
                a['best'] = e['best']
    return agg


def phase2(shard, of):
    agg = cells_so_far()
    order = sorted(agg, key=lambda k: -agg[k]['max'])
    eps_den = WORKDEF['probe_eps_den']
    for idx, key in enumerate(order):
        if idx % of != shard:
            continue
        name = 'p2_%03d' % idx
        if os.path.exists(unit_path(name)):
            continue
        cfg = [tuple(q) for q in agg[key]['best']]
        full = idx < WORKDEF['probe_full_top']
        dirs = ([d for d in itertools.product((-1, 0, 1), repeat=9) if any(d)]
                if full else None)
        if dirs is None:
            rng = random.Random(hash(key) & 0xffffffff)
            dirs = [tuple(rng.choice((-1, 0, 1)) for _ in range(9))
                    for _ in range(WORKDEF['probe_sampled'])]
            dirs = [d for d in dirs if any(d)]
        t0 = time.time()
        nb = []
        for d in dirs:
            c = [cfg[0]]
            okc = True
            for j in range(3):
                # perturb cube j+1 in Cayley coordinates by d[3j..3j+2]/eps_den
                w, x, y, z = cfg[j+1]
                num = [w*eps_den, x*eps_den + d[3*j]*w,
                       y*eps_den + d[3*j+1]*w, z*eps_den + d[3*j+2]*w]
                if not any(num):
                    okc = False
                    break
                c.append(red(tuple(num)))
            if okc:
                nb.append(c)
        keep = 0
        for i in range(0, len(nb), 400):
            for tot, lab in labels_of(nb[i:i+400]):
                if lab is not None and ','.join(map(str, lab)) == key:
                    keep += 1
        write_unit(name, {'cell': key, 'ceiling': agg[key]['max'],
                          'probed': len(nb), 'keep': keep, 'full': full,
                          'secs': round(time.time()-t0, 1)})
        print('  %s cell %-22s probed %5d keep %5d (%.0fs)'
              % (name, key, len(nb), keep, time.time()-t0), flush=True)


def report():
    agg = cells_so_far()
    probes = {}
    for fn in sorted(os.listdir(PARTS)):
        if fn.startswith('p2_'):
            d = json.load(open(os.path.join(PARTS, fn)))
            probes[d['cell']] = d
    rec = labels_of([RECORD4])[0]
    reckey = ','.join(map(str, rec[1]))
    print('n = 4 structure, run %s' % TAG)
    print('configurations counted: %d' % sum(e['n'] for e in agg.values()))
    print('cells observed: %d of 210 possible\n' % len(agg))
    print('%-24s %7s %7s %8s   %s' % ('cell (six pair counts)', 'ceiling',
                                      'configs', 'dim', 'note'))
    for k in sorted(agg, key=lambda k: -agg[k]['max']):
        p = probes.get(k)
        dim = ''
        if p and p['probed']:
            frac = p['keep'] / p['probed']
            if p['full']:
                d = round(math.log(p['keep'] + 1, 3), 2) if p['keep'] else 0
                dim = '%.2f' % d
            else:
                dim = '~%.0f%%' % (100*frac)
        note = 'THE RECORD 183' if k == reckey else ''
        print('%-24s %7d %7d %8s   %s' % (k, agg[k]['max'], agg[k]['n'],
                                          dim, note))
    print('\nrecord 183 label: %s' % reckey)
    top = max(agg, key=lambda k: agg[k]['max'])
    print('highest ceiling found: %d in cell %s' % (agg[top]['max'], top))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['gate', 'phase1', 'phase2', 'report'])
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--of', type=int, default=1)
    a = ap.parse_args()
    os.makedirs(PARTS, exist_ok=True)
    if a.cmd == 'gate':
        gate()
    elif a.cmd == 'phase1':
        phase1(a.shard, a.of)
    elif a.cmd == 'phase2':
        phase2(a.shard, a.of)
    else:
        report()
