"""Human corrections are a new version, cryptographically tied to prior extraction."""
from copy import deepcopy
from datetime import datetime
from .model import digest, json_hash, validate_content, validate_document, identified_issues, content_hash


def review_template(document):
    return {"schema_version": 1, "source_sha256": document["source"]["sha256"],
            "base_extraction_sha256": json_hash(document), "reviewer": "", "reviewed_at": "",
            "coverage_confirmed": False, "notes": "",
            "fields": deepcopy(document["fields"]), "items": deepcopy(document["items"]),
            "resolutions": [{"issue_id": entry["issue_id"], "action": "open", "note": ""}
                            for entry in identified_issues(document)]}


def apply_review(original, corrections, source):
    validate_document(original)
    required = {"schema_version", "source_sha256", "base_extraction_sha256", "reviewer", "reviewed_at",
                "coverage_confirmed", "notes", "fields", "items"}
    if set(corrections) not in (required, required | {"resolutions"}) or corrections["schema_version"] != 1:
        raise ValueError("修正文件 schema 不匹配")
    if corrections["source_sha256"] != original["source"]["sha256"] or digest(source) != original["source"]["sha256"]:
        raise ValueError("修正文件与原 PDF 指纹不符")
    if corrections["base_extraction_sha256"] != json_hash(original):
        raise ValueError("原提取结果已变化，请重新生成复核模板")
    for key in ("reviewer", "reviewed_at", "notes"):
        if not isinstance(corrections[key], str) or not corrections[key].strip() or len(corrections[key]) > 8000:
            raise ValueError("复核人、时间和说明必须填写")
    try:
        reviewed_at = datetime.fromisoformat(corrections["reviewed_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("复核时间必须为 ISO 8601，例如 2026-10-24T20:00:00+08:00") from exc
    if reviewed_at.tzinfo is None:
        raise ValueError("复核时间必须带时区")
    if type(corrections["coverage_confirmed"]) is not bool:
        raise ValueError("coverage_confirmed 必须为 true 或 false")
    known = {entry["issue_id"]: entry for entry in identified_issues(original)}
    resolutions = corrections.get("resolutions", [])
    if not isinstance(resolutions, list):
        raise ValueError("resolutions 必须为列表")
    seen = set()
    for resolution in resolutions:
        if not isinstance(resolution, dict) or set(resolution) != {"issue_id", "action", "note"}:
            raise ValueError("问题处理记录格式无效")
        identity = resolution["issue_id"]
        if not isinstance(identity, str) or identity not in known or identity in seen:
            raise ValueError("问题 ID 不存在或重复；不能手动关闭算术差异")
        seen.add(identity)
        if resolution["action"] not in ("open", "resolved"):
            raise ValueError("问题状态必须为 open 或 resolved")
        if not isinstance(resolution["note"], str) or len(resolution["note"]) > 8000:
            raise ValueError("问题处理说明格式无效")
        if resolution["action"] == "resolved":
            if not resolution["note"].strip():
                raise ValueError("关闭提取提示必须填写处理依据")
            if known[identity]["code"] == "COVERAGE_REVIEW" and not corrections["coverage_confirmed"]:
                raise ValueError("未确认完整性时不能关闭完整性复核提示")
    validate_content({"fields": corrections["fields"], "items": corrections["items"]}, original["source"]["pages"])
    updated = deepcopy(original)
    changes = []
    for key in ("fields", "items"):
        if original[key] != corrections[key]:
            changes.append({"section": key, "before": original[key], "after": corrections[key]})
        updated[key] = deepcopy(corrections[key])
    updated["human_review"] = {k: corrections[k] for k in ("reviewer", "reviewed_at", "coverage_confirmed", "notes")}
    updated["human_review"]["base_extraction_sha256"] = json_hash(original)
    updated["human_review"]["changes"] = changes
    updated["human_review"]["resolutions"] = deepcopy(resolutions)
    updated["human_review"]["reviewed_content_sha256"] = content_hash(updated)
    # Avoid presenting superseded PDF text as evidence for corrected header values.
    for key, value in corrections["fields"].items():
        if original["fields"][key] != value:
            updated["field_evidence"].pop(key, None)
    return updated
