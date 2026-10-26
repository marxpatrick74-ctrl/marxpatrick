# Interchange schema v1

`extracted.json` is produced by the CLI. Treat it as a preserved extraction record; edit its generated `review-template.json` copy instead. The engine input/output content has exactly `fields` and `items`.

## Fields

All keys must exist. Values are strings or JSON null:

```json
{
  "fields": {
    "document_type": "invoice",
    "document_number": "INV-001",
    "date": "2026-10-24",
    "seller": "Example Supplier",
    "buyer": "Example Buyer",
    "currency": "USD",
    "subtotal": "20.00",
    "tax": null,
    "discount": null,
    "shipping": null,
    "total": "20.00"
  },
  "items": [
    {
      "row_id": "p1-r1",
      "page": 1,
      "description": "Example item",
      "quantity": "2",
      "unit_price": "10.00",
      "amount": "20.00",
      "evidence": "Example item | 2 | 10.00 | 20.00"
    }
  ]
}
```

Amounts and quantity must be decimal strings without currency signs, grouping or exponent notation, e.g. `"-2.50"`. Do not use JSON floats. A string `"0"` means zero is known; `null` means unknown. Max 15 significant digits per input. Item page is a 1-based integer, row_id is unique `[A-Za-z0-9_-]` up to 64 characters; description/evidence must be nonempty. Preserve identifiers with leading zeros as strings.

## Preserved metadata

- `source.file`: source basename, never an output destination.
- `source.sha256`: hash of original bytes; `source.pages`: 1–100.
- `document_id`: CLI-generated `d001_<8 lowercase hash characters>`.
- `engine`, `number_format`, `field_evidence`, `extraction_issues`, `human_review`.
- `source.json`: per-page original text, detected tables and `text`/`ocr` method.

The correction template includes `source_sha256`, `base_extraction_sha256` and a full editable `fields`/`items` snapshot. It also requires nonempty reviewer, ISO timestamp with offset, explanatory notes, and a boolean `coverage_confirmed`. This is version binding and attribution, not a digital signature. `review` preserves original metadata and source warnings and writes a separate result.

Version 0.2 adds optional `resolutions`: a list of `{ "issue_id": "issue-...", "action": "open" | "resolved", "note": "..." }`. IDs come from the generated template and are stable within a preserved extraction. Resolved decisions need a nonempty reason; resolving COVERAGE_REVIEW additionally requires coverage_confirmed=true. Unknown or duplicate IDs are rejected. Only extraction notices can be manually resolved; computed arithmetic differences and missing-field issues are recalculated. Existing version 0.1 JSON corrections without resolutions remain accepted, leaving notices open.

`human_review.reviewed_content_sha256` binds decisions to current fields/items. If content changes, previous decisions reopen. `audit.json` separates `issues` (open) from `resolved_issues` (with reviewer, timestamp and reason). Original extraction_issues are never deleted. `audit_policy` stores tolerance and decimal_places; review inherits these unless explicitly overridden.

The primary user interface is now review.xlsx. Its hidden metadata binds to the same hashes; editable tabs are translated into this JSON contract after rejecting formulas, changed headers/original columns, missing original rows and duplicate IDs. Deletion must be explicit in the operation column.

## Checks and issue codes

| Code | Meaning |
|---|---|
| LINE_AMOUNT | Compare quantity×price with stated amount |
| SUBTOTAL | Compare sum of extracted stated line amounts with stated subtotal |
| TOTAL | Compare subtotal+tax−discount+shipping with stated total |
| NO_TEXT / NO_ITEMS / NO_ITEMS_ON_PAGE | Image/empty/unsupported page or document requires attention |
| ROW_NUMBER / FIELD_NUMBER | Refused an ambiguous number; value left unknown |
| UNPARSED_ROW / UNMAPPED_TABLE | Potential omitted data; confirm with source |
| CONFLICTING_FIELD | Multiple differing header values; first value retained |
| MISSING_DESCRIPTION / MISSING_FIELD | Incomplete required descriptive data |
| CURRENCY_PRECISION | Missing/unrecognized currency or unsuitable requested decimal places |
| OCR_REVIEW / AI_REVIEW | Machine extraction needs source verification |
| EVIDENCE_UNVERIFIED | AI source quote did not match extracted page text exactly |
| COVERAGE_REVIEW | Always confirm full coverage and business meaning manually |
| DUPLICATE_FILE | Identical PDF bytes in the same batch, both retained |
| INHERITED_HEADER | Previous-page column layout reused; confirm the continuation |
| PROCESSING_ERROR | File failed, visible in batch report and JSON |

`delta = observed - expected`. `expected` rounds using ROUND_HALF_UP and requested places. `abs(delta) > tolerance` flags a difference; missing prerequisites are uncheckable; otherwise arithmetic is consistent. All checks are independent of AI responses. No check signifies payment approval.
