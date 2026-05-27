# Claim-Boundary Audit Quick Demo

Claim-Boundary Audit asks which feedback-use claim is warranted:

- local utility;
- local + transfer utility;
- feedback-text sensitivity;
- text-presence utility;
- hold.

## One Command

```bash
make smoke
```

## Synthetic Smoke Output

The tiny synthetic demo writes:

- `docs/result_cards/sample_claim_boundary_card.md`
- `docs/result_cards/sample_claim_boundary_metrics.json`

Current synthetic label:

```text
correct-feedback-specific local+transfer utility
```

## Aggregate Four-Bridge Card

The included aggregate card reports positive local+transfer deltas across four
public code-review surfaces:

| Provider | Control | Positive bridges | Row-pooled delta |
| --- | --- | ---: | ---: |
| DeepSeek | shuffled-feedback | 4/4 | +0.247 [+0.194, +0.300] |
| DeepSeek | no-feedback | 4/4 | +0.228 [+0.175, +0.281] |
| GLM-4.5 | shuffled-feedback | 4/4 | +0.264 [+0.211, +0.317] |
| GLM-4.5 | no-feedback | 4/4 | +0.244 [+0.197, +0.294] |

## Claim Boundary

This is a target-selection audit. It is not evidence of broad downstream
executable repair, deployment performance, or human-level code-review
understanding.
