import os
import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.schema import BaseOutputParser

# Initialize OpenAI API Key (ensure your OpenAI API key is set as an environment variable or manually)
openai.api_key = os.environ['OPENAI_API_KEY']

# Define the Prompt Template for extracting data
invoice_prompt = """
Extract the following information from the given invoice text:
- Invoice Number: (e.g., INV12345)
- Vendor Name: (e.g., ABC Supplies)
- Total Amount: (e.g., 250.75)
- Invoice Date: (e.g., 2025-03-18)

Invoice Text:
{invoice_text}

Output the extracted information in the format:
- Invoice Number: <value>
- Vendor Name: <value>
- Total Amount: <value>
- Invoice Date: <value>
"""

# Define the LangChain prompt template and chain
prompt_template = PromptTemplate(
    input_variables=["invoice_text"],
    template=invoice_prompt
)

llm = OpenAI(temperature=0.5)  # Set the LLM to GPT-3/4 (can adjust temperature for randomness)

chain = LLMChain(prompt=prompt_template, llm=llm)

def extract_invoice_data(invoice_text: str):
    """Extract structured data from the invoice text."""
    result = chain.run({"invoice_text": invoice_text})
    return result
