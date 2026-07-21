#!/usr/bin/env python3
"""Targeted refinement pass: widen G to |components|<=6 around the CURRENT
best clique pair for the near-record cells found in the main sweep, append
to the same glue_results.jsonl. Bounded (no clique-candidate regeneration)."""
import json
import sys
sys.path.insert(0, '/Users/dmi/carroll')
from glue_search import (gen_G_menu, build_glued_quats, run_batch_parallel,
                          quat_to_matrix_exact, mat_mul, mat_transpose,
                          mats_to_quats, RECORDS)


def main():
    with open('/Users/dmi/carroll/glue_best.json') as f:
        best = json.load(f)

    CELLS = ['4_3_1', '4_2_2', '5_4_1', '5_3_2', '6_4_2', '6_3_3', '6_5_1']
    G6 = gen_G_menu(6)
    print(f'widen menu |comp|<=6: {len(G6)}')

    log_fh = open('/Users/dmi/carroll/glue_results.jsonl', 'a')
    final = {}
    for key in CELLS:
        n, a, b = map(int, key.split('_'))
        total0, rec = best[key]['total'], best[key]['rec']
        cliqueA = {'quats': rec['quats'][:a]}
        if b >= 2:
            Gmat = quat_to_matrix_exact(*rec['Gquat'])
            Ginv = mat_transpose(Gmat)
            matsB = [mat_mul(Ginv, quat_to_matrix_exact(*q)) for q in rec['quats'][a:]]
            cliqueB = {'quats': mats_to_quats(matsB)}
        else:
            cliqueB = None
        quat_lists, metas = [], []
        for Gq in G6:
            qs = build_glued_quats(cliqueA, cliqueB, tuple(Gq))
            if qs is None:
                continue
            quat_lists.append(qs)
            metas.append((Gq, qs))
        best_total, best_rec = total0, rec
        for bstart in range(0, len(quat_lists), 2000):
            bq = quat_lists[bstart:bstart+2000]
            bm = metas[bstart:bstart+2000]
            results = run_batch_parallel(n, bq)
            for (Gq, qs), res in zip(bm, results):
                if res is None:
                    continue
                tot, depth = res
                rc = {'n': n, 'sizeA': a, 'sizeB': b, 'kind': 'widen6_refine',
                      'psiA_pqr': None, 'thetasA_pqr': None, 'psiB_pqr': None, 'thetasB_pqr': None,
                      'Gquat': list(Gq), 'quats': [list(q) for q in qs], 'total': tot, 'by_depth': depth}
                log_fh.write(json.dumps(rc) + '\n')
                if tot > best_total:
                    best_total, best_rec = tot, rc
        log_fh.flush()
        print(f'{key}: {total0} -> {best_total}  (record {RECORDS[n]})', flush=True)
        final[key] = {'total': best_total, 'rec': best_rec}

    log_fh.close()
    with open('/Users/dmi/carroll/glue_best.json', 'w') as f:
        json.dump(final, f, indent=1, default=str)
    print('done')


if __name__ == '__main__':
    main()
