import os
import re
from fpdf import FPDF

def generate_pdf(content):
    """Generates a PDF from the travel plan content, stripping non-ASCII characters."""
    # Strip emojis and special characters that FPDF doesn't handle well
    clean_content = re.sub(r'[^\x00-\x7F]+', '', content)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=10)

    lines = clean_content.split("\n")
    for line in lines:
        if line.strip():
            pdf.multi_cell(0, 8, line)
        else:
            pdf.ln(5)

    # Use absolute path in the project root
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(os.path.dirname(base_dir), "travel_plan.pdf")
    
    pdf.output(file_path)
    return file_path