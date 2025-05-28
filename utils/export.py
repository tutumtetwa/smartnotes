from reportlab.pdfgen import canvas

from fpdf import FPDF
import os
import uuid

def export_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)

    filename = f"output_{uuid.uuid4().hex}.pdf"
    filepath = os.path.join("static", filename)
    pdf.output(filepath)
    return filepath


def export_txt(text):
    file_path = 'output.txt'
    with open(file_path, 'w') as f:
        f.write(text)
    return file_path
