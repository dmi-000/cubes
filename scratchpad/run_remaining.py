import sys, json, glob, time
sys.path.insert(0, '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad')
from harness import run_batch

SD = '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad'

def process(chunk_glob, out_path, tag_prefix, workers=8):
    files = sorted(glob.glob(chunk_glob))
    total_done = 0
    t0 = time.time()
    for i, fn in enumerate(files):
        with open(fn) as f:
            configs = [l.strip() for l in f if l.strip()]
        if not configs:
            continue
        results, elapsed = run_batch(configs, workers=workers, tag=f'{tag_prefix}_{i}')
        with open(out_path, 'a') as out:
            for cfg, (b, obj) in zip(configs, results):
                if isinstance(obj, dict):
                    out.write(json.dumps({'bounded': b, 'quats': obj.get('quats')}) + '\n')
                else:
                    out.write(json.dumps({'bounded': None, 'raw': str(obj)}) + '\n')
        total_done += len(configs)
        print(f'[{tag_prefix}] chunk {fn}: {len(configs)} configs in {elapsed:.1f}s (cum {total_done})', file=sys.stderr, flush=True)
    print(f'[{tag_prefix}] TOTAL: {total_done} configs in {time.time()-t0:.1f}s', file=sys.stderr, flush=True)

# remaining task2 chunks (00 already done separately, skip it)
process(f'{SD}/t2chunk_0[1-9]', f'{SD}/task2_results.jsonl', 't2')

# task3: 7th cube replacement
process(f'{SD}/t3a_*', f'{SD}/task3_7th_results.jsonl', 't3a')

# task3: 6th cube replacement
process(f'{SD}/t3b_*', f'{SD}/task3_6th_results.jsonl', 't3b')

print('ALL DONE', file=sys.stderr, flush=True)
