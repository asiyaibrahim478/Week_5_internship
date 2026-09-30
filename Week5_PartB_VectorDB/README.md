# Week 5 — Part B: Vector Databases

## Overview
Comparing a query embedding against every single vector one-by-one using a standard Python `for` loop works for a small toy dataset (e.g. 10 items), but cannot scale to thousands or millions of documents. A **Vector Database** indexes embeddings using Approximate Nearest Neighbor (ANN) algorithms to find closest matches in sub-linear time (e.g. HNSW indexing).

## Core Concepts
1. **Vector Storage:** Each record stores an embedding vector, the raw original text chunk, and arbitrary JSON metadata (such as document source, title, category, creation date).
2. **Nearest-Neighbor Query (ANN):** Given a query embedding, returns the $k$ closest items based on cosine distance or euclidean distance.
3. **Metadata Filtering:** Allows combining structured filter conditions (e.g. `where={"category": "Fantasy"}`) with semantic vector search.
4. **Vector DB Landscape:**
   - *Local / Embedded (Ideal for learning & testing):* ChromaDB, FAISS.
   - *Hosted / Production-Grade:* Pinecone, Qdrant, Weaviate, Milvus, pgvector.

## How to Run
```bash
pip install chromadb
python chroma_demo.py
```

## Practice Takeaways
- Chroma automatically handles embedding generation using its built-in sentence transformer model if no custom embedding function is passed, or can be configured to use OpenAI / custom embeddings.
- Metadata filters (`where={...}`) prune the search space to only consider candidate chunks matching the specified criteria.
