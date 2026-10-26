# Windows desktop

Download `SheetAudit-Desktop-v0.4.0-Windows-x64.zip` from the GitHub release. Extract the entire archive, then open `program/SheetAudit.exe`. Python and runtime dependencies are included. Keep `_internal`, notices and licenses beside the executable.

Select **English** or **简体中文** at the top right. English is the first-launch default, and the app remembers the choice locally. Switching preserves the current selection and settings. Both audit and human-review views keep the same window size. Language selection is disabled during processing, so each job keeps its starting language.

The portable package writes to its adjacent `reports` directory. Existing installations with the original program folder name retain their existing output location. You can choose another folder in the window. Opening workbooks requires Excel, WPS or another compatible application.

1. Click **Load examples**, or add authorized text-based PDFs.
2. Choose an output folder, tolerance and number format, then **Generate report**.
3. Check differences, uncheckable items and open notices.
4. For corrections, edit and save `review.xlsx`. Enter a real human reviewer, timezone-aware timestamp, notes and coverage confirmation. Resolve notices with reasons.
5. In **Human review**, select the extraction record, saved workbook and original PDF, then **Recalculate**.

Reports use the selected language. Existing reports are never rewritten by switching. Either UI language can import English, Chinese and legacy Chinese workbooks. Source names, descriptions, evidence and amounts remain unchanged. Do not edit hidden metadata or original-value columns.

Default processing stays local; outputs are not automatically encrypted. The desktop does not enable optional Tesseract or Ollama integrations. Arithmetic agreement is not authenticity, completeness, tax validation or payment approval.

## Run or build from source

Install the project, then run `python desktop_launcher.py`. Use `--language en` or `--language zh` to choose the launch language. Tk must be available in your Python installation.

For a developer build on Windows, install PyInstaller, then run `./scripts/build_desktop.ps1 -Python ./.venv/Scripts/python.exe`. Keep the complete generated program directory, including notices and dependency licenses. See `THIRD_PARTY_NOTICES.md`. A rebuilt binary must be validated on its target environment before distribution. Windows x64 / Python 3.12.14 is the current reference environment; macOS/Linux desktop behavior is untested.
