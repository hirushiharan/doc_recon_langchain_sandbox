import boto3
import time
from functions import structure_extract_data

# Initialize AWS Textract Client
textract = boto3.client("textract")

def start_textract_job(bucket_name: str, file_name: str) -> str:
    """
    Starts an AWS Textract text detection job.
    
    Args:
        bucket_name (str): Name of the S3 bucket.
        file_name (str): Name of the file in the bucket.
    
    Returns:
        str: Job ID of the started Textract job.
    """
    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": file_name}}
    )
    return response["JobId"]

def check_job_status(job_id: str) -> dict:
    """
    Checks the status of a Textract job until completion.
    
    Args:
        job_id (str): The Textract job ID.
    
    Returns:
        dict: The response containing job results.
    """
    while True:
        response = textract.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        if status in ["SUCCEEDED", "FAILED"]:
            return response
        print("Processing...")
        time.sleep(5)

def extract_text_from_result(result: dict, output_file: str) -> list:
    """
    Extracts text from the Textract response and saves it to a file.
    
    Args:
        result (dict): The Textract job result.
        output_file (str): Path to the output text file.
    
    Returns:
        list: Extracted text lines.
    """
    extracted_text = []
    with open(output_file, "w") as f:
        if result["JobStatus"] == "SUCCEEDED":
            for block in result["Blocks"]:
                if block["BlockType"] == "LINE":
                    f.write(block["Text"] + "\n")
                    extracted_text.append(block["Text"])
        else:
            print("Textract failed!")
    return extracted_text

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
