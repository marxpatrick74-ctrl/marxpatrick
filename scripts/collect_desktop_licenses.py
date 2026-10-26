"""Preserve installed dependencies' notices next to a portable distribution."""
import importlib.metadata as metadata
import json
import shutil
import sys
from pathlib import Path
from sheetaudit import __version__


def collect(destination):
    dest = Path(destination)
    notices = dest / "THIRD_PARTY_LICENSES"
    notices.mkdir(parents=True, exist_ok=True)
    packages = ("pdfplumber", "pdfminer.six", "openpyxl", "et_xmlfile", "pypdfium2", "Pillow",
                "cryptography", "cffi", "charset-normalizer", "pycparser", "pyinstaller")
    versions = {}
    for name in packages:
        dist = metadata.distribution(name)
        versions[name] = dist.version
        for entry in dist.files or []:
            if any(word in str(entry).lower() for word in ("license", "licence", "copying", "notice", "authors")):
                path = Path(dist.locate_file(entry))
                if path.is_file():
                    # Flatten unusual metadata paths; no install path leaks in the bundle.
                    target = notices / name / str(entry).replace("/", "_").replace("\\", "_").replace(":", "_")
                    target.parent.mkdir(exist_ok=True)
                    shutil.copyfile(path, target)
    base = Path(sys.base_prefix)
    for source in [base / "LICENSE.txt", *base.glob("tcl/**/license.terms")]:
        if source.is_file():
            target = notices / "Python-Tcl-Tk" / str(source.relative_to(base)).replace("\\", "_").replace("/", "_")
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(source, target)
    (dest / "build-manifest.json").write_text(json.dumps({"app_version": __version__, "python": sys.version.split()[0],
        "platform": "Windows x64", "packages": versions}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    collect(sys.argv[1])
