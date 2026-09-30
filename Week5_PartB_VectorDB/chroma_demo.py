"""
Week 5 Part B — Vector Databases (Chroma)
Demonstrating collection creation, vector addition with metadata, and nearest-neighbor search with metadata filtering.
"""
import chromadb


def run_chroma_demo():
    print("=== Week 5 Part B: Local Vector Database Demo (ChromaDB) ===\n")

    # 1. Initialize an in-memory local Chroma client
    chroma_client = chromadb.Client()

    # 2. Create a collection (Chroma's term for a table / index)
    collection_name = "books_demo"
    # Clean up if existing
    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        pass

    collection = chroma_client.create_collection(name=collection_name)

    # 3. Add documents with metadata and unique identifiers
    documents = [
        "A young wizard attends a magic school and fights a dark lord.",
        "A crew travels through a wormhole to save humanity from a dying Earth.",
        "Two feuding families in 19th century England navigate love and marriage.",
        # Additional practice documents
        "A detective investigates a mysterious murder in a locked room in Victorian London.",
        "A cyberpunk hacker uncovers an AI conspiracy in Neo-Tokyo in the year 2099."
    ]

    metadatas = [
        {"source": "book_1.txt", "category": "Fantasy", "year": 1997},
        {"source": "book_2.txt", "category": "Science Fiction", "year": 2014},
        {"source": "book_3.txt", "category": "Romance", "year": 1813},
        {"source": "book_4.txt", "category": "Mystery", "year": 1887},
        {"source": "book_5.txt", "category": "Science Fiction", "year": 2023}
    ]

    ids = ["book_1", "book_2", "book_3", "book_4", "book_5"]

    print("Adding 5 documents with metadata to Chroma collection...")
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Total documents indexed in '{collection_name}': {collection.count()}\n")

    # 4. Standard semantic query
    query_text = "a space journey story"
    print(f"--- Query 1: Unfiltered Nearest-Neighbor Search for '{query_text}' ---")
    results = collection.query(query_texts=[query_text], n_results=2)

    for i in range(len(results["documents"][0])):
        doc = results["documents"][0][i]
        meta = results["metadatas"][0][i]
        doc_id = results["ids"][0][i]
        dist = results["distances"][0][i] if "distances" in results and results["distances"] else "N/A"
        print(f"  [{i+1}] ID: {doc_id} | Category: {meta['category']} | Text: {doc}")

    # 5. Metadata filtered query (where clause)
    fantasy_query = "a story about battles and destiny"
    print(f"\n--- Query 2: Filtered Search (category == 'Fantasy') for '{fantasy_query}' ---")
    filtered_results = collection.query(
        query_texts=[fantasy_query],
        n_results=2,
        where={"category": "Fantasy"}
    )

    for i in range(len(filtered_results["documents"][0])):
        doc = filtered_results["documents"][0][i]
        meta = filtered_results["metadatas"][0][i]
        print(f"  [{i+1}] ID: {filtered_results['ids'][0][i]} | Category: {meta['category']} | Text: {doc}")

    # 6. Metadata filtered query (category == 'Science Fiction')
    scifi_query = "futuristic technology and space"
    print(f"\n--- Query 3: Filtered Search (category == 'Science Fiction') for '{scifi_query}' ---")
    scifi_results = collection.query(
        query_texts=[scifi_query],
        n_results=2,
        where={"category": "Science Fiction"}
    )
    for i in range(len(scifi_results["documents"][0])):
        doc = scifi_results["documents"][0][i]
        meta = scifi_results["metadatas"][0][i]
        print(f"  [{i+1}] ID: {scifi_results['ids'][0][i]} | Category: {meta['category']} | Text: {doc}")


if __name__ == "__main__":
    run_chroma_demo()
