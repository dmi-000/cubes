#!/usr/bin/env python3
"""The glue lemma, checked locally and exhaustively.  [P422]

The glue lemma (P422) says patches of two sharing classes can merge only along an edge of a cube
that belongs to BOTH classes. Here is an independent, computer-assisted check of the local
statement. It is a second argument beside the great-circle algebra.

**Local statement.**
- At a point of a glue arc, Γ's tie set around it is the whole circle (the point is interior to
  Γ°).
- Both classes' shared points are owned by tying cubes: `s` of one class, `t` of the other.
- **If no cube owns both `s` and `t`, Γ is never the whole circle there.**

**Which patterns.**
- Disjoint classes with at least two cubes each need all four cubes: `s` owned by {a, b}, `t` by
  {c, d}, all four tying. That is also the only vertex kind where Γ's tie set involves both.
- Each cube may own one more point, `θ` from its first (θ in (120°, 180°]). Second points may be
  shared, subject to the structure rules (`lowend_check.realisable`).
- Positions are affine in (offset of `t`, θ). Every cell of the coincidence arrangement is
  sampled, as in residue_exact.

**Positive control.** The hub pattern must make Γ the whole circle in some cell; that is its
interior glue. There `a` owns both: a = {s, t}, b = {s}, c = {t}, d inner.

Output: data/glue_check.json.
"""
import os, sys, json, itertools, collections
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from residue_exact import (cd, critical, placements, samples, evalf, CUBES, INF, NEG, set_partitions)
from lowend_check import realisable

ROOT = os.path.dirname(os.path.dirname(HERE))


def gamma_whole(pts, outer):
    allpts = sorted({p % 360 for ps in pts.values() for p in ps})
    crit = critical(allpts)
    n = len(crit)
    mids = [((crit[i] + (crit[(i + 1) % n] if i + 1 < n else crit[0] + 360)) / 2) % 360 for i in range(n)]
    def dist(x, w):
        if x in pts:
            return min(cd(w, p) for p in pts[x])
        return INF if x in outer else NEG
    def tie(w):
        ds = sorted((dist(x, w) for x in CUBES), reverse=True)
        return ds[1] == ds[2]
    return all(tie(c) for c in crit) and all(tie(m) for m in mids)


def patterns():
    """owners: list of frozensets; label 0 = s (owned by a, b), label 1 = t (owned by c, d)"""
    seen = set()
    for extra in itertools.product([0, 1], repeat=4):           # which cubes have a second point
        slots = [x for x, e in zip(CUBES, extra) if e]
        for part in set_partitions(slots):
            owners = [frozenset('ab'), frozenset('cd')] + [frozenset(b) for b in part]
            if any(len(set(b)) != len(b) for b in part):
                continue
            if any(len(o1 & o2) > 1 for o1, o2 in itertools.combinations(owners, 2)):
                continue
            classes = sorted({''.join(sorted(o)) for o in owners if len(o) >= 2})
            if not realisable(classes):
                continue
            key = tuple(sorted(tuple(sorted(o)) for o in owners))
            if key in seen:
                continue
            seen.add(key)
            yield owners


def run(owners, outer, T):
    st = collections.Counter()
    for forms, params in placements(T, owners, False):
        for vals in samples(forms, params):
            if 't' in vals and not (Fr(120) < vals['t'] <= 180):
                st['out_of_domain'] += 1
                continue
            pos = {i: evalf(f, vals) % 360 for i, f in forms.items()}
            if len(set(pos.values())) < len(pos):
                st['points_coincide'] += 1
                continue
            pts = {x: [pos[i] for i in pos if x in owners[i]] for x in T}
            st['GAMMA_WHOLE' if gamma_whole(pts, outer) else 'not_whole'] += 1
    return st


def main():
    total = collections.Counter()
    bad = []
    npat = 0
    for owners in patterns():
        npat += 1
        st = run(owners, set(), list(CUBES))
        total.update(st)
        if st['GAMMA_WHOLE']:
            bad.append({'owners': [''.join(sorted(o)) for o in owners], 'stats': dict(st)})
    print('disjoint-class patterns: %d; cell samples %s' % (npat, dict(total)))
    print('patterns where Γ is the whole circle (would refute the lemma): %d' % len(bad))
    for b in bad[:10]:
        print('  ', b)
    # positive control: the hub, a owns both s and t
    ctrl = run([frozenset('ab'), frozenset('ac')], set(), list('abc'))
    print('control (hub a={s,t}, b={s}, c={t}, d inner): %s' % dict(ctrl))
    assert ctrl['GAMMA_WHOLE'] > 0, 'control failed'
    json.dump({'patterns': npat, 'samples': dict(total), 'refuting': bad, 'control': dict(ctrl)},
              open(os.path.join(ROOT, 'data', 'glue_check.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
