# Week 5 Project — Library Knowledge Assistant (RAG)

## Overview
This project builds a RAG-powered `/ask` endpoint that answers questions about the library's book catalog using the live data from the .NET API as the single source of truth.

---

## Complete Data Flow Architecture

```
+------------------+
|   SQL Server     |
| (Library DB)     |
+--------+---------+
         |
         v
+------------------+
|   .NET 8 API     |  (GET /api/books - Public Endpoint)
+--------+---------+
         |
         v
+------------------+
| fetch_corpus.py  |  (Formats Title, Author, Category, Description)
+--------+---------+
         |
         v
+------------------+
| vector_store.py  |  (chunk_text -> OpenAI / Chroma Embeddings -> ChromaDB Collection)
+--------+---------+
         |
         v
+------------------+
| FastAPI /ask     |  (Retrieves top-k chunks -> Injects into Grounded Prompt)
+--------+---------+
         |
         v
+------------------+
| LLM (Claude /    |  (Strictly answers using context only or says "I don't have that info")
| GPT-4o-mini)     |
+--------+---------+
         |
         v
+------------------+
| JSON Response    |  {"answer": "...", "sources": ["Clean Code", ...]}
+------------------+
```

---

## Project Structure & Files

1. `fetch_corpus.py`: Fetches catalog from `http://localhost:5000/api/books` (with resilient local seed fallback if .NET API is offline) and writes `corpus.json`.
2. `vector_store.py`: Splits documents into chunks (350 chars with 40-char overlap), embeds them, and stores them in ChromaDB with metadata (`source`, `category`, `chunk_index`).
3. `main.py`: Exposes `POST /ask` with request/response validation, grounded prompt assembly, and source attribution.
4. `test_grounding.py`: Automated test suite testing 3 in-catalog queries and 1 out-of-catalog query to verify zero hallucination.

---

## Running the Project

### 1. Fetch the Corpus & Build the Vector Store
```bash
python fetch_corpus.py
python vector_store.py
```

### 2. Launch FastAPI Server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Run Grounding Tests
```bash
python test_grounding.py
```

### 4. Interactive Swagger Documentation
Navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
