import os, shutil
from fastapi import APIRouter, UploadFile, File
from typing import List
from app.ingestion.loaders import load_document
from app.ingestion.chunker import chunk_text
from app.rag.vectorstore import add_chunks
from app.utils.logger import get_logger

router = APIRouter(prefix="/documents", tags=["Knowledge Base"])
logger = get_logger(__name__)

UPLOAD_DIR = "kb_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_documents(files: List[UploadFile] = File(...)):
    ingested = []
    for file in files:
        try:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            text = load_document(file_path, file.filename)
            chunks = chunk_text(text, source=file.filename)
            add_chunks(chunks)
            ingested.append({"file": file.filename, "chunks_added": len(chunks)})
        except Exception as e:
            logger.error(f"Failed to ingest {file.filename}: {e}")
            continue
    return {"ingested": ingested}