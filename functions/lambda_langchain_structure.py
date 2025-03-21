import os
import json
import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

# Set up OpenAI API Key (Ensure the key is set as an environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY')

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
                  "shipVia": "value_if_available", 
                 "mainOrderNo" :  "value_if_available",               
                 "productCode": "value_if_available",
                "styleDescription": "value_if_available",
                "colorCode": "value_if_available",
                 "quantity" : "value_if_available",
              "documentDate":"value_if_available"
 
                  

    Don't Include any additional fields present in the document. Only return the fields mentioned in the above example output. Return the output in JSON format without using square brackets, formatting each row as a separate JSON object. Ensure proper alignment of data for seamless integration. Separate each set by comma and also return the number value in double quotes and without any html tag
    """
)

# Initialize the OpenAI LLM
llm = OpenAI(temperature=0.5)

# Create the order extraction chain
order_chain = LLMChain(prompt=order_prompt_template, llm=llm)

def lambda_handler(event, context):
    try:
        # Parse request body to get the extracted text from previous Lambda
        body = json.loads(event['body'])
        extracted_text = body.get('extracted_text')

        if not extracted_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'extracted_text' in request"})
            }

        # Step 1: Run the extraction using LangChain
        structured_data = order_chain.run({"text": extracted_text})

        # Step 2: Return the structured data as JSON
        return {
            "statusCode": 200,
            "body": json.dumps({"structured_data": structured_data})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }