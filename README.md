# langchain_sandbox
Document reconcilation using Langchain sandbox

1. Backend (Python)
    Framework: FastAPI (lightweight and async support) or Flask (simpler for quick prototyping)
    File Handling: pdfplumber (for PDFs) and pytesseract (for OCR if needed)

2. Database (Local SQL)
    SQLite (easy to set up locally, use SQLAlchemy for ORM)

3. AI & LangChain
    LLM: OpenAI GPT-4
    Vector Database: FAISS (lightweight and runs locally)
    LangChain Components:
    Document Loaders (for extracting text from invoices)
    Text Splitters (to preprocess content)
    Embeddings (store document vectors for similarity search)

4. DevOps
    Docker: For containerizing the app
    GitHub: Version control and project tracking