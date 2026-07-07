import chromadb
from sentence_transformers import SentenceTransformer
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
collection = client.get_or_create_collection(name="company_knowledge")

def add_chunks(chunks: list[dict]):
    if not chunks:
        return
    texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts).tolist()
    ids = [f"{c['source']}_{c['chunk_id']}" for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]
    collection.upsert(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)
    logger.info(f"Added {len(chunks)} chunks to vector store")

def search(query: str, top_k: int = None) -> list[dict]:
    top_k = top_k or settings.top_k_chunks
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)

    matches = []
    for doc, distance, metadata in zip(
        results["documents"][0], results["distances"][0], results["metadatas"][0]
    ):
        # Chroma returns squared L2 distance by default. For normalized embeddings, 
        # L2_squared = 2 - 2 * cosine_similarity. 
        # Therefore, cosine_similarity = 1 - (distance / 2)
        similarity = 1 - (distance / 2)
        matches.append({"text": doc, "similarity": similarity, "source": metadata.get("source")})
    return matches