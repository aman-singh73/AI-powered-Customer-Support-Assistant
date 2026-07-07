from groq import Groq
from app.config import settings
from app.rag.vectorstore import search
from app.utils.logger import get_logger

logger = get_logger(__name__)
client = Groq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = """You are a helpful customer support assistant. 
Answer the user's question ONLY using the provided context below. 
If the context does not contain enough information to answer confidently, say "I don't have enough information to answer that." 
Keep answers concise and directly relevant to the question. Do not make up information not present in the context."""

def build_prompt(query: str, context_chunks: list[dict], history: list[dict]) -> list[dict]:
    context_text = "\n\n".join([f"[Source: {c['source']}]\n{c['text']}" for c in context_chunks])
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for turn in history[-3:]:  # last 3 turns for context, keeps prompt size manageable
        messages.append({"role": "user", "content": turn["query"]})
        messages.append({"role": "assistant", "content": turn["answer"]})

    messages.append({
        "role": "user",
        "content": f"Context:\n{context_text}\n\nQuestion: {query}"
    })
    return messages

def get_answer(query: str, history: list[dict]) -> dict:
    chunks = search(query)

    if not chunks or chunks[0]["similarity"] < settings.similarity_threshold:
        logger.info(f"Low confidence for query: '{query}' — escalating")
        return {
            "answer": "I don't know the answer to that. I'm escalating this to a human support agent.",
            "escalated": True,
            "confidence": chunks[0]["similarity"] if chunks else 0.0,
            "sources": [],
        }

    messages = build_prompt(query, chunks, history)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # fast + free tier on Groq
        messages=messages,
        temperature=0.2,
        max_tokens=400,
    )
    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "escalated": False,
        "confidence": chunks[0]["similarity"],
        "sources": list(set(c["source"] for c in chunks)),
    }