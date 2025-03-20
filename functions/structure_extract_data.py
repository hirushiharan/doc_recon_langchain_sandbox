import os
import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

# Set up OpenAI API Key (Ensure the key is set as an environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize the LLM model with a moderate temperature for balanced creativity and consistency
llm = OpenAI(temperature=0.5)

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
    - Map fields dynamically as follows:
    - "Fabric Code" → "Product Code" in product details.
    - "CC" → "Color Code" in product details.
    - "Department" → "Style Description" in product details.
    - "Ship Via" → "Mode of Transport" in order details.

    Example JSON output:
    {{
        "Ship Via": "value_if_available",
        "Items": [
            {{
                "Product Code": "value_if_available",
                "Style Description": "value_if_available",
                "Color Code": "value_if_available"
            }}
        ]
    }}

    Don't Include any additional fields present in the document. Only return the fileds mentioned in the above example output. And ensure the output is always valid JSON.

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