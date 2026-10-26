# Validation record

Version: 0.4.0. Reference environment: Windows x64, Python 3.12.14. The tested dependency snapshot is `constraints-tested.txt`.

Run `python -m unittest discover -s tests -v` from this source directory. All 67 tests pass, covering arithmetic, tolerance boundaries, missing values, repeated/continuation rows, unsupported scans, local execution without network access, correction-source binding, stale reviews, tamper/formula rejection and benchmark counting. Language tests cover English CLI defaults, both CLI language positions, both workbook languages, cross-language imports, legacy Chinese metadata, preservation of source values, job language and local preference handling. OCR/model tests use mocks; real-engine accuracy remains unvalidated.

The public demo PDFs are English and synthetic. A Chinese extraction fixture remains under `tests/fixtures` for multilingual regression coverage. Parser vocabulary, internal records and tests intentionally retain the legacy Chinese vocabulary; presentation labels support English and Chinese.

The release must pass the suite and skill metadata validation before upload. A limited secret/local-path scan checks the selected public files; it is not a comprehensive security audit. Customer documents, generated private reports, virtual environments, caches and prior sales research are excluded.

The Windows portable executable was rebuilt with PyInstaller 6.22.3. Both English and Chinese packaged smoke tests process the five synthetic PDFs with zero failures and the expected single discrepancy, including paths with spaces and Chinese characters. Manual desktop inspection confirms both modules and languages retain the same window dimensions and selected examples. The English interface footer was checked for untranslated text.

Fresh installation was validated on Windows/Python 3.12.14. Other Python versions, macOS/Linux behavior and real-customer extraction accuracy remain unvalidated. Synthetic results must not be presented as real-world invoice accuracy.
