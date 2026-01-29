# Desafio MBA Engenharia de Software com IA - Full Cycle

## Objetivo
Implementar uma solução de ingestão e busca semântica a partir de um PDF, permitindo consultas via CLI com respostas baseadas exclusivamente no conteúdo do documento.

---

## Tecnologias
- Python
- LangChain
- PostgreSQL + pgVector
- Docker / Docker Compose
- Google Gemini  
  - Embeddings: models/embedding-001  
  - LLM: gemini-2.5-flash-lite  

---

## Estrutura do Projeto
```
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── src/
│   ├── ingest.py
│   ├── search.py
│   ├── chat.py
├── document.pdf
└── README.md
```

---

## Configuração

### Ambiente virtual (Windows)
```bash
python -m venv venv
venv\Scripts\activate.bat
```

### Dependências
```bash
pip install -r requirements.txt
```

### Variáveis de ambiente
Crie o arquivo `.env`:
```env
GOOGLE_API_KEY=SUA_API_KEY_AQUI
GOOGLE_EMBEDDING_MODEL=models/embedding-001
GOOGLE_LLM_MODEL=gemini-2.5-flash-lite

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=pdf_documents

PDF_PATH=document.pdf
```

---

## Execução

### 1. Subir o banco
```bash
docker compose up -d
```

### 2. Ingestão do PDF
```bash
python src/ingest.py
```

### 3. Rodar o chat
```bash
python src/chat.py
```

Perguntas fora do contexto do PDF retornam:
```
Não tenho informações necessárias para responder sua pergunta.
```

---

## Observações
- Chunking: 1000 caracteres com sobreposição de 150.
- Busca semântica: similarity_search_with_score(k=10).
- Respostas limitadas estritamente ao conteúdo do PDF.
