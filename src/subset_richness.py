#!/usr/bin/env python3
"""
Subset richness analysis: correlate bounded region counts with subset-level distribution.

Working principles:
- For each 6-cube config, extract total=bounded, per-cube counts (d1), and per-pair counts (d2)
- Quantify balance (spread) and richness (max) of each dimension
- Report correlations with total, percentile locations of rich-subset peaks, and balance patterns
- Expected: max_d1/max_d2 peaks at mid-totals, not tops (verification task)
"""

import json
import sys
from collections import defaultdict
from scipy.stats import pearsonr
import numpy as np

def main():
    filepath = "/Users/dmi/carroll/campaign_results.jsonl"

    configs = []
    skipped_no_per_label = 0

    # Parse all configs
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            record = json.loads(line)

            if "per_label" not in record:
                skipped_no_per_label += 1
                continue

            per_label = record["per_label"]

            # Compute d1 vector (single cubes)
            d1 = [per_label.get(str(1 << k), 0) for k in range(6)]

            # Compute d2 vector (pairs)
            d2 = []
            for i in range(6):
                for j in range(i + 1, 6):
                    mask = (1 << i) | (1 << j)
                    d2.append(per_label.get(str(mask), 0))

            max_d1 = max(d1)
            spread_d1 = max(d1) - min(d1)

            max_d2 = max(d2)
            spread_d2 = max(d2) - min(d2)

            config = {
                "total": record["bounded"],
                "d1": d1,
                "d2": d2,
                "max_d1": max_d1,
                "spread_d1": spread_d1,
                "max_d2": max_d2,
                "spread_d2": spread_d2,
            }
            configs.append(config)

    print(f"Loaded {len(configs)} configs (skipped {skipped_no_per_label} without per_label)")

    # Extract arrays for correlation
    totals = np.array([c["total"] for c in configs])
    max_d1_arr = np.array([c["max_d1"] for c in configs])
    max_d2_arr = np.array([c["max_d2"] for c in configs])
    spread_d1_arr = np.array([c["spread_d1"] for c in configs])
    spread_d2_arr = np.array([c["spread_d2"] for c in configs])

    # (A) Correlation of total vs max_d1, total vs max_d2
    corr_total_d1, pval_d1 = pearsonr(totals, max_d1_arr)
    corr_total_d2, pval_d2 = pearsonr(totals, max_d2_arr)

    print(f"\n=== (A) Correlations ===")
    print(f"total vs max_d1: r = {corr_total_d1:.4f} (p={pval_d1:.2e})")
    print(f"total vs max_d2: r = {corr_total_d2:.4f} (p={pval_d2:.2e})")

    # Bucket by total: use deciles
    percentiles = np.percentile(totals, np.linspace(0, 100, 11))
    buckets = np.digitize(totals, percentiles)

    bucket_stats = []
    for b in range(1, 11):
        mask = buckets == b
        if not mask.any():
            continue
        bucket_totals = totals[mask]
        bucket_d1 = max_d1_arr[mask]
        bucket_d2 = max_d2_arr[mask]

        stats = {
            "bucket": b,
            "total_range": (bucket_totals.min(), bucket_totals.max()),
            "n": mask.sum(),
            "mean_max_d1": bucket_d1.mean(),
            "mean_max_d2": bucket_d2.mean(),
        }
        bucket_stats.append(stats)

    print("\nBucket analysis (deciles by total):")
    print("Bucket | Total range      | N     | mean max_d1 | mean max_d2")
    for s in bucket_stats:
        print(f"  {s['bucket']:2d}  | {s['total_range'][0]:3d}-{s['total_range'][1]:3d}     | {s['n']:5d} | {s['mean_max_d1']:7.2f}  | {s['mean_max_d2']:7.2f}")

    # Check if monotone
    d1_means = [s["mean_max_d1"] for s in bucket_stats]
    d2_means = [s["mean_max_d2"] for s in bucket_stats]
    d1_mono = all(d1_means[i] <= d1_means[i+1] for i in range(len(d1_means)-1)) or \
              all(d1_means[i] >= d1_means[i+1] for i in range(len(d1_means)-1))
    d2_mono = all(d2_means[i] <= d2_means[i+1] for i in range(len(d2_means)-1)) or \
              all(d2_means[i] >= d2_means[i+1] for i in range(len(d2_means)-1))

    print(f"Monotone d1: {d1_mono}, Monotone d2: {d2_mono}")

    # (B) Find configs with max max_d1 and max_d2
    print(f"\n=== (B) Rich-subset peaks ===")
    global_max_d1 = max_d1_arr.max()
    global_max_d2 = max_d2_arr.max()

    rich_d1_mask = max_d1_arr == global_max_d1
    rich_d2_mask = max_d2_arr == global_max_d2

    rich_d1_totals = totals[rich_d1_mask]
    rich_d2_totals = totals[rich_d2_mask]

    print(f"Global max max_d1: {global_max_d1}")
    print(f"  Found in {rich_d1_mask.sum()} configs")
    print(f"  Their totals: min={rich_d1_totals.min()}, max={rich_d1_totals.max()}, mean={rich_d1_totals.mean():.1f}")
    print(f"  Percentiles in overall total distribution:")
    for tot in sorted(set(rich_d1_totals)):
        pct = (totals <= tot).mean() * 100
        print(f"    total={tot}: {pct:.1f}th percentile")

    print(f"\nGlobal max max_d2: {global_max_d2}")
    print(f"  Found in {rich_d2_mask.sum()} configs")
    print(f"  Their totals: min={rich_d2_totals.min()}, max={rich_d2_totals.max()}, mean={rich_d2_totals.mean():.1f}")
    print(f"  Percentiles in overall total distribution:")
    for tot in sorted(set(rich_d2_totals)):
        pct = (totals <= tot).mean() * 100
        print(f"    total={tot}: {pct:.1f}th percentile")

    # (C) Balance vs total: top 1%, median, bottom 1%
    print(f"\n=== (C) Balance analysis ===")

    top1_threshold = np.percentile(totals, 99)
    bottom1_threshold = np.percentile(totals, 1)
    median = np.percentile(totals, 50)

    top1_mask = totals >= top1_threshold
    median_mask = (totals >= median - 5) & (totals <= median + 5)
    bottom1_mask = totals <= bottom1_threshold

    top1_spread_d1 = spread_d1_arr[top1_mask].mean()
    top1_spread_d2 = spread_d2_arr[top1_mask].mean()

    median_spread_d1 = spread_d1_arr[median_mask].mean()
    median_spread_d2 = spread_d2_arr[median_mask].mean()

    bottom1_spread_d1 = spread_d1_arr[bottom1_mask].mean()
    bottom1_spread_d2 = spread_d2_arr[bottom1_mask].mean()

    print(f"Top 1% by total (>= {top1_threshold:.0f}):")
    print(f"  mean spread_d1: {top1_spread_d1:.2f}")
    print(f"  mean spread_d2: {top1_spread_d2:.2f}")
    print(f"  n: {top1_mask.sum()}")

    print(f"\nMedian-total configs (around {median:.0f}):")
    print(f"  mean spread_d1: {median_spread_d1:.2f}")
    print(f"  mean spread_d2: {median_spread_d2:.2f}")
    print(f"  n: {median_mask.sum()}")

    print(f"\nBottom 1% by total (<= {bottom1_threshold:.0f}):")
    print(f"  mean spread_d1: {bottom1_spread_d1:.2f}")
    print(f"  mean spread_d2: {bottom1_spread_d2:.2f}")
    print(f"  n: {bottom1_mask.sum()}")

    # (D) Coupling: correlation of max_d1 vs max_d2
    print(f"\n=== (D) Coupling correlation ===")
    corr_d1_d2, pval_d1_d2 = pearsonr(max_d1_arr, max_d2_arr)
    print(f"max_d1 vs max_d2: r = {corr_d1_d2:.4f} (p={pval_d1_d2:.2e})")

    # Summary statistics
    print(f"\n=== Summary ===")
    print(f"Total configs analyzed: {len(configs)}")
    print(f"Skipped (no per_label): {skipped_no_per_label}")
    print(f"Total bounded regions: min={totals.min()}, max={totals.max()}, mean={totals.mean():.1f}")
    print(f"max_d1: min={max_d1_arr.min()}, max={max_d1_arr.max()}, mean={max_d1_arr.mean():.2f}")
    print(f"max_d2: min={max_d2_arr.min()}, max={max_d2_arr.max()}, mean={max_d2_arr.mean():.2f}")

if __name__ == "__main__":
    main()
