from functions import extract_tesseract

# Define file paths and bucket details
FILE_PATH = "data/Order Sample 1.pdf"
TEXT_OUTPUT_FILE = "docs/Order Sample 1.txt"
STRUCTURED_OUTPUT_FILE = "docs/Order Sample Invoice 1.txt"

# Start AWS Textract job for document text extraction
extracted_text = extract_tesseract.process_document(FILE_PATH, TEXT_OUTPUT_FILE)

# Process extracted text using LangChain for structured data extraction
extract_tesseract.process_extracted_data(extracted_text, STRUCTURED_OUTPUT_FILE)