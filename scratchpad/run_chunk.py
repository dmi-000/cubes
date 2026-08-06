import sys, json, time
sys.path.insert(0, '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad')
from harness import run_batch

# generic chunk runner: reads configs (one per line) from a file given as argv[1],
# runs them with given worker count argv[2], appends JSON results to argv[3] (one json per line, with meta prepended)
in_file = sys.argv[1]
workers = int(sys.argv[2])
out_file = sys.argv[3]
tag = sys.argv[4]

with open(in_file) as f:
    configs = [line.strip() for line in f if line.strip()]

t0=time.time()
results, elapsed = run_batch(configs, workers=workers, tag=tag)
print(f'chunk: {len(configs)} configs, elapsed {elapsed:.1f}s', file=sys.stderr)

with open(out_file, 'a') as f:
    for cfg, (b, obj) in zip(configs, results):
        if isinstance(obj, dict):
            f.write(json.dumps({'bounded': b, 'quats': obj.get('quats'), 'cfg': cfg}) + '\n')
        else:
            f.write(json.dumps({'bounded': None, 'raw': str(obj), 'cfg': cfg}) + '\n')
