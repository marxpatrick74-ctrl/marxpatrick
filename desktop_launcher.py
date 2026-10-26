"""PyInstaller entry point. The diagnostic path processes bundled synthetic PDFs only."""
import json
import sys
from pathlib import Path
from sheetaudit.desktop import audit_arguments, execute_job, main, sample_directory

if __name__ == "__main__":
    if len(sys.argv) in (3, 5) and sys.argv[1] == "--smoke-test":
        parent = Path(sys.argv[2]).resolve()
        language = "en"
        if len(sys.argv) == 5:
            if sys.argv[3] != "--language" or sys.argv[4] not in ("en", "zh"):
                raise SystemExit("Use --smoke-test OUTPUT [--language en|zh]")
            language = sys.argv[4]
        result = execute_job(audit_arguments([str(sample_directory())], str(parent), language=language))
        (parent / "desktop-smoke-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        raise SystemExit(result["code"])
    main()
