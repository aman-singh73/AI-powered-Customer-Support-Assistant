---
title: Customer Support AI Backend
emoji: 🦀
colorFrom: blue
colorTo: pink
sdk: docker
pinned: false
---

# Intelligent Customer Support AI Assistant

A full-stack RAG (Retrieval-Augmented Generation) system built to answer user queries based on company documentation. If the system doesn't have enough context or confidence to answer a question, it safely escalates the query to a human agent.

## Tech Stack
* **Frontend**: React + Vite (Vanilla CSS, Glassmorphic UI)
* **Backend**: FastAPI, Python
* **LLM Provider**: Groq (Llama 3.1 8B Instant)
* **Vector Database**: ChromaDB (Local persistent)
* **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Relational Database**: PostgreSQL + SQLAlchemy (For tracking sessions/metadata if needed)
* **Parsers**: pdfplumber, python-docx

---

## Architecture Diagram

Here is a high-level overview of how the data flows through the system during ingestion and chat.

```mermaid
flowchart TD
    User([User])
    UI[React Frontend]
    API[FastAPI Backend]
    
    subgraph Ingestion Pipeline
        Parser[Document Parser\nPDF/DOCX/TXT]
        Chunker[Text Chunker]
        Embedder[SentenceTransformer\nall-MiniLM-L6-v2]
        Chroma[(ChromaDB)]
    end
    
    subgraph Chat Pipeline
        Retriever[Similarity Search]
        Groq[Groq API\nLlama 3.1]
    end
    
    User -- Uploads Doc --> UI
    UI -- POST /documents/upload --> API
    API --> Parser --> Chunker --> Embedder --> Chroma
    
    User -- Asks Question --> UI
    UI -- POST /chat/ --> API
    API --> Embedder
    Embedder -- Encoded Query --> Retriever
    Retriever -- Fetches Context --> Chroma
    Retriever -- Context + History --> Groq
    Groq -- Generated Answer --> API
    API -- JSON Response --> UI
```

---

## Quick Start (Local Development)

### 1. Database Setup
The system requires a running PostgreSQL instance. You can spin one up quickly using Docker:
```bash
docker run --name support-db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=support_db -p 5433:5432 -d postgres:16
```
*(Note: We are mapping to port 5433 locally to avoid conflicts with default Postgres installations)*

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
database_url=postgresql://postgres:postgres@localhost:5433/support_db
groq_api_key=gsk_your_groq_api_key_here
similarity_threshold=0.15
chroma_persist_dir=./chroma_db
top_k_chunks=4
chunk_size=500
chunk_overlap=50
```

### 3. Start the Backend
Open a terminal in the root directory:
```bash
python -m venv venv
source venv\Scripts\activate 
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the Swagger UI at `http://localhost:8000/docs`.

### 4. Start the Frontend
Open a second terminal in the `frontend` directory:
```bash
cd frontend
npm install
npm run dev
```
The React app will be available at `http://localhost:5173`.

---

## API Documentation

### `POST /documents/upload`
Uploads and indexes documents into the knowledge base. Supports `.txt`, `.pdf`, and `.docx`. It automatically extracts hidden hyperlinks (like `mailto:`) from PDFs so contact info is indexed properly.

**Request:**
* Content-Type: `multipart/form-data`
* Body: `files` (Array of files)

**Response:**
```json
{
  "ingested": [
    {
      "file": "company_policy.pdf",
      "chunks_added": 12
    }
  ]
}
```

### `POST /chat/`
Sends a query to the AI assistant. It retrieves relevant chunks from ChromaDB and generates an answer using Groq.

**Request:**
* Content-Type: `application/json`
```json
{
  "session_id": "user-session-123",
  "query": "What is the company refund policy?"
}
```

**Response (Success):**
```json
{
  "answer": "According to the company policy, refunds are processed within 5-7 business days.",
  "escalated": false,
  "confidence": 0.85,
  "sources": ["company_policy.pdf"]
}
```

**Response (Escalated):**
Triggered if the vector search confidence is lower than the `similarity_threshold` set in your `.env`.
```json
{
  "answer": "I don't know the answer to that. I'm escalating this to a human support agent.",
  "escalated": true,
  "confidence": 0.12,
  "sources": []
}
```
