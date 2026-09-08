#!/usr/bin/env python3
"""Minimal two-cube search campaign for n=4 record.
Target: beat 183.
"""
import collections
import json
import os
import subprocess
import sys
import time


def quat_str(q):
    return ','.join(str(x) for x in q)


# Run verification first
print("KNOWN-ANSWER GATE", flush=True)
gates = [
    ("1,0,0,0;3,1,1,1", 13),
    ("1,0,0,0;4,3,3,0", 13),
    ("1,0,0,0;0,5,3,2;1,-4,-1,1;1,1,-1,-4", 183),
]

for cfg_str, expected in gates:
    r = subprocess.run(
        ['./cube_regions_q2w', '--d', '0', '--quats-stdin'],
        input=cfg_str + '\n',
        capture_output=True, text=True, timeout=30
    )
    obj = json.loads(r.stdout.strip())
    actual = obj.get('bounded')
    print(f"  {cfg_str[:30]:30s} expected {expected:3d}, got {actual:3d}: "
          + ("PASS" if actual == expected else "FAIL"))
    if actual != expected:
        sys.exit(1)

print("\nStarting search...")
start_time = time.time()

# Two bases and two magnitude caps
bases = [
    ("1,0,0,0", "3,1,1,1"),
    ("1,0,0,0", "4,3,3,0"),
]

best_count = 0
best_config = None
all_counts = collections.Counter()

for base0_str, base1_str in bases:
    print(f"\nBase: {base0_str};{base1_str}", flush=True)

    for mag_cap in [2, 3]:
        print(f"  mag_cap {mag_cap}...", flush=True, end=" ")

        # Generate cubes and build configs
        cube_list = []
        for w in range(-mag_cap, mag_cap + 1):
            for x in range(-mag_cap, mag_cap + 1):
                for y in range(-mag_cap, mag_cap + 1):
                    for z in range(-mag_cap, mag_cap + 1):
                        if w*w + x*x + y*y + z*z <= mag_cap * mag_cap:
                            cube_list.append((w, x, y, z))

        configs = []
        for c1 in cube_list[:30]:
            for c2 in cube_list[:30]:
                cfg_line = f"{base0_str};{base1_str};{quat_str(c1)};{quat_str(c2)}"
                configs.append(cfg_line)

        # Query in batches
        refusal_count = 0
        tested = 0
        valid = 0

        for i in range(0, len(configs), 2000):
            batch = configs[i:i+2000]
            tested += len(batch)

            r = subprocess.run(
                ['./cube_regions_q2w', '--d', '0', '--quats-stdin'],
                input='\n'.join(batch) + '\n',
                capture_output=True, text=True, timeout=120
            )

            for line in r.stdout.splitlines():
                if line.startswith('{'):
                    try:
                        obj = json.loads(line)
                        cnt = obj.get('bounded')
                        valid += 1
                        all_counts[cnt] += 1
                        if cnt > best_count:
                            best_count = cnt
                            best_config = line
                            print(f"NEW BEST: {cnt}", flush=True)
                    except:
                        refusal_count += 1
                else:
                    refusal_count += 1

        print(f"tested {tested:4d}, valid {valid:4d}, refusals {refusal_count}", flush=True)

elapsed = time.time() - start_time

print(f"\n{'='*60}")
print(f"RESULTS")
print(f"{'='*60}")
print(f"Elapsed: {elapsed:.1f} sec")
print(f"Best count: {best_count}")

if best_config:
    obj = json.loads(best_config)
    quats = obj.get('quats', [])
    print(f"Best config: {';'.join(','.join(q) for q in quats)}")

    # Verify
    cfg_str = ';'.join(','.join(q) for q in quats)
    print("\nVerification (cube_regions_q2w):")
    r = subprocess.run(
        ['./cube_regions_q2w', '--d', '0', '--quats-stdin'],
        input=cfg_str + '\n',
        capture_output=True, text=True, timeout=30
    )
    if r.stdout.strip():
        obj = json.loads(r.stdout.strip())
        print(f"  bounded: {obj.get('bounded')}")

    print("Verification (cube_regions_n):")
    r = subprocess.run(
        ['./cube_regions_n', '--quats', cfg_str],
        capture_output=True, text=True, timeout=30
    )
    print(f"  {r.stdout.strip()[:100]}")

print("\nCount distribution (top 15):")
for cnt, freq in sorted(all_counts.items(), reverse=True)[:15]:
    print(f"  {cnt:3d}: {freq:6d}")

print("")
if best_count >= 183:
    print(f"SUCCESS: reached or exceeded 183")
else:
    print(f"Did not reach 183 (best: {best_count})")

# Write outputs
ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT, 'twocube_n4.log'), 'w') as f:
    f.write(f"Campaign result: {best_count}\n")
    f.write(f"Config: {best_config}\n" if best_config else "No results\n")

with open(os.path.join(ROOT, 'twocube_n4.json'), 'w') as f:
    json.dump({
        'best_count': best_count,
        'best_config': json.loads(best_config) if best_config else None,
        'elapsed': elapsed,
        'count_distribution': dict(sorted(all_counts.items()))
    }, f, indent=2)

print(f"\nFiles written to {ROOT}/twocube_n4.{{json,log}}")
