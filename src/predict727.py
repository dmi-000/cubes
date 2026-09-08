#!/usr/bin/env python3
"""Estimate the 727 chamber count from the remaining walls, by exact sampling.

WHY.  At stage 25 of 27 the enumeration holds 2 981 760 chambers and the two
remaining walls decide everything between 2 981 760 (no split) and 11 927 040
(both double).  Each wall's effect is the SPLIT FRACTION -- what proportion of
current chambers the new hyperplane passes through -- and that is a proportion,
which sampling estimates honestly, unlike a count, which it does not.

THE PREDICATE IS EXACT.  Each sampled chamber is decided by two
`feasible_strict` calls, the same Farkas test the enumerator uses; no chamber is
approximated.  What is sampled is WHICH chambers get tested, so the reported
figure is an interval on a proportion, and the derived totals are labelled
estimates.  A sampled count would be a lower bound; a sampled proportion with a
stated interval is a measurement.

UNIFORMITY, and why the obvious shortcut is wrong.  Wall 27 acts on stage-26
chambers, which do not exist on disk yet.  They are generated here from sampled
stage-25 parents.  Each parent yields one or two children, so "sample parents,
keep all their children" does NOT oversample: a given stage-26 chamber is
included exactly when its unique parent is drawn, so every child carries the
same inclusion probability.  Taking a fixed number of CHILDREN instead would
have been size-biased toward parents that split.
"""
import json, os, random, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from growth727 import walls_of, BASE
from exactlp import feasible_strict
from pstream_chambers import _stage_paths, _sv_read_many

DEFAULTS = {'n': 600, 'seed': 20260822, 'stage': 25}


def _wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    cfg = dict(DEFAULTS)
    for a in sys.argv[1:]:
        k, v = a.split('=', 1)
        cfg[k] = type(DEFAULTS[k])(v)
    W, ncols = walls_of(BASE + [(7, 14, 1, -5)])
    st = int(cfg['stage'])
    paths = _stage_paths(os.path.join(HERE, 'stream_727'), st)
    if paths is None:
        raise SystemExit('stage %d not complete on disk' % st)

    total = sum(1 for _ in _sv_read_many(paths))
    rnd = random.Random(cfg['seed'])
    idx = set(rnd.sample(range(total), min(int(cfg['n']), total)))
    sample = [sv for i, sv in enumerate(_sv_read_many(paths)) if i in idx]
    print('stage %d holds %s chambers; sampled %d' %
          (st, '{:,}'.format(total), len(sample)), flush=True)

    def children(sv, wall_index):
        w = W[wall_index]
        rows = [[s * W[j][t] for t in range(ncols)] for j, s in enumerate(sv)]
        out = []
        if feasible_strict(rows + [[w[t] for t in range(ncols)]], ncols) is not None:
            out.append(sv + (1,))
        if feasible_strict(rows + [[-w[t] for t in range(ncols)]], ncols) is not None:
            out.append(sv + (-1,))
        return out

    t0 = time.time()
    kids26, split26 = [], 0
    for sv in sample:
        c = children(sv, st)                 # wall index st (0-based) = wall st+1
        if len(c) == 2:
            split26 += 1
        kids26.extend(c)
    lo, hi = _wilson(split26, len(sample))
    est26 = total * (1 + split26 / len(sample))
    print('wall %d: split %d/%d = %.4f  [%.4f, %.4f]  -> stage %d approx {:,.0f}'
          .format(int(est26)) % (st + 1, split26, len(sample),
                                 split26 / len(sample), lo, hi, st + 1), flush=True)

    split27 = 0
    for sv in kids26:
        if len(children(sv, st + 1)) == 2:
            split27 += 1
    lo7, hi7 = _wilson(split27, len(kids26))
    est27 = est26 * (1 + split27 / len(kids26))
    print('wall %d: split %d/%d = %.4f  [%.4f, %.4f]  -> stage %d approx {:,.0f}'
          .format(int(est27)) % (st + 2, split27, len(kids26),
                                 split27 / len(kids26), lo7, hi7, st + 2), flush=True)

    lo_tot = total * (1 + lo) * (1 + lo7)
    hi_tot = total * (1 + hi) * (1 + hi7)
    out = {'stage': st, 'stage_count': total, 'n_sampled': len(sample),
           'wall26_split': split26, 'wall26_ci': [lo, hi],
           'n_children26': len(kids26), 'wall27_split': split27,
           'wall27_ci': [lo7, hi7],
           'estimate_total': est27, 'ci_total': [lo_tot, hi_tot],
           'hard_ceiling': total * 4, 'wall_s': time.time() - t0}
    json.dump(out, open(os.path.join(HERE, 'predict727_report.json'), 'w'), indent=1)
    print('\nESTIMATED 727 CHAMBERS: {:,.0f}   95% CI [{:,.0f}, {:,.0f}]'
          .format(est27, lo_tot, hi_tot))
    print('hard ceiling (both walls double): {:,}'.format(total * 4))
    print('%.0fs' % (time.time() - t0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
