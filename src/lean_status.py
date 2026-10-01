#!/usr/bin/env python3
"""Read each Lean bound's hypotheses back from Lean, derive its label, and check the hypotheses bite.

`lean/CubeBounds/Basic.lean` states every upper-bound reduction on max(n) with each geometric input
as a NAMED hypothesis whose prefix records its ledger status (proved_, argued_, hyp_, refuted_).
This script:

  1. asks Lean for each theorem's signature (`#check`), so the hypothesis list is Lean's, not a
     transcription, and derives the label:
         any refuted_ -> PROOF GAP;  any hyp_ or argued_ -> PROVED IF;  else PROVED
  2. asks Lean for its axioms (`#print axioms`): anything beyond propext / Quot.sound /
     Classical.choice, and above all `sorryAx`, fails the run;
  3. NECESSITY: recompiles each theorem with each non-proved hypothesis deleted, and requires the
     proof to FAIL.  A hypothesis that is listed but not used would make a PROVED result read as
     PROVED IF, the mirror image of [P395].  The unmodified theorem is compiled the same way first,
     as the control: a variant that fails for an unrelated reason would otherwise pass.
     `omega` is a decision procedure for linear arithmetic, so "fails without it" means the
     conclusion does not follow linearly from the rest, with C(n,k) as opaque atoms.
  4. prints the label beside the one the documents give (EXPECT), and fails on a mismatch.

    python3 src/lean_status.py
"""
import os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAN = os.path.join(ROOT, 'lean')
SRCS = [os.path.join(LEAN, 'CubeBounds', f) for f in ('Basic.lean', 'Proofs.lean')]
OK_AXIOMS = {'propext', 'Quot.sound', 'Classical.choice'}
# the label the documents give each theorem's conclusion, and where
EXPECT = {
    'h_le': ('PROVED IF', 'GLOSSARY h(S); P348 scope note'),
    'total_le_195_minus_Q4': ('PROVED IF', 'ORIENTATION, LEVELS (P395)'),
    'total_le_195_minus_Q4_from_caps': ('PROVED IF', 'ORIENTATION, LEVELS (P395)'),
    'tower': ('PROVED IF', 'RESULTS section 2, "PROVED IF c_l <= 2"'),
    'holes_of_c_le_two': ('PROVED IF', 'RESULTS section 4, c_l <= 2 is a STRONG CONJECTURE'),
    'total_le_953': ('PROOF GAP', 'RESULTS section 2 and 4'),
    # Proofs.lean: the counting skeletons of RESULTS section 2
    'max2_le_13': ('PROVED', 'RESULTS section 2, max2_report.md'),
    'max3_le_67_MV': ('PROVED', 'RESULTS section 2, P110'),
    'lemma1a_triple_le_32': ('PROVED', 'PROOF_67 Lemma 1a'),
    'weight_le_92': ('PROVED', 'PROOF_FORMAL Parts C-D, PROOF_STEP_T (scope: pairwise transversal)'),
    'max3_le_67_Euler': ('PROVED IF', 'PROOF_FORMAL B2/E, PROOF_67 section 5 (P398)'),
    'd1_bound': ('PROVED IF', 'RESULTS section 2, P237 with c1 = 1 (P398)'),
    'd1_bound_with_c': ('PROVED', 'P237 step 1 with c kept'),
    'pair_gain_le_10': ('PROVED', 'P237 step 3'),
    'per_cube_n4': ('PROVED', 'PROOF_SUBSET per-cube theorem'),
    'theoremS_n4': ('PROVED', 'RESULTS section 2, PROOF_SUBSET'),
    'increment': ('PROVED', 'RESULTS section 2, P56'),
    'max4_le_285': ('PROVED', 'RESULTS section 2, P399'),
    'per_set_closed_form': ('PROVED', 'P400'),
    'per_set_closed_form_tight': ('PROVED', 'P401'),
    'depth1_ceiling': ('PROVED', 'P401, RESULTS ceiling law at l = n - 1'),
    'max4_le_261': ('PROVED', 'P401'),
    'max4_le_195_charging': ('PROVED IF', 'P404, RESULTS section 4'),
}


def lean_run(text):
    with tempfile.NamedTemporaryFile('w', suffix='.lean', delete=False, dir=LEAN) as f:
        f.write(text)
        path = f.name
    try:
        r = subprocess.run(['lake', 'env', 'lean', path], cwd=LEAN, capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr
    finally:
        os.unlink(path)


def label(names):
    if any(n.startswith('refuted_') for n in names):
        return 'PROOF GAP'
    if any(n.startswith(('hyp_', 'argued_')) for n in names):
        return 'PROVED IF'
    return 'PROVED'


def blocks(src):
    """theorem name -> its full text (doc comment excluded), and the `def C` block"""
    out = {}
    for m in re.finditer(r'^theorem (\w+) \(.*?(?=^(?:theorem |example|/--|/-!|end Cube))', src, re.S | re.M):
        out[m.group(1)] = m.group(0)
    m = re.search(r'^def C .*?(?=^example)', src, re.S | re.M)
    defc = m.group(0) if m else None
    return out, defc


def drop_binder(text, name):
    i = text.index('(' + name + ' :')
    depth, j = 0, i
    while True:
        depth += {'(': 1, ')': -1}.get(text[j], 0)
        j += 1
        if depth == 0:
            break
    return text[:i] + text[j:]


# MUST-FAIL controls for the generated identity file (Detq.lean): a wrong target, a wrong wall, a
# wrong edge condition.  If any of these compiles, `grind` is not checking what it appears to.
CONTROLS = {
    'wrong W4 target (|p|^2 - 2)': '''theorem bad (p1 p2 p3 : Int) :
    det4 (Q_W4_axis0_pos p1 p2 p3) = 16 * (p1^2 + p2^2 + p3^2 - 2)^2 := by
  simp only [det4, Q_W4_axis0_pos]; grind''',
    'wrong W4 wall (one column swapped)': '''theorem bad (x y z p1 p2 p3 : Int) :
    2 * (p1 * Mr x y z 0 0 + p2 * Mr x y z 1 0 + p3 * Mr x y z 2 1 - Nn x y z) = qf (Q_W4_axis0_pos p1 p2 p3) x y z := by
  simp only [qf, Q_W4_axis0_pos, Mr, Nn]; grind''',
    'wrong W3 target (3|m|^2)': '''theorem bad (q1 q2 q3 m1 m2 m3 : Int) :
    det4 (Q_W3_edge0_pp q1 q2 q3 m1 m2 m3) = 256 * ((m2*q3 - m3*q2)^2 + (m3*q1 - m1*q3)^2 + (m1*q2 - m2*q1)^2 - 3*(m1^2 + m2^2 + m3^2))^2 := by
  simp only [det4, Q_W3_edge0_pp]; grind''',
}


def controls():
    bad = 0
    for name, text in CONTROLS.items():
        rc, _ = lean_run('import CubeBounds.Detq\nopen Cube.Detq\n' + text + '\n')
        print('control %-38s %s' % (name, 'fails, as it must' if rc else 'COMPILES: THE CHECK IS VACUOUS'))
        bad += not rc
    rc, out = lean_run('import CubeBounds.Detq\n#print axioms Cube.Detq.W3_edge2_mm_det\n#print axioms Cube.Detq.W4_axis2_neg_form\n')
    ax = set(re.findall(r"\[([^\]]*)\]", out)[0].replace(' ', '').split(',')) if not rc else {'?'}
    extra = {a for m in re.findall(r"\[([^\]]*)\]", out) for a in m.replace(' ', '').split(',')} - OK_AXIOMS
    print('Detq axioms beyond the standard ones: %s' % (sorted(extra) or 'none'))
    return bad + bool(extra) + bool(rc)


def main():
    subprocess.run(['lake', 'build'], cwd=LEAN, check=True, capture_output=True)
    thms, defc = {}, None
    for path in SRCS:
        t, d = blocks(open(path).read())
        thms.update(t)
        defc = defc or d
    q = 'import CubeBounds\n' + ''.join('#check Cube.%s\n#print axioms Cube.%s\n' % (t, t) for t in thms)
    rc, out = lean_run(q)
    if rc:
        sys.exit('Lean refused the query:\n' + out)
    bad = 0
    for t in thms:
        sig = re.search(r'^Cube\.%s .*?(?=^Cube\.|^\'Cube)' % t, out, re.S | re.M).group(0)
        names = re.findall(r'\((\w+) :', sig)
        hyps = [n for n in names if re.match(r'(proved|argued|hyp|refuted)_', n)]
        ax = re.search(r"'Cube\.%s' depends on axioms: \[([^\]]*)\]" % t, out)
        axioms = {a.strip() for a in ax.group(1).split(',')} if ax else set()
        ax_bad = axioms - OK_AXIOMS
        lab = label(hyps)
        want, where = EXPECT.get(t, ('?', 'not listed in EXPECT'))
        print('%-34s %-10s documents: %-10s %s' % (t, lab, want, 'OK' if lab == want else 'MISMATCH (%s)' % where))
        bad += lab != want
        if ax_bad:
            print('    AXIOMS beyond the standard ones: %s' % sorted(ax_bad)); bad += 1
        for h in hyps:
            print('    %s' % h)
        # necessity, with the unmodified theorem compiled the same way as the control
        base = 'namespace Cube\n%s\n%s\nend Cube\n' % (defc, thms[t])
        rc0, o0 = lean_run(base)
        if rc0:
            print('    CONTROL FAILED: the theorem does not compile standalone\n' + o0); bad += 1
            continue
        for h in hyps:
            if h.startswith('proved_'):
                continue
            rc1, _ = lean_run('namespace Cube\n%s\n%s\nend Cube\n' % (defc, drop_binder(thms[t], h)))
            print('      without %-44s %s' % (h, 'proof fails: NEEDED' if rc1 else 'STILL PROVES: NOT NEEDED'))
            bad += not rc1
    bad += controls()
    print('\n%s' % ('all labels agree, no extra axioms, every non-proved hypothesis is needed'
                    if not bad else '%d problems' % bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
