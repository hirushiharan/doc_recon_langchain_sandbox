from functions import extraction, structure_extract_data

pdf_file = "data\sample-invoice.pdf"
extracted_text = extraction.process_document(pdf_file)

if extracted_text is not None:
    # Process the extracted text using LangChain
    structured_data = structure_extract_data.extract_invoice_data(extracted_text)

    print("Structured Data:\n", structured_data)

else:
    print("No data")