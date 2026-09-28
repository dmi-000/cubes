#!/usr/bin/env python3
"""Draw the 727 arc network in CLASS space: viewers/arcmap.svg (+ PNGs via rsvg-convert).

Why a redraw ([P391], [P392]).  The earlier map (kept as viewers/arcmap_fixed_base.svg) holds the
393 base FIXED, where five lines are distinct.  Up to congruence they are three: arc B is D1 and
arc C is D2, carried by the base's own 120-degree symmetry to the record's other spellings, and
arc A is a separate piece.  So this map draws A, and the node where D1 and D2 cross at the record.

Data, every figure sourced:
  lengths      integrated rotation angle over SOLVED extents ([P97]'s measure): A 3.994, D1 = B
               7.045, D2 = C 8.431 degrees.  D1 = B and D2 = C agree exactly ([P392]).
  stations     the field classes on each line, in their true ORDER (spacing even), located from
               data/wide_campaign_shard_*.jsonl by their parameter on the line: on B (= D1)
               sqrt25561 < record < sqrt12313 < sqrt1614; on C (= D2) 13461, 13489, 5305, 226 <
               record < 27349, 3459, 1785, 1930.  A: 1093, 13, 403, 2741 ([P79], [P93]).
  W4           the one wall ([P93]) crossed by every arc: on A between 403 and 2741, on B (= D1)
               between 1614 and the upper end, on C (= D2) between 1785 and 1930.
"""
import os, math, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PX = 60.0                                   # pixels per degree of rotation
INK, MUTED, BG = '#15181d', '#6a7180', '#faf9f7'
COL = {'A': '#c2553a', 'D1': '#3d7e87', 'D2': '#4b6fb0', 'node': '#7a4fa0'}
STYLE = ('<style>.stn{fill:#fff;stroke-width:3.5}.lbl{font:12.5px "SFMono-Regular",Menlo,monospace;fill:#15181d}'
         '.lblm{font:12px "Helvetica Neue",Helvetica,Arial,sans-serif;fill:#6a7180}'
         '.lname{font:600 15px "Helvetica Neue",Helvetica,Arial,sans-serif}'
         '.ttl{font:600 27px "Helvetica Neue",Helvetica,Arial,sans-serif;fill:#15181d}'
         '.sub{font:14.5px "Helvetica Neue",Helvetica,Arial,sans-serif;fill:#6a7180}'
         '.cap{font:13px "Helvetica Neue",Helvetica,Arial,sans-serif;fill:#6a7180}'
         '.capb{font:600 13px "Helvetica Neue",Helvetica,Arial,sans-serif;fill:#15181d}</style>')


def line(name, x0, y0, ang_deg, length_deg, slots, w4_after, col, ends, lab_dy=24):
    """slots: labels in order, 'END' at both ends and 'REC' for the record; spacing even.
    Returns (svg, {label: (x, y)})."""
    L = length_deg * PX
    ux, uy = math.cos(math.radians(ang_deg)), math.sin(math.radians(ang_deg))
    n = len(slots) - 1
    pos = {}
    out = ['<path d="M %.1f %.1f L %.1f %.1f" stroke="%s" stroke-width="7" fill="none" '
           'stroke-linecap="round"/>' % (x0, y0, x0 + L * ux, y0 + L * uy, col)]
    if not isinstance(lab_dy, tuple):
        lab_dy = (lab_dy, lab_dy)                 # (before the record, after it)
    rec_i = slots.index('REC') if 'REC' in slots else n + 1
    for i, lab in enumerate(slots):
        x, y = x0 + L * ux * i / n, y0 + L * uy * i / n
        dy = lab_dy[0] if i < rec_i else lab_dy[1]
        pos[lab if lab not in ('END',) else 'END%d' % i] = (x, y)
        if lab == 'REC':
            continue
        r = 7 if lab == 'END' else 6
        out.append('<circle class="stn" cx="%.1f" cy="%.1f" r="%d" stroke="%s"/>' % (x, y, r, col))
        if lab != 'END':
            out.append('<text class="lbl" x="%.1f" y="%.1f" text-anchor="middle">√%s</text>'
                       % (x, y + dy, lab))
    i = w4_after                       # W4 tick midway between slot i and i+1
    x = x0 + L * ux * (i + 0.5) / n; y = y0 + L * uy * (i + 0.5) / n
    px, py = -uy, ux
    out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#9aa0ab" stroke-width="2.5" '
               'stroke-dasharray="4 3"/>' % (x - 16 * px, y - 16 * py, x + 16 * px, y + 16 * py))
    (xa, ya), (xb, yb) = pos['END0'], pos['END%d' % n]
    out.append('<text class="lblm" x="%.1f" y="%.1f" text-anchor="end">%s</text>' % (xa - 12, ya + 4, ends[0]))
    out.append('<text class="lblm" x="%.1f" y="%.1f">%s</text>' % (xb + 12, yb + 4, ends[1]))
    return '\n'.join(out), pos


def main():
    W, H = 1200, 960
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
         STYLE, '<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG),
         '<text class="ttl" x="48" y="54">The 727 arc network</text>',
         '<text class="sub" x="48" y="82">Every known six-cube configuration reaching 727, UP TO CONGRUENCE: three arcs, '
         'two of them crossing at the record · lengths TO SCALE in rotation angle</text>']
    # arc A, a separate piece
    ax = 480
    sv, _ = line('A', ax, 190, 0, 3.994, ['END', '1093', '13', '403', '2741', 'END'], 3, COL['A'],
                 ('2.0640 · 723 ↓', '19/6 · 723 ↓'))
    s += [sv, '<text class="lname" x="%d" y="150" fill="%s">A</text>' % (ax, COL['A']),
          '<text class="lblm" x="%d" y="150">a separate piece: meets no spelling of the record · 4 fields · 10 chambers · 3.99°</text>' % (ax + 22)]
    # the node: D1 (= B) and D2 (= C) crossing at the record, angle drawn wide
    cx, cy, half = 600, 410, 17.0
    L1, L2 = 7.045 * PX, 8.431 * PX
    f1, f2 = 2 / 5, 5 / 10                   # the record's slot along each line
    x1 = cx - L1 * f1 * math.cos(math.radians(half)); y1 = cy - L1 * f1 * math.sin(math.radians(half))
    x2 = cx - L2 * f2 * math.cos(math.radians(-half)); y2 = cy - L2 * f2 * math.sin(math.radians(-half))
    sv1, _ = line('D1', x1, y1, half, 7.045, ['END', '25561', 'REC', '12313', '1614', 'END'], 4, COL['D1'],
                  ('−2/19 · 723 ↓', '0.1965 · 723 ↓'), lab_dy=(-14, 26))
    sv2, _ = line('D2', x2, y2, -half, 8.431,
                  ['END', '13461', '13489', '5305', '226', 'REC', '27349', '3459', '1785', '1930', 'END'], 8, COL['D2'],
                  ('−0.1358 · 723 ↓', '0.2207 · 723 ↓'), lab_dy=(26, -14))
    s += [sv1, sv2,
          '<circle cx="%d" cy="%d" r="15" fill="#fff" stroke="%s" stroke-width="4"/>' % (cx, cy, COL['node']),
          '<text class="lname" x="%.1f" y="%.1f" fill="%s">D1 = B</text>' % (x1 - 10, y1 - 30, COL['D1']),
          '<text class="lblm" x="%.1f" y="%.1f">3 fields · 11 chambers · 7.04°</text>' % (x1 - 10, y1 - 14),
          '<text class="lname" x="%.1f" y="%.1f" fill="%s">D2 = C</text>' % (x2 - 10, y2 + 60, COL['D2']),
          '<text class="lblm" x="%.1f" y="%.1f">8 fields · 12 chambers · 8.43°</text>' % (x2 - 10, y2 + 76),
          '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>' % (cx + 12, cy + 10, cx + 150, cy + 150, MUTED),
          '<text class="lbl" x="%d" y="%d">the n = 6 record (7,14,1,−5)</text>' % (cx + 156, cy + 156),
          '<text class="lblm" x="%d" y="%d">a node: the two branches cross here, really 4.51° apart</text>' % (cx + 156, cy + 174)]
    # key
    ky = 660
    s += ['<text class="capb" x="48" y="%d">KEY</text>' % ky,
          '<circle class="stn" cx="60" cy="%d" r="7" stroke="%s"/>' % (ky + 24, INK),
          '<text class="cap" x="80" y="%d">terminus: the count steps down to 723 beyond it</text>' % (ky + 28),
          '<circle class="stn" cx="60" cy="%d" r="6" stroke="%s"/>' % (ky + 50, INK),
          '<text class="cap" x="80" y="%d">a congruence class living in ℚ(√d), labelled by d</text>' % (ky + 54),
          '<circle cx="60" cy="%d" r="10" fill="#fff" stroke="%s" stroke-width="4"/>' % (ky + 78, COL['node']),
          '<text class="cap" x="80" y="%d">the record: where the two branches of the node cross</text>' % (ky + 82),
          '<line x1="60" y1="%d" x2="60" y2="%d" stroke="#9aa0ab" stroke-width="2.5" stroke-dasharray="4 3"/>' % (ky + 96, ky + 116),
          '<text class="cap" x="80" y="%d">where each arc crosses the one W4 wall they all cross: a free-cube face plane through a base triple point</text>' % (ky + 110)]
    cy2 = 810
    caps = [('TO SCALE', 'line length is rotation angle over the SOLVED extent, 60 px per degree. D1 = B and D2 = C agree exactly (P392).'),
            ('NOT TO SCALE', 'station spacing is even, not proportional (the ORDER is true); the D1/D2 crossing is 4.51°, drawn wide.'),
            ('UP TO CONGRUENCE', 'the fixed-base drawing (arcmap_fixed_base.svg) shows five lines; B and C there are D1 and D2 here (P391).'),
            ('', 'The vertical axis carries nothing: row order and spacing are for legibility only.')]
    for i, (k, t) in enumerate(caps):
        y = cy2 + 26 * i
        if k:
            s.append('<text class="capb" x="48" y="%d">%s</text>' % (y, k))
        s.append('<text class="cap" x="%d" y="%d">%s</text>' % (200, y, t))
    s.append('</svg>')
    out = os.path.join(ROOT, 'viewers', 'arcmap.svg')
    open(out, 'w', encoding='utf-8').write('\n'.join(s))
    for w, name in ((1800, 'arcmap.png'), (3600, 'arcmap@2x.png')):
        subprocess.run(['rsvg-convert', '-w', str(w), out, '-o', os.path.join(ROOT, 'viewers', name)], check=True)
    print('wrote viewers/arcmap.svg and PNGs')


if __name__ == '__main__':
    main()
