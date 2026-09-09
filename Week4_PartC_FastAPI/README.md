# Week 4 — Part C: FastAPI Foundations (Python AI Backend)

**Author:** Asiya  
**Project:** AI Backend Microservice (`ai-service`)

## Overview
Part C transitions Python AI capabilities from standalone CLI scripts to a production-ready asynchronous API service built with **FastAPI** and **Uvicorn**.

### Key Concepts
1. **FastAPI Web Framework:**
   - High-performance, asynchronous REST framework built on Starlette and Pydantic.
   - Automatically generates interactive OpenAPI / Swagger documentation at `/docs` and ReDoc at `/redoc`.
2. **Pydantic Data Validation:**
   - Enforces strict data types and schema contracts on request bodies and responses.
   - Automatically returns HTTP 422 Unprocessable Entity with detailed error diagnostics on invalid JSON structures.
3. **Path Operations:**
   - Clean route decorators: `@app.get("/health")`, `@app.post("/summarize")`, `@app.post("/genre-suggestion")`.

---

## How to Run the FastAPI Service
```bash
cd ai-service
# Activate virtual environment if configured
# pip install fastapi uvicorn pydantic requests
uvicorn main:app --reload --port 8000
```
Visit the interactive Swagger UI at: `http://localhost:8000/docs`
