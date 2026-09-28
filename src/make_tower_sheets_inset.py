#!/usr/bin/env python3
"""The 1217 detail inset of TOWER_DIAGRAM.html: both sheets, each flat in its own (t, u) plane.  [P394]

Replaces the pentagon panel, whose bottom and right edges were the edges of a 5x5 grid's box, not
walls.  Drawn from data/n7_sheet_outline.json (`src/probes/n7_sheet_outline.py`): the third wall is
evaluated exactly on 61 lines per sheet, the corners are its roots on the other two walls.  Both
panels share one scale, and t and u are at the same scale, so shapes and sizes compare directly.
Colours are the page's CSS variables, so both themes work.
"""
import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = json.load(open(os.path.join(ROOT, 'data', 'n7_sheet_outline.json')))
T0, T1, U0, U1 = -0.145, 0.085, -0.118, 0.010
X0, W = 34, 256
K = W / (T1 - T0)                     # px per unit, t and u alike
PH = (U1 - U0) * K                    # panel height


def build():
    o = ['<svg viewBox="0 0 300 %d" role="img" aria-label="The two sheets of the 1217 plateau, each in its '
         'own plane, to one scale: a curved triangle bounded by its branch\'s lower 727 wall, a flat fibre wall '
         'on top, and one curved wall; the fibre segment over the record lies in both.">' % int(2 * PH + 150)]
    T = lambda x, y, s, fill='var(--faint)', size=9, anchor='start': o.append(
        '<text x="%.1f" y="%.1f" font-family="IBM Plex Mono, monospace" font-size="%s" fill="%s" '
        'text-anchor="%s">%s</text>' % (x, y, size, fill, anchor, s))
    ut = O['u_top']
    for k, (b, col) in enumerate((('D1', 'var(--accent)'), ('D2', 'var(--accent-ink)'))):
        y0 = 22 + k * (PH + 58)
        P = lambda t, u: (X0 + (t - T0) * K, y0 + (U1 - u) * K)
        sh = O['sheets'][b]
        tl = sh['t_left']
        curve = sh['third_wall_curve']
        # axes through the record
        o.append('<g stroke="var(--rule)" stroke-width="1">')
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (P(T0, 0) + P(T1, 0)))
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (P(0, U1) + P(0, U0)))
        o.append('</g>')
        # the region
        pts = [P(tl, ut), P(sh['corner_top_right'][0], ut)] + [P(t, u) for t, u in reversed(curve)]
        o.append('<path d="M %s Z" fill="var(--gold)" fill-opacity=".24"/>' % ' L '.join('%.1f,%.1f' % p for p in pts))
        # the three walls
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.5"/>'
                 % (P(tl, curve[0][1]) + P(tl, ut) + (col,)))
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--muted)" stroke-width="1.5"/>'
                 % (P(tl, ut) + P(sh['corner_top_right'][0], ut)))
        o.append('<path d="M %s" fill="none" stroke="var(--warn)" stroke-width="2"/>'
                 % ' L '.join('%.1f,%.1f' % P(t, u) for t, u in curve))
        # seams
        tw = next(t0 + (t1 - t0) * (-1 / 36 - u0) / (u1 - u0)
                  for (t0, u0), (t1, u1) in zip(curve, curve[1:]) if u0 <= -1 / 36 <= u1)
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--warn)" stroke-width="1" '
                 'stroke-dasharray="2 3"/>' % (P(tl, -1 / 36) + P(tw, -1 / 36)))
        if b == 'D2':
            uw = next(u0 + (u1 - u0) * (-3 / 31 - t0) / (t1 - t0)
                      for (t0, u0), (t1, u1) in zip(curve, curve[1:]) if t0 <= -3 / 31 <= t1)
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--warn)" stroke-width="1" '
                     'stroke-dasharray="2 3"/>' % (P(-3 / 31, uw) + P(-3 / 31, ut)))
            T(P(-3 / 31, uw)[0] + 3, P(-3 / 31, uw)[1] - 5, 't = &#8722;3/31', fill='var(--warn)', size=8)
        # the crossing segment and the record
        lo, hi = O['crossing_segment']['u']
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--gold)" stroke-width="3.5"/>'
                 % (P(0, lo) + P(0, hi)))
        o.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="var(--accent)"/>' % P(0, 0))
        # labels
        T(X0, y0 - 8, '%s sheet' % b, fill=col, size=11)
        T(X0 + W, y0 - 8, 't along %s &#8594; &#183; u (fibre) &#8593;' % b, anchor='end', size=8)
        T(P(tl, U0)[0] - 3, P(tl, U0)[1] + 12, 't = %s' % ('&#8722;2/19' if b == 'D1' else '&#8722;0.1358'),
          fill=col, size=8, anchor='start')
        c = sh['corner_top_right']
        T(P(c[0], ut)[0], P(c[0], ut)[1] - 4, '%.4f' % c[0], size=8, anchor='end')
        T(P(tl, sh['corner_bottom_left'][1])[0] + 4, P(tl, sh['corner_bottom_left'][1])[1] + 3,
          'u = %.4f' % sh['corner_bottom_left'][1], size=8)
    y = int(2 * PH + 150) - 30
    T(X0, y, 'gold bar: the crossing, in both sheets', fill='var(--gold)', size=8.5)
    T(X0, y + 11, 'red: the one curved wall &#183; dotted: seams', fill='var(--warn)', size=8.5)
    T(X0, y + 22, 't and u to one scale, both panels', size=8.5)
    o.append('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    sys.stdout.write(build())
