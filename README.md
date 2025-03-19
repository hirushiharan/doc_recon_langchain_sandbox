LangChain Sandbox - Document Reconciliation
===========================================

Overview
--------

LangChain Sandbox is a document reconciliation tool that leverages AWS Textract and OpenAI's GPT models to extract and process structured data from invoices and order documents. The system efficiently handles both digital and scanned PDFs, ensuring accurate data extraction and transformation.

Features
--------

*   **AWS Textract Integration**: Extracts text from documents stored in an S3 bucket.
    
*   **OCR Support**: Uses Tesseract OCR for processing scanned PDFs.
    
*   **Structured Data Extraction**: Utilizes LangChain to format extracted text into structured JSON or predefined formats.
    
*   **Automated Processing**: Extracts, transforms, and saves structured data seamlessly.
    

Setup Instructions
------------------

### 1\. Prerequisites

Ensure you have the following installed:

*   Python 3.8+
    
*   AWS CLI configured with appropriate permissions
    
*   OpenAI API key
    
*   Required Python packages (see requirements.txt)
    

### 2\. Clone the Repository

`git clone https://github.com/hirushiharan/doc_recon_langchain_sandbox.git`

### 3\. Create a Virtual Environment

`python -m venv venv  source venv/bin/activate  # On Windows use: venv\Scripts\activate`

### 4\. Install Dependencies

`pip install -r requirements.txt`

### 5\. Configure Environment Variables

Create a .env file and add your API keys:

`OPENAI_API_KEY="your-openai-api-key"`

### 6\. Run the Application

`python main.py`

Project Structure
-----------------
    doc_recon_langchain_sandbox/
        ├── data/
        │   ├── <sample pdfs>
        ├── docs/
        │   ├── <output text files>
        ├── functions/
        │   ├── <output text files>
        │   │   │   ├── extraction.py     # Extracts text from PDFs
        │   │   │   ├── structure_extract_data.py # Uses LangChain for structured extraction
        │   │   │   └── extract_aws.py
        ├── .gitignore
        ├── .env
        ├── main.py
        ├── LICENSE
        ├── README.md
        └── requirements.txt

Usage
-----

1.  Upload documents to the data/ directory or an S3 bucket.
    
2.  Run main.py to extract and process the data.
    
3.  Extracted raw text is saved in docs/.
    
4.  Structured data is generated and stored in docs/.
    

Technologies Used
-----------------

*   **Python**
    
*   **AWS Textract**
    
*   **Tesseract OCR**
    
*   **LangChain**
    
*   **OpenAI API**
    

Contribution
------------

Feel free to fork and contribute! Open a pull request with your improvements.

License
-------

This project is licensed under the MIT License.