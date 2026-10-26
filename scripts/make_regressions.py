"""Synthetic regression PDFs: distinct layouts, no customer data."""
from pathlib import Path
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parents[1] / "examples" / "regressions"
HEADER = ["Description", "Quantity", "Unit Price", "Amount"]


def draw(c, number, rows, *, framed=True, header=True, totals=None, shift=0):
    c.setFont("Helvetica-Bold", 20)
    c.drawString(42, 795, "SYNTHETIC REGRESSION INVOICE")
    c.setFont("Helvetica", 10)
    for y, text in zip(range(770, 650, -20), ["No real customer or transaction data", "Invoice No: " + number,
                     "Date: 2026-10-25", "Seller: Test Supplier", "Buyer: Demo Buyer", "Currency: USD"]):
        c.drawString(42, y, text)
    xs = [42+shift, 290+shift, 370+shift, 455+shift, 550+shift]
    all_rows = ([HEADER] if header else []) + rows
    top = 620
    for i, row in enumerate(all_rows):
        for j, text in enumerate(row):
            c.drawString(xs[j]+6, top-i*32-22, str(text))
    if framed:
        for x in xs:
            c.line(x, top, x, top-len(all_rows)*32)
        for i in range(len(all_rows)+1):
            c.line(xs[0], top-i*32, xs[-1], top-i*32)
    if totals is not None:
        for i, (name, value) in enumerate([("Subtotal", totals), ("Tax", "0.00"), ("Discount", "0.00"), ("Shipping", "0.00"), ("Total", totals)]):
            c.drawString(360, top-len(all_rows)*32-35-i*22, f"{name}: {value}")
    c.drawString(42, 35, "SheetAudit AI / synthetic regression only")
    c.showPage()


def generate():
    OUT.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT / "shipping_product.pdf"), pagesize=(595, 842), invariant=1)
    draw(c, "REG-01", [["Cable", "2", "10.00", "20.00"], ["Shipping labels", "3", "5.00", "15.00"],
                      ["Adapter", "1", "8.00", "8.00"]], totals="43.00")
    c.save()
    c = canvas.Canvas(str(OUT / "continuation_grid.pdf"), pagesize=(595, 842), invariant=1)
    draw(c, "REG-02", [["Cable", "2", "10.00", "20.00"]])
    draw(c, "REG-02", [["Adapter", "1", "8.00", "8.00"]], header=False, totals="28.00")
    c.save()
    c = canvas.Canvas(str(OUT / "borderless.pdf"), pagesize=(595, 842), invariant=1)
    draw(c, "REG-03", [["Cable", "2", "10.00", "20.00"], ["Adapter", "1", "8.00", "8.00"]], framed=False, totals="28.00")
    c.save()
    c = canvas.Canvas(str(OUT / "continuation_borderless.pdf"), pagesize=(595, 842), invariant=1)
    draw(c, "REG-04", [["Cable", "2", "10.00", "20.00"]], framed=False)
    draw(c, "REG-04", [["Adapter", "1", "8.00", "8.00"]], framed=False, header=False, totals="28.00")
    c.save()
    print("Generated 4 synthetic regression PDFs")


if __name__ == "__main__":
    generate()
