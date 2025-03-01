from fpdf import FPDF
import os

def save_summary_as_pdf(title: str, summary: str):
    """
    Save a research summary as a PDF file.

    Args:
        title (str): The title of the research paper.
        summary (str): The summary text.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="", size=12)

    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)  # Line break
    pdf.multi_cell(0, 8, summary)

    save_path = f"data/processed/{title.replace(' ', '_')}.pdf"
    pdf.output(save_path)

    return save_path  # Return path for UI to show download link

# Example Usage
if __name__ == "__main__":
    pdf_path = save_summary_as_pdf("Deep Learning in NLP", "This paper discusses NLP techniques using deep learning models...")
    print(f"PDF saved at: {pdf_path}")
