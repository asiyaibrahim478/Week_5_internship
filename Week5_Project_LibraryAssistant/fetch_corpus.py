"""
Week 5 Project — Step 1: Build the Corpus from Real Data
Fetches the book catalog from the .NET API (GET /api/books) and formats each book into a text document.
"""
import os
import json
import requests

DOTNET_API_URL = os.getenv("DOTNET_API_URL", "http://localhost:5000/api/books")
OUTPUT_CORPUS_FILE = "corpus.json"

# Fallback seed data matching the SQL Server Library database schema
FALLBACK_BOOKS = [
    {
        "id": 1,
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "category": "Software Engineering",
        "description": "Even bad code can function. But if code isn't clean, it can bring a development organization to its knees. This book presents best practices for writing clean, readable, and maintainable software with meaningful names, small functions, and robust unit testing."
    },
    {
        "id": 2,
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "category": "Database & Distributed Systems",
        "description": "Data is at the center of many challenges in system design today. Difficult issues need to be figured out, such as scalability, consistency, reliability, efficiency, and maintainability. Covers storage engines, replication, partitioning, transactions, and Apache Kafka stream processing."
    },
    {
        "id": 3,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas and Andrew Hunt",
        "category": "Software Engineering",
        "description": "Written as a series of self-contained sections and filled with entertaining anecdotes, thoughtful examples, and interesting analogies, this book illustrates the best approaches and major pitfalls of many different aspects of software development."
    },
    {
        "id": 4,
        "title": "Dune",
        "author": "Frank Herbert",
        "category": "Science Fiction",
        "description": "Set on the desert planet Arrakis, Dune is the story of the boy Paul Atreides, heir to a noble family tasked with ruling an inhospitable world where the only valuable commodity is the spice melange, capable of extending life and enabling interstellar space navigation."
    },
    {
        "id": 5,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "category": "Romance / Classic Literature",
        "description": "A romantic novel of manners following the character development of Elizabeth Bennet, the dynamic protagonist who learns about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness and actual goodness."
    }
]


def fetch_books_from_api() -> list[dict]:
    """
    Calls GET /api/books on .NET API.
    If the .NET API is not currently running locally, falls back to the database-matched corpus.
    """
    try:
        print(f"[FETCH] Requesting book catalog from .NET API: {DOTNET_API_URL} ...")
        resp = requests.get(DOTNET_API_URL, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            print(f"[SUCCESS] Retrieved {len(data)} books directly from .NET API.")
            return data
        else:
            print(f"[WARN] API returned status {resp.status_code}. Using local corpus data.")
            return FALLBACK_BOOKS
    except Exception as ex:
        print(f"[INFO] .NET API not reachable ({ex}). Using local seed catalog.")
        return FALLBACK_BOOKS


def format_book_document(book: dict) -> dict:
    """
    Transforms a single book database record into a standardized document structure.
    """
    title = book.get("title", "Untitled")
    author = book.get("author", "Unknown Author")
    category = book.get("category", book.get("genre", "General"))
    description = book.get("description", "")

    document_text = (
        f"Title: {title}\n"
        f"Author: {author}\n"
        f"Category: {category}\n"
        f"Description: {description}"
    )

    return {
        "id": f"book_{book.get('id', title.lower().replace(' ', '_'))}",
        "text": document_text,
        "metadata": {
            "title": title,
            "author": author,
            "category": category,
            "source": title
        }
    }


def build_and_save_corpus(output_path: str = OUTPUT_CORPUS_FILE) -> list[dict]:
    books = fetch_books_from_api()
    documents = [format_book_document(b) for b in books]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2)

    print(f"[CORPUS] Saved {len(documents)} formatted documents to {output_path}")
    return documents


if __name__ == "__main__":
    docs = build_and_save_corpus()
    for d in docs:
        print(f"\n--- Document ID: {d['id']} ---")
        print(d["text"])
