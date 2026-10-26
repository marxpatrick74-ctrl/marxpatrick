# Validate extraction against human ground truth

All bundled PDFs are synthetic. `examples/benchmark-synthetic.json` checks covered layouts and regressions, not real-world market accuracy.

```text
python -m sheetaudit benchmark examples/benchmark-synthetic.json --out reports/benchmark-synthetic-001.json
```

For a real evaluation, obtain permission for 10-20 redacted documents from 2-3 layouts. Keep originals and annotations local. Record each PDF path relative to the manifest, its SHA-256, all 11 header fields and every line in original order. Never use unreviewed program output as ground truth. Have another person check the annotation where possible.

Use decimal strings without grouping or currency symbols; use null for unknown values. Each item requires page, description, quantity, unit_price and amount. Pages start at 1. Preserve repeated lines. Set `dataset_type` to `authorized_real` for authorized customer data, or `synthetic` for generated documents. This is an operator declaration, not proof of consent.

```text
python -m sheetaudit benchmark private-inputs/ground-truth.json --out reports/benchmark-real-001.json
```

The result contains case numbers, counts and metrics, without document paths, names or amounts. Input manifests and PDFs remain sensitive.

- Field accuracy compares all 11 fields. Numbers compare as Decimal; text matches exactly; two nulls match.
- Line recall is matched reference lines divided by reference lines; precision uses extracted lines as its denominator.
- Numeric accuracy counts correct quantity, price and amount cells against three times the reference-line count. Unmatched lines contribute no correct cells.
- Alignment uses page and exact description in sequence, preserving duplicate occurrences. Misspelled descriptions or reordered lines require human interpretation.
- Changed hashes and processing failures remain failures. Precision with zero extracted lines is null, not 100 percent.

Also record manual-only time, tool runtime, subsequent review time, edits and final missed errors. Accept a layout only after checking coverage, taxes, discounts and rounding. Synthetic tests do not justify advertising an unattended accounting service.
