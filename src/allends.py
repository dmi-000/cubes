#!/usr/bin/env python3
"""Endpoints of the CONNECTED COMPONENT containing each record — W3 and W4 walls.

Supersedes the endpoint rows of [P187]/[P189]. Two defects made those wrong:

  1. Roots were deduped through a lossy symbolic key, so the walk stepped OVER
     intervals. With the full value-deduped list, 1217's level set turns out to be
     PUNCTURED — a 0.0022-wide chamber of 1215 sits between the record and the
     endpoint previously reported, verified by direct engine calls at three interior
     points. So -0.045258752 is the outer edge of a FURTHER component, not the
     boundary of the record's own.
  2. Only W4 walls were enumerated. A component bounded by a W3 (edge-edge) wall
     would be missed identically.

Both fixed. This reports the boundary of the component CONTAINING THE RECORD, which
is what "the continuum" means, and says which wall type bounds it.
"""
import sys
sys.path.insert(0, '.')
from fractions import Fraction as F
from solve_more_ends import ends_of

BASE = [(4,1,1,-1),(3,3,7,3),(5,-1,-5,-5),(2,1,1,1),(1,1,1,1)]
C6 = BASE + [(7,14,1,-5)]
C7 = C6 + [(4,-3,-4,-4)]
C8 = C7 + [(24,-24,24,-61)]

ends_of(C6, [F(-3,4), F(-1), F(-1)], [F(1), F(0), F(0)], 1217, 'n=7  1217')
ends_of(C7, [F(-1), F(1), F(-61,24)], [F(0), F(0), F(1)], 1895, 'n=8  1895')
ends_of(C8, [F(1), F(55,56), F(1)], [F(0), F(1), F(0)], 2785, 'n=9  2785')
