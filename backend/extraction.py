import pdfplumber
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file using pdfplumber (for structured PDFs)."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text with pdfplumber: {e}")
        return None

def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    """Perform OCR on scanned PDFs using pytesseract."""
    text = ""
    try:
        doc = fitz.open(pdf_path)  # Open the PDF
        for page_num in range(len(doc)):
            img = doc[page_num].get_pixmap()  # Convert page to image
            img_pil = Image.open(io.BytesIO(img.tobytes("png")))  # Convert to PIL image
            text += pytesseract.image_to_string(img_pil) + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text with OCR: {e}")
        return None

def process_document(pdf_path: str) -> str:
    """
    Process a PDF document:
    - First, try extracting text using pdfplumber.
    - If extraction fails (possible scanned PDF), fallback to OCR.
    """
    text = extract_text_from_pdf(pdf_path)
    if not text:  # If no text found, assume it's a scanned PDF and use OCR
        print("Fallback to OCR for scanned PDF...")
        text = extract_text_from_scanned_pdf(pdf_path)
    
    return text
