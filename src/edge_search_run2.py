#!/usr/bin/env python3
"""Driver: runs front1b + front2random + front2climb sequentially (single
core), logging to edge_search.jsonl, for the edge-concurrence-richness
task. Not itself a validated file -- just a runner around edge_search.py.
"""
from edge_search import run_front1b, run_front2_random, run_front2_hillclimb

print('=== front1b: rational Pythagorean-angle octahedral-pair overlay ===')
run_front1b(levels=(3, 4, 5, 6, 7), qmax_axis=8, n_random=80, best_n=20)

print('\n=== front2 random: rational random baseline, edge-richness vs total ===')
run_front2_random(n_samples=3000, cap=30, seed=2026)

print('\n=== front2 hill-climb: maximize edge-richness, track total ===')
run_front2_hillclimb(n_seeds=10, n_steps=250, cap=24, seed=3000)

print('\nALL DONE')
