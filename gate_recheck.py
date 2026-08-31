#!/usr/bin/env python3
"""Re-establish correctness after the root_values / cached-catalogue surgery.

Both known answers must come back: 1217's two ends (n78_ends, 2026-08-08) and
n=9's lower end (P187). If either moves, the refactor broke something.
"""
import sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from solve_more_ends import ends_of, C6, C8

ends_of(C6, [F(-3,4), F(-1), F(-1)], [F(1), F(0), F(0)], 1217,
        'RECHECK n=7 1217 (must give -0.045258752093 / +0.002550224044, both 1215)',
        expect={'lower': -0.045258752093, 'upper': 0.002550224044})
ends_of(C8, [F(1), F(55,56), F(1)], [F(0), F(1), F(0)], 2785,
        'RECHECK n=9 2785 lower (must give -0.000004029245, count 2783)')
