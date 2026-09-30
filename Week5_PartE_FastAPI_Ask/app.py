"""
Week 5 Part E — Adding a /ask Endpoint to the FastAPI Service

Wires the manual RAG pipeline into FastAPI with Pydantic request/response schemas,
graceful error handling, and source attribution.
"""
import os
import chromadb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(
    title="Library Knowledge Assistant API",
    description="FastAPI service with manual RAG pipeline and /ask endpoint",
    version="1.0.0"
)

# -------------------------------------------------------------
# Pydantic Schemas
# -------------------------------------------------------------
class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, example="What books are available on software architecture?")


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


# -------------------------------------------------------------
# ChromaDB Setup & Helper Functions
# -------------------------------------------------------------
chroma_client = chromadb.Client()
try:
    chroma_client.delete_collection("library_ask_demo")
except Exception:
    pass

collection = chroma_client.create_collection("library_ask_demo")

# Seed initial library documents
sample_data = [
    {
        "id": "book-1",
        "text": "Clean Code: A Handbook of Agile Software Craftsmanship by Robert C. Martin. Focuses on writing readable, maintainable, and well-tested code.",
        "meta": {"source": "Clean Code", "category": "Software Engineering"}
    },
    {
        "id": "book-2",
        "text": "Designing Data-Intensive Applications by Martin Kleppmann. Key concepts: distributed systems, transactions, replication, and streaming.",
        "meta": {"source": "Designing Data-Intensive Applications", "category": "Database Architecture"}
    },
    {
        "id": "book-3",
        "text": "The Pragmatic Programmer by David Thomas and Andrew Hunt. Covers pragmatic philosophy, career growth, testing, and modular design.",
        "meta": {"source": "The Pragmatic Programmer", "category": "Software Engineering"}
    }
]

collection.add(
    documents=[item["text"] for item in sample_data],
    metadatas=[item["meta"] for item in sample_data],
    ids=[item["id"] for item in sample_data]
)


def retrieve(question: str, k: int = 3) -> tuple[list[str], list[dict]]:
    results = collection.query(query_texts=[question], n_results=k)
    chunks = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    return chunks, metadatas


def build_prompt(question: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)
    return f"""Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I don't have that information."
Do not use outside knowledge.

Context:
{context}

Question: {question}"""


def call_llm(prompt: str) -> str:
    """Executes call to LLM with fallback simulation."""
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
        # Fallback simulation for local inspection
        return "Simulated response: Verified grounded answer based on catalog data."


# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "library-rag-service"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        chunks, metadatas = retrieve(req.question)
        if not chunks:
            return AskResponse(answer="I don't have that information.", sources=[])

        prompt = build_prompt(req.question, chunks)
        answer = call_llm(prompt)
        sources = sorted(list(set(m["source"] for m in metadatas if "source" in m)))

        return AskResponse(answer=answer, sources=sources)

    except Exception as ex:
        # Prevent server crash on unexpected LLM or retrieval errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing RAG query: {str(ex)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
