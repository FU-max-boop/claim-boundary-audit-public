#!/usr/bin/env python3
"""Render a real aggregate Claim-Boundary result card from cached JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def fmt_delta(row: dict[str, Any], prefix: str) -> str:
    value = row[f"{prefix}_joint_delta"]
    low = row[f"{prefix}_ci95_low"]
    high = row[f"{prefix}_ci95_high"]
    return f"{value:+.3f} [{low:+.3f}, {high:+.3f}]"


def render(summary: dict[str, Any]) -> str:
    bridge_lines = [
        f"- {bridge['name']} (`n={bridge['n_rows']}`)" for bridge in summary["bridges"]
    ]
    table_rows = []
    for row in summary["rows"]:
        table_rows.append(
            "| "
            + " | ".join(
                [
                    row["provider"],
                    row["control"],
                    row["positive_bridges"],
                    fmt_delta(row, "equal_weight"),
                    fmt_delta(row, "row_pooled"),
                ]
            )
            + " |"
        )

    return "\n".join(
        [
            "# Four-Bridge Positive Meta-Analysis Card",
            "",
            "This card is rendered from a cached aggregate result in",
            "`paper_results/four_bridge_positive_meta_summary.json`.",
            "",
            f"- Date: `{summary['date']}`",
            f"- Metric: `{summary['metric']}`",
            f"- Bootstrap: `{summary['bootstrap']['n_boot']}` resamples, seed `{summary['bootstrap']['seed']}`",
            f"- Scope: {summary['scope']}",
            "",
            "## Bridges",
            "",
            *bridge_lines,
            "",
            "## Joint Local+Transfer Summary",
            "",
            "| Provider | Control | Positive bridges | Equal-weight delta | Row-pooled delta |",
            "| --- | --- | ---: | ---: | ---: |",
            *table_rows,
            "",
            "## Interpretation",
            "",
            "All four public review-surface bridges have positive joint local+transfer",
            "deltas for both providers and both controls. This supports the bounded",
            "claim that the staged audit can identify correct-feedback-specific",
            "target-selection utility across heterogeneous public code-review surfaces.",
            "",
            "## Claim Boundary",
            "",
            "This is an aggregate target-selection audit. It is not evidence of broad",
            "end-to-end executable repair, deployment performance, or human-level code",
            "review understanding.",
            "",
            "## Source Note",
            "",
            summary["source_note"],
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("--card", type=Path, required=True)
    args = parser.parse_args()

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    args.card.parent.mkdir(parents=True, exist_ok=True)
    args.card.write_text(render(summary), encoding="utf-8")
    print(f"Rendered aggregate card: {args.card}")


if __name__ == "__main__":
    main()

