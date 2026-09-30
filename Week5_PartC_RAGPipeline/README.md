# Week 5 — Part C: RAG Fundamentals (Building the Pipeline by Hand)

## Overview
Retrieval-Augmented Generation (RAG) grounds Large Language Models in verifiable external knowledge. Before querying the model, relevant text chunks are retrieved from a vector database and injected into the prompt as bounded context.

## The 8 Stages of RAG
1. **Document Loading:** Ingesting source texts, documents, or API responses.
2. **Chunking / Text Splitting:** Segmenting documents into overlapping blocks (e.g. 500 chars with 50 chars overlap) so embeddings focus on coherent thoughts.
3. **Embedding:** Generating vector representations for each text chunk using an embedding model.
4. **Vector Storage:** Persisting chunk vectors along with metadata (source document, category, chunk index) into ChromaDB.
5. **Retrieval:** Embedding the user query and retrieving top-$k$ nearest chunks.
6. **Context Construction:** Assembling the retrieved chunks into a strictly bounded prompt with grounding constraints.
7. **Answer Generation:** Sending the prompt to the LLM (temperature = 0).
8. **Source Attribution:** Returning citation metadata alongside the final response.

## Running the Pipeline
```bash
python rag_pipeline.py
```
