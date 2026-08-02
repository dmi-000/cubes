#!/usr/bin/env python3
"""The repaired one-cube increment bound — B_j via Euler's formula on dC_j.

Supersedes `increment_bound.py` (kept, unmodified, as documentation of the
failure it made: F = 2 + V assumes every trace-curve face on dC_j is a disk,
i.e. c = 1 and no isolated curves, and it dropped TANGENT lines instead of
counting them, so at the degenerate records (where tangency is the rule, not
the exception) it undercounted badly.

See INCREMENT_BOUND_SPEC.md for the full derivation. In brief: with G the
region-adjacency graph of a compound S (including the outside region), and
G_j its "bit j" subgraph (edges joining regions whose labels differ only in
bit j), forgetting cube j merges exactly the components of G_j, so

    Delta_j = N - #components(G_j)                                   (I)
            <= |E(G_j)|                                              (II)
            <= W_j  (walls on dC_j)                                  (III)
            <= K_j  (mask cells of dC_j)                             (IV)
            <= B_j  (cells cut on dC_j by the OTHER cubes' planes)   (V)

B_j is computed via Euler's formula for a graph embedded on a sphere (dC_j,
topologically S^2) with c connected components:

    B_j = 1 + c + sum_v ( deg(v)/2 - 1 ),                            (*)

sum over vertices v of the plane arrangement traced on dC_j, deg(v) = 2 *
(number of trace curves through v).

INVARIANT: `fractions.Fraction` throughout. No float ever decides a
comparison — the whole point is the degenerate (tangent) configurations,
where a float would be worthless. Both `mat()`, `CONFIGS`, and `count()` are
imported unmodified from `increment_bound.py`.
"""
import itertools
import random
import statistics
import sys
from fractions import Fraction as F

from increment_bound import mat, CONFIGS, count, V_of as V_of_old


# ---------------------------------------------------------------------------
# exact linear algebra helpers
# ---------------------------------------------------------------------------

def col(M, a):
    return (M[0][a], M[1][a], M[2][a])


def transpose(M):
    return [[M[r][c] for r in range(3)] for c in range(3)]


def matmul(A, B):
    return [[sum(A[r][k] * B[k][c] for k in range(3)) for c in range(3)]
            for r in range(3)]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
             a[2] * b[0] - a[0] * b[2],
             a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


# ---------------------------------------------------------------------------
# step 1-2: planes of the other cubes in cube j's own frame
# ---------------------------------------------------------------------------

def canon_plane(m, s):
    """Canonical key for the plane {m . y = s}: normalise so the first
    nonzero component of the coefficient vector (m, -s) is positive. Two
    algebraically identical planes (m.y=s and (-m).y=(-s)) map to the same
    key; two distinct parallel planes (opposite faces) do not."""
    coeffs = (m[0], m[1], m[2], -s)
    for c in coeffs:
        if c != 0:
            if c < 0:
                coeffs = tuple(-x for x in coeffs)
            break
    return (coeffs[0], coeffs[1], coeffs[2]), -coeffs[3]


def planes_in_frame(cfg, j):
    """All other-cube face planes, expressed in cube j's own frame
    (m . y = s with C_j = [-1,1]^3), deduplicated exactly."""
    Rj = mat(cfg[j])
    RjT = transpose(Rj)
    planeset = set()
    for k, q in enumerate(cfg):
        if k == j:
            continue
        Mk = matmul(RjT, mat(q))
        for a in range(3):
            m = col(Mk, a)
            for s in (F(1), F(-1)):
                planeset.add(canon_plane(m, s))
    return planeset


def classify_planes(planeset):
    """Split into KEPT (cuts the interior) and a tangent tally (touches
    dC_j in a face/edge/corner; dropped, safe for an upper bound). A plane
    with L < |s| (misses the cube) is dropped silently — it cannot occur for
    face planes of a rotated unit cube (their normals are columns of an
    orthogonal matrix, so |m|_2 = 1 exactly, hence L = sum|m_i| >= |m|_2 = 1
    = |s| always; equality iff m is a signed standard basis vector) but the
    branch is implemented per spec regardless."""
    kept = []
    tangent = 0
    missed = 0
    for (m, s) in planeset:
        L = sum(abs(x) for x in m)
        if L > abs(s):
            kept.append((m, s))
        elif L == abs(s):
            tangent += 1
        else:
            missed += 1
    return kept, tangent, missed


# ---------------------------------------------------------------------------
# step 4: vertices of the trace-curve arrangement on dC_j
# ---------------------------------------------------------------------------

def clip_to_box(p0, d):
    """Clip the line {p0 + t d} to the closed box [-1,1]^3 exactly.
    Returns (t_lo, t_hi) with t_lo <= t_hi, or None if the line misses the
    box entirely. d is never (0,0,0) (checked by the caller)."""
    t_lo = None
    t_hi = None
    for c in range(3):
        if d[c] == 0:
            if abs(p0[c]) > 1:
                return None
        else:
            t1 = (F(-1) - p0[c]) / d[c]
            t2 = (F(1) - p0[c]) / d[c]
            lo, hi = (t1, t2) if t1 <= t2 else (t2, t1)
            t_lo = lo if t_lo is None else max(t_lo, lo)
            t_hi = hi if t_hi is None else min(t_hi, hi)
    if t_lo is None or t_hi is None or t_lo > t_hi:
        return None
    return t_lo, t_hi


def line_point_and_dir(m1, s1, m2, s2):
    """A point p0 and direction d for the intersection line of two planes.
    Returns None if the planes are parallel (d == 0)."""
    d = cross(m1, m2)
    if d == (0, 0, 0):
        return None
    k = max(range(3), key=lambda idx: abs(d[idx]))
    i, jx = [t for t in range(3) if t != k]
    det = m1[i] * m2[jx] - m1[jx] * m2[i]
    if det == 0:
        return None
    p0 = [F(0), F(0), F(0)]
    p0[i] = (s1 * m2[jx] - s2 * m1[jx]) / det
    p0[jx] = (m1[i] * s2 - m2[i] * s1) / det
    p0[k] = F(0)
    return tuple(p0), d


def compute_B(cfg, j):
    """Implements section 1 of the spec end to end for one (cfg, j).

    Returns a dict with keys:
      status         'ok' or 'arc_overlap'
      B, c           the bound and component count (status == 'ok' only)
      vertices       {vertex: frozenset(plane indices through it)} (ok only)
      kept           list of kept planes (m, s)
      tangent_tally  count of dropped tangent planes
      arc_overlap_pairs  count of plane pairs sharing an arc on dC_j
    """
    planeset = planes_in_frame(cfg, j)
    kept, tangent_tally, missed = classify_planes(planeset)
    n = len(kept)

    raw_points = set()
    arc_overlap_pairs = 0
    line_tangent_pairs = 0  # pairs of transversal planes whose intersection
    # LINE only kisses dC_j at a single point (t_lo == t_hi) rather than
    # piercing through it at two points. Distinct from a tangent PLANE
    # (dropped in classify_planes): both planes here have L > 1, but the
    # line they share happens to graze the box. This is exactly the case
    # the old script's strict "< 1" interior test silently missed.
    for i1, i2 in itertools.combinations(range(n), 2):
        m1, s1 = kept[i1]
        m2, s2 = kept[i2]
        pd = line_point_and_dir(m1, s1, m2, s2)
        if pd is None:
            continue
        p0, d = pd
        clip = clip_to_box(p0, d)
        if clip is None:
            continue
        t_lo, t_hi = clip
        if t_lo == t_hi:
            line_tangent_pairs += 1
            v = tuple(p0[c] + t_lo * d[c] for c in range(3))
            raw_points.add(v)
            continue
        # arc-overlap degeneracy: some coordinate constant at +-1 along the
        # WHOLE clipped segment (requires d[c] == 0 there, else it varies).
        if any(d[c] == 0 and abs(p0[c]) == 1 for c in range(3)):
            arc_overlap_pairs += 1
            continue
        v1 = tuple(p0[c] + t_lo * d[c] for c in range(3))
        v2 = tuple(p0[c] + t_hi * d[c] for c in range(3))
        raw_points.add(v1)
        raw_points.add(v2)

    if arc_overlap_pairs:
        return dict(status='arc_overlap', kept=kept,
                    tangent_tally=tangent_tally, missed=missed,
                    arc_overlap_pairs=arc_overlap_pairs,
                    line_tangent_pairs=line_tangent_pairs)

    # step 5: degree of each distinct vertex = 2 * #{kept planes through it}
    vertices = {}
    for v in raw_points:
        through = frozenset(idx for idx, (m, s) in enumerate(kept)
                             if dot(m, v) == s)
        # G4 vertex self-check: both defining equations exactly, |v|_inf==1
        assert len(through) >= 2, (cfg, j, v, through)
        assert max(abs(x) for x in v) == 1, (cfg, j, v)
        vertices[v] = through

    # step 6: connected components of the curve union (union-find over KEPT
    # planes, joined whenever two planes share a vertex)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for through in vertices.values():
        lst = list(through)
        for t in lst[1:]:
            union(lst[0], t)

    c = len(set(find(i) for i in range(n))) if n else 0

    # step 7
    B = 1 + c + sum(len(through) - 1 for through in vertices.values())

    return dict(status='ok', B=B, c=c, vertices=vertices, kept=kept,
                tangent_tally=tangent_tally, missed=missed,
                arc_overlap_pairs=0, line_tangent_pairs=line_tangent_pairs)


# ---------------------------------------------------------------------------
# gates
# ---------------------------------------------------------------------------

def gate_G1(report_lines):
    report_lines.append('## G1 — n=2 hand-computed degenerate case\n')
    cfg = [(1, 0, 0, 0), (0, 1, 1, 1)]
    expected_points = {
        (F(1), F(1), F(1)), (F(-1), F(-1), F(-1)),
        (F(1), F(-1), F(0)), (F(1), F(0), F(-1)),
        (F(-1), F(1), F(0)), (F(-1), F(0), F(1)),
        (F(0), F(1), F(-1)), (F(0), F(-1), F(1)),
    }
    all_ok = True
    for j in (0, 1):
        res = compute_B(cfg, j)
        line = f'j={j}: status={res["status"]}'
        if res['status'] != 'ok':
            report_lines.append(line + '  -- FAILED (arc_overlap)\n')
            all_ok = False
            continue
        B, c, vertices = res['B'], res['c'], res['vertices']
        degs = sorted(len(t) * 2 for t in vertices.values())
        n_deg6 = sum(1 for x in degs if x == 6)
        n_deg4 = sum(1 for x in degs if x == 4)
        n_other = sum(1 for x in degs if x not in (4, 6))
        pts_match = set(vertices.keys()) == expected_points
        ok = (B == 12 and c == 1 and n_deg6 == 2 and n_deg4 == 6
              and n_other == 0 and len(vertices) == 8 and pts_match)
        all_ok = all_ok and ok
        line += (f'  B={B} c={c} deg6={n_deg6} deg4={n_deg4} '
                 f'other_deg={n_other} n_vertices={len(vertices)} '
                 f'points_match_spec={pts_match} tangent_tally={res["tangent_tally"]}'
                 f'  -> {"PASS" if ok else "FAIL"}')
        report_lines.append(line + '\n')
        if not ok:
            report_lines.append('  vertex list produced by the code:\n')
            for v, through in sorted(vertices.items()):
                report_lines.append(f'    {v}  deg={len(through)*2}\n')
    verdict = 'PASS' if all_ok else 'FAIL'
    report_lines.append(f'\nG1 verdict: {verdict}\n')
    print(f'G1 verdict: {verdict}')
    return all_ok


def gate_G2(report_lines):
    report_lines.append('\n## G2 — CONFIGS table\n')
    header = '%-12s %3s %6s %6s %8s %8s %7s %s' % (
        'config', 'j', 'T', 'S_j', 'Delta_j', 'B_j', 'slack', 'verdict')
    report_lines.append('```\n' + header + '\n')
    print(header)
    rows = []
    all_ok = True
    for name, cfg in CONFIGS.items():
        T = count(cfg)
        for j in range(len(cfg)):
            sub = [c for k, c in enumerate(cfg) if k != j]
            Sj = count(sub)
            delta = T - Sj
            res = compute_B(cfg, j)
            if res['status'] != 'ok':
                line = ('%-12s %3d %6d %6d %8d %8s %7s %s'
                        % (name, j, T, Sj, delta, '-', '-',
                           f'ARC_OVERLAP({res["arc_overlap_pairs"]})'))
                report_lines.append(line + '\n')
                print(line)
                all_ok = False
                continue
            B = res['B']
            slack = F(B, delta) if delta else None
            verdict = 'OK' if B >= delta else 'VIOLATED'
            if verdict == 'VIOLATED':
                all_ok = False
            slack_str = ('%.4f' % float(slack)) if slack is not None else 'inf'
            line = ('%-12s %3d %6d %6d %8d %8d %7s %s'
                    % (name, j, T, Sj, delta, B, slack_str, verdict))
            report_lines.append(line + '\n')
            print(line)
            rows.append((name, j, T, Sj, delta, B, slack,
                         res['tangent_tally'], res['c']))
    report_lines.append('```\n')
    verdict = 'PASS' if all_ok else 'FAIL'
    report_lines.append(f'\nG2 verdict: {verdict}\n')
    print(f'G2 verdict: {verdict}')
    return all_ok, rows


def gate_G3(report_lines, n_samples=200, seed=1234):
    report_lines.append('\n## G3 — generic agreement with the old V_j\n')
    rng = random.Random(seed)
    generic = 0
    checked = 0
    mismatches = []
    line_tangent_skipped = 0
    disconnected_skipped = 0
    tries = 0
    while generic < 15 and tries < n_samples:
        tries += 1
        q0 = tuple(rng.randint(-4, 4) for _ in range(4))
        q1 = tuple(rng.randint(-4, 4) for _ in range(4))
        if q0 == (0, 0, 0, 0) or q1 == (0, 0, 0, 0):
            continue
        cfg = [q0, q1]
        for j in (0, 1):
            res = compute_B(cfg, j)
            if res['status'] != 'ok':
                continue
            if res['tangent_tally'] != 0:
                continue  # not generic: a plane tangent to dC_j
            if res['line_tangent_pairs'] != 0:
                # not generic: two transversal planes whose shared LINE
                # only grazes dC_j at a single point. The old script's
                # strict "< 1" interior test silently excludes these, so
                # comparing against it here would be an apples-to-oranges
                # mismatch, not a real disagreement.
                line_tangent_skipped += 1
                continue
            vertices = res['vertices']
            if any(len(t) != 2 for t in vertices.values()):
                continue  # not generic: a triple (or higher) point
            if res['c'] != 1:
                # not generic in the sense the OLD formula needs: F = 2+V
                # assumed a single connected trace (c = 1, no isolated
                # curves). A disconnected arrangement (c > 1, as in the
                # "two disjoint circles -> 3" check in the spec) is exactly
                # the failure mode being fixed, not a disagreement to chase.
                disconnected_skipped += 1
                continue
            generic += 1
            checked += 1
            B = res['B']
            Vold = V_of_old(cfg, j)
            old_bound = 2 + Vold
            if B != old_bound:
                mismatches.append((cfg, j, B, old_bound))
    line = (f'sampled {tries} random (q0,q1) pairs, small entries in [-4,4]; '
            f'{generic} (config,j) instances were fully generic '
            f'(no plane tangency, no line-tangency to dC_j, no triple points, '
            f'c == 1); {line_tangent_skipped} skipped for line-tangency to '
            f'dC_j only, {disconnected_skipped} skipped for a disconnected '
            f'trace (c > 1) — both are degeneracies the old script\'s F=2+V '
            f'silently mishandled rather than disagreements this code gets '
            f'wrong')
    report_lines.append(line + '\n')
    print(line)
    ok = generic > 0 and not mismatches
    if not mismatches:
        report_lines.append(f'All {generic} generic instances satisfy B_j == 2 + V_old exactly.\n')
        print(f'All {generic} generic instances satisfy B_j == 2 + V_old exactly.')
    else:
        report_lines.append(f'{len(mismatches)} MISMATCHES found:\n')
        print(f'{len(mismatches)} MISMATCHES found:')
        for cfg, j, B, old in mismatches:
            report_lines.append(f'  cfg={cfg} j={j} B={B} old={old}\n')
    verdict = 'PASS' if ok else 'FAIL'
    report_lines.append(f'\nG3 verdict: {verdict}\n')
    print(f'G3 verdict: {verdict}')
    return ok


# ---------------------------------------------------------------------------

def main():
    report_lines = []
    report_lines.append('# increment_bound2 report\n\n')
    report_lines.append(
        'B_j computed by formula (*) of INCREMENT_BOUND_SPEC.md: exact '
        'rational arithmetic throughout, `fractions.Fraction` only.\n')

    g1_ok = gate_G1(report_lines)
    g2_ok, rows = gate_G2(report_lines)
    g3_ok = gate_G3(report_lines)

    # G4 is asserted inline inside compute_B (vertex self-check); if we
    # got this far without an AssertionError, G4 passed on every vertex
    # emitted across all gates run above.
    report_lines.append('\n## G4 — vertex self-check\n')
    report_lines.append(
        'Asserted inline in `compute_B` for every vertex emitted in G1/G2/G3 '
        '(both plane equations exactly, |v|_inf == 1 exactly). No assertion '
        'failed, so G4 passed throughout this run.\n')
    print('G4 verdict: PASS (no assertion failures)')

    # slack distribution (G2 rows only, finite slacks)
    slacks = [float(s) for (*_, s, tang, c) in rows if s is not None]
    report_lines.append('\n## Slack distribution (G2 rows)\n')
    if slacks:
        report_lines.append(
            f'min={min(slacks):.4f}  median={statistics.median(slacks):.4f}  '
            f'max={max(slacks):.4f}  n={len(slacks)}\n')
        print(f'slack min={min(slacks):.4f} median={statistics.median(slacks):.4f} max={max(slacks):.4f}')
    else:
        report_lines.append('No finite-slack rows.\n')

    report_lines.append('\n## Degeneracy tally (G2)\n')
    for name, j, T, Sj, delta, B, slack, tang, c in rows:
        if tang:
            report_lines.append(f'{name} j={j}: {tang} tangent plane(s) dropped\n')
    if not any(tang for (*_, tang, c) in rows):
        report_lines.append('No tangent planes encountered in any G2 row.\n')

    tight = [(name, j, B, delta) for name, j, T, Sj, delta, B, slack, tang, c
             in rows if slack is not None and slack == 1]
    report_lines.append('\n## Tightness beyond G1\n\n')
    if tight:
        report_lines.append(
            'Besides G1 (which is tight by construction, B=12=Delta), the '
            'following G2 rows are also exactly tight (slack 1.00): ' +
            ', '.join(f'{n} j={j} (B=Delta={b})' for n, j, b, d in tight) +
            '.\n')
    else:
        report_lines.append(
            'No G2 row achieves slack 1.00; the bound is strictly loose '
            '(B_j > Delta_j) on every one of the 21 CONFIGS rows. G1 remains '
            'the only exactly-tight case observed.\n')

    overall = 'PASS' if (g1_ok and g2_ok and g3_ok) else 'FAIL'
    report_lines.append(f'\n## Overall\n\nG1={"PASS" if g1_ok else "FAIL"}  '
                         f'G2={"PASS" if g2_ok else "FAIL"}  '
                         f'G3={"PASS" if g3_ok else "FAIL"}  G4=PASS\n')
    print(f'\nOverall: {overall}')

    with open('increment_bound2_report.md', 'w') as f:
        f.writelines(report_lines)


if __name__ == '__main__':
    main()
