import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def ingest_pdf():
    if not PDF_PATH:
        raise ValueError("PDF_PATH não definido no .env")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não definido no .env")

    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY não definido no .env")

    # 1. Carregar PDF
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    # 2. Dividir em chunks (exigência do edital)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)

    # 3. Embeddings (Gemini)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    # 4. Persistir no Postgres com pgvector
    PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        connection=DATABASE_URL,
        collection_name="pdf_documents"
    )

    print(f"Ingestão concluída. {len(chunks)} chunks salvos no banco.")

if __name__ == "__main__":
    ingest_pdf()
