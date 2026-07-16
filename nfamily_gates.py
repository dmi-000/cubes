#!/usr/bin/env python3
# Working principles: NFAMILY_SPEC.md. Project index: README.md
"""G0/G1/G2 gates for the n-family sweep (NFAMILY_SPEC.md). Run with no
args; prints PASS/FAIL for each gate and exits nonzero on any failure."""
import json
import subprocess
import sys

from fractions import Fraction as Fr

from nfamily_common import (PyAngle, IDENTITY_ANGLE, rel_matrix,
                             is_rotation_exact, matrix_to_int_quat,
                             build_family_quats, quat_to_matrix_exact)
from golden_rotations import rot_from_quat
from certify_six import exact_count_config


def run_cpp(quats, n=None):
    n = n or len(quats)
    qstr = ';'.join(','.join(str(c) for c in q) for q in quats)
    out = subprocess.run(['./cube_regions_n', '--n', str(n), '--quats', qstr],
                          capture_output=True, text=True, check=True).stdout
    return json.loads(out.strip())


def gate_g0():
    print('=== G0: exact rational round-trip (chain triple, no floats) ===')
    a = PyAngle.from_pqr(3, 4, 5)        # 36.8699 deg = asin(3/5)
    psi = PyAngle.from_pqr(4, 3, 5)      # 53.1301 deg = asin(4/5)
    ok = True
    for k in range(3):
        theta = a.pow(k)
        delta = theta  # base is IDENTITY_ANGLE (theta_1=0)
        M = rel_matrix(delta, psi)
        rot_ok = is_rotation_exact(M)
        q = matrix_to_int_quat(M)   # asserts round-trip internally
        back = quat_to_matrix_exact(*q)
        exact_ok = all(back[i][j] == M[i][j] for i in range(3) for j in range(3))
        print(f'  k={k} theta={theta.deg():.4f}deg  rotation_ok={rot_ok}  '
              f'quat={q}  round_trip_exact={exact_ok}')
        ok = ok and rot_ok and exact_ok
    print(f'G0: {"PASS" if ok else "FAIL"}\n')
    return ok


def gate_g1():
    print('=== G1: two-engine agreement (n=3 chain, n=4 family) ===')
    ok = True

    # n=3 chain: a=36.87 (3,4,5), psi=53.13 (4,3,5), theta=(0,a,2a)
    a = PyAngle.from_pqr(3, 4, 5)
    psi = PyAngle.from_pqr(4, 3, 5)
    thetas3 = [IDENTITY_ANGLE, a, a.pow(2)]
    quats3, _ = build_family_quats(psi, thetas3)
    r_cpp = run_cpp(quats3, n=3)
    rots = [rot_from_quat(*q) for q in quats3]
    py_total, py_depth = exact_count_config(rots, verbose=False)
    py_depth = {int(k): v for k, v in py_depth.items()}
    cpp_depth = {int(k): v for k, v in r_cpp['by_depth'].items()}
    match3 = (r_cpp['bounded'] == py_total and cpp_depth == py_depth)
    print(f'  n=3 chain quats={quats3}')
    print(f'  cpp: total={r_cpp["bounded"]} depth={cpp_depth}')
    print(f'  py:  total={py_total} depth={py_depth}')
    print(f'  n=3 match: {match3}')
    ok = ok and match3

    # n=4 family config: same chain extended to k=0..3, plus a second psi
    # to also exercise a non-chain (independent-phase) member.
    thetas4 = [IDENTITY_ANGLE, a, a.pow(2), a.pow(3)]
    quats4, _ = build_family_quats(psi, thetas4)
    r_cpp4 = run_cpp(quats4, n=4)
    rots4 = [rot_from_quat(*q) for q in quats4]
    py_total4, py_depth4 = exact_count_config(rots4, verbose=False)
    py_depth4 = {int(k): v for k, v in py_depth4.items()}
    cpp_depth4 = {int(k): v for k, v in r_cpp4['by_depth'].items()}
    match4 = (r_cpp4['bounded'] == py_total4 and cpp_depth4 == py_depth4)
    print(f'  n=4 chain quats={quats4}')
    print(f'  cpp: total={r_cpp4["bounded"]} depth={cpp_depth4}')
    print(f'  py:  total={py_total4} depth={py_depth4}')
    print(f'  n=4 match: {match4}')
    ok = ok and match4

    print(f'G1: {"PASS" if ok else "FAIL"}\n')
    return ok, (quats3, r_cpp['bounded'], cpp_depth), (quats4, r_cpp4['bounded'], cpp_depth4)


def gate_g2():
    print('=== G2: record reproduction (n=6, 723 from ledger quats) ===')
    quats = [(4, 1, 1, -1), (3, 3, 7, 3), (5, -1, -5, -5),
             (2, 1, 1, 1), (1, 1, 1, 1), (5, 2, 2, 2)]
    r = run_cpp(quats, n=6)
    depth = {int(k): v for k, v in r['by_depth'].items() if int(k) != 0}
    expect_depth = {1: 210, 2: 216, 3: 164, 4: 96, 5: 36, 6: 1}
    ok = (r['bounded'] == 723 and depth == expect_depth)
    print(f'  cpp: total={r["bounded"]} depth={depth}')
    print(f'  expect: total=723 depth={expect_depth}')
    print(f'G2: {"PASS" if ok else "FAIL"}\n')
    return ok


if __name__ == '__main__':
    g0 = gate_g0()
    g1, n3info, n4info = gate_g1()
    g2 = gate_g2()
    all_ok = g0 and g1 and g2
    print(f'ALL GATES: {"PASS" if all_ok else "FAIL"}')
    sys.exit(0 if all_ok else 1)
