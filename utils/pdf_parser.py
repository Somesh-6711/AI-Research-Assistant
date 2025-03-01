import pdfplumber

def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF file.
    
    Args:
        pdf_file: Uploaded PDF file.
    
    Returns:
        str: Extracted text.
    """
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text
