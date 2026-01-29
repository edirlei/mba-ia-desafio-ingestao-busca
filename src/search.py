import os
from dotenv import load_dotenv

from langchain_postgres import PGVector
from langchain_google_genai import (
    GoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_core.prompts import PromptTemplate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_documents")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_prompt(pergunta: str):
    if not pergunta:
        return None

    # 🔹 Embeddings (OBRIGATÓRIO também na busca)
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY
    )

    # 🔹 Conexão com o banco vetorial
    vectorstore = PGVector(
        connection=DATABASE_URL,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings
    )

    # 🔹 Busca semântica (k=10 – exigência do edital)
    results = vectorstore.similarity_search_with_score(pergunta, k=10)

    if not results:
        contexto = ""
    else:
        contexto = "\n\n".join([doc.page_content for doc, _ in results])

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["contexto", "pergunta"]
    ).format(contexto=contexto, pergunta=pergunta)

    llm = GoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )

    return llm.invoke(prompt)
