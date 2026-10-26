"""PyInstaller entry point. The diagnostic path processes bundled synthetic PDFs only."""
import json
import sys
from pathlib import Path
from sheetaudit.desktop import audit_arguments, execute_job, main, sample_directory

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--smoke-test":
        parent = Path(sys.argv[2]).resolve()
        result = execute_job(audit_arguments([str(sample_directory())], str(parent)))
        (parent / "desktop-smoke-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        raise SystemExit(result["code"])
    main()
