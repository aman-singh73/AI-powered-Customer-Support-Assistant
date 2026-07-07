from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

def chunk_text(text: str, source: str) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_text(text)
    return [{"text": chunk, "source": source, "chunk_id": i} for i, chunk in enumerate(chunks)]