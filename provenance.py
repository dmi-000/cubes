#!/usr/bin/env python3
"""Make a data file say how to reproduce it.

WHY.  On 2026-08-17 `data_inventory.py` found that `census_variety.py` writes
`census_variety4_*.json` and that NOTHING in the repository writes generations
1, 2 or 3 -- the script had been edited in place for each generation. The output
name was bumped every time, so the data survived, but the code that produced it
did not. Data preserved, provenance lost. Those numbers can no longer be
reproduced or even attributed to a known method.

The static-reference check (does any .py mention this filename) cannot fix that,
because it asks the SOURCE about the DATA. This asks the data about itself.

WHAT IS RECORDED, and why each item is needed:

    argv        the exact command line -- the thing you retype to reproduce.
                A shard number or budget passed as an argument appears nowhere
                in the source, so without this it is unrecoverable.
    script      which program, resolved to a real path
    sha1        CONTENT HASH OF THAT SCRIPT AT RUN TIME.  This is the item that
                would have caught the census_variety failure: argv alone is not
                enough when the script is mutated between runs, because the same
                command produces different numbers. If the hash on the data does
                not match the file on disk today, the code has changed since --
                and you know it rather than assuming it.
    started/    wall-clock bracket, so a file can be matched to a log
    finished
    inputs      optional: files the run consumed, each with its own sha1

SIDECAR, NOT EMBEDDED.  The stamp goes to `<output>.prov.json`, deliberately.
Producers here write bare JSON lists, and readers (including this project's own
resume logic) iterate them directly, so wrapping records in an envelope would
break live consumers -- including two census workers running as this was
written. A sidecar adds provenance to any producer without negotiating format.
The cost is that a sidecar can be separated from its data; `data_inventory.py`
reports a stamp whose data file is missing, and vice versa.
"""
import hashlib, json, os, socket, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))


def sha1_of(path):
    try:
        h = hashlib.sha1()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def stamp(output_path, inputs=None, started=None, note=None, argv=None,
          retroactive=False):
    """Write <output_path>.prov.json describing the run that produced it.

    retroactive=True marks a stamp written AFTER the fact. It matters: the script
    hash is then taken at STAMP time, not at RUN time, so it cannot certify that
    the recorded script produced the data. Caught on 2026-08-17 when a retro-
    stamped file reported "OK reproducible" although the producing script had
    been edited between the run and the stamp -- the stamp manufactured exactly
    the false assurance the hash exists to prevent.
    """
    script = os.path.abspath((argv or sys.argv)[0]) if (argv or sys.argv) else None
    rec = {
        'output': os.path.relpath(os.path.abspath(output_path), HERE),
        'argv': list(argv or sys.argv),
        'rerun': ' '.join(['python3'] + list(argv or sys.argv)),
        'script': os.path.relpath(script, HERE) if script else None,
        'script_sha1': sha1_of(script) if script else None,
        'started': started,
        'finished': time.strftime('%Y-%m-%d %H:%M:%S'),
        'host': socket.gethostname(),
        'python': sys.version.split()[0],
    }
    if retroactive:
        rec['retroactive'] = True
        rec['hash_taken'] = 'at stamp time, NOT at run time -- cannot certify the producer'
    if note:
        rec['note'] = note
    if inputs:
        rec['inputs'] = [{'path': os.path.relpath(os.path.abspath(p), HERE),
                          'sha1': sha1_of(p)} for p in inputs]
    p = output_path + '.prov.json'
    tmp = p + '.%d.tmp' % os.getpid()
    with open(tmp, 'w') as f:
        json.dump(rec, f, indent=1)
    os.replace(tmp, p)
    return p


def read(output_path):
    try:
        return json.load(open(output_path + '.prov.json'))
    except Exception:
        return None


def verify(output_path):
    """(ok, message): does the producing script still match the recorded hash?"""
    r = read(output_path)
    if not r:
        return None, 'no provenance stamp'
    sp = os.path.join(HERE, r.get('script') or '')
    if r.get('retroactive'):
        return None, ('stamp is RETROACTIVE: hash taken after the run, so it '
                      'cannot certify the producer. Recorded command: %s'
                      % r.get('rerun'))
    if not r.get('script_sha1'):
        return None, 'stamp records no script hash'
    if not os.path.exists(sp):
        return False, 'producing script %s no longer exists' % r.get('script')
    now = sha1_of(sp)
    if now != r['script_sha1']:
        return False, ('%s has CHANGED since this data was produced '
                       '(%s -> %s); rerunning will not reproduce it'
                       % (r.get('script'), r['script_sha1'][:8], now[:8]))
    return True, 'reproducible: %s' % r.get('rerun')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        ok, msg = verify(p)
        print('%-40s %-8s %s' % (p, {True: 'OK', False: 'STALE',
                                     None: 'UNKNOWN'}[ok], msg))
