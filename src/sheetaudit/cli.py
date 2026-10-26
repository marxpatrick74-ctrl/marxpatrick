import argparse
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

from . import __version__
from .audit import audit_document
from .extract import extract_document
from .model import digest, issue
from .report import write_report
from .review import apply_review, review_template
from .review_excel import write_review_workbook, read_review_workbook
from .privacy import private_summary
from .benchmark import evaluate_manifest


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path):
    if path.stat().st_size > 20_000_000:
        raise ValueError("JSON 超过 20 MB")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def collect(inputs):
    paths = []
    for raw in inputs:
        path = Path(raw)
        if path.is_dir():
            paths.extend(sorted((p for p in path.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"), key=lambda p: p.name))
        elif path.is_file() and path.suffix.lower() == ".pdf":
            paths.append(path)
        else:
            raise ValueError("输入必须为现有 PDF 或包含 PDF 的目录")
    paths = list(dict.fromkeys(p.resolve() for p in paths))
    if not paths or len(paths) > 100:
        raise ValueError("单批须包含 1–100 个 PDF；目录只扫描一层")
    return paths


def build_parser():
    parser = argparse.ArgumentParser(description="SheetAudit AI — 本地 PDF 提取与金额核对")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="提取 PDF 并生成 Excel/JSON 报告")
    audit.add_argument("inputs", nargs="+", help="PDF 文件或目录")
    audit.add_argument("--engine", choices=("rules", "ollama"), default="rules")
    audit.add_argument("--model", help="已安装的 Ollama 本地模型名；不下载模型")
    audit.add_argument("--ollama-port", type=int, default=11434)
    audit.add_argument("--number-format", choices=("en", "de"), default="en", help="en: 1,234.56；de: 1.234,56")
    audit.add_argument("--ocr", action="store_true", help="只对少文字页面运行本地 Tesseract")
    audit.add_argument("--ocr-language", default="eng", help="如 chi_sim+eng；须已安装语言包")
    audit.add_argument("--tesseract", default="tesseract", help="本机 Tesseract 可执行文件路径")
    review = sub.add_parser("review", help="应用人工修正，验证原 PDF 指纹，输出新版本")
    review.add_argument("extracted", type=Path)
    review.add_argument("--corrections", type=Path, required=True)
    review.add_argument("--source", type=Path, required=True)
    summary = sub.add_parser("summary", help="只输出匿名统计，不显示文件名、金额、原文或签注")
    summary.add_argument("report_dir", type=Path, help="包含 summary.json 的报告目录")
    benchmark = sub.add_parser("benchmark", help="对带人工标注和指纹的样本进行规则提取验证")
    benchmark.add_argument("manifest", type=Path)
    benchmark.add_argument("--out", type=Path, required=True, help="新的验证结果 JSON 文件")
    for cmd in (audit, review):
        cmd.add_argument("--out", type=Path, required=True, help="新的输出目录；拒绝覆盖已有目录")
        cmd.add_argument("--tolerance", default="0.01", help="绝对差异≤容差视为算术一致（默认 0.01）")
        cmd.add_argument("--decimal-places", type=int, choices=range(5), default=2)
        cmd.add_argument("--fail-on-issues", action="store_true", help="存在差异、无法核验或待复核提示时返回 1")
    review.set_defaults(tolerance=None, decimal_places=None)
    return parser


def run(args, progress=None, announce=print):
    if args.command == "benchmark":
        if args.out.exists():
            raise ValueError("验证结果文件已存在，请选择新文件")
        result = evaluate_manifest(read_json(args.manifest), args.manifest.parent)
        dump(args.out, result)
        announce(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result["failed"] else 0
    if args.command == "summary":
        safe = private_summary(read_json(args.report_dir / "summary.json"))
        announce(json.dumps(safe, ensure_ascii=False, indent=2))
        return 0
    original = read_json(args.extracted) if args.command == "review" else None
    if original is not None:
        policy = original.get("audit_policy", {})
        args.tolerance = args.tolerance if args.tolerance is not None else policy.get("tolerance", "0.01")
        args.decimal_places = args.decimal_places if args.decimal_places is not None else policy.get("decimal_places", 2)
    tolerance = Decimal(args.tolerance)
    if not tolerance.is_finite() or not 0 <= tolerance <= 1000:
        raise ValueError("容差须为 0–1000 的有限十进制数")
    if args.out.exists():
        raise ValueError("输出目录已存在；请选择新目录以保留历史报告")
    paths = collect(args.inputs) if args.command == "audit" else []
    if args.command == "audit" and args.engine == "ollama" and not args.model:
        raise ValueError("Ollama 模式需要 --model 指定已安装本地模型")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".sheetaudit-", dir=args.out.parent))
    records, errors, source_paths = [], [], {}
    try:
        if args.command == "audit":
            for idx, path in enumerate(paths, 1):
                if progress:
                    progress(idx - 1, len(paths), "正在读取和提取")
                did = f"d{idx:03d}"
                try:
                    doc, pages = extract_document(path, engine=args.engine, number_format=args.number_format,
                        ocr=args.ocr, language=args.ocr_language, tesseract=args.tesseract,
                        model=args.model, port=args.ollama_port)
                    did += "_" + doc["source"]["sha256"][:8]
                    doc["document_id"] = did
                    dump(staging / "documents" / did / "source.json", {"source": doc["source"], "pages": pages})
                    records.append({"document": doc, "audit": None})
                    source_paths[did] = path
                except Exception as exc:
                    # Do not leak document text, endpoint response bodies or absolute paths to logs.
                    message = str(exc) if isinstance(exc, ValueError) and exc.__class__ is ValueError else "读取/提取失败，请检查文件、PDF 加密或本地 OCR/模型依赖"
                    errors.append({"document_id": did, "file": path.name, "error_type": type(exc).__name__, "message": message})
                if progress:
                    progress(idx, len(paths), "已完成提取")
            fingerprints = {}
            for record in records:
                d = record["document"]
                fingerprints.setdefault(d["source"]["sha256"], []).append(d)
            for docs in fingerprints.values():
                if len(docs) > 1:
                    for d in docs:
                        d["extraction_issues"].append(issue("DUPLICATE_FILE", "批次内存在内容完全相同的 PDF；保留每份，避免误删合法记录"))
        else:
            corrections = (read_review_workbook(args.corrections, original) if args.corrections.suffix.lower() == ".xlsx"
                           else read_json(args.corrections))
            doc = apply_review(original, corrections, args.source)
            records.append({"document": doc, "audit": None})
            source_paths[doc["document_id"]] = args.source
            target = staging / "documents" / doc["document_id"]
            # Only a known sibling name is copied, never paths supplied inside JSON.
            evidence_file = args.extracted.parent / "source.json"
            if evidence_file.exists():
                evidence = read_json(evidence_file)
                if evidence["source"]["sha256"] != doc["source"]["sha256"]:
                    raise ValueError("source.json 的来源指纹不符")
                dump(target / "source.json", evidence)
            dump(target / "before-review.json", original)
            dump(target / "review-applied.json", corrections)
            if args.corrections.suffix.lower() == ".xlsx":
                shutil.copyfile(args.corrections, target / "review-applied.xlsx")
        if progress:
            progress(len(paths), len(paths), "正在核算并生成 Excel")
        for record in records:
            d = record["document"]
            d["audit_policy"] = {"tolerance": str(args.tolerance), "decimal_places": args.decimal_places}
            record["audit"] = audit_document(d, args.tolerance, args.decimal_places)
            target = staging / "documents" / d["document_id"]
            dump(target / "extracted.json", d)
            dump(target / "audit.json", record["audit"])
            dump(target / "review-template.json", review_template(d))
            write_review_workbook(d, target / "review.xlsx", source_paths.get(d["document_id"]))
        summary = {"version": __version__, "created_at": datetime.now(timezone.utc).isoformat(),
                   "documents": len(records), "failed": len(errors),
                   "differences": sum(r["audit"]["differences"] for r in records),
                   "uncheckable": sum(r["audit"]["uncheckable"] for r in records),
                   "review_notices": sum(len(r["audit"]["issues"]) for r in records),
                   "resolved_notices": sum(len(r["audit"]["resolved_issues"]) for r in records),
                   "tolerance": args.tolerance, "decimal_places": args.decimal_places,
                   "records": records, "errors": errors}
        write_report(records, errors, staging / "report.xlsx")
        dump(staging / "summary.json", summary)
        dump(staging / "privacy-summary.json", private_summary(summary))
        # Rename within the same filesystem: never replace an existing successful run.
        staging.rename(args.out)
        announce(f"报告已生成：成功 {len(records)}，失败 {len(errors)}，差异 {summary['differences']}，无法核验 {summary['uncheckable']}，待复核提示 {summary['review_notices']}。")
        announce("输出：report.xlsx；每份单据的 documents 子目录包含可编辑 review.xlsx。")
        if errors:
            return 2
        return 1 if args.fail_on_issues and (summary["differences"] or summary["uncheckable"] or summary["review_notices"]) else 0
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except (ValueError, OSError, InvalidOperation, KeyError, TypeError) as exc:
        # Expected argument/schema errors only; unexpected programmer errors retain traceback.
        message = str(exc) if type(exc) is ValueError else "参数、文件或 JSON schema 无效；请参照 README 和 review-template.json"
        print("SheetAudit: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
