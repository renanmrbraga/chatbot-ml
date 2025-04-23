# utils/export_utils.py
from typing import Optional
import pandas as pd
import io
import base64

from fpdf import FPDF


def exportar_csv_base64(df: pd.DataFrame) -> str:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return base64.b64encode(buffer.read().encode("utf-8")).decode("utf-8")


def exportar_pdf_base64(
    df: pd.DataFrame, titulo: Optional[str] = "Comparação entre cidades"
) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, titulo, ln=True, align="C")

    pdf.set_font("Arial", "", 10)
    col_width = 60
    row_height = 8

    cols = list(df.columns)
    for col in cols:
        pdf.cell(col_width, row_height, str(col), border=1)
    pdf.ln()

    for _, row in df.iterrows():
        for col in cols:
            texto = str(row[col])[:30]
            pdf.cell(col_width, row_height, texto, border=1)
        pdf.ln()

    # Correção da geração do PDF em memória
    pdf_bytes: bytes = pdf.output(dest="S").encode("latin1")
    return base64.b64encode(pdf_bytes).decode("utf-8")
