# AI Microservice (FastAPI + LLM Prompt Engineering)

**Author:** Asiya  
**Service:** Library AI Microservice  
**Framework:** FastAPI + Uvicorn + Pydantic

---

## Overview
This service provides AI-powered literary analysis, structured book summaries, and genre classification for the Library Management ecosystem.

> [!NOTE]
> As per Week 4 architecture specifications, the .NET Web API and this Python FastAPI AI service operate as independent microservices. The direct service-to-service orchestration is integrated in Week 6.

---

## Features
- **Pydantic Validation:** Strict request/response data contracts with automatic validation and error reporting.
- **Engineered Prompts:** Zero-Shot, Few-Shot, and Role-Based structured output prompts.
- **Error Resilience:** Protected JSON extraction, sanitization of markdown fences, and fallback handling.
- **Prompt Injection Defense:** Input isolation within boundary tags to treat user input strictly as data.
- **Interactive API Docs:** Automatic Swagger UI at `http://localhost:8000/docs`.

---

## How to Run

### 1. Prerequisites & Virtual Environment
```bash
# Navigate to the ai-service directory
cd ai-service

# Create and activate virtual environment (optional but recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Test Endpoints

#### Health Check:
```bash
curl -X GET http://localhost:8000/health
```

#### Summarize & Classify:
```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "description": "A dystopian novel exploring government surveillance and mind control in Oceania."}'
```

#### Interactive Documentation:
Open your browser and visit: `http://localhost:8000/docs`
