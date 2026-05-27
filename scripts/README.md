# Scripts

Minimal runnable entry points:

- `run_smoke_test.sh`: runs the synthetic smoke artifact end to end.
- `score_claim_boundary.py`: scores a JSONL file with local/transfer gold targets
  and predictions under correct-feedback, shuffled-feedback, and no-feedback
  conditions.
- `render_positive_bridge_card.py`: renders the cached four-bridge aggregate
  result into a Markdown result card.

The scripts use only the Python standard library.

Example:

```bash
bash scripts/run_smoke_test.sh
```

The smoke test writes synthetic-demo metrics and a real aggregate result card
into `docs/result_cards/`.
