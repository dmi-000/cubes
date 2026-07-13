#!/usr/bin/env python3
# Working principles: this file's own docstring + PROJECT.md + six_cube_search_results.md
# Postscripts 12/16/17/17-addendum. Project index: README.md.
"""shared_axis_search.py -- test the "hub-and-spoke / shared-axis-cluster
with FREE continuous spoke angles" hypothesis directly.

FAMILY. n cubes = union of CLUSTERS sharing one common axis a, plus
optional fully-free cubes. A cluster is (base, angles): base is either
None ("on-axis" cluster: members are axis_rot(a,p,q) directly, i.e. the
cube's own corner sits on axis a -- CORNER concurrence, pairwise count 13
generically) or an integer quat B ("spoke" cluster: members are
axis_rot(a,p,q).B for a shared but otherwise generic base orientation --
pairwise count 9 generically, the "shared face-axis" locus of Postscript
17-addendum). angles = list of independent rational (p,q) pairs (tan
half-angle = p/q about axis a; q=0 encodes the 180-degree element). This
covers BOTH concurrence types the project's incidence geometry (Section 6
of six_cube_search_results.md) identifies as the ingredients of every
record.

GATE (see run_gates()): 183 (n=4) and 723 (n=6) are reconstructed EXACTLY,
bit for bit, from this family:
  183 = axis(1,1,1): on-axis cluster{(0,1),(1,4)} + spoke cluster
        base=(0,5,3,2){(0,1),(-1,1)}            <- spoke pair IS the exact
        C3-locked pair; on-axis pair is FREE (angle 1/4, no group meaning).
  723 = axis(1,1,1): spoke cluster base=(4,1,1,-1){(0,1),(1,1),(-1,1)}
        (the EXACT C3 orbit, fully locked) + on-axis cluster
        {(1,2),(1,1),(2,5)}  <- only the MIDDLE member (1,1) is the C3
        angle; the other two are FREE.
So BOTH known records already mix one fully-locked cluster with one
partly-or-fully FREE cluster -- this script asks whether freeing every
cluster (coordinate search over the continuous angle DOF, from scratch,
not just fine-tuning near the record) reaches or beats 183/393/723, and
whether "shared axis cluster" structure beats matched non-clustered
controls at equal n.

HARD RULES (per task spec): exact counting only (cube_regions_n), gate
against known records before trusting anything, do not modify validated
files (six_cube_search_results.md, exact_search_results.jsonl) -- this
script never writes to them, <=4 worker processes, run detached.

Usage:
  python3 shared_axis_search.py gates     # gates only, then stop
  python3 shared_axis_search.py           # gates, then full campaign
"""
import json
import math
import os
import random
import subprocess
import sys
import time

import symmetry_search as ss

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, 'cube_regions_n')
LOG_PATH = os.path.join(HERE, 'shared_axis_search.jsonl')
REPORT_PATH = os.path.join(HERE, 'shared_axis_search_report.md')
WORKERS = 4                      # hard cap per task instructions
MAXC = ss.MAXC                   # 512, int128 overflow budget

gcd_reduce = ss.gcd_reduce
quat_mul = ss.quat_mul
cap_ok = ss.cap_ok

RECORDS = {4: 183, 5: 393, 6: 723}

# ============================================================ core family
AX111 = (1, 1, 1)
AX001 = (0, 0, 1)
AX110 = (1, 1, 0)
AXES = {'(1,1,1)': AX111, '(0,0,1)': AX001, '(1,1,0)': AX110}

# rational finite orders realizable EXACTLY (as equally-spaced angles) on
# each axis -- see symmetry_search3.py's correctness note: only th with
# rational tan(th/2) survive the axis normalization.
LOCKABLE_ORDERS = {
    '(1,1,1)': {1: 'C1', 2: 'C2', 3: 'C3', 6: 'C6'},
    '(0,0,1)': {1: 'C1', 2: 'C2', 4: 'C4'},
    '(1,1,0)': {1: 'C1', 2: 'C2'},
}


def axis_rot(axis, p, q):
    """Integer quat for tan(half-angle)=p/q rotation about integer axis
    `axis`. q=0 encodes the pure-quaternion 180-degree element."""
    return tuple(gcd_reduce([q, p * axis[0], p * axis[1], p * axis[2]]))


def cluster_quats(axis, base, angles):
    out = []
    for p, q in angles:
        ar = axis_rot(axis, p, q)
        cq = ar if base is None else tuple(gcd_reduce(list(quat_mul(ar, base))))
        out.append(cq)
    return out


def build_config(axis, clusters, free):
    """clusters: list of (base_or_None, [(p,q),...]). free: list of
    integer quats. Returns the full n-cube quat list, or None if any
    piece exceeds the component cap."""
    cfg = []
    for base, angles in clusters:
        cfg.extend(cluster_quats(axis, base, angles))
    cfg.extend(free)
    if not all(cap_ok(q) for q in cfg):
        return None
    return cfg


def locked_angles(axis_name, m, seed_pq=(0, 1)):
    """Exact equally-spaced m-element angle list on axis_name, if that
    order is rationally realizable there (see LOCKABLE_ORDERS); else None.
    seed_pq lets a spoke cluster start its locked orbit anywhere (locking
    is about SPACING, not absolute phase)."""
    orders = LOCKABLE_ORDERS[axis_name]
    if m not in orders:
        return None
    gname = orders[m]
    if gname == 'C1':
        return [seed_pq]
    axis = AXES[axis_name]
    seed_q = axis_rot(axis, *seed_pq)
    gq = ss.group_quats(gname)
    orb = ss.quat_orbit(gq, seed_q, ss.O_Q5)
    if len(orb) != m:
        return None
    # recover (p,q) is not needed -- callers that need locked_angles use it
    # only to build clusters, so return the ORBIT QUATS directly via a
    # sentinel: caller detects seed_pq usage. Simplify: return None here
    # and let callers use locked_cluster_quats instead (see below).
    return orb  # list of integer quats (NOT (p,q) pairs) when m>1


def locked_cluster_quats(axis_name, base, m, seed_pq=(0, 1)):
    """Build a LOCKED (exactly equally-spaced, group-orbit) cluster of m
    members with the given base, on axis_name, if realizable; else None."""
    orb = locked_angles(axis_name, m, seed_pq)
    if orb is None:
        return None
    if m == 1:
        p, q = orb[0]
        ar = axis_rot(AXES[axis_name], p, q)
        cq = ar if base is None else tuple(gcd_reduce(list(quat_mul(ar, base))))
        return [cq]
    out = []
    for gq in orb:
        cq = gq if base is None else tuple(gcd_reduce(list(quat_mul(gq, base))))
        out.append(cq)
    return out


# ============================================================ evaluation
def quats_line(quats):
    return ';'.join(','.join(str(c) for c in q) for q in quats)


def cpp_batch_n(configs, workers=WORKERS):
    """Exact-count many configs (possibly different n each) via
    cube_regions_n --quats-stdin (n inferred per line). Returns list of
    (total, by_depth) aligned with input order; None for any that error."""
    if not configs:
        return []
    n = len(configs)
    nproc = max(1, min(workers, n))
    chunks = [[] for _ in range(nproc)]
    for i, cfg in enumerate(configs):
        chunks[i % nproc].append((i, cfg))
    results = [None] * n
    procs = []
    for chunk in chunks:
        if not chunk:
            continue
        inp = '\n'.join(quats_line(cfg) for _, cfg in chunk) + '\n'
        p = subprocess.Popen([BIN, '--quats-stdin'], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        procs.append((p, chunk, inp))
    for p, chunk, inp in procs:
        out, err = p.communicate(inp)
        lines = [l for l in out.strip().split('\n') if l]
        assert len(lines) == len(chunk), \
            f'cpp_batch_n: expected {len(chunk)} results got {len(lines)}: {err[:400]}'
        for (idx, cfg), line in zip(chunk, lines):
            rec = json.loads(line)
            if 'error' in rec:
                results[idx] = None
            else:
                bd = {int(k): v for k, v in rec['by_depth'].items() if k != '0'}
                results[idx] = (rec['bounded'], bd)
    return results


def log(rec):
    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(rec) + '\n')


# ================================================================= GATES
def run_gates():
    print('=== GATES ===', flush=True)
    cfg183 = build_config(AX111,
        [(None, [(0, 1), (1, 4)]), ((0, 5, 3, 2), [(0, 1), (-1, 1)])], [])
    res = cpp_batch_n([cfg183])[0]
    tot183 = res[0] if res else None
    print(f'  GATE 183 (n=4, on-axis{{(0,1),(1,4)}} + spoke{{(0,1),(-1,1)}}): '
          f'total={tot183} (want 183) {"PASS" if tot183 == 183 else "FAIL"}',
          flush=True)

    cfg723 = build_config(AX111,
        [((4, 1, 1, -1), [(0, 1), (1, 1), (-1, 1)]),
         (None, [(1, 2), (1, 1), (2, 5)])], [])
    res = cpp_batch_n([cfg723])[0]
    tot723 = res[0] if res else None
    print(f'  GATE 723 (n=6, spoke{{C3-locked}} + on-axis{{(1,2),(1,1),(2,5)}}): '
          f'total={tot723} (want 723) {"PASS" if tot723 == 723 else "FAIL"}',
          flush=True)

    if tot183 != 183 or tot723 != 723:
        raise SystemExit('GATE FAILED -- family does not reproduce the records. Stopping.')
    print('  BOTH GATES PASS -- the family CONTAINS both records exactly.\n', flush=True)
    return {'gate183': tot183, 'gate723': tot723}


# ============================================================== genomes
# genome = {'axis_name': str, 'clusters': [{'kind':'onaxis'|'spoke',
#            'base': quat|None, 'angles': [(p,q),...]}, ...], 'free': [quat,...]}

def genome_config(genome):
    axis = AXES[genome['axis_name']]
    clusters = [(c['base'] if c['kind'] == 'spoke' else None, c['angles'])
                for c in genome['clusters']]
    return build_config(axis, clusters, genome['free'])


def genome_n(genome):
    tot = 0
    for c in genome['clusters']:
        tot += len(c['angles']) if c.get('angles') is not None else len(c['fixed_quats'])
    return tot + len(genome['free'])


FREEB = [(1, 0, 0, 0), (2, 1, 1, 1), (3, 1, 1, 1), (5, 2, 2, 2),
         (2, 1, 0, 0), (3, 2, 1, 0), (4, 1, 1, -1), (5, -1, -5, -5)]


def rand_pq(rng, kmax=12):
    while True:
        p = rng.randint(-kmax, kmax)
        q = rng.randint(0, kmax)
        if p == 0 and q == 0:
            continue
        if q == 0 and p < 0:
            p = -p  # (p,0) all equivalent up to sign/gcd
        g = math.gcd(abs(p), abs(q)) or 1
        return (p // g, q // g)


def rand_base(rng):
    return tuple(gcd_reduce([rng.randint(-15, 15) for _ in range(4)]))


def random_genome(axis_name, spec, rng):
    """spec: list of ('onaxis'|'spoke', size) for clusters, plus n_free."""
    cluster_specs, n_free = spec
    clusters = []
    for kind, m in cluster_specs:
        base = rand_base(rng) if kind == 'spoke' else None
        angles = [rand_pq(rng) for _ in range(m)]
        clusters.append({'kind': kind, 'base': base, 'angles': angles})
    free = [rand_base(rng) for _ in range(n_free)]
    return {'axis_name': axis_name, 'clusters': clusters, 'free': free}


def locked_genome(axis_name, spec, rng):
    """Best-effort LOCKED control: every cluster forced to an exact
    equally-spaced group orbit where realizable on this axis; clusters
    whose size has no rational order on this axis fall back to a random
    (still independently-drawn, NOT coordinate-searched) angle set --
    flagged via 'locked' bool per cluster so the report can tell exact
    from best-effort."""
    cluster_specs, n_free = spec
    clusters = []
    for kind, m in cluster_specs:
        base = rand_base(rng) if kind == 'spoke' else None
        seed_pq = rand_pq(rng) if m > 1 else (0, 1)
        lq = locked_cluster_quats(axis_name, base, m, seed_pq)
        if lq is not None:
            # recover as raw quats directly (bypass angle repr: store as
            # a pseudo-cluster with base=None, angles=[] and inject via
            # 'fixed_quats' so genome_config can special-case it)
            clusters.append({'kind': kind, 'base': base, 'angles': None,
                              'fixed_quats': lq, 'locked': True})
        else:
            angles = [rand_pq(rng) for _ in range(m)]
            clusters.append({'kind': kind, 'base': base, 'angles': angles,
                              'locked': False})
    free = [rand_base(rng) for _ in range(n_free)]
    return {'axis_name': axis_name, 'clusters': clusters, 'free': free}


def genome_config2(genome):
    """genome_config, extended to honor 'fixed_quats' (locked clusters)."""
    cfg = []
    for c in genome['clusters']:
        if c.get('fixed_quats') is not None:
            cfg.extend(c['fixed_quats'])
        else:
            axis = AXES[genome['axis_name']]
            base = c['base'] if c['kind'] == 'spoke' else None
            cfg.extend(cluster_quats(axis, base, c['angles']))
    cfg.extend(genome['free'])
    if not all(cap_ok(q) for q in cfg):
        return None
    return cfg


# ============================================================ neighbors
def perturb_pq(pq, rng):
    p, q = pq
    cands = set()
    for d in (-2, -1, 1, 2):
        cands.add((p + d, q))
        if q + d >= 0:
            cands.add((p, q + d))
    cands.add((-p, q))
    if p != 0:
        cands.add((q, p))
    out = []
    for np_, nq_ in cands:
        if np_ == 0 and nq_ == 0:
            continue
        g = math.gcd(abs(np_), abs(nq_)) or 1
        np_, nq_ = np_ // g, nq_ // g
        if nq_ < 0:
            np_, nq_ = -np_, -nq_
        out.append((np_, nq_))
    return list(set(out))


def perturb_base(base, rng):
    out = []
    for i in range(4):
        for d in (-2, -1, 1, 2):
            nb = list(base)
            nb[i] += d
            out.append(tuple(gcd_reduce(nb)))
    return out


def neighbor_genomes(genome, rng, max_per_param=6):
    """Yield (move_desc, new_genome) with ONE parameter perturbed."""
    for ci, c in enumerate(genome['clusters']):
        if c.get('locked'):
            continue  # locked clusters are never perturbed (that's the control)
        if c['angles'] is not None:
            for ai in range(len(c['angles'])):
                cands = perturb_pq(c['angles'][ai], rng)
                rng.shuffle(cands)
                for npq in cands[:max_per_param]:
                    g2 = _copy_genome(genome)
                    g2['clusters'][ci]['angles'][ai] = npq
                    yield (f'c{ci}.angle{ai}', g2)
        if c['kind'] == 'spoke' and c['base'] is not None:
            cands = perturb_base(c['base'], rng)
            rng.shuffle(cands)
            for nb in cands[:max_per_param]:
                g2 = _copy_genome(genome)
                g2['clusters'][ci]['base'] = nb
                yield (f'c{ci}.base', g2)
    for fi in range(len(genome['free'])):
        cands = perturb_base(genome['free'][fi], rng)
        rng.shuffle(cands)
        for nb in cands[:max_per_param]:
            g2 = _copy_genome(genome)
            g2['free'][fi] = nb
            yield (f'free{fi}', g2)


def _copy_genome(genome):
    return {'axis_name': genome['axis_name'],
            'clusters': [dict(c, angles=(list(c['angles']) if c.get('angles') is not None else None),
                               base=c.get('base'))
                          for c in genome['clusters']],
            'free': list(genome['free'])}


def wide_perturb(genome, rng, n_changes=3):
    """Multi-parameter jump (escape plateaus, per Postscript 15's lesson
    that wide perturbation -- not single-step greedy -- is what escapes
    stalls)."""
    g2 = _copy_genome(genome)
    movable = []
    for ci, c in enumerate(g2['clusters']):
        if c.get('locked'):
            continue
        if c['angles'] is not None:
            for ai in range(len(c['angles'])):
                movable.append(('angle', ci, ai))
        if c['kind'] == 'spoke' and c['base'] is not None:
            movable.append(('base', ci, None))
    for fi in range(len(g2['free'])):
        movable.append(('free', fi, None))
    if not movable:
        return g2
    for _ in range(min(n_changes, len(movable))):
        kind, i, j = movable[rng.randrange(len(movable))]
        if kind == 'angle':
            g2['clusters'][i]['angles'][j] = rand_pq(rng)
        elif kind == 'base':
            g2['clusters'][i]['base'] = rand_base(rng)
        else:
            g2['free'][i] = rand_base(rng)
    return g2


# =============================================================== climber
def climb(genome0, rng, steps=25, restarts=3, wide_tries=6, tag='', part=''):
    """Coordinate-descent hillclimb with wide-perturbation basin hops.
    Returns dict(best_total, best_bd, best_genome, evals)."""
    best_genome, best_total, best_bd = None, -1, None
    nev = 0

    def eval_genomes(genomes):
        nonlocal nev
        cfgs, valid = [], []
        for g in genomes:
            cfg = genome_config2(g)
            if cfg is not None:
                cfgs.append(cfg)
                valid.append(g)
        if not cfgs:
            return []
        res = cpp_batch_n(cfgs)
        nev += len(cfgs)
        out = []
        for g, cfg, r in zip(valid, cfgs, res):
            if r is None:
                continue
            tot, bd = r
            out.append((g, cfg, tot, bd))
        return out

    cur = genome0
    res = eval_genomes([cur])
    if not res:
        return dict(best_total=-1, best_bd=None, best_genome=None, evals=nev)
    cur, cur_cfg, cur_total, cur_bd = res[0]
    if cur_total > best_total:
        best_genome, best_total, best_bd = cur, cur_total, cur_bd

    stall = 0
    for step in range(steps):
        cands = list(neighbor_genomes(cur, rng))
        gs = [g for _, g in cands]
        results = eval_genomes(gs)
        for g, cfg, tot, bd in results:
            log({'tag': tag, 'part': part, 'stage': f'climb{step}',
                 'n': genome_n(g), 'quats': cfg, 'total': tot, 'by_depth': bd})
        results.sort(key=lambda r: -r[2])
        if results and results[0][2] > cur_total:
            cur, _, cur_total, cur_bd = results[0]
            stall = 0
        else:
            stall += 1
        if cur_total > best_total:
            best_genome, best_total, best_bd = cur, cur_total, cur_bd
        if stall >= 4:
            break

    # wide-perturbation basin hops from the best-so-far
    for _ in range(wide_tries):
        wg = wide_perturb(best_genome, rng, n_changes=rng.choice([2, 3, 4]))
        res = eval_genomes([wg])
        if not res:
            continue
        g, cfg, tot, bd = res[0]
        log({'tag': tag, 'part': part, 'stage': 'wide', 'n': genome_n(g),
             'quats': cfg, 'total': tot, 'by_depth': bd})
        if tot > best_total * 0.85:  # only re-climb promising basins
            cur = g
            for step in range(steps // 2):
                cands = list(neighbor_genomes(cur, rng))
                gs = [gg for _, gg in cands]
                results = eval_genomes(gs)
                for gg, cfg2, tot2, bd2 in results:
                    log({'tag': tag, 'part': part, 'stage': f'rewide{step}',
                         'n': genome_n(gg), 'quats': cfg2, 'total': tot2, 'by_depth': bd2})
                results.sort(key=lambda r: -r[2])
                if results and results[0][2] > tot:
                    cur, _, tot, bd = results[0]
                else:
                    break
            if tot > best_total:
                best_genome, best_total, best_bd = cur, tot, bd

    return dict(best_total=best_total, best_bd=best_bd, best_genome=best_genome, evals=nev)


def multi_restart(spec, axis_name, n_random, rng, steps=20, restarts_wide=4,
                   tag='', part='', start_genomes=()):
    """n_random fresh random-init climbs + any explicit start genomes
    (e.g. reproducing/near a known record), keep the best."""
    overall = dict(best_total=-1, best_bd=None, best_genome=None, evals=0)
    all_starts = list(start_genomes) + \
        [random_genome(axis_name, spec, rng) for _ in range(n_random)]
    for g0 in all_starts:
        r = climb(g0, rng, steps=steps, wide_tries=restarts_wide, tag=tag, part=part)
        overall['evals'] += r['evals']
        if r['best_total'] > overall['best_total']:
            overall.update(best_total=r['best_total'], best_bd=r['best_bd'],
                            best_genome=r['best_genome'])
    return overall


ALL_RESULTS = {}


def run_template(tag, axis_name, spec, record, n_random_free=6, n_random_locked=4,
                  start_genomes=(), rng=None):
    """Run BOTH a LOCKED-control search (angles forced to exact group
    orbits where realizable) and a FREE search (independent coordinate
    search over every angle), for one (axis, cluster-size) template."""
    print(f'  [{tag}] axis={axis_name} spec={spec} (record n={sum(m for _,m in spec[0])+spec[1]}={record})',
          flush=True)
    t0 = time.time()
    locked = multi_restart(spec, axis_name, n_random_locked, rng, steps=14,
                            restarts_wide=2, tag=tag, part='locked',
                            start_genomes=[locked_genome(axis_name, spec, rng)
                                           for _ in range(2)])
    free = multi_restart(spec, axis_name, n_random_free, rng, steps=22,
                          restarts_wide=6, tag=tag, part='free',
                          start_genomes=start_genomes)
    dt = time.time() - t0
    rec = dict(axis=axis_name, spec=spec, record=record,
               locked_best=locked['best_total'], free_best=free['best_total'],
               locked_genome=locked['best_genome'], free_genome=free['best_genome'],
               free_bd=free['best_bd'], evals=locked['evals'] + free['evals'], dt=dt)
    ALL_RESULTS[tag] = rec
    beat = 'BEATS RECORD' if free['best_total'] and free['best_total'] > record else ''
    print(f'      locked={locked["best_total"]}  free={free["best_total"]}  '
          f'(record {record}) {beat}  evals={rec["evals"]}  {dt:.0f}s', flush=True)
    if beat:
        log({'FLAG': 'NEW RECORD OR TIE-BREAK', 'tag': tag, 'total': free['best_total'],
             'record': record, 'config': genome_config2(free['best_genome'])})
    return rec


# ================================================================ MAIN
def main():
    rng = random.Random(20260712)
    t0 = time.time()
    gates = run_gates()

    print('########## n=4 templates (record 183) ##########', flush=True)
    # reproduce-and-free-search starting exactly from the 183 structure
    seed183 = {'axis_name': '(1,1,1)',
               'clusters': [{'kind': 'onaxis', 'base': None, 'angles': [(0, 1), (1, 4)]},
                             {'kind': 'spoke', 'base': (0, 5, 3, 2), 'angles': [(0, 1), (-1, 1)]}],
               'free': []}
    run_template('n4_onaxis2+spoke2', '(1,1,1)', ([('onaxis', 2), ('spoke', 2)], 0),
                 183, n_random_free=8, start_genomes=[seed183], rng=rng)
    run_template('n4_onaxis1+spoke3', '(1,1,1)', ([('onaxis', 1), ('spoke', 3)], 0),
                 183, n_random_free=8, rng=rng)
    run_template('n4_onaxis3+spoke1', '(1,1,1)', ([('onaxis', 3), ('spoke', 1)], 0),
                 183, n_random_free=8, rng=rng)
    run_template('n4_spoke4_axis001', '(0,0,1)', ([('spoke', 4)], 0), 183,
                 n_random_free=8, rng=rng)
    # non-clustered control: n=4 fully free/independent cubes (no shared axis)
    run_template('n4_control_4free', '(1,1,1)', ([], 4), 183,
                 n_random_free=10, n_random_locked=0, rng=rng)

    print('########## n=5 templates (record 393) ##########', flush=True)
    run_template('n5_onaxis2+spoke3', '(1,1,1)', ([('onaxis', 2), ('spoke', 3)], 0),
                 393, n_random_free=8, rng=rng)
    run_template('n5_onaxis1+spoke4', '(1,1,1)', ([('onaxis', 1), ('spoke', 4)], 0),
                 393, n_random_free=8, rng=rng)
    seed393 = {'axis_name': '(1,1,1)',
               'clusters': [{'kind': 'spoke', 'base': (4, 1, 1, -1),
                              'angles': [(0, 1), (1, 1), (-1, 1)]},
                             {'kind': 'onaxis', 'base': None, 'angles': [(1, 2), (1, 1)]}],
               'free': []}
    run_template('n5_spoke3+onaxis2(723sub)', '(1,1,1)',
                 ([('spoke', 3), ('onaxis', 2)], 0), 393, n_random_free=8,
                 start_genomes=[seed393], rng=rng)
    run_template('n5_onaxis1+spoke3+free1', '(1,1,1)',
                 ([('onaxis', 1), ('spoke', 3)], 1), 393, n_random_free=8, rng=rng)
    run_template('n5_control_5free', '(1,1,1)', ([], 5), 393,
                 n_random_free=10, n_random_locked=0, rng=rng)

    print('########## n=6 templates (record 723) ##########', flush=True)
    seed723 = {'axis_name': '(1,1,1)',
               'clusters': [{'kind': 'spoke', 'base': (4, 1, 1, -1),
                              'angles': [(0, 1), (1, 1), (-1, 1)]},
                             {'kind': 'onaxis', 'base': None,
                              'angles': [(1, 2), (1, 1), (2, 5)]}],
               'free': []}
    run_template('n6_spoke3+onaxis3(=723)', '(1,1,1)',
                 ([('spoke', 3), ('onaxis', 3)], 0), 723, n_random_free=8,
                 start_genomes=[seed723], rng=rng)
    run_template('n6_onaxis1+spoke3+free2', '(1,1,1)',
                 ([('onaxis', 1), ('spoke', 3)], 2), 723, n_random_free=8, rng=rng)
    run_template('n6_onaxis1+spoke4+free1', '(1,1,1)',
                 ([('onaxis', 1), ('spoke', 4)], 1), 723, n_random_free=8, rng=rng)
    run_template('n6_spoke3+spoke3(twoclusters)', '(1,1,1)',
                 ([('spoke', 3), ('spoke', 3)], 0), 723, n_random_free=8, rng=rng)
    run_template('n6_onaxis2+spoke4', '(1,1,1)',
                 ([('onaxis', 2), ('spoke', 4)], 0), 723, n_random_free=8, rng=rng)
    run_template('n6_control_6free', '(1,1,1)', ([], 6), 723,
                 n_random_free=10, n_random_locked=0, rng=rng)

    dt = time.time() - t0
    print(f'\nTotal wall time: {dt:.0f}s', flush=True)
    write_report(gates, dt)
    print(f'Report -> {REPORT_PATH}', flush=True)


def write_report(gates, dt):
    L = []
    L.append('# Shared-axis flexible-spoke search report\n')
    L.append('Working principles: this file\'s own docstring; PROJECT.md; '
             'six_cube_search_results.md Postscripts 12/16/17/17-addendum. '
             'Generated by shared_axis_search.py.\n')

    L.append('## Gate: does the family CONTAIN the records?\n')
    L.append(f'- 183 (n=4): reconstructed EXACTLY as axis(1,1,1), '
             f'on-axis cluster {{(0,1),(1,4)}} + spoke cluster '
             f'base=(0,5,3,2) {{(0,1),(-1,1)}} -> total={gates["gate183"]} '
             f'{"PASS" if gates["gate183"]==183 else "FAIL"}.')
    L.append(f'- 723 (n=6): reconstructed EXACTLY as axis(1,1,1), spoke '
             f'cluster base=(4,1,1,-1) {{(0,1),(1,1),(-1,1)}} (the exact C3 '
             f'orbit) + on-axis cluster {{(1,2),(1,1),(2,5)}} -> '
             f'total={gates["gate723"]} {"PASS" if gates["gate723"]==723 else "FAIL"}.')
    L.append('- **Structural finding from the gate itself**: both records '
             'already mix ONE fully group-locked cluster with ONE cluster '
             'that is only PARTLY or NOT AT ALL at a group-special angle '
             '(183\'s on-axis pair is free at 1/4; 723\'s on-axis triple is '
             'free at 1/2 and 2/5, only its middle member at the C3 angle '
             '1/1). The records were already living in the flexible part '
             'of this family before this search ever ran.\n')

    L.append('## Per-template results (LOCKED control vs FREE search)\n')
    L.append('| template | axis | record | locked best | free best | vs record | evals |')
    L.append('|---|---|---|---|---|---|---|')
    for tag, r in ALL_RESULTS.items():
        fb = r['free_best']
        cmp = ('BEATS' if fb and fb > r['record'] else
               ('TIES' if fb == r['record'] else
                (f'{fb - r["record"]:+d}' if fb is not None and fb >= 0 else '?')))
        L.append(f'| {tag} | {r["axis"]} | {r["record"]} | {r["locked_best"]} | '
                 f'{fb} | {cmp} | {r["evals"]} |')
    L.append('')

    L.append('## Records beaten or tied\n')
    beats = [(tag, r) for tag, r in ALL_RESULTS.items()
             if r['free_best'] and r['free_best'] >= r['record']]
    if beats:
        for tag, r in beats:
            cfg = genome_config2(r['free_genome'])
            L.append(f'- [{tag}] total={r["free_best"]} (record {r["record"]}) '
                     f'quats={cfg}')
    else:
        L.append('None. No free-search result reached its template\'s record '
                 '(183 / 393 / 723) from these templates and this evaluation '
                 'budget.')
    L.append('')

    L.append('## Verdict\n')
    n4 = [r for t, r in ALL_RESULTS.items() if t.startswith('n4_') and 'control' not in t]
    n5 = [r for t, r in ALL_RESULTS.items() if t.startswith('n5_') and 'control' not in t]
    n6 = [r for t, r in ALL_RESULTS.items() if t.startswith('n6_') and 'control' not in t]
    n4c = ALL_RESULTS.get('n4_control_4free')
    n5c = ALL_RESULTS.get('n5_control_5free')
    n6c = ALL_RESULTS.get('n6_control_6free')

    def best_of(rs):
        vals = [r['free_best'] for r in rs if r['free_best'] is not None]
        return max(vals) if vals else None

    b4, b5, b6 = best_of(n4), best_of(n5), best_of(n6)
    L.append(f'- Best FREE (clustered) result reached: n=4 {b4} (record 183), '
             f'n=5 {b5} (record 393), n=6 {b6} (record 723).')
    if n4c:
        L.append(f'- n=4 non-clustered control (4 fully free cubes, same evals '
                 f'budget): {n4c["free_best"]}.')
    if n5c:
        L.append(f'- n=5 non-clustered control (5 fully free cubes): {n5c["free_best"]}.')
    if n6c:
        L.append(f'- n=6 non-clustered control (6 fully free cubes): {n6c["free_best"]}.')
    L.append(f'- Total wall time: {dt:.0f}s.')
    with open(REPORT_PATH, 'w') as f:
        f.write('\n'.join(L) + '\n')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'gates':
        run_gates()
    else:
        main()
