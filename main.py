from functions import extraction, structure_extract_data, extract_aws

# Define file paths and bucket details
BUCKET_NAME = "extract-document-lcm"
FILE_NAME = "Order Sample 1.pdf"
TEXT_OUTPUT_FILE = "docs/Order Sample 1.txt"
STRUCTURED_OUTPUT_FILE = "docs/Order Sample Invoice 1.txt"

# Start AWS Textract job for document text extraction
job_id = extract_aws.start_textract_job(BUCKET_NAME, FILE_NAME)
print(f"Job started: {job_id}")

# Check job status and retrieve results
result = extract_aws.check_job_status(job_id)
extracted_text = extract_aws.extract_text_from_result(result, TEXT_OUTPUT_FILE)

# Process extracted text using LangChain for structured data extraction
extract_aws.process_extracted_data(extracted_text, STRUCTURED_OUTPUT_FILE)