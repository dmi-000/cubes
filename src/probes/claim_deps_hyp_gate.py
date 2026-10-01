#!/usr/bin/env python3
"""Gate for `claim_deps.py --hyp` ([P395]): it must flag the line that motivated it, and pass its fix.

The control is the hardest one available: ORIENTATION.md's line of 2026-09-24, which stated
P348's bound as proved under the WRONG condition while citing P374 and P237 and never P348.
Only the claim-string search can see it.  Also checked: a negated statement ("NOT yet a theorem")
is not a claim of proof, and a statement that keeps a condition phrase passes.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import claim_deps as C

tag, fallen, suspect, span = C.status_of_postscripts()
assert '348' in C.HYP, 'P348 carries no proved-if tag'
CASES = [
    ('the pre-fix ORIENTATION line', True,
     "* **Proved and still standing:** `E_i <= 10` ([P237]), `E_S <= 32` (PROOF_67), hence\n"
     "  `EE + B <= 188 - 2*SC2`, and `TOTAL <= 195 - Q4` **only for compounds with no `(1,1,2)`,\n"
     "  `(1,2,2)` or `(2,2,2)` vertices** ([P374])."),
    ('the corrected line', False,
     "* **Proved IF the holes are trivial:** `TOTAL <= 195 - Q4` ([P348])."),
    ('a negation', False,
     "`max(4) <= 195` is NOT yet a theorem ([P348])."),
    ('a bare citation claiming proof', True,
     "`h <= 47.5` is proved ([P348])."),
]
bad = 0
for name, want, text in CASES:
    got = bool([x for x in C.hyp_hits(span, only=[('ORIENTATION.md', text)]) if x[3] == '348'])
    print('%-36s flagged=%-5s want=%-5s %s' % (name, got, want, 'PASS' if got == want else 'FAIL'))
    bad += got != want
sys.exit(1 if bad else 0)
