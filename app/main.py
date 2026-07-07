from fastapi import FastAPI
from app.database import Base, engine
from app.routers import documents, chat

app = FastAPI(
    title="Intelligent Customer Support AI Assistant",
    description="RAG-based assistant answering queries from company documentation with escalation support.",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)
app.include_router(documents.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "running", "docs": "/docs"}