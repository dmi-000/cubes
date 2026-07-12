#!/usr/bin/env python3
# Working principles: ALGEBRAIC_SEARCH.md. Project index: README.md
"""Count the candidate configs emitted by algebraic_demo.wl.

Reads algebraic_walls.json ({points, quats}), runs each integer-quaternion
config through the validated ./cube_regions counter, and reports the count
spectrum along the exact algebraic line search -- flagging the s=0 anchor
(must reproduce the seed record) and anything that beats the current
record. This is the counting half of the algebraic search: Wolfram finds
the exact rational walls; the exact engine counts them.

Usage: python3 algebraic_bridge.py [walls.json] [RECORD=723]
"""
import json
import subprocess
import sys

RECORD = int(sys.argv[2]) if len(sys.argv) > 2 else 723


def count(quats):
    s = ';'.join(','.join(map(str, q)) for q in quats)
    try:
        o = subprocess.run(['./cube_regions', '--quats', s],
                           capture_output=True, text=True, timeout=120).stdout
        r = json.loads(o)
        return r['bounded'], r['by_depth']
    except Exception as e:
        return None, str(e)


def main(path):
    d = json.load(open(path))
    pts, quats = d['points'], d['quats']
    rows = []
    best = 0
    for s, q in zip(pts, quats):
        if max(abs(c) for cube in q for c in cube) > 100000:
            rows.append((s, None, 'quat too large'))
            continue
        tot, bd = count(q)
        rows.append((s, tot, bd))
        if isinstance(tot, int):
            best = max(best, tot)
    rows.sort(key=lambda r: (r[1] is None, -(r[1] or 0)))
    print(f'counted {len(rows)} configs; best total = {best} '
          f'(record {RECORD})')
    # s=0 anchor
    anchor = [r for r in rows if abs(r[0]) < 1e-9]
    if anchor:
        print(f's=0 anchor -> {anchor[0][1]} (must equal the seed record)')
    print('\ntop 15 by total:')
    for s, tot, bd in rows[:15]:
        flag = '  *** BEATS RECORD ***' if isinstance(tot, int) and tot > RECORD else ''
        print(f'  s={s:+.6g}  total={tot}  {bd if isinstance(bd, dict) else ""}{flag}')
    beat = [r for r in rows if isinstance(r[1], int) and r[1] > RECORD]
    print(f'\n{len(beat)} configs beat {RECORD}.')
    for s, tot, bd in beat:
        q = quats[pts.index(s)]
        print(f'  total={tot} s={s} quats={q} by_depth={bd}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'algebraic_walls.json')
