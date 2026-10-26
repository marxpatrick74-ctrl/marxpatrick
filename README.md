# SheetAudit AI 0.3.2

[Agent skill](SKILL.md) · [MIT license](LICENSE)

Turn purchase-order and invoice PDFs into an Excel report on your own computer. Extract header fields and line items, check quantity × unit price and document totals, and retain exceptions for human review.

The default workflow uses local rules. It needs no API key, account or cloud service. It does not post to accounting software or approve payments.

## Release scope

This release contains the runnable Python project and agent skill. Documentation and public demo PDFs are in English. The existing desktop source and workbook interface retain their original Chinese labels; this is not a fully localized English application. No prebuilt Windows executable is included in this source release. See [desktop notes](DESKTOP.md).

## Python project and agent skill

Python 3.10+ is required. The tested environment is Windows with Python 3.12.14. After downloading the source, open a terminal in the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -c constraints-tested.txt -e .
.\.venv\Scripts\python.exe -m sheetaudit audit examples/pdfs examples/regressions --out reports/demo-001
.\.venv\Scripts\python.exe -m unittest discover -s tests -q
```

On macOS/Linux, substitute `.venv/bin/python` for the Windows executable path. These platforms have not been validated. Initial dependency installation requires network access. Default document processing then runs locally.

For an AI coding agent, load the root `SKILL.md` and use this folder as the project root. Keep `src/`, `scripts/`, `references/`, the example PDFs and `pyproject.toml` with the skill. The skill guides extraction, privacy summaries, arithmetic interpretation and local human corrections.

## Supported pilot

- Text-based Chinese or English invoices and purchase orders with common field labels and consistently aligned line-item columns.
- One document per PDF, including supported continuation pages.
- Up to 100 PDFs per batch, 100 pages and 50 MB per file. Directory inputs scan one level.
- Decimal arithmetic with configurable rounding. Default tolerance is 0.01; differences strictly greater than the tolerance are flagged.
- Missing values stay unknown. They are not replaced with zero or inferred from arithmetic.

Scans, handwriting, complex merged layouts, multiple documents in one PDF, per-line discounts and tax conventions may require separate assessment and manual input. Optional Tesseract/Ollama integrations exist, but their real-engine recognition quality has not been validated. The portable desktop does not enable those integrations.

## Output and corrections

`report.xlsx` is a snapshot containing fields, line items, discrepancies and source evidence. Each document also has an editable `review.xlsx` and supporting local JSON files.

Editing the report does not recalculate it. Correct the document's `review.xlsx`, save it, and run the human-review workflow below. The original PDF and prior report remain unchanged. A real reviewer must confirm coverage and provide the actual review signature. No identity or completeness sign-off is invented.

For an English-keyed correction file, copy the generated `review-template.json` to a new local file, correct `fields` / `items`, and fill in the real `reviewer`, timezone-aware `reviewed_at`, `notes` and `coverage_confirmed`. Resolve extraction notices only with a recorded reason. Keep source hashes unchanged. Do not let an agent invent a human sign-off.

```text
python -m sheetaudit review reports/demo-001/documents/<document-id>/extracted.json --corrections path/to/corrections.json --source path/to/original.pdf --out reports/review-001
```

The same command accepts the generated `review.xlsx` as `--corrections`. See [the schema](references/schema.md) for field definitions. Review workbooks and reports keep the original interface language in this version.

For a privacy-reduced status summary, run:

```powershell
.\.venv\Scripts\python.exe -m sheetaudit summary reports/demo-001
```

## Privacy and validation

Document processing is local by default. Outputs and raw-evidence JSON files are not encrypted. Keep customer files outside source control and automatic cloud-sync folders. Do not attach real invoices, customer records or unredacted reports to public issues.

The project has 57 automated tests. The bundled PDFs are synthetic examples, including intentional discrepancies and unsupported cases. They are not client work or a claim of real-world invoice accuracy. Arithmetic agreement does not establish completeness, invoice authenticity, tax correctness or permission to pay.

Report a reproducible problem using synthetic or authorized redacted documents, the version, expected result and actual result. Third-party libraries and the bundled desktop runtime retain their own licenses and notices. See `THIRD_PARTY_NOTICES.md`.

## Demo cases

| PDF | Expected behavior |
| --- | --- |
| `good_invoice.pdf` | Two lines; no arithmetic differences; human coverage review still required. |
| `discrepancy_invoice.pdf` | First line states 42.50 instead of 3 x 12.50 = 37.50; one 5.00 difference. |
| `purchase_order_multipage.pdf` | Two identical legitimate rows on separate pages; preserve both. |
| `unsupported_invoice.pdf` | Ambiguous quantity and missing price remain unknown. |
| `scanned_invoice.pdf` | Image-only; default rules mode must flag missing text/items. |

Run `./run_demo.ps1` on Windows for an automatically named demo output directory. It creates a project virtual environment and installs dependencies if necessary. A supported Python installation and internet connection are needed for first-time setup.

To regenerate demo PDFs, install the optional dependencies with `python -m pip install -c constraints-tested.txt -e ".[demo]"`, then run `python scripts/make_examples.py`. Regression fixtures and their hash-bound benchmark are preserved separately. See [benchmarking](BENCHMARK.md) and [validation](VALIDATION.md).

## License and contributions

Original source and synthetic examples are available under the [MIT license](LICENSE), allowing use, modification and redistribution with the required notice. Dependencies keep their own licenses. Please use synthetic reproductions in issues and pull requests. Never submit private invoices or credentials.
