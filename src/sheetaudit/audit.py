"""Deterministic arithmetic independent of extraction engine."""
from decimal import Decimal, ROUND_HALF_UP, localcontext
from .model import AMOUNTS, NUMBERS, validate_content, identified_issues, content_hash


def audit_document(doc, tolerance="0.01", places=2):
    validate_content({"fields": doc["fields"], "items": doc["items"]}, doc["source"]["pages"])
    tol = Decimal(tolerance)
    if not tol.is_finite() or tol < 0 or tol > 1000 or places not in range(5):
        raise ValueError("容差须为 0–1000 的有限数；小数位须为 0–4")
    quant = Decimal(1).scaleb(-places)
    checks = []

    def check(code, label, expected=None, observed=None, row=None, note=""):
        with localcontext() as ctx:
            ctx.prec = 50
            exp = expected.quantize(quant, rounding=ROUND_HALF_UP) if expected is not None else None
            delta = observed-exp if observed is not None and exp is not None else None
        checks.append({"code": code, "label": label, "row_id": row.get("row_id") if row else None,
                       "page": row.get("page") if row else None,
                       "expected": str(exp) if exp is not None else None,
                       "observed": str(observed) if observed is not None else None,
                       "delta": str(delta) if delta is not None else None,
                       "status": "无法核验" if delta is None else "差异" if abs(delta) > tol else "算术一致",
                       "note": note})

    with localcontext() as ctx:
        ctx.prec = 50
        for row in doc["items"]:
            q, p, a = (Decimal(row[k]) if row[k] is not None else None for k in NUMBERS)
            check("LINE_AMOUNT", "数量×单价", q*p if q is not None and p is not None else None,
                  a, row, "先按指定小数位四舍五入；差异=原金额−计算金额。行级折扣/税额须人工确认。")
        f = doc["fields"]
        val = {k: Decimal(f[k]) if f[k] is not None else None for k in AMOUNTS}
        complete = bool(doc["items"]) and all(i["amount"] is not None for i in doc["items"])
        line_sum = sum((Decimal(i["amount"]) for i in doc["items"]), Decimal(0)) if complete else None
        check("SUBTOTAL", "明细原金额合计→小计", line_sum, val["subtotal"],
              note="含未解析金额或零行时不核验；提取完整性仍需人工确认。")
        required = ("subtotal", "tax", "discount", "shipping")
        total = val["subtotal"]+val["tax"]-val["discount"]+val["shipping"] if all(val[k] is not None for k in required) else None
        check("TOTAL", "小计+税额−折扣+运费→总计", total, val["total"],
              note="缺失税/折扣/运费不擅自按 0 处理；可人工确认后在修正 JSON 中填 0。")
    issues, resolved = [], []
    review = doc.get("human_review") or {}
    decisions = {entry["issue_id"]: entry for entry in review.get("resolutions", [])}
    current_review = review.get("reviewed_content_sha256") == content_hash(doc)
    for entry in identified_issues(doc):
        decision = decisions.get(entry["issue_id"], {}) if current_review else {}
        coverage_ok = entry["code"] != "COVERAGE_REVIEW" or review.get("coverage_confirmed") is True
        if decision.get("action") == "resolved" and coverage_ok:
            resolved.append({**entry, "resolution_note": decision["note"], "reviewer": review["reviewer"],
                             "reviewed_at": review["reviewed_at"]})
        else:
            issues.append(entry)
    for key in ("document_number", "date", "seller", "buyer", "currency"):
        if not doc["fields"][key]:
            issues.append({"code": "MISSING_FIELD", "message": f"缺少关键字段 {key}", "page": None, "row_id": None})
    currency = doc["fields"]["currency"]
    typical = {"CNY": 2, "USD": 2, "EUR": 2, "GBP": 2, "JPY": 0, "KRW": 0, "KWD": 3, "BHD": 3}
    if currency not in typical or typical[currency] != places:
        issues.append({"code": "CURRENCY_PRECISION", "message": "确认币种及当前金额小数位是否适用", "page": None, "row_id": None})
    if not doc["items"]:
        issues.append({"code": "NO_ITEMS", "message": "零条明细，不能得出单据无差异结论", "page": None, "row_id": None})
    if not review:
        review_status = "待人工复核"
    elif not current_review:
        review_status = "数据已变化或旧版签注，需重新复核（非自动批准）"
    elif not review.get("coverage_confirmed"):
        review_status = "局部复核已记录，完整性未确认（非自动批准）"
    elif issues or any(c["status"] != "算术一致" for c in checks):
        review_status = "复核已记录，仍有待处理项（非自动批准）"
    else:
        review_status = "本次复核完成（非自动批准）"
    return {"checks": checks, "issues": issues, "resolved_issues": resolved, "tolerance": str(tol), "decimal_places": places,
            "rounding": "ROUND_HALF_UP", "differences": sum(c["status"] == "差异" for c in checks),
            "uncheckable": sum(c["status"] == "无法核验" for c in checks),
            "review_status": review_status}
