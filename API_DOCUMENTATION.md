# API Documentation

This document describes the REST API endpoints available in the Intelligent Customer Support AI Assistant backend.

## Base URL
When running locally, the API is available at: `http://localhost:8000`

---

## 1. Document Upload
Upload and process documents for the knowledge base. The system extracts text, chunks it, generates vector embeddings, and stores them in ChromaDB.

* **URL:** `/documents/upload`
* **Method:** `POST`
* **Content-Type:** `multipart/form-data`

### Request Parameters
* `files`: A list of files to be uploaded. Supported formats are `.pdf`, `.docx`, and `.txt`.

### Success Response
* **Code:** 200 OK
* **Content:**
```json
{
  "ingested": [
    {
      "file": "company_policy.pdf",
      "chunks_added": 15
    },
    {
      "file": "FAQ.txt",
      "chunks_added": 4
    }
  ]
}
```

### Error Responses
* **Code:** 400 Bad Request
* **Content:** `{ "detail": "No files provided." }`

* **Code:** 500 Internal Server Error
* **Content:** `{ "detail": "Error processing document filename.pdf" }`

---

## 2. Chat Interface
Submit a user query to the assistant. The endpoint retrieves relevant context from the knowledge base and generates an AI response. If the confidence threshold is not met, the query is escalated.

* **URL:** `/chat/`
* **Method:** `POST`
* **Content-Type:** `application/json`

### Request Payload
```json
{
  "session_id": "string",
  "query": "string"
}
```
* `session_id`: Unique identifier for the user's conversation to maintain history and context.
* `query`: The question or statement from the user.

### Success Response (Standard Answer)
* **Code:** 200 OK
* **Content:**
```json
{
  "answer": "According to the company policy, refunds take 5-7 business days.",
  "escalated": false,
  "confidence": 0.85,
  "sources": ["company_policy.pdf"]
}
```

### Success Response (Escalated Query)
Triggered when the vector search returns results below the required similarity threshold.
* **Code:** 200 OK
* **Content:**
```json
{
  "answer": "I don't know the answer to that. I'm escalating this to a human support agent.",
  "escalated": true,
  "confidence": 0.12,
  "sources": []
}
```

### Error Responses
* **Code:** 422 Unprocessable Entity
* **Content:** Validation error if the payload is missing required fields.

---

## 3. Health Check
Simple endpoint to verify the API is running.

* **URL:** `/`
* **Method:** `GET`

### Success Response
* **Code:** 200 OK
* **Content:**
```json
{
  "status": "online",
  "message": "Customer Support AI Backend is running"
}
```
