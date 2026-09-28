#!/usr/bin/env python3
"""Outline of each 1217 sheet in its own (t, u) plane, from the walls themselves.  [P394]

`n7_two_sheets.py` found each sheet bounded by three walls: the branch's lower 727 wall (left), a
flat fibre wall (top), and P301's third wall (lower right), whose root matched the measured
boundary on 33 of 34 lines.  This evaluates the third wall EXACTLY on dense vertical lines, via
`wall_keys.on_line`, and finds the two corners as roots of the same polynomial:
    top-right    third wall on the horizontal line u = u_top
    bottom-left  third wall on the vertical line t = t_left
u_top and D2's t_left are brackets from `n7_two_sheets.py` (width ~5e-10 and ~6e-9); the corner
is computed at the bracket's midpoint and so inherits that width.  The figure is drawn from this.

GATE: every measured vertical-line boundary in data/n7_two_sheets.json that is not on a seam must
equal the third-wall root on its line to 2e-6.
"""
import sys, os, json
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..')); sys.path.insert(0, HERE)
import sympy as sp
import n7_two_sheets as S, wall_keys as W

ROOT = os.path.dirname(os.path.dirname(HERE))
T = sp.Symbol('s')


def main():
    q0, pt = S.setup()
    L = json.load(open(os.path.join(ROOT, 'data', 'n7_two_sheets.json')))['lines']
    tw = json.load(open(os.path.join(ROOT, 'data', 'plateau_1217.json')))['third_wall']
    key = {'frame': tw['frame'], 'group': tuple(tuple(g) for g in tw['group']),
           'sig': tuple(tw['sig']), 'c0': tw['c0']}
    mid = lambda k: (F(L[k]['inside']) + F(L[k]['outside'])) / 2
    u_top = mid('D1|t=0|u+')
    t_left = {'D1': F(-2, 19), 'D2': -mid('D2|u=0|t-')}

    def roots(p0, d, lo, hi):
        co = W.on_line(key, q0, p0, d)
        P = sp.Poly([sp.Rational(x) for x in reversed(co)], T)
        return sorted(float(r) for r in sp.real_roots(P) if lo < float(r) < hi)

    e15 = [F(0)] * len(pt); e15[15] = F(1)
    out = {'what': 'outline of each 1217 sheet in its (t, u) plane [P394]', 'u_top': float(u_top),
           'seams': {'both': 'u = -1/36 (count 1215 on the line)', 'D2': 't = -3/31 (count 1213 on the line)'},
           'crossing_segment': None, 'sheets': {}}
    for b in ('D1', 'D2'):
        bd = S.vec(len(pt), b)
        # top-right corner: third wall along u = u_top, positive t
        tr = roots(S.at(pt, F(0), u_top, b), bd, 0.0, 0.2)
        t_tr = tr[0]
        # bottom-left corner: third wall along t = t_left, below the record
        bl = roots(S.at(pt, t_left[b], F(0), b), e15, -0.2, 0.0)
        u_bl = bl[-1]
        # dense curve
        n = 60
        curve = []
        for i in range(n + 1):
            t = t_left[b] + (F(t_tr).limit_denominator(10 ** 9) - t_left[b]) * F(i, n)
            r = roots(S.at(pt, t, F(0), b), e15, -0.2, float(u_top) + 1e-9)
            curve.append([float(t), r[-1] if r else None])
        curve[0][1], curve[-1][1] = u_bl, float(u_top)
        # gate against the measured lines
        bad = []
        for k, v in L.items():
            if k.startswith(b + '|t=') and k.endswith('u-') and v['inside']:
                t = F(k.split('t=')[1].split('|')[0])
                m = -float(F(v['outside']))
                r = roots(S.at(pt, t, F(0), b), e15, -0.2, 0.01)
                if not r or abs(r[-1] - m) > 2e-6:
                    bad.append({'line': k, 'measured': m, 'wall_root': r[-1] if r else None})
        out['sheets'][b] = {'t_left': float(t_left[b]), 'corner_top_right': [t_tr, float(u_top)],
                            'corner_bottom_left': [float(t_left[b]), u_bl],
                            'third_wall_curve': curve, 'gate_mismatches': bad}
        print('%s  corners: bottom-left (%.6f, %.6f)  top-right (%.6f, %.7f)  gate mismatches %d %s'
              % (b, t_left[b], u_bl, t_tr, u_top, len(bad), [x['line'] for x in bad]), flush=True)
    r0 = roots(S.at(pt, F(0), F(0), 'D1'), e15, -0.2, 0.0)[-1]
    out['crossing_segment'] = {'t': 0, 'u': [r0, float(u_top)]}
    print('crossing segment over the record: u in (%.6f, %.7f)' % (r0, u_top))
    json.dump(out, open(os.path.join(ROOT, 'data', 'n7_sheet_outline.json'), 'w'), indent=1)
    print('wrote data/n7_sheet_outline.json')


if __name__ == '__main__':
    main()
