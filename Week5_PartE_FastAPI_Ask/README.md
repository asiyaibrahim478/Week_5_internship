# Week 5 — Part E: Adding /ask Endpoint to FastAPI Service

## Overview
This section wires the manual RAG pipeline built in Parts C & D directly into a FastAPI microservice, exposing a clean HTTP `POST /ask` endpoint.

## Request & Response Format

### Request Body (`POST /ask`)
```json
{
  "question": "What books are available on software architecture?"
}
```

### Response Body (`200 OK`)
```json
{
  "answer": "Designing Data-Intensive Applications by Martin Kleppmann is available, covering distributed systems, replication, and data architecture.",
  "sources": [
    "Designing Data-Intensive Applications"
  ]
}
```

## Running & Interactive Testing
1. Start the server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
2. Open Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. Test `/ask` with valid questions and verify that `sources` correctly outputs the book titles.
