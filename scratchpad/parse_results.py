#!/usr/bin/env python3
"""Parse the (possibly pretty-printed, concatenated) JSON records emitted
by sweep_uniform.wl / sweep_mixed.wl, classify each real solution's field
(rational / single Q(sqrt d) / messy-higher), dedupe by congruence
fingerprint, and emit a clean summary."""
import json
import math
import re
import sys
from fractions import Fraction as Fr

import sympy as sp


def stream_json_objects(path):
    with open(path) as f:
        text = f.read()
    # WL's N[...] sometimes prints "0.e-57" style (no digit before 'e'),
    # which is not valid JSON number syntax -- patch it.
    text = re.sub(r'(\d)\.e', r'\1.0e', text)
    dec = json.JSONDecoder()
    i = 0
    n = len(text)
    out = []
    while i < n:
        while i < n and text[i] in ' \t\n\r':
            i += 1
        if i >= n:
            break
        obj, j = dec.raw_decode(text, i)
        out.append(obj)
        i = j
    return out


def wl_to_sympy(s):
    """Convert a Mathematica InputForm string (Sqrt[..], ^, fractions with
    escaped slashes) into a sympy expression."""
    s = s.replace('\\/', '/')
    s = s.replace('^', '**')
    # Sqrt[...] -> sqrt(...), need bracket matching since nested
    def repl_sqrt(s):
        out = []
        i = 0
        while i < len(s):
            if s[i:i+5] == 'Sqrt[':
                depth = 1
                j = i + 5
                while j < len(s) and depth > 0:
                    if s[j] == '[':
                        depth += 1
                    elif s[j] == ']':
                        depth -= 1
                    j += 1
                inner = repl_sqrt(s[i+5:j-1])
                out.append(f'sqrt({inner})')
                i = j
            else:
                out.append(s[i])
                i += 1
        return ''.join(out)
    s = repl_sqrt(s)
    return sp.sympify(s)


def classify_field(vals):
    """vals: dict name->sympy expr. Returns (kind, info).
    kind in {'rational','quad','messy'}."""
    all_syms = set()
    for v in vals.values():
        all_syms |= v.free_symbols
    sqrt_atoms = set()
    messy = False
    for v in vals.values():
        for a in sp.preorder_traversal(v):
            if a.is_Pow and a.exp == sp.Rational(1, 2):
                base = a.base
                if base.is_Integer:
                    sqrt_atoms.add(int(base))
                else:
                    messy = True
    if not sqrt_atoms:
        return 'rational', {}
    if messy or len(sqrt_atoms) != 1:
        return 'messy', {'sqrt_atoms': sorted(sqrt_atoms), 'messy_nested': messy}
    d = next(iter(sqrt_atoms))
    # squarefree-reduce d
    dd = d
    k = 2
    mult = 1
    while k * k <= dd:
        while dd % (k * k) == 0:
            dd //= (k * k)
            mult *= k
        k += 1
    # verify each value is expressible as a + b*sqrt(d) cleanly
    y = sp.symbols('y_tmp')
    coeffs = {}
    for name, v in vals.items():
        vv = v.subs(sp.sqrt(d), y)
        if vv.has(sp.sqrt(d)) or vv.has(sp.sqrt):
            return 'messy', {'sqrt_atoms': [d], 'reason': f'{name} not linear in sqrt({d})'}
        poly = sp.Poly(vv, y) if vv.free_symbols == {y} or vv.is_number else None
        try:
            poly = sp.Poly(sp.expand(vv), y)
        except sp.PolynomialError:
            return 'messy', {'sqrt_atoms': [d], 'reason': f'{name} poly-fail'}
        cs = poly.all_coeffs()[::-1]
        a0 = cs[0] if len(cs) > 0 else sp.Integer(0)
        b0 = cs[1] if len(cs) > 1 else sp.Integer(0)
        if len(cs) > 2:
            return 'messy', {'sqrt_atoms': [d], 'reason': f'{name} degree>1 in sqrt'}
        coeffs[name] = (Fr(a0.p, a0.q) if a0.is_Rational else Fr(int(a0)),
                         Fr(b0.p, b0.q) if b0.is_Rational else Fr(int(b0)))
    return 'quad', {'d': d, 'coeffs': coeffs}


def process_file(path):
    objs = stream_json_objects(path)
    ok = [o for o in objs if o.get('status') != 'timeout_or_fail' and 'c2' in o]
    fails = [o for o in objs if o.get('status') == 'timeout_or_fail']
    print(f'{path}: {len(objs)} records, {len(ok)} solutions, {len(fails)} timeout/fail systems')
    kinds = {}
    parsed = []
    for o in ok:
        try:
            vals = {k: wl_to_sympy(o[k]) for k in ('c2', 's2', 'c3', 's3', 'c4', 's4', 'cP', 'sP')}
        except Exception as e:
            kinds['unparseable_root'] = kinds.get('unparseable_root', 0) + 1
            parsed.append((o, None, 'unparseable_root', {'err': str(e)[:80]}))
            continue
        kind, info = classify_field(vals)
        kinds[kind] = kinds.get(kind, 0) + 1
        parsed.append((o, vals, kind, info))
    print('field kinds:', kinds)
    return parsed, fails


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'uniform_k4_results.jsonl'
    parsed, fails = process_file(path)
    for o, vals, kind, info in parsed[:5]:
        print(o['subset'], o['type'], kind, info if kind != 'rational' else '', 'psi=', o['psiDeg'])
