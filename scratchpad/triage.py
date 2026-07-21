#!/usr/bin/env python3
"""Fast float triage: for every solution in the jsonl sweep outputs, build
the 4 Rel-gauge rotation matrices numerically from (t2,t3,t4,psi) degrees,
dedupe by a rounded congruence-ish fingerprint, and rank by an approximate
voxel region count (six_cube_search.count_mats, read-only reference code)
at a modest resolution. This is TRIAGE ONLY -- not a certified count."""
import json
import math
import re
import sys
import numpy as np

sys.path.insert(0, '/Users/dmi/carroll')
from six_cube_search import count_mats


def stream_json_objects(path):
    with open(path) as f:
        text = f.read()
    text = re.sub(r'(\d)\.e', r'\1.0e', text)
    dec = json.JSONDecoder()
    i, n, out = 0, len(text), []
    while i < n:
        while i < n and text[i] in ' \t\n\r':
            i += 1
        if i >= n:
            break
        obj, j = dec.raw_decode(text, i)
        out.append(obj)
        i = j
    return out


def rel_matrix_np(delta_deg, psi_deg):
    D = math.radians(delta_deg)
    P = math.radians(psi_deg)
    cD, sD, cP, sP = math.cos(D), math.sin(D), math.cos(P), math.sin(P)
    return np.array([
        [cD*cP*cP+sP*sP, cP*sP*(1-cD), cP*sD],
        [cP*sP*(1-cD), cD*sP*sP+cP*cP, -sD*sP],
        [-cP*sD, sD*sP, cD],
    ])


def build_mats(t2, t3, t4, psi):
    return [np.eye(3), rel_matrix_np(t2, psi), rel_matrix_np(t3, psi), rel_matrix_np(t4, psi)]


def fingerprint(o, ndigits=3):
    psi = round(float(o['psiDeg']) % 90, ndigits)
    ts = sorted(round(float(o[k]) % 360, ndigits) for k in ('t2Deg', 't3Deg', 't4Deg'))
    return (psi, tuple(ts))


def main(paths, R=120, top=40):
    objs = []
    for p in paths:
        objs.extend(stream_json_objects(p))
    ok = [o for o in objs if o.get('status') != 'timeout_or_fail' and 't2Deg' in o]
    print(f'{len(ok)} solutions loaded from {len(paths)} file(s)')
    seen = {}
    for o in ok:
        fp = fingerprint(o)
        if fp not in seen:
            seen[fp] = o
    uniq = list(seen.values())
    print(f'{len(uniq)} unique (psi, theta-multiset) fingerprints')

    scored = []
    for o in uniq:
        t2, t3, t4, psi = o['t2Deg'], o['t3Deg'], o['t4Deg'], o['psiDeg']
        psi = float(psi)
        if psi <= 0.5 or psi >= 89.5:
            continue  # degenerate shared-axis
        mats = build_mats(float(t2), float(t3), float(t4), psi)
        try:
            tot, bd, *_ = count_mats(mats, R, verbose=False)
        except Exception as e:
            continue
        scored.append((tot, o, bd))
    scored.sort(key=lambda x: -x[0])
    print(f'{len(scored)} scored (non-degenerate).')
    print('\ntop candidates by approx voxel total:')
    for tot, o, bd in scored[:top]:
        print(f'  total~{tot:4d}  psi={float(o["psiDeg"]):8.4f}  t2={float(o["t2Deg"]):9.4f} '
              f't3={float(o["t3Deg"]):9.4f} t4={float(o["t4Deg"]):9.4f}  subset={o["subset"]} type={o["type"]}')
    return scored


if __name__ == '__main__':
    paths = sys.argv[1:] or ['uniform_k4_results.jsonl']
    main(paths)
