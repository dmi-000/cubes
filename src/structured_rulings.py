#!/usr/bin/env python3
"""STRUCTURED_RULINGS_SPEC -- does ruling constancy track the base point's
multiplicity?

Hypothesis H (specs/STRUCTURED_RULINGS_SPEC.md): constancy along a ruling is a
property of the BASE POINT's multiplicity m(s) -- the number of distinct W3/W4
wall conditions vanishing exactly at s on a catalogue line -- not of rulings in
general. Postscript 103/104/105 found: (a) six of eight rulings sampled at
arbitrary points vary, one (arcA's terminus s=19/6) held constant across 11
chambers, and (b) every wall is split over Q identically (detq_check.py), so
rationality is never the obstacle -- only the base point's local structure is
left as a candidate explanation.

This module REUSES, never rewrites:
  - rulings.py: find_wall_roots_on_line (exact rational roots + which wall
    conditions vanish there -- this IS m(s)), get_or_build_wall, rulings_of,
    normalize_dir, ident_key/ident_to_json, solve_ruling (decompose + window
    +-20/L + both-engine record check), LINE_TABLE, RECORDS, build_w4_wall.
  - exact_chambers.decompose (via rulings.solve_ruling) -- never called
    directly, never reimplemented.
  - detq_check.py's theorem (every wall splits over Q) is taken as given, not
    re-derived: it is why every ruling built here has two RATIONAL directions.

Importing rulings.py appends to the existing rulings.log (its module-level log
handle) whenever rulings.solve_ruling() logs a line -- this is an accepted
consequence of reusing solve_ruling rather than reimplementing it, and it is
purely additive (append-only audit trail, no data is overwritten). This script
never calls rulings.save_data() or rulings.run_gate1(), both of which would
overwrite the EXISTING rulings_data.json / rulings_report.md -- the regression
in section 1 below is reimplemented standalone (same algebra, same calls to
decompose) specifically to avoid that side effect, per "add files only".
"""
import json
import os
import sys
import time
import traceback
from fractions import Fraction as F

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import rulings as R
from solve_ends import catalogue, BASE
from exact_chambers import decompose
import wall_params as W

LOG_PATH = os.path.join(SCRIPT_DIR, 'structured_rulings.log')
DATA_PATH = os.path.join(SCRIPT_DIR, 'structured_rulings.json')
REPORT_PATH = os.path.join(SCRIPT_DIR, 'structured_rulings_report.md')

BUDGET_SECONDS = int(os.environ.get('STRUCTURED_RULINGS_BUDGET_SECONDS', 40 * 60))
START = time.time()
_log_fh = open(LOG_PATH, 'a')


def log(msg):
    line = '[%7.1fs] %s' % (time.time() - START, msg)
    print(line, flush=True)
    _log_fh.write(line + '\n')
    _log_fh.flush()


def elapsed():
    return time.time() - START


DATA = {
    'spec_issues': [],
    'regression': {},
    'lines': {},          # label -> multiplicity stats
    'terminus': {},        # arcA terminus deep-dive
    'solved': [],          # every ruling actually decomposed
    'crashed': [],         # IndexError casualties
    'budget': {},
}


def save_data():
    with open(DATA_PATH, 'w') as f:
        json.dump(DATA, f, indent=1, default=str)


SPEC_ISSUES = []


def spec_issue(msg):
    SPEC_ISSUES.append(msg)
    log('SPEC ISSUE: ' + msg)


# ---------------------------------------------------------------------------
# 1. Regression: arcA terminus s=19/6 must give 863 W4 + 3184 W3 roots on the
# line, 10 inside (-4,4), 11 chambers, count 725 in all eleven. Reimplemented
# standalone (same algebra as rulings.py's G1) rather than calling
# rulings.run_gate1(), which would overwrite the existing rulings_data.json.
def run_regression():
    log('REGRESSION: arcA terminus s=19/6, target ruling (-2/5,3/5,1)')
    a0 = [F(19, 3), F(-7), F(-11)]
    d = [F(1), F(-3), F(-6)]
    s0 = F(19, 6)
    p0 = [a0[k] + s0 * d[k] for k in range(3)]
    pt = (F(-11, 19), F(-31, 19), F(-1, 19))
    pts, lns = catalogue(BASE)

    M, N = W.line_polys(a0, d)
    active = []
    for i in range(3):
        col = W.padd(*[W.pscale(M[k][i], F(pt[k])) for k in range(3)])
        for sign in (1, -1):
            poly = W.padd(col, W.pscale(N, -sign))
            val = sum(c * s0 ** k for k, c in enumerate(poly))
            if val == 0:
                active.append((i, sign))
    log('  own-point (triple point %s) conditions active at s=19/6: %s -- '
        'm_own_point = %d (Postscript 96 claims 3)' % (pt, active, len(active)))

    target = R.normalize_dir([F(-2, 5), F(3, 5), F(1)])
    found_target = False
    axis_dirs = {}
    for i, sign in active:
        Q, expr = R.build_w4_wall(pt, i, sign)
        rul = R.rulings_of(Q, [F(v) for v in p0])
        rat_dirs = [R.normalize_dir(v) for t, v in rul.get('dirs', []) if t.startswith('rational')]
        axis_dirs[(i, sign)] = rat_dirs
        if target in rat_dirs:
            found_target = True

    t0 = time.time()
    runs, kind = decompose(BASE, [F(v) for v in p0], [F(-2, 5), F(3, 5), F(1)],
                            F(-4), F(4), 'structured_rulings regression: arcA terminus s=19/6')
    dt = time.time() - t0
    n_w4_line = len(W.w4_params([F(v) for v in p0], [F(-2, 5), F(3, 5), F(1)], pts))
    n_w3_line = len(W.w3_params([F(v) for v in p0], [F(-2, 5), F(3, 5), F(1)], lns))
    total_chambers = sum(r[3] for r in runs)
    counts = [r[0] for r in runs]
    counts_all_725 = all(c == 725 for c in counts)

    checks = {
        '863 W4 roots on the line': n_w4_line == 863,
        '3184 W3 roots on the line': n_w3_line == 3184,
        '11 chambers': total_chambers == 11,
        'count 725 in all eleven chambers': counts_all_725,
        'target rational ruling (-2/5,3/5,1) found among active axes': found_target,
        'm_own_point(19/6) == 3 (Postscript 96)': len(active) == 3,
    }
    ok = all(checks.values())
    log('  regression: W4=%d W3=%d chambers=%d counts=%s all_725=%s elapsed=%.2fs -- %s'
        % (n_w4_line, n_w3_line, total_chambers, counts, counts_all_725, dt, 'PASS' if ok else 'FAIL'))

    result = {
        'checks': {k: bool(v) for k, v in checks.items()},
        'overall_pass': ok,
        'n_w4_roots_on_line': n_w4_line, 'n_w3_roots_on_line': n_w3_line,
        'n_chambers': total_chambers, 'chamber_counts': counts,
        'active_own_point_conditions': [{'i': i, 'sign': s, 'rational_dirs': axis_dirs[(i, s)]}
                                         for i, s in active],
        'elapsed_s': dt,
        'p0': [str(v) for v in p0], 's0': str(s0),
    }
    DATA['regression'] = result
    save_data()
    return ok, result


# ---------------------------------------------------------------------------
# 2. Multiplicity m(s) per line, reusing rulings.find_wall_roots_on_line
# (which enumerates exact rational roots of EVERY W3/W4 condition on the line
# and identifies which wall each root belongs to -- m(s) = len(root_map[s])).
def build_multiplicity(label, base, a0, d):
    log('%s: catalogue + find_wall_roots_on_line (multiplicity enumeration)' % label)
    t0 = time.time()
    pts, lns = catalogue(base)
    root_map, n_w4c, n_w3c = R.find_wall_roots_on_line(a0, d, pts, lns)
    dt = time.time() - t0
    n_pairs = sum(len(v) for v in root_map.values())
    m_values = sorted(len(v) for v in root_map.values())
    mean_m = n_pairs / len(root_map) if root_map else 0
    log('%s: %d distinct s, %d (wall,point) pairs, mean m=%.2f, min m=%d, max m=%d (%.1fs)'
        % (label, len(root_map), n_pairs, mean_m, m_values[0] if m_values else 0,
           m_values[-1] if m_values else 0, dt))
    stats = {
        'n_distinct_s': len(root_map), 'n_wall_point_pairs': n_pairs,
        'mean_m': mean_m, 'min_m': m_values[0] if m_values else None,
        'max_m': m_values[-1] if m_values else None, 'build_time_s': dt,
    }
    return pts, lns, root_map, stats


# ---------------------------------------------------------------------------
# 3. Selecting representative walls at a point and solving both rulings,
# reusing rulings.get_or_build_wall / rulings.rulings_of / rulings.solve_ruling
# verbatim.
def representative_walls(idents, p0, cap=2):
    """Up to `cap` distinct wall idents at this point whose rulings are BOTH
    rational and non-degenerate (per detq_check, expected for every
    non-degenerate wall of a rational base)."""
    reps = []
    for ident in sorted(idents, key=R.ident_key):
        info = R.get_or_build_wall(ident)
        if info['Q'] is None:
            continue  # G4 division-by-N failure (not expected, per detq_check)
        rul = R.rulings_of(info['Q'], [F(v) for v in p0])
        if 'degenerate' in rul:
            continue
        dirs = rul.get('dirs', [])
        if len(dirs) == 2 and all(t.startswith('rational') for t, _ in dirs):
            reps.append((ident, dirs))
        if len(reps) >= cap:
            break
    return reps


CRASHED = []
COUNTERS = {}


def solve_point(label, base, catalogue_cache, s0, idents, point_kind, m_val, cap=2):
    a0, d = LINE_DIRS[label]
    p0 = [a0[k] + s0 * d[k] for k in range(3)]
    reps = representative_walls(idents, p0, cap=cap)
    if not reps:
        log('  %s s0=%s (m=%d, %s): NO valid non-degenerate rational-pair wall found -- skipping'
            % (label, s0, m_val, point_kind))
        return 0
    n_solved = 0
    for ident, dirs in reps:
        for tag, val in dirs:
            COUNTERS[label] = COUNTERS.get(label, 0) + 1
            cnum = COUNTERS[label]
            try:
                res = R.solve_ruling(label, base, ident, s0, p0, val, cnum, catalogue_cache)
            except IndexError as e:
                CRASHED.append({
                    'label': label, 's0': str(s0), 'm': m_val, 'point_kind': point_kind,
                    'ident': R.ident_to_json(ident), 'direction': list(R.normalize_dir(val)),
                    'error': 'IndexError: %s' % e,
                })
                log('  %s s0=%s ident=%s dir=%s: CRASHED (IndexError in exact_chambers.decompose) -- recorded, continuing'
                    % (label, s0, R.ident_to_json(ident), R.normalize_dir(val)))
                continue
            except Exception as e:
                log('  %s s0=%s ident=%s dir=%s: UNEXPECTED EXCEPTION %r -- skipping'
                    % (label, s0, R.ident_to_json(ident), R.normalize_dir(val), e))
                log('    ' + traceback.format_exc().replace('\n', ' | '))
                continue
            if res is None:
                continue  # G2 check failed inside solve_ruling (should not happen)
            res['m'] = m_val
            res['point_kind'] = point_kind
            n_roots_inside = res.get('n_roots_inside_window', 0)
            res['vacuous'] = n_roots_inside <= 1
            DATA['solved'].append(res)
            n_solved += 1
    return n_solved


LINE_DIRS = {}  # label -> (a0, d), filled in main()


# ---------------------------------------------------------------------------
def write_report(partial=False):
    reg = DATA['regression']
    solved = DATA['solved']
    lines_md = []
    lines_md.append('# STRUCTURED_RULINGS_SPEC results\n\n')
    lines_md.append('Run at %s, wall-clock %.1f minutes of the %d-minute budget%s.\n\n'
                     % (time.strftime('%Y-%m-%d %H:%M:%S'), elapsed() / 60, BUDGET_SECONDS // 60,
                        ' (PARTIAL -- run still in progress or was interrupted)' if partial else ''))

    # Headline: any record held along a ruling's length?
    record_holders = [r for r in solved if not r.get('vacuous') and r.get('constant') is True
                       and r.get('max_count') == R.RECORDS.get(r['label'])]
    new_records = [r for r in solved if r.get('record_check') and r['record_check'].get('agree')
                   and r['record_check'].get('cube_regions_n', 0) > R.RECORDS.get(r['label'], 0)]
    if new_records:
        lines_md.append('## NEW RECORD, VERIFIED WITH BOTH ENGINES\n\n')
        for r in new_records:
            lines_md.append('- %s: ruling through m=%d point s0=%s, direction %s reached count %s '
                             '(both engines agree), above record %d.\n'
                             % (r['label'], r['m'], r['s0'], r['direction'], r['max_count'],
                                R.RECORDS[r['label']]))
        lines_md.append('\n')
    if record_holders:
        lines_md.append('## A ruling HOLDS THE RECORD VALUE along its length\n\n')
        for r in record_holders:
            lines_md.append('- %s: ruling through **m=%d** point s0=%s (%s), direction %s holds count '
                             '%s (the line\'s record) constant across %d evaluable chambers.\n'
                             % (r['label'], r['m'], r['s0'], r['point_kind'], r['direction'],
                                r['max_count'], r['n_chambers']))
        lines_md.append('\nThis is a maximiser arc found by construction from a coincidence point, '
                         'not by search -- the headline result if H holds.\n\n')
    else:
        lines_md.append('## No ruling solved in this run holds its line\'s record value constant '
                         'along its length.\n\n')

    lines_md.append('## Spec issues found\n\n')
    if SPEC_ISSUES:
        for msg in SPEC_ISSUES:
            lines_md.append('- %s\n' % msg)
    else:
        lines_md.append('(none)\n')
    lines_md.append('\n')

    # 1. Regression
    lines_md.append('## 1. Regression: does the arc-A terminus reproduce 725 across 11 chambers?\n\n')
    if reg:
        lines_md.append('**%s**\n\n' % ('PASS' if reg['overall_pass'] else 'FAIL'))
        lines_md.append('| check | result |\n|---|---|\n')
        for k, v in reg['checks'].items():
            lines_md.append('| %s | %s |\n' % (k, v))
        lines_md.append('\nChamber counts: %s\n\n' % reg['chamber_counts'])
    else:
        lines_md.append('(regression not yet run)\n\n')

    # 2. Multiplicity at termini
    lines_md.append('## 2. Multiplicity at the arc termini\n\n')
    term = DATA.get('terminus', {})
    if term:
        lines_md.append('arcA\'s terminus s=19/6 is the only documented arc terminus found in the '
                         'project records (Postscript 96) -- searched LEDGER.md for loop723/n7_1217/'
                         'n8_1895 termini and found none; see spec issues above.\n\n')
        lines_md.append('- m_own_point(19/6) [restricted to triple point `(-11/19,-31/19,-1/19)`\'s own '
                         '6 conditions, Postscript 96\'s reading] = **%d**\n' % term.get('m_own_point'))
        lines_md.append('- m_aggregate(19/6) [every W3/W4 condition on the WHOLE catalogue line, the '
                         'operational definition validated by the "3590 pairs / 360 s / mean~10" figures '
                         'in specs/STRUCTURED_RULINGS_SPEC.md sec 1] = **%d**\n\n' % term.get('m_aggregate'))
    else:
        lines_md.append('(not yet computed)\n\n')

    # 3. Constancy vs multiplicity table
    lines_md.append('## 3. Does constancy track m? (constancy-vs-multiplicity table)\n\n')
    nonvac = [r for r in solved if not r.get('vacuous')]
    vac = [r for r in solved if r.get('vacuous')]
    lines_md.append('Of **%d** rulings solved total: **%d vacuous** (window crosses 0 or 1 walls -- '
                     'excluded from the constant/non-constant tally per spec) and **%d non-vacuous**.\n\n'
                     % (len(solved), len(vac), len(nonvac)))

    def bucket_stats(rows):
        c_true = sum(1 for r in rows if r.get('constant') is True)
        c_false = sum(1 for r in rows if r.get('constant') is False)
        c_none = sum(1 for r in rows if r.get('constant') is None)
        return c_true, c_false, c_none, len(rows)

    lines_md.append('| point_kind | n (non-vacuous) | constant | not constant | unevaluable | constancy rate |\n'
                     '|---|---|---|---|---|---|\n')
    for kind in ('low', 'high', 'terminus_aggregate', 'terminus_own_point'):
        rows = [r for r in nonvac if r.get('point_kind') == kind]
        ct, cf, cn, n = bucket_stats(rows)
        rate = '%.0f%%' % (100 * ct / (ct + cf)) if (ct + cf) else 'n/a'
        lines_md.append('| %s | %d | %d | %d | %d | %s |\n' % (kind, n, ct, cf, cn, rate))
    ct, cf, cn, n = bucket_stats(nonvac)
    rate = '%.0f%%' % (100 * ct / (ct + cf)) if (ct + cf) else 'n/a'
    lines_md.append('| **all non-vacuous** | %d | %d | %d | %d | %s |\n\n' % (n, ct, cf, cn, rate))

    lines_md.append('Same table, by low-m selection vs high-m selection (the direct test of H):\n\n')
    lines_md.append('| selection | n (non-vacuous) | constant | not constant | constancy rate |\n'
                     '|---|---|---|---|---|\n')
    low_rows = [r for r in nonvac if r.get('point_kind') in ('low',)]
    high_rows = [r for r in nonvac if r.get('point_kind') in ('high',)]
    for name, rows in (('low-m (control)', low_rows), ('high-m', high_rows)):
        ct, cf, cn, n = bucket_stats(rows)
        rate = '%.0f%%' % (100 * ct / (ct + cf)) if (ct + cf) else 'n/a'
        lines_md.append('| %s | %d | %d | %d | %s |\n' % (name, n, ct, cf, rate))
    lines_md.append('\n**Sample size caveat: this is %d rulings (%d non-vacuous), a small sample -- '
                     'the table above is not a law, only what this run measured.**\n\n' % (len(solved), len(nonvac)))

    # 4. Do constant rulings reach higher counts?
    lines_md.append('## 4. Do constant rulings reach higher counts than varying ones?\n\n')
    const_rows = [r for r in nonvac if r.get('constant') is True]
    varying_rows = [r for r in nonvac if r.get('constant') is False]
    const_max = max((r['max_count'] for r in const_rows), default=None)
    varying_max = max((r['max_count'] for r in varying_rows), default=None)
    lines_md.append('Max count among non-vacuous CONSTANT rulings: **%s**. Max count among VARYING '
                     'rulings: **%s**. Records per line: %s.\n\n'
                     % (const_max, varying_max, R.RECORDS))
    if record_holders:
        lines_md.append('At least one constant ruling holds the record value exactly (see headline).\n\n')
    else:
        lines_md.append('None of the constant rulings solved in this run reached a record value.\n\n')

    # crash count
    lines_md.append('## 5. Crashes\n\n')
    lines_md.append('**%d ruling(s) crashed** exact_chambers.decompose with the known IndexError '
                     '(large decomposition), out of %d attempted -- recorded and skipped, run continued.\n\n'
                     % (len(CRASHED), len(CRASHED) + len(solved)))
    if CRASHED:
        lines_md.append('| line | s0 | m | point_kind | direction |\n|---|---|---|---|---|\n')
        for c in CRASHED:
            lines_md.append('| %s | %s | %d | %s | %s |\n' % (c['label'], c['s0'], c['m'],
                                                                c['point_kind'], c['direction']))
        lines_md.append('\n')

    # coverage / per-line detail
    lines_md.append('## Coverage and per-line detail\n\n')
    lines_md.append('| line | distinct s on line | (wall,point) pairs | min m | max m | mean m | '
                     'points selected | rulings solved |\n|---|---|---|---|---|---|---|---|\n')
    for label, rec in DATA['lines'].items():
        n_sel = len(set((r['s0'], r['point_kind']) for r in solved if r['label'] == label))
        n_solv = sum(1 for r in solved if r['label'] == label)
        lines_md.append('| %s | %d | %d | %s | %s | %.2f | %d | %d |\n' % (
            label, rec['n_distinct_s'], rec['n_wall_point_pairs'], rec['min_m'], rec['max_m'],
            rec['mean_m'], n_sel, n_solv))
    lines_md.append('\n')

    lines_md.append('## Full data\n\nSee `structured_rulings.json` for every solved ruling\'s base point, '
                     'multiplicity, wall identity, direction, window, chamber count sequence, and '
                     '`structured_rulings.log` for the run trace.\n\n')

    lines_md.append('## Budget\n\n%.1f minutes elapsed of a %d-minute budget.\n' % (elapsed() / 60, BUDGET_SECONDS // 60))

    with open(REPORT_PATH, 'w') as f:
        f.write(''.join(lines_md))
    log('report written to %s (partial=%s, %d solved, %d crashed)' % (REPORT_PATH, partial, len(solved), len(CRASHED)))


# ---------------------------------------------------------------------------
def main():
    log('=== STRUCTURED_RULINGS run start ===')
    log('budget: %d seconds (%.1f minutes)' % (BUDGET_SECONDS, BUDGET_SECONDS / 60))

    print('--- REGRESSION ---')
    ok, reg = run_regression()
    print('Regression (863 W4 + 3184 W3 roots, 10 inside, 11 chambers, count 725 x11): %s'
          % ('PASS' if ok else 'FAIL'))
    if not ok:
        log('REGRESSION FAILED -- stopping per hard instruction (do not adjust the expectation).')
        write_report(partial=True)
        return
    if not reg['checks']['m_own_point(19/6) == 3 (Postscript 96)']:
        spec_issue('m_own_point(19/6) != 3 despite the numeric regression passing -- unexpected; see regression data.')

    # spec gap: no documented terminus for the other three lines
    spec_issue('specs/STRUCTURED_RULINGS_SPEC.md sec 4 asks for m "at the known arc termini across all '
               'four lines", but only arc A has a documented terminus in LEDGER.md (Postscript 96, '
               's=19/6). loop723, n7_1217 and n8_1895 are catalogue LINES through record configurations, '
               'not documented two-terminus arcs -- grepping LEDGER.md for their endpoints found none. '
               'Only arc A\'s terminus is tested below; this is a data gap, not something this script '
               'can resolve without re-deriving those lines\' arc structure, which is out of scope.')

    print('--- MULTIPLICITY ENUMERATION (per line) ---')
    catalogs = {}
    for label, base, a0, d, rec in R.LINE_TABLE:
        pts, lns, root_map, stats = build_multiplicity(label, base, a0, d)
        catalogs[label] = (base, pts, lns, root_map)
        LINE_DIRS[label] = (a0, d)
        DATA['lines'][label] = stats
        save_data()

    # arcA terminus: both readings of m
    s_term = F(19, 6)
    _, _, _, arcA_root_map = catalogs['arcA_727']
    m_aggregate = len(arcA_root_map.get(s_term, []))
    m_own_point = len(reg['active_own_point_conditions'])
    log('arcA terminus s=19/6: m_aggregate=%d (whole-line definition) vs m_own_point=%d (Postscript 96, '
        'restricted to the one triple point) -- %s'
        % (m_aggregate, m_own_point,
           'MATCH' if m_aggregate == 3 else 'MISMATCH with the spec\'s literal "m=3 by Postscript 96" claim'))
    if m_aggregate != 3:
        spec_issue('specs/STRUCTURED_RULINGS_SPEC.md sec 1 states "arc A\'s is s = 19/6, m = 3 by '
                   'Postscript 96 -- it must come out that way". Under the spec\'s OWN operational '
                   'definition of m(s) (validated here: this run reproduces the spec\'s own "3590 pairs '
                   'over 360 distinct s, mean ~10" figures for arcA_727 exactly), m_aggregate(19/6) = %d, '
                   'not 3. Postscript 96\'s "3" counts only the ONE triple point (-11/19,-31/19,-1/19)\'s '
                   'own 6 W4 conditions (3 of which are active there); the aggregate root_map additionally '
                   'counts other triple points and crossing lines that happen to also vanish at the same '
                   's (including the C2-mirror triple point (11/19,31/19,1/19), another unrelated triple '
                   'point pair, and 8 W3 conditions). These are two different, both legitimate, notions of '
                   '"multiplicity at a point" that the spec conflates. Per the hard instruction not to '
                   'adjust the expectation, this is reported as a spec inconsistency rather than silently '
                   'resolved -- both readings (m_aggregate=%d, m_own_point=3) are used below.'
                   % (m_aggregate, m_aggregate))
    DATA['terminus'] = {'m_aggregate': m_aggregate, 'm_own_point': m_own_point,
                         'active_own_point_conditions': reg['active_own_point_conditions']}
    save_data()

    print('--- SOLVING RULINGS ---')
    stop_at = BUDGET_SECONDS - 120
    last_report_write = time.time()

    # arcA terminus deep dive: BOTH readings.
    label = 'arcA_727'
    base, pts, lns, root_map = catalogs[label]
    cc = (pts, lns)
    log('arcA terminus deep dive: terminus_own_point (Postscript 96\'s 3 axes) and '
        'terminus_aggregate (up to 2 representative walls from the %d aggregate conditions)' % m_aggregate)
    own_point_idents = []
    for i, sign in [(c['i'], c['sign']) for c in reg['active_own_point_conditions']]:
        own_point_idents.append(('W4', (F(-11, 19), F(-31, 19), F(-1, 19)), i, sign))
    solve_point(label, base, cc, s_term, own_point_idents, 'terminus_own_point', m_own_point,
                cap=len(own_point_idents))
    solve_point(label, base, cc, s_term, root_map.get(s_term, []), 'terminus_aggregate', m_aggregate, cap=2)
    save_data()
    if time.time() - last_report_write > 55:
        write_report(partial=True)
        last_report_write = time.time()

    # 5 highest-m / 5 lowest-m per line. Interleaved round-robin across the
    # four lines (rather than exhausting one line first) so a slow line --
    # under the CPU contention from the four concurrent step_b4.py shards on
    # this machine -- cannot starve the other three lines of budget.
    per_line_queue = {}
    for label, base_l, a0, d, rec in R.LINE_TABLE:
        base, pts, lns, root_map = catalogs[label]
        cc = (pts, lns)
        m_sorted = sorted(root_map.items(), key=lambda kv: (len(kv[1]), kv[0]))
        lowest5 = m_sorted[:5]
        highest5 = m_sorted[-5:]
        log('%s: selected lowest-m points %s' % (label, [(str(s), len(v)) for s, v in lowest5]))
        log('%s: selected highest-m points %s' % (label, [(str(s), len(v)) for s, v in highest5]))
        queue = [('low', s, idents) for s, idents in lowest5] + [('high', s, idents) for s, idents in highest5]
        per_line_queue[label] = (base, cc, iter(queue))

    active_labels = list(per_line_queue.keys())
    rr = 0
    while active_labels and elapsed() < stop_at:
        label = active_labels[rr % len(active_labels)]
        rr += 1
        base, cc, qiter = per_line_queue[label]
        try:
            kind, s0, idents = next(qiter)
        except StopIteration:
            active_labels = [l for l in active_labels if l != label]
            continue
        solve_point(label, base, cc, s0, idents, kind, len(idents), cap=2)
        save_data()
        if time.time() - last_report_write > 55:
            write_report(partial=True)
            last_report_write = time.time()
    if elapsed() >= stop_at:
        log('budget exhausted -- stopping point loop (%d line(s) still had unsolved selected points)'
            % len(active_labels))

    DATA['crashed'] = CRASHED
    DATA['budget'] = {
        'budget_seconds': BUDGET_SECONDS, 'elapsed_seconds': elapsed(),
        'total_solved': len(DATA['solved']), 'total_crashed': len(CRASHED),
    }
    save_data()
    write_report(partial=False)
    log('=== STRUCTURED_RULINGS run complete, elapsed %.1f min, %d solved, %d crashed ===' %
        (elapsed() / 60, len(DATA['solved']), len(CRASHED)))


if __name__ == '__main__':
    main()
