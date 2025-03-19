import os
import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

# Set up OpenAI API Key (Ensure the key is set as an environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the prompt template for extracting invoice data
invoice_prompt_template = PromptTemplate(
    input_variables=["invoice_text"],
    template="""
    Extract the following information from the given invoice text:
    - Invoice Number: (e.g., INV12345)
    - Vendor Name: (e.g., ABC Supplies)
    - Total Amount: (e.g., 250.75)
    - Invoice Date: (e.g., 2025-03-18)
    - Services: (e.g.,  Transaction fee - 250.36
                        Basic fee - 185.36)

    Invoice Text:
    {invoice_text}

    Output the extracted information in the format:
    - Invoice Number: <value>
    - Vendor Name: <value>
    - Total Amount: <value>
    - Invoice Date: <value>
    - Services: <list data>
    """
)

# Initialize the LLM model with a moderate temperature for balanced creativity and consistency
llm = OpenAI(temperature=0.5)

# Create the invoice extraction chain
invoice_chain = LLMChain(prompt=invoice_prompt_template, llm=llm)

def extract_invoice_data(invoice_text: str) -> str:
    """
    Extracts structured invoice data from the given invoice text using an LLM.
    
    Args:
        invoice_text (str): The text content of the invoice document.
    
    Returns:
        str: The extracted invoice details in a structured format.
    """
    return invoice_chain.run({"invoice_text": invoice_text})

# Define the prompt template for extracting order sample data
order_prompt_template = PromptTemplate(
    input_variables=["text"],
    template="""
    Extract all relevant details from the given order document text.

    Order Text:
    {text}

    Output the extracted information as a JSON object. Ensure:
    - The keys match the document's terminology.
    - The output remains in valid JSON format.
    - If an expected field is missing, omit it instead of inserting null values.

    Example JSON output:
    {{
        "Order Number": "value_if_available",
        "Contract Number": "value_if_available",
        "Supplier Name": "value_if_available",
        "Buyer": "value_if_available",
        "Payment Terms": "value_if_available",
        "Country of Origin": "value_if_available",
        "Order Total": "value_if_available",
        "Items": [
            {{
                "Item ID": "value_if_available",
                "Description": "value_if_available",
                "Quantity": "value_if_available",
                "Unit Price": "value_if_available"
            }}
        ]
    }}
    
    Include any additional fields present in the document and ensure the output is always valid JSON.
    """
)

# Create the order extraction chain
order_chain = LLMChain(prompt=order_prompt_template, llm=llm)

def extract_order_sample_data(text: str) -> str:
    """
    Extracts structured order details from the given order text using an LLM.
    
    Args:
        text (str): The text content of the order document.
    
    Returns:
        str: The extracted order details formatted as a JSON string.
    """
    return order_chain.run({"text": text})