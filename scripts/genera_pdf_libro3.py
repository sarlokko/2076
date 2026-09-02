#!/usr/bin/env python3
"""Genera un PDF dai capitoli markdown del Libro III (Eredità).

Scopre da solo `libro-3/capitoli/NN.md` e scrive
`libro-3/capitoli/eredita-capitoli-01-NN.pdf`.

Uso: python3 scripts/genera_pdf_libro3.py
"""

from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
CAPITOLI_DIR = ROOT / "libro-3" / "capitoli"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_TITLE = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Bold.ttf"


def find_chapters() -> list[Path]:
    paths = sorted(CAPITOLI_DIR.glob("[0-9][0-9].md"))
    if not paths:
        raise FileNotFoundError(f"Nessun capitolo in {CAPITOLI_DIR}")
    return paths


def output_path(chapters: list[Path]) -> Path:
    first = int(chapters[0].stem)
    last = int(chapters[-1].stem)
    return CAPITOLI_DIR / f"eredita-capitoli-{first:02d}-{last:02d}.pdf"


class RomanzoPDF(FPDF):
    header_title = "2076 — Eredità"

    def header(self) -> None:
        if self.page_no() <= 1:
            return
        self.set_font("DejaVu", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, self.header_title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self) -> None:
        if self.page_no() <= 1:
            return
        self.set_y(-15)
        self.set_font("DejaVu", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"{self.page_no() - 1}", align="C")


def strip_md_inline(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    return text


def write_paragraph(pdf: RomanzoPDF, text: str, *, bold: bool = False) -> None:
    text = strip_md_inline(text.strip())
    if not text:
        return
    pdf.set_font("DejaVu", "B" if bold else "", 11)
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

        write_paragraph(pdf, line)

    if in_quote:
        flush_quote()


def add_title_page(pdf: RomanzoPDF, last_chapter: int) -> None:
    pdf.add_page()
    page_w, page_h = pdf.w, pdf.h

    pdf.set_draw_color(30, 30, 30)
    pdf.set_line_width(0.4)
    pdf.rect(18, 18, page_w - 36, page_h - 36)

    pdf.set_y(page_h * 0.28)
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 8, "2076  ·  LIBRO III", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    title_font = "Title" if Path(FONT_TITLE).exists() else "DejaVu"
    pdf.set_font(title_font, "B" if title_font == "DejaVu" else "", 42)
    pdf.set_text_color(15, 15, 15)
    pdf.cell(0, 18, "EREDITÀ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    pdf.set_font("DejaVu", "", 13)
    pdf.set_text_color(70, 70, 70)
    pdf.cell(0, 8, "titolo di lavoro", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(18)

    pdf.set_font("DejaVu", "", 12)
    pdf.set_text_color(40, 40, 40)
    rng = f"Capitoli 1–{last_chapter}" if last_chapter > 1 else "Capitolo 1"
    pdf.cell(0, 8, rng, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "prima stesura", align="C", new_x="LMARGIN", new_y="NEXT")


def main() -> None:
    chapters = find_chapters()
    last = int(chapters[-1].stem)
    dest = output_path(chapters)

    pdf = RomanzoPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(22, 22, 22)
    pdf.add_font("DejaVu", "", FONT)
    pdf.add_font("DejaVu", "B", FONT_BOLD)
    if Path(FONT_TITLE).exists():
        pdf.add_font("Title", "", FONT_TITLE)

    add_title_page(pdf, last)

    for path in chapters:
        pdf.add_page()
        render_markdown(pdf, path.read_text(encoding="utf-8"))

    dest.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(dest))
    print(f"PDF creato: {dest} ({len(chapters)} capitoli)")


if __name__ == "__main__":
    main()
