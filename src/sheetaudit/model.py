"""Strict interchange contract; amounts are decimal strings, never binary floats."""
import hashlib
import json
import re
import unicodedata
from decimal import Decimal, InvalidOperation

FIELDS = ("document_type", "document_number", "date", "seller", "buyer", "currency",
          "subtotal", "tax", "discount", "shipping", "total")
AMOUNTS = ("subtotal", "tax", "discount", "shipping", "total")
NUMBERS = ("quantity", "unit_price", "amount")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def json_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def parse_number(value, locale="en"):
    """Strict en/de separators; refuse exponent/NaN/guessing OCR substitutions."""
    if value is None or str(value).strip() in ("", "-", "—"):
        return None
    s = unicodedata.normalize("NFKC", str(value)).strip()
    s = re.sub(r"^(?:CNY|RMB|USD|EUR|GBP|JPY|[¥$€£])\s*", "", s, flags=re.I)
    s = re.sub(r"\s*(?:元|CNY|RMB|USD|EUR|GBP|JPY)$", "", s, flags=re.I)
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    group, point = (",", ".") if locale == "en" else (".", ",")
    g, p = re.escape(group), re.escape(point)
    if not re.fullmatch(rf"[+-]?(?:\d{{1,3}}(?:{g}\d{{3}})+|\d+)(?:{p}\d+)?", s):
        raise ValueError("无法明确解析数字（分隔符、单位或 OCR 字符需要复核）")
    normalized = s.replace(group, "").replace(point, ".")
    # Bound precision so Decimal calculations and Excel's numeric precision stay useful.
    digits = normalized.lstrip("+-").replace(".", "").lstrip("0")
    if len(digits) > 15 or len(normalized) > 40:
        raise ValueError("数字超过 MVP 支持的 15 位有效数字")
    return format(Decimal(normalized), "f")


def canonical_number(value):
    if value is None:
        return None
    if not isinstance(value, str) or not re.fullmatch(r"-?\d+(?:\.\d+)?", value):
        raise ValueError("JSON 数字必须是无千分位的十进制字符串或 null")
    return parse_number(value)


def validate_content(content, page_count):
    """Validate model/manual output. Reject unknown fields and missing required keys."""
    if not isinstance(content, dict) or set(content) != {"fields", "items"}:
        raise ValueError("提取内容必须且只能包含 fields 和 items")
    fields = content["fields"]
    if not isinstance(fields, dict) or set(fields) != set(FIELDS):
        raise ValueError("fields 必须包含 schema 中的全部字段；未知值填 null")
    for key, value in fields.items():
        if value is not None and (not isinstance(value, str) or len(value) > 2000):
            raise ValueError(f"字段 {key} 必须为短字符串或 null")
        if key in AMOUNTS:
            canonical_number(value)
    items = content["items"]
    if not isinstance(items, list) or len(items) > 10000:
        raise ValueError("items 必须为不超过 10000 行的列表")
    seen = set()
    required = {"row_id", "page", "description", *NUMBERS, "evidence"}
    for row in items:
        if not isinstance(row, dict) or set(row) != required:
            raise ValueError("明细行字段不匹配 schema")
        row_id = row["row_id"]
        if not isinstance(row_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", row_id) or row_id in seen:
            raise ValueError("row_id 必须为唯一的字母数字 ID")
        seen.add(row_id)
        if type(row["page"]) is not int or not 1 <= row["page"] <= page_count:
            raise ValueError("明细页码超出 PDF 范围")
        for key in ("description", "evidence"):
            if not isinstance(row[key], str) or not row[key].strip() or len(row[key]) > 8000:
                raise ValueError(f"明细 {key} 必须为非空短字符串")
        for key in NUMBERS:
            canonical_number(row[key])
    return content


def issue(code, message, page=None, row_id=None):
    return {"code": code, "message": message, "page": page, "row_id": row_id}


def identified_issues(document):
    """Stable within a preserved extraction, including duplicate warning occurrences."""
    return [{**entry, "issue_id": "issue-" + json_hash({"index": index, **entry})[:16]}
            for index, entry in enumerate(document["extraction_issues"])]


def content_hash(document):
    return json_hash({"fields": document["fields"], "items": document["items"]})


def validate_document(document):
    """Validate persisted record metadata before using it in output paths."""
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("不支持的提取记录版本")
    did = document.get("document_id")
    if not isinstance(did, str) or not re.fullmatch(r"d\d{3}_[a-f0-9]{8}", did):
        raise ValueError("提取记录的 document_id 无效")
    source = document.get("source")
    if not isinstance(source, dict) or set(source) != {"file", "sha256", "pages"}:
        raise ValueError("提取记录的 source 无效")
    if not isinstance(source["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", source["sha256"]):
        raise ValueError("提取记录的来源指纹无效")
    if type(source["pages"]) is not int or not 1 <= source["pages"] <= 100:
        raise ValueError("提取记录页数无效")
    if not isinstance(source["file"], str) or len(source["file"]) > 255:
        raise ValueError("提取记录文件名无效")
    validate_content({"fields": document["fields"], "items": document["items"]}, source["pages"])
    if not isinstance(document.get("field_evidence"), dict) or not isinstance(document.get("extraction_issues"), list):
        raise ValueError("提取记录缺少来源证据或提示列表")
    return document
