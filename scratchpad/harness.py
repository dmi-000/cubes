import subprocess, os, json, sys, tempfile, time

BIN = '/Users/dmi/cube-compounds/cube_regions_n'
TMP = '/private/tmp/claude-502/-Users-dmi-cube-compounds/88682f8c-0607-4f2d-8384-b3993c9c5ded/scratchpad'

def run_batch(configs, workers=8, tag='batch'):
    """configs: list of strings 'w,x,y,z;...;w,x,y,z' (8 groups).
    Returns list of (bounded_or_None, raw_json_or_error) in same order as configs."""
    n = len(configs)
    if n == 0:
        return []
    chunk_size = (n + workers - 1) // workers
    chunks = [configs[i:i+chunk_size] for i in range(0, n, chunk_size)]
    infiles = []
    outfiles = []
    procs = []
    for idx, ch in enumerate(chunks):
        inf = os.path.join(TMP, f'{tag}_in_{idx}.txt')
        outf = os.path.join(TMP, f'{tag}_out_{idx}.txt')
        with open(inf, 'w') as f:
            for c in ch:
                f.write(c + '\n')
        infiles.append(inf)
        outfiles.append(outf)
    t0 = time.time()
    for inf, outf in zip(infiles, outfiles):
        p = subprocess.Popen([BIN, '--quats-stdin'], stdin=open(inf), stdout=open(outf, 'w'), stderr=subprocess.DEVNULL)
        procs.append(p)
    for p in procs:
        p.wait()
    elapsed = time.time() - t0
    results = []
    for outf in outfiles:
        with open(outf) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    results.append((obj.get('bounded'), obj))
                except Exception as e:
                    results.append((None, line))
    # cleanup
    for f in infiles + outfiles:
        try:
            os.remove(f)
        except OSError:
            pass
    if len(results) != n:
        print(f'WARNING: expected {n} results, got {len(results)}', file=sys.stderr)
    return results, elapsed
