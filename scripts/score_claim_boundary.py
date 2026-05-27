#!/usr/bin/env python3
"""Score a small claim-boundary target-selection audit.

The script intentionally uses only the Python standard library so reviewers can
run the smoke test from a clean checkout.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


CONDITIONS = ("correct_feedback", "shuffled_feedback", "no_feedback")
STAGES = ("local", "transfer")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    if not records:
        raise SystemExit(f"{path}: no records found")
    return records


def require_schema(records: list[dict[str, Any]]) -> None:
    for idx, record in enumerate(records, start=1):
        rid = record.get("id", f"record-{idx}")
        if "predictions" not in record:
            raise SystemExit(f"{rid}: missing predictions")
        for stage in STAGES:
            stage_obj = record.get(stage)
            if not isinstance(stage_obj, dict) or "gold" not in stage_obj:
                raise SystemExit(f"{rid}: missing {stage}.gold")
        for condition in CONDITIONS:
            pred_obj = record["predictions"].get(condition)
            if not isinstance(pred_obj, dict):
                raise SystemExit(f"{rid}: missing predictions.{condition}")
            for stage in STAGES:
                if stage not in pred_obj:
                    raise SystemExit(f"{rid}: missing predictions.{condition}.{stage}")


def accuracy(records: list[dict[str, Any]], condition: str, stage: str) -> float:
    correct = 0
    for record in records:
        gold = record[stage]["gold"]
        pred = record["predictions"][condition][stage]
        correct += int(pred == gold)
    return correct / len(records)


def joint_accuracy(records: list[dict[str, Any]], condition: str) -> float:
    correct = 0
    for record in records:
        local_ok = record["predictions"][condition]["local"] == record["local"]["gold"]
        transfer_ok = (
            record["predictions"][condition]["transfer"] == record["transfer"]["gold"]
        )
        correct += int(local_ok and transfer_ok)
    return correct / len(records)


def stage_label(metrics: dict[str, Any], stage: str, threshold: float) -> str:
    c = metrics["conditions"]["correct_feedback"][stage]
    s = metrics["conditions"]["shuffled_feedback"][stage]
    n = metrics["conditions"]["no_feedback"][stage]
    beats_shuffled = c - s >= threshold
    beats_no_feedback = c - n >= threshold
    if beats_shuffled and beats_no_feedback:
        return "correct-feedback-specific utility"
    if beats_shuffled:
        return "feedback-text sensitivity"
    if beats_no_feedback:
        return "text-presence utility"
    return "hold"


def overall_label(metrics: dict[str, Any], threshold: float) -> str:
    local = stage_label(metrics, "local", threshold)
    transfer = stage_label(metrics, "transfer", threshold)
    if (
        local == "correct-feedback-specific utility"
        and transfer == "correct-feedback-specific utility"
    ):
        return "correct-feedback-specific local+transfer utility"
    if local == "correct-feedback-specific utility":
        return "correct-feedback-specific local utility"
    if transfer == "correct-feedback-specific utility":
        return "correct-feedback-specific transfer utility"
    if local == "feedback-text sensitivity" or transfer == "feedback-text sensitivity":
        return "feedback-text sensitivity"
    if local == "text-presence utility" or transfer == "text-presence utility":
        return "text-presence utility"
    return "hold"


def score(records: list[dict[str, Any]], threshold: float) -> dict[str, Any]:
    require_schema(records)
    metrics: dict[str, Any] = {
        "n": len(records),
        "threshold": threshold,
        "conditions": {},
        "deltas": {},
        "source_families": dict(Counter(r.get("source_family", "unknown") for r in records)),
    }
    for condition in CONDITIONS:
        metrics["conditions"][condition] = {
            "local": accuracy(records, condition, "local"),
            "transfer": accuracy(records, condition, "transfer"),
            "joint_local_transfer": joint_accuracy(records, condition),
        }
    for control in ("shuffled_feedback", "no_feedback"):
        metrics["deltas"][f"correct_minus_{control}"] = {
            stage: metrics["conditions"]["correct_feedback"][stage]
            - metrics["conditions"][control][stage]
            for stage in ("local", "transfer", "joint_local_transfer")
        }
    metrics["stage_labels"] = {
        stage: stage_label(metrics, stage, threshold) for stage in STAGES
    }
    metrics["claim_label"] = overall_label(metrics, threshold)
    return metrics


def fmt(value: float) -> str:
    return f"{value:.3f}"


def write_card(metrics: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for condition in CONDITIONS:
        item = metrics["conditions"][condition]
        rows.append(
            "| "
            + " | ".join(
                [
                    condition,
                    fmt(item["local"]),
                    fmt(item["transfer"]),
                    fmt(item["joint_local_transfer"]),
                ]
            )
            + " |"
        )

    delta_rows = []
    for name, item in metrics["deltas"].items():
        delta_rows.append(
            "| "
            + " | ".join(
                [
                    name,
                    fmt(item["local"]),
                    fmt(item["transfer"]),
                    fmt(item["joint_local_transfer"]),
                ]
            )
            + " |"
        )

    text = "\n".join(
        [
            "# Sample Claim-Boundary Card",
            "",
            "This card is generated from a tiny synthetic smoke-test set. It demonstrates",
            "the audit protocol; it is not a submitted-paper result source.",
            "",
            f"- Records: `{metrics['n']}`",
            f"- Decision threshold: `{metrics['threshold']:.3f}`",
            f"- Claim label: `{metrics['claim_label']}`",
            "",
            "## Accuracy By Condition",
            "",
            "| Condition | Local | Transfer | Joint local+transfer |",
            "| --- | ---: | ---: | ---: |",
            *rows,
            "",
            "## Control Deltas",
            "",
            "| Delta | Local | Transfer | Joint local+transfer |",
            "| --- | ---: | ---: | ---: |",
            *delta_rows,
            "",
            "## Stage Labels",
            "",
            f"- Local: `{metrics['stage_labels']['local']}`",
            f"- Transfer: `{metrics['stage_labels']['transfer']}`",
            "",
            "## Reading Boundary",
            "",
            "A positive label means the fixed target-selection policy benefits from the",
            "correct feedback text on this audited surface. It does not imply broad",
            "end-to-end executable repair, deployment performance, or human-level code",
            "review understanding.",
            "",
        ]
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", type=Path)
    parser.add_argument("--card", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--threshold", type=float, default=0.15)
    args = parser.parse_args()

    records = load_jsonl(args.records)
    metrics = score(records, args.threshold)

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    if args.card:
        write_card(metrics, args.card)

    print("Claim-boundary audit")
    print(f"n: {metrics['n']}")
    print(f"local acc: {fmt(metrics['conditions']['correct_feedback']['local'])}")
    print(f"transfer acc: {fmt(metrics['conditions']['correct_feedback']['transfer'])}")
    print(f"joint acc: {fmt(metrics['conditions']['correct_feedback']['joint_local_transfer'])}")
    print(f"claim label: {metrics['claim_label']}")


if __name__ == "__main__":
    main()

