"""Generate synthetic, reproducible PDFs. No real business/customer data."""
from pathlib import Path
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "pdfs"
FONT = "Helvetica"


def font_for(text):
    return FONT if any(ord(c) > 255 for c in text) else "Helvetica"


def page(c, title, fields, headers, rows, totals=None, page_number=1, note=""):
    c.setFillColorRGB(.09, .20, .28)
    c.setFont(font_for(title), 23)
    c.drawString(44, 796, title)
    c.setFont(FONT, 10)
    c.setFillColorRGB(.35, .4, .45)
    c.drawString(44, 774, "SYNTHETIC SAMPLE - No real transaction")
    y = 744
    c.setFillColorRGB(.09, .20, .28)
    for label, value in fields:
        c.setFont(font_for(f"{label}: {value}"), 11)
        c.drawString(44, y, f"{label}: {value}")
        y -= 22
    y -= 18
    xs = [44, 310, 382, 464, 550]
    row_height = 34
    top = y
    bottom = y - row_height * (len(rows)+1)
    c.setFillColorRGB(.0, .45, .47)
    c.rect(xs[0], y-row_height, xs[-1]-xs[0], row_height, fill=1, stroke=0)
    for i, row in enumerate([headers]+rows):
        c.setFillColorRGB(1, 1, 1) if i == 0 else c.setFillColorRGB(.09, .20, .28)
        c.setFont(FONT, 11)
        for col, value in enumerate(row):
            c.setFont(font_for(str(value)), 11)
            c.drawString(xs[col]+8, y-22-i*row_height, str(value))
    c.setStrokeColorRGB(.68, .75, .80)
    c.setLineWidth(.5)
    for x in xs:
        c.line(x, bottom, x, top)
    for i in range(len(rows)+2):
        c.line(xs[0], top-i*row_height, xs[-1], top-i*row_height)
    y = bottom - 34
    c.setFont(FONT, 11)
    c.setFillColorRGB(.09, .20, .28)
    for label, value in totals or []:
        c.setFont(font_for(f"{label}: {value}"), 11)
        c.drawString(335, y, f"{label}: {value}")
        y -= 23
    c.setFont(FONT, 10)
    if note:
        c.setFont(font_for(note), 10)
        c.drawString(44, max(100, y-30), note)
    c.setStrokeColorRGB(.7, .75, .8)
    c.line(44, 64, 550, 64)
    c.setFont("Helvetica", 10)
    c.drawString(44, 45, "SheetAudit AI / Demo data only")
    c.drawRightString(550, 45, f"Page {page_number}")
    c.showPage()


def english_fields(number, kind="Invoice"):
    return [("Invoice No" if kind == "Invoice" else "PO No", number), ("Date", "2026-10-24"),
            ("Seller", "Demo Components Ltd"), ("Buyer", "Example Workshop"), ("Currency", "USD")]


def generate():
    OUT.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT / "good_invoice.pdf"), pagesize=(595, 842), invariant=1)
    page(c, "INVOICE", english_fields("INV-DEMO-001"), ["Description", "Quantity", "Unit Price", "Amount"],
         [["Cable A", "3", "12.50", "37.50"], ["Adapter B", "2", "10.00", "20.00"]],
         [("Subtotal", "57.50"), ("Tax", "5.75"), ("Discount", "0.00"), ("Shipping", "0.00"), ("Total", "63.25")])
    c.save()
    c = canvas.Canvas(str(OUT / "discrepancy_invoice.pdf"), pagesize=(595, 842), invariant=1)
    page(c, "INVOICE", english_fields("INV-DEMO-002"),
         ["Description", "Quantity", "Unit Price", "Amount"], [["Paper A4", "3", "12.50", "42.50"], ["Folder", "2", "10.00", "20.00"]],
         [("Subtotal", "62.50"), ("Tax", "5.00"), ("Discount", "0.00"), ("Shipping", "0.00"), ("Total", "67.50")],
         note="Demo: first line exceeds quantity x unit price by 5.00.")
    c.save()
    c = canvas.Canvas(str(OUT / "purchase_order_multipage.pdf"), pagesize=(595, 842), invariant=1)
    for n in (1, 2):
        page(c, "PURCHASE ORDER", english_fields("PO-DEMO-003", "PO"),
             ["Description", "Quantity", "Unit Price", "Amount"],
             [["Identical legitimate line", "2", "15.00", "30.00"]],
             [("Subtotal", "60.00"), ("Tax", "0.00"), ("Discount", "0.00"), ("Shipping", "0.00"), ("Total", "60.00")] if n == 2 else [],
             page_number=n, note="Both identical rows are intentional; do not deduplicate.")
    c.save()
    c = canvas.Canvas(str(OUT / "unsupported_invoice.pdf"), pagesize=(595, 842), invariant=1)
    page(c, "INVOICE", english_fields("INV-DEMO-004"), ["Description", "Quantity", "Unit Price", "Amount"],
         [["OCR-like ambiguous quantity", "O2", "10.00", "20.00"], ["Missing unit price", "1", "", "8.00"]],
         [("Subtotal", "28.00"), ("Total", "28.00")], note="Missing adjustments are unknown, not automatically zero.")
    c.save()
    image = Image.new("RGB", (1190, 1684), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 27) if Path("C:/Windows/Fonts/arial.ttf").exists() else ImageFont.load_default(size=27)
    lines = ["INVOICE - SYNTHETIC SCANNED SAMPLE", "Invoice No: INV-SCAN-005", "Date: 2026-10-24",
             "Seller: Demo Scan Ltd", "Buyer: Example Workshop", "Currency: USD", "",
             "Description | Quantity | Unit Price | Amount", "Cable | 2 | 10.00 | 20.00", "",
             "Subtotal: 20.00", "Tax: 0.00", "Discount: 0.00", "Shipping: 0.00", "Total: 20.00",
             "", "Image-only PDF. Local OCR or manual entry required."]
    for i, line in enumerate(lines):
        draw.text((80, 100+i*65), line, fill="#183349", font=font)
    c = canvas.Canvas(str(OUT / "scanned_invoice.pdf"), pagesize=(595, 842), invariant=1)
    c.drawImage(ImageReader(image), 0, 0, 595, 842)
    c.showPage()
    c.save()
    print(f"Generated 5 synthetic PDFs in {OUT}")


if __name__ == "__main__":
    generate()
