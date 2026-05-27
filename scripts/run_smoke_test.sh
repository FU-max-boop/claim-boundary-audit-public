#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$ROOT/docs/result_cards"

mkdir -p "$OUT_DIR"

python "$ROOT/scripts/score_claim_boundary.py" \
  "$ROOT/data/sample_claim_boundary_records.jsonl" \
  --card "$OUT_DIR/sample_claim_boundary_card.md" \
  --json "$OUT_DIR/sample_claim_boundary_metrics.json"

python "$ROOT/scripts/render_positive_bridge_card.py" \
  "$ROOT/paper_results/four_bridge_positive_meta_summary.json" \
  --card "$OUT_DIR/four_bridge_positive_meta_card.md"

test -s "$OUT_DIR/sample_claim_boundary_card.md"
test -s "$OUT_DIR/sample_claim_boundary_metrics.json"
test -s "$OUT_DIR/four_bridge_positive_meta_card.md"

echo "Smoke test passed: $OUT_DIR/sample_claim_boundary_card.md"
echo "Aggregate card rendered: $OUT_DIR/four_bridge_positive_meta_card.md"
