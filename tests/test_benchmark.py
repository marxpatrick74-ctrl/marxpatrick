import unittest
from copy import deepcopy
from pathlib import Path

from sheetaudit.benchmark import evaluate_manifest
from sheetaudit.model import digest

ROOT = Path(__file__).resolve().parents[1]


def gold():
    return {"dataset_type": "synthetic", "cases": [{"pdf": "pdfs/good_invoice.pdf",
        "sha256": digest(ROOT / "examples/pdfs/good_invoice.pdf"), "expected": {
            "fields": {"document_type": "invoice", "document_number": "INV-DEMO-001", "date": "2026-10-24",
                       "seller": "Demo Components Ltd", "buyer": "Example Workshop", "currency": "USD",
                       "subtotal": "57.50", "tax": "5.75", "discount": "0.00", "shipping": "0.00", "total": "63.25"},
            "items": [{"page": 1, "description": "Cable A", "quantity": "3", "unit_price": "12.50", "amount": "37.50"},
                      {"page": 1, "description": "Adapter B", "quantity": "2", "unit_price": "10.00", "amount": "20.00"}]}}]}


class BenchmarkTests(unittest.TestCase):
    def test_independent_gold_and_numeric_normalization(self):
        data = gold()
        data["cases"][0]["expected"]["items"][0]["amount"] = "37.5"
        result = evaluate_manifest(data, ROOT / "examples")
        self.assertEqual(result["field_accuracy"], 1)
        self.assertEqual(result["row_recall"], 1)
        self.assertEqual(result["line_number_accuracy"], 1)

    def test_missing_gold_row_and_wrong_number_reduce_metrics(self):
        data = gold()
        data["cases"][0]["expected"]["items"].append({"page": 1, "description": "Not extracted", "quantity": "1", "unit_price": "1", "amount": "1"})
        data["cases"][0]["expected"]["items"][0]["amount"] = "42.50"
        result = evaluate_manifest(data, ROOT / "examples")
        self.assertAlmostEqual(result["row_recall"], 2/3, places=5)
        self.assertAlmostEqual(result["line_number_accuracy"], 5/9, places=5)

    def test_source_mismatch_is_failure_without_exposing_path(self):
        data = gold()
        data["cases"][0]["sha256"] = "0"*64
        result = evaluate_manifest(data, ROOT / "examples")
        self.assertEqual(result["failed"], 1)
        self.assertEqual(result["row_recall"], 0)
        self.assertNotIn("good_invoice", str(result))
