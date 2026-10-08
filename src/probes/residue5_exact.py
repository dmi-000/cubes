#!/usr/bin/env python3
"""H1 at multi-shared vertices for n = 5, settled exactly on the residue u <= 3.  [P439]

[P438]: with u >= 4 cubes owning an unshared point, H1 at the vertex follows from Check 1′ and
hand lemmas. This script settles every vertex with u <= 3 and two or more sharing pairs (or one
point with three or more owners) by exhaustion, as [P420]'s residue_exact.py did at n = 4.

1. **Patterns** come from residue5_patterns.py with UMAX = 3: every realisable owner pattern up to
   relabelling (200 patterns, 3 to 5 tying cubes).
2. **Placements.** Labels become affine forms in (θ, offsets). A cycle of links fixes θ to the
   finitely many solutions in [120, 180]; a corner fixes θ = 120. Placements that force two
   distinct labels together are dropped (they are another pattern).
3. **Cells.** The per-vertex slack depends only on the cyclic order, with ties, of the critical
   directions (points, antipodes, bisectors and their antipodes). That order changes only where two
   critical directions coincide, a linear condition in the parameters.
   - 0 and 1 parameters: every critical value and every midpoint.
   - 2 parameters: [P420]'s sampler, which visits every vertex, every edge midpoint, and a point
     off each edge on both sides at a SOLVED distance below that to any other line.
   - 3 parameters: slices at every critical value of the first parameter, meaning every
     coordinate of a triple intersection and every condition on it alone, plus the midpoints
     between consecutive ones. Each slice gets the 2-parameter sampler.
4. **Evaluation.** At each sample, the FULL per-vertex slack of H1′ (h1_shared_local.slack2:
   weights from the circle, whole graphs weigh 0) for every number c of cubes containing P,
   c = 0 … 5 − t. A sample where two labels coincide is evaluated as the configuration it is,
   provided no two cubes then co-own two points; otherwise it is skipped as unrealisable and
   counted.
5. **Cross-check** (as in [P420]). For each placement with parameters, every order type reached by
   random rational parameter values must appear among the cell samples' order types.

Output: data/residue5_exact.json. Any negative slack is printed: a counterexample to H1′.
"""
import os, sys, json, itertools, collections, random, time, multiprocessing as mp
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import residue5_patterns as RP
import residue_exact as RE
import h1_shared_local as HL

ROOT = os.path.dirname(os.path.dirname(HERE))
RP.UMAX = 3


def placements_forms(t, owners):
    """yield (forms, params): forms[label] = affine form {'1': const, 't': coeff, 'oK': 1}"""
    labels = list(range(len(owners)))
    cube_pts = {x: [i for i in labels if x in owners[i]] for x in range(t)}
    corner = any(len(v) == 3 for v in cube_pts.values())
    multi = [x for x in range(t) if len(cube_pts[x]) == 2]
    choices = []
    for x in range(t):
        ps = cube_pts[x]
        if len(ps) == 2:
            choices.append([(ps, s) for s in (1, -1)])
        elif len(ps) == 3:
            choices.append([(perm, 1) for perm in itertools.permutations(ps)])
        else:
            choices.append([(tuple(ps), 0)])
    seen = set()
    for combo in itertools.product(*choices):
        par = {i: (i, 0, Fr(0)) for i in labels}

        def find(i):
            p, c, d = par[i]
            if p == i:
                return i, 0, Fr(0)
            r, c2, d2 = find(p)
            par[i] = (r, c + c2, d + d2)
            return par[i]
        thetas, ok = None, True
        for ps, s in combo:
            if len(ps) == 2:
                links = [(ps[0], ps[1], s, Fr(0))]
            elif len(ps) == 3:
                links = [(ps[0], ps[1], 0, Fr(120)), (ps[0], ps[2], 0, Fr(-120))]
            else:
                links = []
            for a, b, c, d in links:
                ra, ca, da = find(a)
                rb, cb, db = find(b)
                if ra != rb:
                    par[rb] = (ra, ca + c - cb, da + d - db)
                else:
                    k, dd = ca + c - cb, da + d - db
                    if k == 0:
                        if dd % 360 != 0:
                            ok = False
                        continue
                    sols = {th for j in range(-10, 11) for th in [(Fr(360) * j - dd) / k] if 120 <= th <= 180}
                    thetas = sols if thetas is None else thetas & sols
                    if not thetas:
                        ok = False
        if not ok:
            continue
        if corner:
            thetas = {Fr(120)} if thetas is None else thetas & {Fr(120)}
            if not thetas:
                continue
        roots = sorted({find(i)[0] for i in labels})
        theta_opts = [None] if (thetas is None and multi) else sorted(thetas) if thetas else [None]
        for th in theta_opts:
            forms = {}
            for i in labels:
                r, c, d = find(i)
                f = {'1': d}
                ri = roots.index(r)
                if ri > 0:
                    f['o%d' % ri] = Fr(1)
                if c:
                    if th is None:
                        f['t'] = Fr(c)
                    else:
                        f['1'] = f['1'] + c * th
                forms[i] = f
            # distinct labels forced together: drop
            nf = [RE.norm({k: (v % 360 if k == '1' else v) for k, v in f.items()}) for f in forms.values()]
            if len(set(nf)) < len(nf):
                continue
            key = tuple(sorted(nf))
            if key in seen:
                continue
            seen.add(key)
            params = sorted({k for f in forms.values() for k in f if k != '1'})
            yield forms, params


def subst(forms, v, x):
    out = {}
    for i, f in forms.items():
        g = {k: c for k, c in f.items() if k != v}
        g['1'] = g.get('1', Fr(0)) + f.get(v, Fr(0)) * x
        out[i] = g
    return out


def samples3(forms, params):
    """3 parameters: slice the first one at every critical value and midpoint"""
    v = params[0]
    L = RE.lines(forms, params)
    box = []
    for j, p in enumerate(params):
        lo, hi = RE.dom(p)
        e = tuple(Fr(1) if k == j else Fr(0) for k in range(3))
        box += [(e, lo), (e, hi)]
    planes = sorted(set(L) | set(box))
    crit = set()
    lo, hi = RE.dom(v)
    crit |= {lo, hi}
    for coef, val in planes:
        if coef[1] == 0 and coef[2] == 0 and coef[0] != 0:
            crit.add(val / coef[0])
    for a, b, c in itertools.combinations(planes, 3):
        M = [a[0], b[0], c[0]]
        det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
               + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
        if det == 0:
            continue
        rhs = [a[1], b[1], c[1]]
        dx = (rhs[0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (rhs[1] * M[2][2] - M[1][2] * rhs[2])
              + M[0][2] * (rhs[1] * M[2][1] - M[1][1] * rhs[2]))
        x = dx / det
        if lo <= x <= hi:
            crit.add(x)
    xs = sorted(crit)
    for x in sorted(set(xs) | {(p + q) / 2 for p, q in zip(xs, xs[1:])}):
        sub = subst(forms, v, x)
        for s in RE.samples(sub, params[1:]):
            s = dict(s); s[v] = x
            yield s


def all_samples(forms, params):
    if len(params) <= 2:
        yield from RE.samples(forms, params)
    else:
        yield from samples3(forms, params)


def evaluate(t, owners, forms, vals):
    """twice-slack for each c, or a status string"""
    if 't' in vals and not (Fr(120) <= vals['t'] <= Fr(180)):
        return 'out_of_domain'
    pos = {i: RE.evalf(f, vals) % 360 for i, f in forms.items()}
    pts = {x: sorted({pos[i] for i in pos if x in owners[i]}) for x in range(t)}
    for x, y in itertools.combinations(range(t), 2):
        if len(set(pts[x]) & set(pts[y])) > 1:
            return 'unrealisable_merge'
    out = {}
    for c in range(0, 5 - t + 1):
        # cubes 0..t−1 tie; relabel so that C = {t, ..., t+c−1}
        C = set(range(t, t + c))
        s2, anom = HL.slack2({x: pts[x] for x in range(t)}, C)
        out[c] = (s2, tuple(sorted(anom)))
    return out


def run_pattern(args):
    t, owners = args
    res = {'t': t, 'owners': [sorted(o) for o in owners], 'placements': 0, 'samples': 0,
           'min': {}, 'fails': [], 'status': collections.Counter(), 'anomalies': collections.Counter(),
           'crosscheck_missed': 0, 'params': []}
    rnd = random.Random(sum(ord(ch) for ch in str(owners)))
    for forms, params in placements_forms(t, owners):
        res['placements'] += 1
        res['params'].append(len(params))
        cell_types = set()
        for vals in all_samples(forms, params):
            r = evaluate(t, owners, forms, vals)
            res['samples'] += 1
            if isinstance(r, str):
                res['status'][r] += 1
                continue
            if params:
                cell_types.add(RE.order_type(forms, vals))
            for c, (s2, an) in r.items():
                res['min'][c] = min(res['min'].get(c, 10 ** 9), s2)
                if an:
                    res['anomalies'][an] += 1
                if s2 < 0 and len(res['fails']) < 10:
                    res['fails'].append({'vals': {k: str(v) for k, v in vals.items()}, 'c': c, 'twice_slack': s2})
        if params:
            for _ in range(300):
                v = {p: (Fr(120 * 89 + rnd.randrange(0, 60 * 89 + 1), 89) if p == 't' else Fr(rnd.randrange(0, 360 * 97), 97))
                     for p in params}
                if RE.order_type(forms, v) not in cell_types:
                    pos = {i: RE.evalf(f, v) % 360 for i, f in forms.items()}
                    if len(set(pos.values())) == len(pos):
                        res['crosscheck_missed'] += 1
    res['status'] = dict(res['status']); res['anomalies'] = {str(k): v for k, v in res['anomalies'].items()}
    return res


def main():
    pats = [(t, owners) for t in range(3, 6) for owners, u in RP.patterns(t)]
    pats = [(t, o) for t, o in pats if any(True for _ in placements_forms(t, o))]
    dmax = {(t, str(o)): max(len(p) for f, p in placements_forms(t, o)) for t, o in pats}
    tag = ''
    if '--upto2' in sys.argv:
        pats = [(t, o) for t, o in pats if dmax[(t, str(o))] <= 2]; tag = '_upto2'
    elif '--only3' in sys.argv:
        pats = [(t, o) for t, o in pats if dmax[(t, str(o))] == 3]; tag = '_only3'
    print('%d patterns to evaluate' % len(pats), flush=True)
    t0 = time.time()
    with mp.Pool(8) as p:
        out = []
        for r in p.imap_unordered(run_pattern, pats):
            out.append(r)
            if r['fails'] or r['crosscheck_missed']:
                print('PATTERN', r['t'], r['owners'], 'fails', r['fails'][:2], 'crosscheck missed', r['crosscheck_missed'], flush=True)
    neg = [r for r in out if r['fails']]
    print('%d patterns, %d placements, %d samples in %.0f s; patterns with a negative slack: %d; cross-check misses: %d'
          % (len(out), sum(r['placements'] for r in out), sum(r['samples'] for r in out), time.time() - t0,
             len(neg), sum(r['crosscheck_missed'] for r in out)), flush=True)
    mins = collections.Counter()
    for r in out:
        for c, v in r['min'].items():
            mins[(r['t'], c, v)] += 1
    print('minimum twice-slack per (t, c): %s' % sorted({(t, c): min(v for (tt, cc, v) in mins if tt == t and cc == c)
                                                        for (t, c, _) in mins}.items()), flush=True)
    st = collections.Counter()
    for r in out:
        st.update(r['status'])
    print('skipped samples: %s' % dict(st), flush=True)
    json.dump(out, open(os.path.join(ROOT, 'data', 'residue5_exact%s.json' % tag), 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
