import boto3
import time
from functions import structure_extract_data

# Initialize AWS Textract Client
textract = boto3.client("textract")

# S3 Bucket and File Name
bucket_name = "extract-document-lcm"
file_name = "Order Sample 2.pdf"

# Start the Textract job
response = textract.start_document_text_detection(
    DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": file_name}}
)

# Get the Job ID
job_id = response["JobId"]
print(f"Job started: {job_id}")

# Function to check job status
def check_job_status(job_id):
    while True:
        response = textract.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        if status in ["SUCCEEDED", "FAILED"]:
            return response
        print("Processing...")
        time.sleep(5)

# Wait for the job to complete
result = check_job_status(job_id)

extracted_text = []
f = open("docs/Order Sample 2.txt", "w")

# Extract and print text
if result["JobStatus"] == "SUCCEEDED":
    for block in result["Blocks"]:
        if block["BlockType"] == "LINE":
            f.write(block["Text"])
            f.write("\n")
            extracted_text.append(block["Text"])
else:
    print("Textract failed!")

f.close()

if extracted_text is not []:
    # Process the extracted text using LangChain
    structured_data = structure_extract_data.extract_invoice_data(extracted_text)
    print(f"Structured Data: {structured_data}")
else:
    print("No data")