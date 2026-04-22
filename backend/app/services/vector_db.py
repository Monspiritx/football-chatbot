import chromadb
from sentence_transformers import SentenceTransformer
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../../data/chroma_db")

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="football_knowledge")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def add_documents(docs: list[dict]):
    ids = [str(i) for i in range(len(docs))]
    texts = [d["text"] for d in docs]
    metadatas = [d.get("metadata", {}) for d in docs]
    embeddings = model.encode(texts).tolist()
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print(f"เพิ่มข้อมูล {len(docs)} รายการเรียบร้อย")

def search(query: str, n_results: int = 3) -> list[str]:
    embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=embedding,
        n_results=n_results,
    )
    if not results["documents"]:
        return []

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    # แนบ source ให้ LLM รู้ว่าข้อมูลมาจากไหน
    enriched = []
    for doc, meta in zip(docs, metadatas):
        source = meta.get("source", "")
        published = meta.get("published", "")
        if source:
            enriched.append(f"[{source}] {doc}")
        else:
            enriched.append(doc)

    return enriched