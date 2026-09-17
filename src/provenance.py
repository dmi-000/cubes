#!/usr/bin/env python3
"""How a data file was made, recorded IN the data file.

THE FAILURE THIS EXISTS TO CATCH.  A .json in `data/` states a number.  Six weeks later the
question is always the same -- which script, which level, which window, which direction
family -- and the answer has usually been reconstructed from a log, from the ledger, or from
the file's own field names.  A run whose parameters cannot be recovered cannot be repeated,
and a measurement that cannot be repeated is an anecdote with a timestamp.

WHAT IS RECORDED.  The exact command line, the script and its SHA-256 (there is no git here,
so the hash IS the version), the declared parameters, the engines, the library versions, and
the input files the run consumed.  The hash matters most: it distinguishes a file written by
today's `concurrency_walls.py` from one written before the plane-convention fix ([P304]),
which no timestamp would.

PATHS ARE RELATIVE, ALWAYS.  Never an absolute path and never a hostname: these files are
quoted in documents that get published, and a resolved path carries the account layout of
whatever machine produced it.  `data/x.json` locates the file in the repo; an absolute path
locates it on one host and nowhere else.
"""
import sys, os, json, hashlib, platform, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'src' else HERE


def rel(p):
    try:
        return os.path.relpath(os.path.abspath(p), ROOT)
    except ValueError:
        return os.path.basename(p)


def sha256(p):
    try:
        return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    except Exception:
        return None


def stamp(parameters=None, inputs=None, note=None):
    """The `reproduce` block to drop into any data file this project writes."""
    script = rel(sys.argv[0]) if sys.argv and sys.argv[0] else None
    args = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    try:
        import sympy as sp
        sv = sp.__version__
    except Exception:
        sv = None
    engines = {}
    try:
        import dimension as D
        for nm in ('ENG', 'ENGW'):
            v = getattr(D, nm, None)
            if v:
                engines[nm] = {'path': rel(v), 'sha256_16': sha256(v)}
    except Exception:
        pass
    out = {
        'command': ('python3 %s %s' % (script, args)).strip() if script else None,
        'run_from': 'src',
        'script': script,
        'script_sha256_16': sha256(sys.argv[0]) if sys.argv and sys.argv[0] else None,
        'parameters': parameters or {},
        'written_utc': datetime.datetime.now(datetime.timezone.utc)
                               .strftime('%Y-%m-%dT%H:%M:%SZ'),
        'python': platform.python_version(),
        'sympy': sv,
        'engines': engines,
    }
    if inputs:
        out['inputs'] = [{'path': rel(p), 'sha256_16': sha256(p)} for p in inputs]
    if note:
        out['note'] = note
    return out


def attach(doc, **kw):
    """Put the stamp into a document under `reproduce` and return the document."""
    doc['reproduce'] = stamp(**kw)
    return doc
