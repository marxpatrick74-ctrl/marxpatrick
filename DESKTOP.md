# Desktop source

The Tkinter desktop source is included in `src/sheetaudit/desktop.py`. Its interface and workbook labels are currently Chinese. This public source release includes English documentation and demo PDFs, but does not include or claim an English Windows binary.

After installing the project, run `python desktop_launcher.py` to open the interface on a machine with Tk. The two views run the same audit and human-review engine as the CLI. The desktop does not enable optional OCR or Ollama integrations.

For a developer build on Windows, install PyInstaller from its official package distribution, install the demo extras, then run `./scripts/build_desktop.ps1 -Python ./.venv/Scripts/python.exe`. Keep the entire generated program directory, including `_internal`, licenses and notices. See `THIRD_PARTY_NOTICES.md`; do not distribute only the executable. A binary built on your machine must be tested on its target Windows environment before distribution.

The existing installed desktop copy is separate from this source release. Source changes do not update an already installed executable.
