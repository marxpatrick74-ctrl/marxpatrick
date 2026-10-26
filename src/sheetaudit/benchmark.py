"""Evaluate against independently labeled, hash-bound PDFs; emit only metrics."""
from collections import Counter
from decimal import Decimal
from difflib import SequenceMatcher
from pathlib import Path

from .extract import extract_document
from .model import FIELDS, AMOUNTS, NUMBERS, canonical_number, digest


def same_number(left, right):
    if left is None or right is None:
        return left is right
    return Decimal(left) == Decimal(right)


def evaluate_manifest(manifest, directory):
    if manifest.get("dataset_type") not in ("synthetic", "authorized_real"):
        raise ValueError("数据集必须声明为 synthetic 或 authorized_real")
    cases = manifest.get("cases")
    if not isinstance(cases, list) or not 1 <= len(cases) <= 100:
        raise ValueError("验证集须包含 1–100 个已标注案例")
    totals = Counter()
    results = []
    for index, case in enumerate(cases, 1):
        expected = case["expected"]
        if set(expected["fields"]) != set(FIELDS):
            raise ValueError("人工标注必须包含全部字段，未知为 null")
        for key in AMOUNTS:
            canonical_number(expected["fields"][key])
        for row in expected["items"]:
            if type(row["page"]) is not int or row["page"] < 1 or not isinstance(row["description"], str):
                raise ValueError("人工明细标注需要有效页码和名称")
            for key in NUMBERS:
                canonical_number(row[key])
        result = {"index": index, "expected_fields": len(FIELDS), "correct_fields": 0,
                  "expected_rows": len(expected["items"]), "extracted_rows": 0, "matched_rows": 0,
                  "correct_line_numbers": 0, "expected_line_numbers": len(expected["items"])*3}
        path = (directory / case["pdf"]).resolve()
        try:
            if digest(path) != case["sha256"]:
                raise ValueError("SOURCE_MISMATCH")
            actual, _ = extract_document(path)
            for key in FIELDS:
                a, e = actual["fields"][key], expected["fields"][key]
                result["correct_fields"] += same_number(a, e) if key in AMOUNTS else a == e
            result["extracted_rows"] = len(actual["items"])
            # Sequence alignment preserves duplicate lines. Page+description must match exactly.
            key = lambda row: (row["page"], row["description"].strip())
            matcher = SequenceMatcher(a=[key(r) for r in expected["items"]],
                                      b=[key(r) for r in actual["items"]], autojunk=False)
            for block in matcher.get_matching_blocks():
                result["matched_rows"] += block.size
                for offset in range(block.size):
                    e, a = expected["items"][block.a+offset], actual["items"][block.b+offset]
                    result["correct_line_numbers"] += sum(same_number(e[k], a[k]) for k in NUMBERS)
            result["state"] = "evaluated"
        except Exception:
            # Error types/messages and paths can contain customer data; aggregate the failure.
            result["state"] = "failed"
        for key, value in result.items():
            if key != "index" and type(value) is int:
                totals[key] += value
        results.append(result)
    def ratio(a, b):
        return round(totals[a]/totals[b], 6) if totals[b] else None
    return {"schema_version": 1, "dataset_type": manifest["dataset_type"],
            "dataset_label_is_user_declared": True,
            "cases": len(cases), "failed": sum(r["state"] == "failed" for r in results),
            "counts": dict(totals), "field_accuracy": ratio("correct_fields", "expected_fields"),
            "row_recall": ratio("matched_rows", "expected_rows"),
            "row_precision": ratio("matched_rows", "extracted_rows"),
            "line_number_accuracy": ratio("correct_line_numbers", "expected_line_numbers"),
            "case_metrics": results}
