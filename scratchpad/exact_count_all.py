#!/usr/bin/env python3
"""End-to-end: parse WL sweep jsonl output(s), classify field per solution,
dedupe, exact-count every rational / single-quadratic candidate, and print
a results table + write resonance4_results.jsonl records."""
import json
import re
import subprocess
import sys
from fractions import Fraction as Fr

sys.path.insert(0, '/Users/dmi/carroll')
sys.path.insert(0, '.')

import sympy as sp
from parse_results import stream_json_objects, wl_to_sympy, classify_field
from resonance4_solve import make_qd, rel_matrix_field, exact_count_field
from golden_rotations import Rot
import nfamily_common as nc


def build_ident(Field):
    return Rot([[Field(1), Field(0), Field(0)],
                [Field(0), Field(1), Field(0)],
                [Field(0), Field(0), Field(1)]])


def quad_to_field_elem(Field, coeff_pair):
    a, b = coeff_pair
    return Field(a, b)


def dedupe_key_quad(o, kind, info):
    """Congruence-agnostic-ish fingerprint: rounded psi + sorted rounded
    theta triple (mod 360), plus field kind/d. Good enough for a first
    pass; exact dedupe by invariant is done downstream only for survivors."""
    psi = round(float(o['psiDeg']) % 90, 4)
    ts = tuple(sorted(round(float(o[k]) % 360, 4) for k in ('t2Deg', 't3Deg', 't4Deg')))
    return (kind, info.get('d'), psi, ts)


def rational_quats(vals):
    """vals: dict of sympy Rational for c2,s2,c3,s3,c4,s4,cP,sP. Build the
    4 Rel-gauge matrices exactly via nfamily_common and return int quats,
    or None if the round-trip / cap fails."""
    def fr(x):
        r = sp.nsimplify(x)
        return Fr(int(r.p), int(r.q)) if r.is_Rational else None

    cP, sP = fr(vals['cP']), fr(vals['sP'])
    if cP is None or sP is None:
        return None
    psi = nc.PyAngle(cP, sP)
    thetas = [nc.IDENTITY_ANGLE]
    for cN, sN in ((vals['c2'], vals['s2']), (vals['c3'], vals['s3']), (vals['c4'], vals['s4'])):
        c, s = fr(cN), fr(sN)
        if c is None or s is None:
            return None
        thetas.append(nc.PyAngle(c, s))
    try:
        quats, mats = nc.build_family_quats(psi, thetas, cap=4000)
    except (AssertionError, ValueError):
        return None
    return quats


def run_cpp(quats):
    qstr = ';'.join(','.join(str(x) for x in q) for q in quats)
    out = subprocess.run(['/Users/dmi/carroll/cube_regions_n', '--n', '4', '--quats', qstr],
                          capture_output=True, text=True, timeout=60)
    return out.stdout


def main(paths, do_quad=True, do_rational=True, limit=None):
    objs = []
    for p in paths:
        objs.extend(stream_json_objects(p))
    ok = [o for o in objs if o.get('status') != 'timeout_or_fail' and 'c2' in o]
    print(f'{len(ok)} raw solutions from {len(paths)} file(s)', flush=True)

    parsed = {}
    for o in ok:
        try:
            vals = {k: wl_to_sympy(o[k]) for k in ('c2', 's2', 'c3', 's3', 'c4', 's4', 'cP', 'sP')}
        except Exception:
            continue
        kind, info = classify_field(vals)
        if kind not in ('rational', 'quad'):
            continue
        psi = float(o['psiDeg']) % 90
        if psi <= 0.5 or psi >= 89.5:
            continue
        key = dedupe_key_quad(o, kind, info)
        if key not in parsed:
            parsed[key] = (o, vals, kind, info)
    items = list(parsed.values())
    print(f'{len(items)} unique candidates (kind in rational/quad) after fingerprint dedupe', flush=True)
    if limit:
        items = items[:limit]

    results = []
    for idx, (o, vals, kind, info) in enumerate(items):
        try:
            if kind == 'rational':
                quats = rational_quats(vals)
                if quats is None:
                    results.append({'kind': 'rational', 'status': 'quat_fail', 'meta': o})
                    continue
                out = run_cpp(quats)
                total, by_depth = None, None
                try:
                    j = json.loads(out.strip().splitlines()[-1])
                    total = j.get('bounded')
                    by_depth = j.get('by_depth')
                except Exception:
                    pass
                results.append({'kind': 'rational', 'total': total, 'by_depth': by_depth, 'quats': quats,
                                 'psiDeg': o['psiDeg'], 'subset': o['subset'], 'type': o['type'],
                                 'raw_out': out.strip()[-500:]})
                print(f'[{idx}] RATIONAL total={total} psi={o["psiDeg"]:.3f} subset={o["subset"]} type={o["type"]}', flush=True)
            elif kind == 'quad':
                d = info['d']
                Field = make_qd(d)
                coeffs = info['coeffs']
                IDENT = build_ident(Field)
                def mk(cn, sn):
                    return quad_to_field_elem(Field, coeffs[cn]), quad_to_field_elem(Field, coeffs[sn])
                cP, sP = mk('cP', 'sP')
                mats = [IDENT]
                for cn, sn in (('c2', 's2'), ('c3', 's3'), ('c4', 's4')):
                    c, s = mk(cn, sn)
                    mats.append(rel_matrix_field(Field, c, s, cP, sP))
                total, bd = exact_count_field(mats, Field)
                results.append({'kind': 'quad', 'd': d, 'total': total, 'by_depth': bd,
                                 'psiDeg': o['psiDeg'], 'subset': o['subset'], 'type': o['type']})
                print(f'[{idx}] QUAD d={d} total={total} bd={bd} psi={o["psiDeg"]:.3f} '
                      f'subset={o["subset"]} type={o["type"]}', flush=True)
        except Exception as e:
            print(f'[{idx}] ERROR {kind}: {e}', flush=True)
            results.append({'kind': kind, 'status': 'error', 'err': str(e)[:200], 'meta': {'subset': o['subset'], 'type': o['type'], 'psiDeg': o['psiDeg']}})

    with open('exact_results.json', 'w') as f:
        json.dump(results, f, indent=1, default=str)
    tots = [r['total'] for r in results if r.get('total') is not None]
    print(f'\nDONE. {len(results)} attempted, {len(tots)} with a total.')
    if tots:
        print('max total found:', max(tots))
    return results


if __name__ == '__main__':
    paths = sys.argv[1:] or ['uniform_k4_results.jsonl']
    main(paths)
