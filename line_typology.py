#!/usr/bin/env python3
"""Do the 727-carrying LINES fit the typology, or are they a separate axis?

TYPOLOGY.md classifies configurations: count -> depth profile -> per-label
type -> congruence, with "a type is a CHAMBER of a wall line".  That puts
lines one level ABOVE types: a line carries a sequence of chambers, hence a
sequence of types.  So the question is whether the typology's own structure
extends upward.

The sharpest test is the C3.  The 393 base is invariant under the 120-degree
rotation about (1,1,1), which is why configurations must be quotiented by it
or they triple-count (Postscript 52 addendum 6: 417 -> 161).  That rotation
acts on a free cube by LEFT MULTIPLICATION by g = (1,1,1,1), and in Cayley
coordinates left multiplication by a fixed quaternion is a PROJECTIVE map of
(1,a,b,c) -- so it carries lines to lines.  If the typology's C3 is real
rather than an artifact of how configurations were enumerated, the 129
727-carrying lines must be closed under it, in orbits of 3 (or 1 for lines
fixed by the rotation).

INVARIANT: line identity is decided by exact collinearity in Fractions -- two
lines are the same iff each of two distinct image points lies on the
candidate.  Matching by rounded direction vectors would merge distinct
parallel lines, which is exactly the error that would manufacture a tidy
orbit structure.
"""
import collections
import json
from fractions import Fraction as F

G = (1, 1, 1, 1)          # the C3 generator: 120 degrees about (1,1,1)


def qmul(p, q):
    w, x, y, z = p
    e, f, g, h = q
    return (w*e - x*f - y*g - z*h,
            w*f + x*e + y*h - z*g,
            w*g - x*h + y*e + z*f,
            w*h + x*g - y*f + z*e)


def act(pt):
    """C3 image of a Cayley point, or None if it goes to infinity."""
    q = (F(1), F(pt[0]), F(pt[1]), F(pt[2]))
    w, x, y, z = qmul(tuple(F(v) for v in G), q)
    if w == 0:
        return None
    return (x/w, y/w, z/w)


def on_line(pt, p0, dd):
    """Exact: does pt lie on p0 + t*dd?"""
    v = [pt[u] - p0[u] for u in range(3)]
    for i in range(3):
        for j in range(i+1, 3):
            if v[i]*dd[j] - v[j]*dd[i] != 0:
                return False
    return True


def main():
    data = json.load(open('typology_data.json'))
    lines = []
    for L in data['lines']:
        p0 = tuple(F(x) for x in L['p0'])
        dd = tuple(F(x) for x in L['dir'])
        lines.append((p0, dd))
    n = len(lines)
    print('727-carrying lines: %d' % n)

    # --- are the 129 distinct as LINES? ------------------------------------
    reps = []
    dup = 0
    which = []
    for p0, dd in lines:
        found = None
        for idx, (q0, ee) in enumerate(reps):
            if on_line(p0, q0, ee) and on_line(tuple(p0[u]+dd[u] for u in range(3)),
                                               q0, ee):
                found = idx
                break
        if found is None:
            reps.append((p0, dd))
            which.append(len(reps)-1)
        else:
            dup += 1
            which.append(found)
    print('distinct as geometric lines: %d  (%d of the %d entries are repeats)'
          % (len(reps), dup, n))

    # --- C3 action ---------------------------------------------------------
    perm = {}
    off = 0
    for i, (p0, dd) in enumerate(reps):
        a = act(p0)
        b = act(tuple(p0[u] + dd[u] for u in range(3)))
        if a is None or b is None:
            perm[i] = None
            off += 1
            continue
        img = None
        for j, (q0, ee) in enumerate(reps):
            if on_line(a, q0, ee) and on_line(b, q0, ee):
                img = j
                break
        perm[i] = img
        if img is None:
            off += 1
    closed = sum(1 for v in perm.values() if v is not None)
    print('\nC3 image lands on another line of the set: %d of %d'
          % (closed, len(reps)))
    if off:
        print('   %d lines whose image is NOT in the set (or runs to infinity)'
              % off)

    # --- orbits ------------------------------------------------------------
    seen = set()
    orbits = []
    for i in range(len(reps)):
        if i in seen or perm[i] is None:
            continue
        orb = [i]
        j = perm[i]
        while j is not None and j != i and j not in orb:
            orb.append(j)
            j = perm[j]
        if j == i:
            orbits.append(orb)
            seen |= set(orb)
    sizes = collections.Counter(len(o) for o in orbits)
    print('\nC3 orbits of lines: %d, sizes %s'
          % (len(orbits), dict(sorted(sizes.items()))))
    print('   lines accounted for by closed orbits: %d' % len(seen))

    # --- do orbit-mates carry the same 727 structure? ----------------------
    # Read the LIVE run's own stdout, not continua_shard_0.jsonl: that file is
    # opened in append mode, so the broken first census (129 records, every
    # one with runs=[]) is still in it, and any line the current run has not
    # reached yet would silently read as "no continua".  Accumulated output
    # from a superseded run is not data.
    runs = {}
    import re
    try:
        for l in open('continua_phaseA.out'):
            m = re.match(r'^line\s+(\d+): (\d+) continua \[(.*)\]', l)
            if not m:
                continue
            got = []
            for piece in re.findall(r"'([-\d.]+)\.\.([-\d.]+)'", m.group(3)):
                got.append([piece[0], piece[1]])
            runs[int(m.group(1))] = got
    except FileNotFoundError:
        pass
    if runs:
        print('\n727 stretches within each C3 orbit (census so far: %d lines):'
              % len(runs))
        agree = disagree = partial = 0
        for orb in orbits:
            ent = []
            for i in orb:
                mem = [k for k, v in enumerate(which) if v == i]
                got = [runs[m] for m in mem if m in runs]
                ent.append(got[0] if got else None)
            if any(e is None for e in ent):
                partial += 1
                continue
            widths = [sorted(round(float(b) - float(a), 6)
                             for a, b in e) for e in ent]
            if all(w == widths[0] for w in widths):
                agree += 1
            else:
                disagree += 1
                print('   orbit %s: differing stretches %s' % (orb, widths))
        print('   orbits fully scanned: agree %d, disagree %d'
              ' (not yet scanned: %d)' % (agree, disagree, partial))


if __name__ == '__main__':
    main()
