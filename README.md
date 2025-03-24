# LangChain Sandbox - Document Reconciliation

## Overview

LangChain Sandbox is a document reconciliation tool that leverages Tesseract, AWS Textract, and OpenAI's GPT models to extract and process structured data from invoices and order documents. The system efficiently handles both digital and scanned PDFs, ensuring accurate data extraction and transformation.

## Features

- **AWS Textract Integration**: Extracts text from documents stored in an S3 bucket.
- **OCR Support**: Uses Tesseract OCR for processing scanned PDFs.
- **Structured Data Extraction**: Utilizes LangChain to format extracted text into structured JSON or predefined formats.
- **Automated Processing**: Extracts, transforms, and saves structured data seamlessly.

## Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:

- Python 3.8+
- AWS CLI configured with appropriate permissions
- OpenAI API key
- Required Python packages (see `requirements.txt`)

### 2. Clone the Repository

```sh
git clone https://github.com/hirushiharan/doc_recon_langchain_sandbox.git
```

### 3. Create a Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 4. Install Dependencies

```sh
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file and add your API keys:

```sh
OPENAI_API_KEY="your-openai-api-key"
```

### 6. Run the Application

```sh
python main.py
```

## Project Structure

```
doc_recon_langchain_sandbox/
├── data/                               # Sample documents
│   ├── <sample pdfs>
├── docs/                               # Extracted and structured output files
│   ├── <output text files>
├── functions/
│   ├── extract_tesseract.py            # Extracts text from PDFs
│   ├── structure_extract_data.py       # Uses LangChain for structured extraction
│   ├── extract_aws.py                  # AWS Textract integration
├── aws_lambda/
│   ├── lambda_aws_textract.py          # Lambda function to extract text using AWS Textract
│   ├── lambda_langchain_structure.py   # Lambda function to structure extracted text using LangChain
├── .gitignore                          # Git ignore file
├── .env                                # Environment variables (excluded from Git)
├── aws_main.py                         # Extract & structure document using AWS Textract
├── tesseract_main.py                   # Extract & structure document using Tesseract
├── LICENSE                             # License file
├── README.md                           # Project documentation
└── requirements.txt                    # Required Python libraries
```

## Usage

### Tesseract

1. Upload documents to the `data/` directory.
2. Run `tesseract_main.py` to extract and process the data.
3. Extracted raw text is saved in `docs/`.
4. Structured data is generated and stored in `docs/`.

### AWS Textract

1. Upload documents to the S3 bucket.
2. Run `aws_main.py` to extract and process the data.
3. Extracted raw text is saved in `docs/`.
4. Structured data is generated and stored in `docs/`.

### AWS Lambda

1. **Upload documents to the S3 bucket**  
   - Ensure the S3 bucket has the correct permissions to allow AWS Textract to process the documents.

2. **Create Lambda functions**  
   - Go to the AWS Lambda console and create two Lambda functions:  
     - `lambda_aws_textract.py`: Extracts text using AWS Textract.  
     - `lambda_langchain_structure.py`: Uses LangChain to structure the extracted text.

3. **Add required dependencies using Lambda layers**  
   - AWS Lambda does not come pre-installed with Python libraries. You need to package dependencies separately.  
   - Follow these steps to create a Lambda layer:

   ```sh
   docker pull <AWS_ECR_PYTHON_IMAGE>  # Pull the appropriate Python build from AWS ECR Public
   docker run -it -v $(pwd):/var/task <AWS_ECR_PYTHON_IMAGE>
   pip install langchain langchain-community openai -t ./python
   zip -r lambda_layer.zip python
   ```

   - Upload the `lambda_layer.zip` file as a new AWS Lambda layer.
   - Attach this layer to both Lambda functions.

4. **Configure API Gateway**  
   - Create an API Gateway to expose your Lambda functions as HTTP endpoints.
   - Set up routes for document processing (e.g., `POST /extract`, `POST /structure`).
   - Deploy the API and obtain the endpoint URL.

5. **Invoke the Lambda functions**  
   - Use an HTTP client (Postman, Curl, or a Python script) to call the API Gateway endpoints and get structured text.

## Technologies Used

- **Python**
- **AWS Textract**
- **Tesseract OCR**
- **LangChain**
- **OpenAI API**

## Contribution

Feel free to fork and contribute! Open a pull request with your improvements.

## License

This project is licensed under the MIT License.
