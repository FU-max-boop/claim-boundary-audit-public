# Data

This directory currently contains a tiny synthetic smoke-test file:

```text
sample_claim_boundary_records.jsonl
```

The sample is not a paper result source. It demonstrates the artifact protocol:

1. provide local and same-family transfer target-selection stages;
2. record the gold target and candidate options for each stage;
3. compare fixed-policy predictions under correct feedback, shuffled feedback,
   and no feedback;
4. assign a bounded claim label from those control comparisons.

Larger cached outputs should be copied only after the privacy and license pass.

Aggregate result summaries live in `paper_results/`, not here, because
they are not raw data rows.
