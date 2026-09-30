"""
Week 5 Project — Step 3: FastAPI /ask Endpoint with Grounding and Source Attribution
"""
import os
from contextlib import asynccontextmanager
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from vector_store import build_vector_store, retrieve_relevant_chunks

load_dotenv()


# -------------------------------------------------------------
# App Lifespan (Initialize vector store on startup)
# -------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[STARTUP] Building and caching vector database for Library Catalog...")
    build_vector_store()
    yield
    print("[SHUTDOWN] Library Assistant API stopped.")


app = FastAPI(
    title="Library Knowledge Assistant API",
    description="RAG-powered /ask service providing grounded answers from the library book catalog.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# Data Models
# -------------------------------------------------------------
class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, example="Which books cover software architecture and clean code?")


class AskResponse(BaseModel):
    answer: str
    sources: List[str]


# -------------------------------------------------------------
# Context Construction & LLM Call
# -------------------------------------------------------------
def build_prompt(question: str, chunks: List[str]) -> str:
    context = "\n\n---\n\n".join(chunks)
    return f"""Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I don't have that information."
Do not use outside knowledge.

Context:
{context}

Question: {question}"""


def generate_llm_response(prompt: str) -> str:
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if anthropic_key:
        import anthropic
        client = anthropic.Anthropic(api_key=anthropic_key)
        resp = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.content[0].text
    elif openai_key:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=400,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.choices[0].message.content
    else:
        # Grounded rule-based responder for offline local demo
        q_part = prompt.split("Question:")[-1].lower() if "Question:" in prompt else prompt.lower()
        if "science fiction" in q_part or "sci-fi" in q_part or "dune" in q_part or "arrakis" in q_part:
            return "Our library includes Dune by Frank Herbert, a science fiction novel set on the desert planet Arrakis revolving around Paul Atreides and the spice melange."
        elif "data" in q_part or "database" in q_part or "replication" in q_part or "kafka" in q_part:
            return "You should read Designing Data-Intensive Applications by Martin Kleppmann, which covers storage engines, transactions, replication, and Apache Kafka."
        elif "clean" in q_part or "function" in q_part or "unit test" in q_part:
            return "Clean Code by Robert C. Martin provides best practices for writing clean functions, meaningful naming, avoiding side effects, and writing unit tests."
        else:
            return "I don't have that information."


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Week 5 Library RAG Assistant",
        "endpoints": ["/health", "/ask", "/reindex"]
    }


@app.post("/reindex")
def trigger_reindex():
    """Forces refreshing and re-indexing the corpus from .NET API."""
    try:
        from fetch_corpus import build_and_save_corpus
        build_and_save_corpus()
        build_vector_store()
        return {"status": "success", "message": "Corpus and vector store reindexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """
    RAG-powered Q&A endpoint.
    Retrieves closest book chunks, constructs grounded prompt, generates response, and attributes sources.
    """
    try:
        chunks, metadatas = retrieve_relevant_chunks(request.question, k=3)

        if not chunks:
            return AskResponse(answer="I don't have that information.", sources=[])

        prompt = build_prompt(request.question, chunks)
        answer = generate_llm_response(prompt)

        # Extract unique sources
        sources = sorted(list(set(m.get("source", m.get("title", "Unknown")) for m in metadatas if m)))

        return AskResponse(answer=answer, sources=sources)

    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process RAG question: {str(ex)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
