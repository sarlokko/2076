#!/usr/bin/env python3
"""Genera un PDF dai capitoli markdown del progetto 2076."""

from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
CAPITOLI = [ROOT / "capitoli" / f"{i:02d}.md" for i in range(1, 15)]
OUTPUT = ROOT / "capitoli" / "2076-capitoli-01-14.pdf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class RomanzoPDF(FPDF):
    def header(self) -> None:
        if self.page_no() > 1:
            self.set_font("DejaVu", "", 9)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, "2076", align="C", new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("DejaVu", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"{self.page_no()}", align="C")


def strip_md_inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def write_paragraph(pdf: RomanzoPDF, text: str, *, bold: bool = False, italic: bool = False) -> None:
    text = strip_md_inline(text.strip())
    if not text:
        return
    style = ""
    if bold:
        style += "B"
    if italic:
        style += "I"
    pdf.set_font("DejaVu", style or "", 11)
    pdf.set_text_color(20, 20, 20)
    pdf.multi_cell(0, 6.5, text)
    pdf.ln(2)


def render_markdown(pdf: RomanzoPDF, content: str) -> None:
    lines = content.splitlines()
    in_quote = False
    quote_lines: list[str] = []

    def flush_quote() -> None:
        nonlocal quote_lines, in_quote
        if not quote_lines:
            return
        pdf.set_font("DejaVu", "", 10.5)
        pdf.set_text_color(60, 60, 60)
        pdf.set_x(pdf.l_margin + 8)
        for q in quote_lines:
            q = strip_md_inline(q.lstrip("> ").strip())
            if q:
                pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 8, 6, q)
        pdf.ln(3)
        quote_lines = []
        in_quote = False

    for raw in lines:
        line = raw.rstrip()

        if line.startswith("> "):
            in_quote = True
            quote_lines.append(line)
            continue
        if in_quote:
            flush_quote()

        if not line.strip():
            pdf.ln(2)
            continue

        if line.startswith("# "):
            pdf.ln(6)
            pdf.set_font("DejaVu", "B", 20)
            pdf.set_text_color(15, 15, 15)
            pdf.multi_cell(0, 10, strip_md_inline(line[2:].strip()))
            pdf.ln(4)
            continue

        if line.startswith("## "):
            pdf.ln(5)
            pdf.set_font("DejaVu", "B", 14)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 8, strip_md_inline(line[3:].strip()))
            pdf.ln(3)
            continue

        if line.strip() == "---":
            pdf.ln(2)
            y = pdf.get_y()
            pdf.set_draw_color(180, 180, 180)
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(5)
            continue

        if line.startswith("— "):
            write_paragraph(pdf, line)
            continue

        write_paragraph(pdf, line)

    if in_quote:
        flush_quote()


def main() -> None:
    pdf = RomanzoPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(22, 22, 22)
    pdf.add_font("DejaVu", "", FONT)
    pdf.add_font("DejaVu", "B", FONT_BOLD)

    pdf.add_page()
    pdf.set_font("DejaVu", "B", 26)
    pdf.ln(40)
    pdf.cell(0, 12, "2076", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("DejaVu", "", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Capitoli 1–13", align="C", new_x="LMARGIN", new_y="NEXT")

    for path in CAPITOLI:
        if not path.exists():
            raise FileNotFoundError(path)
        pdf.add_page()
        render_markdown(pdf, path.read_text(encoding="utf-8"))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))
    print(f"PDF creato: {OUTPUT}")


if __name__ == "__main__":
    main()
