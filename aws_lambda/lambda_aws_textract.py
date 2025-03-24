import json
import time
import boto3

# Initialize AWS Textract client
textract = boto3.client("textract")

def start_textract_job(bucket_name, file_name):
    """Start an asynchronous Textract job for text detection."""
    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": file_name}}
    )
    return response["JobId"]

def check_job_status(job_id):
    """Check the job status and wait until completion."""
    while True:
        response = textract.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]

        if status in ["SUCCEEDED", "FAILED"]:
            return response

        print("Processing... Waiting for 5 seconds")
        time.sleep(5)

def extract_text_from_result(result):
    """Extracts and formats text from Textract response."""
    extracted_text = [
        block["Text"] for block in result.get("Blocks", []) if block["BlockType"] == "LINE"
    ]
    return "\n".join(extracted_text)

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event["body"])
        bucket_name = body.get("bucket")
        file_name = body.get("document")

        if not bucket_name or not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'bucket' or 'document' in request"})
            }

        # Step 1: Start Textract Job
        job_id = start_textract_job(bucket_name, file_name)
        print(f"Textract job started: {job_id}")

        # Step 2: Wait for Textract to complete
        result = check_job_status(job_id)

        if result["JobStatus"] == "SUCCEEDED":
            extracted_text = extract_text_from_result(result)
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Textract job failed!"})
            }

        # Step 3: Return Extracted Data
        return {
            "statusCode": 200,
            "body": json.dumps({"extracted_text": extracted_text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
