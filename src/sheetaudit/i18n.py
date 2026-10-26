"""Local presentation languages; canonical records and source evidence stay unchanged."""
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
import json
import os
import re
import tempfile

from .translations import ENGLISH

LANGUAGES = ("en", "zh")
# Preserve programmatic API behavior; CLI and desktop explicitly default to English.
_language = ContextVar("sheetaudit_language", default="zh")
_templates = []
for source, target in ENGLISH.items():
    if re.search(r"\{\d+\}", source):
        parts = re.split(r"(\{\d+\})", source)
        pattern = "".join("(.*?)" if re.fullmatch(r"\{\d+\}", p) else re.escape(p) for p in parts)
        _templates.append((re.compile(pattern, re.DOTALL), target))


def check_language(language):
    if language not in LANGUAGES:
        raise ValueError("Language must be en or zh")
    return language


def current_language():
    return _language.get()


@contextmanager
def use_language(language):
    token = _language.set(check_language(language))
    try:
        yield
    finally:
        _language.reset(token)


def translate(message, language=None):
    """Translate program text only. Never apply this function to source data cells."""
    language = check_language(language or current_language())
    if language == "zh" or not isinstance(message, str):
        return message
    if message in ENGLISH:
        return ENGLISH[message]
    for pattern, target in _templates:
        match = pattern.fullmatch(message)
        if match:
            return target.format(*match.groups())
    return message


def settings_file():
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".config"))
    return base / "SheetAudit" / "settings.json"


def load_language(path=None):
    try:
        value = json.loads(Path(path or settings_file()).read_text(encoding="utf-8"))
        language = value.get("language") if isinstance(value, dict) else None
        return language if language in LANGUAGES else "en"
    except (OSError, ValueError, UnicodeError):
        return "en"


def save_language(language, path=None):
    """Persist only the UI preference, atomically, without customer filenames or data."""
    check_language(language)
    path = Path(path or settings_file())
    temporary = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".settings-", suffix=".json", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump({"language": language}, stream)
            stream.write("\n")
        temporary.replace(path)
        return True
    except OSError:
        return False  # Read-only portable deployments still support in-memory switching.
    finally:
        if temporary is not None and temporary.exists():
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
