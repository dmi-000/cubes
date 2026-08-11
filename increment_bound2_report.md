# increment_bound2 report

B_j computed by formula (*) of specs/INCREMENT_BOUND_SPEC.md: exact rational arithmetic throughout, `fractions.Fraction` only.
## G1 — n=2 hand-computed degenerate case
j=0: status=ok  B=12 c=1 deg6=2 deg4=6 other_deg=0 n_vertices=8 points_match_spec=True tangent_tally=0  -> PASS
j=1: status=ok  B=12 c=1 deg6=2 deg4=6 other_deg=0 n_vertices=8 points_match_spec=True tangent_tally=0  -> PASS

G1 verdict: PASS

## G2 — CONFIGS table
```
config         j      T    S_j  Delta_j      B_j   slack verdict
727 record     0    727    385      342      358  1.0468 OK
727 record     1    727    385      342      358  1.0468 OK
727 record     2    727    385      342      362  1.0585 OK
727 record     3    727    383      344      360  1.0465 OK
727 record     4    727    377      350      358  1.0229 OK
727 record     5    727    393      334      370  1.1078 OK
723            0    723    381      342      366  1.0702 OK
723            1    723    381      342      366  1.0702 OK
723            2    723    381      342      366  1.0702 OK
723            3    723    387      336      348  1.0357 OK
723            4    723    375      348      348  1.0000 OK
723            5    723    393      330      354  1.0727 OK
393 (n=5)      0    393    179      214      226  1.0561 OK
393 (n=5)      1    393    179      214      226  1.0561 OK
393 (n=5)      2    393    179      214      226  1.0561 OK
393 (n=5)      3    393    183      210      222  1.0571 OK
393 (n=5)      4    393    171      222      222  1.0000 OK
183 (n=4)      0    183     55      128      128  1.0000 OK
183 (n=4)      1    183     63      120      128  1.0667 OK
183 (n=4)      2    183     63      120      128  1.0667 OK
183 (n=4)      3    183     63      120      128  1.0667 OK
```

G2 verdict: PASS

## G3 — generic agreement with the old V_j
sampled 22 random (q0,q1) pairs, small entries in [-4,4]; 15 (config,j) instances were fully generic (no plane tangency, no line-tangency to dC_j, no triple points, c == 1); 14 skipped for line-tangency to dC_j only, 15 skipped for a disconnected trace (c > 1) — both are degeneracies the old script's F=2+V silently mishandled rather than disagreements this code gets wrong
All 15 generic instances satisfy B_j == 2 + V_old exactly.

G3 verdict: PASS

## G4 — vertex self-check
Asserted inline in `compute_B` for every vertex emitted in G1/G2/G3 (both plane equations exactly, |v|_inf == 1 exactly). No assertion failed, so G4 passed throughout this run.

## Slack distribution (G2 rows)
min=1.0000  median=1.0561  max=1.1078  n=21

## Degeneracy tally (G2)
No tangent planes encountered in any G2 row.

## Tightness beyond G1

Besides G1 (which is tight by construction, B=12=Delta), the following G2 rows are also exactly tight (slack 1.00): 723 j=4 (B=Delta=348), 393 (n=5) j=4 (B=Delta=222), 183 (n=4) j=0 (B=Delta=128).

## Overall

G1=PASS  G2=PASS  G3=PASS  G4=PASS
