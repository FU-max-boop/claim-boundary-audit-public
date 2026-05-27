# Four-Bridge Positive Meta-Analysis Card

This card is rendered from a cached aggregate result in
`paper_results/four_bridge_positive_meta_summary.json`.

- Date: `2026-05-24`
- Metric: `joint local+transfer target-selection delta`
- Bootstrap: `4000` resamples, seed `20260524`
- Scope: Fixed-policy target-selection audit; not a downstream executable repair evaluation.

## Bridges

- GH Archive PR reviews (`n=120`)
- PR_Review-Benchmark (`n=80`)
- OpenStack+Qt Gerrit (`n=80`)
- CROP inline reviews (`n=80`)

## Joint Local+Transfer Summary

| Provider | Control | Positive bridges | Equal-weight delta | Row-pooled delta |
| --- | --- | ---: | ---: | ---: |
| DeepSeek | shuffled-feedback | 4/4 | +0.231 [+0.163, +0.322] | +0.247 [+0.194, +0.300] |
| DeepSeek | no-feedback | 4/4 | +0.214 [+0.150, +0.297] | +0.228 [+0.175, +0.281] |
| GLM-4.5 | shuffled-feedback | 4/4 | +0.245 [+0.153, +0.362] | +0.264 [+0.211, +0.317] |
| GLM-4.5 | no-feedback | 4/4 | +0.228 [+0.144, +0.319] | +0.244 [+0.197, +0.294] |

## Interpretation

All four public review-surface bridges have positive joint local+transfer
deltas for both providers and both controls. This supports the bounded
claim that the staged audit can identify correct-feedback-specific
target-selection utility across heterogeneous public code-review surfaces.

## Claim Boundary

This is an aggregate target-selection audit. It is not evidence of broad
end-to-end executable repair, deployment performance, or human-level code
review understanding.

## Source Note

Derived from the submitted package aggregate files outputs/reports/positive_bridge_meta_analysis_2026-05-24.json and outputs/reports/headline_evidence_table_2026-05-24.md. It contains aggregate statistics only, not per-example data.
