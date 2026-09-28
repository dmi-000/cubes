#!/usr/bin/env python3
"""The 727 node inset of TOWER_DIAGRAM.html, drawn in CLASS space ([P391], [P392]).

Replaces the four-parallel-arcs drawing, which showed D1 twice (as D and as B) and D2 only as C.
Every coordinate below is sourced:
  D1 (= B), direction (-1,-1/7,3/14) from the record: 727 on (-2/19, 0.1964879746) [P296];
      1217 shadow (-2/19, ~0.0497) [P303]; swept window (-1/8, 1/4) [P94]; 725 at -2/19 and 713 at
      2/9 [P294].
  D2 (= C), direction (-1,-4/21,2/7): 727 on (-0.135781, 0.220728), a 723 puncture at t = -3/31
      (C's 164/87 carried over, engine-checked) [P392].
  A, own parameter: 727 on (2.0640, 19/6); 725 at 13/6 and at 19/6 [P93], [P294].
  n = 7 ([P393], [P394]): with the record's seventh cube, a SEGMENT of each branch extends to 1217:
      D1 (-2/19, ~0.0497) and D2 (-0.135781, ~0.0702); arc A does not. The 1217 plateau near the record
      is two sheets, each a curved triangle in its own (t, u) plane, CROSSING along the fibre segment
      over the record.  The sketch is drawn from data/n7_sheet_outline.json: each sheet exact in its own
      plane, t and u at one scale; only the angle between the two planes is widened (really 4.51 deg).
Colours are the page's CSS variables, so both themes work.
"""
import math, os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTLINE = json.load(open(os.path.join(ROOT, 'data', 'n7_sheet_outline.json')))
OY = 490                    # the n = 6 drawing sits this far below the n = 7 sketch
K = 1100.0                  # px per unit t, D1 and D2 alike (their direction vectors have norm 1.035, 1.064)
RX, RY = 330, 360           # the record
TILT = 24.0                 # D2 drawn at 24 degrees from D1; really 4.51


def d1(t): return RX, RY - K * t
def d2(t):
    a = math.radians(TILT)
    return RX + K * t * math.sin(a), RY - K * t * math.cos(a)
def A(s): return 890, 470 - (s - 2.0640) / (19 / 6 - 2.0640) * 290

# ---- n = 7: the two sheets, drawn as the n = 6 X swept along the fibre ---------------------------
KS = 1600.0                 # px per unit, t and u alike: each sheet is to scale in its own plane
SX, SY = 300, 205           # the record in the sketch
FIB = (-0.94, -0.34)        # screen direction of +u (the fibre); -u, where the sheets mostly lie, runs right-down


def s7(branch, t, u):
    """screen point of (t along branch, u along the fibre); branches as in the n = 6 drawing"""
    a = math.radians(0.0 if branch == 'D1' else TILT)
    return (SX + KS * (t * math.sin(a) + u * FIB[0]),
            SY - KS * (t * math.cos(a) - u * FIB[1]) )


def sheet_path(branch):
    sh = OUTLINE['sheets'][branch]
    tl, ut = sh['t_left'], OUTLINE['u_top']
    pts = [s7(branch, tl, ut), s7(branch, sh['corner_top_right'][0], ut)]
    pts += [s7(branch, t, u) for t, u in reversed(sh['third_wall_curve'])]
    return 'M ' + ' L '.join('%.1f,%.1f' % p for p in pts) + ' Z'


def wall_t_at(branch, u):
    """t where the third wall reaches height u, by interpolation in the solved curve"""
    c = OUTLINE['sheets'][branch]['third_wall_curve']
    for (t0, u0), (t1, u1) in zip(c, c[1:]):
        if u0 <= u <= u1:
            return t0 + (t1 - t0) * (u - u0) / (u1 - u0)
    return None


def wall_u_at(branch, t):
    c = OUTLINE['sheets'][branch]['third_wall_curve']
    for (t0, u0), (t1, u1) in zip(c, c[1:]):
        if t0 <= t <= t1:
            return u0 + (u1 - u0) * (t - t0) / (t1 - t0)
    return None


def sketch():
    o = []
    T = lambda x, y, s, fill='var(--muted)', size=11, anchor='start', weight='normal': o.append(
        '<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s">%s</text>'
        % (x, y, size, fill, anchor, weight, s))
    L = lambda p, q, col, w, extra='': o.append(
        '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" %s/>'
        % (p[0], p[1], q[0], q[1], col, w, extra))
    T(4, 18, 'n = 7 &#8212; over the node: 1217 = the record + 4,&#8722;3,&#8722;4,&#8722;4. Its plateau is two sheets, one over each',
      fill='var(--ink)')
    T(4, 34, 'branch, CROSSING along the fibre segment over the record, as the branches cross at the record below.',
      fill='var(--ink)')
    ut = OUTLINE['u_top']
    # the sheets: D2 first (it is drawn nearer the viewer, so D1 shows through it)
    for b, col, dash in (('D1', 'var(--accent)', ''), ('D2', 'var(--accent-ink)', 'stroke-dasharray="6 4"')):
        o.append('<path d="%s" fill="var(--gold)" fill-opacity=".20" stroke="%s" stroke-width="1.6" %s/>'
                 % (sheet_path(b), col, dash))
    # seams: zero-width lines of lower count with 1217 on both sides
    for b in ('D1', 'D2'):
        t_end = wall_t_at(b, -1 / 36)
        L(s7(b, OUTLINE['sheets'][b]['t_left'], -1 / 36), s7(b, t_end, -1 / 36), 'var(--warn)', 1, 'stroke-dasharray="2 3"')
    L(s7('D2', -3 / 31, wall_u_at('D2', -3 / 31)), s7('D2', -3 / 31, ut), 'var(--warn)', 1, 'stroke-dasharray="2 3"')
    # the branches at u = 0 (the recorded seventh cube): their 727 extents, as below
    L(s7('D1', -2 / 19, 0), s7('D1', 0.06, 0), 'var(--accent)', 3)
    L(s7('D2', -0.135781, 0), s7('D2', 0.075, 0), 'var(--accent-ink)', 3, 'stroke-opacity=".85"')
    # the crossing: the fibre segment over the record, in both sheets
    lo, hi = OUTLINE['crossing_segment']['u']
    L(s7('D1', 0, lo), s7('D1', 0, hi), 'var(--gold)', 4)
    p = s7('D1', 0, 0)
    o.append('<circle cx="%.1f" cy="%.1f" r="7" fill="var(--accent)" stroke="var(--card)" stroke-width="2"/>' % p)
    # labels
    q = s7('D1', 0, lo)
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--gold)" stroke-width="1"/>'
             % (q[0] + 3, q[1] + 3, q[0] + 150, q[1] + 60))
    T(q[0] + 154, q[1] + 58, 'the crossing: over the record,', fill='var(--gold)', size=10)
    T(q[0] + 154, q[1] + 72, 't = 0, u from &#8722;0.0453 to +0.00255', fill='var(--gold)', size=10)
    T(p[0] - 12, p[1] - 10, '1217 &#183; the record + its 7th cube', fill='var(--ink)', size=11, anchor='end', weight='600')
    a = s7('D1', OUTLINE['sheets']['D1']['t_left'], -0.11)
    T(a[0] + 10, a[1] + 16, 'D1 sheet', fill='var(--accent)', size=12, weight='600')
    a = s7('D2', OUTLINE['sheets']['D2']['t_left'], 0)
    T(a[0] - 8, a[1] + 4, 'D2 sheet', fill='var(--accent-ink)', size=12, anchor='end', weight='600')
    f = s7('D1', 0, 0.0025); g = s7('D1', 0, -0.03)
    T(g[0] + 30, g[1] - 70, '&#8722;u (the fibre) &#8600;', size=10)
    a = s7('D1', 0.06, 0)
    T(a[0] - 6, a[1] - 6, 'D1 at u = 0', fill='var(--accent)', size=10, anchor='end')
    a = s7('D2', 0.075, 0)
    T(a[0] + 6, a[1] - 6, 'D2 at u = 0', fill='var(--accent-ink)', size=10)
    kx = 640
    T(kx, 70, 'each sheet: a curved triangle, three walls', size=10, fill='var(--ink)')
    T(kx, 84, 'left &#8212; its branch&#8217;s lower 727 wall', size=10)
    T(kx, 98, 'top &#8212; u = 0.00255, flat, the same on both', size=10)
    T(kx, 112, 'lower right &#8212; one wall (P301&#8217;s third wall)', size=10)
    T(kx, 132, 'dotted: seams, zero-width lines of lower', size=10, fill='var(--warn)')
    T(kx, 146, 'count with 1217 on both sides', size=10, fill='var(--warn)')
    T(kx, 166, 't and u to one scale; the angle between', size=10)
    T(kx, 180, 'the sheets drawn at 19&#176;, really 4.51&#176;', size=10)
    # the step down to n = 6
    T(4, OY - 14, '&#8593; each gold bar below is its sheet&#8217;s u = 0 line: add the 7th cube to any point of it and the count is 1217',
      fill='var(--gold)', size=10)
    o.append('<line x1="0" y1="%d" x2="1010" y2="%d" stroke="var(--rule)" stroke-width="1"/>' % (OY - 4, OY - 4))
    return o


def build():
    o = []
    T = lambda x, y, s, fill='var(--muted)', size=11, anchor='start', weight='normal': o.append(
        '<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" font-weight="%s">%s</text>'
        % (x, y, size, fill, anchor, weight, s))
    T(4, 18, 'n = 6 &#8212; the node: D1 and D2 cross at the record, each TO SCALE in its own t;')
    T(4, 34, 'arc A is a separate piece (own scale). Arcs B and C of the catalogue are D1 and D2 respelled.')
    # D1: swept window, 727 extent, 1217 shadow
    (x, ya), (_, yb) = d1(0.25), d1(-0.125)
    o.append('<rect x="%.1f" y="%.1f" width="22" height="%.1f" fill="var(--warn-soft)"/>' % (x - 11, ya, yb - ya))
    sx, sy = x + 24, ya + 0.3 * (yb - ya)       # right of the bar, above the gold bar, left of D2
    T(sx, sy, 'SWEPT &#8212; not a bound', fill='var(--warn)', size=10, anchor='middle')
    o[-1] = o[-1].replace('<text ', '<text transform="rotate(-90 %.1f %.1f)" ' % (sx, sy))
    (x, y1), (_, y2) = d1(0.196487974607), d1(-2 / 19)
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--accent)" stroke-width="8"/>' % (x, y1, x, y2))
    (_, y3) = d1(0.0497)
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--gold)" stroke-width="5"/>' % (x + 16, y3, x + 16, y2))
    # D2
    (x1, y1), (x2, y2) = d2(0.220728), d2(-0.135781)
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--accent-ink)" stroke-width="8" '
             'stroke-opacity=".85"/>' % (x1, y1, x2, y2))
    a = math.radians(TILT); ox, oy = 16 * math.cos(a), 16 * math.sin(a)   # offset to D2's right
    (b1x, b1y), (b2x, b2y) = d2(0.0702), d2(-0.135781)
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--gold)" stroke-width="5"/>'
             % (b1x + ox, b1y + oy, b2x + ox, b2y + oy))
    D2BAR = ((b1x + ox, b1y + oy), (b2x + ox, b2y + oy))
    # special points
    def hollow(p, col='var(--muted)'):
        o.append('<circle cx="%.1f" cy="%.1f" r="6" fill="var(--card)" stroke="%s" stroke-width="2.5"/>' % (p[0], p[1], col))
    p = d1(-2 / 19); hollow(p, 'var(--warn)'); T(p[0] + 26, p[1] + 16, '725 &#183; t = &#8722;2/19 &#183; shared wall', fill='var(--warn)')
    p = d1(2 / 9); hollow(p); T(p[0] - 14, p[1] + 4, '713 &#183; t = 2/9 &#183; outside the plateau', anchor='end')
    p = d1(0.196487974607); T(p[0] - 14, p[1] + 4, '727 plateau ends 0.19648797&#8230;', fill='var(--accent-ink)', anchor='end')
    p = d1(0.0497); T(p[0] - 30, p[1] + 4, 'lifts to 1217 up to &#8776; 0.0497', fill='var(--gold)', anchor='end')
    T(D2BAR[0][0] + 14, D2BAR[0][1] + 4, 'lifts to 1217 up to &#8776; 0.0702', fill='var(--gold)')
    p = d2(-3 / 31); hollow(p); T(p[0] - 12, p[1] + 4, '723 &#183; t = &#8722;3/31 &#183; a puncture', anchor='end')
    p = d2(0.220728); T(p[0] + 10, p[1] - 6, 'D2 ends 0.2207', fill='var(--accent-ink)')
    p = d2(-0.135781); T(p[0] - 12, p[1] + 4, 'D2 (= C) ends &#8722;0.1358', fill='var(--accent-ink)', anchor='end')
    x, y = d1(-0.125); T(x, y + 24, 'D1 (= B)', fill='var(--ink)', size=13, anchor='middle', weight='600')
    T(x, y + 40, 'TO SCALE in t', fill='var(--accent)', size=10, anchor='middle')
    # the record
    o.append('<circle cx="%d" cy="%d" r="9" fill="var(--accent)" stroke="var(--card)" stroke-width="2"/>' % (RX, RY))
    T(RX + 22, RY + 22, '727 &#183; t = 0 &#183; the record', fill='var(--ink)', size=12, weight='600')
    T(RX + 22, RY + 38, 'two branches cross here: really 4.51&#176;, drawn at 24&#176;', size=10)
    # arc A
    (xa, ya), (_, yb) = A(19 / 6), A(2.0640)
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--warn)" stroke-width="6" stroke-dasharray="7 5"/>' % (xa, ya, xa, yb))
    for s in (13 / 6, 19 / 6):
        p = A(s); hollow(p, 'var(--warn)'); T(p[0] + 12, p[1] + 4, '725', fill='var(--warn)')
    T(xa, yb + 24, 'arc A', fill='var(--warn)', size=13, anchor='middle', weight='600')
    T(xa, yb + 40, 'own scale &#183; s &#8712; (2.064, 19/6)', fill='var(--warn)', size=10, anchor='middle')
    T(xa, ya - 30, 'a separate piece:', fill='var(--warn)', size=10, anchor='middle')
    T(xa, ya - 16, 'meets no spelling of the record', fill='var(--warn)', size=10, anchor='middle')
    # the base
    o.append('<path d="M 230 560 V 568 H 800 V 560" fill="none" stroke="var(--rule)" stroke-width="1.5"/>')
    o.append('<circle cx="515" cy="590" r="8" fill="var(--accent)"/>')
    T(533, 594, '393 &#183; n = 5 &#8212; every arc lies in ONE fibre over this base', fill='var(--ink)', size=11)
    head = ['<svg viewBox="0 0 1010 %d" role="img" aria-label="The 727 node in class space and what lies over it. '
            'At n = 7, the 1217 plateau: two sheets crossing along the fibre segment over the record. At n = 6, '
            'two branches, D1 and D2, crossing at the record, each to scale in its own parameter, with the segment '
            'of each that lifts to 1217 marked beside it; arc A separate. The 393 base beneath.">' % (620 + OY)]
    return '\n'.join(head + sketch() + ['<g transform="translate(0,%d)">' % OY] + o + ['</g>', '</svg>'])


if __name__ == '__main__':
    sys.stdout.write(build())
