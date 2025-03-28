import pdfplumber
import pytesseract
from PIL import Image
import io
import fitz
from functions import structure_extract_data

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file using pdfplumber (for structured PDFs).
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from the PDF, or None if an error occurs.
    """
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
    """
    Performs OCR on scanned PDFs using pytesseract.
    
    Args:
        pdf_path (str): Path to the scanned PDF file.
    
    Returns:
        str: Extracted text from the scanned PDF, or None if an error occurs.
    """
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
    Processes a PDF document:
    - Attempts text extraction using pdfplumber.
    - If extraction fails (indicating a scanned PDF), falls back to OCR.
    
    Args:
        pdf_path (str): Path to the PDF file.
    
    Returns:
        str: Extracted text from the PDF.
    """
    text = extract_text_from_pdf(pdf_path)
    if not text:  # If no text found, assume it's a scanned PDF and use OCR
        print("Fallback to OCR for scanned PDF...")
        text = extract_text_from_scanned_pdf(pdf_path)
    
    return text

def process_extracted_data(extracted_text: list, output_file: str):
    """
    Processes extracted text using LangChain and saves structured data.
    
    Args:
        extracted_text (list): List of extracted text lines.
        output_file (str): Path to the structured data output file.
    """
    if extracted_text:
        structured_data = structure_extract_data.extract_order_sample_data(" ".join(extracted_text))
        with open(output_file, "w") as f:
            f.write(structured_data)
        print(f"Structured Data: {structured_data}")
    else:
        print("No data")