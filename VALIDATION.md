# Validation record

Version: 0.3.2. Reference environment: Windows x64, Python 3.12.14. The tested dependency snapshot is `constraints-tested.txt`.

Run `python -m unittest discover -s tests -v` from this source directory. The suite contains 57 tests covering decimal arithmetic, tolerance boundaries, missing values, repeated and continuation rows, unsupported scans, local processing without network access, correction-source binding, stale reviews, workbook tampering/formulas, safe text output and benchmark counting. OCR and model tests use mocks; real OCR/model accuracy is unvalidated.

The public demo PDFs are English and synthetic. A Chinese extraction fixture is kept under `tests/fixtures` to retain multilingual regression coverage. Parser vocabulary and internal test assertions intentionally include Chinese. The original workbook and desktop interface labels are not localized by this documentation release.

The release must pass the suite and skill metadata validation before upload. A limited secret/local-path scan checks the selected public files; it is not a comprehensive security audit. Customer documents, generated private reports, virtual environments, caches and prior sales research are excluded.

Fresh dependency installation on every supported Python version, macOS/Linux behavior, real-customer accuracy and a newly rebuilt Windows binary have not been validated. The existing portable desktop installation is not changed by this release.
