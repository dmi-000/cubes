#!/usr/bin/env python3
"""Map the COUNT plateaus of every record -- the continua, with the right instrument.

Three integer probes failed before this ([P287] and the two after it).  The count
plateau is not the coincidence variety (dimension.py solves that; 727 is isolated
there while sitting on arcs), and it is not detectable by lattice probing: the
project's own principle says an infinitesimal is exact and a small number is a
sample, and FAILURE_MODES 11d says a zero probe reading means "not aligned", never
"isolated".

arc_eps.tangents_eps is the instrument built for this and already gated on 727 arc D,
a known NODE.  It SOLVES tangent candidates from the wall normals rather than
guessing directions, verifies each with eps in both signs, then tests combinations
to separate a surface from a node.  Its own controls -- zero-displacement must
reproduce the record, a wall-normal displacement must NOT -- both able to fail.

Run cheapest first so partial results survive.
"""
import sys, os as _os
HERE=_os.path.dirname(_os.path.abspath(__file__)); sys.path.insert(0,HERE)
from arc_eps import tangents_eps, BASE

C4 = [BASE[i] for i in (0,1,2,4)]                       # 183
C5 = BASE                                                # 393
C6 = BASE + [(7,14,1,-5)]                                # 727 -- known arcs, the control
C7 = C6 + [(4,-3,-4,-4)]                                 # 1217
C8 = C7 + [(24,-24,24,-61)]                              # 1895

for label, cfg in (("n=4 183 (P287: count plateau expected 0-dimensional)", C4),
                   ("n=5 393", C5),
                   ("n=6 727 (CONTROL: known arcs / node)", C6),
                   ("n=7 1217", C7),
                   ("n=8 1895", C8)):
    try:
        tangents_eps(cfg, label)
    except Exception as e:
        print("%s FAILED: %s" % (label, type(e).__name__+": "+str(e)[:100]), flush=True)
