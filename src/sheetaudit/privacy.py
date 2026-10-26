"""Allowlisted progress statistics; never return source text or user-controlled labels."""
from collections import Counter

CODES = frozenset("""LINE_AMOUNT SUBTOTAL TOTAL NO_TEXT NO_ITEMS NO_ITEMS_ON_PAGE ROW_NUMBER
FIELD_NUMBER UNPARSED_ROW UNMAPPED_TABLE CONFLICTING_FIELD MISSING_DESCRIPTION MISSING_FIELD
CURRENCY_PRECISION OCR_REVIEW AI_REVIEW EVIDENCE_UNVERIFIED COVERAGE_REVIEW DUPLICATE_FILE
PROCESSING_ERROR INHERITED_HEADER""".split())


def private_summary(summary):
    counts = Counter()
    docs = []
    for index, record in enumerate(summary.get("records", []), 1):
        d, a = record["document"], record["audit"]
        for entry in a["issues"]:
            counts[entry["code"] if entry.get("code") in CODES else "OTHER"] += 1
        for check in a["checks"]:
            if check["status"] != "算术一致":
                counts[check["code"] if check.get("code") in CODES else "OTHER"] += 1
        docs.append({"index": index, "pages": int(d["source"]["pages"]), "items": len(d["items"]),
                     "differences": sum(c["status"] == "差异" for c in a["checks"]),
                     "uncheckable": sum(c["status"] == "无法核验" for c in a["checks"]),
                     "open_notices": len(a["issues"]), "resolved_notices": len(a.get("resolved_issues", []))})
    failed = len(summary.get("errors", []))
    if failed:
        counts["PROCESSING_ERROR"] += failed
    return {"schema_version": 1, "documents": len(docs), "failed": failed,
            "pages": sum(d["pages"] for d in docs), "items": sum(d["items"] for d in docs),
            "differences": sum(d["differences"] for d in docs),
            "uncheckable": sum(d["uncheckable"] for d in docs),
            "open_notices": sum(d["open_notices"] for d in docs),
            "resolved_notices": sum(d["resolved_notices"] for d in docs),
            "issue_counts": dict(sorted(counts.items())), "document_stats": docs}
