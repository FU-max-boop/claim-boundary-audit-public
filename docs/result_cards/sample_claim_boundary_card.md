# Sample Claim-Boundary Card

This card is generated from a tiny synthetic smoke-test set. It demonstrates
the audit protocol; it is not a submitted-paper result source.

- Records: `8`
- Decision threshold: `0.150`
- Claim label: `correct-feedback-specific local+transfer utility`

## Accuracy By Condition

| Condition | Local | Transfer | Joint local+transfer |
| --- | ---: | ---: | ---: |
| correct_feedback | 0.875 | 0.625 | 0.625 |
| shuffled_feedback | 0.000 | 0.000 | 0.000 |
| no_feedback | 0.125 | 0.000 | 0.000 |

## Control Deltas

| Delta | Local | Transfer | Joint local+transfer |
| --- | ---: | ---: | ---: |
| correct_minus_shuffled_feedback | 0.875 | 0.625 | 0.625 |
| correct_minus_no_feedback | 0.750 | 0.625 | 0.625 |

## Stage Labels

- Local: `correct-feedback-specific utility`
- Transfer: `correct-feedback-specific utility`

## Reading Boundary

A positive label means the fixed target-selection policy benefits from the
correct feedback text on this audited surface. It does not imply broad
end-to-end executable repair, deployment performance, or human-level code
review understanding.
